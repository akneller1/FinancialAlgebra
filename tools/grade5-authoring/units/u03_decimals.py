"""Unit 3: Decimal Operations (decimal-operations)."""
from g5lib import *

UNIT_ID = "decimal-operations"


def rdec(r, lo, hi, places):
    return F(r.randint(int(lo * 10 ** places), int(hi * 10 ** places)), 10 ** places)


def places(x):
    s = dec(x)
    return len(s.split(".")[1]) if "." in s else 0


def misalign(a, b, op):
    """Answer a student gets by lining up the right-most digits instead of the decimal points."""
    pa, pb = places(a), places(b)
    if pa == pb:
        return None
    ia, ib = int(dec(a).replace(".", "").replace(",", "")), int(dec(b).replace(".", "").replace(",", ""))
    p = max(pa, pb)
    v = F(ia + ib if op == "+" else ia - ib, 10 ** p)
    return dec(v) if v > 0 else None


# ============================================================== S1 Adding and Subtracting Decimals
def addsub_pair(r, L):
    if L == 0:
        a, b = rdec(r, 1, 30, 1), rdec(r, 1, 20, pick(r, [1, 2]))
    elif L == 1:
        a, b = rdec(r, 2, 80, pick(r, [1, 2])), rdec(r, 1, 50, pick(r, [1, 2]))
    else:
        a, b = pick(r, [F(r.randint(5, 90)), rdec(r, 10, 200, 1)]), rdec(r, 1, 60, 2)
    need(a.denominator > 1 or b.denominator > 1)
    return a, b


@fam("012")
def a_add(r, L):
    a, b = addsub_pair(r, L)
    s = a + b
    bad = [W(misalign(a, b, "+"), "lined up the last digits instead of the decimal points")] if misalign(a, b, "+") else []
    bad += [W(dec(s - F(1, 10)) if s > 1 else dec(s + 1), "forgot to regroup (carry) a ten"), W(dec(s + F(1, 10)), "regrouped when it was not needed"), W(dec(s + 1), "added the whole numbers incorrectly")]
    return Item(f"Add: {dec(a)} + {dec(b)}", dec(s), ["Line up the decimal points. Write zeros so both numbers have the same number of places.", f"{dec(a)} + {dec(b)} = {dec(s)}."],
                bad, EX(f"{dec(a)}+{dec(b)}"), qtype="procedural", claim=f"{dec(a)} + {dec(b)}")


@fam("012")
def a_sub(r, L):
    a, b = addsub_pair(r, L)
    if a < b:
        a, b = b, a
    need(a != b)
    s = a - b
    bad = [W(misalign(a, b, "-"), "lined up the last digits instead of the decimal points")] if misalign(a, b, "-") else []
    bad += [W(dec(s + F(1, 10)), "forgot to regroup (borrow) when subtracting"), W(dec(a + b), "added instead of subtracting"), W(dec(s - F(1, 10)) if s > F(1, 10) else dec(s + 1), "regrouped twice")]
    return Item(f"Subtract: {dec(a)} − {dec(b)}", dec(s), ["Line up the decimal points. Write zeros to fill empty places.", f"{dec(a)} − {dec(b)} = {dec(s)}."],
                bad, EX(f"{dec(a)}-{dec(b)}"), qtype="procedural", claim=f"{dec(a)} − {dec(b)}")


@fam("012")
def a_missing(r, L):
    a, b = addsub_pair(r, L)
    s = a + b
    return Item(f"Fill in the blank: {dec(a)} + ___ = {dec(s)}", dec(b), [f"The missing addend is {dec(s)} − {dec(a)}.", f"{dec(s)} − {dec(a)} = {dec(b)}."],
                [W(dec(s + a), "added instead of subtracting"), W(misalign(s, a, "-") or dec(b + 1), "lined up the last digits"), W(dec(b + F(1, 10)), "did not regroup")],
                EX(f"{dec(s)}-{dec(a)}"), qtype="fill-blank")


CTX_ADD = [("{n} ran {a} kilometers on Monday and {b} kilometers on Tuesday. How far did {n} run in all?", "kilometers", "+"),
           ("A pumpkin weighs {a} pounds. A watermelon weighs {b} pounds. How much do they weigh together?", "pounds", "+"),
           ("A rope is {a} meters long. {n} cuts off {b} meters. How long is the rope now?", "meters", "-"),
           ("A bottle holds {a} liters of water. {n} drinks {b} liters. How much water is left?", "liters", "-"),
           ("{n} has {a} centimeters of tape and buys {b} centimeters more. How much tape does {n} have now?", "centimeters", "+")]


