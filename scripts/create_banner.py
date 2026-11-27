"""Regenerate the profile banner: python3 scripts/create_banner.py."""

from pathlib import Path
import random

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "profile-banner.png"
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
WIDTH, HEIGHT = 1370, 610


def main():
    image = Image.new("RGB", (WIDTH, HEIGHT), "#030711")
    draw = ImageDraw.Draw(image)
    rng = random.Random(17)

    # Sparse cyan pixels and fine diagonal traces echo the supplied reference.
    for _ in range(105):
        x, y = rng.randrange(WIDTH), rng.randrange(HEIGHT)
        side = rng.choice((2, 2, 3, 4, 7))
        color = rng.choice(("#07374b", "#0b5165", "#105d72"))
        draw.rectangle((x, y, x + side, y + side), fill=color)
    draw.line((710, 606, 1080, 357), fill="#0a394e", width=1)
    draw.line((1018, 538, 1235, 389), fill="#0a394e", width=1)

    bright = "#08e6fa"
    draw.rounded_rectangle((77, 64, 140, 68), radius=2, fill=bright)
    draw.text((158, 49), "HELLO, I’M", font=ImageFont.truetype(FONT, 34), fill=bright)

    name_font = ImageFont.truetype(FONT, 116)
    for y, label in ((126, "Sukirthan"), (253, "Chandrakumar")):
        draw.text((77, y + 4), label, font=name_font, fill="#073845")
        draw.text((75, y), label, font=name_font, fill="#ffffff")

    degree_font = ImageFont.truetype(FONT, 49)
    draw.text((77, 420), "BSc (Hons) in Information Technology", font=degree_font, fill=bright)
    draw.text((77, 486), "Specializing in Artificial Intelligence", font=degree_font, fill="#31bafa")

    OUTPUT.parent.mkdir(exist_ok=True)
    image.save(OUTPUT, optimize=True)
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    main()
