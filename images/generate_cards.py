#!/usr/bin/env python3
"""Batch-generate satirical card art for AI Cards TCG using DALL-E 3.

Usage:
    python3 images/generate_cards.py                    # all 162 cards
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
