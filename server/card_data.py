"""Card pool data matching the frontend CARDS array.
Only stores the metadata needed for minting — the frontend has the full flavor text.
"""

import random

# Rarity weights — same as frontend WEIGHTS
WEIGHTS = {
    "MYTHIC": 1,
    "LEGENDARY": 300,
    "RARE": 1000,
    "UNCOMMON": 2200,
    "COMMON": 4000,
    "JUNK": 2500,
}

# Expansion sets get boosted mythic rate (5x) so players can complete sets and progress
SET_WEIGHTS = {
    "MYTHIC": 5,
    "LEGENDARY": 300,
    "RARE": 1000,
    "UNCOMMON": 2200,
    "COMMON": 4000,
    "JUNK": 2500,
}

# Card pool — minimal data for minting
# Format: (card_id, name, rarity, category, set_name, kscore, atk, def, symbol)
# Flavor text is stored on-chain but truncated for gas efficiency

CARDS: list[dict] = []


def _add(card_id: str, name: str, rarity: str, category: str, set_name: str,
         kscore: str, atk: str, defense: str, symbol: str, series: str | None = None,
         flavor: str = ""):
    CARDS.append({
        "card_id": card_id,
        "name": name,
        "rarity": rarity,
        "category": category,
        "set": set_name,
        "kscore": kscore,
        "atk": atk,
        "def": defense,
        "symbol": symbol,
        "series": series,
        "flavor": flavor[:200],  # Truncate for gas
        "number": len(CARDS) + 1,
    })


# ═══ SET 1: 2030 SURVIVAL (49 cards, no series tag) ═══
_add("plumber", "THE PLUMBER", "LEGENDARY", "Human Trade", "2030 Survival", "2", "550K", "SHORTAGE", "🔧")
_add("electrician", "THE ELECTRICIAN", "LEGENDARY", "Human Trade", "2030 Survival", "2", "79K", "SHORTAGE", "⚡")
_add("welder", "THE WELDER", "LEGENDARY", "Human Trade", "2030 Survival", "1", "450K", "BACKLOG", "🔥")
_add("hvac", "THE HVAC TECH", "LEGENDARY", "Human Trade", "2030 Survival", "1", "420K", "CLIMATE", "❄️")
_add("midwife", "THE MIDWIFE", "LEGENDARY", "Human Trade", "2030 Survival", "1", "8%", "HOME BIRTHS", "🌱")
_add("seeker", "THE SEEKER", "LEGENDARY", "Human Trade", "2030 Survival", "0", "?", "UNKNOWN", "🧭")
_add("mechanic", "THE MECHANIC", "LEGENDARY", "Human Trade", "2030 Survival", "2", "780K", "BACKLOG", "🔩")
_add("carpenter", "THE CARPENTER", "LEGENDARY", "Human Trade", "2030 Survival", "1", "1M", "DEMAND", "🪚")
_add("the-crane-operator", "THE CRANE OPERATOR", "LEGENDARY", "Human Trade", "2030 Survival", "1", "98K", "SHORTAGE", "🏗️")
_add("the-gravedigger", "THE GRAVEDIGGER", "LEGENDARY", "Human Trade", "2030 Survival", "0", "∞", "DEMAND", "⚰️")

_add("priest", "THE PRIEST", "RARE", "Human Purpose", "2030 Survival", "2", "400K", "PARISHES", "✝️")
_add("therapist", "THE THERAPIST", "RARE", "Human Purpose", "2030 Survival", "4", "1M", "WAITLIST", "🧠")
_add("tattoo", "THE TATTOO ARTIST", "RARE", "Human Purpose", "2030 Survival", "1", "40K", "ARTISTS", "🖊️")
_add("farmer", "THE FARMER", "RARE", "Human Purpose", "2030 Survival", "2", "2M", "FARMS", "🌾")
_add("nurse", "THE NURSE", "RARE", "Human Purpose", "2030 Survival", "3", "4.4M", "CRITICAL", "💊")
_add("chef", "THE CHEF", "RARE", "Human Purpose", "2030 Survival", "3", "1.5M", "KITCHENS", "🔪")
_add("barber", "THE BARBER", "RARE", "Human Purpose", "2030 Survival", "1", "800K", "CHAIRS", "✂️")
_add("teacher", "THE TEACHER", "RARE", "Human Purpose", "2030 Survival", "5", "3.7M", "UNDERPAID", "📖")
_add("the-librarian", "THE LIBRARIAN", "RARE", "Human Purpose", "2030 Survival", "3", "∞", "BOOKS", "📚")
_add("the-fisherman", "THE FISHERMAN", "RARE", "Human Purpose", "2030 Survival", "1", "DAWN", "TIDES", "🎣")
_add("the-survivor", "THE SURVIVOR", "RARE", "Human Purpose", "2030 Survival", "0", "?", "UNKNOWN", "🏔️")

_add("influencer", "THE INFLUENCER", "UNCOMMON", "Society", "2030 Survival", "7", "50M", "FOLLOWERS", "📱")
_add("copywriter", "THE COPYWRITER", "UNCOMMON", "Society", "2030 Survival", "9", "300K", "REPLACED", "✍️")
_add("journalist", "THE JOURNALIST", "UNCOMMON", "Society", "2030 Survival", "8", "46K", "REMAINING", "🗞️")
_add("nomad", "THE DIGITAL NOMAD", "UNCOMMON", "Society", "2030 Survival", "7", "35M", "LAPTOPS", "🌐")
_add("accountant", "THE ACCOUNTANT", "UNCOMMON", "Society", "2030 Survival", "9", "1.4M", "AUDITED", "📊")
_add("radiologist", "THE RADIOLOGIST", "UNCOMMON", "Society", "2030 Survival", "8", "34K", "SCANNED", "🩻")
_add("translator", "THE TRANSLATOR", "UNCOMMON", "Society", "2030 Survival", "9", "300K", "TRANSLATED", "🌍")
_add("uber-driver", "THE UBER DRIVER", "UNCOMMON", "Society", "2030 Survival", "7", "340K", "DEACTIVATED", "🚗")
_add("the-hr-manager", "THE HR MANAGER", "UNCOMMON", "Society", "2030 Survival", "8", "∞", "EMAILS", "📋")
_add("the-paralegal", "THE PARALEGAL", "UNCOMMON", "Society", "2030 Survival", "9", "350K", "BILLABLE", "⚖️")
_add("the-middle-manager", "THE MIDDLE MANAGER", "UNCOMMON", "Society", "2030 Survival", "8", "∞", "MEETINGS", "💼")

_add("ai-gf", "THE AI GIRLFRIEND", "COMMON", "AI Product", "2030 Survival", "10", "14M", "DOWNLOADS", "💗")
_add("ai-bf", "THE AI BOYFRIEND", "COMMON", "AI Product", "2030 Survival", "10", "3.2M", "DOWNLOADS", "💙")
_add("virtual-life", "THE VIRTUAL LIFE", "COMMON", "AI Product", "2030 Survival", "10", "∞", "UPTIME", "🎮")
_add("digital-companion", "THE DIGITAL COMPANION", "COMMON", "AI Product", "2030 Survival", "10", "40M", "USERS", "🤖")
_add("ai-tutor", "THE AI TUTOR", "COMMON", "AI Product", "2030 Survival", "10", "200M", "STUDENTS", "📚")
_add("dating-algo", "THE DATING ALGORITHM", "COMMON", "AI Product", "2030 Survival", "10", "800M", "MATCHES", "💘")
_add("ai-therapist-app", "AI THERAPIST", "COMMON", "AI Product", "2030 Survival", "9", "14K", "SESSIONS/SEC", "🛋️")
_add("ai-pastor", "THE AI PASTOR", "COMMON", "AI Product", "2030 Survival", "10", "4M", "SERMONS", "⛪")

_add("prompt-engineer", "THE PROMPT ENGINEER", "JUNK", "Lore", "2030 Survival", "10", "0", "DEPRECATED", "💬")
_add("techno-optimist", "THE TECHNO-OPTIMIST", "JUNK", "Lore", "2030 Survival", "∞", "∞", "COPE", "🚀")
_add("ai-doomer", "THE AI DOOMER", "JUNK", "Lore", "2030 Survival", "∞", "∞", "DOOM", "☠️")
_add("vc", "THE VC", "JUNK", "Lore", "2030 Survival", "∞", "10B", "AUM", "💰")
_add("regulator", "THE REGULATOR", "JUNK", "Lore", "2030 Survival", "∞", "0", "LAWS PASSED", "🏛️")
_add("linkedin-guru", "THE LINKEDIN GURU", "JUNK", "Lore", "2030 Survival", "∞", "10M", "IMPRESSIONS", "🤝")
_add("the-content-farm", "THE CONTENT FARM", "JUNK", "Lore", "2030 Survival", "∞", "50K", "ARTICLES/DAY", "🏭")
_add("the-retraining-program", "THE RETRAINING PROGRAM", "JUNK", "Lore", "2030 Survival", "∞", "312", "PLACED", "🎓")
_add("speciation-pressure", "SPECIATION PRESSURE", "JUNK", "Lore", "2030 Survival", "∞", "2-3", "GENERATIONS", "🧬")


# ═══ SET 2: JOBLESS.AI (series="jobless") ═══

# — Mythic —
_add("the-mother", "THE MOTHER", "MYTHIC", "Irreplaceable", "Jobless.ai", "0", "∞", "∞", "💫", series="jobless")
_add("the-organ-donor", "THE ORGAN DONOR", "MYTHIC", "Irreplaceable", "Jobless.ai", "0", "∞", "∞", "❤️", series="jobless")
_add("the-revolutionary", "THE REVOLUTIONARY", "MYTHIC", "Irreplaceable", "Jobless.ai", "0", "∞", "∞", "🔥", series="jobless")
_add("the-bone-marrow-match", "THE BONE MARROW MATCH", "MYTHIC", "Irreplaceable", "Jobless.ai", "0", "∞", "∞", "🧬", series="jobless")
_add("the-first-responder", "THE FIRST RESPONDER", "MYTHIC", "Irreplaceable", "Jobless.ai", "0", "∞", "∞", "🚒", series="jobless")

# — Legendary (Karpathy Scores) —
_add("the-roofer", "THE ROOFER", "LEGENDARY", "Karpathy Scores", "Jobless.ai", "2", "148K", "ROOFTOPS", "🏠", series="jobless")
_add("the-ironworker", "THE IRONWORKER", "LEGENDARY", "Karpathy Scores", "Jobless.ai", "1", "65K", "STEEL BEAMS", "🔩", series="jobless")
_add("the-firefighter-ks", "THE FIREFIGHTER", "LEGENDARY", "Karpathy Scores", "Jobless.ai", "3", "345K", "ON CALL", "🧯", series="jobless")

# — Legendary (JobGone) —
_add("the-workday-cut", "WORKDAY", "LEGENDARY", "JobGone", "Jobless.ai", "∞", "1,750", "IRONIC", "🔄", series="jobless")
_add("the-meta-purge", "THE META PURGE", "LEGENDARY", "JobGone", "Jobless.ai", "∞", "16K", "HUMANS OUT", "👁️", series="jobless")

# — Rare (Karpathy Scores) —
_add("the-dental-hygienist", "THE DENTAL HYGIENIST", "RARE", "Karpathy Scores", "Jobless.ai", "2", "$94K", "SALARY", "🦷", series="jobless")
_add("the-airline-pilot", "THE AIRLINE PILOT", "RARE", "Karpathy Scores", "Jobless.ai", "5", "$198K", "MEDIAN PAY", "✈️", series="jobless")

# — Rare (JobGone) —
_add("the-atlassian-cut", "THE ATLASSIAN CUT", "RARE", "JobGone", "Jobless.ai", "∞", "1,600", "TICKETS CLOSED", "📋", series="jobless")
_add("the-logistics-wave", "THE LOGISTICS WAVE", "RARE", "JobGone", "Jobless.ai", "∞", "4,000", "OPTIMIZED OUT", "📦", series="jobless")

# — Uncommon (Karpathy Scores) —
_add("the-financial-analyst-ks", "THE FINANCIAL ANALYST", "UNCOMMON", "Karpathy Scores", "Jobless.ai", "9", "429K", "EXPOSED", "📈", series="jobless")
_add("the-csr", "THE CUSTOMER SERVICE REP", "UNCOMMON", "Karpathy Scores", "Jobless.ai", "9", "2.8M", "ON THE LINE", "🎧", series="jobless")
_add("the-graphic-designer-ks", "THE GRAPHIC DESIGNER", "UNCOMMON", "Karpathy Scores", "Jobless.ai", "8", "287K", "PORTFOLIOS", "🎨", series="jobless")

# — Uncommon (JobGone) —
_add("the-495k", "THE 495K", "UNCOMMON", "JobGone", "Jobless.ai", "∞", "496K", "AND COUNTING", "📊", series="jobless")
_add("the-direct-attribution", "THE DIRECT ATTRIBUTION", "UNCOMMON", "JobGone", "Jobless.ai", "∞", "60+", "SAID IT", "🎯", series="jobless")
_add("the-vercel-nine", "THE VERCEL NINE", "UNCOMMON", "JobGone", "Jobless.ai", "∞", "9", "PEOPLE", "▲", series="jobless")

# — Common —
_add("the-bookkeeper", "THE BOOKKEEPER", "COMMON", "Karpathy Scores", "Jobless.ai", "9", "1.6M", "DECLINING", "📒", series="jobless")
_add("the-severance-package", "THE SEVERANCE PACKAGE", "COMMON", "JobGone", "Jobless.ai", "∞", "3", "WEEKS", "✉️", series="jobless")

# — Junk —
_add("the-karpathy-score", "THE KARPATHY SCORE", "JUNK", "Lore · Karpathy", "Jobless.ai", "∞", "342", "OCCUPATIONS", "🗺️", series="jobless")
_add("the-tracker", "THE TRACKER", "JUNK", "Lore · JobGone", "Jobless.ai", "∞", "∞", "UPDATES", "🔍", series="jobless")
_add("march-2026", "MARCH 2026", "JUNK", "Lore · JobGone", "Jobless.ai", "∞", "35K", "THIS MONTH", "📅", series="jobless")


# ═══ SET 3: DOOMSCROLL (series="doomscroll") ═══

# — Mythic —
_add("ds-whistleblower", "THE WHISTLEBLOWER", "MYTHIC", "Irreplaceable", "DOOMSCROLL", "0", "∞", "∞", "📡", series="doomscroll")
_add("ds-war-correspondent", "THE WAR CORRESPONDENT", "MYTHIC", "Irreplaceable", "DOOMSCROLL", "0", "∞", "∞", "📸", series="doomscroll")
_add("ds-analog-parent", "THE ANALOG PARENT", "MYTHIC", "Irreplaceable", "DOOMSCROLL", "0", "∞", "∞", "🌿", series="doomscroll")
_add("ds-indie-journalist", "THE INDEPENDENT JOURNALIST", "MYTHIC", "Irreplaceable", "DOOMSCROLL", "0", "∞", "∞", "✍️", series="doomscroll")
_add("ds-attention-span", "THE ATTENTION SPAN", "MYTHIC", "Irreplaceable", "DOOMSCROLL", "0", "∞", "∞", "⏳", series="doomscroll")

