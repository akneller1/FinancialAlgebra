"""Grade 2 named checks for verify.py (added to the Grade 3 checks in tools/grade3-authoring/checks3.py).
Each check recomputes the answer from the stored check data with its own arithmetic; nothing is imported from the
families or from g2lib. bind() gives access to the generic helpers in verify.py (parse_value, eval_expr, norm)."""
import os, re, sys
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(HERE, "..", "grade3-authoring"))
import checks3

V = checks3.V


def bind(g):
    checks3.bind(g)


def pv(t):
    x = V["parse_value"](t)
    return None if x is None else x[0]


def norm(t):
    return V["norm"](t)


FNS = dict(checks3.FNS)


# ---------------------------------------------------------------- unit 1 (facts within 20)
def _eq(text):
    a, b = str(text).split("=")
    return V["eval_expr"](a) == V["eval_expr"](b)


def helps_sub(c, t):
    """An addition fact 'p + x = w' that is true and uses the part c['part'] and the whole c['whole']."""
    m = re.fullmatch(r"(\d+) \+ (\d+) = (\d+)", str(t).strip())
    return bool(m) and _eq(t) and int(m.group(3)) == c["whole"] and c["part"] in (int(m.group(1)), int(m.group(2)))


def fam_member(c, t):
    """True subtraction equation using exactly the three numbers of the family."""
    m = re.fullmatch(r"(\d+) − (\d+) = (\d+)", str(t).strip())
    return bool(m) and _eq(t) and sorted(int(x) for x in m.groups()) == sorted(c["nums"])


def fam_fact(c, t):
    m = re.fullmatch(r"(\d+) ([+−]) (\d+) = (\d+)", str(t).strip())
    if not m or not _eq(t):
        return False
    x, op, y, z = m.groups()
    if sorted(int(v) for v in (x, y, z)) != sorted(c["nums"]):
        return False
    have = {re.sub(r"\s+", " ", h.strip()) for h in c["have"]}
    return re.sub(r"\s+", " ", str(t).strip()) not in have


def eq_truth(c, t):
    m = re.fullmatch(r"(True|False)\. (\d+) \+ (\d+) is (\d+)\.", str(t).strip())
    if not m:
        return False
    truth = _eq(c["eq"])
    return (m.group(1) == "True") == truth and int(m.group(2)) + int(m.group(3)) == int(m.group(4))


FNS.update({"helps_sub": helps_sub, "fam_member": fam_member, "fam_fact": fam_fact, "eq_truth": eq_truth})


# ---------------------------------------------------------------- unit 2 (odd, even, arrays)
def _par(n):
    return "even" if int(n) % 2 == 0 else "odd"


def _unit(c, t):
    """Answer text without unit when c has no unit; with the unit when it has one. Returns the number or None."""
    x = V["parse_value"](t)
    if x is None:
        return None
    if c.get("unit"):
        return x[0] if V["unorm"](x[1]) == V["unorm"](c["unit"]) else None
    return x[0] if x[1] == "" else None


def parity(c, t):
    return norm(t) == _par(c["n"])


def parity_reason(c, t):
    m = re.fullmatch(r"(odd|even), because (one counter is left over|every counter has a partner) when you make pairs", str(t).strip())
    return bool(m) and m.group(1) == _par(c["n"]) and (m.group(2).startswith("one") == (c["n"] % 2 == 1))


def parity_pick(c, t):
    return re.fullmatch(r"\d+", str(t).strip()) is not None and _par(t) == c["want"]


def pairs_story(c, t):
    n = c["n"]
    good = (f"No. {n} is odd, so one is left over." if n % 2 else f"Yes. {n} is even, so everyone has a partner.")
    return str(t).strip() == good


def next_parity(c, t):
    v = _unit(c, t)
    return v is not None and v > c["n"] and _par(v) == c["want"] and all(_par(k) != c["want"] for k in range(c["n"] + 1, int(v)))


def parity_digit(c, t):
    m = re.fullmatch(r"(odd|even)\. The ones digit, (\d), is (odd|even)\.", str(t).strip())
    n = c["n"]
    return bool(m) and m.group(1) == _par(n) and int(m.group(2)) == n % 10 and m.group(3) == _par(n % 10)


def equal_addends(c, t):
    m = re.fullmatch(r"(\d+) \+ (\d+)", str(t).strip())
    return bool(m) and m.group(1) == m.group(2) and 2 * int(m.group(1)) == c["n"]


def half_of(c, t):
    v = _unit(c, t)
    return v is not None and v + v == c["n"]


def double_eq(c, t):
    m = re.fullmatch(r"(\d+) \+ (\d+) = (\d+)", str(t).strip())
    return bool(m) and m.group(1) == m.group(2) and int(m.group(3)) == c["n"] and 2 * int(m.group(1)) == c["n"]


