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
    elif pack_type in ("jobless", "doomscroll", "loveexe"):
        return [pick_card(pack_type) for _ in range(5)]
    else:
        raise ValueError(f"Unknown pack type: {pack_type}")