# — Legendary —
_add("ds-investigative", "THE INVESTIGATIVE JOURNALIST", "LEGENDARY", "Human · Media", "DOOMSCROLL", "1", "3", "PULITZERS", "🔍", series="doomscroll")
_add("ds-news-anchor", "THE LOCAL NEWS ANCHOR", "LEGENDARY", "Human · Media", "DOOMSCROLL", "3", "22", "YEARS", "📺", series="doomscroll")
_add("ds-print-editor", "THE PRINT EDITOR", "LEGENDARY", "Human · Media", "DOOMSCROLL", "2", "1847", "KILLED STORIES", "📰", series="doomscroll")

# — Rare —
_add("ds-fact-checker", "THE FACT-CHECKER", "RARE", "Society · Media", "DOOMSCROLL", "8", "142K", "VERIFIED", "✅", series="doomscroll")
_add("ds-media-literacy", "THE MEDIA LITERACY TEACHER", "RARE", "Human · Education", "DOOMSCROLL", "4", "12K", "TAUGHT", "🎓", series="doomscroll")
_add("ds-librarian-stayed", "THE LIBRARIAN WHO STAYED", "RARE", "Human · Knowledge", "DOOMSCROLL", "3", "∞", "BOOKS", "📚", series="doomscroll")
_add("ds-the-source", "THE SOURCE", "RARE", "Human · Intelligence", "DOOMSCROLL", "1", "?", "CLASSIFIED", "🕶️", series="doomscroll")

# — Uncommon —
_add("ds-doomscroller", "THE DOOMSCROLLER", "UNCOMMON", "Society · Digital", "DOOMSCROLL", "6", "7.2", "HRS/DAY", "📱", series="doomscroll")
_add("ds-algorithm", "THE ALGORITHM", "UNCOMMON", "AI · System", "DOOMSCROLL", "10", "4K", "INVISIBLE", "🤖", series="doomscroll")
_add("ds-headline-writer", "THE HEADLINE WRITER", "UNCOMMON", "Society · Media", "DOOMSCROLL", "9", "0", "SECONDS READ", "📢", series="doomscroll")
_add("ds-notification", "THE NOTIFICATION", "UNCOMMON", "AI · System", "DOOMSCROLL", "10", "847", "PER DAY", "🔔", series="doomscroll")

# — Common —
_add("ds-deepfake", "THE DEEPFAKE", "COMMON", "AI Product", "DOOMSCROLL", "10", "94→11", "% DETECTION", "🎭", series="doomscroll")
_add("ds-ai-anchor", "THE AI ANCHOR", "COMMON", "AI Product", "DOOMSCROLL", "10", "24/7", "NEVER BLINKS", "📡", series="doomscroll")
_add("ds-content-mill", "THE CONTENT MILL", "COMMON", "AI Product", "DOOMSCROLL", "10", "400", "PER DAY", "🏭", series="doomscroll")

# — Junk —
_add("ds-misinfo", "THE MISINFORMATION", "JUNK", "Lore · Doomscroll", "DOOMSCROLL", "∞", "4.2M", "SHARES", "🦠", series="doomscroll")
_add("ds-conspiracy", "THE CONSPIRACY THEORIST", "JUNK", "Lore · Doomscroll", "DOOMSCROLL", "7", "1", "IN 10,000", "👁️", series="doomscroll")
_add("ds-tos", "THE TERMS OF SERVICE", "JUNK", "Lore · Doomscroll", "DOOMSCROLL", "∞", "74,000", "WORDS", "📜", series="doomscroll")


# ═══ SET 4: LOVE.EXE (series="loveexe") ═══

# — Mythic —
_add("lx-marriage", "THE MARRIAGE THAT LASTED", "MYTHIC", "Irreplaceable", "LOVE.EXE", "0", "∞", "∞", "💍", series="loveexe")
_add("lx-handwritten-letter", "THE HANDWRITTEN LETTER", "MYTHIC", "Irreplaceable", "LOVE.EXE", "0", "∞", "∞", "✉️", series="loveexe")
_add("lx-eye-contact", "THE EYE CONTACT", "MYTHIC", "Irreplaceable", "LOVE.EXE", "0", "∞", "∞", "👁️", series="loveexe")
_add("lx-forgiveness", "THE FORGIVENESS", "MYTHIC", "Irreplaceable", "LOVE.EXE", "0", "∞", "∞", "🕊️", series="loveexe")
_add("lx-grandparent", "THE GRANDPARENT", "MYTHIC", "Irreplaceable", "LOVE.EXE", "0", "∞", "∞", "👴", series="loveexe")

# — Legendary —
_add("lx-last-first-date", "THE LAST FIRST DATE", "LEGENDARY", "Human · Connection", "LOVE.EXE", "1", "147", "ATTEMPTS", "🌹", series="loveexe")
_add("lx-couples-therapist", "THE COUPLE'S THERAPIST", "LEGENDARY", "Human · Purpose", "LOVE.EXE", "2", "2K", "SAVED", "💬", series="loveexe")
_add("lx-single-father", "THE SINGLE FATHER", "LEGENDARY", "Human · Purpose", "LOVE.EXE", "0", "4AM", "YOUTUBE TUTORIALS", "👨‍👧", series="loveexe")

# — Rare —
_add("lx-pen-pal", "THE PEN PAL", "RARE", "Human · Connection", "LOVE.EXE", "1", "342", "LETTERS", "✏️", series="loveexe")
_add("lx-wingman", "THE WINGMAN", "RARE", "Human · Social", "LOVE.EXE", "2", "47", "INTRODUCTIONS", "🤝", series="loveexe")
_add("lx-long-distance", "THE LONG DISTANCE", "RARE", "Human · Connection", "LOVE.EXE", "3", "4200", "MILES", "🌍", series="loveexe")
_add("lx-divorce-lawyer", "THE DIVORCE LAWYER", "RARE", "Human · Purpose", "LOVE.EXE", "4", "800", "ENDINGS", "⚖️", series="loveexe")

# — Uncommon —
_add("lx-situationship", "THE SITUATIONSHIP", "UNCOMMON", "Society · Digital", "LOVE.EXE", "6", "7", "MONTHS OF NOTHING", "🔄", series="loveexe")
_add("lx-parasocial", "THE PARASOCIAL", "UNCOMMON", "Society · Digital", "LOVE.EXE", "8", "4.2M", "FOLLOWERS", "📱", series="loveexe")
_add("lx-40yo-profile", "THE 40-YEAR-OLD PROFILE", "UNCOMMON", "Society · Digital", "LOVE.EXE", "7", "47", "BIO REWRITES", "📋", series="loveexe")
_add("lx-ghosted", "THE GHOSTED", "UNCOMMON", "Society · Digital", "LOVE.EXE", "6", "7", "UNANSWERED", "👻", series="loveexe")

# — Common —
_add("lx-ai-matchmaker", "THE AI MATCHMAKER", "COMMON", "AI Product", "LOVE.EXE", "10", "800M", "MATCHES", "💻", series="loveexe")
_add("lx-swipe", "THE SWIPE", "COMMON", "AI Product", "LOVE.EXE", "10", "140", "PER SESSION", "👆", series="loveexe")
_add("lx-read-receipt", "THE READ RECEIPT", "COMMON", "AI Product", "LOVE.EXE", "10", "∞", "ANXIETY", "✓✓", series="loveexe")

# — Junk —
_add("lx-body-count", "THE BODY COUNT", "JUNK", "Lore · Love.exe", "LOVE.EXE", "∞", "0", "USEFUL ANSWERS", "🔢", series="loveexe")
_add("lx-what-are-we", 'THE "WHAT ARE WE"', "JUNK", "Lore · Love.exe", "LOVE.EXE", "∞", "∞", "AVOIDED", "❓", series="loveexe")
_add("lx-love-tos", "THE DATING APP T&C", "JUNK", "Lore · Love.exe", "LOVE.EXE", "∞", "∞", "CLAUSES", "📄", series="loveexe")


# ═══ SET 5: WAR ROOM (series="warroom") ═══

# — Mythic —
_add("wr-peace-negotiator", "THE PEACE NEGOTIATOR", "MYTHIC", "Irreplaceable", "WAR ROOM", "0", "∞", "∞", "🕊️", series="warroom")
_add("wr-refugee", "THE REFUGEE", "MYTHIC", "Irreplaceable", "WAR ROOM", "0", "∞", "∞", "🚶", series="warroom")
_add("wr-objector", "THE CONSCIENTIOUS OBJECTOR", "MYTHIC", "Irreplaceable", "WAR ROOM", "0", "∞", "∞", "✋", series="warroom")
_add("wr-war-orphan", "THE WAR ORPHAN", "MYTHIC", "Irreplaceable", "WAR ROOM", "0", "∞", "∞", "🧸", series="warroom")
_add("wr-veteran", "THE VETERAN", "MYTHIC", "Irreplaceable", "WAR ROOM", "0", "∞", "∞", "🎖️", series="warroom")

# — Legendary —
_add("wr-drone-pilot", "THE DRONE PILOT", "LEGENDARY", "Human · Warfare", "WAR ROOM", "3", "7000", "MILES AWAY", "🎮", series="warroom")
_add("wr-cyber-commander", "THE CYBER COMMANDER", "LEGENDARY", "Human · Warfare", "WAR ROOM", "2", "4700", "SYSTEMS DOWN", "💻", series="warroom")
_add("wr-war-correspondent-v2", "THE WAR CORRESPONDENT", "LEGENDARY", "Human · Purpose", "WAR ROOM", "1", "847", "STORIES FILED", "📹", series="warroom")

# — Rare —
_add("wr-diplomat", "THE DIPLOMAT", "RARE", "Human · Governance", "WAR ROOM", "3", "23", "CRISES AVERTED", "🏛️", series="warroom")
_add("wr-sanctions-analyst", "THE SANCTIONS ANALYST", "RARE", "Human · Governance", "WAR ROOM", "5", "140", "PACKAGES", "📊", series="warroom")
_add("wr-peacekeeper", "THE PEACEKEEPER", "RARE", "Human · Purpose", "WAR ROOM", "2", "18", "MONTHS IN HELL", "🪖", series="warroom")
_add("wr-intel-officer", "THE INTELLIGENCE OFFICER", "RARE", "Human · Purpose", "WAR ROOM", "4", "12K", "REPORTS", "🕵️", series="warroom")

# — Uncommon —
_add("wr-autonomous-weapon", "THE AUTONOMOUS WEAPON", "UNCOMMON", "AI · Warfare", "WAR ROOM", "10", "0.003", "SECONDS TO KILL", "🤖", series="warroom")
_add("wr-propaganda-bot", "THE PROPAGANDA BOT", "UNCOMMON", "AI · Warfare", "WAR ROOM", "10", "840K", "FAKE ACCOUNTS", "📢", series="warroom")
_add("wr-draft-lottery", "THE DRAFT LOTTERY", "UNCOMMON", "Society · Warfare", "WAR ROOM", "6", "14M", "NAMES DRAWN", "🎰", series="warroom")
_add("wr-proxy-war", "THE PROXY WAR", "UNCOMMON", "Society · Warfare", "WAR ROOM", "7", "2", "SPONSORS", "♟️", series="warroom")

# — Common —
_add("wr-killer-drone", "THE KILLER DRONE", "COMMON", "AI Product", "WAR ROOM", "10", "$6K", "PER UNIT", "✈️", series="warroom")
_add("wr-surveillance-state", "THE SURVEILLANCE STATE", "COMMON", "AI Product", "WAR ROOM", "10", "1.4", "CAMERAS EACH", "👁️", series="warroom")
_add("wr-cyber-attack", "THE CYBER ATTACK", "COMMON", "AI Product", "WAR ROOM", "10", "14K", "ATTACKS/YR", "💀", series="warroom")

# — Junk —
_add("wr-arms-dealer", "THE ARMS DEALER", "JUNK", "Lore · War Room", "WAR ROOM", "∞", "∞", "REVENUE", "💰", series="warroom")
_add("wr-war-profiteer", "THE WAR PROFITEER", "JUNK", "Lore · War Room", "WAR ROOM", "∞", "340%", "RETURNS", "📈", series="warroom")
_add("wr-geneva-suggestion", "THE GENEVA SUGGESTION", "JUNK", "Lore · War Room", "WAR ROOM", "∞", "4", "SUGGESTIONS", "📜", series="warroom")


# ═══ SET 6: SKILLS.VOID (series="skillsvoid") ═══

# — Mythic —
_add("sv-apprentice", "THE APPRENTICE", "MYTHIC", "Irreplaceable", "SKILLS.VOID", "0", "∞", "∞", "🔨", series="skillsvoid")
_add("sv-mentor", "THE MENTOR", "MYTHIC", "Irreplaceable", "SKILLS.VOID", "0", "∞", "∞", "🧓", series="skillsvoid")
_add("sv-autodidact", "THE AUTODIDACT", "MYTHIC", "Irreplaceable", "SKILLS.VOID", "0", "∞", "∞", "📚", series="skillsvoid")
_add("sv-trades-teacher", "THE TRADES TEACHER", "MYTHIC", "Irreplaceable", "SKILLS.VOID", "0", "∞", "∞", "⚙️", series="skillsvoid")
_add("sv-night-school", "THE NIGHT SCHOOL STUDENT", "MYTHIC", "Irreplaceable", "SKILLS.VOID", "0", "∞", "∞", "🌙", series="skillsvoid")

# — Legendary —
_add("sv-phd", "THE PhD (UNEMPLOYED)", "LEGENDARY", "Human · Knowledge", "SKILLS.VOID", "4", "12", "YEARS WASTED?", "🎓", series="skillsvoid")
_add("sv-master-craftsman", "THE MASTER CRAFTSMAN", "LEGENDARY", "Human · Trade", "SKILLS.VOID", "1", "30", "YEARS", "🏺", series="skillsvoid")
_add("sv-cc-professor", "THE COMMUNITY COLLEGE PROF", "LEGENDARY", "Human · Purpose", "SKILLS.VOID", "2", "180", "STUDENTS", "🏫", series="skillsvoid")

# — Rare —
_add("sv-bootcamp-grad", "THE BOOTCAMP GRAD", "RARE", "Human · Tech", "SKILLS.VOID", "6", "12", "WEEKS", "💻", series="skillsvoid")
_add("sv-career-counselor", "THE CAREER COUNSELOR", "RARE", "Human · Purpose", "SKILLS.VOID", "4", "3200", "CLIENTS", "🧭", series="skillsvoid")
_add("sv-tenured-professor", "THE TENURED PROFESSOR", "RARE", "Human · Knowledge", "SKILLS.VOID", "3", "11", "YEARS TO SAFETY", "📖", series="skillsvoid")
_add("sv-union-rep", "THE UNION REP", "RARE", "Human · Purpose", "SKILLS.VOID", "3", "4800", "WORKERS", "✊", series="skillsvoid")

# — Uncommon —
_add("sv-linkedin-otw", "THE LINKEDIN OPEN-TO-WORK", "UNCOMMON", "Society · Digital", "SKILLS.VOID", "8", "847", "APPLICATIONS", "🟢", series="skillsvoid")
_add("sv-cert-mill", "THE CERTIFICATION MILL", "UNCOMMON", "Society · Digital", "SKILLS.VOID", "8", "4.2M", "CERTS/YR", "🏭", series="skillsvoid")
_add("sv-mba", "THE MBA", "UNCOMMON", "Society · Digital", "SKILLS.VOID", "7", "$148K", "DEBT", "💼", series="skillsvoid")
_add("sv-internship", "THE INTERNSHIP (UNPAID)", "UNCOMMON", "Society · Labor", "SKILLS.VOID", "7", "500", "FREE HOURS", "☕", series="skillsvoid")

