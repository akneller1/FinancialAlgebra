"""Unit 1: Understanding Multiplication (multiplication-meaning)."""
from g3lib import *

UNIT_ID = "multiplication-meaning"

THINGS = [("bags", "apples"), ("boxes", "crayons"), ("vases", "flowers"), ("plates", "cookies"), ("jars", "marbles"),
          ("baskets", "eggs"), ("packs", "stickers"), ("tables", "chairs"), ("trays", "muffins"), ("cups", "pencils")]


def gn(r, L, big=False):
    if L == 0:
        return r.randint(2, 5), r.randint(2, 5)
    if L == 1:
        return r.randint(3, 6 if not big else 9), r.randint(3, 8)
    return r.randint(4, 9), r.randint(4, 9)


def total_wrongs(g, n):
    return [W(g + n, "added the number of groups and the number in each group"),
            W(g * n - n, "missed one group when counting"), W(g * n + n, "counted one group twice"), W(n, "counted only one group")]


# ============================================================== S1 Equal Groups and Multiplication
@fam("012")
def eg_pic_total(r, L):
    g, n = gn(r, L)
    need(g <= 8 and n <= 9)
    lead = "Count the groups and the dots in each group. " if L == 0 else ""
    alt = f"{g} circles. Each circle has {n} dots."
    return Item(f"{lead}How many dots are there in all?", g * n,
                [f"There are {g} equal groups with {n} dots in each group.", f"{g} × {n} = {g * n}."],
                total_wrongs(g, n), EX(f"{g}*{n}"), qtype="visual", diagram=Diagram("groups", {"groups": g, "each": n}, alt))


@fam("012", mode="mc")
def eg_pic_expr(r, L):
    g, n = gn(r, L)
    need(g != n and g <= 8)
    good = f"{g} × {n}"
    bad = [f"{g} + {n}", f"{g} × {g}", f"{n} × {n}"] if L == 0 else [f"{g} + {n}", f"{g - 1} × {n}", f"{g} × {n + 1}"]
    alt = f"{g} circles. Each circle has {n} dots."
    return mc_key("Which multiplication expression matches the picture? (The first number tells how many groups.)" if L == 0 else
                  "Which expression tells how many groups and how many in each group?",
                  good, bad, [f"There are {g} groups.", f"Each group has {n} dots, so the expression is {g} × {n}."], qtype="visual",
                  diagram=Diagram("groups", {"groups": g, "each": n}, alt), r=r, why="added, or used the wrong number of groups")


@fam("012", mode="mc")
def eg_meaning(r, L):
    g, n = gn(r, L)
    need(g != n)
    good = f"{g} groups with {n} in each group"
    bad = [f"{g} groups with {g} in each group", f"{n} more than {g}", f"{g} groups with {g + n} in each group"]
    return mc_key(f"What does {g} × {n} mean?", good, bad,
                  [f"In {g} × {n}, the first factor {g} is the number of groups.", f"The second factor {n} is the number in each group."], r=r)


@fam("012", mode="mc")
def eg_story_expr(r, L):
    g, n = gn(r, L)
    need(g != n)
    a, b = pick(r, THINGS)
    nm = name(r)
    t = f"{nm} has {g} {a}. There are {n} {b} in each of the {a}."
    good = f"{g} × {n}"
    bad = [f"{g} + {n}", f"{g} × {g}", f"{g + n} × {n}"] if L < 2 else [f"{g} + {n}", f"{n} + {n}", f"{g} × {g}"]
    return mc_key(f"{t} Which expression shows how many {b} {nm} has?", good, bad,
                  [f"There are {g} equal groups ({a}) with {n} {b} in each group.", f"{g} groups of {n} is {g} × {n}."], qtype="word-problem", r=r)