@fam("012")
def a_word(r, L):
    a, b = addsub_pair(r, L)
    t, unit, op = pick(r, CTX_ADD)
    if op == "-" and a < b:
        a, b = b, a
    need(a != b)
    v = a + b if op == "+" else a - b
    return Item(t.format(n=name(r), a=dec(a), b=dec(b)), f"{dec(v)} {unit}",
                [f"{'Add' if op == '+' else 'Subtract'}: {dec(a)} {op if op == '+' else '−'} {dec(b)}.", f"The answer is {dec(v)} {unit}."],
                [W(f"{dec(a - b if op == '+' else a + b)} {unit}", "used the wrong operation"), W(f"{misalign(a, b, op)} {unit}", "lined up the last digits") if misalign(a, b, op) else W(f"{dec(v + 1)} {unit}", "made a regrouping mistake"),
                 W(f"{dec(v + F(1, 10))} {unit}", "made a regrouping mistake")],
                EX(f"{dec(a)}{op}{dec(b)}", unit=unit), qtype="word-problem", tags={"modeling"})


@fam("012")
def a_estimate(r, L):
    a, b = rdec(r, 2, 40, 2), rdec(r, 1, 30, 2)
    op = pick(r, ["+", "−"]) if L else "+"
    if op == "−" and a < b:
        a, b = b, a
    ra, rb = F(round(a)), F(round(b))
    need(abs(a - ra) != F(1, 2) and abs(b - rb) != F(1, 2))
    v = ra + rb if op == "+" else ra - rb
    return Item(f"Estimate by rounding each number to the nearest whole number: {dec(a)} {op} {dec(b)}", dec(v),
                [f"{dec(a)} ≈ {dec(ra)} and {dec(b)} ≈ {dec(rb)}.", f"{dec(ra)} {op} {dec(rb)} = {dec(v)}."],
                [W(dec(a + b if op == "+" else a - b), "found the exact answer instead of estimating"), W(dec(F(int(a)) + F(int(b)) if op == "+" else F(int(a)) - F(int(b))), "dropped the decimals instead of rounding"),
                 W(dec(v + 1), "rounded one number the wrong way")],
                FN("est_sum", a=dec(a), b=dec(b), op=op), qtype="procedural")


@fam("012")
def a_grid(r, L):
    a = r.randint(11, 70)
    b = r.randint(5, 99 - a) if L == 0 else r.randint(10, 99)
    total = a + b
    g = 1 if total <= 100 else 2
    alt = f"{g} hundred grid{'s' if g > 1 else ''}; each grid is one whole; {total} small squares are shaded: {a} first, then {b} more."
    it = Item(f"The model shows {dec(F(a, 100))} + {dec(F(b, 100))}. Each large square is 1 whole. What is the sum?", dec(F(total, 100)),
              [f"{a} hundredths + {b} hundredths = {total} hundredths.", f"{total} hundredths = {dec(F(total, 100))}."],
              [W(dec(F(total, 10)), "read the squares as tenths"), W(str(total), "forgot that each square is a hundredth"), W(dec(F(abs(a - b), 100)), "subtracted")],
              EX(f"{dec(F(a, 100))}+{dec(F(b, 100))}"), qtype="visual", diagram=Diagram("hundred_grid", {"shaded": total, "grids": g}, alt))
    return it


# ============================================================== S2 Multiplying Decimals by Whole Numbers
def place_wrongs(v, why_more="put the decimal point in the wrong place (one place too far right)", why_less="put the decimal point in the wrong place (one place too far left)"):
    return [W(dec(v * 10), why_more), W(dec(v / 10), why_less)]


@fam("012")
def mw_compute(r, L):
    n = r.randint(2, 9) if L < 2 else r.randint(11, 48)
    x = rdec(r, 0.1, 0.9, 1) if L == 0 else rdec(r, 1, 9, 2) if L == 1 else rdec(r, 1, 20, pick(r, [1, 2]))
    need(x.denominator > 1)
    v = n * x
    ign = int(dec(x).replace(".", "")) * n
    return Item(f"Multiply: {n} × {dec(x)}", dec(v), [f"Multiply as if whole numbers: {n} × {dec(x).replace('.', '').lstrip('0')} = {comma(ign)}.", f"{dec(x)} has {places(x)} decimal place{'s' if places(x) > 1 else ''}, so {n} × {dec(x)} = {dec(v)}."],
                place_wrongs(v) + [W(comma(ign), "ignored the decimal point"), W(dec(n + x), "added instead of multiplying")], EX(f"{n}*{dec(x)}"), qtype="procedural", claim=f"{n} × {dec(x)}")


