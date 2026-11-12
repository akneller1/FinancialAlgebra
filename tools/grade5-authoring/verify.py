"""Independent verifier for the Grade 5 (math5) banks.

It never imports the families or g5lib. It reads the published bank JSON plus the check file
(tools/grade5-authoring/out/<unit>.checks.json) and re-derives every answer, every multiple-choice and
select-all option, every open-response part, and every true/false claim from the stored check data, using its
own arithmetic (exact fractions) and its own implementations of the named checks.

Usage: python3 verify.py [repo_root]    -> prints a report, exits 1 on any error.
"""
import json, os, re, subprocess, sys
from collections import Counter, defaultdict
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
from outline import UNITS, COURSE_ID, skill_records  # outline is data only

# ------------------------------------------------------------------ parsing what students see
NUM = r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?"


def pnum(t):
    t = t.replace(",", "").strip()
    return F(t)


def parse_value(text):
    """'$4.50' '1,250' '3.45' '2 1/3' '7/4' '24 cubic units' -> (Fraction, unit or '')."""
    s = str(text).strip().replace("−", "-")
    m = re.fullmatch(r"\$?(-?(?:" + NUM + r"))(?:\s+(\d+)/(\d+))?(?:/(\d+))?\s*(.*)", s)
    if not m:
        return None
    a, wn, wd, d2, unit = m.groups()
    v = pnum(a)
    if wn:
        if "." in a:
            return None
        v = v + F(int(wn), int(wd))
    elif d2:
        if "." in a:
            return None
        v = v / int(d2)
    if s.startswith("$"):
        unit = "$" + (" " + unit if unit else "")
    return v, unit.strip()


def form_ok(text, form):
    s = str(text).strip()
    core = re.sub(r"^\$", "", s).split(" ")
    if form == "mixed":   # simplest: whole or proper fraction or mixed number with proper simplified fraction
        m = re.fullmatch(r"(?:(\d[\d,]*) )?(\d+)/(\d+)(?:\s+\D.*)?", s)
        if not m:
            return re.fullmatch(r"\$?-?[\d,]+(?:\s+\D.*)?", s) is not None
        w, n, d = m.groups()
        n, d = int(n), int(d)
        from math import gcd
        return n < d and gcd(n, d) == 1
    if form == "frac":    # simplest fraction (improper allowed) or whole
        m = re.fullmatch(r"(\d+)/(\d+)(?:\s+\D.*)?", s)
        if not m:
            return re.fullmatch(r"-?[\d,]+(?:\s+\D.*)?", s) is not None
        from math import gcd
        return gcd(int(m.group(1)), int(m.group(2))) == 1
    if form == "dec":
        return "/" not in s
    if form == "whole":
        return re.fullmatch(r"\$?[\d,]+(?:\s+\D.*)?", s) is not None
    if form == "money":
        return re.fullmatch(r"\$[\d,]+\.\d\d", s) is not None
    return True


def eval_expr(e):
    e = re.sub(r"(?<=\d),(?=\d{3})", "", str(e)).replace("[", "(").replace("]", ")").replace("{", "(").replace("}", ")").replace("−", "-")
    src = re.sub(r"(\d+(?:\.\d+)?)", r'F("\1")', e.replace("×", "*").replace("÷", "/").replace("^", "**"))
    return F(eval(src, {"__builtins__": {}}, {"F": F}))


def unorm(u):
    u = norm(u).replace("feet", "foot")
    u = re.sub(r"(ch|sh|x|bus)es\b", r"\1", u)
    u = re.sub(r"ves\b", "f", u)
    return re.sub(r"s\b", "", u)


def norm(t):
    return re.sub(r"\s+", " ", str(t).strip().lower().replace(",", "").replace("\u2011", "-").rstrip("."))


# ------------------------------------------------------------------ named checks (own implementations)
PLACE_EXP = {"thousands": 3, "hundreds": 2, "tens": 1, "ones": 0, "tenths": -1, "hundredths": -2, "thousandths": -3,
             "ten thousands": 4, "hundred thousands": 5, "millions": 6, "whole number": 0}


def rnd(x, place):
    q = Decimal(1).scaleb(PLACE_EXP[place]) if PLACE_EXP[place] < 0 else Decimal(10) ** PLACE_EXP[place]
    d = Decimal(x.numerator) / Decimal(x.denominator)
    return F(str((d / q).quantize(Decimal(1), rounding=ROUND_HALF_UP) * q))


def tri_class(sides=None, angles=None, by="sides"):
    if by == "sides":
        a, b, c = sorted(sides)
        return "equilateral" if a == c else "isosceles" if a == b or b == c else "scalene"
    m = max(angles)
    return "right" if m == 90 else "obtuse" if m > 90 else "acute"


def quad_names(q):
    """q: dict with booleans parallel_pairs (0,1,2), all_sides_equal, right_angles(bool), adj_pairs_equal (kite)."""
    out = {"quadrilateral"}
    if q["parallel_pairs"] >= 1:
        out.add("trapezoid")          # inclusive definition (at least one pair), as used in the MA framework progression
    if q["parallel_pairs"] == 2:
        out.add("parallelogram")
        if q["right_angles"]:
            out.add("rectangle")
        if q["all_sides_equal"]:
            out.add("rhombus")
        if q["right_angles"] and q["all_sides_equal"]:
            out.add("square")
    if q.get("kite") or q["all_sides_equal"]:
        out.add("kite")
    return out