@fam("012")
def eg_repeated(r, L):
    g, n = gn(r, L)
    need(2 <= g <= 7)
    ask = pick(r, ["groups", "value"]) if L else "value"
    s = " + ".join([str(n)] * g)
    if ask == "groups":
        it = Item(f"Complete the equation: {s} = ___ × {n}", g,
                  [f"Count the addends: there are {g} addends of {n}.", f"{s} = {g} × {n}."],
                  [W(n, "wrote the addend instead of the number of addends"), W(g * n, "found the total instead of the number of groups"), W(g + 1, "miscounted the addends")],
                  FN("repadd_groups", sum=s, addend=n), qtype="fill-blank", tags={"multiple-representations"})
    else:
        it = Item(f"Find the total. Write it as a multiplication equation in your head first: {s} = ?", g * n,
                  [f"There are {g} addends of {n}, so this is {g} × {n}.", f"{g} × {n} = {g * n}."],
                  total_wrongs(g, n)[:3], FN("repadd_value", sum=s), qtype="procedural", claim=f"{s} = ?")
    return it


@fam("12", mode="mc")
def eg_which_story(r, L):
    g, n = gn(r, L)
    need(g != n and g * n <= 81)
    a, b = pick(r, THINGS)
    good = f"{g} {a} with {n} {b} in each"
    bad = [f"{g} {b} and {n} more {b}", f"{g * n} {b} shared among {g} {a}", f"{n} {a} with {n} {b} in each"]
    return mc_key(f"Which situation can be solved with {g} × {n}?", good, bad,
                  [f"{g} × {n} means {g} equal groups with {n} in each group.", f"“{good}” is {g} groups of {n}."], qtype="explain",
                  tags={"reasoning"}, r=r)


@fam("12", mode="mc")
def eg_unequal(r, L):
    g, n = r.randint(3, 5), r.randint(3, 6)
    counts = [n] * g
    k = r.randrange(g)
    counts[k] = n + pick(r, [-1, 1])
    alt = f"{g} circles with " + ", ".join(map(str, counts)) + " dots."
    good = "No, because the groups are not equal."
    bad = [f"Yes, {g} × {n}", f"Yes, {g} × {counts[k]}", f"Yes, {g} + {n}"]
    return mc_key("Can the picture be shown with one multiplication expression? Choose the best answer.", good, bad,
                  ["Multiplication is for equal groups.", f"One group has {counts[k]} dots, not {n}, so the groups are not equal."],
                  qtype="visual", tags={"reasoning"}, diagram=Diagram("groups", {"counts": counts}, alt), r=r)


# ============================================================== S2 Arrays and Multiplication
def rc(r, L):
    if L == 0:
        return r.randint(2, 4), r.randint(2, 6)
    if L == 1:
        return r.randint(3, 6), r.randint(3, 9)
    return r.randint(4, 9), r.randint(5, 10)


@fam("01")
def ar_count(r, L):
    a, b = rc(r, L)
    need(a != b)
    lead = "Count the rows and how many dots are in each row. " if L == 0 else ""
    alt = f"An array of dots with {a} rows and {b} dots in each row."
    return Item(f"{lead}How many dots are in the array?", a * b, [f"The array has {a} rows of {b}.", f"{a} × {b} = {a * b}."],
                [W(a + b, "added the rows and the columns"), W(2 * a + 2 * b - 4, "counted only the dots around the edge"), W(a * b - b, "missed a row"), W(a * b + a, "counted an extra column")],
                EX(f"{a}*{b}"), qtype="visual", diagram=Diagram("array3", {"rows": a, "cols": b}, alt))


@fam("012", mode="mc")
def ar_equation(r, L):
    a, b = rc(r, L)
    need(a != b and a * b <= 90)
    good = f"{a} × {b} = {a * b}"
    bad = [f"{a} + {b} = {a + b}", f"{a} × {b} = {a * b + b}", f"{a} × {a} = {a * a}"]
    alt = f"An array of dots with {a} rows and {b} dots in each row."
    return mc_key("Which equation matches the array?", good, bad, [f"Count {a} rows with {b} dots in each row.", f"{a} × {b} = {a * b}."],
                  qtype="visual", diagram=Diagram("array3", {"rows": a, "cols": b}, alt), r=r)


