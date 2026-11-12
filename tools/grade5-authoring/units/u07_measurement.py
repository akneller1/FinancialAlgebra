"""Unit 7: Measurement and Conversions (measurement-conversions)."""
from g5lib import *

UNIT_ID = "measurement-conversions"

# generator-side factors (the verifier keeps its own table)
LEN = [("inches", "feet", 12), ("feet", "yards", 3), ("inches", "yards", 36), ("feet", "miles", 5280)]
WT = [("ounces", "pounds", 16), ("pounds", "tons", 2000)]
CAP = [("cups", "pints", 2), ("pints", "quarts", 2), ("quarts", "gallons", 4), ("cups", "quarts", 4), ("cups", "gallons", 16), ("fluid ounces", "cups", 8)]
MET = [("millimeters", "centimeters", 10), ("centimeters", "meters", 100), ("millimeters", "meters", 1000), ("meters", "kilometers", 1000),
       ("grams", "kilograms", 1000), ("milligrams", "grams", 1000), ("milliliters", "liters", 1000)]


def qty(x, unit):
    s = mixed(x) if F(x).denominator in (2, 3, 4, 8) else dec(x)
    return f"{s} {unit}"


def conv_item(r, L, table, metric=False):
    small, big, k = pick(r, table if L else table[:2])
    if metric and L == 0:
        need(k <= 1000)
    up = r.random() < 0.5    # big -> small
    if metric:
        if up:
            x = F(r.randint(2, 30)) if L == 0 else F(r.randint(11, 999), pick(r, [10, 100]))
            v = x * k
        else:
            v = F(r.randint(2, 30)) if L == 0 else F(r.randint(11, 999), pick(r, [10, 100]))
            x = v * k
            v, x = x / k / k * k, x   # placeholder (overwritten below)
            x = F(r.randint(1, 9999)) if L else F(r.randint(1, 30)) * k
            v = x / k
        need(is_term(v) and is_term(x) and len(dec(v).split(".")[-1]) <= 3)
    else:
        if up:
            x = F(r.randint(2, 12)) if L < 2 else r.randint(1, 9) + pick(r, [F(1, 2), F(1, 4), F(3, 4)])
            v = x * k
            need(v.denominator == 1)
        else:
            if L < 2:
                v = F(r.randint(2, 12))
                x = v * k
            else:
                x = F(r.randint(k + 1, k * 9))
                v = x / k
                need(v.denominator in (1, 2, 4, 8))
        if k >= 2000 and not up:
            need(v.denominator == 1)
    frm, to = (big, small) if up else (small, big)
    return x, frm, v, to, k, up


def conv_wrongs(x, frm, v, to, k, up):
    return [W(qty(x / k if up else x * k, to), "multiplied when it should divide" if not up else "divided when it should multiply"),
            W(qty(x + k if up else x - k if x > k else x + k, to), "added or subtracted the conversion number instead of multiplying or dividing"),
            W(qty(v * 10, to), "used the wrong conversion number"), W(qty(x, to), "changed the unit but not the number")]


# ============================================================== S1 Customary Length
@fam("012")
def cl_convert(r, L):
    x, frm, v, to, k, up = conv_item(r, L, LEN)
    return Item(f"Convert: {qty(x, frm)} = ? {to}", qty(v, to),
                [f"1 {frm[:-1] if not frm.endswith('feet') else 'foot'} = {k} {to}" if up else f"{k} {frm} = 1 {to[:-1] if to != 'feet' else 'foot'}",
                 f"{'Multiply' if up else 'Divide'}: {mixed(x) if x.denominator > 1 else comma(x)} {'×' if up else '÷'} {k} = {qty(v, to)}."],
                conv_wrongs(x, frm, v, to, k, up), FN("convert", x=frac(x), frm=frm, to=to), qtype="procedural", claim=f"{qty(x, frm)} in {to}")


