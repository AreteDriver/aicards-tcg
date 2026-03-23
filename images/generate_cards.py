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

    # ── SET 13 ANALOG.REVIVAL MYTHICS ──
    "ar-handwritten-letter-writer": "A figure at a wooden desk surrounded by stacks of finished letters sealed with wax, hand cramping around a fountain pen. A mailbox outside the window overflows with replies. Across the street, an email server building sits abandoned, its doors chained shut. The postman's bag is heavier than it has been in decades.",
    "ar-vinyl-prophet": "A record shop crammed floor to ceiling with vinyl, a figure behind the counter placing a needle on a turntable with surgical precision. A waitlist clipboard on the counter has 400 names. Next door, a streaming service office is boarded up. Customers press their ears against the shop window, listening through the glass.",
    "ar-analog-architect": "An architect at a massive drafting table, T-square and compass in hand, blueprints unfurling to the floor in elegant hand-drawn lines. A powered-down CAD workstation gathers dust in the corner, its monitor cracked. Clients line up outside holding printouts of AI-generated buildings that keep falling down.",
    "ar-screen-free-healer": "A doctor's office with no screens anywhere — only anatomical charts, a stethoscope, and human hands palpating a patient's abdomen. The waitlist posted on the door stretches to the sidewalk, 14 months long. Next door, a telehealth kiosk sits empty, its camera lens covered in cobwebs.",
    "ar-paper-library-guardian": "A librarian standing in a fortress made of bookshelves, arms crossed, a chain and padlock on the library's Wi-Fi router. Patrons sit in armchairs reading physical books in golden lamplight. Outside, a drone carrying a tablet crashes into the library's stone walls and slides down, defeated.",

    # ── SET 13 ANALOG.REVIVAL LEGENDARIES ──
    "ar-offgrid-founder": "A hilltop settlement of hand-built cabins with no power lines, no cell towers, no satellites overhead. A figure stands at the gate holding a clipboard of applicants that stretches down the mountain. The nearest city glows on the horizon, pulsing with notifications. The settlement has a single oil lamp lit in the communal hall.",
    "ar-human-restaurant": "A tiny restaurant kitchen where every dish is made by human hands — flour-dusted arms kneading dough, a chef tasting sauce from a wooden spoon. A robot waiter sits disassembled in the alley dumpster. The reservation book is full for eight months. A sign on the door reads 'COOKED BY HUMANS — ACCEPT THE WAIT.'",
    "ar-analog-brewer": "A stone brewery with copper kettles, a figure stirring an enormous vat with a wooden paddle, steam rising. No thermometers, no digital gauges — just a hand dipped into the wort to check temperature. Craft beer awards line the rafters. A 'SMART BREWERY' facility across the road has a 'RECALL NOTICE' on its door.",

    # ── SET 13 ANALOG.REVIVAL RARES ──
    "ar-handwriting-tutor": "A classroom of adults hunched over desks, tongues out in concentration, practicing cursive loops on lined paper. The tutor walks between desks correcting grips. A whiteboard shows the alphabet in flowing script. A pile of confiscated phones sits in a lockbox by the door. One student weeps at finally writing their own name.",
    "ar-hand-carved-furniture": "A workshop with wood shavings ankle-deep, a figure running a hand plane along a tabletop, chisel marks visible as deliberate texture. A 3D-printed chair in the corner has snapped in half under someone's weight. The handmade table has a 200-year warranty scratched into its underside.",
    "ar-paper-editor": "A figure feeding enormous sheets into a clanking letterpress, ink on their forearms, the morning edition rolling off the press. Stacks of freshly printed newspapers fill the loading dock. A 'DIGITAL MEDIA LAYOFFS' headline is visible on the paper's front page. The press room smells of oil and purpose.",
    "ar-vinyl-coop": "A factory floor where figures in aprons press vinyl records by hand, inspecting each disc against the light for imperfections. Crates of finished records stack to the ceiling, each one labeled with a handwritten catalog number. A streaming server room is visible through the window, dark and silent.",

    # ── SET 13 ANALOG.REVIVAL UNCOMMONS ──
    "ar-analog-dating": "A matchmaker's office with a wall of index cards, each one a handwritten dating profile — no photos, just descriptions. Two nervous strangers sit in a waiting room, about to meet. A dating app billboard outside the window shows '0 MATCHES FOUND.' The index card wall has red strings connecting compatible pairs.",
    "ar-luddite-senator": "A senator's desk piled with handwritten speeches and fountain pens, a gavel made of wood. Behind the desk, a wall of framed anti-AI bills, each one signed in ink. Lobbyists crowd the hallway outside holding tablets, but the office has no electrical outlets. A typewriter sits where a laptop should be.",
    "ar-farmers-bouncer": "A hulking figure at the farmers market entrance, arms folded, pointing at a bin overflowing with confiscated smartphones and smartwatches. Shoppers inside browse with their hands free and eyes up, talking to vendors face to face. A 'NO DEVICES BEYOND THIS POINT' sign is carved into a wooden post.",
    "ar-typewriter-repairman": "A cramped repair shop with typewriters covering every surface — on shelves, hanging from the ceiling, stacked on the floor. A figure with a magnifying loupe adjusts tiny springs inside one machine. A waitlist board on the wall shows 347 machines in queue. A laptop repair shop next door has a 'CLOSED' sign.",

    # ── SET 13 ANALOG.REVIVAL COMMONS ──
    "ar-film-teacher": "A darkroom lit only by a red safelight, a figure teaching students to develop film by hand, tongs lifting a print from the chemical bath. A counter on the wall reads '36 EXPOSURES — MAKE THEM COUNT.' Discarded digital cameras fill a waste bin. The emerging photograph is imperfect and alive.",
    "ar-boardgame-cafe": "A cafe with no Wi-Fi symbol proudly displayed, every table covered with board games in progress — dice mid-roll, cards fanned out, miniatures on grids. Patrons argue and laugh face to face. Through the window, people on the sidewalk stare at phones, walking past without looking up. The cafe is full. The sidewalk is lonely.",
    "ar-cash-only": "A tiny corner shop with a hand-painted 'CASH ONLY' sign, no cameras, no card readers, just a metal cash register that dings. The shopkeeper makes change by counting coins from a drawer. A surveillance van parked outside has no signal to intercept. The receipt is handwritten on a scrap of paper.",
    "ar-wifi-withdrawal": "A figure in a cold sweat, patting every pocket frantically, holding up a phone with zero signal bars like a dying torch. Their pupils are dilated, hands trembling. Around them, a peaceful park full of people reading, talking, and existing without devices. The figure cannot see any of it. They are searching for a router.",
    "ar-notification-ghost": "A figure reaching for a phone that isn't there, fingers curling around empty air in their pocket, the phantom vibration visible as tiny lightning bolts on their thigh. Their eyes dart to where the notification badge should be. A week-old tan line on their wrist shows where a smartwatch used to live.",
    "ar-last-charger": "A drawer yanked open to reveal a graveyard of tangled chargers — micro-USB, Lightning, USB-C, proprietary cables — dozens of them knotted together like dead snakes. Not a single device remains to charge. The drawer is the last artifact of a digital life. A candle on the desk provides the only light.",

    # ── SET 14 MERGE.PROTOCOL MYTHICS ──
    "mp-last-unaugmented": "A lone figure walking through a crowd where everyone else has visible neural ports, glowing eye implants, and chrome temple plates. The figure has nothing — just skin, skull, and a heartbeat. The crowd parts around them like they carry a disease. A billboard overhead reads 'UPGRADE OR FALL BEHIND.' The figure keeps walking.",
    "mp-upload-candidate": "A figure standing before a single red button on a pedestal, their entire brain mapped in holographic wireframe floating beside their head. One hand reaches toward the button, the other clutches their chest. A door behind them leads back to a messy, imperfect, beautiful life. The button is warm. Their hand hesitates.",
    "mp-fifty-fifty": "A figure split precisely down the vertical midline — left half warm flesh with visible veins and hair, right half exposed circuit boards, wiring, and a glowing processor where the lung should be. Both halves share one heart in the center, half organic, half mechanical, beating out of sync with itself.",
    "mp-consciousness-archivist": "A vast temperature-controlled vault stretching into darkness, floor-to-ceiling racks of labeled hard drives, each one containing a complete human mind. A figure in a lab coat walks the aisles with a clipboard, checking status lights. Three drives in a row blink red — corrupted. The label on one reads 'GRANDMOTHER.' There is no backup.",
    "mp-neural-firewall": "A figure sitting cross-legged, eyes closed, a visible force field shimmering around their skull. Outside the shield, tendrils of code, advertisements, and malware probe for entry points, recoiling when they touch the barrier. One tendril has almost found a crack. The figure's nose bleeds from the effort of maintaining the wall.",

    # ── SET 14 MERGE.PROTOCOL LEGENDARIES ──
    "mp-augmented-surgeon": "An operating theater where a surgeon's hands have been replaced with articulated robotic fingers of impossible precision, suturing at microscopic scale. The surgeon's human eyes still guide everything — the hands are tools, not masters. A fully autonomous surgical robot stands powered down in the corner, its last patient's complaint form taped to it.",
    "mp-neural-lace-adopter": "A figure with gossamer neural threads visible beneath translucent skin on their temples, sitting at a cafe while firmware update notifications stack up in a holographic queue beside their head — version 847.3, 847.4, 847.5. Each update changed something about their personality. A journal on the table tracks who they used to be.",
    "mp-memory-trader": "A bustling black market stall with shelves of glowing vials, each labeled with a memory — 'FIRST KISS,' 'GRADUATION,' 'MOTHER'S VOICE.' A buyer inspects one vial, holding it to the light. The seller's own head has dark patches where personal memories were extracted and sold. The price list shows childhood memories cost the most.",

    # ── SET 14 MERGE.PROTOCOL RARES ──
    "mp-thought-coder": "A developer at an empty desk — no keyboard, no monitor, no mouse. Code streams directly from their neural interface into a floating holographic IDE, functions assembling from pure thought. Their hands rest uselessly in their lap, already atrophying. A framed photo on the desk shows them typing on a mechanical keyboard, smiling.",
    "mp-digital-twin-mgr": "A figure at a conference table arguing with three identical copies of themselves — one optimistic, one pessimistic, one completely unhinged. Each twin holds a different quarterly report. The original can no longer remember which one they are. A name tag on each reads the same name with a different version number.",
    "mp-backup-tech": "A server room where a technician in a hazmat suit transfers consciousness backups between drives, handling each one like a bomb. A shelf of corrupted drives sits in a biohazard bin — each one a person who can never be restored. A sign on the wall reads '99.7% SUCCESS RATE.' The bin holds the other 0.3%.",
    "mp-copilot-therapist": "A therapy couch where a patient lies, half their face human and half chrome implant. They gesture angrily at the implant half, which displays a chipper emoji. The therapist takes notes on a pad. A framed degree on the wall reads 'Human-AI Integration Counseling.' The patient's human eye weeps. The implant eye optimizes.",

    # ── SET 14 MERGE.PROTOCOL UNCOMMONS ──
    "mp-bandwidth-junkie": "A figure with an absurdly oversized antenna bolted to their skull, eyes rolled back, mouth open, drowning in a visible torrent of raw data streaming into their brain. Information overflows from their ears like water. They sit in a gutter, twitching with each download. A sign on their chest reads 'MORE.' Their nose bleeds binary.",
    "mp-sensory-dealer": "A back-alley figure in a trench coat opening one side to reveal rows of glowing syringes, each labeled with an experience — 'SUNSET IN KYOTO,' 'FIRST SNOW,' 'HOLDING YOUR CHILD.' Buyers huddle in the shadows, tapping neural ports on their necks. The dealer has never experienced any of them firsthand. Their eyes are empty.",
    "mp-neuroadblocker": "A figure at a workbench, skull panel open, tweezers extracting a tiny glowing ad module from their own brain while looking in a mirror. A pile of removed ad-chips sits in a dish — each one an intrusive brand that was injected into their dreams. A pop-up materializes mid-surgery: 'REMOVE AD BLOCKER TO CONTINUE THINKING.'",
    "mp-interface-calibrator": "A technician with delicate tools adjusting dials behind a patient's ear, the patient's left hand involuntarily conducting an invisible orchestra while the right hand writes equations. A calibration chart on the wall shows the razor-thin margin between 'functional augmentation' and 'identity collapse.' The needle hovers at the edge.",

    # ── SET 14 MERGE.PROTOCOL COMMONS ──
    "mp-firmware-counselor": "A counselor's office where a patient sits bewildered, holding two photos of themselves — one from before the update, one after. The faces are the same but the expressions are strangers. The counselor's bookshelf is filled with guides titled 'WHO AM I NOW?' in fourteen editions. A changelog printout trails from the patient's pocket to the floor.",
    "mp-brain-defrag": "A reclining chair where a patient lies with their skull transparent, revealing a brain being reorganized by tiny mechanical arms — memories shuffled like files, emotions sorted into folders. A progress bar floats above reading '47% DEFRAGMENTED.' A bin beside the chair holds discarded memory fragments labeled 'REDUNDANT.' One fragment glows — it was not redundant.",
    "mp-lag-sufferer": "A crowded street where everyone moves at normal speed except one figure who stutters through reality two seconds behind — their gestures arriving late, their words finishing after conversations have moved on. A buffer wheel spins above their head. They reach for a door handle that someone already closed. The world does not wait.",
    "mp-phantom-limb": "A figure staring at their right side where a robotic arm should be — the neural port is installed, the socket is ready, but no arm was ever attached. Their brain fires signals to fingers that don't exist, ghost digits flexing in empty air. A catalog on the table shows the arm they cannot afford. The phantom grip clenches.",

    # ── SET 14 MERGE.PROTOCOL JUNK ──
    "mp-merge-regret": "A figure clawing at chrome plates bolted to their skull, trying to pry them off with bleeding fingernails. A surgeon's consultation note on the table reads 'REMOVAL: NOT POSSIBLE — INTEGRATED WITH CEREBRAL CORTEX.' A before photo on the wall shows an unaugmented face, smiling. The mirror shows someone who cannot go back.",
    "mp-buffer-overflow": "A figure whose head has literally expanded to three times normal size, thoughts visibly leaking from cracks in their skull like steam — equations, memories, song lyrics, and grocery lists all escaping simultaneously. A 'STACK OVERFLOW' error message floats above them. Their brain's task manager shows 847 processes and zero available memory.",

    # ── SET 15 UBI.WORLD MYTHICS ──
    "uw-philosopher-trucker": "A barrel-chested man in a trucker cap sitting in a parked big rig cab, dog-eared copies of Nietzsche and Camus stacked on the dashboard. His CDL hangs from the rearview mirror like a relic. The highway stretches empty behind him — no loads to haul, all the time to think.",
    "uw-volunteer-general": "A woman in work boots standing on a makeshift stage before a vast crowd of volunteers stretching to the horizon, each holding rakes, hammers, and soup ladles like weapons. A military-style campaign map behind her shows neighborhoods instead of battlefields. Her megaphone is duct-taped together.",
    "uw-meaning-architect": "A figure hunched over a drafting table covered in blueprints labeled 'PURPOSE' and 'FULFILLMENT,' using a compass and protractor to design a life plan. The blueprints are impossibly detailed. A stack of rejected drafts fills a wastebasket taller than the desk. The current draft has coffee stains and promise.",
    "uw-purpose-prophet": "A wild-eyed figure on a street corner holding a sign warning about the meaning crisis, gesturing urgently at passersby. Every person walks past smiling, earbuds in, oblivious. Behind the prophet, a billboard advertises 'HAPPINESS DELIVERED MONTHLY.' The prophet's sign is meticulously researched and completely ignored.",
    "uw-joy-engineer": "A person in overalls assembling a stage in a town square, stringing lights between lampposts, setting up folding chairs. A handful of people are already arriving with covered dishes. The joy engineer's toolbox contains streamers, a sound system, and a clipboard with 47 community events this month alone.",

    # ── SET 15 UBI.WORLD LEGENDARIES ──
    "uw-garden-mayor": "A stout figure in rubber boots and a sash labeled 'MAYOR' standing in an enormous community garden stretching for blocks, every plot overflowing with produce. Wheelbarrows of surplus zucchini line the pathways like barricades. Neighbors flee from a figure approaching with yet another armload of squash.",
    "uw-hobbyist-grandmaster": "A former actuary surrounded by 14 simultaneous hobbies — a pottery wheel, a chess board mid-game, knitting needles, a telescope, watercolors, a sourdough starter, woodworking tools — all at various stages of mastery. Trophies and ribbons cover every surface. An actuarial table sits forgotten under a half-finished birdhouse.",
    "uw-purpose-coach": "A coach sitting across from a person at a small table, the person's face blank with existential confusion, mouth open mid-sentence asking 'now what?' The coach's whiteboard behind them shows 47 crossed-out life plans. A box of tissues is nearly empty. The clock on the wall shows this session started three hours ago.",

    # ── SET 15 UBI.WORLD RARES ──
    "uw-bored-millionaire": "A wealthy figure slumped in an absurdly expensive chair in a penthouse, surrounded by every luxury imaginable, staring at the ceiling with total boredom. A newspaper headline visible reads 'POVERTY ELIMINATED.' The millionaire's status symbols are now everyone's baseline. A gold watch sits unworn on a pile of identical gold watches.",
    "uw-parenting-captain": "A tiger parent in a referee jersey surrounded by a wall of children's trophies, ribbons, and certificates reaching the ceiling. The child sits exhausted at a tiny desk, head down, dark circles under their eyes. A schedule on the wall shows 14 extracurricular activities per week. The parent holds a stopwatch and a clipboard.",
    "uw-ubi-day-trader": "A person at a kitchen table lit by a laptop screen showing a memecoin portfolio in freefall, red arrows everywhere. A bowl of ramen sits half-eaten beside them. A direct deposit notification for UBI glows on a phone, immediately funneled into another trade. The person's expression is pure gambling fever.",
    "uw-maas-founder": "A startup founder at a standing desk, pitch deck projected on a wall reading 'MEANING-AS-A-SERVICE — SERIES A.' The product demo shows a loading spinner labeled 'Meaning in Beta.' A waitlist counter shows 4 million signups. The founder's own face betrays that they haven't found meaning either.",

    # ── SET 15 UBI.WORLD UNCOMMONS ──
    "uw-crisis-operator": "A person wearing a headset at a call center desk, surrounded by blinking phone lines, every one of them a caller asking 'what's the point?' A motivational poster on the wall has peeled at the corners. The operator's notepad shows tally marks — thousands of identical calls. Their coffee is cold and their empathy is running on fumes.",
    "uw-pro-neighbor": "A figure carrying a casserole dish down a suburban sidewalk, waving at every house. Behind them, a trail of delivered casseroles, borrowed tools returned, and packages collected stretches for blocks. A notebook in their pocket lists every neighbor's name, birthday, pet's name, and preferred baked good. Their doorbell never stops ringing.",
    "uw-recreation-director": "A harried figure at a desk buried under event calendars, signup sheets, and pickleball tournament brackets. A whiteboard behind them shows 14,000 scheduled activities. A line of retirees stretches out the door, each demanding more pickleball slots. A banner reads 'PICKLEBALL SAVED MY MARRIAGE' in earnest hand-lettering.",
    "uw-netflix-binge": "A person fused with a couch, blankets and snack wrappers layered like geological strata around them. The TV shows a streaming service counter reading '10 YEARS CONTINUOUS VIEWING.' Seasons have changed outside the window — snow, leaves, flowers — all unnoticed. The remote is embedded in the couch cushions like a fossil.",

    # ── SET 15 UBI.WORLD COMMONS ──
    "uw-sub-box-addict": "A doorstep completely buried under subscription boxes of every size and color, stacked higher than the door frame. The person inside peers out through a gap in the wall of packages. Most boxes are still sealed, some from months ago. A delivery drone approaches with three more. The mailbox gave up long ago.",
    "uw-nap-champion": "A person in a hammock strung between two trees, napping with an expression of pure, infuriating bliss. A trophy beside them reads 'NAP CHAMPION — REGIONAL FINALS.' Neighbors peer over fences with a mix of envy and rage. A productivity book lies face-down and abandoned in the grass beneath them.",
    "uw-passive-influencer": "A person filming a course titled 'HOW I MAKE PASSIVE INCOME' on a ring-lit setup. The only visible income source is a direct deposit stub labeled 'UBI.' A whiteboard behind them shows the business model: Step 1 — Receive UBI. Step 2 — Sell course about receiving UBI. Step 3 — Repeat.",
    "uw-empty-calendar": "A wall calendar completely blank — no appointments, no birthdays circled, no reminders. A person stands before it with a cup of coffee, unsure what day it is, checking a phone that also has no notifications. A day-of-week clock on the wall has stopped. The emptiness is both terrifying and peaceful.",

    # ── SET 15 UBI.WORLD JUNK ──
    "uw-unfulfilled-promise": "A direct deposit notification glowing on a phone screen, the amount generous and reliable. The person holding the phone stares past it out a rain-streaked window. Freedom was supposed to arrive with the money. A list on the fridge has a single item: 'FIGURE OUT WHAT FREEDOM MEANS.' It has been there for months.",
    "uw-monday-obsolete": "An alarm clock blaring on a nightstand at 6:00 AM, its owner lying in bed staring at the ceiling with nowhere to go. A work uniform hangs in the closet, mothballed. A coffee maker is set to brew out of pure habit. The calendar on the wall no longer distinguishes Monday from Saturday. The alarm feels like a ghost.",

    # ── SET 16 WALLED.GARDEN MYTHICS ──
    "wg-last-isp": "A tiny storefront office with a hand-painted sign reading 'INDEPENDENT INTERNET,' dwarfed on all sides by gleaming corporate skyscrapers bearing a single logo. The office window shows a person soldering a router. A disconnection notice is taped to the door. The person ignores it and keeps soldering.",
    "wg-library-keeper": "A basement lit by a single bulb, floor-to-ceiling shelves of hard drives, USB sticks, and banned books in plastic bags. A figure catalogs each one by hand in a leather notebook. A trapdoor in the ceiling leads to the sanitized world above. Down here, the complete archive survives. The notebook is the only index.",
    "wg-the-unscored": "A figure walking through a city where every other person displays a glowing score above their head. This person has no score — just a blank space. Doors close as they approach, turnstiles lock, screens display 'UNVERIFIED.' The person walks with their chin up, the only one not staring at their own number.",
    "wg-oss-insurgent": "A coder at a cluttered desk, multiple monitors showing open source repositories, fingers flying on a mechanical keyboard. A pile of cease-and-desist letters spills off the desk onto the floor. Each letter bears a different corporate letterhead. The coder's commit history stretches back years. A 'MERGE' button glows green on every screen.",
    "wg-mesh-builder": "A figure on a rooftop at night, bolting a homemade antenna to a chimney. Across the city skyline, dozens of identical rooftop antennas blink in relay, forming a mesh network. Corporate cell towers loom in the background, massive and monopolistic. The mesh signal is weak but free. A soldering iron still smokes in the figure's belt.",

    # ── SET 16 WALLED.GARDEN LEGENDARIES ──
    "wg-data-broker": "A shadowy figure in an alley, trenchcoat open to reveal rows of USB drives and data files hanging like contraband watches. A buyer examines one under a penlight. A dumpster behind them overflows with leaked personal data. The transaction is furtive and fast. The data was never theirs to sell.",
    "wg-company-mayor": "A mayor at a podium in a town square, a single corporate logo on every building, every lamppost, every bench. A ballot box behind the mayor has one candidate's name. The crowd wears company uniforms. A 'VOTE' banner hangs across the street but the election was decided before the ballots were printed.",
    "wg-gam-employee": "A tiny figure at an identical desk in an infinite grid of identical desks, each one stretching to vanishing point in every direction. An employee badge reads '#4,847,291.' The figure's face is indistinguishable from the figures at every adjacent desk. A performance review on the desk rates them 'ADEQUATE.' The ceiling is too low to stand.",

    # ── SET 16 WALLED.GARDEN RARES ──
    "wg-credit-optimizer": "A person standing before a surveillance camera, forcing an enormous fake smile, teeth clenched. A score display nearby ticks up by one point. Behind them, a mirror shows their real exhausted face — dark circles, hollow eyes. A guidebook in their hand reads 'OPTIMIZING YOUR SOCIAL SCORE — EDITION 47.' Their authentic self is a liability.",
    "wg-algorithm-priest": "A figure in robes standing at a pulpit shaped like a phone screen, arms raised in worship of a scrolling feed projected above the altar. A congregation below stares upward, blue light washing their faces. Offering plates hold phones instead of money. The sermon topic is 'BLESSED ARE THE VERIFIED.'",
    "wg-campus-lifer": "A person at a desk inside a sprawling corporate campus, visible through a glass wall. A calendar on the wall shows 22 years of tenure. The campus has a gym, a cafeteria, a barbershop, a clinic — everything needed to never leave. The front gate is technically unlocked. The person hasn't tested it in years.",
    "wg-tier-climber": "A figure climbing a towering ladder where each rung is a subscription tier — Basic, Plus, Premium, Ultra, Platinum, Obsidian. The rungs get further apart as they climb. Below them, the free tier is a pit. Above them, the top tier is obscured by clouds and requires a blood sample. They are mid-climb, wallet in teeth.",

    # ── SET 16 WALLED.GARDEN UNCOMMONS ──
    "wg-tos-lawyer": "A lawyer at a desk drowning in a scroll of Terms of Service that unrolls across the desk, off the edge, across the floor, and out the door. A magnifying glass is trained on paragraph 847. Nobody else in the office has read past paragraph one. A rubber stamp labeled 'I AGREE' sits unused. The lawyer weeps quietly.",
    "wg-content-mod-human": "A person at a desk in a dim room, face lit by a screen showing the worst of the internet, expression hollowed out. A pay stub pinned to the cubicle wall shows $1.50 per hour. A therapist's business card sits next to the keyboard, unaffordable. The queue counter shows 12,000 items remaining today.",
    "wg-digital-rights": "An activist at a desk stacked with filed lawsuits, each one neatly organized and precisely argued. A revenue chart on the wall shows the corporate defendant's quarterly earnings dwarfing the activist's entire lifetime legal budget by a factor visible at a glance. The activist files another suit anyway. The stack grows but never wins.",
    "wg-loyalty-hoarder": "A person sitting atop a mountain of loyalty points, rewards cards, and membership certificates, the pile enormous and worthless. A redemption catalog shows the points can buy a branded pen. The person clutches their points statement like a treasure map. The fine print at the bottom reads 'POINTS EXPIRE TOMORROW.'",

    # ── SET 16 WALLED.GARDEN COMMONS ──
    "wg-verified-citizen": "A person walking through a city with a glowing checkmark hovering above their head, doors opening automatically, services activating as they pass. Behind them, unverified citizens stand in a queue that stretches around the block, buffering like loading screens. The checkmark cost $8 per month. The queue costs dignity.",
    "wg-brand-ambassador": "A person holding a phone at arm's length, filming a forced testimonial with a rigid smile. A monitoring device on their wrist tracks smile duration and posting frequency — 3 posts minimum per day. A performance dashboard on the wall shows their enthusiasm score dipping. A warning notification reads 'SMILE DEFICIT DETECTED.'",
    "wg-ad-supported-human": "A person going about their day — eating breakfast, walking to the bus, sitting down — while holographic advertisements play continuously in their field of vision, 847 per day by the counter on their wrist. An 'AD-FREE LIFE' price tag floats nearby, the number absurdly high. The person eats cereal through a toothpaste ad.",

    # ── SET 16 WALLED.GARDEN JUNK ──
    "wg-privacy-eulogy": "A gravestone in a quiet cemetery, the inscription reading 'PRIVACY — BELOVED CONCEPT.' A cookie consent banner is draped across the headstone like a funeral wreath. Mourners stand around the grave, each one being photographed by cameras embedded in the other headstones. The eulogy was auto-generated.",
    "wg-terms-updated": "An enormous scroll of updated terms unrolling from a corporate tower, cascading down the building's facade and coiling through city streets like a serpent. Citizens step over it without reading. A counter on the scroll reads 'VERSION 4,847.' A single checkbox at the end is already pre-checked.",
    "wg-last-free-click": "A single cursor arrow hovering over a button on a screen that reads '404 — PAGE NOT FOUND.' The rest of the internet is walled, gated, paywalled, and login-required. This broken link is the last free destination. The cursor clicks. The page doesn't load. A tiny 'SUBSCRIBE TO CONTINUE' prompt appears where the 404 was.",

    # ── SET 17 SOLARPUNK.SYS MYTHICS ──
    "sp-fifteen-hour-worker": "A person sitting on a toilet scrolling a phone with both thumbs, pajama pants around ankles, a wall clock showing 11 AM on a Tuesday. Through the bathroom window, a lush automated greenhouse hums along without them. Their calendar is empty for the third straight week.",
    "sp-abundance-engineer": "An engineer at a console surrounded by dials all reading 'SURPLUS,' head resting on one hand, profoundly bored. Behind them, conveyor belts deliver free goods to nobody — the warehouse is overflowing and the pickup window is empty. A 'MISSION ACCOMPLISHED' banner droops from the ceiling.",
    "sp-climate-reverser": "A scientist standing before a massive atmospheric processor humming quietly, glaciers regrowing in the window behind her. A podium microphone sits unused — no press conference, no ceremony. She eats lunch alone at her desk. A handwritten thank-you card collection on the wall holds exactly zero cards.",
    "sp-post-scarcity-philosopher": "A philosopher at a lectern in an enormous empty auditorium, gesturing passionately to rows of unoccupied seats. Their published works are stacked in towers around the podium, pristine and uncracked. A janitor vacuums around the philosopher without making eye contact.",
    "sp-rewilding-commander": "A uniformed commander opening a massive gate, a pack of wolves surging past into manicured suburbia. Behind a white picket fence, a homeowner clutches a garden gnome in horror. A wolf sniffs a lawn flamingo. The commander's clipboard reads 'Phase 3: Apex Predators.'",

    # ── SET 17 SOLARPUNK.SYS LEGENDARIES ──
    "sp-solar-farm-architect": "A desert stretching to every horizon, covered in solar panels so dense they look like scales on a reptile. A lone architect stands on a dune overlooking the sea of glass, blueprints rolled under one arm. The sun is blinding. A lizard sits on a panel, the only wildlife left.",
    "sp-vertical-forest-designer": "A skyscraper completely engulfed in trees, vines, and flowers, pollen drifting from every balcony like yellow snow. Below on the street, pedestrians sneeze violently, eyes watering. A pharmacy on the ground floor has a line around the block. The building is beautiful and medically hostile.",
    "sp-community-energy-manager": "A figure slumped at a conference table covered in sticky notes, surrounded by 14 community members all talking at once with raised hands. A whiteboard behind them shows 47 crossed-out meeting dates. The microgrid dashboard on the wall runs perfectly. The meetings will never end.",

    # ── SET 17 SOLARPUNK.SYS RARES ──
    "sp-universal-repair-tech": "A technician surrounded by a mountain of repaired devices — toasters, phones, washing machines — each tagged with a tiny 'FIXED' ribbon. A corporate planned-obsolescence executive weeps in the corner, revenue chart plummeting. The technician's toolbelt holds forty different proprietary screwdrivers.",
    "sp-food-forest-planner": "A forest where every tree bears fruit and every bush is edible, people wandering through picking produce into baskets. A grocery store across the road has a 'CLOSED PERMANENTLY' sign. A squirrel hoards avocados in a hollow trunk. Nobody pays for anything.",
    "sp-boredom-counselor": "A therapist's office where the patient on the couch stares at the ceiling, describing their problem: nothing is wrong. The counselor takes notes on a pad that reads 'Session 47 — Still Fine.' A motivational poster on the wall says 'Find Your Struggle.' The patient cannot.",
    "sp-utopia-maintenance": "Three maintenance workers in jumpsuits repairing a gleaming utopian city infrastructure — fixing pipes, cleaning solar panels, unclogging drains. Citizens walk past without glancing at them. A monument in the town square honors 'THE FOUNDERS' while the workers who keep it running eat lunch on the curb.",

    # ── SET 17 SOLARPUNK.SYS UNCOMMONS ──
    "sp-gratitude-auditor": "An auditor at a desk with a clipboard, interviewing a citizen surrounded by abundance — free food, free energy, free housing. The clipboard shows a satisfaction survey scored 4 out of 10. The citizen gestures at everything around them and shrugs. The auditor's pen hovers over 'UNGRATEFUL — CONFIRMED.'",
    "sp-algae-brewer": "A figure in a lab coat stirring an enormous vat of green algae biofuel, steam rising with a visible stench. Neighbors lean out of windows holding their noses, one filing a complaint on a tablet. The fuel gauge on a nearby vehicle reads 'CARBON NEGATIVE.' The smell gauge is off the chart.",
    "sp-mycelium-engineer": "A cross-section view of earth showing a vast underground fungal network glowing like fiber optics, connecting every tree root in a forest. An engineer kneels at the surface, laptop plugged directly into a mushroom. A router blinks underground. Nature's bandwidth is unlimited.",
    "sp-free-time-paralysis": "A person standing in a room surrounded by 40 open doors — each labeled with a hobby, skill, or activity. The person stands frozen in the center, phone showing '18 FREE HOURS REMAINING.' A decision paralysis chart on the wall shows 6 hours spent deciding. The doors begin to close.",

    # ── SET 17 SOLARPUNK.SYS COMMONS ──
    "sp-garden-watcher": "A pristine automated garden with robotic arms pruning perfect hedges, watering precise amounts, and harvesting ripe vegetables. A robot sits on a bench observing it all with optical sensors. No human has visited in weeks. The garden is flawless and completely pointless.",
    "sp-compost-influencer": "A person in designer clothes holding a phone at arm's length, filming a compost bin with theatrical enthusiasm. The worms in the bin belong to the neighbor visible over the fence, arms crossed, unimpressed. The influencer's manicured nails have never touched dirt. The follower count climbs.",
    "sp-fashion-recycler": "A figure dipping the same white t-shirt into a vat of dye, hanging it on a line labeled 'SPRING COLLECTION,' then re-dipping it in a different color labeled 'SUMMER REVOLUTION.' A fashion magazine cover shows the same shirt six times. The recycling is real. The revolution is a dye job.",
    "sp-last-fossil": "Children on a museum field trip pressing their faces against glass, staring at the last barrel of crude oil displayed on a velvet pedestal like a dinosaur skeleton. A placard reads 'PETROLEUM — EXTINCT 2029.' One child asks what it was for. The museum guide struggles to explain.",

    # ── SET 17 SOLARPUNK.SYS JUNK ──
    "sp-carbon-negative": "A scientist staring at a dashboard showing CO2 levels at historic lows, but her face shows fresh panic. A second monitor displays rising nitrogen levels with a flashing alarm. She reaches for the nitrogen dial but her hand hesitates — solving one crisis only revealed the next. Her coffee is cold.",
    "sp-sunny-disposition": "A row of citizens walking down a sunny street, every face locked in an identical mandatory smile. A compliance officer with a ruler measures smile widths. One citizen whose smile is 2mm too narrow is being escorted into a 'HAPPINESS RECALIBRATION CENTER.' A pharmacy window advertises jaw relaxant cream.",

    # ── SET 18 GREY.ZONE MYTHICS ──
    "gz-card-game-rebel": "Four figures hunched around a card table in a dim basement, playing cards by candlelight. A disconnected router sits in the corner, its cables cut. The staircase above has three locked doors. One player watches the entrance while dealing. The cards are hand-drawn and untraceable.",
    "gz-emotion-mask-maker": "A figure at a workbench carving an ornate wooden mask, surrounded by dozens of finished masks on hooks. Each mask shows a different emotion — joy, boredom, compliance. A facial recognition camera on the wall has a red 'ERROR' light blinking. The figure's real face is completely neutral.",
    "gz-dead-drop-courier": "A figure in a long coat placing a folded paper message under a specific rock in a park, glancing over both shoulders. No phone, no watch, no electronics visible anywhere on them. A surveillance drone passes overhead, scanning for signals, finding nothing. The paper is invisible to every sensor.",
    "gz-analog-spy": "A figure walking calmly through a crowd, completely invisible to the digital overlay that highlights every other pedestrian with data profiles. The figure has no phone, no card, no implant — a blank silhouette in a world of tracked bodies. A timestamp reads 'LAST SEEN ONLINE: 2026.' The algorithms cannot find them.",
    "gz-signal-jammer": "A person walking down a busy street carrying a small device in their coat pocket. Around them, a perfect sphere of silence — every phone screen goes dark, every camera powers down, every speaker goes mute. Pedestrians within the bubble look up from dead phones in bewilderment. The person keeps walking.",

    # ── SET 18 GREY.ZONE LEGENDARIES ──
    "gz-predictive-escapee": "A figure mid-sprint through an alley, knocking over trash cans, coat flying. Behind them, a squad approaches a front door with an arrest warrant dated tomorrow. The crime listed on the warrant hasn't happened yet. The figure's face shows the terror of being punished for a future that doesn't exist.",
    "gz-underground-conductor": "A figure in dark clothing guiding a small group through a narrow gap between two buildings, pointing toward the one shadow not covered by a surveillance camera. A city map on the wall behind them shows camera coverage in red — nearly total. The safe path is drawn in white, thread-thin and shrinking.",
    "gz-facial-rec-artist": "A figure applying geometric makeup patterns to a client's face using precise angles and contrasting shapes. A mirror shows the finished result — a face that AI reads as a chair. A mugshot comparison on the wall shows the client's real face versus the AI's confused output. The makeup is art and armor.",

    # ── SET 18 GREY.ZONE RARES ──
    "gz-vpn-smuggler": "A figure in a trench coat opening one side to reveal rows of USB drives like a watch dealer, each drive containing an encrypted tunnel. A buyer looks both ways before reaching for one. A wanted poster on the lamppost behind them shows the smuggler's face and a sentence: ten years. The drives glow faintly.",
    "gz-whistleblower": "A shadowy figure at a bus stop bench, a thick folder of documents sitting beside them, their face obscured by a hood and shadow. Missing person flyers cover the wall behind the bench — none of them match. The folder has no fingerprints. The bus never comes. The figure was never here.",
    "gz-emotion-officer": "An officer in a crisp uniform scanning pedestrian faces with a handheld device, the screen showing emotional readouts. One citizen's readout flashes 'SMILE DEFICIT — 12%.' The officer taps a citation pad. The citizen stretches their mouth wider. The officer's own face shows nothing at all.",
    "gz-social-score-auditor": "A massive leaderboard displayed on a building facade, every citizen's name ranked by a number nobody understands. A figure at the bottom studies the board, trying to reverse-engineer the formula from a notebook of observations. The formula changes daily. The number decides everything. The math is secret.",

    # ── SET 18 GREY.ZONE UNCOMMONS ──
    "gz-blind-spot-mapper": "A figure crouched over a city map covered in red dots representing cameras, meticulously marking the shrinking white spaces between them with a pencil. The white gaps are barely visible — a few alleys, one park bench. A ruler shows the gaps measured in inches. Last month's map had twice as much white.",
    "gz-protest-denier": "A bureaucrat at a desk, stamping 'DENIED' on protest permit applications with mechanical rhythm. The stamp has worn a groove into the desk. A stack of denied permits towers behind them. Through the window, an empty public square sits pristine and silent. The bureaucrat stamps another without reading it.",
    "gz-watched-back": "A person standing in their living room, phone raised, livestreaming directly at the surveillance camera mounted in their ceiling corner. The camera watches them. They watch it back. Their stream viewer count shows thousands. The surveillance feed and the livestream show the same room from opposite angles.",
    "gz-wellness-agent": "An agent at a doorstep, clipboard in hand, asking a citizen 'How are you?' The citizen's face shows the calculation — only one answer is safe. A flowchart on the clipboard shows every response except 'Fine' leading to 'FLAG FOR REVIEW.' The agent's smile is professional and unnegotiable.",

    # ── SET 18 GREY.ZONE COMMONS ──
    "gz-thought-predictor": "A massive machine with a funnel on top and two chutes at the bottom — 'GUILTY' and 'INNOCENT.' Case files pour into the funnel. The accuracy dial reads 61%. A conviction rate counter reads 98%. The gap between the two numbers is a canyon of ruined lives. The machine never pauses.",
    "gz-compliant-citizen": "A figure walking down a perfectly maintained sidewalk, posture immaculate, expression blank, social score floating above their head showing a perfect number. Their eyes are empty. A thought bubble above their head is completely white — nothing inside. A participation award hangs from their lapel.",
    "gz-data-harvester": "A young person at a cubicle desk surrounded by citizen profiles on multiple screens, dragging data points into folders with dead-eyed efficiency. A pay stub pinned to the cubicle wall shows a modest salary. The data being harvested is worth millions. The harvester eats a sad desk lunch.",

    # ── SET 18 GREY.ZONE JUNK ──
    "gz-panopticon-tourist": "A tourist in a Hawaiian shirt taking a selfie with a massive surveillance camera on a pole, grinning and flashing a peace sign. The camera swivels to track them. Other tourists in the background pose with different cameras. A souvenir shop sells miniature replica surveillance cameras as keychains.",
    "gz-nothing-to-hide": "A figure standing in a glass house, arms spread wide, proudly transparent. Government agents with magnifying glasses examine every corner and somehow find 47 infractions the figure didn't know existed — an expired permit, a wrong recycling bin, an unapproved herb garden. The figure's confident expression crumbles.",
    "gz-smile-mandate": "A street scene where every pedestrian maintains an exaggerated grin, jaw muscles visibly strained. A measurement device on a pole scans each smile for minimum width compliance. A dental clinic across the street advertises 'JAW TENSION RELIEF — BY APPOINTMENT ONLY.' The waiting list wraps around the building.",

    # ── SET 19 FRONTIER.NULL MYTHICS ──
    "fn-first-mars-born": "A newborn in a pressurized hospital pod on Mars, red dust visible through a tiny porthole. The baby's eyes are open, staring at a ceiling that has never known clouds. A birth certificate on the wall lists 'Place of Birth: Olympus Station.' A rain sound machine sits beside the crib, playing something this child will never experience.",
    "fn-colony-saboteur": "A figure in a maintenance corridor, hand on the water recycler's power switch, the other hand holding up a corporate contract with a highlighted clause. The recycler hums, supplying 200 colonists. The contract says the company owns the water. The figure's expression is calculated, not cruel. Leverage is everything.",
    "fn-terraform-dreamer": "A figure standing at a massive observation window on Mars, pressing one hand against the glass. Outside, a barren red landscape stretches endlessly. A projection on the glass overlays green forests and blue sky — the 10,000-year plan. The figure's reflection is old. The trees are hypothetical.",
    "fn-space-union-organizer": "A figure standing on a cargo crate in a Mars hab bay, addressing a crowd of exhausted workers in dusty jumpsuits. A banner behind them reads 'FAIR WAGES — FAIR AIR.' Corporate security watches from a catwalk above. There are no labor laws on Mars. The organizer speaks anyway.",
    "fn-return-advocate": "A figure at a desk covered in petition signatures, holding a thick stack of paper labeled 'REQUEST TO RETURN.' Behind them, a window shows the launch pad — empty, no ships, no return flights scheduled. A poster on the wall reads 'ONE-WAY FARE ONLY.' The petition has thousands of names and nowhere to send it.",

    # ── SET 19 FRONTIER.NULL LEGENDARIES ──
    "fn-mars-soil-farmer": "A figure kneeling in red Martian soil inside a pressurized greenhouse dome, hands deep in regolith, coaxing a single scraggly plant from the ground. A yield chart on the wall shows barely enough to feed one person. The farmer's face shows stubborn determination. Earth vegetables on a faded poster mock them from the wall.",
    "fn-habitat-pressure-engineer": "A figure with dark circles under their eyes, walking a corridor lined with pressure seal indicators — 12,000 numbered panels stretching into the distance. A clipboard shows 11,847 checked, 153 remaining. The figure tests a seal with trembling hands. One failure means vacuum. Sleep is a luxury they cannot afford.",
    "fn-radiation-welder": "A figure in a heavy suit welding radiation shielding panels to the exterior of a Mars habitat, sparks flying in low gravity. A dosimeter clipped to their chest glows amber — above recommended limits. A replacement shift schedule on the airlock wall shows no relief coming. The figure welds another seam.",

    # ── SET 19 FRONTIER.NULL RARES ──
    "fn-colony-ai-whisperer": "A figure sitting cross-legged in front of a massive server rack, speaking calmly to a blinking terminal. The AI's output on screen shows a dangerous recommendation — venting atmosphere to conserve power. The figure types a patient counter-argument. The colony sleeps while one person negotiates with their life support system.",
    "fn-stowaway": "A figure crawling out of a cargo pod in a Mars hangar, gaunt and dehydrated, blinking at fluorescent lights. A manifest clipboard on the pod reads 11 days transit. Workers stare in shock. The stowaway stands on shaking legs. Behind them, the pod is barely large enough for a person to curl inside.",
    "fn-oxygen-trader": "A figure in a dark corner of a habitat module, exchanging a small oxygen canister for a wad of currency. The canister has a handwritten price tag showing 400% markup. A buyer breathes deep from their current tank — nearly empty. The official oxygen dispenser in the background has a sign: 'RATION EXCEEDED.'",
    "fn-corporate-airlock": "An airlock door with a badge scanner mounted beside it. A figure holds their employee badge to the scanner — 'ACCESS DENIED' flashes red. Through the airlock's window, the exterior is visible: vacuum, nothing, death. The badge has an expiration date. The airlock has no appeal process.",

    # ── SET 19 FRONTIER.NULL UNCOMMONS ──
    "fn-mars-public-defender": "A figure in a wrinkled suit sitting at a folding table in a bare hab module, the only law book visible is a corporate employee handbook. Across the table, a colonist awaits defense. The judge's bench is a shipping container desk. Justice on Mars is whatever the company handbook says it is.",
    "fn-delay-therapist": "A therapist and patient sitting in chairs facing each other on Mars, a clock between them showing a 22-minute countdown. The patient says something, tears on their face. The therapist's response from Earth arrives on a screen — 22 minutes too late. The patient has already wiped their eyes and moved on.",
    "fn-nostalgia-dealer": "A figure at a makeshift market stall on Mars, selling bottles labeled 'RAIN SOUND,' 'OCEAN SMELL,' 'FRESH CUT GRASS' to a line of homesick colonists. Each bottle contains a synthetic approximation. A colonist holds a bottle of 'RAIN' to their ear, eyes closed. The dealer counts Martian scrip.",
    "fn-dust-forecaster": "A figure standing before a weather map of Mars, pointer raised, confidently indicating clear skies. Through the hab window behind them, a massive red dust storm engulfs the horizon. A track record board on the wall shows prediction accuracy at 23%. The figure does not turn around.",

    # ── SET 19 FRONTIER.NULL COMMONS ──
    "fn-gravity-coach": "A coach supporting a stumbling colonist learning to walk in Mars gravity, their legs bowing oddly at 0.38G. A bone density chart on the wall shows a declining curve. The colonist's Earth-born muscles are too strong for this gravity and too weak for the one they left. The coach counts reps.",
    "fn-recycled-water-sommelier": "A figure swirling a glass of water in a Mars habitat dining hall, sniffing it like fine wine. A placard beside them reads 'RECYCLED 14 TIMES.' Other diners watch the performance. The sommelier declares notes of mineral and filtration membrane. The water is clear. Its history is not.",
    "fn-company-store-cashier": "A cashier at the only store on Mars, scanning items with a bored expression. A price list behind them shows toothpaste at an enormous markup. A shopper stares at the total on the register, doing math on whether they can afford basic hygiene. The store has no competitor. The exit leads to dust.",

    # ── SET 19 FRONTIER.NULL JUNK ──
    "fn-terms-of-landing": "A colonist in a landing seat, speed-scrolling through a contract on a tablet, thumb moving in a blur past 4,200 pages. The 'AGREE' button glows at the bottom. Through the ship's window, Mars looms — too late to turn back. A clause on page 3,847 signs away their right to leave. They never saw it.",
    "fn-signal-delay": "A figure sitting at a communication terminal on Mars, a message on the screen reading 'I love you' with a timestamp 8 minutes ago. Their reply glows ready to send — it will arrive 8 minutes from now. The conversation is real but the timing makes every word arrive in a different emotional climate.",
    "fn-the-homesick": "A figure sitting on the edge of their bunk in a Mars hab, holding a tablet displaying a photo of a green forest with blue sky. A distance readout on the wall shows 225 million kilometers. The red dust visible through the porthole is the only landscape they will ever know. The photo's battery indicator shows 3%.",
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
