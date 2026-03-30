#!/usr/bin/env python3
"""Generate the main AI Cards logo + Set 1 icon via DALL-E 3.

Usage:
    OPENAI_API_KEY=sk-... python3 images/generate_logo.py
    OPENAI_API_KEY=sk-... python3 images/generate_logo.py --only main
    OPENAI_API_KEY=sk-... python3 images/generate_logo.py --only set1
    OPENAI_API_KEY=sk-... python3 images/generate_logo.py --only shop
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

LOGOS = {
    "main": {
        "path": "logo.png",
        "prompt": (
            "Logo wordmark for 'AI CARDS' — a dark, gritty collectible card game. "
            "The letters should look like they were carved or stamped in metal, "
            "weathered and distressed. Dense crosshatching style, underground comix aesthetic. "
            "The 'AI' portion glows faintly red like heated metal. "
            "The 'CARDS' portion is stark white with cracks and wear. "
            "Below in tiny letters: '2030 SURVIVAL EDITION'. "
            "Pure black background. Horizontal layout. "
            "Raw, subversive, satirical tone. "
            "No other imagery — just the text wordmark."
        ),
        "size": "1792x1024",
    },
    "set1": {
        "path": "sets/standard.png",
        "prompt": (
            "Minimal black and white icon logo, dense crosshatching, underground comix style, "
            "stark contrast, no text, no words, no letters, no numbers. "
            "Single centered symbolic object on pure white background. "
            "Square composition, bold linework, satirical edge. "
            "A human hand reaching upward through cracked concrete, "
            "fingers spread wide, gripping nothing but air. "
            "Cracks radiate from where the hand breaks through. "
            "Symbol of survival against automation."
        ),
        "size": "1024x1024",
    },
    "shop": {
        "path": "sets/shop.png",
        "prompt": (
            "Minimal black and white icon logo, dense crosshatching, underground comix style, "
            "stark contrast, no text, no words, no letters, no numbers. "
            "Single centered symbolic object on pure white background. "
            "Square composition, bold linework. "
            "An old-fashioned cash register with a digital screen, "
            "the drawer open and overflowing with cards instead of money. "
            "Symbol of a card shop."
        ),
        "size": "1024x1024",
    },
}

OUTPUT_DIR = Path(__file__).parent


def generate(client: OpenAI, key: str, config: dict) -> Path:
    output_path = OUTPUT_DIR / config["path"]
    if output_path.exists():
        log.info("Skipping %s — already exists", key)
        return output_path

    output_path.parent.mkdir(exist_ok=True)
    log.info("Generating %s ...", key)

    response = client.images.generate(
        model="dall-e-3",
        prompt=config["prompt"],
        size=config["size"],
        quality="hd",
        n=1,
    )

    image_url = response.data[0].url
    log.info("Downloading %s", key)

    import httpx
    img_data = httpx.get(image_url, timeout=30).content
    output_path.write_bytes(img_data)
    log.info("Saved %s (%d KB)", output_path.name, len(img_data) // 1024)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate AI Cards logos via DALL-E 3")
    parser.add_argument("--only", type=str, choices=list(LOGOS.keys()), help="Generate only one")
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Set OPENAI_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    targets = {args.only: LOGOS[args.only]} if args.only else LOGOS
    for i, (key, config) in enumerate(targets.items()):
        generate(client, key, config)
        if i < len(targets) - 1:
            time.sleep(2)

    log.info("Done!")
    log.info("Resize: convert images/logo.png -resize 600x -quality 90 images/logo.png")
    log.info("Resize: convert images/sets/standard.png -resize 96x96 images/sets/standard.png")
    log.info("Resize: convert images/sets/shop.png -resize 96x96 images/sets/shop.png")


if __name__ == "__main__":
    main()
