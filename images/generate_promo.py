#!/usr/bin/env python3
"""Generate a 5-card promotional image for social media sharing."""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE = Path(__file__).parent

# Card definitions — 5 cards spanning all rarities
CARDS = [
    {
        "id": "the-mother", "name": "THE MOTHER", "rarity": "MYTHIC",
        "category": "Irreplaceable", "atk": "∞", "def": "∞",
        "kscore": "0", "flavor": "GPT-7 passed the Turing test.\nHer toddler didn't care.",
        "symbol": "💫",
    },
    {
        "id": "welder", "name": "THE WELDER", "rarity": "LEGENDARY",
        "category": "Human Trade", "atk": "400K", "def": "SHORTAGE",
        "kscore": "2", "flavor": "55, knees hurt,\nnobody coming to replace him.",
        "symbol": "🔥",
    },
    {
        "id": "therapist", "name": "THE THERAPIST", "rarity": "RARE",
        "category": "Human Purpose", "atk": "160M", "def": "UNTREATED",
        "kscore": "4", "flavor": "Can't feel witnessed\nby what can't suffer.",
        "symbol": "🧠",
    },
    {
        "id": "plumber", "name": "THE PLUMBER", "rarity": "LEGENDARY",
        "category": "Human Trade", "atk": "550K", "def": "SHORTAGE",
        "kscore": "2", "flavor": "Booked until March.\nNo degree. No apologies.",
        "symbol": "🔧",
    },
    {
        "id": "ai-gf", "name": "AI GIRLFRIEND", "rarity": "COMMON",
        "category": "AI Product", "atk": "112M", "def": "SUBSCRIBERS",
        "kscore": "10", "flavor": "112M men chose her.\nLoneliness up 31%.",
        "symbol": "💘",
    },
]

RARITY_COLORS = {
    "MYTHIC": (255, 255, 255),
    "LEGENDARY": (200, 168, 75),
    "RARE": (155, 89, 208),
    "UNCOMMON": (33, 150, 200),
    "COMMON": (212, 68, 144),
    "JUNK": (102, 112, 128),
}

RARITY_BG = {
    "MYTHIC": (30, 25, 35),
    "LEGENDARY": (25, 22, 12),
    "RARE": (20, 12, 28),
    "UNCOMMON": (12, 18, 25),
    "COMMON": (25, 12, 18),
    "JUNK": (15, 16, 18),
}

# Fonts
FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"