@fam("012")
def mw_money(r, L):
    n = r.randint(2, 9) if L < 2 else r.randint(11, 30)
    x = rdec(r, 0.25, 9.99, 2)
    need(x.denominator > 1)
    item = pick(r, ["notebooks", "markers", "bags of popcorn", "bottles of juice", "packs of cards", "glue sticks"])
    v = n * x
    return Item(f"{name(r)} buys {n} {item} for {money(x)} each. What is the total cost?", money(v),
                [f"Multiply: {n} × {money(x)}.", f"{n} × {money(x)} = {money(v)}."],
                [W(money(v * 10), "put the decimal point in the wrong place"), W(money(n + x), "added instead of multiplying"), W(money(v - x), "multiplied by one less"), W(money(v / 10), "put the decimal point in the wrong place")],
                EX(f"{n}*{dec(x)}", form="money"), qtype="real-world", tags={"modeling"})


@fam("012")
def mw_repeated(r, L):
    n = r.randint(3, 6)
    x = rdec(r, 0.1, 0.9, 1) if L == 0 else rdec(r, 0.11, 2.5, 2)
    need(x.denominator > 1)
    v = n * x
    it = Item(f"Write the sum as a product and find its value: {' + '.join([dec(x)] * n)}", dec(v),
                [f"{n} groups of {dec(x)} is {n} × {dec(x)}.", f"{n} × {dec(x)} = {dec(v)}."],
                place_wrongs(v) + [W(dec(x + n), "added the number of groups")], EX(f"{n}*{dec(x)}"), qtype="conceptual", tags={"connections"})
    it.consts = [n]
    return it


@fam("012")
def mw_area(r, L):
    n = r.randint(3, 9)
    w = r.randint(1, 9)
    t, h = r.randint(1, 9), r.randint(0 if L < 2 else 1, 9)
    x = w + F(t, 10) + F(h, 100)
    cols = [str(w), dec(F(t, 10))] + ([dec(F(h, 100))] if h else [])
    cells = [[dec(n * F(c)) for c in cols]]
    v = n * x
    alt = f"Area model for {n} × {dec(x)}: top labels {', '.join(cols)}; side label {n}; partial products {', '.join(cells[0])}."
    return Item(f"The area model shows {n} × {dec(x)}. What is the product?", dec(v),
                [f"Partial products: {' + '.join(cells[0])}.", f"Sum: {dec(v)}."],
                place_wrongs(v) + [W(dec(n * w), "used only the whole-number part")], EX(f"{n}*{dec(x)}"), qtype="visual",
                diagram=Diagram("area_model", {"rows": [str(n)], "cols": cols, "cells": cells}, alt))


@fam("012", mode="mc")
def mw_place_point(r, L):
    n = r.randint(3, 9) if L < 2 else r.randint(12, 40)
    x = rdec(r, 1.1, 9.9, 1 if L == 0 else 2)
    need(x.denominator > 1 and (n * x).denominator > 1)
    v = n * x
    digits = dec(v).replace(".", "").replace(",", "")
    good = dec(v)
    bad = list(dict.fromkeys([dec(v * 10), dec(v / 10), comma(int(digits)), dec(v * 100)]))
    bad = [b for b in bad if b != good][:3]
    return mc_key(f"{name(r)} multiplied {n} × {dec(x)} and got the digits {digits} but forgot the decimal point. What is the correct product?", good, bad,
                  [f"Estimate: {n} × {round(x)} ≈ {n * round(x)}.", f"So the product is {good}."], r=r, qtype="explain", tags={"reasoning"})


# ============================================================== S3 Multiplying Decimals by Decimals
def dd_pair(r, L):
    if L == 0:
        return rdec(r, 0.1, 0.9, 1), rdec(r, 0.1, 0.9, 1)
    if L == 1:
        return rdec(r, 1.1, 9.9, 1), rdec(r, 0.1, 0.9, 1)
    return rdec(r, 1.01, 9.99, pick(r, [1, 2])), rdec(r, 1.1, 5.9, 1)


@fam("012")
def md_compute(r, L):
    a, b = dd_pair(r, L)
    need(a.denominator > 1 and b.denominator > 1)
    v = a * b
    return Item(f"Multiply: {dec(a)} × {dec(b)}", dec(v), [f"Multiply the digits as whole numbers, then count decimal places: {places(a)} + {places(b)} = {places(a) + places(b)}.", f"{dec(a)} × {dec(b)} = {dec(v)}."],
                place_wrongs(v, "counted too few decimal places", "counted too many decimal places") + [W(dec(a + b), "added instead of multiplying"), W(dec(F(int(a)) * F(int(b)) + (a - int(a)) * (b - int(b))), "multiplied the whole parts and the decimal parts separately") if a > 1 else W(dec(v * 100), "ignored the decimal places")],
                EX(f"{dec(a)}*{dec(b)}"), qtype="procedural", claim=f"{dec(a)} × {dec(b)}")