def odd_double(c, t):
    n = c["n"]
    m = re.fullmatch(r"No\. (\d+) is odd, so it cannot be two equal addends; (\d+) \+ (\d+) = (\d+)\.", str(t).strip())
    return bool(m) and n % 2 == 1 and int(m.group(1)) == n and m.group(2) == m.group(3) and 2 * int(m.group(2)) == int(m.group(4)) != n


def rep_eq(c, t):
    """'b + b + ... = total' with one addend per row (by rows) or per column (by cols)."""
    m = re.fullmatch(r"([\d +]+) = (\d+)", str(t).strip())
    if not m:
        return False
    adds = [int(x) for x in m.group(1).split("+")]
    R, C = c["rows"], c["cols"]
    size, count = (C, R) if c["by"] == "rows" else (R, C)
    return adds == [size] * count and int(m.group(2)) == R * C


def rows_of(c, t):
    m = re.fullmatch(r"(\d+) rows of (\d+)", str(t).strip())
    return bool(m) and int(m.group(1)) == c["rows"] and int(m.group(2)) == c["cols"]


def rep_unknown(c, t):
    """The number that, added `times` times, makes `total` (or, with times as the addend, how many times)."""
    v = _unit(c, t)
    return v is not None and v * c["times"] == c["total"]


def same_array(c, t):
    m = re.fullmatch(r"(\d+) rows of (\d+)", str(t).strip())
    return bool(m) and int(m.group(1)) * int(m.group(2)) == c["total"]


FNS.update({k: v for k, v in dict(parity=parity, parity_reason=parity_reason, parity_pick=parity_pick, pairs_story=pairs_story,
                                  next_parity=next_parity, parity_digit=parity_digit, equal_addends=equal_addends, half_of=half_of,
                                  double_eq=double_eq, odd_double=odd_double, rep_eq=rep_eq, rows_of=rows_of, rep_unknown=rep_unknown,
                                  same_array=same_array).items()})


def more_array(c, t):
    m = re.fullmatch(r"(\d+) rows of (\d+), because it has (\d+) dots", str(t).strip())
    if not m:
        return False
    a, b, n = (int(x) for x in m.groups())
    tots = [x * y for x, y in c["arrays"]]
    return [a, b] in c["arrays"] and a * b == max(tots) and tots.count(max(tots)) == 1 and n == a * b


FNS["more_array"] = more_array


# ---------------------------------------------------------------- unit 3 (place value)
PLV = {"hundred": 100, "ten": 10, "one": 1}


def _amount(t):
    """'12 tens' -> 120, '1 hundred' -> 100 (exact plural agreement required)."""
    m = re.fullmatch(r"(\d+) (hundred|ten|one)(s?)", str(t).strip())
    if not m or (m.group(3) == "s") != (int(m.group(1)) != 1):
        return None
    return int(m.group(1)) * PLV[m.group(2)]


def tens_in(c, t):
    v = _unit(c, t)
    return v is not None and 10 * v == c["n"]


def tens_value(c, t):
    v = _unit(c, t)
    return v is not None and v == 10 * c["tens"]


def same_amount(c, t):
    return _amount(t) == c["value"]


def more_tens(c, t):
    v = _unit(c, t)
    return v is not None and 10 * (c["have"] + v) == c["target"]


def tens_reason(c, t):
    n = c["n"]
    m = re.fullmatch(r"(\d+) is 1 hundred and (\d+) tens?, and 1 hundred is 10 tens, so there are (\d+) tens\.", str(t).strip())
    return bool(m) and int(m.group(1)) == n and 100 + 10 * int(m.group(2)) == n and 10 * int(m.group(3)) == n


def _hto_text(n):
    def p(k, w):
        return f"{k} {w}" if k == 1 else f"{k} {w}s"
    return f"{p(n // 100, 'hundred')}, {p(n // 10 % 10, 'ten')}, and {p(n % 10, 'one')}"


def hto(c, t):
    m = re.fullmatch(r"(\d+) hundreds?, (\d+) tens?, and (\d+) ones?", str(t).strip())
    return bool(m) and str(t).strip() == _hto_text(c["n"])


def digit_in(c, t):
    s = str(c["n"])
    i = {"hundreds": 0, "tens": 1, "ones": 2}[c["place"]]
    return str(t).strip() == s[i]


def zero_tens(c, t):
    n = c["n"]
    h, o = n // 100, n % 10
    p = lambda k, w: f"{k} {w}" if k == 1 else f"{k} {w}s"
    return n // 10 % 10 == 0 and str(t).strip() == f"No. The 0 is in the tens place, so {n} has 0 tens. It has {p(h, 'hundred')} and {p(o, 'one')}."


def hundreds_value(c, t):
    v = _unit(c, t)
    return v is not None and v == 100 * c["h"]


