"""Grade 3 named checks for verify.py. Independent of the families and of g3lib: each check recomputes the answer from
the stored check data (which is the data the question and its diagram were drawn from) with its own arithmetic.
bind() gives access to the generic helpers in verify.py (parse_value, eval_expr, norm, accepts)."""
import re
from fractions import Fraction as F
from math import gcd

V = {}


def bind(g):
    V.update(g)


def pv(t):
    x = V["parse_value"](t)
    return None if x is None else x[0]


def num_only(t):
    return re.fullmatch(r"[\d,]+", str(t).strip()) is not None


# ---------------------------------------------------------------- unit 1-5 (operations)
def repadd_groups(c, t):
    adds = [int(x) for x in c["sum"].split("+")]
    return num_only(t) and all(a == c["addend"] for a in adds) and pv(t) == len(adds)


def skip_missing(c, t):
    parts = [x.strip() for x in c["seq"].split(",")]
    k = parts.index("?")
    known = [(i, int(x)) for i, x in enumerate(parts) if x != "?"]
    step = c["step"]
    assert all(b - a == step * (j - i) for (i, a), (j, b) in zip(known, known[1:])), "sequence is not arithmetic"
    i0, v0 = known[0]
    return num_only(t) and pv(t) == v0 + (k - i0) * step


def repadd_value(c, t):
    return num_only(t) and pv(t) == sum(int(x) for x in c["sum"].split("+"))


def repsub_groups(c, t):
    lhs = c["expr"].split("=")[0].split("−")
    start, subs = int(lhs[0]), [int(x) for x in lhs[1:]]
    assert len(set(subs)) == 1 and start - sum(subs) == 0
    return num_only(t) and pv(t) == len(subs)


def blank_eq(c, t):
    """Put the answer into the blank and check that both sides of the equation are equal (verify.py arithmetic)."""
    if c.get("unit"):
        if not _unit_ok(c, t):
            return False
    elif not num_only(t):
        return False
    lhs, rhs = c["eq"].replace("___", str(pv(t))).split("=")
    try:
        return V["eval_expr"](lhs) == V["eval_expr"](rhs)
    except ZeroDivisionError:
        return False


def _eq_true(text):
    sides = str(text).replace("?", "").split("=")
    if len(sides) != 2:
        return None
    try:
        return V["eval_expr"](sides[0]) == V["eval_expr"](sides[1])
    except Exception:
        return False


def true_eq(c, t):
    """Option is an equation 'A = B' that is true."""
    return _eq_true(t) is True


def false_eq(c, t):
    """'Which is NOT …' items: the correct option is the one false equation."""
    return _eq_true(t) is False


def strategy(c, t):
    """'5 × 6 plus 1 × 6', 'double 4 × 7', '10 × 6 minus 1 × 6' must equal the target product."""
    e = str(t).replace(" plus ", " + ").replace(" minus ", " − ")
    e = re.sub(r"double (\d+ × \d+)", r"2 × (\1)", e)
    try:
        return V["eval_expr"](e) == V["eval_expr"](c["target"])
    except Exception:
        return False


def _rnd(n, place):
    s = 10 if place == "tens" else 100
    q, rem = divmod(n, s)
    return (q + (1 if rem * 2 >= s else 0)) * s


def _unit_ok(c, t):
    x = V["parse_value"](t)
    if x is None:
        return False
    return (not c.get("unit")) or V["unorm"](x[1]) == V["unorm"](c["unit"]) or not x[1]


def round_to(c, t):
    return _unit_ok(c, t) and pv(t) == _rnd(int(c["x"]), c["place"])


def rounds_to(c, t):
    return num_only(t) and _rnd(int(pv(t)), c["place"]) == int(c["target"])


def round_extreme(c, t):
    s = 10 if c["place"] == "tens" else 100
    T = int(c["target"])
    cands = [n for n in range(max(0, T - s), T + s) if _rnd(n, c["place"]) == T]
    return num_only(t) and pv(t) == (max(cands) if c["which"] == "greatest" else min(cands))


