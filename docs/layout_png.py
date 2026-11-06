"""Render the Totem keymap (Qwerty-Lafayette + Arsenik) as one PNG page."""
import sys
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1]
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
f_main = ImageFont.truetype(FONTB, 17)
f_small = ImageFont.truetype(FONT, 11)
f_title = ImageFont.truetype(FONTB, 22)
f_head = ImageFont.truetype(FONTB, 30)
f_note = ImageFont.truetype(FONT, 14)

C = {  # category: (fill, text)
    "alpha": ("#ffffff", "#222222"),
    "mod":   ("#d6e8ff", "#123a6b"),
    "thumb": ("#ffe1b3", "#6b3d00"),
    "sym":   ("#e3d7ff", "#3b2470"),
    "num":   ("#d5f5dc", "#14532d"),
    "nav":   ("#cdf0f7", "#0b4a57"),
    "dead":  ("#ffd1dc", "#7a1030"),
    "sys":   ("#ffc9c9", "#7a0000"),
    "fn":    ("#fff3b0", "#5c4b00"),
    "app":   ("#f0e0d0", "#5a3a20"),
    "trans": ("#eeeeee", "#aaaaaa"),
    "none":  ("#f7f7f7", "#f7f7f7"),
}

# Key = (label, hold label or "", category). 38 keys in Totem order.
def k(l, h="", c="alpha"): return (l, h, c)
T = k("▽", "", "trans")
N = k("", "", "none")

LAYERS = [
 ("BASE — Qwerty + home-row mods", [
  k("Q"),k("W"),k("E"),k("R"),k("T"), k("Y"),k("U"),k("I"),k("O"),k("P"),
  k("A"),k("S","Gui","mod"),k("D","Ctrl","mod"),k("F","Alt","mod"),k("G"),
  k("H"),k("J","Alt","mod"),k("K","Ctrl","mod"),k("L","Gui","mod"),k("★","dead key","dead"),
  k("<  >","","alpha"),k("Z"),k("X"),k("C"),k("V"),k("B"),
  k("N"),k("M"),k(", ;"),k(". :"),k("/ ?"),k("' \"","","alpha"),
  k("Tab","","thumb"),k("⌫","Shift","thumb"),k("Space","NAV","thumb"),
  k("⏎","SYM","thumb"),k("Del","","thumb"),k("ADJ","hold","thumb"),
 ]),
 ("SYM — hold ⏎ (Lafayette AltGr)", [
  *[k(x,"","sym") for x in "^<>$%@&*'`"],
  *[k(x,"","sym") for x in "{()}=\\+-/\""],
  N, *[k(x,"","sym") for x in "~[]_#|!;:?"], T,
  T, k("NUM","hold","thumb"), k("Space","","thumb"), T, T, T,
 ]),
 ("NAV — hold Space", [
  k("Tab","","nav"),k("Home","","nav"),k("↑","","nav"),k("End","","nav"),k("PgUp","","nav"),
  k("/","","num"),k("7","","num"),k("8","","num"),k("9","","num"),k("Gui+E","","app"),
  k("Ctrl+A","all","app"),k("←","","nav"),k("↓","","nav"),k("→","","nav"),k("PgDn","","nav"),
  k("-","","num"),k("4","","num"),k("5","","num"),k("6","","num"),k("0","","num"),
  T,k("Ctrl+Z","undo","app"),k("Ctrl+X","cut","app"),k("Ctrl+C","copy","app"),k("Ctrl+V","paste","app"),k("⇧Tab","","nav"),
  k(",","","num"),k("1","","num"),k("2","","num"),k("3","","num"),k(".","","num"),T,
  T,k("Del","","thumb"),T, k("Esc","DESK","thumb"),T,T,
 ]),
 ("NUM — hold ⏎ + ⌫", [
  *[k(x,"","sym") for x in "!@#$%^&*()"],
  *[k(x,"","num") for x in "1234567890"],
  T, k("¡","★+1","dead"),k("«","★+2","dead"),k("»","★+3","dead"),k("£","★+4","dead"),k("€","★+5","dead"),
  N, k("-","","num"),k(",","","num"),k(".","","num"),k("/","","num"),T,
  T,T,k("nbsp","narrow","thumb"), T,T,T,
 ]),
 ("DESK — hold Space + hold ⏎", [
  *[k("G⇧"+x,"","app") for x in "1234567890"],
  *[k("Gui+"+x,"","app") for x in "1234567890"],
  T,T,T,T,T,T, T,T,T,T,T,T,
  T,T,T, T,T,T,
 ]),
 ("ADJ — hold right outer thumb", [
  k("Reset","","sys"),k("BT clr","","sys"),k("USB/BT","","sys"),T,T, T,k("F7","","fn"),k("F8","","fn"),k("F9","","fn"),k("F12","","fn"),
  k("Boot","loader","sys"),k("BT next","","sys"),T,T,T, T,k("F4","","fn"),k("F5","","fn"),k("F6","","fn"),k("F11","","fn"),
  T,T,k("BT prev","","sys"),T,T,T, T,k("F1","","fn"),k("F2","","fn"),k("F3","","fn"),k("F10","","fn"),T,
  T,T,T, T,T,T,
 ]),
 ("TVP 1 — TVPaint (toggle A+S+D)", [
  k("Tab","","app"),k("I","","app"),k("Ctrl+Alt","","app"),k("O","","app"),k("C-F20","","app"), N,N,N,N,N,
  k("L","TVP 2","thumb"),k("←","","nav"),k("Alt","","mod"),k("→","","nav"),k("Space","","app"), N,N,N,N,N,
  k("J","","app"),k("Shift","","mod"),k("Ctrl+C","","app"),k("⌫","","app"),k("Ctrl+V","","app"),k("C-F19","","app"),
  N,N,N,N,N,N,
  T,k("C-F14","","app"),k("C-F13","","app"), N,N,N,
 ]),
 ("TVP 2 — hold L in TVP 1", [
  k("C-F18","","app"),k("⇧I","","app"),k("⇧Home","","app"),k("⇧O","","app"),k("⇧F","","app"), T,k("F7","","fn"),k("F8","","fn"),k("F9","","fn"),k("F12","","fn"),
  T,k("⇧←","","nav"),k("C-F17","","app"),k("⇧→","","nav"),k("⏎","","app"), T,k("F4","","fn"),k("F5","","fn"),k("F6","","fn"),k("F11","","fn"),
  T,k("J","","app"),k("⇧C","","app"),k("C-F16","","app"),k("⇧V","","app"),k("C-F15","","app"),
  T,k("F1","","fn"),k("F2","","fn"),k("F3","","fn"),k("F10","","fn"),T,
  T,k("C-F12","","app"),k("C-F11","","app"), T,T,T,
 ]),
]

