"""Generador del set de sprites de VELADOR (pixel art 16x16, vista cenital 3/4)."""
import json, os, random
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.dirname(os.path.abspath(__file__)) + "/sprites"
os.makedirs(OUT, exist_ok=True)

# ---------- Paleta "Duermevela" (24 colores) ----------
PAL = {
    "K": "#0b0b12", "N": "#050508", "D": "#1b1b2a", "G": "#3a3a52", "m": "#56566e",
    "g": "#6b6b85", "L": "#a9a9c0", "W": "#e6e3d8", "S": "#d9a886", "s": "#a8735a",
    "C": "#3f5a7a", "c": "#2a3d57", "B": "#5a3b2a", "b": "#3b2619", "Y": "#f2c46b",
    "O": "#c9773a", "R": "#b3202f", "r": "#4a0f18", "P": "#6a4c8c", "p": "#b59de0",
    "v": "#45325e", "T": "#4f7a6a", "t": "#2f4f45", "Q": "#c77d9a", "q": "#8e4f6b",
}
def hex2rgba(h, a=255):
    h = h.lstrip("#"); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)

def draw(rows, name, alpha=255, w=16):
    for i, r in enumerate(rows):
        assert len(r) == w, f"{name} fila {i}: {len(r)} -> '{r}'"
    im = Image.new("RGBA", (w, len(rows)), (0, 0, 0, 0))
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch != ".":
                im.putpixel((x, y), hex2rgba(PAL[ch], alpha))
    return im

# ---------- Plantillas humanoides ----------
# h pelo, F piel, f sombra piel, e ojo, A ropa, a sombra ropa, x pantalón
FRONT = ["................", ".....KKKKKK.....", "....KhhhhhhK....", "...KhhhhhhhhK...",
         "...KhFFFFFFhK...", "...KFeFFFFeFK...", "...KFFFFFFFFK...", "....KFFffFFK....",
         "...KKAAAAAAKK...", "..KAAAAAAAAAAK..", "..KAaAAAAAAaAK..", "..KFKAAAAAAKFK..",
         "...KKAAAAAAKK..."]
BACK = FRONT[:4] + ["...KhhhhhhhhK..."] * 3 + ["....KhhhhhhK...."] + FRONT[8:]
SIDE = ["................", "......KKKKK.....", ".....KhhhhhK....", "....KhhhhhhhK...",
        "....KhhhFFFFK...", "....KhhFFFeFK...", "....KhhFFFFFK...", ".....KhFFFfK....",
        "....KKAAAAKK....", "....KAAAAAAK....", "....KAaAAAAK....", "....KAaFFAAK....",
        "....KKAAAAKK...."]
LEGS_F = {"idle":  ["....KxxKKxxK....", "....KxxKKxxK....", "....KKKKKKKK...."],
          "walk1": ["....KxxKKxxK....", "....KxxKKKKK....", "....KKKK........"],
          "walk2": ["....KxxKKxxK....", "....KKKKKxxK....", "........KKKK...."]}
LEGS_S = {"idle":  [".....KxxxxK.....", ".....KxKKxK.....", ".....KK..KK....."],
          "walk1": [".....KxxxxK.....", "....KxK..KxK....", "....KK....KK...."],
          "walk2": [".....KxxxxK.....", "......KxxK......", "......KKKK......"]}

def recolor(rows, m):
    return ["".join(m.get(c, c) for c in r) for r in rows]

def humanoid(direction, frame, m, blink=False):
    if direction in ("down", "up"):
        rows = (FRONT if direction == "down" else BACK) + LEGS_F[frame]
    else:
        rows = SIDE + LEGS_S[frame]
    if blink:
        rows = [r.replace("e", "F") for r in rows]
    return recolor(rows, m)

CHARS = {
    "velador": {"h": "b", "F": "S", "f": "s", "e": "K", "A": "C", "a": "c", "x": "D"},
    "anciano": {"h": "L", "F": "S", "f": "s", "e": "K", "A": "B", "a": "b", "x": "G"},
    "nina":    {"h": "O", "F": "S", "f": "s", "e": "K", "A": "Q", "a": "q", "x": "Q"},
    "madre":   {"h": "b", "F": "S", "f": "s", "e": "K", "A": "T", "a": "t", "x": "G"},
    "eco":     {"h": "p", "F": "p", "f": "P", "e": "W", "A": "P", "a": "v", "x": "P", "K": "v"},
}

