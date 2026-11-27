"""Regenerate the small animated profile greeting: python3 scripts/create_welcome.py."""

from pathlib import Path
from math import sin, pi

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "welcome.gif"
SIZE = 240
SCALE = 3
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def font(size):
    return ImageFont.truetype(FONT, size * SCALE)


def frame(index):
    s = SCALE
    canvas = Image.new("RGBA", (SIZE * s, SIZE * s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    def ellipse(box, fill):
        draw.ellipse(tuple(int(v * s) for v in box), fill=fill)

    def rounded(box, radius, fill):
        draw.rounded_rectangle(tuple(int(v * s) for v in box), radius * s, fill=fill)

    def line(points, fill, width):
        draw.line([(int(x * s), int(y * s)) for x, y in points], fill=fill, width=width * s, joint="curve")

    ellipse((3, 3, 237, 237), "#22d3ee")
    ellipse((7, 7, 233, 233), "#10213f")
    ellipse((17, 17, 223, 223), "#162e54")

    # Greeting bubble.
    rounded((23, 28, 105, 70), 18, "#f8fafc")
    draw.polygon([(72 * s, 67 * s), (84 * s, 67 * s), (79 * s, 80 * s)], fill="#f8fafc")
    draw.text((44 * s, 36 * s), "Hi!", font=font(24), fill="#10213f")

    # Character: hair behind the face, shirt, face and eyes.
    ellipse((72, 83, 158, 176), "#101827")
    rounded((65, 151, 174, 220), 30, "#19b7b5")
    ellipse((79, 91, 151, 164), "#bd805f")
    ellipse((77, 84, 153, 122), "#101827")
    ellipse((103, 109, 155, 129), "#101827")
    ellipse((95, 130, 100, 135), "#162031")
    ellipse((127, 130, 132, 135), "#162031")
    draw.arc((103 * s, 132 * s, 125 * s, 150 * s), 15, 165, fill="#582d30", width=2 * s)

    # Moving arm creates a clear, short wave in the loop.
    swing = sin(index * 2 * pi / 12)
    hand_x = 191 + int(12 * swing)
    hand_y = 86 + int(8 * swing)
    line([(161, 166), (183, 143), (hand_x, hand_y + 14)], "#bd805f", 15)
    ellipse((hand_x - 12, hand_y - 14, hand_x + 12, hand_y + 14), "#bd805f")
    for offset in (-7, 0, 7):
        line([(hand_x + offset, hand_y - 7), (hand_x + offset + 2, hand_y - 22)], "#bd805f", 4)

    # Message remains readable at the README display width.
    rounded((24, 184, 216, 227), 15, "#07152b")
    draw.text((51 * s, 190 * s), "Welcome to my", font=font(14), fill="#ffffff")
    draw.text((81 * s, 208 * s), "GitHub!", font=font(14), fill="#67e8f9")
    return canvas.resize((SIZE, SIZE), Image.Resampling.LANCZOS)


def main():
    OUTPUT.parent.mkdir(exist_ok=True)
    frames = []
    for index in range(12):
        rgba = frame(index)
        white_bg = Image.new("RGB", rgba.size, "#ffffff")
        white_bg.paste(rgba, mask=rgba.getchannel("A"))
        indexed = white_bg.quantize(colors=255)
        palette = indexed.getpalette()
        palette[0:3] = [255, 255, 255]
        indexed.putpalette(palette)
        indexed.paste(0, mask=rgba.getchannel("A").point(lambda a: 255 if a < 128 else 0))
        indexed.info["transparency"] = 0
        frames.append(indexed)
    frames[0].save(
        OUTPUT,
        save_all=True,
        append_images=frames[1:],
        duration=115,
        loop=0,
        transparency=0,
        disposal=2,
        optimize=False,
    )
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    main()