@fam("012")
def md_grid(r, L):
    a, b = r.randint(1, 9), r.randint(1, 9)
    v = F(a * b, 100)
    alt = f"A 10 by 10 square (1 whole). {a} of 10 rows and {b} of 10 columns are shaded; the overlap is {a * b} small squares."
    return Item(f"The model shows {dec(F(a, 10))} × {dec(F(b, 10))}. The darkest part is where the two shadings overlap. What is the product?", dec(v),
                [f"The overlap is {a} × {b} = {a * b} small squares out of 100.", f"{a * b} hundredths = {dec(v)}."],
                [W(dec(F(a * b, 10)), "read the squares as tenths"), W(dec(F(a + b, 10)), "added the tenths"), W(str(a * b), "forgot that each square is a hundredth")],
                EX(f"{dec(F(a, 10))}*{dec(F(b, 10))}"), qtype="visual",
                diagram=Diagram("area_grid", {"rows": 10, "cols": 10, "sh_rows": a, "sh_cols": b, "mode": "overlap"}, alt))


@fam("012")
def md_places(r, L):
    a, b = dd_pair(r, L)
    need(a.denominator > 1 and b.denominator > 1)
    k = places(a) + places(b)
    return Item(f"Before any zeros are dropped, how many decimal places does the product {dec(a)} × {dec(b)} have?", str(k),
                [f"{dec(a)} has {places(a)} and {dec(b)} has {places(b)} decimal place{'s' if places(b) > 1 else ''}.", f"{places(a)} + {places(b)} = {k}."],
                [W(str(max(places(a), places(b))), "used the larger count instead of the total"), W(str(k + 1), "counted the whole-number digits"), W(str(places(a) * places(b)) if places(a) * places(b) != k else str(k + 2), "multiplied the counts")],
                FN("dec_places", a=dec(a), b=dec(b)), qtype="conceptual", tags={"reasoning"})


@fam("012", mode="mc")
def md_estimate(r, L):
    a, b = rdec(r, 1.1, 9.9, 1), rdec(r, 1.1, 9.9, 1)
    ra, rb = round(a), round(b)
    need(abs(a - ra) < F(4, 10) and abs(b - rb) < F(4, 10))
    good = f"about {ra * rb}"
    bad = [f"about {ra + rb}", f"about {ra * rb * 10}", f"about {F(ra * rb, 10)}" if (ra * rb) % 10 else f"about {ra * rb // 10}"]
    bad = [str(x).replace("about ", "about ") for x in bad]
    return mc_key(f"Which is the best estimate of {dec(a)} × {dec(b)}?", good, bad, [f"{dec(a)} ≈ {ra} and {dec(b)} ≈ {rb}.", f"{ra} × {rb} = {ra * rb}."], r=r, qtype="numerical")


CTX_DD = [("Ribbon costs {p} per meter. How much do {q} meters cost?", "money"),
          ("A car travels {q} miles on each tenth of a gallon... ", None),
          ("A garden bed is {p2} meters long and {q} meters wide. What is its area?", "square meters"),
          ("One pound of grapes costs {p}. How much do {q} pounds cost?", "money")]


@fam("012")
def md_word(r, L):
    t, unit = pick(r, [CTX_DD[0], CTX_DD[2], CTX_DD[3]])
    q = rdec(r, 1.5, 6.5, 1)
    need(q.denominator > 1)
    if unit == "money":
        p = rdec(r, 0.4, 4.8, 1)
        v = p * q
        need((v * 100).denominator == 1)
        return Item(t.format(p=money(p), q=dec(q)), money(v), [f"Multiply: {dec(q)} × {money(p)}.", f"{dec(q)} × {money(p)} = {money(v)}."],
                    [W(money(v * 10), "put the decimal point in the wrong place"), W(money(p + q), "added instead of multiplying"), W(money(v / 10) if (v / 10 * 100).denominator == 1 else money(v + 1), "put the decimal point in the wrong place")],
                    EX(f"{dec(q)}*{dec(p)}", form="money"), qtype="real-world", tags={"modeling"})
    p2 = rdec(r, 2.1, 9.9, 1)
    v = p2 * q
    return Item(t.format(p2=dec(p2), q=dec(q)), f"{dec(v)} square meters", [f"Area = length × width = {dec(p2)} × {dec(q)}.", f"= {dec(v)} square meters."],
                [W(f"{dec(p2 + q)} square meters", "added instead of multiplying"), W(f"{dec(2 * (p2 + q))} square meters", "found the perimeter"), W(f"{dec(v * 10)} square meters", "misplaced the decimal point")],
                EX(f"{dec(p2)}*{dec(q)}", unit="square meters"), qtype="real-world", tags={"modeling"})


