"""Unit 3: Properties and Fact Strategies (properties-fact-strategies)."""
from g3lib import *

UNIT_ID = "properties-fact-strategies"


def ab(r, L, lo=2):
    if L == 0:
        return r.randint(lo, 5), r.randint(lo, 6)
    if L == 1:
        return r.randint(3, 9), r.randint(3, 9)
    return r.randint(6, 9), r.randint(6, 9)


# ============================================================== S1 Commutative Property
@fam("012")
def cm_fill(r, L):
    a, b = ab(r, L)
    need(a != b)
    form = pick(r, ["right", "left"]) if L else "right"
    if form == "right":
        q = f"Complete the equation: {a} × {b} = {b} × ___"
    else:
        q = f"Complete the equation: {a} × ___ = {b} × {a}"
    ans = a if form == "right" else b
    return Item(q, ans, ["The commutative property: changing the order of the factors does not change the product.",
                         f"{a} × {b} = {b} × {a} = {a * b}."],
                [W(a * b, "wrote the product instead of the missing factor"), W(b if ans == a else a, "repeated the factor that is already there"), W(a + b, "added the factors")],
                FN("blank_eq", eq=q.split(": ")[1]), qtype="fill-blank", claim=q.split(": ")[1])


@fam("012")
def cm_use(r, L):
    a, b = ab(r, L)
    need(a != b)
    return Item(f"{name(r)} knows that {a} × {b} = {a * b}. What is {b} × {a}?", a * b,
                [f"{b} × {a} has the same factors in a different order.", f"So {b} × {a} = {a * b}."],
                [W(a + b, "added the factors"), W(a * b + a, "added one more group"), W(a * b - b, "used one group fewer")], EX(f"{b}*{a}"), qtype="procedural")


@fam("012", mode="mc")
def cm_array(r, L):
    a, b = ab(r, L)
    need(a != b)
    good = f"{a} × {b} = {a * b} and {b} × {a} = {a * b}"
    bad = [f"{a} × {b} = {a * b} and {b} × {a} = {b * a + a}", f"{a} + {b} = {a + b} and {b} + {a} = {a + b}", f"{a} × {a} = {a * a} and {b} × {b} = {b * b}"]
    alt = f"An array of dots with {a} rows and {b} columns."
    return mc_key("You can read the array by rows or by columns. Which pair of equations both match the array?", good, bad,
                  [f"By rows: {a} rows of {b} is {a} × {b}. By columns: {b} columns of {a} is {b} × {a}.", f"Both equal {a * b}."],
                  qtype="visual", tags={"multiple-representations"}, diagram=Diagram("array3", {"rows": a, "cols": b}, alt), r=r)


@fam("012", mode="mc")
def cm_true(r, L):
    a, b = ab(r, L)
    need(a != b and (a * b) % a == 0)
    good = f"{a} × {b} = {b} × {a}"
    bad = [f"{a} × {b} = {a} + {b}", f"{a} × {b} = {b} × {b}", f"{a * b} ÷ {a} = {a} ÷ {a * b}" if L else f"{a} × {b} = {a} × {a}"]
    it = mc_key("Which equation is true?", good, bad, [f"{a} × {b} = {a * b} and {b} × {a} = {a * b}.", "Only the commutative property equation is true."],
                  qtype="conceptual", tags={"reasoning"}, r=r)
    it.check = FN("true_eq")
    return it


@fam("12", mode="mc")
def cm_division(r, L):
    a, b = ab(r, L)
    need(a != b)
    P = a * b
    good = f"No. {P} ÷ {a} = {b}, but {a} ÷ {P} is not {b}."
    bad = [f"Yes. Order never matters.", f"Yes. Both are equal to {b}.", f"No. {P} ÷ {a} = {a}."]
    return mc_key(f"{name(r)} says {P} ÷ {a} = {a} ÷ {P} because of the commutative property. Is that right?", good, bad,
                  ["The commutative property works for multiplication, not division.", f"{P} ÷ {a} = {b}. Sharing {a} among {P} groups is not {b}."],
                  qtype="error-analysis", tags={"reasoning", "misconception"}, r=r)