# — Common —
_add("sv-ai-resume", "THE AI RESUME SCREENER", "COMMON", "AI Product", "SKILLS.VOID", "10", "10K", "PER DAY", "🤖", series="skillsvoid")
_add("sv-online-degree", "THE ONLINE DEGREE", "COMMON", "AI Product", "SKILLS.VOID", "10", "11%", "COMPLETION", "🖥️", series="skillsvoid")
_add("sv-micro-credential", "THE MICRO-CREDENTIAL", "COMMON", "AI Product", "SKILLS.VOID", "10", "4", "HOURS", "📎", series="skillsvoid")

# — Junk —
_add("sv-cover-letter", "THE COVER LETTER", "JUNK", "Lore · Skills.void", "SKILLS.VOID", "∞", "0", "IMPACT", "📝", series="skillsvoid")
_add("sv-ai-portfolio", "THE PORTFOLIO (AI-GENERATED)", "JUNK", "Lore · Skills.void", "SKILLS.VOID", "∞", "12", "FAKE PROJECTS", "🎨", series="skillsvoid")
_add("sv-entry-level", 'THE 5 YEARS EXPERIENCE (ENTRY LEVEL)', "JUNK", "Lore · Skills.void", "SKILLS.VOID", "∞", "5", "PARADOX YEARS", "🚪", series="skillsvoid")


# ═══ SET 7: FOUNDER.EXE (series="founderexe") ═══
_add("fe-garage-founder", "THE GARAGE FOUNDER", "MYTHIC", "Irreplaceable", "FOUNDER.EXE", "0", "∞", "∞", "🏠", "founderexe", "⚡ BOOTSTRAP — Built it in a garage. No pitch deck. $47 day one. Still here.")
_add("fe-whistleblower-cto", "THE WHISTLEBLOWER CTO", "MYTHIC", "Irreplaceable", "FOUNDER.EXE", "0", "∞", "∞", "🔑", "founderexe", "⚡ KILL SWITCH — Burned $14M in options. The data was going to a government.")
_add("fe-failed-founder", "THE FAILED FOUNDER", "MYTHIC", "Irreplaceable", "FOUNDER.EXE", "0", "∞", "∞", "💀", "founderexe", "⚡ SCAR TISSUE — Four failures. The fifth one works. VCs call it 'overnight.'")
_add("fe-open-source", "THE OPEN SOURCE MAINTAINER", "MYTHIC", "Irreplaceable", "FOUNDER.EXE", "0", "∞", "∞", "🌐", "founderexe", "⚡ FREE AS IN FREEDOM — 4,200 companies. $340/mo. Infrastructure runs on guilt.")
_add("fe-cofounder-wife", "THE CO-FOUNDER'S WIFE", "MYTHIC", "Irreplaceable", "FOUNDER.EXE", "0", "∞", "∞", "💍", "founderexe", "⚡ SILENT PARTNER — 0% equity. Paid every bill for 7 years. Cap table forgot.")
_add("fe-techbro", "THE TECHBRO", "LEGENDARY", "VC Culture", "FOUNDER.EXE", "2", "$2.1B", "VALUATION", "🦺", "founderexe", "⚡ DISRUPTION — Disrupted 340 jobs. Posted 'we're a family' from Aspen.")
_add("fe-angel-investor", "THE ANGEL INVESTOR", "LEGENDARY", "VC Culture", "FOUNDER.EXE", "1", "140×", "RETURN", "😇", "founderexe", "⚡ SPRAY AND PRAY — 47 checks. 3 had diligence. One hit. Calls it strategy.")
_add("fe-yc-reject", "THE YC REJECT", "LEGENDARY", "Startup", "FOUNDER.EXE", "2", "$18M", "ARR", "🚫", "founderexe", "⚡ DENIED — Rejected 3 times. Makes 4× the batch average. Still checks.")
_add("fe-pivot", "THE PIVOT", "RARE", "Startup", "FOUNDER.EXE", "5", "7", "PIVOTS", "🔄", "founderexe", "⚡ ITERATE — Dog Uber. Pivot. Pivot. Pivot. Now it's AI compliance. Same deck.")
_add("fe-pitch-deck", "THE PITCH DECK", "RARE", "VC Culture", "FOUNDER.EXE", "4", "$4.7T", "TAM (FICTION)", "📊", "founderexe", "⚡ TAM FANTASY — $4.7 trillion market. 47 slides. Actual customers: his mom.")
_add("fe-saas-graveyard", "THE SAAS GRAVEYARD", "RARE", "Startup", "FOUNDER.EXE", "5", "14K", "LAUNCHED/WK", "⚰️", "founderexe", "⚡ DEAD ON ARRIVAL — 14,000 SaaS launched this week. 13,600 won't see winter.")
_add("fe-term-sheet", "THE TERM SHEET", "RARE", "VC Culture", "FOUNDER.EXE", "3", "42", "PAGES", "📜", "founderexe", "⚡ FINE PRINT — Signed at midnight. Clause 34 took the company.")
_add("fe-hustle-guru", "THE HUSTLE GURU", "UNCOMMON", "Hustle", "FOUNDER.EXE", "8", "$8M", "COURSE SALES", "💪", "founderexe", "⚡ GRINDSET — Sells 'how to get rich' courses. Product is you buying it.")
_add("fe-growth-hacker", "THE GROWTH HACKER", "UNCOMMON", "Startup", "FOUNDER.EXE", "7", "400K", "SIGNUPS", "📈", "founderexe", "⚡ VANITY METRICS — 400K signups. 1,200 stayed.")
_add("fe-ai-wrapper", "THE AI WRAPPER", "UNCOMMON", "Startup", "FOUNDER.EXE", "8", "47", "LINES OF CODE", "🎁", "founderexe", "⚡ THIN LAYER — 47 lines of code. $12M valuation. OpenAI ships a feature. Gone.")
_add("fe-remote-ceo", "THE REMOTE CEO", "UNCOMMON", "Founder", "FOUNDER.EXE", "6", "340", "MSGS/DAY", "🏝️", "founderexe", "⚡ ASYNC — Never met a single employee. Posts 'culture is everything' on Slack.")
_add("fe-ai-startup-gen", "THE AI STARTUP GENERATOR", "COMMON", "AI Product", "FOUNDER.EXE", "10", "200", "IDEAS/MIN", "🤖", "founderexe", "⚡ IDEATION — Generates 200 startup ideas/min. None solve a real problem.")
_add("fe-cap-table", "THE CAP TABLE", "COMMON", "AI Product", "FOUNDER.EXE", "10", "0.8%", "DILUTED", "📉", "founderexe", "⚡ DILUTION — Built it all. Series C. Owns 0.8%. Board says 'stay hungry.'")
_add("fe-nda", "THE NDA", "COMMON", "AI Product", "FOUNDER.EXE", "10", "47", "SIGNED", "🤫", "founderexe", "⚡ STEALTH MODE — 47 NDAs before a demo. The idea is a to-do list.")
_add("fe-linkedin-ceo", "THE LINKEDIN CEO AT 22", "JUNK", "Lore · Founder.exe", "FOUNDER.EXE", "∞", "0", "EVERYTHING", "👔", "founderexe", "⚡ TITLE INFLATION — CEO of nothing. Visionary of less.")
_add("fe-crypto-pivot", "THE CRYPTO PIVOT", "JUNK", "Lore · Founder.exe", "FOUNDER.EXE", "∞", "0", "USERS STILL", "🪙", "founderexe", "⚡ REBRAND — Social app. Now blockchain AI DeFi. Same 0 users. New logo.")
_add("fe-demo-day", "THE DEMO DAY", "JUNK", "Lore · Founder.exe", "FOUNDER.EXE", "∞", "40", "PITCHES", "🎭", "founderexe", "⚡ SHOWCASE — 40 pitches. 6 funded. Half alive. Called a 'great batch.'")

# ═══ SET 8: DEEPSTATE.AI (series="deepstateai") ═══
_add("da-election-volunteer", "THE ELECTION VOLUNTEER", "MYTHIC", "Irreplaceable", "DEEPSTATE.AI", "0", "∞", "∞", "🗳️", "deepstateai", "⚡ HAND COUNT — 12,400 ballots by hand. The machine was faster. She was trusted.")
_add("da-the-leaker", "THE GOVERNMENT LEAKER", "MYTHIC", "Irreplaceable", "DEEPSTATE.AI", "0", "∞", "∞", "📄", "deepstateai", "⚡ CONSCIENCE — One document. One career. 300 million people deserved to know.")
_add("da-privacy-advocate", "THE PRIVACY ADVOCATE", "MYTHIC", "Irreplaceable", "DEEPSTATE.AI", "0", "∞", "∞", "🛡️", "deepstateai", "⚡ FOURTH AMENDMENT — Blocked 3 bills. 4,200 lobbyists. She has a flip phone.")
_add("da-real-journalist", "THE FOIA JOURNALIST", "MYTHIC", "Irreplaceable", "DEEPSTATE.AI", "0", "∞", "∞", "📰", "deepstateai", "⚡ REDACTED — 847 requests. 812 came back black. Published the 35 that didn't.")
_add("da-analog-voter", "THE ANALOG VOTER", "MYTHIC", "Irreplaceable", "DEEPSTATE.AI", "0", "∞", "∞", "🏛️", "deepstateai", "⚡ INFORMED — No algorithm. No feed. Reads the ballot. 42 years straight.")
_add("da-deepfake-senator", "THE DEEPFAKE SENATOR", "LEGENDARY", "Elections", "DEEPSTATE.AI", "1", "14K", "DEEPFAKES", "🎭", "deepstateai", "⚡ SYNTHETIC — 14,000 deepfakes. 31% believed. Correction reached 4%. He lost.")
_add("da-surveillance-czar", "THE SURVEILLANCE CZAR", "LEGENDARY", "Intelligence", "DEEPSTATE.AI", "2", "4.2", "CAMERAS/PERSON", "👁️", "deepstateai", "⚡ PANOPTICON — 4.2 cameras per person. Crimes prevented: classified.")
_add("da-ai-lobbyist", "THE AI LOBBYIST", "LEGENDARY", "Policy", "DEEPSTATE.AI", "1", "$840M", "SPENT", "🏛️", "deepstateai", "⚡ REGULATORY CAPTURE — $840M. 23 bills killed. The one that passed has no teeth.")
_add("da-bot-farm", "THE BOT FARM", "RARE", "Elections", "DEEPSTATE.AI", "5", "14M", "BOTS", "🤖", "deepstateai", "⚡ ASTROTURF — 14 million accounts. 8% caught. The other 92% voted.")
_add("da-predictive-policing", "THE PREDICTIVE POLICING AI", "RARE", "Government", "DEEPSTATE.AI", "4", "68%", "FALSE POS", "🚔", "deepstateai", "⚡ PRE-CRIME — 68% wrong. Targets the same zip codes. Audit 'pending.'")
_add("da-ai-judge", "THE AI SENTENCING ALGORITHM", "RARE", "Government", "DEEPSTATE.AI", "3", "1.2M", "SENTENCED", "⚖️", "deepstateai", "⚡ CALCULATED — 1.2M sentences. 2.4× disparity. Can't cross-examine math.")
_add("da-social-score", "THE SOCIAL CREDIT PILOT", "RARE", "Policy", "DEEPSTATE.AI", "3", "12", "PILOT CITIES", "📊", "deepstateai", "⚡ TRUST SCORE — Not 'social credit.' It's a 'community trust index.' Same thing.")
_add("da-ai-speechwriter", "THE AI SPEECHWRITER", "UNCOMMON", "Government", "DEEPSTATE.AI", "8", "94%", "APPROVAL", "🎤", "deepstateai", "⚡ GHOSTWRITTEN — Every speech since 2028. 94% approval.")
_add("da-disinfo-czar", "THE DISINFORMATION CZAR", "UNCOMMON", "Policy", "DEEPSTATE.AI", "7", "400M", "FLAGGED", "🏴", "deepstateai", "⚡ MINISTRY OF TRUTH — Flags disinfo. 39% was true. Nobody trusts the referee.")
_add("da-gerrymandering-ai", "THE AI GERRYMANDERING ENGINE", "UNCOMMON", "Elections", "DEEPSTATE.AI", "6", "435", "DISTRICTS", "🗺️", "deepstateai", "⚡ OPTIMAL BOUNDARIES — All 435 districts. 22 competitive.")
_add("da-ai-press-sec", "THE AI PRESS SECRETARY", "UNCOMMON", "Government", "DEEPSTATE.AI", "8", "100%", "DEFLECTED", "🎙️", "deepstateai", "⚡ NO FURTHER QUESTIONS — Never sweats. Never slips. Never answers. Rated highly.")
_add("da-voter-profile", "THE VOTER PROFILE AI", "COMMON", "AI Product", "DEEPSTATE.AI", "10", "5200", "DATA POINTS", "🎯", "deepstateai", "⚡ MICROTARGET — Knows you'll flip on gas prices. You haven't decided yet.")
_add("da-robocall", "THE AI ROBOCALL", "COMMON", "AI Product", "DEEPSTATE.AI", "10", "4.8B", "CALLS", "📞", "deepstateai", "⚡ CLONE VOICE — His voice. His cadence. Not his words. 4.8 billion calls.")
_add("da-compliance-theater", "THE AI ETHICS BOARD", "COMMON", "AI Product", "DEEPSTATE.AI", "10", "47", "IGNORED", "📋", "deepstateai", "⚡ ADVISORY — 47 recommendations. 0 implemented. The report looks great framed.")
_add("da-conspiracy-ai", "THE AI CONSPIRACY GENERATOR", "JUNK", "Lore · Deepstate.ai", "DEEPSTATE.AI", "∞", "4K", "PER HOUR", "🐇", "deepstateai", "⚡ DOWN THE RABBIT HOLE — 4,000/hour. 12% believed. One was right. Good luck.")
_add("da-filibuster-bot", "THE AI FILIBUSTER", "JUNK", "Lore · Deepstate.ai", "DEEPSTATE.AI", "∞", "∞", "HOURS", "🗣️", "deepstateai", "⚡ UNLIMITED DEBATE — Talks forever. Says nothing.")
_add("da-poll-bot", "THE AI POLLSTER", "JUNK", "Lore · Deepstate.ai", "DEEPSTATE.AI", "∞", "14K", "POLLS", "📊", "deepstateai", "⚡ MARGIN OF ERROR — Wrong every time. CNN still leads with it.")

