"""Unit 5: Unknowns, Patterns, and Two-Step Problems (patterns-unknowns-two-step)."""
from g3lib import *

UNIT_ID = "patterns-unknowns-two-step"


def fct(r, L):
    if L == 0:
        return pick(r, [2, 3, 4, 5, 10]), r.randint(2, 6)
    if L == 1:
        return r.randint(3, 9), r.randint(3, 9)
    return r.randint(6, 9), r.randint(4, 10)


# ============================================================== S1 Unknown Numbers in Equations
@fam("012")
def un_eq(r, L):
    a, b = fct(r, L)
    P = a * b
    forms = [(f"{a} × ? = {P}", b), (f"? × {b} = {P}", a), (f"{P} ÷ ? = {b}", a), (f"? ÷ {a} = {b}", P)]
    if L >= 1:
        forms += [(f"{P} = {a} × ?", b), (f"{b} = ? ÷ {a}", P), (f"{b} = {P} ÷ ?", a)]
    if L == 0:
        forms = forms[:2] + [(f"{a} × {b} = ?", P)]
    eq, ans = pick(r, forms)
    wr = [W(P if ans != P else a, "gave the wrong number from the equation"), W(abs(P - a) if ans != abs(P - a) else P + a, "subtracted or added instead"),
          W(ans + 1, "used a nearby fact"), W(b if ans != b else a, "copied a number from the equation")]
    return Item(f"What number makes the equation true? {eq}", ans, ["Read the equation and think of the related fact.", f"{eq.replace('?', str(ans))} is true."],
                wr, FN("blank_eq", eq=eq.replace("?", "___")), qtype="fill-blank", claim=eq)


@fam("012", mode="mc")
def un_which_true(r, L):
    a, b = fct(r, L)
    P = a * b
    need(a != b)
    good = f"{P} ÷ {a} = {b}"
    bad = [f"{P} ÷ {a} = {b + 1}", f"{a} ÷ {P} = {b}", f"{P} ÷ {b} = {b}"]
    it = mc_key(f"The unknown in {a} × □ = {P} is {b}. Which division equation is also true?", good, bad,
                [f"{a} × {b} = {P}.", f"So {P} ÷ {a} = {b}."], qtype="conceptual", tags={"connections"}, r=r)
    it.check = FN("true_eq")
    return it


@fam("012")
def un_symbol(r, L):
    a, b = fct(r, L)
    P = a * b
    sym = pick(r, ["n", "□", "k"])
    eq, ans = pick(r, [(f"{sym} × {a} = {P}", b), (f"{P} ÷ {sym} = {a}", b), (f"{sym} ÷ {b} = {a}", P)])
    return Item(f"Find the value of {sym}: {eq}", ans, [f"{sym} stands for the unknown number.", f"{eq.replace(sym, str(ans))}, so {sym} = {ans}."],
                [W(P if ans != P else a, "used the wrong number"), W(ans + 1, "used a nearby fact"), W(a + b, "added the numbers")],
                FN("blank_eq", eq=eq.replace(sym, "___")), qtype="fill-blank")


@fam("2")
def un_two(r, L):
    a, b = fct(r, L)
    P = a * b
    return _un_two(a, b, P, r)


def _un_two(a, b, P, r):
    c = r.randint(2, 9)
    return Item(f"□ × {a} = {P} and □ + △ = {b + c}. What number is △?", c,
                [f"□ × {a} = {P}, so □ = {b}.", f"{b} + △ = {b + c}, so △ = {c}."],
                [W(b, "gave □ instead of △"), W(b + c - a, "used the wrong number"), W(P - (b + c) if P > b + c else P + c, "combined the wrong numbers")],
                FN("chain_unknown", P=P, a=a, s=b + c), qtype="multi-step", tags={"multistep", "reasoning"})


