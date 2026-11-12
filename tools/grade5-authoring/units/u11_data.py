"""Unit 11: Data, Line Plots, and Problem Solving (data-line-plots)."""
from g5lib import *
from collections import Counter
import u03_decimals as D3, u05_fraction_add as F5, u06_fraction_mult as F6, u07_measurement as M7

UNIT_ID = "data-line-plots-problem-solving"
CTX = [("Ribbon Lengths", "Length (yards)", "yard", "ribbons", "ribbon"), ("Pencil Lengths", "Length (inches)", "inch", "pencils", "pencil"),
       ("Water in Beakers", "Amount (liters)", "liter", "beakers", "beaker"), ("Bags of Trail Mix", "Weight (pounds)", "pound", "bags", "bag"),
       ("Plant Growth in a Week", "Growth (inches)", "inch", "plants", "plant"), ("Leaf Lengths", "Length (inches)", "inch", "leaves", "leaf")]


def fs(x):
    return mixed(x)


def verb(ctx):
    return {"pound": "weighed", "liter": "held"}.get(ctx[2], "measured")


def dataset(r, L):
    den = pick(r, [2, 4]) if L == 0 else pick(r, [4, 8])
    lo = F(r.randint(0, 2))
    span = 4 if den == 2 else (6 if den == 4 else 8)
    choices = [lo + F(i, den) for i in range(1, span + 1)]
    k = r.randint(4, 6) if L == 0 else r.randint(5, 7)
    vals = r.sample(choices, min(k, len(choices)))
    n = r.randint(7, 10) if L == 0 else r.randint(9, 14)
    data = vals[:]
    while len(data) < n:
        data.append(pick(r, vals))
    cnt = Counter(data)
    need(max(cnt.values()) <= 6)
    hi = max(choices)
    return data, den, lo, hi


def plot(data, den, lo, hi, ctx):
    srt = sorted(data)
    alt = f"Line plot titled {ctx[0]}. The number line runs from {fs(lo)} to {fs(hi)} in steps of 1/{den}. X marks: " + \
          ", ".join(f"{fs(v)} ({c})" for v, c in sorted(Counter(data).items())) + "."
    return Diagram("lineplot", {"values": [fs(v) for v in srt], "lo": fs(lo), "hi": fs(hi), "den": den, "title": ctx[0], "unit": ctx[1]}, alt)


def lp_item(r, L, op, prompt_fn, ans_fn, steps_fn, wrong_fn, unit=None, form=None, x=None, qtype="visual"):
    ctx = pick(r, CTX)
    data, den, lo, hi = dataset(r, L)
    p = prompt_fn(ctx, data)
    a = ans_fn(data)
    ans = f"{a} {unit(ctx, a)}" if unit else a
    chk = FN("lp", values=[fs(v) for v in data], op=op, **({"x": x(data)} if x else {}), **({"unit": unit(ctx, 2)} if unit else {}), **({"form": form} if form else {}))
    return Item(p, ans, steps_fn(ctx, data), wrong_fn(ctx, data, ans), chk, qtype=qtype, diagram=plot(data, den, lo, hi, ctx))


def plural(ctx, a):
    return ctx[2] if a in ("1",) or (isinstance(a, str) and "/" in a and " " not in a) else {"inch": "inches"}.get(ctx[2], ctx[2] + "s")


# ============================================================== S1 Reading Line Plots with Fractions
@fam("012")
def rd_count(r, L):
    ctx = pick(r, CTX)
    data, den, lo, hi = dataset(r, L)
    v = pick(r, list(set(data)))
    c = data.count(v)
    return Item(f"The line plot shows data about {ctx[3]}. How many {ctx[3]} {verb(ctx)} {fs(v)} {ctx[2] if v <= 1 else plural(ctx, '2')}?", str(c),
                ["Each X stands for one measurement.", f"There {'is' if c == 1 else 'are'} {c} X{'s' if c != 1 else ''} above {fs(v)}."],
                [W(str(c + 1), "counted the X's above a neighboring mark"), W(str(len(data)), "counted every X"), W(str(max(1, c - 1)) if c > 1 else "2", "miscounted the X's")],
                FN("lp", values=[fs(x) for x in data], op="count_at", x=fs(v)), qtype="visual", diagram=plot(data, den, lo, hi, ctx))


