"""Unit 10: Data, Line Plots, and Multi-Step Word Problems (4.MD.B.4, 4.OA.A.3)."""
from g4lib import *

UNIT_ID = "data-line-plots-word-problems"
TOPICS = [("Lengths of Pencils", "inches", "pencils", "long"), ("Lengths of Leaves", "inches", "leaves", "long"), ("Heights of Seedlings", "inches", "seedlings", "tall"),
          ("Lengths of Ribbons", "feet", "ribbons", "long"), ("Distances Walked", "miles", "students", "far"), ("Rainfall Each Day", "inches", "days", "much"),
          ("Lengths of Caterpillars", "inches", "caterpillars", "long"), ("Weights of Tomatoes", "pounds", "tomatoes", "heavy")]


def mxv(v):
    """Fraction -> mixed-number text that keeps the plot's denominator when possible (2 2/4 stays 2 2/4? no: simplest form)."""
    return mixed(v)


def plot(r, L, small=False):
    den = pick(r, [2, 4] if L == 0 else [2, 4, 8] if L == 1 else [4, 8])
    lo = r.randint(0, 5)
    span = {2: 3, 4: 2, 8: 1}[den]
    ticks = [lo + F(i, den) for i in range(span * den + 1)]
    k = r.randint(5, 7) if small else r.randint(8, 14)
    vals = [pick(r, ticks) for _ in range(k)]
    need(len(set(vals)) >= 3)
    t = pick(r, TOPICS)
    def lab(v):
        w, rem = divmod(v.numerator, v.denominator)
        return str(w) if rem == 0 else (f"{w} {rem}/{v.denominator}" if w else f"{rem}/{v.denominator}")
    sv = [lab(v) for v in sorted(vals)]
    cnt = {}
    for v in sorted(vals):
        cnt[lab(v)] = cnt.get(lab(v), 0) + 1
    alt = f"A line plot titled {t[0]}. The number line goes from {lo} to {lo + span} {t[1]} with tick marks every 1/{den}. X marks: " + "; ".join(f"{c} above {x}" for x, c in cnt.items()) + "."
    dg = Diagram("lineplot", {"values": sv, "lo": str(lo), "hi": str(lo + span), "den": den, "title": t[0], "unit": t[1].capitalize()}, alt)
    return vals, sv, t, dg, lab, ticks


def unit_s(v, u):
    return u if v != 1 and not (0 < v < 1) else {"inches": "inch", "feet": "foot", "miles": "mile", "pounds": "pound"}[u]


# ============================================================== S1 Reading and Making Line Plots
@fam("012")
def lp_count_at(r, L):
    vals, sv, t, dg, lab, ticks = plot(r, L)
    x = pick(r, sorted(set(vals)))
    c = vals.count(x)
    return Item(f"The line plot shows data about {t[2]}. Each X stands for one measurement. How many measurements are exactly {lab(x)} {unit_s(x, t[1])}?", str(c),
                [f"Find {lab(x)} on the number line and count the X marks above it.", f"There are {c}."],
                [W(str(c + 1), "counted one X mark from a neighboring value"), W(str(len(vals)), "counted every X on the plot"), W(str(abs(c - 1)) if c != 1 else "0", "missed one X mark"), W(str(c + 2), "counted two columns")],
                FN("lp", values=sv, op="count_at", x=lab(x)), qtype="visual", diagram=dg)


@fam("012")
def lp_total_n(r, L):
    vals, sv, t, dg, lab, ticks = plot(r, L)
    return Item(f"The line plot shows data about {t[2]}. Each X stands for one measurement. How many measurements are shown in all?", str(len(vals)),
                ["Count every X on the plot.", f"There are {len(vals)} measurements."],
                [W(str(len(set(vals))), "counted the columns instead of the X marks"), W(str(len(vals) + 1), "counted one X twice"), W(str(len(vals) - 1), "missed one X mark"), W(str(len(ticks)), "counted the tick marks on the number line") if len(ticks) not in (len(vals), len(vals) + 1, len(vals) - 1, len(set(vals))) else W(str(len(vals) + 2), "miscounted")],
                FN("lp", values=sv, op="n"), qtype="visual", diagram=dg)


@fam("012")
def lp_mode(r, L):
    vals, sv, t, dg, lab, ticks = plot(r, L)
    cnt = {v: vals.count(v) for v in set(vals)}
    mx = max(cnt.values())
    need(sum(1 for c in cnt.values() if c == mx) == 1)
    m = [v for v, c in cnt.items() if c == mx][0]
    others = sorted(set(vals) - {m})
    return Item(f"The line plot shows data about {t[2]}. Which measurement appears most often?", f"{lab(m)} {unit_s(m, t[1])}",
                ["Look for the tallest stack of X marks.", f"The tallest stack is above {lab(m)}."],
                [W(f"{lab(max(vals))} {unit_s(max(vals), t[1])}", "chose the greatest value instead of the most common one") if max(vals) != m else W(f"{lab(min(vals))} {unit_s(min(vals), t[1])}", "chose the least value"), W(f"{mx} {t[1]}" if F(mx) != m else f"{mx + 1} {t[1]}", "gave the number of X marks instead of the measurement"), W(f"{lab(others[0])} {unit_s(others[0], t[1])}", "chose a shorter stack")],
                FN("lp", values=sv, op="mode", unit=t[1]), qtype="visual", diagram=dg)


@fam("012")
def lp_count_compare(r, L):
    vals, sv, t, dg, lab, ticks = plot(r, L)
    x = pick(r, ticks[1:-1])
    op = pick(r, ["count_gt", "count_lt"] if L else ["count_gt"])
    c = sum(1 for v in vals if (v > x if op == "count_gt" else v < x))
    eq = vals.count(x)
    return Item(f"The line plot shows data about {t[2]}. How many measurements are {'greater' if op == 'count_gt' else 'less'} than {lab(x)} {unit_s(x, t[1])}?", str(c),
                [f"Count the X marks to the {'right' if op == 'count_gt' else 'left'} of {lab(x)}. Do not count the X marks above {lab(x)}.", f"There are {c}."],
                [W(str(c + eq) if eq else str(c + 1), f"also counted the X marks above {lab(x)}" if eq else "miscounted"), W(str(len(vals) - c - eq) if len(vals) - c - eq not in (c, c + eq) else str(c + 2), "counted the wrong side"), W(str(len(vals)), "counted every X"), W(str(abs(c - 1)) if c != 1 else "3", "missed one X mark")],
                FN("lp", values=sv, op=op, x=lab(x)), qtype="visual", diagram=dg, tags={"reasoning"})