@fam("2")
def cm_known_fact(r, L):
    a, b = r.randint(6, 9), r.randint(3, 5)
    return Item(f"{name(r)} does not know {a} × {b} but knows all the {b}s facts. What fact can help, and what is {a} × {b}? Give the product.", a * b,
                [f"Turn the factors around: {a} × {b} = {b} × {a}.", f"{b} × {a} = {a * b}."],
                [W(a * b + b, "added an extra group"), W(a + b, "added"), W(a * b - a, "left out a group")], EX(f"{a}*{b}"), qtype="explain", tags={"reasoning"})


# ============================================================== S2 Associative Property
def three(r, L):
    if L == 0:
        return pick(r, [2, 5]), r.randint(2, 4), pick(r, [2, 5])
    if L == 1:
        return r.randint(2, 5), r.randint(2, 4), r.randint(2, 5)
    return r.randint(2, 4), r.randint(3, 6), r.randint(2, 5)


@fam("012")
def as_fill(r, L):
    a, b, c = three(r, L)
    need(len({a, b, c}) == 3)
    q = f"({a} × {b}) × {c} = {a} × ({b} × ___)"
    return Item(f"Complete the equation: {q}", c, ["The associative property: you can group the factors in a different way.", f"({a} × {b}) × {c} = {a} × ({b} × {c}) = {a * b * c}."],
                [W(a, "used the first factor"), W(a * b, "wrote a partial product"), W(a * b * c, "wrote the product")], FN("blank_eq", eq=q), qtype="fill-blank", claim=q)


@fam("012")
def as_compute(r, L):
    a, b, c = three(r, L)
    need(a * c in (10, 20, 4, 6, 8, 12, 15) or L)
    return Item(f"Find {a} × {b} × {c}. Hint: multiply {a} × {c} first.", a * b * c,
                [f"{a} × {c} = {a * c}.", f"{a * c} × {b} = {a * b * c}."],
                [W(a * b + c, "added the last factor"), W(a + b + c, "added all the factors"), W(a * c + b, "added instead of multiplying the second time"), W(a * b, "used only two factors")],
                EX(f"{a}*{b}*{c}"), qtype="procedural", claim=f"{a} × {b} × {c}")


@fam("012", mode="mc")
def as_best(r, L):
    a, b = pick(r, [(5, 2), (2, 5)])
    c = r.randint(3, 9)
    good = f"{a} × {b} = 10, then 10 × {c} = {10 * c}"
    bad = [f"{a} + {b} = 7, then 7 × {c} = {7 * c}", f"{a} × {c} = {a * c}, then {a * c} + {b} = {a * c + b}", f"{a} × {b} = 10, then 10 + {c} = {10 + c}"]
    return mc_key(f"Which way is a correct and easy way to find {a} × {c} × {b}?", good, bad,
                  [f"Group {a} × {b} first because it makes 10.", f"10 × {c} = {10 * c}."], qtype="compare-strategies", tags={"reasoning"}, r=r)


@fam("012")
def as_story(r, L):
    a, b, c = three(r, L)
    need(len({a, b, c}) >= 2)
    return Item(f"There are {a} shelves. Each shelf has {b} boxes. Each box has {c} toy cars. How many toy cars are there?", f"{a * b * c} toy cars",
                [f"{a} × {b} = {a * b} boxes.", f"{a * b} × {c} = {a * b * c} toy cars."],
                [W(f"{a + b + c} toy cars", "added the numbers"), W(f"{a * b} toy cars", "found the boxes, not the cars"), W(f"{a * b + c} toy cars", "added the last number")],
                EX(f"{a}*{b}*{c}", unit="toy cars"), qtype="word-problem", tags={"multistep"})


