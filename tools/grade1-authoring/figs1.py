"""Grade 1 diagram renderer (Pillow).

Same contract as the Grade 5 figure module: a diagram is declared as (kind, data) by a
question family, rendered here to PNG bytes, and its alt text is written from the same data
so the description can never drift from the picture.

No SVG rasteriser is available in this environment, so figures are drawn directly with
Pillow primitives on a fixed 720x480 canvas.  Colours are chosen for print and for colour
vision deficiency (blue / orange / green / purple, no red-green pairings as the only cue).
"""
import io
from PIL import Image, ImageDraw, ImageFont

W, H = 720, 480
BG = (255, 255, 255)
INK = (24, 35, 51)
GRID = (203, 213, 225)
BLUE = (37, 99, 235)
ORANGE = (234, 88, 12)
GREEN = (21, 128, 61)
PURPLE = (126, 34, 206)
TEAL = (13, 148, 136)
YELLOW = (250, 204, 21)
RED = (190, 30, 45)
SOFT_BLUE = (219, 234, 254)
SOFT_ORANGE = (255, 237, 213)

_COLORS = {"blue": BLUE, "orange": ORANGE, "green": GREEN, "purple": PURPLE, "teal": TEAL,
           "yellow": YELLOW, "red": RED}

_FONT_CACHE = {}


def _font(size, bold=False):
    key = (size, bold)
    if key not in _FONT_CACHE:
        try:
            _FONT_CACHE[key] = ImageFont.load_default(size=size)
        except TypeError:                                    # very old Pillow
            _FONT_CACHE[key] = ImageFont.load_default()
    return _FONT_CACHE[key]


def _canvas():
    im = Image.new("RGB", (W, H), BG)
    return im, ImageDraw.Draw(im)


def _text(d, x, y, s, size=26, fill=INK, anchor="la"):
    d.text((int(x), int(y)), str(s), font=_font(size), fill=fill, anchor=anchor)


def _center_text(d, x, y, s, size=26, fill=INK):
    d.text((int(x), int(y)), str(s), font=_font(size), fill=fill, anchor="mm")


def _color(name, default=BLUE):
    return _COLORS.get(str(name).lower(), default)


def _png(im):
    buf = io.BytesIO()
    im.convert("RGB").quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(buf, "PNG", optimize=True)
    return buf.getvalue()


# --------------------------------------------------------------------------- primitives
def _counter(d, cx, cy, r, fill):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=INK, width=2)


def _star(d, cx, cy, r, fill):
    import math
    pts = []
    for k in range(10):
        ang = -math.pi / 2 + k * math.pi / 5
        rad = r if k % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=fill, outline=INK)


def _tally_mark(d, x, y, h=54, fill=INK):
    d.line([x, y, x, y + h], fill=fill, width=5)


# --------------------------------------------------------------------------- kinds
def _tenframe(data):
    frames = data.get("frames", [10, 10])
    filled = data.get("filled", [0, 0])
    im, d = _canvas()
    n = len(frames)
    fw, fh = 300, 150
    gap = 40
    total_w = n * fw + (n - 1) * gap
    x0 = (W - total_w) // 2
    y0 = 130
    cw, ch = fw / 5, fh / 2
    for fi in range(n):
        ox = x0 + fi * (fw + gap)
        d.rectangle([ox, y0, ox + fw, y0 + fh], fill=(250, 252, 255), outline=INK, width=3)
        for row in range(2):
            for col in range(5):
                x1, y1 = ox + col * cw, y0 + row * ch
                d.rectangle([x1, y1, x1 + cw, y1 + ch], outline=GRID, width=2)
        # counters (a caller may supply fewer values than frames)
        count = filled[fi] if fi < len(filled) else 0
        for j in range(min(count, 10)):
            row, col = divmod(j, 5)
            cx = ox + col * cw + cw / 2
            cy = y0 + row * ch + ch / 2
            _counter(d, cx, cy, min(cw, ch) * 0.33, _color(data.get("color", "blue")))
    cap = data.get("caption")
    if cap:
        _center_text(d, W / 2, 360, cap, 30)
    return im