def hundreds_count(c, t):
    v = _unit(c, t)
    return v is not None and 100 * v == c["n"]


def hundreds_reason(c, t):
    h = c["h"]
    return str(t).strip() == f"No. {100 * h} means {h} hundred{'s' if h != 1 else ''}, 0 tens, and 0 ones, so the 0s are needed."


def numeral_reason(c, t):
    m = re.fullmatch(r"(\d+), because there are (\d+) hundreds?, (\d+) tens?, and (\d+) ones?", str(t).strip())
    if not m:
        return False
    n, h, te, o = (int(x) for x in m.groups())
    return n == c["n"] and 100 * h + 10 * te + o == n and te == n // 10 % 10


FNS.update(dict(tens_in=tens_in, tens_value=tens_value, same_amount=same_amount, more_tens=more_tens, tens_reason=tens_reason, hto=hto,
                digit_in=digit_in, zero_tens=zero_tens, hundreds_value=hundreds_value, hundreds_count=hundreds_count,
                hundreds_reason=hundreds_reason, numeral_reason=numeral_reason))


# ---------------------------------------------------------------- unit 4 (counting and comparing)
def neighbor(c, t):
    v = _unit(c, t)
    return v is not None and v == c["n"] + (1 if c["way"] == "after" else -1)


def chart_hidden(c, t):
    v = _unit(c, t)
    cells = [c["start"] + i for i in range(c["per_row"] * c["rows"])]
    return v is not None and len(c["hide"]) == 1 and c["hide"][0] in cells and v == c["hide"][0]


def between_one(c, t):
    v = _unit(c, t)
    return v is not None and c["lo"] < v < c["hi"] and c["hi"] - c["lo"] == 2


def count_seq(c, t):
    parts = [p.strip() for p in str(t).split(",")]
    try:
        vals = [int(p) for p in parts]
    except ValueError:
        return False
    return vals[0] == c["start"] and all(b - a == c["step"] for a, b in zip(vals, vals[1:]))


def cross_reason(c, t):
    n = c["n"]
    h = (n + 2) // 100
    return (n + 2) % 100 == 0 and str(t).strip() == f"No. After {n + 1} comes {n + 2}, which is {h} hundred{'s' if h != 1 else ''}."


def step_of(c, t):
    v = _unit(c, t)
    s = c["seq"]
    d = {b - a for a, b in zip(s, s[1:])}
    return v is not None and len(d) == 1 and v == d.pop()


def count_by(c, t):
    v = _unit(c, t)
    return v is not None and v == sum([c["step"]] * c["times"])


def jumps_land(c, t):
    v = _unit(c, t)
    x = c["start"]
    for _ in range(c["jumps"]):
        x += c["step"]
    return v is not None and v == x


def seq_by(c, t):
    try:
        vals = [int(p) for p in str(t).split(",")]
    except ValueError:
        return False
    return len(vals) >= 3 and all(b - a == c["step"] for a, b in zip(vals, vals[1:]))


def next_by10(c, t):
    m = re.fullmatch(r"(\d+), because (\d+) \+ 10 = (\d+)", str(t).strip())
    return bool(m) and int(m.group(2)) == c["n"] and int(m.group(1)) == int(m.group(3)) == c["n"] + 10


def cmp_pick(c, t):
    v = _unit(c, t)
    a, b = c["nums"]
    return v is not None and v == (max(a, b) if c["want"] == "greater" else min(a, b)) and a != b


def true_cmp(c, t):
    m = re.fullmatch(r"(\d+) ([<>=]) (\d+)", str(t).strip())
    if not m:
        return False
    a, s, b = int(m.group(1)), m.group(2), int(m.group(3))
    return (a < b) if s == "<" else (a > b) if s == ">" else a == b


def who_more2(c, t):
    p = c["people"]
    best = max(p, key=p.get)
    return list(p.values()).count(p[best]) == 1 and str(t).strip() == best


def cmp_digit(c, t):
    v = _unit(c, t)
    if v is None or not (0 <= v <= 9):
        return False
    ok = [d for d in range(10) if ((c["h"] * 100 + d * 10 + c["o"] < c["other"]) if c["want"] == "greatest" else (c["h"] * 100 + d * 10 + c["o"] > c["other"]))]
    return bool(ok) and v == (max(ok) if c["want"] == "greatest" else min(ok))


def cmp_reason(c, t):
    a, b = c["a"], c["b"]
    m = re.fullmatch(r"(\d+), because (\d+) hundreds is more than (\d+) hundreds?", str(t).strip())
    return bool(m) and int(m.group(1)) == max(a, b) and int(m.group(2)) == max(a, b) // 100 and int(m.group(3)) == min(a, b) // 100 and a // 100 != b // 100


