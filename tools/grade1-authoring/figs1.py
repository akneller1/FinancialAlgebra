"""Grade 1 diagram kinds, added to the Grade 2 kit (figs2.py -> figs3.py -> Grade 5 figs.py).

render(kind, data) -> SVG. Every drawing is built only from `data`, which is also stored in the check file.
Reused unchanged: counters, jline, tally, chart, blocks, digital, solids, bars (Grade 2); clock, picgraph, partition,
groups (Grade 3); table (Grade 5). New kinds: tenframe, crossrow, lengths, measure, shapes1, compose."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(HERE, "..", "grade2-authoring"))
sys.path.append(os.path.join(HERE, "..", "grade3-authoring"))
sys.path.append(os.path.join(HERE, "..", "grade5-authoring"))
import figs2 as G2
from figs import svg, text, rect, line, poly, INK, FILL

RED, YEL, BLUE, ORANGE, GREEN = "#e2563b", "#f5c400", "#2f7fd8", "#f08c1a", "#1aa37a"


def _dot(cx, cy, col, r=15, crossed=False):
    s = f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{col}" stroke="{INK}" stroke-width="1.6"/>'
    if crossed:
        s += line(cx - r, cy - r, cx + r, cy + r, INK, 3.5) + line(cx - r, cy + r, cx + r, cy - r, INK, 3.5)
    return s


def tenframe(d):
    """Ten frames (frames: 1 or 2). a red counters then b yellow counters, filled in reading order (top row first, frame by
    frame); x: the last x counters are crossed out."""
    k, a, b, x = d.get("frames", 1), d.get("a", 0), d.get("b", 0), d.get("x", 0)
    n = a + b
    W, H = 30 + k * 250, 132
    out = ""
    for f in range(k):
        for i in range(10):
            cx, cy = 20 + f * 250 + (i % 5) * 44, 18 + (i // 5) * 48
            out += rect(cx, cy, 44, 48, "#fff", sw=2.2)
            j = f * 10 + i
            if j < n:
                out += _dot(cx + 22, cy + 24, RED if j < a else YEL, 15, j >= n - x)
    return svg(W, H, out)


def crossrow(d):
    """n counters in rows of `per` (default 5); the last x are crossed out. color: red|blue."""
    n, x, per = d["n"], d.get("x", 0), d.get("per", 5)
    rows = math.ceil(n / per)
    W, H = 40 + per * 46 + (per // 5 - 1) * 14, 24 + rows * 46
    out = ""
    col = BLUE if d.get("color") == "blue" else RED
    for i in range(n):
        r_, c = divmod(i, per)
        out += _dot(36 + c * 46 + (c // 5) * 14, 36 + r_ * 46, col, 16, i >= n - x)
    return svg(W, H, out)


COLS = {"blue": "#7fb6f0", "orange": "#ffc27a", "green": "#8fdcbf", "pink": "#f5a3c4", "purple": "#c3a6f0", "yellow": "#ffe08a"}


def lengths(d):
    """Objects drawn as long rounded bars, one per row. items [{"label", "len", "start", "color"}] in grid units (u px each).
    grid: each row sits on a strip of unit squares (so lengths can be counted); line: draw the start line at 0."""
    items, u = d["items"], d.get("u", 40)
    span = max(it.get("start", 0) + it["len"] for it in items) + (1 if d.get("grid") else 0)
    W, H = 150 + span * u + 30, 30 + len(items) * 62
    out = ""
    for i, it in enumerate(items):
        y = 26 + i * 62
        if d.get("grid"):
            for k in range(span):
                out += rect(140 + k * u, y - 6, u, 46, "#f4f7fc", "#9aa8bb", 1.4)
        x0 = 140 + it.get("start", 0) * u
        out += rect(x0, y + 5, it["len"] * u, 24, COLS.get(it.get("color", "blue"), "#7fb6f0"), INK, 2.4, rx=12)
        if d.get("grid"):
            for k in range(span + 1):
                out += line(140 + k * u, y - 6, 140 + k * u, y + 40, "#5b6b80", 1.2, 'stroke-opacity="0.55"')
        out += text(126, y + 24, it["label"], 19, anchor="end", weight="800")
    if d.get("line", True):
        out += line(140, 10, 140, H - 6, INK, 3)
    return svg(W, H, out)


def measure(d):
    """An object (bar of length `len` units) with units laid under it. units: [[x0, w], ...] in units (gaps, overlaps and
    other sizes are drawn exactly as given). unit: 'cube'|'clip'. label: object name."""
    L, u = d["len"], 44
    units = d["units"]
    span = max([L] + [a + w for a, w in units])
    W, H = 60 + span * u + 40, 170
    x0 = 50
    out = text(x0, 28, d.get("label", ""), 19, anchor="start", weight="800")
    out += rect(x0, 40, L * u, 36, "#7fb6f0", INK, 2.4, rx=12)
    out += line(x0, 34, x0, 150, "#7a8799", 1.5, 'stroke-dasharray="5 4"')
    out += line(x0 + L * u, 34, x0 + L * u, 150, "#7a8799", 1.5, 'stroke-dasharray="5 4"')
    for k, (a, w) in enumerate(units):
        x, y = x0 + a * u, 96 + (8 if k % 2 and d.get("stagger") else 0)
        if d.get("unit") == "clip":
            out += rect(x + 2, y + 6, w * u - 4, 22, "none", "#5a62d8", 3.5, rx=11) + rect(x + 10, y + 12, w * u - 18, 10, "none", "#5a62d8", 2.5, rx=5)
        else:
            out += rect(x, y, w * u, 34, "#ffc27a", INK, 2, rx=3)
    return svg(W, H, out)


def _shape_pts(kind):
    """Unit outlines (y down) for named 2-D shapes; curves as polylines."""
    if kind == "triangle":
        return [(0, 1), (0.5, 0), (1, 1)]
    if kind == "triangle2":                       # skinny right triangle
        return [(0, 0), (0, 1), (0.6, 1)]
    if kind == "square":
        return [(0, 0), (1, 0), (1, 1), (0, 1)]
    if kind == "rectangle":
        return [(0, 0.2), (1.6, 0.2), (1.6, 0.9), (0, 0.9)]
    if kind == "trapezoid":
        return [(0.3, 0.15), (1.1, 0.15), (1.4, 0.85), (0, 0.85)]
    if kind == "hexagon":
        return [(0.5 + 0.5 * math.cos(math.radians(60 * k)), 0.5 + 0.5 * math.sin(math.radians(60 * k))) for k in range(6)]
    if kind == "rhombus":
        return [(0.5, 0), (1, 0.5), (0.5, 1), (0, 0.5)]
    if kind == "pentagon":
        return [(0.5 + 0.5 * math.cos(math.radians(72 * k - 90)), 0.5 + 0.5 * math.sin(math.radians(72 * k - 90))) for k in range(5)]
    if kind == "circle":
        return [(0.5 + 0.5 * math.cos(t / 36 * math.tau), 0.5 + 0.5 * math.sin(t / 36 * math.tau)) for t in range(36)]
    if kind == "halfcircle":
        return [(0.5 + 0.5 * math.cos(math.pi + t / 18 * math.pi), 0.75 + 0.5 * math.sin(math.pi + t / 18 * math.pi)) for t in range(19)]
    if kind == "quartercircle":
        return [(0, 0)] + [(math.sin(t / 18 * math.pi / 2), math.cos(t / 18 * math.pi / 2)) for t in range(19)]
    if kind == "oval":
        return [(0.7 + 0.7 * math.cos(t / 36 * math.tau), 0.5 + 0.4 * math.sin(t / 36 * math.tau)) for t in range(36)]
    raise KeyError(kind)


def _place(pts, cx, cy, size, rot):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    mx, my = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    sc = size / max(max(xs) - min(xs), max(ys) - min(ys))
    a = math.radians(rot)
    return [(cx + ((x - mx) * math.cos(a) - (y - my) * math.sin(a)) * sc, cy + ((x - mx) * math.sin(a) + (y - my) * math.cos(a)) * sc) for x, y in pts]


def shapes1(d):
    """Row of labeled shapes. items [{"kind", "rot", "size" (0.5-1), "color", "label", "open" (gap: not closed)}].
    kind: triangle, triangle2, square, rectangle, trapezoid, hexagon, rhombus, pentagon, circle, halfcircle, quartercircle, oval."""
    items = d["items"]
    cw = 170
    W, H = cw * len(items) + 20, 210
    out = ""
    for k, it in enumerate(items):
        P = _place(_shape_pts(it["kind"]), 10 + k * cw + cw / 2, 92, 125 * it.get("size", 1), it.get("rot", 0))
        col = COLS.get(it.get("color", "blue"), "#7fb6f0")
        if it.get("open"):
            p = " ".join(f"{x:.1f},{y:.1f}" for x, y in P)
            out += f'<polyline points="{p}" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'
        else:
            out += poly(P, col, INK, 3)
        if it.get("label"):
            out += text(10 + k * cw + cw / 2, 198, it["label"], 20, weight="800")
    return svg(W, H, out)


# composite shapes drawn with every piece outlined: name -> (piece kind, pieces as polygons in a 0..4 box)
COMPOSE = {
    "square_tri2": ("triangle", [[(0, 0), (4, 0), (0, 4)], [(4, 0), (4, 4), (0, 4)]]),
    "square_tri4": ("triangle", [[(0, 0), (4, 0), (2, 2)], [(4, 0), (4, 4), (2, 2)], [(4, 4), (0, 4), (2, 2)], [(0, 4), (0, 0), (2, 2)]]),
    "rect_sq2": ("square", [[(0, 1), (2, 1), (2, 3), (0, 3)], [(2, 1), (4, 1), (4, 3), (2, 3)]]),
    "rect_sq3": ("square", [[(0, 1.4), (1.33, 1.4), (1.33, 2.73), (0, 2.73)], [(1.33, 1.4), (2.67, 1.4), (2.67, 2.73), (1.33, 2.73)],
                            [(2.67, 1.4), (4, 1.4), (4, 2.73), (2.67, 2.73)]]),
    "square_sq4": ("square", [[(0, 0), (2, 0), (2, 2), (0, 2)], [(2, 0), (4, 0), (4, 2), (2, 2)], [(0, 2), (2, 2), (2, 4), (0, 4)], [(2, 2), (4, 2), (4, 4), (2, 4)]]),
    "rect_tri2": ("triangle", [[(0, 1), (4, 1), (0, 3)], [(4, 1), (4, 3), (0, 3)]]),
    "square_rect2": ("rectangle", [[(0, 0), (4, 0), (4, 2), (0, 2)], [(0, 2), (4, 2), (4, 4), (0, 4)]]),
    "hex_tri6": ("triangle", None),
    "hex_trap2": ("trapezoid", None),
    "trap_tri3": ("triangle", None),
    "circle_half2": ("half-circle", None),
    "circle_quarter4": ("quarter-circle", None),
    "rhombus_tri2": ("triangle", None),
}


def _hex():
    return [(2 + 2 * math.cos(math.radians(60 * k)), 2 + 2 * math.sin(math.radians(60 * k))) for k in range(6)]


def compose(d):
    """A composite shape with the outline of every piece drawn. data: name (key of COMPOSE), color."""
    nm = d["name"]
    piece, polys = COMPOSE[nm]
    h = _hex()
    if nm == "hex_tri6":
        polys = [[(2, 2), h[k], h[(k + 1) % 6]] for k in range(6)]
    elif nm == "hex_trap2":
        polys = [[h[0], h[1], h[2], h[3]], [h[3], h[4], h[5], h[0]]]
    elif nm == "trap_tri3":
        s = 4 / 3 * 1.0
        r3 = math.sqrt(3) / 2 * 2
        top = 1 + r3
        polys = [[(0, top), (1, 1), (2, top)], [(1, 1), (3, 1), (2, top)], [(2, top), (3, 1), (4, top)]]
        polys = [[(x, y) for x, y in p] for p in polys]
    elif nm == "rhombus_tri2":
        r3 = math.sqrt(3)
        polys = [[(0, 2), (1, 2 - r3), (2, 2)], [(1, 2 - r3), (3, 2 - r3), (2, 2)]]
    out = ""
    S, ox, oy = 52, 40, 30
    if polys:
        xs = [x for p in polys for x, _ in p]
        ys = [y for p in polys for _, y in p]
        dx, dy = 2 - (max(xs) + min(xs)) / 2, 2 - (max(ys) + min(ys)) / 2
        polys = [[(x + dx, y + dy) for x, y in p] for p in polys]
    fills = [COLS[c] for c in ("blue", "orange", "green", "pink", "purple", "yellow")]
    if nm in ("circle_half2", "circle_quarter4"):
        cx, cy, R = ox + 2 * S, oy + 2 * S, 2 * S
        k = 2 if nm == "circle_half2" else 4
        for i in range(k):
            a0, a1 = math.tau * i / k, math.tau * (i + 1) / k
            pts = [(cx, cy)] + [(cx + R * math.cos(a0 + (a1 - a0) * t / 24), cy + R * math.sin(a0 + (a1 - a0) * t / 24)) for t in range(25)]
            out += poly(pts, fills[i % 6], INK, 3)
    else:
        for i, p in enumerate(polys):
            out += poly([(ox + x * S, oy + y * S) for x, y in p], fills[i % 6], INK, 3)
    return svg(ox * 2 + 4 * S, oy * 2 + 4 * S, out)


KINDS = dict(G2.KINDS)
KINDS.update({"tenframe": tenframe, "crossrow": crossrow, "lengths": lengths, "measure": measure, "shapes1": shapes1, "compose": compose})


def render(kind, data):
    return KINDS[kind](data)