@fam("12", mode="mc")
def as_same(r, L):
    a, b, c = three(r, L)
    need(len({a, b, c}) == 3)
    good = f"({a} × {c}) × {b}"
    bad = [f"({a} + {c}) × {b}", f"({a} × {c}) + {b}", f"{a} × {c}"]
    it = mc_key(f"Which expression has the same value as ({a} × {b}) × {c}?", good, bad,
                  ["You can change the order and grouping of factors (commutative and associative properties).", f"Both equal {a * b * c}."], qtype="conceptual", r=r)
    it.check = FN("same_value", target=f"({a}*{b})*{c}")
    return it


@fam("2")
def as_break(r, L):
    a = r.randint(6, 9)
    q = f"{a} × 4 = {a} × (2 × 2) = ({a} × 2) × 2"
    return Item(f"{name(r)} finds {a} × 4 like this: {q}. What is {a} × 4?", a * 4, [f"{a} × 2 = {a * 2}.", f"{a * 2} × 2 = {a * 4}."],
                [W(a * 2, "stopped after doubling once"), W(a * 2 + 2, "added 2 instead of doubling"), W(a + 4, "added")], EX(f"{a}*4"), qtype="compare-strategies", tags={"reasoning"})


@fam("2", mode="mc")
def as_error(r, L):
    a, b, c = r.randint(2, 4), r.randint(3, 6), r.randint(2, 5)
    need(len({a, b, c}) == 3)
    wrong = a * b + c
    good = f"{a * b * c}, because ({a} × {b}) × {c} = {a * b} × {c}"
    bad = [f"{wrong}, because {a} × {b} = {a * b} and then add {c}", f"{a + b + c}, because you combine all three numbers", f"{a * b}, because you multiply the first two numbers"]
    return mc_key(f"What is {a} × {b} × {c}? Choose the answer with the correct reason.", good, bad, [f"Multiply two factors, then multiply by the third.", f"{a * b} × {c} = {a * b * c}."],
                  qtype="explain", tags={"reasoning"}, r=r)