@fam("012")
def rd_at_least(r, L):
    ctx = pick(r, CTX)
    data, den, lo, hi = dataset(r, L)
    v = pick(r, sorted(set(data))[1:-1] or sorted(set(data)))
    ge = r.random() < 0.5
    c = sum(1 for x in data if (x >= v if ge else x < v))
    return Item(f"How many {ctx[3]} {verb(ctx)} {'at least' if ge else 'less than'} {fs(v)} {ctx[2] if v <= 1 else plural(ctx, '2')}?", str(c),
                [f"Count the X's {'at or to the right of' if ge else 'to the left of'} {fs(v)}.", f"There are {c}."],
                [W(str(sum(1 for x in data if (x > v if ge else x <= v))), "included or left out the X's exactly at the value"), W(str(len(data) - c), "counted the other side"), W(str(data.count(v)), "counted only the X's at the value")],
                FN("lp", values=[fs(x) for x in data], op="count_ge" if ge else "count_lt", x=fs(v)), qtype="visual", diagram=plot(data, den, lo, hi, ctx))


@fam("012")
def rd_mode(r, L):
    ctx = pick(r, CTX)
    data, den, lo, hi = dataset(r, L)
    cnt = Counter(data)
    mx = max(cnt.values())
    modes = [v for v, k in cnt.items() if k == mx]
    need(len(modes) == 1)
    m = modes[0]
    others = [v for v in cnt if v != m]
    return Item(f"Which measurement appears most often in the line plot?", f"{fs(m)} {ctx[2] if m <= 1 else plural(ctx, '2')}",
                ["Find the tallest stack of X's.", f"{fs(m)} has the most X's ({mx})."],
                [W(f"{fs(max(data))} {ctx[2] if max(data) <= 1 else plural(ctx, '2')}", "chose the largest measurement"), W(f"{fs(others[0])} {ctx[2] if others[0] <= 1 else plural(ctx, '2')}", "misread the stacks"),
                 W(f"{mx} {plural(ctx, '2')}", "gave the number of X's instead of the measurement")],
                FN("lp", values=[fs(x) for x in data], op="mode", unit=ctx[2]), qtype="visual", diagram=plot(data, den, lo, hi, ctx))


@fam("012")
def rd_n(r, L):
    ctx = pick(r, CTX)
    data, den, lo, hi = dataset(r, L)
    return Item(f"How many {ctx[3]} are shown in the line plot in all?", str(len(data)), ["Each X is one measurement.", f"Count every X: {len(data)}."],
                [W(str(len(set(data))), "counted the marks that have X's instead of the X's"), W(str(len(data) + 1), "miscounted"), W(str(int((hi - lo) * den)), "counted the tick marks")],
                FN("lp", values=[fs(x) for x in data], op="n"), qtype="visual", diagram=plot(data, den, lo, hi, ctx))


@fam("012")
def rd_diff(r, L):
    ctx = pick(r, CTX)
    data, den, lo, hi = dataset(r, L)
    d = max(data) - min(data)
    u = ctx[2] if d <= 1 else plural(ctx, "2")
    return Item(f"What is the difference between the greatest and the least measurement in the line plot?", f"{fs(d)} {u}",
                [f"Greatest: {fs(max(data))}. Least: {fs(min(data))}.", f"{fs(max(data))} − {fs(min(data))} = {fs(d)} {u}."],
                [W(f"{fs(max(data) + min(data))} {plural(ctx, '2')}", "added instead of subtracting"), W(f"{fs(max(data))} {ctx[2] if max(data) <= 1 else plural(ctx, '2')}", "gave the greatest value"),
                 W(f"{len(set(data)) - 1} {plural(ctx, '2')}", "counted the steps between the values")],
                FN("lp", values=[fs(x) for x in data], op="diff", unit=ctx[2], form="mixed"), qtype="visual", diagram=plot(data, den, lo, hi, ctx))


@fam("012", mode="mc")
def rd_meaning(r, L):
    ctx = pick(r, CTX)
    good = f"one {ctx[4]} that was measured"
    bad = [f"the total of all the {ctx[3]}", f"1/2 {ctx[2]}", f"the number of tick marks"]
    data, den, lo, hi = dataset(r, L)
    return mc_key("In this line plot, what does each X stand for?", good, bad, ["A line plot shows one X for each piece of data.", f"Each X is {good}."], r=r, qtype="conceptual",
                  diagram=plot(data, den, lo, hi, ctx))


# ============================================================== S2 Making Line Plots
def data_text(data):
    return ", ".join(fs(v) for v in data)


