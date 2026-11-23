"""Draw entry.png: a newspaper front page summing up Sunday 22 Nov 2026.

Pure local build script (Pillow + DejaVu fonts). The submitted program is
main.py, which only copies the finished entry.png to /output/entry.png
with the standard library, so the grader needs no network and no Pillow.
Run: python3 draw_image.py  -> writes entry.png (1024x1024, < 1 MiB).
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (17, 17, 17)
NAVY = (15, 42, 68)
RED = (185, 28, 28)
BLUE = (29, 78, 216)
TEAL = (13, 116, 128)
GOLD = (245, 197, 66)
GREY = (90, 90, 90)
LINE = (200, 192, 172)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    out = []
    for para in text.split("\n"):
        out.extend(textwrap.wrap(para, width=width) or [""])
    # re-wrap by pixel width: textwrap by chars is rough, so split long lines
    lines = []
    for line in out:
        while draw.textlength(line, font=fnt) > width:
            cut = len(line) - 1
            while cut > 0 and draw.textlength(line[:cut], font=fnt) > width:
                cut -= 1
            # break at a space if possible
            sp = line.rfind(" ", 0, cut)
            if sp > 10:
                cut = sp
            lines.append(line[:cut].rstrip())
            line = line[cut:].lstrip()
        lines.append(line)
    return lines


def text_block(draw, xy, text, fnt, fill, width, leading=1.25):
    x, y = xy
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def kicker(draw, x, y, label, color=RED):
    f = font(SANS_B, 20)
    draw.text((x, y), label, font=f, fill=color)
    return y + 28


def headline(draw, x, y, text, size=34, width=440, color=INK):
    f = font(SERIF_B, size)
    return text_block(draw, (x, y), text, f, color, width, leading=1.08)


def body(draw, x, y, text, size=21, width=440, color=INK):
    f = font(SANS, size)
    return text_block(draw, (x, y), text, f, color, width, leading=1.3)


def ship(draw, x, y, s=1.0):
    # simple warship silhouette on waves
    draw.rectangle([x, y + 34, x + 150, y + 52], fill=NAVY)
    draw.polygon([(x + 20, y + 34), (x + 40, y + 6), (x + 60, y + 34)], fill=NAVY)
    draw.rectangle([x + 70, y + 18, x + 110, y + 34], fill=NAVY)
    draw.rectangle([x + 115, y + 26, x + 128, y + 34], fill=NAVY)
    for i, wx in enumerate([x - 6, x + 40, x + 90, x + 130]):
        draw.arc([wx, y + 56, wx + 34, y + 70], 0, 180, fill=BLUE, width=4)


def flats(draw, x, y):
    # apartment block, top corner broken
    draw.rectangle([x, y + 20, x + 130, y + 110], fill=(120, 110, 95))
    draw.polygon([(x, y + 20), (x + 55, y), (x + 80, y + 20)], fill=(120, 110, 95))
    draw.line([x + 55, y, x + 80, y + 20], fill=RED, width=3)
    for r in range(2):
        for c in range(4):
            draw.rectangle(
                [x + 14 + c * 30, y + 34 + r * 32, x + 32 + c * 30, y + 52 + r * 32],
                fill=GOLD,
            )


def capitol(draw, x, y):
    draw.rectangle([x, y + 70, x + 150, y + 110], fill=NAVY)
    draw.rectangle([x + 10, y + 54, x + 140, y + 70], fill=NAVY)
    draw.pieslice([x + 55, y + 6, x + 95, y + 58], 180, 360, fill=NAVY)
    draw.rectangle([x + 72, y - 2, x + 78, y + 10], fill=NAVY)
    for c in range(5):
        draw.rectangle(
            [x + 18 + c * 26, y + 76, x + 34 + c * 26, y + 104], fill=PAPER
        )


def chart_down(draw, x, y):
    draw.line(
        [(x, y + 20), (x + 40, y + 44), (x + 75, y + 34), (x + 110, y + 78),
         (x + 145, y + 96)],
        fill=RED, width=7, joint="curve",
    )
    draw.polygon(
        [(x + 145, y + 96), (x + 128, y + 96), (x + 145, y + 78)], fill=RED
    )
    for gy in [y + 20, y + 55, y + 90]:
        draw.line([(x, gy), (x + 150, gy)], fill=(210, 210, 210), width=1)


def planet(draw, x, y):
    draw.ellipse([x, y + 10, x + 110, y + 110], fill=(176, 141, 87))
    draw.ellipse([x + 22, y + 30, x + 52, y + 62], fill=(140, 105, 60))
    draw.ellipse([x + 60, y + 62, x + 88, y + 88], fill=(140, 105, 60))
    draw.arc([x - 14, y, x + 124, y + 120], 200, 340, fill=TEAL, width=5)
    draw.arc([x - 14, y, x + 124, y + 120], 20, 160, fill=TEAL, width=5)


def globe(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(38, 132, 210))
    draw.ellipse([cx - r + 28, cy - r + 18, cx - r + 78, cy - r + 58], fill=(74, 160, 90))
    draw.ellipse([cx + 8, cy + 12, cx + 62, cy + 52], fill=(74, 160, 90))
    draw.ellipse([cx - r + 18, cy + 34, cx - r + 52, cy + 66], fill=(74, 160, 90))
    draw.arc([cx - r, cy - r, cx + r, cy + r], 0, 360, fill=NAVY, width=4)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ---
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.text((32, 18), "THE WORLD IN ONE DAY", font=font(SERIF_B, 62), fill=(255, 255, 255))
    d.text((32, 96), "SUNDAY,  22  NOVEMBER  2026", font=font(SANS_B, 30), fill=GOLD)
    d.text((688, 100), "SIX STORIES  •  ONE DAY", font=font(SANS_B, 22), fill=(255, 255, 255))

    # --- lead: COP31 ---
    y = 168
    y = kicker(d, 32, y, "CLIMATE  •  ANTALYA, TURKEY")
    y = headline(d, 32, y, "COP31 ENDS\nWITH NO DEAL", size=52, width=560)
    y = body(
        d, 32, y + 6,
        "Climate talks collapse after the EU and about 130 countries "
        "reject a draft with no mention of fossil fuels. The longest "
        "UN climate summit on record.",
        size=23, width=560,
    )
    globe(d, 830, 300, 105)
    d.text((724, 414), "NO DEAL", font=font(SANS_B, 34), fill=RED)
    d.line([32, 452, 992, 452], fill=LINE, width=2)

    # --- 2x2 grid ---
    panels = [
        ("BENGHAZI, LIBYA", "Russian warship hit at sea",
         "A Russian warship docked at Benghazi is hit by suspected "
         "Ukrainian sea drones.",
         ship),
        ("DYMER, UKRAINE", "Drone hits flats near Kyiv",
         "A Russian drone partly destroys a five-storey block. "
         "14 people are missing.",
         flats),
        ("WASHINGTON, USA", "Democrats take the House",
         "Democrats win at least 258 seats, their largest House "
         "majority since 1992.",
         capitol),
        ("MARKETS", "Stocks fall in AI sell-off",
         "The S&P 500 falls 3.7% and Japan's Nikkei drops 5.06%.",
         chart_down),
    ]
    gx, gy = 32, 472
    cw, ch = 468, 204
    for i, (kick, head, txt, icon) in enumerate(panels):
        x = gx + (i % 2) * (cw + 24)
        yy = gy + (i // 2) * (ch + 10)
        d.rectangle([x, yy, x + cw, yy + ch], outline=LINE, width=2)
        d.rectangle([x, yy, x + cw, yy + 6], fill=NAVY)
        kicker(d, x + 16, yy + 18, kick)
        headline(d, x + 16, yy + 46, head, size=26, width=436)
        body(d, x + 16, yy + 96, txt, size=19, width=290)
        icon(d, x + 318, yy + 85)

    # --- bottom strip: Mercury + also ---
    by = 890
    d.rectangle([0, by, W, H], fill=NAVY)
    d.text((32, by + 12), "MERCURY", font=font(SANS_B, 20), fill=GOLD)
    d.text((32, by + 38), "BepiColombo reaches Mercury",
           font=font(SERIF_B, 27), fill=(255, 255, 255))
    d.text((32, by + 74),
           "The European-Japanese probe enters orbit",
           font=font(SANS, 18), fill=(220, 225, 235))
    d.text((32, by + 98),
           "around Mercury after an 8-year journey.",
           font=font(SANS, 18), fill=(220, 225, 235))
    planet(d, 522, by + 6)
    d.line([640, by + 14, 640, H - 14], fill=(90, 110, 140), width=2)
    d.text((664, by + 12), "ALSO", font=font(SANS_B, 20), fill=GOLD)
    d.text((664, by + 38), "Las Vegas: Verstappen",
           font=font(SANS_B, 17), fill=(255, 255, 255))
    d.text((664, by + 60), "wins the Grand Prix.",
           font=font(SANS, 17), fill=(220, 225, 235))
    d.text((664, by + 86), "Mexico: 'El Chapo Isidro'",
           font=font(SANS_B, 17), fill=(255, 255, 255))
    d.text((664, by + 108), "captured in Sinaloa.",
           font=font(SANS, 17), fill=(220, 225, 235))

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