@fam("012")
def ar_rows_missing(r, L):
    a, b = rc(r, L)
    need(a != b)
    ask = pick(r, ["rows", "each"])
    t = f"{name(r)} puts {a * b} chairs in an array. "
    if ask == "rows":
        q = t + f"There are {b} chairs in each row. How many rows are there?"
        ans, ex = a, f"{a * b}/{b}"
    else:
        q = t + f"There are {a} rows. How many chairs are in each row?"
        ans, ex = b, f"{a * b}/{a}"
    return Item(q, ans, [f"Think: {a} × {b} = {a * b}.", f"The answer is {ans}."],
                [W(a * b - (b if ask == 'rows' else a), "subtracted instead of dividing"), W(a + b, "added the two numbers"), W(ans + 1, "made a counting error"), W(a * b, "gave the total")],
                EX(ex), qtype="word-problem", tags={"connections"})


@fam("01")
def ar_story(r, L):
    a, b = rc(r, L)
    ctx = pick(r, [("A garden has {a} rows of plants with {b} plants in each row. How many plants are in the garden?", "plants"),
                   ("A box of chocolates has {a} rows with {b} chocolates in each row. How many chocolates are in the box?", "chocolates"),
                   ("The class lines up in {a} rows with {b} students in each row. How many students are there?", "students"),
                   ("A sheet of stamps has {a} rows of {b} stamps. How many stamps are on the sheet?", "stamps")])
    return Item(ctx[0].format(a=a, b=b), f"{a * b} {ctx[1]}", [f"An array with {a} rows of {b}.", f"{a} × {b} = {a * b} {ctx[1]}."],
                [W(f"{a + b} {ctx[1]}", "added the rows and the number in each row"), W(f"{a * b - b} {ctx[1]}", "missed a row"), W(f"{a * b + a} {ctx[1]}", "counted an extra column")],
                EX(f"{a}*{b}", unit=ctx[1]), qtype="word-problem", tags={"modeling"})


@fam("12", mode="mc")
def ar_two_ways(r, L):
    a, b = rc(r, L)
    need(a != b)
    good = f"{a} rows of {b}, or {b} columns of {a}"
    bad = [f"{a} rows of {a}, or {b} columns of {b}", f"{a} + {b} dots in all", f"{b} rows of {b}, or {a} columns of {b}"]
    alt = f"An array of dots with {a} rows and {b} dots in each row."
    return mc_key("Which description of the array is correct?", good, bad, [f"Each row has {b} dots and there are {a} rows.", f"Each column has {a} dots and there are {b} columns."],
                  qtype="visual", tags={"multiple-representations"}, diagram=Diagram("array3", {"rows": a, "cols": b}, alt), r=r)


@fam("2")
def ar_fix_array(r, L):
    a, b = r.randint(3, 6), r.randint(4, 8)
    add = pick(r, [1, 2])
    nm = name(r)
    return Item(f"{nm} has an array with {a} rows of {b} tiles. {nm} adds {add} more {'row' if add == 1 else 'rows'} of {b}. How many tiles are in the new array?",
                (a + add) * b, [f"The new array has {a} + {add} = {a + add} rows of {b}.", f"{a + add} × {b} = {(a + add) * b}."],
                [W(a * b + add, "added only one tile for each new row"), W(a * b, "forgot the new rows"), W((a + add) * (b + add), "added to both the rows and the columns")],
                EX(f"({a}+{add})*{b}"), qtype="multi-step", tags={"multistep"})


# ============================================================== S3 Multiplying by 2, 5, and 10
def two_five_ten(r, L):
    k = pick(r, [2, 5, 10]) if L else pick(r, [2, 5, 10, 2, 10])
    m = r.randint(1, 5) if L == 0 else r.randint(2, 10)
    return k, m


