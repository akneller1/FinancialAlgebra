"""Unit 3: Multiplication Strategies and Multi-Digit Multiplication (4.OA.A.1-3, 4.NBT.B.5)."""
from g4lib import *

UNIT_ID = "multiplication-strategies"
PAIRS = [("stickers", "has"), ("baseball cards", "has"), ("marbles", "has"), ("shells", "found"), ("pages", "read"), ("laps", "swam"), ("points", "scored"), ("beads", "used")]
PACK = [("box", "boxes", "crayons"), ("bag", "bags", "oranges"), ("crate", "crates", "bottles"), ("pack", "packs", "pencils"), ("tray", "trays", "seedlings"),
        ("shelf", "shelves", "books"), ("carton", "cartons", "eggs"), ("bus", "buses", "seats"), ("row", "rows", "chairs"), ("case", "cases", "cans")]


def expand(n):
    s = str(n)
    return [int(c) * 10 ** (len(s) - 1 - i) for i, c in enumerate(s) if c != "0"]


# ============================================================== S1 Multiplicative Comparisons
def cmp_nums(r, L):
    k = r.randint(2, 5 if L == 0 else 9)
    a = r.randint(2, 9) if L == 0 else r.randint(3, 12) if L == 1 else r.randint(6, 25)
    return k, a


@fam("012", mode="mc")
def cm_statement(r, L):
    k, a = cmp_nums(r, L)
    need(k != a)
    p = k * a
    good = f"{p} = {k} × {a}"
    return Item(f"Which equation shows that {p} is {k} times as many as {a}?", good, [f"“{k} times as many as {a}” means {k} × {a}.", f"{good}."],
                [W(f"{p} = {k} + {a}", "used addition for a times-as-many comparison"), W(f"{a} = {k} × {p}", "switched the larger and smaller amounts"), W(f"{k} = {p} × {a}", "put the numbers in the wrong positions")],
                FN("true_eq"), qtype="conceptual")


@fam("012", mode="mc")
def cm_interpret(r, L):
    k, a = cmp_nums(r, L)
    need(k != a)
    p = k * a
    good = f"{p} is {k} times as many as {a}"
    return Item(f"Which statement matches the equation {p} = {k} × {a}?", good, [f"The product {p} is {k} groups of {a}.", f"So {good}. It is also true that {p} is {a} times as many as {k}."],
                [W(f"{p} is {k} more than {a}", "read the equation as addition"), W(f"{a} is {k} times as many as {p}", "switched the larger and smaller amounts"), W(f"{k} is {p} times as many as {a}", "put the numbers in the wrong positions")],
                FN("times_statement"), qtype="conceptual", tags={"reasoning"})


@fam("012")
def cm_times_as_many(r, L):
    k, a = cmp_nums(r, L)
    n1, n2 = r.sample(NAMES, 2)
    thing, verb = pick(r, PAIRS)
    return Item(f"{n1} {verb} {a} {thing}. {n2} {verb} {k} times as many {thing} as {n1}. How many {thing} does {n2} have?".replace(f"does {n2} have", {"has": f"does {n2} have", "found": f"did {n2} find", "read": f"did {n2} read", "swam": f"did {n2} swim", "scored": f"did {n2} score", "used": f"did {n2} use"}[verb]),
                f"{k * a} {thing}", [f"“{k} times as many” means multiply by {k}.", f"{k} × {a} = {k * a} {thing}."],
                [W(f"{k + a} {thing}", "added instead of multiplying"), W(f"{k * a + a} {thing}", "added the first amount again"), W(f"{abs(k * a - k)} {thing}" if k * a - k != k + a else f"{k * a + 1} {thing}", "made a multiplication fact mistake"), W(f"{a} {thing}", "gave the first amount")],
                EX(f"{k} × {a}", unit=thing), qtype="word-problem")


@fam("012")
def cm_find_smaller(r, L):
    k, a = cmp_nums(r, L)
    n1, n2 = r.sample(NAMES, 2)
    thing, verb = pick(r, PAIRS[:3])
    p = k * a
    return Item(f"{n2} has {p} {thing}. That is {k} times as many as {n1} has. How many {thing} does {n1} have?", f"{a} {thing}",
                [f"{k} × (the smaller amount) = {p}, so divide.", f"{p} ÷ {k} = {a} {thing}."],
                [W(f"{p * k} {thing}", "multiplied instead of dividing"), W(f"{p - k} {thing}", "subtracted instead of dividing"), W(f"{p + k} {thing}", "added instead of dividing")],
                EX(f"{p} ÷ {k}", unit=thing), qtype="word-problem", tags={"reasoning"})