def missing_digit(c, t):
    if not re.fullmatch(r"\d", str(t).strip()):
        return False
    a = int(c["shown"].replace("□", str(t).strip()))
    return (a + c["other"] if c["op"] == "+" else a - c["other"]) == c["total"]


def estimate(c, t):
    ra, rb = _rnd(c["a"], c["place"]), _rnd(c["b"], c["place"])
    return _unit_ok(c, t) and pv(t) == (ra + rb if c["op"] == "+" else ra - rb)


def estimate3(c, t):
    return _unit_ok(c, t) and pv(t) == _rnd(c["a"], "hundreds") + _rnd(c["b"], "hundreds") - _rnd(c["c"], "hundreds")


def reasonable(c, t):
    exact = c["a"] + c["b"] if c["op"] == "+" else c["a"] - c["b"]
    est = _rnd(c["a"], "hundreds") + (_rnd(c["b"], "hundreds") if c["op"] == "+" else -_rnd(c["b"], "hundreds"))
    t = str(t)
    nums = [int(x.replace(",", "")) for x in re.findall(r"\d[\d,]*", t)]
    if c["shown"] == exact:
        return t.startswith("Yes.") and est in nums and abs(est - exact) < 100
    return t.startswith("No.") and est in nums and abs(c["shown"] - est) >= 100


def chain_unknown(c, t):
    box = F(c["P"], c["a"])
    return num_only(t) and box.denominator == 1 and pv(t) == c["s"] - box


def lead_num(c, t):
    m = re.match(r"(\d+),", str(t))
    return bool(m) and blank_eq({"eq": c["eq"]}, m.group(1))


def greatest_product(c, t):
    vals = [V["eval_expr"](o) for o in c["opts"]]
    if str(t).startswith("They are equal"):
        return len(set(vals)) == 1
    try:
        v = V["eval_expr"](t)
    except Exception:
        return False
    return v == max(vals) and vals.count(v) == 1 and str(t).replace(" × ", "*") in c["opts"]


def table_step(c, t):
    return num_only(t) and pv(t) == (c["col"] if c["op"] == "×" else 1)


def table_cell(c, t):
    return num_only(t) and pv(t) == (c["row"] * c["col"] if c["op"] == "×" else c["row"] + c["col"])


def _lhs(eq):
    return V["eval_expr"](eq.rsplit("=", 1)[0])


def letter_eq(c, t):
    """Equation options '… = c': the left side must equal the value of the unknown. Solve items: answer = left side of c['eq']."""
    if c.get("eq"):
        return _unit_ok(c, t) and pv(t) == _lhs(c["eq"])
    try:
        return _lhs(t) == c["value"]
    except Exception:
        return False


def reasonable2(c, t):
    est = _rnd(c["b"], "hundreds") + _rnd(c["c"], "tens")
    nums = [int(x.replace(",", "")) for x in re.findall(r"\d[\d,]*", str(t))]
    ok = c["shown"] == c["b"] + c["c"]
    return str(t).startswith("Yes." if ok else "No.") and est in nums


def units_in_whole(c, t):
    return num_only(t) and pv(t) == c["d"]


def copies(c, t):
    return num_only(t) and pv(t) * F(1, c["d"]) == F(c["n"], c["d"])


def point_at(c, t):
    hits = [p["label"] for p in c["points"] if p["n"] == c["n"]]
    if str(t).strip() == "none of them":
        return not hits
    return hits == [str(t).strip()]


def jumps_between(c, t):
    return num_only(t) and pv(t) == c["a2"] - c["a1"]


def _fr(t):
    m = re.fullmatch(r"\s*(\d+)/(\d+)\s*", str(t))
    return (int(m.group(1)), int(m.group(2))) if m else None


def frac_text(c, t):
    x = _fr(t)
    return bool(x) and x[1] == c["d"] and F(*x) == F(c["n"], c["d"])