@fam("012")
def f_fact(r, L):
    k, m = two_five_ten(r, L)
    a, b = (k, m) if r.random() < 0.5 else (m, k)
    need(a * b > 4)
    return Item(f"Multiply: {a} × {b}", a * b, [f"Skip count by {k}s {m} {'time' if m == 1 else 'times'}.", f"{a} × {b} = {a * b}."],
                [W(a + b, "added instead of multiplying"), W(a * b + k, "skip counted one extra time"), W(a * b - k, "skip counted one time too few"),
                 W(a * b * 10 if k == 5 else a * b + 10, "added a zero to a 5s fact" if k == 5 else "made a skip-counting error")],
                EX(f"{a}*{b}"), qtype="procedural", claim=f"{a} × {b}")


@fam("012")
def f_skip_line(r, L):
    k = pick(r, [2, 5, 10])
    m = r.randint(3, 6) if L == 0 else r.randint(4, 10)
    seq = [k * i for i in range(1, m + 1)]
    hide = r.randrange(1, m) if L else m - 1
    shown = ", ".join("?" if i == hide else str(v) for i, v in enumerate(seq))
    return Item(f"Skip count by {k}s: {shown}. What number goes where the ? is?", seq[hide],
                [f"Each number is {k} more than the one before.", f"The missing number is {seq[hide]} = {hide + 1} × {k}."],
                [W(seq[hide] + 1, "counted by 1 instead of by " + str(k)), W(seq[hide] + k, "skipped a number"), W(seq[hide] - 1, "counted back by 1")],
                FN("skip_missing", seq=shown, step=k), qtype="fill-blank", tags={"reasoning"})


@fam("01")
def f_coins(r, L):
    k, coin = pick(r, [(5, "nickels"), (10, "dimes")])
    m = r.randint(2, 5) if L == 0 else r.randint(4, 9)
    return Item(f"{name(r)} has {m} {coin}. Each one is worth {k} cents. How many cents is that?", f"{m * k} cents",
                [f"Skip count by {k}s {m} times.", f"{m} × {k} = {m * k} cents."],
                [W(f"{m + k} cents", "added instead of multiplying"), W(f"{m * k - k} cents", "skip counted one time too few"), W(f"{m} cents", "counted coins, not cents")],
                EX(f"{m}*{k}", unit="cents"), qtype="word-problem", tags={"connections"})


@fam("12")
def f_hands(r, L):
    things = pick(r, [(2, "pairs of socks", "socks"), (5, "hands", "fingers"), (10, "packs of 10 pencils", "pencils"), (2, "bikes", "wheels"), (5, "nickels", "cents")])
    k, grp, unit = things
    m = r.randint(3, 10)
    return Item(f"There are {m} {grp}. How many {unit} are there? ({'Each has' if k != 10 else 'Each pack has'} {k}.)", f"{m * k} {unit}",
                [f"{m} groups of {k}.", f"{m} × {k} = {m * k} {unit}."],
                [W(f"{m + k} {unit}", "added instead of multiplying"), W(f"{m * k + k} {unit}", "counted one extra group"), W(f"{m * k - k} {unit}", "missed a group")],
                EX(f"{m}*{k}", unit=unit), qtype="word-problem")


@fam("012", mode="mc")
def f_pattern(r, L):
    k = pick(r, [2, 5, 10])
    good = {2: "They are all even.", 5: "They end in 0 or 5.", 10: "They end in 0."}[k]
    bad = [x for x in ["They are all even.", "They end in 0 or 5.", "They end in 0.", "They are all odd.", "They end in 5."] if x != good]
    if k == 2:
        bad = ["They are all odd.", "They end in 0 or 5.", "They end in 5."]
    if k == 10:
        bad = ["They end in 5.", "They are all odd.", "They end in 1."]
    if k == 5:
        bad = ["They end in 0.", "They are all odd.", "They are all even."]
    m = r.randint(3, 6)
    ex = ", ".join(str(k * i) for i in range(1, m + 1))
    return mc_key(f"Look at these products of {k}: {ex}. What pattern is true for every product of {k}?", good, bad,
                  [f"Skip count by {k}s and look at the ones digits.", good], qtype="conceptual", tags={"reasoning"}, r=r)


