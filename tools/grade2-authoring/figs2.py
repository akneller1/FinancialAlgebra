"""Grade 2 diagram kinds, added to the Grade 3 kit (tools/grade3-authoring/figs3.py, which extends the Grade 5 figs.py).

render(kind, data) -> SVG. Every drawing is built only from `data`, which is also stored in the check file, so the
verifier can recompute answers from exactly what is drawn. Reused unchanged: base_ten, shape_row, shape, lineplot, table,
tape (Grade 5); clock, array3, picgraph, bargraph, wholeline, grid, partition, groups (Grade 3). New kinds are below."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(HERE, "..", "grade3-authoring"))
sys.path.append(os.path.join(HERE, "..", "grade5-authoring"))
import figs3 as G3
from figs import svg, text, ftext, rect, line, poly, INK, FILL, PAL, esc

BLUE, ORANGE, GREEN, PINK = "#2f7fd8", "#f08c1a", "#1aa37a", "#d63c7a"


def _arrowhead(x, y, dx, dy, col, s=9):
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    return poly([(x, y), (x - ux * s - uy * s * 0.6, y - uy * s + ux * s * 0.6), (x - ux * s + uy * s * 0.6, y - uy * s - ux * s * 0.6)], col, col, 1)


def jline(d):
    """Whole-number line lo..hi, tick every `step`, label every `label_every` ticks (or labels: list of values),
    jumps [[from, to, label]] drawn as arrows above the line, points [{"v", "label"}]."""
    lo, hi, st = d["lo"], d["hi"], d.get("step", 1)
    W = d.get("width", 700)
    jumps = d.get("jumps", [])
    H = 150 if not jumps else 200
    x0, x1, y = 40, W - 40, H - 62
    X = lambda v: x0 + (v - lo) * (x1 - x0) / (hi - lo)
    out = line(x0 - 18, y, x1 + 18, y, sw=2.5)
    out += poly([(x1 + 22, y), (x1 + 10, y - 7), (x1 + 10, y + 7)], INK, INK, 1) + poly([(x0 - 22, y), (x0 - 10, y - 7), (x0 - 10, y + 7)], INK, INK, 1)
    le, labs = d.get("label_every", 1), d.get("labels")
    for i, v in enumerate(range(lo, hi + 1, st)):
        big = (v in labs) if labs is not None else i % le == 0
        out += line(X(v), y - (13 if big else 8), X(v), y + (13 if big else 8), sw=2.4 if big else 1.6)
        if big:
            out += text(X(v), y + 36, str(v), 16 if hi < 1000 else 14, weight="700")
    for k, (a, b, lab) in enumerate(jumps):
        A, B = X(a), X(b)
        hgt = 40 + 26 * min(1, abs(B - A) / 160)
        col = ORANGE if b >= a else PINK
        out += f'<path d="M{A:.1f},{y - 6} Q{(A + B) / 2:.1f},{y - 6 - 2 * hgt} {B:.1f},{y - 6}" fill="none" stroke="{col}" stroke-width="3"/>'
        out += _arrowhead(B, y - 6, (B - A) * 0.25, 2 * hgt * 0.9, col)
        if lab:
            out += text((A + B) / 2, y - 12 - hgt, lab, 16, weight="800", fill="#9a4a00" if b >= a else "#a3245a")
    for p in d.get("points", []):
        out += f'<circle cx="{X(p["v"]):.1f}" cy="{y}" r="8" fill="{PINK}" stroke="#fff" stroke-width="2"/>'
        if p.get("label"):
            out += text(X(p["v"]), y - 20 - (0 if not jumps else 0), p["label"], 18, weight="800", fill=PINK)
    if d.get("unit"):
        out += text(W - 40, H - 6, d["unit"], 14, anchor="end", weight="600")
    return svg(W, H, out)


COIN = {"penny": (1, 30, "#c77b3a", "#8a4d1d"), "nickel": (5, 36, "#c9ced6", "#6d7480"), "dime": (10, 27, "#d8dde4", "#6d7480"),
        "quarter": (25, 40, "#cfd5dd", "#6d7480")}


def _coin(cx, cy, kind, show):
    v, r, f, s = COIN[kind]
    out = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{f}" stroke="{s}" stroke-width="3"/>'
    out += f'<circle cx="{cx}" cy="{cy}" r="{r - 5}" fill="none" stroke="{s}" stroke-width="1.2"/>'
    if show:
        out += text(cx, cy + 6, f"{v}¢", 16 if r > 30 else 14, weight="800")
    else:
        out += text(cx, cy + 5, kind.upper(), 10 if r > 30 else 8, weight="800")
    return out


def _bill(x, y, v):
    out = rect(x, y, 120, 58, "#cfe8c6", "#2f6b2a", 2.5, rx=4) + rect(x + 6, y + 6, 108, 46, "none", "#2f6b2a", 1, rx=3)
    out += f'<ellipse cx="{x + 60}" cy="{y + 29}" rx="17" ry="20" fill="#e9f5e4" stroke="#2f6b2a" stroke-width="1.4"/>'
    out += text(x + 20, y + 24, str(v), 15, weight="800", fill="#1f4d1b") + text(x + 100, y + 48, str(v), 15, weight="800", fill="#1f4d1b")
    out += text(x + 60, y + 35, f"${v}", 16, weight="800", fill="#1f4d1b")
    return out


def money(d):
    """Bills and coins. data: bills [1, 5, ...] (dollar values), coins ["quarter", "dime", ...], show_value (label coins with ¢)."""
    bills, coins, show = d.get("bills", []), d.get("coins", []), d.get("show_value", True)
    out, x = "", 20
    per = 4
    for k, v in enumerate(bills):
        out += _bill(20 + (k % per) * 132, 18 + (k // per) * 70, v)
    yb = 18 + math.ceil(len(bills) / per) * 70 if bills else 10
    x = 20
    rowy = yb + 46
    xmax = 20 + min(len(bills), per) * 132
    for kind in coins:
        r = COIN[kind][1]
        if x + 2 * r > 640:
            x, rowy = 20, rowy + 92
        out += _coin(x + r, rowy, kind, show)
        x += 2 * r + 14
        xmax = max(xmax, x)
    W = max(260, xmax + 10)
    H = rowy + 50 if coins else yb + 10
    return svg(W, H, out)


def ruler2(d):
    """Ruler in whole units (inches or centimeters), length units long; objects [{start, end, label}] drawn above it
    (start may be other than 0 to practice measuring from a different mark)."""
    L, unit = d["length"], d.get("unit", "inches")
    W = d.get("width", 700)
    objs = d.get("objects", [])
    top = 20 + 44 * len(objs)
    H = top + 100
    x0 = 40
    sc = (W - 80) / L
    X = lambda v: x0 + v * sc
    out = ""
    cols = [FILL["orange"], FILL["blue"], FILL["green"]]
    for k, o in enumerate(objs):
        y = 18 + k * 44
        out += rect(X(o["start"]), y, X(o["end"]) - X(o["start"]), 30, cols[k % 3], sw=2, rx=6)
        if o.get("label"):
            out += text((X(o["start"]) + X(o["end"])) / 2, y + 21, o["label"], 15, weight="700")
        out += line(X(o["start"]), y + 30, X(o["start"]), top + 4, "#8a97a8", 1.2, 'stroke-dasharray="4 4"')
        out += line(X(o["end"]), y + 30, X(o["end"]), top + 4, "#8a97a8", 1.2, 'stroke-dasharray="4 4"')
    out += rect(x0 - 14, top + 4, W - 52, 70, "#fff7d6", sw=2, rx=6)
    half = unit == "inches" and d.get("halves", False)
    for i in range(L + 1):
        out += line(X(i), top + 4, X(i), top + 38, sw=2)
        out += text(X(i), top + 60, str(i), 16 if L <= 20 else 13, weight="700")
        if half and i < L:
            out += line(X(i + 0.5), top + 4, X(i + 0.5), top + 22, sw=1.4)
    if unit == "centimeters" and L <= 15:
        for i in range(L * 2):
            if i % 2:
                out += line(X(i / 2), top + 4, X(i / 2), top + 18, sw=1.2)
    out += text(W - 44, H - 8, unit, 13, anchor="end", weight="600")
    return svg(W, H, out)


def counters(d):
    """n counters. layout 'pairs' (two rows, partners lined up), 'scatter' (fixed rows of 5), 'frames' (ten frames)."""
    n, lay = d["n"], d.get("layout", "scatter")
    out = ""
    if lay == "pairs":
        cols = math.ceil(n / 2)
        W, H = 60 + cols * 44, 130
        for i in range(n):
            c, r_ = i // 2, i % 2
            out += f'<circle cx="{40 + c * 44}" cy="{42 + r_ * 46}" r="16" fill="{BLUE if r_ == 0 else ORANGE}" stroke="{INK}" stroke-width="1.6"/>'
        return svg(W, H, out)
    if lay == "frames":
        k = math.ceil(n / 10) or 1
        W, H = 30 + k * 250, 140
        for f in range(k):
            for i in range(10):
                x, y = 20 + f * 250 + (i % 5) * 44, 20 + (i // 5) * 48
                out += rect(x, y, 44, 48, "#fff", sw=2)
                if f * 10 + i < n:
                    out += f'<circle cx="{x + 22}" cy="{y + 24}" r="15" fill="{GREEN}" stroke="{INK}" stroke-width="1.5"/>'
        return svg(W, H, out)
    rows = math.ceil(n / 5)
    W, H = 300, 30 + rows * 46
    off = [0, 9, -6, 4, -3]
    for i in range(n):
        r_, c = divmod(i, 5)
        out += f'<circle cx="{40 + c * 52 + off[(i * 3) % 5]}" cy="{30 + r_ * 46 + off[(i * 2) % 5] / 2}" r="15" fill="{PINK}" stroke="{INK}" stroke-width="1.5"/>'
    return svg(W, H, out)


def _solid(kind, cx, cy, s):
    """A small 3-D solid centered near (cx, cy)."""
    dx, dy = s * 0.35, s * 0.25
    if kind == "cube":
        x, y = cx - s / 2 - dx / 2, cy - s / 2 + dy / 2
        return (poly([(x, y), (x + dx, y - dy), (x + s + dx, y - dy), (x + s, y)], "#bcd8f7", INK, 2)
                + poly([(x + s, y), (x + s + dx, y - dy), (x + s + dx, y + s - dy), (x + s, y + s)], "#7fa9d8", INK, 2) + rect(x, y, s, s, "#9cc4ee", INK, 2))
    if kind == "prism":   # rectangular prism that is not a cube
        w, h = s * 1.5, s * 0.7
        x, y = cx - w / 2 - dx / 2, cy - h / 2 + dy / 2
        return (poly([(x, y), (x + dx, y - dy), (x + w + dx, y - dy), (x + w, y)], "#ffd9a8", INK, 2)
                + poly([(x + w, y), (x + w + dx, y - dy), (x + w + dx, y + h - dy), (x + w, y + h)], "#e8a95c", INK, 2) + rect(x, y, w, h, "#ffc27a", INK, 2))
    if kind == "cylinder":
        w, h = s * 0.9, s * 1.1
        return (rect(cx - w / 2, cy - h / 2, w, h, "#b8e6d4", "none", 0) + line(cx - w / 2, cy - h / 2, cx - w / 2, cy + h / 2, INK, 2)
                + line(cx + w / 2, cy - h / 2, cx + w / 2, cy + h / 2, INK, 2)
                + f'<path d="M{cx - w / 2},{cy + h / 2} A{w / 2},{s * 0.18} 0 0 0 {cx + w / 2},{cy + h / 2}" fill="#b8e6d4" stroke="{INK}" stroke-width="2"/>'
                + f'<ellipse cx="{cx}" cy="{cy - h / 2}" rx="{w / 2}" ry="{s * 0.18}" fill="#8fdcbf" stroke="{INK}" stroke-width="2"/>')
    if kind == "cone":
        w, h = s, s * 1.15
        return (poly([(cx, cy - h / 2), (cx - w / 2, cy + h / 2), (cx + w / 2, cy + h / 2)], "#f5c2d6", "none", 0)
                + f'<ellipse cx="{cx}" cy="{cy + h / 2}" rx="{w / 2}" ry="{s * 0.16}" fill="#f5a3c4" stroke="{INK}" stroke-width="2"/>'
                + line(cx, cy - h / 2, cx - w / 2, cy + h / 2, INK, 2) + line(cx, cy - h / 2, cx + w / 2, cy + h / 2, INK, 2))
    if kind == "sphere":
        return (f'<circle cx="{cx}" cy="{cy}" r="{s * 0.55}" fill="#d9c8f5" stroke="{INK}" stroke-width="2"/>'
                + f'<ellipse cx="{cx}" cy="{cy}" rx="{s * 0.55}" ry="{s * 0.16}" fill="none" stroke="{INK}" stroke-width="1.2" stroke-dasharray="4 3"/>')
    if kind == "pyramid":
        w = s * 1.1
        A, B, C, T = (cx - w / 2, cy + s * 0.45), (cx + w / 2 - dx, cy + s * 0.45), (cx + w / 2, cy + s * 0.2), (cx, cy - s * 0.6)
        return poly([A, B, T], "#ffe08a", INK, 2) + poly([B, C, T], "#e6c25c", INK, 2)
    raise ValueError(kind)


def solids(d):
    """Row of labeled solids. data: items [{"kind": "cube"|"prism"|"cylinder"|"cone"|"sphere"|"pyramid", "label": "A"}]."""
    items = d["items"]
    cw = 150
    W, H = cw * len(items) + 20, 190
    out = ""
    for k, it in enumerate(items):
        cx = 10 + k * cw + cw / 2
        out += _solid(it["kind"], cx, 90, 70)
        out += text(cx, 178, it.get("label", ""), 20, weight="800")
    return svg(W, H, out)


def bars(d):
    """Bar (tape) model. rows: [{"label": "Mia", "parts": [[value, "text"], ...]}] drawn to scale on one axis;
    brace: {"row": i, "from": v0, "to": v1, "text": "?"} drawn above row i (or below the last row when row == -1)."""
    rows = d["rows"]
    mx = max(sum(p[0] for p in r["parts"]) for r in rows)
    W = d.get("width", 640)
    lm = 20 + 11 * max(len(r.get("label", "")) for r in rows) if any(r.get("label") for r in rows) else 30
    bw = W - lm - 30
    sc = bw / mx
    top = 50
    H = top + len(rows) * 64 + 40
    out = ""
    cols = [FILL["blue"], FILL["orange"], FILL["green"], FILL["pink"]]
    for i, r in enumerate(rows):
        y = top + i * 64
        if r.get("label"):
            out += text(lm - 10, y + 30, r["label"], 16, anchor="end", weight="700")
        x = lm
        for k, (v, t) in enumerate(r["parts"]):
            out += rect(x, y, v * sc, 46, cols[(i + k) % 4] if t != "?" else "#ffffff", sw=2)
            out += ftext(x + v * sc / 2, y + 30, t, 17)
            x += v * sc
    for b in d.get("braces", []):
        i = b["row"]
        a, z = lm + b["from"] * sc, lm + b["to"] * sc
        if i >= 0:
            y = top + i * 64 - 8
            out += line(a, y, z, y, sw=1.8) + line(a, y, a, y + 8, sw=1.8) + line(z, y, z, y + 8, sw=1.8)
            out += ftext((a + z) / 2, y - 8, b["text"], 17)
        else:
            y = top + len(rows) * 64 - 8
            out += line(a, y, z, y, sw=1.8) + line(a, y, a, y - 8, sw=1.8) + line(z, y, z, y - 8, sw=1.8)
            out += ftext((a + z) / 2, y + 24, b["text"], 17)
    return svg(W, H, out)


def digital(d):
    """Digital clock face. data: h, m, ampm ('a.m.'|'p.m.'|'')."""
    out = rect(20, 20, 300, 110, "#1d2a3a", INK, 3, rx=16) + rect(36, 34, 268, 82, "#0e1620", "#0e1620", 1, rx=8)
    out += text(170 - (18 if d.get("ampm") else 0), 96, f"{d['h']}:{d['m']:02d}", 54, weight="800", fill="#7dffb2")
    if d.get("ampm"):
        out += text(282, 104, d["ampm"], 16, anchor="end", weight="800", fill="#7dffb2")
    return svg(340, 150, out)


def tally(d):
    """Tally chart. data: title, cats, counts. Each group of five is four marks with a slash."""
    cats, counts = d["cats"], d["counts"]
    W = 520
    H = 70 + 52 * len(cats)
    out = text(W / 2, 30, d.get("title", ""), 19, weight="800")
    for i, (c, n) in enumerate(zip(cats, counts)):
        y = 48 + i * 52
        out += rect(20, y, 180, 52, "#dfeafb", sw=1.5) + rect(200, y, 300, 52, "#fff", sw=1.5)
        out += text(110, y + 32, c, 17, weight="700")
        x = 216
        for g in range(math.ceil(n / 5)):
            k = min(5, n - 5 * g)
            for j in range(min(k, 4)):
                out += line(x + j * 10, y + 12, x + j * 10, y + 42, sw=2.6)
            if k == 5:
                out += line(x - 6, y + 36, x + 36, y + 16, sw=2.6)
            x += 58
    return svg(W, H, out)


def chart(d):
    """Part of a counting chart: rows of numbers (start, per_row, rows); hide: values shown as '?'; blank: values left empty;
    shade: values shaded."""
    s0, pr, rows = d["start"], d.get("per_row", 10), d["rows"]
    hide, blank, shade = set(d.get("hide", [])), set(d.get("blank", [])), set(d.get("shade", []))
    cw = 58 if s0 + pr * rows <= 1000 else 64
    W, H = 30 + pr * cw, 30 + rows * 44
    out = ""
    for i in range(rows):
        for j in range(pr):
            v = s0 + i * pr + j
            x, y = 15 + j * cw, 15 + i * 44
            out += rect(x, y, cw, 44, FILL["yellow"] if v in shade else "#fff", sw=1.4)
            t = "?" if v in hide else ("" if v in blank else str(v))
            out += text(x + cw / 2, y + 29, t, 16, weight="800" if v in hide else "600", fill=PINK if v in hide else INK)
    return svg(W, H, out)


def blocks(d):
    """Base-ten blocks with optional labels: hundreds flats, tens rods, ones cubes (same as figs.base_ten but sized for up to
    9 flats in two rows). data: h, t, o."""
    h, t, o = d.get("h", 0), d.get("t", 0), d.get("o", 0)
    s = 7.5
    out = ""
    x, y = 16, 16
    per = 5
    for k in range(h):
        xx, yy = 16 + (k % per) * (10 * s + 12), 16 + (k // per) * (10 * s + 12)
        for i in range(10):
            for j in range(10):
                out += rect(xx + j * s, yy + i * s, s, s, FILL["blue"], sw=0.6)
        out += rect(xx, yy, 10 * s, 10 * s, "none", sw=1.8)
    fw = 16 + min(h, per) * (10 * s + 12) if h else 16
    hh = 16 + math.ceil(h / per) * (10 * s + 12) if h else 16
    x = fw + (10 if h else 0)
    for k in range(t):
        for i in range(10):
            out += rect(x, 16 + i * s, s, s, FILL["green"], sw=0.6)
        out += rect(x, 16, s, 10 * s, "none", sw=1.6)
        x += s + 7
    x += 8
    for k in range(o):
        out += rect(x + (k % 3) * (s + 5), 16 + (k // 3) * (s + 5), s, s, FILL["orange"], sw=1.1)
    W = max(x + 3 * (s + 5) + 16, 220)
    H = max(hh, 16 + 10 * s + 16)
    return svg(W, H, out)


def pv_chart(d):
    """Place-value chart: hundreds, tens, ones with digits (or '?' or '')."""
    cols = ["hundreds", "tens", "ones"]
    out = ""
    for i, p in enumerate(cols):
        x = 20 + i * 120
        out += rect(x, 16, 120, 40, "#e6f0fc", sw=1.5) + text(x + 60, 42, p, 16, weight="800")
        out += rect(x, 56, 120, 62, "#fff", sw=1.5) + text(x + 60, 100, str(d.get(p, "")), 32, weight="800", fill=PINK if d.get(p) == "?" else INK)
    return svg(400, 136, out)


def draw_shape(d):
    """Polygon drawn on a dot grid (for 'which shape matches the description' and shape naming). data: pts (grid units), dots."""
    pts = d["pts"]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    gw, gh = max(xs) + 1, max(ys) + 1
    s = min(46, 400 / max(gw, 1), 240 / max(gh, 1))
    W, H = gw * s + 40, gh * s + 40
    out = ""
    if d.get("dots", True):
        for i in range(int(gw) + 1):
            for j in range(int(gh) + 1):
                out += f'<circle cx="{20 + i * s:.1f}" cy="{20 + j * s:.1f}" r="2.6" fill="#9aa8bb"/>'
    out += poly([(20 + x * s, 20 + y * s) for x, y in pts], FILL[d.get("fill", "blue")], INK, 3)
    return svg(W, H, out)


def bargraph1(d):
    """Single-unit-scale bar graph (Grade 2). data: title, cats, vals, top, ylabel, horizontal (bool)."""
    cats, vals, top = d["cats"], d["vals"], d["top"]
    every = 1 if top <= 12 else 2
    if d.get("horizontal"):
        W, H = 680, 90 + len(cats) * 58 + 40
        x0, x1, y0 = 150, 650, 60
        sc = (x1 - x0) / top
        out = text(W / 2, 32, d.get("title", ""), 20, weight="800")
        yb = y0 + len(cats) * 58
        for v in range(top + 1):
            out += line(x0 + v * sc, y0 - 6, x0 + v * sc, yb, "#c7d3e6", 1.2)
            if v % every == 0:
                out += text(x0 + v * sc, yb + 24, str(v), 14, weight="700")
        for i, (c, v) in enumerate(zip(cats, vals)):
            y = y0 + i * 58 + 10
            out += rect(x0, y, v * sc, 38, PAL[i % len(PAL)], INK, 1.8) + text(x0 - 10, y + 25, c, 16, anchor="end", weight="700")
        out += line(x0, y0 - 6, x0, yb, sw=2.5) + line(x0, yb, x1 + 10, yb, sw=2.5)
        if d.get("ylabel"):
            out += text((x0 + x1) / 2, H - 8, d["ylabel"], 15, weight="700")
        return svg(W, H, out)
    W = max(520, 120 + len(cats) * 120)
    H = 400
    x0, y0, y1 = 80, 340, 60
    sc = (y0 - y1) / top
    out = text(W / 2, 32, d.get("title", ""), 20, weight="800")
    for v in range(top + 1):
        y = y0 - v * sc
        out += line(x0, y, W - 30, y, "#c7d3e6", 1.2)
        if v % every == 0:
            out += text(x0 - 10, y + 5, str(v), 14, anchor="end", weight="700")
    bw = (W - 30 - x0) / len(cats)
    for i, (c, v) in enumerate(zip(cats, vals)):
        x = x0 + i * bw + bw * 0.2
        out += rect(x, y0 - v * sc, bw * 0.6, v * sc, PAL[i % len(PAL)], INK, 1.8)
        out += text(x + bw * 0.3, y0 + 24, c, 16, weight="700")
    out += line(x0, y0, W - 30, y0, sw=2.5) + line(x0, y0, x0, y1 - 10, sw=2.5)
    if d.get("ylabel"):
        out += f'<text x="20" y="{(y0 + y1) / 2:.0f}" font-size="15" font-weight="700" fill="{INK}" text-anchor="middle" transform="rotate(-90 20 {(y0 + y1) / 2:.0f})">{esc(d["ylabel"])}</text>'
    return svg(W, H, out)


def partition_pair(d):
    """Two partitioned shapes side by side (figs3.partition each). data: a, b."""
    a = G3.partition(d["a"]).replace("<svg ", '<svg x="0" y="0" ', 1)
    b = G3.partition(d["b"]).replace("<svg ", '<svg x="380" y="0" ', 1)
    return svg(740, 260, a + b)


KINDS = dict(G3.KINDS)
KINDS.update({"jline": jline, "money": money, "ruler2": ruler2, "counters": counters, "solids": solids, "bars": bars,
              "digital": digital, "tally": tally, "chart": chart, "blocks": blocks, "pv_chart": pv_chart, "draw_shape": draw_shape, "bargraph1": bargraph1, "partition_pair": partition_pair})


def render(kind, data):
    return KINDS[kind](data)
