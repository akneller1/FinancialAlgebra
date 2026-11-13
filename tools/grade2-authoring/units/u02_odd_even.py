"""Unit 2: Odd and Even Numbers and Arrays (odd-even-arrays). 2.OA.C.3, 2.OA.C.4."""
from g2lib import *

UNIT_ID = "odd-even-arrays"


def par(n):
    return "even" if n % 2 == 0 else "odd"


def num_for(r, L):
    return r.randint(3, 12) if L == 0 else r.randint(9, 20) if L == 1 else r.randint(11, 20)


# ============================================================== S1 Odd and Even Numbers
@fam("012", mode="sa")
def oe_pairs(r, L):
    n = num_for(r, L)
    alt = f"{n} counters lined up in pairs, in two rows." + (" One counter has no partner." if n % 2 else " Every counter has a partner.")
    return Item("Does the group have an odd or even number of counters?", par(n),
                [f"Look for partners. {'One counter is left over' if n % 2 else 'Every counter has a partner'}.", f"There are {n} counters, so the number is {par(n)}."],
                [W(par(n + 1), "did not check for a counter without a partner")], FN("parity", n=n), qtype="visual",
                diagram=Diagram("counters", {"n": n, "layout": "pairs"}, alt))


@fam("012", mode="mc")
def oe_pairs_mc(r, L):
    n = num_for(r, L)
    alt = f"{n} counters in rows of five."
    left = n % 2
    good = f"{par(n)}, because {'one counter is left over' if left else 'every counter has a partner'} when you make pairs"
    bad = [f"{par(n + 1)}, because {'every counter has a partner' if left else 'one counter is left over'} when you make pairs",
           f"{par(n + 1)}, because there are {n} counters" if n % 10 else f"odd, because the last row is full",
           f"{par(n)}, because the counters are in rows"]
    it = mc_key("Is the number of counters odd or even? Make pairs to check.", good, bad,
                [f"There are {n} counters.", f"{n} is {par(n)}: {'one is left over' if left else 'every counter has a partner'}."], qtype="explain", tags={"reasoning"}, r=r,
                diagram=Diagram("counters", {"n": n}, alt))
    it.check = FN("parity_reason", n=n)
    return it


@fam("012", mode="sa")
def oe_number(r, L):
    n = num_for(r, L)
    return Item(f"Is {n} odd or even?", par(n), [f"Count by 2s or look at the ones digit, {n % 10}.", f"{n} is {par(n)}."],
                [W(par(n + 1), "looked at the wrong digit")], FN("parity", n=n), qtype="conceptual", claim=f"Is {n} odd or even?")


@fam("012", mode="mc")
def oe_which(r, L):
    want = pick(r, ["even", "odd"])
    lo, hi = (2, 12) if L == 0 else (5, 20)
    good = pick(r, [x for x in range(lo, hi + 1) if par(x) == want])
    pool = [x for x in range(lo, hi + 1) if par(x) != want]
    r.shuffle(pool)
    bad = pool[:3]
    it = mc_key(f"Which number is {want}?", str(good), [str(b) for b in bad],
                [f"{'Even' if want == 'even' else 'Odd'} numbers end in {'0, 2, 4, 6, or 8' if want == 'even' else '1, 3, 5, 7, or 9'}.", f"{good} is {want}."], r=r)
    it.check = FN("parity_pick", want=want)
    return it


@fam("01")
def oe_count2(r, L):
    start = pick(r, [0, 2, 4, 6]) if L == 0 else pick(r, [1, 2, 3, 5, 6, 8, 9])
    seq = [start + 2 * i for i in range(5)]
    need(seq[-1] <= 20)
    k = r.randint(1, 4)
    shown = ", ".join("?" if i == k else str(v) for i, v in enumerate(seq))
    return Item(f"Count by 2s. What number is missing? {shown}", seq[k],
                [f"Each number is 2 more than the one before.", f"The missing number is {seq[k]}."],
                [W(seq[k] + 1, "counted by 1s"), W(seq[k] - 1, "counted by 1s"), W(seq[k] + 2, "skipped a number"), W(seq[k] + 10, "counted by 10s")],
                FN("skip_missing", seq=shown, step=2), qtype="procedural")