@fam("012")
def cm_how_many_times(r, L):
    k, a = cmp_nums(r, L)
    need(k != a)
    p = k * a
    t = pick(r, [f"A blue ribbon is {a} feet long. A red ribbon is {p} feet long. The red ribbon is how many times as long as the blue ribbon?",
                 f"A puppy weighs {a} pounds. Its mother weighs {p} pounds. The mother weighs how many times as much as the puppy?",
                 f"A small jar holds {a} ounces. A large jar holds {p} ounces. The large jar holds how many times as much as the small jar?"])
    return Item(t, str(k), [f"Ask: {a} times what number equals {p}?", f"{p} ÷ {a} = {k}, so it is {k} times as much."],
                [W(str(p - a), "subtracted to compare (that tells how many more, not how many times)"), W(str(p * a), "multiplied the two amounts"), W(str(a), "gave one of the amounts"), W(str(k + 1), "made a division fact mistake")],
                EX(f"{p} ÷ {a}"), qtype="word-problem", tags={"reasoning"})


@fam("012")
def cm_tape(r, L):
    k, a = cmp_nums(r, L)
    alt = f"A tape diagram with {k} equal parts. Each part is labeled {a}. The whole bar is labeled with a question mark."
    return Item(f"The bar is made of {k} equal parts. Each part stands for {a}. What number does the whole bar stand for?", str(k * a),
                [f"The whole bar is {k} times as much as one part.", f"{k} × {a} = {k * a}."],
                [W(str(k + a), "added the number of parts and the size of a part"), W(str(a), "gave the size of one part"), W(str(k * a - a), "left out one part"), W(str(k * a + a), "counted one part too many")],
                EX(f"{k} × {a}"), qtype="visual", diagram=Diagram("tape", {"parts": k, "each": str(a), "total_label": "?"}, alt), tags={"modeling"})


@fam("12")
def cm_vs_additive(r, L):
    k, a = cmp_nums(r, L)
    need(k * a != a + k)
    n1, n2, n3 = r.sample(NAMES, 3)
    v = k * a - (a + k)
    return Item(f"{n1} has {a} marbles. {n2} has {k} times as many marbles as {n1}. {n3} has {k} more marbles than {n1}. How many more marbles does {n2} have than {n3}?", f"{v} marbles",
                [f"{n2}: {k} × {a} = {k * a} marbles.", f"{n3}: {a} + {k} = {a + k} marbles.", f"{k * a} − {a + k} = {v} marbles."],
                [W("0 marbles", "treated “times as many” and “more than” as the same thing"), W(f"{k * a} marbles", f"found only the amount for {n2}"), W(f"{k * a - a} marbles", f"compared {n2} with {n1}"), W(f"{k * a + a + k} marbles", "added instead of comparing")],
                EX(f"{k} × {a} − ({a} + {k})", unit="marbles"), qtype="multi-step", tags={"multistep", "reasoning"})