@fam("012", mode="mc")
def lp_make(r, L):
    vals, sv, t, dg, lab, ticks = plot(r, L, small=True)
    order = [lab(v) for v in vals]
    x = pick(r, sorted(set(vals)))
    c = vals.count(x)
    return Item(f"{name(r)} measures some {t[2]} and records these values, in {t[1]}: {', '.join(order)}. On a line plot of the data, how many X marks belong above {lab(x)}?", str(c),
                [f"Count how many times {lab(x)} appears in the list.", f"It appears {c} time{'s' if c != 1 else ''}, so draw {c} X mark{'s' if c != 1 else ''}."],
                [W(str(c + 1), "counted a different value"), W(str(len(vals)), "counted every value"), W(str(c + 2), "miscounted"), W("0" if c != 0 else "4", "did not find the value in the list")],
                FN("lp", values=order, op="count_at", x=lab(x)), qtype="conceptual", tags={"modeling"})


@fam("012", mode="mc")
def lp_match_data(r, L):
    vals, sv, t, dg, lab, ticks = plot(r, L, small=True)
    def mut(kind):
        v = sorted(vals)
        if kind == 0:
            i = r.randrange(len(v))
            cands = [x for x in ticks if x != v[i]]
            v[i] = pick(r, cands)
        elif kind == 1:
            v = v[:-1]
        else:
            v = v + [pick(r, ticks)]
        return ", ".join(lab(x) for x in sorted(v))
    good = ", ".join(sv)
    bad = [mut(0), mut(1), mut(2)]
    need(len({good, *bad}) == 4)
    return Item("Which list of data matches the line plot?", good, ["Read the plot from left to right. Write each value once for every X above it.", f"The data are {good}."],
                [W(bad[0], "one value does not match the plot"), W(bad[1], "one X is missing from the list"), W(bad[2], "the list has an extra value")], FN("lp_data", values=sv), qtype="visual", diagram=dg, tags={"multiple-representations"})


@fam("012")
def lp_max(r, L):
    vals, sv, t, dg, lab, ticks = plot(r, L)
    m = max(vals)
    return Item(f"The line plot shows data about {t[2]}. What is the greatest measurement shown?", f"{lab(m)} {unit_s(m, t[1])}", ["Find the X that is farthest to the right.", f"It is above {lab(m)}."],
                [W(f"{lab(ticks[-1])} {unit_s(ticks[-1], t[1])}", "used the end of the number line instead of the last X") if ticks[-1] != m else W(f"{lab(min(vals))} {unit_s(min(vals), t[1])}", "chose the least value"), W(f"{lab(min(vals))} {unit_s(min(vals), t[1])}" if ticks[-1] != m else f"{lab(sorted(set(vals))[-2])} {unit_s(sorted(set(vals))[-2], t[1])}", "chose a different value"), W(f"{len(vals)} {t[1]}" if F(len(vals)) != m else f"{len(vals) + 1} {t[1]}", "counted the X marks")],
                FN("lp", values=sv, op="max", unit=t[1]), qtype="visual", diagram=dg)


# ============================================================== S2 Solving Problems with Line Plots
def fw(v, u):
    return f"{mixed(v)} {unit_s(v, u)}"


@fam("012")
def ls_range(r, L):
    vals, sv, t, dg, lab, ticks = plot(r, L)
    hi, lo = max(vals), min(vals)
    d = hi - lo
    return Item(f"The line plot shows data about {t[2]}. What is the difference between the greatest and the least measurement?", fw(d, t[1]),
                [f"The greatest is {lab(hi)} and the least is {lab(lo)}.", f"{lab(hi)} − {lab(lo)} = {mixed(d)} {unit_s(d, t[1])}."],
                [W(fw(hi + lo, t[1]), "added instead of subtracting"), W(fw(hi, t[1]), "gave the greatest measurement"), W(fw(ticks[-1] - ticks[0], t[1]), "used the ends of the number line") if ticks[-1] - ticks[0] != d else W(fw(d + 1, t[1]), "made a subtraction mistake"), W(fw(d + F(1, hi.denominator if hi.denominator > 1 else 2), t[1]), "made a subtraction mistake")],
                FN("lp", values=sv, op="diff", unit=t[1]), qtype="multi-step", diagram=dg, tags={"multistep"})


@fam("012")
def ls_total_at(r, L):
    vals, sv, t, dg, lab, ticks = plot(r, L)
    c2 = [v for v in set(vals) if 2 <= vals.count(v) <= 4 and v.denominator > 1]
    need(c2)
    x = pick(r, c2)
    c = vals.count(x)
    tot = x * c
    return Item(f"The line plot shows data about {t[2]}. What is the total of all the measurements that are exactly {lab(x)} {t[1]}?", fw(tot, t[1]),
                [f"There are {c} X marks above {lab(x)}.", f"Add {lab(x)} {c} times: {mixed(tot)} {t[1]}."],
                [W(fw(x, t[1]), "did not add the repeated measurements"), W(f"{c} {t[1]}", "gave the number of X marks"), W(fw(tot + x, t[1]), "added one measurement too many"), W(fw(x * c - F(1, x.denominator), t[1]), "made an addition mistake")],
                FN("lp", values=sv, op="total_at", x=lab(x), unit=t[1]), qtype="multi-step", diagram=dg, tags={"multistep"})


