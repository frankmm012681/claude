from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import sys

OUT = sys.argv[1]
import os
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
LOGO_FULL = os.path.join(ASSETS, "logo-completo.png")
LOGO_TEXT = os.path.join(ASSETS, "logo-texto.png")
LOGO_ICON = os.path.join(ASSETS, "logo-personajes.png")

# ---------- fonts ----------
L = "/usr/share/fonts/truetype/liberation/"
D = "/usr/share/fonts/truetype/dejavu/"
MS = "/usr/share/fonts/truetype/montserrat/"
JB = "/usr/share/fonts/truetype/jetbrains-mono/"
pdfmetrics.registerFont(TTFont("Sans", MS + "Montserrat-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Sans-B", MS + "Montserrat-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans-X", MS + "Montserrat-ExtraBold.ttf"))
pdfmetrics.registerFont(TTFont("Sans-I", MS + "Montserrat-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Sym", D + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Sym-B", D + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Mono", JB + "JetBrainsMono-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Mono-B", JB + "JetBrainsMono-Bold.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-B")

# ---------- brand ----------
GOLD = HexColor("#E8AF3A")
GOLD_D = HexColor("#C98F1E")
RED = HexColor("#D62828")
BLUE = HexColor("#3E7CB1")
INK = HexColor("#17161A")
INK2 = HexColor("#211F26")
INK3 = HexColor("#2A2830")
CREAM = HexColor("#F7F3E9")
BROWN = HexColor("#241D07")
PAPER = HexColor("#FBF9F4")  # fondo crema para documentos de trabajo (manual de marca)
# tonos de texto derivados para cumplir WCAG 2.2 AA (4.5:1) sobre fondo crema
GOLD_TXT = HexColor("#8A6212")
BLUE_TXT = HexColor("#2F6390")
# derived tints (mixes of the brand colors with cream/white)
CARD = HexColor("#FFFDF8")
LINE = HexColor("#E4DCC8")
MUTED = HexColor("#5F5A52")
GOLD_T = HexColor("#F7E6C0")
BLUE_T = HexColor("#DDE8F2")
RED_T = HexColor("#F7DADA")
CREAM_D = HexColor("#BDB6A6")

W, H = A4
M = 48  # margin
CW = W - 2 * M

c = canvas.Canvas(OUT, pagesize=A4)
c.setTitle("Cómo instalar una Skill en Claude — Guía 2026")
c.setAuthor("")
c.setSubject("Guía paso a paso para instalar skills en Claude (claude.ai y Claude Code), actualizada a octubre de 2026")

# ---------- text helpers ----------
def style(size=10.5, color=INK, font="Sans", lead=None, align=TA_LEFT):
    return ParagraphStyle("s", fontName=font, fontSize=size, leading=lead or size * 1.42,
                          textColor=color, alignment=align)

BODY = style()
SMALL = style(9, MUTED)

def para(text, x, ytop, w, st=BODY):
    p = Paragraph(text, st)
    _, h = p.wrap(w, 1000)
    p.drawOn(c, x, ytop - h)
    return ytop - h

def txt(s, x, y, size=10, font="Sans", color=INK, anchor="l"):
    # el mostaza profundo y el azul no alcanzan 4.5:1 como texto: se usan sus tonos oscuros
    color = {id(GOLD_D): GOLD_TXT, id(BLUE): BLUE_TXT}.get(id(color), color)
    c.setFont(font, size)
    c.setFillColor(color)
    if anchor == "l":
        c.drawString(x, y, s)
    elif anchor == "c":
        c.drawCentredString(x, y, s)
    else:
        c.drawRightString(x, y, s)

def rrect(x, y, w, h, r=8, fill=None, stroke=None, lw=1, dash=None):
    c.saveState()
    if fill is not None:
        c.setFillColor(fill)
    if stroke is not None:
        c.setStrokeColor(stroke)
        c.setLineWidth(lw)
    if dash:
        c.setDash(*dash)
    c.roundRect(x, y, w, h, r, stroke=1 if stroke is not None else 0, fill=1 if fill is not None else 0)
    c.restoreState()

def badge(x, y, n, r=11, fill=GOLD, color=BROWN):
    c.setFillColor(fill)
    c.circle(x, y, r, stroke=0, fill=1)
    txt(str(n), x, y - r * 0.36, r * 1.05, "Sans-B", color, "c")

def arrow(x1, y1, x2, y2, color=GOLD_TXT, lw=1.6, head=6):
    import math
    c.saveState()
    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setLineWidth(lw)
    ang = math.atan2(y2 - y1, x2 - x1)
    ex, ey = x2 - head * 0.8 * math.cos(ang), y2 - head * 0.8 * math.sin(ang)
    c.line(x1, y1, ex, ey)
    p = c.beginPath()
    p.moveTo(x2, y2)
    p.lineTo(x2 - head * math.cos(ang - 0.45), y2 - head * math.sin(ang - 0.45))
    p.lineTo(x2 - head * math.cos(ang + 0.45), y2 - head * math.sin(ang + 0.45))
    p.close()
    c.drawPath(p, stroke=0, fill=1)
    c.restoreState()

def toggle(x, y, on=True, scale=1.0):
    w, h = 26 * scale, 14 * scale
    rrect(x, y, w, h, h / 2, fill=GOLD if on else CREAM_D)
    c.setFillColor(CARD)
    cx = x + w - h / 2 if on else x + h / 2
    c.circle(cx, y + h / 2, h / 2 - 2 * scale, stroke=0, fill=1)

def logo_slot(x, y, w, h, dark=True):
    col = GOLD if dark else GOLD_D
    rrect(x, y, w, h, 6, stroke=col, lw=1, dash=(3, 2))
    txt("TU LOGO", x + w / 2, y + h / 2 - 3.5, 8.5, "Sans-B", col, "c")

def code_block(lines, x, ytop, w, size=9, pad=12, title=None):
    lh = size * 1.55
    h = pad * 2 + lh * len(lines) + (18 if title else 0)
    rrect(x, ytop - h, w, h, 8, fill=INK2)
    yy = ytop - pad - size
    if title:
        for i, col in enumerate([RED, GOLD, BLUE]):
            c.setFillColor(col)
            c.circle(x + pad + 3 + i * 11, ytop - pad - 2, 3, stroke=0, fill=1)
        txt(title, x + pad + 40, ytop - pad - 5, 8, "Mono", CREAM_D)
        yy -= 18
    for ln in lines:
        segs = ln if isinstance(ln, list) else [(ln, CREAM)]
        xx = x + pad
        for s, col in segs:
            txt(s, xx, yy, size, "Mono", col)
            xx += pdfmetrics.stringWidth(s, "Mono", size)
        yy -= lh
    return ytop - h

def callout(x, ytop, w, title, body, kind="tip"):
    fill, accent, icon = {"tip": (GOLD_T, GOLD_TXT, "★"), "info": (BLUE_T, BLUE_TXT, "i"),
                          "warn": (RED_T, RED, "!")}[kind]
    p = Paragraph(f"<b>{title}</b><br/>{body}", style(9.5, INK, lead=13.5))
    _, ph = p.wrap(w - 52, 1000)
    h = ph + 22
    rrect(x, ytop - h, w, h, 8, fill=fill)
    c.setFillColor(accent)
    c.rect(x, ytop - h, 4, h, stroke=0, fill=1)
    c.circle(x + 24, ytop - 20, 9, stroke=0, fill=1)
    txt(icon, x + 24, ytop - 23.5, 10, "Sym-B", CARD, "c")
    p.drawOn(c, x + 42, ytop - 11 - ph)
    return ytop - h

def page_bg():
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)