def _counters(data):
    groups = data.get("groups") or [{"count": 5, "color": "blue"}]
    im, d = _canvas()
    top = 90 if data.get("caption") else 70
    rows = len(groups)
    band = (H - top - 40) / max(rows, 1)
    for gi, g in enumerate(groups):
        cnt = int(g.get("count", 0))
        color = _color(g.get("color", "blue"))
        cols = min(cnt, 10) if cnt > 0 else 1
        rowsn = (cnt + 9) // 10 if cnt else 1
        r = min(26, 240 / max(cols, 1) / 2.4, band / (rowsn * 2.6))
        gw = cols * (r * 2.5)
        x0 = (W - gw) / 2
        y0 = top + gi * band + band / 2 - (rowsn * r * 2.4) / 2 + r
        for j in range(cnt):
            rr, cc = divmod(j, 10)
            cx = x0 + cc * (r * 2.5) + r
            cy = y0 + rr * (r * 2.4)
            if data.get("style") == "star":
                _star(d, cx, cy, r * 0.9, color)
            else:
                _counter(d, cx, cy, r * 0.9, color)
        label = g.get("label")
        if label:
            _text(d, 34, y0 - 10, label, 24)
    cap = data.get("caption")
    if cap:
        _center_text(d, W / 2, H - 46, cap, 28)
    return im


def _numberline(data):
    lo, hi = int(data.get("min", 0)), int(data.get("max", 10))
    step = int(data.get("step", 1))
    im, d = _canvas()
    y = 300
    left, right = 60, W - 60
    d.line([left, y, right, y], fill=INK, width=4)
    span = max(hi - lo, 1)
    ticks = list(range(lo, hi + 1, step))
    for t in ticks:
        x = left + (t - lo) / span * (right - left)
        d.line([x, y - 12, x, y + 12], fill=INK, width=3)
        _center_text(d, x, y + 40, t, 24)
    for m in data.get("marks", []):
        x = left + (m - lo) / span * (right - left)
        d.ellipse([x - 13, y - 13, x + 13, y + 13], fill=YELLOW, outline=INK, width=3)
        _center_text(d, x, y - 1, m, 20)
    for j in data.get("jumps", []):
        a, b = j[0], j[1]
        xa = left + (a - lo) / span * (right - left)
        xb = left + (b - lo) / span * (right - left)
        top = y - 70 - 40 * j[2] if len(j) > 2 else y - 70
        d.arc([min(xa, xb), top, max(xa, xb), y - 20], 180, 360, fill=BLUE, width=4)
        if len(j) > 3 and j[3]:
            _center_text(d, (xa + xb) / 2, top - 18, j[3], 24, BLUE)
    if data.get("point") is not None:
        p = data["point"]
        x = left + (p - lo) / span * (right - left)
        d.polygon([(x, y - 26), (x - 14, y - 50), (x + 14, y - 50)], fill=RED, outline=INK)
    cap = data.get("caption")
    if cap:
        _center_text(d, W / 2, 110, cap, 28)
    return im


def _baseten(data):
    tens, ones = int(data.get("tens", 0)), int(data.get("ones", 0))
    im, d = _canvas()
    x = 60
    ybase = 380
    for _ in range(tens):
        d.rectangle([x, ybase - 200, x + 34, ybase], fill=SOFT_BLUE, outline=BLUE, width=3)
        for k in range(1, 10):
            yy = ybase - 200 + k * 20
            d.line([x + 3, yy, x + 31, yy], fill=BLUE, width=1)
        x += 46
        if x > W - 90:
            x = 60
            ybase -= 215
    if tens:
        x += 12
    for i in range(ones):
        d.rectangle([x, ybase - 20, x + 20, ybase], fill=SOFT_ORANGE, outline=ORANGE, width=2)
        x += 26
    cap = data.get("caption")
    if cap:
        _center_text(d, W / 2, 60, cap, 28)
    _text(d, 60, 430, f"{tens} tens and {ones} ones", 24, INK)
    return im