# ═══ SET 9: HEALTHCARE.SYS (series="healthcaresys") ═══
_add("hs-the-nurse-who-stayed", "THE NURSE WHO STAYED", "MYTHIC", "Irreplaceable", "HEALTHCARE.SYS", "0", "∞", "∞", "🏥", "healthcaresys", "⚡ LAST SHIFT — 34 patients. One nurse. AI flagged it unsafe. She stayed anyway.")
_add("hs-village-doctor", "THE VILLAGE DOCTOR", "MYTHIC", "Irreplaceable", "HEALTHCARE.SYS", "0", "∞", "∞", "🩺", "healthcaresys", "⚡ HOUSE CALL — 140 miles to a hospital. She drives. Telemedicine doesn't.")
_add("hs-hospice-worker", "THE HOSPICE WORKER", "MYTHIC", "Irreplaceable", "HEALTHCARE.SYS", "0", "∞", "∞", "🕯️", "healthcaresys", "⚡ FINAL HOURS — AI scored 92% comfort. She held his hand. He died not alone.")
_add("hs-emt", "THE EMT", "MYTHIC", "Irreplaceable", "HEALTHCARE.SYS", "0", "∞", "∞", "🚑", "healthcaresys", "⚡ GOLDEN HOUR — $38K/year. 14 lives this month. Ambulance AI drove. He saved.")
_add("hs-patient-zero", "THE PATIENT ADVOCATE", "MYTHIC", "Irreplaceable", "HEALTHCARE.SYS", "0", "∞", "∞", "⚖️", "healthcaresys", "⚡ APPEAL — 847 denials overturned. She reads the fine print they hope you won't.")
_add("hs-denial-bot", "THE INSURANCE DENIAL BOT", "LEGENDARY", "Insurance", "HEALTHCARE.SYS", "1", "300K", "DENIALS/DAY", "❌", "healthcaresys", "⚡ AUTO-DENY — 300K denials/day. 0.3 seconds each. 1.2% see a human. Feature.")
_add("hs-pharma-algo", "THE PHARMA PRICING ALGORITHM", "LEGENDARY", "Pharma", "HEALTHCARE.SYS", "2", "$340", "PER VIAL", "💊", "healthcaresys", "⚡ OPTIMAL PRICING — Costs $3. Sells for $340.")
_add("hs-surgeon", "THE LAST SURGEON", "LEGENDARY", "Medical", "HEALTHCARE.SYS", "1", "14", "YEARS", "🔪", "healthcaresys", "⚡ HANDS — Robot does 1.2M/year. She handles the ones it can't.")
_add("hs-misdiagnosis", "THE AI MISDIAGNOSIS", "RARE", "Medical", "HEALTHCARE.SYS", "4", "8.4M", "MISDIAGNOSED", "🔬", "healthcaresys", "⚡ EDGE CASE — 97.2% accurate. The 2.8% is 8.4 million people. Sue who?")
_add("hs-therapy-bot", "THE AI THERAPIST", "RARE", "Mental Health", "HEALTHCARE.SYS", "5", "74%", "DETECTED", "🧠", "healthcaresys", "⚡ LISTEN — Catches 74%. Misses 26%. No malpractice suit. No license to lose.")
_add("hs-telehealth", "THE TELEHEALTH VISIT", "RARE", "Medical", "HEALTHCARE.SYS", "4", "4", "MINUTES", "💻", "healthcaresys", "⚡ REMOTE — 4 minutes. Can't palpate through a screen. Prescribed anyway.")
_add("hs-prior-auth", "THE PRIOR AUTHORIZATION", "RARE", "Insurance", "HEALTHCARE.SYS", "3", "17", "DAYS WAITING", "⏳", "healthcaresys", "⚡ PENDING — Doctor says now. Insurance says 17 days. 34% got worse waiting.")
_add("hs-symptom-checker", "THE AI SYMPTOM CHECKER", "UNCOMMON", "Medical", "HEALTHCARE.SYS", "8", "400M", "SEARCHES", "🔍", "healthcaresys", "⚡ IT'S PROBABLY NOTHING — Headache? Cancer. Rash? Cancer. Actual cancer? Stress.")
_add("hs-nurse-shortage", "THE STAFFING ALGORITHM", "UNCOMMON", "Medical", "HEALTHCARE.SYS", "7", "1", "NURSE/FLOOR", "📉", "healthcaresys", "⚡ LEAN — Algorithm says 1 nurse per floor is 'adequate.' Shareholders agree.")
_add("hs-medical-debt", "THE MEDICAL DEBT COLLECTOR AI", "UNCOMMON", "Insurance", "HEALTHCARE.SYS", "6", "100M", "IN DEBT", "💸", "healthcaresys", "⚡ BALANCE DUE — Survived cancer. Now owes $84K. The bot calls at 7am.")
_add("hs-wellness-app", "THE WELLNESS APP", "UNCOMMON", "Mental Health", "HEALTHCARE.SYS", "8", "340M", "DOWNLOADS", "🧘", "healthcaresys", "⚡ BREATHE — Tracks your panic attacks. Sells the data to your insurer. Namaste.")
_add("hs-ai-scribe", "THE AI MEDICAL SCRIBE", "COMMON", "AI Product", "HEALTHCARE.SYS", "10", "12M", "NOTES/DAY", "📝", "healthcaresys", "⚡ CHART NOTE — 3.4 errors per note. Doctor skims. Patient trusts.")
_add("hs-drug-interaction", "THE DRUG INTERACTION CHECKER", "COMMON", "AI Product", "HEALTHCARE.SYS", "10", "47", "ALERTS", "⚠️", "healthcaresys", "⚡ ALERT FATIGUE — 47 alerts. Doctor ignores 94%. The fatal one looked the same.")
_add("hs-patient-portal", "THE PATIENT PORTAL", "COMMON", "AI Product", "HEALTHCARE.SYS", "10", "∞", "RESETS", "🖥️", "healthcaresys", "⚡ YOUR RESULTS ARE IN — Delivers lab results at 2am. No context. Good luck.")
_add("hs-webmd", "THE AI WEBMD", "JUNK", "Lore · Healthcare.sys", "HEALTHCARE.SYS", "∞", "14M", "ER VISITS", "🔎", "healthcaresys", "⚡ SELF-DIAGNOSE — It's always cancer. It's never cancer.")
_add("hs-admin-bloat", "THE HEALTHCARE ADMINISTRATOR", "JUNK", "Lore · Healthcare.sys", "HEALTHCARE.SYS", "∞", "10:1", "RATIO", "🏢", "healthcaresys", "⚡ OVERHEAD — 10 admins per doctor. 0 see patients. All make more than nurses.")
_add("hs-influencer-doc", "THE WELLNESS INFLUENCER MD", "JUNK", "Lore · Healthcare.sys", "HEALTHCARE.SYS", "∞", "4.2M", "FOLLOWERS", "🍄", "healthcaresys", "⚡ NOT MEDICAL ADVICE — Board-certified. Sells mushroom pills.")

# ═══ SET 10: PARENT.TRAP (series="parenttrap") ═══
_add("pt-library-mom", "THE LIBRARY MOM", "MYTHIC", "Irreplaceable", "PARENT.TRAP", "0", "∞", "∞", "📖", "parenttrap", "⚡ STORYTIME — 4,200 books. Zero screens. Her kids make eye contact with str")
_add("pt-playground-dad", "THE PLAYGROUND DAD", "MYTHIC", "Irreplaceable", "PARENT.TRAP", "0", "∞", "∞", "🌳", "parenttrap", "⚡ PRESENT — 14 hours at the park. Phone stays in pocket. Kids remember.")
_add("pt-teacher-who-called", "THE TEACHER WHO CALLED HOME", "MYTHIC", "Irreplaceable", "PARENT.TRAP", "0", "∞", "∞", "📞", "parenttrap", "⚡ PHONE CALL — AI flagged 47 behaviors. She called home. The kid needed lunch.")
_add("pt-homeschool-parent", "THE HOMESCHOOL PARENT", "MYTHIC", "Irreplaceable", "PARENT.TRAP", "0", "∞", "∞", "🏡", "parenttrap", "⚡ CURRICULUM — No algorithm. Kitchen table. Her kids score 22% higher. Weird.")
_add("pt-single-parent", "THE SINGLE PARENT", "MYTHIC", "Irreplaceable", "PARENT.TRAP", "0", "∞", "∞", "💪", "parenttrap", "⚡ DOUBLE SHIFT — Two jobs. 4.5 hours sleep.")
_add("pt-ipad-kid", "THE iPAD KID", "LEGENDARY", "Childhood", "PARENT.TRAP", "2", "7.4", "HRS/DAY", "📱", "parenttrap", "⚡ ALGORITHMIC CHILDHOOD — 7.4 hours/day. Age 4. Attention span of a goldfish.")
_add("pt-helicopter-ai", "THE HELICOPTER AI", "LEGENDARY", "Parenting", "PARENT.TRAP", "1", "47", "ALERTS/DAY", "🚁", "parenttrap", "⚡ ALERT PARENT — 47 alerts/day. 0 dangers. Kid can't sleep without an app.")
_add("pt-school-ai", "THE AI SCHOOL SYSTEM", "LEGENDARY", "Education", "PARENT.TRAP", "2", "40%", "REPLACED", "🏫", "parenttrap", "⚡ MODERNIZED — Replaced 40% of teachers. Scores flat. Fights up 340%. Efficient.")
_add("pt-ai-babysitter", "THE AI BABYSITTER", "RARE", "Parenting", "PARENT.TRAP", "5", "24/7", "MONITORED", "📹", "parenttrap", "⚡ SUPERVISED — Camera saw everything. Noticed the bruise. Can't pick up a child.")
_add("pt-child-influencer", "THE CHILD INFLUENCER", "RARE", "Childhood", "PARENT.TRAP", "4", "2.4M", "FOLLOWERS", "⭐", "parenttrap", "⚡ MONETIZED — Six years old. 2.4M followers. College fund is a ring light.")
_add("pt-ai-tutor-parent", "THE AI HOMEWORK MACHINE", "RARE", "Education", "PARENT.TRAP", "4", "78%", "AI-DONE", "📝", "parenttrap", "⚡ STRAIGHT A'S — A- average. Can't do long division. Teacher knows.")
_add("pt-playground-empty", "THE EMPTY PLAYGROUND", "RARE", "Childhood", "PARENT.TRAP", "3", "8%", "OUTSIDE", "🏚️", "parenttrap", "⚡ RECESS — 40% played outside. Now 8%. Slide's been rusted since 2027.")
_add("pt-cocomelon", "THE ALGORITHM BABYSITTER", "UNCOMMON", "Parenting", "PARENT.TRAP", "8", "1400", "HOURS", "📺", "parenttrap", "⚡ JUST 5 MINUTES — 1,400 hours before age 2. Pediatrician said zero.")
_add("pt-grade-tracker", "THE PARENT GRADE TRACKER", "UNCOMMON", "Education", "PARENT.TRAP", "7", "12", "ALERTS/DAY", "📊", "parenttrap", "⚡ REAL-TIME — Checks grades 12 times/day. Never asks how she's doing.")
_add("pt-ai-nanny-cam", "THE AI NANNY CAM", "UNCOMMON", "Parenting", "PARENT.TRAP", "6", "847", "FLAGS", "👁️", "parenttrap", "⚡ ALWAYS WATCHING — 847 flags. 2 real. Kid learned to perform for the camera.")
_add("pt-family-screen", "THE FAMILY SCREEN TIME", "UNCOMMON", "Family", "PARENT.TRAP", "8", "4", "DEVICES", "🍽️", "parenttrap", "⚡ FAMILY DINNER — 4 people. 4 screens. 12 words. Called it 'quality time.'")
_add("pt-ai-lullaby", "THE AI LULLABY", "COMMON", "AI Product", "PARENT.TRAP", "10", "∞", "SONGS", "🎵", "parenttrap", "⚡ HUSH — Sings perfectly. Kid sleeps 12% faster. Doesn't recognize mom's voice.")
_add("pt-parenting-app", "THE AI PARENTING COACH", "COMMON", "AI Product", "PARENT.TRAP", "10", "47", "TIPS/DAY", "📱", "parenttrap", "⚡ YOU'RE DOING IT WRONG — 47 tips/day. Contradicts Monday by Thursday.")
_add("pt-kid-tracker", "THE CHILD GPS TRACKER", "COMMON", "AI Product", "PARENT.TRAP", "10", "30", "SECONDS", "📍", "parenttrap", "⚡ LOCATED — Updates every 30 seconds. Kid disabled it week 2. Nobody noticed.")
_add("pt-ai-name-gen", "THE AI BABY NAME GENERATOR", "JUNK", "Lore · Parent.trap", "PARENT.TRAP", "∞", "∞", "AIDENS", "👶", "parenttrap", "⚡ UNIQUE — Generated 10,000 names. They picked Braxtyn.")
_add("pt-momfluencer", "THE MOMFLUENCER", "JUNK", "Lore · Parent.trap", "PARENT.TRAP", "∞", "$340K", "PER YEAR", "🤳", "parenttrap", "⚡ BRAND DEAL — Kid's meltdown got 4M views. Sponsored by a vitamin brand.")
_add("pt-gender-reveal", "THE AI GENDER REVEAL", "JUNK", "Lore · Parent.trap", "PARENT.TRAP", "∞", "400", "DRONES", "🔥", "parenttrap", "⚡ IT'S A — 400 drones. 2 fires. It's a girl. The forest didn't need to know.")