FNS.update(dict(neighbor=neighbor, chart_hidden=chart_hidden, between_one=between_one, count_seq=count_seq, cross_reason=cross_reason,
                step_of=step_of, count_by=count_by, jumps_land=jumps_land, seq_by=seq_by, next_by10=next_by10, cmp_pick=cmp_pick,
                true_cmp=true_cmp, who_more2=who_more2, cmp_digit=cmp_digit, cmp_reason=cmp_reason))


def cmp_place(c, t):
    a, b = str(c["a"]), str(c["b"])
    m = re.fullmatch(r"(\d+) ([<>]) (\d+), because the (hundreds|tens|ones) digits are different and (\d) ([<>]) (\d)", str(t).strip())
    if not m or m.group(1) != a or m.group(3) != b:
        return False
    k = next(i for i in range(3) if a[i] != b[i])
    s = ">" if int(a) > int(b) else "<"
    return m.group(2) == s == m.group(6) and m.group(4) == ["hundreds", "tens", "ones"][k] and m.group(5) == a[k] and m.group(7) == b[k]


FNS["cmp_place"] = cmp_place


# ---------------------------------------------------------------- unit 5 (within 100)
def check_add(c, t):
    m = re.fullmatch(r"(\d+) \+ (\d+) = (\d+)", str(t).strip())
    return bool(m) and _eq(t) and int(m.group(3)) == c["whole"] and sorted([int(m.group(1)), int(m.group(2))]) == sorted([c["part"], c["whole"] - c["part"]])


def check_claim(c, t):
    s, a, sh = c["whole"], c["part"], c["shown"]
    ok = sh + a == s
    m = re.fullmatch(r"(Yes|No)\. (\d+) \+ (\d+) = (\d+)(?:, not (\d+))?\.", str(t).strip())
    if not m:
        return False
    return (m.group(1) == "Yes") == ok and int(m.group(2)) == sh and int(m.group(3)) == a and int(m.group(4)) == sh + a and (m.group(5) is None) == ok and (ok or int(m.group(5)) == s)


def ten_pair(c, t):
    m = re.fullmatch(r"(\d+) \+ (\d+), because the ones make a ten", str(t).strip())
    if not m:
        return False
    x, y = int(m.group(1)), int(m.group(2))
    return x in c["nums"] and y in c["nums"] and x != y and (x + y) % 10 == 0


def order_reason(c, t):
    a, b = c["a"], c["b"]
    return str(t).strip() == f"Yes. Adding in any order gives the same sum: {a} + {b} = {b} + {a} = {a + b}."


def lead_diff(c, t):
    m = re.match(r"(\d+)\. ", str(t))
    return bool(m) and int(m.group(1)) == c["a"] - c["b"] and "not enough ones" in str(t) and c["a"] % 10 < c["b"] % 10


FNS.update(dict(check_add=check_add, check_claim=check_claim, ten_pair=ten_pair, order_reason=order_reason, lead_diff=lead_diff))


# ---------------------------------------------------------------- unit 6 (word problems)
def story_eq(c, t):
    s = str(t).strip()
    if s.count("?") != 1 or "=" not in s:
        return False
    nums_ = sorted(int(x) for x in re.findall(r"\d+", s))
    if nums_ != sorted(c["given"]):
        return False
    return _eq(s.replace("?", str(c["ans"])))


def lead_value(c, t):
    m = re.match(r"(\d+),", str(t))
    return bool(m) and int(m.group(1)) == c["value"]


def expr_eq(c, t):
    s = str(t).strip()
    m = re.fullmatch(r"(.+) = \?", s)
    if not m or sorted(int(x) for x in re.findall(r"\d+", m.group(1))) != sorted(c["nums"]):
        return False
    return V["eval_expr"](m.group(1)) == c["value"]


FNS.update(dict(story_eq=story_eq, lead_value=lead_value, expr_eq=expr_eq))


# ---------------------------------------------------------------- unit 7 (within 1,000)
def _d(n):
    return n // 100, n // 10 % 10, n % 10


def place_sum(c, t):
    m = re.fullmatch(r"(\d+) \+ (\d+) \+ (\d+)", str(t).strip())
    if not m:
        return False
    (ah, at_, ao), (bh, bt, bo) = _d(c["a"]), _d(c["b"])
    return [int(x) for x in m.groups()] == [(ah + bh) * 100, (at_ + bt) * 10, ao + bo]


def trade_blank(c, t):
    v = _unit(c, t)
    return v is not None and c["hundreds"] * 100 + v * 10 + c["ones"] == c["n"]


def lead_sum(c, t):
    m = re.match(r"(\d+)\. ", str(t))
    return bool(m) and int(m.group(1)) == c["a"] + c["b"] and "did not add the new ten or hundred" in str(t)


def lead_diff2(c, t):
    m = re.match(r"(\d+)\. ", str(t))
    return bool(m) and int(m.group(1)) == c["a"] - c["b"] and "instead of breaking apart" in str(t)


