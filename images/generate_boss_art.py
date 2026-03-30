#!/usr/bin/env python3
"""Generate raid boss art for AI Cards TCG using DALL-E 3.

Usage:
    OPENAI_API_KEY=sk-... python3 images/generate_boss_art.py
    OPENAI_API_KEY=sk-... python3 images/generate_boss_art.py --boss replaced_overnight
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
    "Dark menacing atmosphere, dramatic lighting. "
)

BOSS_SCENES: dict[str, str] = {
    "replaced_overnight": (
        "A monstrous office chair with mechanical spider legs, "
        "its seat replaced by a glowing computer monitor showing a job listing. "
        "A ghostly business suit hangs empty above it. "
        "Threatening, looming over a tiny desk."
    ),
    "white_collar_bloodbath": (
        "A towering stock ticker machine transformed into a guillotine, "
        "its blade shaped like a downward graph arrow. "
        "Briefcases and diplomas scattered at its base. "
        "Corporate skyscraper silhouettes behind."
    ),
    "the_last_interview": (
        "A massive ornate door slamming shut, seen from the rejected side. "
        "The door handle is a robotic hand giving a thumbs down. "
        "A crumpled resume floats in the air. "
        "The hallway stretches infinitely behind."
    ),
    "automation_anxiety": (
        "A giant mechanical keyboard where each key is a tombstone, "
        "mechanical fingers pressing them rapidly. "
        "Sparks and binary code erupting from the keys. "
        "A terrified figure reflected in the screen above."
    ),
    "the_pivot": (
        "A massive spinning compass needle gone haywire, "
        "spinning so fast it creates a vortex. "
        "Career ladders and self-help books being sucked into the spiral. "
        "A figure clinging to the edge of the whirlpool."
    ),
    "the_loneliness_machine": (
        "A huge cracked heart made of circuit boards and phone screens, "
        "glowing with artificial warmth. Charging cables extend like tentacles "
        "from its base, reaching toward lonely silhouettes. "
        "A price tag dangles from the heart."
    ),
    "the_content_flood": (
        "An enormous tidal wave made of newspapers, screens, and documents, "
        "crashing over a tiny lighthouse. The wave is grey and lifeless, "
        "each page identical. A single human writer on the lighthouse "
        "holds a pen like a sword against the flood."
    ),
    "degree_devalued": (
        "A giant diploma scroll curling in on itself and crumbling to dust, "
        "the mortarboard cap falling off a cliff. "
        "Below, a robot casually juggles textbooks. "
        "Pile of student loan bills beneath."
    ),
    "surveillance_creep": (
        "A colossal unblinking eye formed from hundreds of small camera lenses, "
        "mounted on a corporate building. Its pupil is a red progress bar. "
        "Tiny workers scurry below, each with a number floating above them. "
        "One worker's number is circled in red."
    ),
    "gig_economy_endgame": (
        "A massive autonomous vehicle with a shark mouth grille, "
        "driving over a pile of car keys and steering wheels. "
        "The headlights are cold and predatory. "
        "Empty driver seats visible through the windows, "
        "a 'NO HUMANS NEEDED' vibe."
    ),
    "the_great_pretending": (
        "A corporate boardroom table shaped like a stage, "
        "executives wearing theatrical masks of concern while holding "
        "scissors behind their backs. Pink slips rain from the ceiling "
        "like confetti. A stock chart arrow points triumphantly upward."
    ),
    "the_hard_truth": (
        "A massive cracked mirror showing a reflection that's decades older "
        "than the person standing before it. The cracks radiate outward "
        "from a central impact point shaped like a lightning bolt. "
        "Behind the figure, an hourglass with no sand left."
    ),
}

OUTPUT_DIR = Path(__file__).parent / "bosses"


def generate_boss(client: OpenAI, boss_id: str, scene: str) -> Path:
    """Generate a single boss image and save it."""
    output_path = OUTPUT_DIR / f"{boss_id}.png"
    if output_path.exists():
        log.info("Skipping %s — already exists", boss_id)
        return output_path

    prompt = STYLE_PREFIX + scene
    log.info("Generating %s ...", boss_id)

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    log.info("Downloading %s", boss_id)

    import httpx
    img_data = httpx.get(image_url, timeout=30).content
    output_path.write_bytes(img_data)
    log.info("Saved %s (%d KB)", output_path.name, len(img_data) // 1024)

    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate AI Cards raid boss art via DALL-E 3")
    parser.add_argument("--boss", type=str, help="Generate a single boss (e.g. 'replaced_overnight')")
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Set OPENAI_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(api_key=api_key)
    OUTPUT_DIR.mkdir(exist_ok=True)

    if args.boss:
        if args.boss not in BOSS_SCENES:
            print(f"Unknown boss: {args.boss}. Options: {', '.join(BOSS_SCENES)}", file=sys.stderr)
            sys.exit(1)
        generate_boss(client, args.boss, BOSS_SCENES[args.boss])
        return

    for i, (boss_id, scene) in enumerate(BOSS_SCENES.items()):
        generate_boss(client, boss_id, scene)
        if i < len(BOSS_SCENES) - 1:
            time.sleep(2)  # rate limit buffer

    log.info("Done! %d boss images generated in images/bosses/", len(BOSS_SCENES))
    log.info("Run: cd images/bosses && for f in *.png; do convert \"$f\" -resize 256x256 \"$f\"; done")


if __name__ == "__main__":
    main()