@fam("012")
def ls_count_diff(r, L):
    vals, sv, t, dg, lab, ticks = plot(r, L)
    u = sorted(set(vals), key=lambda v: -vals.count(v))
    need(vals.count(u[0]) > vals.count(u[-1]))
    x, y = u[0], u[-1]
    d = vals.count(x) - vals.count(y)
    return Item(f"The line plot shows data about {t[2]}. How many more measurements are {lab(x)} {unit_s(x, t[1])} than {lab(y)} {unit_s(y, t[1])}?", str(d),
                [f"There are {vals.count(x)} X marks above {lab(x)} and {vals.count(y)} above {lab(y)}.", f"{vals.count(x)} − {vals.count(y)} = {d}."],
                [W(str(vals.count(x) + vals.count(y)), "added instead of subtracting"), W(str(vals.count(x)), "gave only one of the counts"), W(str(d + 1), "miscounted"), W(mixed(abs(x - y)) if mixed(abs(x - y)) not in (str(d), str(d + 1)) else str(d + 2), "subtracted the measurements instead of the counts")],
                FN("lp", values=sv, op="count_diff", x=lab(x), y=lab(y)), qtype="visual", diagram=dg, tags={"reasoning"})


@fam("012")
def ls_two_extremes(r, L):
    vals, sv, t, dg, lab, ticks = plot(r, L)
    k = 2
    which = pick(r, ["shortest", "longest"]) if t[3] == "long" else pick(r, ["least", "greatest"])
    sv_ = sorted(vals)
    part = sv_[:k] if which in ("shortest", "least") else sv_[-k:]
    tot = sum(part)
    need(part[0].denominator > 1 or part[1].denominator > 1)
    return Item(f"The line plot shows data about {t[2]}. What is the sum of the two {which} measurements? (Each X is one measurement.)", fw(tot, t[1]),
                [f"The two {which} measurements are {lab(part[0])} and {lab(part[1])}.", f"{lab(part[0])} + {lab(part[1])} = {mixed(tot)} {t[1]}."],
                [W(fw(abs(part[1] - part[0]), t[1]) if part[1] != part[0] else fw(part[0], t[1]), "subtracted instead of adding"), W(fw(sv_[0] + sv_[-1], t[1]) if sv_[0] + sv_[-1] != tot else fw(tot + 1, t[1]), "added the least and the greatest"), W(fw(tot + F(1, 2), t[1]), "made an addition mistake"), W(fw(tot + 1, t[1]), "added an extra whole")],
                FN("lp2", values=sv, op="sum_low" if which in ("shortest", "least") else "sum_high", count=k, unit=t[1]), qtype="multi-step", diagram=dg, tags={"multistep"})


@fam("12")
def ls_total(r, L):
    vals, sv, t, dg, lab, ticks = plot(r, L, small=True)
    tot = sum(vals)
    return Item(f"The line plot shows data about {t[2]}. What is the total of all the measurements?", fw(tot, t[1]),
                ["Add the wholes, then add the fractions with the same denominator and regroup.", f"The total is {mixed(tot)} {t[1]}."],
                [W(f"{len(vals)} {t[1]}" if F(len(vals)) != tot else f"{len(vals) + 1} {t[1]}", "counted the X marks"), W(fw(tot + 1, t[1]), "added an extra whole when regrouping"), W(fw(tot - F(1, 2) if tot > 1 else tot + F(1, 2), t[1]), "made an addition mistake"), W(fw(sum(set(vals)), t[1]) if sum(set(vals)) != tot else fw(tot + 2, t[1]), "added each value only once")],
                FN("lp", values=sv, op="total", unit=t[1]), qtype="multi-step", diagram=dg, tags={"multistep", "challenge"})


@fam("12")
def ls_max_minus_mode(r, L):
    vals, sv, t, dg, lab, ticks = plot(r, L)
    cnt = {v: vals.count(v) for v in set(vals)}
    mx = max(cnt.values())
    need(sum(1 for c in cnt.values() if c == mx) == 1)
    m = [v for v, c in cnt.items() if c == mx][0]
    d = max(vals) - m
    need(d > 0)
    return Item(f"The line plot shows data about {t[2]}. How much greater is the greatest measurement than the measurement that appears most often?", fw(d, t[1]),
                [f"The greatest is {lab(max(vals))}. The most common is {lab(m)}.", f"{lab(max(vals))} − {lab(m)} = {mixed(d)} {unit_s(d, t[1])}."],
                [W(fw(max(vals) - min(vals), t[1]) if max(vals) - min(vals) != d else fw(d + 1, t[1]), "subtracted the least measurement instead of the most common one"), W(fw(max(vals) + m, t[1]), "added instead of subtracting"), W(fw(m, t[1]), "gave the most common measurement"), W(fw(d + F(1, 4), t[1]), "made a subtraction mistake")],
                FN("lp", values=sv, op="max_minus_mode", unit=t[1]), qtype="multi-step", diagram=dg, tags={"multistep", "reasoning"})