FNS.update(dict(place_sum=place_sum, trade_blank=trade_blank, lead_sum=lead_sum, lead_diff2=lead_diff2))


# ---------------------------------------------------------------- unit 8 (length)
def _len(c, t):
    x = V["parse_value"](t)
    if x is None or V["unorm"](x[1]) != V["unorm"](c["unit"]):
        return None
    return x[0]


def measure2(c, t):
    v = _len(c, t)
    return v is not None and v == c["end"] - c["start"]


def measure_claim(c, t):
    s, e, u, o = c["start"], c["end"], c["unit"], c["obj"]
    return str(t).strip() == f"No. The {o} starts at {s}, so it is {e - s} {u} long." and s != 0


def _tool(inches, curved):
    if curved:
        return "measuring tape"
    return "ruler" if inches <= 12 else "yardstick or meter stick" if inches <= 40 else "measuring tape"


def best_tool(c, t):
    return norm(t) == _tool(c["inches"], c["curved"])


def best_unit(c, t):
    if c["system"] == "us":
        return norm(t) == ("inches" if c["inches"] < 24 else "feet")
    return norm(t) == ("centimeters" if c["cm"] < 100 else "meters")


def pair_units(c, t):
    m = re.fullmatch(r"inches for the (.+) and feet for the (.+)", str(t).strip())
    return bool(m) and c["short"] < 24 and c["long"] >= 24


def unit_number(c, t):
    v = _unit(c, t)
    small_num, big_num = max(c["nums"]), min(c["nums"])
    return v is not None and v == (small_num if c["which"] == c["small"] else big_num)


def smaller_more(c, t):
    return str(t).strip() == f"{c['small'].capitalize()} are shorter than {c['big']}, so it takes more {c['small']} to cover the same length."


def unit_size(c, t):
    cnt = c["counts"]
    ks = sorted(cnt, key=cnt.get)       # fewer units -> longer unit
    return len(set(cnt.values())) == 2 and str(t).strip() == (ks[0] if c["which"] == "longer" else ks[1])


def rep_unit(c, t):
    v = _len(c, t)
    return v is not None and v == sum([c["size"]] * c["count"])


EST_IN = {"inches": 1, "feet": 12}
EST_CM = {"centimeters": 1, "meters": 100}


def estimate_len(c, t):
    m = re.fullmatch(r"about (\d+) (inches|feet|centimeters|meters)", str(t).strip())
    if not m:
        return False
    v, u = int(m.group(1)), m.group(2)
    true_ = c["inches"] if u in EST_IN else c["cm"]
    got = v * (EST_IN.get(u) or EST_CM[u])
    return abs(got - true_) <= 0.35 * true_


def estimate_unit(c, t):
    u = norm(t)
    if u not in ("inches", "feet", "centimeters", "meters"):
        return False
    true_ = c["inches"] if u in EST_IN else c["cm"]
    got = c["v"] * (EST_IN.get(u) or EST_CM[u])
    return abs(got - true_) <= 0.35 * true_


def lp_two(c, t):
    v = _unit(c, t)
    vals = [int(x) for x in c["values"]]
    return v is not None and v == sum(1 for x in vals if x in c["xs"])


FNS.update(dict(measure2=measure2, measure_claim=measure_claim, best_tool=best_tool, best_unit=best_unit, pair_units=pair_units,
                unit_number=unit_number, smaller_more=smaller_more, unit_size=unit_size, rep_unit=rep_unit, estimate_len=estimate_len,
                estimate_unit=estimate_unit, lp_two=lp_two))


# ---------------------------------------------------------------- unit 9 (number line)
def point_val(c, t):
    v = _unit(c, t)
    return v is not None and v == c["v"]


def point_label(c, t):
    hits = [k for k, v in c["points"].items() if v == c["v"]]
    return hits == [str(t).strip()]


def lead_len(c, t):
    v = c["v"]
    return str(t).strip() == f"No. Count the spaces from 0, not the tick marks. The length is {v}."


def jump_eq(c, t):
    m = re.fullmatch(r"(\d+) ([+−]) (\d+) = (\d+)", str(t).strip())
    if not m or not _eq(t):
        return False
    s, op, k, e = int(m.group(1)), m.group(2), int(m.group(3)), int(m.group(4))
    return s == c["start"] and e == c["end"] and (op == "+") == (c["end"] > c["start"])


def jump_desc(c, t):
    m = re.fullmatch(r"Start at (\d+) and jump (forward|back) (\d+)\.", str(t).strip())
    return bool(m) and int(m.group(1)) == c["start"] and int(m.group(3)) == c["size"] and (m.group(2) == "forward") == (c["op"] == "+")


FNS.update(dict(point_val=point_val, point_label=point_label, lead_len=lead_len, jump_eq=jump_eq, jump_desc=jump_desc))