@fam("012")
def cl_compound(r, L):
    small, big, k = pick(r, LEN[:2])
    a = r.randint(1, 9)
    b = r.randint(1, k - 1)
    tot = a * k + b
    ans = f"{a} {big} {b} {small}"
    return Item(f"Write {tot} {small} using {big} and {small}. (Example: 5 {big} 2 {small})", ans,
                [f"{tot} ÷ {k} = {a} R {b}.", f"So {tot} {small} = {a} {big} {b} {small}."],
                [W(f"{a} {big} {k - b} {small}", "used the wrong remainder"), W(f"{a + 1} {big} {b} {small}", "miscounted the groups"), W(f"{tot // 10} {big} {tot % 10} {small}", "split the number into tens and ones")],
                FN("compound", big=big, big1=big, small=small, small1=small, total=str(tot)), qtype="procedural")


@fam("012")
def cl_add(r, L):
    small, big, k = pick(r, LEN[:2])
    a1, b1, a2, b2 = r.randint(1, 8), r.randint(1, k - 1), r.randint(1, 6), r.randint(1, k - 1)
    op = "+" if L < 2 or r.random() < 0.5 else "−"
    t1, t2 = a1 * k + b1, a2 * k + b2
    if op == "−" and t1 < t2:
        a1, b1, a2, b2, t1, t2 = a2, b2, a1, b1, t2, t1
    tot = t1 + t2 if op == "+" else t1 - t2
    need(tot > k)
    A, B = divmod(tot, k)
    ans = f"{A} {big} {B} {small}"
    raw = f"{a1 + a2 if op == '+' else a1 - a2} {big} {b1 + b2 if op == '+' else abs(b1 - b2)} {small}"
    need(B != 0)
    return Item(f"{'Add' if op == '+' else 'Subtract'}: {a1} {big} {b1} {small} {op} {a2} {big} {b2} {small}. Write the answer in {big} and {small}.", ans,
                [f"{'Add' if op == '+' else 'Subtract'} the {small} and the {big}, regrouping 1 {big[:-1] if big != 'feet' else 'foot'} = {k} {small} when needed.", f"The answer is {ans}."],
                [W(raw, f"did not regroup {small} into {big}") if raw != ans else W(f"{A + 1} {big} {B} {small}", "regrouped twice"), W(f"{A} {big} {k - B} {small}", "subtracted the inches the wrong way"), W(f"{A + 1} {big} {B} {small}", "added an extra unit when regrouping")],
                FN("compound", big=big, big1=big, small=small, small1=small, total=str(tot)), qtype="multi-step", tags={"multistep"})


@fam("012")
def cl_table(r, L):
    small, big, k = pick(r, LEN[:3])
    rows = sorted(r.sample(range(1, 10), 4))
    j = r.randint(1, 3)
    cells = [[str(x), comma(x * k) if i != j else "?"] for i, x in enumerate(rows)]
    alt = f"Table with columns {big} and {small}: " + "; ".join(f"{a} → {b}" for a, b in cells) + "."
    return Item(f"The table shows {big} and {small}. What number belongs in place of “?”", comma(rows[j] * k),
                [f"Each {big[:-1] if big != 'feet' else 'foot'} is {k} {small}.", f"{rows[j]} × {k} = {comma(rows[j] * k)}."],
                [W(comma(rows[j] + k), "added instead of multiplying"), W(comma(rows[j - 1] * k + k), "added one more group to the row above"), W(comma(rows[j] * k * 10), "used the wrong conversion number")],
                FN("convert", x=str(rows[j]), frm=big, to=small, bare=True), qtype="visual", diagram=Diagram("table", {"header": [big, small], "rows": cells}, alt))


@fam("012", mode="sa")
def cl_compare(r, L):
    small, big, k = pick(r, LEN[:3])
    a = r.randint(2, 9)
    b = a * k + pick(r, [-k + 1, -1, 1, 2, -2])
    need(b > 0 and b != a * k)
    ans = f"{a} {big}" if a * k > b else f"{b} {small}"
    return Item(f"Which is longer: {a} {big} or {b} {small}?", ans, [f"{a} {big} = {a * k} {small}.", f"{max(a * k, b)} {small} is longer, so the answer is {ans}."],
                [W(f"{b} {small}" if ans != f"{b} {small}" else f"{a} {big}", "compared the numbers without converting")],
                FN("extreme", values={f"{a} {big}": f"{a}*{k}", f"{b} {small}": str(b)}, which="max", expr=True), qtype="conceptual", mode="sa")