KW, KH, G = 62, 52, 5          # key size, gap
U = KW + G
GAP_MID = 70                   # gap between halves
# (row, col) per key position; col 0..11 (0 and 11 = outer pinky keys)
POS = ([(0, c) for c in range(1, 6)] + [(0, c) for c in range(6, 11)]
     + [(1, c) for c in range(1, 6)] + [(1, c) for c in range(6, 11)]
     + [(2, c) for c in range(0, 12)]
     + [(3, c) for c in (3, 4, 5, 6, 7, 8)])
# Totem column stagger (fraction of key height), outer pinky to inner index
STAG = [0.5, 0.4, 0.12, 0.0, 0.12, 0.25]
STAG = STAG + STAG[::-1]
# Thumb fan: (dx in key units, dy in key units, rotation deg) for left L1 L2 L3
THUMB = [(2.55, 3.35, 18), (3.6, 3.55, 6), (4.65, 3.55, -6)]

PW = int(12 * U + GAP_MID + 20)
PH = int(4.9 * (KH + G) + 60)
COLS, MARGIN = 2, 30
rows = (len(LAYERS) + 1 + COLS - 1) // COLS
W = COLS * PW + (COLS + 1) * MARGIN
H = 80 + rows * (PH + MARGIN) + MARGIN
img = Image.new("RGB", (W, H), "#fafaf7")
d = ImageDraw.Draw(img)
d.text((MARGIN, 24), "TOTEM — Qwerty-Lafayette + Arsenik", font=f_head, fill="#222")

def fit(txt, dd):
    for size in (17, 15, 13, 11):
        f = ImageFont.truetype(FONTB, size)
        if dd.textlength(txt, font=f) <= KW - 8:
            return f
    return ImageFont.truetype(FONTB, 10)