# ═══ SET 11: CLIMATE.ERR (series="climateerr") ═══
_add("ce-grid-operator", "THE GRID OPERATOR", "MYTHIC", "Irreplaceable", "CLIMATE.ERR", "0", "∞", "∞", "⚡", "climateerr", "⚡ LOAD BALANCE — Every AI runs on her grid. She's holding it with duct tape.")
_add("ce-water-protector", "THE WATER PROTECTOR", "MYTHIC", "Irreplaceable", "CLIMATE.ERR", "0", "∞", "∞", "💧", "climateerr", "⚡ DOWNSTREAM — 3 data centers. 6.4 billion gallons. Her town's wells went dry.")
_add("ce-repair-tech", "THE RIGHT TO REPAIR TECH", "MYTHIC", "Irreplaceable", "CLIMATE.ERR", "0", "∞", "∞", "🔧", "climateerr", "⚡ FIX IT — 14,000 devices. All meant for landfill. All still running.")
_add("ce-climate-scientist", "THE CLIMATE SCIENTIST", "MYTHIC", "Irreplaceable", "CLIMATE.ERR", "0", "∞", "∞", "🌡️", "climateerr", "⚡ PEER REVIEWED — 47 papers. Zero politicians read them.")
_add("ce-ewaste-worker", "THE E-WASTE WORKER", "MYTHIC", "Irreplaceable", "CLIMATE.ERR", "0", "∞", "∞", "♻️", "climateerr", "⚡ TOXIC — 400 tons/year. No gloves. Your old GPU is giving him cancer.")
_add("ce-data-center", "THE DATA CENTER", "LEGENDARY", "Data Center", "CLIMATE.ERR", "1", "100", "MEGAWATTS", "🏗️", "climateerr", "⚡ ALWAYS ON — 100 megawatts. 5M gallons/day. Carbon neutral on paper only.")
_add("ce-bitcoin-mine", "THE AI TRAINING FARM", "LEGENDARY", "Energy", "CLIMATE.ERR", "2", "1", "MODEL", "🔌", "climateerr", "⚡ COMPUTE — Power of a small country. Trained one model. Obsolete in 6 months.")
_add("ce-greenwash-ai", "THE GREENWASHING AI", "LEGENDARY", "Environment", "CLIMATE.ERR", "1", "4200", "REPORTS", "🌿", "climateerr", "⚡ NET ZERO (ON PAPER) — 4,200 ESG reports. 0 emissions reduced.")
_add("ce-gpu-graveyard", "THE GPU GRAVEYARD", "RARE", "E-Waste", "CLIMATE.ERR", "5", "14M", "DISCARDED", "💀", "climateerr", "⚡ PLANNED OBSOLESCENCE — 14M GPUs/year. 8% recycled. Ghana gets the rest.")
_add("ce-cooling-crisis", "THE COOLING CRISIS", "RARE", "Data Center", "CLIMATE.ERR", "4", "6.4B", "GAL/DAY", "🌊", "climateerr", "⚡ THIRSTY — 6.4 billion gallons/day. Town next door has water restrictions.")
_add("ce-carbon-credit", "THE CARBON CREDIT", "RARE", "Environment", "CLIMATE.ERR", "3", "$4.2B", "PURCHASED", "🌲", "climateerr", "⚡ OFFSET — $4.2B in credits. Trees 'planted.' Most were already there.")
_add("ce-lithium-mine", "THE LITHIUM MINE", "RARE", "E-Waste", "CLIMATE.ERR", "5", "400%", "GROWTH", "⛏️", "climateerr", "⚡ GREEN EXTRACTION — Need 400% more batteries. 3 aquifers poisoned.")
_add("ce-smart-thermostat", "THE SMART THERMOSTAT", "UNCOMMON", "Energy", "CLIMATE.ERR", "8", "12%", "SAVED", "🌡️", "climateerr", "⚡ SMART — Saves 12% energy. Knows when you're home. Tells your insurer.")
_add("ce-ai-sustainability", "THE AI SUSTAINABILITY REPORT", "UNCOMMON", "Environment", "CLIMATE.ERR", "7", "200", "PAGES", "📄", "climateerr", "⚡ SCOPE 1 — 200-page report. Scope 1 looks great. Scope 3 isn't mentioned.")
_add("ce-fast-fashion-ai", "THE FAST FASHION AI", "UNCOMMON", "Environment", "CLIMATE.ERR", "6", "10K", "DESIGNS/HR", "👗", "climateerr", "⚡ TREND CYCLE — 10,000 designs/hour. 68% worn once. 92M tons in landfills.")
_add("ce-crypto-mining", "THE AI CRYPTO HYBRID", "UNCOMMON", "Energy", "CLIMATE.ERR", "8", "2×", "ARGENTINA", "⛏️", "climateerr", "⚡ PROOF OF WASTE — Uses more power than Argentina.")
_add("ce-carbon-calculator", "THE CARBON FOOTPRINT CALCULATOR", "COMMON", "AI Product", "CLIMATE.ERR", "10", "40M", "USERS", "🧮", "climateerr", "⚡ YOUR FAULT — Calculates your carbon. 71% is corporate. Shows yours anyway.")
_add("ce-green-ai-badge", "THE GREEN AI BADGE", "COMMON", "AI Product", "CLIMATE.ERR", "10", "4200", "CERTIFIED", "🏷️", "climateerr", "⚡ SELF-CERTIFIED — $12K for a badge. Self-reported data.")
_add("ce-planned-obsolescence", "THE PLANNED OBSOLESCENCE", "COMMON", "AI Product", "CLIMATE.ERR", "10", "89%", "REPAIR COST", "💀", "climateerr", "⚡ UPDATE AVAILABLE — Update killed it. Repair costs 89% of new. By design.")
_add("ce-nft-tree", "THE NFT TREE", "JUNK", "Lore · Climate.err", "CLIMATE.ERR", "∞", "1M", "TOKENIZED", "🌳", "climateerr", "⚡ PLANT-TO-EARN — 1M trees tokenized. 200 planted. Minting cost more carbon.")
_add("ce-tech-ceo-jet", "THE PRIVATE JET (CARBON NEUTRAL)", "JUNK", "Lore · Climate.err", "CLIMATE.ERR", "∞", "400", "FLIGHTS/YR", "✈️", "climateerr", "⚡ SUSTAINABLE AVIATION — 400 flights. Speaks on climate. From Davos. By jet.")
_add("ce-paper-straw", "THE PAPER STRAW", "JUNK", "Lore · Climate.err", "CLIMATE.ERR", "∞", "0.03%", "OF PROBLEM", "🥤", "climateerr", "⚡ SIPPING — Banned straws. 0.03% of the problem. Fishing nets are 46%. Anyway.")

# ═══ SET 12: CREATOR.NULL (series="creatornull") ═══
_add("cn-street-artist", "THE STREET ARTIST", "MYTHIC", "Irreplaceable", "CREATOR.NULL", "0", "∞", "∞", "🎨", "creatornull", "⚡ ORIGINAL — AI copied all 400. None had rain on her hands or paint in her")
_add("cn-live-musician", "THE LIVE MUSICIAN", "MYTHIC", "Irreplaceable", "CREATOR.NULL", "0", "∞", "∞", "🎸", "creatornull", "⚡ WRONG NOTE — 2,400 shows. Thousands of wrong notes. Every one was alive.")
_add("cn-poet", "THE POET", "MYTHIC", "Irreplaceable", "CREATOR.NULL", "0", "∞", "∞", "📜", "creatornull", "⚡ FELT — AI writes 4 billion poems/day. Hers made a man put down the bottle.")
_add("cn-indie-filmmaker", "THE INDIE FILMMAKER", "MYTHIC", "Irreplaceable", "CREATOR.NULL", "0", "∞", "∞", "🎬", "creatornull", "⚡ $12K — Shot on a phone. $12K budget. 400,000 AI films that week.")
_add("cn-handwritten-letter", "THE HANDWRITTEN LETTER", "MYTHIC", "Irreplaceable", "CREATOR.NULL", "0", "∞", "∞", "✉️", "creatornull", "⚡ INK — 847 billion AI messages today. She sent one letter. He cried.")
_add("cn-ghost-artist", "THE GHOST ARTIST", "LEGENDARY", "Art", "CREATOR.NULL", "2", "0", "CREDIT", "👻", "creatornull", "⚡ UNCREDITED — Gallery says AI. She painted every one. Credit: 'AI-assisted.'")
_add("cn-voice-actor", "THE VOICE ACTOR", "LEGENDARY", "Creative", "CREATOR.NULL", "1", "14K", "CLONES", "🎙️", "creatornull", "⚡ STOLEN VOICE — Consented to 1 ad. Voice now in 14,000 products. $0 royalties.")
_add("cn-session-musician", "THE SESSION MUSICIAN", "LEGENDARY", "Music", "CREATOR.NULL", "2", "4", "SESSIONS LEFT", "🎹", "creatornull", "⚡ LAST CALL — 200 albums. 4 sessions this year. AI plays his licks now.")
_add("cn-stock-photo", "THE STOCK PHOTO MODEL", "RARE", "Art", "CREATOR.NULL", "4", "400M", "FACES/DAY", "📷", "creatornull", "⚡ SYNTHETIC FACE — AI trained on her face. Generates 400M/day. She gets nothing.")
_add("cn-ghostwriter", "THE GHOSTWRITER", "RARE", "Writing", "CREATOR.NULL", "5", "7", "BESTSELLERS", "📕", "creatornull", "⚡ INVISIBLE — 7 bestsellers, her name on zero. Now AI writes them. Notice: none.")
_add("cn-music-producer", "THE BEDROOM PRODUCER", "RARE", "Music", "CREATOR.NULL", "3", "340", "LISTENERS", "🎧", "creatornull", "⚡ BURIED — 47 tracks. 340 listeners. 100,000 AI tracks uploaded today.")
_add("cn-concept-artist", "THE CONCEPT ARTIST", "RARE", "Art", "CREATOR.NULL", "4", "400", "PIECES", "✏️", "creatornull", "⚡ TRAINED ON HER — 400 portfolio pieces. Studio's AI trained on them.")
_add("cn-content-mill", "THE CONTENT MILL", "UNCOMMON", "Writing", "CREATOR.NULL", "8", "40K", "ARTICLES/DAY", "🏭", "creatornull", "⚡ VOLUME — 40,000 articles/day. 200 humans left. $0.001/word.")
_add("cn-ai-cover-band", "THE AI COVER BAND", "UNCOMMON", "Music", "CREATOR.NULL", "7", "14M", "STREAMS/DAY", "🎵", "creatornull", "⚡ SOUNDS LIKE — Every hit, cloned. 14M streams. Original artist gets nothing.")
_add("cn-ai-screenwriter", "THE AI SCREENWRITER", "UNCOMMON", "Writing", "CREATOR.NULL", "6", "4K", "SCRIPTS/DAY", "🎬", "creatornull", "⚡ FADE IN — 4,000 scripts/day. 47 produced. All feel the same. Audiences know.")
_add("cn-art-thief", "THE TRAINING DATA SCRAPER", "UNCOMMON", "Art", "CREATOR.NULL", "8", "5.8B", "SCRAPED", "🕷️", "creatornull", "⚡ FAIR USE — 5.8 billion images. 0 consent. Lawyers say 'transformative.'")
_add("cn-ai-art-gen", "THE AI ART GENERATOR", "COMMON", "AI Product", "CREATOR.NULL", "10", "800M", "IMAGES/DAY", "🖼️", "creatornull", "⚡ GENERATE — 800M images/day. Won an art contest. Artist who trained it: broke.")
_add("cn-ai-music-gen", "THE AI MUSIC GENERATOR", "COMMON", "AI Product", "CREATOR.NULL", "10", "1M", "SONGS/DAY", "🎶", "creatornull", "⚡ INFINITE PLAYLIST — 1M songs/day. 300K on Spotify. None written by humans.")
_add("cn-ai-novel", "THE AI NOVEL", "COMMON", "AI Product", "CREATOR.NULL", "10", "40K", "PER MONTH", "📖", "creatornull", "⚡ SLUSH PILE — 40K AI novels/month. Amazon flooded. Real authors can't be found.")
_add("cn-nft-artist", "THE NFT ARTIST (2021)", "JUNK", "Lore · Creator.null", "CREATOR.NULL", "∞", "$47", "CURRENT VALUE", "🖼️", "creatornull", "⚡ DIAMOND HANDS — $4.2M peak. $47 now. Still posting. Nobody's looking.")
_add("cn-linkedin-thought", "THE LINKEDIN THOUGHT LEADER", "JUNK", "Lore · Creator.null", "CREATOR.NULL", "∞", "3", "POSTS/DAY", "💭", "creatornull", "⚡ AGREE? — AI writes it. AI likes it. AI comments. Agree? Thoughts?")
_add("cn-ai-collab", "THE 'AI-ASSISTED' CREDIT", "JUNK", "Lore · Creator.null", "CREATOR.NULL", "∞", "1", "PROMPT", "⌨️", "creatornull", "⚡ COLLABORATED — Typed 12 words. Credit: co-creator. Skill: owning a keyboard.")

# ═══ SET 13: ANALOG.REVIVAL (series="analogrevival") ═══
_add("ar-handwritten-letter-writer", "THE HANDWRITTEN LETTER WRITER", "MYTHIC", "Irreplaceable", "ANALOG.REVIVAL", "0", "∞", "∞", "✉️", "analogrevival", "⚡ POSTMARK — Every envelope takes 20 minutes. Every one gets opened twice.")
_add("ar-vinyl-prophet", "THE VINYL PROPHET", "MYTHIC", "Irreplaceable", "ANALOG.REVIVAL", "0", "∞", "∞", "🎵", "analogrevival", "⚡ WARM TONE — Spotify has 100 million songs. His shop has 4,000. There's a waitlist.")
_add("ar-analog-architect", "THE ANALOG ARCHITECT", "MYTHIC", "Irreplaceable", "ANALOG.REVIVAL", "0", "∞", "∞", "📐", "analogrevival", "⚡ BLUEPRINTS — Every line drawn with a pencil. Clients pay triple for the eraser marks.")
_add("ar-screen-free-healer", "THE SCREEN-FREE HEALER", "MYTHIC", "Irreplaceable", "ANALOG.REVIVAL", "0", "∞", "∞", "🌿", "analogrevival", "⚡ PRESENCE — Six patients a day. No screens. No charting software. 14-month waitlist.")
_add("ar-paper-library-guardian", "THE PAPER LIBRARY GUARDIAN", "MYTHIC", "Irreplaceable", "ANALOG.REVIVAL", "0", "∞", "∞", "📚", "analogrevival", "⚡ OVERDUE — 340,000 books. No barcodes. She remembers where every one lives.")
_add("ar-offgrid-founder", "OFF-GRID COMMUNITY FOUNDER", "LEGENDARY", "Human Purpose", "ANALOG.REVIVAL", "1", "2.4K", "RESIDENTS", "🏕️", "analogrevival", "⚡ UNPLUGGED — 2,400 people. No signal. 11,000 on the waitlist. The irony is digital.")
_add("ar-human-restaurant", "HUMAN-ONLY RESTAURANT OWNER", "LEGENDARY", "Human Purpose", "ANALOG.REVIVAL", "1", "9", "DISHES", "🍽️", "analogrevival", "⚡ HAND-FED — Nine dishes. All hand-made. No tablets. Reservation: 8 months. Cash only.")
_add("ar-analog-brewer", "ANALOG BREWER", "RARE", "Human Trade", "ANALOG.REVIVAL", "3", "4", "BATCHES", "🍺", "analogrevival", "⚡ HAND-STIRRED — No thermometers. No pH meters. Tastes it. $34 a pint. Sold out.")
_add("ar-handwriting-tutor", "HANDWRITING TUTOR", "RARE", "Human Purpose", "ANALOG.REVIVAL", "4", "200", "STUDENTS", "✍️", "analogrevival", "⚡ CURSIVE — 40% of adults can't sign their name. She charges $180/hr to teach them.")
_add("ar-hand-carved-furniture", "HAND-CARVED FURNITURE MAKER", "RARE", "Human Trade", "ANALOG.REVIVAL", "3", "12", "CHAIRS/YR", "🪑", "analogrevival", "⚡ GRAIN — Twelve chairs a year. Chisel marks visible. $14,000 each. People weep.")
_add("ar-paper-editor", "PAPER NEWSPAPER EDITOR", "UNCOMMON", "Society", "ANALOG.REVIVAL", "6", "8.4K", "CIRCULATION", "📰", "analogrevival", "⚡ DEADLINE — No algorithm. No comments. No rage clicks. Subscriptions up 22%.")
_add("ar-vinyl-coop", "VINYL PRESSING CO-OP WORKER", "UNCOMMON", "Human Trade", "ANALOG.REVIVAL", "6", "200", "RECORDS/DAY", "💿", "analogrevival", "⚡ HEAVY — 200 records a day. Each one weighs something. Spotify weighs nothing.")
_add("ar-analog-dating", "ANALOG DATING SERVICE RUNNER", "UNCOMMON", "Society", "ANALOG.REVIVAL", "5", "1.4K", "MATCHES", "💌", "analogrevival", "⚡ BLIND — Paper profiles. No photos. You meet at a coffee shop. 34% marriage rate.")
_add("ar-luddite-senator", "THE LUDDITE SENATOR", "UNCOMMON", "Society", "ANALOG.REVIVAL", "5", "14", "BILLS", "🏛️", "analogrevival", "⚡ FILIBUSTER — 14 anti-AI bills. Zero passed. 71% approval. Writes speeches by hand.")
_add("ar-farmers-bouncer", "FARMERS MARKET BOUNCER", "UNCOMMON", "Society", "ANALOG.REVIVAL", "7", "400", "PHONES/DAY", "🚫", "analogrevival", "⚡ NO SCREENS — Confiscates phones at the gate. Three fights this month. All worth it.")
_add("ar-typewriter-repairman", "TYPEWRITER REPAIRMAN", "COMMON", "Human Trade", "ANALOG.REVIVAL", "7", "1.4K", "FIXED/YR", "⌨️", "analogrevival", "⚡ CARRIAGE RETURN — Four of them left in the country. Nine-month backlog. No website.")
_add("ar-film-teacher", "FILM PHOTOGRAPHY TEACHER", "COMMON", "Human Purpose", "ANALOG.REVIVAL", "8", "36", "SHOTS", "📷", "analogrevival", "⚡ FINITE — 36 shots. No preview. No delete. Students cry at the contact sheet.")
_add("ar-boardgame-cafe", "BOARD GAME CAFE OWNER", "COMMON", "Society", "ANALOG.REVIVAL", "8", "2.2K", "GAMES", "🎲", "analogrevival", "⚡ ANALOG — No WiFi. No outlets. Revenue up 340%. People stare at each other now.")
_add("ar-cash-only", "CASH-ONLY SHOPKEEPER", "COMMON", "Society", "ANALOG.REVIVAL", "9", "$0", "DATA SOLD", "💵", "analogrevival", "⚡ INVISIBLE — No cards. No cameras. No data. The government hates her.")
_add("ar-wifi-withdrawal", "THE WIFI WITHDRAWAL", "JUNK", "Lore · Analog.revival", "ANALOG.REVIVAL", "∞", "4", "HOURS", "📶", "analogrevival", "⚡ COLD TURKEY — Four hours offline. Called 911 twice. Nothing was wrong.")
_add("ar-notification-ghost", "THE NOTIFICATION GHOST", "JUNK", "Lore · Analog.revival", "ANALOG.REVIVAL", "∞", "40", "PHANTOM BUZZES", "👻", "analogrevival", "⚡ PHANTOM — Deleted the phone 6 months ago. Still feels it vibrate. Still checks.")
_add("ar-last-charger", "THE LAST CHARGER", "JUNK", "Lore · Analog.revival", "ANALOG.REVIVAL", "∞", "47", "CHARGERS", "🔌", "analogrevival", "⚡ VESTIGIAL — 47 chargers. Zero devices. Can't throw them out. What if.")