@fam("012")
def mk_xs(r, L):
    ctx = pick(r, CTX)
    data, den, lo, hi = dataset(r, L)
    r.shuffle(data)
    v = pick(r, list(set(data)))
    return Item(f"{name(r)} measured some {ctx[3]} (in {plural(ctx, '2')}): {data_text(data)}. When making a line plot, how many X's go above {fs(v)}?", str(data.count(v)),
                [f"Count how many times {fs(v)} appears in the list.", f"It appears {data.count(v)} time{'s' if data.count(v) != 1 else ''}."],
                [W(str(data.count(v) + 1), "counted a value twice"), W(str(len(data)), "counted every value"), W("1", "made one X for each different value")],
                FN("lp", values=[fs(x) for x in data], op="count_at", x=fs(v)), qtype="procedural")


@fam("012", mode="mc")
def mk_which(r, L):
    ctx = pick(r, CTX)
    data, den, lo, hi = dataset(r, L)
    good = data_text(sorted(data))
    alt1 = sorted(data[:-1] + [data[-1] + F(1, den)]) if data[-1] + F(1, den) <= hi else sorted(data[:-1] + [data[-1] - F(1, den)])
    alt2 = sorted(data + [data[0]])
    alt3 = sorted(set(data))
    bad = [data_text(x) for x in (alt1, alt2, alt3)]
    need(len(set(bad + [good])) == 4)
    opts = [(good, True)] + [(b, False) for b in bad]
    r.shuffle(opts)
    return Item("Which data set matches the line plot?", good, ["Read every X, including stacked ones.", f"The data are {good}."],
                check=FN("lp_data", values=[fs(v) for v in data]), options=opts, mode="mc", qtype="visual", diagram=plot(data, den, lo, hi, ctx))


@fam("012", mode="mc")
def mk_scale(r, L):
    den = pick(r, [2, 4, 8])
    data = sorted({F(r.randint(1, den * 2), den) for _ in range(8)})
    need(any(v.denominator == den for v in data))
    good = f"every 1/{den}"
    bad = [f"every 1/{x}" for x in [2, 4, 8, 3] if x != den][:2] + ["every 1 whole"]
    return mc_key(f"{name(r)} wants to make a line plot of these measurements: {data_text(data)}. What should the spacing between tick marks be so every value has its own mark?", good, bad,
                  [f"The smallest part used is 1/{den}.", f"Mark the number line {good}."], r=r, qtype="conceptual")


@fam("012")
def mk_order(r, L):
    data, den, lo, hi = dataset(r, L)
    vals = list(dict.fromkeys(data))[:5]
    need(len(vals) >= 4)
    shown = vals[:]
    r.shuffle(shown)
    ans = ", ".join(fs(v) for v in sorted(vals))
    return Item(f"To place the data on a number line, order them from least to greatest: {', '.join(fs(v) for v in shown)}", ans,
                ["Compare using a common denominator.", ans],
                [W(", ".join(fs(v) for v in sorted(vals, reverse=True)), "ordered from greatest to least"), W(", ".join(fs(v) for v in sorted(vals, key=lambda x: (x.denominator, x))), "sorted by denominator"),
                 W(", ".join(fs(v) for v in shown), "did not reorder")],
                FN("order", values=[fs(v).replace(" ", "+") for v in vals]), qtype="procedural")


@fam("012")
def mk_ends(r, L):
    data, den, lo, hi = dataset(r, L)
    r.shuffle(data)
    a, b = min(data), max(data)
    return Item(f"These lengths will be shown on a line plot: {data_text(data)}. What is the greatest value that needs a mark?", fs(b),
                ["Find the largest number in the list.", f"The greatest value is {fs(b)}."],
                [W(fs(a), "chose the least value"), W(fs(b - F(1, den)), "chose the second greatest value"), W(str(len(data)), "counted the values")],
                FN("lp", values=[fs(v) for v in data], op="max"), qtype="procedural")


def short_data(r, L):
    """5 or 6 values, short enough to list in a one-line prompt (Tarsia and small printable boxes)."""
    den = pick(r, [2, 4]) if L == 0 else pick(r, [4, 8])
    lo = F(r.randint(0, 1 if L == 0 else 2))
    choices = [lo + F(i, den) for i in range(1, (4 if den == 2 else 6) + 1)]
    vals = r.sample(choices, r.randint(3, 4))
    data = vals[:] + [pick(r, vals) for _ in range(r.randint(2, 3))]
    r.shuffle(data)
    return data, den


