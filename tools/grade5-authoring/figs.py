"""Reusable SVG diagram generators for Grade 5 (also used for cheat sheets and project pages).

render(kind, data) -> SVG string. Every drawing is built only from `data`, which is also stored in the
check file, so the verifier can recompute the answer from exactly what is drawn.
"""
import math
from fractions import Fraction as F

FONT = "Inter, 'DejaVu Sans', Arial, sans-serif"
INK = "#1d2a3a"
PAL = ["#2f7fd8", "#f08c1a", "#1aa37a", "#d63c7a", "#8a4fd6", "#0f97b5", "#e2563b", "#5a62d8", "#2a9d4b", "#b8860b"]
FILL = {"blue": "#7fb6f0", "orange": "#ffc27a", "green": "#8fdcbf", "pink": "#f5a3c4", "purple": "#c3a6f0", "teal": "#86d4e4",
        "yellow": "#ffe08a", "red": "#f6a08f", "gray": "#e8ecf2"}


def PF(v):
    """Fraction from int/Fraction/'a/b'/'w a/b'/'1.25'."""
    if isinstance(v, (int, F)):
        return F(v)
    v = str(v).strip()
    if " " in v:
        w, fr = v.split(" ", 1)
        return int(w) + F(fr)
    return F(v)


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(w, h, body, bg="#ffffff"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="{FONT}">'
            f'<rect width="{w}" height="{h}" fill="{bg}"/>{body}</svg>')


def text(x, y, s, size=18, anchor="middle", weight="600", fill=INK, extra=""):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{fill}" {extra}>{esc(s)}</text>'


def ftext(x, y, s, size=18, fill=INK, weight="700"):
    """Text that may be a fraction 'a/b' or mixed 'w a/b': drawn stacked. y = baseline of a whole number."""
    s = str(s)
    if "/" not in s:
        return text(x, y, s, size, weight=weight, fill=fill)
    whole, fr = (s.split(" ", 1) + [""])[:2] if " " in s else ("", s)
    n, d = fr.split("/")
    fs = size * 0.78
    wd = max(len(n), len(d)) * fs * 0.62 + 4
    out = ""
    if whole:
        ww = len(whole) * size * 0.62
        total = ww + 3 + wd
        x0 = x - total / 2
        out += text(x0 + ww / 2, y, whole, size, weight=weight, fill=fill)
        cx = x0 + ww + 3 + wd / 2
    else:
        cx = x
    out += text(cx, y - fs * 0.55, n, fs, weight=weight, fill=fill)
    out += f'<line x1="{cx - wd / 2:.1f}" y1="{y - fs * 0.32:.1f}" x2="{cx + wd / 2:.1f}" y2="{y - fs * 0.32:.1f}" stroke="{fill}" stroke-width="1.6"/>'
    out += text(cx, y + fs * 0.62, d, fs, weight=weight, fill=fill)
    return out


def rect(x, y, w, h, fill="#fff", stroke=INK, sw=2, rx=0, extra=""):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'


def line(x1, y1, x2, y2, stroke=INK, sw=2, extra=""):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'


def poly(pts, fill="#fff", stroke=INK, sw=2.5):
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polygon points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'


def title(w, s):
    return text(w / 2, 26, s, 18, weight="700") if s else ""


# ------------------------------------------------------------------ fraction models
def fraction_bars(d):
    """bars: [{"parts": n, "shaded": k, "label": "..."}]; all bars represent the same whole."""
    bars = d["bars"]
    W, bw, top = 640, 520, 44 if d.get("title") else 16
    h = top + len(bars) * 64 + 10
    out = title(W, d.get("title"))
    for i, b in enumerate(bars):
        y = top + i * 64
        n, k = b["parts"], b["shaded"]
        col = FILL[b.get("color", ["blue", "orange", "green", "pink"][i % 4])]
        whole = b.get("wholes", 1)
        cell = bw / n if whole == 1 else bw / (n)
        for j in range(n):
            out += rect(20 + j * cell, y, cell, 44, col if j < k else "#ffffff", sw=2)
        if b.get("label"):
            out += ftext(20 + bw + 50, y + 29, b["label"], 20)
    return svg(W, h, out)