def child(rows):  # la niña es más bajita
    body = [r for i, r in enumerate(rows) if i not in (9, 12)]
    return ["." * 16] * 2 + body

# ---------- Criatura: EL HUÉSPED (16x32) ----------
E = "." * 16
ACECHA = [E, E, "......NNNN......", ".....NNNNNN.....", ".....NWNNWN.....", ".....NNNNNN.....",
          "......NNNN......", ".......NN.......", ".....NNNNNN.....", "....NNNNNNNN....",
          "...NNNNNNNNNN...", "...NN.NNNN.NN...", "..NN..NNNN..NN..", "..N...NNNN...N..",
          "..N...NNNN...N..", ".NN...NNNN...NN.", ".N....NNNN....N.", ".N....NNNN....N.",
          ".N....NNNN....N.", ".N....NNNN....N.", "NN....NNNN....NN", "N.N...NNNN...N.N",
          "N.N...NNNN...N.N", "......NNNN......", "......NNNN......", "......NN.NN.....",
          "......NN..NN....", ".....NN...NN....", ".....NN....NN...", ".....NN....NN...",
          "....NNN....NNN..", E]
CAZA = [E, E, "......NNNN......", ".....NNNNNN.....", ".....NRNNRN.....", ".....NNNNNN.....",
        "N.N..NRWWRN..N.N", "N.N...NRRN...N.N", "N....NNNNNN....N", "NN..NNNNNNNN..NN",
        ".NNNNNNNNNNNNNN.", "..NN..NNNN..NN.."] + ["......NNNN......"] * 11 + ACECHA[23:]
LATENTE_A = [E] * 27 + ["....NNNNNNNN....", "..NNNNWNNWNNNN..", ".NNNNNNNNNNNNNN.",
                        "..NNNNNNNNNNNN..", "....NNNNNNNN...."]
LATENTE_B = [E] * 27 + ["...NNNNNNNNNN...", "..NNNNNWNNWNNN..", "NNNNNNNNNNNNNNNN",
                        "..NNNNNNNNNNNN..", ".....NNNNNN....."]

def jitter(rows, start=2, end=8, dx=1):
    out = list(rows)
    for i in range(start, end):
        r = out[i]; out[i] = ("." * dx + r)[:16] if dx > 0 else (r + ".")[1:]
    return out