@fam("012")
def mk_xs_short(r, L):
    data, den = short_data(r, L)
    v = pick(r, list(set(data)))
    c = data.count(v)
    return Item(f"Data: {data_text(data)}. On a line plot, how many X's go above {fs(v)}?", str(c),
                [f"Count how many times {fs(v)} appears.", f"It appears {c} time{'s' if c != 1 else ''}."],
                [W(str(c + 1), "counted a value twice"), W(str(len(data)), "counted every value"), W(str(len(set(data))), "counted the different values")],
                FN("lp", values=[fs(x) for x in data], op="count_at", x=fs(v)), qtype="procedural")


@fam("012")
def mk_mode_short(r, L):
    data, den = short_data(r, L)
    cnt = Counter(data)
    top = max(cnt.values())
    need(sum(1 for k in cnt.values() if k == top) == 1)
    m = [v for v, k in cnt.items() if k == top][0]
    return Item(f"Data: {data_text(data)}. Which value will have the tallest stack of X's?", fs(m),
                ["Count how many times each value appears.", f"{fs(m)} appears {top} times, more than any other value."],
                [W(fs(max(data)), "chose the greatest value"), W(fs(min(data)), "chose the least value"), W(str(top), "gave the number of X's instead of the value")],
                FN("lp", values=[fs(x) for x in data], op="mode"), qtype="procedural")


@fam("012")
def ps_range_short(r, L):
    data, den = short_data(r, L)
    a, b = min(data), max(data)
    return Item(f"Data: {data_text(data)}. What is the greatest value minus the least value?", fs(b - a),
                [f"Greatest: {fs(b)}. Least: {fs(a)}.", f"{fs(b)} − {fs(a)} = {fs(b - a)}."],
                [W(fs(b + a), "added instead of subtracting"), W(fs(b), "gave the greatest value"), W(str(len(data)), "counted the values")],
                FN("lp", values=[fs(x) for x in data], op="diff"), qtype="procedural")


@fam("012")
def ps_total_short(r, L):
    data, den = short_data(r, L)
    t = sum(data)
    return Item(f"Data: {data_text(data)}. What is the total of all the values?", fs(t),
                ["Add every value, including repeated ones.", f"The total is {fs(t)}."],
                [W(fs(sum(set(data))), "added each different value only once"), W(fs(t - min(data)), "left out one value"), W(str(len(data)), "counted the values")],
                FN("lp", values=[fs(x) for x in data], op="total", form="mixed"), qtype="multi-step", tags={"multistep"})


# ============================================================== S3 Solving Problems with Line Plot Data
@fam("012")
def ps_total(r, L):
    ctx = pick(r, CTX[:4])
    data, den, lo, hi = dataset(r, L)
    t = sum(data)
    u = plural(ctx, "2")
    return Item(f"What is the total of all the measurements in the line plot?", f"{fs(t)} {u}",
                ["Multiply each value by its number of X's, then add.", f"Total: {fs(t)} {u}."],
                [W(f"{fs(sum(set(data)))} {u}", "added each value only once"), W(f"{len(data)} {u}", "counted the X's"), W(f"{fs(t - min(data))} {u}", "left out one X")],
                FN("lp", values=[fs(v) for v in data], op="total", unit=ctx[2], form="mixed"), qtype="multi-step", tags={"multistep"}, diagram=plot(data, den, lo, hi, ctx))


@fam("012")
def ps_fair(r, L):
    ctx = CTX[2]
    data, den, lo, hi = dataset(r, L)
    t = sum(data)
    each = t / len(data)
    need(each.denominator in (1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 24) and len(data) <= 12)
    u = "liter" if each <= 1 else "liters"
    return Item(f"The line plot shows the amount of water in {len(data)} identical beakers. If all the water were poured together and shared equally among the beakers, how much would each beaker hold?",
                f"{fs(each)} {u}", [f"Total water: {fs(t)} liters.", f"Share equally: {fs(t)} ÷ {len(data)} = {fs(each)} {u}."],
                [W(f"{fs(t)} liters", "found the total but did not share it"), W(f"{fs(Counter(data).most_common(1)[0][0])} liters", "used the most common amount"), W(f"{fs((max(data) + min(data)) / 2)} liters", "used the middle of the greatest and least")],
                FN("lp", values=[fs(v) for v in data], op="fair", unit="liters", form="mixed"), qtype="multi-step", tags={"multistep", "modeling", "challenge"}, diagram=plot(data, den, lo, hi, ctx))