def equiv_num(c, t):
    return _unit_ok(c, t) and F(int(pv(t)), c["d"]) == F(c["a"], c["b"])


def equiv_pair(c, t):
    m = re.fullmatch(r"(\d+/\d+) and (\d+/\d+)", str(t).strip())
    return bool(m) and F(m.group(1)) == F(m.group(2))


def equiv_blank(c, t):
    if not num_only(t):
        return False
    lhs, rhs = [x.strip().replace("?", str(int(pv(t)))) for x in c["q"].split("=")]
    try:
        return F(lhs) == F(rhs) and F(rhs).denominator > 0
    except (ZeroDivisionError, ValueError):
        return False


def equiv_to(c, t):
    return _fr(t) is not None and F(t.strip()) == F(c["target"])


def wholes_of(c, t):
    return num_only(t) and pv(t) == F(c["n"], c["d"])


def equals_whole(c, t):
    return _fr(t) is not None and F(t.strip()) == c["n"]


def pick_greater(c, t):
    a, b = F(c["a"]), F(c["b"])
    if str(t).startswith("They are equal"):
        return a == b
    if str(t).startswith("You cannot tell"):
        return False
    return _fr(t) is not None and F(t.strip()) == max(a, b) and a != b and t.strip() in (c["a"], c["b"])


def order_fracs(c, t):
    got = [x.strip() for x in str(t).split(",")]
    want = sorted(c["values"], key=F, reverse=c.get("desc", False))
    return sorted(got) == sorted(c["values"]) and [F(x) for x in got] == [F(x) for x in want]


def who_more(c, t):
    best = max(c["people"].values(), key=F)
    winners = [k for k, v in c["people"].items() if F(v) == F(best)]
    return len(winners) == 1 and str(t).strip() == winners[0]


def group_of(c, t):
    m = re.fullmatch(r"the group of (\d+)", V["norm"](t))
    return bool(m) and F(1, int(m.group(1))) == max(F(1, c["b"]), F(1, c["d"])) and c["b"] != c["d"]


def wholes_parts(c, t):
    return num_only(t) and F(int(pv(t)), c["d"]) == c["n"]


def _t(text):
    m = re.fullmatch(r"\s*(\d{1,2}):(\d{2})\s*", str(text))
    if not m:
        return None
    h, mi = int(m.group(1)), int(m.group(2))
    return (h, mi) if 1 <= h <= 12 and mi < 60 else None


def _tmin(text):
    h, m = _t(text)
    return (h % 12) * 60 + m


def clock(c, t):
    return _t(t) == (c["h"], c["m"])


def clock_lead(c, t):
    return clock(c, str(t).split(".")[0])


def until_hour(c, t):
    return _unit_ok({"unit": "minutes"}, t) and pv(t) == 60 - c["m"]


def hour_hand(c, t):
    f = F(c["m"], 60)
    h, nxt = c["h"], c["h"] % 12 + 1
    want = f"just past the {h}" if f < F(1, 4) else f"about halfway between the {h} and the {nxt}" if F(2, 5) <= f <= F(3, 5) else f"almost at the {nxt}" if f > F(3, 4) else None
    return want is not None and str(t).strip() == want


def elapsed(c, t):
    d = (_tmin(c["b"]) - _tmin(c["a"])) % 720
    return _unit_ok(c, t) and pv(t) == d


def end_time(c, t):
    if _t(t) is None:
        return False
    if c.get("rev"):
        return (_tmin(c["rev"]) - _tmin(t)) % 720 == c["d"]
    return (_tmin(t) - _tmin(c["a"])) % 720 == c["d"]


def longer(c, t):
    p = c["people"]
    if str(t).startswith("They practiced the same"):
        return len(set(p.values())) == 1
    m = re.fullmatch(r"(\w+), by (\d+) minutes", str(t).strip())
    if not m:
        return False
    best = max(p, key=p.get)
    return m.group(1) == best and int(m.group(2)) == max(p.values()) - min(p.values())


