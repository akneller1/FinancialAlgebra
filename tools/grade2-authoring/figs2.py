"""Grade 2 diagram kinds, drawn with Pillow and registered into the shared Grade 1 renderer.

Everything already available for Grade 1 (ten-frames, counters, number lines, base-ten, tally,
pictograph, bar graph, shapes, partitions, clocks, rulers, place value, arrays, sorting boxes)
is reused as-is. This module only adds what Grade 2 needs: hundreds blocks, three-digit place
value, coins, line plots, tape diagrams and polygons.
"""
import math
import figs1
from figs1 import (_canvas, _text, _center_text, _color, _RENDERERS,
                   INK, BLUE, GRID, SOFT_BLUE, SOFT_ORANGE, ORANGE, YELLOW, RED, GREEN, W, H)


def _baseten3(data):
    """Hundreds flats, tens rods and ones cubes on one baseline."""
    hundreds = int(data.get("hundreds", 0))
    tens = int(data.get("tens", 0))
    ones = int(data.get("ones", 0))
    im, d = _canvas()
    base, x = 300, 60
    for _ in range(hundreds):
        d.rectangle([x, base - 96, x + 96, base], fill=SOFT_BLUE, outline=BLUE, width=3)
        for k in range(1, 10):
            d.line([x + k * 9.6, base - 96, x + k * 9.6, base], fill=BLUE, width=1)
            d.line([x, base - 96 + k * 9.6, x + 96, base - 96 + k * 9.6], fill=BLUE, width=1)
        x += 108
        if x > W - 140:
            x, base = 60, base - 112
    if hundreds:
        x += 16
    for _ in range(tens):
        d.rectangle([x, base - 96, x + 30, base], fill=SOFT_ORANGE, outline=ORANGE, width=3)
        for k in range(1, 10):
            d.line([x, base - 96 + k * 9.6, x + 30, base - 96 + k * 9.6], fill=ORANGE, width=1)
        x += 40
    if tens:
        x += 16
    for _ in range(ones):
        d.rectangle([x, base - 20, x + 20, base], fill=SOFT_ORANGE, outline=ORANGE, width=2)
        x += 26
    cap = data.get("caption")
    if cap:
        _center_text(d, W / 2, 60, cap, 28)
    label = (f"{hundreds} {'hundred' if hundreds == 1 else 'hundreds'}, "
             f"{tens} {'ten' if tens == 1 else 'tens'}, {ones} {'one' if ones == 1 else 'ones'}")
    _text(d, 60, 440, label, 24)
    return im


def _place3(data):
    hundreds = int(data.get("hundreds", 0))
    tens = int(data.get("tens", 0))
    ones = int(data.get("ones", 0))
    im, d = _canvas()
    _center_text(d, W / 2, 56, data.get("caption", "Place value chart"), 26)
    cols = [("Hundreds", hundreds, BLUE), ("Tens", tens, ORANGE), ("Ones", ones, GREEN)]
    for i, (label, val, col) in enumerate(cols):
        x0 = 70 + i * 200
        d.rounded_rectangle([x0, 110, x0 + 170, 148], radius=8, fill=col, outline=INK, width=2)
        _center_text(d, x0 + 85, 129, label, 22, (255, 255, 255))
        d.rectangle([x0, 148, x0 + 170, 330], fill=(250, 252, 255), outline=INK, width=3)
        _center_text(d, x0 + 85, 240, val, 66, INK)
    return im


def _coins(data):
    """Coin piles with their values, e.g. [{"value": 25, "count": 3}]."""
    coins = data.get("coins", [])
    im, d = _canvas()
    _text(d, 50, 44, data.get("caption", "Coins"), 28)
    x, y = 80, 160
    names = {1: "1c", 5: "5c", 10: "10c", 25: "25c", 100: "$1"}
    colors = {1: (205, 127, 50), 5: (160, 170, 180), 10: (170, 180, 190), 25: (150, 160, 175), 100: (120, 150, 110)}
    for group in coins:
        v = int(group.get("value", 1))
        for _ in range(int(group.get("count", 1))):
            r = 34
            d.ellipse([x - r, y - r, x + r, y + r], fill=colors.get(v, (200, 200, 200)),
                      outline=INK, width=3)
            _center_text(d, x, y, names.get(v, str(v)), 22, (20, 20, 20))
            x += 84
            if x > W - 70:
                x, y = 80, y + 90
        x += 14
    total = data.get("total")
    if total is not None:
        _text(d, 60, 400, total, 28)
    return im