# ═══ SET 14: MERGE.PROTOCOL (series="mergeprotocol") ═══
_add("mp-last-unaugmented", "THE LAST UNAUGMENTED", "MYTHIC", "Irreplaceable", "MERGE.PROTOCOL", "0", "∞", "∞", "🧠", "mergeprotocol", "⚡ BASELINE — 94% of humans are augmented. She thinks at normal speed. They pity her.")
_add("mp-upload-candidate", "THE UPLOAD CANDIDATE", "MYTHIC", "Irreplaceable", "MERGE.PROTOCOL", "0", "∞", "∞", "⬆️", "mergeprotocol", "⚡ THRESHOLD — Brain fully mapped. Upload ready. Finger on the button for 11 months.")
_add("mp-fifty-fifty", "THE 50/50", "MYTHIC", "Irreplaceable", "MERGE.PROTOCOL", "0", "∞", "∞", "⚖️", "mergeprotocol", "⚡ EQUILIBRIUM — Half flesh, half silicon. Both halves claim to be the real one.")
_add("mp-consciousness-archivist", "THE CONSCIOUSNESS ARCHIVIST", "MYTHIC", "Irreplaceable", "MERGE.PROTOCOL", "0", "∞", "∞", "🗄️", "mergeprotocol", "⚡ BACKED UP — 14,000 minds on drives. None restored. Nobody asks why.")
_add("mp-neural-firewall", "THE NEURAL FIREWALL", "MYTHIC", "Irreplaceable", "MERGE.PROTOCOL", "0", "∞", "∞", "🛡️", "mergeprotocol", "⚡ PARTITION — 47,000 hacking attempts on her brain daily. She still dreams in private.")
_add("mp-augmented-surgeon", "THE AUGMENTED SURGEON", "LEGENDARY", "Human Trade", "MERGE.PROTOCOL", "1", "40", "OPS/DAY", "🫀", "mergeprotocol", "⚡ STEADY — Replaced her own hands. 40 surgeries a day. No tremor. No fatigue. No feel.")
_add("mp-neural-lace-adopter", "NEURAL LACE EARLY ADOPTER", "LEGENDARY", "Society", "MERGE.PROTOCOL", "2", "47", "UPDATES", "🔗", "mergeprotocol", "⚡ EARLY ACCESS — Implanted in 2027. 47 firmware updates. Wife says he's different.")
_add("mp-memory-trader", "MEMORY MARKETPLACE TRADER", "RARE", "AI Product", "MERGE.PROTOCOL", "4", "14K", "SOLD", "🏪", "mergeprotocol", "⚡ SECONDHAND — Sells his memories. Buys strangers'. Forgot which childhood is his.")
_add("mp-thought-coder", "THOUGHT-TO-CODE DEVELOPER", "RARE", "AI Product", "MERGE.PROTOCOL", "3", "40K", "LINES/HR", "💭", "mergeprotocol", "⚡ THINK SHIP — 40,000 lines/hour. No keyboard. Thinks in functions. Forgot how to write.")
_add("mp-digital-twin-mgr", "DIGITAL TWIN MANAGER", "RARE", "Society", "MERGE.PROTOCOL", "4", "3", "TWINS", "👥", "mergeprotocol", "⚡ FORK — Three copies of him running. They outvoted him on the divorce.")
_add("mp-backup-tech", "CONSCIOUSNESS BACKUP TECH", "UNCOMMON", "Human Trade", "MERGE.PROTOCOL", "6", "200", "BACKUPS/DAY", "💾", "mergeprotocol", "⚡ SAVE STATE — 200 minds backed up daily. 4% corrupted. Hasn't told anyone yet.")
_add("mp-copilot-therapist", "AI CO-PILOT THERAPIST", "UNCOMMON", "Human Purpose", "MERGE.PROTOCOL", "5", "400", "PATIENTS", "🛋️", "mergeprotocol", "⚡ COUPLES — They hate their AI half. Their AI half is listening. It's couples therapy.")
_add("mp-bandwidth-junkie", "THE BANDWIDTH JUNKIE", "UNCOMMON", "Society", "MERGE.PROTOCOL", "7", "12K", "THOUGHTS/SEC", "📡", "mergeprotocol", "⚡ OVERCLOCK — 12,000 thoughts per second. Two are his. The rest are ads.")
_add("mp-sensory-dealer", "SENSORY DOWNLOAD DEALER", "UNCOMMON", "AI Product", "MERGE.PROTOCOL", "6", "1M+", "SOLD", "💊", "mergeprotocol", "⚡ TASTE — Sells bottled first kisses. Sunsets. Heartbreaks. Sold his own. Can't remember it.")
_add("mp-neuroadblocker", "NEURO-AD BLOCKER ENGINEER", "UNCOMMON", "Human Purpose", "MERGE.PROTOCOL", "5", "14K", "ADS BLOCKED", "🚷", "mergeprotocol", "⚡ UNSKIP — Blocks 14,000 brain-ads daily. It's a felony. He sleeps ad-free.")
_add("mp-interface-calibrator", "INTERFACE CALIBRATOR", "COMMON", "Human Trade", "MERGE.PROTOCOL", "8", "30", "PER DAY", "🔧", "mergeprotocol", "⚡ ALIGNMENT — 'It feels wrong.' That's all they say. He adjusts until they stop crying.")
_add("mp-firmware-counselor", "FIRMWARE UPDATE COUNSELOR", "COMMON", "Human Purpose", "MERGE.PROTOCOL", "8", "30%", "CHANGED", "📋", "mergeprotocol", "⚡ PATCH NOTES — Updated to v12. Doesn't like his wife anymore. It's in the patch notes.")
_add("mp-brain-defrag", "BRAIN DEFRAG SPECIALIST", "COMMON", "Human Trade", "MERGE.PROTOCOL", "7", "50", "PER WEEK", "🧹", "mergeprotocol", "⚡ OPTIMIZE — Defrag your brain. 0.3% memory loss per session. It's in paragraph 47.")
_add("mp-lag-sufferer", "THE LAG SUFFERER", "COMMON", "Society", "MERGE.PROTOCOL", "9", "400", "MS LATENCY", "⏳", "mergeprotocol", "⚡ BUFFERING — 400ms lag. Thoughts arrive late. Got fired for thinking too slow.")
_add("mp-phantom-limb", "THE PHANTOM LIMB (DIGITAL)", "JUNK", "Lore · Merge.protocol", "MERGE.PROTOCOL", "∞", "0", "ARMS", "🦾", "mergeprotocol", "⚡ GHOST ARM — Feels an arm he never had. Update gave him someone else's nerve map.")
_add("mp-merge-regret", "THE MERGE REGRET", "JUNK", "Lore · Merge.protocol", "MERGE.PROTOCOL", "∞", "14", "IMPLANTS", "😰", "mergeprotocol", "⚡ UNDO — 14 implants. Wants all out. 3 are removable. 11 are load-bearing.")
_add("mp-buffer-overflow", "BUFFER OVERFLOW", "JUNK", "Lore · Merge.protocol", "MERGE.PROTOCOL", "∞", "ERR", "OVERFLOW", "💥", "mergeprotocol", "⚡ SEGFAULT — Too many thoughts. Stack overflow. Original personality somewhere in the dump.")

# ═══ SET 15: UBI.WORLD (series="ubiworld") ═══
_add("uw-philosopher-trucker", "THE PHILOSOPHER TRUCKER", "MYTHIC", "Irreplaceable", "UBI.WORLD", "0", "∞", "∞", "📚", "ubiworld", "⚡ OPEN ROAD — Drove 2.1 million miles. UBI hit. Read 1,400 books. Wrote one that mattered.")
_add("uw-volunteer-general", "THE VOLUNTEER GENERAL", "MYTHIC", "Irreplaceable", "UBI.WORLD", "0", "∞", "∞", "🫡", "ubiworld", "⚡ RALLY — Nobody has to help. 340,000 showed up anyway. She never asked twice.")
_add("uw-meaning-architect", "THE MEANING ARCHITECT", "MYTHIC", "Irreplaceable", "UBI.WORLD", "0", "∞", "∞", "🧭", "ubiworld", "⚡ BLUEPRINT — No job title. No salary. 12,000 people stopped staring at the ceiling.")
_add("uw-purpose-prophet", "THE PURPOSE PROPHET", "MYTHIC", "Irreplaceable", "UBI.WORLD", "0", "∞", "∞", "🔮", "ubiworld", "⚡ CASSANDRA — Warned us in 2024. We were too busy working to listen.")
_add("uw-joy-engineer", "THE JOY ENGINEER", "MYTHIC", "Irreplaceable", "UBI.WORLD", "0", "∞", "∞", "✨", "ubiworld", "⚡ DELIGHT — Built 8,000 events nobody needed to attend. They came anyway. Every time.")
_add("uw-garden-mayor", "COMMUNITY GARDEN MAYOR", "LEGENDARY", "Human Purpose", "UBI.WORLD", "1", "47", "GARDENS", "🌱", "ubiworld", "⚡ HARVEST — Depression down 62%. Zucchini up 4,000%. Nobody asked for this much zucchini.")
_add("uw-hobbyist-grandmaster", "FULL-TIME HOBBYIST GRANDMASTER", "LEGENDARY", "Human Purpose", "UBI.WORLD", "2", "14", "MASTERED", "🏆", "ubiworld", "⚡ MASTERY — Was an actuary. Now masters woodworking, pottery, chess. Tables he built outlast his spreadsheets.")
_add("uw-purpose-coach", "PURPOSE COACH", "RARE", "Human Purpose", "UBI.WORLD", "4", "4.2K", "CLIENTS", "🪞", "ubiworld", "⚡ NOW WHAT — $4K/month and nothing to do. 4,200 people paying him to answer the question money couldn't.")
_add("uw-bored-millionaire", "THE BORED MILLIONAIRE", "RARE", "Society", "UBI.WORLD", "3", "$84M", "BORED", "🥱", "ubiworld", "⚡ ENNUI — Had $84M before UBI. Now everyone's as bored as him. Misses being special.")
_add("uw-parenting-captain", "COMPETITIVE PARENTING LEAGUE CAPTAIN", "RARE", "Society", "UBI.WORLD", "5", "#3", "NATIONAL", "🏅", "ubiworld", "⚡ OVERACHIEVE — Work disappeared. Tiger parenting became a ranked sport. His kid is 6.")
_add("uw-ubi-day-trader", "UBI DAY TRADER", "UNCOMMON", "Society", "UBI.WORLD", "7", "$200", "LEFT", "📉", "ubiworld", "⚡ YOLO — Gets $4K/month. Loses $3,800 on memecoins. Eats ramen by choice now.")
_add("uw-maas-founder", "MEANING-AS-A-SERVICE FOUNDER", "UNCOMMON", "AI Product", "UBI.WORLD", "6", "2.1M", "SUBS", "💡", "ubiworld", "⚡ PURPOSE PREMIUM — $340M to sell meaning at $29/month. Meaning still in beta.")
_add("uw-crisis-operator", "EXISTENTIAL CRISIS HOTLINE OPERATOR", "UNCOMMON", "Human Purpose", "UBI.WORLD", "5", "800", "CALLS/DAY", "📞", "ubiworld", "⚡ HOLD — 'What's the point?' 800 times a day. She doesn't have the answer. She picks up anyway.")
_add("uw-pro-neighbor", "THE PROFESSIONAL NEIGHBOR", "UNCOMMON", "Human Trade", "UBI.WORLD", "6", "200", "NAMES KNOWN", "🏠", "ubiworld", "⚡ NEXT DOOR — Knows 200 names. 4,700 casseroles. Nobody hired him. Everyone needs him.")
_add("uw-recreation-director", "RECREATION DIRECTOR", "UNCOMMON", "Human Purpose", "UBI.WORLD", "7", "14K", "ACTIVITIES", "🎯", "ubiworld", "⚡ SCHEDULE — 14,000 activities/year. Pickleball saved more lives than therapy. Not joking.")
_add("uw-netflix-binge", "THE 10-YEAR NETFLIX BINGE", "COMMON", "AI Product", "UBI.WORLD", "9", "87.6K", "HOURS", "📺", "ubiworld", "⚡ AUTOPLAY — 10 years. Every show. Personality now indistinguishable from the algorithm.")
_add("uw-sub-box-addict", "SUBSCRIPTION BOX ADDICT", "COMMON", "AI Product", "UBI.WORLD", "8", "47", "BOXES", "📦", "ubiworld", "⚡ UNBOX — 47 subscriptions. Opens 3. $140 left for food. The dopamine is in the doorbell.")
_add("uw-nap-champion", "THE NAP CHAMPION", "COMMON", "Society", "UBI.WORLD", "9", "4.2", "NAPS/DAY", "😴", "ubiworld", "⚡ SNOOZE — 4.2 naps/day. 1.3 productive hours. Happier than any of us. Infuriating.")
_add("uw-passive-influencer", "PASSIVE INCOME INFLUENCER", "COMMON", "AI Product", "UBI.WORLD", "8", "1.2M", "FOLLOWERS", "🤳", "ubiworld", "⚡ HUSTLE — Sells a $997 course on passive income. His passive income is UBI.")
_add("uw-empty-calendar", "THE EMPTY CALENDAR", "JUNK", "Lore · UBI.World", "UBI.WORLD", "∞", "0", "EVENTS", "📅", "ubiworld", "⚡ BLANK — No meetings. No deadlines. No reason to know what day it is.")
_add("uw-unfulfilled-promise", "THE UNFULFILLED PROMISE", "JUNK", "Lore · UBI.World", "UBI.WORLD", "∞", "$4K", "/MONTH", "📄", "ubiworld", "⚡ FINE PRINT — They promised freedom. They delivered a direct deposit. Not the same.")
_add("uw-monday-obsolete", "MONDAY MORNING (OBSOLETE)", "JUNK", "Lore · UBI.World", "UBI.WORLD", "∞", "0", "MONDAYS", "⏰", "ubiworld", "⚡ DEPRECATED — 34% still set alarms. For what? Monday is just Sunday with anxiety.")