@fam("012", mode="mc")
def oe_story(r, L):
    n = num_for(r, max(L, 1))
    t = pick(r, ["{n} children need partners to play a game", "{n} socks need to be put into matching pairs", "{n} children line up two by two"])
    q = t.format(n=n)
    if n % 2:
        good = f"No. {n} is odd, so one is left over."
        bad = [f"Yes. {n} is even, so everyone has a partner.", f"Yes. Every number can be made into pairs.", f"No. {n} is even, so one is left over."]
    else:
        good = f"Yes. {n} is even, so everyone has a partner."
        bad = [f"No. {n} is odd, so one is left over.", "No. Numbers bigger than 10 cannot be made into pairs.", f"Yes. {n} is odd, so everyone has a partner."]
    it = mc_key(f"{q[0].upper() + q[1:]}. Can they all be put in pairs with none left over?", good, bad,
                [f"Make pairs or count by 2s to {n}.", good], qtype="word-problem", tags={"reasoning"}, r=r)
    it.check = FN("pairs_story", n=n)
    return it


@fam("2")
def oe_next(r, L):
    n = r.randint(5, 18)
    want = pick(r, ["even", "odd"])
    k = n + 1 if par(n + 1) == want else n + 2
    need(k <= 20)
    return Item(f"What is the next {want} number after {n}?", k, [f"Count up from {n}: {n + 1}, {n + 2}.", f"The next {want} number is {k}."],
                [W(n + 1 if k != n + 1 else n + 2, "chose a number that is not " + want), W(n + 2 if k != n + 2 else n + 3, "skipped a number"), W(n, "gave the starting number")],
                FN("next_parity", n=n, want=want), qtype="conceptual")