def accepts(chk, text, item=None):
    """Is `text` a correct answer for this check?"""
    k = chk["k"]
    if k == "expr":
        pv = parse_value(text)
        if pv is None:
            return False
        v, unit = pv
        want = eval_expr(chk["e"])
        if v != want:
            return False
        if chk.get("unit") is not None and unorm(unit) != unorm(chk["unit"]):
            return False
        if chk.get("unit") is None and unit and not unit.startswith("$"):
            pass
        return form_ok(text, chk.get("form"))
    if k == "key":
        return norm(text) in [norm(a) for a in chk["accept"]]
    if k == "fn":
        return FNS[chk["fn"]](chk, text)
    raise KeyError(k)


def fn_tf(c, text):
    inner, shown, ans = c["inner"], c["shown"], c["answer"]
    shown_ok = accepts(inner, shown)
    assert accepts(inner, ans), "tf: stored answer rejected"
    t = text.strip()
    if t.startswith("True."):
        return shown_ok
    m = re.match(r"False\. The correct answer is (.+)\.$", t)
    if m:
        return (not shown_ok) and accepts(inner, m.group(1))
    return False


def fn_claims(c, text):
    e = c["table"][text]
    return accepts(e["inner"], e["shown"])


def fn_compare(c, text):
    a, b = eval_expr(c["a"]), eval_expr(c["b"])
    sym = "<" if a < b else ">" if a > b else "="
    return text.strip() == sym or norm(text) == norm(c.get("fmt", "{a} {s} {b}").format(a=c.get("at", ""), b=c.get("bt", ""), s=sym))


def fn_round(c, text):
    pv = parse_value(text)
    return pv is not None and pv[0] == rnd(eval_expr(c["x"]), c["place"]) and "/" not in text


def fn_order(c, text):
    vals = [eval_expr(v) for v in c["values"]]
    shown = [s.strip() for s in text.split(",")]
    if len(shown) != len(vals):
        return False
    try:
        pv = [parse_value(s)[0] for s in shown]
    except TypeError:
        return False
    want = sorted(vals, reverse=c.get("desc", False))
    return pv == want and sorted(pv) == sorted(vals)


def fn_digit_value(c, text):
    """value of the digit at `place` in number `n` (string)."""
    n = c["n"]
    intpart, _, frac_ = n.replace(",", "").partition(".")
    e = PLACE_EXP[c["place"]]
    dg = int(intpart[len(intpart) - 1 - e]) if e >= 0 else int(frac_[-e - 1])
    pv = parse_value(text)
    return pv is not None and pv[0] == dg * F(10) ** e


def fn_place_of(c, text):
    n = c["n"].replace(",", "")
    intpart, _, frac_ = n.partition(".")
    d = c["digit"]
    pos = [k for k in PLACE_EXP if k not in ("whole number",)]
    for p in pos:
        e = PLACE_EXP[p]
        try:
            dg = intpart[len(intpart) - 1 - e] if e >= 0 else frac_[-e - 1]
        except IndexError:
            continue
        if e >= 0 and len(intpart) - 1 - e < 0:
            continue
        if dg == str(d) and norm(text) == p:
            return True
    return False


def fn_times(c, text):
    """How many times as much is digit value a than digit value b."""
    pv = parse_value(text)
    return pv is not None and pv[0] == eval_expr(c["a"]) / eval_expr(c["b"])


