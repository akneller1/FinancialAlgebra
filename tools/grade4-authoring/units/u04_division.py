"""Unit 4: Division and Remainders (4.NBT.B.6, 4.OA.A.2-3)."""
from g4lib import *

UNIT_ID = "division-remainders"
SHARE = [("stickers", "friends"), ("pencils", "tables"), ("muffins", "boxes"), ("marbles", "bags"), ("books", "shelves"), ("seeds", "pots"), ("cards", "players"), ("beads", "bracelets")]


def div_case(r, L, rem=False):
    b = r.randint(2, 9)
    if L == 0:
        q = r.randint(11, 99)
    elif L == 1:
        q = r.randint(21, 450)
    else:
        q = r.randint(102, 1100)
    rr = r.randint(1, b - 1) if rem else 0
    a = b * q + rr
    need(a <= 9999)
    return a, b, q, rr


def div_wrongs(a, b, q, unit=""):
    u = (" " + unit) if unit else ""
    s = str(q)
    out = []
    if "0" in s[1:]:
        out.append(W(comma(int(s[0] + s[1:].replace("0", "", 1))) + u, "left out the zero in the quotient"))
    out += [W(comma(q + 10) + u, "made a mistake with the tens"), W(comma(q - 1) + u, "made a multiplication fact mistake"), W(comma(q * 10) + u, "wrote one digit too many"), W(comma(q + 1) + u, "made a multiplication fact mistake"),
            W(comma(a - b) + u, "subtracted instead of dividing")]
    return out


# ============================================================== S1 Division Facts and Patterns
@fam("012")
def df_fact(r, L):
    b, q = r.randint(3, 12 if L else 9), r.randint(3, 12)
    a = b * q
    k = r.randrange(3)
    if k == 0:
        return Item(f"Divide: {a} ÷ {b}", str(q), [f"Think: {b} × what number = {a}?", f"{b} × {q} = {a}, so {a} ÷ {b} = {q}."],
                    [W(str(q + 1), "was off by one group"), W(str(q - 1), "was off by one group"), W(str(a - b), "subtracted instead of dividing"), W(str(b), "gave the divisor")], EX(f"{a} ÷ {b}"), claim=f"{a} ÷ {b}")
    if k == 1:
        return Item(f"Find the missing number: ___ ÷ {b} = {q}", str(a), ["Multiply the quotient by the divisor.", f"{q} × {b} = {a}."],
                    [W(str(q + b), "added instead of multiplying"), W(str(a + b), "counted one group too many"), W(str(a - q), "counted one group too few")], EX(f"{q} × {b}"), qtype="fill-blank")
    need(b != q)
    return Item(f"Find the missing number: {a} ÷ ___ = {q}", str(b), [f"Think: {q} × what number = {a}?", f"{q} × {b} = {a}."],
                [W(str(b + 1), "was off by one group"), W(str(a - q), "subtracted instead of dividing"), W(str(q), "repeated the quotient")], EX(f"{a} ÷ {q}"), qtype="fill-blank")


