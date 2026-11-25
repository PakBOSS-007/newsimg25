#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news poster (1024x1024 PNG).

Build tool for the make.fun news-image-20261125 entry. It renders
entry.png from the day's verified headlines using PIL + Liberation
fonts (system fonts on the author's machine). The entry program
(main.ts) only copies the finished PNG; this script is not run in
the grader's sandbox.

Content: six stories from Wednesday 25 November 2026, each verified
against that day's reporting (Hormuz tankers, Houthi Riyadh attack,
Huawei conviction, Ukraine refinery strikes, Australia-Solomon
treaty, Shenzhou-24 and Pakistan's first astronaut).
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 56
CONTENT_W = W - 2 * MARGIN

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

NAVY = (27, 47, 74)
GOLD = (232, 197, 71)
WHITE = (255, 255, 255)
INK = (20, 20, 20)
GREY = (90, 90, 90)
RULE = (200, 200, 200)
RED = (176, 58, 46)
MAROON = (123, 36, 28)
BLUE = (27, 79, 114)
TEAL = (14, 102, 85)
GREEN = (30, 132, 73)
BROWN = (147, 81, 22)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_tracked(draw, xy, text, fnt, fill, tracking=2):
    """Draw uppercase text with extra letter spacing."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x


def main():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------
    d.rectangle([0, 0, W, 140], fill=NAVY)
    title_f = font(SERIF_B, 74)
    title = "THE WORLD"
    tw = d.textlength(title, font=title_f)
    d.text(((W - tw) / 2, 14), title, font=title_f, fill=WHITE)
    date_f = font(SANS_B, 30)
    date = "WEDNESDAY, 25 NOVEMBER 2026"
    dw = d.textlength(date, font=date_f)
    d.text(((W - dw) / 2, 96), date, font=date_f, fill=GOLD)
    d.rectangle([0, 140, W, 144], fill=GOLD)

    # ---- Lead story: Hormuz tankers ------------------------------
    y = 168
    label_f = font(SANS_B, 18)
    draw_tracked(d, (MARGIN, y), "MIDDLE EAST  ·  ENERGY", label_f, TEAL, tracking=2)
    y += 30
    head_f = font(SERIF_B, 46)
    for line in wrap(d, "Two oil tankers hit mines and catch fire in the Strait of Hormuz", head_f, CONTENT_W):
        d.text((MARGIN, y), line, font=head_f, fill=INK)
        y += 54
    y += 6
    deck_f = font(SANS_R, 21)
    deck = ("Iran's Revolutionary Guard said the vessels struck naval mines and exploded "
            "as they tried to cross the world's busiest oil waterway.")
    for line in wrap(d, deck, deck_f, CONTENT_W):
        d.text((MARGIN, y), line, font=deck_f, fill=GREY)
        y += 28

    # ---- Divider ---------------------------------------------------
    y = 402
    d.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=2)

    # ---- Five more stories ----------------------------------------
    stories = [
        ("CONFLICT  ·  SAUDI ARABIA", MAROON,
         "Houthi drone attack on a Riyadh tower injures 11",
         "The strike hit a tower in the capital's financial district; the Houthis also said they attacked the Ras Tanura refinery."),
        ("TECH  ·  UNITED STATES", BLUE,
         "US jury convicts Huawei of stealing trade secrets",
         "Huawei was found guilty on 10 of 12 counts, including bank fraud, but cleared of racketeering."),
        ("WAR  ·  RUSSIA", RED,
         "Ukrainian drones set two Russian oil refineries ablaze",
         "Drones hit the Syzran and Kuibyshev refineries in the Samara region; one person was killed."),
        ("DIPLOMACY  ·  PACIFIC", GREEN,
         "Australia and Solomon Islands sign treaty barring foreign bases",
         "The treaty precludes any foreign military or security base on the Solomon Islands."),
        ("SPACE  ·  CHINA", TEAL,
         "China launches Pakistan's first astronaut into orbit",
         "Shenzhou-24 docked with the Tiangong station hours after launch, carrying Pakistan's first astronaut."),
    ]
    y = 424
    sh_f = font(SERIF_B, 27)
    ss_f = font(SANS_R, 19)
    for i, (label, color, head, summ) in enumerate(stories):
        draw_tracked(d, (MARGIN, y), label, label_f, color, tracking=2)
        y += 28
        for line in wrap(d, head, sh_f, CONTENT_W):
            d.text((MARGIN, y), line, font=sh_f, fill=INK)
            y += 33
        y += 2
        for line in wrap(d, summ, ss_f, CONTENT_W):
            d.text((MARGIN, y), line, font=ss_f, fill=GREY)
            y += 25
        if i < len(stories) - 1:
            y += 8
            d.line([MARGIN, y, W - MARGIN, y], fill=(228, 228, 228), width=1)
            y += 14

    # ---- Footer ----------------------------------------------------
    foot_f = font(SANS_R, 15)
    foot = "Six stories that defined the day  ·  Reported 25 November 2026"
    fw = d.textlength(foot, font=foot_f)
    d.text(((W - fw) / 2, 986), foot, font=foot_f, fill=GREY)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