def fraction_circle(d):
    n, k = d["parts"], d["shaded"]
    count = d.get("circles", 1)
    W = 40 + count * 190
    out = ""
    for c in range(count):
        cx, cy, R = 115 + c * 190, 105, 85
        sh = d["per_circle"] if d.get("per_circle") else min(n, max(0, k - c * n))
        for j in range(n):
            a0, a1 = -math.pi / 2 + 2 * math.pi * j / n, -math.pi / 2 + 2 * math.pi * (j + 1) / n
            x0, y0, x1, y1 = cx + R * math.cos(a0), cy + R * math.sin(a0), cx + R * math.cos(a1), cy + R * math.sin(a1)
            large = 1 if a1 - a0 > math.pi else 0
            fill = FILL[d.get("color", "orange")] if j < sh else "#ffffff"
            if n == 1:
                out += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{fill}" stroke="{INK}" stroke-width="2.5"/>'
            else:
                out += f'<path d="M{cx},{cy} L{x0:.1f},{y0:.1f} A{R},{R} 0 {large} 1 {x1:.1f},{y1:.1f} Z" fill="{fill}" stroke="{INK}" stroke-width="2.5"/>'
    return svg(W, 210, out)


def area_grid(d):
    """Unit square (or rectangle of whole units) cut into rows x cols; shaded rectangle sh_r x sh_c (fraction multiplication / area).
    data: rows, cols, sh_rows, sh_cols, side labels optional, double (cross-hatch) optional."""
    R, C = d["rows"], d["cols"]
    W, H = 640, 330
    s = min(400 / C, 250 / R)
    x0, y0 = (W - C * s) / 2, 40
    out = ""
    shr, shc = d.get("sh_rows", 0), d.get("sh_cols", 0)
    for i in range(R):
        for j in range(C):
            a = i < shr
            b = j < shc
            fill = "#ffffff"
            if d.get("mode") == "overlap":
                fill = "#b9a3f2" if (a and b) else ("#cfe4fb" if b else ("#ffe2bf" if a else "#ffffff"))
            elif a and b:
                fill = FILL[d.get("color", "green")]
            out += rect(x0 + j * s, y0 + i * s, s, s, fill, sw=1.6)
    out += rect(x0, y0, C * s, R * s, "none", sw=3.5)
    if d.get("top"):
        out += ftext(x0 + C * s / 2, y0 - 12, d["top"], 18)
    if d.get("left"):
        out += ftext(x0 - 40, y0 + R * s / 2 + 6, d["left"], 18)
    if d.get("units"):
        out += text(W / 2, H - 8, d["units"], 15, weight="500")
    return svg(W, H, out)


def tape(d):
    """Tape (bar) diagram: total split into equal parts, some labeled. data: parts, shaded, total_label, part_label."""
    n, k = d["parts"], d.get("shaded", 0)
    W, bw = 640, 560
    out = ""
    cell = bw / n
    for j in range(n):
        out += rect(40 + j * cell, 50, cell, 50, FILL["teal"] if j < k else "#fff", sw=2)
        if d.get("each"):
            out += ftext(40 + j * cell + cell / 2, 82, d["each"], 16)
    out += line(40, 30, 40 + bw, 30, sw=1.6) + line(40, 22, 40, 38, sw=1.6) + line(40 + bw, 22, 40 + bw, 38, sw=1.6)
    out += ftext(40 + bw / 2, 22, d.get("total_label", ""), 18)
    if d.get("note"):
        out += text(W / 2, 134, d["note"], 16, weight="500")
    return svg(W, 150, out)


