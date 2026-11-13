"""Unit 2: Multi-Digit Addition and Subtraction (4.NBT.B.4, 4.OA.A.3)."""
from g4lib import *

UNIT_ID = "multi-digit-addition-subtraction"
RNG = {0: (1000, 9999), 1: (10000, 99999), 2: (100000, 999999)}
CTX = [("A bakery sold {a} muffins in March and {b} muffins in April.", "muffins"), ("A school collected {a} cans in the fall and {b} cans in the spring.", "cans"),
       ("A zoo had {a} visitors on Saturday and {b} visitors on Sunday.", "visitors"), ("A library has {a} fiction books and {b} nonfiction books.", "books"),
       ("A farm picked {a} apples in the first week and {b} apples in the second week.", "apples"), ("A game store sold {a} games online and {b} games in the shop.", "games"),
       ("A town planted {a} trees last year and {b} trees this year.", "trees"), ("A theater sold {a} tickets in June and {b} tickets in July.", "tickets")]


def n_(r, L, lo=None, hi=None):
    a, b = RNG[L]
    return r.randint(lo or a, hi or b)


def carries(a, b):
    c = k = 0
    while a or b:
        s = a % 10 + b % 10 + c
        c = s // 10
        k += c
        a //= 10
        b //= 10
    return k


def borrows(a, b):
    c = k = 0
    while a or b:
        d = a % 10 - b % 10 - c
        c = 1 if d < 0 else 0
        k += c
        a //= 10
        b //= 10
    return k


def nocarry(a, b):
    out, p = 0, 1
    while a or b:
        out += (a % 10 + b % 10) % 10 * p
        p *= 10
        a //= 10
        b //= 10
    return out


def smallbig(a, b):
    out, p = 0, 1
    while a or b:
        out += abs(a % 10 - b % 10) * p
        p *= 10
        a //= 10
        b //= 10
    return out


def add_w(a, b, unit=""):
    u = (" " + unit) if unit else ""
    s = a + b
    return [W(comma(nocarry(a, b)) + u, "forgot to add the regrouped digits"), W(comma(s + 10 ** (len(str(s)) - 2)) + u, "regrouped an extra time"), W(comma(a - b if a > b else b - a) + u, "subtracted instead of adding"),
            W(comma(s - 10) + u, "made an addition fact mistake"), W(comma(s + 100) + u, "made a regrouping mistake")]


def sub_w(a, b, unit=""):
    u = (" " + unit) if unit else ""
    d = a - b
    return [W(comma(smallbig(a, b)) + u, "subtracted the smaller digit from the larger digit in every place"), W(comma(a + b) + u, "added instead of subtracting"),
            W(comma(d + 10 ** (len(str(a)) - 2)) + u, "forgot that a digit was regrouped"), W(comma(d + 10) + u, "forgot to regroup a ten"), W(comma(abs(d - 100)) + u, "made a regrouping mistake")]