@fam("012")
def df_multiples(r, L):
    b, d = r.randint(2, 9), r.randint(2, 9)
    e = r.randint(1, 2 if L < 2 else 2)
    a = b * d * 10 ** e
    need(a <= 9999)
    q = d * 10 ** e
    return Item(f"Divide: {comma(a)} ÷ {b}", comma(q), [f"Use the basic fact {b * d} ÷ {b} = {d}.", f"{b * d} {PLACE_NAMES[e]} ÷ {b} = {d} {PLACE_NAMES[e]} = {comma(q)}."],
                [W(comma(q * 10), "wrote one zero too many"), W(comma(q // 10), "left out a zero"), W(comma((d + 1) * 10 ** e), "made a division fact mistake"), W(comma(a - b), "subtracted instead of dividing")],
                EX(f"{a} ÷ {b}"), claim=f"{comma(a)} ÷ {b}")


@fam("012", mode="mc")
def df_related(r, L):
    b, q = r.randint(3, 12 if L else 9), r.randint(3, 12)
    need(b != q)
    a = b * q
    good = f"{b} × {q} = {a}"
    return Item(f"Which multiplication fact can help you solve {a} ÷ {b}?", good, ["Division and multiplication are related: divisor × quotient = dividend.", f"{good}, so {a} ÷ {b} = {q}."],
                [W(f"{b} × {q + 1} = {a}", "the fact is not true"), W(f"{b} + {q} = {a}", "used addition"), W(f"{a} × {b} = {q}", "multiplied the dividend and divisor")],
                FN("true_eq"), qtype="conceptual", tags={"connections"})


@fam("012")
def df_unit_form(r, L):
    b, d = r.randint(2, 9), r.randint(2, 9)
    e = r.randint(1, 2 if L < 2 else 3)
    unit = PLACE_NAMES[e]
    return Item(f"Fill in the blank: {b * d} {unit} ÷ {b} = ___ {unit}", str(d), [f"{b * d} ÷ {b} = {d}, so {b * d} {unit} ÷ {b} = {d} {unit}.", f"In standard form: {comma(b * d * 10 ** e)} ÷ {b} = {comma(d * 10 ** e)}."],
                [W(comma(d * 10 ** e), f"wrote the standard form instead of the number of {unit}"), W(str(d + 1), "made a division fact mistake"), W(str(b * d - b), "subtracted instead of dividing"), W(str(d * 10), "wrote an extra zero")],
                EX(f"{b * d} ÷ {b}"), qtype="conceptual", tags={"multiple-representations"})


@fam("012")
def df_pattern(r, L):
    b, d = r.randint(2, 9), r.randint(2, 9)
    e = r.randint(1, 2)
    a = b * d * 10 ** e
    return Item(f"You know that {b * d} ÷ {b} = {d}. Use this fact to find {comma(a)} ÷ {b}.", comma(d * 10 ** e), [f"{comma(a)} is {b * d} {PLACE_NAMES[e]}.", f"{b * d} {PLACE_NAMES[e]} ÷ {b} = {d} {PLACE_NAMES[e]} = {comma(d * 10 ** e)}."],
                [W(str(d), "did not use the place value"), W(comma(d * 10 ** (e + 1)), "wrote one zero too many"), W(comma(d * 10 ** (e - 1)) if e > 1 else comma(d + 10), "left out a zero"), W(comma(b * 10 ** e), "used the divisor")],
                EX(f"{a} ÷ {b}"), qtype="conceptual")


@fam("012")
def df_word(r, L):
    thing, group = pick(r, SHARE)
    b, q = r.randint(3, 12 if L else 9), r.randint(4, 12)
    if L == 2:
        q *= 10
    a = b * q
    nm = name(r)
    return Item(f"{nm} shares {comma(a)} {thing} equally among {b} {group}. How many {thing} does each of the {b} {group} get?", f"{q} {thing}", [f"Equal sharing means divide: {comma(a)} ÷ {b}.", f"{comma(a)} ÷ {b} = {q} {thing}."],
                [W(f"{comma(a - b)} {thing}", "subtracted instead of dividing"), W(f"{q + 1} {thing}", "made a division fact mistake"), W(f"{comma(a * b)} {thing}", "multiplied instead of dividing"), W(f"{b} {thing}", "gave the number of groups")],
                EX(f"{a} ÷ {b}", unit=thing), qtype="word-problem")


# ============================================================== S2 Models and Partial Quotients
def split_case(r, L):
    b = r.randint(3, 9)
    t = r.randint(1, 3 if L == 0 else 9) * 10 * (10 if L == 2 and r.random() < 0.5 else 1)
    o = r.randint(2, 9 if L == 0 else 12)
    need(b * (t + o) <= 9999)
    return b, t, o


@fam("012")
def dm_area_missing(r, L):
    b, t, o = split_case(r, L)
    a = b * (t + o)
    alt = f"An area model for {comma(a)} ÷ {b}. The side is {b}. The total area {comma(a)} is split into two boxes with areas {comma(b * t)} and {b * o}. The top of the first box is labeled {t}. The top of the second box is labeled with a question mark."
    return Item(f"The area model shows {comma(a)} ÷ {b}. The rectangle has a side of {b} and is split into areas of {comma(b * t)} and {b * o}. What is the missing length?", str(o),
                [f"The second box has area {b * o} and side {b}.", f"{b * o} ÷ {b} = {o}."],
                [W(str(b * o), "gave the area instead of the length"), W(str(t + o), "gave the whole quotient"), W(str(o + 1), "made a division fact mistake"), W(str(t), "repeated the other length")],
                EX(f"{b * o} ÷ {b}"), qtype="visual", diagram=Diagram("area_model", {"rows": [str(b)], "cols": [str(t), "?"], "cells": [[comma(b * t), str(b * o)]]}, alt), tags={"modeling"})


@fam("012")
def dm_area_quotient(r, L):
    b, t, o = split_case(r, L)
    a = b * (t + o)
    alt = f"An area model for {comma(a)} ÷ {b}. The side is {b}. The top is split into {t} and {o}. The boxes have areas {comma(b * t)} and {b * o}."
    return Item(f"The area model shows a way to divide {comma(a)} by {b}. The top lengths are {t} and {o}. What is {comma(a)} ÷ {b}?", comma(t + o),
                [f"The quotient is the total length across the top.", f"{t} + {o} = {t + o}, so {comma(a)} ÷ {b} = {t + o}."],
                [W(comma(b * t), "gave one of the areas"), W(str(t), "used only the first part"), W(comma(t * o), "multiplied the two lengths"), W(comma(a), "gave the dividend")],
                EX(f"{t} + {o}"), qtype="visual", diagram=Diagram("area_model", {"rows": [str(b)], "cols": [str(t), str(o)], "cells": [[comma(b * t), str(b * o)]]}, alt), tags={"modeling"})


@fam("012", mode="mc")
def dm_break_apart(r, L):
    b, t, o = split_case(r, L)
    a = b * (t + o)
    x, y = b * t, b * o
    good = f"({comma(x)} ÷ {b}) + ({y} ÷ {b})"
    return Item(f"Which expression shows a correct way to break apart {comma(a)} ÷ {b}?", good, [f"Break {comma(a)} into {comma(x)} + {y}. Both parts are easy to divide by {b}.", f"{good} = {t} + {o} = {t + o}."],
                [W(f"({comma(x)} ÷ {b}) + {y}", "divided only the first part"), W(f"({comma(x)} ÷ {b}) × ({y} ÷ {b})", "multiplied the two partial quotients"), W(f"({comma(x)} ÷ {b}) − ({y} ÷ {b})", "subtracted the partial quotients")],
                FN("expr_eq", e=f"{a} ÷ {b}"), qtype="compare-strategies", tags={"reasoning"})


@fam("012")
def dm_partial_sum(r, L):
    b, t, o = split_case(r, L)
    a = b * (t + o)
    nm = name(r)
    return Item(f"{nm} uses partial quotients to find {comma(a)} ÷ {b}. First {nm} subtracts {comma(b * t)}, which is {t} groups of {b}. Then {nm} subtracts {b * o}, which is {o} groups of {b}. Nothing is left. What is the quotient?", comma(t + o),
                ["Add the partial quotients.", f"{t} + {o} = {t + o}."],
                [W(comma(b * t + b * o), "added the amounts subtracted instead of the numbers of groups"), W(str(t), "used only the first partial quotient"), W(comma(t * o), "multiplied the partial quotients"), W(str(t + o + 1), "counted an extra group")],
                EX(f"{t} + {o}"), qtype="conceptual", tags={"reasoning"})


@fam("012")
def dm_partial_missing(r, L):
    b, t, o = split_case(r, L)
    a = b * (t + o)
    return Item(f"Partial quotients for {comma(a)} ÷ {b}: {b} × {t} = {comma(b * t)}, and {comma(a)} − {comma(b * t)} = {b * o}. Then {b} × ___ = {b * o}. What number goes in the blank?", str(o),
                [f"{b * o} ÷ {b} = {o}.", f"The quotient is {t} + {o} = {t + o}."],
                [W(str(b * o), "wrote the amount left instead of the number of groups"), W(str(t + o), "gave the whole quotient"), W(str(o + 1), "made a division fact mistake"), W(str(o - 1), "made a division fact mistake")],
                EX(f"{b * o} ÷ {b}"), qtype="fill-blank")


@fam("012")
def dm_array(r, L):
    R, C = r.randint(2, 6), r.randint(4, 12)
    alt = f"An array of dots with {R} rows and {C} dots in each row."
    return Item(f"The array has {R * C} dots arranged in {R} equal rows. How many dots are in each row?", str(C), [f"{R * C} ÷ {R} = {C}.", f"Check: {R} × {C} = {R * C}."],
                [W(str(R), "gave the number of rows"), W(str(R * C), "gave the total"), W(str(C + 1), "miscounted"), W(str(R * C - R), "subtracted instead of dividing")],
                FN("array_div", rows=R, cols=C), qtype="visual", diagram=Diagram("array", {"rows": R, "cols": C}, alt), tags={"modeling"})


@fam("012", mode="mc")
def dm_check(r, L):
    a, b, q, _ = div_case(r, L)
    good = f"{comma(q)} × {b} = {comma(a)}"
    return Item(f"{name(r)} finds that {comma(a)} ÷ {b} = {comma(q)}. Which equation checks the answer?", good, ["Multiply the quotient by the divisor. The product should be the dividend.", f"{good}."],
                [W(f"{comma(q)} + {b} = {comma(a)}", "used addition"), W(f"{comma(a)} × {b} = {comma(q)}", "multiplied the dividend by the divisor"), W(f"{comma(q)} × {comma(a)} = {b}", "put the numbers in the wrong positions")],
                FN("true_eq"), qtype="conceptual", tags={"connections"})


# ============================================================== S3 Dividing by One-Digit Divisors
@fam("012")
def dd_basic(r, L):
    a, b, q, _ = div_case(r, L)
    return Item(f"Divide: {comma(a)} ÷ {b}", comma(q), ["Divide one place at a time, starting with the greatest place.", f"{comma(a)} ÷ {b} = {comma(q)}.", f"Check: {comma(q)} × {b} = {comma(a)}."],
                div_wrongs(a, b, q), EX(f"{a} ÷ {b}"), claim=f"{comma(a)} ÷ {b}")


@fam("12")
def dd_zero(r, L):
    b = r.randint(2, 9)
    h = r.randint(1, 9)
    o = r.randint(1, 9)
    q = h * 100 + o if L == 1 or r.random() < 0.5 else h * 1000 + r.randint(1, 9) * 10 + o
    a = b * q
    need(a <= 9999 and "0" in str(q)[1:])
    return Item(f"Divide: {comma(a)} ÷ {b}", comma(q), [f"When a place cannot be divided, write 0 in the quotient to hold that place.", f"{comma(a)} ÷ {b} = {comma(q)}.", f"Check: {comma(q)} × {b} = {comma(a)}."],
                div_wrongs(a, b, q), EX(f"{a} ÷ {b}"), claim=f"{comma(a)} ÷ {b}", tags={"misconception"})


@fam("012")
def dd_word(r, L):
    a, b, q, _ = div_case(r, L)
    t = pick(r, [(f"A school has {comma(a)} students. They are placed in {b} equal groups for field day. How many students are in each group?", "students"),
                 (f"A bakery packs {comma(a)} cookies equally into {b} large boxes. How many cookies are in each box?", "cookies"),
                 (f"A farmer plants {comma(a)} seeds in {b} equal rows. How many seeds are in each row?", "seeds"),
                 (f"A machine fills {comma(a)} bottles in {b} hours, the same number each hour. How many bottles does it fill each hour?", "bottles")])
    return Item(t[0], f"{comma(q)} {t[1]}", [f"Divide {comma(a)} by {b}.", f"{comma(a)} ÷ {b} = {comma(q)} {t[1]}."], div_wrongs(a, b, q, t[1]), EX(f"{a} ÷ {b}", unit=t[1]), qtype="word-problem")


@fam("012")
def dd_missing_factor(r, L):
    a, b, q, _ = div_case(r, L)
    return Item(f"Find the missing factor: {b} × ___ = {comma(a)}", comma(q), [f"Divide the product by the known factor: {comma(a)} ÷ {b}.", f"{comma(a)} ÷ {b} = {comma(q)}."],
                div_wrongs(a, b, q), EX(f"{a} ÷ {b}"), qtype="fill-blank")


@fam("012", mode="mc")
def dd_digits(r, L):
    a, b, q, _ = div_case(r, max(L, 1))
    k = len(str(q))
    first = int(str(a)[0])
    why = f"{first} {'can' if first >= b else 'cannot'} be divided by {b}, so the quotient starts in the {PLACE_NAMES[k - 1]} place."
    opts = [x for x in (1, 2, 3, 4) if x != k]
    return Item(f"Without dividing all the way, decide: how many digits are in the quotient of {comma(a)} ÷ {b}?", str(k), ["Look at the first digit of the dividend.", why, f"The quotient has {k} digits."],
                [W(str(x), "did not compare the first digit of the dividend with the divisor") for x in opts], FN("quotient_digits", a=str(a), b=str(b)), qtype="conceptual", tags={"reasoning"})


@fam("012", mode="mc")
def dd_between(r, L):
    a, b, q, _ = div_case(r, max(L, 1))
    u = 10 ** (len(str(q)) - 1)
    need(q % u)
    lo = q // u * u
    f = lambda x: f"between {comma(x)} and {comma(x + u)}"
    bad = [lo + u, lo - u if lo - u > 0 else lo + 2 * u, lo * 10]
    return Item(f"Use multiplication to estimate. The quotient {comma(a)} ÷ {b} is between which two numbers?", f(lo),
                [f"{b} × {comma(lo)} = {comma(b * lo)} and {b} × {comma(lo + u)} = {comma(b * (lo + u))}.", f"{comma(a)} is between those products, so the quotient is {f(lo)}."],
                [W(f(x), "the products for these numbers do not surround the dividend") for x in bad], FN("value_between", e=f"{a} ÷ {b}"), qtype="conceptual", tags={"reasoning"})


# ============================================================== S4 Division with Remainders
def rem_wrongs(a, b, q, rr):
    return [W(f"{comma(q - 1)} R {rr + b}", "left a remainder that is larger than the divisor"), W(f"{comma(q)}", "left out the remainder"),
            W(f"{comma(q + 1)} R {rr}", "made a multiplication fact mistake"), W(f"{comma(q)} R {rr + 1 if rr + 1 < b else rr - 1}", "made a subtraction mistake")]


@fam("012")
def dr_basic(r, L):
    a, b, q, rr = div_case(r, L, rem=True)
    if L == 0:
        b = r.randint(2, 9)
        q = r.randint(3, 12)
        rr = r.randint(1, b - 1)
        a = b * q + rr
    return Item(f"Divide: {comma(a)} ÷ {b}. Write the answer as a quotient and a remainder, like 12 R 3.", f"{comma(q)} R {rr}",
                [f"{b} × {comma(q)} = {comma(b * q)}, which is the closest product that is not more than {comma(a)}.", f"{comma(a)} − {comma(b * q)} = {rr}, so the answer is {comma(q)} R {rr}."],
                rem_wrongs(a, b, q, rr), FN("quotient_rem", a=str(a), b=str(b)), claim=f"{comma(a)} ÷ {b}")


@fam("012")
def dr_remainder(r, L):
    a, b, q, rr = div_case(r, L, rem=True)
    return Item(f"What is the remainder when {comma(a)} is divided by {b}?", str(rr), [f"{b} × {comma(q)} = {comma(b * q)}.", f"{comma(a)} − {comma(b * q)} = {rr}. The remainder is {rr}."],
                [W(comma(q), "gave the quotient"), W(str(b - rr) if b - rr != rr else str(rr + 1), "subtracted from the next multiple"), W("0", "ignored the remainder"), W(str(rr + b), "left a remainder larger than the divisor")],
                FN("remainder_use", a=str(a), b=str(b), mode="rem"), claim=f"Remainder of {comma(a)} ÷ {b}")


@fam("012")
def dr_undo(r, L):
    a, b, q, rr = div_case(r, L, rem=True)
    return Item(f"A number is divided by {b}. The answer is {comma(q)} R {rr}. What is the number?", comma(a), ["Multiply the quotient by the divisor, then add the remainder.", f"{b} × {comma(q)} + {rr} = {comma(a)}."],
                [W(comma(b * q), "forgot to add the remainder"), W(comma(b * (q + rr)), "added the remainder before multiplying"), W(comma(b * q - rr), "subtracted the remainder"), W(comma(q + b + rr), "added all three numbers")],
                EX(f"{b} × {q} + {rr}"), qtype="conceptual", tags={"reasoning"})


@fam("012", mode="mc")
def dr_possible(r, L):
    b = r.randint(4, 9)
    good = pick(r, [b, b + 1, b + 2])
    bad = r.sample(range(0, b), 3)
    return Item(f"A number is divided by {b}. Which of these can NOT be the remainder?", str(good), [f"A remainder must be less than the divisor, {b}.", f"{good} is not less than {b}, so another group of {b} could still be made."],
                [W(str(x), f"{x} is less than {b}, so it can be a remainder") for x in bad], FN("bad_remainder", b=b), qtype="conceptual", tags={"reasoning"})


@fam("012", mode="mc")
def dr_which_has(r, L):
    rr = r.randint(1, 3)
    opts, seen = [], set()
    for k in range(40):
        a, b, q, x = div_case(sub(r, k), L, rem=True)
        if b <= rr or x == rr and any(c for _, c in opts):
            continue
        if x != rr and len([1 for _, c in opts if not c]) >= 3:
            continue
        t = f"{comma(a)} ÷ {b}"
        if t in seen:
            continue
        seen.add(t)
        opts.append((t, x == rr))
        if len(opts) == 4:
            break
    need(len(opts) == 4 and sum(c for _, c in opts) == 1)
    good = [t for t, c in opts if c][0]
    return Item(f"Which division has a remainder of {rr}?", good, ["Divide each one and look at what is left over.", f"{good} has a remainder of {rr}."],
                [W(t, "this division has a different remainder") for t, c in opts if not c], FN("has_remainder", rem=rr), qtype="conceptual")


@fam("12")
def dr_greatest(r, L):
    b = r.randint(3, 9)
    return Item(f"What is the greatest remainder you can get when you divide a whole number by {b}?", str(b - 1), [f"The remainder must be less than {b}.", f"The greatest whole number less than {b} is {b - 1}."],
                [W(str(b), "a remainder equal to the divisor makes another group"), W(str(b + 1), "a remainder cannot be greater than the divisor"), W("9", "thought 9 is always the greatest") if b != 10 and b - 1 != 9 else W("1", "gave the least remainder"), W("0", "gave the least remainder")],
                EX(f"{b} − 1"), qtype="conceptual", tags={"reasoning"})


# ============================================================== S5 Interpreting Remainders
UP = [("{a} students are going on a trip. Each van holds {b} students.", "How many vans are needed so that every student has a seat?", "vans"),
      ("{a} eggs must be packed in cartons. Each carton holds {b} eggs.", "How many cartons are needed to hold all the eggs?", "cartons"),
      ("{a} people are waiting for a boat ride. Each boat holds {b} people.", "How many boat trips are needed so that everyone gets a ride?", "trips"),
      ("A class needs {a} markers. Markers are sold in packs of {b}.", "How many packs must the class buy?", "packs")]
DOWN = [("A baker has {a} muffins and puts {b} muffins in each box.", "How many boxes can the baker fill completely?", "boxes"),
        ("{a} players sign up for a league. Each team needs exactly {b} players.", "How many full teams can be made?", "teams"),
        ("A ribbon is {a} inches long. Each bow uses {b} inches of ribbon.", "How many bows can be made?", "bows"),
        ("{a} photos are placed in an album with {b} photos on each page.", "How many pages can be filled completely?", "pages")]
REM = [("{a} stickers are shared equally among {b} friends, and each friend gets as many as possible.", "How many stickers are left over?", "stickers"),
       ("{a} chairs are set up in rows of {b}.", "After making as many full rows as possible, how many chairs are left over?", "chairs"),
       ("{a} apples are packed {b} to a bag, filling as many bags as possible.", "How many apples are left out of the full bags?", "apples")]


def ir_case(r, L):
    b = r.randint(3, 9)
    q = r.randint(4, 12) if L == 0 else r.randint(13, 99) if L == 1 else r.randint(101, 450)
    rr = r.randint(1, b - 1)
    return b * q + rr, b, q, rr


@fam("012")
def ir_up(r, L):
    a, b, q, rr = ir_case(r, L)
    t = pick(r, UP)
    return Item(t[0].format(a=comma(a), b=b) + " " + t[1], f"{comma(q + 1)} {t[2]}", [f"{comma(a)} ÷ {b} = {comma(q)} R {rr}.", f"{comma(q)} {t[2]} are full, and the {rr} left over need 1 more. The answer is {comma(q + 1)} {t[2]}."],
                [W(f"{comma(q)} {t[2]}", "dropped the remainder, leaving some out"), W(f"{rr} {t[2]}", "gave the remainder"), W(f"{comma(q + rr)} {t[2]}", "added the remainder to the quotient"), W(f"{comma(q + 2)} {t[2]}", "added too many")],
                FN("remainder_use", a=str(a), b=str(b), mode="up", unit=t[2]), qtype="real-world", tags={"reasoning"})


@fam("012")
def ir_down(r, L):
    a, b, q, rr = ir_case(r, L)
    t = pick(r, DOWN)
    return Item(t[0].format(a=comma(a), b=b) + " " + t[1], f"{comma(q)} {t[2]}", [f"{comma(a)} ÷ {b} = {comma(q)} R {rr}.", f"Only full groups count, so drop the remainder: {comma(q)} {t[2]}."],
                [W(f"{comma(q + 1)} {t[2]}", "rounded up, but the last group is not full"), W(f"{rr} {t[2]}", "gave the remainder"), W(f"{comma(q + rr)} {t[2]}", "added the remainder to the quotient"), W(f"{comma(q - 1)} {t[2]}", "made a division mistake")],
                FN("remainder_use", a=str(a), b=str(b), mode="down", unit=t[2]), qtype="real-world", tags={"reasoning"})


@fam("012")
def ir_rem(r, L):
    a, b, q, rr = ir_case(r, L)
    t = pick(r, REM)
    return Item(t[0].format(a=comma(a), b=b) + " " + t[1], f"{rr} {t[2]}", [f"{comma(a)} ÷ {b} = {comma(q)} R {rr}.", f"The remainder is what is left over: {rr} {t[2]}."],
                [W(f"{comma(q)} {t[2]}", "gave the quotient"), W(f"{comma(q + 1)} {t[2]}", "rounded the quotient up"), W(f"{b - rr} {t[2]}" if b - rr != rr else f"{rr + 1} {t[2]}", "found how many more are needed for another group"), W(f"0 {t[2]}", "ignored the remainder")],
                FN("remainder_use", a=str(a), b=str(b), mode="rem", unit=t[2]), qtype="real-world", tags={"reasoning"})


@fam("012", mode="mc")
def ir_decide(r, L):
    a, b, q, rr = ir_case(r, L)
    mode, t = pick(r, [("up", pick(r, UP)), ("down", pick(r, DOWN)), ("rem", pick(r, REM))])
    texts = {"down": f"Drop the remainder. The answer is {comma(q)}.", "up": f"Add 1 to the quotient. The answer is {comma(q + 1)}.", "rem": f"Use the remainder as the answer. The answer is {rr}."}
    extra = f"Add the quotient and the remainder. The answer is {comma(q + rr)}."
    return Item(t[0].format(a=comma(a), b=b) + " " + t[1] + f" You find that {comma(a)} ÷ {b} = {comma(q)} R {rr}. How should the remainder be used?", texts[mode],
                ["Reread the question to decide what the remainder means in the story.", texts[mode]],
                [W(texts[m], "did not match the remainder to the question") for m in texts if m != mode] + [W(extra, "the quotient and remainder count different things")],
                FN("rem_action", a=str(a), b=str(b), mode=mode), qtype="explain", tags={"reasoning"})


@fam("012")
def ir_two_step(r, L):
    b = r.randint(3, 9)
    q = r.randint(6, 12) if L == 0 else r.randint(13, 60) if L == 1 else r.randint(61, 240)
    keep = r.randint(3, 20)
    a = b * q + keep
    nm = name(r)
    return Item(f"{nm} has {comma(a)} trading cards. {nm} keeps {keep} cards and shares the rest equally among {b} friends. How many cards does each friend get?", f"{comma(q)} cards",
                [f"Cards to share: {comma(a)} − {keep} = {comma(a - keep)}.", f"{comma(a - keep)} ÷ {b} = {comma(q)} cards."],
                [W(f"{comma(a - keep)} cards", "stopped after the first step"), W(f"{comma(a // b)} cards", "divided before subtracting the cards kept"), W(f"{comma(q + keep)} cards", "added the cards kept to the quotient"), W(f"{comma(q + 1)} cards", "made a division mistake")],
                EX(f"({a} − {keep}) ÷ {b}", unit="cards"), qtype="multi-step", tags={"multistep"})


@fam("12")
def ir_compare_div(r, L):
    k = r.randint(3, 9)
    small = r.randint(12, 60) if L == 1 else r.randint(61, 240)
    big = k * small
    return Item(f"A blue whale model is {comma(big)} centimeters long. That is {k} times as long as a dolphin model. How many centimeters long is the dolphin model?", f"{comma(small)} centimeters",
                [f"{k} × (dolphin length) = {comma(big)}, so divide.", f"{comma(big)} ÷ {k} = {comma(small)} centimeters."],
                [W(f"{comma(big * k)} centimeters", "multiplied instead of dividing"), W(f"{comma(big - k)} centimeters", "subtracted instead of dividing"), W(f"{comma(small + 10)} centimeters", "made a division mistake"), W(f"{comma(small - 1)} centimeters", "made a division mistake")],
                EX(f"{big} ÷ {k}", unit="centimeters"), qtype="word-problem", tags={"reasoning"})


SKILLS = {
    1: dict(name="Division Facts and Patterns", fams=[df_fact, df_multiples, df_related, df_unit_form, df_pattern, df_word]),
    2: dict(name="Dividing with Models and Partial Quotients", fams=[dm_area_missing, dm_area_quotient, dm_break_apart, dm_partial_sum, dm_partial_missing, dm_array, dm_check]),
    3: dict(name="Dividing by One-Digit Divisors", fams=[dd_basic, dd_zero, dd_word, dd_missing_factor, dd_digits, dd_between]),
    4: dict(name="Division with Remainders", fams=[dr_basic, dr_remainder, dr_undo, dr_possible, dr_which_has, dr_greatest]),
    5: dict(name="Interpreting Remainders in Word Problems", fams=[ir_up, ir_down, ir_rem, ir_decide, ir_two_step, ir_compare_div]),
}