# ------------------------------------------------------------------ number lines and rulers
def number_line(d):
    """lo, hi (Fractions as strings), den: tick denominator, label_every, points [{"x":"3/4","label":"A","color":..}], jumps."""
    lo, hi, den = PF(d["lo"]), PF(d["hi"]), int(d["den"])
    W, H = 680, 150 if not d.get("jumps") else 180
    x0, x1, y = 40, W - 40, H - 70
    sc = (x1 - x0) / float(hi - lo)
    X = lambda v: x0 + float(PF(v) - lo) * sc
    out = line(x0 - 18, y, x1 + 18, y, sw=2.5)
    out += poly([(x1 + 22, y), (x1 + 10, y - 7), (x1 + 10, y + 7)], INK, INK, 1) + poly([(x0 - 22, y), (x0 - 10, y - 7), (x0 - 10, y + 7)], INK, INK, 1)
    n = int((hi - lo) * den)
    lab = d.get("label_every", 1)
    for i in range(n + 1):
        v = lo + F(i, den)
        big = v.denominator == 1
        out += line(X(v), y - (13 if big else 8), X(v), y + (13 if big else 8), sw=2.5 if big else 1.6)
        if d.get("labels", "all") == "all" and i % lab == 0 or (d.get("labels") == "whole" and big):
            t = str(v.numerator // v.denominator) if big else (d.get("fmt") == "dec" and _decs(v) or f"{v.numerator}/{v.denominator}")
            if d.get("fmt") == "dec" and not big:
                t = _decs(v)
            out += ftext(X(v), y + 38, t, 16)
    for p in d.get("points", []):
        col = p.get("color", "#d63c7a")
        out += f'<circle cx="{X(p["x"]):.1f}" cy="{y}" r="8" fill="{col}" stroke="#fff" stroke-width="2"/>'
        if p.get("label"):
            out += text(X(p["x"]), y - 18, p["label"], 18, weight="800", fill=col)
    for j in d.get("jumps", []):
        a, b = X(j[0]), X(j[1])
        out += f'<path d="M{a:.1f},{y - 4} Q{(a + b) / 2:.1f},{y - 70} {b:.1f},{y - 4}" fill="none" stroke="#f08c1a" stroke-width="3"/>'
        if len(j) > 2:
            out += ftext((a + b) / 2, y - 50, j[2], 15, fill="#b35d00")
    return svg(W, H, out)


def _decs(v):
    from g5lib import dec
    return dec(v)


def ruler(d):
    """Inch ruler 0..length with 1/den marks and a bar (object) from start to end (inches as fraction strings)."""
    L, den = int(d["length"]), int(d.get("den", 8))
    s, e = PF(d.get("start", "0")), PF(d["end"])
    W, H = 680, 170
    x0, sc = 40, 600 / L
    X = lambda v: x0 + float(PF(v)) * sc
    out = rect(X(s), 26, X(e) - X(s), 30, FILL["orange"], sw=2, rx=6)
    if d.get("object"):
        out += text((X(s) + X(e)) / 2, 47, d["object"], 15, weight="700")
    out += rect(x0 - 12, 70, 624, 74, "#fff7d6", sw=2, rx=6)
    for i in range(L * den + 1):
        v = F(i, den)
        hgt = 34 if v.denominator == 1 else 24 if v.denominator == 2 else 17 if v.denominator == 4 else 11
        out += line(X(v), 70, X(v), 70 + hgt, sw=2 if v.denominator == 1 else 1.4)
        if v.denominator == 1:
            out += text(X(v), 128, str(v.numerator), 17)
    out += text(W - 46, 160, "inches", 13, anchor="end", weight="500")
    return svg(W, H, out)


# ------------------------------------------------------------------ place value and base ten
PLACES = ["thousands", "hundreds", "tens", "ones", "tenths", "hundredths", "thousandths"]


def place_chart(d):
    """digits: dict place -> digit; highlight: place."""
    cols = d.get("places", PLACES)
    W = 40 + len(cols) * 88
    out = ""
    for i, p in enumerate(cols):
        x = 20 + i * 88
        dec_side = p in ("tenths", "hundredths", "thousandths")
        out += rect(x, 20, 88, 40, "#e6f0fc" if not dec_side else "#fff0dc", sw=1.5)
        out += text(x + 44, 45, p, 13, weight="700")
        hi = d.get("highlight") == p
        out += rect(x, 60, 88, 60, FILL["yellow"] if hi else "#fff", sw=1.5)
        dg = d["digits"].get(p, "")
        out += text(x + 44, 102, str(dg), 30, weight="800")
    ones_i = cols.index("ones") if "ones" in cols else None
    if ones_i is not None and any(p in cols for p in ("tenths",)):
        out += f'<circle cx="{20 + (ones_i + 1) * 88:.1f}" cy="112" r="5" fill="{INK}"/>'
    return svg(W, 140, out)


def base_ten(d):
    """Base-ten blocks: flats (hundreds), rods (tens), units. Optional decimal meaning (flat = 1 whole)."""
    fl, rd, un = d.get("flats", 0), d.get("rods", 0), d.get("units", 0)
    s = 9
    x = 20
    out = ""
    for _ in range(fl):
        for i in range(10):
            for j in range(10):
                out += rect(x + j * s, 30 + i * s, s, s, FILL["blue"], sw=0.8)
        out += rect(x, 30, 10 * s, 10 * s, "none", sw=2)
        x += 10 * s + 14
    for _ in range(rd):
        for i in range(10):
            out += rect(x, 30 + i * s, s, s, FILL["green"], sw=0.8)
        out += rect(x, 30, s, 10 * s, "none", sw=2)
        x += s + 10
    ux = x + 6
    for k in range(un):
        out += rect(ux + (k % 3) * (s + 5), 30 + (k // 3) * (s + 5), s, s, FILL["orange"], sw=1.2)
    W = max(ux + 3 * (s + 5) + 20, 260)
    if d.get("key"):
        out += text(20, 160, d["key"], 14, anchor="start", weight="500")
    return svg(W, 175, out)


def hundred_grid(d):
    """10 x 10 grid representing one whole; `shaded` hundredths shaded (row by row). grids: number of grids."""
    sh = d["shaded"]
    g = d.get("grids", 1)
    s = 17
    W = 30 + g * (10 * s + 30)
    out = ""
    for k in range(g):
        x0 = 20 + k * (10 * s + 30)
        for i in range(100):
            r_, c_ = divmod(i, 10)
            on = (k * 100 + i) < sh
            out += rect(x0 + c_ * s, 20 + r_ * s, s, s, FILL["green"] if on else "#fff", sw=1)
        out += rect(x0, 20, 10 * s, 10 * s, "none", sw=2.5)
    return svg(W, 10 * s + 40, out)


# ------------------------------------------------------------------ area model and arrays
def area_model(d):
    """Partial-products area model. rows: labels (left), cols: labels (top), cells: 2D labels ('' allowed, '?' for unknown)."""
    rows, cols, cells = d["rows"], d["cols"], d["cells"]
    W = 640
    cw = [max(70, 360 * (len(str(c)) / max(1, sum(len(str(x)) for x in cols)))) for c in cols]
    tot = sum(cw)
    cw = [c * 460 / tot for c in cw]
    rh = 64 if len(rows) <= 2 else 52
    x0, y0 = 120, 52
    out = ""
    y = y0
    for i, rl in enumerate(rows):
        x = x0
        for j, cl in enumerate(cols):
            out += rect(x, y, cw[j], rh, [FILL["blue"], FILL["orange"], FILL["green"], FILL["pink"], FILL["purple"]][(i + j) % 5] if d.get("color", True) else "#fff", sw=2)
            out += text(x + cw[j] / 2, y + rh / 2 + 7, cells[i][j], 19, weight="700")
            if i == 0:
                out += text(x + cw[j] / 2, y0 - 14, cl, 19, weight="800", fill="#2b4f8c")
            x += cw[j]
        out += text(x0 - 16, y + rh / 2 + 7, rl, 19, anchor="end", weight="800", fill="#2b4f8c")
        y += rh
    return svg(W, y + 20, out)


def array_dots(d):
    R, C = d["rows"], d["cols"]
    s = min(36, 560 / C, 230 / R)
    W, H = C * s + 60, R * s + 40
    out = ""
    for i in range(R):
        for j in range(C):
            out += f'<circle cx="{30 + j * s + s / 2:.1f}" cy="{20 + i * s + s / 2:.1f}" r="{s * 0.34:.1f}" fill="{PAL[i % len(PAL)] if d.get("rainbow") else "#2f7fd8"}"/>'
    return svg(W, H, out)


# ------------------------------------------------------------------ coordinate plane
def coord(d):
    """First-quadrant grid 0..xmax, 0..ymax. points: [{"x":..,"y":..,"label":..}], path: [[x,y],...], polygon: [[x,y],...],
    xlab/ylab axis titles, step (tick label step)."""
    xm, ym = d["xmax"], d["ymax"]
    st = d.get("step", 1)
    s = min(480 / xm, 360 / ym)
    left, bottom = 70, 60
    W, H = int(left + xm * s + 50), int(ym * s + bottom + 40)
    X = lambda v: left + float(PF(v)) * s
    Y = lambda v: H - bottom - float(PF(v)) * s
    out = ""
    for i in range(xm + 1):
        out += line(X(i), Y(0), X(i), Y(ym), "#c9d6e6", 1)
    for j in range(ym + 1):
        out += line(X(0), Y(j), X(xm), Y(j), "#c9d6e6", 1)
    out += line(X(0), Y(0), X(xm) + 14, Y(0), sw=2.5) + line(X(0), Y(0), X(0), Y(ym) - 14, sw=2.5)
    out += poly([(X(xm) + 20, Y(0)), (X(xm) + 8, Y(0) - 6), (X(xm) + 8, Y(0) + 6)], INK, INK, 1)
    out += poly([(X(0), Y(ym) - 20), (X(0) - 6, Y(ym) - 8), (X(0) + 6, Y(ym) - 8)], INK, INK, 1)
    for i in range(0, xm + 1, st):
        out += text(X(i), Y(0) + 22, str(i * d.get("xscale", 1)), 14, weight="600")
    for j in range(0, ym + 1, st):
        if j:
            out += text(X(0) - 10, Y(j) + 5, str(j * d.get("yscale", 1)), 14, anchor="end", weight="600")
    if d.get("xlab"):
        out += text(X(xm / 2), H - 12, d["xlab"], 15, weight="700")
    if d.get("ylab"):
        out += f'<text x="18" y="{Y(ym / 2):.1f}" font-size="15" font-weight="700" fill="{INK}" text-anchor="middle" transform="rotate(-90 18 {Y(ym / 2):.1f})">{esc(d["ylab"])}</text>'
    if d.get("polygon"):
        out += poly([(X(x), Y(y)) for x, y in d["polygon"]], "#cfe4fb", "#2f7fd8", 2.5)
    if d.get("path"):
        pts = " ".join(f"{X(x):.1f},{Y(y):.1f}" for x, y in d["path"])
        out += f'<polyline points="{pts}" fill="none" stroke="#f08c1a" stroke-width="3"/>'
    for k, p in enumerate(d.get("points", [])):
        col = p.get("color", PAL[k % len(PAL)])
        out += f'<circle cx="{X(p["x"]):.1f}" cy="{Y(p["y"]):.1f}" r="7" fill="{col}" stroke="#fff" stroke-width="2"/>'
        if p.get("label"):
            out += text(X(p["x"]) + 12, Y(p["y"]) - 10, p["label"], 17, anchor="start", weight="800", fill=col)
    return svg(W, H, out)


# ------------------------------------------------------------------ polygons
def _marks(a, b, n, size=8):
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    px, py = -uy, ux
    out = ""
    for i in range(n):
        off = (i - (n - 1) / 2) * 6
        cx, cy = mx + ux * off, my + uy * off
        out += line(cx - px * size, cy - py * size, cx + px * size, cy + py * size, sw=2)
    return out


def _arrow(a, b, n):
    mx, my = a[0] + (b[0] - a[0]) * 0.3, a[1] + (b[1] - a[1]) * 0.3
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    px, py = -uy, ux
    out = ""
    for i in range(n):
        cx, cy = mx + ux * (i * 9 - (n - 1) * 4.5), my + uy * (i * 9 - (n - 1) * 4.5)
        out += f'<polyline points="{cx - ux * 8 + px * 7:.1f},{cy - uy * 8 + py * 7:.1f} {cx:.1f},{cy:.1f} {cx - ux * 8 - px * 7:.1f},{cy - uy * 8 - py * 7:.1f}" fill="none" stroke="#d63c7a" stroke-width="2.4"/>'
    return out


def _right(p, a, b, s=16):
    ax, ay = a[0] - p[0], a[1] - p[1]
    bx, by = b[0] - p[0], b[1] - p[1]
    la, lb = math.hypot(ax, ay), math.hypot(bx, by)
    ax, ay, bx, by = ax / la * s, ay / la * s, bx / lb * s, by / lb * s
    return f'<polyline points="{p[0] + ax:.1f},{p[1] + ay:.1f} {p[0] + ax + bx:.1f},{p[1] + ay + by:.1f} {p[0] + bx:.1f},{p[1] + by:.1f}" fill="none" stroke="{INK}" stroke-width="2"/>'


def shape(d):
    """pts: polygon vertices (any scale; fitted). ticks: [[i, n]] side i (pts[i]→pts[i+1]) gets n tick marks.
    arrows: [[i, n]] parallel arrows. right: [i] vertex indices with right-angle marks. side_labels: [[i, text]],
    angle_labels: [[i, text]], fill color name."""
    pts = d["pts"]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    w, h = max(xs) - min(xs), max(ys) - min(ys)
    sc = min(360 / max(w, 1e-9), 220 / max(h, 1e-9))
    W, H = 520, 300
    ox, oy = (W - w * sc) / 2, (H - h * sc) / 2 + 4
    P = [(ox + (x - min(xs)) * sc, H - (oy + (y - min(ys)) * sc)) for x, y in pts]
    out = poly(P, FILL[d.get("fill", "blue")], INK, 3)
    n = len(P)
    for i, k in d.get("ticks", []):
        out += _marks(P[i], P[(i + 1) % n], k)
    for i, k in d.get("arrows", []):
        out += _arrow(P[i], P[(i + 1) % n], k)
    for i in d.get("right", []):
        out += _right(P[i], P[i - 1], P[(i + 1) % n])
    cx, cy = sum(p[0] for p in P) / n, sum(p[1] for p in P) / n
    for i, t in d.get("side_labels", []):
        a, b = P[i], P[(i + 1) % n]
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        vx, vy = mx - cx, my - cy
        L = math.hypot(vx, vy) or 1
        out += text(mx + vx / L * 26, my + vy / L * 26 + 6, t, 17, weight="700")
    for i, t in d.get("angle_labels", []):
        p = P[i]
        vx, vy = cx - p[0], cy - p[1]
        L = math.hypot(vx, vy) or 1
        out += text(p[0] + vx / L * 38, p[1] + vy / L * 38 + 6, t, 16, weight="700", fill="#8a2d5a")
    for i, t in d.get("vertex_labels", []):
        p = P[i]
        vx, vy = p[0] - cx, p[1] - cy
        L = math.hypot(vx, vy) or 1
        out += text(p[0] + vx / L * 20, p[1] + vy / L * 20 + 6, t, 18, weight="800")
    return svg(W, H, out)


def shape_row(d):
    """Several labeled small shapes in a row: items [{"pts":..., "label":"A", "right":[..], "ticks":[...], "arrows":[...]}]"""
    items = d["items"]
    cw = 170
    W, H = cw * len(items) + 20, 200
    out = ""
    for k, it in enumerate(items):
        pts = it["pts"]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        w, h = max(xs) - min(xs), max(ys) - min(ys)
        sc = min(120 / max(w, 1e-9), 120 / max(h, 1e-9))
        ox = 10 + k * cw + (cw - w * sc) / 2
        oy = 30 + (130 - h * sc) / 2
        P = [(ox + (x - min(xs)) * sc, 30 + 130 - ((y - min(ys)) * sc) - (oy - 30)) for x, y in pts]
        out += poly(P, FILL[["blue", "orange", "green", "pink", "purple", "teal"][k % 6]], INK, 2.5)
        n = len(P)
        for i, m in it.get("ticks", []):
            out += _marks(P[i], P[(i + 1) % n], m, 6)
        for i, m in it.get("arrows", []):
            out += _arrow(P[i], P[(i + 1) % n], m)
        for i in it.get("right", []):
            out += _right(P[i], P[i - 1], P[(i + 1) % n], 11)
        out += text(10 + k * cw + cw / 2, 190, it["label"], 20, weight="800")
    return svg(W, H, out)


# ------------------------------------------------------------------ 3-D: unit cubes and prisms
def _cube(x, y, s, fill):
    """Isometric-ish cube with front face at (x, y) (top-left), size s, depth offset."""
    dx, dy = s * 0.5, s * 0.35
    top = poly([(x, y), (x + dx, y - dy), (x + s + dx, y - dy), (x + s, y)], _shade(fill, 1.12), INK, 1.3)
    side = poly([(x + s, y), (x + s + dx, y - dy), (x + s + dx, y + s - dy), (x + s, y + s)], _shade(fill, 0.82), INK, 1.3)
    front = rect(x, y, s, s, fill, INK, 1.3)
    return front + top + side


def _shade(hexc, f):
    h = hexc.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    c = lambda v: max(0, min(255, int(v * f)))
    return f"#{c(r):02x}{c(g):02x}{c(b):02x}"


def cubes(d):
    """Unit-cube prism(s). blocks: [{"l":, "w":, "h":, "x":offset_in_units, "color":}] drawn back to front.
    l along x (right), w into depth, h up. labels: show edge counts."""
    blocks = d["blocks"]
    maxl = max(b.get("x", 0) + b["l"] for b in blocks)
    maxw = max(b["w"] for b in blocks)
    maxh = max(b["h"] for b in blocks)
    s = min(46, 430 / (maxl + maxw * 0.5 + 0.5), 250 / (maxh + maxw * 0.35 + 0.3))
    W = int((maxl + maxw * 0.5) * s + 120)
    H = int((maxh + maxw * 0.35) * s + 90)
    out = ""
    base_y = H - 50
    cells = []
    for bi, b in enumerate(blocks):
        for k in range(b["w"]):
            for z in range(b["h"]):
                for i in range(b["l"]):
                    cells.append((k, z, b.get("x", 0) + i, b.get("color", "#7fb6f0")))
    # painter: far depth first (k high first), then bottom-up, then left to right
    cells.sort(key=lambda c: (-c[0], c[1], c[2]))
    for k, z, i, col in cells:
        x = 50 + i * s + k * s * 0.5
        y = base_y - (z + 1) * s - k * s * 0.35
        out += _cube(x, y, s, col)
    if d.get("labels"):
        b = blocks[0]
        out += text(50 + b["l"] * s / 2, base_y + 26, f'{b["l"]} {d.get("unit_word", "units")}', 16, weight="700")
        out += text(50 + b["l"] * s + b["w"] * s * 0.5 + 14, base_y - b["w"] * s * 0.175 + 4, f'{b["w"]}', 16, anchor="start", weight="700")
        out += text(38, base_y - b["h"] * s / 2, f'{b["h"]}', 16, anchor="end", weight="700")
    return svg(W, H, out)


def prism(d):
    """Solid rectangular prism with edge labels (not cubes). l, w, h numbers (used for proportions, capped), labels text."""
    l, w, h = float(d["l"]), float(d["w"]), float(d["h"])
    m = max(l, w * 0.6, h)
    s = 300 / m
    L_, H_ = max(l * s, 90), max(h * s, 70)
    D = max(min(w * s * 0.45, 140), 40)
    dx, dy = D * 0.8, D * 0.55
    x, y = 70, 60 + dy
    W, Hh = int(L_ + dx + 160), int(H_ + dy + 110)
    col = FILL[d.get("color", "teal")]
    out = poly([(x, y), (x + dx, y - dy), (x + dx + L_, y - dy), (x + L_, y)], _shade(col, 1.1), INK, 2.5)
    out += poly([(x + L_, y), (x + L_ + dx, y - dy), (x + L_ + dx, y + H_ - dy), (x + L_, y + H_)], _shade(col, 0.85), INK, 2.5)
    out += rect(x, y, L_, H_, col, INK, 2.5)
    out += text(x + L_ / 2, y + H_ + 28, d["lt"], 17, weight="700")
    out += text(x + L_ + dx / 2 + 14, y + H_ - dy / 2 + 14, d["wt"], 17, anchor="start", weight="700")
    out += text(x - 12, y + H_ / 2 + 6, d["ht"], 17, anchor="end", weight="700")
    return svg(W, Hh, out)


def composite(d):
    """Two rectangular prisms side by side (L-shape): a = {l,w,h,lt,wt,ht}, b = {...} sharing depth w, b placed right of a."""
    A, B = d["a"], d["b"]
    w = float(A["w"])
    m = max(float(A["l"]) + float(B["l"]), float(A["h"]), float(B["h"]))
    s = 320 / m
    D = max(min(w * s * 0.45, 120), 40)
    dx, dy = D * 0.8, D * 0.55
    la, ha, lb, hb = float(A["l"]) * s, float(A["h"]) * s, float(B["l"]) * s, float(B["h"]) * s
    base = 60 + dy + max(ha, hb)
    x = 80
    W, H = int(la + lb + dx + 190), int(max(ha, hb) + dy + 120)
    out = ""
    for (xx, ll, hh, col, lab) in ((x, la, ha, FILL["blue"], A), (x + la, lb, hb, FILL["orange"], B)):
        y = base - hh
        out += poly([(xx, y), (xx + dx, y - dy), (xx + dx + ll, y - dy), (xx + ll, y)], _shade(col, 1.1), INK, 2.2)
        out += poly([(xx + ll, y), (xx + ll + dx, y - dy), (xx + ll + dx, base - dy), (xx + ll, base)], _shade(col, 0.85), INK, 2.2)
        out += rect(xx, y, ll, hh, col, INK, 2.2)
        out += text(xx + ll / 2, base + 26, lab["lt"], 16, weight="700")
        out += text(xx + ll / 2, y + hh / 2 + 6, lab["ht"], 16, weight="700")
    out += text(x + la + lb + dx / 2 + 14, base - dy / 2 + 6, A["wt"], 16, anchor="start", weight="700")
    return svg(W, H, out)


# ------------------------------------------------------------------ data
def lineplot(d):
    """values: list of fraction strings; lo, hi, den; title; unit. Dots stacked as X marks (circles)."""
    lo, hi, den = PF(d["lo"]), PF(d["hi"]), int(d["den"])
    vals = [PF(v) for v in d["values"]]
    from collections import Counter
    cnt = Counter(vals)
    mx = max(cnt.values())
    W = 680
    H = 120 + mx * 26 + (30 if d.get("title") else 0)
    x0, x1 = 50, W - 50
    y = H - 62
    sc = (x1 - x0) / float(hi - lo)
    X = lambda v: x0 + float(PF(v) - lo) * sc
    out = title(W, d.get("title"))
    out += line(x0 - 16, y, x1 + 16, y, sw=2.5)
    n = int((hi - lo) * den)
    for i in range(n + 1):
        v = lo + F(i, den)
        out += line(X(v), y - 8, X(v), y + 8, sw=2)
        w_, r_ = divmod(v.numerator, v.denominator)
        t = str(w_) if r_ == 0 else (f"{w_} {r_}/{v.denominator}" if w_ else f"{r_}/{v.denominator}")
        out += ftext(X(v), y + 32, t, 15)
    for v, c in cnt.items():
        for k in range(c):
            cx, cy = X(v), y - 22 - k * 26
            out += line(cx - 8, cy - 8, cx + 8, cy + 8, "#2f7fd8", 3.4) + line(cx - 8, cy + 8, cx + 8, cy - 8, "#2f7fd8", 3.4)
    if d.get("unit"):
        out += text(W / 2, H - 6, d["unit"], 15, weight="600")
    return svg(W, H, out)


def table(d):
    """Simple table: header [..], rows [[..]]. Cells may be fractions."""
    hd, rows = d["header"], d["rows"]
    cols = len(hd)
    cw = min(150, 600 / cols)
    W = int(cw * cols + 40)
    rh = 46
    H = int(rh * (len(rows) + 1) + 30)
    out = ""
    for j, h in enumerate(hd):
        out += rect(20 + j * cw, 14, cw, rh, "#dfeafb", sw=1.5) + text(20 + j * cw + cw / 2, 14 + 30, h, 16, weight="800")
    for i, row in enumerate(rows):
        for j, c in enumerate(row):
            out += rect(20 + j * cw, 14 + (i + 1) * rh, cw, rh, "#fff" if i % 2 == 0 else "#f6f8fc", sw=1.5)
            out += ftext(20 + j * cw + cw / 2, 14 + (i + 1) * rh + 30, c, 17)
    return svg(W, H, out)


def two_tables(d):
    """Two pattern rows (term number on top): rows [["Pattern A", [..]], ["Pattern B", [..]]]."""
    rows = d["rows"]
    n = max(len(r[1]) for r in rows)
    cw = 72
    W = int(150 + cw * n + 20)
    H = 30 + 46 * (len(rows) + 1)
    out = rect(10, 14, 140, 46, "#dfeafb", sw=1.5) + text(80, 44, "Term", 16, weight="800")
    for j in range(n):
        out += rect(150 + j * cw, 14, cw, 46, "#dfeafb", sw=1.5) + text(150 + j * cw + cw / 2, 44, str(j + 1), 16, weight="800")
    for i, (lab, vals) in enumerate(rows):
        y = 14 + (i + 1) * 46
        out += rect(10, y, 140, 46, "#fff", sw=1.5) + text(80, y + 30, lab, 16, weight="800", fill=PAL[i])
        for j, v in enumerate(vals):
            out += rect(150 + j * cw, y, cw, 46, "#fff", sw=1.5) + ftext(150 + j * cw + cw / 2, y + 30, v, 17)
    return svg(W, H, out)


KINDS = {"fraction_bars": fraction_bars, "fraction_circle": fraction_circle, "area_grid": area_grid, "tape": tape,
         "number_line": number_line, "ruler": ruler, "place_chart": place_chart, "base_ten": base_ten,
         "hundred_grid": hundred_grid, "area_model": area_model, "array": array_dots, "coord": coord, "shape": shape,
         "shape_row": shape_row, "cubes": cubes, "prism": prism, "composite": composite, "lineplot": lineplot,
         "table": table, "two_tables": two_tables}


def render(kind, data):
    return KINDS[kind](data)
