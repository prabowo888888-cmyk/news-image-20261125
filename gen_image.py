#!/usr/bin/env python3
"""Draw the front page for 'Sum up 25 November's world news in one image'.

A single 1024x1024 newspaper-style page: a bold masthead naming the day,
then five stories, each with its own coloured tag, a short headline, a
two-line summary and a small drawn motif. Everything is drawn with PIL
primitives, no photos and no network, so the output is fully deterministic.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (20, 38, 74)
GOLD = (212, 175, 105)
INK = (24, 24, 24)
GREY = (74, 74, 74)
RULE = (200, 200, 200)

# tag, colour, headline, summary -- each summary kept short enough for two
# lines at 21 px across the text column.
STORIES = [
    (
        "SPACE",
        (31, 111, 178),
        "Pakistan's first astronaut lifts off for China's Tiangong station",
        "Muhammad Zeeshan Ali, a Pakistan Air Force pilot, rode Shenzhou-24 "
        "to orbit -- the first Pakistani in space and the first foreign "
        "guest aboard Tiangong.",
    ),
    (
        "CONFLICT",
        (163, 51, 39),
        "Ukraine's drone war reaches the Mediterranean as Putin warns of payback",
        "Kyiv confirmed sea-drone strikes on Russian ships off Libya and in "
        "the Gulf of Finland. Moscow called them terrorism and vowed a "
        "response.",
    ),
    (
        "MARKETS",
        (139, 47, 47),
        "AI stocks slide as Trump readies new tariffs on China and Europe",
        "The Nasdaq fell 1.5% and Nvidia about 6% after reports of planned "
        "tariffs on China, the EU and 14 more economies. Micron dropped 11%.",
    ),
    (
        "TECH",
        (91, 58, 142),
        "US jury convicts Huawei of stealing trade secrets and bank fraud",
        "A Brooklyn jury found the Chinese telecom giant guilty on 10 of 12 "
        "counts, but cleared it of racketeering. Huawei says it will appeal.",
    ),
    (
        "MIDDLE EAST",
        (176, 119, 31),
        "Iraq orders federal forces to seize Kurdish oilfields",
        "Baghdad told its troops to take over oilfields and crossings in "
        "Kurdish-run areas. Kurdish leaders rejected the order outright.",
    ),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels, without breaking words."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_rocket(d, x, y, s):
    # A simple white rocket: body, nose cone, fins and flame.
    d.polygon([(x + s * 0.5, y + s * 0.08), (x + s * 0.30, y + s * 0.34),
               (x + s * 0.70, y + s * 0.34)], fill="white")
    d.rounded_rectangle([x + s * 0.30, y + s * 0.32, x + s * 0.70, y + s * 0.72],
                        radius=int(s * 0.08), fill="white")
    d.ellipse([x + s * 0.42, y + s * 0.40, x + s * 0.58, y + s * 0.56],
              fill=(31, 111, 178))
    d.polygon([(x + s * 0.30, y + s * 0.60), (x + s * 0.14, y + s * 0.80),
               (x + s * 0.34, y + s * 0.74)], fill="white")
    d.polygon([(x + s * 0.70, y + s * 0.60), (x + s * 0.86, y + s * 0.80),
               (x + s * 0.66, y + s * 0.74)], fill="white")
    d.polygon([(x + s * 0.42, y + s * 0.72), (x + s * 0.50, y + s * 0.94),
               (x + s * 0.58, y + s * 0.72)], fill=(255, 176, 66))


def draw_ship(d, x, y, s):
    # A ship on waves with a burst above it.
    d.polygon([(x + s * 0.16, y + s * 0.52), (x + s * 0.84, y + s * 0.52),
               (x + s * 0.72, y + s * 0.72), (x + s * 0.28, y + s * 0.72)],
              fill="white")
    d.rectangle([x + s * 0.44, y + s * 0.30, x + s * 0.56, y + s * 0.52],
                fill="white")
    d.polygon([(x + s * 0.50, y + s * 0.10), (x + s * 0.58, y + s * 0.26),
               (x + s * 0.42, y + s * 0.26)], fill=(255, 176, 66))
    for i, wy in enumerate((0.80, 0.88)):
        d.arc([x + s * 0.10 + i * s * 0.06, y + s * wy, x + s * 0.46 + i * s * 0.06,
               y + s * wy + s * 0.10], 180, 360, fill="white", width=5)
        d.arc([x + s * 0.54 + i * s * 0.06, y + s * wy, x + s * 0.90 + i * s * 0.06,
               y + s * wy + s * 0.10], 180, 360, fill="white", width=5)


def draw_chart(d, x, y, s):
    # Axes with a falling line and arrowhead.
    d.line([x + s * 0.16, y + s * 0.16, x + s * 0.16, y + s * 0.84,
            x + s * 0.86, y + s * 0.84], fill="white", width=6)
    pts = [(0.24, 0.30), (0.40, 0.44), (0.52, 0.38), (0.68, 0.62), (0.80, 0.72)]
    xy = [(x + s * px, y + s * py) for px, py in pts]
    d.line(xy, fill=(255, 176, 66), width=7, joint="curve")
    d.polygon([(x + s * 0.80, y + s * 0.72), (x + s * 0.66, y + s * 0.66),
               (x + s * 0.72, y + s * 0.82)], fill=(255, 176, 66))


def draw_chip(d, x, y, s):
    # A microchip: square body, pins, inner die.
    for i in range(4):
        px = x + s * (0.26 + i * 0.16)
        d.rectangle([px, y + s * 0.10, px + s * 0.06, y + s * 0.24], fill="white")
        d.rectangle([px, y + s * 0.76, px + s * 0.06, y + s * 0.90], fill="white")
    for i in range(4):
        py = y + s * (0.26 + i * 0.16)
        d.rectangle([x + s * 0.10, py, x + s * 0.24, py + s * 0.06], fill="white")
        d.rectangle([x + s * 0.76, py, x + s * 0.90, py + s * 0.06], fill="white")
    d.rounded_rectangle([x + s * 0.24, y + s * 0.24, x + s * 0.76, y + s * 0.76],
                        radius=int(s * 0.06), fill="white")
    d.rectangle([x + s * 0.38, y + s * 0.38, x + s * 0.62, y + s * 0.62],
                fill=(91, 58, 142))


def draw_derrick(d, x, y, s):
    # An oil derrick: tapered tower with cross braces and a pump arm.
    d.polygon([(x + s * 0.30, y + s * 0.12), (x + s * 0.52, y + s * 0.12),
               (x + s * 0.62, y + s * 0.82), (x + s * 0.20, y + s * 0.82)],
              fill="white")
    d.line([x + s * 0.28, y + s * 0.30, x + s * 0.56, y + s * 0.46], fill=(176, 119, 31), width=5)
    d.line([x + s * 0.56, y + s * 0.30, x + s * 0.26, y + s * 0.46], fill=(176, 119, 31), width=5)
    d.line([x + s * 0.26, y + s * 0.60, x + s * 0.58, y + s * 0.60], fill=(176, 119, 31), width=5)
    d.line([x + s * 0.52, y + s * 0.12, x + s * 0.86, y + s * 0.30], fill="white", width=7)
    d.ellipse([x + s * 0.74, y + s * 0.62, x + s * 0.90, y + s * 0.78], fill="white")


ICONS = [draw_rocket, draw_ship, draw_chart, draw_chip, draw_derrick]


def main():
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)

    # Masthead: navy band naming the day, loud and unmissable.
    d.rectangle([0, 0, W, 140], fill=NAVY)
    f_small = font(BOLD, 20)
    f_title = font(BOLD, 64)
    f_date = font(BOLD, 30)
    d.text((W / 2, 16), "THE WORLD IN ONE PAGE", font=f_small, fill=GOLD,
           anchor="ma")
    d.text((W / 2, 36), "WORLD NEWS", font=f_title, fill="white", anchor="ma")
    d.text((W / 2, 102), "WEDNESDAY, 25 NOVEMBER 2026", font=f_date,
           fill=GOLD, anchor="ma")

    f_tag = font(BOLD, 19)
    f_head = font(BOLD, 27)
    f_body = font(REG, 20)

    y = 150
    row_h, gap = 160, 4
    text_x, text_w = 188, 800
    for i, (tag, colour, headline, summary) in enumerate(STORIES):
        # Icon tile.
        d.rounded_rectangle([36, y + 8, 164, y + 136], radius=16, fill=colour)
        ICONS[i](d, 36, y + 8, 128)

        # Tag chip.
        tag_w = int(d.textlength(tag, font=f_tag)) + 24
        d.rounded_rectangle([text_x, y + 6, text_x + tag_w, y + 34],
                            radius=14, fill=colour)
        d.text((text_x + 12, y + 20), tag, font=f_tag, fill="white",
               anchor="lm")

        # Headline, up to two lines -- anything longer would clip.
        head_lines = wrap(d, headline, f_head, text_w)
        assert len(head_lines) <= 2, f"headline too long: {headline!r}"
        hy = y + 44
        for line in head_lines:
            d.text((text_x, hy), line, font=f_head, fill=INK)
            hy += 31

        # Summary, up to two lines.
        body_lines = wrap(d, summary, f_body, text_w)
        assert len(body_lines) <= 2, f"summary too long: {summary!r}"
        by = hy + 2
        for line in body_lines:
            d.text((text_x, by), line, font=f_body, fill=GREY)
            by += 24

        if i < len(STORIES) - 1:
            d.line([36, y + row_h + 1, W - 36, y + row_h + 1], fill=RULE,
                   width=2)
        y += row_h + gap

    # Footer credit line.
    f_foot = font(REG, 17)
    d.text((W / 2, 978), "Sources: Reuters  -  AP  -  US Dept. of Justice  -  Al Jazeera",
           font=f_foot, fill=GREY, anchor="ma")

    # Thin navy frame.
    d.rectangle([0, 0, W - 1, H - 1], outline=NAVY, width=6)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