def fn_word_form(c, text):
    return norm(text) == norm(words_decimal(c["n"]))


ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen",
        "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def words_int(n):
    n = int(n)
    if n < 20:
        return ONES[n]
    if n < 100:
        return TENS[n // 10] + ("-" + ONES[n % 10] if n % 10 else "")
    if n < 1000:
        return ONES[n // 100] + " hundred" + (" " + words_int(n % 100) if n % 100 else "")
    return words_int(n // 1000) + " thousand" + (" " + words_int(n % 1000) if n % 1000 else "")


def words_decimal(s):
    s = s.replace(",", "")
    a, _, b = s.partition(".")
    if not b:
        return words_int(a)
    if len(b) > 3:
        return "\u0000"
    unit = {1: "tenth", 2: "hundredth", 3: "thousandth"}[len(b)]
    fw = words_int(b) + " " + unit + ("s" if int(b) != 1 else "")
    return fw if int(a) == 0 else words_int(a) + " and " + fw


def fn_expanded(c, text):
    """'3 × 10 + 4 × 1 + 5 × (1/10)' style or '30 + 4 + 0.5' : sum of terms must equal n and each term one nonzero place."""
    t = text.replace(" ", "")
    terms = t.split("+")
    try:
        tot = sum(eval_expr(x.replace("(", "(").replace(")", ")")) for x in terms)
    except Exception:
        return False
    if tot != eval_expr(c["n"].replace(",", "")):
        return False
    # every term a single digit times a power of ten, distinct places, no zero terms
    exps = []
    for x in terms:
        v = eval_expr(x)
        if v == 0:
            return False
        e = 0
        while v.denominator != 1 or v.numerator % 10 == 0:
            if v.denominator != 1:
                v *= 10
                e -= 1
            else:
                v /= 10
                e += 1
        if not (1 <= v <= 9):
            return False
        exps.append(e)
    return len(set(exps)) == len(exps)


def fn_quotient_rem(c, text):
    q, r = divmod(int(eval_expr(c["a"])), int(eval_expr(c["b"])))
    m = re.fullmatch(r"([\d,]+)(?: R ?(\d+))?", text.strip())
    if not m:
        return False
    return int(m.group(1).replace(",", "")) == q and int(m.group(2) or 0) == r


def fn_remainder_use(c, text):
    """mode: up (round quotient up), down (drop), rem (the remainder), frac (mixed number), dec."""
    a, b = int(eval_expr(c["a"])), int(eval_expr(c["b"]))
    q, r = divmod(a, b)
    want = {"up": q + (1 if r else 0), "down": q, "rem": r}.get(c["mode"])
    pv = parse_value(text)
    if pv is None:
        return False
    if c["mode"] == "frac":
        return pv[0] == F(a, b) and form_ok(text, "mixed") and (c.get("unit") is None or unorm(pv[1]) == unorm(c["unit"]))
    return pv[0] == want and (c.get("unit") is None or unorm(pv[1]) == unorm(c["unit"]))


def fn_pattern_term(c, text):
    """start, op ('add'|'mul'), k, n (1-based term)."""
    v = eval_expr(c["start"])
    for _ in range(int(c["n"]) - 1):
        v = v + eval_expr(c["step"]) if c["op"] == "add" else v * eval_expr(c["step"])
    pv = parse_value(text)
    return pv is not None and pv[0] == v


def fn_pattern_list(c, text):
    v = eval_expr(c["start"])
    seq = [v]
    for _ in range(int(c["count"]) - 1):
        v = v + eval_expr(c["step"]) if c["op"] == "add" else v * eval_expr(c["step"])
        seq.append(v)
    parts = [p.strip() for p in text.split(",")]
    try:
        return [parse_value(p)[0] for p in parts] == seq
    except TypeError:
        return False


def fn_pair(c, text):
    m = re.fullmatch(r"\((\S+?), (\S+?)\)", text.strip())
    if not m:
        return False
    return parse_value(m.group(1))[0] == eval_expr(c["x"]) and parse_value(m.group(2))[0] == eval_expr(c["y"])


def fn_point_at(c, text):
    """Which labeled point is at (x, y)? points: {label: [x, y]}"""
    for lab, (x, y) in c["points"].items():
        if F(x) == eval_expr(c["x"]) and F(y) == eval_expr(c["y"]):
            return norm(text) == norm(lab) or norm(text) == norm("point " + lab)
    return False


def fn_tri(c, text):
    return norm(text) == tri_class(c.get("sides"), c.get("angles"), c["by"])


def fn_tri_both(c, text):
    want = tri_class(None, c["angles"], "angles") + " " + tri_class(c["sides"], None, "sides")
    return norm(text) == want


def fn_quad_is(c, text):
    """Option text: a quadrilateral name that must belong to the figure (or 'most specific' when c['most'])."""
    names = quad_names(c["q"])
    t = norm(text)
    if c.get("most"):
        order = ["square", "rectangle", "rhombus", "parallelogram", "kite", "trapezoid", "quadrilateral"]
        best = next(n for n in order if n in names)
        if best == "rectangle" and "rhombus" in names:
            best = "square"
        return t == best
    return t in names


def fn_statement(c, text):
    """Hierarchy statements: 'All A are B.' / 'Some A are B.' / 'No A are B.' judged by the authored truth table below."""
    return norm(text) == norm(c["good"]) and c["good"] in HIER_TRUE


HIER_TRUE = set()


def fn_lp(c, text):
    """Line-plot questions computed from the plotted values. op: count_at, count_ge, count_le, total, diff, mode, fair."""
    vals = [parse_value(v)[0] for v in c["values"]]
    op = c["op"]
    if op == "count_at":
        want = sum(1 for v in vals if v == parse_value(c["x"])[0])
    elif op == "count_ge":
        want = sum(1 for v in vals if v >= parse_value(c["x"])[0])
    elif op == "count_le":
        want = sum(1 for v in vals if v <= parse_value(c["x"])[0])
    elif op == "count_lt":
        want = sum(1 for v in vals if v < parse_value(c["x"])[0])
    elif op == "count_diff":
        want = sum(1 for v in vals if v == parse_value(c["x"])[0]) - sum(1 for v in vals if v == parse_value(c["y"])[0])
    elif op == "max":
        want = max(vals)
    elif op == "max_minus_mode":
        cnt = Counter(vals)
        mx = max(cnt.values())
        modes = [v for v, k in cnt.items() if k == mx]
        if len(modes) != 1:
            return False
        want = max(vals) - modes[0]
    elif op == "count_gt":
        want = sum(1 for v in vals if v > parse_value(c["x"])[0])
    elif op == "total":
        want = sum(vals)
    elif op == "total_at":
        x = parse_value(c["x"])[0]
        want = sum(v for v in vals if v == x)
    elif op == "diff":
        want = max(vals) - min(vals)
    elif op == "mode":
        cnt = Counter(vals)
        mx = max(cnt.values())
        modes = [v for v, k in cnt.items() if k == mx]
        if len(modes) != 1:
            return False
        want = modes[0]
    elif op == "fair":
        want = sum(vals) / len(vals)
    elif op == "n":
        want = len(vals)
    else:
        raise KeyError(op)
    pv = parse_value(text)
    return pv is not None and pv[0] == want and (c.get("form") is None or form_ok(text, c["form"])) and (c.get("unit") is None or unorm(pv[1]) == unorm(c["unit"]))


def fn_lp_data(c, text):
    """Which data set matches the plot? text is a list 'a, b, c'."""
    try:
        got = sorted(parse_value(p.strip())[0] for p in text.split(","))
    except TypeError:
        return False
    return got == sorted(parse_value(v)[0] for v in c["values"])


def fn_convert(c, text):
    """value in unit `frm` -> unit `to` using the table below (independent factors)."""
    want = eval_expr(c["x"]) * FACT[c["frm"]] / FACT[c["to"]]
    pv = parse_value(text)
    if c.get("bare"):
        return pv is not None and pv[0] == want and pv[1] == ""
    return pv is not None and pv[0] == want and unorm(pv[1]) == unorm(c["to"]) and form_ok(text, c.get("form"))


def fn_compound(c, text):
    """'5 feet 3 inches' style: big + small unit, total in small units must equal `small_total`."""
    m = re.fullmatch(r"([\d,]+) ([a-z ]+?) ([\d,]+) ([a-z ]+)", text.strip())
    if not m:
        return False
    a, u1, b, u2 = m.groups()
    if unorm(u1) != unorm(c["big"]) or unorm(u2) != unorm(c["small"]):
        return False
    a, b = int(a.replace(",", "")), int(b.replace(",", ""))
    per = FACT[c["big"]] / FACT[c["small"]]
    return b < per and a * per + b == eval_expr(c["total"])


FACT = {"foot": F(12), "inch": F(1),   # in base units: inches, ounces (weight), fluid ounces (capacity), meters, grams, liters, seconds
    "inches": F(1), "feet": F(12), "yards": F(36), "miles": F(63360),
    "ounces": F(1), "pounds": F(16), "tons": F(32000),
    "fluid ounces": F(1), "cups": F(8), "pints": F(16), "quarts": F(32), "gallons": F(128),
    "millimeters": F(1, 1000), "centimeters": F(1, 100), "meters": F(1), "kilometers": F(1000),
    "milligrams": F(1, 1000), "grams": F(1), "kilograms": F(1000),
    "milliliters": F(1, 1000), "liters": F(1),
    "seconds": F(1), "minutes": F(60), "hours": F(3600), "days": F(86400), "weeks": F(604800),
}


def fn_volume_cubes(c, text):
    tot = sum(b["l"] * b["w"] * b["h"] for b in c["blocks"])
    pv = parse_value(text)
    return pv is not None and pv[0] == tot and (c.get("unit") is None or unorm(pv[1]) == unorm(c["unit"]))


def fn_volume_comp(c, text):
    tot = sum(eval_expr(str(p["l"])) * eval_expr(str(p["w"])) * eval_expr(str(p["h"])) for p in c["parts"])
    pv = parse_value(text)
    return pv is not None and pv[0] == tot and unorm(pv[1]) == unorm(c["unit"])


def fn_prisms_with(c, text):
    """Which l × w × h (text 'l × w × h') has volume V (and optionally given base)?"""
    m = re.fullmatch(r"(\d+) (?:\w+ )?× (\d+) (?:\w+ )?× (\d+)(?: \w+)?", text.strip())
    return bool(m) and int(m.group(1)) * int(m.group(2)) * int(m.group(3)) == int(c["v"])


def fn_scale_cmp(c, text):
    """Product of n and factor f compared with n: 'greater than', 'less than', 'equal to'."""
    f = eval_expr(c["f"])
    want = "greater than" if f > 1 else "less than" if f < 1 else "equal to"
    return norm(text).startswith(norm(c.get("lead", ""))) and want in norm(text) and all(w not in norm(text) for w in {"greater than", "less than", "equal to"} - {want})


def fn_expr_value_cmp(c, text):
    """'A is n times as large as B' style interpretation: ratio of value(a) to value(b)."""
    pv = parse_value(text)
    return pv is not None and pv[0] == eval_expr(c["a"]) / eval_expr(c["b"])


def fn_ratio_terms(c, text):
    """Pattern relationship: each term of B is k times (or k more than) the corresponding term of A."""
    a = [eval_expr(x) for x in c["a"]]
    b = [eval_expr(x) for x in c["b"]]
    t = norm(text)
    m = re.search(r"(\d+(?:/\d+)?) times", t)
    if m and all(bb == aa * F(m.group(1)) for aa, bb in zip(a, b)) and ("b" in t.split()[0] or c.get("dir") == "ba"):
        return True
    return norm(text) == norm(c.get("good", "\u0000"))


def fn_missing_exp(c, text):
    a, b = eval_expr(c["a"].replace(",", "")), eval_expr(c["b"].replace(",", ""))
    pv = parse_value(text)
    if pv is None or pv[0].denominator != 1 or pv[0] < 0:
        return False
    n = int(pv[0])
    return (a * 10 ** n == b) if c["op"] == "×" else (a / 10 ** n == b)


def fn_zero_count(c, text):
    s = str(int(eval_expr(c["e"])))
    pv = parse_value(text)
    return pv is not None and pv[0] == len(s) - len(s.rstrip("0"))


def fn_from_words(c, text):
    if not re.fullmatch(r"[\d,]+(?:\.\d+)?", text.strip()):
        return False
    return norm(words_decimal(text.strip())) == norm(c["words"])


def fn_between(c, text):
    pv = parse_value(text)
    return pv is not None and eval_expr(c["lo"].replace(",", "")) < pv[0] < eval_expr(c["hi"].replace(",", ""))


def fn_extreme(c, text):
    vals = {k: (eval_expr(v) if c.get("expr") else parse_value(v)[0]) for k, v in c["values"].items()}
    best = (min if c["which"] == "min" else max)(vals.values())
    winners = [k for k, v in vals.items() if v == best]
    return len(winners) == 1 and norm(text) == norm(winners[0])


def fn_rounds_to(c, text):
    pv = parse_value(text)
    return pv is not None and rnd(pv[0], c["place"]) == eval_expr(c["target"])


def fn_rounds_extreme(c, text):
    t = eval_expr(c["target"])
    step = F(1, 10 ** int(c["places"]))
    cands = [t + k * step for k in range(-60, 61) if rnd(t + k * step, "tenths") == t]
    want = max(cands) if c["which"] == "max" else min(cands)
    pv = parse_value(text)
    return pv is not None and pv[0] == want


def fn_closer(c, text):
    x, a, b = eval_expr(c["x"]), eval_expr(c["a"]), eval_expr(c["b"])
    pv = parse_value(text)
    if pv is None or abs(x - a) == abs(x - b):
        return False
    want = a if abs(x - a) < abs(x - b) else b
    return pv[0] == want and text.strip() in (c["a"], c["b"])


def fn_same_value(c, text):
    try:
        return eval_expr(text) == eval_expr(c["target"])
    except Exception:
        return False


def lead_round_v(n):
    n = int(n)
    e = len(str(n)) - 1
    return int(rnd(F(n), {0: "ones", 1: "tens", 2: "hundreds", 3: "thousands", 4: "ten thousands"}[e]))


def fn_est_product(c, text):
    pv = parse_value(text)
    return pv is not None and pv[0] == lead_round_v(c["a"]) * lead_round_v(c["b"])


def fn_over_under(c, text):
    est, exact = eval_expr(c["est"]), F(int(c["a"]) * int(c["b"]))
    return norm(text) == ("overestimate" if est > exact else "underestimate" if est < exact else "exact")


def fn_bus_cost(c, text):
    n, d, price = int(c["n"]), int(c["d"]), int(c["price"])
    buses = (n + d - 1) // d
    pv = parse_value(text)
    return pv is not None and pv[0] == buses * price and text.strip().startswith("$")


def fn_est_sum(c, text):
    a, b = eval_expr(c["a"]), eval_expr(c["b"])
    ra, rb = rnd(a, "ones"), rnd(b, "ones")
    want = ra + rb if c["op"] == "+" else ra - rb
    pv = parse_value(text)
    return pv is not None and pv[0] == want


def fn_dec_places(c, text):
    cnt = lambda s: len(s.split(".")[1]) if "." in s else 0
    pv = parse_value(text)
    return pv is not None and pv[0] == cnt(c["a"]) + cnt(c["b"])


def fn_div_cmp(c, text):
    n, d = F(int(c["n"])), eval_expr(c["d"])
    q = n / d
    want = "greater than" if q > n else "less than" if q < n else "equal to"
    return norm(text) == want


def fn_better_buy(c, text):
    ua = eval_expr(c["a"][1]) / int(c["a"][0])
    ub = eval_expr(c["b"][1]) / int(c["b"][0])
    if ua == ub:
        return False
    return norm(text) == ("pack a" if ua < ub else "pack b")


def fn_extreme_expr(c, text):
    disp = c.get("display", c["exprs"])
    vals = {d: eval_expr(x) for x, d in zip(c["exprs"], disp)}
    best = (max if c["which"] == "max" else min)(vals.values())
    win = [x for x, v in vals.items() if v == best]
    return len(win) == 1 and text.strip() == win[0]


def fn_expr_times(c, text):
    try:
        return eval_expr(text) == int(c["mult"]) * eval_expr(c["base"])
    except Exception:
        return False


def fn_expr_ratio_blank(c, text):
    pv = parse_value(text)
    s = int(c["a"]) + int(c["b"])
    return pv is not None and pv[0] * s == int(c["mult"]) * s


def fn_pattern_ratio(c, text):
    a, b = int(c["a"]), int(c["b"])
    A = [a * i for i in range(1, 8)]
    B = [b * i for i in range(1, 8)]
    ratios = {F(y, x) for x, y in zip(A, B)}
    pv = parse_value(text)
    return len(ratios) == 1 and pv is not None and pv[0] == ratios.pop()


def fn_pattern_pair(c, text):
    n = int(c["n"])
    return fn_pair({"x": str(int(c["a"]) * (n - 1)), "y": str(int(c["b"]) * (n - 1))}, text)


def fn_pattern_pair_any(c, text):
    m = re.fullmatch(r"\((\d+), (\d+)\)", text.strip())
    if not m:
        return False
    x, y = int(m.group(1)), int(m.group(2))
    a, b = int(c["a"]), int(c["b"])
    return x % a == 0 and y == (x // a) * b


def fn_blank_is(c, text):
    """Words 'add A and B, then multiply by C' / 'multiply B by C, then subtract A' against the expression with one blank."""
    w = c["words"]
    m = re.fullmatch(r"add (\d+) and (\d+), then multiply by (\d+)", w)
    e = c["expr"]
    pv = parse_value(text)
    if pv is None:
        return False
    filled = e.replace("___", str(pv[0]))
    if m:
        want = (int(m.group(1)) + int(m.group(2))) * int(m.group(3))
        return eval_expr(filled) == want and str(pv[0]) == m.group(3)
    m = re.fullmatch(r"multiply (\d+) by (\d+), then subtract (\d+)", w)
    want = int(m.group(1)) * int(m.group(2)) - int(m.group(3))
    return eval_expr(filled) == want


def fn_equiv_blank(c, text):
    pv = parse_value(text)
    if pv is None or pv[0].denominator != 1:
        return False
    left = eval_expr(c["left"])
    n, d = c["right"].split("/")
    right = F(int(pv[0]), int(d)) if n == "?" else F(int(n), int(pv[0])) if pv[0] else None
    return right == left


def fn_lcd(c, text):
    from math import gcd as g
    da, db = F(c["a"]).denominator, F(c["b"]).denominator
    pv = parse_value(text)
    return pv is not None and pv[0] == da * db // g(da, db)


def fn_equiv_to(c, text):
    m = re.fullmatch(r"(\d+)/(\d+)", text.strip())
    return bool(m) and F(int(m.group(1)), int(m.group(2))) == F(c["target"])


def fn_frac_text_equal(c, text):
    return text.strip() == f"{c['n']}/{c['d']}"


def fn_improper(c, text):
    m = re.fullmatch(r"(\d+)/(\d+)", text.strip())
    return bool(m) and int(m.group(1)) == int(c["n"]) and int(m.group(2)) == int(c["d"])


def fn_regroup(c, text):
    pv = parse_value(text)
    w, n, d = int(c["w"]), int(c["n"]), int(c["d"])
    return pv is not None and (w - 1) + pv[0] / d == w + F(n, d)


def bench_v(x):
    cands = [F(k, 2) for k in range(0, 40)]
    best = min(cands, key=lambda b: abs(b - x))
    ties = [b for b in cands if abs(b - x) == abs(best - x)]
    return best if len(ties) == 1 else None


def fn_benchmark(c, text):
    b = bench_v(eval_expr(c["x"]))
    pv = parse_value(text)
    return b is not None and pv is not None and pv[0] == b


def fn_bench_sum(c, text):
    ba, bb = bench_v(eval_expr(c["a"])), bench_v(eval_expr(c["b"]))
    if ba is None or bb is None:
        return False
    want = ba + bb if c["op"] == "+" else ba - bb
    pv = parse_value(text)
    return pv is not None and pv[0] == want


def fn_sum_cmp(c, text):
    s = eval_expr(c["a"]) + eval_expr(c["b"])
    return norm(text) == ("greater than 1" if s > 1 else "less than 1" if s < 1 else "equal to 1")


def fn_between_whole(c, text):
    m = re.fullmatch(r"(\d+) and (\d+)", text.strip())
    x = eval_expr(c["x"])
    return bool(m) and int(m.group(2)) == int(m.group(1)) + 1 and int(m.group(1)) < x < int(m.group(2))


def fn_tile_count(c, text):
    b1, b2, w = int(c["b1"]), int(c["b2"]), int(c["w"])
    pv = parse_value(text)
    return pv is not None and pv[0] == (F(w * w) / (F(1, b1) * F(1, b2)))


def fn_cube_fit(c, text):
    s = int(c["s"])
    l, w, h = (int(x) for x in c["box"])
    if l % s or w % s or h % s:
        return False
    pv = parse_value(text)
    return pv is not None and pv[0] == F(l * w * h, s ** 3)


def _xy(text):
    m = re.fullmatch(r"\((\d+), (\d+)\)", text.strip())
    return (int(m.group(1)), int(m.group(2))) if m else None


def fn_axis_of(c, text):
    x, y = _xy(c["p"])
    want = "the x-axis" if y == 0 and x != 0 else "the y-axis" if x == 0 and y != 0 else None
    return want is not None and norm(text) == want


def fn_rect_corner(c, text):
    g = [tuple(p) for p in c["given"]]
    xs = [p[0] for p in g]
    ys = [p[1] for p in g]
    want = (min(set(xs), key=xs.count), min(set(ys), key=ys.count))
    return _xy(text) == want and want not in g


def fn_graph_value(c, text):
    pts = {int(p[0]): F(p[1]) for p in c["data"]}
    pv = parse_value(text)
    return pv is not None and pv[0] == pts[int(c["x"])] and unorm(pv[1]) == unorm(c["unit"])


def fn_not_pattern_pair(c, text):
    return not fn_pattern_pair_any(c, text) and _xy(text) is not None


def fn_pair_in_table(c, text):
    return _xy(text) in [(int(a), int(b)) for a, b in c["rows"]]


# guaranteed properties of each category (independent model of the hierarchy)
PROPS = {"quadrilaterals": {"4 sides"}, "parallelograms": {"4 sides", "2 parallel pairs"}, "rectangles": {"4 sides", "2 parallel pairs", "4 right angles"},
         "rhombuses": {"4 sides", "2 parallel pairs", "4 equal sides"}, "squares": {"4 sides", "2 parallel pairs", "4 right angles", "4 equal sides"}}


def is_sub(a, b):
    return PROPS[b] <= PROPS[a]


def fn_all_are_false(c, text):
    m = re.fullmatch(r"All (\w+) are (\w+)\.", text.strip())
    return bool(m) and not is_sub(m.group(1), m.group(2))


def fn_is_every(c, text):
    return norm(text) == ("yes" if is_sub(c["a"], c["b"]) else "no")


def fn_count_marks(c, text):
    d = c["data"]
    want = len(d.get("arrows", [])) // 2 if c["what"] == "parallel_pairs" else len(d.get("right", []))
    pv = parse_value(text)
    return pv is not None and pv[0] == want


def fn_poly_sides(c, text):
    n = {"triangle": 3, "quadrilateral": 4, "pentagon": 5, "hexagon": 6, "octagon": 8}[c["name"]]
    pv = parse_value(text)
    return pv is not None and pv[0] == n * int(c["count"])


def fn_quad_perimeter(c, text):
    s = int(c["s"])
    want = 4 * s if c["kind"] in ("square", "rhombus") else 2 * (s + int(c["t"]))
    pv = parse_value(text)
    return pv is not None and pv[0] == want and unorm(pv[1]) == "inch"


FNS = {"all_are_false": fn_all_are_false, "is_every": fn_is_every, "count_marks": fn_count_marks, "poly_sides": fn_poly_sides,
       "quad_perimeter": fn_quad_perimeter, "axis_of": fn_axis_of, "rect_corner": fn_rect_corner, "graph_value": fn_graph_value, "not_pattern_pair": fn_not_pattern_pair,
       "pair_in_table": fn_pair_in_table, "cube_fit": fn_cube_fit, "between_whole": fn_between_whole, "tile_count": fn_tile_count, "equiv_blank": fn_equiv_blank, "lcd": fn_lcd, "equiv_to": fn_equiv_to, "frac_text_equal": fn_frac_text_equal, "improper": fn_improper,
       "regroup": fn_regroup, "benchmark": fn_benchmark, "bench_sum": fn_bench_sum, "sum_cmp": fn_sum_cmp, "extreme_expr": fn_extreme_expr, "expr_times": fn_expr_times, "expr_ratio_blank": fn_expr_ratio_blank, "pattern_ratio": fn_pattern_ratio,
       "pattern_pair": fn_pattern_pair, "pattern_pair_any": fn_pattern_pair_any, "blank_is": fn_blank_is, "est_sum": fn_est_sum, "dec_places": fn_dec_places, "div_cmp": fn_div_cmp, "better_buy": fn_better_buy, "same_value": fn_same_value, "est_product": fn_est_product, "over_under": fn_over_under, "bus_cost": fn_bus_cost, "closer": fn_closer, "missing_exp": fn_missing_exp, "zero_count": fn_zero_count, "from_words": fn_from_words, "between": fn_between,
       "extreme": fn_extreme, "rounds_to": fn_rounds_to, "rounds_extreme": fn_rounds_extreme,
"tf": fn_tf, "claims": fn_claims, "compare": fn_compare, "round": fn_round, "order": fn_order,
       "digit_value": fn_digit_value, "place_of": fn_place_of, "times": fn_times, "word_form": fn_word_form,
       "expanded": fn_expanded, "quotient_rem": fn_quotient_rem, "remainder_use": fn_remainder_use,
       "pattern_term": fn_pattern_term, "pattern_list": fn_pattern_list, "pair": fn_pair, "point_at": fn_point_at,
       "tri": fn_tri, "tri_both": fn_tri_both, "quad_is": fn_quad_is, "lp": fn_lp, "lp_data": fn_lp_data,
       "convert": fn_convert, "compound": fn_compound, "volume_cubes": fn_volume_cubes, "volume_comp": fn_volume_comp,
       "prisms_with": fn_prisms_with, "scale_cmp": fn_scale_cmp, "expr_ratio": fn_expr_value_cmp}


# ------------------------------------------------------------------ text-quality lints
BAD_NOTATION = [(r"\d\s*\*\s*\d", "uses * for multiplication"), (r"\d\s+x\s+\d", "uses x for multiplication"),
                (r"\^", "caret exponent (use superscripts)"), (r"\d\s+/\s+\d", "spaced slash used as division (use ÷)"),
                (r"\\frac|\$\$|\\\(", "raw LaTeX"), (r"\bNaN\b|undefined|None\b", "broken value"),
                (r"(?<![\w$])\.\d", "decimal without leading zero"), (r"\b(?:kg|lb|oz|qt|pt|gal|mL|mg)\b", "abbreviated unit renders as variables; spell it out")]


def lint_text(t):
    out = []
    for pat, msg in BAD_NOTATION:
        if re.search(pat, t):
            out.append(msg)
    return out


SUPD = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")


def numbers_in(t):
    t = re.sub(r"([⁰¹²³⁴⁵⁶⁷⁸⁹]+)", lambda m: " " + m.group(1).translate(SUPD) + " ", str(t))
    return {F(x.replace(",", "")) for x in re.findall(NUM, str(t))}


# ------------------------------------------------------------------ main
def main():
    errors, warn = [], []
    stats = Counter()
    per = defaultdict(Counter)
    fams_per = defaultdict(set)
    qtypes = Counter()
    seen_prompt = {}
    near = Counter()
    keyed = 0
    manifest_units = []
    for u in UNITS:
        bf = os.path.join(ROOT, "question-banks", COURSE_ID, u["id"] + ".json")
        cf = os.path.join(HERE, "out", u["id"] + ".checks.json")
        mf = os.path.join(ROOT, "question-banks", COURSE_ID, "meta", u["id"] + ".meta.json")
        if not os.path.exists(bf):
            errors.append(f"missing bank {u['id']}")
            continue
        bank = json.load(open(bf, encoding="utf-8"))
        checks = json.load(open(cf, encoding="utf-8"))
        meta = json.load(open(mf, encoding="utf-8"))
        assert bank["courseId"] == COURSE_ID and bank["unitId"] == u["id"] and bank["schemaVersion"] == 1
        recs = {r["id"]: r for r in skill_records(u)}
        manifest_units.append(u["id"])
        for q in bank["questions"]:
            qid = q["id"]
            E = lambda m: errors.append(f"{qid}: {m}")
            if q["skillId"] not in recs:
                E("unknown skill")
                continue
            stats["questions"] += 1
            per[(q["skillId"], q["level"])][q["format"]] += 1
            c = checks.get(qid)
            m = meta.get(qid, {})
            if not c:
                E("no check")
                continue
            fams_per[(q["skillId"], q["level"])].add(c["family"].split("_error")[0].split("_tf")[0].split("_sel")[0].split("_open")[0].split("_match")[0])
            qtypes[m.get("questionType")] += 1
            if set(q.get("standards", [])) - set(recs[q["skillId"]]["standards"]):
                E("standard not in skill map")
            # text lints
            texts = [q["prompt"]] + [o["text"] for o in q.get("options", [])] + [p["prompt"] for p in q.get("parts", [])] + \
                    [p["answer"] for p in q.get("parts", [])] + ([q["answer"]] if isinstance(q["answer"], str) else list(q["answer"])) + q["solutionSteps"]
            for t in texts:
                for msg in lint_text(t):
                    E(f"notation: {msg}: {t[:80]}")
            key = (re.sub(r"\s+", " ", q["prompt"].lower()), "|".join(sorted(o["text"] for o in q.get("options", []))),
                   "|".join(p["prompt"] for p in q.get("parts", [])), q.get("diagram", {}).get("spec", {}).get("alt", ""))
            if key in seen_prompt:
                E(f"duplicate of {seen_prompt[key]}")
            seen_prompt[key] = qid
            near[(re.sub(r"\d+", "#", key[0]) + key[1][:0], q["skillId"], q["level"])] += 1
            # diagram
            if q.get("diagram"):
                src = os.path.join(ROOT, q["diagram"]["spec"]["src"])
                if not os.path.exists(src):
                    E("diagram file missing")
                if not q["diagram"]["spec"].get("alt", "").strip():
                    E("diagram alt missing")
                if not c.get("diagram"):
                    E("diagram has no stored data")
            chk = c["q"] or {"k": "parts"}
            if chk["k"] == "key":
                keyed += 1
            try:
                if q["format"] == "short-answer":
                    if not accepts(chk, q["answer"], q):
                        E(f"answer rejected by check: {q['answer']!r} ({chk})")
                    for w in m.get("distractors", {}):
                        if accepts(chk, w, q):
                            E(f"stored distractor is actually correct: {w}")
                    for w in m.get("shown", []):
                        if accepts(chk, w, q):
                            E(f"error-analysis 'student answer' is actually correct: {w}")
                elif q["format"] == "multiple-choice":
                    opts = q["options"]
                    if len(opts) != 4 and chk["k"] != "key" and chk.get("fn") not in ("tf",):
                        warn.append(f"{qid}: {len(opts)} options")
                    if len({norm(o['text']) for o in opts}) != len(opts):
                        E("repeated option text")
                    good = [o for o in opts if o["correct"]]
                    if len(good) != 1 or good[0]["text"] != q["answer"]:
                        E("answer does not match the single correct option")
                    for w in m.get("distractors", {}):
                        if accepts(chk, w, q):
                            E(f"stored distractor is actually correct: {w}")
                    for o in opts:
                        t = accepts(chk, o["text"], q)
                        if t != o["correct"]:
                            E(f"option {o['text']!r} judged {t} but flagged {o['correct']}")
                elif q["format"] == "select-all":
                    for o in q["options"]:
                        t = accepts(chk, o["text"], q)
                        if t != o["correct"]:
                            E(f"select-all option {o['text']!r} judged {t} but flagged {o['correct']}")
                    if sorted(q["answer"]) != sorted(o["text"] for o in q["options"] if o["correct"]):
                        E("select-all answer list mismatch")
                elif q["format"] == "open-response":
                    for p, pc in zip(q["parts"], c["parts"]):
                        if not accepts(pc, p["answer"]):
                            E(f"part rejected: {p['prompt']} -> {p['answer']}")
                    if len(q["parts"]) < 4:
                        E("open response needs 4 parts")
            except Exception as ex:  # noqa
                E(f"check failed to run: {type(ex).__name__}: {ex}")
            # numbers in an expression check must be visible to the student (prompt, diagram data, parts)
            if chk["k"] == "expr" and q["format"] != "open-response":
                vis = numbers_in(q["prompt"]) | numbers_in(json.dumps(c.get("diagram") or {})) | set(map(F, c.get("consts", [])))
                vis |= numbers_in(" ".join(o["text"] for o in q.get("options", [])))
                used = numbers_in(chk["e"])
                miss = {x for x in used - vis if x not in (0, 1, 2, 10, 100, 1000)}
                if miss:
                    E(f"check uses numbers not shown to the student: {sorted(map(str, miss))}")
    # coverage
    for u in UNITS:
        if f"missing bank {u['id']}" in errors:
            continue
        for r in skill_records(u):
            for lv in ("cp2", "cp1", "honors"):
                n = sum(per[(r["id"], lv)].values())
                if n < 30:
                    errors.append(f"{r['id']} {lv}: only {n} questions")
                if len(fams_per[(r['id'], lv)]) < 5:
                    warn.append(f"{r['id']} {lv}: only {len(fams_per[(r['id'], lv)])} families")
    near_dups = sum(v - 1 for v in near.values() if v > 6)
    print(f"Grade 5 verifier: {stats['questions']} questions in {len(manifest_units)} banks")
    print(f"  authored-key checks: {keyed}")
    print("  question types:", dict(qtypes.most_common()))
    print(f"  heavy same-template clusters (>6 items sharing one template in a skill/level): {near_dups}")
    for w in warn[:40]:
        print("  WARN", w)
    if len(warn) > 40:
        print(f"  ... {len(warn) - 40} more warnings")
    for e in errors[:int(os.environ.get("VMAX", "200"))]:
        print("  ERROR", e)
    print(f"TOTAL ERRORS {len(errors)}  WARNINGS {len(warn)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
