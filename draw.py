#!/usr/bin/env python3
"""Draw THE WORLD TODAY front page for Wednesday 25 November 2026.

A 1024x1024 newspaper front page: masthead, one lead story with a small
market chart, four more stories in two columns, and an In Brief strip.
Plain ASCII text only, DejaVu fonts, so every glyph renders cleanly.
Layout is built top-down with a running cursor so sections never overlap.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 251, 244)
INK = (17, 17, 17)
GREY = (90, 86, 78)
RED = (139, 0, 0)
RULE = (40, 40, 40)
LIGHT = (214, 208, 194)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

MX = 36          # left margin
RX = 988         # right edge
COL_W = 452      # story column width
GAP = 28
X2 = MX + COL_W + GAP

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(text, fnt, x, y, max_w, leading, color=INK):
    """Draw wrapped paragraph, return y below the last line."""
    for line in wrap(text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def hline(y, x0=MX, x1=RX, width=2, color=RULE):
    d.line([(x0, y), (x1, y)], fill=color, width=width)


def kicker(text, x, y):
    f = font(SANS_B, 19)
    d.text((x, y), text, font=f, fill=RED)
    return y + 26


def fit_font(path, text, max_w, start):
    """Largest font size at or below start whose text fits max_w."""
    size = start
    while size > 10 and font(path, size).getlength(text) > max_w:
        size -= 2
    return font(path, size)


# ---- top dateline -------------------------------------------------------
top_f = font(SANS_B, 17)
d.text((MX, 22), "WEDNESDAY 25 NOVEMBER 2026", font=top_f, fill=INK)
right = "WORLD NEWS  •  ONE PAGE"
d.text((RX - top_f.getlength(right), 22), right, font=top_f, fill=GREY)
hline(50, width=2)

# ---- masthead, sized to fit the page width ------------------------------
mast = fit_font(SERIF_B, "THE WORLD TODAY", RX - MX, 90)
title = "THE WORLD TODAY"
tw = mast.getlength(title)
d.text(((W - tw) / 2, 52), title, font=mast, fill=INK)
mast_bottom = 52 + mast.size + 4
hline(mast_bottom, width=3)
hline(mast_bottom + 6, width=1)

# ---- date strip ---------------------------------------------------------
y = mast_bottom + 14
strip_f = font(SERIF, 21)
strip = "Wednesday 25 November 2026  —  The day in world news"
sw = strip_f.getlength(strip)
d.text(((W - sw) / 2, y), strip, font=strip_f, fill=GREY)
y += 32
hline(y, width=1, color=LIGHT)

# ---- lead story: Nvidia -------------------------------------------------
y += 12
lead_top = y
y = kicker("MARKETS  •  LEAD STORY", MX, y)
lead_h = font(SERIF_B, 40)
y = para("Huang admits mistakes as Nvidia rally cools",
         lead_h, MX, y, 600, 47)
y = para("Jensen Huang, reinstated as Nvidia chief after a suspected "
         "spy scandal, says he is in therapy and made some terrible "
         "mistakes. Shares jumped 31.5 percent on Monday, regaining "
         "about $1 trillion, then slipped again.",
         font(SERIF, 21), MX, y + 6, 600, 25)
lead_bottom = y

# small market chart, right of the lead text
cx, cy, cw, chh = 668, lead_top, 320, 180
d.rectangle([cx, cy, cx + cw, cy + chh], outline=RULE, width=2)
d.text((cx + 12, cy + 8), "NVIDIA SHARES", font=font(SANS_B, 16), fill=INK)
d.text((cx + 12, cy + 30), "Mon +31.5%  •  then fading",
       font=font(SANS, 16), fill=GREY)
pts = [(cx + 14, cy + 155), (cx + 60, cy + 150), (cx + 105, cy + 138),
       (cx + 150, cy + 92), (cx + 195, cy + 60), (cx + 240, cy + 76),
       (cx + 285, cy + 100), (cx + 306, cy + 112)]
d.line(pts, fill=RED, width=4, joint="curve")
for px, py in pts:
    d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED)
d.text((cx + 14, cy + chh - 22), "FRI", font=font(SANS, 14), fill=GREY)
d.text((cx + 150, cy + chh - 22), "MON", font=font(SANS, 14), fill=GREY)
d.text((cx + 272, cy + chh - 22), "TUE", font=font(SANS, 14), fill=GREY)

y = max(lead_bottom, cy + chh) + 8
hline(y, width=2)

# ---- second row: China / Huawei ----------------------------------------
y += 10
row2_top = y
h2 = font(SERIF_B, 28)
body = font(SERIF, 19)

ya = kicker("CHINA", MX, row2_top)
ya = para("China investigates top Shanghai official",
          h2, MX, ya, COL_W, 33)
ya = para("Beijing investigates Chen Jining, a Politburo member and "
         "the Communist Party chief of Shanghai, in a rare move "
         "against a senior leader.",
         body, MX, ya + 4, COL_W, 25)

yb = kicker("TECH AND TRADE", X2, row2_top)
yb = para("US jury convicts Huawei of trade-secret theft",
          h2, X2, yb, COL_W, 33)
yb = para("A federal jury finds the Chinese telecoms giant guilty of "
         "stealing trade secrets, in a case that has long shadowed "
         "US-China tech ties.",
         body, X2, yb + 4, COL_W, 25)

y = max(ya, yb) + 8
hline(y, width=1, color=LIGHT)

# ---- third row: Riyadh / Ukraine + Sarkozy ------------------------------
y += 10
row3_top = y

ya = kicker("MIDDLE EAST", MX, row3_top)
ya = para("Houthi strike hits Riyadh tower; 11 hurt",
          h2, MX, ya, COL_W, 33)
ya = para("A Houthi attack hits a tower at the King Abdullah Financial "
         "Centre in Riyadh, injuring 11 people, including two Indians.",
         body, MX, ya + 4, COL_W, 25)

yb = kicker("EUROPE", X2, row3_top)
yb = para("Kyiv says it hit Russian ship in Gulf of Finland",
          h2, X2, yb, COL_W, 33)
yb = para("President Zelenskiy confirms Ukraine struck a Russian ship "
         "in the Gulf of Finland.",
         body, X2, yb + 4, COL_W, 25)
yb = para("Sarkozy to stand trial for corruption",
          font(SERIF_B, 22), X2, yb + 8, COL_W, 27)
yb = para("Nicolas Sarkozy is ordered to stand trial for corruption, "
         "with his wife Carla Bruni.",
         body, X2, yb + 4, COL_W, 25)

y = max(ya, yb) + 8
hline(y, width=2)

# ---- In Brief, two columns ---------------------------------------------
y += 10
d.text((MX, y), "IN BRIEF", font=font(SANS_B, 19), fill=RED)
y += 26
briefs_l = [
    "Three tankers hit by mines in the Strait of Hormuz.",
    "NATO to send early-warning aircraft to Poland.",
    "Hanoi hot-pot blast kills six and injures 14.",
]
briefs_r = [
    "Magnitude 5.3 earthquake strikes Nepal.",
    "Shein to pay $100 million in FTC settlement.",
    "Trump awards Rudy Giuliani the Medal of Freedom.",
]
bf = font(SANS, 17)
by = y
for item in briefs_l:
    d.text((MX, by), "\u2022  " + item, font=bf, fill=INK)
    by += 20
by = y
for item in briefs_r:
    d.text((X2, by), "\u2022  " + item, font=bf, fill=INK)
    by += 20
y = by + 6

# ---- footer -------------------------------------------------------------
hline(y, width=1, color=LIGHT)
foot = font(SANS, 14)
d.text((MX, y + 4), "THE WORLD TODAY", font=foot, fill=GREY)
d.text((RX - foot.getlength("WEDNESDAY 25 NOVEMBER 2026"), y + 4),
       "WEDNESDAY 25 NOVEMBER 2026", font=foot, fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