@fam("012")
def md_compare(r, L):
    n = rdec(r, 2, 30, 1)
    f = rdec(r, 0.1, 0.9, 1) if r.random() < 0.5 else rdec(r, 1.1, 3.9, 1)
    ans = "less than" if f < 1 else "greater than"
    return Item(f"Without multiplying, is {dec(f)} × {dec(n)} greater than or less than {dec(n)}?", ans,
                [f"{dec(f)} is {'less' if f < 1 else 'greater'} than 1.", f"Multiplying by a number {'less' if f < 1 else 'greater'} than 1 makes the product {ans} {dec(n)}."],
                [W("greater than" if f < 1 else "less than", "thought multiplication always makes a number bigger" if f < 1 else "thought decimals always make a number smaller")],
                FN("scale_cmp", f=dec(f)), qtype="conceptual", mode="sa", tags={"reasoning"})


# ============================================================== S4 Dividing Decimals by Whole Numbers
def dw_pair(r, L):
    d = r.randint(2, 9)
    q = rdec(r, 0.2, 2.9, 1) if L == 0 else rdec(r, 1.01, 9.99, 2) if L == 1 else rdec(r, 0.02, 0.99, 2)
    if L == 2 and r.random() < 0.5:
        q = rdec(r, 1.01, 4.09, 2)
        s = dec(q)
        need("0" in s.split(".")[1])
    need(q.denominator > 1)
    return d, q, q * d


@fam("012")
def dw_compute(r, L):
    d, q, n = dw_pair(r, L)
    return Item(f"Divide: {dec(n)} ÷ {d}", dec(q), [f"Divide as with whole numbers and place the decimal point in the quotient directly above the one in the dividend.", f"{dec(n)} ÷ {d} = {dec(q)}. Check: {dec(q)} × {d} = {dec(n)}."],
                place_wrongs(q) + [W(dec(n * d), "multiplied instead of dividing"), W(dec(q).replace(".0", ".") if ".0" in dec(q) else dec(q + F(1, 10)), "left out a zero in the quotient" if ".0" in dec(q) else "made a subtraction mistake")],
                EX(f"{dec(n)}/{d}"), qtype="procedural", claim=f"{dec(n)} ÷ {d}")


@fam("012")
def dw_share(r, L):
    d = r.randint(2, 5) if L == 0 else r.randint(2, 8)
    each = rdec(r, 1.05, 9.95 if L == 0 else 19.95, 2)
    need((each * 100).denominator == 1)
    tot = each * d
    item = pick(r, ["a pizza", "a gift for their teacher", "a movie outing", "a bag of craft supplies"])
    return Item(f"{d} friends share the cost of {item} equally. The total is {money(tot)}. How much does each friend pay?", money(each),
                [f"Divide: {money(tot)} ÷ {d}.", f"{money(tot)} ÷ {d} = {money(each)}."],
                [W(money(each * 10), "put the decimal point in the wrong place"), W(money(tot - d), "subtracted instead of dividing"), W(money(tot * d), "multiplied instead of dividing")],
                EX(f"{dec(tot)}/{d}", form="money"), qtype="real-world", tags={"modeling"})


@fam("012")
def dw_tape(r, L):
    d, q, n = dw_pair(r, L)
    alt = f"Tape diagram: a bar labeled {dec(n)} in all, split into {d} equal parts."
    return Item(f"The tape diagram shows {dec(n)} split into {d} equal parts. What is the value of one part?", dec(q),
                [f"One part is {dec(n)} ÷ {d}.", f"{dec(n)} ÷ {d} = {dec(q)}."],
                place_wrongs(q) + [W(dec(n - d) if n > d else dec(n + d), "subtracted the number of parts")], EX(f"{dec(n)}/{d}"), qtype="visual",
                diagram=Diagram("tape", {"parts": d, "shaded": 1, "total_label": dec(n), "note": f"{d} equal parts"}, alt))


@fam("012", mode="mc")
def dw_check(r, L):
    d, q, n = dw_pair(r, L)
    good = f"{dec(q)} × {d} = {dec(n)}"
    bad = [f"{dec(n)} × {d} = {dec(n * d)}", f"{dec(q)} + {d} = {dec(q + d)}", f"{dec(q)} ÷ {d} = {dec(q / d)}" if is_term(q / d) else f"{dec(n)} − {dec(q)} = {dec(n - q)}"]
    return mc_key(f"Which equation checks that {dec(n)} ÷ {d} = {dec(q)}?", good, bad, ["Multiply the quotient by the divisor; you should get the dividend.", good], r=r, qtype="conceptual")