@fam("2", mode="mc")
def un_error(r, L):
    a, b = r.randint(3, 9), r.randint(3, 9)
    P = a * b
    good = f"{P}, because {P} ÷ {a} = {b}"
    bad = [f"{a}, because the ? goes with {a}", f"{a + b}, because {a} + {b} = {a + b}", f"{abs(b - a) + 1}, because you take away"]
    need(len({P, a, a + b, abs(b - a) + 1}) == 4)
    it = mc_key(f"What number makes ? ÷ {a} = {b} true? Choose the answer and the reason.", good, bad, [f"? is the total. Think {a} × {b} = {P}.", f"{P} ÷ {a} = {b}."],
                qtype="explain", tags={"reasoning"}, r=r)
    it.check = FN("lead_num", eq=f"___ ÷ {a} = {b}")
    return it


# ============================================================== S2 Word Problems with Unknowns in Any Position
def story(r, L):
    a, b = fct(r, L)
    P = a * b
    pos = pick(r, ["product", "size", "groups"])
    nm = name(r)
    ctx = pick(r, [("bags", "oranges"), ("boxes", "markers"), ("rows", "chairs"), ("vans", "students"), ("shelves", "books")])
    g, item = ctx
    if pos == "product":
        q = f"There are {a} {g} with {b} {item} in each. How many {item} are there?"
        ans, unit, eq = P, item, f"{a} × {b} = n"
    elif pos == "size":
        q = f"{nm} has {P} {item} in {a} {g}. Each has the same number. How many {item} are in each of the {g}?"
        ans, unit, eq = b, item, f"{a} × n = {P}"
    else:
        q = f"{nm} has {P} {item}. {nm} puts {b} {item} in each of the {g}. How many {g} are there?"
        ans, unit, eq = a, g, f"n × {b} = {P}"
    return q, ans, unit, eq, a, b, P, pos