# ---------- Objetos ----------
ITEMS = {
 "foto": [E, E, "...KKKKKKKKKK...", "...KWWWWWWWWK...", "...KWLLLLLLWK...", "...KWLgLLgLWK...",
          "...KWLgLLgLWK...", "...KWLGGGGLWK...", "...KWLLLLLLWK...", "...KWWWWWWWWK...",
          "...KWWWWWWWWK...", "...KKKKKKKKKK...", E, E, E, E],
 "cajita_musica": [E, E, E, "....KKKKKKKK....", "...KOOOOOOOOK...", "...KObbbbbbOK...",
          "...KKKKKKKKKK...", "...KBBBBBBBBK...", "...KBYBBBBYBK...", "...KBBBBBBBBK...",
          "...KbbbbbbbbK...", "...KKKKKKKKKK...", "..........KK....", E, E, E],
 "carta": [E, E, E, "..KKKKKKKKKKKK..", "..KWKWWWWWWKWK..", "..KWWKWWWWKWWK..",
          "..KWWWKWWKWWWK..", "..KWWWWKKWWWWK..", "..KWWWWRRWWWWK..", "..KWWWWWWWWWWK..",
          "..KLLLLLLLLLLK..", "..KKKKKKKKKKKK..", E, E, E, E],
 "vela_a": [E, E, ".......Y........", "......YYY.......", "......YWY.......", ".......O........",
          ".......K........", "......KWWK......", "......KWLK......", "......KWLK......",
          "......KWLK......", "......KWLK......", "....KKKKKKKK....", "....KggggggK....",
          "....KKKKKKKK....", E],
 "vela_b": [E, E, "........Y.......", ".......YYY......", "......YWY.......", ".......O........",
          ".......K........", "......KWWK......", "......KWLK......", "......KWLK......",
          "......KWLK......", "......KWLK......", "....KKKKKKKK....", "....KggggggK....",
          "....KKKKKKKK....", E],
 "llave": [E, E, E, E, E, "...KKKK.........", "..KYYYYK........", "..KYKKYKKKKKKK..",
          "..KYKKYYYYYYYYK.", "..KYYYYKKKYKYK..", "...KKKK...K.K...", E, E, E, E, E],
 "caja_cerrada": [E, E, E, "...KKKKKKKKKK...", "..KGGGGGGGGGGK..", "..KgggggggggGK..",
          "..KKKKKKKKKKKK..", "..KGGGGPPGGGGK..", "..KGGGPKKPGGGK..", "..KGGGGPPGGGGK..",
          "..KGGGGGGGGGGK..", "..KDDDDDDDDDDK..", "..KKKKKKKKKKKK..", E, E, E],
 "caja_abierta": ["...KKKKKKKKKK...", "..KGGGGGGGGGGK..", "..KKKKKKKKKKKK..", "....p..p..p.....",
          "...p.pp..pp.p...", "..KKKKKKKKKKKK..", "..KppppppppppK..", "..KGGGGGGGGGGK..",
          "..KGGGGGGGGGGK..", "..KGGGGGGGGGGK..", "..KGGGGGGGGGGK..", "..KDDDDDDDDDDK..",
          "..KKKKKKKKKKKK..", E, E, E],
}
UI = {
 "ojo_don": [E, E, E, E, E, ".....KKKKKK.....", "...KKppppppKK...", "..KppWWPPWWppK..",
          ".KpWWWPKKPWWWpK.", "..KppWWPPWWppK..", "...KKppppppKK...", ".....KKKKKK.....",
          E, E, E, E],
 "luna_cordura": [E, E, "......KKKK......", "....KKWWWK......", "...KWWWKK.......",
          "..KWWWK.........", "..KWWK..........", ".KWWLK..........", ".KWWLK..........",
          ".KWWLK..........", "..KWWLK.........", "..KWWWLK........", "...KWWWLKK......",
          "....KKWWWLKK....", "......KKKK......", E],
}

# ---------- Tiles procedurales ----------
def tile(fn):
    im = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            c = fn(x, y)
            im.putpixel((x, y), hex2rgba(PAL[c]) if c != "." else (0, 0, 0, 0))
    return im

def madera(x, y):
    row = y // 4
    if y % 4 == 0: return "b"
    if x == (row * 5 + 3) % 16: return "b"
    return "b" if (x * 7 + row * 5 + y) % 13 == 0 else "B"
