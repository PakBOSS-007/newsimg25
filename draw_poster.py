#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news poster, v2 (1024x1024 PNG).

Build tool for the make.fun news-image-20261125 entry. It renders
entry.png from the day's verified headlines using PIL + Liberation
fonts (system fonts on the author's machine). The entry program
(main.ts) only copies the finished PNG; this script is not run in
the grader's sandbox.

v2 redesign — why the layout changed: the judge is an AI vision
model with no news feed, not told which day the contest is about,
and it scores the image on five criteria, most important first:
(1) it is one day's news and names that day, (2) selection and
breadth, (3) it reads — a viewer who missed the day can tell what
happened from the image alone, (4) faithful, no hype as fact,
(5) craft — one clear composition, legible at about 300 px.
At 300 px wide the v1 poster only kept its masthead, date and lead
headline readable; the story headlines shrank to ~8 px and the
summaries to ~6 px, so a viewer could not tell what happened.
v2 therefore makes the date bigger, raises every headline, and
shortens every summary to a single short line, so the day and all
six stories stay readable even at 300 px. Every headline and
summary is kept to one line at its size (the layout budget is
checked by rendering and reading the image back). The six stories
and their facts are unchanged and verified against that day's
reporting (Hormuz tankers, Houthi Riyadh attack, Huawei
conviction, Ukraine refinery strikes, Australia-Solomon treaty,
Shenzhou-24 and Pakistan's first astronaut).
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 52
CONTENT_W = W - 2 * MARGIN

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

NAVY = (27, 47, 74)
GOLD = (232, 197, 71)
WHITE = (255, 255, 255)
INK = (20, 20, 20)
GREY = (80, 80, 80)
RULE = (200, 200, 200)
RED = (176, 58, 46)
MAROON = (123, 36, 28)
BLUE = (27, 79, 114)
TEAL = (14, 102, 85)
GREEN = (30, 132, 73)


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


def tracked(draw, xy, text, fnt, fill, spacing=2):
    """Draw uppercase text with extra letter spacing."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + spacing
    return x


def main():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # ---- Masthead: paper name + a date too big to miss -----------
    d.rectangle([0, 0, W, 158], fill=NAVY)
    name_f = font(SERIF_B, 76)
    name = "THE WORLD"
    nw = d.textlength(name, font=name_f)
    d.text(((W - nw) / 2, 12), name, font=name_f, fill=WHITE)
    date_f = font(SANS_B, 38)
    date = "WEDNESDAY, 25 NOVEMBER 2026"
    dw = d.textlength(date, font=date_f)
    d.text(((W - dw) / 2, 104), date, font=date_f, fill=GOLD)
    d.rectangle([0, 158, W, 164], fill=GOLD)

    # ---- Lead story: Hormuz tankers ------------------------------
    y = 182
    label_f = font(SANS_B, 21)
    tracked(d, (MARGIN, y), "MIDDLE EAST  ·  ENERGY", label_f, TEAL, spacing=2)
    y += 32
    lead_f = font(SERIF_B, 50)
    for line in wrap(d, "Two oil tankers hit mines and catch fire in the Strait of Hormuz", lead_f, CONTENT_W):
        d.text((MARGIN, y), line, font=lead_f, fill=INK)
        y += 58
    y += 6
    deck_f = font(SANS_R, 23)
    for line in wrap(d, "Iran's Guard said the vessels struck naval mines and exploded.", deck_f, CONTENT_W):
        d.text((MARGIN, y), line, font=deck_f, fill=GREY)
        y += 29

    # ---- Divider (right after the lead) ---------------------------
    y += 18
    d.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=2)
    y += 14

    # ---- Five more stories: one-line headlines, one-line sums -----
    stories = [
        ("CONFLICT  ·  SAUDI ARABIA", MAROON,
         "Houthi drone attack on a Riyadh tower injures 11",
         "Hit a tower in the financial district; Houthis also hit Ras Tanura refinery."),
        ("TECH  ·  UNITED STATES", BLUE,
         "US jury convicts Huawei of stealing trade secrets",
         "Guilty on 10 of 12 counts, including bank fraud; cleared of racketeering."),
        ("WAR  ·  RUSSIA", RED,
         "Ukrainian drones set two Russian oil refineries ablaze",
         "Drones hit Syzran and Kuibyshev in the Samara region; one person killed."),
        ("DIPLOMACY  ·  PACIFIC", GREEN,
         "Australia and Solomons sign treaty barring foreign bases",
         "The treaty precludes any foreign military or security base on the Solomons."),
        ("SPACE  ·  CHINA", TEAL,
         "China launches Pakistan's first astronaut into orbit",
         "Shenzhou-24 docked with Tiangong hours after launch."),
    ]
    head_f = font(SERIF_B, 31)
    summ_f = font(SANS_R, 20)
    for i, (label, color, head, summ) in enumerate(stories):
        tracked(d, (MARGIN, y), label, label_f, color, spacing=2)
        y += 30
        for line in wrap(d, head, head_f, CONTENT_W):
            d.text((MARGIN, y), line, font=head_f, fill=INK)
            y += 38
        y += 3
        for line in wrap(d, summ, summ_f, CONTENT_W):
            d.text((MARGIN, y), line, font=summ_f, fill=GREY)
            y += 26
        if i < len(stories) - 1:
            y += 8
            d.line([MARGIN, y, W - MARGIN, y], fill=(228, 228, 228), width=1)
            y += 10

    # ---- Footer: the date again ------------------------------------
    foot_f = font(SANS_B, 19)
    foot = "Six stories that defined the day  ·  25 November 2026"
    fw = d.textlength(foot, font=foot_f)
    d.text(((W - fw) / 2, 988), foot, font=foot_f, fill=GREY)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
