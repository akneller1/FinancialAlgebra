"""Grade 3 diagram kinds, added to the shared Grade 5 drawing kit (tools/grade5-authoring/figs.py).

render(kind, data) -> SVG. Every drawing is built only from `data`, which is also stored in the check file, so the
verifier can recompute answers from exactly what is drawn. Kinds from figs.py (fraction_bars, fraction_circle, tape,
ruler, shape, shape_row, lineplot, table, array) are reused unchanged; the kinds below are new for Grade 3."""
import math, os, sys
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(HERE, "..", "grade5-authoring"))
import figs as G5
from figs import svg, text, ftext, rect, line, poly, INK, FILL, PAL, esc

BLUE, ORANGE, GREEN = "#2f7fd8", "#f08c1a", "#1aa37a"


def groups(d):
    """Equal groups: g circles each holding n dots. data: groups, each, (optional) extra=[counts] for unequal groups."""
    counts = d.get("counts") or [d["each"]] * d["groups"]
    g = len(counts)
    per_row = min(g, 5)
    rows = math.ceil(g / per_row)
    R = 52
    W, H = 30 + per_row * (2 * R + 22), 24 + rows * (2 * R + 22)
    out = ""
    for k, n in enumerate(counts):
        cx = 30 + (k % per_row) * (2 * R + 22) + R - 4
        cy = 20 + (k // per_row) * (2 * R + 22) + R
        out += f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#eef5ff" stroke="{INK}" stroke-width="2.5"/>'
        cols = 3 if n > 4 else 2 if n > 1 else 1
        if n > 9:
            cols = 4
        rr = math.ceil(n / cols) if n else 0
        s = 22 if n <= 9 else 19
        for i in range(n):
            x = cx + ((i % cols) - (cols - 1) / 2) * s
            y = cy + ((i // cols) - (rr - 1) / 2) * s
            out += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{s * 0.36:.1f}" fill="{ORANGE}" stroke="{INK}" stroke-width="1.2"/>'
    return svg(W, H, out)


def array3(d):
    """Array of dots: rows x cols; optional split_col (vertical dashed line after that column) or split_row."""
    R, C = d["rows"], d["cols"]
    s = min(38, 520 / C, 260 / R)
    W, H = C * s + 60, R * s + 40
    out = ""
    sc, sr = d.get("split_col"), d.get("split_row")
    for i in range(R):
        for j in range(C):
            col = ORANGE if (sc and j >= sc) or (sr and i >= sr) else BLUE
            out += f'<circle cx="{30 + j * s + s / 2:.1f}" cy="{20 + i * s + s / 2:.1f}" r="{s * 0.34:.1f}" fill="{col}"/>'
    if sc:
        out += line(30 + sc * s, 8, 30 + sc * s, H - 8, sw=3, extra='stroke-dasharray="7 6"')
    if sr:
        out += line(18, 20 + sr * s, W - 18, 20 + sr * s, sw=3, extra='stroke-dasharray="7 6"')
    return svg(W, H, out)


def clock(d):
    """Analog clock showing h:m (hands placed exactly: hour hand at h + m/60)."""
    h, m = d["h"], d["m"]
    cx, cy, R = 130, 130, 112
    out = f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#fffdf2" stroke="{INK}" stroke-width="5"/>'
    for i in range(60):
        a = math.radians(i * 6 - 90)
        r1 = R - (14 if i % 5 == 0 else 7)
        out += line(cx + r1 * math.cos(a), cy + r1 * math.sin(a), cx + (R - 3) * math.cos(a), cy + (R - 3) * math.sin(a), sw=3 if i % 5 == 0 else 1.4)
    for k in range(1, 13):
        a = math.radians(k * 30 - 90)
        out += text(cx + (R - 32) * math.cos(a), cy + (R - 32) * math.sin(a) + 8, str(k), 22, weight="800")
    ha = math.radians((h % 12 + m / 60) * 30 - 90)
    ma = math.radians(m * 6 - 90)
    out += line(cx, cy, cx + 58 * math.cos(ha), cy + 58 * math.sin(ha), "#1d2a3a", 8, 'stroke-linecap="round"')
    out += line(cx, cy, cx + 90 * math.cos(ma), cy + 90 * math.sin(ma), BLUE, 5, 'stroke-linecap="round"')
    out += f'<circle cx="{cx}" cy="{cy}" r="7" fill="{INK}"/>'
    return svg(260, 260, out)


def beaker(d):
    """Measuring container. data: max, step (liters per tick), label_every (ticks), level (liters, a multiple of step), unit."""
    mx, st, le, lv = d["max"], d["step"], d.get("label_every", 1), d["level"]
    W, H = 300, 330
    x0, x1, yb, yt = 90, 200, 300, 40
    sc = (yb - yt) / mx
    out = rect(x0, yb - lv * sc, x1 - x0, lv * sc, "#8fc8f2", "none", 0)
    out += f'<path d="M{x0},{yt - 15} L{x0},{yb} L{x1},{yb} L{x1},{yt - 15}" fill="none" stroke="{INK}" stroke-width="4"/>'
    n = round(mx / st)
    for i in range(n + 1):
        v = i * st
        y = yb - v * sc
        big = i % le == 0
        out += line(x0, y, x0 + (26 if big else 14), y, sw=2.4 if big else 1.4)
        if big:
            out += text(x0 - 10, y + 6, f"{v:g}", 17, anchor="end", weight="700")
    out += text(x1 + 12, yt + 4, d.get("unit", "liters"), 16, anchor="start", weight="700")
    return svg(W, H, out)


def scale(d):
    """Platform scale with a straight dial strip and a pointer. data: max, step, label_every, value, unit."""
    mx, st, le, v = d["max"], d["step"], d.get("label_every", 1), d["value"]
    W, H = 660, 210
    x0, x1, y = 50, 610, 140
    sc = (x1 - x0) / mx
    out = rect(150, 22, 360, 26, "#c9d3e3", INK, 2.5, rx=6) + rect(316, 48, 28, 30, "#c9d3e3", INK, 2) + text(330, 18, d.get("object", ""), 16, weight="700")
    out += rect(30, 78, 600, 100, "#fff7d6", INK, 2.5, rx=10)
    n = round(mx / st)
    for i in range(n + 1):
        val = i * st
        X = x0 + val * sc
        big = i % le == 0
        out += line(X, y - (22 if big else 12), X, y, sw=2.4 if big else 1.4)
        if big:
            out += text(X, y + 24, f"{val:g}", 15, weight="700")
    if v:
        X = x0 + v * sc
        out += poly([(X, y - 2), (X - 9, y - 44), (X + 9, y - 44)], "#e2563b", INK, 1.5)
    out += text(W - 40, H - 10, d.get("unit", "grams"), 15, anchor="end", weight="700")
    return svg(W, H, out)


def _icon(kind, x, y, s, frac=1):
    """Picture-graph symbol of size s at (x, y) top-left; frac=1/2 draws the left half only."""
    clip = ""
    cid = f"c{int(x)}_{int(y)}"
    if frac != 1:
        clip = f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{s * float(frac):.1f}" height="{s}"/></clipPath>'
    att = f' clip-path="url(#{cid})"' if frac != 1 else ""
    cx, cy = x + s / 2, y + s / 2
    if kind == "star":
        pts = []
        for k in range(10):
            r = s / 2 if k % 2 == 0 else s / 4.6
            a = math.radians(-90 + k * 36)
            pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
        body = f'<polygon points="{" ".join(pts)}" fill="#ffc533" stroke="{INK}" stroke-width="1.5"{att}/>'
    elif kind == "apple":
        body = f'<g{att}><circle cx="{cx:.1f}" cy="{cy + 2:.1f}" r="{s * 0.42:.1f}" fill="#e2563b" stroke="{INK}" stroke-width="1.5"/><rect x="{cx - 1.5:.1f}" y="{y:.1f}" width="3" height="{s * 0.2:.1f}" fill="#6b3d1f"/></g>'
    elif kind == "book":
        body = f'<rect x="{x + 2:.1f}" y="{y + 3:.1f}" width="{s - 4:.1f}" height="{s - 6:.1f}" rx="3" fill="#2f7fd8" stroke="{INK}" stroke-width="1.5"{att}/>'
    else:  # smiley / circle
        body = f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{s * 0.44:.1f}" fill="#8fdcbf" stroke="{INK}" stroke-width="1.5"{att}/>'
    return clip + body


def picgraph(d):
    """Scaled picture graph. data: title, cats, symbols (number of symbols per category, may end in .5), key (value per symbol), icon."""
    cats, syms, key, ic = d["cats"], [F(x) for x in d["symbols"]], d["key"], d.get("icon", "star")
    s, gap = 34, 6
    mx = max(math.ceil(x) for x in syms)
    W = max(560, 190 + mx * (s + gap) + 30)
    H = 70 + len(cats) * (s + 14) + 56
    out = text(W / 2, 30, d.get("title", ""), 20, weight="800")
    for i, (c, n) in enumerate(zip(cats, syms)):
        y = 52 + i * (s + 14)
        out += rect(14, y - 4, W - 28, s + 8, "#ffffff" if i % 2 else "#f4f8fd", "#c7d3e6", 1)
        out += text(170, y + s / 2 + 6, c, 17, anchor="end", weight="700")
        whole = int(n)
        for k in range(whole):
            out += _icon(ic, 185 + k * (s + gap), y, s)
        if n - whole:
            out += _icon(ic, 185 + whole * (s + gap), y, s, n - whole)
    y = H - 34
    out += _icon(ic, W / 2 - 80, y - 4, 28) + text(W / 2 - 44, y + 17, f"= {key} {d.get('unit', '')}".strip(), 18, anchor="start", weight="800")
    return svg(W, H, out)


def bargraph(d):
    """Scaled vertical bar graph. data: title, cats, vals (multiples of scale/2), scale (value per grid line), top, ylabel."""
    cats, vals, scl, top = d["cats"], d["vals"], d["scale"], d["top"]
    W = max(560, 120 + len(cats) * 110)
    H = 380
    x0, y0, y1 = 90, 320, 60
    sc = (y0 - y1) / top
    out = text(W / 2, 32, d.get("title", ""), 20, weight="800")
    for i in range(0, top // scl + 1):
        v = i * scl
        y = y0 - v * sc
        out += line(x0, y, W - 30, y, "#c7d3e6", 1.3) + text(x0 - 10, y + 6, str(v), 15, anchor="end", weight="700")
    bw = (W - 30 - x0) / len(cats)
    for i, (c, v) in enumerate(zip(cats, vals)):
        x = x0 + i * bw + bw * 0.2
        out += rect(x, y0 - v * sc, bw * 0.6, v * sc, PAL[i % len(PAL)], INK, 1.8)
        out += text(x + bw * 0.3, y0 + 24, c, 16, weight="700")
    out += line(x0, y0, W - 30, y0, sw=2.5) + line(x0, y0, x0, y1 - 10, sw=2.5)
    if d.get("ylabel"):
        out += f'<text x="22" y="{(y0 + y1) / 2:.0f}" font-size="15" font-weight="700" fill="{INK}" text-anchor="middle" transform="rotate(-90 22 {(y0 + y1) / 2:.0f})">{esc(d["ylabel"])}</text>'
    return svg(W, H, out)


def numline(d):
    """Number line with UNREDUCED fraction labels (Grade 3). data: den, hi (whole number), lo (default 0),
    labels: 'all' | 'wholes' | 'none' | list of tick indices to label, points [{"n": numerator, "label": "A"}], jumps (count of 1/den jumps from 0),
    whole_as: 'num' (1, 2) or 'frac' (4/4, 8/4)."""
    den, hi, lo = int(d["den"]), int(d["hi"]), int(d.get("lo", 0))
    W, H = d.get("width", 680), 150 if not d.get("jumps") else 190
    x0, x1, y = 50, W - 50, H - 64
    n = (hi - lo) * den
    X = lambda k: x0 + (k - lo * den) * (x1 - x0) / n
    out = line(x0 - 20, y, x1 + 20, y, sw=2.5)
    out += poly([(x1 + 24, y), (x1 + 12, y - 7), (x1 + 12, y + 7)], INK, INK, 1) + poly([(x0 - 24, y), (x0 - 12, y - 7), (x0 - 12, y + 7)], INK, INK, 1)
    labs = d.get("labels", "wholes")
    for k in range(lo * den, hi * den + 1):
        big = k % den == 0
        out += line(X(k), y - (14 if big else 9), X(k), y + (14 if big else 9), sw=2.6 if big else 1.8)
        show = labs == "all" or (labs == "wholes" and big) or (isinstance(labs, list) and k in labs)
        if show:
            if big and d.get("whole_as", "num") == "num":
                out += text(X(k), y + 40, str(k // den), 18, weight="700")
            else:
                out += ftext(X(k), y + 40, f"{k}/{den}", 18)
    jumps = d.get("jumps", 0)
    for j in range(jumps):
        a, b = X(lo * den + j), X(lo * den + j + 1)
        out += f'<path d="M{a:.1f},{y - 5} Q{(a + b) / 2:.1f},{y - 58} {b:.1f},{y - 5}" fill="none" stroke="{ORANGE}" stroke-width="3"/>'
    for p in d.get("points", []):
        col = p.get("color", "#d63c7a")
        out += f'<circle cx="{X(p["n"]):.1f}" cy="{y}" r="8" fill="{col}" stroke="#fff" stroke-width="2"/>'
        if p.get("label"):
            out += text(X(p["n"]), y - (66 if jumps else 20), p["label"], 19, weight="800", fill=col)
    return svg(W, H, out)


def wholeline(d):
    """Whole-number line from lo to hi with tick every `step`, labels every `label_every` ticks, optional point (value, label)."""
    lo, hi, st = d["lo"], d["hi"], d["step"]
    W, H = d.get("width", 680), 140
    x0, x1, y = 50, W - 50, 80
    X = lambda v: x0 + (v - lo) * (x1 - x0) / (hi - lo)
    out = line(x0 - 16, y, x1 + 16, y, sw=2.5)
    le = d.get("label_every", 1)
    for i, v in enumerate(range(lo, hi + 1, st)):
        big = i % le == 0
        out += line(X(v), y - (13 if big else 8), X(v), y + (13 if big else 8), sw=2.4 if big else 1.6)
        if big:
            out += text(X(v), y + 38, f"{v:,}", 16, weight="700")
    for p in d.get("points", []):
        out += f'<circle cx="{X(p["v"]):.1f}" cy="{y}" r="8" fill="#d63c7a" stroke="#fff" stroke-width="2"/>'
        out += text(X(p["v"]), y - 20, p.get("label", ""), 18, weight="800", fill="#d63c7a")
    return svg(W, H, out)


def timeline(d):
    """Open number line for elapsed time. data: ticks [[minute, label]], jumps [[a, b, label]] (minutes from a reference)."""
    ticks, jumps = d["ticks"], d.get("jumps", [])
    lo, hi = min(t[0] for t in ticks), max(t[0] for t in ticks)
    W, H = d.get("width", 680), 180
    x0, x1, y = 50, W - 50, 120
    X = lambda v: x0 + (v - lo) * (x1 - x0) / max(1, hi - lo)
    out = line(x0 - 16, y, x1 + 16, y, sw=2.5)
    for v, lab in ticks:
        out += line(X(v), y - 12, X(v), y + 12, sw=2.4) + text(X(v), y + 38, lab, 17, weight="700")
    for a, b, lab in jumps:
        A, B = X(a), X(b)
        out += f'<path d="M{A:.1f},{y - 5} Q{(A + B) / 2:.1f},{y - 70} {B:.1f},{y - 5}" fill="none" stroke="{ORANGE}" stroke-width="3"/>'
        out += text((A + B) / 2, y - 46, lab, 16, weight="800", fill="#b35d00")
    return svg(W, H, out)


def grid(d):
    """Unit-square grid figure. data: cells [[r, c], ...] shaded cells (a rectilinear figure or a rectangle), rows, cols,
    grid: show the full background grid; label: unit caption; tiled: if False, draw only the outline of the figure
    with tick marks on the sides (side lengths shown as unit marks)."""
    R, C = d["rows"], d["cols"]
    s = min(40, 520 / C, 270 / R)
    W, H = C * s + 60, R * s + (60 if d.get("label") else 40)
    x0, y0 = 30, 20
    cells = {tuple(c) for c in d["cells"]}
    out = ""
    if d.get("grid", True):
        for i in range(R):
            for j in range(C):
                out += rect(x0 + j * s, y0 + i * s, s, s, "#ffffff", "#c7d3e6", 1)
    col = FILL[d.get("color", "orange")]
    for (i, j) in cells:
        out += rect(x0 + j * s, y0 + i * s, s, s, col, INK if d.get("tiled", True) else col, 1.4 if d.get("tiled", True) else 0)
    # outline of the figure
    for (i, j) in cells:
        for (di, dj, xa, ya, xb, yb) in ((-1, 0, 0, 0, 1, 0), (1, 0, 0, 1, 1, 1), (0, -1, 0, 0, 0, 1), (0, 1, 1, 0, 1, 1)):
            if (i + di, j + dj) not in cells:
                out += line(x0 + (j + xa) * s, y0 + (i + ya) * s, x0 + (j + xb) * s, y0 + (i + yb) * s, INK, 3.2)
    if d.get("label"):
        out += rect(W - 150, H - 32, 18, 18, col, INK, 1.4) + text(W - 126, H - 17, d["label"], 14, anchor="start", weight="700")
    return svg(W, H, out)


def rects(d):
    """Rectangle(s) with side-length labels, drawn to scale (no unit squares). data: items [{w, h, wt, ht, split: k (column), splitw: [wa, wb]}]
    or a single rectangle via w, h, wt, ht. Optional 'grid': draw unit squares inside."""
    items = d.get("items") or [{k: d[k] for k in ("w", "h", "wt", "ht", "split", "wta", "wtb", "grid", "label") if k in d}]
    maxw = max(it["w"] for it in items)
    maxh = max(it["h"] for it in items)
    s = min(46, (560 / len(items)) / (maxw + 1.5), 230 / maxh)
    lm = 30 + 10 * max(len(str(it.get("ht", ""))) for it in items)
    W = int(sum(it["w"] * s + 110 for it in items) + lm)
    H = int(maxh * s + 90)
    out, x = "", lm
    for k, it in enumerate(items):
        w, h = it["w"] * s, it["h"] * s
        y = 30
        if it.get("grid"):
            for i in range(it["h"]):
                for j in range(it["w"]):
                    out += rect(x + j * s, y + i * s, s, s, "#fff3e2", "#c9a27a", 1)
            out += rect(x, y, w, h, "none", INK, 3)
        else:
            out += rect(x, y, w, h, [FILL["blue"], FILL["green"], FILL["pink"]][k % 3], INK, 3)
        if it.get("split"):
            xs = x + it["split"] * s
            out += rect(xs, y, w - it["split"] * s, h, FILL["orange"], INK, 3) + line(xs, y, xs, y + h, INK, 3, 'stroke-dasharray="8 5"')
            out += text(x + it["split"] * s / 2, y + h + 26, it["wta"], 17, weight="800") + text(xs + (w - it["split"] * s) / 2, y + h + 26, it["wtb"], 17, weight="800")
        elif it.get("wt"):
            out += text(x + w / 2, y + h + 26, it["wt"], 17, weight="800")
        if it.get("ht"):
            out += text(x - 12, y + h / 2 + 6, it["ht"], 17, anchor="end", weight="800")
        if it.get("label"):
            out += text(x + w / 2, y + h / 2 + 8, it["label"], 22, weight="800")
        x += w + 110
    return svg(W, H, out)


def partition(d):
    """A shape cut into parts. data: shape ('rect'|'circle'|'square'|'hexagon'|'triangle'), cuts:
       rect/square: 'v' with widths [..] (column widths in units), or 'grid' rows x cols, or 'diag2'/'diag4';
       circle: n (equal sectors) or angles [..] in degrees for unequal parts; hexagon: 'tri6'|'rhomb3'|'trap2';
       triangle: 'mid2' (median) | 'off2' (cut not through the midpoint).
       shade: indices of shaded parts."""
    sh, sd = d["shape"], set(d.get("shade", []))
    col = FILL[d.get("color", "green")]
    fill = lambda k: col if k in sd else "#ffffff"
    W, H = 360, 260
    out = ""
    if sh in ("rect", "square"):
        x0, y0 = 50, 30
        if d["cuts"] == "v":
            ws = d["widths"]
            tw = sum(ws)
            Wd, Hd = (260, 200) if sh == "rect" else (200, 200)
            x = x0
            for k, wv in enumerate(ws):
                w = Wd * wv / tw
                out += rect(x, y0, w, Hd, fill(k), INK, 3)
                x += w
        elif d["cuts"] == "grid":
            r, c = d["rows"], d["cols"]
            Wd, Hd = (260, 200) if sh == "rect" else (200, 200)
            for i in range(r):
                for j in range(c):
                    out += rect(x0 + j * Wd / c, y0 + i * Hd / r, Wd / c, Hd / r, fill(i * c + j), INK, 3)
        elif d["cuts"] in ("diag2", "diag4"):
            Wd, Hd = (260, 200) if sh == "rect" else (200, 200)
            A, B, C_, D = (x0, y0), (x0 + Wd, y0), (x0 + Wd, y0 + Hd), (x0, y0 + Hd)
            if d["cuts"] == "diag2":
                out += poly([A, B, C_], fill(0), INK, 3) + poly([A, C_, D], fill(1), INK, 3)
            else:
                M = (x0 + Wd / 2, y0 + Hd / 2)
                for k, (p, q) in enumerate(((A, B), (B, C_), (C_, D), (D, A))):
                    out += poly([p, q, M], fill(k), INK, 3)
    elif sh == "circle":
        cx, cy, R = 180, 130, 105
        angs = d.get("angles") or [360 / d["n"]] * d["n"]
        a0 = -90
        for k, a in enumerate(angs):
            a1 = a0 + a
            p0 = (cx + R * math.cos(math.radians(a0)), cy + R * math.sin(math.radians(a0)))
            p1 = (cx + R * math.cos(math.radians(a1)), cy + R * math.sin(math.radians(a1)))
            large = 1 if a > 180 else 0
            out += f'<path d="M{cx},{cy} L{p0[0]:.1f},{p0[1]:.1f} A{R},{R} 0 {large} 1 {p1[0]:.1f},{p1[1]:.1f} Z" fill="{fill(k)}" stroke="{INK}" stroke-width="3"/>'
            a0 = a1
    elif sh == "hexagon":
        cx, cy, R = 180, 130, 112
        P = [(cx + R * math.cos(math.radians(60 * k)), cy + R * math.sin(math.radians(60 * k))) for k in range(6)]
        C0 = (cx, cy)
        if d["cuts"] == "tri6":
            for k in range(6):
                out += poly([C0, P[k], P[(k + 1) % 6]], fill(k), INK, 3)
        elif d["cuts"] == "rhomb3":
            for k in range(3):
                out += poly([C0, P[2 * k], P[2 * k + 1], P[(2 * k + 2) % 6]], fill(k), INK, 3)
        elif d["cuts"] == "trap2":
            out += poly([P[0], P[1], P[2], P[3]], fill(0), INK, 3) + poly([P[3], P[4], P[5], P[0]], fill(1), INK, 3)
    elif sh == "triangle":
        A, B, C_ = (40, 230), (320, 230), (180, 30)
        M = ((A[0] + B[0]) / 2, 230) if d["cuts"] == "mid2" else (A[0] + (B[0] - A[0]) * 0.32, 230)
        out += poly([A, M, C_], fill(0), INK, 3) + poly([M, B, C_], fill(1), INK, 3)
    return svg(W, H, out)


def mtable(d):
    """Addition or multiplication table (0/1..n). data: op ('×' or '+'), lo, n, highlight: [[r, c], ...], rows_hl, cols_hl, hide: [[r,c]] -> '?'"""
    op, lo, n = d["op"], d.get("lo", 1), d["n"]
    k = n - lo + 1
    s = min(46, 560 / (k + 1))
    W, H = int((k + 1) * s + 40), int((k + 1) * s + 40)
    hl = {tuple(x) for x in d.get("highlight", [])}
    hide = {tuple(x) for x in d.get("hide", [])}
    out = ""
    for i in range(k + 1):
        for j in range(k + 1):
            x, y = 20 + j * s, 20 + i * s
            if i == 0 and j == 0:
                out += rect(x, y, s, s, "#2b4f8c", INK, 1.2) + text(x + s / 2, y + s * 0.68, op, s * 0.5, weight="800", fill="#fff")
            elif i == 0 or j == 0:
                v = lo + (j if i == 0 else i) - 1
                out += rect(x, y, s, s, "#dfeafb", INK, 1.2) + text(x + s / 2, y + s * 0.66, str(v), s * 0.42, weight="800")
            else:
                r, c = lo + i - 1, lo + j - 1
                v = r * c if op == "×" else r + c
                on = (r, c) in hl or r in d.get("rows_hl", []) or c in d.get("cols_hl", [])
                out += rect(x, y, s, s, FILL["yellow"] if on else "#fff", INK, 1.2)
                out += text(x + s / 2, y + s * 0.66, "?" if (r, c) in hide else str(v), s * 0.4, weight="700" if on else "500")
    return svg(W, H, out)


def strips(d):
    """Fraction strips for the SAME whole, labels drawn as unit fractions in each part (fraction wall). data: dens [..], shade [[k], ...]."""
    dens, shade = d["dens"], d.get("shade", [0] * len(d["dens"]))
    W = d.get("width", 640)
    bw = W - 80
    H = 20 + len(dens) * 58
    out = ""
    for i, n in enumerate(dens):
        y = 14 + i * 58
        for j in range(n):
            out += rect(40 + j * bw / n, y, bw / n, 46, FILL[["blue", "orange", "green", "pink", "purple"][i % 5]] if j < shade[i] else "#ffffff", INK, 2)
            if d.get("unit_labels", True) and n > 1:
                out += ftext(40 + j * bw / n + bw / n / 2, y + 30, f"1/{n}", 15 if n <= 8 else 12)
            elif n == 1:
                out += text(40 + bw / 2, y + 30, "1", 18, weight="800")
    return svg(W, H, out)


def circles2(d):
    """Two same-size circles side by side: left cut into a[0] equal parts with a[1] shaded, right cut into b[0] with b[1] shaded."""
    out = ""
    for k, (n, sh) in enumerate((d["a"], d["b"])):
        cx, cy, R = 115 + k * 230, 110, 92
        for j in range(n):
            a0, a1 = -math.pi / 2 + 2 * math.pi * j / n, -math.pi / 2 + 2 * math.pi * (j + 1) / n
            x0, y0, x1, y1 = cx + R * math.cos(a0), cy + R * math.sin(a0), cx + R * math.cos(a1), cy + R * math.sin(a1)
            fill = FILL["orange" if k == 0 else "blue"] if j < sh else "#ffffff"
            out += f'<path d="M{cx},{cy} L{x0:.1f},{y0:.1f} A{R},{R} 0 {1 if a1 - a0 > math.pi else 0} 1 {x1:.1f},{y1:.1f} Z" fill="{fill}" stroke="{INK}" stroke-width="2.5"/>'
    return svg(460, 220, out)


def ruler3(d):
    """Inch ruler like figs.ruler with an adjustable drawing width (for cheat sheets): length, den, start, end, object, width."""
    L, den = int(d["length"]), int(d.get("den", 4))
    s0, e = F(G5.PF(d.get("start", "0"))), F(G5.PF(d["end"]))
    W, H = d.get("width", 680), 170
    x0, sc = 40, (W - 80) / L
    X = lambda v: x0 + float(v) * sc
    out = rect(X(s0), 26, X(e) - X(s0), 30, FILL["orange"], sw=2, rx=6)
    if d.get("object"):
        out += text((X(s0) + X(e)) / 2, 47, d["object"], 15, weight="700")
    out += rect(x0 - 12, 70, W - 56, 74, "#fff7d6", sw=2, rx=6)
    for i in range(L * den + 1):
        v = F(i, den)
        hgt = 34 if v.denominator == 1 else 24 if v.denominator == 2 else 17
        out += line(X(v), 70, X(v), 70 + hgt, sw=2 if v.denominator == 1 else 1.4)
        if v.denominator == 1:
            out += text(X(v), 128, str(v.numerator), 18)
    out += text(W - 46, 162, "inches", 14, anchor="end", weight="600")
    return svg(W, H, out)


KINDS = dict(G5.KINDS)
KINDS.update({"groups": groups, "array3": array3, "clock": clock, "beaker": beaker, "scale": scale, "picgraph": picgraph,
              "bargraph": bargraph, "numline": numline, "wholeline": wholeline, "timeline": timeline, "grid": grid, "rects": rects,
              "partition": partition, "mtable": mtable, "strips": strips, "ruler3": ruler3, "circles2": circles2})


def render(kind, data):
    return KINDS[kind](data)