def _tally(data):
    rows = data.get("rows", [])
    im, d = _canvas()
    top = 100
    band = 86
    _text(d, 60, 42, data.get("caption", "Tally chart"), 28)
    for i, (label, count) in enumerate(rows):
        y = top + i * band
        _text(d, 60, y, label, 26)
        x = 250
        n = int(count)
        for g in range(n // 5):
            for k in range(4):
                _tally_mark(d, x + k * 12, y - 4)
            d.line([x - 6, y + 48, x + 48, y - 8], fill=INK, width=5)
            x += 70
        for k in range(n % 5):
            _tally_mark(d, x, y - 4)
            x += 12
        _text(d, 620, y, f"= {n}", 24)
    return im


def _pictograph(data):
    rows = data.get("rows", [])
    key = data.get("key", 1)
    sym = data.get("symbol", "dot")
    im, d = _canvas()
    _text(d, 50, 40, data.get("caption", "Picture graph"), 28)
    _text(d, W - 50, 40, f"Each {sym} = {key}", 24, anchor="ra")
    top, band = 110, 78
    for i, (label, count) in enumerate(rows):
        y = top + i * band
        _text(d, 50, y, label, 25)
        n = int(count) // max(int(key), 1)
        for j in range(n):
            cx = 250 + j * 52
            if sym == "star":
                _star(d, cx, y + 12, 18, ORANGE)
            else:
                _counter(d, cx, y + 12, 16, BLUE)
    return im


def _bargraph(data):
    rows = data.get("rows", [])
    im, d = _canvas()
    _text(d, 50, 34, data.get("caption", "Bar graph"), 28)
    top, band = 110, 80
    maxv = max([int(c) for _, c in rows] + [1])
    for i, (label, count) in enumerate(rows):
        y = top + i * band
        _text(d, 50, y, label, 24)
        w = int((W - 330) * int(count) / maxv)
        d.rectangle([240, y, 240 + max(w, 6), y + 46], fill=_color(data.get("color", "blue")), outline=INK, width=2)
        _text(d, 240 + max(w, 6) + 14, y + 8, count, 24)
    return im


def _shapes(data):
    items = data.get("shapes", [])
    im, d = _canvas()
    _text(d, 50, 34, data.get("caption", ""), 26)
    n = max(len(items), 1)
    slot = (W - 100) / n
    for i, s in enumerate(items):
        cx = 50 + slot * (i + 0.5)
        cy = 250
        size = min(slot * 0.32, 95)
        kind = s.get("type", "square")
        fill = _color(s.get("color", "blue"))
        if kind in ("square", "rectangle"):
            w = size * (1.55 if kind == "rectangle" else 1)
            d.rectangle([cx - w / 2, cy - size / 2, cx + w / 2, cy + size / 2], fill=fill, outline=INK, width=4)
        elif kind == "triangle":
            d.polygon([(cx, cy - size * 0.72), (cx - size * 0.85, cy + size * 0.6), (cx + size * 0.85, cy + size * 0.6)], fill=fill, outline=INK)
        elif kind == "circle":
            d.ellipse([cx - size / 2, cy - size / 2, cx + size / 2, cy + size / 2], fill=fill, outline=INK, width=4)
        elif kind == "hexagon":
            import math
            pts = [(cx + size * 0.6 * math.cos(math.pi / 3 * k), cy + size * 0.6 * math.sin(math.pi / 3 * k)) for k in range(6)]
            d.polygon(pts, fill=fill, outline=INK)
        elif kind in ("cube", "cylinder", "sphere", "cone"):
            if kind == "cube":
                d.rectangle([cx - size / 2, cy - size / 2, cx + size * 0.2, cy + size * 0.2], fill=fill, outline=INK, width=3)
                d.polygon([(cx - size / 2, cy - size / 2), (cx - size / 4, cy - size * 0.8), (cx + size * 0.45, cy - size * 0.8), (cx + size * 0.2, cy - size / 2)], fill=fill, outline=INK)
                d.polygon([(cx + size * 0.2, cy - size / 2), (cx + size * 0.45, cy - size * 0.8), (cx + size * 0.45, cy - size * 0.1), (cx + size * 0.2, cy + size * 0.2)], fill=fill, outline=INK)
            elif kind == "cylinder":
                d.rectangle([cx - size / 2, cy - size / 2, cx + size / 2, cy + size / 2], fill=fill, outline=INK, width=3)
                d.ellipse([cx - size / 2, cy - size * 0.65, cx + size / 2, cy - size * 0.25], fill=fill, outline=INK, width=3)
            elif kind == "sphere":
                d.ellipse([cx - size / 2, cy - size / 2, cx + size / 2, cy + size / 2], fill=fill, outline=INK, width=3)
            else:
                d.polygon([(cx, cy - size * 0.7), (cx - size * 0.6, cy + size * 0.5), (cx + size * 0.6, cy + size * 0.5)], fill=fill, outline=INK)
        label = s.get("label")
        if label:
            _center_text(d, cx, cy + size * 0.95, label, 24)
    cap = data.get("footer")
    if cap:
        _center_text(d, W / 2, H - 40, cap, 24)
    return im


def _partition(data):
    shape = data.get("shape", "rectangle")
    parts = int(data.get("parts", 2))
    shaded = int(data.get("shaded", 0))
    im, d = _canvas()
    cx, cy = W / 2, H / 2 + 20
    if shape == "circle":
        r = 160
        colors = [SOFT_BLUE] * parts
        for k in range(shaded):
            colors[k] = BLUE
        step = 360 / parts
        for k in range(parts):
            d.pieslice([cx - r, cy - r, cx + r, cy + r], k * step, (k + 1) * step, fill=colors[k], outline=INK, width=3)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=4)
    else:
        w, h = 440, 240
        pw = w / parts
        for k in range(parts):
            fill = BLUE if k < shaded else SOFT_BLUE
            d.rectangle([cx - w / 2 + k * pw, cy - h / 2, cx - w / 2 + (k + 1) * pw, cy + h / 2], fill=fill, outline=INK, width=3)
    cap = data.get("caption")
    if cap:
        _center_text(d, W / 2, 70, cap, 28)
    return im