# ============================================================== S3 Multi-Step Word Problems
@fam("012")
def ms_shop(r, L):
    n1, p1 = r.randint(2, 5), r.randint(3, 9) if L == 0 else r.randint(8, 25)
    n2, p2 = r.randint(2, 4), r.randint(2, 8) if L == 0 else r.randint(6, 20)
    cost = n1 * p1 + n2 * p2
    pay = (cost // 50 + 1) * 50 if L else (cost // 10 + 1) * 10 + 10
    i1, i2 = r.sample(["notebooks", "T‑shirts", "puzzles", "posters", "plants", "games", "caps"], 2)
    nm = name(r)
    if L == 0:
        return Item(f"{nm} buys {n1} {i1} for ${p1} each and {n2} {i2} for ${p2} each. How much does {nm} spend in all?", f"${cost}",
                    [f"{n1} × {p1} = {n1 * p1} and {n2} × {p2} = {n2 * p2}.", f"{n1 * p1} + {n2 * p2} = {cost}, so the total is ${cost}."],
                    [W(f"${p1 + p2}", "added the two prices without multiplying"), W(f"${(n1 + n2) * (p1 + p2)}", "added first and then multiplied"), W(f"${n1 * p1}", "left out the second item"), W(f"${cost + p2}", "counted an extra item")],
                    EX(f"{n1} × {p1} + {n2} × {p2}"), qtype="multi-step", tags={"multistep"})
    return Item(f"{nm} buys {n1} {i1} for ${p1} each and {n2} {i2} for ${p2} each. {nm} pays with ${pay}. How much change does {nm} get?", f"${pay - cost}",
                [f"Cost: {n1} × {p1} + {n2} × {p2} = {n1 * p1} + {n2 * p2} = {cost}.", f"Change: {pay} − {cost} = {pay - cost}, so the change is ${pay - cost}."],
                [W(f"${cost}", "found the cost but not the change"), W(f"${pay - n1 * p1}", "left out the second item"), W(f"${pay - p1 - p2}", "did not multiply by the number of items"), W(f"${pay - cost + 10}", "made a subtraction mistake")],
                EX(f"{pay} − ({n1} × {p1} + {n2} × {p2})"), qtype="multi-step", tags={"multistep"})


@fam("012")
def ms_pack(r, L):
    per = r.randint(4, 9)
    boxes = r.randint(6, 12) if L == 0 else r.randint(15, 60)
    extra = r.randint(1, per - 1)
    total = per * boxes + extra
    thing = pick(r, ["muffins", "candles", "oranges", "golf balls", "cupcakes", "bars of soap"])
    sold = r.randint(2, boxes - 2)
    if L == 2:
        return Item(f"A shop has {comma(total)} {thing}. Workers pack them into boxes of {per}. Then the shop sells {sold} of the full boxes. How many full boxes are left?", f"{boxes - sold} boxes",
                    [f"{comma(total)} ÷ {per} = {boxes} R {extra}, so there are {boxes} full boxes.", f"{boxes} − {sold} = {boxes - sold} boxes."],
                    [W(f"{boxes + 1 - sold} boxes", "counted the box that is not full"), W(f"{boxes} boxes", "forgot the boxes that were sold"), W(f"{extra} boxes", "gave the remainder"), W(f"{boxes + sold} boxes", "added instead of subtracting")],
                    FN("pack_left", total=total, per=per, sold=sold, unit="boxes"), qtype="multi-step", tags={"multistep", "reasoning"})
    return Item(f"A baker makes {comma(per * boxes)} {thing} and packs them equally into {boxes} boxes. Then the baker adds {extra} more to each box. How many {thing} are in each box now?", f"{per + extra} {thing}",
                [f"{comma(per * boxes)} ÷ {boxes} = {per} in each box.", f"{per} + {extra} = {per + extra} {thing}."],
                [W(f"{per} {thing}", "stopped after dividing"), W(f"{comma(per * boxes + extra)} {thing}", "added before dividing and did not divide"), W(f"{per * extra} {thing}", "multiplied instead of adding"), W(f"{per + extra + 1} {thing}", "made a division mistake")],
                EX(f"{per * boxes} ÷ {boxes} + {extra}", unit=thing), qtype="multi-step", tags={"multistep"})


@fam("012")
def ms_save(r, L):
    wk = r.randint(4, 9) if L < 2 else r.randint(8, 16)
    per = r.randint(5, 12) if L == 0 else r.randint(12, 35)
    have = r.randint(10, 60)
    price = have + wk * per + r.randint(15, 90)
    nm = name(r)
    thing = pick(r, ["bike", "tablet", "telescope", "skateboard", "guitar"])
    need_ = price - have - wk * per
    return Item(f"{nm} wants to buy a {thing} that costs ${price}. {nm} has ${have} and saves ${per} each week for {wk} weeks. How much more money does {nm} still need?", f"${need_}",
                [f"Savings: {wk} × {per} = {wk * per}. Money so far: {have} + {wk * per} = {have + wk * per}.", f"{price} − {have + wk * per} = {need_}, so {nm} still needs ${need_}."],
                [W(f"${price - wk * per}", "forgot the money already saved"), W(f"${have + wk * per}", "found the money so far"), W(f"${price - have - per}", "did not multiply by the number of weeks"), W(f"${need_ + 10}", "made a subtraction mistake")],
                EX(f"{price} − {have} − {wk} × {per}"), qtype="multi-step", tags={"multistep"})


@fam("012")
def ms_vans(r, L):
    per_bus = pick(r, [24, 28, 30, 36, 40, 45])
    buses = r.randint(2, 5)
    van = pick(r, [6, 7, 8])
    left = r.randint(van + 1, van * 5)
    need(left % van)
    total = per_bus * buses + left
    return Item(f"{comma(total)} students are going on a field trip. {buses} buses each carry {per_bus} students. The rest of the students ride in vans that hold {van} students each. How many vans are needed?", f"{left // van + 1} vans",
                [f"Students on buses: {buses} × {per_bus} = {buses * per_bus}. Students left: {comma(total)} − {buses * per_bus} = {left}.", f"{left} ÷ {van} = {left // van} R {left % van}. The extra students need 1 more van: {left // van + 1} vans."],
                [W(f"{left // van} vans", "dropped the remainder, leaving students without a ride"), W(f"{left} vans", "gave the number of students left"), W(f"{left % van} vans", "gave the remainder"), W(f"{left // van + 2} vans", "added too many")],
                FN("remainder_use", a=f"{total} − {buses} × {per_bus}", b=str(van), mode="up", unit="vans"), qtype="multi-step", tags={"multistep", "reasoning"})


@fam("012")
def ms_compare_total(r, L):
    k = r.randint(2, 5)
    a = r.randint(6, 15) if L == 0 else r.randint(18, 75)
    n1, n2 = r.sample(NAMES, 2)
    thing = pick(r, ["cans", "pages", "stickers", "shells", "points"])
    if L == 2:
        c = r.randint(5, 30)
        return Item(f"{n1} collected {a} {thing}. {n2} collected {k} times as many {thing} as {n1}. Together they gave away {c} {thing}. How many {thing} are left altogether?", f"{a + k * a - c} {thing}",
                    [f"{n2}: {k} × {a} = {k * a}. Together: {a} + {k * a} = {a + k * a}.", f"{a + k * a} − {c} = {a + k * a - c} {thing}."],
                    [W(f"{k * a - c} {thing}", f"left out the amount for {n1}"), W(f"{a + k * a} {thing}", "forgot to subtract"), W(f"{a + k - c if a + k > c else a + k} {thing}", "added instead of multiplying"), W(f"{a + k * a + c} {thing}", "added instead of subtracting")],
                    EX(f"{a} + {k} × {a} − {c}", unit=thing), qtype="multi-step", tags={"multistep"})
    return Item(f"{n1} collected {a} {thing}. {n2} collected {k} times as many {thing} as {n1}. How many {thing} did they collect altogether?", f"{a + k * a} {thing}",
                [f"{n2}: {k} × {a} = {k * a}.", f"Together: {a} + {k * a} = {a + k * a} {thing}."],
                [W(f"{k * a} {thing}", f"left out the amount for {n1}"), W(f"{a + k} {thing}", "added instead of multiplying"), W(f"{2 * k * a} {thing}", "doubled the larger amount"), W(f"{a + k * a + a} {thing}", "added the first amount twice")],
                EX(f"{a} + {k} × {a}", unit=thing), qtype="multi-step", tags={"multistep"})


@fam("012")
def ms_table(r, L):
    items = r.sample([("Adult ticket", "adult tickets"), ("Child ticket", "child tickets"), ("Popcorn", "bags of popcorn"), ("Juice", "bottles of juice"), ("Program", "programs"), ("Parking pass", "parking passes")], 3)
    prices = [r.randint(3, 9) if L == 0 else r.randint(6, 24) for _ in items]
    i, j = r.sample(range(3), 2)
    a, b = r.randint(2, 4), r.randint(2, 6)
    rows = [[it[0], f"${p}"] for it, p in zip(items, prices)]
    alt = "A price table. " + "; ".join(f"{x}: {y}" for x, y in rows) + "."
    v = a * prices[i] + b * prices[j]
    return Item(f"The table shows prices at a school play. What is the total cost of {a} {items[i][1]} and {b} {items[j][1]}?", f"${v}",
                [f"{a} × {prices[i]} = {a * prices[i]} and {b} × {prices[j]} = {b * prices[j]}.", f"{a * prices[i]} + {b * prices[j]} = {v}, so the total is ${v}."],
                [W(f"${prices[i] + prices[j]}", "added the prices without multiplying"), W(f"${(a + b) * prices[i]}", "used one price for every item"), W(f"${v + prices[j]}", "counted an extra item"), W(f"${a * prices[j] + b * prices[i]}" if a * prices[j] + b * prices[i] != v else f"${v + 2}", "matched the numbers to the wrong prices")],
                EX(f"{a} × {prices[i]} + {b} × {prices[j]}"), qtype="real-world", diagram=Diagram("table", {"header": ["Item", "Price"], "rows": rows}, alt), tags={"modeling", "multistep"})


@fam("12")
def ms_read(r, L):
    pages = r.randint(180, 480)
    per = r.randint(12, 35)
    days = r.randint(4, 9)
    need(pages - per * days > per)
    left = pages - per * days
    nm = name(r)
    if L == 2 and left % per:
        return Item(f"{nm} is reading a book with {pages} pages. {nm} reads {per} pages each day for {days} days. If {nm} keeps reading {per} pages each day, how many more days are needed to finish the book?", f"{left // per + 1} days",
                    [f"Pages read: {days} × {per} = {days * per}. Pages left: {pages} − {days * per} = {left}.", f"{left} ÷ {per} = {left // per} R {left % per}. The last {left % per} pages need 1 more day: {left // per + 1} days."],
                    [W(f"{left // per} days", "dropped the remainder, so the book is not finished"), W(f"{left} days", "gave the number of pages left"), W(f"{pages // per + 1} days" if pages // per + 1 != left // per + 1 else f"{left // per + 3} days", "did not subtract the pages already read"), W(f"{left % per} days", "gave the remainder")],
                    FN("remainder_use", a=f"{pages} − {days} × {per}", b=str(per), mode="up", unit="days"), qtype="multi-step", tags={"multistep", "challenge"})
    return Item(f"{nm} is reading a book with {pages} pages. {nm} reads {per} pages each day for {days} days. How many pages are left to read?", f"{left} pages",
                [f"Pages read: {days} × {per} = {days * per}.", f"{pages} − {days * per} = {left} pages."],
                [W(f"{days * per} pages", "found the pages read"), W(f"{pages - per - days} pages", "subtracted without multiplying"), W(f"{pages + days * per} pages", "added instead of subtracting"), W(f"{left + 10} pages", "made a subtraction mistake")],
                EX(f"{pages} − {days} × {per}", unit="pages"), qtype="multi-step", tags={"multistep"})


# ============================================================== S4 Equations and Reasonable Answers
@fam("012", mode="mc")
def eq_choose(r, L):
    a, b = r.randint(3, 9), r.randint(4, 12) if L == 0 else r.randint(12, 40)
    c = r.randint(5, 40)
    nm = name(r)
    kind = r.randrange(3)
    if kind == 0:
        story = f"{nm} has {a} boxes with {b} crayons in each box. {nm} gives away {c} crayons. Let n be the number of crayons {nm} has left."
        need(a * b > c)
        good, v = f"n = {a} × {b} − {c}", a * b - c
        bad = [f"n = {a} × {b} + {c}", f"n = {a} + {b} − {c}", f"n = {a} × ({b} − {c})"]
    elif kind == 1:
        story = f"A class collects {b} cans each day for {a} days. Then a parent donates {c} more cans. Let n be the total number of cans."
        good, v = f"n = {a} × {b} + {c}", a * b + c
        bad = [f"n = {a} × {b} − {c}", f"n = {a} + {b} + {c}", f"n = {a} × ({b} + {c})"]
    else:
        tot = a * b + c
        story = f"{nm} has {tot} beads. {nm} keeps {c} beads and shares the rest equally among {a} friends. Let n be the number of beads each friend gets."
        good, v = f"n = ({tot} − {c}) ÷ {a}", b
        bad = [f"n = {tot} − {c} ÷ {a}", f"n = ({tot} + {c}) ÷ {a}", f"n = ({tot} − {c}) × {a}"]
    return Item(story + " Which equation matches the story?", good, ["Write the steps in the order they happen in the story.", f"{good}, so n = {comma(v)}."],
                [W(x, "the operations do not match the story") for x in bad], FN("eq_with", n=str(v)), qtype="conceptual", tags={"modeling", "reasoning"})


@fam("012")
def eq_value(r, L):
    a, b = r.randint(3, 9), r.randint(6, 15) if L == 0 else r.randint(15, 60)
    c = r.randint(5, 50)
    kind = r.randrange(3)
    if kind == 0:
        return Item(f"Find the value of n: n = {a} × {b} + {c}", comma(a * b + c), [f"Multiply first: {a} × {b} = {a * b}.", f"Then add: {a * b} + {c} = {comma(a * b + c)}."],
                    [W(comma(a * (b + c)), "added before multiplying"), W(comma(a * b), "forgot to add"), W(comma(a + b + c), "added instead of multiplying"), W(comma(a * b - c) if a * b > c else comma(a * b + c + 1), "subtracted instead of adding")], EX(f"{a} × {b} + {c}"), qtype="procedural")
    if kind == 1:
        t = a * b + c
        return Item(f"Find the value of p: {a} × {b} + p = {t}", str(c), [f"{a} × {b} = {a * b}.", f"{a * b} + p = {t}, so p = {t} − {a * b} = {c}."],
                    [W(comma(t + a * b), "added instead of subtracting"), W(comma(t - a - b), "subtracted the factors instead of the product"), W(str(c + 10), "made a subtraction mistake"), W(comma(t), "gave the total")], EX(f"{t} − {a} × {b}"), qtype="procedural", tags={"reasoning"})
    return Item(f"Find the value of n: {a} × n = {a * b}", str(b), [f"Divide the product by the known factor.", f"{a * b} ÷ {a} = {b}."],
                [W(str(a * b - a), "subtracted instead of dividing"), W(comma(a * b * a), "multiplied instead of dividing"), W(str(b + 1), "made a division mistake"), W(str(b - 1), "made a division mistake")], EX(f"{a * b} ÷ {a}"), qtype="procedural")


@fam("012", mode="mc")
def eq_estimate(r, L):
    a = r.randint(3, 9)
    b = r.randint(102, 398) if L else r.randint(21, 89)
    need(b % 10 not in (0, 5))
    c = r.randint(103, 897) if L else r.randint(21, 89)
    e = len(str(b)) - 1
    rb, rc = rnd_to(b, e), rnd_to(c, len(str(c)) - 1)
    est = a * rb + rc
    exact = a * b + c
    opts = [est, est * 10, a + rb + rc, max(10, est // 2 // 10 ** e * 10 ** e)]
    need(len(set(opts)) == 4 and min(opts, key=lambda x: abs(x - exact)) == est)
    thing = pick(r, ["stickers", "cards", "beads", "seeds"])
    return Item(f"{name(r)} has {a} boxes with {b} {thing} in each box and {c} loose {thing}. Which is the best estimate of the total number of {thing}?", comma(est),
                [f"Round: {b} is about {rb} and {c} is about {rc}.", f"{a} × {rb} + {rc} = {comma(est)}."],
                [W(comma(opts[1]), "wrote an extra zero"), W(comma(opts[2]), "added instead of multiplying"), W(comma(opts[3]), "estimated too low")],
                FN("best_estimate", e=f"{a} × {b} + {c}", options=[str(x) for x in opts]), qtype="conceptual", tags={"reasoning"})


@fam("012", mode="mc")
def eq_reasonable(r, L):
    a = r.randint(3, 9)
    b = r.randint(102, 898)
    need(b % 100 not in range(40, 61))
    rb = rnd_to(b, 2)
    exact, est = a * b, a * rb
    wrong = pick(r, [exact * 10, exact + 2000, exact // 10])
    need(abs(wrong - exact) > 100 * a)
    nm = name(r)
    good = f"No. An estimate is {a} × {comma(rb)} = {comma(est)}, which is not close to {comma(wrong)}."
    return Item(f"A school orders {a} cases of paper. Each case has {b} sheets. {nm} says the school ordered {comma(wrong)} sheets. Use estimation to decide: is this answer reasonable?", good,
                [f"Round {b} to {comma(rb)}: {a} × {comma(rb)} = {comma(est)}.", f"{comma(wrong)} is not close to {comma(est)}, so the answer is not reasonable."],
                [W(f"Yes. An estimate is {a} × {comma(rb)} = {comma(est)}, which is close to {comma(wrong)}.", "did not compare the estimate with the answer"),
                 W("Yes. Any answer greater than the number of sheets in one case is reasonable.", "used a rule that does not check the size of the answer"), W("No. The number of sheets must be an odd number.", "used a rule that is not true")],
                FN("est_judge", a=str(a), b=str(b), op="×", place="hundreds", claimed=str(wrong), keep_a=True), qtype="explain", tags={"reasoning"})


@fam("012", mode="mc")
def eq_first_step(r, L):
    a, b = r.randint(3, 9), r.randint(12, 48)
    c = r.randint(20, 90)
    nm = name(r)
    kind = r.randrange(2)
    if kind == 0:
        need(c < a * b)
        story = f"{nm} buys {a} packs of {b} balloons and uses {c} balloons for a party. How many balloons are left?"
        good, bad = f"Multiply {a} × {b} to find the total number of balloons.", [f"Subtract {b} − {c}.", f"Add {a} + {b} + {c}.", f"Divide {c} ÷ {a}."]
    else:
        tot = a * b + c
        story = f"{nm} has {tot} photos. {nm} puts {c} photos on a poster and places the rest equally on {a} album pages. How many photos are on each page?"
        good, bad = f"Subtract {tot} − {c} to find how many photos belong in the album.", [f"Divide {tot} ÷ {a}.", f"Multiply {a} × {c}.", f"Add {tot} + {c}."]
    return mc_key(story + " What is the first step?", good, bad, ["Think about what must be known before the last step can be done.", good], qtype="explain", tags={"reasoning"}, r=r)


@fam("012")
def eq_letter_story(r, L):
    a = r.randint(3, 9)
    b = r.randint(8, 15) if L == 0 else r.randint(16, 60)
    c = r.randint(5, 40)
    t = a * b + c
    nm = name(r)
    return Item(f"{nm} scored {t} points in a game. {nm} earned {b} points in each of {a} rounds and p bonus points. The equation {a} × {b} + p = {t} matches the story. How many bonus points did {nm} earn?", f"{c} points",
                [f"{a} × {b} = {a * b} points from the rounds.", f"p = {t} − {a * b} = {c} points."],
                [W(f"{t - b} points", "subtracted the points for only one round"), W(f"{a * b} points", "gave the points from the rounds"), W(f"{t + a * b} points", "added instead of subtracting"), W(f"{c + 10} points", "made a subtraction mistake")],
                EX(f"{t} − {a} × {b}", unit="points"), qtype="word-problem", tags={"modeling"})


@fam("12", mode="mc")
def eq_extra_info(r, L):
    a, b, c, d = r.randint(3, 8), r.randint(12, 30), r.randint(5, 12), r.randint(2, 9)
    nm = name(r)
    kind = r.randrange(2)
    if kind == 0:
        story = f"{nm} is {c} years old. {nm} buys {a} packs of stickers. Each pack has {b} stickers and costs ${d}. How many stickers does {nm} buy?"
        good, bad = f"{nm} is {c} years old.", [f"{nm} buys {a} packs.", f"Each pack has {b} stickers.", "All of the information is needed."]
        why = f"Only the number of packs and the stickers in each pack are needed: {a} × {b} = {a * b}. (The cost is not needed either.)"
    else:
        story = f"A bus has {b} seats. It makes {a} trips each day and uses {c} gallons of fuel. Every seat is full on every trip. How many riders does the bus carry each day?"
        good, bad = f"The bus uses {c} gallons of fuel.", [f"The bus has {b} seats.", f"The bus makes {a} trips each day.", "All of the information is needed."]
        why = f"Only the seats and the trips are needed: {a} × {b} = {a * b} riders."
    return mc_key(story + " Which piece of information is NOT needed to solve the problem?", good, bad, ["Decide which numbers the question depends on.", why], qtype="explain", tags={"reasoning"}, r=r)


def small_data(r, L):
    den = pick(r, [2, 4] if L == 0 else [2, 4, 8])
    lo = r.randint(0, 4)
    ticks = [lo + F(i, den) for i in range(2 * den + 1)]
    vals = [pick(r, ticks) for _ in range(r.randint(4, 6))]
    need(len(set(vals)) >= 3)
    return vals


def lab_(v):
    w, rem = divmod(v.numerator, v.denominator)
    return str(w) if rem == 0 else (f"{w} {rem}/{v.denominator}" if w else f"{rem}/{v.denominator}")


@fam("012")
def lp_list_count(r, L):
    vals = small_data(r, L)
    x = pick(r, sorted(set(vals)))
    c = vals.count(x)
    lst = [lab_(v) for v in vals]
    return Item(f"Data: {', '.join(lst)}. How many X marks belong above {lab_(x)} on a line plot?", str(c), [f"Count how many times {lab_(x)} is in the list.", f"It appears {c} time{'s' if c != 1 else ''}."],
                [W(str(c + 1), "counted a different value"), W(str(len(vals)), "counted every value"), W(str(len(set(vals))), "counted the different values") if len(set(vals)) not in (c, c + 1, len(vals)) else W(str(c + 2), "miscounted"), W("0", "did not find the value")],
                FN("lp", values=lst, op="count_at", x=lab_(x)), qtype="conceptual")


@fam("012")
def ls_list_range(r, L):
    vals = small_data(r, L)
    hi, lo = max(vals), min(vals)
    lst = [lab_(v) for v in vals]
    d = hi - lo
    return Item(f"Data, in inches: {', '.join(lst)}. What is the greatest value minus the least value?", fw(d, "inches"), [f"The greatest is {lab_(hi)} and the least is {lab_(lo)}.", f"{lab_(hi)} − {lab_(lo)} = {mixed(d)}."],
                [W(fw(hi + lo, "inches"), "added instead of subtracting"), W(fw(hi, "inches"), "gave the greatest value"), W(fw(d + F(1, 2), "inches"), "made a subtraction mistake"), W(fw(d + 1, "inches"), "made a subtraction mistake")],
                FN("lp", values=lst, op="diff", unit="inches"), qtype="procedural")


@fam("012")
def ls_list_sum(r, L):
    vals = small_data(r, L)[:3]
    need(len(vals) == 3)
    lst = [lab_(v) for v in vals]
    tot = sum(vals)
    return Item(f"Three ribbons are {', '.join(lst[:2])} and {lst[2]} feet long. What is their total length?", fw(tot, "feet"), ["Add the wholes, then add the fractions that have the same denominator.", f"The total is {mixed(tot)} feet."],
                [W(fw(tot + 1, "feet"), "added an extra whole"), W(fw(vals[0] + vals[1], "feet"), "left out one ribbon"), W(fw(tot + F(1, 2), "feet"), "made an addition mistake"), W(fw(max(vals), "feet"), "gave the longest ribbon")],
                FN("lp", values=lst, op="total", unit="feet"), qtype="procedural")


@fam("012")
def eq_short(r, L):
    a, b, c = r.randint(3, 9), r.randint(4, 12) if L < 2 else r.randint(12, 25), r.randint(2, 30)
    kind = r.randrange(3)
    need(a * b > c + 1)
    if kind == 0:
        return Item(f"Find the value: {a} × {b} − {c}", str(a * b - c), [f"Multiply first: {a} × {b} = {a * b}.", f"Then subtract: {a * b} − {c} = {a * b - c}."],
                    [W(str(a * (b - c)) if b > c else str(a * b), "subtracted before multiplying" if b > c else "forgot to subtract"), W(str(a * b + c), "added instead of subtracting"), W(str(a + b - c) if a + b > c else str(a * b - c + 1), "added instead of multiplying"), W(str(a * b - c + 10), "made a computation mistake")],
                    EX(f"{a} × {b} − {c}"), claim=f"{a} × {b} − {c}")
    if kind == 1:
        return Item(f"Find the value: ({a * b} + {a * c}) ÷ {a}", str(b + c), [f"Add inside the parentheses first: {a * b} + {a * c} = {a * b + a * c}.", f"Then divide: {a * b + a * c} ÷ {a} = {b + c}."],
                    [W(str(a * b + c), "divided only the second number"), W(str(b + a * c), "divided only the first number"), W(str(b + c + 1), "made a division mistake"), W(str(a * b + a * c), "forgot to divide")],
                    EX(f"({a * b} + {a * c}) ÷ {a}"), claim=f"({a * b} + {a * c}) ÷ {a}")
    return Item(f"Find the value: {c} + {a} × {b}", str(c + a * b), [f"Multiply first: {a} × {b} = {a * b}.", f"Then add: {c} + {a * b} = {c + a * b}."],
                [W(str((c + a) * b), "added before multiplying"), W(str(a * b), "forgot to add"), W(str(c + a + b), "added instead of multiplying"), W(str(c + a * b + 10), "made a computation mistake")],
                EX(f"{c} + {a} × {b}"), claim=f"{c} + {a} × {b}")


@fam("012")
def ms_short(r, L):
    """Short two-step stories (no diagram, one line) so puzzles and card activities have enough word problems."""
    a = r.randint(3, 9)
    b = r.randint(4, 12) if L == 0 else r.randint(12, 30) if L == 1 else r.randint(25, 60)
    c = r.randint(3, 20) if L < 2 else r.randint(15, 60)
    nm = name(r)
    kind = r.randrange(4 if L else 3)
    if kind == 0:
        thing = pick(r, ["marbles", "stickers", "beads", "shells"])
        v = a * b + c
        return Item(f"{nm} has {a} bags of {b} {thing} and {c} loose {thing}. How many {thing} is that in all?", f"{comma(v)} {thing}",
                    [f"Bags: {a} × {b} = {comma(a * b)}.", f"Add the loose ones: {comma(a * b)} + {c} = {comma(v)} {thing}."],
                    [W(f"{comma(a * b)} {thing}", "stopped after the first step"), W(f"{comma(a * (b + c))} {thing}", "added before multiplying"), W(f"{a + b + c} {thing}", "added all the numbers"), W(f"{comma(v + a)} {thing}", "made a multiplication mistake")],
                    EX(f"{a} × {b} + {c}", unit=thing), qtype="multi-step", tags={"multistep"})
    if kind == 1:
        thing = pick(r, ["pens", "muffins", "tickets", "apples"])
        need(a * b > c + 5)
        v = a * b - c
        return Item(f"A shop has {a} boxes of {b} {thing}. It sells {c} {thing}. How many {thing} are left?", f"{comma(v)} {thing}",
                    [f"Start: {a} × {b} = {comma(a * b)}.", f"Subtract the ones sold: {comma(a * b)} − {c} = {comma(v)} {thing}."],
                    [W(f"{comma(a * b)} {thing}", "stopped after the first step"), W(f"{comma(a * b + c)} {thing}", "added instead of subtracting"), W(f"{comma(a * abs(b - c))} {thing}" if b != c else f"{comma(v + 1)} {thing}", "subtracted before multiplying"), W(f"{comma(v + a)} {thing}", "made a multiplication mistake")],
                    EX(f"{a} × {b} − {c}", unit=thing), qtype="multi-step", tags={"multistep"})
    if kind == 2:
        k = r.randint(3, 9)
        q = r.randint(4, 12) if L == 0 else r.randint(11, 40)
        t = k * q + c
        return Item(f"{nm} has {comma(t)} cards, keeps {c}, and shares the rest equally among {k} friends. How many cards does each friend get?", f"{q} cards",
                    [f"Cards to share: {comma(t)} − {c} = {comma(k * q)}.", f"{comma(k * q)} ÷ {k} = {q} cards."],
                    [W(f"{comma(k * q)} cards", "stopped after the first step"), W(f"{q + c} cards", "added the cards kept"), W(f"{t // k} cards" if t // k != q else f"{q + 2} cards", "divided before subtracting"), W(f"{q + 1} cards", "made a division mistake")],
                    EX(f"({t} − {c}) ÷ {k}", unit="cards"), qtype="multi-step", tags={"multistep"})
    k = r.randint(2, 6)
    v = (b + c) * k
    return Item(f"A ticket costs ${b} and a snack costs ${c}. What is the total cost of {k} tickets and {k} snacks?", f"${comma(v)}",
                [f"One ticket and one snack: {b} + {c} = {b + c}.", f"{k} × {b + c} = {comma(v)}, so the cost is ${comma(v)}."],
                [W(f"${comma(b * k + c)}", "multiplied only the ticket price"), W(f"${b + c}", "found the cost of one ticket and one snack"), W(f"${comma(b + c * k)}", "multiplied only the snack price"), W(f"${comma(v + k)}", "made a multiplication mistake")],
                EX(f"({b} + {c}) × {k}"), qtype="multi-step", tags={"multistep"})


SKILLS = {
    1: dict(name="Reading and Making Line Plots", fams=[lp_count_at, lp_total_n, lp_mode, lp_count_compare, lp_make, lp_match_data, lp_max, lp_list_count]),
    2: dict(name="Solving Problems with Line Plots", fams=[ls_range, ls_total_at, ls_count_diff, ls_two_extremes, ls_total, ls_max_minus_mode, ls_list_range, ls_list_sum]),
    3: dict(name="Multi-Step Word Problems", fams=[ms_shop, ms_pack, ms_save, ms_vans, ms_compare_total, ms_table, ms_read, ms_short]),
    4: dict(name="Equations and Reasonable Answers", fams=[eq_choose, eq_value, eq_estimate, eq_reasonable, eq_first_step, eq_letter_story, eq_extra_info, eq_short]),
}