def read_scale(c, t):
    assert c["v"] % c["st"] == 0 and 0 < c["v"] <= c["mx"]
    return _unit_ok(c, t) and pv(t) == c["v"]


def _syms(c):
    return [F(x) for x in c["syms"]]


def pic_value(c, t):
    return _unit_ok(c, t) and pv(t) == _syms(c)[c["i"]] * c["key"]


def pic_diff(c, t):
    s = _syms(c)
    return _unit_ok(c, t) and pv(t) == (s[c["i"]] - s[c["j"]]) * c["key"]


def pic_sum(c, t):
    s = _syms(c)
    return _unit_ok(c, t) and pv(t) == sum(s[i] for i in c["idx"]) * c["key"]


def pic_most(c, t):
    s = _syms(c)
    return s.count(max(s)) == 1 and str(t).strip() == c["cats"][s.index(max(s))]


def bar_value(c, t):
    return _unit_ok(c, t) and pv(t) == c["vals"][c["i"]]


def bar_diff(c, t):
    return _unit_ok(c, t) and pv(t) == c["vals"][c["i"]] - c["vals"][c["j"]]


def bar_combo(c, t):
    v = c["vals"]
    return _unit_ok(c, t) and pv(t) == sum(v[i] for i in c["plus"]) - sum(v[i] for i in c["minus"])


def bar_has(c, t):
    hits = [k for k, v in zip(c["cats"], c["vals"]) if v == c["v"]]
    return hits == [str(t).strip()]


def bar_scale(c, t):
    return num_only(t) and pv(t) == c["scale"]


def symbols_for(c, t):
    x = V["parse_value"](t)
    return x is not None and x[0] * c["key"] == c["v"] and (x[0] * 2).denominator == 1


def bar_end(c, t):
    return num_only(t) and pv(t) == c["v"]


def spaces_for(c, t):
    return num_only(t) and pv(t) * c["scale"] == c["v"]


def key_whole(c, t):
    m = re.fullmatch(r"each symbol = (\d+)", str(t).strip())
    return bool(m) and all(v % int(m.group(1)) == 0 for v in c["vals"])


def row_for(c, t):
    m = re.fullmatch(r"(\d+) whole symbols?(?: and 1 half symbol)?", str(t).strip())
    if not m:
        return False
    n = F(int(m.group(1))) + (F(1, 2) if "half" in t else 0)
    return n * c["key"] == c["v"]


def _mx(s):
    s = str(s).strip()
    if " " in s:
        w, f = s.split(" ")
        return int(w) + F(f)
    return F(s)


def measure(c, t):
    x = V["parse_value"](t)
    return x is not None and V["unorm"](x[1]) == V["unorm"]("inches") and x[0] == _mx(c["end"]) - _mx(c["start"]) and (x[0] * 4).denominator == 1


def parts_in(c, t):
    q = c["q"]
    unit = F(1, 4) if "quarter" in q else F(1, 2)
    m = re.search(r"in (1|2|3) inch|in a half inch", q)
    whole = F(1, 2) if "a half inch" in q else int(re.search(r"in (\d+) inch", q).group(1))
    return num_only(t) and pv(t) == whole / unit


def ruler_mark(c, t):
    q = c["q"]
    x = V["parse_value"](t)
    if x is None:
        return False
    nums = [int(n) for n in re.findall(r"\d+", q)]
    if "halfway" in q:
        want = F(nums[0] + nums[1], 2)
    elif "past" in q:
        want = nums[-1] + F(1, 4)
    else:
        want = nums[-1] - F(1, 4)
    return x[0] == want


def scale_marks(c, t):
    dens = {F(v.split(" ")[-1]).denominator if "/" in v else 1 for v in c["values"]}
    need = 4 if 4 in dens else 2 if 2 in dens else 1
    return str(t).strip() == {4: "in quarter inches", 2: "in half inches", 1: "in whole inches"}[need]