def _lineplot(data):
    """Line plot: values stacked as X marks on a number line."""
    values = [int(v) for v in data.get("values", [])]
    lo = int(data.get("min", min(values) if values else 0))
    hi = int(data.get("max", max(values) if values else 6))
    im, d = _canvas()
    left, right, y = 80, W - 80, 380
    d.line([left, y, right, y], fill=INK, width=4)
    span = max(hi - lo, 1)
    counts = {v: values.count(v) for v in set(values)}
    for v in range(lo, hi + 1):
        x = left + (v - lo) / span * (right - left)
        d.line([x, y - 10, x, y + 12], fill=INK, width=3)
        _center_text(d, x, y + 40, v, 24)
        for k in range(counts.get(v, 0)):
            _center_text(d, x, y - 26 - k * 30, "x", 26, BLUE)
    _text(d, 70, 60, data.get("title", "Lengths of pencils (in inches)"), 26)
    return im


def _tape(data):
    """Tape diagram: two labelled bars drawn to scale."""
    rows = data.get("rows", [])
    im, d = _canvas()
    _text(d, 50, 44, data.get("caption", "Tape diagram"), 26)
    unit = float(data.get("unit", 1))
    y = 140
    for row in rows:
        label = str(row.get("label", ""))
        length = float(row.get("len", 0))
        col = _color(row.get("color", "blue"))
        w = max(30.0, length / max(unit, 1) * 520)
        _text(d, 60, y + 6, label, 24)
        d.rectangle([60, y + 40, 60 + w, y + 92], fill=col, outline=INK, width=3)
        _center_text(d, 60 + w / 2, y + 66, row.get("text", ""), 24, (255, 255, 255))
        y += 120
    return im


def _polygon(data):
    items = data.get("shapes", [])
    im, d = _canvas()
    _text(d, 50, 34, data.get("caption", ""), 26)
    n = max(len(items), 1)
    slot = (W - 100) / n
    for i, s in enumerate(items):
        cx, cy = 50 + slot * (i + 0.5), 250
        size = min(slot * 0.32, 95)
        kind = s.get("type", "square")
        fill = _color(s.get("color", "blue"))
        if kind == "pentagon":
            pts = [(cx + size * 0.7 * math.cos(math.radians(-90 + 72 * k)),
                    cy + size * 0.7 * math.sin(math.radians(-90 + 72 * k))) for k in range(5)]
            d.polygon(pts, fill=fill, outline=INK)
        elif kind == "trapezoid":
            # exactly one pair of parallel sides: long base, short parallel top
            d.polygon([(cx - size * 0.85, cy + size * 0.5), (cx + size * 0.85, cy + size * 0.5),
                       (cx + size * 0.45, cy - size * 0.5), (cx - size * 0.45, cy - size * 0.5)],
                      fill=fill, outline=INK)
        elif kind == "quadrilateral":
            d.polygon([(cx - size * 0.7, cy + size * 0.5), (cx + size * 0.55, cy + size * 0.5),
                       (cx + size * 0.75, cy - size * 0.5), (cx - size * 0.5, cy - size * 0.5)],
                      fill=fill, outline=INK)
        elif kind in ("heptagon", "octagon"):
            sides = 7 if kind == "heptagon" else 8
            pts = [(cx + size * 0.62 * math.cos(math.radians(-90 + 360 / sides * k)),
                    cy + size * 0.62 * math.sin(math.radians(-90 + 360 / sides * k)))
                   for k in range(sides)]
            d.polygon(pts, fill=fill, outline=INK)
        elif kind == "hexagon":
            pts = [(cx + size * 0.62 * math.cos(math.pi / 3 * k), cy + size * 0.62 * math.sin(math.pi / 3 * k)) for k in range(6)]
            d.polygon(pts, fill=fill, outline=INK)
        elif kind == "triangle":
            d.polygon([(cx, cy - size * 0.72), (cx - size * 0.85, cy + size * 0.6), (cx + size * 0.85, cy + size * 0.6)], fill=fill, outline=INK)
        elif kind == "rectangle":
            d.rectangle([cx - size * 0.8, cy - size / 2, cx + size * 0.8, cy + size / 2], fill=fill, outline=INK, width=4)
        else:
            d.rectangle([cx - size / 2, cy - size / 2, cx + size / 2, cy + size / 2], fill=fill, outline=INK, width=4)
        if s.get("label"):
            _center_text(d, cx, cy + size * 0.95, s["label"], 24)
    if data.get("footer"):
        _center_text(d, W / 2, H - 40, data["footer"], 24)
    return im


_RENDERERS.update({"baseten3": _baseten3, "place3": _place3, "coins": _coins,
                   "lineplot": _lineplot, "tape": _tape, "polygon": _polygon})
