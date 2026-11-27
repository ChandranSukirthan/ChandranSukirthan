"""Regenerate the looping profile banner: python3 scripts/create_banner.py."""

from math import pi, sin
from pathlib import Path
import random

from PIL import Image, ImageChops, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "profile-banner.gif"
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
WIDTH, HEIGHT = 1370, 610
FRAME_COUNT = 20


def text_mask(label, position, font):
    mask = Image.new("L", (WIDTH, HEIGHT))
    ImageDraw.Draw(mask).text(position, label, font=font, fill=255)
    return mask


def banner_frame(index, stars, name_masks):
    phase = 2 * pi * index / FRAME_COUNT
    image = Image.new("RGB", (WIDTH, HEIGHT), "#030815")
    draw = ImageDraw.Draw(image)

    # A quiet moving constellation, short accents, and diagonal light trails.
    for number, (x, y, size) in enumerate(stars):
        brightness = (sin(phase + number * 1.71) + 1) / 2
        blue = int(42 + 92 * brightness)
        draw.rectangle((x, y, x + size, y + size), fill=(7, blue, min(196, blue + 37)))
    offset = int(34 * sin(phase))
    draw.line((715 + offset, 602, 1100 + offset, 351), fill="#0a4259", width=2)
    draw.line((1000 - offset, 542, 1250 - offset, 384), fill="#0a384d", width=1)
    draw.rounded_rectangle((76, 66, 143 + int(10 * sin(phase)), 70), radius=2, fill="#16dff6")

    draw.text((158, 48), "HELLO, I’M", font=ImageFont.truetype(FONT, 34), fill="#11e6f7")

    # The glint travels across the letters while the name remains visible.
    shine_x = int(80 + 1040 * index / FRAME_COUNT)
    band = Image.new("L", (WIDTH, HEIGHT))
    ImageDraw.Draw(band).polygon(
        [(shine_x - 110, 125), (shine_x - 15, 125),
         (shine_x + 130, 380), (shine_x + 35, 380)],
        fill=255,
    )
    for mask in name_masks:
        shadow = Image.new("RGB", (WIDTH, HEIGHT), "#103f52")
        image.paste(shadow, (0, 4), mask)
        image.paste("#f7fbff", (0, 0), mask)
        gleam = ImageChops.multiply(mask, band)
        image.paste("#7cf4ff", (0, 0), gleam)

    draw = ImageDraw.Draw(image)
    pulse = (sin(phase - 0.8) + 1) / 2
    cyan = (7, int(196 + 34 * pulse), int(224 + 24 * pulse))
    sky = (35, int(168 + 40 * pulse), 251)
    degree_font = ImageFont.truetype(FONT, 49)
    draw.text((77, 420), "BSc (Hons) in Information Technology", font=degree_font, fill=cyan)
    draw.text((77, 486), "Specializing in Artificial Intelligence", font=degree_font, fill=sky)

    # The progress trace gently grows and returns as the GIF loops.
    length = int(125 + 45 * (sin(phase) + 1) / 2)
    draw.rounded_rectangle((78, 567, 78 + length, 571), radius=2, fill="#15d8ee")
    return image.quantize(colors=96, method=Image.Quantize.FASTOCTREE)


def main():
    rng = random.Random(17)
    stars = [(rng.randrange(WIDTH), rng.randrange(HEIGHT), rng.choice((2, 2, 3, 5, 7)))
             for _ in range(105)]
    name_font = ImageFont.truetype(FONT, 116)
    name_masks = [
        text_mask("Sukirthan", (75, 126), name_font),
        text_mask("Chandrakumar", (75, 253), name_font),
    ]
    frames = [banner_frame(index, stars, name_masks) for index in range(FRAME_COUNT)]
    OUTPUT.parent.mkdir(exist_ok=True)
    frames[0].save(
        OUTPUT, save_all=True, append_images=frames[1:], duration=120,
        loop=0, optimize=True, disposal=2,
    )
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    main()