@fam("012")
def ps_total_at(r, L):
    ctx = pick(r, CTX[:4])
    data, den, lo, hi = dataset(r, L)
    v = pick(r, [x for x in set(data) if data.count(x) >= 2] or list(set(data)))
    c = data.count(v)
    t = v * c
    u = ctx[2] if t <= 1 and t.denominator > 1 else plural(ctx, "2")
    return Item(f"What is the combined measurement of all the {ctx[3]} that {verb(ctx)} {fs(v)} {ctx[2] if v <= 1 else plural(ctx, '2')}?", f"{fs(t)} {u}",
                [f"There are {c} X's at {fs(v)}.", f"{c} × {fs(v)} = {fs(t)} {u}."],
                [W(f"{fs(v)} {ctx[2] if v <= 1 else plural(ctx, '2')}", "used only one X"), W(f"{c} {plural(ctx, '2')}", "gave the number of X's"), W(f"{fs(v + c)} {plural(ctx, '2')}", "added instead of multiplying")],
                FN("lp", values=[fs(x) for x in data], op="total_at", x=fs(v), unit=ctx[2], form="mixed"), qtype="visual", diagram=plot(data, den, lo, hi, ctx))


@fam("012")
def ps_count_diff(r, L):
    ctx = pick(r, CTX)
    data, den, lo, hi = dataset(r, L)
    a, b = r.sample(sorted(set(data)), 2)
    ca, cb = data.count(a), data.count(b)
    need(ca != cb)
    if ca < cb:
        a, b, ca, cb = b, a, cb, ca
    return Item(f"How many more {ctx[3]} {verb(ctx)} {fs(a)} than {verb(ctx)} {fs(b)}?", str(ca - cb),
                [f"{fs(a)}: {ca} X's. {fs(b)}: {cb} X's.", f"{ca} − {cb} = {ca - cb}."],
                [W(str(ca + cb), "added the counts"), W(fs(a - b) if a > b else fs(b - a), "subtracted the measurements instead of the counts"), W(str(ca), "gave one count")],
                FN("lp", values=[fs(x) for x in data], op="count_diff", x=fs(a), y=fs(b)), qtype="visual", diagram=plot(data, den, lo, hi, ctx))


@fam("12")
def ps_max_mode(r, L):
    ctx = pick(r, CTX)
    data, den, lo, hi = dataset(r, L)
    cnt = Counter(data)
    mx = max(cnt.values())
    modes = [v for v, k in cnt.items() if k == mx]
    need(len(modes) == 1 and max(data) != modes[0])
    d = max(data) - modes[0]
    u = ctx[2] if d <= 1 else plural(ctx, "2")
    return Item(f"How much greater is the greatest measurement than the most common measurement?", f"{fs(d)} {u}",
                [f"Greatest: {fs(max(data))}. Most common: {fs(modes[0])}.", f"{fs(max(data))} − {fs(modes[0])} = {fs(d)} {u}."],
                [W(f"{fs(max(data) - min(data))} {u}", "used the least value instead of the most common"), W(f"{fs(max(data))} {u}", "gave the greatest value"), W(f"{mx} {plural(ctx, '2')}", "used the number of X's")],
                FN("lp", values=[fs(x) for x in data], op="max_minus_mode", unit=ctx[2], form="mixed"), qtype="multi-step", tags={"multistep"}, diagram=plot(data, den, lo, hi, ctx))


# ============================================================== S4 Multi-Step Problem Solving
@fam("012")
def mx_fundraiser(r, L):
    n = r.randint(12, 40)
    price = D3.rdec(r, 1.25, 4.75, 2)
    cost = D3.rdec(r, 8, 30, 2)
    v = n * price - cost
    need(v > 0)
    return Item(f"A class sells {n} muffins for {money(price)} each. They spent {money(cost)} on ingredients. How much money did they make after paying for ingredients?", money(v),
                [f"Sales: {n} × {money(price)} = {money(n * price)}.", f"Profit: {money(n * price)} − {money(cost)} = {money(v)}."],
                [W(money(n * price), "forgot to subtract the ingredients"), W(money(n * price + cost), "added the cost"), W(money(price - cost / n) if ((price - cost / n) * 100).denominator == 1 and price > cost / n else money(v + 1), "mixed up the steps")],
                EX(f"{n}*{dec(price)}-{dec(cost)}", form="money"), qtype="multi-step", tags={"multistep", "modeling"})


