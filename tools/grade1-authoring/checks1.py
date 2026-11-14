"""Grade 1 named checks for verify.py (added to the Grade 2 checks, which include the Grade 3 checks).
Each check recomputes the answer from the stored check data with its own arithmetic and tables; nothing is imported
from the families, g1lib or figs1."""
import math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(HERE, "..", "grade2-authoring"))
import checks2

V = checks2.V


def bind(g):
    checks2.bind(g)


FNS = dict(checks2.FNS)


def _int(t, unit=None):
    """Whole number in the answer; when unit is given the answer must carry it (plural agreement ignored)."""
    x = V["parse_value"](t)
    if x is None or x[0].denominator != 1:
        return None
    if unit is None:
        return int(x[0]) if not x[1] else None
    return int(x[0]) if V["unorm"](x[1]) == V["unorm"](unit) else None


def reg(f):
    FNS[f.__name__] = f
    return f


# ---------------------------------------------------------------- counting and number names
@reg
def count_n(c, t):
    return _int(t, c.get("unit")) == c["n"]


@reg
def count_words(c, t):
    """Exactly n numbers starting at start, each step apart."""
    try:
        vals = [int(p) for p in str(t).split(",")]
    except ValueError:
        return False
    return vals == [c["start"] + i * c["step"] for i in range(c["n"])]


_ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
_TENS = {2: "twenty", 3: "thirty", 4: "forty", 5: "fifty", 6: "sixty", 7: "seventy", 8: "eighty", 9: "ninety"}


def name_of(n):
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("-" + _ONES[n % 10] if n % 10 else "")
    return "one hundred" + (" " + name_of(n - 100) if n > 100 else "")


@reg
def num_word(c, t):
    return V["norm"](t) == name_of(c["n"])


@reg
def num_digits(c, t):
    return re.fullmatch(r"\d{1,3}", str(t).strip()) is not None and int(t) == c["n"]


@reg
def pair_ten(c, t):
    """'a and b' with a + b == total."""
    m = re.fullmatch(r"(\d+) and (\d+)", str(t).strip())
    return bool(m) and int(m.group(1)) + int(m.group(2)) == c["total"]


def _sides(eq):
    lhs, rhs = str(eq).split("=")
    return V["eval_expr"](lhs.replace("−", "-").strip()), V["eval_expr"](rhs.replace("−", "-").strip())


@reg
def eq_tf(c, t):
    """'True. Both sides are X.' or 'False. One side is X and the other side is Y.' judged from the equation."""
    a, b = _sides(c["eq"])
    s = str(t).strip()
    m = re.fullmatch(r"True\. Both sides are (\d+)\.", s)
    if m:
        return a == b == int(m.group(1))
    m = re.fullmatch(r"False\. One side is (\d+) and the other side is (\d+)\.", s)
    if m:
        return a != b and int(m.group(1)) == a and int(m.group(2)) == b
    return False


@reg
def eq_word(c, t):
    a, b = _sides(c["eq"])
    return V["norm"](t) == ("true" if a == b else "false")


@reg
def parts_make(c, t):
    m = re.fullmatch(r"(\d+) red and (\d+) blue", str(t).strip())
    return bool(m) and int(m.group(1)) + int(m.group(2)) == c["total"]


# ---------------------------------------------------------------- tens and ones
def _to(t):
    m = re.fullmatch(r"(\d+) (ten|tens) and (\d+) (one|ones)", V["norm"](t))
    if not m:
        return None
    a, tw, b, ow = int(m.group(1)), m.group(2), int(m.group(3)), m.group(4)
    if (tw == "ten") != (a == 1) or (ow == "one") != (b == 1):
        return None
    return a, b


@reg
def tens_ones(c, t):
    """'4 tens and 7 ones' naming c['n']; std: ones must be 0-9."""
    x = _to(t)
    return x is not None and 10 * x[0] + x[1] == c["n"] and (not c.get("std", True) or x[1] < 10)