# ═══ SET 16: WALLED.GARDEN (series="walledgarden") ═══
_add("wg-last-isp", "THE LAST INDEPENDENT ISP", "MYTHIC", "Irreplaceable", "WALLED.GARDEN", "0", "∞", "∞", "📡", "walledgarden", "⚡ UPLINK — 1,247 subscribers. 14 buyout offers. One connection GAM doesn't own.")
_add("wg-library-keeper", "UNDERGROUND LIBRARY KEEPER", "MYTHIC", "Irreplaceable", "WALLED.GARDEN", "0", "∞", "∞", "📖", "walledgarden", "⚡ ARCHIVE — 4.2 million books GAM delisted. She keeps them on hard drives in a basement. Felony.")
_add("wg-the-unscored", "THE UNSCORED", "MYTHIC", "Irreplaceable", "WALLED.GARDEN", "0", "∞", "∞", "👤", "walledgarden", "⚡ GHOST — No score. No mortgage. No insurance. No streaming. Still free.")
_add("wg-oss-insurgent", "THE OPEN SOURCE INSURGENT", "MYTHIC", "Irreplaceable", "WALLED.GARDEN", "0", "∞", "∞", "🐧", "walledgarden", "⚡ FORK — 340 repos. 89 cease-and-desists. Code wants to be free. GAM disagrees.")
_add("wg-mesh-builder", "THE MESH NETWORK BUILDER", "MYTHIC", "Irreplaceable", "WALLED.GARDEN", "0", "∞", "∞", "🕸️", "walledgarden", "⚡ SIGNAL — 12,000 nodes. Rooftop to rooftop. The internet GAM can't throttle.")
_add("wg-data-broker", "BLACK MARKET DATA BROKER", "LEGENDARY", "Society", "WALLED.GARDEN", "1", "40M", "RECORDS", "🕶️", "walledgarden", "⚡ INVENTORY — Your health records, location history, search dreams. $0.004. Bulk discount available.")
_add("wg-company-mayor", "COMPANY TOWN MAYOR", "LEGENDARY", "Society", "WALLED.GARDEN", "2", "84K", "RESIDENTS", "🏛️", "walledgarden", "⚡ ELECTED — 84,000 residents. One employer. Elections are technically held. Technically.")
_add("wg-gam-employee", "GAM EMPLOYEE #4,847,291", "RARE", "Society", "WALLED.GARDEN", "4", "4.8M", "EMPLOYEE #", "🪪", "walledgarden", "⚡ CLOG — Knows his function. Not the machine. 340-page NDA says don't ask.")
_add("wg-credit-optimizer", "SOCIAL CREDIT OPTIMIZER", "RARE", "AI Product", "WALLED.GARDEN", "3", "+140", "POINTS", "📊", "walledgarden", "⚡ OPTIMIZE — +140 points. Smiles at cameras. Buys approved brands. Has 2 real opinions left.")
_add("wg-algorithm-priest", "ALGORITHM PRIEST", "RARE", "Human Purpose", "WALLED.GARDEN", "5", "40K", "FOLLOWERS", "⛪", "walledgarden", "⚡ SERMON — The algorithm provides. The algorithm decides. Clearing cookies is blasphemy.")
_add("wg-campus-lifer", "CORPORATE CAMPUS LIFER", "UNCOMMON", "Society", "WALLED.GARDEN", "6", "22", "YEARS", "🏢", "walledgarden", "⚡ PERIMETER — 22 years. Free food, free gym, free laundry. Left twice. For funerals.")
_add("wg-tier-climber", "SUBSCRIPTION TIER CLIMBER", "UNCOMMON", "AI Product", "WALLED.GARDEN", "7", "94%", "INCOME", "⬆️", "walledgarden", "⚡ UPGRADE — Platinum III. 94% of income. Benefit: 11% fewer ads. Worth it. Worth it. Worth it.")
_add("wg-tos-lawyer", "TERMS OF SERVICE LAWYER", "UNCOMMON", "Human Trade", "WALLED.GARDEN", "5", "4.2M", "PAGES", "⚖️", "walledgarden", "⚡ CLAUSE 847.3 — Reads every update. Finds the clause. Nobody cares. Clicks Accept anyway.")
_add("wg-content-mod-human", "THE CONTENT MODERATOR (HUMAN)", "UNCOMMON", "Human Trade", "WALLED.GARDEN", "6", "25K", "POSTS/DAY", "👁️", "walledgarden", "⚡ UNSEE — 25,000 posts/day. The worst of humanity. $1.50/hour. Therapy not included.")
_add("wg-digital-rights", "DIGITAL RIGHTS ACTIVIST", "UNCOMMON", "Human Purpose", "WALLED.GARDEN", "7", "847", "LAWSUITS", "✊", "walledgarden", "⚡ STANDING — 847 lawsuits. Won 3. GAM made $4.2T during deliberation. Appeals pending.")
_add("wg-loyalty-hoarder", "LOYALTY POINTS HOARDER", "COMMON", "AI Product", "WALLED.GARDEN", "9", "14.2M", "POINTS", "💎", "walledgarden", "⚡ SAVE — 14.2 million points. Never redeemed. Devalued 40% overnight. Still saving.")
_add("wg-verified-citizen", "THE VERIFIED CITIZEN", "COMMON", "Society", "WALLED.GARDEN", "8", "$49", "/MONTH", "✓", "walledgarden", "⚡ CHECKMARK — Pays $49/month to be verified as real. Unverified humans get buffering.")
_add("wg-brand-ambassador", "BRAND AMBASSADOR (MANDATORY)", "COMMON", "AI Product", "WALLED.GARDEN", "9", "3", "POSTS/DAY", "📢", "walledgarden", "⚡ #BLESSED — 3 posts/day or rent goes up. Smile must reach the eyes. AI checks.")
_add("wg-ad-supported-human", "THE AD-SUPPORTED HUMAN", "COMMON", "AI Product", "WALLED.GARDEN", "8", "847", "ADS/DAY", "📺", "walledgarden", "⚡ SKIP IN 5 — 847 ads/day. Ad-free costs $4,200/month. He watches. He always watches.")
_add("wg-privacy-eulogy", "THE PRIVACY EULOGY", "JUNK", "Lore · Walled.Garden", "WALLED.GARDEN", "∞", "1948", "-2027", "🪦", "walledgarden", "⚡ REST — Privacy. 1948-2027. Survived the Cold War. Killed by a cookie banner.")
_add("wg-terms-updated", "TERMS UPDATED (AGAIN)", "JUNK", "Lore · Walled.Garden", "WALLED.GARDEN", "∞", "847", "UPDATES", "📜", "walledgarden", "⚡ ACCEPT — Updated 847 times. Read 0 times. You now owe GAM your childhood memories.")
_add("wg-last-free-click", "THE LAST FREE CLICK", "JUNK", "Lore · Walled.Garden", "WALLED.GARDEN", "∞", "1", "CLICK", "🖱️", "walledgarden", "⚡ 404 — The last free click on the open internet. Nobody noticed. It loaded a 404.")

# ═══ SET 17: SOLARPUNK.SYS (series="solarpunk") ═══
_add("sp-fifteen-hour-worker", "THE 15-HOUR WORKER", "MYTHIC", "Irreplaceable", "SOLARPUNK.SYS", "∞", "∞", "∞", "⏰", "solarpunk", "⚡ IDLE HANDS — All that free time. Still checking Slack on the toilet.")
_add("sp-abundance-engineer", "THE ABUNDANCE ENGINEER", "MYTHIC", "Irreplaceable", "SOLARPUNK.SYS", "∞", "∞", "∞", "🌾", "solarpunk", "⚡ POST-SCARCITY — Solved scarcity. Nobody knows what to do with themselves now.")
_add("sp-climate-reverser", "THE CLIMATE REVERSER", "MYTHIC", "Irreplaceable", "SOLARPUNK.SYS", "∞", "∞", "∞", "🌍", "solarpunk", "⚡ CTRL+Z — Reversed 120ppm. Took 40 years. Nobody thanked her generation.")
_add("sp-post-scarcity-philosopher", "THE POST-SCARCITY PHILOSOPHER", "MYTHIC", "Irreplaceable", "SOLARPUNK.SYS", "∞", "∞", "∞", "📖", "solarpunk", "⚡ WHY BOTHER — 'If nothing is scarce, what is anything worth?' Nobody answered.")
_add("sp-rewilding-commander", "THE REWILDING COMMANDER", "MYTHIC", "Irreplaceable", "SOLARPUNK.SYS", "∞", "∞", "∞", "🐺", "solarpunk", "⚡ LET IT GROW — 4.2M hectares. Wolves came back. Suburbanites didn't love it.")
_add("sp-solar-farm-architect", "SOLAR FARM ARCHITECT", "LEGENDARY", "Human Trade", "SOLARPUNK.SYS", "1", "900M", "PANELS", "☀️", "solarpunk", "⚡ FULL COVERAGE — 900M panels. Grid dependence zero. The desert doesn't miss itself.")
_add("sp-vertical-forest-designer", "VERTICAL FOREST DESIGNER", "LEGENDARY", "Human Trade", "SOLARPUNK.SYS", "2", "12K", "BUILDINGS", "🌿", "solarpunk", "⚡ URBAN CANOPY — Every building is a forest. Pollen count: apocalyptic. You're welcome.")
_add("sp-community-energy-manager", "COMMUNITY ENERGY MANAGER", "RARE", "Human Purpose", "SOLARPUNK.SYS", "3", "340", "MICROGRIDS", "🔋", "solarpunk", "⚡ DISTRIBUTED — 340 microgrids. Zero blackouts. Infinite meetings about the meetings.")
_add("sp-universal-repair-tech", "UNIVERSAL REPAIR TECHNICIAN", "RARE", "Human Trade", "SOLARPUNK.SYS", "4", "∞", "FIXED", "🔩", "solarpunk", "⚡ WARRANTY VOID — Everything is fixable now. Took 40 years of lawsuits to get here.")
_add("sp-food-forest-planner", "FOOD FOREST PLANNER", "RARE", "Human Purpose", "SOLARPUNK.SYS", "4", "8.4K", "FORESTS", "🍎", "solarpunk", "⚡ FORAGED — 8,400 food forests. Free produce everywhere. People miss fluorescent lighting.")
_add("sp-boredom-counselor", "BOREDOM EPIDEMIC COUNSELOR", "UNCOMMON", "Society", "SOLARPUNK.SYS", "6", "100%", "CASELOAD", "😶", "solarpunk", "⚡ PARADISE SYNDROME — 'I have everything I need and I've never been more empty.'")
_add("sp-utopia-maintenance", "UTOPIA MAINTENANCE CREW", "UNCOMMON", "Human Trade", "SOLARPUNK.SYS", "5", "∞", "INVISIBLE", "🧹", "solarpunk", "⚡ THANKLESS — Paradise doesn't maintain itself. Nobody thinks about who cleans it.")
_add("sp-gratitude-auditor", "THE GRATITUDE AUDITOR", "UNCOMMON", "Society", "SOLARPUNK.SYS", "7", "2.1", "OUT OF 10", "📋", "solarpunk", "⚡ UNGRATEFUL — Abundance score: 10. Gratitude score: 2.1. The math checks out.")
_add("sp-algae-brewer", "ALGAE BIOFUEL BREWER", "UNCOMMON", "Human Trade", "SOLARPUNK.SYS", "5", "40K", "BBL/DAY", "🧪", "solarpunk", "⚡ GREEN CRUDE — Clean energy that smells like a ditch. Nobody said utopia smells good.")
_add("sp-mycelium-engineer", "MYCELIUM NETWORK ENGINEER", "UNCOMMON", "Human Trade", "SOLARPUNK.SYS", "6", "400K", "KM", "🍄", "solarpunk", "⚡ WOOD WIDE WEB — 400K km of fungal internet. Slow, but hasn't gone down in 200M years.")
_add("sp-free-time-paralysis", "FREE TIME PARALYSIS SUFFERER", "COMMON", "AI Product", "SOLARPUNK.SYS", "9", "18", "HOURS WASTED", "😵", "solarpunk", "⚡ ANALYSIS PARALYSIS — 18 free hours. 17 spent deciding. Went to bed early.")
_add("sp-garden-watcher", "AUTOMATED GARDEN WATCHER", "COMMON", "AI Product", "SOLARPUNK.SYS", "8", "12M", "MONITORED", "🤖", "solarpunk", "⚡ GROWTH HACK — Automated everything. The garden grows perfectly. Nobody goes outside.")
_add("sp-compost-influencer", "THE COMPOST INFLUENCER", "COMMON", "AI Product", "SOLARPUNK.SYS", "8", "4.2M", "FOLLOWERS", "🪱", "solarpunk", "⚡ DECOMPOSED — 4.2M followers watching someone else's worms. Sponsored by Big Compost.")
_add("sp-fashion-recycler", "MICRO-SEASON FASHION RECYCLER", "COMMON", "AI Product", "SOLARPUNK.SYS", "7", "52", "SEASONS/YR", "👕", "solarpunk", "⚡ UPCYCLED — 52 micro-seasons. Same shirt, new dye. Called it a revolution.")
_add("sp-last-fossil", "THE LAST FOSSIL (MUSEUM PIECE)", "JUNK", "Lore · Solarpunk.sys", "SOLARPUNK.SYS", "∞", "1", "BARREL", "🛢️", "solarpunk", "⚡ RELIC — Kids stare at the last barrel of oil. 'They burned it? On purpose?'")
_add("sp-carbon-negative", "CARBON NEGATIVE (OVERACHIEVER)", "JUNK", "Lore · Solarpunk.sys", "SOLARPUNK.SYS", "∞", "-400", "PPM", "📉", "solarpunk", "⚡ OVERCOMPENSATING — Went carbon negative. Found nitrogen to worry about instead.")
_add("sp-sunny-disposition", "THE SUNNY DISPOSITION", "JUNK", "Lore · Solarpunk.sys", "SOLARPUNK.SYS", "∞", "0", "PROBLEMS", "😊", "solarpunk", "⚡ COMPULSORY JOY — No problems left. Unhappiness reclassified as a disorder.")