@fam("2", mode="mc")
def oe_ones(r, L):
    n = r.randint(11, 19)
    t = 10 * (n // 10)
    good = f"{par(n)}. The ones digit, {n % 10}, is {par(n)}."
    bad = [f"{'odd' if n // 10 % 2 else 'even'}. The tens digit, {n // 10}, is {'odd' if n // 10 % 2 else 'even'}." if par(n // 10) != par(n) else f"{par(n + 1)}. The tens digit, {n // 10}, is {par(n + 1)}.",
           f"{par(n + 1)}. The ones digit, {n % 10}, is {par(n + 1)}.", f"{par(n + 1)}. Numbers greater than 10 are always {par(n + 1)}."]
    it = mc_key(f"{name(r)} has {n} toy blocks. Is the number odd or even? Choose the best reason.", good, bad,
                [f"{t} blocks make {t // 2} pairs. Look at the other {n % 10}.", good], qtype="explain", tags={"reasoning"}, r=r)
    it.check = FN("parity_digit", n=n)
    return it


# ============================================================== S2 Even Numbers as Doubles
def even_n(r, L):
    return r.randint(2, 6) * 2 if L == 0 else r.randint(4, 10) * 2 if L == 1 else r.randint(6, 10) * 2


@fam("012")
def db_write(r, L):
    n = even_n(r, L)
    h = n // 2
    return Item(f"Write {n} as the sum of two equal addends.", f"{h} + {h}",
                [f"Split {n} into two equal groups.", f"{h} + {h} = {n}."],
                [W(f"{h + 1} + {h - 1}", "the addends are not equal"), W(f"{n} + {n}", "doubled the number"), W(f"10 + {n - 10}" if n > 10 else f"{n - 1} + 1", "the addends are not equal")],
                FN("equal_addends", n=n), qtype="procedural", claim=f"{n} as two equal addends")


@fam("012")
def db_blank(r, L):
    n = even_n(r, L)
    return Item(f"The same number goes in both blanks. ___ + ___ = {n}. What is the number?", n // 2,
                [f"Find the double that makes {n}.", f"{n // 2} + {n // 2} = {n}."],
                [W(n, "used the total"), W(n // 2 + 1, "the addends do not make the total"), W(2 * n, "doubled the total"), W(n - 2, "subtracted 2")],
                FN("half_of", n=n), qtype="fill-blank")


@fam("012")
def db_pic(r, L):
    n = even_n(r, L)
    alt = f"{n} counters in two rows of {n // 2}."
    return Item("Write an equation with two equal addends that shows the number of counters.", f"{n // 2} + {n // 2} = {n}",
                [f"Each row has {n // 2} counters.", f"{n // 2} + {n // 2} = {n}."],
                [W(f"{n // 2} + {n // 2} = {n + 2}", "counted the total wrong"), W(f"{n // 2 + 1} + {n // 2 - 1} = {n}", "the addends are not equal")],
                FN("double_eq", n=n), qtype="visual", diagram=Diagram("counters", {"n": n, "layout": "pairs"}, alt))


@fam("012", mode="mc")
def db_which(r, L):
    n = even_n(r, L)
    h = n // 2
    good = f"{h} + {h}"
    bad = [f"{h + 1} + {h - 1}", f"{h} + {h + 1}", f"{n} + {n}" if L == 0 else f"{h - 2} + {h + 2}"]
    it = mc_key(f"Which shows {n} as the sum of two equal addends?", good, bad, [f"The two addends must be the same number and add to {n}.", f"{good} = {n}."], r=r)
    it.check = FN("equal_addends", n=n)
    return it


@fam("12", mode="mc")
def db_can(r, L):
    want_even = r.randint(6, 20)
    good = want_even if want_even % 2 == 0 else want_even + 1
    need(good <= 20)
    pool = [x for x in range(5, 20, 2) if x != good]
    r.shuffle(pool)
    it = mc_key("Which number can be written as the sum of two equal addends?", str(good), [str(x) for x in pool[:3]],
                ["Only even numbers can be split into two equal addends.", f"{good} = {good // 2} + {good // 2}."], qtype="conceptual", tags={"reasoning"}, r=r)
    it.check = FN("parity_pick", want="even")
    return it


@fam("012")
def db_share(r, L):
    n = even_n(r, L)
    nm1, nm2 = name(r), name(sub(r, 2))
    need(nm1 != nm2)
    t = pick(r, [("grapes", "share {n} grapes equally"), ("crayons", "split {n} crayons into two equal piles"), ("stickers", "share {n} stickers equally")])
    return Item(f"{nm1} and {nm2} {t[1].format(n=n)}. How many {t[0]} does each child get?", f"{n // 2} {t[0]}",
                [f"Find the double that makes {n}: ___ + ___ = {n}.", f"{n // 2} + {n // 2} = {n}, so each child gets {n // 2} {t[0]}."],
                [W(f"{n} {t[0]}", "gave the total"), W(f"{n // 2 + 1} {t[0]}", "the two shares are not equal"), W(f"{2 * n} {t[0]}", "doubled the total")],
                FN("half_of", n=n, unit=t[0]), qtype="word-problem", tags={"modeling"})


@fam("2", mode="mc")
def db_error(r, L):
    n = r.randint(5, 9) * 2 + 1
    h = n // 2
    good = f"No. {n} is odd, so it cannot be two equal addends; {h} + {h} = {2 * h}."
    bad = [f"Yes. {h} + {h} = {n}.", f"Yes. Every number is a double.", f"No. It should be {h + 1} + {h + 1}."]
    nm = name(r)
    it = mc_key(f"{nm} says {n} = {h} + {h}. Is {nm} right?", good, bad, [f"{h} + {h} = {2 * h}, not {n}.", f"{n} is odd."], qtype="error-analysis", tags={"misconception"}, r=r)
    it.check = FN("odd_double", n=n)
    return it


@fam("2")
def db_fill(r, L):
    h = r.randint(4, 10)
    n = 2 * h
    k = r.randint(1, h - 1)
    eq = f"{n} = {h} + ___ + {k}"
    return Item(f"{n} is the double {h} + {h}. What number makes this true? {eq}", h - k,
                [f"{h} + {h} = {n}, so the second {h} is split into ___ and {k}.", f"{h - k} + {k} = {h}, so the number is {h - k}."],
                [W(h, "used the double without splitting"), W(n - k, "subtracted from the total only"), W(h - k + 1, "made a counting mistake")],
                FN("blank_eq", eq=eq), qtype="explain", tags={"reasoning"})


# ============================================================== S3 Arrays and Repeated Addition
def rc(r, L):
    if L == 0:
        a, b = r.randint(2, 4), r.randint(2, 5)
    else:
        a, b = r.randint(2, 5), r.randint(2, 5)
    need(L < 2 or a * b >= 9)
    return a, b


def rep(n, k):
    return " + ".join([str(n)] * k)


def arr_wrongs(rows, cols):
    t = rows * cols
    return [W(rows + cols, "added the number of rows and the number in each row"), W(t - cols, "left out a row"), W(t + cols, "added an extra row"),
            W(2 * rows + 2 * cols - 4, "counted only the dots on the outside")]


@fam("012")
def ar_total(r, L):
    a, b = rc(r, L)
    alt = f"An array of dots with {a} rows and {b} dots in each row."
    return Item("How many dots are in the array?", a * b, [f"There are {a} rows of {b}.", f"{rep(b, a)} = {a * b}."],
                arr_wrongs(a, b), EX(rep(b, a)), qtype="visual", diagram=Diagram("array3", {"rows": a, "cols": b}, alt))


@fam("012")
def ar_eq(r, L):
    a, b = rc(r, L)
    need(a != b)
    alt = f"An array of dots with {a} rows and {b} dots in each row."
    return Item("Write an addition equation with equal addends to find the total. Add the rows.", f"{rep(b, a)} = {a * b}",
                [f"Each row has {b} dots and there are {a} rows.", f"{rep(b, a)} = {a * b}."],
                [W(f"{a} + {b} = {a + b}", "added the rows and the number in each row"), W(f"{rep(b, a - 1)} = {(a - 1) * b}" if a > 2 else f"{b} = {b}", "left out a row")],
                FN("rep_eq", rows=a, cols=b, by="rows"), qtype="visual", diagram=Diagram("array3", {"rows": a, "cols": b}, alt))


@fam("012", mode="mc")
def ar_which(r, L):
    a, b = rc(r, L)
    need(a != b)
    good = f"{rep(b, a)} = {a * b}"
    bad = [f"{a} + {b} = {a + b}", f"{rep(b, a + 1)} = {(a + 1) * b}", f"{rep(a, a)} = {a * a}"]
    alt = f"An array of dots with {a} rows and {b} dots in each row."
    it = mc_key("Which equation matches the array? Add the rows.", good, bad, [f"There are {a} rows of {b}.", good + "."], qtype="visual",
                diagram=Diagram("array3", {"rows": a, "cols": b}, alt), r=r)
    it.check = FN("rep_eq", rows=a, cols=b, by="rows")
    return it


@fam("012")
def ar_build(r, L):
    a, b = rc(r, L)
    return Item(f"An array has {a} rows. There are {b} dots in each row. How many dots are there in all?", a * b,
                [f"Add {b} for each of the {a} rows.", f"{rep(b, a)} = {a * b}."], arr_wrongs(a, b), EX(rep(b, a)), qtype="procedural",
                claim=f"{a} rows of {b} dots in all")


@fam("12")
def ar_cols(r, L):
    a, b = rc(r, L)
    need(a != b)
    alt = f"An array of dots with {a} rows and {b} dots in each row."
    return Item("Write an addition equation with equal addends to find the total. This time, add the columns.", f"{rep(a, b)} = {a * b}",
                [f"There are {b} columns and each column has {a} dots.", f"{rep(a, b)} = {a * b}."],
                [W(f"{rep(b, a)} = {a * b}", "added the rows instead of the columns"), W(f"{a} + {b} = {a + b}", "added the rows and the columns")],
                FN("rep_eq", rows=a, cols=b, by="cols"), qtype="visual", diagram=Diagram("array3", {"rows": a, "cols": b}, alt))


@fam("012")
def ar_rows(r, L):
    a, b = rc(r, L)
    need(a != b)
    alt = f"An array of dots with {a} rows and {b} dots in each row."
    return Item("How many rows are in the array, and how many dots are in each row?", f"{a} rows of {b}",
                [f"Rows go across. Count the rows: {a}.", f"Each row has {b} dots, so it is {a} rows of {b}."],
                [W(f"{b} rows of {a}", "mixed up rows and columns"), W(f"{a} rows of {a * b}", "gave the total as the row size")],
                FN("rows_of", rows=a, cols=b), qtype="visual", diagram=Diagram("array3", {"rows": a, "cols": b}, alt))


@fam("2")
def ar_missing(r, L):
    a, b = rc(r, 2)
    return Item(f"An array has {a * b} dots in {a} equal rows. How many dots are in each row?", b,
                [f"Find the number that adds {a} times to make {a * b}.", f"{rep(b, a)} = {a * b}, so each row has {b} dots."],
                [W(a * b - a, "subtracted the number of rows"), W(a, "gave the number of rows"), W(b + 1, "made a counting mistake")],
                FN("rep_unknown", total=a * b, times=a), qtype="explain", tags={"reasoning"})


@fam("12", mode="mc")
def ar_same(r, L):
    a, b = rc(r, L)
    need(a != b)
    good = f"{b} rows of {a}"
    bad = [f"{a} rows of {a}", f"{b} rows of {b}", f"{a} rows of {b + 1}" if b < 5 else f"{a - 1} rows of {b}"]
    need(len({good} | set(bad)) == 4)
    it = mc_key(f"Which array has the same number of dots as {a} rows of {b}?", good, bad,
                [f"{a} rows of {b} is {rep(b, a)} = {a * b}.", f"{b} rows of {a} is {rep(a, b)} = {a * b} too."], qtype="conceptual", tags={"reasoning"}, r=r)
    it.check = FN("same_array", total=a * b)
    return it


@fam("012")
def ar_split(r, L):
    a, b = rc(r, L)
    need(a >= 3)
    k = r.randint(1, a - 1)
    alt = f"An array of dots with {a} rows and {b} dots in each row. A dashed line splits it into {pl(k, 'row')} on top and {pl(a - k, 'row')} on the bottom."
    return Item(f"The array is split into two parts. The top part is {k} rows of {b}. The bottom part is {a - k} rows of {b}. How many dots are there in all?", a * b,
                [f"Top: {k * b} dots. Bottom: {(a - k) * b} dots.", f"{k * b} + {(a - k) * b} = {a * b}."],
                arr_wrongs(a, b) + [W(k * b, "counted only the top part")], EX(f"({rep(b, k)})+({rep(b, a - k)})"), qtype="visual", tags={"multiple-representations"},
                diagram=Diagram("array3", {"rows": a, "cols": b, "split_row": k}, alt))


@fam("12", mode="mc")
def ar_more(r, L):
    a, b = rc(r, L)
    c, d = rc(r, L)
    need(a * b != c * d and {a, b} != {c, d})
    big, small = ((a, b), (c, d)) if a * b > c * d else ((c, d), (a, b))
    good = f"{big[0]} rows of {big[1]}, because it has {big[0] * big[1]} dots"
    bad = [f"{small[0]} rows of {small[1]}, because it has {small[0] * small[1]} dots", f"{small[0]} rows of {small[1]}, because it has {big[0] * big[1]} dots",
           f"{big[0]} rows of {big[1]}, because it has {big[0] + big[1]} dots"]
    it = mc_key(f"Which array has more dots: {a} rows of {b} or {c} rows of {d}?", good, bad,
                [f"{a} rows of {b}: {rep(b, a)} = {a * b}. {c} rows of {d}: {rep(d, c)} = {c * d}.", good + "."], qtype="compare-strategies", tags={"reasoning"}, r=r)
    it.check = FN("more_array", arrays=[[a, b], [c, d]])
    return it


@fam("2")
def ar_two(r, L):
    a, b = rc(r, 2)
    c = r.randint(2, 5)
    need(c != b)
    return Item(f"One array has {a} rows of {b}. Another array has {a} rows of {c}. How many dots are in both arrays together?", a * b + a * c,
                [f"{rep(b, a)} = {a * b} and {rep(c, a)} = {a * c}.", f"{a * b} + {a * c} = {a * b + a * c}."],
                [W(a * b, "counted only one array"), W(a * (b + c) + b, "added an extra row"), W(a + b + c, "added the numbers in the problem")],
                EX(f"({rep(b, a)})+({rep(c, a)})"), qtype="multi-step", tags={"multistep"})


# ============================================================== S4 Array Word Problems
THINGS = [("a garden", "carrots"), ("a box", "crayons"), ("a tray", "muffins"), ("a sheet", "stickers"), ("a classroom", "desks"), ("a parking lot", "cars"),
          ("a pan", "cookies"), ("a carton", "eggs")]


@fam("012")
def aw_story(r, L):
    a, b = rc(r, L)
    pl_, it_ = pick(r, THINGS)
    return Item(f"In {pl_}, there are {a} rows of {it_} with {b} {it_} in each row. How many {it_} are there?", f"{a * b} {it_}",
                [f"Add {b} for each of the {a} rows.", f"{rep(b, a)} = {a * b} {it_}."],
                [W(f"{w} {it_}", y) for w, y in arr_wrongs(a, b)], EX(rep(b, a), unit=it_), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def aw_eq(r, L):
    a, b = rc(r, L)
    need(a != b)
    pl_, it_ = pick(r, THINGS)
    good = f"{rep(b, a)} = {a * b}"
    bad = [f"{a} + {b} = {a + b}", f"{rep(a, a)} = {a * a}", f"{rep(b, a)} = {a * b + b}"]
    it = mc_key(f"{name(r)} puts {it_} in {a} rows with {b} in each row. Which equation shows how many {it_} there are?", good, bad,
                [f"Add {b} once for each row.", good + "."], qtype="word-problem", tags={"modeling"}, r=r)
    it.check = FN("rep_eq", rows=a, cols=b, by="rows")
    return it


@fam("12")
def aw_compare(r, L):
    a, b = rc(r, L)
    c, d = rc(r, L)
    need(a * b != c * d)
    n1, n2 = name(r), name(sub(r, 4))
    need(n1 != n2)
    big = n1 if a * b > c * d else n2
    diff = abs(a * b - c * d)
    return Item(f"{n1} has {a} rows of {b} stamps. {n2} has {c} rows of {d} stamps. How many more stamps does {big} have?", f"{diff} stamps",
                [f"{n1}: {rep(b, a)} = {a * b}. {n2}: {rep(d, c)} = {c * d}.", f"{max(a * b, c * d)} − {min(a * b, c * d)} = {diff} stamps."],
                [W(f"{a * b + c * d} stamps", "added the two totals"), W(f"{abs(a + b - c - d)} stamps" if abs(a + b - c - d) != diff else f"{diff + 1} stamps", "added rows and row sizes"), W(f"{max(a * b, c * d)} stamps", "gave one total")],
                EX(f"{max(a * b, c * d)}-{min(a * b, c * d)}" if False else (f"({rep(b, a)})-({rep(d, c)})" if a * b > c * d else f"({rep(d, c)})-({rep(b, a)})"), unit="stamps"),
                qtype="multi-step", tags={"multistep"})


@fam("012")
def aw_rows_needed(r, L):
    a, b = rc(r, L)
    t = pick(r, [("chairs", "Each row has {b} chairs"), ("plants", "Each row has {b} plants")])
    return Item(f"{name(r)} sets up {a * b} {t[0]} in equal rows. {t[1].format(b=b)}. How many rows are there?", f"{a} rows",
                [f"Add {b} again and again until you reach {a * b}: {rep(b, a)}.", f"That is {a} groups of {b}, so there are {a} rows."],
                [W(f"{b} rows", "gave the number in each row"), W(f"{a * b - b} rows", "subtracted one row"), W(f"{a + 1} rows", "counted one extra row")],
                FN("rep_unknown", total=a * b, times=b, unit="rows"), qtype="word-problem", tags={"modeling"})


@fam("2")
def aw_add_row(r, L):
    a, b = rc(r, 2)
    need(a < 5)
    return Item(f"A tray has {a} rows of muffins with {b} muffins in each row. The baker adds 1 more row of {b}. How many muffins are on the tray now?", f"{(a + 1) * b} muffins",
                [f"Now there are {a + 1} rows of {b}.", f"{rep(b, a + 1)} = {(a + 1) * b} muffins."],
                [W(f"{a * b} muffins", "forgot the new row"), W(f"{a * b + 1} muffins", "added one muffin instead of one row"), W(f"{a + 1 + b} muffins", "added rows and row size")],
                EX(rep(b, a + 1), unit="muffins"), qtype="multi-step", tags={"multistep"})


@fam("012")
def aw_empty(r, L):
    a, b = rc(r, L)
    k = r.randint(2, a * b - 2)
    return Item(f"A room has {a} rows of seats with {b} seats in each row. {k} children are sitting. How many seats are empty?", f"{a * b - k} seats",
                [f"Seats: {rep(b, a)} = {a * b}.", f"{a * b} − {k} = {a * b - k} seats."],
                [W(f"{a * b} seats", "gave all the seats"), W(f"{a * b + k} seats", "added the children"), W(f"{a + b - k if a + b > k else a * b - k + 1} seats", "added rows and seats in a row")],
                EX(f"({rep(b, a)})-{k}", unit="seats"), qtype="multi-step", tags={"multistep"})


@fam("01")
def aw_pic(r, L):
    a, b = rc(r, L)
    t = pick(r, [("eggs", "carton"), ("cupcakes", "box"), ("buttons", "card")])
    alt = f"A {t[1]} of {t[0]} shown as an array with {a} rows and {b} in each row."
    return Item(f"The picture shows a {t[1]} of {t[0]}. How many {t[0]} are there?", f"{a * b} {t[0]}",
                [f"There are {a} rows of {b}.", f"{rep(b, a)} = {a * b} {t[0]}."], [W(f"{w} {t[0]}", y) for w, y in arr_wrongs(a, b)],
                EX(rep(b, a), unit=t[0]), qtype="visual", diagram=Diagram("array3", {"rows": a, "cols": b}, alt))


SKILLS = {
    1: dict(name="Odd and Even Numbers", fams=[oe_pairs, oe_pairs_mc, oe_number, oe_which, oe_count2, oe_story, oe_next, oe_ones]),
    2: dict(name="Even Numbers as Doubles", fams=[db_write, db_blank, db_pic, db_which, db_can, db_share, db_error, db_fill]),
    3: dict(name="Arrays and Repeated Addition", fams=[ar_total, ar_eq, ar_which, ar_build, ar_cols, ar_rows, ar_missing, ar_same, ar_split, ar_more, ar_two]),
    4: dict(name="Array Word Problems", fams=[aw_story, aw_eq, aw_compare, aw_rows_needed, aw_add_row, aw_empty, aw_pic]),
}