def header(num, title, kicker):
    page_bg()
    c.setFillColor(INK)
    c.rect(0, H - 78, W, 78, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(0, H - 81, W, 3, stroke=0, fill=1)
    txt(num, M, H - 50, 26, "Sans-B", GOLD)
    nw = pdfmetrics.stringWidth(num, "Sans-B", 26)
    txt(kicker.upper(), M + nw + 14, H - 34, 7.5, "Sans-B", GOLD)
    txt(title, M + nw + 14, H - 52, 16, "Sans-B", CREAM)
    lh = 24
    lw = lh * 1278 / 282
    c.drawImage(LOGO_TEXT, W - M - lw, H - 39 - lh / 2, lw, lh, mask="auto")

def footer(n):
    # manual de marca: logo pequeño + nombre de marca + numeración
    c.setStrokeColor(LINE)
    c.setLineWidth(0.8)
    c.line(M, 44, W - M, 44)
    ih = 20
    iw = ih * 1258 / 1327
    c.drawImage(LOGO_ICON, M, 17, iw, ih, mask="auto")
    txt("El Gigante Despierto", M + iw + 7, 28, 8, "Sans-B", INK)
    txt("Cómo instalar una Skill en Claude · octubre 2026", M + iw + 7, 18.5, 7, "Sans", MUTED)
    if n is not None:
        txt(str(n), W - M, 24, 10, "Sans-B", GOLD_TXT, "r")

def h2(s, y, color=INK):
    c.setFillColor(GOLD)
    c.rect(M, y - 2, 3, 14, stroke=0, fill=1)
    txt(s, M + 10, y, 13, "Sans-B", color)
    return y - 4

# =====================================================================
# PAGE 1 — COVER
# =====================================================================
# Portada según el manual de marca: logo centrado, eyebrow rojo, título extrabold, línea mostaza
page_bg()
lgw = 176
lgh = lgw * 1632 / 1278
c.drawImage(LOGO_FULL, (W - lgw) / 2, H - 52 - lgh, lgw, lgh, mask="auto")
ty = H - 52 - lgh - 40
txt("GUÍA PASO A PASO  ·  EDICIÓN OCTUBRE 2026", W / 2, ty, 9.5, "Sans-B", RED, "c")
txt("Cómo instalar una Skill", W / 2, ty - 46, 34, "Sans-X", INK, "c")
txt("en Claude", W / 2, ty - 86, 34, "Sans-X", INK, "c")
c.setFillColor(GOLD)
c.rect(W / 2 - 40, ty - 108, 80, 4, stroke=0, fill=1)
para("Activa, sube, comparte y usa skills en <b>claude.ai</b> (web y escritorio) "
     "y en <b>Claude Code</b>, con diagramas de cada paso.",
     W / 2 - 200, ty - 124, 400, style(12, MUTED, lead=18, align=TA_CENTER))

# ilustración: el paquete de la skill entra a Claude
bx, by = M + 2, 118
rrect(bx, by, 150, 120, 12, fill=INK2, stroke=INK3)
c.setFillColor(GOLD)
c.rect(bx + 18, by + 82, 30, 22, stroke=0, fill=1)
c.rect(bx + 18, by + 104, 14, 5, stroke=0, fill=1)
txt("mi-skill.zip", bx + 18, by + 60, 11, "Mono-B", CREAM)
txt("SKILL.md", bx + 18, by + 40, 8.5, "Mono", CREAM_D)
txt("scripts/  resources/", bx + 18, by + 26, 8.5, "Mono", CREAM_D)
arrow(bx + 162, by + 60, bx + 232, by + 60, GOLD_TXT, 2.2, 9)
wx = bx + 244
rrect(wx, by - 10, 251, 140, 12, fill=INK2, stroke=INK3)
for i, col in enumerate([RED, GOLD, BLUE]):
    c.setFillColor(col)
    c.circle(wx + 16 + i * 12, by + 116, 3.5, stroke=0, fill=1)
txt("Customize  ›  Skills", wx + 60, by + 112, 8.5, "Sans-B", CREAM_D)
for i, (nm, on) in enumerate([("mi-skill", True), ("pdf", True), ("brand-guidelines", False)]):
    yy = by + 80 - i * 30
    rrect(wx + 14, yy - 8, 223, 24, 6, fill=INK3)
    txt(nm, wx + 26, yy, 9.5, "Mono", CREAM if on else CREAM_D)
    toggle(wx + 198, yy - 3, on, 1.0)
c.setStrokeColor(GOLD)
c.setLineWidth(1.5)
c.roundRect(wx + 11, by + 69, 229, 30, 7, stroke=1, fill=0)

footer(None)
txt("Basado en la documentación oficial de Anthropic (support.claude.com y code.claude.com), consultada el 1 de octubre de 2026.",
    W / 2, 64, 7.5, "Sans", MUTED, "c")
c.showPage()

# =====================================================================
# PAGE 2 — ¿QUÉ ES UNA SKILL?
# =====================================================================
pg = 2
header("01", "¿Qué es una Skill?", "Conceptos básicos")
y = H - 112
y = para("Una <b>skill</b> (habilidad) es una carpeta con instrucciones, scripts y recursos que Claude "
         "carga <b>solo cuando la necesita</b>. Le enseña a hacer una tarea de forma repetible: aplicar "
         "tu manual de marca, generar reportes con tu formato, seguir el proceso de tu equipo, etc.",
         M, y, CW, style(11, INK, lead=16.5))
y -= 22
y = h2("Anatomía de una skill", y)
y -= 14

# folder tree diagram (left) + explanation cards (right)
tx, ty = M, y
rrect(tx, ty - 190, 230, 190, 10, fill=INK2)
rows = [
    (0, "mi-skill/", GOLD, "Mono-B"),
    (1, "SKILL.md", CREAM, "Mono-B"),
    (1, "scripts/", BLUE_T, "Mono"),
    (2, "generar.py", CREAM_D, "Mono"),
    (1, "resources/", BLUE_T, "Mono"),
    (2, "logo.png", CREAM_D, "Mono"),
    (2, "plantilla.docx", CREAM_D, "Mono"),
    (1, "REFERENCE.md", CREAM_D, "Mono"),
]
yy = ty - 28
for lvl, name, col, f in rows:
    x0 = tx + 20 + lvl * 20
    if lvl:
        c.setStrokeColor(INK3 if lvl else GOLD)
        c.setStrokeColor(HexColor("#4A4652"))
        c.setLineWidth(0.8)
        c.line(x0 - 12, yy + 3, x0 - 4, yy + 3)
        c.line(x0 - 12, yy + 3, x0 - 12, yy + 17)
    txt(name, x0, yy, 9.5, f, col)
    yy -= 20.5
# tags
txt("obligatorio", tx + 130, ty - 48.5, 7.5, "Sans-B", GOLD)
txt("opcional", tx + 130, ty - 69, 7.5, "Sans", CREAM_D)
txt("opcional", tx + 130, ty - 110, 7.5, "Sans", CREAM_D)

cx = M + 248
cw = CW - 248
cards = [
    (GOLD_D, "SKILL.md", "El corazón de la skill. Lleva un encabezado YAML con <b>name</b> y <b>description</b>, y debajo las instrucciones en Markdown."),
    (BLUE, "scripts/", "Código (Python, JavaScript/Node) que Claude puede ejecutar. Requiere tener activada la ejecución de código."),
    (BLUE, "resources/", "Archivos de apoyo: logos, fuentes, plantillas o ejemplos que la skill usa."),
]
yy = ty
for col, ttl, body in cards:
    p = Paragraph(body, style(9.2, INK, lead=12.8))
    _, ph = p.wrap(cw - 26, 500)
    h = ph + 30
    rrect(cx, yy - h, cw, h, 8, fill=CARD, stroke=LINE)
    c.setFillColor(col)
    c.rect(cx, yy - h, 4, h, stroke=0, fill=1)
    txt(ttl, cx + 14, yy - 16, 9.5, "Mono-B", col)
    p.drawOn(c, cx + 14, yy - 22 - ph)
    yy -= h + 8
y = min(ty - 190, yy) - 26

y = h2("¿Cómo decide Claude cuándo usarla?", y)
y -= 16
# progressive disclosure diagram: 3 stages
stages = [
    ("1", "Lee la descripción", "Al inicio solo ve el nombre y la descripción de cada skill activa (ocupa muy poco contexto)."),
    ("2", "Detecta que encaja", "Si tu petición coincide con la descripción, decide usarla."),
    ("3", "Carga todo", "Lee SKILL.md completo y, si hace falta, sus scripts y recursos."),
]
bw = (CW - 2 * 26) / 3
for i, (n, t, b) in enumerate(stages):
    bx = M + i * (bw + 26)
    rrect(bx, y - 104, bw, 104, 10, fill=CARD, stroke=LINE)
    # fill bar showing context used
    frac = [0.12, 0.35, 1.0][i]
    rrect(bx + 14, y - 94, bw - 28, 7, 3.5, fill=LINE)
    rrect(bx + 14, y - 94, (bw - 28) * frac, 7, 3.5, fill=GOLD if i < 2 else GOLD_D)
    badge(bx + 24, y - 22, n)
    txt(t, bx + 42, y - 26, 9.6, "Sans-B", INK)
    para(b, bx + 14, y - 40, bw - 28, style(8.6, MUTED, lead=11.5))
    if i < 2:
        arrow(bx + bw + 4, y - 52, bx + bw + 22, y - 52)
txt("contexto usado", M + 14, y - 116, 7, "Sans-I", MUTED)
y -= 140

y = h2("¿Quién puede usar skills?", y)
y -= 14
plans = ["Free", "Pro", "Max", "Team", "Enterprise"]
pw = (CW - 4 * 8) / 5
for i, p_ in enumerate(plans):
    px = M + i * (pw + 8)
    rrect(px, y - 46, pw, 46, 8, fill=INK if i < 3 else INK3)
    txt(p_, px + pw / 2, y - 20, 11, "Sans-B", CREAM, "c")
    txt("✓ disponible", px + pw / 2, y - 36, 8, "Sym", GOLD, "c")
y -= 56
para("Requisito común a todos los planes: tener activada la <b>ejecución de código</b> (lo vemos en el paso 02). "
     "En Team y Enterprise, además, un propietario de la organización debe habilitar las skills.",
     M, y, CW, SMALL)
footer(pg)
c.showPage()

# =====================================================================
# PAGE 3 — PASO 0: ACTIVAR EJECUCIÓN DE CÓDIGO
# =====================================================================
pg = 3
header("02", "Antes de empezar: activa los permisos", "Requisito previo")
y = H - 112
y = para("Las skills necesitan que Claude pueda ejecutar código y crear archivos. Según tu plan, "
         "esto lo activas tú o el propietario de tu organización.", M, y, CW, style(11, INK, lead=16.5))
y -= 20

def mock_window(x, ytop, w, h, crumb):
    rrect(x, ytop - h, w, h, 10, fill=CARD, stroke=LINE)
    c.saveState()
    p = c.beginPath()
    p.roundRect(x, ytop - 26, w, 26, 10)
    c.setFillColor(INK)
    c.rect(x, ytop - 26, w, 16, stroke=0, fill=1)
    c.roundRect(x, ytop - 26, w, 26, 10, stroke=0, fill=1)
    c.restoreState()
    for i, col in enumerate([RED, GOLD, BLUE]):
        c.setFillColor(col)
        c.circle(x + 14 + i * 11, ytop - 13, 3, stroke=0, fill=1)
    txt(crumb, x + 54, ytop - 16.5, 8, "Sans-B", CREAM_D)

# Left: individual plans
colw = (CW - 20) / 2
lx, rx = M, M + colw + 20
for (xx, tag, tagc, ttl) in [(lx, "FREE · PRO · MAX", GOLD_D, "Lo activas tú"),
                             (rx, "TEAM · ENTERPRISE", BLUE_TXT, "Lo activa el propietario")]:
    rrect(xx, y - 22, pdfmetrics.stringWidth(tag, "Sans-B", 8) + 18, 20, 10, fill=tagc)
    txt(tag, xx + 9, y - 15, 8, "Sans-B", CARD if tagc == BLUE_TXT else BROWN)
    txt(ttl, xx, y - 42, 13, "Sans-B", INK)
y -= 58

# left mock
mock_window(lx, y, colw, 200, "Settings  ›  Capabilities")
c.setFillColor(GOLD_T)
c.rect(lx + 1, y - 200 + 1, 70, 172, stroke=0, fill=1)
for i, s in enumerate(["General", "Account", "Privacy", "Capabilities", "Connectors"]):
    f = "Sans-B" if s == "Capabilities" else "Sans"
    txt(s, lx + 10, y - 48 - i * 19, 7.5, f, INK if s == "Capabilities" else MUTED)
items = [("Code execution and file creation", True, True), ("Memory", True, False), ("Web search", True, False)]
for i, (s, on, hl) in enumerate(items):
    yy = y - 58 - i * 40
    txt(s, lx + 80, yy, 6.4 if hl else 8, "Sans-B" if hl else "Sans", INK)
    toggle(lx + colw - 40, yy - 4, on, 0.95)
    if hl:
        c.setStrokeColor(GOLD_D)
        c.setLineWidth(1.6)
        c.roundRect(lx + 76, yy - 12, colw - 82, 28, 6, stroke=1, fill=0)
        badge(lx + colw - 6, yy + 16, 1, 9)
txt("Menú: Settings → Capabilities", lx + 82, y - 182, 7.5, "Sans-I", MUTED)

# right mock
mock_window(rx, y, colw, 200, "Organization settings  ›  Plugins & skills")
# tabs
for i, (s, act) in enumerate([("Directory", False), ("Policy", True), ("Requests", False)]):
    tx_ = rx + 14 + i * 64
    txt(s, tx_, y - 46, 8, "Sans-B" if act else "Sans", INK if act else MUTED)
    if act:
        c.setFillColor(BLUE)
        c.rect(tx_, y - 52, pdfmetrics.stringWidth(s, "Sans-B", 8), 2, stroke=0, fill=1)
        badge(tx_ + 44, y - 36, 1, 8, BLUE_TXT, CARD)
items = [("Cloud code execution and file creation", True), ("Skills", True)]
for i, (s, on) in enumerate(items):
    yy = y - 84 - i * 40
    txt(s, rx + 14, yy, 8, "Sans-B", INK)
    toggle(rx + colw - 40, yy - 4, on, 0.95)
    c.setStrokeColor(BLUE)
    c.setLineWidth(1.6)
    c.roundRect(rx + 8, yy - 12, colw - 16, 28, 6, stroke=1, fill=0)
    badge(rx + colw - 6, yy + 16, i + 2, 9, BLUE_TXT, CARD)
txt("Menú: Organization settings → Plugins & skills", rx + 14, y - 182, 7.5, "Sans-I", MUTED)
y -= 216

# step lists
def steps(x, ytop, w, items, col=GOLD, tcol=BROWN):
    yy = ytop
    for i, s in enumerate(items):
        badge(x + 10, yy - 8, i + 1, 9, col, tcol)
        yy = para(s, x + 26, yy, w - 26, style(9.5, INK, lead=13.5)) - 9
    return yy

ly = steps(lx, y, colw, [
    "Abre <b>Settings</b> (Configuración) desde tu foto o nombre.",
    "Entra en <b>Capabilities</b> (Capacidades).",
    "Activa <b>Code execution and file creation</b>.",
])
ry = steps(rx, y, colw, [
    "El propietario abre <b>Organization settings → Plugins &amp; skills</b>.",
    "En la pestaña <b>Policy</b>, activa <b>Cloud code execution and file creation</b>.",
    "En la misma pestaña, activa <b>Skills</b>.",
], BLUE_TXT, CARD)
y = min(ly, ry) - 14
y = callout(M, y, CW, "¿Tu Claude está en español?",
            "Los menús aparecen traducidos (por ejemplo, <i>Settings</i> = Configuración, <i>Capabilities</i> = Capacidades). "
            "En esta guía mostramos los nombres en inglés tal como aparecen en la documentación oficial, para que los reconozcas en cualquier idioma.",
            "info")
y -= 10
callout(M, y, CW, "Sin este paso, nada funciona",
        "Si la ejecución de código está desactivada, las skills no aparecen o Claude no puede usarlas. "
        "Es la causa más común de problemas.", "warn")
footer(pg)
c.showPage()

# =====================================================================
# PAGE 4 — RUTA A: SUBIR UNA SKILL EN CLAUDE.AI
# =====================================================================
pg = 4
header("03", "Instalar una skill en claude.ai", "Web y app de escritorio")
y = H - 112
y = para("Con los permisos activos, instalar una skill personalizada toma menos de un minuto. "
         "Solo necesitas el archivo <b>.zip</b> de la skill (en la página 5 te explicamos cómo prepararlo).",
         M, y, CW, style(11, INK, lead=16.5))
y -= 20
y = h2("El recorrido completo", y)
y -= 18

# flow: 5 steps horizontally
flow = [
    ("Customize", "› Skills"),
    ("Botón  +", ""),
    ("Create skill", ""),
    ("Upload a skill", ""),
    ("Elige el .zip", "y actívala"),
]
fw = (CW - 4 * 14) / 5
for i, (a, b) in enumerate(flow):
    fx = M + i * (fw + 14)
    last = i == 4
    rrect(fx, y - 66, fw, 66, 10, fill=GOLD if last else INK)
    badge(fx + fw / 2, y, i + 1, 11, GOLD_D if not last else INK, CARD if last else BROWN)
    txt(a, fx + fw / 2, y - 34, 9.5, "Sans-B", BROWN if last else CREAM, "c")
    if b:
        txt(b, fx + fw / 2, y - 48, 9, "Sans", BROWN if last else CREAM_D, "c")
    if i < 4:
        arrow(fx + fw + 2, y - 33, fx + fw + 12, y - 33, GOLD_D, 1.6, 5)
y -= 92

# big mock of skills page with dropdown
mx, mw, mh = M, CW, 250
mock_window(mx, y, mw, mh, "claude.ai  ›  Customize  ›  Skills")
c.setFillColor(GOLD_T)
c.rect(mx + 1, y - mh + 1, 110, mh - 28, stroke=0, fill=1)
for i, s in enumerate(["Skills", "…"]):
    txt(s, mx + 14, y - 48 - i * 20, 9, "Sans-B" if i == 0 else "Sans", INK if i == 0 else MUTED)
badge(mx + 60, y - 45, 1, 8)
txt("Skills", mx + 128, y - 50, 14, "Sans-B", INK)
# + button
bxp = mx + mw - 46
rrect(bxp, y - 60, 30, 24, 6, fill=INK)
txt("+", bxp + 15, y - 54, 15, "Sans-B", GOLD, "c")
badge(bxp - 10, y - 38, 2, 8)
# dropdown
dx, dw = mx + mw - 182, 168
rrect(dx, y - 150, dw, 84, 8, fill=CARD, stroke=LINE)
txt("+ Create skill", dx + 12, y - 84, 9, "Sans-B", INK)
badge(dx + dw - 14, y - 80, 3, 8)
c.setStrokeColor(LINE); c.line(dx + 8, y - 92, dx + dw - 8, y - 92)
for i, s in enumerate(["Upload a skill", "Otras opciones…"]):
    yy = y - 110 - i * 22
    if i == 0:
        rrect(dx + 6, yy - 7, dw - 12, 20, 5, fill=GOLD_T)
        badge(dx + dw - 14, yy + 3, 4, 8)
    txt(s, dx + 16, yy, 9, "Sans-B" if i == 0 else "Sans-I", INK if i == 0 else MUTED)
# list of skills
lst = [("mi-skill", "Mi skill recién subida", True, True), ("pdf", "Anthropic · Crear y procesar PDF", True, False),
       ("xlsx", "Anthropic · Hojas de cálculo", True, False)]
for i, (nm, desc, on, hl) in enumerate(lst):
    yy = y - 96 - i * 46
    rrect(mx + 126, yy - 18, 170, 38, 7, fill=CARD, stroke=GOLD_D if hl else LINE, lw=1.6 if hl else 0.8)
    txt(nm, mx + 138, yy + 4, 9.5, "Mono-B", INK)
    txt(desc, mx + 138, yy - 9, 7.5, "Sans", MUTED)
    toggle(mx + 260, yy - 6, on, 0.9)
    if hl:
        badge(mx + 296, yy + 18, 5, 8)
txt("Shared with you", mx + 128, y - mh + 30, 8, "Sans-B", MUTED)
txt("(skills que otras personas compartieron contigo)", mx + 200, y - mh + 30, 7.5, "Sans-I", MUTED)
y -= mh + 18

y = steps(M, y, CW, [
    "En la barra lateral, abre <b>Customize</b> y entra a <b>Skills</b>.",
    "Pulsa el botón <b>+</b> de la parte superior.",
    "Elige <b>+ Create skill</b>.",
    "Selecciona <b>Upload a skill</b> y elige el archivo <b>.zip</b> desde tu computadora.",
    "La skill aparece en tu lista. Verifica que el interruptor esté <b>activado</b>. Con el menú <font name='Sym'>⋯</font> puedes ver, descargar o eliminarla.",
])
y -= 4
callout(M, y, CW, "Las skills de Anthropic ya vienen incluidas",
        "Excel, Word, PowerPoint y PDF están disponibles sin instalar nada: Claude las usa automáticamente cuando hacen falta. "
        "Tus skills activas también funcionan en Claude para Excel, PowerPoint, Word y Outlook (escribe <b>/</b> para verlas).",
        "tip")
footer(pg)
c.showPage()

# =====================================================================
# PAGE 5 — PREPARAR EL ZIP
# =====================================================================
pg = 5
header("04", "Prepara tu archivo .zip", "Crear la skill")
y = H - 112
y = h2("El archivo SKILL.md", y)
y -= 12
y = para("Es un archivo de texto con dos partes: un encabezado YAML (entre las líneas <font name='Mono'>---</font>) "
         "y las instrucciones en Markdown.", M, y, CW, BODY)
y -= 10
G, C_, B_, D_ = GOLD, CREAM, BLUE_T, CREAM_D
cb_bottom = code_block([
    [("---", D_)],
    [("name", G), (": ", C_), ("manual-de-marca", C_)],
    [("description", G), (": ", C_), ("Aplica los colores, tipografías y tono de", C_)],
    [("  la marca a documentos y presentaciones.", C_)],
    [("---", D_)],
    "",
    [("# Manual de marca", B_)],
    "",
    [("## Cuándo usar esta skill", B_)],
    "Úsala al crear documentos o presentaciones.",
    "",
    [("## Colores", B_)],
    "- Principal: #E8AF3A",
    "- Acento: #D62828",
], M, y, CW * 0.62, 8.6, title="SKILL.md")

# right: rules
rx = M + CW * 0.62 + 16
rw = CW - CW * 0.62 - 16
rules = [
    ("name", "Máx. 64 caracteres. Usa minúsculas, números y guiones."),
    ("description", "Máx. 200 caracteres. Di <b>qué hace</b> y <b>cuándo usarla</b>: Claude la lee para decidir si la activa."),
    ("Instrucciones", "Claras y en pasos. Lo más importante, arriba."),
]
yy = y
for k, v in rules:
    p = Paragraph(v, style(8.8, INK, lead=12))
    _, ph = p.wrap(rw - 24, 300)
    h = ph + 30
    rrect(rx, yy - h, rw, h, 8, fill=CARD, stroke=LINE)
    txt(k, rx + 12, yy - 16, 9.5, "Mono-B", GOLD_D)
    p.drawOn(c, rx + 12, yy - 22 - ph)
    yy -= h + 8
y = min(cb_bottom, yy) - 24

y = h2("Estructura del .zip: correcta vs. incorrecta", y)
y -= 16
half = (CW - 20) / 2
for j, (ok, title, lines) in enumerate([
    (True, "CORRECTO", [("mi-skill.zip", 0, "Mono-B"), ("mi-skill/", 1, "Mono-B"), ("SKILL.md", 2, "Mono"), ("resources/", 2, "Mono")]),
    (False, "INCORRECTO", [("mi-skill.zip", 0, "Mono-B"), ("SKILL.md", 1, "Mono"), ("resources/", 1, "Mono")]),
]):
    bx = M + j * (half + 20)
    col = BLUE if ok else RED
    rrect(bx, y - 148, half, 148, 10, fill=CARD, stroke=col, lw=1.4)
    c.setFillColor(col)
    c.circle(bx + 22, y - 22, 10, stroke=0, fill=1)
    txt("✓" if ok else "✗", bx + 22, y - 26.5, 12, "Sym-B", CARD, "c")
    txt(title, bx + 40, y - 26, 10, "Sans-B", col)
    yy = y - 52
    for name, lvl, f in lines:
        x0 = bx + 20 + lvl * 18
        if lvl:
            c.setStrokeColor(CREAM_D); c.setLineWidth(0.8)
            c.line(x0 - 10, yy + 3, x0 - 3, yy + 3)
            c.line(x0 - 10, yy + 3, x0 - 10, yy + 15)
        txt(name, x0, yy, 9.5, f, INK)
        yy -= 18
    note = ("La carpeta de la skill va dentro del .zip, y lleva el mismo nombre que la skill." if ok
            else "Los archivos sueltos en la raíz del .zip: Claude no encuentra la skill.")
    para(note, bx + 16, y - 116, half - 32, style(8.3, MUTED, lead=11))
y -= 166

y = h2("Cómo comprimirlo", y)
y -= 14
os_cols = [
    ("Windows", "Clic derecho sobre la <b>carpeta</b> mi-skill → <b>Enviar a</b> → <b>Carpeta comprimida (zip)</b>."),
    ("Mac", "Clic derecho sobre la <b>carpeta</b> mi-skill → <b>Comprimir \"mi-skill\"</b>."),
    ("Terminal", "<font name='Mono'>zip -r mi-skill.zip mi-skill/</font>"),
]
ow = (CW - 2 * 10) / 3
for i, (t, b) in enumerate(os_cols):
    ox = M + i * (ow + 10)
    rrect(ox, y - 74, ow, 74, 8, fill=INK)
    txt(t, ox + 12, y - 18, 10, "Sans-B", GOLD)
    para(b, ox + 12, y - 26, ow - 24, style(8.6, CREAM, lead=12))
y -= 90
callout(M, y, CW, "Atajo: deja que Claude la cree por ti",
        "Pide en un chat: <i>\"Ayúdame a crear una skill para…\"</i>. Claude usa su skill <b>skill-creator</b> para redactar el SKILL.md "
        "y te entrega el .zip listo para subir.",
        "tip")
footer(pg)
c.showPage()

# =====================================================================
# PAGE 6 — CLAUDE CODE
# =====================================================================
pg = 6
header("05", "Instalar skills en Claude Code", "Terminal, IDE y escritorio")
y = H - 112
y = para("En Claude Code las skills son carpetas en tu disco. Hay tres maneras de tenerlas: copiarlas a una carpeta, "
         "instalarlas desde un marketplace de plugins o sincronizarlas desde tu cuenta de claude.ai.",
         M, y, CW, style(11, INK, lead=16.5))
y -= 20

# three route cards
routes = [
    ("A", "Copiar la carpeta", BLUE_TXT, "Pon la carpeta de la skill en la ruta adecuada. Claude Code la detecta al momento, sin reiniciar."),
    ("B", "Marketplace", GOLD_D, "Instala un plugin que trae una o varias skills con el comando /plugin."),
    ("C", "Sincronizar cuenta", RED, "Al iniciar sesión, tus skills de claude.ai se sincronizan (versión 2.1.273 o superior)."),
]
rw3 = (CW - 2 * 12) / 3
for i, (l, t, col, b) in enumerate(routes):
    rx_ = M + i * (rw3 + 12)
    rrect(rx_, y - 112, rw3, 112, 10, fill=CARD, stroke=LINE)
    c.setFillColor(col)
    c.rect(rx_, y - 4, rw3, 4, stroke=0, fill=1)
    c.roundRect(rx_ + 12, y - 38, 24, 24, 6, stroke=0, fill=1)
    txt(l, rx_ + 24, y - 31, 12, "Sans-B", BROWN if col == GOLD_D else CARD, "c")
    txt(t, rx_ + 44, y - 30, 10.5, "Sans-B", INK)
    para(b, rx_ + 12, y - 48, rw3 - 24, style(8.6, MUTED, lead=12))
y -= 144

y = h2("A · ¿Dónde guardar la carpeta?", y)
y -= 14
# diagram of scopes: nested rectangles
sx, sw, sh = M, CW, 118
rows = [
    ("Personal", "~/.claude/skills/<nombre>/SKILL.md", "Todos tus proyectos en esta computadora", GOLD),
    ("Proyecto", ".claude/skills/<nombre>/SKILL.md", "Solo este repositorio · súbela a git para compartirla", BLUE_TXT),
    ("Plugin", "<plugin>/skills/<nombre>/SKILL.md", "Donde el plugin esté activado", GOLD_D),
]
for i, (k, path, desc, col) in enumerate(rows):
    yy = y - i * 38
    rrect(sx, yy - 32, sw, 32, 7, fill=INK if i % 2 == 0 else INK2)
    c.setFillColor(col)
    c.roundRect(sx + 8, yy - 25, 74, 18, 9, stroke=0, fill=1)
    txt(k, sx + 45, yy - 19.5, 8.5, "Sans-B", CARD if col == BLUE_TXT else BROWN, "c")
    txt(path, sx + 94, yy - 19.5, 8.8, "Mono", CREAM)
    txt(desc, sx + sw - 12, yy - 19.5, 7.8, "Sans", CREAM_D, "r")
y -= 3 * 38 + 18

y = h2("B · Instalar desde el marketplace oficial", y)
y -= 12
cb = code_block([
    [("# 1. (si hace falta) añade el marketplace oficial", CREAM_D)],
    [("/plugin marketplace add ", GOLD), ("anthropics/claude-plugins-official", C_)],
    [("# 2. instala el plugin (o navega con /plugin → Discover)", CREAM_D)],
    [("/plugin install ", GOLD), ("skill-creator@claude-plugins-official", C_)],
    [("# 3. recarga para activarlo", CREAM_D)],
    [("/reload-plugins", GOLD)],
], M, y, CW, 9, title="Claude Code")
y = cb - 20

y = h2("Usar y revisar tus skills", y)
y -= 12
uses = [
    ("/nombre-skill", "Invocar una skill directamente, con o sin argumentos."),
    ("/plugin:skill", "Invocar una skill que viene dentro de un plugin."),
    ("/skills", "Ver tus skills, incluidas las sincronizadas."),
    ("/skill-doctor", "Detectar skills que no usas y cuánto contexto ocupan."),
]
for i, (cmd, d) in enumerate(uses):
    col_ = i % 2
    ux = M + col_ * (CW / 2 + 6)
    uy = y - (i // 2) * 46
    uw = CW / 2 - 6
    rrect(ux, uy - 38, uw, 38, 7, fill=CARD, stroke=LINE)
    txt(cmd, ux + 12, uy - 16, 9.5, "Mono-B", GOLD_D)
    para(d, ux + 12, uy - 21, uw - 24, style(8, MUTED, lead=10.5))
y -= 2 * 46
para("También puedes no escribir nada: si la descripción encaja con tu petición, Claude activa la skill por su cuenta.",
     M, y - 4, CW, SMALL)
footer(pg)
c.showPage()

# =====================================================================
# PAGE 7 — COMPARTIR + SEGURIDAD
# =====================================================================
pg = 7
header("06", "Compartir y usar con seguridad", "Equipos y buenas prácticas")
y = H - 112
y = h2("Compartir en Team y Enterprise", y)
y -= 14
# diagram: author -> 3 sharing options
ax, ay = M, y - 120
rrect(ax, ay + 20, 120, 80, 10, fill=INK)
txt("Tu skill", ax + 60, ay + 70, 11, "Sans-B", GOLD, "c")
txt("Share  /  Publish", ax + 60, ay + 50, 8.5, "Sans", CREAM_D, "c")
txt("desde Customize › Skills", ax + 60, ay + 36, 7.5, "Sans", CREAM_D, "c")
opts = [
    ("Con personas", "Acceso de solo lectura. Las actualizaciones se sincronizan solas. Aparece en \"Shared with you\".", "Team y Enterprise", BLUE),
    ("Con grupos", "Comparte con un grupo completo. El propietario debe habilitarlo.", "Solo Enterprise", GOLD_D),
    ("Publicar a la organización", "Se publica en el directorio de la organización; puede requerir revisión. Los demás la instalan desde ahí.", "Team y Enterprise", RED),
]
ox = ax + 170
ow_ = CW - 170
for i, (t, d, tag, col) in enumerate(opts):
    oy = y - i * 64
    rrect(ox, oy - 56, ow_, 56, 8, fill=CARD, stroke=LINE)
    c.setFillColor(col)
    c.rect(ox, oy - 56, 4, 56, stroke=0, fill=1)
    txt(t, ox + 14, oy - 17, 10, "Sans-B", INK)
    tw = pdfmetrics.stringWidth(tag, "Sans-B", 7)
    rrect(ox + ow_ - tw - 22, oy - 22, tw + 12, 14, 7, fill=BLUE_TXT if col == BLUE else col)
    txt(tag, ox + ow_ - 16, oy - 17.5, 7, "Sans-B", BROWN if col == GOLD_D else CARD, "r")
    para(d, ox + 14, oy - 24, ow_ - 28, style(8.4, MUTED, lead=11))
    # connector from author card
    c.setStrokeColor(col); c.setLineWidth(1.3)
    sy = ay + 60
    ty_ = oy - 28
    p = c.beginPath()
    p.moveTo(ax + 120, sy)
    p.curveTo(ax + 145, sy, ax + 140, ty_, ox - 8, ty_)
    c.drawPath(p, stroke=1, fill=0)
    arrow(ox - 12, ty_, ox - 2, ty_, col, 1.3, 5)
y -= 3 * 64 + 16

y = h2("Seguridad: revisa antes de activar", y)
y -= 10
y = para("Una skill puede ejecutar código. Según Anthropic, los mayores riesgos son la <b>inyección de instrucciones</b> "
         "(prompt injection) y la <b>fuga de datos</b>. Usa esta lista antes de instalar cualquier skill de terceros:",
         M, y, CW, BODY)
y -= 12
checks = [
    ("¿Viene de una fuente de confianza?", "Prefiere skills de Anthropic, de tu organización o de autores que conozcas."),
    ("¿Leíste el SKILL.md completo?", "Busca instrucciones extrañas u ocultas que no tengan relación con la tarea."),
    ("¿Revisaste los scripts?", "Fíjate en qué paquetes instala y qué archivos lee o modifica."),
    ("¿Se conecta a internet?", "Desconfía si envía datos a servidores externos sin una razón clara."),
]
for i, (q, a) in enumerate(checks):
    col_ = i % 2
    cx_ = M + col_ * (CW / 2 + 6)
    cy_ = y - (i // 2) * 70
    cw_ = CW / 2 - 6
    rrect(cx_, cy_ - 62, cw_, 62, 8, fill=CARD, stroke=LINE)
    rrect(cx_ + 12, cy_ - 28, 16, 16, 4, stroke=GOLD_D, lw=1.4)
    txt("✓", cx_ + 20, cy_ - 24.5, 11, "Sym-B", GOLD_D, "c")
    txt(q, cx_ + 36, cy_ - 24, 9.5, "Sans-B", INK)
    para(a, cx_ + 36, cy_ - 32, cw_ - 48, style(8.4, MUTED, lead=11.2))
y -= 2 * 70 + 6
callout(M, y, CW, "Regla de oro",
        "Si no entiendes lo que hace una skill, no la actives. Puedes pedirle a Claude que la revise contigo antes de subirla.",
        "warn")
footer(pg)
c.showPage()

# =====================================================================
# PAGE 8 — PROBLEMAS FRECUENTES + RESUMEN
# =====================================================================
pg = 8
header("07", "Solución de problemas", "Si algo no funciona")
y = H - 112
probs = [
    ("No veo la sección Skills", "La ejecución de código está desactivada, o en Team/Enterprise el propietario no habilitó Skills.",
     "Activa Code execution (paso 02) o pide a tu administrador que active Skills en Plugins & skills → Policy."),
    ("Error al subir el .zip", "Falta SKILL.md, la carpeta no está dentro del zip, o el nombre/descripción tiene caracteres inválidos.",
     "Revisa la estructura (página 5). La carpeta debe llamarse igual que la skill."),
    ("Claude no usa mi skill", "La descripción es vaga, o el interruptor de la skill está apagado.",
     "Reescribe la descripción con palabras clave de la tarea, o pídela por su nombre."),
    ("Se activa cuando no debe", "La descripción es demasiado amplia.",
     "Hazla más específica. En Claude Code, añade disable-model-invocation: true para usarla solo con /nombre."),
    ("No puedo crear o compartir", "Tu organización restringe la creación o el uso compartido de skills.",
     "Consulta con el propietario de la organización."),
]
# table header
c1, c2, c3 = 140, (CW - 140) / 2, (CW - 140) / 2
rrect(M, y - 26, CW, 26, 6, fill=INK)
txt("Problema", M + 12, y - 17, 9, "Sans-B", GOLD)
txt("Causa probable", M + c1 + 12, y - 17, 9, "Sans-B", GOLD)
txt("Solución", M + c1 + c2 + 12, y - 17, 9, "Sans-B", GOLD)
y -= 30
for i, (p_, ca, so) in enumerate(probs):
    ps = [Paragraph(f"<b>{p_}</b>", style(9, INK, lead=12)),
          Paragraph(ca, style(8.5, MUTED, lead=11.5)),
          Paragraph(so, style(8.5, INK, lead=11.5))]
    hs = [p.wrap(w_ - 24, 300)[1] for p, w_ in zip(ps, [c1, c2, c3])]
    rh = max(hs) + 18
    rrect(M, y - rh, CW, rh, 6, fill=CARD if i % 2 == 0 else GOLD_T)
    for p, xo in zip(ps, [0, c1, c1 + c2]):
        p.drawOn(c, M + xo + 12, y - 9 - p.height)
    y -= rh + 4
y -= 18

y = h2("Resumen en una mirada", y)
y -= 16
# summary flow vertical-ish: 4 big steps in a 2x2 with arrows
summ = [
    ("1", "Activa", "Code execution y, en equipos, Skills."),
    ("2", "Prepara", "Carpeta con SKILL.md, comprimida en .zip."),
    ("3", "Sube", "Customize → Skills → + → Create skill → Upload a skill."),
    ("4", "Usa", "Pide la tarea o escribe /nombre. Claude hace el resto."),
]
sw4 = (CW - 3 * 16) / 4
for i, (n, t, d) in enumerate(summ):
    sx_ = M + i * (sw4 + 16)
    rrect(sx_, y - 122, sw4, 122, 10, fill=INK)
    txt(n, sx_ + 14, y - 34, 26, "Sans-B", GOLD)
    txt(t, sx_ + 14, y - 56, 12, "Sans-B", CREAM)
    para(d, sx_ + 14, y - 64, sw4 - 28, style(8.4, CREAM_D, lead=11.5))
    if i < 3:
        arrow(sx_ + sw4 + 2, y - 55, sx_ + sw4 + 14, y - 55, GOLD, 1.8, 6)
y -= 144

y = h2("Fuentes oficiales", y)
y -= 12
src = [
    "Use skills in Claude — support.claude.com/en/articles/12512180",
    "How to create custom skills — support.claude.com/en/articles/12512198",
    "Extend Claude with skills (Claude Code) — code.claude.com/docs/en/skills",
]
for s in src:
    txt("›", M + 2, y - 10, 10, "Sans-B", GOLD_D)
    txt(s, M + 14, y - 10, 9, "Sans", INK)
    y -= 16
y -= 6
para("Información verificada el 1 de octubre de 2026. Anthropic actualiza la interfaz con frecuencia: si un menú cambió de nombre, "
     "busca la sección <b>Skills</b> dentro de <b>Customize</b> o consulta las fuentes de arriba.",
     M, y, CW, style(8.5, MUTED, font="Sans-I", lead=12))
footer(pg)
c.showPage()

c.save()
print("ok")