@fam("012")
def cl_word(r, L):
    t = pick(r, [("A ribbon is {x} yards long. How many feet long is it?", 3, "yards", "feet"), ("A window is {x} feet tall. How many inches tall is it?", 12, "feet", "inches"),
                 ("{n} jumped {y} inches. How many feet is that?", 12, "inches", "feet"), ("A trail is {x} miles long. How many feet long is it?", 5280, "miles", "feet")])
    k = t[1]
    if "{y}" in t[0]:
        v = F(r.randint(2, 9)) if L < 2 else F(r.randint(3, 19), 2)
        x = v * k
        q = t[0].format(y=comma(x), n=name(r))
        need(x.denominator == 1)
    else:
        x = F(r.randint(2, 9)) if L < 2 or k == 5280 else r.randint(1, 8) + F(1, 2)
        v = x * k
        q = t[0].format(x=mixed(x), n=name(r))
    return Item(q, qty(v, t[3]), [f"{'Multiply' if '{y}' not in t[0] else 'Divide'} by {comma(k)}.", f"The answer is {qty(v, t[3])}."],
                [W(qty(x / k if "{y}" not in t[0] else x * k, t[3]), "used the wrong operation"), W(qty(x + k, t[3]), "added the conversion number"), W(qty(x, t[3]), "did not convert")],
                FN("convert", x=frac(x), frm=t[2], to=t[3]), qtype="word-problem", tags={"modeling"})


# ============================================================== S2 Customary Weight and Capacity
@fam("012")
def wc_convert(r, L):
    x, frm, v, to, k, up = conv_item(r, L, pick(r, [WT, CAP]))
    return Item(f"Convert: {qty(x, frm)} = ? {to}", qty(v, to),
                [f"Use the fact: 1 {sing(frm if up else to)} = {comma(k)} {to if up else frm}.", f"{'Multiply' if up else 'Divide'} by {comma(k)}: {qty(v, to)}."],
                conv_wrongs(x, frm, v, to, k, up), FN("convert", x=frac(x), frm=frm, to=to), qtype="procedural", claim=f"{qty(x, frm)} in {to}")


def sing(u):
    return {"feet": "foot", "inches": "inch", "fluid ounces": "fluid ounce"}.get(u, u[:-1])


@fam("012")
def wc_compound(r, L):
    small, big, k = pick(r, [("ounces", "pounds", 16), ("cups", "quarts", 4), ("quarts", "gallons", 4), ("pints", "quarts", 2)])
    a, b = r.randint(1, 9), r.randint(1, k - 1)
    tot = a * k + b
    ans = f"{a} {big} {b} {small}" if b != 1 else f"{a} {big} 1 {small}"
    return Item(f"Write {tot} {small} using {big} and {small}.", ans, [f"{tot} ÷ {k} = {a} R {b}.", f"{tot} {small} = {ans}."],
                [W(f"{a} {big} {k - b} {small}", "used the wrong remainder"), W(f"{tot // 10} {big} {tot % 10} {small}", "split the digits instead of dividing by the conversion number"), W(f"{a + 1} {big} {b} {small}", "miscounted")],
                FN("compound", big=big, big1=big, small=small, small1=sing(small), total=str(tot)), qtype="procedural")