@fam("012")
def wu_solve(r, L):
    q, ans, unit, eq, a, b, P, pos = story(r, L)
    return Item(q, f"{ans} {unit}", [f"An equation: {eq}.", f"n = {ans}, so the answer is {ans} {unit}."],
                [W(f"{P if ans != P else a + b} {unit}", "used the wrong operation"), W(f"{ans + 1} {unit}", "used a nearby fact"), W(f"{P - a if pos != 'product' else a + b} {unit}", "subtracted or added instead")],
                FN("blank_eq", eq=eq.replace("n", "___"), unit=unit), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def wu_equation(r, L):
    q, ans, unit, eq, a, b, P, pos = story(r, L)
    good = eq
    bad = {"product": [f"{a} + {b} = n", f"n ÷ {a} = {b + a}", f"{a} × n = {b}"], "size": [f"{a} × {P} = n", f"{P} + {a} = n", f"n ÷ {a} = {P}"],
           "groups": [f"{P} × {b} = n", f"n ÷ {P} = {b}", f"{b} + n = {P}"]}[pos]
    return mc_key(q + " Which equation matches the story? (n is the unknown.)", good, bad,
                  ["Decide what is known: the number of groups, the size of each group, or the total.", f"{good}, so n = {ans}."], qtype="word-problem", r=r)


@fam("012", mode="mc")
def wu_what_unknown(r, L):
    q, ans, unit, eq, a, b, P, pos = story(r, L)
    good = {"product": "the total", "size": "the number in each group", "groups": "the number of groups"}[pos]
    bad = [x for x in ["the total", "the number in each group", "the number of groups", "the number left over"] if x != good][:3]
    return mc_key(q + " What is unknown in this story?", good, bad, ["Look at what the question asks.", f"It asks for {good}."], qtype="conceptual", r=r)


@fam("12")
def wu_array(r, L):
    a, b = fct(r, L)
    P = a * b
    ask = pick(r, ["rows", "cols"])
    if ask == "rows":
        q, ans, u = f"A garden has {P} plants in rows. Each row has {b} plants. How many rows are there?", a, "rows"
    else:
        q, ans, u = f"A wall of {P} tiles has {a} rows. How many tiles are in each row?", b, "tiles"
    return Item(q, f"{ans} {u}", [f"Rows × number in each row = total.", f"{P} ÷ {b if ask == 'rows' else a} = {ans}."],
                [W(f"{P - (b if ask == 'rows' else a)} {u}", "subtracted"), W(f"{ans + 1} {u}", "used a nearby fact"), W(f"{P} {u}", "gave the total")],
                EX(f"{P}/{b if ask == 'rows' else a}", unit=u), qtype="word-problem")


@fam("2")
def wu_measure(r, L):
    a, b = fct(r, L)
    P = a * b
    nm = name(r)
    q = pick(r, [(f"A rope {P} feet long is cut into pieces that are each {b} feet long. How many pieces are there?", a, "pieces", f"{P}/{b}"),
                 (f"{nm} runs the same number of laps each day. After {a} days, {nm} has run {P} laps. How many laps are run each day?", b, "laps", f"{P}/{a}"),
                 (f"A box holds {b} kilograms of sand. How many kilograms do {a} boxes hold?", P, "kilograms", f"{a}*{b}")])
    return Item(q[0], f"{q[1]} {q[2]}", ["Decide which number is unknown: the total, the size, or the number of groups.", f"{q[3].replace('*', ' × ').replace('/', ' ÷ ')} = {q[1]}."],
                [W(f"{q[1] + 1} {q[2]}", "used a nearby fact"), W(f"{P if q[1] != P else a + b} {q[2]}", "used the wrong operation"), W(f"{abs(P - b)} {q[2]}", "subtracted")],
                EX(q[3], unit=q[2]), qtype="word-problem", tags={"modeling"})


@fam("2", mode="mc")
def wu_write_story(r, L):
    a, b = fct(r, L)
    P = a * b
    need(a != b)
    good = f"{P} cards are put into piles of {b}. How many piles are there?"
    bad = [f"{a} piles have {b} cards each. How many cards are there?", f"{P} cards and {b} more cards. How many cards are there?", f"{b} piles have {P} cards each. How many cards are there?"]
    return mc_key(f"Which story matches the equation n × {b} = {P}?", good, bad,
                  [f"n × {b} = {P}: an unknown number of groups of {b} make {P}.", f"n = {a} piles."], qtype="explain", tags={"reasoning"}, r=r)


# ============================================================== S3 Multiplying by Multiples of 10
def m10(r, L):
    if L == 0:
        return r.randint(2, 5), r.randint(1, 5) * 10
    if L == 1:
        return r.randint(2, 9), r.randint(2, 9) * 10
    return r.randint(4, 9), r.randint(4, 9) * 10


def m10_wrongs(a, t):
    return [W(a * t // 10, "left off the zero"), W(a * t * 10, "wrote an extra zero") if a * t * 10 <= 1000 else W(a * t + 100, "made a fact error in the tens"),
            W(a + t, "added instead of multiplying"), W(a * (t // 10) * 10 + 10, "made a fact error")]


@fam("012")
def mt_fact(r, L):
    a, t = m10(r, L)
    x, y = (a, t) if r.random() < 0.6 else (t, a)
    return Item(f"Multiply: {x} × {y}", comma(a * t), [f"{a} × {t // 10} tens = {a * t // 10} tens.", f"{a * t // 10} tens = {comma(a * t)}."],
                m10_wrongs(a, t), EX(f"{x}*{y}"), qtype="procedural", claim=f"{x} × {y}")


@fam("012")
def mt_tens(r, L):
    a, t = m10(r, L)
    k = t // 10
    return Item(f"{a} × {k} tens = ___ tens. What number goes in the blank?", a * k, [f"Multiply the number of tens: {a} × {k} = {a * k}.", f"{a} × {k} tens = {a * k} tens = {comma(a * t)}."],
                [W(a * t, "wrote the product in ones, not the number of tens"), W(a + k, "added"), W(a * k + 1, "made a fact error")], EX(f"{a}*{k}"), qtype="fill-blank", tags={"multiple-representations"})


@fam("012")
def mt_word(r, L):
    a, t = m10(r, L)
    q = pick(r, [(f"Each box has {t} crayons. How many crayons are in {a} boxes?", "crayons"), (f"A class reads {t} pages each week. How many pages is that in {a} weeks?", "pages"),
                 (f"Each bus seats {t} people. How many people fit on {a} buses?", "people"), (f"A ticket costs {t} cents. How many cents do {a} tickets cost?", "cents")])
    return Item(q[0], f"{comma(a * t)} {q[1]}", [f"{a} × {t // 10} tens = {a * t // 10} tens.", f"{a} × {t} = {comma(a * t)} {q[1]}."],
                [W(f"{w[0]} {q[1]}", w[1]) for w in m10_wrongs(a, t)[:3]], EX(f"{a}*{t}", unit=q[1]), qtype="word-problem")


@fam("012", mode="mc")
def mt_strategy(r, L):
    a, t = m10(r, L)
    k = t // 10
    good = f"{a} × {k} × 10"
    bad = [f"{a} × {k} + 10", f"{a} + {k} × 10", f"{a} × {t} × 10"]
    it = mc_key(f"Which expression has the same value as {a} × {t}?", good, bad, [f"{t} = {k} × 10.", f"{a} × {t} = ({a} × {k}) × 10 = {comma(a * t)}."],
                qtype="compare-strategies", tags={"multiple-representations"}, r=r)
    it.check = FN("same_value", target=f"{a}*{t}")
    return it


@fam("2")
def mt_missing(r, L):
    a, t = m10(r, L)
    eq, ans = pick(r, [(f"{a} × ___ = {a * t}", t), (f"___ × {t} = {a * t}", a)])
    return Item(f"What number makes the equation true? {eq}", ans, ["Think in tens.", f"{eq.replace('___', str(ans))}."],
                [W(t // 10 if ans == t else a * 10, "mixed up ones and tens"), W(ans * 10, "wrote an extra zero"), W(ans + 10 if ans == t else ans + 1, "used a nearby fact")],
                FN("blank_eq", eq=eq), qtype="fill-blank", tags={"reasoning"})


@fam("2", mode="mc")
def mt_compare(r, L):
    exprs = []
    for k in range(3):
        a, t = m10(sub(r, k), L)
        exprs.append((a, t))
    vals = [a * t for a, t in exprs]
    need(len(set(vals)) == 3 and len(set(exprs)) == 3)
    texts = [f"{a} × {t}" for a, t in exprs]
    good = texts[vals.index(max(vals))]
    bad = [x for x in texts if x != good] + ["They are equal."]
    it = mc_key(f"Which product is greatest: {texts[0]}, {texts[1]}, or {texts[2]}?", good, bad,
                [", ".join(f"{x} = {comma(v)}" for x, v in zip(texts, vals)) + ".", f"The greatest is {good}."], qtype="explain", tags={"reasoning"}, r=r)
    it.check = FN("greatest_product", opts=[x.replace(" × ", "*") for x in texts])
    return it


# ============================================================== S4 Patterns in Tables
@fam("012", mode="mc")
def pt_evenodd(r, L):
    k = pick(r, [2, 4, 6, 8])
    good = f"Always even, because {k} × a number is {k // 2 if k > 2 else 1} {'group' if k == 2 else 'groups'} of 2 × that number" if k > 2 else "Always even, because 2 × a number is two equal groups"
    bad = ["Always odd, because the factors are different", "Sometimes even and sometimes odd", "Even only when the other factor is even"]
    return mc_key(f"Is the product of {k} and any whole number even or odd?", good, bad,
                  [f"{k} = 2 × {k // 2}, so {k} × n can be split into two equal addends.", "A number made of two equal parts is even."], qtype="explain", tags={"reasoning"}, r=r)


@fam("012")
def pt_column(r, L):
    k = r.randint(2, 9)
    n = 6 if L == 0 else 9
    alt = f"A multiplication table from 1 to {n}. The column for {k} is highlighted."
    return Item(f"Look at the highlighted column in the multiplication table. How much does each number grow from one row to the next?", k,
                [f"The column shows 1 × {k}, 2 × {k}, 3 × {k}, ...", f"Each product is {k} more than the one above it."],
                [W(1, "counted by 1"), W(2 * k, "skipped a row"), W(k + 1, "looked at the wrong column")], FN("table_step", op="×", col=k), qtype="visual", tags={"reasoning"},
                diagram=Diagram("mtable", {"op": "×", "n": n, "cols_hl": [k]}, alt))


@fam("012")
def pt_hidden(r, L):
    n = 6 if L == 0 else 9
    a, b = r.randint(2, n), r.randint(2, n)
    op = "×" if L or r.random() < 0.5 else "+"
    v = a * b if op == "×" else a + b
    alt = f"{'A multiplication' if op == '×' else 'An addition'} table from 1 to {n}. One number in row {a}, column {b} is hidden by a question mark."
    return Item(f"One number in the {'multiplication' if op == '×' else 'addition'} table is hidden. Use the pattern in its row or column. What is the hidden number?", v,
                [f"The ? is in row {a} and column {b}.", f"{a} {op} {b} = {v}."], [W(v + (b if op == '×' else 1), "used the next number in the row"), W(v - (a if op == '×' else 1), "used the number above it"), W(a + b if op == '×' else a * b, "used the wrong operation")],
                FN("table_cell", op=op, row=a, col=b), qtype="visual", diagram=Diagram("mtable", {"op": op, "n": n, "hide": [[a, b]], "highlight": [[a, b]]}, alt))


@fam("012", mode="mc")
def pt_addition(r, L):
    good, bad, why = pick(r, [("even", ["odd", "sometimes even and sometimes odd", "always 0"], "Odd + odd is always even: two odd numbers each have one left over, and the two left over make a pair."),
                              ("odd", ["even", "sometimes even and sometimes odd", "always 1"], "Even + odd is always odd: the even part makes pairs and the odd number has one left over."),
                              ("even", ["odd", "sometimes odd", "always 10"], "Even + even is always even: both numbers are made of pairs.")])
    kind = {"Odd + odd": "two odd numbers", "Even + odd": "an even number and an odd number", "Even + even": "two even numbers"}[why.split(" is")[0]]
    return mc_key(f"In the addition table, what is always true about the sum of {kind}?", good, bad, [why.split(":")[0] + ".", why.split(": ")[1][0].upper() + why.split(": ")[1][1:]], qtype="conceptual", tags={"reasoning"}, r=r)


@fam("12", mode="mc")
def pt_double_col(r, L):
    k = pick(r, [2, 3, 4])
    good = f"Each number in the {2 * k}s column is double the number in the {k}s column."
    bad = [f"Each number in the {2 * k}s column is {k} more than the number in the {k}s column.", f"Each number in the {2 * k}s column is 2 more than the number in the {k}s column.", f"The {2 * k}s column and the {k}s column are the same."]
    alt = f"A multiplication table from 1 to 9 with the columns for {k} and {2 * k} highlighted."
    return mc_key(f"Compare the two highlighted columns. Which statement is true?", good, bad, [f"{2 * k} = 2 × {k}.", f"So {2 * k} × n = 2 × ({k} × n): double."],
                  qtype="visual", tags={"reasoning"}, diagram=Diagram("mtable", {"op": "×", "n": 9, "cols_hl": [k, 2 * k]}, alt), r=r)


@fam("2")
def pt_nines(r, L):
    n = r.randint(2, 10)
    return Item(f"In the 9s facts, the digits of each product add to 9 (for example 9 × 4 = 36 and 3 + 6 = 9). Use the pattern to check 9 × {n}. What is 9 × {n}?", 9 * n,
                [f"9 × {n} = 10 × {n} − {n} = {9 * n}.", f"The digits of {9 * n} add to {sum(map(int, str(9 * n)))}."],
                [W(9 * n + 9, "added an extra group"), W(10 * n, "multiplied by 10"), W(9 * n - 9, "left out a group")], EX(f"9*{n}"), qtype="procedural", tags={"reasoning"})


# ============================================================== S5 Writing Equations for Two-Step Problems
def two_step_story(r, L):
    kind = pick(r, ["mult_add", "mult_sub", "div_add", "add_mult", "sub_div"])
    nm = name(r)
    a, b = fct(r, L)
    c = r.randint(3, 15) if L < 2 else r.randint(12, 40)
    if kind == "mult_add":
        q = f"{nm} has {a} packs of {b} cards and gets {c} more cards. How many cards does {nm} have now?"
        eq, val, wrong = f"({a} × {b}) + {c} = c", a * b + c, [f"{a} + {b} + {c} = c", f"{a} × ({b} + {c}) = c", f"({a} × {b}) − {c} = c"]
    elif kind == "mult_sub":
        need(a * b > c)
        q = f"A baker makes {a} trays of {b} rolls. {c} rolls are sold. How many rolls are left?"
        eq, val, wrong = f"({a} × {b}) − {c} = r", a * b - c, [f"({a} × {b}) + {c} = r", f"({a} + {b}) − {c} = r", f"{a} × ({b} − {c}) = r" if b > c else f"({a} + {c}) × {b} = r"]
    elif kind == "div_add":
        q = f"{a * b} stickers are shared equally by {a} friends. Then each friend gets {c} more. How many stickers does each friend have?"
        eq, val, wrong = f"({a * b} ÷ {a}) + {c} = s", b + c, [f"({a * b} × {a}) + {c} = s", f"({a * b} ÷ {a}) − {c} = s", f"{a * b} + {a} + {c} = s"]
    elif kind == "add_mult":
        c = r.randint(2, 5)
        q = f"Each bag has {b} red beads and {c} blue beads. How many beads are in {a} bags?"
        eq, val, wrong = f"{a} × ({b} + {c}) = n", a * (b + c), [f"({a} × {b}) + {c} = n", f"{a} + {b} + {c} = n", f"{a} × {b} × {c} = n"]
    else:
        extra = r.randint(2, 12)
        q = f"{nm} had {a * b + extra} marbles and lost {extra}. The rest are put in {a} equal bags. How many marbles are in each bag?"
        eq, val, wrong = f"({a * b + extra} − {extra}) ÷ {a} = m", b, [f"({a * b + extra} − {extra}) × {a} = m", f"({a * b + extra} + {extra}) ÷ {a} = m", f"({a * b + extra} − {a}) ÷ {extra} = m"]
    return q, eq, val, wrong, kind


@fam("012", mode="mc")
def we_choose(r, L):
    q, eq, val, wrong, kind = two_step_story(r, L)
    need(len(set(wrong + [eq])) == 4)
    it = mc_key(q + " Which equation can be used to solve the problem? (The letter stands for the answer.)", eq, wrong,
                ["Find the two steps in the story and the order they happen.", f"{eq}; the letter is {val}."], qtype="word-problem", tags={"modeling"}, r=r)
    it.check = FN("letter_eq", value=val)
    return it


@fam("012", mode="mc")
def we_letter(r, L):
    q, eq, val, wrong, kind = two_step_story(r, L)
    letter = eq.split("= ")[-1]
    good = {"mult_add": "the number of cards now", "mult_sub": "the number of rolls left", "div_add": "the number of stickers each friend has",
            "add_mult": "the number of beads in all the bags", "sub_div": "the number of marbles in each bag"}[kind]
    bad = {"mult_add": ["the number of packs", "the number of cards in one pack", "the number of new cards"], "mult_sub": ["the number of trays", "the number of rolls sold", "the number of rolls on one tray"],
           "div_add": ["the number of friends", "the total number of stickers", "the extra stickers"], "add_mult": ["the number of bags", "the number of red beads in one bag", "the beads in one bag"],
           "sub_div": ["the number of bags", "the number of marbles lost", "the marbles at the start"]}[kind]
    return mc_key(q + f" The equation is {eq}. What does {letter} stand for?", good, bad, ["The letter stands for the unknown the question asks for.", f"{letter} is {good}."], qtype="conceptual", r=r)


@fam("12")
def we_solve_eq(r, L):
    q, eq, val, wrong, kind = two_step_story(r, L)
    letter = eq.split("= ")[-1]
    return Item(f"Solve the equation for {letter}: {eq}", val, ["Do the operation in parentheses first, then multiply or divide, then add or subtract.", f"{letter} = {val}."],
                [W(val + 1, "made a fact error"), W(val - 1, "made a fact error"), W(val * 2, "doubled by mistake")], FN("letter_eq", value=None, eq=eq), qtype="procedural")


@fam("2", mode="mc")
def we_story_for(r, L):
    a, b = fct(r, L)
    c = r.randint(3, 12)
    eq = f"({a} × {b}) − {c} = p"
    good = f"{a} boxes hold {b} pens each. {c} pens are given away. How many pens are left?"
    bad = [f"{a} boxes hold {b} pens each. {c} more pens are bought. How many pens are there?", f"{a} pens and {b} pens are put together. {c} are given away. How many are left?",
           f"{a} × {b} pens are shared by {c} friends. How many does each get?"]
    return mc_key(f"Which story matches the equation {eq}?", good, bad, [f"{a} × {b}: equal groups. − {c}: some are taken away.", f"p = {a * b - c}."], qtype="explain", tags={"reasoning"}, r=r)


# ============================================================== S6 Solving Two-Step Problems
@fam("012")
def ts_solve(r, L):
    q, eq, val, wrong, kind = two_step_story(r, L)
    unit = {"mult_add": "cards", "mult_sub": "rolls", "div_add": "stickers", "add_mult": "beads", "sub_div": "marbles"}[kind]
    first = {"mult_add": "multiply", "mult_sub": "multiply", "div_add": "divide", "add_mult": "add", "sub_div": "subtract"}[kind]
    return Item(q, f"{val} {unit}", [f"Step 1: {first}. Step 2: use that answer.", f"{eq.rsplit('=', 1)[0].strip()} = {val} {unit}."],
                [W(f"{eval_two(wrong[0])} {unit}", "used the wrong operation for one step"), W(f"{eval_two(wrong[1])} {unit}", "set up the steps incorrectly"), W(f"{val + 10} {unit}", "made a computation error")],
                FN("letter_eq", value=None, eq=eq, unit=unit), qtype="multi-step", tags={"multistep"})


def eval_two(eq):
    e = eq.split("=")[0].replace("×", "*").replace("÷", "//").replace("−", "-")
    return eval(e, {"__builtins__": {}})


@fam("012", mode="mc")
def ts_reasonable(r, L):
    a = r.randint(3, 6)
    b, c = (r.randint(110, 190), r.randint(15, 45)) if L == 0 else (r.randint(110, 290), r.randint(25, 95)) if L == 1 else (r.randint(310, 690), r.randint(55, 95))
    exact = b + c
    item = pick(r, ["books", "cans", "tickets"])
    shown_ok = r.random() < 0.4
    shown = exact if shown_ok else exact + pick(r, [100, 200])
    need(b % 100 and c % 10)
    est = (b + 50) // 100 * 100 + (c + 5) // 10 * 10
    good = (f"Yes. {comma(b)} is about {comma((b + 50) // 100 * 100)} and {c} is about {(c + 5) // 10 * 10}, so the answer should be near {comma(est)}." if shown_ok else
            f"No. {comma(b)} is about {comma((b + 50) // 100 * 100)} and {c} is about {(c + 5) // 10 * 10}, so the answer should be near {comma(est)}.")
    bad = ([f"No. The answer should be near {comma(est + 300)}.", "No. The answer must be less than 100.", f"Yes, because it ends in {shown % 10}."] if shown_ok else
           [f"Yes. It is near {comma(est)}.", f"Yes, because it ends in {shown % 10}.", f"No. The answer should be near {comma(est + 300)}."])
    it = mc_key(f"A class collected {comma(b)} {item} last month and {c} {item} this week. {name(r)} says the total is {comma(shown)}. Is that reasonable?", good, bad,
                [f"Estimate: {comma((b + 50) // 100 * 100)} + {(c + 5) // 10 * 10} = {comma(est)}.", f"The exact total is {comma(exact)}."], qtype="explain", tags={"reasoning"}, r=r)
    it.check = FN("reasonable2", b=b, c=c, shown=shown)
    return it


@fam("12")
def ts_money(r, L):
    a, b = r.randint(2, 6), r.randint(3, 9)
    c = r.randint(1, 4) * 10 if L == 2 else r.randint(5, 20)
    budget = a * b + c + r.randint(5, 40)
    nm = name(r)
    return Item(f"{nm} has {budget} dollars. {nm} buys {a} games for {b} dollars each and a ball for {c} dollars. How many dollars are left?",
                f"{budget - a * b - c} dollars", [f"Spent: {a} × {b} + {c} = {a * b + c} dollars.", f"{budget} − {a * b + c} = {budget - a * b - c} dollars."],
                [W(f"{budget - a * b} dollars", "forgot the ball"), W(f"{budget - a - b - c} dollars", "added the price instead of multiplying"), W(f"{a * b + c} dollars", "found the amount spent")],
                EX(f"{budget}-{a}*{b}-{c}", unit="dollars"), qtype="multi-step", tags={"multistep"})


@fam("2")
def ts_compare(r, L):
    a, b, c, d = r.randint(4, 9), r.randint(4, 9), r.randint(3, 8), r.randint(4, 9)
    need(a * b != c * d)
    hi, lo = max(a * b, c * d), min(a * b, c * d)
    return Item(f"The red team sold {a} boxes of {b} cookies. The blue team sold {c} boxes of {d} cookies. How many more cookies did the team that sold more sell?",
                f"{hi - lo} cookies", [f"Red: {a} × {b} = {a * b}. Blue: {c} × {d} = {c * d}.", f"{hi} − {lo} = {hi - lo} cookies."],
                [W(f"{a * b + c * d} cookies", "added the totals"), W(f"{hi} cookies", "stopped after one step"), W(f"{abs(a - c) * abs(b - d) if abs(a - c) * abs(b - d) != hi - lo else hi - lo + 1} cookies", "subtracted the factors")],
                EX(f"{a}*{b}-{c}*{d}" if a * b > c * d else f"{c}*{d}-{a}*{b}", unit="cookies"), qtype="multi-step", tags={"multistep"})


@fam("2")
def ts_check(r, L):
    a, b = r.randint(3, 8), r.randint(4, 9)
    c = r.randint(2, 9)
    total = a * b + c
    nm = name(r)
    return Item(f"{nm} has {total} stamps. {nm} puts {b} stamps on each page and has {c} stamps left over. How many full pages are there?",
                f"{a} pages", [f"Take away the leftover stamps: {total} − {c} = {a * b}.", f"{a * b} ÷ {b} = {a} pages."],
                [W(f"{a + 1} pages", "counted the leftover stamps as a page"), W(f"{a * b} pages", "stopped after subtracting"), W(f"{(total + c) // b} pages" if (total + c) % b == 0 and (total + c) // b != a else f"{a + 2} pages", "added the leftover stamps")],
                EX(f"({total}-{c})/{b}", unit="pages"), qtype="multi-step", tags={"multistep", "reasoning"})


SKILLS = {
    1: dict(name="Unknown Numbers in Multiplication and Division Equations", fams=[un_eq, un_which_true, un_symbol, un_two, un_error]),
    2: dict(name="Word Problems with Unknowns in Any Position", fams=[wu_solve, wu_equation, wu_what_unknown, wu_array, wu_measure, wu_write_story]),
    3: dict(name="Multiplying by Multiples of 10", fams=[mt_fact, mt_tens, mt_word, mt_strategy, mt_missing, mt_compare]),
    4: dict(name="Patterns in the Addition and Multiplication Tables", fams=[pt_evenodd, pt_column, pt_hidden, pt_addition, pt_double_col, pt_nines]),
    5: dict(name="Writing Equations for Two-Step Problems", fams=[we_choose, we_letter, we_solve_eq, we_story_for]),
    6: dict(name="Solving Two-Step Problems and Checking Reasonableness", fams=[ts_solve, ts_reasonable, ts_money, ts_compare, ts_check]),
}