@fam("012")
def mx_garden(r, L):
    l = r.randint(4, 12)
    w = r.randint(3, 10)
    frac_ = pick(r, [F(1, 2), F(1, 4), F(3, 4), F(2, 3), F(1, 3)])
    area = l * w
    v = frac_ * area
    need(v.denominator <= 4)
    return Item(f"A garden is {l} feet by {w} feet. {frac_} of the garden is planted with carrots. How many square feet are planted with carrots?", f"{fs(v)} square feet",
                [f"Area: {l} × {w} = {area} square feet.", f"{frac_} × {area} = {fs(v)} square feet."],
                [W(f"{area} square feet", "found the whole area only"), W(f"{fs(frac_ * 2 * (l + w))} square feet", "used the perimeter"), W(f"{fs(area - v)} square feet", "found the part without carrots")],
                EX(f"{frac_}*{l}*{w}", unit="square feet", form="mixed"), qtype="multi-step", tags={"multistep"})


@fam("012")
def mx_trip(r, L):
    d1 = D3.rdec(r, 2.5, 15, 1)
    d2 = D3.rdec(r, 2.5, 15, 1)
    days = r.randint(2, 5)
    tot = (d1 + d2) * days
    return Item(f"Each day for {days} days, {name(r)} bikes {dec(d1)} miles to the library and then {dec(d2)} miles to the park. How many miles is that in all?", f"{dec(tot)} miles",
                [f"One day: {dec(d1)} + {dec(d2)} = {dec(d1 + d2)} miles.", f"{days} days: {days} × {dec(d1 + d2)} = {dec(tot)} miles."],
                [W(f"{dec(d1 + d2)} miles", "found one day only"), W(f"{dec(d1 * days + d2)} miles", "multiplied only the first part"), W(f"{dec(d1 + d2 + days)} miles", "added the number of days")],
                EX(f"({dec(d1)}+{dec(d2)})*{days}", unit="miles"), qtype="multi-step", tags={"multistep"})


@fam("012", mode="mc")
def mx_first_step(r, L):
    n, p, k = r.randint(3, 9), D3.rdec(r, 1.5, 6.5, 2), r.randint(2, 5)
    nm = name(r)
    q = f"{nm} buys {n} notebooks for {money(p)} each and pays with a $50 bill. How much change does {nm} get?"
    good = f"Multiply {n} × {money(p)} to find the total cost."
    bad = [f"Subtract {money(p)} from $50.", f"Divide $50 by {n}.", f"Add {n} and {money(p)}."]
    return mc_key(f"{q} What is the best first step?", good, bad, ["You need the total cost before you can find the change.", good], r=r, qtype="explain", tags={"reasoning"})


@fam("012")
def mx_recipe(r, L):
    cups = pick(r, [F(1, 2), F(3, 4), F(2, 3), F(1, 3), F(1, 4)]) + (r.randint(0, 1) if L else 0)
    batches = r.randint(2, 6)
    tot = cups * batches
    return Item(f"One batch of granola uses {fs(cups)} cup{'s' if cups > 1 else ''} of oats. How many cups of oats are needed for {batches} batches?", f"{fs(tot)} cups",
                [f"Multiply: {batches} × {fs(cups)}.", f"= {fs(tot)} cups."],
                [W(f"{fs(cups + batches)} cups", "added instead of multiplying"), W(f"{fs(cups)} cups", "found one batch"), W(f"{fs(batches / cups)} cups", "divided instead of multiplying")],
                EX(f"{batches}*{F6.ex(cups)}", unit="cups", form="mixed"), qtype="multi-step", tags={"modeling"})


mx_change = D3.w_change
mx_pieces = M7.ms_pieces
mx_fraction_left = F5.w_left

SKILLS = {
    1: dict(name="Reading Line Plots with Fractions", fams=[rd_count, rd_at_least, rd_mode, rd_n, rd_diff, rd_meaning]),
    2: dict(name="Making Line Plots", fams=[mk_xs, mk_which, mk_scale, mk_order, mk_ends, mk_xs_short, mk_mode_short]),
    3: dict(name="Solving Problems with Line Plot Data", fams=[ps_total, ps_fair, ps_total_at, ps_count_diff, ps_max_mode, ps_range_short, ps_total_short]),
    4: dict(name="Multi-Step Problem Solving", fams=[mx_fundraiser, mx_garden, mx_trip, mx_first_step, mx_recipe, mx_change, mx_pieces, mx_fraction_left]),
}