def cells(c, t):
    n = len({tuple(x) for x in c["cells"]}) if "cells" in c else c["count"]
    return _unit_ok(c, t) and V["parse_value"](t)[1] != "" and pv(t) == n


def _shoelace(pts):
    s = 0
    for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
        s += x1 * y2 - x2 * y1
    return F(abs(s), 2)


def poly_area(c, t):
    return _unit_ok(c, t) and V["parse_value"](t)[1] != "" and pv(t) == _shoelace(c["pts"])


def expr_poly_area(c, t):
    try:
        return V["eval_expr"](t) == _shoelace(c["pts"])
    except Exception:
        return False


def pair_sum(c, t):
    parts = str(t).split(" and ")
    if len(parts) != 2:
        return False
    try:
        return sum(V["eval_expr"](p) for p in parts) == V["eval_expr"](c["target"]) and all("×" in p for p in parts)
    except Exception:
        return False


def grid_perim(c, t):
    cs = {tuple(x) for x in c["cells"]}
    p = sum(1 for (i, j) in cs for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)) if (i + di, j + dj) not in cs)
    return _unit_ok(c, t) and pv(t) == p


def lead_side(c, t):
    m = re.match(r"(\d+) units\.", str(t))
    return bool(m) and int(m.group(1)) == c["P"] - sum(c["known"]) and "subtract" in str(t)


def _wh(t):
    m = re.fullmatch(r"(\d+) by (\d+)", str(t).strip())
    return (int(m.group(1)), int(m.group(2))) if m else None


def same_perim(c, t):
    x = _wh(t)
    return bool(x) and 2 * sum(x) == 2 * (c["w"] + c["h"]) and set(x) != {c["w"], c["h"]}


def same_area(c, t):
    x = _wh(t)
    return bool(x) and x[0] * x[1] == c["w"] * c["h"] and set(x) != {c["w"], c["h"]}


def bigger_area(c, t):
    a, b = c["A"][0] * c["A"][1], c["B"][0] * c["B"][1]
    return a != b and str(t).strip() == ("A" if a > b else "B")