@fam("2")
def as_missing(r, L):
    a, b, c = r.randint(2, 4), r.randint(2, 5), r.randint(3, 6)
    need(len({a, b, c}) == 3)
    eq = f"({a} × ___) × {c} = {a * b * c}"
    return Item(f"What number makes the equation true? {eq}", b, [f"First, {a * b * c} ÷ {c} = {a * b}, so {a} × ___ = {a * b}.", f"{a} × {b} = {a * b}, so the missing factor is {b}."],
                [W(a * b, "stopped after dividing by the last factor"), W(a * b * c // a, "divided by only one factor"), W(b + 1, "used a nearby fact")],
                FN("blank_eq", eq=eq), qtype="multi-step", tags={"multistep", "reasoning"})


# ============================================================== S3 Distributive Property
def split_fact(r, L):
    if L == 0:
        a = r.randint(2, 5)
        b = r.randint(6, 8)
        p = 5
    elif L == 1:
        a = r.randint(3, 9)
        b = r.randint(6, 9)
        p = pick(r, [5, 2, 3])
    else:
        a = r.randint(6, 9)
        b = r.randint(7, 9)
        p = pick(r, [5, 4, 3])
    need(0 < p < b)
    return a, b, p, b - p


@fam("012", mode="mc")
def di_array(r, L):
    a, b, p, q = split_fact(r, L)
    good = f"({a} × {p}) + ({a} × {q})"
    bad = [f"({a} × {p}) × ({a} × {q})", f"({a} + {p}) + ({a} + {q})", f"({a} × {p}) + {q}"]
    alt = f"An array with {a} rows and {b} columns, split by a dashed line into {p} blue columns and {q} orange columns."
    it = mc_key("The dashed line splits the array into two parts. Which expression matches the two parts?", good, bad,
                  [f"Blue part: {a} × {p}. Orange part: {a} × {q}.", f"Add the parts: {a * p} + {a * q} = {a * b}."], qtype="visual",
                  tags={"multiple-representations"}, diagram=Diagram("array3", {"rows": a, "cols": b, "split_col": p}, alt), r=r)
    it.check = FN("same_value", target=f"{a}*{b}")
    return it


@fam("012")
def di_fill(r, L):
    a, b, p, q = split_fact(r, L)
    eq = f"{a} × {b} = ({a} × {p}) + ({a} × ___)"
    return Item(f"Complete the equation: {eq}", q, [f"Break {b} into {p} + {q}.", f"{a} × {b} = ({a} × {p}) + ({a} × {q})."],
                [W(b, "repeated the whole factor"), W(a * q, "wrote the partial product"), W(p, "repeated the first part")], FN("blank_eq", eq=eq), qtype="fill-blank", claim=eq)


@fam("012")
def di_compute(r, L):
    a, b, p, q = split_fact(r, L)
    return Item(f"Find {a} × {b} by breaking {b} into {p} + {q}. What is {a} × {b}?", a * b,
                [f"{a} × {p} = {a * p} and {a} × {q} = {a * q}.", f"{a * p} + {a * q} = {a * b}."],
                [W(a * p + q, "multiplied only one part"), W(a * p, "forgot the second part"), W(a * p * a * q if a * p * a * q < 1000 else a * p + a, "multiplied the parts instead of adding")],
                EX(f"{a}*{p}+{a}*{q}"), qtype="compare-strategies", tags={"multiple-representations"})


@fam("012")
def di_partial(r, L):
    a, b, p, q = split_fact(r, L)
    return Item(f"{a} × {b} = ({a} × {p}) + ({a} × {q}). {a} × {p} = {a * p}. What is {a} × {q}?", a * q,
                [f"{a} × {q} = {a * q}.", f"Then {a * p} + {a * q} = {a * b}."],
                [W(a * b, "found the whole product"), W(a + q, "added"), W(a * q + a, "added an extra group")], EX(f"{a}*{q}"), qtype="procedural")


@fam("12", mode="mc")
def di_choose(r, L):
    a, b, p, q = split_fact(r, L)
    good = f"{a} × {p} and {a} × {q}"
    bad = [f"{a} × {p} and {q}", f"{a} × {p} and {a} × {b}", f"{p} × {q} and {a}"]
    return mc_key(f"Which two facts can you add to find {a} × {b}?", good, bad, [f"{b} = {p} + {q}.", f"{a} × {b} = ({a} × {p}) + ({a} × {q})."], qtype="conceptual", r=r)


@fam("2", mode="mc")
def di_error(r, L):
    a, b, p, q = split_fact(r, L)
    wrong = a * p + q
    good = f"{name(r)} added {q} instead of {a} × {q}. The product is {a * b}."
    bad = [f"There is no mistake. The product is {wrong}.", f"{b} should be broken into {p} + {q + 1}. The product is {a * (b + 1)}.", f"The parts should be multiplied. The product is {a * p * q}."]
    nm = good.split(" ")[0]
    return mc_key(f"{nm} wrote {a} × {b} = ({a} × {p}) + {q} = {wrong}. What is the mistake?", good, bad,
                  [f"Both parts must be multiplied by {a}.", f"({a} × {p}) + ({a} × {q}) = {a * p} + {a * q} = {a * b}."], qtype="error-analysis", tags={"misconception"}, r=r)


# ============================================================== S4 0 and 1
@fam("012")
def z_fact(r, L):
    n = r.randint(2, 10) if L < 2 else r.randint(11, 99)
    kind = pick(r, ["x0", "0x", "x1", "1x", "d1", "dn", "0d"])
    q, e = {"x0": (f"{n} × 0", f"{n}*0"), "0x": (f"0 × {n}", f"0*{n}"), "x1": (f"{n} × 1", f"{n}*1"), "1x": (f"1 × {n}", f"1*{n}"),
            "d1": (f"{n} ÷ 1", f"{n}/1"), "dn": (f"{n} ÷ {n}", f"{n}/{n}"), "0d": (f"0 ÷ {n}", f"0/{n}")}[kind]
    ans = eval_safe(e)
    wr = {"x0": [W(n, "thought multiplying by 0 keeps the number"), W(1, "mixed up the 0 and 1 rules")], "0x": [W(n, "thought multiplying by 0 keeps the number"), W(1, "mixed up the 0 and 1 rules")],
          "x1": [W(1, "thought multiplying by 1 gives 1"), W(0, "mixed up the 0 and 1 rules")], "1x": [W(1, "thought multiplying by 1 gives 1"), W(n + 1, "added 1")],
          "d1": [W(1, "thought dividing by 1 gives 1"), W(0, "mixed up the 0 and 1 rules")], "dn": [W(n, "kept the number"), W(0, "thought a number divided by itself is 0")],
          "0d": [W(n, "kept the number"), W(1, "thought the answer is 1")]}[kind]
    rule = {"x0": "Any number times 0 is 0.", "0x": "0 times any number is 0.", "x1": "Any number times 1 is that number.", "1x": "Multiplying any number by 1 gives that number.",
            "d1": "Any number divided by 1 is that number.", "dn": "Any number (not 0) divided by itself is 1.", "0d": "0 divided by any number (not 0) is 0."}[kind]
    return Item(f"Find: {q}", ans, [rule, f"{q} = {ans}."], wr + [W(n * 10 if n < 100 else n + 10, "wrote a different number")], EX(e), qtype="procedural", claim=q)


def eval_safe(e):
    from fractions import Fraction
    if "*" in e:
        x, y = e.split("*")
        return int(x) * int(y)
    x, y = e.split("/")
    return int(Fraction(int(x), int(y)))


@fam("012")
def z_story(r, L):
    n = r.randint(3, 9)
    kind = pick(r, ["zero", "one", "share1", "eachone"])
    nm = name(r)
    if kind == "zero":
        q, a, e, u = f"{nm} has {n} plates. There are 0 cookies on each plate. How many cookies are there?", 0, f"{n}*0", "cookies"
    elif kind == "one":
        q, a, e, u = f"{nm} has {n} cups. There is 1 straw in each cup. How many straws are there?", n, f"{n}*1", "straws"
    elif kind == "share1":
        q, a, e, u = f"{nm} has {n} stickers and keeps them all on 1 page. How many stickers are on the page?", n, f"{n}/1", "stickers"
    else:
        q, a, e, u = f"{n} friends share {n} apples equally. How many apples does each friend get?", 1, f"{n}/{n}", "apples"
    return Item(q, f"{a} {u}" if a != 1 else f"1 {u[:-1]}", [f"Write the equation: {e.replace('*', ' × ').replace('/', ' ÷ ')}.", f"The answer is {a}."],
                [W(f"{n} {u}" if a != n else f"0 {u}", "used the wrong rule for 0 or 1"), W(f"{n + 1} {u}", "added 1"), W(f"0 {u}" if a else f"1 {u[:-1]}", "used the wrong rule for 0 or 1")],
                EX(e, unit=u), qtype="word-problem")


@fam("012", mode="mc")
def z_rule(r, L):
    n = r.randint(2, 9)
    good, bad = pick(r, [(f"{n} × 0 = 0", [f"{n} × 0 = {n}", f"{n} × 1 = 1", f"{n} ÷ {n} = 0"]),
                          (f"{n} ÷ 1 = {n}", [f"{n} ÷ 1 = 1", f"{n} × 0 = {n}", f"0 ÷ {n} = {n}"]),
                          (f"0 ÷ {n} = 0", [f"0 ÷ {n} = {n}", f"{n} ÷ {n} = 0", f"{n} × 1 = 1"])])
    it = mc_key("Which equation is true?", good, bad, ["Use the rules for 0 and 1.", f"{good} is true."], qtype="conceptual", r=r)
    it.check = FN("true_eq")
    return it


@fam("012")
def z_missing(r, L):
    n = r.randint(2, 9)
    eq, ans = pick(r, [(f"{n} × ___ = {n}", 1), (f"___ × {n} = 0", 0), (f"{n} ÷ ___ = {n}", 1), (f"{n} ÷ ___ = 1", n), (f"___ ÷ {n} = 0", 0)])
    return Item(f"What number makes the equation true? {eq}", ans, ["Think about the rules for 0 and 1.", f"{eq.replace('___', str(ans))} is true."],
                [W(n if ans != n else 1, "used the wrong rule"), W(0 if ans else 1, "mixed up the 0 and 1 rules"), W(n + 1, "added")],
                FN("blank_eq", eq=eq), qtype="fill-blank", claim=eq)


@fam("2", mode="mc")
def z_divide_zero(r, L):
    n = r.randint(3, 9)
    good = f"No. You cannot share {n} things into 0 groups, so {n} ÷ 0 has no answer."
    bad = [f"Yes. {n} ÷ 0 = 0.", f"Yes. {n} ÷ 0 = {n}.", f"No. {n} ÷ 0 = 1."]
    return mc_key(f"{name(r)} says {n} ÷ 0 = 0 because 0 ÷ {n} = 0. Is that right?", good, bad,
                  [f"0 ÷ {n} = 0 because 0 shared among {n} groups gives 0 each.", f"But no number times 0 makes {n}, so {n} ÷ 0 has no answer."], qtype="explain", tags={"reasoning"}, r=r)


@fam("2")
def z_mixed(r, L):
    a, b = r.randint(2, 9), r.randint(2, 9)
    return Item(f"Find (({a} × {b}) × 0) + ({b} × 1)", b, [f"Anything times 0 is 0, so ({a} × {b}) × 0 = 0.", f"{b} × 1 = {b}. 0 + {b} = {b}."],
                [W(a * b + b, "multiplied by 1 instead of 0"), W(0, "made every part 0"), W(a * b, "ignored the 0")], EX(f"(({a}*{b})*0)+({b}*1)"), qtype="multi-step", tags={"multistep"})


# ============================================================== S5 Fact Strategies
def hard(r, L):
    if L == 0:
        return pick(r, [3, 4]), r.randint(2, 6)
    if L == 1:
        return pick(r, [3, 4, 6, 7, 8, 9]), r.randint(3, 9)
    return pick(r, [6, 7, 8, 9]), r.randint(6, 9)


@fam("012")
def fs_fact(r, L):
    a, b = hard(r, L)
    x, y = (a, b) if r.random() < 0.5 else (b, a)
    return Item(f"Multiply: {x} × {y}", a * b, [f"Use a fact you know, like {min(a, b)} × {max(a, b) - 1} = {min(a, b) * (max(a, b) - 1)}, and add one more group of {min(a, b)}.", f"{x} × {y} = {a * b}."],
                [W(a * b + min(a, b), "added an extra group"), W(a * b - min(a, b), "left out a group"), W(a * b + 10, "used a wrong fact"), W(a + b, "added")],
                EX(f"{x}*{y}"), qtype="procedural", claim=f"{x} × {y}")


@fam("012")
def fs_double(r, L):
    k = pick(r, [4, 8]) if L else 4
    n = r.randint(3, 9)
    h = k // 2
    return Item(f"{k} × {n} is double {h} × {n}. {h} × {n} = {h * n}. What is {k} × {n}?", k * n,
                [f"Double {h * n}: {h * n} + {h * n} = {k * n}.", f"{k} × {n} = {k * n}."],
                [W(h * n + 2, "added 2 instead of doubling"), W(h * n, "did not double"), W(h * n + n, "added one group instead of doubling")], EX(f"{k}*{n}"), qtype="compare-strategies")


@fam("012")
def fs_add_group(r, L):
    k = pick(r, [6, 3]) if L == 0 else pick(r, [6, 7, 3])
    base = {6: 5, 7: 5, 3: 2}[k]
    n = r.randint(3, 9)
    return Item(f"Use {base} × {n} = {base * n} to find {k} × {n}.", k * n,
                [f"{k} × {n} is {k - base} more {'group' if k - base == 1 else 'groups'} of {n} than {base} × {n}.", f"{base * n} + {(k - base) * n} = {k * n}."],
                [W(base * n + (k - base), f"added {k - base} instead of {k - base} groups of {n}"), W(base * n + n * (k - base + 1), "added too many groups"), W(base * n, "did not add the extra groups")],
                EX(f"{base}*{n}+{k - base}*{n}"), qtype="compare-strategies", tags={"reasoning"})


@fam("12")
def fs_sub_group(r, L):
    n = r.randint(3, 9)
    return Item(f"Use 10 × {n} = {10 * n} to find 9 × {n}.", 9 * n, [f"9 × {n} is one group of {n} less than 10 × {n}.", f"{10 * n} − {n} = {9 * n}."],
                [W(10 * n - 1, "subtracted 1 instead of a group of " + str(n)), W(10 * n - 9, "subtracted 9 instead of " + str(n)), W(10 * n + n, "added a group")],
                EX(f"10*{n}-{n}"), qtype="compare-strategies", tags={"reasoning"})


@fam("012")
def fs_divide(r, L):
    a, b = hard(r, L)
    return Item(f"Divide: {a * b} ÷ {a}", b, [f"Think: {a} × ? = {a * b}.", f"{a} × {b} = {a * b}, so {a * b} ÷ {a} = {b}."],
                [W(b + 1, "used a nearby fact"), W(b - 1, "used a nearby fact"), W(a * b - a, "subtracted")], EX(f"{a * b}/{a}"), qtype="procedural", claim=f"{a * b} ÷ {a}")


@fam("12", mode="mc")
def fs_strategy(r, L):
    a, n = pick(r, [6, 7, 8, 9]), r.randint(4, 9)
    opts = {6: f"5 × {n} plus 1 × {n}", 7: f"5 × {n} plus 2 × {n}", 8: f"double 4 × {n}", 9: f"10 × {n} minus 1 × {n}"}
    good = opts[a]
    bad = {6: [f"5 × {n} plus 1", f"6 × 5 plus 1", f"double 6 × {n}"], 7: [f"5 × {n} plus 2", f"7 × 5 plus {n}", f"double 3 × {n}"],
           8: [f"double 8 × {n}", f"4 × {n} plus 4", f"10 × {n} minus 1"], 9: [f"10 × {n} minus 1", f"10 × {n} minus 10", f"9 × 5 plus {n}"]}[a]
    it = mc_key(f"Which strategy gives the correct product for {a} × {n}?", good, bad, ["Start from a known fact and add or subtract whole groups.", f"{good} = {a * n}."],
                qtype="compare-strategies", tags={"reasoning"}, r=r)
    it.check = FN("strategy", target=f"{a}*{n}")
    return it


@fam("2")
def fs_word(r, L):
    a, b = hard(r, L)
    t = pick(r, [("A week has 7 days. How many days are in {b} weeks?", 7, "days"), ("A spider has 8 legs. How many legs do {b} spiders have?", 8, "legs"),
                 ("Each ant has 6 legs. How many legs do {b} ants have?", 6, "legs"), ("Each pack has 9 stickers. How many stickers are in {b} packs?", 9, "stickers")])
    q, k, u = t
    return Item(q.format(b=b), f"{k * b} {u}", [f"{b} groups of {k}.", f"{b} × {k} = {k * b} {u}."],
                [W(f"{k * b + k} {u}", "added an extra group"), W(f"{k * b - k} {u}", "left out a group"), W(f"{k + b} {u}", "added")],
                EX(f"{b}*{k}", unit=u), qtype="word-problem")


SKILLS = {
    1: dict(name="Commutative Property of Multiplication", fams=[cm_fill, cm_use, cm_array, cm_true, cm_division, cm_known_fact]),
    2: dict(name="Associative Property of Multiplication", fams=[as_fill, as_compute, as_best, as_story, as_same, as_break, as_error, as_missing]),
    3: dict(name="Distributive Property: Break Apart Facts", fams=[di_array, di_fill, di_compute, di_partial, di_choose, di_error]),
    4: dict(name="Multiplying and Dividing with 0 and 1", fams=[z_fact, z_story, z_rule, z_missing, z_divide_zero, z_mixed]),
    5: dict(name="Fact Strategies for 3, 4, 6, 7, 8, and 9", fams=[fs_fact, fs_double, fs_add_group, fs_sub_group, fs_divide, fs_strategy, fs_word]),
}
