#!/usr/bin/env python3
"""Generate set logo icons for AI Cards TCG using DALL-E 3.

Usage:
    OPENAI_API_KEY=sk-... python3 images/generate_set_logos.py
    OPENAI_API_KEY=sk-... python3 images/generate_set_logos.py --set jobless
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
    "Minimal black and white icon logo, dense crosshatching, underground comix style, "
    "stark contrast, no text, no words, no letters, no numbers. "
    "Single centered symbolic object on pure white background. "
    "Square composition, bold linework, satirical edge. "
)

SET_LOGOS: dict[str, str] = {
    "jobless": (
        "A cracked briefcase lying open and empty, cobwebs inside, "
        "a wilted flower growing from it. Symbol of mass unemployment."
    ),
    "doomscroll": (
        "A smartphone melting downward like a Salvador Dali clock, "
        "the screen showing an infinite spiral. Hypnotic doom scroll symbol."
    ),
    "loveexe": (
        "A pixelated heart with a visible crack running through it, "
        "circuit board traces visible inside. Digital love glitching out."
    ),
    "warroom": (
        "Military crosshairs overlaid on a chess piece (king), "
        "with tiny drone silhouettes circling it. Autonomous warfare symbol."
    ),
    "skillsvoid": (
        "An hourglass where the sand has been replaced by falling binary digits, "
        "the bottom half empty and cracked. Skills becoming obsolete."
    ),
    "founderexe": (
        "A throne made of burning venture capital money, "
        "a crown tilted and falling off. Startup hubris symbol."
    ),
    "deepstateai": (
        "A massive unblinking eye made of camera lenses and circuit boards, "
        "with a tiny human silhouette reflected in the pupil. Surveillance state."
    ),
    "healthcaresys": (
        "A caduceus (medical symbol) where the snakes are replaced by USB cables, "
        "the wings replaced by loading spinners. Healthcare automation."
    ),
    "parenttrap": (
        "A baby crib with a tablet screen as the mattress, "
        "glowing softly. A mobile above it made of social media icons. Digital childhood."
    ),
    "climateerr": (
        "A thermometer bursting at the top like a volcano, "
        "the mercury replaced by factory smokestacks. Climate debt symbol."
    ),
    "creatornull": (
        "A broken paintbrush crossed with a severed pen, "
        "surrounded by AI-generated geometric perfection. Creative extinction."
    ),
    "analogrevival": (
        "A vinyl record with a sprouting plant growing from the center hole, "
        "roots wrapping around it. Analog renaissance symbol."
    ),
    "mergeprotocol": (
        "A human brain and a circuit board merging together at the center, "
        "neurons and wires intertwining. Human-AI merge."
    ),
    "ubiworld": (
        "An open hand receiving coins that are also pills, "
        "falling from a cloud. Universal basic income as medication."
    ),
    "walledgarden": (
        "A beautiful garden enclosed in a glass jar with a corporate padlock, "
        "flowers pressing against the glass. Corporate consolidation."
    ),
    "solarpunk": (
        "A solar panel growing like a sunflower, with roots visible underground "
        "and a small crack in the stem. Optimistic future with hidden fragility."
    ),
    "greyzone": (
        "A fingerprint where half the ridges are barcode lines, "
        "dissolving at the edges. Identity and surveillance resistance."
    ),
    "frontiernull": (
        "A space helmet visor reflecting Earth very small and far away, "
        "a single tear track on the glass. Mars colony isolation."
    ),
}

OUTPUT_DIR = Path(__file__).parent / "sets"


def generate_logo(client: OpenAI, set_key: str, scene: str) -> Path:
    """Generate a single set logo and save it."""
    output_path = OUTPUT_DIR / f"{set_key}.png"
    if output_path.exists():
        log.info("Skipping %s — already exists", set_key)
        return output_path

    prompt = STYLE_PREFIX + scene
    log.info("Generating %s ...", set_key)

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    log.info("Downloading %s", set_key)

    import httpx
    img_data = httpx.get(image_url, timeout=30).content
    output_path.write_bytes(img_data)
    log.info("Saved %s (%d KB)", output_path.name, len(img_data) // 1024)

    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate AI Cards set logos via DALL-E 3")
    parser.add_argument("--set", type=str, help="Generate a single set (e.g. 'jobless')")
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Set OPENAI_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(api_key=api_key)
    OUTPUT_DIR.mkdir(exist_ok=True)

    if args.set:
        if args.set not in SET_LOGOS:
            print(f"Unknown set: {args.set}. Options: {', '.join(SET_LOGOS)}", file=sys.stderr)
            sys.exit(1)
        generate_logo(client, args.set, SET_LOGOS[args.set])
        return

    for i, (set_key, scene) in enumerate(SET_LOGOS.items()):
        generate_logo(client, set_key, scene)
        if i < len(SET_LOGOS) - 1:
            time.sleep(2)  # rate limit buffer

    log.info("Done! %d logos generated in images/sets/", len(SET_LOGOS))

    # Print HTML snippet
    print("\n<!-- Set logo images -->")
    for set_key in SET_LOGOS:
        print(f'<!-- {set_key}: images/sets/{set_key}.png -->')


if __name__ == "__main__":
    main()