@reg
def place_digit(c, t):
    """Value of a digit place: 'tens' -> number of tens digit, 'ones' -> ones digit."""
    v = _int(t)
    return v is not None and v == (c["n"] // 10 % 10 if c["place"] == "tens" else c["n"] % 10)


@reg
def cmp_word(c, t):
    """'greater' / 'less' / 'equal' answer about a vs b."""
    a, b = c["a"], c["b"]
    w = V["norm"](t)
    return w == ("greater" if a > b else "less" if a < b else "equal")


@reg
def pick_num(c, t):
    """Number chosen from c['nums'] that is the greatest / least, or one that makes 'x {sym} y' true when put in the blank."""
    v = _int(t)
    if v is None or v not in c["nums"]:
        return False
    if c["want"] in ("greatest", "least"):
        tgt = max(c["nums"]) if c["want"] == "greatest" else min(c["nums"])
        return v == tgt and c["nums"].count(tgt) == 1
    a = v if c["blank"] == 0 else c["other"]
    b = c["other"] if c["blank"] == 0 else v
    return {"<": a < b, ">": a > b, "=": a == b}[c["want"]]


@reg
def who_cmp(c, t):
    v = c["vals"]
    pick = (max if c["want"] == "more" else min)(v, key=v.get)
    return len(set(v.values())) == len(v) and V["norm"](t) == V["norm"](pick)


@reg
def cmp_stmt(c, t):
    """'a S b' or 'b S a' using exactly the two given numbers, and true."""
    m = re.fullmatch(r"(\d+) ([<>=]) (\d+)", str(t).strip())
    if not m:
        return False
    x, s, y = int(m.group(1)), m.group(2), int(m.group(3))
    if sorted([x, y]) != sorted([c["a"], c["b"]]):
        return False
    return {"<": x < y, ">": x > y, "=": x == y}[s]


@reg
def digit_fill(c, t):
    """tmpl like '4? > 47': the digit t replaces ? and the comparison is true."""
    if not re.fullmatch(r"\d", str(t).strip()):
        return False
    a, s, b = c["tmpl"].replace("?", str(t).strip()).split(" ")
    a, b = int(a), int(b)
    return {"<": a < b, ">": a > b, "=": a == b}[s]


@reg
def between_nums(c, t):
    v = _int(t)
    return v is not None and c["lo"] < v < c["hi"]


@reg
def order_nums(c, t):
    try:
        vals = [int(x) for x in str(t).split(",")]
    except ValueError:
        return False
    want = sorted(c["vals"], reverse=c["want"] == "greatest to least")
    return vals == want


@reg
def make_num(c, t):
    a, b = c["d"]
    opts = [10 * a + b, 10 * b + a]
    v = _int(t)
    return v == (max(opts) if c["want"] == "greatest" else min(opts))


# ---------------------------------------------------------------- length
def _span(c):
    """Number of units if the units are laid correctly (same size, end to end from 0 with no gaps or overlaps, covering len)."""
    us = sorted(c["units"])
    if any(w != us[0][1] for _, w in us):
        return None
    x = 0
    for a, w in us:
        if abs(a - x) > 1e-9:
            return None
        x += w
    return len(us) if abs(x - c["len"]) < 1e-9 else None


@reg
def units_long(c, t):
    n = _span(c)
    return n is not None and _int(t, c.get("unit")) == n


@reg
def measure_ok(c, t):
    """'Yes' when the units are laid correctly, otherwise the named mistake."""
    n = _span(c)
    w = V["norm"](t)
    if n is not None:
        return w.startswith("yes")
    us = sorted(c["units"])
    sizes = {u[1] for u in us}
    if len(sizes) > 1:
        return w.startswith("no") and "same size" in w
    x, gap, over = 0, False, False
    for a, wd in us:
        gap |= a > x + 1e-9
        over |= a < x - 1e-9
        x = a + wd
    if gap and not over:
        return w.startswith("no") and "gap" in w
    if over and not gap:
        return w.startswith("no") and "overlap" in w
    return False


@reg
def len_pick(c, t):
    """Name of the longest / shortest object (lengths in c['lens']); unique extreme required."""
    L = c["lens"]
    v = (max if c["want"] == "longest" else min)(L.values())
    names = [k for k, x in L.items() if x == v]
    return len(names) == 1 and V["norm"](t) == V["norm"](names[0])


@reg
def len_order(c, t):
    L = c["lens"]
    order = sorted(L, key=L.get, reverse=c["want"] == "longest first")
    return len(set(L.values())) == len(L) and [V["norm"](x) for x in str(t).split(",")] == [V["norm"](x) for x in order]


@reg
def indirect(c, t):
    """facts: [[A, B], ...] meaning A is longer than B (a chain). want: longest | shortest | 'cmp X Y' -> 'X'/'Y' longer one."""
    longer = {}
    names = set()
    for a, b in c["facts"]:
        longer.setdefault(a, set()).add(b)
        names |= {a, b}
    changed = True
    while changed:                                   # transitive closure
        changed = False
        for a in list(longer):
            for b in list(longer[a]):
                for x in longer.get(b, ()):
                    if x not in longer[a]:
                        longer[a].add(x)
                        changed = True
    w = V["norm"](t)
    if c["want"] == "longest":
        best = [n for n in names if len(longer.get(n, ())) == len(names) - 1]
        return len(best) == 1 and w == V["norm"](best[0])
    if c["want"] == "shortest":
        low = [n for n in names if all(n in longer.get(m, ()) for m in names if m != n)]
        return len(low) == 1 and w == V["norm"](low[0])
    x, y = c["pair"]
    if y in longer.get(x, ()):
        lo, sh = x, y
    elif x in longer.get(y, ()):
        lo, sh = y, x
    else:
        return False
    return w == V["norm"](sh if c["want"] == "cmp_short" else lo)


@reg
def indirect_word(c, t):
    """'longer' / 'shorter': is pair[0] longer or shorter than pair[1] from the facts."""
    x, y = c["pair"]
    lon = FNS["indirect"](dict(facts=c["facts"], want="cmp", pair=[x, y]), x)
    sh = FNS["indirect"](dict(facts=c["facts"], want="cmp", pair=[x, y]), y)
    w = V["norm"](t)
    return (lon and w == "longer") or (sh and w == "shorter")


@reg
def len_of(c, t):
    return _int(t, c.get("unit")) == c["lens"][c["item"]]


@reg
def len_is(c, t):
    hits = [k for k, v in c["lens"].items() if v == c["n"]]
    return len(hits) == 1 and V["norm"](t) == V["norm"](hits[0])


# ---------------------------------------------------------------- time
@reg
def clock_say(c, t):
    """'3 o'clock' or 'half past 3' for (h, m) with m in {0, 30}; digital form 'h:mm' also accepted when c['digital']."""
    w = V["norm"](t).replace("’", "'")
    h, m = c["h"], c["m"]
    if c.get("digital") and re.fullmatch(r"\d{1,2}:\d{2}", w):
        a, b = w.split(":")
        return int(a) == h and int(b) == m
    return w == (f"{h} o'clock" if m == 0 else f"half past {h}" if m == 30 else None)


@reg
def later_time(c, t):
    """Time (h:mm) that is c['add'] minutes after h:m on a 12-hour clock."""
    tot = (c["h"] % 12) * 60 + c["m"] + c["add"]
    hh, mm = divmod(tot % 720, 60)
    hh = 12 if hh == 0 else hh
    m_ = re.fullmatch(r"(\d{1,2}):(\d{2})", str(t).strip())
    return bool(m_) and int(m_.group(1)) == hh and int(m_.group(2)) == mm


@reg
def hour_hand(c, t):
    """Where the hour hand points: at h (o'clock) or between h and h+1 (half past)."""
    w = V["norm"](t)
    h, m = c["h"], c["m"]
    nx = h % 12 + 1
    return w == (f"at the {h}" if m == 0 else f"between the {h} and the {nx}")


# ---------------------------------------------------------------- data
@reg
def data_q(c, t):
    """counts: {category: n}. q: value(a) | total | diff(a, b) | most | least | sum(a, b)."""
    cnt, q = c["counts"], c["q"]
    if q in ("most", "least"):
        v = (max if q == "most" else min)(cnt.values())
        cats = [k for k, x in cnt.items() if x == v]
        return len(cats) == 1 and V["norm"](t) == V["norm"](cats[0])
    want = {"value": lambda: cnt[c["a"]], "total": lambda: sum(cnt.values()), "diff": lambda: abs(cnt[c["a"]] - cnt[c["b"]]),
            "sum": lambda: cnt[c["a"]] + cnt[c["b"]]}[q]()
    return _int(t, c.get("unit")) == want


@reg
def list_count(c, t):
    return _int(t) == c["items"].count(c["want"])


@reg
def tally_say(c, t):
    m = re.fullmatch(r"(\d+) bundles? of 5(?: and (\d+) more marks?)?", str(t).strip())
    if not m:
        return False
    b, o = int(m.group(1)), int(m.group(2) or 0)
    return o < 5 and 5 * b + o == c["n"]


@reg
def tally_parts(c, t):
    return _int(t) == 5 * c["b"] + c["o"]


# ---------------------------------------------------------------- shapes
SIDES = {"triangle": 3, "triangle2": 3, "square": 4, "rectangle": 4, "trapezoid": 4, "rhombus": 4, "hexagon": 6, "pentagon": 5,
         "circle": 0, "oval": 0, "halfcircle": 1, "quartercircle": 2}
SHAPE_NAME = {"triangle": "triangle", "triangle2": "triangle", "square": "square", "rectangle": "rectangle", "trapezoid": "trapezoid",
              "rhombus": "rhombus", "hexagon": "hexagon", "pentagon": "pentagon", "circle": "circle", "halfcircle": "half-circle",
              "quartercircle": "quarter-circle", "cube": "cube", "prism": "rectangular prism", "cylinder": "cylinder", "cone": "cone",
              "sphere": "sphere"}
CORNERS = {"triangle": 3, "triangle2": 3, "square": 4, "rectangle": 4, "trapezoid": 4, "rhombus": 4, "hexagon": 6, "pentagon": 5,
           "circle": 0, "oval": 0, "halfcircle": 2, "quartercircle": 3}


@reg
def shape_name(c, t):
    return V["norm"](t) == SHAPE_NAME[c["kind"]]


@reg
def shape_count(c, t):
    """Number of sides (straight) or corners of a named shape kind."""
    tab = SIDES if c["what"] == "sides" else CORNERS
    return _int(t, c.get("unit")) == tab[c["kind"]]


@reg
def shape_label(c, t):
    """Label of the one item in c['items'] that matches c['rule'] (kind in rule['kinds'], closed unless rule allows)."""
    ok = [it["label"] for it in c["items"] if it["kind"] in c["rule"]["kinds"] and not it.get("open")]
    return len(ok) == 1 and V["norm"](t) == V["norm"](ok[0])


COMPOSE_PIECES = {"square_tri2": ("triangle", 2), "square_tri4": ("triangle", 4), "rect_sq2": ("square", 2), "rect_sq3": ("square", 3),
                  "square_sq4": ("square", 4), "rect_tri2": ("triangle", 2), "square_rect2": ("rectangle", 2), "hex_tri6": ("triangle", 6),
                  "hex_trap2": ("trapezoid", 2), "trap_tri3": ("triangle", 3), "circle_half2": ("half-circle", 2),
                  "circle_quarter4": ("quarter-circle", 4), "rhombus_tri2": ("triangle", 2)}
COMPOSE_WHOLE = {"square_tri2": "square", "square_tri4": "square", "rect_sq2": "rectangle", "rect_sq3": "rectangle", "square_sq4": "square",
                 "rect_tri2": "rectangle", "square_rect2": "square", "hex_tri6": "hexagon", "hex_trap2": "hexagon", "trap_tri3": "trapezoid",
                 "circle_half2": "circle", "circle_quarter4": "circle", "rhombus_tri2": "rhombus"}


@reg
def compose_count(c, t):
    return _int(t, c.get("unit")) == COMPOSE_PIECES[c["name"]][1] * c.get("copies", 1)


@reg
def compose_whole(c, t):
    return V["norm"](t) == COMPOSE_WHOLE[c["name"]]


@reg
def solid_lbl(c, t):
    hits = [it["label"] for it in c["items"] if it["kind"] == c["want"]]
    return len(hits) == 1 and V["norm"](t) == V["norm"](hits[0])


# ---------------------------------------------------------------- equal shares
def _equal(c):
    if c.get("n"):
        return True
    if c.get("widths"):
        return len(set(c["widths"])) == 1
    if c.get("angles"):
        return len(set(c["angles"])) == 1
    return c.get("cuts") in ("grid", "diag2", "diag4")


def _parts(c):
    if c.get("n"):
        return c["n"]
    if c.get("widths"):
        return len(c["widths"])
    if c.get("angles"):
        return len(c["angles"])
    if c.get("cuts") == "grid":
        return c["rows"] * c["cols"]
    return {"diag2": 2, "diag4": 4}[c["cuts"]]


@reg
def share_word(c, t):
    """halves / fourths for equal shares, 'not equal shares' otherwise."""
    w = V["norm"](t)
    if not _equal(c):
        return w == "not equal shares"
    return w == {2: "halves", 4: "fourths"}.get(_parts(c))


@reg
def share_of(c, t):
    """'half of' / 'fourth of' / 'quarter of' the shape for ONE equal share (c: partition data)."""
    w = V["norm"](t)
    if not _equal(c):
        return False
    n = _parts(c)
    return (n == 2 and w in ("half of the shape", "one half of the shape")) or (n == 4 and w in ("a fourth of the shape", "a quarter of the shape", "one fourth of the shape"))


@reg
def shares_left(c, t):
    return _int(t) == {"halves": 2, "fourths": 4}[c["word"]] - c["eaten"]


@reg
def share_n(c, t):
    return _equal(c) and _int(t) == _parts(c)


@reg
def pair_equal(c, t):
    ea, eb = _equal(c["a"]), _equal(c["b"])
    w = V["norm"](t)
    want = "both shapes" if ea and eb else "neither shape" if not (ea or eb) else ("shape a" if ea else "shape b")
    return w == want


@reg
def smaller_piece(c, t):
    a, b = c["a"], c["b"]
    if a == b:
        return V["norm"](t).startswith("they are the same")
    return V["norm"](t) == V["norm"](c["names"][0] if a > b else c["names"][1])


@reg
def shares_whole(c, t):
    """How many equal shares make the whole for halves (2) or fourths (4)."""
    return _int(t, c.get("unit")) == {"halves": 2, "fourths": 4, "quarters": 4}[c["word"]]


@reg
def bigger_piece(c, t):
    """Which is bigger: a half or a fourth of the same whole (or same size)."""
    w = V["norm"](t)
    a, b = c["a"], c["b"]                     # numbers of equal shares
    if a == b:
        return w.startswith("they are the same")
    big = c["names"][0] if a < b else c["names"][1]
    return w == V["norm"](big)