# ---------------------------------------------------------------- unit 10 (time and money)
def _t2(text):
    m = re.fullmatch(r"\s*(\d{1,2}):(\d{2})(?: (AM|PM))?\s*", str(text))
    if not m:
        return None
    h, mi = int(m.group(1)), int(m.group(2))
    if not (1 <= h <= 12 and mi < 60):
        return None
    return h, mi, m.group(3)


def _h24(h, ap):
    return (h % 12) + (12 if ap == "PM" else 0)


def min_after(c, t):
    v = _unit(c, t)
    return v is not None and v == 5 * c["hand"]


def min_point(c, t):
    v = _unit(c, t)
    return v is not None and 5 * v == c["m"] and 1 <= v <= 11


def clock_reason(c, t):
    h, m = c["h"], c["m"]
    return str(t).strip() == f"No. The minute hand on the {m // 5} means {m} minutes, so the time is {h}:{m:02d}."


def ampm_of(c, t):
    return str(t).strip() == ("AM" if c["h24"] < 12 else "PM")


def event_time(c, t):
    x = _t2(t)
    return x is not None and x[2] is not None and c["lo"] <= _h24(x[0], x[2]) < c["hi"]


def time_ampm(c, t):
    x = _t2(t)
    return x is not None and x[0] == c["h"] and x[1] == c["m"] and x[2] == ("AM" if c["h24"] < 12 else "PM") and _h24(x[0], x[2]) == c["h24"] % 24


def earlier(c, t):
    xs = [_t2(s) for s in c["times"]]
    keys = [(_h24(h, ap), mi) for h, mi, ap in xs]
    if keys[0] == keys[1]:
        return False
    return str(t).strip() == c["times"][keys.index(min(keys))]


CV = {"penny": 1, "pennies": 1, "nickel": 5, "nickels": 5, "dime": 10, "dimes": 10, "quarter": 25, "quarters": 25}


def _coins(text):
    parts = re.split(r", | and ", str(text).strip())
    tot, n = 0, 0
    for p in parts:
        m = re.fullmatch(r"(\d+) (penny|pennies|nickels?|dimes?|quarters?)", p)
        if not m:
            return None
        k = int(m.group(1))
        if (k == 1) != (m.group(2) in ("penny", "nickel", "dime", "quarter")):
            return None
        tot += k * CV[m.group(2)]
        n += k
    return tot, n


def coin_value(c, t):
    x = _coins(t)
    return x is not None and x[0] == c["v"]


def coin_is(c, t):
    val = {"penny": 1, "nickel": 5, "dime": 10, "quarter": 25}[c["coin"]]
    if c["what"] == "value":
        return str(t).strip() == f"{val}¢"
    return str(t).strip() == c["coin"]


def fewest(c, t):
    x = _coins(t)
    if x is None or x[0] != c["v"]:
        return False
    best = [10 ** 9] * (c["v"] + 1)
    best[0] = 0
    for s in range(1, c["v"] + 1):
        for d in (1, 5, 10, 25):
            if d <= s:
                best[s] = min(best[s], best[s - d] + 1)
    return x[1] == best[c["v"]]


def dollars_cents(c, t):
    m = re.fullmatch(r"\$(\d+) and (\d+)¢", str(t).strip())
    return bool(m) and int(m.group(1)) == c["d"] and int(m.group(2)) == c["c"]


def money_sym(c, t):
    return str(t).strip() == (f"{c['v']}¢" if c["form"] == "cents" else f"${c['v']}")


def enough(c, t):
    v, p = c["v"], c["price"]
    s = str(t).strip()
    if v >= p:
        return s.startswith("Yes.") and f"has {v}¢, which is {v - p}¢ more than {p}¢" in s
    return s.startswith("No.") and f"has {v}¢ and needs {p - v}¢ more" in s


FNS.update(dict(min_after=min_after, min_point=min_point, clock_reason=clock_reason, ampm_of=ampm_of, event_time=event_time, time_ampm=time_ampm,
                earlier=earlier, coin_value=coin_value, coin_is=coin_is, fewest=fewest, dollars_cents=dollars_cents, money_sym=money_sym, enough=enough))


# ---------------------------------------------------------------- unit 11 (graphs)
def graph_extreme(c, t):
    v = c["vals"]
    best = max(v) if c["want"] == "most" else min(v)
    return v.count(best) == 1 and str(t).strip() == c["cats"][v.index(best)]


def graph_claim(c, t):
    i = c["i"]
    return str(t).strip() == f"No. Each picture stands for 1, so {c['cats'][i]} has {c['vals'][i]}."


def tally_val(c, t):
    v = _unit(c, t)
    return v is not None and v == c["counts"][c["i"]]


def graph_list(c, t):
    want = ", ".join(f"{a} {b}" for a, b in zip(c["cats"], c["vals"]))
    return str(t).strip() == want


