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
    elif pack_type in ("jobless", "doomscroll", "loveexe", "warroom", "skillsvoid",
                       "founderexe", "deepstateai", "healthcaresys", "parenttrap",
                       "climateerr", "creatornull"):
        return [pick_card(pack_type) for _ in range(5)]
    else:
        raise ValueError(f"Unknown pack type: {pack_type}")