@fam("012")
def dw_word(r, L):
    d, q, n = dw_pair(r, L)
    t, unit = pick(r, [("A {n}-meter rope is cut into {d} equal pieces. How long is each piece?", "meters"),
                       ("{d} runners ran a {n}-kilometer relay, each running the same distance. How far did each run?", "kilometers"),
                       ("A {n}-liter jug of juice is poured equally into {d} pitchers. How much juice is in each pitcher?", "liters")])
    return Item(t.format(n=dec(n), d=d), f"{dec(q)} {unit}", [f"Divide: {dec(n)} ÷ {d}.", f"{dec(n)} ÷ {d} = {dec(q)} {unit}."],
                [W(f"{dec(q * 10)} {unit}", "put the decimal point in the wrong place"), W(f"{dec(n * d)} {unit}", "multiplied instead of dividing"), W(f"{dec(q / 10)} {unit}", "put the decimal point in the wrong place")],
                EX(f"{dec(n)}/{d}", unit=unit), qtype="word-problem", tags={"modeling"})


# ============================================================== S5 Dividing by Decimals
def by_dec(r, L):
    if L == 0:
        d = pick(r, [F(1, 2), F(1, 10), F(1, 4), F(1, 5)])
        q = r.randint(2, 12)
    elif L == 1:
        d = rdec(r, 0.2, 0.9, 1)
        q = r.randint(2, 15)
    else:
        d = pick(r, [rdec(r, 0.02, 0.9, 2), rdec(r, 1.1, 2.5, 1)])
        q = pick(r, [r.randint(3, 40), rdec(r, 1.1, 9.9, 1)])
    n = q * d
    need(is_term(n) and places(n) <= 2 and d.denominator > 1)
    return n, d, q


@fam("012")
def dd_compute(r, L):
    n, d, q = by_dec(r, L)
    k = 10 ** places(d)
    return Item(f"Divide: {dec(n)} ÷ {dec(d)}", dec(q), [f"Multiply both numbers by {k} so the divisor is a whole number: {dec(n * k)} ÷ {dec(d * k)}.", f"{dec(n * k)} ÷ {dec(d * k)} = {dec(q)}."],
                place_wrongs(q, "moved the decimal point too far", "did not move the decimal point in the dividend") + [W(dec(n * d), "multiplied instead of dividing")],
                EX(f"{dec(n)}/{dec(d)}"), qtype="procedural", claim=f"{dec(n)} ÷ {dec(d)}")