def baldosa(x, y):
    if x % 8 == 0 or y % 8 == 0: return "D"
    return "g" if (x // 8 + y // 8) % 2 == 0 else "m"
def pared(x, y):
    if y < 4: return "D" if y else "K"
    if y == 15: return "K"
    if (y - 4) % 4 == 3: return "D"
    off = 0 if ((y - 4) // 4) % 2 == 0 else 4
    return "D" if (x + off) % 8 == 0 else ("G" if (x + y) % 9 else "m")
def puerta_cerrada(x, y):
    if x in (0, 15) or y == 0: return "K"
    if x in (1, 14) or y == 1: return "b"
    if (x, y) in ((11, 8), (11, 9)): return "Y"
    return "b" if x == 7 else "B"
def puerta_abierta(x, y):
    if x in (0, 15) or y == 0: return "K"
    if x in (1, 14) or y == 1: return "b"
    return "N"
def ventana(x, y):
    if not (3 <= x <= 12 and 5 <= y <= 12): return pared(x, y)
    if x in (3, 12) or y in (5, 12) or x == 8 or y == 8: return "b"
    if (x, y) in ((5, 6), (6, 6), (5, 7)): return "p"
    return "v"
def cama(x, y, ocupada=False):
    if x in (0, 15) or y == 15: return "K"
    if y <= 2: return "K" if y == 0 else "b"
    if ocupada and 3 <= y <= 6 and 5 <= x <= 10:
        if y == 3 or x in (5, 10): return "K"
        return "b" if y == 4 else ("S" if x not in (6, 9) or y != 6 else "s")
    if y <= 5: return "W" if 2 <= x <= 13 else "L"
    if y == 6: return "c"
    if ocupada and 7 <= y <= 12 and 5 <= x <= 10: return "C" if (x + y) % 4 else "L"
    return "c" if x in (1, 14) or (x + y) % 7 == 0 else "C"
def vacio(x, y):
    rnd = random.Random(x * 31 + y * 17 + 7).random()
    return "P" if rnd > 0.97 else ("v" if rnd > 0.88 else ("D" if rnd > 0.7 else "N"))
def umbral(x, y):
    if y in (7, 8): return "Y"
    if y in (6, 9): return "O"
    return baldosa(x, y)
CRACK = {(3, 2), (4, 3), (5, 4), (5, 5), (6, 6), (7, 7), (8, 7), (9, 8), (10, 9), (10, 10), (11, 11), (12, 12), (8, 8), (7, 9), (6, 10)}
def grieta(x, y):
    if (x, y) in CRACK: return "N"
    if any((x + dx, y + dy) in CRACK for dx in (-1, 1) for dy in (0,)): return "P" if (x + y) % 3 == 0 else baldosa(x, y)
    return baldosa(x, y)

TILES = {"suelo_madera": madera, "suelo_baldosa": baldosa, "pared": pared, "ventana": ventana,
         "puerta_cerrada": puerta_cerrada, "puerta_abierta": puerta_abierta,
         "cama": lambda x, y: cama(x, y), "cama_ocupada": lambda x, y: cama(x, y, True),
         "vacio_transito": vacio, "umbral_luz": umbral, "grieta": grieta}

# ---------- Ensamblado de spritesheets ----------
meta = {"tile_size": 16, "sheets": {}}

def save_sheet(name, frames, cols, fw=16, fh=16):
    rows = (len(frames) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * fw, rows * fh), (0, 0, 0, 0))
    info = {}
    for i, (fname, im) in enumerate(frames):
        x, y = (i % cols) * fw, (i // cols) * fh
        sheet.paste(im, (x, y)); info[fname] = [x, y, fw, fh]
    sheet.save(f"{OUT}/{name}.png")
    meta["sheets"][name] = {"file": f"{name}.png", "frames": info}
    return sheet

# Velador: 4 direcciones x 3 frames (izquierda = espejo de derecha)
vel = []
for d in ("down", "up", "right", "left"):
    for fr in ("idle", "walk1", "walk2"):
        src = "right" if d == "left" else d
        im = draw(humanoid(src, fr, CHARS["velador"]), f"velador {d} {fr}")
        if d == "left": im = im.transpose(Image.FLIP_LEFT_RIGHT)
        vel.append((f"velador_{d}_{fr}", im))
save_sheet("velador", vel, 3)

npcs = []
for n in ("anciano", "nina", "madre"):
    for blink in (False, True):
        rows = humanoid("down", "idle", CHARS[n], blink)
        if n == "nina": rows = child(rows)
        npcs.append((f"{n}_{'parpadeo' if blink else 'idle'}", draw(rows, n)))
for fr in ("idle", "walk1"):
    npcs.append((f"eco_{fr}", draw(humanoid("down", fr, CHARS["eco"]), "eco", alpha=170)))
save_sheet("soñadores", npcs, 2)

cri = [("huesped_latente_a", draw(LATENTE_A, "lat a")), ("huesped_latente_b", draw(LATENTE_B, "lat b")),
       ("huesped_acecha_a", draw(ACECHA, "acecha")), ("huesped_acecha_b", draw(jitter(ACECHA), "acecha b")),
       ("huesped_caza_a", draw(CAZA, "caza")), ("huesped_caza_b", draw(jitter(CAZA, 2, 12, -1), "caza b"))]
save_sheet("huesped", cri, 2, 16, 32)

save_sheet("tiles", [(k, tile(f)) for k, f in TILES.items()], 4)
save_sheet("objetos", [(k, draw(v, k)) for k, v in ITEMS.items()], 4)
save_sheet("ui", [(k, draw(v, k)) for k, v in UI.items()], 2)
meta["animaciones"] = {
    "velador_caminar": ["idle", "walk1", "idle", "walk2"],
    "vela": ["vela_a", "vela_b"], "huesped_latente": ["huesped_latente_a", "huesped_latente_b"],
    "huesped_acecha": ["huesped_acecha_a", "huesped_acecha_b"], "huesped_caza": ["huesped_caza_a", "huesped_caza_b"]}
meta["paleta"] = PAL
with open(f"{OUT}/sprites.json", "w", encoding="utf-8") as f:
    json.dump(meta, f, indent=2, ensure_ascii=False)

# ---------- Vista previa ampliada ----------
S = 5
def cargar_fuente(nombres, tam):
    rutas = ["/usr/share/fonts/truetype/dejavu/", "/usr/share/fonts/dejavu-sans-fonts/",
             "/usr/share/fonts/dejavu/", "C:/Windows/Fonts/", "/Library/Fonts/"]
    for r in rutas:
        for n in nombres:
            try: return ImageFont.truetype(r + n, tam)
            except OSError: pass
    return ImageFont.load_default(size=tam)
font = cargar_fuente(["DejaVuSans-Bold.ttf", "arialbd.ttf"], 18)
small = cargar_fuente(["DejaVuSans.ttf", "arial.ttf"], 12)
W_, H_ = 1180, 1080
pv = Image.new("RGBA", (W_, H_), hex2rgba("#101019"))
dr = ImageDraw.Draw(pv)
def big(im): return im.resize((im.width * S, im.height * S), Image.NEAREST)
def section(title, x, y): dr.text((x, y), title, font=font, fill=hex2rgba(PAL["p"]))
def put(im, x, y, label=None):
    pv.alpha_composite(big(im), (x, y))
    if label: dr.text((x, y + im.height * S + 4), label, font=small, fill=hex2rgba(PAL["L"]))

section("VELADOR  (abajo / arriba / derecha / izquierda · idle, paso 1, paso 2)", 30, 20)
for i, (n, im) in enumerate(vel):
    d, c = divmod(i, 3)
    put(im, 30 + (d * 3 + c) * 90, 55)
for d, lab in enumerate(("abajo", "arriba", "derecha", "izquierda")):
    dr.text((30 + d * 270, 145), lab, font=small, fill=hex2rgba(PAL["L"]))

section("SOÑADORES Y ECO", 30, 185)
for i, (n, im) in enumerate(npcs):
    put(im, 30 + i * 125, 220, n.replace("_", " "))

section("EL HUÉSPED  (latente · acecha · caza)", 30, 345)
floor = Image.new("RGBA", (6 * 24, 34))
for tx in range(0, 6 * 24, 16):
    for ty in range(0, 34, 16):
        floor.paste(tile(baldosa), (tx, ty))
lamp = Image.new("RGBA", floor.size, (0, 0, 0, 0))
ImageDraw.Draw(lamp).ellipse((-20, -10, 6 * 24 + 20, 50), fill=(242, 196, 107, 40))
floor.alpha_composite(lamp)
for i, (n, im) in enumerate(cri):
    floor.alpha_composite(im, (4 + i * 24, 1))
pv.alpha_composite(big(floor), (30, 380))
for i, (n, _) in enumerate(cri):
    dr.text((30 + (4 + i * 24) * S - 10, 380 + 34 * S + 4), n.replace("huesped_", ""), font=small, fill=hex2rgba(PAL["L"]))

section("TILES", 30, 605)
for i, (n, f) in enumerate(TILES.items()):
    put(tile(f), 30 + i * 100, 640, n.replace("_", " "))

section("OBJETOS", 30, 770)
for i, (n, v) in enumerate(ITEMS.items()):
    put(draw(v, n), 30 + i * 100, 805, n.replace("_", " "))
section("INTERFAZ", 30, 915)
for i, (n, v) in enumerate(UI.items()):
    put(draw(v, n), 30 + i * 120, 945, n.replace("_", " "))

# muestra de paleta
for i, (k, h) in enumerate(PAL.items()):
    dr.rectangle((870 + (i % 8) * 36, 400 + (i // 8) * 36, 870 + (i % 8) * 36 + 30, 430 + (i // 8) * 36), fill=hex2rgba(h))
dr.text((870, 365), "PALETA DUERMEVELA", font=font, fill=hex2rgba(PAL["p"]))
pv.convert("RGB").save(f"{OUT}/preview.png")
print("ok")