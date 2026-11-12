"""Unit 2: Multi-Digit Multiplication and Division (multiply-divide-whole)."""
from g5lib import *

UNIT_ID = "multi-digit-multiplication-division"


def factors(r, L):
    if L == 0:
        return r.randint(12, 99) if r.random() < 0.5 else r.randint(102, 499), r.randint(3, 9)
    if L == 1:
        return r.randint(102, 899), r.randint(12, 89)
    return pick(r, [(r.randint(1021, 4999), r.randint(12, 79)), (r.randint(121, 899), r.randint(102, 399))])


def partial_wrongs(a, b):
    out = []
    if b >= 10:
        t, o = b // 10 * 10, b % 10
        out.append(W(comma(a * (t // 10) + a * o), "forgot the placeholder zero in the second partial product"))
        out.append(W(comma(a * t), "multiplied by only the tens digit"))
        out.append(W(comma(a * o + a * t + 10 * (1 if a * o % 100 >= 10 else 0) + 100), "made a regrouping (carrying) mistake"))
    else:
        out.append(W(comma(a * b + 10), "forgot to subtract a regrouped ten / added an extra ten"))
        hi, lo = a // 10, a % 10
        out.append(W(str(hi * b) + str(lo * b % 10), "did not regroup (carry) when a partial product was 10 or more") if lo * b >= 10 else W(comma(a * b - 10), "dropped a regrouped ten"))
        out.append(W(comma(a + b), "added instead of multiplying"))
    out.append(W(comma(a * b + 100), "made an addition mistake when adding the partial products"))
    return out


# ============================================================== S1 Multiplying Multi-Digit Whole Numbers
@fam("012")
def m1_std(r, L):
    a, b = factors(r, L)
    p = a * b
    return Item(f"Multiply: {comma(a)} × {comma(b)}", comma(p),
                [f"Multiply {comma(a)} by each place value of {comma(b)}.", f"Add the partial products: {comma(a)} × {comma(b)} = {comma(p)}."],
                partial_wrongs(a, b), EX(f"{a}*{b}"), qtype="procedural", claim=f"{comma(a)} × {comma(b)}")


@fam("012")
def m1_area_model(r, L):
    if L == 0:
        a, b = r.randint(21, 98), r.randint(3, 9)
        rows = [str(b)]
        cols = [str(a // 10 * 10), str(a % 10)]
        need(a % 10)
        cells = [[comma(b * (a // 10 * 10)), comma(b * (a % 10))]]
    else:
        a, b = r.randint(102, 899) if L == 2 else r.randint(21, 98), r.randint(12, 89)
        need(a % 10 and b % 10)
        cols = [str(a // 100 * 100), str(a // 10 % 10 * 10), str(a % 10)] if a >= 100 else [str(a // 10 * 10), str(a % 10)]
        cols = [c for c in cols if c != "0"]
        rows = [str(b // 10 * 10), str(b % 10)]
        cells = [[comma(int(rr) * int(cc)) for cc in cols] for rr in rows]
    p = a * b
    ask = pick(r, ["total", "cell"]) if L else "total"
    alt = f"Area model for {a} × {b}: top labels {', '.join(cols)}; side labels {', '.join(rows)}; partial products " + ", ".join(c for row in cells for c in row) + "."
    if ask == "total":
        it = Item(f"The area model shows {comma(a)} × {comma(b)}. Add the partial products. What is the product?", comma(p),
                  ["Add every partial product in the model.", f"{' + '.join(c for row in cells for c in row)} = {comma(p)}."],
                  partial_wrongs(a, b) if b >= 10 else [W(comma(sum(int(c.replace(',', '')) for c in cells[0][:1])), "used only one partial product"), W(comma(p + 10), "added incorrectly"), W(comma(a + b), "added the factors")],
                  EX(f"{a}*{b}"), qtype="visual", diagram=Diagram("area_model", {"rows": rows, "cols": cols, "cells": cells}, alt))
    else:
        i, j = r.randrange(len(rows)), r.randrange(len(cols))
        v = int(rows[i]) * int(cols[j])
        shown = [[("?" if (x, y) == (i, j) else cells[x][y]) for y in range(len(cols))] for x in range(len(rows))]
        alt2 = f"Area model for {a} × {b}: top labels {', '.join(cols)}; side labels {', '.join(rows)}; one box is marked with a question mark."
        it = Item("What partial product belongs in the box marked “?” in the area model?", comma(v),
                  [f"The box is in the row labeled {rows[i]} and the column labeled {cols[j]}.", f"{rows[i]} × {cols[j]} = {comma(v)}."],
                  [W(comma(int(rows[i]) + int(cols[j])), "added the labels instead of multiplying"), W(comma(v // 10) if v >= 100 else comma(v * 10), "lost or added a zero"), W(comma(v * 10), "wrote an extra zero")],
                  EX(f"{rows[i]}*{cols[j]}"), qtype="visual", diagram=Diagram("area_model", {"rows": rows, "cols": cols, "cells": shown}, alt2))
    return it


@fam("012")
def m1_partial(r, L):
    a, b = factors(r, max(L, 1))
    need(b >= 10 and b < 100)
    t, o = b // 10 * 10, b % 10
    need(o)
    which = pick(r, ["tens", "ones"])
    v = a * (t if which == "tens" else o)
    return Item(f"To find {comma(a)} × {b}, Mia writes {comma(a)} × {b} = ({comma(a)} × {t}) + ({comma(a)} × {o}). What is {comma(a)} × {t if which == 'tens' else o}?", comma(v),
                [f"Multiply {comma(a)} by {t if which == 'tens' else o}.", f"{comma(a)} × {t if which == 'tens' else o} = {comma(v)}."],
                [W(comma(a * (t // 10)) if which == "tens" else comma(a * o * 10), "forgot the zero for the tens" if which == "tens" else "wrote an extra zero"), W(comma(a + (t if which == 'tens' else o)), "added instead of multiplying"), W(comma(a * b), "found the whole product")],
                EX(f"{a}*{t if which == 'tens' else o}"), qtype="fill-blank", tags={"multiple-representations"})


CTX_MULT = [("A school orders {b} boxes of pencils. Each box has {a} pencils. How many pencils are there in all?", "pencils"),
            ("A theater has {b} rows with {a} seats in each row. How many seats are there?", "seats"),
            ("A farmer plants {b} rows of corn with {a} plants in each row. How many plants is that?", "plants"),
            ("A bakery makes {a} muffins each day for {b} days. How many muffins does it make?", "muffins"),
            ("Each of {b} buses travels {a} miles on a field-trip route. How many miles do the buses travel in all?", "miles")]


@fam("012")
def m1_word(r, L):
    a, b = factors(r, L)
    t, unit = pick(r, CTX_MULT)
    p = a * b
    return Item(t.format(a=comma(a), b=comma(b)), f"{comma(p)} {unit}", [f"Multiply {comma(a)} × {comma(b)}.", f"{comma(a)} × {comma(b)} = {comma(p)} {unit}."],
                [W(f"{w[0]} {unit}", w[1]) for w in partial_wrongs(a, b)], EX(f"{a}*{b}", unit=unit), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def m1_same_value(r, L):
    a = r.randint(12, 99) if L < 2 else r.randint(102, 499)
    b = r.randint(12, 49)
    need(a % 10 and b % 10)
    t, o = a // 10 * 10, a % 10
    good = f"({t} × {b}) + ({o} × {b})"
    bad = [f"({t} × {b}) + {o}", f"({t} + {b}) × ({o} + {b})", f"{t} × {b} × {o}"]
    opts = [(good, True)] + [(x, False) for x in bad]
    r.shuffle(opts)
    return Item(f"Which expression has the same value as {a} × {b}?", good,
                [f"Break {a} into {t} + {o} and multiply each part by {b} (the distributive property).", f"{good} = {comma(a * b)}."],
                check=FN("same_value", target=f"{a}*{b}"), options=opts, mode="mc", qtype="compare-strategies", tags={"multiple-representations"})


@fam("12", mode="mc")
def m1_steps(r, L):
    a, b = r.randint(21, 98), r.randint(21, 89)
    need(a % 10 and b % 10)
    o, t = b % 10, b // 10 * 10
    A = f"Multiply {a} × {o} = {comma(a * o)}."
    B = f"Multiply {a} × {t} = {comma(a * t)}."
    C = f"Add {comma(a * o)} + {comma(a * t)} = {comma(a * b)}."
    lab = ["A", "B", "C"]
    steps = [A, B, C]
    order = list(range(3))
    r.shuffle(order)
    need(order != [0, 1, 2])
    shown = "  ".join(f"{lab[i]}) {steps[order[i]]}" for i in range(3))
    pos = {order[i]: lab[i] for i in range(3)}
    good = ", ".join(pos[k] for k in (0, 1, 2))
    import itertools
    bad = [", ".join(p) for p in itertools.permutations(lab) if ", ".join(p) != good]
    r.shuffle(bad)
    return mc_key(f"Put the steps for {a} × {b} in order (standard algorithm). {shown}", good, bad[:3],
                  ["First multiply by the ones digit, then by the tens, then add the partial products.", f"Order: {good}."], r=r, qtype="ordering")


# ============================================================== S2 Estimating Products and Quotients
def lead_round(n):
    p = 10 ** (len(str(n)) - 1)
    return (n + p // 2) // p * p


@fam("012")
def e_product(r, L):
    a, b = factors(r, max(L, 1))
    ra, rb = lead_round(a), lead_round(b)
    need(ra != a or rb != b)
    est = ra * rb
    return Item(f"Estimate {comma(a)} × {comma(b)} by rounding each factor to its greatest place value.", comma(est),
                [f"{comma(a)} rounds to {comma(ra)}; {comma(b)} rounds to {comma(rb)}.", f"{comma(ra)} × {comma(rb)} = {comma(est)}."],
                [W(comma(a * b), "found the exact product instead of an estimate"), W(comma(ra * rb // 10), "lost a zero when multiplying"), W(comma(ra * rb * 10), "wrote an extra zero"),
                 W(comma(a // (10 ** (len(str(a)) - 1)) * 10 ** (len(str(a)) - 1) * rb), "rounded down instead of rounding")],
                FN("est_product", a=a, b=b), qtype="procedural", claim=f"Estimate of {comma(a)} × {comma(b)}")


@fam("012", mode="mc")
def e_quotient(r, L):
    d = r.randint(3, 9) if L < 2 else r.randint(12, 89)
    if L < 2:
        q0 = r.randint(2, 9) * (100 if L else 10)
        n = q0 * d + r.randint(1, d * (10 if L else 5)) * pick(r, [1, -1])
        comp = q0 * d
        good = f"{comma(comp)} ÷ {d} = {comma(q0)}"
    else:
        d10 = lead_round(d)
        need(d10 != d)
        q0 = r.randint(2, 9) * 10
        comp = q0 * d10
        n = comp + r.randint(-d10 * 3, d10 * 3)
        good = f"{comma(comp)} ÷ {d10} = {comma(q0)}"
    need(n > 0 and n != comp)
    dd = d if L < 2 else lead_round(d)
    ln = lead_round(n)
    bad = []
    if ln % dd:
        bad.append(f"{comma(ln)} ÷ {dd}")
    bad += [f"{comma(n)} ÷ {dd + 1}" if n % (dd + 1) else f"{comma(n + 1)} ÷ {dd}", f"{comma(comp + dd * 10 + 1)} ÷ {dd}", f"{comma(n)} ÷ 10"]
    bad = [x for x in dict.fromkeys(bad) if x != f"{comma(comp)} ÷ {dd}"][:3]
    good = f"{comma(comp)} ÷ {dd}"
    return mc_key(f"Which division uses compatible numbers to estimate {comma(n)} ÷ {d}?", good, bad,
                  [f"Compatible numbers divide evenly and are close to the real numbers: {comma(comp)} is close to {comma(n)} and {comma(comp)} ÷ {dd} = {comma(q0)}.", f"So use {good}."], r=r, qtype="compare-strategies")


@fam("012", mode="mc")
def e_quotient_value(r, L):
    d = r.randint(3, 9)
    q0 = r.randint(2, 9) * (10 if L == 0 else 100)
    comp = q0 * d
    n = comp + pick(r, [1, -1]) * r.randint(1, d * 3)
    need(n > 0 and n % d)
    good = comma(q0)
    bad = [comma(q0 * 10), comma(q0 // 10), comma(q0 + 100 if L else q0 + 10)]
    return mc_key(f"{name(r)} uses compatible numbers to estimate {comma(n)} ÷ {d}. Which estimate makes sense?", good, bad,
                  [f"{comma(comp)} is close to {comma(n)} and divides evenly by {d}.", f"{comma(comp)} ÷ {d} = {good}."], r=r, qtype="numerical")


@fam("012", mode="mc")
def e_reasonable(r, L):
    a, b = factors(r, max(L, 1))
    ra, rb = lead_round(a), lead_round(b)
    est = ra * rb
    nm = name(r)
    wrong_claim = r.random() < 0.6
    claim = a * b if not wrong_claim else pick(r, [a * b // 10, a * (b // 10) + a * (b % 10)])
    need(claim != a * b or not wrong_claim)
    big_gap = abs(claim - est) * 3 > est
    need(big_gap == wrong_claim)
    good = (f"Not reasonable. {comma(ra)} × {comma(rb)} = {comma(est)}, so the answer should be close to {comma(est)}." if wrong_claim
            else f"Reasonable. {comma(ra)} × {comma(rb)} = {comma(est)}, which is close to {comma(claim)}.")
    bad = [(f"Reasonable. {comma(ra)} × {comma(rb)} = {comma(est)}, which is close to {comma(claim)}." if wrong_claim
            else f"Not reasonable. {comma(ra)} × {comma(rb)} = {comma(est)}, so the answer should be close to {comma(est)}."),
           f"Reasonable, because the answer has more digits than both factors.", f"Not reasonable, because the product should be less than {comma(a)}."]
    return mc_key(f"{nm} found {comma(a)} × {comma(b)} = {comma(claim)}. Use estimation. Is the answer reasonable?", good, bad,
                  [f"Round: {comma(ra)} × {comma(rb)} = {comma(est)}.", good], r=r, qtype="explain", tags={"reasoning"})


@fam("012")
def e_over_under(r, L):
    a, b = r.randint(12, 98), r.randint(12, 98)
    up = r.random() < 0.5
    ra = (a // 10 + (1 if up else 0)) * 10
    rb = (b // 10 + (1 if up else 0)) * 10
    need(a % 10 and b % 10 and ra > 0 and rb > 0)
    ans = "overestimate" if up else "underestimate"
    return Item(f"{name(r)} estimates {a} × {b} as {ra} × {rb} = {comma(ra * rb)}. Is the estimate an overestimate or an underestimate?", ans,
                [f"Both factors were rounded {'up' if up else 'down'}.", f"So {comma(ra * rb)} is {'greater' if up else 'less'} than the exact product {comma(a * b)}: an {ans}."],
                [W("underestimate" if up else "overestimate", "mixed up which way the factors were rounded")], FN("over_under", a=a, b=b, est=f"{ra}*{rb}"), qtype="conceptual", mode="sa", tags={"reasoning"})


@fam("012", mode="mc")
def e_between(r, L):
    d = r.randint(3, 9) if L < 2 else r.randint(11, 29)
    lo_q = r.randint(2, 9) * (10 if L == 0 else 100 if L == 1 else 10)
    n = lo_q * d + r.randint(1, d * (10 if L != 1 else 100) - 1)
    q = n // d
    step = 10 if L != 1 else 100
    lo = q // step * step
    good = f"between {comma(lo)} and {comma(lo + step)}"
    bad = [f"between {comma(lo + step)} and {comma(lo + 2 * step)}", f"between {comma(lo - step)} and {comma(lo)}" if lo >= step else f"between {comma(lo * 10 + step * 10)} and {comma(lo * 10 + 2 * step * 10)}",
           f"between {comma(lo * 10)} and {comma((lo + step) * 10)}"]
    return mc_key(f"The quotient {comma(n)} ÷ {d} is ___.", good, bad,
                  [f"{d} × {comma(lo)} = {comma(d * lo)} and {d} × {comma(lo + step)} = {comma(d * (lo + step))}.", f"{comma(n)} is between those, so the quotient is {good}."],
                  r=r, qtype="explain", tags={"reasoning"})


@fam("012")
def e_word(r, L):
    a, b = factors(r, max(L, 1))
    ra, rb = lead_round(a), lead_round(b)
    need(ra != a and rb != b)
    t = pick(r, ["A store sells {a} games each week for {b} weeks.", "A train carries {a} people on each of {b} trips.", "A club collects {a} cans each day for {b} days."])
    return Item(t.format(a=comma(a), b=comma(b)) + " Round each number to its greatest place to estimate the total.", comma(ra * rb),
                [f"Round: {comma(a)} ≈ {comma(ra)} and {comma(b)} ≈ {comma(rb)}.", f"Estimate: {comma(ra)} × {comma(rb)} = {comma(ra * rb)}."],
                [W(comma(a * b), "found the exact answer instead of estimating"), W(comma(ra + rb), "added instead of multiplying"), W(comma(ra * rb // 10), "lost a zero")],
                FN("est_product", a=a, b=b), qtype="real-world", tags={"modeling"})



# ============================================================== S3 Dividing by One-Digit Divisors
def div1(r, L, rem=False):
    d = r.randint(2, 9)
    q = r.randint(12, 99) if L == 0 else r.randint(102, 999) if L == 1 else r.randint(1002, 1999) if d < 5 else r.randint(102, 999)
    if L == 2 and r.random() < 0.4:
        q = int(str(q)[:-2] + "0" + str(q)[-1]) if len(str(q)) >= 3 else q   # a zero in the quotient
    rr = r.randint(1, d - 1) if rem else 0
    return d, q, q * d + rr, rr


def quotient_wrongs(n, d, q):
    out = [W(comma(q * 10), "wrote an extra digit in the quotient"), W(comma(q // 10) if q >= 100 else comma(q + 10), "left out a digit of the quotient")]
    s = str(q)
    if "0" in s[1:]:
        out.insert(0, W(s.replace("0", ""), "left out the zero in the quotient"))
    out.append(W(comma(q + 1), "subtracted incorrectly in one step"))
    out.append(W(comma(n * d), "multiplied instead of dividing"))
    return out


@fam("012")
def d1_divide(r, L):
    d, q, n, _ = div1(r, L)
    return Item(f"Divide: {comma(n)} ÷ {d}", comma(q), [f"Divide place by place: how many groups of {d} in each part of {comma(n)}?", f"{comma(n)} ÷ {d} = {comma(q)}. Check: {comma(q)} × {d} = {comma(n)}."],
                quotient_wrongs(n, d, q), EX(f"{n}/{d}"), qtype="procedural", claim=f"{comma(n)} ÷ {d}")


@fam("012", mode="sa")
def d1_remainder(r, L):
    d, q, n, rr = div1(r, L, True)
    ans = f"{comma(q)} R {rr}"
    return Item(f"Find the quotient and remainder: {comma(n)} ÷ {d}. Write your answer like 12 R 3.", ans,
                [f"{d} × {comma(q)} = {comma(q * d)}.", f"{comma(n)} − {comma(q * d)} = {rr}, which is less than {d}. So the answer is {ans}."],
                [W(f"{comma(q - 1)} R {rr + d}", "left a remainder that is greater than the divisor"), W(f"{comma(q)} R {d - rr}", "found the remainder by counting up instead of subtracting"), W(comma(q), "left out the remainder")],
                FN("quotient_rem", a=str(n), b=str(d)), qtype="procedural", mode="sa", claim=f"{comma(n)} ÷ {d}")


@fam("012")
def d1_area(r, L):
    d = r.randint(3, 9)
    q = r.randint(112, 999) if L else r.randint(21, 99)
    need("0" not in str(q))
    parts = [int(c) * 10 ** (len(str(q)) - 1 - i) for i, c in enumerate(str(q))]
    n = q * d
    hide = r.randrange(len(parts))
    cols = [("?" if i == hide and L == 2 else str(p)) for i, p in enumerate(parts)]
    cells = [[comma(p * d) for p in parts]]
    alt = f"Area model for {comma(n)} ÷ {d}: the side is {d}; the parts across the top are " + ", ".join(cols) + "; the areas inside are " + ", ".join(cells[0]) + "."
    if L < 2:
        return Item(f"The area model shows {comma(n)} ÷ {d}. What is the quotient?", comma(q),
                    [f"The side length is {d}. The top lengths are {' + '.join(map(str, parts))}.", f"Quotient: {' + '.join(map(str, parts))} = {comma(q)}."],
                    [W(comma(n), "gave the dividend"), W(comma(parts[0]), "used only one part of the model"), W(comma(q * 10), "added the parts incorrectly")],
                    EX(f"{n}/{d}"), qtype="visual", diagram=Diagram("area_model", {"rows": [str(d)], "cols": cols, "cells": cells}, alt))
    v = parts[hide]
    return Item(f"The area model shows {comma(n)} ÷ {d}. What number belongs in place of “?”", comma(v),
                [f"The area of that part is {cells[0][hide]} and its side is {d}.", f"{cells[0][hide]} ÷ {d} = {comma(v)}."],
                [W(cells[0][hide], "gave the area instead of the length"), W(comma(v * d * d), "multiplied instead of dividing"), W(comma(q), "gave the whole quotient")],
                EX(f"{parts[hide] * d}/{d}"), qtype="visual", diagram=Diagram("area_model", {"rows": [str(d)], "cols": cols, "cells": cells}, alt))


@fam("012", mode="mc")
def d1_check(r, L):
    d, q, n, _ = div1(r, L)
    good = f"{comma(q)} × {d}"
    bad = [f"{comma(n)} × {d}", f"{comma(q)} + {d}", f"{comma(n)} × {comma(q)}"]
    return mc_key(f"Which expression can you use to check that {comma(n)} ÷ {d} = {comma(q)}?", good, bad,
                  ["Multiplication undoes division: quotient × divisor = dividend.", f"{good} = {comma(n)}."], r=r, qtype="conceptual")


@fam("012")
def d1_missing(r, L):
    d, q, n, _ = div1(r, L)
    return Item(f"Fill in the blank: ___ ÷ {d} = {comma(q)}", comma(n), [f"The missing number is the dividend: quotient × divisor.", f"{comma(q)} × {d} = {comma(n)}."],
                [W(comma(F(q, d)) if q % d == 0 else comma(q + d), "divided instead of multiplying"), W(comma(q + d), "added"), W(comma(n + d), "made a multiplication mistake")],
                EX(f"{q}*{d}"), qtype="fill-blank")


CTX_DIV = [("{n} stickers are shared equally among {d} friends. How many stickers does each friend get?", "stickers"),
           ("A library puts {n} books equally on {d} shelves. How many books go on each shelf?", "books"),
           ("A coach splits {n} tennis balls equally into {d} bins. How many balls are in each bin?", "balls"),
           ("{d} classes collected {n} cans in all, the same number each. How many cans did each class collect?", "cans")]


@fam("012")
def d1_word(r, L):
    d, q, n, _ = div1(r, L)
    t, unit = pick(r, CTX_DIV)
    return Item(t.format(n=comma(n), d=d), f"{comma(q)} {unit}", [f"Divide the total into {d} equal groups: {comma(n)} ÷ {d}.", f"{comma(n)} ÷ {d} = {comma(q)} {unit}."],
                [W(f"{w[0]} {unit}", w[1]) for w in quotient_wrongs(n, d, q)], EX(f"{n}/{d}", unit=unit), qtype="word-problem", tags={"modeling"})


# ============================================================== S4 Dividing by Two-Digit Divisors
def div2(r, L, rem=False):
    d = r.randint(11, 25) if L == 0 else r.randint(12, 59) if L == 1 else r.randint(21, 89)
    q = r.randint(11, 40) if L == 0 else r.randint(21, 99) if L == 1 else r.randint(41, 199)
    rr = r.randint(1, d - 1) if rem else 0
    n = q * d + rr
    need(n < 10000)
    return d, q, n, rr


@fam("012")
def d2_divide(r, L):
    d, q, n, _ = div2(r, L)
    return Item(f"Divide: {comma(n)} ÷ {d}", comma(q), [f"Estimate each digit of the quotient, multiply, subtract, and bring down.", f"{comma(n)} ÷ {d} = {comma(q)}. Check: {comma(q)} × {d} = {comma(n)}."],
                quotient_wrongs(n, d, q), EX(f"{n}/{d}"), qtype="procedural", claim=f"{comma(n)} ÷ {d}")


@fam("012", mode="sa")
def d2_remainder(r, L):
    d, q, n, rr = div2(r, L, True)
    ans = f"{comma(q)} R {rr}"
    return Item(f"Find the quotient and remainder: {comma(n)} ÷ {d}. Write your answer like 12 R 3.", ans,
                [f"{d} × {comma(q)} = {comma(q * d)}.", f"{comma(n)} − {comma(q * d)} = {rr}, which is less than {d}. Answer: {ans}."],
                [W(f"{comma(q - 1)} R {rr + d}", "left a remainder greater than the divisor"), W(f"{comma(q + 1)} R {rr}", "estimated a quotient digit too high"), W(comma(q), "left out the remainder")],
                FN("quotient_rem", a=str(n), b=str(d)), qtype="procedural", mode="sa", claim=f"{comma(n)} ÷ {d}")


@fam("012")
def d2_related(r, L):
    d, q, n, _ = div2(r, L)
    return Item(f"Use the fact {comma(q)} × {d} = {comma(n)}. What is {comma(n)} ÷ {d}?", comma(q),
                [f"Division undoes multiplication.", f"Since {comma(q)} × {d} = {comma(n)}, {comma(n)} ÷ {d} = {comma(q)}."],
                [W(comma(n * d), "multiplied again"), W(str(d), "gave the divisor"), W(comma(n - d), "subtracted")], EX(f"{n}/{d}"), qtype="conceptual", tags={"connections"})


@fam("012")
def d2_pattern(r, L):
    a, b = r.randint(2, 9), r.randint(2, 9)
    p = a * b
    k = r.randint(1, 2) if L < 2 else r.randint(1, 3)
    j = r.randint(0, 1) if L else 0
    n, d = p * 10 ** (k + j), b * 10 ** j
    q = n // d
    return Item(f"Use the basic fact {p} ÷ {b} = {a}. What is {comma(n)} ÷ {comma(d)}?", comma(q),
                [f"{comma(n)} ÷ {comma(d)} is the same as {p} ÷ {b} with the zeros moved.", f"{comma(n)} ÷ {comma(d)} = {comma(q)}."],
                [W(comma(q * 10), "kept too many zeros"), W(comma(q // 10) if q >= 10 else comma(q * 100), "dropped a zero"), W(str(a), "used only the basic fact")],
                EX(f"{n}/{d}"), qtype="numerical", tags={"connections"})


@fam("12")
def d2_area(r, L):
    d = r.randint(12, 39)
    q = r.randint(21, 99) if L == 1 else r.randint(112, 299)
    need(q % 10 and "0" not in str(q))
    parts = [int(c) * 10 ** (len(str(q)) - 1 - i) for i, c in enumerate(str(q))]
    n = q * d
    cells = [[comma(p * d) for p in parts]]
    alt = f"Area model for {comma(n)} ÷ {d}: side {d}; parts across the top " + ", ".join(map(str, parts)) + "; areas " + ", ".join(cells[0]) + "."
    return Item(f"The area model shows {comma(n)} ÷ {d}. What is the quotient?", comma(q),
                [f"Add the lengths across the top: {' + '.join(map(str, parts))}.", f"Quotient = {comma(q)}."],
                [W(comma(parts[0]), "used only one part"), W(comma(n // 10), "divided by 10 instead"), W(comma(q + d), "added the side length")],
                EX(f"{n}/{d}"), qtype="visual", diagram=Diagram("area_model", {"rows": [str(d)], "cols": [str(p) for p in parts], "cells": cells}, alt))


CTX_DIV2 = [("A theater has {n} seats in rows of {d}. How many rows are there?", "rows"),
            ("A factory packs {n} crayons into boxes of {d}. How many boxes are filled?", "boxes"),
            ("A cyclist rides {n} miles in {d} days, the same distance each day. How many miles each day?", "miles"),
            ("{n} students are split into {d} equal teams. How many students are on each team?", "students")]


@fam("012")
def d2_word(r, L):
    d, q, n, _ = div2(r, L)
    t, unit = pick(r, CTX_DIV2)
    return Item(t.format(n=comma(n), d=d), f"{comma(q)} {unit}", [f"Divide: {comma(n)} ÷ {d}.", f"{comma(n)} ÷ {d} = {comma(q)} {unit}."],
                [W(f"{w[0]} {unit}", w[1]) for w in quotient_wrongs(n, d, q)], EX(f"{n}/{d}", unit=unit), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def d2_first_digit(r, L):
    d, q, n, _ = div2(r, L)
    need(q >= 10)
    places = len(str(q))
    good = {1: "ones", 2: "tens", 3: "hundreds"}[places]
    bad = [x for x in ["ones", "tens", "hundreds", "thousands"] if x != good][:3]
    return mc_key(f"In {comma(n)} ÷ {d}, what is the greatest place value in the quotient?", good, bad,
                  [f"{d} × {10 ** (places - 1)} = {comma(d * 10 ** (places - 1))} ≤ {comma(n)} < {comma(d * 10 ** places)} = {d} × {comma(10 ** places)}.", f"So the quotient has {places} digits; the first is in the {good} place."],
                  r=r, qtype="explain", tags={"reasoning"})


# ============================================================== S5 Interpreting Remainders
REM = {"up": [("{n} students are going on a field trip. Each van holds {d} students. How many vans are needed?", "vans"),
              ("A baker needs to pack {n} cookies in boxes that hold {d} each. How many boxes does she need for all the cookies?", "boxes"),
              ("{n} people want to ride a roller coaster. Each car holds {d} people. How many cars are needed?", "cars")],
       "down": [("A florist has {n} roses. Each bouquet uses {d} roses. How many complete bouquets can she make?", "bouquets"),
                ("{n} eggs are put into cartons of {d}. How many cartons can be filled completely?", "cartons"),
                ("A ribbon is {n} inches long. How many {d}-inch pieces can be cut from it?", "pieces")],
       "rem": [("{n} marbles are shared equally by {d} kids. Each kid gets as many as possible. How many marbles are left over?", "marbles"),
               ("A teacher puts {n} crayons into cups of {d}. How many crayons are left after filling as many cups as possible?", "crayons")]}


@fam("012")
def r_interpret(r, L):
    mode = pick(r, ["up", "down", "rem"])
    d = r.randint(3, 9) if L == 0 else r.randint(6, 15) if L == 1 else r.randint(12, 48)
    q = r.randint(3, 12) if L == 0 else r.randint(8, 40) if L == 1 else r.randint(12, 80)
    rr = r.randint(1, d - 1)
    n = q * d + rr
    t, unit = pick(r, REM[mode])
    want = {"up": q + 1, "down": q, "rem": rr}[mode]
    ans = f"{comma(want)} {unit}"
    why = {"up": f"{q} groups leave {rr} still needing a spot, so one more is needed: {q + 1}.", "down": f"Only complete groups count, so the {rr} left over do not make another.", "rem": f"The remainder is the number left over: {rr}."}[mode]
    others = {"up": [q, f"{q} R {rr}", rr], "down": [q + 1, f"{q} R {rr}", rr], "rem": [q, q + 1, d - rr]}[mode]
    return Item(t.format(n=comma(n), d=d), ans, [f"{comma(n)} ÷ {d} = {comma(q)} R {rr}.", why],
                [W(f"{x} {unit}" if not isinstance(x, str) else f"{x} {unit}", "did not think about what the remainder means") for x in others],
                FN("remainder_use", a=str(n), b=str(d), mode=mode, unit=unit), qtype="word-problem", tags={"modeling", "reasoning"})


@fam("012")
def r_share(r, L):
    d = r.randint(2, 6) if L < 2 else r.randint(4, 12)
    q = r.randint(1, 9)
    rr = r.randint(1, d - 1)
    n = q * d + rr
    item = pick(r, [("pizzas", "pizzas"), ("pounds of clay", "pounds"), ("yards of ribbon", "yards"), ("granola bars", "granola bars")])
    v = F(n, d)
    ans = f"{mixed(v)} {item[1]}"
    return Item(f"{n} {item[0]} are shared equally by {d} friends. How much does each friend get? Write a mixed number.", ans,
                [f"{n} ÷ {d} = {q} R {rr}.", f"The remainder is shared too: each gets {q} and {rr}/{d} more = {mixed(v)} {item[1]}."],
                [W(f"{q} {item[1]}", "ignored the remainder"), W(f"{q} {rr}/{n} {item[1]}" if rr < n else f"{q + 1} {item[1]}", "used the dividend as the denominator"), W(f"{q + 1} {item[1]}", "rounded up instead of sharing the remainder"),
                 W(f"{d}/{n} {item[1]}", "divided the wrong way")],
                FN("remainder_use", a=str(n), b=str(d), mode="frac", unit=item[1]), qtype="real-world", tags={"connections"})


@fam("012", mode="mc")
def r_which(r, L):
    n, d = r.randint(50, 300), r.randint(6, 30)
    need(n % d)
    t = pick(r, list(REM))
    stem = {"up": f"How many tables of {d} are needed to seat {n} guests?", "down": f"How many full packs of {d} can be made from {n} cards?", "rem": f"If {n} cards are put in packs of {d}, how many cards are left over?"}[t]
    good = {"up": "Round the quotient up to the next whole number.", "down": "Drop the remainder and use the whole-number quotient.", "rem": "Use the remainder as the answer."}[t]
    bad = [v for k, v in {"up": "Round the quotient up to the next whole number.", "down": "Drop the remainder and use the whole-number quotient.", "rem": "Use the remainder as the answer."}.items() if k != t]
    bad.append("Write the remainder as a decimal and keep it.")
    return mc_key(f"{stem} How should you use the remainder?", good, bad,
                  [f"{n} ÷ {d} = {n // d} R {n % d}.", good], r=r, qtype="explain", tags={"reasoning"})


@fam("12")
def r_two_step(r, L):
    per = r.randint(12, 30)
    tickets = r.randint(3, 9)
    total_people = per * r.randint(6, 20) + r.randint(1, per - 1)
    cost = tickets
    vans = -(-total_people // per)
    ans = f"${comma(vans * r.randint(40, 90))}"
    price = int(ans[1:].replace(",", "")) // vans
    tot = vans * price
    return Item(f"{comma(total_people)} students are going to a museum. Each bus holds {per} students and costs ${price} to rent. What is the total cost of the buses?",
                f"${comma(tot)}", [f"{comma(total_people)} ÷ {per} = {total_people // per} R {total_people % per}, so {vans} buses are needed.", f"{vans} × ${price} = ${comma(tot)}."],
                [W(f"${comma((vans - 1) * price)}", "dropped the remainder, leaving students without a bus"), W(f"${comma(total_people * price)}", "multiplied the number of students by the price"), W(f"${comma(price * per)}", "multiplied the bus size by the price")],
                FN("bus_cost", n=total_people, d=per, price=price), qtype="multi-step", tags={"multistep", "modeling"})


@fam("012", mode="mc")
def r_meaning(r, L):
    d = r.randint(3, 9)
    q = r.randint(4, 15)
    rr = r.randint(1, d - 1)
    n = q * d + rr
    thing, grp = pick(r, [("pencils", "tables"), ("apples", "baskets"), ("stickers", "pages"), ("cards", "players")])
    good = f"Each of the {d} {grp} gets {q} {thing}, and {rr} {thing} are left over."
    bad = [f"Each of the {d} {grp} gets {rr} {thing}, and {q} {thing} are left over.", f"Each of the {d} {grp} gets {q + 1} {thing}.",
           f"There are {q} {grp} with {d} {thing} each and none left over."]
    return mc_key(f"{n} {thing} are shared equally among {d} {grp}. The answer to {n} ÷ {d} is {q} R {rr}. What does {q} R {rr} mean?", good, bad,
                  [f"{q} is the number each group gets; {rr} is what remains.", good], r=r, qtype="explain", tags={"reasoning"})


@fam("012")
def r_total(r, L):
    d = r.randint(3, 9) if L == 0 else r.randint(6, 24)
    q = r.randint(4, 15) if L == 0 else r.randint(12, 60)
    rr = r.randint(1, d - 1)
    nm = name(r)
    n = q * d + rr
    return Item(f"{nm} put cards into packs of {d}. {nm} made {q} full packs and had {rr} cards left over. How many cards did {nm} start with?", f"{comma(n)} cards",
                [f"{q} packs × {d} cards = {comma(q * d)} cards.", f"{comma(q * d)} + {rr} = {comma(n)} cards."],
                [W(f"{comma(q * d)} cards", "forgot to add the leftover cards"), W(f"{comma(q + d + rr)} cards", "added all the numbers"), W(f"{comma(q * (d + rr))} cards", "added the leftovers to every pack")],
                EX(f"{q}*{d}+{rr}", unit="cards"), qtype="word-problem", tags={"reasoning"})


SKILLS = {
    1: dict(name="Multiplying Multi-Digit Whole Numbers", fams=[m1_std, m1_area_model, m1_partial, m1_word, m1_same_value, m1_steps]),
    2: dict(name="Estimating Products and Quotients", fams=[e_product, e_quotient, e_quotient_value, e_reasonable, e_over_under, e_between, e_word]),
    3: dict(name="Dividing by One-Digit Divisors", fams=[d1_divide, d1_remainder, d1_area, d1_check, d1_missing, d1_word]),
    4: dict(name="Dividing by Two-Digit Divisors", fams=[d2_divide, d2_remainder, d2_related, d2_pattern, d2_area, d2_word, d2_first_digit]),
    5: dict(name="Interpreting Remainders in Word Problems", fams=[r_interpret, r_share, r_which, r_two_step, r_meaning, r_total]),
}