@fam("012")
def dd_how_many(r, L):
    d = pick(r, [F(1, 2), F(1, 4), F(1, 10), F(1, 5)]) if L == 0 else pick(r, [F(1, 4), F(3, 4), F(1, 5), F(2, 5), F(1, 20), F(3, 10)])
    k = r.randint(2, 12)
    n = d * k
    need(is_term(n))
    if n.denominator != 1 and L == 0:
        raise Reject()
    nm = name(r)
    t = pick(r, [f"{nm} has {dec(n)} liters of lemonade and fills cups that hold {dec(d)} liter each. How many cups can {nm} fill?",
                 f"A board is {dec(n)} meters long. How many {dec(d)}-meter pieces can be cut from it?"])
    return Item(t, str(k), [f"Find how many groups of {dec(d)} are in {dec(n)}: {dec(n)} ÷ {dec(d)}.", f"{dec(n)} ÷ {dec(d)} = {k}."],
                [W(dec(n * d), "multiplied instead of dividing"), W(str(k * 10), "moved the decimal point too far"), W(dec(F(k, 10)), "did not move the decimal point")],
                EX(f"{dec(n)}/{dec(d)}"), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def dd_equiv(r, L):
    n, d, q = by_dec(r, max(L, 1))
    k = 10 ** places(d)
    good = f"{dec(n * k)} ÷ {dec(d * k)}"
    bad = [f"{dec(n)} ÷ {dec(d * k)}", f"{dec(n * k)} ÷ {dec(d)}", f"{dec(n / 10)} ÷ {dec(d * k)}"]
    bad = [b for b in dict.fromkeys(bad) if b != good]
    opts = [(good, True)] + [(b, False) for b in bad]
    r.shuffle(opts)
    return Item(f"Which expression has the same quotient as {dec(n)} ÷ {dec(d)}?", good,
                [f"Multiplying the dividend and the divisor by the same number ({k}) keeps the quotient the same.", f"{good} = {dec(q)}."],
                check=FN("same_value", target=f"{dec(n)}/{dec(d)}"), options=opts, mode="mc", qtype="compare-strategies", tags={"reasoning"})


@fam("012")
def dd_bigger(r, L):
    n = r.randint(2, 40)
    d = rdec(r, 0.1, 0.9, 1) if r.random() < 0.6 else rdec(r, 1.5, 4, 1)
    ans = "greater than" if d < 1 else "less than"
    return Item(f"Without dividing, is {n} ÷ {dec(d)} greater than or less than {n}?", ans,
                [f"Dividing by a number less than 1 asks how many small parts fit, so the quotient is greater." if d < 1 else "Dividing by a number greater than 1 makes equal groups that are smaller than the total.",
                 f"{n} ÷ {dec(d)} is {ans} {n}."],
                [W("less than" if d < 1 else "greater than", "thought division always makes a number smaller" if d < 1 else "mixed up dividing and multiplying")],
                FN("div_cmp", n=n, d=dec(d)), qtype="conceptual", mode="sa", tags={"reasoning"})


@fam("012")
def dd_jumps(r, L):
    d = pick(r, [F(1, 2), F(1, 4), F(1, 5)]) if L < 2 else pick(r, [F(1, 4), F(1, 5), F(1, 10)])
    n = r.randint(1, 3) if d != F(1, 10) else 1
    k = n / d
    den = d.denominator
    alt = f"Number line from 0 to {n} marked every {dec(d)}, with equal jumps of {dec(d)} from 0 to {n}."
    jumps = [[frac(i * d), frac((i + 1) * d)] for i in range(int(k))]
    it = Item(f"The number line shows jumps of {dec(d)} from 0 to {n}. What is {n} ÷ {dec(d)}?", dec(k),
              [f"Count the jumps of {dec(d)} that fit between 0 and {n}.", f"There are {dec(k)} jumps, so {n} ÷ {dec(d)} = {dec(k)}."],
              [W(dec(n * d), "multiplied instead of dividing"), W(dec(k - 1), "counted the tick marks between, not the jumps"), W(dec(k + 1), "counted the tick marks, including 0")],
              EX(f"{n}/{dec(d)}"), qtype="visual",
              diagram=Diagram("number_line", {"lo": "0", "hi": str(n), "den": den, "fmt": "dec", "labels": "whole", "jumps": jumps}, alt))
    return it


# ============================================================== S6 Decimal Word Problems and Money
@fam("012")
def w_change(r, L):
    a, b = rdec(r, 1.25, 9.75, 2), rdec(r, 0.5, 7.5, 2)
    pay = pick(r, [10, 20]) if a + b < 10 else 20
    need(a + b < pay)
    nm = name(r)
    v = pay - a - b
    return Item(f"{nm} buys a book for {money(a)} and a pen for {money(b)}. {nm} pays with a ${pay} bill. How much change should {nm} get?", money(v),
                [f"Total: {money(a)} + {money(b)} = {money(a + b)}.", f"Change: ${pay}.00 − {money(a + b)} = {money(v)}."],
                [W(money(a + b), "found the total cost, not the change"), W(money(pay - a + b), "added the second price instead of subtracting it"), W(money(v + 1), "made a regrouping mistake")],
                EX(f"{pay}-{dec(a)}-{dec(b)}", form="money"), qtype="real-world", tags={"multistep"})


@fam("012", mode="sa")
def w_better_buy(r, L):
    n1, n2 = r.sample([2, 3, 4, 5, 6, 8, 10], 2)
    u1, u2 = rdec(r, 0.5, 3, 2), rdec(r, 0.5, 3, 2)
    need(u1 != u2 and abs(u1 - u2) >= F(5, 100))
    p1, p2 = u1 * n1, u2 * n2
    need((p1 * 100).denominator == 1 and (p2 * 100).denominator == 1)
    item = pick(r, ["juice boxes", "granola bars", "pencils", "yogurt cups"])
    ans = "Pack A" if u1 < u2 else "Pack B"
    return Item(f"Pack A has {n1} {item} for {money(p1)}. Pack B has {n2} {item} for {money(p2)}. Which pack costs less per item?", ans,
                [f"Pack A: {money(p1)} ÷ {n1} = {money(u1)} each. Pack B: {money(p2)} ÷ {n2} = {money(u2)} each.", f"{ans} costs less per item."],
                [W("Pack B" if ans == "Pack A" else "Pack A", "compared total prices instead of price per item")],
                FN("better_buy", a=[n1, dec(p1)], b=[n2, dec(p2)]), qtype="real-world", mode="sa", tags={"reasoning"})


@fam("012")
def w_multi(r, L):
    lb = r.randint(2, 6) if L < 2 else rdec(r, 1.5, 4.5, 1)
    price = rdec(r, 0.85, 4.95, 2)
    extra = rdec(r, 0.5, 3.5, 2)
    tot = lb * price + extra
    need((tot * 100).denominator == 1)
    food = pick(r, ["apples", "cherries", "carrots", "grapes"])
    return Item(f"{food.capitalize()} cost {money(price)} per pound. {name(r)} buys {dec(lb)} pounds of {food} and a {money(extra)} bag of nuts. What is the total cost?", money(tot),
                [f"{food.capitalize()}: {dec(lb)} × {money(price)} = {money(lb * price)}.", f"Total: {money(lb * price)} + {money(extra)} = {money(tot)}."],
                [W(money(lb * price), "forgot to add the bag of nuts"), W(money(price + extra), "forgot to multiply by the number of pounds"), W(money((price + extra) * lb), "multiplied the nuts by the pounds too")],
                EX(f"{dec(lb)}*{dec(price)}+{dec(extra)}", form="money"), qtype="multi-step", tags={"multistep", "modeling"})


@fam("012")
def w_split(r, L):
    a, b = rdec(r, 8, 30, 2), rdec(r, 1, 8, 2)
    d = r.randint(2, 6)
    tot = a + b
    need(((tot / d) * 100).denominator == 1)
    v = tot / d
    return Item(f"{d} friends order a pizza for {money(a)} and drinks for {money(b)}. They split the total equally. How much does each friend pay?", money(v),
                [f"Total: {money(a)} + {money(b)} = {money(tot)}.", f"Each pays {money(tot)} ÷ {d} = {money(v)}."],
                [W(money(a / d + b) if ((a / d + b) * 100).denominator == 1 else money(tot), "divided only the pizza cost"), W(money(tot), "forgot to divide"), W(money(tot * d), "multiplied instead of dividing")],
                EX(f"({dec(a)}+{dec(b)})/{d}", form="money"), qtype="multi-step", tags={"multistep"})


@fam("012")
def w_budget(r, L):
    budget = r.randint(15, 50)
    n = r.randint(2, 5)
    p = rdec(r, 2.25, 9.75, 2)
    need(n * p < budget)
    v = budget - n * p
    item = pick(r, ["books", "T-shirts", "board games", "model kits"])
    return Item(f"{name(r)} has ${budget} and buys {n} {item} for {money(p)} each. How much money is left?", money(v),
                [f"Cost: {n} × {money(p)} = {money(n * p)}.", f"Left: ${budget}.00 − {money(n * p)} = {money(v)}."],
                [W(money(budget - p), "subtracted the price of only one item"), W(money(n * p), "found the cost, not what is left"), W(money(v + 1), "made a regrouping mistake")],
                EX(f"{budget}-{n}*{dec(p)}", form="money"), qtype="multi-step", tags={"multistep"})


@fam("012", mode="mc")
def w_which_op(r, L):
    a = rdec(r, 2, 20, 2)
    k = r.randint(3, 8)
    op = pick(r, ["×", "÷", "+", "−"])
    stem = {"×": f"Each sticker sheet costs {money(a)}. What do {k} sheets cost?",
            "÷": f"{k} friends share {money(a * k)} equally. How much does each get?",
            "+": f"A shirt costs {money(a)} and a hat costs ${k}.00. What do both cost?",
            "−": f"A game costs {money(a + k)}. It is on sale for ${k}.00 off. What is the sale price?"}[op]
    exprs = {"×": f"{k} × {money(a)}", "÷": f"{money(a * k)} ÷ {k}", "+": f"{money(a)} + ${k}.00", "−": f"{money(a + k)} − ${k}.00"}
    good = exprs[op]
    bad_ops = {"×": [f"{money(a)} + {k}", f"{money(a)} ÷ {k}", f"{money(a)} − {k}"], "÷": [f"{money(a * k)} × {k}", f"{money(a * k)} − {k}", f"{k} ÷ {money(a * k)}"],
               "+": [f"{money(a)} × {k}", f"{money(a)} − ${k}.00", f"${k}.00 − {money(a)}"], "−": [f"{money(a + k)} + ${k}.00", f"{money(a + k)} × {k}", f"{money(a + k)} ÷ {k}"]}[op]
    return mc_key(f"{stem} Which expression answers the question?", good, bad_ops, [f"Decide what the question asks.", f"Use {good}."], r=r, qtype="word-problem", tags={"modeling"})


SKILLS = {
    1: dict(name="Adding and Subtracting Decimals", fams=[a_add, a_sub, a_missing, a_word, a_estimate, a_grid]),
    2: dict(name="Multiplying Decimals by Whole Numbers", fams=[mw_compute, mw_money, mw_repeated, mw_area, mw_place_point]),
    3: dict(name="Multiplying Decimals by Decimals", fams=[md_compute, md_grid, md_places, md_estimate, md_word, md_compare]),
    4: dict(name="Dividing Decimals by Whole Numbers", fams=[dw_compute, dw_share, dw_tape, dw_check, dw_word]),
    5: dict(name="Dividing by Decimals", fams=[dd_compute, dd_how_many, dd_equiv, dd_bigger, dd_jumps]),
    6: dict(name="Decimal Word Problems and Money", fams=[w_change, w_better_buy, w_multi, w_split, w_budget, w_which_op]),
}