# ============================================================== S2 Multiples of 10, 100, 1,000
def zero_wrongs(v):
    return [W(comma(v * 10), "wrote one zero too many"), W(comma(v // 10), "left out a zero")]


@fam("012")
def mt_basic(r, L):
    a, d = r.randint(2, 9), r.randint(2, 9)
    e = r.randint(1, 2 if L == 0 else 3)
    b = d * 10 ** e
    v = a * b
    return Item(f"Multiply: {a} × {comma(b)}", comma(v), [f"Use the basic fact {a} × {d} = {a * d}.", f"{a} × {d} {PLACE_NAMES[e]} = {a * d} {PLACE_NAMES[e]} = {comma(v)}."],
                zero_wrongs(v) + [W(comma((a + d) * 10 ** e), "added the digits instead of multiplying"), W(comma((a * d + a) * 10 ** e), "made a multiplication fact mistake")],
                EX(f"{a} × {b}"), claim=f"{a} × {comma(b)}")


@fam("12")
def mt_two_multiples(r, L):
    a, d = r.randint(2, 9), r.randint(2, 9)
    e1, e2 = 1, r.randint(1, L)
    x, y = a * 10 ** e1, d * 10 ** e2
    v = x * y
    return Item(f"Multiply: {x} × {comma(y)}", comma(v), [f"Multiply the basic fact: {a} × {d} = {a * d}.", f"{x} × {comma(y)} = {a * d} × {comma(10 ** (e1 + e2))} = {comma(v)}."],
                zero_wrongs(v) + [W(comma(a * d), "left out all the zeros"), W(comma((a + d) * 10 ** (e1 + e2)), "added the digits instead of multiplying")], EX(f"{x} × {y}"), claim=f"{x} × {comma(y)}")


@fam("012")
def mt_missing(r, L):
    a, d = r.randint(2, 9), r.randint(2, 9)
    e = r.randint(1, 2 if L == 0 else 3)
    b = d * 10 ** e
    v = a * b
    return Item(f"Find the missing factor: {a} × ___ = {comma(v)}", comma(b), [f"Think: {a} × {d} = {a * d}.", f"{a} × {comma(b)} = {comma(v)}, so the missing factor is {comma(b)}."],
                [W(comma(b * 10), "wrote one zero too many"), W(comma(b // 10), "left out a zero"), W(str(d), "gave only the basic fact"), W(comma(v - a), "subtracted instead of dividing")],
                EX(f"{v} ÷ {a}"), qtype="fill-blank")


@fam("012")
def mt_unit_form(r, L):
    a, d = r.randint(2, 9), r.randint(2, 9)
    e = r.randint(1, 2 if L == 0 else 3)
    unit = PLACE_NAMES[e]
    return Item(f"Fill in the blank: {a} × {d} {unit} = ___ {unit}", str(a * d), [f"{a} groups of {d} {unit} is {a} × {d} = {a * d} {unit}.", f"That is {comma(a * d * 10 ** e)}."],
                [W(comma(a * d * 10 ** e), "wrote the standard form instead of the number of " + unit), W(str(a + d), "added instead of multiplying"), W(str(a * d * 10), "wrote an extra zero"), W(str(a * d + a), "made a multiplication fact mistake")],
                EX(f"{a} × {d}"), qtype="conceptual", tags={"multiple-representations"})


@fam("012")
def mt_word(r, L):
    one, many, thing = pick(r, PACK)
    a, d = r.randint(3, 9), r.randint(2, 9)
    e = r.randint(1, 2 if L < 2 else 3)
    b = d * 10 ** e
    return Item(f"Each {one} holds {comma(b)} {thing}. How many {thing} are in {a} {many}?", f"{comma(a * b)} {thing}", [f"{a} × {comma(b)}: use {a} × {d} = {a * d}.", f"{a} × {comma(b)} = {comma(a * b)} {thing}."],
                [W(f"{comma(a * b * 10)} {thing}", "wrote one zero too many"), W(f"{comma(a * b // 10)} {thing}", "left out a zero"), W(f"{comma(a + b)} {thing}", "added instead of multiplying"), W(f"{comma(b)} {thing}", "gave the amount in one group")],
                EX(f"{a} × {b}", unit=thing), qtype="word-problem")


@fam("012")
def mt_fact(r, L):
    a, b = r.randint(6, 12), r.randint(6 if L else 3, 12)
    if r.random() < 0.5:
        return Item(f"Multiply: {a} × {b}", str(a * b), [f"{a} × {b} = {a * b}."],
                    [W(str(a * b + a), "counted one group too many"), W(str(a * b - b), "counted one group too few"), W(str(a + b), "added instead of multiplying"), W(str(a * b + 10), "made a fact mistake")], EX(f"{a} × {b}"), claim=f"{a} × {b}")
    return Item(f"Find the missing factor: ___ × {b} = {a * b}", str(a), [f"Think: what number times {b} equals {a * b}?", f"{a} × {b} = {a * b}."],
                [W(str(a + 1), "was off by one group"), W(str(a - 1), "was off by one group"), W(str(a * b - b), "subtracted instead of dividing")], EX(f"{a * b} ÷ {b}"), qtype="fill-blank")


@fam("012", mode="mc")
def mt_same_value(r, L):
    a, d = r.randint(2, 9), r.randint(2, 9)
    e = r.randint(2, 2 + (L > 0))
    b = d * 10 ** e
    good = f"{a} × {d} × {comma(10 ** e)}"
    return Item(f"Which expression has the same value as {a} × {comma(b)}?", good, [f"{comma(b)} = {d} × {comma(10 ** e)}.", f"So {a} × {comma(b)} = {good} = {comma(a * b)}."],
                [W(f"{a} × {d} × {comma(10 ** (e - 1))}", "used a place value that is too small"), W(f"{a} + {d} × {comma(10 ** e)}", "added the first factor instead of multiplying"), W(f"{a}{d} × {comma(10 ** e)}", "wrote the digits side by side instead of multiplying them")],
                FN("expr_eq", e=f"{a} × {b}"), qtype="conceptual", tags={"reasoning", "connections"})


# ============================================================== S3 Multiplying by One-Digit Numbers
def one_digit_case(r, L):
    b = r.randint(2, 9)
    n = r.randint(12, 99) if L == 0 and r.random() < 0.4 else r.randint(101, 999) if L < 2 or r.random() < 0.3 else r.randint(1001, 9999)
    need(n % 10 and len(expand(n)) >= 2)
    return b, n


def m1_wrongs(b, n, unit=""):
    u = (" " + unit) if unit else ""
    v = b * n
    nc = int("".join(str(int(c) * b % 10) for c in str(n)))
    ex = expand(n)
    return [W(comma(nc) + u if nc != v else comma(v + 10) + u, "forgot to add the regrouped digits"), W(comma(b * ex[0] + ex[-1]) + u if len(ex) > 1 else comma(v + b) + u, "multiplied only the first part by the one-digit number"),
            W(comma(v + 10 * b) + u, "made a regrouping mistake"), W(comma(v - b) + u, "made a multiplication fact mistake"), W(comma(v + 100) + u, "regrouped an extra hundred")]


@fam("012")
def m1_basic(r, L):
    b, n = one_digit_case(r, L)
    ex = expand(n)
    return Item(f"Multiply: {b} × {comma(n)}", comma(b * n), ["Break the larger number into parts: " + " + ".join(comma(x) for x in ex) + ".", "Partial products: " + ", ".join(f"{b} × {comma(x)} = {comma(b * x)}" for x in ex) + ".", f"Add them: {comma(b * n)}."],
                m1_wrongs(b, n), EX(f"{b} × {n}"), claim=f"{b} × {comma(n)}")


@fam("012")
def m1_area(r, L):
    b, n = one_digit_case(r, L)
    ex = expand(n)
    i = r.randrange(len(ex))
    cells = [[("?" if j == i else comma(b * x)) for j, x in enumerate(ex)]]
    alt = f"An area model for {b} × {comma(n)}. The side is {b}. The top is split into " + ", ".join(comma(x) for x in ex) + ". The boxes show " + ", ".join(cells[0]) + "."
    return Item(f"The area model shows {b} × {comma(n)}. What number belongs in the box with the question mark?", comma(b * ex[i]),
                [f"The box is {b} × {comma(ex[i])}.", f"{b} × {comma(ex[i])} = {comma(b * ex[i])}."],
                [W(comma(b * ex[i] * 10), "wrote one zero too many"), W(comma(b * ex[i] // 10) if ex[i] >= 10 else comma(b + ex[i]), "left out a zero"), W(comma(b + ex[i]), "added instead of multiplying"), W(comma(b * n), "gave the whole product")],
                EX(f"{b} × {ex[i]}"), qtype="visual", diagram=Diagram("area_model", {"rows": [str(b)], "cols": [comma(x) for x in ex], "cells": cells}, alt), tags={"modeling"})


@fam("012", mode="mc")
def m1_partial_choice(r, L):
    b, n = one_digit_case(r, L)
    ex = expand(n)
    need(len(ex) >= 2 and all(x >= 10 for x in ex[:-1]))
    good = " + ".join(f"{b} × {comma(x)}" for x in ex)
    b1 = " + ".join(f"{b} × {str(x)[0]}" for x in ex)
    b2 = " + ".join([f"{b} × {comma(ex[0])}"] + [comma(x) for x in ex[1:]])
    b3 = " + ".join(f"{b} + {comma(x)}" for x in ex)
    return Item(f"Which expression shows a correct way to find {b} × {comma(n)} with partial products?", good, [f"Break {comma(n)} into " + " + ".join(comma(x) for x in ex) + f" and multiply each part by {b}.", f"{good} = {comma(b * n)}."],
                [W(b1, "used the digits instead of their place values"), W(b2, "multiplied only the first part"), W(b3, "added instead of multiplying")],
                FN("expr_eq", e=f"{b} × {n}"), qtype="compare-strategies", tags={"reasoning"})


@fam("012")
def m1_missing_partial(r, L):
    b, n = one_digit_case(r, L)
    ex = expand(n)
    need(len(ex) >= 3 or L == 0)
    i = r.randrange(len(ex))
    shown = " + ".join("___" if j == i else comma(b * x) for j, x in enumerate(ex))
    rest = " − ".join(str(b * x) for j, x in enumerate(ex) if j != i)
    v = b * ex[i]
    return Item(f"Fill in the missing partial product: {b} × {comma(n)} = {shown}", comma(v), [f"The missing part is {b} × {comma(ex[i])}.", f"{b} × {comma(ex[i])} = {comma(v)}."],
                [W(comma(v * 10), "wrote one zero too many"), W(str(b * int(str(ex[i])[0])) if ex[i] >= 10 else str(v + b), "used the digit instead of its place value"), W(comma(ex[i]), "did not multiply")],
                FN("partial_missing", b=str(b), n=str(n), index=i), qtype="fill-blank")


@fam("012")
def m1_word(r, L):
    b, n = one_digit_case(r, L)
    t = pick(r, [(f"A plane ticket costs ${comma(n)}. What is the cost of {b} tickets?", "$", ""), (f"A factory makes {comma(n)} toys each day. How many toys does it make in {b} days?", "", "toys"),
                 (f"A printer uses {comma(n)} sheets of paper each week. How many sheets does it use in {b} weeks?", "", "sheets"), (f"A stadium section has {comma(n)} seats. How many seats are in {b} sections?", "", "seats")])
    v = b * n
    fmt = lambda x: f"${comma(x)}" if t[1] else f"{comma(x)} {t[2]}"
    return Item(t[0], fmt(v), [f"Multiply {b} × {comma(n)} with partial products.", f"{b} × {comma(n)} = {fmt(v)}."],
                [W(fmt(b + n), "added instead of multiplying"), W(fmt(v + 10 * b), "made a regrouping mistake"), W(fmt(v - b), "made a multiplication fact mistake"), W(fmt(v + 100), "regrouped an extra hundred")],
                EX(f"{b} × {n}", unit=t[2] or None), qtype="word-problem")


@fam("012")
def m1_distributive(r, L):
    b = r.randint(3, 9)
    n = r.randint(13, 99)
    need(n % 10)
    t, o = n // 10 * 10, n % 10
    return Item(f"Fill in the blank: {b} × {n} = ({b} × {t}) + ({b} × ___)", str(o), [f"{n} = {t} + {o}.", f"So {b} × {n} = ({b} × {t}) + ({b} × {o})."],
                [W(str(n), "used the whole number again"), W(str(t), "repeated the tens part"), W(str(b * o), "wrote the partial product instead of the missing factor"), W(str(o + 1), "broke the number apart incorrectly")],
                EX(f"{n} − {t}"), qtype="conceptual", tags={"reasoning"})


# ============================================================== S4 Multiplying Two-Digit Numbers
def two_case(r, L):
    a = r.randint(11, 29 if L == 0 else 99)
    b = r.randint(11, 39 if L == 0 else 99)
    need(a % 10 and b % 10)
    return a, b


def m2_wrongs(a, b, unit=""):
    u = (" " + unit) if unit else ""
    v = a * b
    a1, a0, b1, b0 = a // 10 * 10, a % 10, b // 10 * 10, b % 10
    return [W(comma(a * b0 + a * (b // 10)) + u, "forgot the zero when multiplying by the tens digit"), W(comma(a1 * b1 + a0 * b0) + u, "multiplied only tens by tens and ones by ones"),
            W(comma(v + 100) + u, "made a regrouping mistake"), W(comma(v - 10) + u, "made an addition mistake with the partial products")]


@fam("012")
def m2_basic(r, L):
    a, b = two_case(r, L)
    a1, a0, b1, b0 = a // 10 * 10, a % 10, b // 10 * 10, b % 10
    return Item(f"Multiply: {a} × {b}", comma(a * b), [f"Partial products: {a1} × {b1} = {comma(a1 * b1)}, {a1} × {b0} = {a1 * b0}, {a0} × {b1} = {a0 * b1}, {a0} × {b0} = {a0 * b0}.", f"Add them: {comma(a * b)}."],
                m2_wrongs(a, b), EX(f"{a} × {b}"), claim=f"{a} × {b}")


def area2(a, b, hide=None):
    a1, a0, b1, b0 = a // 10 * 10, a % 10, b // 10 * 10, b % 10
    cells = [[comma(a1 * b1), str(a1 * b0)], [str(a0 * b1), str(a0 * b0)]]
    if hide is not None:
        cells[hide[0]][hide[1]] = "?"
    alt = f"An area model for {a} × {b}. The side is split into {a1} and {a0}. The top is split into {b1} and {b0}. The four boxes show {cells[0][0]}, {cells[0][1]}, {cells[1][0]} and {cells[1][1]}."
    return Diagram("area_model", {"rows": [str(a1), str(a0)], "cols": [str(b1), str(b0)], "cells": cells}, alt)


@fam("012")
def m2_area_box(r, L):
    a, b = two_case(r, L)
    i, j = r.randrange(2), r.randrange(2)
    x, y = [a // 10 * 10, a % 10][i], [b // 10 * 10, b % 10][j]
    return Item(f"The area model shows {a} × {b}. What number belongs in the box with the question mark?", comma(x * y), [f"The box is {x} × {y}.", f"{x} × {y} = {comma(x * y)}."],
                [W(comma(x * y * 10), "wrote one zero too many"), W(comma(x * y // 10) if x * y % 10 == 0 else comma(x + y), "left out a zero"), W(comma(x + y), "added instead of multiplying"), W(comma(a * b), "gave the whole product")],
                EX(f"{x} × {y}"), qtype="visual", diagram=area2(a, b, (i, j)), tags={"modeling"})


@fam("012")
def m2_area_total(r, L):
    a, b = two_case(r, L)
    a1, a0, b1, b0 = a // 10 * 10, a % 10, b // 10 * 10, b % 10
    return Item(f"The area model shows the four partial products for {a} × {b}. What is {a} × {b}?", comma(a * b),
                [f"Add the partial products: {comma(a1 * b1)} + {a1 * b0} + {a0 * b1} + {a0 * b0}.", f"The sum is {comma(a * b)}."],
                m2_wrongs(a, b), EX(f"{a1 * b1} + {a1 * b0} + {a0 * b1} + {a0 * b0}"), qtype="visual", diagram=area2(a, b), tags={"modeling"})


@fam("012")
def m2_by_tens(r, L):
    a = r.randint(12, 99)
    b = r.randint(2, 9) * 10
    need(a % 10)
    return Item(f"Multiply: {a} × {b}", comma(a * b), [f"{a} × {b // 10} = {a * (b // 10)}.", f"{a} × {b} is 10 times as much: {comma(a * b)}."],
                [W(comma(a * (b // 10)), "forgot the zero for the tens"), W(comma(a * b * 10), "wrote one zero too many"), W(comma(a * b + b), "made a multiplication fact mistake"), W(comma(a + b), "added instead of multiplying")],
                EX(f"{a} × {b}"), claim=f"{a} × {b}")


@fam("012")
def m2_word(r, L):
    a, b = two_case(r, L)
    one, many, thing = pick(r, PACK)
    return Item(f"There are {a} {many}. Each {one} holds {b} {thing}. How many {thing} are there in all?", f"{comma(a * b)} {thing}",
                [f"Multiply {a} × {b}.", f"{a} × {b} = {comma(a * b)} {thing}."], m2_wrongs(a, b, thing)[:3] + [W(f"{a + b} {thing}", "added instead of multiplying")], EX(f"{a} × {b}", unit=thing), qtype="word-problem")


@fam("012")
def m2_missing_partial(r, L):
    a, b = two_case(r, L)
    a1, a0, b1, b0 = a // 10 * 10, a % 10, b // 10 * 10, b % 10
    parts = [(a1, b1), (a1, b0), (a0, b1), (a0, b0)]
    i = r.randrange(4)
    shown = " + ".join("___" if j == i else comma(x * y) for j, (x, y) in enumerate(parts))
    x, y = parts[i]
    return Item(f"{a} × {b} = ({a1} + {a0}) × ({b1} + {b0}). Fill in the missing partial product: {a} × {b} = {shown}", comma(x * y), [f"The missing partial product is {x} × {y}.", f"{x} × {y} = {comma(x * y)}."],
                [W(comma(x * y * 10), "wrote one zero too many"), W(comma(x + y), "added instead of multiplying"), W(str(int(str(x)[0]) * int(str(y)[0])) if x * y >= 10 and int(str(x)[0]) * int(str(y)[0]) != x * y else comma(x * y + 10), "used the digits instead of their place values")],
                EX(f"{x} × {y}"), qtype="fill-blank", tags={"reasoning"})


# ============================================================== S5 Estimating Products and Multiplication Word Problems
@fam("012")
def ep_estimate1(r, L):
    b, n = one_digit_case(r, L)
    e = len(str(n)) - 1
    rn = rnd_to(n, e)
    return Item(f"Estimate {b} × {comma(n)} by rounding {comma(n)} to the nearest {sg(PLACE_NAMES[e])}.", comma(b * rn), [f"{comma(n)} rounds to {comma(rn)}.", f"{b} × {comma(rn)} = {comma(b * rn)}."],
                [W(comma(b * n), "found the exact product instead of an estimate"), W(comma(b * (rn + 10 ** e if rn < n else rn - 10 ** e)), "rounded the wrong way"), W(comma(b * rn * 10), "wrote one zero too many"), W(comma(b + rn), "added instead of multiplying")],
                FN("est_prod", a=str(b), b=str(n), place=PLACE_NAMES[e]), qtype="procedural")


@fam("012")
def ep_estimate2(r, L):
    a, b = two_case(r, 1)
    ra, rb = rnd_to(a, 1), rnd_to(b, 1)
    return Item(f"Estimate {a} × {b} by rounding each factor to the nearest ten.", comma(ra * rb), [f"{a} rounds to {ra} and {b} rounds to {rb}.", f"{ra} × {rb} = {comma(ra * rb)}."],
                [W(comma(a * b), "found the exact product instead of an estimate"), W(comma(ra * rb // 10), "left out a zero"), W(comma(ra + rb), "added instead of multiplying"), W(comma((ra + 10) * rb), "rounded one factor the wrong way")],
                FN("est_prod", a=str(a), b=str(b), place="tens", place_a="tens"), qtype="procedural")


@fam("012", mode="mc")
def ep_reasonable(r, L):
    b, n = one_digit_case(r, max(L, 1))
    e = len(str(n)) - 1
    rn = rnd_to(n, e)
    exact, est = b * n, b * rn
    wrong = pick(r, [exact * 10, exact + 10 ** (e + 1) * 2, exact // 10])
    need(abs(wrong - exact) > 10 ** e * b)
    nm = name(r)
    good = f"No. An estimate is {b} × {comma(rn)} = {comma(est)}, which is not close to {comma(wrong)}."
    return Item(f"{nm} says that {b} × {comma(n)} = {comma(wrong)}. Use estimation to decide: is the answer reasonable?", good,
                [f"Round {comma(n)} to {comma(rn)}: {b} × {comma(rn)} = {comma(est)}.", f"{comma(wrong)} is not close to {comma(est)}, so the answer is not reasonable."],
                [W(f"Yes. An estimate is {b} × {comma(rn)} = {comma(est)}, which is close to {comma(wrong)}.", "did not compare the estimate with the answer"),
                 W("Yes. The product of two whole numbers is always greater than both factors.", "used a rule that does not check the size of the answer"), W(f"No. A product can never have {len(str(wrong))} digits.", "used a rule that is not true")],
                FN("est_judge", a=str(b), b=str(n), op="×", place=PLACE_NAMES[e], claimed=str(wrong), keep_a=True), qtype="explain", tags={"reasoning"})


@fam("012")
def ep_two_step(r, L):
    one, many, thing = pick(r, PACK)
    a = r.randint(3, 9) if L == 0 else r.randint(12, 48)
    b = r.randint(12, 48) if L < 2 else r.randint(24, 96)
    c = r.randint(5, 40)
    if r.random() < 0.5:
        return Item(f"A store has {a} full {many} with {b} {thing} in each {one}. There are also {c} loose {thing}. How many {thing} does the store have?", f"{comma(a * b + c)} {thing}",
                    [f"Full {many}: {a} × {b} = {comma(a * b)}.", f"Add the loose ones: {comma(a * b)} + {c} = {comma(a * b + c)} {thing}."],
                    [W(f"{comma(a * b)} {thing}", "forgot to add the loose ones"), W(f"{comma(a * (b + c))} {thing}", "added before multiplying"), W(f"{a + b + c} {thing}", "added all the numbers"), W(f"{comma(a * b - c)} {thing}", "subtracted instead of adding")],
                    EX(f"{a} × {b} + {c}", unit=thing), qtype="multi-step", tags={"multistep"})
    need(a * b > c + 10)
    return Item(f"A shop received {a} {many} with {b} {thing} in each {one}. It sold {c} {thing}. How many {thing} are left?", f"{comma(a * b - c)} {thing}",
                [f"Received: {a} × {b} = {comma(a * b)}.", f"Subtract the ones sold: {comma(a * b)} − {c} = {comma(a * b - c)} {thing}."],
                [W(f"{comma(a * b)} {thing}", "forgot to subtract the ones sold"), W(f"{comma(a * abs(b - c))} {thing}" if b != c else f"{comma(a * b + 1)} {thing}", "subtracted before multiplying"), W(f"{comma(a * b + c)} {thing}", "added instead of subtracting")],
                EX(f"{a} × {b} − {c}", unit=thing), qtype="multi-step", tags={"multistep"})


@fam("012", mode="mc")
def ep_equation(r, L):
    a = r.randint(3, 9)
    b = r.randint(12, 60) if L else r.randint(11, 25)
    c = r.randint(5, 30)
    nm = name(r)
    v = a * b + c
    good = f"n = {a} × {b} + {c}"
    return Item(f"{nm} buys {a} packs of trading cards with {b} cards in each pack. A friend gives {nm} {c} more cards. Let n be the total number of cards. Which equation matches the story?", good,
                [f"{a} packs of {b} is {a} × {b}. Then add {c}.", f"{good}, so n = {comma(v)}."],
                [W(f"n = {a} + {b} + {c}", "added the packs instead of multiplying"), W(f"n = {a} × {b} − {c}", "subtracted the extra cards"), W(f"n = {a} × ({b} + {c})", "added the extra cards to every pack")],
                FN("eq_with", n=str(v)), qtype="conceptual", tags={"modeling"})


@fam("012")
def ep_compare_products(r, L):
    a, b = two_case(r, L)
    c = r.randint(3, 9)
    d = r.randint(101, 499)
    need(a * b != c * d)
    v = abs(a * b - c * d)
    big = "A" if a * b > c * d else "B"
    return Item(f"Theater A has {a} rows with {b} seats in each row. Theater B has {c} sections with {d} seats in each section. How many more seats does the larger theater have?", f"{comma(v)} seats",
                [f"Theater A: {a} × {b} = {comma(a * b)} seats. Theater B: {c} × {d} = {comma(c * d)} seats.", f"Theater {big} is larger. The difference is {comma(v)} seats."],
                [W(f"{comma(a * b + c * d)} seats", "added the two totals"), W(f"{comma(max(a * b, c * d))} seats", "gave the size of the larger theater"), W(f"{comma(v + 100)} seats", "made a subtraction mistake"), W(f"{comma(min(a * b, c * d))} seats", "gave the size of the smaller theater")],
                FN("abs_diff", a=f"{a} × {b}", b=f"{c} × {d}", unit="seats"), qtype="multi-step", tags={"multistep", "challenge"} if L == 2 else {"multistep"})


SKILLS = {
    1: dict(name="Multiplicative Comparisons", fams=[cm_statement, cm_interpret, cm_times_as_many, cm_find_smaller, cm_how_many_times, cm_tape, cm_vs_additive]),
    2: dict(name="Multiplying by Multiples of 10, 100, and 1,000", fams=[mt_basic, mt_two_multiples, mt_missing, mt_unit_form, mt_word, mt_fact, mt_same_value]),
    3: dict(name="Multiplying by One-Digit Numbers", fams=[m1_basic, m1_area, m1_partial_choice, m1_missing_partial, m1_word, m1_distributive]),
    4: dict(name="Multiplying Two-Digit Numbers", fams=[m2_basic, m2_area_box, m2_area_total, m2_by_tens, m2_word, m2_missing_partial]),
    5: dict(name="Estimating Products and Multiplication Word Problems", fams=[ep_estimate1, ep_estimate2, ep_reasonable, ep_two_step, ep_equation, ep_compare_products]),
}