def _clock(data):
    h = int(data.get("hour", 3)) % 12
    m = int(data.get("minute", 0))
    im, d = _canvas()
    cx, cy, r = W / 2, H / 2 + 10, 170
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255), outline=INK, width=5)
    import math
    for k in range(1, 13):
        ang = math.radians(k * 30 - 90)
        tx, ty = cx + (r - 30) * math.cos(ang), cy + (r - 30) * math.sin(ang)
        _center_text(d, tx, ty, k, 28)
    # minute ticks
    for k in range(60):
        ang = math.radians(k * 6 - 90)
        r1 = r - 8 if k % 5 else r - 16
        d.line([cx + r1 * math.cos(ang), cy + r1 * math.sin(ang), cx + r * math.cos(ang), cy + r * math.sin(ang)],
               fill=INK if k % 5 == 0 else GRID, width=3 if k % 5 == 0 else 1)
    # hour hand
    ha = math.radians((h % 12) * 30 + m * 0.5 - 90)
    d.line([cx, cy, cx + r * 0.52 * math.cos(ha), cy + r * 0.52 * math.sin(ha)], fill=INK, width=10)
    # minute hand
    ma = math.radians(m * 6 - 90)
    d.line([cx, cy, cx + r * 0.76 * math.cos(ma), cy + r * 0.76 * math.sin(ma)], fill=BLUE, width=6)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=INK)
    cap = data.get("caption")
    if cap:
        _center_text(d, W / 2, 40, cap, 26)
    return im


def _ruler(data):
    units = int(data.get("units", 6))
    label = data.get("unit", "unit")
    show = data.get("show")          # if set, shade the measured length
    im, d = _canvas()
    left, right, y = 70, W - 70, 250
    seg = (right - left) / max(units, 1)
    d.rectangle([left, y - 34, right, y + 34], fill=(254, 252, 232), outline=INK, width=3)
    for k in range(units + 1):
        x = left + k * seg
        d.line([x, y - 34, x, y + 34], fill=INK, width=2)
        _center_text(d, x, y + 58, k, 22)
    if show:
        d.rectangle([left, y - 34, left + show * seg, y + 34], fill=(191, 219, 254), outline=BLUE, width=0)
        d.rectangle([left, y - 34, right, y + 34], outline=INK, width=3)
    _text(d, left, y - 80, data.get("caption", f"Measured in {label}s"), 26)
    return im


def _comparegroups(data):
    im, d = _canvas()
    left = data.get("left", {})
    right = data.get("right", {})
    for i, g in enumerate((left, right)):
        x0 = 60 + i * (W / 2)
        w = W / 2 - 100
        d.rounded_rectangle([x0, 120, x0 + w, 400], radius=18, outline=GRID, width=3, fill=(250, 252, 255))
        _text(d, x0 + 20, 132, g.get("label", ""), 24)
        cnt = int(g.get("count", 0))
        r = 20
        cols = max(min(cnt, 5), 1)
        for j in range(cnt):
            rr, cc = divmod(j, 5)
            cx = x0 + 50 + cc * (r * 2.6)
            cy = 210 + rr * (r * 2.6)
            _counter(d, cx, cy, r, _color(g.get("color", "blue")))
    cap = data.get("caption")
    if cap:
        _center_text(d, W / 2, 60, cap, 28)
    return im


def _placevalue(data):
    tens, ones = int(data.get("tens", 0)), int(data.get("ones", 0))
    im, d = _canvas()
    _center_text(d, W / 2, 56, data.get("caption", "Place value chart"), 26)
    cols = [("Tens", tens, BLUE), ("Ones", ones, ORANGE)]
    for i, (label, val, col) in enumerate(cols):
        x0 = 120 + i * 250
        d.rounded_rectangle([x0, 110, x0 + 200, 150], radius=8, fill=col, outline=INK, width=2)
        _center_text(d, x0 + 100, 130, label, 26, (255, 255, 255))
        d.rectangle([x0, 150, x0 + 200, 330], fill=(250, 252, 255), outline=INK, width=3)
        _center_text(d, x0 + 100, 240, val, 74, INK)
    return im


