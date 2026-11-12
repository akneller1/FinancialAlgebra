"""Unit 6: Multiplying and Dividing Fractions (fraction-multiply-divide)."""
from g5lib import *
from math import gcd

UNIT_ID = "fraction-multiplication-division"


def fs(x):
    return mixed(x)


def ex(x):
    """Expression text for a value written as a mixed number ('2 1/3' -> '(2+1/3)')."""
    s = fs(x)
    return f"({s.replace(' ', '+')})" if " " in s else s


def proper(r, dens):
    d = pick(r, dens)
    return F(r.randint(1, d - 1), d)


def mult_wrongs(a, b):
    a, b = F(a), F(b)
    out = [W(fs(a + b), "added instead of multiplying")]
    if a.denominator > 1 and b.denominator > 1:
        out.append(W(f"{a.numerator * b.numerator}/{a.denominator + b.denominator}", "multiplied the numerators but added the denominators"))
        out.append(W(fs(F(a.numerator * b.denominator, a.denominator * b.numerator)), "multiplied across diagonally (flipped one fraction)"))
    else:
        f_, w = (a, b) if a.denominator > 1 else (b, a)
        out.append(W(fs(F(f_.numerator * w, f_.denominator * w)), "multiplied both the numerator and the denominator by the whole number"))
        out.append(W(fs(w / f_), "divided instead of multiplying"))
        out.append(W(fs(F(f_.numerator + w, f_.denominator)), "added the whole number to the numerator"))
    return out