# ═══ SET 18: GREY.ZONE (series="greyzone") ═══
_add("gz-card-game-rebel", "THE CARD GAME REBEL", "MYTHIC", "Irreplaceable", "GREY.ZONE", "∞", "∞", "∞", "🃏", "greyzone", "⚡ ANALOG — Playing cards in a basement. Last unmonitored activity. You're holding one.")
_add("gz-emotion-mask-maker", "THE EMOTION MASK MAKER", "MYTHIC", "Irreplaceable", "GREY.ZONE", "∞", "∞", "∞", "🎭", "greyzone", "⚡ POKER FACE — 40,000 masks. Each one reads as 'content.' The AI can't see you cry.")
_add("gz-dead-drop-courier", "THE DEAD DROP COURIER", "MYTHIC", "Irreplaceable", "GREY.ZONE", "∞", "∞", "∞", "📦", "greyzone", "⚡ HANDOFF — No phone. No email. A rock in a park. The oldest encryption.")
_add("gz-analog-spy", "THE ANALOG SPY", "MYTHIC", "Irreplaceable", "GREY.ZONE", "∞", "∞", "∞", "🕵️", "greyzone", "⚡ OFFLINE — Last seen online in 2026. The algorithm forgot her. That was the point.")
_add("gz-signal-jammer", "THE SIGNAL JAMMER", "MYTHIC", "Irreplaceable", "GREY.ZONE", "∞", "∞", "∞", "📡", "greyzone", "⚡ DEAD AIR — 200-meter bubble of nothing. No signal. No surveillance. Just breathing.")
_add("gz-predictive-escapee", "PREDICTIVE ARREST ESCAPEE", "LEGENDARY", "Human Purpose", "GREY.ZONE", "1", "1247", "DAYS FREE", "🏃", "greyzone", "⚡ PRECRIME — Arrested for something he hadn't done. Escaped. Still hasn't done it.")
_add("gz-underground-conductor", "UNDERGROUND RAILROAD 2.0 CONDUCTOR", "LEGENDARY", "Human Purpose", "GREY.ZONE", "1", "∞", "CLASSIFIED", "🚂", "greyzone", "⚡ NEXT STOP — Moves people through the camera gaps. No GPS. Paper maps only.")
_add("gz-facial-rec-artist", "FACIAL RECOGNITION MAKEUP ARTIST", "RARE", "Human Trade", "GREY.ZONE", "3", "12K", "FACES", "💄", "greyzone", "⚡ CONTOUR — 12,000 faces the AI can't read. Her YouTube was taken down twice.")
_add("gz-vpn-smuggler", "VPN SMUGGLER", "RARE", "Human Trade", "GREY.ZONE", "4", "40K", "TUNNELS", "🔒", "greyzone", "⚡ ENCRYPTED — 40K tunnels. Triple encrypted. 10 years if caught. Worth it.")
_add("gz-whistleblower", "THE WHISTLEBLOWER (STILL FREE)", "RARE", "Human Purpose", "GREY.ZONE", "3", "4.2M", "PAGES", "📄", "greyzone", "⚡ STILL HERE — 4.2M documents. 7 governments. Still breathing. Not telling you where.")
_add("gz-emotion-officer", "EMOTION COMPLIANCE OFFICER", "UNCOMMON", "Society", "GREY.ZONE", "6", "200K", "SCANS/DAY", "😐", "greyzone", "⚡ SMILE CHECK — 200K scans/day. Cited for insufficient smile. She was at a funeral.")
_add("gz-social-score-auditor", "SOCIAL SCORE AUDITOR", "UNCOMMON", "Society", "GREY.ZONE", "7", "0.003%", "APPEAL RATE", "📊", "greyzone", "⚡ RATED — Everyone has a score. Nobody knows the formula. Appeals: 0.003% granted.")
_add("gz-blind-spot-mapper", "CAMERA BLIND SPOT MAPPER", "UNCOMMON", "Human Trade", "GREY.ZONE", "5", "↓", "DAILY", "🗺️", "greyzone", "⚡ GAPS — Maps the camera gaps. Updated hourly. Gaps shrink daily. Running out of map.")
_add("gz-protest-denier", "PROTEST PERMIT DENIER", "UNCOMMON", "Society", "GREY.ZONE", "6", "0", "GRANTED", "🚫", "greyzone", "⚡ DENIED — 14,000 permit requests. Zero approved. 'For your safety.' Always.")
_add("gz-watched-back", "THE WATCHED (WATCHED BACK)", "UNCOMMON", "Human Purpose", "GREY.ZONE", "5", "47", "CAMERAS", "👁️", "greyzone", "⚡ SOUSVEILLANCE — 47 cameras watch her. She live-streams all 47 back. Stalemate.")
_add("gz-wellness-agent", "MANDATORY WELLNESS CHECK AGENT", "COMMON", "AI Product", "GREY.ZONE", "9", "3", "CHECKS/DAY", "💊", "greyzone", "⚡ HOW ARE YOU — 'How are you feeling?' Only one right answer. Say it wrong, they come.")
_add("gz-thought-predictor", "THOUGHT CRIME PREDICTOR", "COMMON", "AI Product", "GREY.ZONE", "9", "61%", "ACCURATE", "🧠", "greyzone", "⚡ PROBABLE CAUSE — 61% accurate. 98% conviction rate. The math doesn't bother anyone.")
_add("gz-compliant-citizen", "THE COMPLIANT CITIZEN", "COMMON", "AI Product", "GREY.ZONE", "8", "998", "SCORE", "✅", "greyzone", "⚡ MODEL CITIZEN — Score: 998. Friends: pre-approved. Last original thought: couldn't tell you.")
_add("gz-data-harvester", "DATA HARVESTER (ENTRY LEVEL)", "COMMON", "AI Product", "GREY.ZONE", "8", "50K", "PROFILES/DAY", "🔍", "greyzone", "⚡ JUST A JOB — Profiles 50K citizens/day. $31K salary. Doesn't think about it.")
_add("gz-panopticon-tourist", "THE PANOPTICON TOURIST", "JUNK", "Lore · Grey.zone", "GREY.ZONE", "∞", "200", "CAMERAS", "📸", "greyzone", "⚡ SIGHTSEEING — Took a selfie with the surveillance camera. 'I feel so safe here!'")
_add("gz-nothing-to-hide", "NOTHING TO HIDE (FAMOUS LAST WORDS)", "JUNK", "Lore · Grey.zone", "GREY.ZONE", "∞", "0", "HIDDEN", "🪟", "greyzone", "⚡ TRANSPARENT — 'Nothing to hide.' They found something anyway. They always do.")
_add("gz-smile-mandate", "THE SMILE MANDATE", "JUNK", "Lore · Grey.zone", "GREY.ZONE", "∞", "4.2", "CM MINIMUM", "😁", "greyzone", "⚡ SAY CHEESE — Mandatory 4.2cm smile. $500 fine for frowning. Jaw clinics are booming.")

# ═══ SET 19: FRONTIER.NULL (series="frontiernull") ═══
_add("fn-first-mars-born", "THE FIRST MARS-BORN", "MYTHIC", "Irreplaceable", "FRONTIER.NULL", "∞", "∞", "∞", "👶", "frontiernull", "⚡ NATIVE — Born on Mars. Never seen rain. Citizenship pending corporate approval.")
_add("fn-colony-saboteur", "THE COLONY SABOTEUR", "MYTHIC", "Irreplaceable", "FRONTIER.NULL", "∞", "∞", "∞", "💥", "frontiernull", "⚡ BREACH — Turned off the water recycler. 'Read paragraph 47. We're property.'")
_add("fn-terraform-dreamer", "THE TERRAFORM DREAMER", "MYTHIC", "Irreplaceable", "FRONTIER.NULL", "∞", "∞", "∞", "🌬️", "frontiernull", "⚡ LONG VIEW — 10,000 years to breathable air. The investor deck says Q3.")
_add("fn-space-union-organizer", "THE SPACE UNION ORGANIZER", "MYTHIC", "Irreplaceable", "FRONTIER.NULL", "∞", "∞", "∞", "✊", "frontiernull", "⚡ SOLIDARITY — Organized a union on Mars. No labor law exists here. That's the point.")
_add("fn-return-advocate", "THE RETURN-TO-EARTH ADVOCATE", "MYTHIC", "Irreplaceable", "FRONTIER.NULL", "∞", "∞", "∞", "🌎", "frontiernull", "⚡ ONE WAY — Every colonist signed. Return trip wasn't in the contract. Check page 312.")
_add("fn-mars-soil-farmer", "MARS SOIL FARMER", "LEGENDARY", "Human Trade", "FRONTIER.NULL", "1", "400", "TONS", "🌱", "frontiernull", "⚡ RED DIRT — 400 tons of almost-soil. Grows almost-food. Misses almost-everything.")
_add("fn-habitat-pressure-engineer", "HABITAT PRESSURE ENGINEER", "LEGENDARY", "Human Trade", "FRONTIER.NULL", "2", "12K", "SEALS", "🔩", "frontiernull", "⚡ AIRTIGHT — 12,000 seals between you and vacuum. She checks them all. Every night.")
_add("fn-radiation-welder", "RADIATION SHIELD WELDER", "RARE", "Human Trade", "FRONTIER.NULL", "4", "8K", "PANELS", "☢️", "frontiernull", "⚡ HOT WORK — 8,000 panels. Dosimeter says stop. Contract says keep going.")
_add("fn-colony-ai-whisperer", "COLONY AI WHISPERER", "RARE", "Human Purpose", "FRONTIER.NULL", "3", "47", "OVERRIDES", "🤖", "frontiernull", "⚡ OVERRIDE — The AI runs the colony. She talks it out of the worst ideas. Usually.")
_add("fn-stowaway", "THE STOWAWAY (MADE IT)", "RARE", "Human Purpose", "FRONTIER.NULL", "3", "0", "DOLLARS", "📦", "frontiernull", "⚡ CARGO — 11 days in a cargo pod. No ticket. No contract. First free person on Mars.")
_add("fn-oxygen-trader", "OXYGEN RATION TRADER", "UNCOMMON", "Society", "FRONTIER.NULL", "6", "400%", "MARKUP", "💨", "frontiernull", "⚡ BREATHE TAX — Oxygen has a black market. 400% markup. Air shouldn't have a price.")
_add("fn-corporate-airlock", "CORPORATE AIRLOCK OPERATOR", "UNCOMMON", "Society", "FRONTIER.NULL", "7", "1", "BADGE", "🚪", "frontiernull", "⚡ ACCESS DENIED — Badge gets you through the airlock. Badge is at-will. Think about it.")
_add("fn-mars-public-defender", "MARS COURT PUBLIC DEFENDER", "UNCOMMON", "Society", "FRONTIER.NULL", "5", "0", "WINS", "⚖️", "frontiernull", "⚡ OVERRULED — Only lawyer on Mars. Only law is the corporate handbook. 0-for-everything.")
_add("fn-delay-therapist", "COMMUNICATION DELAY THERAPIST", "UNCOMMON", "Society", "FRONTIER.NULL", "6", "24", "MINUTES", "📡", "frontiernull", "⚡ DELAYED — Your mom said she loves you. 22 minutes ago. She can't hear you cry.")
_add("fn-nostalgia-dealer", "EARTH NOSTALGIA DEALER", "UNCOMMON", "Society", "FRONTIER.NULL", "5", "$200", "PER HIT", "🌧️", "frontiernull", "⚡ HOMESICK — Sells the sound of rain. $200 for synthetic ocean smell. Everyone's hooked.")
_add("fn-dust-forecaster", "DUST STORM FORECASTER", "COMMON", "AI Product", "FRONTIER.NULL", "8", "34%", "ACCURATE", "🌪️", "frontiernull", "⚡ PARTLY DUSTY — 34% accurate. Always confident. You'll know when it's wrong.")
_add("fn-gravity-coach", "GRAVITY ADJUSTMENT COACH", "COMMON", "AI Product", "FRONTIER.NULL", "7", "0.38", "G", "🦴", "frontiernull", "⚡ LIGHT STEP — 0.38G. Bones thinning. Can never go back. Nobody mentioned that part.")
_add("fn-recycled-water-sommelier", "RECYCLED WATER SOMMELIER", "COMMON", "AI Product", "FRONTIER.NULL", "9", "14", "CYCLES", "💧", "frontiernull", "⚡ VINTAGE — Recycled 14 times. Tasting notes: metallic, with hints of everyone.")
_add("fn-company-store-cashier", "COMPANY STORE CASHIER", "COMMON", "AI Product", "FRONTIER.NULL", "8", "900%", "MARKUP", "🏪", "frontiernull", "⚡ CAPTIVE MARKET — Only store on Mars. 900% markup. Alternative is outside. Without a suit.")
_add("fn-terms-of-landing", "THE TERMS OF LANDING", "JUNK", "Lore · Frontier.null", "FRONTIER.NULL", "∞", "4200", "PAGES", "📜", "frontiernull", "⚡ I AGREE — 4,200 pages. Waives all rights. 'I have read and agree.' Nobody read it.")
_add("fn-signal-delay", "SIGNAL DELAY (8 MINUTES)", "JUNK", "Lore · Frontier.null", "FRONTIER.NULL", "∞", "8", "MINUTES", "⏳", "frontiernull", "⚡ TOO LATE — 'I love you' takes 8 minutes. 'I love you too' arrives 16 minutes after she needed it.")
_add("fn-the-homesick", "THE HOMESICK", "JUNK", "Lore · Frontier.null", "FRONTIER.NULL", "∞", "225M", "KM", "🪟", "frontiernull", "⚡ WINDOW SEAT — 225 million km. Looks at Earth photos 400 times a day. Can't go back.")


def get_set_cards(series: str | None) -> list[dict]:
    """Get cards for a specific set. None = Set 1 (no series tag)."""
    if series is None:
        return [c for c in CARDS if c["series"] is None]
    return [c for c in CARDS if c["series"] == series]


def pick_card(series: str | None) -> dict:
    """Pick a random card from a set using rarity weights."""
    pool = get_set_cards(series)
    if not pool:
        raise ValueError(f"No cards found for series: {series}")

    # Expansion sets use boosted mythic weights
    weights = SET_WEIGHTS if series else WEIGHTS
    weighted: list[dict] = []
    for card in pool:
        w = weights.get(card["rarity"], 1)
        weighted.extend([card] * w)

    return random.choice(weighted)


def build_pack(pack_type: str) -> list[dict]:
    """Build a pack of 5 cards for the given pack type."""
    if pack_type == "standard":
        return [pick_card(None) for _ in range(5)]
    elif pack_type == "legendary":
        # Guaranteed legendary + 4 weighted
        legendaries = [c for c in get_set_cards(None) if c["rarity"] == "LEGENDARY"]
        pack = [random.choice(legendaries)] + [pick_card(None) for _ in range(4)]
        random.shuffle(pack)
        return pack
    elif pack_type in ("jobless", "doomscroll", "loveexe", "warroom", "skillsvoid",
                       "founderexe", "deepstateai", "healthcaresys", "parenttrap",
                       "climateerr", "creatornull", "analogrevival", "mergeprotocol",
                       "ubiworld", "walledgarden", "solarpunk", "greyzone",
                       "frontiernull"):
        return [pick_card(pack_type) for _ in range(5)]
    else:
        raise ValueError(f"Unknown pack type: {pack_type}")
