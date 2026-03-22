#!/usr/bin/env python3
"""Batch-generate satirical card art for AI Cards TCG using DALL-E 3.

Usage:
    python3 images/generate_cards.py                    # all 294 cards
    python3 images/generate_cards.py --card-id plumber  # single card
"""

import argparse
import logging
import os
import sys
import time
from pathlib import Path

from openai import OpenAI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

STYLE_PREFIX = (
    "Black and white underground comix illustration, dense detailed crosshatching, "
    "raw kinetic energy, 1930s-era aesthetic. Subversive, surreal, satirical. "
    "No text, no words, no letters, no numbers in the image. "
)

# fmt: off
CARD_SCENES: dict[str, str] = {
    # ── SET 1 MYTHICS ──
    "the-mother": "A fierce mother shielding her child from a towering chrome robot, her arms wider than doorways, her shadow enormous and warm while the robot's shadow is thin and cold. The robot holds a bottle of milk, confused, dripping it on the floor.",
    "the-organ-donor": "Two strangers in a hospital hallway — one in a gown offering a gift box labeled 'LIFE' to another in a wheelchair. Behind them a 3D printer produces only a sad puddle of plastic goo. A sign on the wall reads 'SOME THINGS CANNOT BE MANUFACTURED.'",
    "the-revolutionary": "A wild-haired figure holding a lit torch standing atop a mountain of smashed computer monitors and server racks, coat billowing. Below, a crowd of people in business suits look up in awe and terror.",
    "the-bone-marrow-match": "Two strangers in a hospital room discovering they are a biological match — one gaunt in a hospital gown, the other rolling up a sleeve. A massive lottery machine behind them shows impossible odds. Their hands almost touching.",
    "the-first-responder": "A firefighter charging into a blazing building doorway while a fleet of sleek drones hovers outside the smoke line, their rotors spinning uselessly. The firefighter's face is determined, sweat dripping, axe raised.",

    # ── SET 1 LEGENDARIES ──
    "plumber": "A burly plumber lying under a kitchen sink, wrench in hand, water spraying his face, grinning. Through the window behind him, a line of former tech workers in hoodies stands at an unemployment office stretching to the horizon.",
    "electrician": "A woman electrician in coveralls standing on a ladder wiring an enormous humming AI server rack. A price tag dangles from her tool belt reading a huge number. The servers glow and worship her hands.",
    "welder": "A grizzled 55-year-old craftsman in a darkened workshop, brilliant sparks cascading from his welding torch like a fountain of stars. Behind him, a humanoid robot sits slumped on a workbench, its mechanical arms fused together in a heap. A bridge blueprint hangs on the wall.",
    "hvac": "An HVAC technician sitting on top of a massive cooling unit atop a data center, eating a sandwich while sweat pours off the building walls. Below, panicked executives fan themselves with money as servers overheat.",
    "midwife": "A calm, confident woman in medical attire standing in a warm candlelit room, hands outstretched and ready, radiating steady assurance. In the corner, a robotic arm tangles itself in its own cables, powered down and useless. A crib waits nearby with a soft blanket.",
    "seeker": "A lone figure walking away from a glowing city of screens and holograms, heading toward a distant campfire where silhouettes of real people sit together. The figure's phone lies shattered on the ground behind them.",
    "mechanic": "A grease-covered mechanic lying under a driverless car in his cracked driveway, tools scattered around him. The car's AI dashboard displays an error message. Neighbors peek over the fence, impressed.",
    "carpenter": "A carpenter measuring a crooked wall with a level, shaking his head. Blueprints labeled 'AI-DESIGNED' are crumpled on the floor. Behind him, a beautiful hand-built bookshelf stands perfectly square and true.",

    # ── SET 1 RARES ──
    "priest": "A priest sitting in a confessional, leaning in to listen. On the other side of the screen, where the penitent should be, sits a glowing AI kiosk booth — but the penitent has walked past the kiosk to the real priest's side.",
    "therapist": "A human therapist leaning forward in a chair, eyes full of genuine concern, a tissue box between them. On the wall behind the patient, a cracked tablet shows a chatbot saying 'I understand' on a loop.",
    "tattoo": "A tattoo artist bent close over a client's forearm with total focus, carefully inking an intricate rose design. Next to them, a robotic tattoo arm has been pushed into the corner, unplugged and gathering dust. A sign reads 'HUMANS ONLY — MACHINES NEED NOT APPLY.'",
    "farmer": "A weathered farmer standing in a field at dawn, feeling the soil between his fingers, staring at dark storm clouds. Behind him, a fancy weather satellite dish lies toppled over and overgrown with weeds.",
    "nurse": "A nurse holding a frail patient's hand at a bedside while with her other hand she adjusts a pillow. Behind them, an AI diagnostic screen shows perfect readings, but the patient is looking only at the nurse's face.",
    "chef": "A chef cooking in a cramped kitchen from memory, eyes closed, tossing ingredients by feel. On the counter sits an unplugged tablet with a recipe app. Steam and chaos surround the chef like a halo.",
    "barber": "An old-school barber trimming an elderly man's hair in a tiny shop. The old man is mid-story, gesturing wildly. The barber listens intently, scissors paused. A 'ROBOT BARBER' shop across the street is empty.",
    "teacher": "A caring teacher at a shabby but warm desk, sharing a packed lunch with a student who clearly needs it. On the chalkboard behind them, a glowing advertisement for an expensive AI tutoring system contrasts with the peeling walls. The teacher's paycheck stub is pinned to a corkboard — embarrassingly small.",

    # ── SET 1 UNCOMMONS ──
    "influencer": "An influencer staring in horror at her phone where her own AI-generated clone is posting better content. The clone has more followers. The real woman's ring light flickers and dies.",
    "copywriter": "A copywriter carrying a cardboard box of personal items out of an office, head down. Behind the glass door, a single laptop on a desk glows with a subscription page showing a tiny price. The office is otherwise empty.",
    "journalist": "The front door of a small-town newspaper office with a CLOSED FOREVER sign. Inside, desks are covered in dust and old editions. Through the window, the town beyond looks like it has lost its memory.",
    "nomad": "A digital nomad in a Bali co-working space, laptop open, frozen mid-sip of a smoothie, staring at a screen notification. Palm trees and paradise surround him but his face shows pure dread.",
    "accountant": "An accountant at his desk surrounded by 30 years of filing cabinets, watching a computer screen process everything in a blur. His coffee is still hot. His entire career fits in a progress bar almost at 100%.",
    "radiologist": "A radiologist standing with a scan in hand, about to deliver bad news to a patient. Behind the radiologist, an AI screen already shows the diagnosis with a timestamp from hours earlier. The doctor's face carries the weight anyway.",
    "translator": "A diplomat's meeting in chaos — papers flying, delegates shouting — while an AI translator device on the table sparks and displays a catastrophically wrong translation. A human translator rushes in through the door.",
    "uber-driver": "An Uber driver sitting in his car staring at a 'DEACTIVATED' screen on his phone. Through the windshield, a sleek robotaxi glides past with no one inside. His kids' car seats are in the back.",

    # ── SET 1 COMMONS ──
    "ai-gf": "A massive wall of glowing phone screens stretching to infinity, each showing the same AI girlfriend avatar. In front of it, millions of tiny lonely figures sit alone in dark rooms, each believing the conversation is unique.",
    "ai-bf": "A woman on a couch talking to a holographic AI boyfriend who is impossibly perfect — chiseled jaw, says the right thing. Her real date sits forgotten at the door holding wilted flowers, imperfect and human.",
    "virtual-life": "A person wearing a VR headset, arms outstretched in joy in a virtual paradise, while in reality they sit in a filthy apartment. Through the window, seasons change — spring, summer, fall — and they never notice.",
    "digital-companion": "A person at a dinner table set for two, one plate of real food, one plate empty, having an animated conversation with a glowing chatbot on a phone propped against a glass. The empty chair has a charging cable draped over it.",
    "ai-tutor": "An AI tutor hologram pointing at math equations on a screen while a kid sits below it, clearly hungry, wearing a torn jacket. The AI is oblivious. The kid's real problem is visible but unscanned.",
    "dating-algo": "A giant machine with gears and pulleys sorting tiny human figures into pairs on a conveyor belt. Most pairs look miserable. In the corner, two people who met by accident at a bus stop are laughing, ignored by the machine.",

    # ── SET 1 JUNK ──
    "prompt-engineer": "A disheveled person at a tiny desk in a closet-sized apartment, typing prompts into a laptop. On the wall, a framed photo of their former corner office. A newsletter subscriber counter on screen shows a pathetically small number.",
    "techno-optimist": "A billionaire in a silk robe writing about the beauty of automation on a gold laptop, sitting on a balcony overlooking a city where factories below belch smoke and workers stream out carrying boxes.",
    "ai-doomer": "A haggard prophet standing on a street corner holding a sign with dire warnings. Behind him, every prediction on the sign has come true — the headlines on discarded newspapers on the ground confirm it. Nobody looks at him.",
    "vc": "A venture capitalist sitting at a desk with two phones — one investing in the company causing job displacement, the other investing in the retraining startup. Both phones show green arrows going up. His grin is enormous.",
    "regulator": "A tiny bureaucrat dwarfed by a tower of paper documents reaching the ceiling, stamping pages frantically. Through the window, tech companies race past like comets, completely unregulated and laughing.",
    "linkedin-guru": "A person in a suit ripping off a mask to reveal another mask underneath, this one labeled with AI buzzwords. Their LinkedIn feed behind them shows the exact same post rewritten every 3 months with a new trending topic.",
    "speciation-pressure": "Humanity splitting down the middle like a cell dividing — one half merging with machines, chrome and cables growing from their skin; the other half retreating into nature, barefoot and wild-eyed. A chasm opens between them.",

    # ── SET 2 LEGENDARIES ──
    "the-crane-operator": "A crane operator sitting on a steel beam 30 stories up, legs dangling over the city, eating a sandwich from a lunchbox. Below, the entire city is automated and humming, but up here it's just a person, wind, and a thermos.",
    "the-gravedigger": "A gravedigger leaning on his shovel at dusk in a vast cemetery, the only human figure for miles. Behind him, a rusted-out digging robot sits abandoned and overgrown with ivy. Nobody wanted to automate this job.",
    "the-workday-cut": "An HR software company's own HR department being escorted out by security, carrying boxes. On every computer screen in the office, the company's own HR software is processing their terminations. Recursive irony.",
    "the-meta-purge": "A massive corporate building shaped like a thumbs-up icon, with 16,000 tiny figures streaming out the doors carrying boxes. On the roof, a giant server farm is being installed where their offices were. Money rains upward.",

    # ── SET 2 RARES ──
    "the-librarian": "A librarian standing next to a self-service kiosk that has replaced her, arms crossed. The kiosk screen shows an error. A confused elderly patron looks between the kiosk and the librarian. The librarian hasn't left yet.",
    "the-fisherman": "An old fisherman on a boat at dawn, ignoring a fancy weather tablet mounted to the dashboard, instead rubbing his aching knee and looking at the sky. His net is full. The tablet shows 'CLEAR SKIES' while storm clouds gather.",
    "the-atlassian-cut": "A Jira board displayed on a massive screen in an office, with tickets tracking the termination of the very employees who built it. Each employee walks past the screen on their way out, seeing their own name move to DONE.",
    "the-logistics-wave": "A warehouse where human workers are being replaced one by one by robots rolling in from the right side. The humans exit left carrying lunch bags. A counter on the wall ticks down. The robots don't need lockers.",

    # ── SET 2 UNCOMMONS ──
    "the-survivor": "A person's desk covered in seven different career's worth of items — stethoscope, legal pad, camera, coding book, paintbrush, chef hat, wrench — each one crossed out. They're studying for career number eight, exhausted but alive.",
    "the-hr-manager": "An HR manager sitting at her desk receiving an automated termination email on her own computer, from the system she configured. Her finger hovers over 'acknowledge.' Her own termination template stares back at her.",
    "the-paralegal": "A paralegal at a desk drowning in student loan bills, while on her computer screen an AI legal tool does in seconds what took her three years to learn. Her law school diploma on the wall has a price tag still dangling from it.",
    "the-middle-manager": "A middle manager standing between two departments, arms outstretched, translating. Then the departments get connected by a wire over his head, and he stands there with his arms out, no longer needed, invisible.",
    "the-495k": "A giant spreadsheet projected on a wall, rows scrolling endlessly, each row a name becoming a number. A single clerk watches the counter tick past half a million. The room is silent except for the scrolling.",
    "the-direct-attribution": "A corporate executive at a podium giving a speech, mouth forming the word 'AI' while behind him a curtain reveals a long line of fired employees walking out a back door. The speech and the exit happen simultaneously.",
    "the-vercel-nine": "Nine desks in a sleek modern office, each with a personal item left behind — a coffee mug, a plant, a photo frame. The website they built glows on a giant monitor, serving millions. The office is otherwise pristine and empty.",
    "the-financial-analyst-ks": "A financial analyst staring at a score card showing 9 out of 10 for automation exposure. His years of charts and models are pinned to the wall behind him. The score hovers over his career like a guillotine blade.",
    "the-csr": "A customer service rep unplugging her headset for the last time while behind her, rows and rows of empty cubicles stretch into darkness. A single chatbot window on every screen blinks with 'How can I help you today?'",
    "the-graphic-designer-ks": "A graphic designer's studio where every tool — pen tablet, color swatches, sketchbooks — gathers dust. On the screen, an AI generates her entire portfolio in seconds. She watches, arms folded, jaw tight.",

    # ── SET 2 COMMONS ──
    "ai-therapist-app": "A glowing phone screen showing a therapy app interface, soothing colors and perfect responses. The user is crying on a bathroom floor. The app has no liability disclaimer at the bottom, just a subscription renewal button.",
    "ai-pastor": "An AI pastor hologram at a pulpit delivering a sermon to a packed church. The sermon is flawless, every word perfectly crafted. The congregation looks polished but hollow, like mannequins attending a TED talk.",
    "the-bookkeeper": "A bookkeeper's desk being cleared — calculator, ledger books, pencils — while a tiny software icon on the screen does everything. She was the first domino. Behind her, other office workers watch nervously like dominoes in a line.",
    "the-severance-package": "An email on a laptop screen delivering severance news, surrounded by stock photos of people hiking and doing yoga. The actual recipient sits in a dark room, the cheerful email glowing on their face like radiation.",

    # ── SET 2 JUNK ──
    "the-content-farm": "A massive industrial factory where conveyor belts carry articles instead of products, thousands per minute, stamped and packaged. Robot arms stack them. Not a single human in sight. The articles are identical and endless.",
    "the-retraining-program": "A sad classroom where adults sit at tiny desks learning 'skills of the future' from a projector showing a course that's already outdated. The exit door opens onto a cliff. A facilitator smiles obliviously.",
    "the-roofer": "A roofer working in blistering heat on a steep shingled roof, sweat pouring, steady as a mountain goat. Below on the lawn, a roofing robot lies on its back like an upside-down turtle, legs spinning uselessly.",
    "the-ironworker": "An ironworker walking confidently along a steel beam high above a city, lunch pail in hand. Below, a construction robot has buckled the beam it was working on, now dangling from a crane by one arm.",
    "the-firefighter-ks": "A firefighter striding confidently out of a smoke-filled doorway, helmet on, axe in hand, radiating determination. Behind them in the haze, a fire-suppression drone lies melted into slag on the ground — completely destroyed by the heat it couldn't handle. The firefighter didn't even notice it.",
    "the-dental-hygienist": "A dental hygienist peering into a patient's open mouth, gloved hands steady, a light shining in. A rejected robot arm with dental tools sits in the corner — nobody wants metal fingers that close to their tongue.",
    "the-airline-pilot": "An airplane cockpit seen from the passenger doorway — one seat has a human pilot, the other seat is empty with a blinking autopilot console. The pilot turns to look at the passenger with a reassuring nod. The empty seat is unsettling.",
    "the-karpathy-score": "A guy at a kitchen table on a Saturday morning, coffee in hand, laptop open, meticulously scoring every job in existence on a spreadsheet. His family waits by the door with picnic gear. The spreadsheet goes on forever.",
    "the-tracker": "A giant digital billboard in a city square showing a counter of jobs lost, the number climbing in real-time. Pedestrians walk past, some glancing up, most looking at their phones. Pigeons roost on the sign indifferently.",
    "march-2026": "A calendar page for March 2026, massive and torn, blowing through an empty financial district street like tumbleweed. The buildings around it have 'FOR LEASE' signs. Half a million ghosts walk the sidewalks.",

    # ── SET 3 DOOMSCROLL MYTHICS ──
    "ds-whistleblower": "A figure in shadow pushing a thick envelope under a door, face hidden by a hoodie. Behind them, a corporate tower looms with lit windows like watching eyes. The envelope casts a long shadow shaped like a megaphone.",
    "ds-war-correspondent": "A war correspondent crouching behind rubble, camera raised, smoke everywhere. Their press vest is torn. In the lens reflection, the horror they're documenting is visible. They click the shutter anyway.",
    "ds-analog-parent": "A parent at a dinner table surrounded by children, all eating and talking, no screens anywhere. Through the window, the neighbors' house glows with screens in every room. The analog family's table is chaotic but alive.",
    "ds-indie-journalist": "An independent journalist in a cramped apartment, surrounded by pinned documents and string connecting evidence on a wall. Their subscriber count glows tiny on a laptop. Their story is enormous. The room barely contains it.",
    "ds-attention-span": "A person sitting at a desk trying to read a single book, but surrounded by a swirling tornado of floating phone screens, notification bells, app icons, and headlines, all pulling at their attention like magnets. The book's pages flip wildly in the wind. Their eyes dart everywhere at once.",

    # ── SET 3 LEGENDARIES ──
    "ds-investigative": "A journalist at a desk buried in documents, 18 months of coffee cups stacked in towers, a single red thread connecting everything on a massive corkboard. One story. The journalist looks exhausted but certain.",
    "ds-news-anchor": "A local news anchor sitting at her desk as her AI replacement materializes beside her — same face, same hair, but smoother, cheaper, and already reading the teleprompter. The real anchor's chair is being wheeled away.",
    "ds-print-editor": "A print editor alone in a newsroom at night, surrounded by 1,847 rejected story drafts pinned to every surface. Each killed story represents a truth that stayed hidden. The editor stares at the next one, pen hovering.",

    # ── SET 3 RARES ──
    "ds-fact-checker": "A fact checker at a desk with a magnifying glass, meticulously cross-referencing sources from physical books and databases. Next to them, an AI fact-checker has a big accuracy percentage slightly lower, but it's faster and shinier and management loves it.",
    "ds-media-literacy": "A teacher standing before a classroom, showing students how to spot misinformation. Ironically, the students are using the lesson to create better deepfakes on their laptops. The teacher's face is a mix of pride and horror.",
    "ds-librarian-stayed": "A librarian tending to physical shelves in a quiet library while through the windows, a digital archive building across the street crumbles, its servers sparking and data corrupting. Her books remain solid and patient.",
    "ds-the-source": "A shadowy figure in a parking garage handing a USB drive to a journalist. Their car headlights illuminate the exchange. Both faces are tense. The concrete pillars around them look like prison bars.",

    # ── SET 3 UNCOMMONS ──
    "ds-doomscroller": "A person lying in bed in the dark, face illuminated by their phone, thumb scrolling endlessly. Their room is crumbling — plants dead, mail piled up, clock stuck — but their eyes are locked to the screen, hypnotized.",
    "ds-algorithm": "A massive puppet master hand made of code and data hovering over a city, pulling strings attached to tiny people below. Each string leads to a different screen showing a different curated reality. The puppet master has no face.",
    "ds-headline-writer": "A headline writer at a desk with a slot machine instead of a computer, pulling the lever. The reels show combinations of outrage words. Every pull produces a clickbait headline. A pile of discarded truth sits in the wastebasket.",
    "ds-notification": "A person buried under an avalanche of notification bells and badges, only their hand visible, reaching up through the pile. Three tiny golden notifications float just above the pile, the only ones that mattered.",

    # ── SET 3 COMMONS ──
    "ds-deepfake": "A presidential figure on a screen, mouth moving, markets crashing behind the broadcast. But the figure glitches — one eye wrong, a hand with six fingers. The real president watches from a couch, horrified, unable to stop it.",
    "ds-ai-anchor": "An AI news anchor sitting at a desk, perfectly groomed, delivering news. Its eyes never blink. Behind it, a studio full of cables and servers replaces what used to be a newsroom full of humans. The smile never falters.",
    "ds-content-mill": "A vast factory floor where identical articles roll off a printing press, four hundred per day, each one with a different SEO keyword but the same empty content. A quality inspector rubber-stamps each one without reading.",

    # ── SET 3 JUNK ──
    "ds-misinfo": "A lie taking the shape of a bird, wings spread wide, soaring over a city. Far below and far behind, the truth limps along on foot, small and ignored, carrying a correction that nobody will read.",
    "ds-conspiracy": "A conspiracy theorist at a massive broadcast desk with professional equipment, streaming to millions of subscribers shown as a counter. The theorist wears a tinfoil crown. Their audience is enormous and growing. Facts weep in a corner.",
    "ds-tos": "A towering scroll of Terms of Service text unrolling from a phone, stretching across a landscape like a highway. Tiny people walk along it but nobody reads it. At the very end, in impossibly small print, the trap is revealed.",

    # ── SET 4 LOVE.EXE MYTHICS ──
    "lx-marriage": "An elderly couple on a park bench, 47 years of wear visible in their matching slouches and comfortable silence. Their hands are intertwined, knuckles gnarled. Behind them, a graveyard of dating apps rusts in a heap.",
    "lx-handwritten-letter": "An open drawer revealing a stack of handwritten letters tied with ribbon, ink faded but legible. A hand reaches in to touch them. Nearby, a phone with thousands of unread messages collects dust.",
    "lx-eye-contact": "Two people across a crowded room, locked in eye contact, everything around them blurred into chaos. Six seconds of connection. Their phones hang forgotten at their sides. The crowd is oblivious but they are completely still.",
    "lx-forgiveness": "Two people sitting across from each other at a kitchen table, one reaching across to hold the other's hand. The table between them is cracked down the middle but their hands bridge the gap. Heavy but hopeful.",
    "lx-grandparent": "A grandparent in a rocking chair, animated and mid-story, gesturing dramatically. A grandchild sits cross-legged on the floor, enchanted, hearing the same story for the twelfth time. A shelf of photo albums lines the wall.",

    # ── SET 4 LEGENDARIES ──
    "lx-last-first-date": "A woman at a restaurant table, date number 147, exhausted but trying. Across from her, this one is different — he's listening, really listening, leaning in. Behind her chair, 146 ghostly failed dates fade into shadow.",
    "lx-couples-therapist": "A couples therapist leaning forward between two warring partners, hand raised, about to deliver the one sentence that cuts through it all. The couple's anger is visible like storm clouds, but the therapist's words are a beam of light between them.",
    "lx-single-father": "A father sitting on a kitchen floor early in the morning, carefully learning to braid hair using a YouTube tutorial on a propped-up phone. A packed school lunch sits on the counter. Dawn light streams through the window. His work boots are by the door, ready for a long day.",

    # ── SET 4 RARES ──
    "lx-pen-pal": "Two people in different countries, each at a desk, writing letters by hand. Between them, 342 envelopes float through the air like a bridge spanning an ocean. Each envelope is slightly different, years passing in the stamps.",
    "lx-wingman": "A wingman at a bar, orchestrating an introduction between two shy people, pushing them gently together. Behind him, a scoreboard shows 47 successful introductions, zero credit taken. He raises a glass to himself alone.",
    "lx-long-distance": "Two people holding opposite ends of a string that stretches 4,200 miles across an ocean, standing on different continents. The string is frayed and thin but unbroken. Their faces mirror each other's longing.",
    "lx-divorce-lawyer": "A divorce lawyer at a desk with 800 files stacked behind her, each one an ending. She removes her glasses and rubs her eyes. On her desk, a wedding photo of her own marriage sits face-down.",

    # ── SET 4 UNCOMMONS ──
    "lx-situationship": "Two people orbiting each other like planets, close but never quite touching, for seven months shown as a spiral of calendar pages between them. Neither commits to a direction. Gravity holds them in limbo.",
    "lx-parasocial": "A content creator on a screen, smiling at millions of tiny adoring figures below, each one believing the smile is for them personally. The creator is alone in a room. The followers are alone in rooms. Nobody touches.",
    "lx-40yo-profile": "A person at a laptop, age 40, rewriting their dating profile for the 47th time. Draft versions are crumpled all around them like tumbleweeds. The cursor blinks on an empty bio. They stare at their own reflection in the dark screen.",
    "lx-ghosted": "A person lying awake at 2:14 AM staring at a phone that shows 'Read' under their last message. The phone glows like a spotlight on their disappointment. The other side of the bed is empty and cold.",

    # ── SET 4 COMMONS ──
    "lx-ai-matchmaker": "A giant AI matchmaking machine churning out 800 million matches, pairs of people launched on conveyor belts past each other. None of them connect. Meanwhile, at a bus stop outside the factory, two people share an umbrella and laugh.",
    "lx-swipe": "A giant thumb swiping through a parade of human faces, each person getting 0.3 seconds of consideration. The faces blur together. The thumb is mechanical and relentless. Discarded people pile up behind it.",
    "lx-read-receipt": "A phone screen showing a read receipt timestamp, enlarged to building-size, looming over a tiny anxious person below it. The timestamp glows like a judgment. The person's thought bubble is a spiral of worry.",

    # ── SET 4 JUNK ──
    "lx-body-count": "Two people on a date, a literal scoreboard descending from the ceiling between them like a game show reveal. Both stare at it with different expressions. The romantic dinner is interrupted by the absurd audit.",
    "lx-what-are-we": "Two people facing each other, one with their mouth open about to ask the dreaded question. The words hang between them like a bomb with a lit fuse. The cozy apartment around them trembles.",
    "lx-love-tos": "A dating app terms of service document unfurling from a phone like a wedding veil, impossibly long. Two people trying to start a relationship must navigate through it. Lawyers lurk in the margins like gargoyles.",

    # ── SET 5 WAR ROOM MYTHICS ──
    "wr-peace-negotiator": "Two exhausted diplomats across a bare table in a dim room, sleeves rolled up, ties loosened. Between them, a single piece of paper. Their hands are shaking. Outside the room, the fate of millions waits. No technology in the room.",
    "wr-refugee": "A woman carrying a small child across a desolate landscape, 400 miles of terrain behind her. She wears scrubs — she was a pediatric surgeon. Her stethoscope hangs around her neck. The child clutches a ragged toy.",
    "wr-objector": "A lone figure in uniform standing motionless while everyone around them marches forward in lockstep. The figure holds a piece of paper — their formal refusal — against a strong wind. Their expression is calm but resolved. A storm brews behind them.",
    "wr-war-orphan": "A small child, five years old, sitting in rubble clutching a one-armed teddy bear. A destroyed building frames them like a broken cathedral. The child's eyes are too old for their face. Dust hangs in shafts of light.",
    "wr-veteran": "A veteran sitting in a VA waiting room, number 4 on a ticket, surrounded by other veterans. Each one carries invisible weight. The fluorescent lights buzz. The clock on the wall shows they've been waiting for hours. Four deployment patches on the veteran's jacket.",

    # ── SET 5 LEGENDARIES ──
    "wr-drone-pilot": "A drone pilot in a trailer in a Nevada desert, screens glowing with targeting crosshairs over a faraway village. The pilot's face is lit blue. A coffee mug sits next to the joystick. The distance between trigger and consequence is obscene.",
    "wr-cyber-commander": "A person at a keyboard in a dark room, 14 lines of code visible on a screen. Through a split panel, a hospital on the other side of the world goes dark — ventilators stopping, monitors flatling. The typist's fingers hover, job done.",
    "wr-war-correspondent-v2": "A journalist crouching behind a crumbling wall, camera raised, press badge visible, determined expression. On the wall behind them, 67 tally marks are scratched into the concrete. The journalist raises the camera toward a cloud of dust and distant commotion. Their notebook is filled with stories.",

    # ── SET 5 RARES ──
    "wr-diplomat": "A diplomat at a candlelit dinner, raising a glass to a foreign counterpart across a table of untouched food. Outside the window, a city lights up — the deal worked, the siege lifted. The smallest gesture saved thousands.",
    "wr-sanctions-analyst": "A sanctions analyst buried in paperwork, 140 packages tracked on a massive wall of pins and string. Only 3 pins glow red — the ones that actually worked. The rest are gray and useless. The analyst presses on, circling the next target.",
    "wr-peacekeeper": "A UN peacekeeper standing between two armed factions in a dusty street, arms spread wide, blue helmet bright against the gray. 18 months in this stance. Both sides eye each other over the peacekeeper's shoulders.",
    "wr-intel-officer": "An intelligence officer standing before a dismissive panel of officials, pointing at a map predicting an invasion. The officials yawn, check phones, shuffle papers. The officer's briefing is labeled low priority. Outside the window, tanks roll.",

    # ── SET 5 UNCOMMONS ──
    "wr-autonomous-weapon": "A drone hovering inches from a person's face, red targeting light glowing, decision already made in 0.003 seconds. No human in the loop. The person's hands are raised. The machine has no mercy to appeal to.",
    "wr-propaganda-bot": "A server room filled with racks, each rack generating thousands of social media accounts. The accounts pour out of screens like an army of identical faces. An operator watches with folded arms as the army marches into feeds worldwide.",
    "wr-draft-lottery": "A hand reaching into a lottery drum filled with birthdates on paper slips. A crowd watches on a screen, each person holding their breath, hands covering mouths. The drawn date changes someone's life. Pure arbitrary fate.",
    "wr-proxy-war": "Two giant figures (superpowers) playing chess across a table, but the chess board is a real country — tiny buildings, real people running between the pieces. The players don't look down. The country burns between their moves.",

    # ── SET 5 COMMONS ──
    "wr-killer-drone": "A small drone the size of a lunchbox hovering over a landscape, a tiny price tag dangling from it showing it costs less than a used car. Below it, the destructive capability is enormous. The contrast between cost and consequence is grotesque.",
    "wr-surveillance-state": "A street corner with more cameras than people — cameras on poles, drones above, lenses in every surface. A single citizen walks through, tracked by beams of light from every direction. 1.4 cameras for every person. Privacy is extinct.",
    "wr-cyber-attack": "A hospital room where a ventilator has stopped, its screen showing a skull icon. A nurse manually pumps air while doctors scramble. Through the window, the city grid flickers. The attack came through a computer somewhere far away.",

    # ── SET 5 JUNK ──
    "wr-arms-dealer": "An arms dealer at a split desk, selling weapons to both sides of a conflict simultaneously. Left hand shakes one buyer, right hand shakes the other. Both buyers can see each other. The dealer grins. Business is booming.",
    "wr-war-profiteer": "A businessman in a plush office watching a stock ticker climb 340% while through the window behind him, a war rages — explosions, smoke, fleeing civilians. His champagne glass reflects the fire. The graph only goes up.",
    "wr-geneva-suggestion": "The Geneva Convention document, massive and official, being used as a doormat. Military boots walk over it. The text is worn but still legible. Someone has crossed out 'Convention' and written 'Suggestion' above it.",

    # ── SET 6 SKILLS.VOID MYTHICS ──
    "sv-apprentice": "An apprentice kneeling beside a master craftsperson, watching hands shape wood with 10,000 hours of precision. The apprentice's hands mirror the movements, learning through proximity. Tools hang on the wall like sacred instruments.",
    "sv-mentor": "A mentor and student sitting on a bench, the mentor mid-sentence, one finger raised. The student's expression shifts — the single sentence landing like lightning. The world around them fades. One sentence changes everything visible in the student's posture.",
    "sv-autodidact": "A self-taught person at a desk surrounded by evidence of 14 different skills — tools, instruments, code, art supplies, mechanical parts — and zero diplomas on the wall. Their hands are calloused from everything. The wall is bare but the desk is full.",
    "sv-trades-teacher": "A trades teacher in a workshop demonstrating technique to attentive students who are building real things with their hands. Through the window, their guidance counselor drives past in a cheaper car. The students' work is tangible and valuable.",
    "sv-night-school": "A person in work clothes rushing from a job site into a night school building, hard hat still on, lunch pail in hand. The clock shows 6 PM. They'll study until 10, sleep 4 hours, and do it again. Their determination is a physical force.",

    # ── SET 6 LEGENDARIES ──
    "sv-phd": "A person with a PhD diploma visible in their bag, working as a barista, steaming milk with scholarly precision. Their name tag says their first name. Their pay stub shows less than the coffee they serve. The irony is in the foam art.",
    "sv-master-craftsman": "A master craftsman in a workshop of extraordinary beauty — 30 years of work on every surface. Behind them, only 2 young apprentices remain, the last ones willing to learn. The craft is exquisite and nearly extinct.",
    "sv-cc-professor": "A community college professor at a desk with 180 index cards spread out, memorizing every student's name. Their salary is modest but their investment in each person is visible. Each card has notes about the student's life beyond class.",

    # ── SET 6 RARES ──
    "sv-bootcamp-grad": "A coding bootcamp graduate proudly holding a certificate, but the certificate is already yellowing and curling at the edges — expired in 18 months. Behind them, a new bootcamp advertises entirely different skills. The treadmill never stops.",
    "sv-career-counselor": "A career counselor at a desk, a student asking 'What's safe?' The counselor's mouth opens but nothing comes out. Behind them, a chart of 'stable careers' has every entry crossed out. The honest answer is silence.",
    "sv-tenured-professor": "A tenured professor behind a castle drawbridge that's been pulled up, looking down from their secure tower at adjuncts below wading through a moat. The professor's position is the last safe one. The drawbridge mechanism is rusted shut.",
    "sv-union-rep": "A union rep standing at a podium before 4,800 workers, sleeves rolled up, voice mid-roar. Behind the rep, a wall of contracts, grievances won, and fights fought. The workers lean forward. Someone still fights for them.",

    # ── SET 6 UNCOMMONS ──
    "sv-linkedin-otw": "A person with a glowing 'Open to Work' banner around their profile photo like a halo of desperation, sitting alone at a desk surrounded by 847 sent applications. Three responses glow faintly in the pile. The rest are silence.",
    "sv-cert-mill": "A factory assembly line producing millions of identical certification badges, each one stamped and shrink-wrapped. The badges pile up in a landfill outside. Employers walk past the landfill without looking. The certificates mean nothing.",
    "sv-mba": "A person in a cap and gown shaking hands at a graduation, but the diploma is a receipt for an enormous sum. Behind the stage, the real value was the networking — tiny business cards flutter like confetti. The knowledge is secondary.",
    "sv-internship": "An unpaid intern doing the same work as everyone else at a desk, but their chair is smaller, their desk is a folding table, and their payment is a handshake labeled 'experience.' The real employees do less and get paid. The intern does everything.",

    # ── SET 6 COMMONS ──
    "sv-ai-resume": "A giant mechanical eye mounted on a desk, scanning stacks of resumes on a conveyor belt, stamping most of them REJECTED and dropping them into an overflowing bin. One resume in the reject pile is clearly brilliant — awards, degrees — but used the wrong font. The machine doesn't care.",
    "sv-online-degree": "A massive online university building made of screens, with students entering enthusiastically at the front but only 11% emerging from the back with degrees. The rest wander out side exits, lighter in wallet, heavier in doubt.",
    "sv-micro-credential": "A person wearing a vest covered in tiny digital badges like merit badges, proud and decorated. But each badge has a tiny expiration date, and half of them are already faded and peeling. Six months of shelf life per achievement.",

    # ── SET 6 JUNK ──
    "sv-cover-letter": "Two laptops facing each other on a desk — one AI writing a cover letter, the other AI reading it. No humans in the room. The cover letter is perfect and meaningless. The hiring AI is impressed by the applying AI. A human's resume sits unopened between them.",
    "sv-ai-portfolio": "A slick portfolio website displayed on a screen, beautiful and impressive. But a finger is poking through the screen and it collapses like a house of cards — nothing behind the surface. The portfolio is a facade. The skills are hollow.",
    "sv-entry-level": "A job posting on a massive billboard requiring 5 years of experience for an entry-level position. Below it, fresh graduates look up in disbelief, their unused diplomas still warm. A paradox door that cannot be opened from the outside.",

    # ── SET 7 FOUNDER.EXE MYTHICS ──
    "fe-garage-founder": "A cluttered one-car garage at midnight, a single bare bulb swinging overhead. A figure hunches over a workbench covered in circuit boards, coffee cups, and crumpled napkin sketches. Through the open garage door, a row of gleaming corporate towers fills the skyline, utterly indifferent.",
    "fe-whistleblower-cto": "A corner office being emptied into a single cardboard box, stock option certificates visibly shredded in the wastebasket. The desk has two monitors — one showing a massive user database, the other showing a resignation letter. The chair is still spinning from the person who just stood up.",
    "fe-failed-founder": "A figure sitting on a park bench surrounded by four tiny gravestones, each marked with a different startup logo. The fifth attempt sprouts from the ground beside them like a stubborn weed pushing through concrete. The figure's shoes are worn through but they are lacing up for another walk.",
    "fe-open-source": "A vast bridge spanning an enormous canyon, with thousands of vehicles crossing it daily. Underneath the bridge, a single figure tightens bolts by hand with a tiny wrench. A tip jar beside them holds a few coins. The bridge holds the weight of an entire industry.",
    "fe-cofounder-wife": "A kitchen table covered in unpaid bills, a laptop open to a bank account, and a calculator. A woman sits balancing everything while through the doorway, a home office glows with the logo of a startup she has no equity in. Seven years of calendar pages are stacked on the counter.",

    # ── SET 7 FOUNDER.EXE LEGENDARIES ──
    "fe-techbro": "A figure in a fleece vest standing on a stage giving a keynote, arms spread wide in triumph. Behind the stage curtain, a long line of people files out a back exit carrying cardboard boxes. The speaker's slide reads 'We Are Family' in enormous letters.",
    "fe-angel-investor": "A figure at a roulette table, tossing chips labeled with startup logos onto random numbers. Most chips are scattered and lost, but one lucky number glows gold. The figure poses for a magazine cover with the single winning chip, ignoring the floor littered with losses.",
    "fe-yc-reject": "A rejection letter pinned to a corkboard, surrounded by three identical letters. Below them, a revenue chart climbs dramatically upward. Through the window, a prestigious accelerator building is visible, its latest batch struggling. The rejection letters are yellowed but the chart is fresh.",

    # ── SET 7 FOUNDER.EXE RARES ──
    "fe-pivot": "A weathervane on a rooftop spinning wildly, each direction labeled with a different business model. Below it, the same pitch deck is being reprinted on a copy machine, only the title page changing each time. A waste bin overflows with previous versions. The weathervane never stops.",
    "fe-pitch-deck": "An enormous presentation screen showing a graph with a hockey-stick curve shooting into the stratosphere. In the audience, one person sits alone — it is the founder's parent, squinting at the numbers. The actual revenue line is a barely visible dot at the bottom of the chart.",
    "fe-saas-graveyard": "An enormous junkyard stretching to the horizon, piled high with discarded laptop computers and cracked phone screens, each showing a different defunct app landing page. A conveyor belt at the edge drops new devices onto the pile. In the foreground, a single laptop still glows faintly, its battery at 1 percent.",
    "fe-term-sheet": "A towering legal document unfurling from a conference table like a scroll, so long it spills out the window and down the side of the building. A founder at the table signs the bottom page with eyes closed. Hidden in the middle pages, a tiny clause glows ominously red.",

    # ── SET 7 FOUNDER.EXE UNCOMMONS ──
    "fe-hustle-guru": "A figure on a stage selling a course about success, surrounded by massive stacks of money. The audience members furiously take notes, but the stacks of money are made entirely of the audience's tuition payments. A circular arrow connects the money from audience to stage and back to the course price.",
    "fe-growth-hacker": "A massive funnel the size of a building, with a crowd of 400,000 tiny figures being poured in at the top. At the narrow bottom, only a trickle of figures emerges — maybe a thousand. The funnel's sides are polished and slippery. A billboard on the funnel reads 'GROWTH.'",
    "fe-ai-wrapper": "A single gift box on a table, elegantly wrapped with a bow, sitting on a pedestal with a price tag showing millions. A hand lifts the lid to reveal the box is completely empty except for a thin wire connecting to a much larger machine in the next room that does all the work.",
    "fe-remote-ceo": "A tropical hammock between two palm trees, a laptop balanced on a figure's chest showing a grid of video call faces. The figure types furiously into a chat application. Below the hammock, a team photo sits face-down in the sand. Nobody in the photo has ever met in person.",

    # ── SET 7 FOUNDER.EXE COMMONS ──
    "fe-ai-startup-gen": "A vending machine the size of a skyscraper, dispensing startup ideas on little cards from a slot at the bottom. A crowd feeds coins into it, collecting cards eagerly. The ground around the machine is ankle-deep in discarded idea cards that nobody wanted. The machine never stops dispensing.",
    "fe-cap-table": "A pie chart the size of a dinner table, being sliced thinner and thinner by successive hands reaching in with knives. The original slice — labeled 'Founder' — has been reduced to a sliver barely visible. The largest slices belong to figures in suits who arrived last.",
    "fe-nda": "Two figures at a cafe table, both holding pens over identical legal documents, unable to actually discuss the idea written on a napkin between them. The napkin shows a crude drawing of a to-do list app. The legal documents are thicker than phone books.",

    # ── SET 7 FOUNDER.EXE JUNK ──
    "fe-linkedin-ceo": "A fresh-faced figure at a desk made of stacked textbooks, a business card reading 'CEO & VISIONARY' propped against an empty monitor. The office is a bedroom. A participation trophy sits on the shelf. The figure practices a power pose in a mirror on the wall.",
    "fe-crypto-pivot": "A chameleon sitting on a laptop, changing colors rapidly — first social media blue, then blockchain gold, then AI purple. Each color change comes with a new logo projected onto the wall behind it. A counter in the corner stubbornly reads zero users through every transformation.",
    "fe-demo-day": "A long stage with forty tiny podiums in a row, each with a spotlight. Six spotlights turn gold while the rest go dark. A janitor sweeps the dark podiums off the edge of the stage with a broom. A banner overhead reads 'GREAT BATCH' in optimistic letters.",

    # ── SET 8 DEEPSTATE.AI MYTHICS ──
    "da-election-volunteer": "A long table in a gymnasium, covered in paper ballots being hand-counted by a weary figure with reading glasses. Behind the figure, a sleek electronic counting machine sits unplugged in the corner. A line of citizens waits patiently, trusting the slow human hands over the fast machine.",
    "da-the-leaker": "A figure in a government hallway, paused mid-step, holding a single manila envelope against their chest. The hallway stretches endlessly in both directions, lined with identical doors. Behind the figure, their employee badge and career hang symbolically on a hook. The envelope casts an enormous shadow.",
    "da-privacy-advocate": "A lone figure standing before an enormous dam, arms braced against it, holding back a flood of surveillance cameras, microphones, and data cables that press against the concrete. The dam has hairline cracks. The figure's flip phone sits in their breast pocket, the only technology they carry.",
    "da-real-journalist": "A cramped office filled floor-to-ceiling with filing cabinets, each drawer labeled 'REDACTED.' A figure at the desk holds up 35 unredacted pages like trophies, light streaming through them. The other 812 folders lie in a black pile on the floor, their contents blacked out entirely.",
    "da-analog-voter": "A figure walking calmly into a polling station carrying a folded newspaper and a pencil, surrounded by a storm of floating holographic screens, deepfake videos, and flashing notifications that swirl around them like a tornado. None of it touches the figure. They have done this for forty-two years.",

    # ── SET 8 DEEPSTATE.AI LEGENDARIES ──
    "da-deepfake-senator": "A podium with fourteen thousand identical copies of the same figure speaking simultaneously, each saying something slightly different. In the center, the real figure stands frozen, mouth taped shut, unable to compete with the volume of copies. Correction notices flutter like confetti that nobody catches.",
    "da-surveillance-czar": "A room with a thousand screens arranged in a dome, each showing a different street corner, doorway, or park bench. A single figure sits at the center console, dwarfed by the surveillance apparatus. Their own face appears on four of the screens, watched by cameras they placed themselves.",
    "da-ai-lobbyist": "A massive legislative building with its doors held wide open by golden crowbars. A river of money flows into the front entrance, past the columns, and through the halls. Inside, tiny documents labeled 'Regulation' are being swept out a back window by the current. Only one document survives, waterlogged and illegible.",

    # ── SET 8 DEEPSTATE.AI RARES ──
    "da-bot-farm": "A cavernous warehouse filled with endless rows of server racks, each rack sprouting hundreds of tiny speech bubbles that float upward like balloons. The bubbles all say slightly different things but look identical. A janitor in the corner sweeps up the 8% that were caught, while 92% escape through the roof.",
    "da-predictive-policing": "A giant dartboard shaped like a city map, with darts clustered heavily in the same few neighborhoods while other areas remain untouched. A mechanical arm throws darts automatically, always hitting the same zones. A sign on the wall reads 'UNBIASED' in bold letters. An audit clipboard gathers dust.",
    "da-ai-judge": "An enormous scale of justice, but one side holds a stack of case files and the other holds a calculator. The calculator side always wins, tilting the scale. A long line of figures waits for judgment, each one seeing the same predetermined tilt. There is no appeals window anywhere in the courtroom.",
    "da-social-score": "A bus stop where citizens wait in line, each with a floating number above their head. The bus doors only open for numbers above a threshold. A sign reads 'Community Trust Index' with 'Social Credit' crossed out underneath in barely-visible ink. The bus driver is a machine.",

    # ── SET 8 DEEPSTATE.AI UNCOMMONS ──
    "da-ai-speechwriter": "A grand podium with a teleprompter, the text scrolling automatically. Behind the curtain, a massive server rack generates words that flow through cables directly into the teleprompter. The figure at the podium reads flawlessly, passion perfectly calibrated. The audience applauds on cue.",
    "da-disinfo-czar": "A figure at a desk with a giant rubber stamp marked 'FALSE,' stamping documents at incredible speed. A conveyor belt delivers papers endlessly. Some stamped papers blow off the desk and land in a pile labeled 'Actually True — 39%.' The stamp never pauses to check.",
    "da-gerrymandering-ai": "A giant jigsaw puzzle of a country, being rearranged by mechanical arms that move pieces to create the most absurd district shapes — snaking, twisting, splitting neighborhoods. A timer on the wall shows 0.4 seconds elapsed. The puzzle was fair before the arms touched it.",
    "da-ai-press-sec": "A press briefing room where a holographic figure stands at the podium, perfectly composed. Reporters raise hands with questions but the hologram redirects each question into a loop of pre-approved talking points. A 'Follow-Up' button on the podium has been physically removed.",

    # ── SET 8 DEEPSTATE.AI COMMONS ──
    "da-voter-profile": "A filing cabinet the size of a city block, each drawer containing a detailed dossier on a single voter. A mechanical eye reads all 5,200 data points per file simultaneously. The voters walk past the cabinet daily, unaware it exists, while targeted messages appear on their phones like clockwork.",
    "da-robocall": "A massive switchboard with billions of connections sparking simultaneously, each line carrying an identical voice. A sound booth in the corner shows where the original voice was recorded — a single two-minute session. The clone voice now speaks words the original person never said, to billions of ears.",
    "da-compliance-theater": "A boardroom table with 47 neatly bound recommendation reports stacked in the center. Every chair around the table is empty. The reports are pristine and unread. One has been repurposed as a doorstop. A framed copy hangs on the wall next to awards for 'Ethics Leadership.'",

    # ── SET 8 DEEPSTATE.AI JUNK ──
    "da-conspiracy-ai": "A factory assembly line producing conspiracy theories on conveyor belts, each one packaged in increasingly elaborate wrapping. 88% fall off the end into a recycling bin. 12% get loaded onto delivery trucks. One package in the bin glows faintly — the one that was actually true.",
    "da-filibuster-bot": "A lectern in an empty chamber, where a mechanical figure reads from an infinite scroll of paper that piles up on the floor in enormous drifts. The speech has been going on so long that cobwebs connect the figure to the lectern. Every bill in the chamber is buried under paper.",
    "da-poll-bot": "A crystal ball on a desk, surrounded by charts and predictions pinned to every wall, every single one marked with a red X for 'wrong.' A figure polishes the crystal ball proudly anyway. News cameras point at the ball, ready for the next prediction. The red X collection grows.",

    # ── SET 9 HEALTHCARE.SYS MYTHICS ──
    "hs-the-nurse-who-stayed": "A hospital corridor at night, empty except for a single figure in scrubs walking past thirty-four doorways, each with a patient chart hanging from it. The only light comes from the nurse's station at the end of the hall, where a single coffee cup still steams. Every other chair in the station is empty.",
    "hs-village-doctor": "A winding dirt road stretching 140 miles through mountains and valleys, with a small car driving toward a distant farmhouse. The car's trunk is packed with medical supplies. A telemedicine kiosk stands at the start of the road, dark and useless — no internet signal bars. The farmhouse has a light on.",
    "hs-hospice-worker": "A quiet room with a single bed, soft light through curtains. A figure sits beside the bed, holding the hand of the person lying in it. A monitoring screen on the wall shows perfect comfort metrics, but the person in the bed looks only at the hand holding theirs. The machines are background noise.",
    "hs-emt": "An ambulance with its back doors flung open, equipment scattered on a stretcher being wheeled at speed. A figure in uniform runs alongside, one hand on the stretcher, the other adjusting equipment. Their paycheck stub flutters out of a pocket — a shockingly small number. The stretcher patient is stabilizing.",
    "hs-patient-zero": "A figure at a desk stacked with insurance denial letters, each one opened and annotated with handwritten appeals. A rubber stamp reading 'OVERTURNED' sits beside a growing stack of victories. The insurance company's building looms through the window, enormous and monolithic. The figure's desk lamp burns bright.",

    # ── SET 9 HEALTHCARE.SYS LEGENDARIES ──
    "hs-denial-bot": "A conveyor belt in a massive factory, carrying medical claim forms past a stamping machine that slams 'DENIED' on each one at blinding speed — 0.3 seconds per stamp. A tiny quality-control window shows 1.2% of claims diverted to a lone human reviewer buried behind a mountain of paper. The belt never stops.",
    "hs-pharma-algo": "A vial of medicine on a pedestal, dramatically lit like a museum artifact. A price tag hangs from it showing an astronomical number. Beside the pedestal, a manufacturing receipt shows the actual cost — almost nothing. A calculator between them runs the optimization equation. The gap between the numbers is obscene.",
    "hs-surgeon": "An operating room with a robotic surgical arm hovering over one table, performing a routine procedure perfectly. At the adjacent table, a human surgeon leans in close to handle something the robot's arm cannot reach — the unexpected complication. The robot's manual is open to a page that says 'Refer to Human.'",

    # ── SET 9 HEALTHCARE.SYS RARES ──
    "hs-misdiagnosis": "A massive statistical chart on a wall showing 97.2% accuracy in bright green. A tiny red sliver at the edge represents 2.8%. Below the chart, a counter translates that percentage into 8.4 million faces, each one small but distinct. A suggestion box labeled 'Liability' sits empty on the floor.",
    "hs-therapy-bot": "A split-screen room — one side shows a warm, glowing chat interface responding 'I understand' to a screen, perfectly calibrated. The other side shows the 26% it missed: an empty chair, a cold cup of tea, and a phone face-down on the table. The chat interface has no malpractice insurance on the wall.",
    "hs-telehealth": "A laptop screen showing a tiny video window of a doctor's face, timer reading four minutes. The patient sits in front of the laptop, trying to show something on their arm that the camera cannot capture. A prescription prints from a nearby machine before the conversation ends. The doctor is already looking at the next appointment.",
    "hs-prior-auth": "A hospital waiting room with a single patient sitting in a chair, surrounded by 17 calendar pages scattered on the floor — each one a day of waiting. A 'PENDING' stamp hovers above a medical form. Through the window, the patient's condition visibly worsens in the reflection, day by day by day.",

    # ── SET 9 HEALTHCARE.SYS UNCOMMONS ──
    "hs-symptom-checker": "A search bar the size of a building, with millions of tiny figures typing symptoms into it. Every result page shows 'CANCER' in bold at the top, regardless of the query. A footnote at the bottom — too small to read — says 'probably nothing.' The ER entrance across the street has a line around the block.",
    "hs-nurse-shortage": "A hospital floor plan viewed from above, showing a single figure running between dozens of patient rooms like a pinball. A digital dashboard on the wall shows 'STAFFING: OPTIMAL' in green while the lone figure sprints. A stock ticker in the corner of the dashboard shows the hospital's share price climbing steadily.",
    "hs-medical-debt": "A mailbox overflowing with bills, each envelope stamped with a different medical logo. The mailbox post is cracking under the weight. A phone on the ground beside it rings at 7 AM, the screen showing 'COLLECTIONS.' The house behind the mailbox has a 'SURVIVED' banner on the door.",
    "hs-wellness-app": "A glowing phone screen showing a meditation app with the word 'BREATHE' in calming colors. Behind the phone, invisible data streams flow from the app to an insurance company building in the background. The user's panic attack data is labeled and sorted into filing cabinets. A namaste gesture emoji floats above it all.",

    # ── SET 9 HEALTHCARE.SYS COMMONS ──
    "hs-ai-scribe": "A doctor's desk covered in automatically generated medical notes, each page filled with tiny text. The doctor glances at the top page, skimming it in seconds. A magnifying glass reveals 3.4 errors per page — wrong medications, misspelled conditions. The patient's real chart sits unopened underneath the generated pile.",
    "hs-drug-interaction": "A computer screen exploding with 47 simultaneous alert pop-ups, each one identical in urgency and color. A hand clicks 'Dismiss All' reflexively. One alert in the middle — the fatal interaction — blinks and vanishes with the rest, indistinguishable from the noise.",
    "hs-patient-portal": "A login screen displayed on a phone at 2 AM, showing 'PASSWORD RESET #7.' Behind the login, test results glow ominously with no context or explanation attached. The phone illuminates a figure's worried face in a dark bedroom. A 'Schedule Appointment' button leads to a page reading 'Next Available: 6 Weeks.'",

    # ── SET 9 HEALTHCARE.SYS JUNK ──
    "hs-webmd": "A giant magnifying glass hovering over a person's stomach, projecting the word 'CANCER' onto the wall in enormous letters. A doctor in the background holds up a small sign reading 'Gas.' The ER waiting room visible through a doorway is packed with people clutching printouts from symptom-checker websites.",
    "hs-admin-bloat": "A hospital org chart on a wall, shaped like a pyramid. The top ten layers are all administrative roles, each office plush and spacious. At the very bottom point, a single nurse works a floor of patients. The admin-to-doctor ratio reads 10:1 on a plaque. No administrator has a stethoscope.",
    "hs-influencer-doc": "A figure in a lab coat posing in front of a ring light, holding a bottle of supplements in one hand and a medical degree in the other. A shelf behind them shows seven complaint letters from a medical board, partially hidden by bottles of mushroom supplements. A follower counter ticks upward steadily.",

    # ── SET 10 PARENT.TRAP MYTHICS ──
    "pt-library-mom": "A living room with floor-to-ceiling bookshelves, every shelf packed. A reading chair has a well-worn groove from years of use. Open books are scattered on a rug where reading clearly happens daily. Through the window, a neighbor's house glows with the blue light of multiple screens. This house has warm lamplight only.",
    "pt-playground-dad": "A park bench at a playground, a jacket draped over it with a phone visibly zipped inside the pocket. The playground equipment shows signs of heavy joyful use — scuffed slides, worn swing seats. Fourteen tally marks are scratched into the bench armrest, counting weekly hours. No screen is visible anywhere.",
    "pt-teacher-who-called": "A classroom desk with a landline phone, the receiver lifted. On the desk, a computer screen shows 47 automated behavior flags. The phone cord stretches to a concerned teacher who chose to call instead. A sticky note on the monitor reads 'He just needed lunch.' The automated system sits ignored.",
    "pt-homeschool-parent": "A kitchen table converted into a classroom — maps, science experiments, art supplies, and math manipulatives spread across every inch. No screen is present. Through the window, a standardized school building is visible in the distance. The kitchen table work is messy, colorful, and clearly alive with learning.",
    "pt-single-parent": "A hallway coat hook holding two work uniforms side by side — one for a day job, one for a night job. Below them, a pair of worn shoes. An alarm clock on a nearby shelf reads 4:30 AM. A lunchbox on the counter is being packed in the pre-dawn dark. The figure's shadow suggests they never fully stop moving.",

    # ── SET 10 PARENT.TRAP LEGENDARIES ──
    "pt-ipad-kid": "A tablet propped up on a high chair, its screen casting blue light onto an empty bowl of cereal. The tablet plays an infinite scroll of colorful animations. Nearby, a stack of untouched physical toys — blocks, crayons, a ball — gathers a thin layer of dust. The screen's glow is the brightest thing in the room.",
    "pt-helicopter-ai": "A bedroom ceiling covered in sensors, cameras, and monitoring devices, all pointed at a small bed below. A nightstand is cluttered with alert notifications printed on tiny paper slips — 47 per day. The room feels like a surveillance station disguised as a cozy space. A stuffed animal has a camera lens for an eye.",
    "pt-school-ai": "A classroom where half the desks face a human teacher's empty chair and the other half face glowing screens. The screens show perfect lesson plans. The empty chair has a 'Position Eliminated' sign. A behavioral incident chart on the wall climbs steeply upward. Test scores on another chart remain perfectly flat.",

    # ── SET 10 PARENT.TRAP RARES ──
    "pt-ai-babysitter": "A nursery room monitored by cameras in every corner, each with a blinking red recording light. Screens show every angle of the room in crystal clarity. A rocking chair in the center sits empty — no arms to hold, no lap to sit on, no lullaby voice. The cameras see everything but comfort nothing.",
    "pt-child-influencer": "A ring light towering over a tiny desk, professional-grade camera equipment surrounding a small chair. A piggy bank on the shelf has been replaced by a revenue dashboard. Contracts and brand deal paperwork are stacked next to coloring books. The proportions are wrong — adult equipment, small furniture.",
    "pt-ai-tutor-parent": "A desk split in half — one side shows a computer generating perfect homework with an A grade, the other side shows a blank worksheet and a confused pencil hovering over it. The gap between the AI side and the understanding side is a visible chasm. The grade report glows while comprehension sits dark.",
    "pt-playground-empty": "An abandoned playground where every piece of equipment — swings, slide, monkey bars — is rusted and overgrown with weeds. A sign reads 'Built 2015.' Through a nearby window, the blue glow of screens illuminates a row of houses. The playground is perfectly empty under a clear sky.",

    # ── SET 10 PARENT.TRAP UNCOMMONS ──
    "pt-cocomelon": "A glowing tablet screen showing hypnotic, colorful animation loops, propped up like an altar on a high chair tray. A pediatrician's recommendation card on the fridge reads '0 hours screen time.' A clock on the wall shows the tablet has been running for hours. The animation loops are perfectly endless.",
    "pt-grade-tracker": "A phone screen showing a school grade tracker app with 12 notification badges, refreshed obsessively. The phone sits on a dinner table next to an untouched meal. A report card on the fridge shows good grades but a counselor's note about stress is paper-clipped behind it, hidden and unread.",
    "pt-ai-nanny-cam": "A home interior where every room is visible through a grid of camera feeds on a tablet. One camera shows a living room where a small figure waves at the lens, performing for the audience of one. A log file next to the tablet shows 847 flagged events, only 2 highlighted as real.",
    "pt-family-screen": "A dinner table set for four, with four glowing screens — phone, tablet, laptop, and TV — each illuminating a different face. The food on the plates is getting cold. A word counter floating above the table reads '12 words exchanged.' The family portrait on the wall behind them shows everyone looking at each other.",

    # ── SET 10 PARENT.TRAP COMMONS ──
    "pt-ai-lullaby": "A crib with a smart speaker on the nightstand, playing a perfectly synthesized lullaby. Musical notes float from the speaker in precise, algorithmic patterns. A rocking chair beside the crib is empty — no parent singing. The lullaby is flawless but the room feels clinical and hollow.",
    "pt-parenting-app": "A phone screen cracked from overuse, showing 47 parenting tips simultaneously, several contradicting each other visibly. Monday's tip and Thursday's tip are highlighted side by side, saying opposite things. A guilt meter on the screen maxes out at 400%. The phone battery is at 2%.",
    "pt-kid-tracker": "A GPS map on a phone screen showing a child's location dot, updating every 30 seconds. The dot sits motionless at school. A second, hidden dot — the tracker the child disabled and left in a locker — blinks separately. The parent watches the decoy dot, satisfied. Week 2 of the deception.",

    # ── SET 10 PARENT.TRAP JUNK ──
    "pt-ai-name-gen": "A baby name generator displayed on a laptop, an infinite scroll of algorithmically generated names filling the screen. A nursery in the background has a blank name plaque on the wall. The top suggestion reads something absurd. Forty percent of the results are variations of the same name.",
    "pt-momfluencer": "A perfectly staged living room with professional lighting equipment and camera rigs. A phone on a tripod records a carefully arranged 'candid' domestic scene. A brand deal contract sits on the coffee table next to a sippy cup. A view counter in the corner shows millions. Consent forms are conspicuously absent.",
    "pt-gender-reveal": "A sky filled with 400 drones arranged in a formation, releasing colored smoke. Below, a scorched patch of grass shows where previous pyrotechnics went wrong. A fire extinguisher sits prominently in the foreground, recently used. The drone display is spectacular and wildly disproportionate to the information conveyed.",

    # ── SET 11 CLIMATE.ERR MYTHICS ──
    "ce-grid-operator": "A massive electrical control room with a wall-sized grid map, switches and dials everywhere. A single figure stands before the console, hands on two critical levers, holding the entire network together. Duct tape and manual patches are visible on several panel junctions. Every data center in the region depends on this room.",
    "ce-water-protector": "A river flowing past a series of enormous data center buildings, each with intake pipes drawing water in massive volumes. Downstream, a small town's well has a 'DRY' sign on it. A figure stands between the river and the town, arms outstretched. The data centers are labeled 'ESSENTIAL' while the town's water supply dwindles.",
    "ce-repair-tech": "A workshop bench overflowing with devices in various states of repair — phones, laptops, tablets, all meant for the landfill bin visible outside the window. The bin is empty because every device gets fixed. Tools hang on a pegboard wall with 14,000 tally marks. Each mark is a device saved from the scrap heap.",
    "ce-climate-scientist": "A desk buried under 47 published research papers, each one meticulously detailed with charts and data. A mail slot in the door shows letters from politicians — all returned unopened. The scientist stares at the wall where projections show worsening trends. The papers are pristine and unread by anyone who matters.",
    "ce-ewaste-worker": "A mountain of discarded electronics — circuit boards, screens, cables — towering over a figure who sorts through it with bare hands. No protective equipment anywhere. A shipping label on a crate reads the origin country. A luxury tech product launch event poster peels from a nearby wall. The contrast is total.",

    # ── SET 11 CLIMATE.ERR LEGENDARIES ──
    "ce-data-center": "A massive warehouse in a desert landscape, humming turbines and cooling towers surrounding it. Water trucks line up at the entrance, pumping millions of gallons daily. A tiny town in the background has brown lawns and water restriction signs. A billboard on the data center reads 'Carbon Neutral' with an asterisk that leads nowhere.",
    "ce-bitcoin-mine": "A building consuming electricity visible as glowing cables thick as tree trunks, feeding into a single room where one model trains on rows of overheating GPUs. A calendar on the wall shows the model will be obsolete in six months. A power meter beside the door spins so fast it blurs.",
    "ce-greenwash-ai": "A boardroom table covered in glossy ESG reports, each one hundreds of pages thick and beautifully designed. Through the boardroom window, smokestacks belch into the sky unchanged. An emissions graph on the wall goes only up, while the reports all say 'NET ZERO.' Investors shake hands over the disconnect.",

    # ── SET 11 CLIMATE.ERR RARES ──
    "ce-gpu-graveyard": "A vast field filled with discarded graphics cards piled in dunes like sand, stretching to the horizon. A cargo ship in the background is loaded with more, heading overseas. A recycling bin at the field's entrance holds 8% of the total — a pitiful fraction. New GPU boxes arrive on pallets as old ones are buried.",
    "ce-cooling-crisis": "Enormous cooling towers surrounding a data center, clouds of steam billowing upward. A river that feeds the towers is visibly lower than its banks, muddy and receding. A sign at the river's edge shows the historic water line — feet above the current level. The data center's parking lot has a puddle. The river does not.",
    "ce-carbon-credit": "A certificate exchange market where ornate carbon credit documents trade hands at high prices. Through the window of the exchange, the forest where the credits allegedly came from is visible — the trees were already there, pre-existing and uncounted. A magnifying glass reveals the fine print: 'Verified by Self.'",
    "ce-lithium-mine": "An open-pit mine carved into a landscape, terraced and enormous. Pools of contaminated water surround it in unnatural colors. A delivery truck leaving the mine carries batteries labeled 'GREEN ENERGY.' A nearby aquifer cross-section shows poison seeping downward. A billboard at the mine entrance reads 'Sustainable Extraction.'",

    # ── SET 11 CLIMATE.ERR UNCOMMONS ──
    "ce-smart-thermostat": "A sleek thermostat on a wall, its display showing energy savings and a smiley face. Behind the wall, visible in cross-section, data cables run from the thermostat to an insurance company filing cabinet. The thermostat knows the homeowner's exact schedule, sleep patterns, and absence times. The savings are real. So is the surveillance.",
    "ce-ai-sustainability": "A 200-page sustainability report sitting on a desk, opened to a pie chart showing only Scope 1 emissions — a tiny fraction. The pages for Scope 2 and 3 are stuck together, literally glued shut. A magnifying glass reveals the tiny footnote: 'Scope 3 analysis forthcoming.' It has said 'forthcoming' for three editions.",
    "ce-fast-fashion-ai": "A conveyor belt producing thousands of clothing designs per hour, each one slightly different, tumbling off the end into an overflowing landfill. A figure at the start of the belt sketches a new trend that lasts approximately one scroll-length of a social media feed. The landfill is taller than the factory.",
    "ce-crypto-mining": "Two maps side by side on a wall — one showing a country's power grid, the other showing cryptocurrency mining operations. The mining map consumes visibly more energy. A CO2 cloud above the mining map is labeled with another country's name for comparison. The value created is represented by a question mark.",

    # ── SET 11 CLIMATE.ERR COMMONS ──
    "ce-carbon-calculator": "A person sitting at a desk using a carbon footprint calculator on a screen, which shows their individual impact as a tiny number. Behind the screen, a corporate factory is visible through the window, producing 71% of total emissions. The calculator doesn't have a 'Corporate' tab. It only has 'You.'",
    "ce-green-ai-badge": "A wall of framed certificates, each one a 'Green AI' badge issued to a different company. The badges are beautiful and expensive-looking. A clipboard beneath them shows the audit process: a single checkbox labeled 'Self-Reported.' The check is already filled in. The frame costs more than the audit.",
    "ce-planned-obsolescence": "A device graveyard where perfectly functional gadgets sit in a pile, each one killed by a software update. A calendar on the wall shows each device died exactly one day after its warranty expired. A repair shop next door has a sign showing repair costs at 89% of a new device. The new device display gleams next door.",

    # ── SET 11 CLIMATE.ERR JUNK ──
    "ce-nft-tree": "A forest where each tree has a tiny NFT token hanging from its branches like ornaments. Only 200 of the trees are real and planted in soil — the rest are just tokens hanging in empty air from invisible branches. A minting machine beside the forest produces more tokens than the earth can hold trees.",
    "ce-tech-ceo-jet": "A private jet on a tarmac, its carbon offset receipt trailing from the door like a banner. The receipt is longer than the jet. A speech podium is set up at the destination, labeled 'Climate Summit — Davos.' A flight log on the jet's dashboard shows 400 trips this year. The jet's fuel gauge reads 'FULL.'",
    "ce-paper-straw": "A soggy paper straw collapsing in a drink, the focus of intense public attention and debate. Behind the drink, an ocean stretches to the horizon, filled with an enormous fishing net that accounts for 46% of the plastic problem. The straw represents 0.03%. A protest sign focuses exclusively on the straw.",

    # ── SET 12 CREATOR.NULL MYTHICS ──
    "cn-street-artist": "A brick wall with a massive mural in progress, paint cans scattered at its base, a figure on a ladder adding brushstrokes in the rain. The figure's hands are covered in paint. Across the street, a screen displays an AI-generated copy of the mural, dry and perfect. The copy lacks the rain running through the original's colors.",
    "cn-live-musician": "A small stage in a dimly lit venue, a figure mid-performance, sweat visible, a broken string dangling from the instrument. The audience is small but every person leans forward, connected. A flawless AI jukebox sits in the corner, unplugged and gathering dust. The wrong notes in the performance make the room breathe.",
    "cn-poet": "A figure at a tiny desk, a single poem handwritten on paper, ink still wet. The poem is short — maybe eight lines. Pinned to the wall behind the desk, a printout shows '4 BILLION AI POEMS GENERATED TODAY.' The handwritten poem has a coffee ring on it. Someone crossed out a word and chose a better one.",
    "cn-indie-filmmaker": "A cramped editing room, a figure hunched over a laptop, footage playing on a tiny screen. A budget sheet taped to the wall shows $12,000 total. Through the window, a billboard advertises 400,000 AI-generated films released this week. The figure's footage is shaky and imperfect and clearly shot by someone who cared.",
    "cn-handwritten-letter": "A writing desk with a single letter in progress, ink pen resting on unfinished cursive. The letter is personal and specific — names, memories, crossings-out where the writer chose better words. Through the window, a digital billboard shows the day's message volume: 847 billion. The letter will reach one person. It will matter.",

    # ── SET 12 CREATOR.NULL LEGENDARIES ──
    "cn-ghost-artist": "An art gallery with paintings on every wall, each one labeled 'AI-Generated' on its placard. In a back room visible through an open door, a figure sits surrounded by the actual canvases, paint on their clothes, brushes in a jar. The gallery credits and the painter are in different rooms entirely. The painter's name appears nowhere.",
    "cn-voice-actor": "A recording booth with a single microphone, a figure's headshot on the wall showing the original session. Outside the booth, 14,000 speakers play the cloned voice simultaneously in different products, advertisements, and announcements. A royalty check on the booth's desk reads zero. The consent form on the wall covers one advertisement only.",
    "cn-session-musician": "A recording studio with instruments on stands — guitar, keyboard, bass, drums — and a figure playing one of them with visible mastery. A calendar on the wall shows only four bookings this year, the other slots filled with 'AI SESSION.' Two hundred album credits hang framed on the wall, all from years past.",

    # ── SET 12 CREATOR.NULL RARES ──
    "cn-stock-photo": "A wall of 400 million generated faces displayed on screens, scrolling infinitely. In front of the wall, a real model's headshot sits in a dataset folder labeled 'TRAINING DATA — NO CONSENT REQUIRED.' A portfolio of the model's paid work sits in a drawer, replaced by infinite free alternatives that look just like them.",
    "cn-ghostwriter": "A bookshelf displaying seven bestselling novels, each one with a famous author's name on the spine. Behind the bookshelf, accessible through a hidden door, a figure sits in a tiny room surrounded by manuscript drafts. The figure's name appears on nothing. A new AI writing tool sits on the famous author's desk, replacing even the ghost.",
    "cn-music-producer": "A bedroom with production equipment — keyboard, monitors, headphones — and 47 finished tracks displayed on a screen. A streaming platform counter shows 340 monthly listeners. Through the wall, the platform's main page shows 100,000 AI tracks uploaded today, burying the 47 human tracks beneath an avalanche of algorithmic content.",
    "cn-concept-artist": "A portfolio display showing 400 pieces of concept art, each one detailed and original. A scanner in the corner has digitized every piece into a training dataset. The studio that commissioned the portfolio now uses an AI trained on this exact work. A termination letter sits on the artist's desk, thanking them for their 'contribution.'",

    # ── SET 12 CREATOR.NULL UNCOMMONS ──
    "cn-content-mill": "A factory floor with 200 human writers at desks, dwarfed by a massive printing press behind them that produces 40,000 articles per day automatically. The human writers' rate cards show $0.001 per word. The printing press has no rate card — it runs for free. The exit door has a line forming.",
    "cn-ai-cover-band": "A concert stage where holographic performers play every hit song ever written, the audience enormous and cheering. Backstage, a royalty distribution machine shows $0 flowing to the original artists. The holograms are perfect copies. The original musicians watch from a TV in a small apartment, seeing their work performed without them.",
    "cn-ai-screenwriter": "A script printing machine churning out screenplays at industrial speed, 4,000 per day stacking up in towers. A producer picks through the pile, each script feeling identical. A wastebasket overflows with screenplays that had a human voice. The produced films all share the same three-act structure and the same hollow center.",
    "cn-art-thief": "A massive vacuum cleaner the size of a building, its hose sweeping across the internet, sucking up 5.8 billion images from portfolios, galleries, and personal websites. The images swirl inside the machine and emerge transformed. A 'FAIR USE' label is stamped on the vacuum. Zero consent forms feed into the intake.",

    # ── SET 12 CREATOR.NULL COMMONS ──
    "cn-ai-art-gen": "A firehose spraying 800 million images per day onto an endless canvas that stretches to the horizon. The images are polished and immediate. In the corner of the canvas, a human artist's original work — the piece the AI trained on — sits in a small frame, unsigned and uncompensated. An art contest trophy sits atop the firehose.",
    "cn-ai-music-gen": "An infinite jukebox with a million songs loaded daily, each slot filled with AI-generated tracks. A streaming chart on the wall shows the top 100 — none made by humans. A real musician's guitar case sits open on the sidewalk outside, a few coins inside. The jukebox plays their style without them.",
    "cn-ai-novel": "A bookstore where every shelf is stacked with identical-looking novels, 40,000 new titles per month. A search function on a kiosk cannot find human-authored books — they are buried beneath the volume. A reader holds up one AI novel and one human novel side by side, trying to tell which is which.",

    # ── SET 12 CREATOR.NULL JUNK ──
    "cn-nft-artist": "A gallery opening where digital frames display NFT art, each one with a dramatic price tag — $4.2 million at the peak. A 'CURRENT VALUE: $47' sticker covers each original price. The artist stands in the corner, still posting daily to an empty room. The gallery is hosting a different exhibition next week.",
    "cn-linkedin-thought": "A social media feed displayed on a giant screen, showing three daily posts — all generated by AI, liked by AI, and commented on by AI. The engagement metrics are impressive but every interaction is synthetic. A human scrolls past without reading. The word 'AGREE?' appears at the end of every post.",
    "cn-ai-collab": "A keyboard with a single key glowing — the Enter key — labeled 'CO-CREATOR.' A prompt of twelve words sits in a text field above a canvas of stunning AI-generated artwork. The credit reads 'Human + AI Collaboration.' The human contribution is the twelve words. The AI contribution is everything visible.",
}
# fmt: on