def _numbercards(data):
    """A row of numeral cards (e.g. "which is greater?"), optional blank card."""
    cards = data.get("cards", [])
    im, d = _canvas()
    n = max(len(cards), 1)
    slot = (W - 80) / n
    for i, c in enumerate(cards):
        cx = 40 + slot * (i + 0.5)
        d.rounded_rectangle([cx - slot * 0.32, 160, cx + slot * 0.32, 320], radius=16, fill=SOFT_BLUE, outline=BLUE, width=4)
        _center_text(d, cx, 240, c if c != "" else "?", 60)
    cap = data.get("caption")
    if cap:
        _center_text(d, W / 2, 70, cap, 28)
    return im


def _array(data):
    rows, cols = int(data.get("rows", 2)), int(data.get("cols", 5))
    im, d = _canvas()
    r = 22
    gapx, gapy = 54, 54
    w = (cols - 1) * gapx + 2 * r
    h = (rows - 1) * gapy + 2 * r
    x0, y0 = (W - w) / 2, (H - h) / 2
    for i in range(rows):
        for j in range(cols):
            _counter(d, x0 + r + j * gapx, y0 + r + i * gapy, r, _color(data.get("color", "green")))
    cap = data.get("caption")
    if cap:
        _center_text(d, W / 2, 60, cap, 28)
    return im


def _sortbox(data):
    """Objects scattered in a box, for sorting/counting tasks."""
    items = data.get("items", [])
    im, d = _canvas()
    d.rounded_rectangle([60, 100, W - 60, H - 70], radius=20, outline=GRID, width=3, fill=(250, 252, 255))
    if items:
        cols = 8
        for i, it in enumerate(items):
            rr, cc = divmod(i, cols)
            cx = 120 + cc * 62
            cy = 160 + rr * 62
            color = _color(it if isinstance(it, str) else it.get("color", "blue"))
            if isinstance(it, dict) and it.get("shape") == "star":
                _star(d, cx, cy, 20, color)
            else:
                _counter(d, cx, cy, 20, color)
    cap = data.get("caption")
    if cap:
        _center_text(d, W / 2, 56, cap, 28)
    return im



def _composition(data):
    """A true joined composite with visible internal triangular boundaries."""
    import math
    shape = data.get("shape")
    im, d = _canvas()
    _center_text(d, W / 2, 60, "How do the triangle pieces fit?", 28)
    cx, cy = W / 2, 255
    if shape == "hexagon":
        radius = 160
        corners = [(cx + radius * math.cos(math.pi * k / 3 - math.pi / 6),
                    cy + radius * math.sin(math.pi * k / 3 - math.pi / 6)) for k in range(6)]
        for k in range(6):
            pts = [(cx, cy), corners[k], corners[(k + 1) % 6]]
            d.polygon(pts, fill=[SOFT_BLUE, SOFT_ORANGE, SOFT_BLUE, SOFT_ORANGE, SOFT_BLUE, SOFT_ORANGE][k],
                      outline=INK, width=3)
    elif shape == "square":
        side = 285
        x1, y1, x2, y2 = cx - side / 2, cy - side / 2, cx + side / 2, cy + side / 2
        d.polygon([(x1, y1), (x2, y1), (x2, y2)], fill=SOFT_BLUE, outline=INK, width=4)
        d.polygon([(x1, y1), (x2, y2), (x1, y2)], fill=SOFT_ORANGE, outline=INK, width=4)
    else:
        raise ValueError("Unsupported composition shape: " + str(shape))
    _center_text(d, W / 2, H - 35, "The outline is formed by joining triangles.", 22)
    return im

_RENDERERS = {
    "tenframe": _tenframe, "counters": _counters, "numberline": _numberline, "baseten": _baseten,
    "tally": _tally, "pictograph": _pictograph, "bargraph": _bargraph, "shapes": _shapes,
    "partition": _partition, "composition": _composition, "clock": _clock, "ruler": _ruler, "comparegroups": _comparegroups,
    "placevalue": _placevalue, "numbercards": _numbercards, "array": _array, "sortbox": _sortbox,
}


def render_png(kind, data):
    if kind not in _RENDERERS:
        raise ValueError(f"unknown diagram kind {kind!r}")
    return _png(_RENDERERS[kind](data))


def render(kind, data):
    """Compatibility with the Grade 5 helper name (returns PNG bytes here, not SVG)."""
    return render_png(kind, data)
