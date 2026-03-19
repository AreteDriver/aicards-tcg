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
_add("ai-therapist", "THE AI THERAPIST APP", "COMMON", "AI Product", "2030 Survival", "10", "20M", "SESSIONS", "🧘")
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

    weighted: list[dict] = []
    for card in pool:
        w = WEIGHTS.get(card["rarity"], 1)
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
    elif pack_type in ("jobless", "doomscroll", "loveexe", "warroom", "skillsvoid"):
        return [pick_card(pack_type) for _ in range(5)]
    else:
        raise ValueError(f"Unknown pack type: {pack_type}")