def _perim_rects(P):
    return [(w, P // 2 - w) for w in range(1, P // 2) if w <= P // 2 - w]


def count_rects(c, t):
    return num_only(t) and pv(t) == len(_perim_rects(c["P"]))


def max_area(c, t):
    return _unit_ok(c, t) and pv(t) == max(w * h for w, h in _perim_rects(c["P"]))


def min_perim(c, t):
    A = c["A"]
    return _unit_ok(c, t) and pv(t) == min(2 * (w + A // w) for w in range(1, A + 1) if A % w == 0)


def _classify(pts):
    n = len(pts)
    if n != 4:
        return {3: {"triangle"}, 5: {"pentagon"}, 6: {"hexagon"}}[n]
    d2 = [(pts[(i + 1) % 4][0] - pts[i][0]) ** 2 + (pts[(i + 1) % 4][1] - pts[i][1]) ** 2 for i in range(4)]
    dots = []
    for i in range(4):
        a, b, c_ = pts[i - 1], pts[i], pts[(i + 1) % 4]
        dots.append((a[0] - b[0]) * (c_[0] - b[0]) + (a[1] - b[1]) * (c_[1] - b[1]))
    out = {"quadrilateral"}
    if len(set(d2)) == 1:
        out.add("rhombus")
    if all(x == 0 for x in dots):
        out.add("rectangle")
    if "rhombus" in out and "rectangle" in out:
        out.add("square")
    return out


def shape_pick(c, t):
    cls = [_classify(p) for p in c["shapes"]]
    w = c["want"]
    test = {"not_quad": lambda s: "quadrilateral" not in s, "square": lambda s: "square" in s, "rhombus": lambda s: "rhombus" in s, "rectangle": lambda s: "rectangle" in s,
            "rhombus_not_square": lambda s: "rhombus" in s and "square" not in s, "rectangle_not_square": lambda s: "rectangle" in s and "square" not in s,
            "neither": lambda s: "quadrilateral" in s and not ({"rhombus", "rectangle", "square"} & s)}[w]
    hits = ["ABCD"[i] for i, s in enumerate(cls) if test(s)]
    return hits == [str(t).strip()]


def _part_areas(sp):
    s = sp["shape"]
    if s in ("rect", "square"):
        if sp["cuts"] == "v":
            return [F(w) for w in sp["widths"]]
        if sp["cuts"] == "grid":
            return [F(1)] * (sp["rows"] * sp["cols"])
        return [F(1)] * (2 if sp["cuts"] == "diag2" else 4)
    if s == "circle":
        return [F(a) for a in sp["angles"]] if sp.get("angles") else [F(1)] * sp["n"]
    if s == "hexagon":
        return [F(1)] * {"tri6": 6, "rhomb3": 3, "trap2": 2}[sp["cuts"]]
    if s == "triangle":
        return [F(1), F(1)] if sp["cuts"] == "mid2" else [F(32), F(68)]
    raise KeyError(s)


def partition_frac(c, t):
    a = _part_areas(c["spec"])
    assert len(set(a)) == 1, "partition is not equal"
    x = _fr(t)
    return bool(x) and F(*x) == F(len(c["shade"]), len(a))


def partition_equal(c, t):
    eq = len(set(_part_areas(c["spec"]))) == 1
    return str(t).startswith("Yes." if eq else "No.") and ("not" in str(t)) != eq


FNS = {"grid_perim": grid_perim, "lead_side": lead_side, "same_perim": same_perim, "same_area": same_area, "bigger_area": bigger_area, "count_rects": count_rects,
       "max_area": max_area, "min_perim": min_perim, "shape_pick": shape_pick, "partition_frac": partition_frac, "partition_equal": partition_equal, "cells": cells, "poly_area": poly_area, "expr_poly_area": expr_poly_area, "pair_sum": pair_sum, "pic_value": pic_value, "pic_diff": pic_diff, "pic_sum": pic_sum, "pic_most": pic_most, "bar_value": bar_value, "bar_diff": bar_diff, "bar_combo": bar_combo,
       "bar_has": bar_has, "bar_scale": bar_scale, "symbols_for": symbols_for, "bar_end": bar_end, "spaces_for": spaces_for, "key_whole": key_whole, "row_for": row_for,
       "measure": measure, "parts_in": parts_in, "ruler_mark": ruler_mark, "scale_marks": scale_marks, "clock": clock, "clock_lead": clock_lead, "until_hour": until_hour, "hour_hand": hour_hand, "elapsed": elapsed, "end_time": end_time,
       "longer": longer, "read_scale": read_scale, "wholes_parts": wholes_parts, "frac_text": frac_text, "equiv_num": equiv_num, "equiv_pair": equiv_pair, "equiv_blank": equiv_blank, "equiv_to": equiv_to,
       "wholes_of": wholes_of, "equals_whole": equals_whole, "pick_greater": pick_greater, "order_fracs": order_fracs, "who_more": who_more, "group_of": group_of, "units_in_whole": units_in_whole, "copies": copies, "point_at": point_at, "jumps_between": jumps_between, "chain_unknown": chain_unknown, "lead_num": lead_num, "greatest_product": greatest_product, "table_step": table_step, "table_cell": table_cell,
       "letter_eq": letter_eq, "reasonable2": reasonable2, "round_to": round_to, "rounds_to": rounds_to, "round_extreme": round_extreme, "missing_digit": missing_digit,
       "estimate": estimate, "estimate3": estimate3, "reasonable": reasonable, "true_eq": true_eq, "false_eq": false_eq, "strategy": strategy, "blank_eq": blank_eq, "repsub_groups": repsub_groups, "repadd_value": repadd_value, "repadd_groups": repadd_groups, "skip_missing": skip_missing}