@fam("2")
def f_five_from_ten(r, L):
    m = r.randint(3, 10)
    return Item(f"{m} × 10 = {m * 10}. Use this fact to find {m} × 5.", m * 5,
                [f"5 is half of 10, so {m} × 5 is half of {m} × 10.", f"Half of {m * 10} is {m * 5}."],
                [W(m * 10, "used the 10s fact without halving"), W(m * 10 - 5, "subtracted 5 instead of halving"), W(m + 5, "added instead of multiplying")],
                EX(f"{m}*5"), qtype="compare-strategies", tags={"reasoning", "connections"})


# ============================================================== S4 Multiplication Word Problems
CTX = [("{nm} buys {g} packs of juice boxes. Each pack has {n} juice boxes. How many juice boxes does {nm} buy?", "juice boxes"),
       ("There are {g} tables in the art room. Each table has {n} chairs. How many chairs are there?", "chairs"),
       ("{nm} reads {n} pages every day for {g} days. How many pages does {nm} read?", "pages"),
       ("A spider has 8 legs. How many legs do {g} spiders have?", "legs"),
       ("Each ribbon is {n} feet long. {nm} has {g} ribbons. How many feet of ribbon is that?", "feet"),
       ("{nm} plants {g} rows of seeds with {n} seeds in each row. How many seeds does {nm} plant?", "seeds"),
       ("A bus ride costs {n} dollars. How much do {g} bus rides cost?", "dollars"),
       ("Each tray holds {n} muffins. How many muffins fit on {g} trays?", "muffins"),
       ("Each team has {n} players. How many players are on {g} teams?", "players")]


def word_mult(r, L, tmpl=None):
    g, n = gn(r, L, True)
    t, unit = tmpl or pick(r, CTX)
    if "8 legs" in t:
        n = 8
    nm = name(r)
    return t.format(g=g, n=n, nm=nm), unit, g, n