def draw_card(card: dict, card_w: int, card_h: int) -> Image.Image:
    """Render a single card as an image."""
    rarity = card["rarity"]
    accent = RARITY_COLORS[rarity]
    bg = RARITY_BG[rarity]

    img = Image.new("RGB", (card_w, card_h), bg)
    draw = ImageDraw.Draw(img)

    # Border
    border_w = 3
    draw.rectangle([0, 0, card_w - 1, card_h - 1], outline=accent, width=border_w)

    # Inner border glow for mythic
    if rarity == "MYTHIC":
        for i in range(1, 4):
            alpha_color = tuple(max(0, c - i * 40) for c in accent)
            draw.rectangle(
                [border_w + i, border_w + i, card_w - border_w - i - 1, card_h - border_w - i - 1],
                outline=alpha_color,
            )

    margin = 18
    y = margin

    # Rarity label
    font_rarity = ImageFont.truetype(FONT_MONO, 14)
    draw.text((margin, y), rarity, fill=accent, font=font_rarity)
    y += 22

    # Card name
    font_name = ImageFont.truetype(FONT_BOLD, 24)
    draw.text((margin, y), card["name"], fill=(240, 240, 240), font=font_name)
    y += 34

    # Category
    font_cat = ImageFont.truetype(FONT_REG, 14)
    draw.text((margin, y), card["category"], fill=tuple(min(255, c + 60) for c in accent), font=font_cat)
    y += 26

    # Card art
    art_path = BASE / "cards" / f"{card['id']}.png"
    if art_path.exists():
        art = Image.open(art_path)
        art_area_w = card_w - margin * 2
        art_area_h = int(art_area_w * 1.0)  # square crop
        art = art.resize((art_area_w, art_area_h), Image.LANCZOS)
        img.paste(art, (margin, y))
        # Art border
        draw.rectangle(
            [margin - 1, y - 1, margin + art_area_w, y + art_area_h],
            outline=tuple(c // 2 for c in accent),
            width=2,
        )
        y += art_area_h + 10

    # ATK / DEF line
    font_stats = ImageFont.truetype(FONT_MONO, 18)
    stats_text = f"ATK {card['atk']}  DEF {card['def']}"
    draw.text((margin, y), stats_text, fill=accent, font=font_stats)
    y += 28

    # Karpathy Score bar
    font_kscore = ImageFont.truetype(FONT_MONO, 12)
    ks_label = f"KARPATHY SCORE: {card['kscore']}/10"
    draw.text((margin, y), ks_label, fill=(140, 140, 140), font=font_kscore)
    y += 20

    # Score bar
    bar_w = card_w - margin * 2
    bar_h = 8
    draw.rectangle([margin, y, margin + bar_w, y + bar_h], fill=(40, 40, 40))
    ks_val = 10 if card["kscore"] == "∞" else int(card["kscore"])
    fill_w = int(bar_w * ks_val / 10)
    if fill_w > 0:
        ks_color = (200, 50, 50) if ks_val >= 7 else (200, 168, 75) if ks_val >= 4 else (50, 180, 80)
        draw.rectangle([margin, y, margin + fill_w, y + bar_h], fill=ks_color)
    y += 18

    # Flavor text
    font_flavor = ImageFont.truetype(FONT_SERIF, 14)
    for line in card["flavor"].split("\n"):
        draw.text((margin, y), line, fill=(160, 160, 160), font=font_flavor)
        y += 19

    return img


def main():
    card_w = 380
    card_h = 620
    gap = 28
    padding = 50
    header_h = 90
    footer_h = 60

    total_w = padding * 2 + card_w * 5 + gap * 4
    total_h = padding + header_h + card_h + footer_h

    canvas = Image.new("RGB", (total_w, total_h), (8, 8, 12))
    draw = ImageDraw.Draw(canvas)

    # Header
    font_title = ImageFont.truetype(FONT_BOLD, 42)
    font_sub = ImageFont.truetype(FONT_MONO, 18)

    title = "AI CARDS — 2030 SURVIVAL EDITION"
    bbox = draw.textbbox((0, 0), title, font=font_title)
    tw = bbox[2] - bbox[0]
    draw.text(((total_w - tw) // 2, padding - 8), title, fill=(240, 240, 240), font=font_title)

    subtitle = "162 CARDS  ·  6 SETS  ·  30 MYTHICS  ·  aicards.fun"
    bbox2 = draw.textbbox((0, 0), subtitle, font=font_sub)
    sw = bbox2[2] - bbox2[0]
    draw.text(((total_w - sw) // 2, padding + 46), subtitle, fill=(120, 120, 120), font=font_sub)

    # Render cards
    for i, card in enumerate(CARDS):
        card_img = draw_card(card, card_w, card_h)
        x = padding + i * (card_w + gap)
        y = padding + header_h
        canvas.paste(card_img, (x, y))

    # Footer
    font_footer = ImageFont.truetype(FONT_MONO, 14)
    footer_text = "COLLECT  ·  BATTLE  ·  TRADE ON SUI BLOCKCHAIN"
    bbox3 = draw.textbbox((0, 0), footer_text, font=font_footer)
    fw = bbox3[2] - bbox3[0]
    draw.text(
        ((total_w - fw) // 2, padding + header_h + card_h + 15),
        footer_text,
        fill=(100, 100, 100),
        font=font_footer,
    )

    out_path = BASE.parent / "promo-5cards.png"
    canvas.save(out_path, "PNG", optimize=True)
    print(f"Saved: {out_path} ({canvas.size[0]}x{canvas.size[1]})")


if __name__ == "__main__":
    main()