FNS.update(dict(graph_extreme=graph_extreme, graph_claim=graph_claim, tally_val=tally_val, graph_list=graph_list))


# ---------------------------------------------------------------- unit 12 (shapes and equal shares)
PN = {3: "triangle", 4: "quadrilateral", 5: "pentagon", 6: "hexagon"}


def _corners(pts):
    """Number of true corners of a simple polygon (collinear points are not corners)."""
    n = len(pts)
    k = 0
    for i in range(n):
        (x1, y1), (x2, y2), (x3, y3) = pts[i - 1], pts[i], pts[(i + 1) % n]
        if (x2 - x1) * (y3 - y2) - (y2 - y1) * (x3 - x2) != 0:
            k += 1
    return k


def poly_name(c, t):
    return norm(t) == PN[_corners(c["pts"])]


def poly_count(c, t):
    v = _unit(c, t)
    return v is not None and v == _corners(c["pts"])


def shape_label(c, t):
    hits = [it["label"] for it in c["items"] if _corners(it["pts"]) == c["sides"]]
    return hits == [str(t).strip()]


def name_sides(c, t):
    return norm(t) == PN[c["n"]]


def count_named(c, t):
    v = _unit(c, t)
    return v is not None and v == sum(1 for it in c["items"] if _corners(it["pts"]) == c["sides"])


def turned_name(c, t):
    n = _corners(c["pts"])
    return str(t).strip() == f"It is a {PN[n]}, because it still has {n} sides and {n} angles."


SIDES = {v: k for k, v in PN.items()}


def sides_total(c, t):
    v = _unit(c, t)
    return v is not None and v == sum(SIDES[x] for x in c["names"])


def sides_more(c, t):
    v = _unit(c, t)
    return v is not None and v == SIDES[c["big"]] - SIDES[c["small"]]


def must_angles(c, t):
    return str(t).strip() == f"It has {c['n']} angles."


def solid_label(c, t):
    hits = [it["label"] for it in c["items"] if it["kind"] == c["kind"]]
    return hits == [str(t).strip()]


def solid_count(c, t):
    v = _unit(c, t)
    return v is not None and v == sum(1 for it in c["items"] if it["kind"] == c["kind"])


CUBE = {"faces": 6, "edges": 12, "vertices": 8}


def cube_parts(c, t):
    v = _unit(c, t)
    return v is not None and v == CUBE[c["what"]] * c["cubes"]


def is_word(c, t):
    return norm(t) == c["word"]


def rows_cols(c, t):
    m = re.fullmatch(r"(\d+) rows? and (\d+) columns?", str(t).strip())
    return bool(m) and int(m.group(1)) == c["rows"] and int(m.group(2)) == c["cols"]


def equal_parts(c, t):
    eq = len(set(c["widths"])) == 1
    return str(t).strip() == ("Yes. All the parts are the same size." if eq else "No. One part is bigger than the others.")


SH = {2: ("half", "halves"), 3: ("third", "thirds"), 4: ("fourth", "fourths")}
NW = {1: "one", 2: "two", 3: "three", 4: "four"}


def share_name(c, t):
    return norm(t) == SH[c["n"]][1]


def share_shaded(c, t):
    n, k = c["n"], c["part"]
    return norm(t) == f"{NW[k]} {SH[n][0] if k == 1 else SH[n][1]}"


def share_one(c, t):
    return norm(t) == f"one {SH[c['n']][0]}"


def bigger_share(c, t):
    return norm(t) == f"one {SH[min(c['a'], c['b'])][0]}"


def cuts_for(c, t):
    return str(t).strip() == f"{c['n']} equal shares"


def whole_count(c, t):
    v = _unit(c, t)
    return v is not None and v == c["n"]


def whole_words(c, t):
    return norm(t) == f"{NW[c['n']]} {SH[c['n']][1]}"


def more_shares(c, t):
    v = _unit(c, t)
    return v is not None and v + c["have"] == c["n"]


FNS.update(dict(poly_name=poly_name, poly_count=poly_count, shape_label=shape_label, name_sides=name_sides, count_named=count_named,
                turned_name=turned_name, sides_total=sides_total, sides_more=sides_more, must_angles=must_angles, solid_label=solid_label,
                solid_count=solid_count, cube_parts=cube_parts, is_word=is_word, rows_cols=rows_cols, equal_parts=equal_parts,
                share_name=share_name, share_shaded=share_shaded, share_one=share_one, bigger_share=bigger_share, cuts_for=cuts_for,
                whole_count=whole_count, whole_words=whole_words, more_shares=more_shares))