# ============================================================== S1 Fractions as Division
@fam("012")
def fd_write(r, L):
    d = r.randint(2, 9) if L < 2 else r.randint(3, 15)
    n = r.randint(1, d - 1) if L == 0 else r.randint(d + 1, d * 6)
    need(n % d)
    v = F(n, d)
    return Item(f"Write {n} ÷ {d} as a fraction or mixed number in simplest form.", fs(v),
                [f"{n} ÷ {d} = {n}/{d}.", f"{n}/{d} = {fs(v)}." if n > d else f"{n}/{d} is already a fraction."],
                [W(fs(F(d, n)), "put the divisor on top"), W(f"{n // d} R {n % d}" if n > d else f"{n}.{d}", "wrote a remainder instead of a fraction" if n > d else "wrote the numbers as a decimal"), W(fs(F(n - d * (n // d) + 1, d) + n // d) if n > d else fs(F(n, d + 1)), "made a division slip")],
                EX(f"{n}/{d}", form="mixed"), qtype="procedural", tags={"connections"}, claim=f"{n} ÷ {d}")


@fam("012")
def fd_share(r, L):
    people = r.randint(2, 8)
    items = r.randint(1, people * (1 if L == 0 else 3))
    need(items % people)
    v = F(items, people)
    thing = pick(r, [("pizzas", "pizza"), ("pans of brownies", "pan"), ("pounds of clay", "pounds"), ("sandwiches", "sandwich")])
    return Item(f"{people} friends share {items} {thing[0]} equally. How much does each friend get?", f"{fs(v)} {thing[1]}",
                [f"Each friend gets {items} ÷ {people} = {items}/{people}.", f"= {fs(v)} {thing[1]}."],
                [W(f"{fs(F(people, items))} {thing[1]}", "divided the number of people by the number of items"), W(f"{fs(F(1, people))} {thing[1]}", "gave one share of one item"), W(f"{items // people} {thing[1]}" if items >= people else f"{items} {thing[1]}", "ignored the leftover part")],
                EX(f"{items}/{people}", unit=thing[1], form="mixed"), qtype="word-problem", tags={"modeling"})


@fam("012")
def fd_between(r, L):
    d = r.randint(2, 9)
    n = r.randint(d + 1, d * 9)
    need(n % d)
    lo = n // d
    ans = f"{lo} and {lo + 1}"
    return Item(f"Between which two whole numbers is {n}/{d}? Write your answer like 3 and 4.", ans,
                [f"{n} ÷ {d} = {lo} R {n % d}.", f"So {n}/{d} = {fs(F(n, d))}, which is between {lo} and {lo + 1}."],
                [W(f"{lo + 1} and {lo + 2}", "rounded up first"), W(f"{lo - 1} and {lo}" if lo > 0 else f"{d} and {d + 1}", "made a division mistake"), W(f"{n % d} and {n % d + 1}", "used the remainder")],
                FN("between_whole", x=f"{n}/{d}"), qtype="conceptual", tags={"reasoning"})


@fam("012", mode="mc")
def fd_which(r, L):
    d = r.randint(3, 12)
    n = r.randint(1, d - 1) if L < 2 else r.randint(d + 1, 3 * d)
    need(n % d and gcd(n, d) == 1 and d - n != 0)
    good = f"{n} ÷ {d}"
    bad = [f"{d} ÷ {n}", f"{n} × {d}", f"{d} − {n}" if d > n else f"{n} − {d}"]
    vals = [F(n, d), F(d, n), F(n * d), F(abs(d - n))]
    need(len(set(vals)) == 4)
    opts = [(good, True)] + [(b, False) for b in bad]
    r.shuffle(opts)
    return Item(f"Which expression has the same value as {n}/{d}?", good, ["A fraction bar means division: numerator ÷ denominator.", f"{n}/{d} = {good}."],
                check=FN("same_value", target=f"{n}/{d}"), options=opts, mode="mc", qtype="conceptual", tags={"connections"})


@fam("012")
def fd_circles(r, L):
    people = pick(r, [3, 4, 5, 6])
    items = r.randint(1, people - 1) if L < 2 else r.randint(people + 1, 2 * people - 1)
    v = F(items, people)
    alt = f"{items} circles, each cut into {people} equal pieces. One person's share, one piece from each circle, is shaded: {items} pieces."
    it = Item(f"{items} pies are shared equally by {people} people. Each pie is cut into {people} equal pieces, and each person gets one piece from every pie (shaded). What fraction of a pie does each person get?",
              fs(v), [f"Each person gets {items} pieces, and each piece is 1/{people} of a pie.", f"{items} × 1/{people} = {items}/{people} = {fs(v)} pie."],
              [W(fs(F(1, people)), "counted only one piece"), W(fs(F(people, items)), "divided the wrong way"), W(fs(F(items, people * items)), "used the total number of pieces as the denominator")],
              EX(f"{items}/{people}", form="mixed"), qtype="visual",
              diagram=Diagram("fraction_circle", {"parts": people, "shaded": items, "circles": items, "per_circle": 1}, alt))
    return it


@fam("12")
def fd_word_mixed(r, L):
    d = r.randint(3, 9)
    n = r.randint(d * 3, d * 12)
    need(n % d)
    t = pick(r, [("A {n}-pound bag of rice is split equally into {d} containers. How many pounds are in each container?", "pounds"),
                 ("A {n}-meter rope is cut into {d} equal pieces. How long is each piece?", "meters"),
                 ("{n} cups of soup are poured equally into {d} bowls. How much soup is in each bowl?", "cups")])
    v = F(n, d)
    return Item(t[0].format(n=n, d=d), f"{fs(v)} {t[1]}", [f"{n} ÷ {d} = {n}/{d}.", f"= {fs(v)} {t[1]}."],
                [W(f"{n // d} {t[1]}", "dropped the remainder"), W(f"{n // d} R {n % d} {t[1]}", "left a remainder instead of a fraction"), W(f"{fs(F(d, n))} {t[1]}", "divided the wrong way")],
                EX(f"{n}/{d}", unit=t[1], form="mixed"), qtype="word-problem", tags={"connections"})


# ============================================================== S2 Multiplying a Fraction by a Whole Number
def fw_pair(r, L):
    f_ = proper(r, [2, 3, 4, 5, 6, 8, 10] if L < 2 else [3, 4, 5, 6, 7, 8, 9, 12])
    if L == 0:
        w = f_.denominator * r.randint(1, 8)
    else:
        w = r.randint(2, 30)
    return f_, w


@fam("012")
def fw_compute(r, L):
    f_, w = fw_pair(r, L)
    v = f_ * w
    order = r.random() < 0.5
    e = f"{frac(f_)} × {w}" if order else f"{w} × {frac(f_)}"
    return Item(f"Multiply: {e}", fs(v), [f"{w} × {f_.numerator} = {w * f_.numerator}, so the product is {w * f_.numerator}/{f_.denominator}.", f"= {fs(v)}."],
                mult_wrongs(f_, w), EX(e.replace("×", "*"), form="mixed"), qtype="procedural", claim=e)


@fam("012")
def fw_of(r, L):
    f_, w = fw_pair(r, L)
    need(L > 0 or (f_ * w).denominator == 1)
    v = f_ * w
    return Item(f"What is {frac(f_)} of {w}?", fs(v), [f"Find 1/{f_.denominator} of {w}: {w} ÷ {f_.denominator} = {fs(F(w, f_.denominator))}.", f"Then take {f_.numerator} of those: {fs(v)}."],
                mult_wrongs(f_, w), EX(f"{frac(f_)}*{w}", form="mixed"), qtype="procedural")


@fam("012")
def fw_tape(r, L):
    d = pick(r, [3, 4, 5, 6, 8])
    n = r.randint(1, d - 1)
    each = r.randint(2, 9)
    tot = d * each
    v = n * each
    alt = f"Tape diagram for {tot} split into {d} equal parts with {n} parts shaded."
    return Item(f"The tape diagram shows {tot} split into {d} equal parts. What is {n}/{d} of {tot}?", str(v),
                [f"Each part is {tot} ÷ {d} = {each}.", f"{n} parts: {n} × {each} = {v}."],
                [W(str(each), "found only one part"), W(str(tot - v), "found the unshaded parts"), W(str(tot * n), "multiplied by the numerator only")],
                EX(f"{n}/{d}*{tot}"), qtype="visual", diagram=Diagram("tape", {"parts": d, "shaded": n, "total_label": str(tot)}, alt))


@fam("012")
def fw_repeated(r, L):
    f_ = proper(r, [3, 4, 5, 6, 8])
    k = r.randint(2, 6)
    v = f_ * k
    it = Item(f"What is {' + '.join([frac(f_)] * k)}? Write it as a multiplication and find the value.", fs(v),
              [f"Adding {frac(f_)} {k} times is {k} × {frac(f_)}.", f"{k} × {frac(f_)} = {k * f_.numerator}/{f_.denominator} = {fs(v)}."],
              [W(f"{k * f_.numerator}/{k * f_.denominator}", "added the denominators too"), W(fs(f_ + k), "added the number of copies"), W(fs(F(f_.numerator, f_.denominator * k)), "divided instead of multiplying")],
              EX(f"{k}*{frac(f_)}", form="mixed"), qtype="conceptual", tags={"connections"})
    it.consts = [k]
    return it


@fam("012", mode="mc")
def fw_same(r, L):
    f_, w = fw_pair(r, L)
    a, b = f_.numerator, f_.denominator
    good = f"{a} × {w} ÷ {b}"
    bad = [f"{w} ÷ {a} × {b}", f"{a} + {w} ÷ {b}", f"{b} × {w} ÷ {a}"]
    vals = [F(a * w, b), F(w, a) * b, a + F(w, b), F(b * w, a)]
    need(len(set(vals)) == 4)
    opts = [(good, True)] + [(x, False) for x in bad]
    r.shuffle(opts)
    return Item(f"Which expression has the same value as {frac(f_)} × {w}?", good, [f"(a/b) × q is the same as a × q ÷ b.", f"{frac(f_)} × {w} = {good}."],
                check=FN("same_value", target=f"{frac(f_)}*{w}"), options=opts, mode="mc", qtype="compare-strategies", tags={"multiple-representations"})


@fam("012")
def fw_word(r, L):
    f_, w = fw_pair(r, 0 if L < 2 else 1)
    need((f_ * w).denominator == 1 and w >= 10)
    t = pick(r, [("There are {w} students in a club. {f} of them play soccer. How many play soccer?", "students"),
                 ("A farmer has {w} chickens. {f} of them are brown. How many are brown?", "chickens"),
                 ("{n} has {w} stickers and gives {f} of them to a friend. How many stickers does {n} give away?", "stickers")])
    v = f_ * w
    return Item(t[0].format(w=w, f=frac(f_), n=name(r)), f"{fs(v)} {t[1]}", [f"Find {frac(f_)} of {w}: {w} ÷ {f_.denominator} × {f_.numerator}.", f"= {fs(v)} {t[1]}."],
                [W(f"{w[0]} {t[1]}", w[1]) for w in mult_wrongs(f_, w)], EX(f"{frac(f_)}*{w}", unit=t[1], form="mixed"), qtype="word-problem", tags={"modeling"})


# ============================================================== S3 Multiplying Fractions by Fractions
def ff_pair(r, L):
    if L < 2:
        return proper(r, [2, 3, 4, 5, 6, 8] if L == 0 else [2, 3, 4, 5, 6, 8, 10, 12]), proper(r, [2, 3, 4, 5, 6, 8] if L == 0 else [3, 4, 5, 6, 7, 8, 9])
    a = r.randint(1, 3) + proper(r, [2, 3, 4, 5])
    b = pick(r, [proper(r, [2, 3, 4, 5, 6, 8]), r.randint(1, 2) + proper(r, [2, 3, 4])])
    return a, b


@fam("012")
def ff_compute(r, L):
    a, b = ff_pair(r, L)
    v = a * b
    wr = mult_wrongs(a, b)
    if L == 2:
        wa, fa = int(a), a - int(a)
        wb, fb = int(b), b - int(b)
        wr.insert(0, W(fs(F(wa * wb) + fa * fb), "multiplied the whole numbers and the fractions separately"))
    return Item(f"Multiply: {fs(a)} × {fs(b)}", fs(v), ([f"Write the mixed numbers as fractions: {frac(a)} × {frac(b)}."] if L == 2 else []) +
                [f"Multiply numerators and denominators: {a.numerator * b.numerator}/{a.denominator * b.denominator}.", f"Simplify: {fs(v)}."],
                wr, EX(f"{ex(a)}*{ex(b)}", form="mixed"), qtype="procedural", claim=f"{fs(a)} × {fs(b)}")


@fam("012")
def ff_grid(r, L):
    a, b = proper(r, [2, 3, 4, 5]), proper(r, [2, 3, 4, 5, 6])
    v = a * b
    alt = f"A unit square cut into {a.denominator} rows and {b.denominator} columns. {a.numerator} rows and {b.numerator} columns are shaded; they overlap in {a.numerator * b.numerator} of {a.denominator * b.denominator} small rectangles."
    return Item(f"The square is 1 whole. The model shows {frac(a)} × {frac(b)}. The overlap is the product. What is {frac(a)} × {frac(b)}?", fs(v),
                [f"The overlap has {a.numerator} × {b.numerator} = {a.numerator * b.numerator} parts out of {a.denominator} × {b.denominator} = {a.denominator * b.denominator}.", f"= {a.numerator * b.numerator}/{a.denominator * b.denominator} = {fs(v)}."],
                mult_wrongs(a, b), EX(f"{frac(a)}*{frac(b)}", form="mixed"), qtype="visual",
                diagram=Diagram("area_grid", {"rows": a.denominator, "cols": b.denominator, "sh_rows": a.numerator, "sh_cols": b.numerator, "mode": "overlap",
                                              "left": frac(a), "top": frac(b)}, alt))


CTX_FF = [("{n} has {b} pound of trail mix and eats {a} of it. How many pounds does {n} eat?", "pound"),
          ("A park is {b} mile long. A path covers {a} of the length of the park. How long is the path?", "mile"),
          ("{n} filled {b} of a jar with beads. {a} of the beads are blue. What fraction of the jar is filled with blue beads?", "of the jar")]


@fam("012")
def ff_word(r, L):
    a, b = proper(r, [2, 3, 4, 5, 6]), proper(r, [2, 3, 4, 5, 6, 8])
    t = pick(r, CTX_FF)
    v = a * b
    return Item(t[0].format(a=frac(a), b=frac(b), n=name(r)), f"{fs(v)} {t[1]}", [f"“{frac(a)} of {frac(b)}” means {frac(a)} × {frac(b)}.", f"= {fs(v)} {t[1]}."],
                [W(f"{w[0]} {t[1]}", w[1]) for w in mult_wrongs(a, b)], EX(f"{frac(a)}*{frac(b)}", unit=t[1], form="mixed"), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def ff_which(r, L):
    a, b = ff_pair(r, min(L, 1))
    good = f"{a.numerator} × {b.numerator} / {a.denominator} × {b.denominator}".replace(" / ", ") ÷ (")
    good = f"({a.numerator} × {b.numerator}) ÷ ({a.denominator} × {b.denominator})"
    bad = [f"({a.numerator} + {b.numerator}) ÷ ({a.denominator} + {b.denominator})", f"({a.numerator} × {b.denominator}) ÷ ({a.denominator} × {b.numerator})", f"({a.numerator} × {b.numerator}) ÷ ({a.denominator} + {b.denominator})"]
    vals = [eval_safe(x) for x in [good] + bad]
    need(len(set(vals)) == 4)
    opts = [(good, True)] + [(x, False) for x in bad]
    r.shuffle(opts)
    return Item(f"Which expression has the same value as {frac(a)} × {frac(b)}?", good, ["Multiply the numerators and multiply the denominators.", f"{good} = {fs(a * b)}."],
                check=FN("same_value", target=f"{frac(a)}*{frac(b)}"), options=opts, mode="mc", qtype="conceptual")


def eval_safe(e):
    import re
    s = re.sub(r"(\d+)", r"F(\1)", e.replace("×", "*").replace("÷", "/"))
    return eval(s, {"F": F})


@fam("12")
def ff_mixed_word(r, L):
    a = r.randint(1, 4) + proper(r, [2, 4, 3])
    b = proper(r, [2, 3, 4]) if L == 1 else r.randint(1, 3) + proper(r, [2, 4])
    v = a * b
    t = pick(r, [("Each lap around the track is {a} miles. {n} runs {b} laps. How far does {n} run?", "miles"),
                 ("A recipe uses {a} cups of flour. {n} makes {b} of the recipe. How much flour is used?", "cups")])
    return Item(t[0].format(a=fs(a), b=fs(b), n=name(r)), f"{fs(v)} {t[1]}", [f"Multiply: {fs(a)} × {fs(b)} = {frac(a)} × {frac(b)}.", f"= {fs(v)} {t[1]}."],
                [W(f"{fs(F(int(a) * int(b)) + (a - int(a)) * (b - int(b)))} {t[1]}", "multiplied the whole numbers and the fractions separately") if int(b) else W(f"{fs(F(int(a)) * b)} {t[1]}", "multiplied only the whole number"),
                 W(f"{fs(a + b)} {t[1]}", "added instead of multiplying"), W(f"{fs(a * b + 1)} {t[1]}", "made a mistake converting the mixed numbers")],
                EX(f"{ex(a)}*{ex(b)}", unit=t[1], form="mixed"), qtype="real-world", tags={"modeling"})


# ============================================================== S4 Area with Fractional Side Lengths
@fam("012")
def ar_rect(r, L):
    if L == 0:
        a, b = proper(r, [2, 3, 4]), proper(r, [2, 3, 4, 5])
    elif L == 1:
        a, b = r.randint(1, 4) + proper(r, [2, 4]), proper(r, [2, 3, 4])
    else:
        a, b = r.randint(1, 5) + proper(r, [2, 3, 4]), r.randint(1, 4) + proper(r, [2, 4, 3])
    unit = pick(r, [("feet", "square feet"), ("meters", "square meters"), ("yards", "square yards")])
    v = a * b
    return Item(f"A rectangle is {fs(a)} {unit[0]} long and {fs(b)} {unit[0]} wide. What is its area?", f"{fs(v)} {unit[1]}",
                [f"Area = length × width = {fs(a)} × {fs(b)}.", f"= {fs(v)} {unit[1]}."],
                [W(f"{fs(2 * (a + b))} {unit[1]}", "found the perimeter"), W(f"{fs(a + b)} {unit[1]}", "added the side lengths")] + [W(f"{w[0]} {unit[1]}", w[1]) for w in mult_wrongs(a, b)[1:2]],
                EX(f"{ex(a)}*{ex(b)}", unit=unit[1], form="mixed"), qtype="procedural", claim=f"Area of a {fs(a)} by {fs(b)} rectangle")


@fam("012")
def ar_tiles(r, L):
    b1, b2 = pick(r, [2, 3, 4]), pick(r, [2, 3, 4, 5])
    n1, n2 = r.randint(1, b1 * (1 if L == 0 else 2)), r.randint(1, b2)
    need(not (n1 == b1 and n2 == b2))
    rows, cols = max(b1, n1 if n1 <= b1 else b1 * 2), b2
    a, b = F(n1, b1), F(n2, b2)
    v = a * b
    alt = f"Grid of tiles; each tile is 1/{b1} unit by 1/{b2} unit ({b1 * b2} tiles make 1 square unit). A rectangle {n1} tiles tall and {n2} tiles wide is shaded."
    it = Item(f"Each tile is 1/{b1} unit by 1/{b2} unit, so {b1 * b2} tiles cover 1 square unit. The shaded rectangle is {n1} tiles by {n2} tiles. What is its area in square units?", fs(v),
              [f"The rectangle has {n1} × {n2} = {n1 * n2} tiles, and each tile is 1/{b1 * b2} square unit.", f"Area = {n1 * n2}/{b1 * b2} = {fs(v)} square unit (also {fs(a)} × {fs(b)})."],
              [W(str(n1 * n2), "counted tiles but forgot each is a fraction of a square unit"), W(fs(F(n1 + n2, b1 * b2)), "added the tiles along the sides"), W(fs(F(n1 * n2, b1 + b2)), "used the wrong tile size")],
              EX(f"{n1}/{b1}*{n2}/{b2}", form="mixed"), qtype="visual",
              diagram=Diagram("area_grid", {"rows": rows, "cols": cols, "sh_rows": n1, "sh_cols": n2, "color": "green"}, alt))
    it.consts = [n1, n2]
    return it


@fam("012")
def ar_how_many(r, L):
    b1, b2 = pick(r, [2, 3, 4, 5]), pick(r, [2, 3, 4, 6])
    w = 1 if L < 2 else r.randint(2, 3)
    v = b1 * b2 * w * w
    return Item(f"How many tiles that are 1/{b1} foot by 1/{b2} foot are needed to cover a square that is {w} foot by {w} foot?" if w == 1 else
                f"How many tiles that are 1/{b1} foot by 1/{b2} foot are needed to cover a square that is {w} feet by {w} feet?", str(v),
                [f"Along one side: {w} ÷ 1/{b1} = {w * b1} tiles; along the other: {w} ÷ 1/{b2} = {w * b2} tiles.", f"{w * b1} × {w * b2} = {v} tiles."],
                [W(str(b1 + b2), "added the denominators"), W(fs(F(1, b1 * b2)), "found the area of one tile"), W(str(b1 * b2), "covered only 1 square foot") if w > 1 else W(str(2 * (b1 + b2)), "counted tiles around the edge")],
                FN("tile_count", b1=b1, b2=b2, w=w), qtype="conceptual", tags={"reasoning"})


@fam("012", mode="sa")
def ar_compare(r, L):
    a1, b1 = r.randint(1, 4) + proper(r, [2, 4]), proper(r, [2, 3, 4]) + (r.randint(1, 3) if L else 0)
    a2, b2 = r.randint(1, 4) + proper(r, [2, 3]), proper(r, [2, 4]) + (r.randint(1, 3) if L else 0)
    need(a1 * b1 != a2 * b2)
    ans = "Garden A" if a1 * b1 > a2 * b2 else "Garden B"
    return Item(f"Garden A is {fs(a1)} meters by {fs(b1)} meters. Garden B is {fs(a2)} meters by {fs(b2)} meters. Which garden has the greater area?", ans,
                [f"Garden A: {fs(a1)} × {fs(b1)} = {fs(a1 * b1)} square meters. Garden B: {fs(a2)} × {fs(b2)} = {fs(a2 * b2)} square meters.", f"{ans} is larger."],
                [W("Garden B" if ans == "Garden A" else "Garden A", "compared perimeters or one side only")],
                FN("extreme", values={"Garden A": f"{ex(a1)}*{ex(b1)}", "Garden B": f"{ex(a2)}*{ex(b2)}"}, which="max", expr=True), qtype="real-world", mode="sa")


@fam("012")
def ar_missing(r, L):
    l = r.randint(2, 9)
    A = r.randint(1, l * 4)
    need(A % l)
    w = F(A, l)
    unit = pick(r, [("feet", "square feet"), ("meters", "square meters")])
    return Item(f"A rectangle has an area of {A} {unit[1]}. Its length is {l} {unit[0]}. What is its width?", f"{fs(w)} {unit[0]}",
                [f"Width = area ÷ length = {A} ÷ {l}.", f"{A} ÷ {l} = {A}/{l} = {fs(w)} {unit[0]}."],
                [W(f"{A * l} {unit[0]}", "multiplied instead of dividing"), W(f"{fs(F(l, A))} {unit[0]}", "divided the length by the area"), W(f"{A - l} {unit[0]}" if A > l else f"{A + l} {unit[0]}", "subtracted the length from the area")],
                EX(f"{A}/{l}", unit=unit[0], form="mixed"), qtype="real-world", tags={"connections"})


@fam("012")
def ar_rug(r, L):
    a = r.randint(1, 6) + proper(r, [2, 4])
    b = r.randint(1, 5) + proper(r, [2, 3, 4]) if L else F(r.randint(2, 6))
    v = a * b
    item = pick(r, ["rug", "garden bed", "poster", "tablecloth"])
    return Item(f"A rectangular {item} is {fs(a)} feet by {fs(b)} feet. How many square feet does it cover?", f"{fs(v)} square feet",
                [f"Area = {fs(a)} × {fs(b)} = {frac(a)} × {frac(b)}.", f"= {fs(v)} square feet."],
                [W(f"{fs(2 * (a + b))} square feet", "found the perimeter"), W(f"{fs(F(int(a)) * F(int(b)))} square feet", "multiplied only the whole numbers"), W(f"{fs(a + b)} square feet", "added the sides")],
                EX(f"{ex(a)}*{ex(b)}", unit="square feet", form="mixed"), qtype="real-world", tags={"modeling"})


# ============================================================== S5 Multiplication as Scaling
@fam("012")
def sc_cmp(r, L):
    n = r.randint(6, 90)
    f_ = pick(r, [proper(r, [2, 3, 4, 5, 6, 8]), F(r.randint(5, 15), r.randint(2, 4)), F(1)])
    if L == 0:
        f_ = pick(r, [proper(r, [2, 3, 4]), F(r.randint(5, 9), 4)])
    need(f_ != 1 or L == 2)
    ans = "greater than" if f_ > 1 else "less than" if f_ < 1 else "equal to"
    return Item(f"Without multiplying, is {fs(f_)} × {n} greater than, less than, or equal to {n}?", ans,
                [f"{fs(f_)} is {'greater than' if f_ > 1 else 'less than' if f_ < 1 else 'equal to'} 1.", f"So {fs(f_)} × {n} is {ans} {n}."],
                [W("greater than" if f_ <= 1 else "less than", "thought multiplication always makes numbers bigger" if f_ < 1 else "thought fractions always make numbers smaller"), W("equal to" if f_ != 1 else "greater than", "did not compare the factor with 1")],
                FN("scale_cmp", f=frac(f_)), qtype="conceptual", tags={"reasoning"})


@fam("012", mode="mc")
def sc_greatest(r, L):
    n = r.randint(8, 60)
    fs_ = [proper(r, [2, 3, 4, 5]), F(1), F(r.randint(5, 9), 4), proper(r, [6, 8, 10])]
    need(len(set(fs_)) == 4)
    exprs = [f"{fs(f_)} × {n}" for f_ in fs_]
    best = exprs[fs_.index(max(fs_))]
    opts = [(e, e == best) for e in exprs]
    r.shuffle(opts)
    return Item("Without multiplying, which product is greatest?", best,
                [f"All products have the factor {n}. The greatest other factor gives the greatest product.", f"{fs(max(fs_))} is the greatest factor, so {best} is greatest."],
                check=FN("extreme_expr", exprs=[e.replace(" ", "").replace("×", "*") for e in exprs], which="max", display=exprs), options=opts, mode="mc", qtype="compare-strategies", tags={"reasoning"})


@fam("012", mode="mc")
def sc_why(r, L):
    n = r.randint(6, 40)
    big = r.random() < 0.5
    f_ = F(r.randint(5, 11), 4) if big else proper(r, [3, 4, 5, 6])
    need(f_.denominator > 1)
    if big:
        good = f"{fs(f_)} is greater than 1, so the product is greater than {n}."
        bad = [f"{fs(f_)} is a fraction, so the product is less than {n}.", f"Multiplying always makes a number greater.", f"{fs(f_)} has a denominator of {f_.denominator}, so the product is {n * f_.denominator}."]
    else:
        good = f"{fs(f_)} is less than 1, so the product is less than {n}."
        bad = [f"Multiplying always makes a number greater, so the product is greater than {n}.", f"{fs(f_)} is less than 1, so the product is greater than {n}.", f"The product equals {n} because {f_.numerator} is less than {f_.denominator}."]
    return mc_key(f"Why is {fs(f_)} × {n} {'greater' if big else 'less'} than {n}?", good, bad, ["Compare the other factor with 1.", good], r=r, qtype="explain", tags={"reasoning"})


@fam("012", mode="mc")
def sc_equiv(r, L):
    a = proper(r, [2, 3, 4, 5, 6])
    k = r.randint(2, 6)
    good = f"{a.numerator * k}/{a.denominator * k}, because {k}/{k} = 1"
    bad = [f"{a.numerator * k}/{a.denominator}, because {k}/{k} = {k}", f"{a.numerator + k}/{a.denominator + k}, because the same number was added", f"{a.numerator}/{a.denominator * k}, because the parts got smaller"]
    return mc_key(f"What is {frac(a)} × {k}/{k}? Why?", good, bad, [f"{k}/{k} = 1, and multiplying by 1 does not change a value.", f"{frac(a)} × {k}/{k} = {a.numerator * k}/{a.denominator * k}, an equivalent fraction."],
                  r=r, qtype="explain", tags={"reasoning"})


@fam("012")
def sc_how_many_times(r, L):
    n = r.randint(4, 40)
    f_ = proper(r, [2, 3, 4, 5]) if r.random() < 0.5 else F(r.randint(3, 5))
    return Item(f"A poster is {n} inches wide. A copy is made that is {fs(f_)} times as wide. How wide is the copy?", f"{fs(f_ * n)} inches",
                [f"Scaling by {fs(f_)} means multiplying: {fs(f_)} × {n}.", f"= {fs(f_ * n)} inches."],
                [W(f"{fs(n + f_)} inches", "added the scale factor"), W(f"{fs(n / f_)} inches", "divided by the scale factor"), W(f"{n} inches", "kept the same width")],
                EX(f"{frac(f_)}*{n}", unit="inches", form="mixed"), qtype="real-world", tags={"connections"})


# ============================================================== S6 Dividing Unit Fractions and Whole Numbers
@fam("012")
def du_unit_by_whole(r, L):
    d = r.randint(2, 8 if L < 2 else 12)
    w = r.randint(2, 6 if L < 2 else 10)
    v = F(1, d * w)
    return Item(f"Divide: 1/{d} ÷ {w}", frac(v), [f"Split 1/{d} into {w} equal parts. Each part is 1/{d * w}.", f"Check: 1/{d * w} × {w} = 1/{d}."],
                [W(fs(F(w, d)), "multiplied instead of dividing"), W(f"1/{d + w}", "added the denominator and the divisor"), W(fs(F(d, w)), "divided the denominator by the whole number")],
                EX(f"1/{d}/{w}", form="frac"), qtype="procedural", claim=f"1/{d} ÷ {w}")


@fam("012")
def du_whole_by_unit(r, L):
    d = r.randint(2, 8 if L < 2 else 12)
    w = r.randint(2, 9 if L < 2 else 20)
    v = w * d
    return Item(f"Divide: {w} ÷ 1/{d}", str(v), [f"Each whole has {d} pieces of size 1/{d}.", f"{w} wholes have {w} × {d} = {v} pieces."],
                [W(frac(F(w, d)), "divided the whole number by the denominator"), W(frac(F(1, w * d)), "found a unit fraction instead"), W(str(w + d), "added")],
                EX(f"{w}/(1/{d})"), qtype="procedural", claim=f"{w} ÷ 1/{d}")


@fam("012")
def du_numberline(r, L):
    d = pick(r, [2, 3, 4])
    w = r.randint(1, 3)
    v = w * d
    jumps = [[frac(F(i, d)), frac(F(i + 1, d))] for i in range(v)]
    alt = f"Number line from 0 to {w} with marks every 1/{d}, showing {v} equal jumps of 1/{d}."
    return Item(f"The number line shows how many jumps of 1/{d} fit from 0 to {w}. What is {w} ÷ 1/{d}?", str(v),
                [f"Count the jumps: each is 1/{d}.", f"There are {v} jumps, so {w} ÷ 1/{d} = {v}."],
                [W(frac(F(w, d)), "divided the whole number by the denominator"), W(str(v + 1), "counted tick marks instead of jumps"), W(str(d), "counted the jumps in only one whole") if w > 1 else W(str(v - 1), "skipped a jump")],
                EX(f"{w}/(1/{d})"), qtype="visual",
                diagram=Diagram("number_line", {"lo": "0", "hi": str(w), "den": d, "labels": "all", "jumps": jumps}, alt))


@fam("012")
def du_bars(r, L):
    d = pick(r, [2, 3, 4])
    w = pick(r, [2, 3, 4])
    v = F(1, d * w)
    alt = f"Two bars of the same whole: the first cut into {d} parts with 1 part shaded (1/{d}); the second cut into {d * w} parts with 1 part shaded, showing the shaded 1/{d} split into {w} equal pieces."
    return Item(f"The model shows 1/{d} split into {w} equal parts. What is 1/{d} ÷ {w}?", frac(v),
                [f"Splitting 1/{d} into {w} parts makes {d * w} parts in the whole.", f"Each part is 1/{d * w}."],
                [W(fs(F(w, d)), "multiplied instead of dividing"), W(f"1/{d + w}", "added"), W(f"{w}/{d}", "put the divisor on top")],
                EX(f"1/{d}/{w}", form="frac"), qtype="visual",
                diagram=Diagram("fraction_bars", {"bars": [{"parts": d, "shaded": 1, "label": f"1/{d}"}, {"parts": d * w, "shaded": 1, "label": "?"}]}, alt))


@fam("012", mode="mc")
def du_check(r, L):
    d, w = r.randint(2, 9), r.randint(2, 6)
    kind = r.random() < 0.5
    if kind:
        good = f"1/{d * w} × {w} = 1/{d}"
        bad = [f"1/{d} × {w} = {fs(F(w, d))}", f"1/{d * w} + {w} = 1/{d}", f"{w} × {d} = {w * d}"]
        q = f"Which equation checks that 1/{d} ÷ {w} = 1/{d * w}?"
    else:
        good = f"{w * d} × 1/{d} = {w}"
        bad = [f"{w} × 1/{d} = {fs(F(w, d))}", f"{w * d} + 1/{d} = {w}", f"{w} × {d} = {w * d}"]
        q = f"Which equation checks that {w} ÷ 1/{d} = {w * d}?"
    return mc_key(q, good, bad, ["Multiply the quotient by the divisor to get the dividend.", good], r=r, qtype="conceptual", tags={"connections"})


@fam("012", mode="mc")
def du_story(r, L):
    d, w = r.randint(2, 6), r.randint(2, 8)
    kind = r.random() < 0.5
    if kind:
        e = f"{w} ÷ 1/{d}"
        good = f"How many 1/{d}-cup servings are in {w} cups of yogurt?"
        bad = [f"{w} friends share 1/{d} cup of yogurt equally. How much does each get?", f"What is 1/{d} of {w} cups of yogurt?", f"How much yogurt is in {w} servings of {d} cups each?"]
    else:
        e = f"1/{d} ÷ {w}"
        good = f"{w} friends share 1/{d} pound of cheese equally. How much does each get?"
        bad = [f"How many 1/{d}-pound pieces are in {w} pounds of cheese?", f"What is {w} times 1/{d} pound of cheese?", f"How many pounds are {w} pieces of 1/{d} pound?"]
    return mc_key(f"Which story matches {e}?", good, bad, [f"“How many groups of 1/{d} fit in {w}?” is {w} ÷ 1/{d}. “Share 1/{d} among {w}” is 1/{d} ÷ {w}.", good], r=r, qtype="word-problem", tags={"modeling"})


@fam("012")
def du_bigger(r, L):
    w = r.randint(2, 20)
    d = r.randint(2, 9)
    return Item(f"Without dividing, is {w} ÷ 1/{d} greater than or less than {w}?", "greater than",
                [f"Many small pieces of size 1/{d} fit into {w}.", f"{w} ÷ 1/{d} = {w * d}, which is greater than {w}."],
                [W("less than", "thought dividing always makes a number smaller")], FN("div_cmp", n=w, d=f"1/{d}"), qtype="conceptual", mode="sa", tags={"reasoning"})


# ============================================================== S7 Word Problems
@fam("012")
def wp_recipe(r, L):
    a = proper(r, [2, 3, 4]) + (r.randint(1, 2) if L else 0)
    b = proper(r, [2, 3, 4])
    v = a * b
    return Item(f"A recipe needs {fs(a)} cups of sugar. {name(r)} makes {frac(b)} of the recipe. How much sugar is needed?", f"{fs(v)} cups",
                [f"Find {frac(b)} of {fs(a)}: {frac(b)} × {fs(a)}.", f"= {fs(v)} cups."],
                [W(f"{fs(a + b)} cups", "added instead of multiplying"), W(f"{fs(a - b) if a > b else fs(b - a)} cups", "subtracted"), W(f"{fs(a / b)} cups", "divided instead of multiplying")],
                EX(f"{frac(b)}*{ex(a)}", unit="cups", form="mixed"), qtype="real-world", tags={"modeling"})


@fam("012")
def wp_servings(r, L):
    d, w = r.randint(2, 8), r.randint(2, 12)
    t = pick(r, [("How many 1/{d}-cup servings are in {w} cups of trail mix?", "servings"), ("A {w}-foot board is cut into pieces that are 1/{d} foot long. How many pieces are there?", "pieces"),
                 ("{n} has {w} pounds of birdseed. Each feeder holds 1/{d} pound. How many feeders can {n} fill?", "feeders")])
    v = w * d
    return Item(t[0].format(d=d, w=w, n=name(r)), f"{v} {t[1]}", [f"Find how many 1/{d}s are in {w}: {w} ÷ 1/{d}.", f"= {w} × {d} = {v} {t[1]}."],
                [W(f"{fs(F(w, d))} {t[1]}", "divided the whole number by the denominator"), W(f"{w + d} {t[1]}", "added"), W(f"{fs(F(1, w * d))} {t[1]}", "divided the unit fraction by the whole number")],
                EX(f"{w}/(1/{d})", unit=t[1]), qtype="word-problem", tags={"modeling"})


@fam("012")
def wp_share(r, L):
    d, w = r.randint(2, 6), r.randint(2, 8)
    t = pick(r, [("{w} friends share 1/{d} pound of chocolate equally. How much chocolate does each friend get?", "pound"),
                 ("1/{d} of a pan of lasagna is split equally among {w} people. What fraction of the pan does each person get?", "of the pan")])
    v = F(1, d * w)
    return Item(t[0].format(d=d, w=w), f"{frac(v)} {t[1]}", [f"Divide: 1/{d} ÷ {w}.", f"= 1/{d * w} {t[1]}."],
                [W(f"{fs(F(w, d))} {t[1]}", "multiplied instead of dividing"), W(f"{w * d} {t[1]}", "divided the whole number by the unit fraction"), W(f"1/{d + w} {t[1]}", "added")],
                EX(f"1/{d}/{w}", unit=t[1], form="frac"), qtype="word-problem", tags={"modeling"})


@fam("012")
def wp_laps(r, L):
    a = r.randint(1, 3) + proper(r, [2, 4])
    b = r.randint(2, 5) + (proper(r, [2]) if L == 2 else 0)
    v = a * b
    return Item(f"One lap around a park is {fs(a)} miles. {name(r)} walks {fs(b)} laps. How many miles is that?", f"{fs(v)} miles",
                [f"Multiply: {fs(a)} × {fs(b)}.", f"= {fs(v)} miles."],
                [W(f"{fs(a + b)} miles", "added instead of multiplying"), W(f"{fs(F(int(a)) * b)} miles", "multiplied only the whole-number part"), W(f"{fs(a * int(b))} miles" if b != int(b) else f"{fs(v + 1)} miles", "ignored part of a lap" if b != int(b) else "made a regrouping mistake")],
                EX(f"{ex(a)}*{ex(b)}", unit="miles", form="mixed"), qtype="real-world", tags={"modeling"})


@fam("12")
def wp_two_step(r, L):
    w = r.randint(2, 6) * 3
    used = F(r.randint(1, 2), 3)
    piece = F(1, pick(r, [2, 4]))
    left = w - used * w
    v = left / piece
    need(v.denominator == 1)
    return Item(f"{name(r)} has a {w}-foot board and uses {frac(used)} of it for a shelf. The rest is cut into pieces that are {frac(piece)} foot long. How many pieces are there?", f"{int(v)} pieces",
                [f"Used: {frac(used)} × {w} = {fs(used * w)} feet. Left: {w} − {fs(used * w)} = {fs(left)} feet.", f"{fs(left)} ÷ {frac(piece)} = {int(v)} pieces."],
                [W(f"{fs(w / piece)} pieces", "cut the whole board into pieces"), W(f"{fs(used * w / piece)} pieces", "cut the shelf part instead of the rest"), W(f"{fs(left * piece)} pieces", "multiplied instead of dividing")],
                EX(f"({w}-{frac(used)}*{w})/({frac(piece)})", unit="pieces"), qtype="multi-step", tags={"multistep"})


@fam("012", mode="mc")
def wp_which_op(r, L):
    d, w = r.randint(2, 6), r.randint(2, 9)
    kind = pick(r, ["mult", "div_wu", "div_uw"])
    if kind == "mult":
        q = f"{name(r)} runs 1/{d} mile each day for {w} days. How far does {name(r)} run in all?"
        good, bad = f"{w} × 1/{d}", [f"{w} ÷ 1/{d}", f"1/{d} ÷ {w}", f"{w} + 1/{d}"]
    elif kind == "div_wu":
        q = f"How many 1/{d}-meter pieces can be cut from {w} meters of string?"
        good, bad = f"{w} ÷ 1/{d}", [f"1/{d} ÷ {w}", f"{w} × 1/{d}", f"{w} − 1/{d}"]
    else:
        q = f"{w} kids share 1/{d} of a cake equally. What fraction of the cake does each kid get?"
        good, bad = f"1/{d} ÷ {w}", [f"{w} ÷ 1/{d}", f"{w} × {d}", f"1/{d} + {w}"]
    return mc_key(f"{q} Which expression solves the problem?", good, bad, ["Decide if you are joining equal groups (×), finding how many groups (÷), or sharing (÷).", good],
                  r=r, qtype="word-problem", tags={"modeling"})


SKILLS = {
    1: dict(name="Fractions as Division", fams=[fd_write, fd_share, fd_between, fd_which, fd_circles, fd_word_mixed]),
    2: dict(name="Multiplying a Fraction by a Whole Number", fams=[fw_compute, fw_of, fw_tape, fw_repeated, fw_same, fw_word]),
    3: dict(name="Multiplying Fractions by Fractions", fams=[ff_compute, ff_grid, ff_word, ff_which, ff_mixed_word]),
    4: dict(name="Area with Fractional Side Lengths", fams=[ar_rect, ar_tiles, ar_how_many, ar_compare, ar_missing, ar_rug]),
    5: dict(name="Multiplication as Scaling", fams=[sc_cmp, sc_greatest, sc_why, sc_equiv, sc_how_many_times]),
    6: dict(name="Dividing Unit Fractions and Whole Numbers", fams=[du_unit_by_whole, du_whole_by_unit, du_numberline, du_bars, du_check, du_story, du_bigger]),
    7: dict(name="Fraction Multiplication and Division Word Problems", fams=[wp_recipe, wp_servings, wp_share, wp_laps, wp_two_step, wp_which_op]),
}