@fam("01")
def w_basic(r, L):
    q, unit, g, n = word_mult(r, L)
    need(g * n <= 100)
    return Item(q, f"{g * n} {unit}", [f"There are {g} equal groups of {n}.", f"{g} × {n} = {g * n} {unit}."],
                [W(f"{g + n} {unit}", "added the two numbers"), W(f"{g * n - n} {unit}", "missed one group"), W(f"{g * n + n} {unit}", "counted an extra group")],
                EX(f"{g}*{n}", unit=unit), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def w_equation(r, L):
    q, unit, g, n = word_mult(r, L)
    need(g != n)
    good = f"{g} × {n} = ?"
    bad = [f"{g} + {n} = ?", f"{g * n} ÷ {n} = ?", f"{n} − {g} = ?" if n > g else f"{g} − {n} = ?"]
    return mc_key(q.replace("How many", "Which equation can you use to find how many").replace("How much", "Which equation can you use to find how much") if L else q + " Which equation can you use?",
                  good, bad, [f"{g} equal groups with {n} in each group means multiply.", f"{good}"], qtype="word-problem", r=r)


@fam("012")
def w_tape(r, L):
    g, n = gn(r, L, True)
    need(g * n <= 90 and g >= 3)
    unit = pick(r, ["stickers", "beads", "cards"])
    alt = f"A tape diagram with {g} equal parts. Each part is labeled {n}. The total is labeled with a question mark."
    lead = f"Each of {g} friends has {n} {unit}. " if L == 0 else f"The tape diagram shows a story about {unit}. "
    return Item(lead + "What is the total?", f"{g * n} {unit}", [f"The diagram has {g} parts of {n}.", f"{g} × {n} = {g * n} {unit}."],
                [W(f"{g + n} {unit}", "added the number of parts and the size of a part"), W(f"{n} {unit}", "gave the size of one part"), W(f"{g * n - n} {unit}", "missed one part")],
                EX(f"{g}*{n}", unit=unit), qtype="visual", diagram=Diagram("tape", {"parts": g, "each": str(n), "total_label": "?"}, alt))


@fam("12")
def w_measure(r, L):
    n = r.randint(3, 9)
    g = r.randint(3, 9)
    t = pick(r, [("A board is cut into {g} pieces. Each piece is {n} inches long. How long was the board?", "inches"),
                 ("{nm} walks {n} blocks to school and the same back home, every school day for {g} trips. How many blocks are all {g} trips?", "blocks"),
                 ("A jug holds {n} liters. How many liters do {g} full jugs hold?", "liters")])
    q = t[0].format(g=g, n=n, nm=name(r))
    return Item(q, f"{g * n} {t[1]}", [f"There are {g} equal groups of {n}.", f"{g} × {n} = {g * n} {t[1]}."],
                [W(f"{g + n} {t[1]}", "added instead of multiplying"), W(f"{g * n + n} {t[1]}", "counted an extra piece"), W(f"{n} {t[1]}", "gave one piece")],
                EX(f"{g}*{n}", unit=t[1]), qtype="word-problem", tags={"modeling"})


@fam("2")
def w_compare_two(r, L):
    g1, n1 = r.randint(3, 6), r.randint(4, 8)
    g2, n2 = r.randint(3, 6), r.randint(4, 8)
    need(g1 * n1 != g2 * n2 and (g1, n1) != (g2, n2))
    a, b = name(r), name(sub(r, 1))
    need(a != b)
    win = a if g1 * n1 > g2 * n2 else b
    diff = abs(g1 * n1 - g2 * n2)
    return Item(f"{a} has {g1} boxes with {n1} crayons in each. {b} has {g2} boxes with {n2} crayons in each. How many more crayons does {win} have?",
                f"{diff} crayons", [f"{a}: {g1} × {n1} = {g1 * n1}. {b}: {g2} × {n2} = {g2 * n2}.", f"{max(g1 * n1, g2 * n2)} − {min(g1 * n1, g2 * n2)} = {diff} crayons."],
                [W(f"{g1 * n1 + g2 * n2} crayons", "added the two totals"), W(f"{abs(g1 - g2) + abs(n1 - n2)} crayons", "compared the factors instead of the products"),
                 W(f"{max(g1 * n1, g2 * n2)} crayons", "gave one total instead of the difference")],
                EX(f"{g1}*{n1}-{g2}*{n2}" if g1 * n1 > g2 * n2 else f"{g2}*{n2}-{g1}*{n1}", unit="crayons"),
                qtype="multi-step", tags={"multistep"})


@fam("2", mode="mc")
def w_choose_op(r, L):
    g, n = r.randint(3, 8), r.randint(3, 8)
    need(g != n)
    a, b = pick(r, THINGS)
    good = f"{g} × {n} = {g * n}, because there are {g} equal groups of {n}"
    bad = [f"{g} + {n} = {g + n}, because you put the {a} together", f"{g} × {n} = {g * n + n}, because you count one more group",
           f"{g * n} ÷ {g} = {n}, because you share the {b}"]
    return mc_key(f"There are {g} {a} with {n} {b} in each. How many {b} are there in all? Which answer and reason are correct?", good, bad,
                  [f"The {a} are equal groups.", f"{g} × {n} = {g * n} {b}."], qtype="explain", tags={"reasoning"}, r=r)


@fam("2")
def ar_missing_part(r, L):
    a, b = r.randint(4, 8), r.randint(5, 9)
    hide = r.randint(2, a - 1)
    alt = f"An array with {a} rows and {b} dots in each row. A card covers some rows; only {a - hide} rows of {b} can be seen."
    return Item(f"{name(r)} made an array with {a} rows of {b} dots. A card covers some of the rows, so only {a - hide} rows show. How many dots are hidden under the card?",
                hide * b, [f"The whole array has {a} × {b} = {a * b} dots. You can see {a - hide} × {b} = {(a - hide) * b}.", f"Hidden: {hide} rows of {b} = {hide * b} dots."],
                [W(a * b, "found the whole array"), W((a - hide) * b, "found the dots that show"), W(hide, "found the hidden rows, not the dots")],
                EX(f"({a}-{a - hide})*{b}"), qtype="multi-step", tags={"multistep", "reasoning"})


@fam("2", mode="mc")
def ar_not_array(r, L):
    a, b = r.randint(3, 6), r.randint(4, 9)
    need(a != b)
    good = f"{a} rows of {b} and 1 row of {b - 1}"
    bad = [f"{a} rows of {b}", f"{b} rows of {a}", f"{a + 1} rows of {b}"]
    return mc_key(f"Which of these is NOT an array that can be shown with one multiplication fact?", good, bad,
                  ["In an array every row has the same number.", f"“{good}” has one row that is different."], qtype="conceptual", tags={"reasoning"}, r=r)


@fam("2")
def f_two_facts(r, L):
    m, n = r.randint(3, 9), r.randint(3, 9)
    need(m != n)
    return Item(f"{name(r)} has {m} nickels and {n} dimes. A nickel is 5 cents and a dime is 10 cents. How many cents is that?", f"{m * 5 + n * 10} cents",
                [f"Nickels: {m} × 5 = {m * 5} cents. Dimes: {n} × 10 = {n * 10} cents.", f"{m * 5} + {n * 10} = {m * 5 + n * 10} cents."],
                [W(f"{(m + n) * 5} cents", "counted every coin as 5 cents"), W(f"{(m + n) * 10} cents", "counted every coin as 10 cents"), W(f"{m + n} cents", "counted the coins, not the cents")],
                EX(f"{m}*5+{n}*10", unit="cents"), qtype="multi-step", tags={"multistep"})


@fam("2", mode="mc")
def f_which_true(r, L):
    k = pick(r, [2, 5, 10]); m = r.randint(3, 9)
    good = f"{m} × {k} = {k} × {m}"
    bad = [f"{m} × {k} = {m} + {k}", f"{m} × 5 = {m} × 10", f"{m} × {k} = {m * k + k}"]
    return mc_key("Which equation is true?", good, bad, [f"{m} × {k} = {m * k} and {k} × {m} = {m * k}.", "Turning the factors around does not change the product."],
                  qtype="explain", tags={"reasoning"}, r=r)


@fam("2")
def w_left_over(r, L):
    g, n = r.randint(4, 8), r.randint(4, 9)
    give = r.randint(3, g * n - 5)
    return Item(f"{name(r)} buys {g} packs of stickers with {n} stickers in each pack. {name(sub(r, 2))} gets {give} of them. How many stickers are left?",
                f"{g * n - give} stickers", [f"First find the total: {g} × {n} = {g * n}.", f"Then subtract: {g * n} − {give} = {g * n - give} stickers."],
                [W(f"{g * n} stickers", "stopped after the first step"), W(f"{g * n + give} stickers", "added instead of subtracting"), W(f"{g + n - give if g + n > give else give - g - n} stickers", "added the factors instead of multiplying")],
                EX(f"{g}*{n}-{give}", unit="stickers"), qtype="multi-step", tags={"multistep"})


SKILLS = {
    1: dict(name="Equal Groups and Multiplication", fams=[eg_pic_total, eg_pic_expr, eg_meaning, eg_story_expr, eg_repeated, eg_which_story, eg_unequal]),
    2: dict(name="Arrays and Multiplication", fams=[ar_count, ar_equation, ar_rows_missing, ar_story, ar_two_ways, ar_fix_array, ar_missing_part, ar_not_array]),
    3: dict(name="Multiplying by 2, 5, and 10", fams=[f_fact, f_skip_line, f_coins, f_hands, f_pattern, f_five_from_ten, f_two_facts, f_which_true]),
    4: dict(name="Multiplication Word Problems", fams=[w_basic, w_equation, w_tape, w_measure, w_compare_two, w_choose_op, w_left_over]),
}