def key_tile(lab, hold, cat):
    t = Image.new("RGBA", (KW + 2, KH + 2), (0, 0, 0, 0))
    td = ImageDraw.Draw(t)
    fill, tc = C[cat]
    if cat == "none":
        td.rounded_rectangle([1, 1, KW, KH], 8, outline="#e6e6e6", width=1, fill=fill)
        return t
    td.rounded_rectangle([1, 1, KW, KH], 8, fill=fill, outline="#9a9a9a", width=1)
    def center(txt, font, cy):
        b = td.textbbox((0, 0), txt, font=font)
        td.text((KW / 2 + 1 - (b[2] - b[0]) / 2 - b[0], cy - (b[3] - b[1]) / 2 - b[1]), txt, font=font, fill=tc)
    if hold:
        center(lab, fit(lab, td), KH / 2 - 6)
        center(hold, f_small, KH - 9)
    else:
        center(lab, fit(lab, td), KH / 2 + 1)
    return t

def place(tile, cx, cy, rot):
    if rot:
        tile = tile.rotate(rot, resample=Image.BICUBIC, expand=True)
    img.paste(tile, (int(cx - tile.width / 2), int(cy - tile.height / 2)), tile)

for i, (title, keys) in enumerate(LAYERS):
    assert len(keys) == 38, (title, len(keys))
    ox = MARGIN + (i % COLS) * (PW + MARGIN)
    oy = 80 + (i // COLS) * (PH + MARGIN)
    d.rounded_rectangle([ox, oy, ox + PW, oy + PH], 14, fill="#ffffff", outline="#d0d0d0", width=2)
    d.text((ox + 14, oy + 10), title, font=f_title, fill="#222")
    left_x0 = ox + 10 + KW / 2
    right_x0 = ox + PW - 10 - KW / 2      # x of col 11
    y0 = oy + 50 + KH / 2
    for idx, ((lab, hold, cat), (r, c)) in enumerate(zip(keys, POS)):
        tile = key_tile(lab, hold, cat)
        if r < 3:
            cx = left_x0 + c * U if c < 6 else right_x0 - (11 - c) * U
            cy = y0 + (r + STAG[c]) * (KH + G)
            place(tile, cx, cy, 0)
        else:
            t = idx - 32                     # 0..5
            if t < 3:
                dx, dy, rot = THUMB[t]
                place(tile, left_x0 + dx * U, y0 + dy * (KH + G), -rot)
            else:
                dx, dy, rot = THUMB[5 - t]
                place(tile, right_x0 - dx * U, y0 + dy * (KH + G), rot)

# Legend in the last free cell
i = len(LAYERS)
ox = MARGIN + (i % COLS) * (PW + MARGIN)
oy = 80 + (i // COLS) * (PH + MARGIN)
d.rounded_rectangle([ox, oy, ox + PW, oy + PH], 14, fill="#ffffff", outline="#d0d0d0", width=2)
d.text((ox + 14, oy + 10), "Legend", font=f_title, fill="#222")
items = [("alpha", "Letter (tap)"), ("mod", "Home-row mod: tap letter / hold mod"),
         ("thumb", "Thumb: tap / hold layer or mod"), ("sym", "Symbol (Lafayette AltGr)"),
         ("num", "Digit / numpad"), ("nav", "Navigation"), ("dead", "★ Lafayette dead key (accents)"),
         ("app", "Shortcut / app"), ("fn", "Function key"), ("sys", "Bluetooth / system"),
         ("trans", "▽ same as lower layer")]
for j, (cat, txt) in enumerate(items):
    x = ox + 20 + (j % 2) * (PW // 2)
    y = oy + 50 + (j // 2) * 32
    d.rounded_rectangle([x, y, x + 34, y + 24], 5, fill=C[cat][0], outline="#9a9a9a")
    d.text((x + 44, y + 4), txt, font=f_note, fill="#333")
notes = ["Accents: ★ then a letter (★ e → é, ★ a → à …). Needs the Qwerty-Lafayette OS layout.",
         "G⇧ = Gui+Shift.   Combos: Q+W = Esc   ·   A+S+D = toggle TVP 1"]
for j, n in enumerate(notes):
    d.text((ox + 20, oy + PH - 50 + j * 20), n, font=f_note, fill="#333")

img.save(OUT)
print(OUT, img.size)