def add_pair(r, L, mincarry=1):
    for _ in range(60):
        a, b = n_(r, L), n_(r, L, RNG[L][0] // (1 if L else 10))
        if a + b <= (999999 if L == 2 else 10 ** 7) and carries(a, b) >= mincarry + (L > 0):
            return a, b
    raise Reject()


def sub_pair(r, L, zeros=False):
    for _ in range(200):
        a = n_(r, L)
        if zeros:
            s = list(str(a))
            for i in r.sample(range(1, len(s)), 2 if L < 2 else 3):
                s[i] = "0"
            if r.random() < 0.3:
                s = [s[0]] + ["0"] * (len(s) - 1)
            a = int("".join(s))
        b = r.randint(a // 10 + 1, a - 11)
        if borrows(a, b) >= (2 if zeros or L else 1) and smallbig(a, b) != a - b:
            return a, b
    raise Reject()


# ============================================================== S1 Adding
@fam("012")
def ad_basic(r, L):
    a, b = add_pair(r, L)
    return Item(f"Add: {comma(a)} + {comma(b)}", comma(a + b), ["Line up the digits by place value. Add the ones first and regroup each time the column total is 10 or more.", f"{comma(a)} + {comma(b)} = {comma(a + b)}."],
                add_w(a, b), EX(f"{a} + {b}"), claim=f"{comma(a)} + {comma(b)}")


@fam("012")
def ad_three(r, L):
    a, b, c = n_(r, L), n_(r, max(L - 1, 0)), n_(r, max(L - 1, 0), 100, 999 if L == 0 else None)
    s = a + b + c
    need(s < 10 ** 6)
    return Item(f"Find the sum: {comma(a)} + {comma(b)} + {comma(c)}", comma(s), ["Line up all three numbers by place value.", f"Add each column and regroup: {comma(s)}."],
                [W(comma(a + b), "left out the third addend"), W(comma(nocarry(nocarry(a, b), c)) if nocarry(nocarry(a, b), c) != s else comma(s - 100), "forgot to add the regrouped digits"), W(comma(s + 1000), "regrouped an extra time"), W(comma(s - 10), "made an addition fact mistake")],
                EX(f"{a} + {b} + {c}"), claim=f"{comma(a)} + {comma(b)} + {comma(c)}")


@fam("012")
def ad_missing(r, L):
    a, b = add_pair(r, L, 0)
    s = a + b
    return Item(f"Find the missing addend: {comma(a)} + ___ = {comma(s)}", comma(b), ["Subtract the known addend from the sum.", f"{comma(s)} − {comma(a)} = {comma(b)}."],
                [W(comma(s + a), "added the two numbers instead of subtracting"), W(comma(smallbig(s, a)) if smallbig(s, a) != b else comma(b + 10), "subtracted the smaller digit from the larger digit"), W(comma(b + 100), "made a regrouping mistake"), W(comma(b - 10) if b > 20 else comma(b + 1), "made a subtraction fact mistake")],
                EX(f"{s} − {a}"), qtype="fill-blank")


@fam("012")
def ad_regroup_count(r, L):
    a, b = add_pair(r, L, 0)
    k = carries(a, b)
    return Item(f"When you add {comma(a)} + {comma(b)} with the standard algorithm, how many times must you regroup?", str(k),
                ["Add each column from right to left. Regroup each time the total of a column is 10 or more.", f"There are {k} columns with a total of 10 or more."],
                [W(str(k + 1), "counted a column that did not need regrouping"), W(str(abs(k - 1)) if k != 1 else "3", "missed a column that needed regrouping"), W(str(len(str(a))) if len(str(a)) != k else str(k + 2), "counted every column")],
                FN("carry_count", a=str(a), b=str(b)), qtype="conceptual", tags={"reasoning"})


@fam("012")
def ad_word(r, L):
    a, b = add_pair(r, L, 0)
    t, u = pick(r, CTX)
    return Item(t.format(a=comma(a), b=comma(b)) + f" How many {u} is that in all?", f"{comma(a + b)} {u}", ["“In all” means add.", f"{comma(a)} + {comma(b)} = {comma(a + b)} {u}."],
                add_w(a, b, u), EX(f"{a} + {b}", unit=u), qtype="word-problem")


@fam("012", mode="mc")
def ad_digit(r, L):
    a, b = add_pair(r, L)
    s = str(a + b)
    e = r.randint(1, len(s) - 2)
    good = s[-e - 1]
    nc = str(nocarry(a, b)).rjust(len(s), "0")[-e - 1]
    bad = []
    for x in [nc, str(a)[-e - 1] if e < len(str(a)) else "0", s[-e], str((int(good) + 1) % 10), str((int(good) + 9) % 10)]:
        if x != good and x not in bad:
            bad.append(x)
    need(len(bad) >= 3)
    return Item(f"Add {comma(a)} + {comma(b)}. What digit is in the {PLACE_NAMES[e]} place of the sum?", good, [f"{comma(a)} + {comma(b)} = {comma(a + b)}.", f"The digit in the {PLACE_NAMES[e]} place is {good}."],
                [W(bad[0], "forgot to add a regrouped digit or looked at the wrong place"), W(bad[1], "looked at the wrong place"), W(bad[2], "looked at the wrong place")],
                FN("digit_of_expr", e=f"{a} + {b}", place=PLACE_NAMES[e]), qtype="conceptual")


# ============================================================== S2 Subtracting
@fam("012")
def sb_basic(r, L):
    a, b = sub_pair(r, L)
    return Item(f"Subtract: {comma(a)} − {comma(b)}", comma(a - b), ["Line up the digits by place value. Subtract the ones first and regroup when the top digit is smaller.", f"{comma(a)} − {comma(b)} = {comma(a - b)}.", f"Check with addition: {comma(a - b)} + {comma(b)} = {comma(a)}."],
                sub_w(a, b), EX(f"{a} − {b}"), claim=f"{comma(a)} − {comma(b)}")


@fam("012")
def sb_missing(r, L):
    a, b = sub_pair(r, L)
    d = a - b
    if r.random() < 0.5:
        return Item(f"Find the missing number: ___ − {comma(b)} = {comma(d)}", comma(a), ["Add the difference and the number subtracted to find the starting number.", f"{comma(d)} + {comma(b)} = {comma(a)}."],
                    [W(comma(abs(d - b)), "subtracted instead of adding"), W(comma(nocarry(d, b)) if nocarry(d, b) != a else comma(a - 10), "forgot to add the regrouped digits"), W(comma(a + 100), "made a regrouping mistake")],
                    EX(f"{d} + {b}"), qtype="fill-blank")
    return Item(f"Find the missing number: {comma(a)} − ___ = {comma(d)}", comma(b), ["Subtract the difference from the starting number.", f"{comma(a)} − {comma(d)} = {comma(b)}."],
                [W(comma(a + d), "added instead of subtracting"), W(comma(smallbig(a, d)) if smallbig(a, d) != b else comma(b + 10), "subtracted the smaller digit from the larger digit"), W(comma(b + 100), "made a regrouping mistake")],
                EX(f"{a} − {d}"), qtype="fill-blank")


@fam("012", mode="mc")
def sb_check(r, L):
    a, b = sub_pair(r, L)
    d = a - b
    good = f"{comma(d)} + {comma(b)} = {comma(a)}"
    return Item(f"{comma(a)} − {comma(b)} = {comma(d)}. Which addition equation can you use to check this subtraction?", good,
                ["Addition undoes subtraction: difference + number subtracted = starting number.", f"{good}."],
                [W(f"{comma(a)} + {comma(b)} = {comma(d)}", "added the starting number instead of the difference"), W(f"{comma(d)} + {comma(a)} = {comma(b)}", "put the numbers in the wrong positions"), W(f"{comma(a)} + {comma(d)} = {comma(b)}", "put the numbers in the wrong positions")],
                FN("true_eq"), qtype="conceptual", tags={"reasoning"})


@fam("012")
def sb_word(r, L):
    a, b = sub_pair(r, L)
    t, u = pick(r, CTX)
    first = t.format(a=comma(a), b=comma(b))
    return Item(first + f" How many more {u} is the first amount than the second?", f"{comma(a - b)} {u}", ["“How many more” means find the difference.", f"{comma(a)} − {comma(b)} = {comma(a - b)} {u}."],
                sub_w(a, b, u), EX(f"{a} − {b}", unit=u), qtype="word-problem")


@fam("012")
def sb_regroup_count(r, L):
    a, b = sub_pair(r, L)
    need("0" not in str(a))
    k = borrows(a, b)
    return Item(f"When you subtract {comma(a)} − {comma(b)} with the standard algorithm, how many times must you regroup?", str(k),
                ["Work from right to left. You regroup whenever the top digit (after any earlier regrouping) is smaller than the bottom digit.", f"You regroup {k} time{'s' if k != 1 else ''}."],
                [W(str(k + 1), "counted a column that did not need regrouping"), W(str(k - 1) if k > 1 else "0", "missed a column that needed regrouping"), W(str(len(str(a))) if len(str(a)) != k else str(k + 2), "counted every column")],
                FN("borrow_count", a=str(a), b=str(b)), qtype="conceptual", tags={"reasoning"})


@fam("012")
def sb_take_from(r, L):
    a, b = sub_pair(r, L)
    nm = name(r)
    thing = pick(r, ["points", "stickers", "pages", "steps", "coins"])
    return Item(f"{nm} had {comma(a)} {thing}. After giving some away, {nm} has {comma(b)} {thing} left. How many {thing} did {nm} give away?", f"{comma(a - b)} {thing}",
                ["Start amount − amount left = amount given away.", f"{comma(a)} − {comma(b)} = {comma(a - b)} {thing}."], sub_w(a, b, thing), EX(f"{a} − {b}", unit=thing), qtype="word-problem")


# ============================================================== S3 Subtracting Across Zeros
@fam("012")
def sz_basic(r, L):
    a, b = sub_pair(r, L, zeros=True)
    return Item(f"Subtract: {comma(a)} − {comma(b)}", comma(a - b), ["When the top digit is 0, regroup from the nearest place on the left that is not 0, then move across the zeros.", f"{comma(a)} − {comma(b)} = {comma(a - b)}.", f"Check: {comma(a - b)} + {comma(b)} = {comma(a)}."],
                sub_w(a, b), EX(f"{a} − {b}"), claim=f"{comma(a)} − {comma(b)}")


@fam("012")
def sz_from_round(r, L):
    a = pick(r, [1000, 2000, 5000, 10000] if L == 0 else [10000, 20000, 50000, 100000] if L == 1 else [100000, 200000, 500000, 1000000])
    b = r.randint(a // 10 + 1, a - 111)
    need(b % 10 and (b // 10) % 10)
    return Item(f"Find the difference: {comma(a)} − {comma(b)}", comma(a - b), [f"One way: subtract from {comma(a - 1)} instead, then add 1 back.", f"{comma(a - 1)} − {comma(b)} = {comma(a - 1 - b)}, and {comma(a - 1 - b)} + 1 = {comma(a - b)}."],
                sub_w(a, b), EX(f"{a} − {b}"), claim=f"{comma(a)} − {comma(b)}")


@fam("012", mode="mc")
def sz_strategy(r, L):
    a = pick(r, [1000, 3000, 5000, 8000] if L == 0 else [10000, 30000, 40000, 70000] if L == 1 else [100000, 300000, 600000])
    b = r.randint(a // 10 + 1, a - 111)
    good = f"{comma(a - 1)} − {comma(b)} + 1"
    return Item(f"Which expression has the same value as {comma(a)} − {comma(b)}?", good, [f"{comma(a)} is 1 more than {comma(a - 1)}.", f"Subtract from {comma(a - 1)} (no regrouping across zeros), then add the 1 back: {good}."],
                [W(f"{comma(a - 1)} − {comma(b)} − 1", "subtracted 1 again instead of adding it back"), W(f"{comma(a - 1)} − {comma(b - 1)} + 1", "changed both numbers and still added 1"), W(f"{comma(a - 1)} − {comma(b)}", "forgot to add the 1 back")],
                FN("expr_eq", e=f"{a} − {b}"), qtype="compare-strategies", tags={"reasoning", "connections"})


@fam("012")
def sz_word(r, L):
    a, b = sub_pair(r, L, zeros=True)
    t = pick(r, [("A reservoir can hold {a} gallons of water. It holds {b} gallons now.", "How many more gallons can it hold?", "gallons"),
                 ("A charity wants to raise {a} dollars. It has raised {b} dollars so far.", "How many more dollars does it need?", "dollars"),
                 ("A stadium has {a} seats. So far, {b} tickets have been sold.", "How many seats are still open?", "seats"),
                 ("A reading club has a goal of {a} pages. Members have read {b} pages.", "How many pages are left to reach the goal?", "pages")])
    return Item(t[0].format(a=comma(a), b=comma(b)) + " " + t[1], f"{comma(a - b)} {t[2]}", ["Subtract the amount so far from the total.", f"{comma(a)} − {comma(b)} = {comma(a - b)} {t[2]}."],
                sub_w(a, b, t[2]), EX(f"{a} − {b}", unit=t[2]), qtype="word-problem")


@fam("012")
def sz_missing(r, L):
    a, b = sub_pair(r, L, zeros=True)
    d = a - b
    return Item(f"Find the missing number: {comma(b)} + ___ = {comma(a)}", comma(d), ["Subtract to find the missing addend.", f"{comma(a)} − {comma(b)} = {comma(d)}."],
                sub_w(a, b), EX(f"{a} − {b}"), qtype="fill-blank")


@fam("012", mode="mc")
def sz_regroup_show(r, L):
    k = 4 if L == 0 else 5
    lead = r.randint(3, 9)   # at least 2 of the leading unit remain after regrouping ("2 thousands", never "1 thousands")
    a = lead * 10 ** (k - 1)
    parts = [f"{lead - 1} {PLACE_NAMES[k - 1]}"] + [f"9 {PLACE_NAMES[i]}" for i in range(k - 2, 0, -1)] + ["10 ones"]
    good = ", ".join(parts)
    b1 = ", ".join([f"{lead - 1} {PLACE_NAMES[k - 1]}"] + [f"10 {PLACE_NAMES[i]}" for i in range(k - 2, 0, -1)] + ["10 ones"])
    b2 = ", ".join([f"{lead} {PLACE_NAMES[k - 1]}"] + [f"9 {PLACE_NAMES[i]}" for i in range(k - 2, 0, -1)] + ["10 ones"])
    b3 = ", ".join([f"{lead - 1} {PLACE_NAMES[k - 1]}"] + [f"9 {PLACE_NAMES[i]}" for i in range(k - 2, 0, -1)] + ["9 ones"])
    return Item(f"To subtract from {comma(a)}, you regroup across the zeros. Which shows {comma(a)} regrouped so that you can subtract in every place?", good,
                [f"Take 1 from the {PLACE_NAMES[k - 1]} place. Each place in the middle becomes 9 and the ones place becomes 10.", f"{good} still equals {comma(a)}."],
                [W(b1, "left 10 in the middle places; that adds up to more than the number"), W(b2, "did not take 1 from the first digit"), W(b3, "the ones place should get 10")],
                FN("unit_names_list", n=str(a)), qtype="conceptual", tags={"reasoning", "multiple-representations"})


# ============================================================== S4 Estimating Sums and Differences
def est_case(r, L):
    a, b = n_(r, L), n_(r, L)
    if a < b:
        a, b = b, a
    k = len(str(b))
    e = r.randint(max(2, k - 2), k - 1)
    need(rnd_to(a, e) != rnd_to(b, e) and a - b > 10 ** e)
    return a, b, e


@fam("012")
def es_sum(r, L):
    a, b, e = est_case(r, L)
    ra, rb = rnd_to(a, e), rnd_to(b, e)
    p = sg(PLACE_NAMES[e])
    return Item(f"Estimate the sum by rounding each number to the nearest {p}: {comma(a)} + {comma(b)}", comma(ra + rb),
                [f"{comma(a)} rounds to {comma(ra)} and {comma(b)} rounds to {comma(rb)}.", f"{comma(ra)} + {comma(rb)} = {comma(ra + rb)}."],
                [W(comma(a + b), "found the exact sum instead of an estimate"), W(comma(ra + rb + 10 ** e), "rounded one number the wrong way"), W(comma(ra + rb - 10 ** e), "rounded one number the wrong way"), W(comma(rnd_to(a, e - 1) + rnd_to(b, e - 1)), "rounded to a different place")],
                FN("est_round", a=str(a), b=str(b), op="+", place=PLACE_NAMES[e]), qtype="procedural")


@fam("012")
def es_diff(r, L):
    a, b, e = est_case(r, L)
    ra, rb = rnd_to(a, e), rnd_to(b, e)
    p = sg(PLACE_NAMES[e])
    return Item(f"Estimate the difference by rounding each number to the nearest {p}: {comma(a)} − {comma(b)}", comma(ra - rb),
                [f"{comma(a)} rounds to {comma(ra)} and {comma(b)} rounds to {comma(rb)}.", f"{comma(ra)} − {comma(rb)} = {comma(ra - rb)}."],
                [W(comma(a - b), "found the exact difference instead of an estimate"), W(comma(ra - rb + 10 ** e), "rounded one number the wrong way"), W(comma(ra + rb), "added instead of subtracting"), W(comma(abs(rnd_to(a, e - 1) - rnd_to(b, e - 1))), "rounded to a different place")],
                FN("est_round", a=str(a), b=str(b), op="-", place=PLACE_NAMES[e]), qtype="procedural")


@fam("012", mode="mc")
def es_reasonable(r, L):
    a, b, e = est_case(r, L)
    op = pick(r, "+-")
    exact = a + b if op == "+" else a - b
    ra, rb = rnd_to(a, e), rnd_to(b, e)
    est = ra + rb if op == "+" else ra - rb
    sym = "+" if op == "+" else "−"
    wrong = pick(r, [exact + 10 ** (e + 1), exact * 10, abs(exact - 10 ** (e + 1))])
    nm = name(r)
    need(wrong != exact and abs(wrong - est) > 10 ** e)
    good = f"No. An estimate is {comma(ra)} {sym} {comma(rb)} = {comma(est)}, which is not close to {comma(wrong)}."
    return Item(f"{nm} says that {comma(a)} {sym} {comma(b)} = {comma(wrong)}. Use estimation to decide: is the answer reasonable?", good,
                [f"Round each number to the nearest {sg(PLACE_NAMES[e])}: {comma(ra)} {sym} {comma(rb)} = {comma(est)}.", f"{comma(wrong)} is not close to {comma(est)}, so the answer is not reasonable."],
                [W(f"Yes. An estimate is {comma(ra)} {sym} {comma(rb)} = {comma(est)}, which is close to {comma(wrong)}.", "did not compare the estimate with the answer"),
                 W(f"Yes. The answer has the same last digit as the exact answer.", "checked only the last digit"), W(f"No. An answer to {'an addition' if op == '+' else 'a subtraction'} problem can never have {len(str(wrong))} digits.", "used a rule that is not true")],
                FN("est_judge", a=str(a), b=str(b), op=op, place=PLACE_NAMES[e], claimed=str(wrong)), qtype="explain", tags={"reasoning"})


@fam("012", mode="mc")
def es_over_under(r, L):
    a, b, e = est_case(r, L)
    u = 10 ** e
    ra, rb = rnd_to(a, e), rnd_to(b, e)
    need((ra > a) == (rb > b) and ra != a and rb != b)
    up = ra > a
    good = f"{'greater' if up else 'less'} than the exact sum"
    return Item(f"To estimate {comma(a)} + {comma(b)}, {name(r)} rounds each number to the nearest {sg(PLACE_NAMES[e])} and gets {comma(ra)} + {comma(rb)} = {comma(ra + rb)}. Is the estimate greater than or less than the exact sum?", good,
                [f"Both numbers were rounded {'up' if up else 'down'}.", f"So the estimate is {good}."],
                [W(f"{'less' if up else 'greater'} than the exact sum", "mixed up the direction of rounding"), W("equal to the exact sum", "thought rounding does not change the total")],
                FN("est_cmp", a=str(a), b=str(b), place=PLACE_NAMES[e]), qtype="conceptual", tags={"reasoning"})


@fam("012")
def es_word(r, L):
    a, b, e = est_case(r, L)
    t, u = pick(r, CTX)
    ra, rb = rnd_to(a, e), rnd_to(b, e)
    return Item(t.format(a=comma(a), b=comma(b)) + f" Round each number to the nearest {sg(PLACE_NAMES[e])}. About how many {u} is that altogether?", f"{comma(ra + rb)} {u}",
                [f"{comma(a)} is about {comma(ra)} and {comma(b)} is about {comma(rb)}.", f"{comma(ra)} + {comma(rb)} = {comma(ra + rb)} {u}."],
                [W(f"{comma(a + b)} {u}", "found the exact sum instead of an estimate"), W(f"{comma(ra + rb + 10 ** e)} {u}", "rounded one number the wrong way"), W(f"{comma(abs(ra - rb))} {u}", "subtracted instead of adding"), W(f"{comma(ra + rb - 10 ** e)} {u}", "rounded one number the wrong way")],
                FN("est_round", a=str(a), b=str(b), op="+", place=PLACE_NAMES[e], unit=u), qtype="real-world")


@fam("012", mode="mc")
def es_between(r, L):
    a, b, e = est_case(r, L)
    op = pick(r, "+-")
    v = a + b if op == "+" else a - b
    u = 10 ** e
    need(v % u)
    lo = v // u * u
    need(lo - u > 0)
    f = lambda x: f"between {comma(x)} and {comma(x + u)}"
    return Item(f"Without finding the exact answer, decide: {comma(a)} {'+' if op == '+' else '−'} {comma(b)} is between which two numbers?", f(lo),
                [f"Estimate with rounded numbers, then check: the exact answer is {comma(v)}.", f"{comma(v)} is {f(lo)}."],
                [W(f(lo + u), "estimated too high"), W(f(lo - u), "estimated too low"), W(f(lo + 2 * u), "estimated too high")],
                FN("value_between", e=f"{a} {op} {b}"), qtype="conceptual", tags={"reasoning"})


# ============================================================== S5 Word problems
@fam("012")
def wp_two_step(r, L):
    a, b = n_(r, L), n_(r, L)
    c = r.randint(RNG[L][0] // 2, a + b - 100)
    nm = name(r)
    t = pick(r, [(f"A warehouse had {comma(a)} boxes. A truck delivered {comma(b)} more boxes. Then {comma(c)} boxes were shipped out.", "How many boxes are in the warehouse now?", "boxes"),
                 (f"{nm} scored {comma(a)} points in the first game and {comma(b)} points in the second game. Then {nm} lost {comma(c)} points in a bonus round.", f"How many points does {nm} have now?", "points"),
                 (f"A museum had {comma(a)} visitors in the morning and {comma(b)} in the afternoon. By evening, {comma(c)} of them had left.", "How many visitors were still in the museum?", "visitors")])
    v = a + b - c
    return Item(t[0] + " " + t[1], f"{comma(v)} {t[2]}", [f"First add: {comma(a)} + {comma(b)} = {comma(a + b)}.", f"Then subtract: {comma(a + b)} − {comma(c)} = {comma(v)} {t[2]}."],
                [W(f"{comma(a + b)} {t[2]}", "stopped after the first step"), W(f"{comma(a + b + c)} {t[2]}", "added all three numbers"), W(f"{comma(abs(a - c))} {t[2]}", "left out the second amount"), W(f"{comma(v + 100)} {t[2]}", "made a regrouping mistake")],
                EX(f"{a} + {b} − {c}", unit=t[2]), qtype="multi-step", tags={"multistep"})


@fam("012")
def wp_compare(r, L):
    a, b = sub_pair(r, L)
    n1, n2 = r.sample(["Lake City", "Pine Town", "Rivertown", "Oakdale", "Maple Grove", "Stone Bridge"], 2)
    if r.random() < 0.5:
        return Item(f"{n1} has {comma(a)} people. {n2} has {comma(a - b)} fewer people than {n1}. How many people live in {n2}?", f"{comma(b)} people",
                    ["“Fewer than” means subtract.", f"{comma(a)} − {comma(a - b)} = {comma(b)} people."], sub_w(a, a - b, "people"), EX(f"{a} − {a - b}", unit="people"), qtype="word-problem")
    return Item(f"{n2} has {comma(b)} people. {n1} has {comma(a - b)} more people than {n2}. How many people live in {n1}?", f"{comma(a)} people",
                ["“More than” means add.", f"{comma(b)} + {comma(a - b)} = {comma(a)} people."], add_w(b, a - b, "people"), EX(f"{b} + {a - b}", unit="people"), qtype="word-problem")


@fam("012", mode="mc")
def wp_equation(r, L):
    a, b = sub_pair(r, L)
    d = a - b
    kind = r.randrange(3)
    if kind == 0:
        story, good, bad, val = f"A store had {comma(a)} toys. After a sale, {comma(d)} toys were left. Let n be the number of toys sold.", f"{comma(a)} − n = {comma(d)}", [f"{comma(a)} + n = {comma(d)}", f"n − {comma(a)} = {comma(d)}", f"{comma(d)} − n = {comma(a)}"], b
    elif kind == 1:
        story, good, bad, val = f"A jar had some marbles. {name(r)} added {comma(b)} marbles. Now the jar has {comma(a)} marbles. Let n be the number of marbles in the jar at the start.", f"n + {comma(b)} = {comma(a)}", [f"n − {comma(b)} = {comma(a)}", f"{comma(a)} + {comma(b)} = n", f"n + {comma(a)} = {comma(b)}"], d
    else:
        story, good, bad, val = f"A club needs {comma(a)} dollars. It has {comma(b)} dollars. Let n be the number of dollars the club still needs.", f"{comma(b)} + n = {comma(a)}", [f"{comma(a)} + {comma(b)} = n", f"{comma(a)} + n = {comma(b)}", f"n − {comma(b)} = {comma(a)}"], d
    return Item(story + " Which equation matches the story?", good, ["Decide what is known and what is unknown, then write the equation in the order of the story.", f"{good}, and n = {comma(val)}."],
                [W(x, "the equation does not match the story") for x in bad], FN("eq_with", n=str(val)), qtype="conceptual", tags={"modeling", "reasoning"})


@fam("012")
def wp_table(r, L):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday"]
    v = [n_(r, L) for _ in days]
    what = pick(r, ["steps walked", "cans recycled", "pages printed", "bottles filled"])
    i, j = r.sample(range(4), 2)
    rows = [[d, comma(x)] for d, x in zip(days, v)]
    alt = f"A table of {what} each day. " + "; ".join(f"{a}: {b}" for a, b in rows) + "."
    dg = Diagram("table", {"header": ["Day", what.title()], "rows": rows}, alt)
    if r.random() < 0.5:
        return Item(f"The table shows the number of {what} each day. How many {what.split()[0]} were {what.split()[1]} on {days[i]} and {days[j]} combined?", comma(v[i] + v[j]),
                    [f"Add the two days: {comma(v[i])} + {comma(v[j])} = {comma(v[i] + v[j])}."], add_w(v[i], v[j]), EX(f"{v[i]} + {v[j]}"), qtype="real-world", diagram=dg, tags={"modeling"})
    hi, lo = max(v), min(v)
    need(hi != lo)
    return Item(f"The table shows the number of {what} each day. What is the difference between the greatest and the least number?", comma(hi - lo),
                [f"The greatest is {comma(hi)} and the least is {comma(lo)}.", f"{comma(hi)} − {comma(lo)} = {comma(hi - lo)}."], sub_w(hi, lo), FN("table_range", values=[str(x) for x in v]), qtype="real-world", diagram=dg, tags={"modeling"})


@fam("12")
def wp_three_step(r, L):
    a = n_(r, L)
    b, c, d = r.randint(a // 6, a // 3), r.randint(a // 6, a // 3), r.randint(a // 8, a // 4)
    nm = name(r)
    v = a - b - c + d
    return Item(f"The class of {nm} has a goal of collecting {comma(a)} bottle caps. They collect {comma(b)} in week 1 and {comma(c)} in week 2. Then the goal is raised by {comma(d)} bottle caps. How many more bottle caps does the class need to reach the new goal?",
                f"{comma(v)} bottle caps", [f"New goal: {comma(a)} + {comma(d)} = {comma(a + d)}.", f"Collected so far: {comma(b)} + {comma(c)} = {comma(b + c)}.", f"Still needed: {comma(a + d)} − {comma(b + c)} = {comma(v)} bottle caps."],
                [W(f"{comma(a - b - c)} bottle caps", "forgot that the goal was raised"), W(f"{comma(a + d)} bottle caps", "found only the new goal"), W(f"{comma(a - b - c - d)} bottle caps", "subtracted the extra amount instead of adding it"), W(f"{comma(b + c)} bottle caps", "found only the amount collected")],
                EX(f"{a} + {d} − {b} − {c}", unit="bottle caps"), qtype="multi-step", tags={"multistep", "challenge"})


@fam("012")
def wp_start_unknown(r, L):
    a, b = add_pair(r, L, 0)
    nm = name(r)
    return Item(f"{nm} is reading a long book series. After reading {comma(b)} pages this month, {nm} has read {comma(a + b)} pages in all. How many pages had {nm} read before this month?", f"{comma(a)} pages",
                ["The total and one part are known. Subtract to find the other part.", f"{comma(a + b)} − {comma(b)} = {comma(a)} pages."],
                [W(f"{comma(a + b + b)} pages", "added instead of subtracting"), W(f"{comma(a + 100)} pages", "made a regrouping mistake"), W(f"{comma(smallbig(a + b, b))} pages" if smallbig(a + b, b) != a else f"{comma(a + 10)} pages", "subtracted the smaller digit from the larger digit")],
                EX(f"{a + b} − {b}", unit="pages"), qtype="word-problem")


SKILLS = {
    1: dict(name="Adding Multi-Digit Whole Numbers", fams=[ad_basic, ad_three, ad_missing, ad_regroup_count, ad_word, ad_digit]),
    2: dict(name="Subtracting Multi-Digit Whole Numbers", fams=[sb_basic, sb_missing, sb_check, sb_word, sb_regroup_count, sb_take_from]),
    3: dict(name="Subtracting Across Zeros", fams=[sz_basic, sz_from_round, sz_strategy, sz_word, sz_missing, sz_regroup_show]),
    4: dict(name="Estimating Sums and Differences", fams=[es_sum, es_diff, es_reasonable, es_over_under, es_word, es_between]),
    5: dict(name="Addition and Subtraction Word Problems", fams=[wp_two_step, wp_compare, wp_equation, wp_table, wp_three_step, wp_start_unknown]),
}