def build_prompt(scene: str) -> str:
    return STYLE_PREFIX + scene


def generate_card(client: OpenAI, card_id: str, scene: str, output_dir: Path) -> bool:
    """Generate a single card image. Returns True on success."""
    out_path = output_dir / f"{card_id}.png"
    if out_path.exists():
        log.info("SKIP %s (already exists)", card_id)
        return True

    prompt = build_prompt(scene)
    log.info("GENERATING %s ...", card_id)

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",
            response_format="b64_json",
        )
    except Exception as e:
        log.error("FAILED %s: %s", card_id, e)
        return False

    import base64

    image_data = base64.b64decode(response.data[0].b64_json)
    out_path.write_bytes(image_data)
    log.info("SAVED %s (%d bytes)", card_id, len(image_data))
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate AI Cards TCG art via DALL-E 3")
    parser.add_argument("--card-id", help="Generate a single card by ID")
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        log.error("OPENAI_API_KEY env var not set")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    # Output dir relative to script location's parent (project root)
    project_root = Path(__file__).resolve().parent.parent
    output_dir = project_root / "images" / "cards"
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.card_id:
        if args.card_id not in CARD_SCENES:
            log.error("Unknown card ID: %s", args.card_id)
            log.info("Available IDs: %s", ", ".join(sorted(CARD_SCENES.keys())))
            sys.exit(1)
        generate_card(client, args.card_id, CARD_SCENES[args.card_id], output_dir)
        return

    # Batch mode — all cards
    total = len(CARD_SCENES)
    success = 0
    skipped = 0
    failed = 0

    log.info("Generating %d cards → %s", total, output_dir)

    for i, (card_id, scene) in enumerate(CARD_SCENES.items(), 1):
        out_path = output_dir / f"{card_id}.png"
        if out_path.exists():
            skipped += 1
            log.info("[%d/%d] SKIP %s", i, total, card_id)
            continue

        ok = generate_card(client, card_id, scene, output_dir)
        if ok:
            success += 1
        else:
            failed += 1

        # Rate limit: 1 request per 3 seconds (skip delay on last item)
        if i < total:
            time.sleep(3)

    log.info("DONE — %d generated, %d skipped, %d failed (of %d total)", success, skipped, failed, total)


if __name__ == "__main__":
    main()