def coins_calc(c, t):
    """add + value(plus coins) - value(minus coins) - sub, in cents (coin values from the coin names)."""
    val = {"penny": 1, "nickel": 5, "dime": 10, "quarter": 25}
    want = c.get("add", 0) + sum(val[k] for k in c.get("plus", [])) - sum(val[k] for k in c.get("minus", [])) - c.get("sub", 0)
    return _len(c, t) == want


FNS["coins_calc"] = coins_calc


def day_part(c, t):
    h = c["h24"]
    want = "morning" if 5 <= h < 12 else "afternoon" if 12 <= h < 18 else "night"
    return norm(t) == want


FNS["day_part"] = day_part

# Grade 2 verifier extensions. These checks interpret the stored question data,
# independently of item-generation families. Included for all published formats.
def _numeric_answer(text, expected, unit=None):
    parsed = V['parse_value'](text)
    if parsed is None or parsed[0] != expected:
        return False
    return V['unorm'](parsed[1]) == V['unorm'](unit) if unit is not None else parsed[1] == ''


def _equation_is_true(eq):
    lhs, rhs = str(eq).replace('−', '-').split('=', 1)
    return V['eval_expr'](lhs.strip()) == V['eval_expr'](rhs.strip())


def blank_eq(c, text):
    parsed = V['parse_value'](text)
    if parsed is None or parsed[0].denominator != 1 or V['unorm'](parsed[1]) != V['unorm'](c.get('unit','')):
        return False
    eq = c['eq']
    if eq.count('___') != 1:
        return False
    return _equation_is_true(eq.replace('___', str(parsed[0])))


def true_eq(c, text):
    try:
        return _equation_is_true(text)
    except (ValueError, SyntaxError, ZeroDivisionError, TypeError):
        return False


def false_eq(c, text):
    try:
        return not _equation_is_true(text)
    except (ValueError, SyntaxError, ZeroDivisionError, TypeError):
        return False


def skip_missing(c, text):
    parsed = V['parse_value'](text)
    if parsed is None or parsed[1] != '' or parsed[0].denominator != 1:
        return False
    parts = [x.strip() for x in c['seq'].split(',')]
    if parts.count('?') != 1:
        return False
    i = parts.index('?')
    start = next((int(x)-j*c['step'] for j,x in enumerate(parts) if x != '?'),None)
    return start is not None and all(x == '?' or int(x) == start+j*c['step'] for j,x in enumerate(parts)) and parsed[0] == start+i*c['step']


def missing_digit(c, text):
    parsed = V['parse_value'](text)
    if parsed is None or parsed[1] or parsed[0].denominator != 1 or not (0 <= parsed[0] <= 9):
        return False
    shown = str(c['shown'])
    if shown.count('□') != 1:
        return False
    a = int(shown.replace('□',str(parsed[0])))
    return ((a+c['other']==c['total']) if c['op']=='+' else (a-c['other']==c['total']) if c['op'] in ('-', '−') else False)


def clock(c, text):
    m = re.fullmatch(r'(\d{1,2}):(\d{2})',str(text).strip())
    return bool(m) and int(m.group(1)) == c['h'] and int(m.group(2)) == c['m']


def pic_value(c, text):
    return _numeric_answer(text,c['syms'][c['i']]*c['key'],c.get('unit'))


def pic_sum(c, text):
    return _numeric_answer(text,sum(c['syms'][i]*c['key'] for i in c['idx']),c.get('unit'))


def bar_value(c, text):
    return _numeric_answer(text,c['vals'][c['i']],c.get('unit'))


def bar_diff(c, text):
    return _numeric_answer(text,abs(c['vals'][c['i']]-c['vals'][c['j']]),c.get('unit'))


def bar_combo(c, text):
    v = sum(c['vals'][i] for i in c['plus'])-sum(c['vals'][i] for i in c['minus'])
    return _numeric_answer(text,v,c.get('unit'))


def bar_has(c, text):
    names = [str(name) for name,value in zip(c['cats'],c['vals']) if value == c['v']]
    return V['norm'](text) in [V['norm'](n) for n in names] if names else V['norm'](text) == 'no bar'


FNS.update({name: globals()[name] for name in (
    'blank_eq', 'true_eq', 'false_eq', 'skip_missing', 'missing_digit', 'clock',
    'pic_value', 'pic_sum', 'bar_value', 'bar_diff', 'bar_combo', 'bar_has')})

# Calculate a displayed 12-hour clock time after a stated duration.
def end_time(c, text):
    start = re.fullmatch(r'(\d{1,2}):(\d{2})', c['a'])
    answer = re.fullmatch(r'(\d{1,2}):(\d{2})', str(text).strip())
    if not start or not answer:
        return False
    minutes = (int(start.group(1)) % 12) * 60 + int(start.group(2)) + int(c['d'])
    minutes %= 720
    hour = (minutes // 60) or 12
    return (int(answer.group(1)), int(answer.group(2))) == (hour, minutes % 60)

FNS['end_time'] = end_time