@fam("012", mode="sa")
def wc_compare(r, L):
    small, big, k = pick(r, [("ounces", "pounds", 16), ("cups", "quarts", 4), ("quarts", "gallons", 4), ("pints", "gallons", 8)])
    a = r.randint(2, 9)
    b = a * k + pick(r, [-1, 1, 2, -2, k // 2])
    need(b > 0 and b != a * k)
    word = "heavier" if small == "ounces" else "more"
    ans = f"{a} {big}" if a * k > b else f"{b} {small}"
    return Item(f"Which is {word}: {a} {big} or {b} {small}?", ans, [f"{a} {big} = {a * k} {small}.", f"Compare {a * k} and {b}: {ans} is {word}."],
                [W(f"{b} {small}" if ans != f"{b} {small}" else f"{a} {big}", "compared the numbers without converting")],
                FN("extreme", values={f"{a} {big}": f"{a}*{k}", f"{b} {small}": str(b)}, which="max", expr=True), qtype="conceptual", mode="sa")


@fam("012")
def wc_word(r, L):
    t = pick(r, [("A recipe needs {x} quarts of milk. How many cups is that?", "quarts", "cups", 4), ("A puppy weighs {x} pounds. How many ounces is that?", "pounds", "ounces", 16),
                 ("A fish tank holds {x} gallons. How many quarts is that?", "gallons", "quarts", 4), ("An elephant weighs {x} tons. How many pounds is that?", "tons", "pounds", 2000)])
    x = F(r.randint(2, 12)) if L < 2 or t[3] == 2000 else r.randint(1, 9) + F(1, 2)
    v = x * t[3]
    return Item(t[0].format(x=mixed(x)), qty(v, t[2]), [f"1 {sing(t[1])} = {comma(t[3])} {t[2]}.", f"{mixed(x)} × {comma(t[3])} = {qty(v, t[2])}."],
                [W(qty(x / t[3], t[2]), "divided instead of multiplying"), W(qty(x + t[3], t[2]), "added the conversion number"), W(qty(x * t[3] * 2, t[2]), "used the wrong conversion number")],
                FN("convert", x=frac(x), frm=t[1], to=t[2]), qtype="word-problem", tags={"modeling"})


@fam("12")
def wc_two_step(r, L):
    g = r.randint(2, 6)
    serve = pick(r, [1, 2])
    cups = g * 16
    v = cups // serve
    it = Item(f"A party has {g} gallons of lemonade. Each glass holds {serve} cup{'s' if serve > 1 else ''}. How many glasses can be filled?", f"{v} glasses",
                [f"1 gallon = 16 cups, so {g} gallons = {cups} cups.", f"{cups} ÷ {serve} = {v} glasses."],
                [W(f"{g * 4 // serve} glasses", "converted to quarts instead of cups"), W(f"{g * 8 // serve} glasses", "used 8 cups in a gallon"), W(f"{cups * serve} glasses", "multiplied by the glass size")],
                EX(f"{g}*16/{serve}", unit="glasses"), qtype="multi-step", tags={"multistep"})
    it.consts = [16]
    return it


@fam("012", mode="mc")
def wc_fact(r, L):
    facts = [("How many cups are in 1 quart?", "4 cups", ["2 cups", "8 cups", "16 cups"]), ("How many ounces are in 1 pound?", "16 ounces", ["12 ounces", "10 ounces", "8 ounces"]),
             ("How many quarts are in 1 gallon?", "4 quarts", ["2 quarts", "8 quarts", "16 quarts"]), ("How many pounds are in 1 ton?", "2,000 pounds", ["1,000 pounds", "100 pounds", "16 pounds"]),
             ("How many pints are in 1 quart?", "2 pints", ["4 pints", "8 pints", "16 pints"]), ("How many cups are in 1 gallon?", "16 cups", ["4 cups", "8 cups", "12 cups"])]
    q, good, bad = pick(r, facts)
    return mc_key(q, good, bad, ["Use the customary conversion facts.", good], r=r, qtype="conceptual")


# ============================================================== S3 Metric Conversions
def met_item(r, L):
    small, big, k = pick(r, MET if L else [m for m in MET if m[2] in (10, 100, 1000) and "milligrams" not in m[0]])
    up = r.random() < 0.5
    if up:
        x = F(r.randint(2, 40)) if L == 0 else F(r.randint(11, 999), pick(r, [10, 100]))
        v = x * k
    else:
        v = F(r.randint(2, 40)) if L == 0 else F(r.randint(1, 999), pick(r, [1, 10, 100]))
        x = v * k
    need(x.denominator in (1, 10, 100) and is_term(v) and len(dec(v).split(".")[-1]) <= 3)
    return (x, big, v, small, k, True) if up else (x, small, v, big, k, False)


@fam("012")
def me_convert(r, L):
    x, frm, v, to, k, up = met_item(r, L)
    return Item(f"Convert: {dec(x)} {frm} = ? {to}", f"{dec(v)} {to}",
                [f"1 {sing(frm if up else to)} = {comma(k)} {to if up else frm}.", f"{'Multiply' if up else 'Divide'} by {comma(k)}: {dec(x)} {'×' if up else '÷'} {comma(k)} = {dec(v)}."],
                [W(f"{dec(x / k if up else x * k)} {to}", "multiplied and divided the wrong way"), W(f"{dec(v * 10)} {to}", "moved the decimal point one place too many"), W(f"{dec(v / 10)} {to}", "moved the decimal point one place too few"),
                 W(f"{dec(x)} {to}", "changed the unit but not the number")],
                FN("convert", x=dec(x).replace(",", ""), frm=frm, to=to), qtype="procedural", claim=f"{dec(x)} {frm} in {to}")


@fam("012", mode="mc")
def me_factor(r, L):
    small, big, k = pick(r, MET)
    up = r.random() < 0.5
    good = f"Multiply by {comma(k)}." if up else f"Divide by {comma(k)}."
    bad = [f"Divide by {comma(k)}." if up else f"Multiply by {comma(k)}.", f"Multiply by {comma(k * 10)}." if up else f"Divide by {comma(k * 10)}.", f"Add {comma(k)}." if up else f"Subtract {comma(k)}."]
    frm, to = (big, small) if up else (small, big)
    return mc_key(f"How do you change {frm} to {to}?", good, bad, [f"1 {sing(big)} = {comma(k)} {small}.", f"Going from {frm} to {to}: {good.lower()}"], r=r, qtype="conceptual", tags={"connections"})


@fam("012", mode="sa")
def me_compare(r, L):
    small, big, k = pick(r, [("centimeters", "meters", 100), ("grams", "kilograms", 1000), ("milliliters", "liters", 1000), ("meters", "kilometers", 1000)])
    a = F(r.randint(11, 99), 10)
    b = a * k + pick(r, [-k // 10, k // 10, -k // 20, 5])
    need(b > 0 and b.denominator == 1 and b != a * k)
    ans = f"{dec(a)} {big}" if a * k > b else f"{comma(b)} {small}"
    return Item(f"Which is greater: {dec(a)} {big} or {comma(b)} {small}?", ans, [f"{dec(a)} {big} = {comma(a * k)} {small}.", f"So {ans} is greater."],
                [W(f"{comma(b)} {small}" if ans.endswith(big) else f"{dec(a)} {big}", "compared the numbers without converting")],
                FN("extreme", values={f"{dec(a)} {big}": f"{dec(a)}*{k}", f"{comma(b)} {small}": str(b)}, which="max", expr=True), qtype="conceptual", mode="sa")


@fam("012")
def me_word(r, L):
    t = pick(r, [("A water bottle holds {x} liters. How many milliliters is that?", "liters", "milliliters", 1000, True),
                 ("A pencil is {x} centimeters long. How many millimeters is that?", "centimeters", "millimeters", 10, True),
                 ("{n} walked {x} meters. How many kilometers is that?", "meters", "kilometers", 1000, False),
                 ("A bag of flour has a mass of {x} grams. What is its mass in kilograms?", "grams", "kilograms", 1000, False),
                 ("A snail moved {x} centimeters. How many meters is that?", "centimeters", "meters", 100, False)])
    up, k = t[4], t[3]
    if up:
        x = F(r.randint(2, 9)) if L == 0 else F(r.randint(11, 99), 10)
        v = x * k
    else:
        x = F(r.randint(2, 9) * k) if L == 0 else F(r.randint(1, 9999))
        v = x / k
    need(is_term(v))
    return Item(t[0].format(x=dec(x), n=name(r)), f"{dec(v)} {t[2]}", [f"1 {sing(t[1] if up else t[2])} = {comma(k)} {t[2] if up else t[1]}.", f"{'Multiply' if up else 'Divide'} by {comma(k)}: {dec(v)} {t[2]}."],
                [W(f"{dec(x / k if up else x * k)} {t[2]}", "used the wrong operation"), W(f"{dec(v * 10)} {t[2]}", "moved the decimal point too far"), W(f"{dec(v / 10)} {t[2]}", "did not move the decimal point far enough")],
                FN("convert", x=dec(x).replace(",", ""), frm=t[1], to=t[2]), qtype="word-problem", tags={"modeling"})


@fam("12")
def me_add(r, L):
    a = F(r.randint(11, 99), 10)
    b = r.randint(50, 950)
    pair = pick(r, [("meters", "centimeters", 100), ("liters", "milliliters", 1000), ("kilograms", "grams", 1000)])
    v = a + F(b, pair[2])
    return Item(f"Add {dec(a)} {pair[0]} and {b} {pair[1]}. Write the answer in {pair[0]}.", f"{dec(v)} {pair[0]}",
                [f"{b} {pair[1]} = {dec(F(b, pair[2]))} {pair[0]}.", f"{dec(a)} + {dec(F(b, pair[2]))} = {dec(v)} {pair[0]}."],
                [W(f"{dec(a + b)} {pair[0]}", "added without converting"), W(f"{dec(a + F(b, pair[2] // 10))} {pair[0]}", "used the wrong conversion number"), W(f"{dec(a * pair[2] + b)} {pair[0]}", "converted the wrong number")],
                EX(f"{dec(a)}+{b}/{pair[2]}", unit=pair[0]), qtype="multi-step", tags={"multistep"})


# ============================================================== S4 Multi-Step Measurement Problems
@fam("012")
def ms_pieces(r, L):
    n = r.randint(3, 8)
    each = r.randint(8, 30) if L < 2 else r.randint(14, 40)
    tot = n * each
    need(tot % 12 == 0 or L > 0)
    v = F(tot, 12)
    ans = f"{mixed(v)} feet" if v != 1 else "1 foot"
    return Item(f"{name(r)} cuts {n} pieces of ribbon, each {each} inches long. How many feet of ribbon is that in all?", ans,
                [f"Total inches: {n} × {each} = {tot} inches.", f"{tot} ÷ 12 = {mixed(v)} feet."],
                [W(f"{comma(tot)} feet", "forgot to convert inches to feet"), W(f"{mixed(F(tot, 3))} feet", "used 3 inches in a foot"), W(f"{mixed(F(n * each, 12) + 1)} feet", "made a division mistake")],
                FN("convert", x=f"{n}*{each}", frm="inches", to="feet", form="mixed"), qtype="multi-step", tags={"multistep"})


@fam("012")
def ms_cups(r, L):
    liters = F(r.randint(1, 4)) if L == 0 else F(r.randint(3, 30), 2)
    cup = pick(r, [200, 250, 500]) if L < 2 else pick(r, [150, 200, 250, 300])
    ml = liters * 1000
    need(ml % cup == 0)
    v = ml / cup
    return Item(f"A pitcher holds {dec(liters)} liters of water. How many {cup}-milliliter cups can be filled?", f"{int(v)} cups",
                [f"{dec(liters)} liters = {comma(ml)} milliliters.", f"{comma(ml)} ÷ {cup} = {int(v)} cups."],
                [W(f"{dec(liters * cup)} cups", "multiplied instead of dividing"), W(f"{dec(ml / cup / 10)} cups", "used 100 milliliters in a liter"), W(f"{comma(ml)} cups", "forgot to divide by the cup size")],
                EX(f"{dec(liters)}*1000/{cup}", unit="cups"), qtype="multi-step", tags={"multistep"})


@fam("012")
def ms_ruler(r, L):
    den = pick(r, [2, 4]) if L == 0 else pick(r, [4, 8])
    a = F(r.randint(den, 5 * den), den)
    need(a.denominator > 1 or L == 0)
    obj = pick(r, ["crayon", "eraser", "key", "paper clip", "leaf"])
    alt = f"Inch ruler marked in 1/{den}-inch marks; a {obj} starts at 0 and ends at the mark for {mixed(a)} inches."
    k = r.randint(2, 4)
    v = a * k
    it = Item(f"The ruler shows the length of one {obj}. How long would {k} of these {obj}s be, placed end to end?", f"{mixed(v)} inches",
              [f"One {obj} is {mixed(a)} inches long.", f"{k} × {mixed(a)} = {mixed(v)} inches."],
              [W(f"{mixed(a)} inches", "gave the length of one"), W(f"{mixed(a + k)} inches", "added instead of multiplying"), W(f"{mixed(a * k + F(1, den))} inches", "misread the ruler by one mark")],
              EX(f"{k}*({mixed(a).replace(' ', '+')})", unit="inches", form="mixed"), qtype="visual",
              diagram=Diagram("ruler", {"length": 6, "den": 8, "end": mixed(a), "object": obj}, alt))
    it.consts = [a.numerator, a.denominator, int(a)] + [int(x) for x in mixed(a).replace("/", " ").split()]
    return it


@fam("012")
def ms_time(r, L):
    h = r.randint(1, 4)
    m = r.randint(5, 55)
    n = r.randint(2, 5)
    tot = n * (h * 60 + m)
    H, M = divmod(tot, 60)
    need(M != 0)
    ans = f"{H} hours {M} minutes" if H != 1 else f"1 hour {M} minutes"
    return Item(f"A movie is {h} hour{'s' if h > 1 else ''} {m} minutes long. {name(r)} watches it {n} times. How long is that in hours and minutes?", ans,
                [f"One movie: {h * 60 + m} minutes. {n} times: {tot} minutes.", f"{tot} ÷ 60 = {H} R {M}: {ans}."],
                [W(f"{n * h} hours {n * m} minutes", "did not regroup minutes into hours"), W(f"{H} hours {60 - M} minutes", "used the wrong remainder"), W(f"{tot // 100} hours {tot % 100} minutes", "used 100 minutes in an hour")],
                FN("compound", big="hours", big1="hour", small="minutes", small1="minute", total=str(tot)), qtype="multi-step", tags={"multistep"})


@fam("012")
def ms_fence(r, L):
    l, w = r.randint(4, 15), r.randint(3, 12)
    per = 2 * (l + w)
    unit = pick(r, [("yards", "feet", 3), ("feet", "inches", 12)])
    v = per * unit[2]
    return Item(f"A rectangular garden is {l} {unit[0]} long and {w} {unit[0]} wide. How many {unit[1]} of fencing go around it?", f"{comma(v)} {unit[1]}",
                [f"Perimeter: 2 × ({l} + {w}) = {per} {unit[0]}.", f"{per} × {unit[2]} = {comma(v)} {unit[1]}."],
                [W(f"{per} {unit[1]}", "forgot to convert"), W(f"{comma((l + w) * unit[2])} {unit[1]}", "used only two sides"), W(f"{comma(l * w * unit[2])} {unit[1]}", "found the area")],
                FN("convert", x=f"2*({l}+{w})", frm=unit[0], to=unit[1]), qtype="multi-step", tags={"multistep", "modeling"})


@fam("012")
def ms_mass(r, L):
    n = r.randint(3, 12)
    g = r.randint(120, 350) if L else r.randint(1, 3) * 100
    tot = n * g
    v = F(tot, 1000)
    return Item(f"Each apple has a mass of about {g} grams. What is the mass of {n} apples in kilograms?", f"{dec(v)} kilograms",
                [f"{n} × {g} = {comma(tot)} grams.", f"{comma(tot)} ÷ 1,000 = {dec(v)} kilograms."],
                [W(f"{comma(tot)} kilograms", "forgot to convert grams to kilograms"), W(f"{dec(F(tot, 100))} kilograms", "divided by 100"), W(f"{dec(F(g, 1000) + n)} kilograms", "added the number of apples")],
                FN("convert", x=f"{n}*{g}", frm="grams", to="kilograms"), qtype="multi-step", tags={"multistep"})


SKILLS = {
    1: dict(name="Customary Length Conversions", fams=[cl_convert, cl_compound, cl_add, cl_table, cl_compare, cl_word]),
    2: dict(name="Customary Weight and Capacity Conversions", fams=[wc_convert, wc_compound, wc_compare, wc_word, wc_two_step, wc_fact]),
    3: dict(name="Metric Conversions", fams=[me_convert, me_factor, me_compare, me_word, me_add]),
    4: dict(name="Multi-Step Measurement Problems", fams=[ms_pieces, ms_cups, ms_ruler, ms_time, ms_fence, ms_mass]),
}
