"""Unit 7: Fraction Operations and Decimals (4.NF.B.3, 4.NF.B.4, 4.NF.C.5-7)."""
from g4lib import *
from math import gcd

UNIT_ID = "fraction-operations-decimals"
DENS = {0: [3, 4, 5, 6, 8], 1: [4, 5, 6, 8, 10, 12], 2: [5, 6, 8, 10, 12, 100]}
FOODS = [("cup", "cups", "of flour"), ("mile", "miles", ""), ("hour", "hours", ""), ("yard", "yards", "of ribbon"), ("pound", "pounds", "of apples"), ("liter", "liters", "of juice"), ("foot", "feet", "of rope")]


def fr(n, d):
    return f"{n}/{d}"


def mx(n, d):
    """n/d as a whole or mixed number with the same denominator (not simplified)."""
    w, rem = divmod(n, d)
    return str(w) if rem == 0 else (fr(rem, d) if w == 0 else f"{w} {rem}/{d}")


def den(r, L):
    return pick(r, DENS[L])


def unit_txt(v, t):
    return t[0] if v <= 1 else t[1]


# ============================================================== S1 Decomposing Fractions
@fam("012", mode="mc")
def dc_unit_sum(r, L):
    d = den(r, min(L, 1))
    n = r.randint(2, min(d - 1, 5))
    good = " + ".join([fr(1, d)] * n)
    bad = [" + ".join([fr(1, d)] * (n + 1)) if n + 1 <= d else " + ".join([fr(1, d)] * (n - 1)), " + ".join([fr(1, n)] * d) if d <= 6 else " + ".join([fr(1, n)] * 3), f"{fr(n, d)} + {fr(1, d)}"]
    return Item(f"Which shows {fr(n, d)} as a sum of unit fractions?", good, [f"A unit fraction has a numerator of 1. {fr(n, d)} is {n} copies of {fr(1, d)}.", f"{fr(n, d)} = {good}."],
                [W(bad[0], "used the wrong number of unit fractions"), W(bad[1], "switched the numerator and denominator"), W(bad[2], "this sum is more than the fraction")],
                FN("unit_sum", f=fr(n, d)), qtype="conceptual")


@fam("012")
def dc_missing(r, L):
    d = den(r, L)
    n = r.randint(3, d - 1) if L < 2 else r.randint(d + 1, 2 * d - 1)
    a = r.randint(1, n - 2)
    if L == 2 and r.random() < 0.5:
        b = r.randint(1, n - a - 1)
        c = n - a - b
        return Item(f"Fill in the blank with a fraction: {fr(n, d)} = {fr(a, d)} + {fr(b, d)} + ___", fr(c, d), [f"The numerators must add to {n}: {a} + {b} + ? = {n}.", f"The missing fraction is {fr(c, d)}."],
                    [W(fr(n - a, d), "subtracted only one of the parts"), W(fr(a + b, d), "added the parts instead of finding what is missing"), W(fr(c, 3 * d), "changed the denominator"), W(fr(c + 1, d), "made a subtraction mistake")],
                    FN("frac_with_den", f=fr(c, d), den=d), qtype="fill-blank")
    return Item(f"Fill in the blank with a fraction: {fr(n, d)} = {fr(a, d)} + ___", fr(n - a, d), [f"The numerators must add to {n}: {a} + ? = {n}.", f"The missing fraction is {fr(n - a, d)}."],
                [W(fr(n + a, d), "added instead of finding the missing part"), W(fr(n - a, 2 * d), "changed the denominator"), W(fr(n - a + 1, d), "made a subtraction mistake"), W(fr(a, d), "repeated the part that was given")],
                FN("frac_with_den", f=fr(n - a, d), den=d), qtype="fill-blank")


@fam("012", mode="mc")
def dc_which(r, L):
    d = den(r, L)
    n = r.randint(3, d - 1)
    a = r.randint(1, n - 1)
    not_ = r.random() < 0.35
    ways = [f"{fr(x, d)} + {fr(n - x, d)}" for x in range(1, n // 2 + 1)]
    three = f"{fr(1, d)} + {fr(1, d)} + {fr(n - 2, d)}" if n > 2 else None
    wrongs_ = [f"{fr(a, d)} + {fr(n - a + 1, d)}", f"{fr(a, 2 * d)} + {fr(n - a, 2 * d)}", f"{fr(n, d)} + {fr(n, d)}", f"{fr(a, d)} + {fr(a, d)}" if 2 * a != n else f"{fr(a, d)} + {fr(a + 1, d)}"]
    if not_:
        pool = ways + ([three] if three else [])
        need(len(pool) >= 3)
        good = wrongs_[0]
        return Item(f"Which is NOT a way to decompose {fr(n, d)}?", good, ["Add the numerators of each choice. The sum must be " + str(n) + f" with the denominator {d}.", f"{good} does not equal {fr(n, d)}."],
                    [W(x, f"this sum equals {fr(n, d)}") for x in r.sample(pool, 3)], FN("expr_ne", e=fr(n, d)), qtype="conceptual", tags={"reasoning"})
    good = pick(r, ways + ([three] if three else []))
    return Item(f"Which shows a way to decompose {fr(n, d)}?", good, [f"The parts must have the same denominator, {d}, and the numerators must add to {n}.", f"{good} = {fr(n, d)}."],
                [W(wrongs_[0], "the numerators do not add to the correct total"), W(wrongs_[1], "changed the denominator"), W(wrongs_[2], "used the whole fraction twice")], FN("expr_eq", e=fr(n, d)), qtype="conceptual", tags={"reasoning"})


@fam("012")
def dc_to_mixed(r, L):
    d = den(r, L)
    w = r.randint(1, 2 if L == 0 else 5)
    k = r.randint(1, d - 1)
    n = w * d + k
    if r.random() < 0.5:
        return Item(f"Write {fr(n, d)} as a mixed number.", f"{w} {fr(k, d)}", [f"{d} pieces of this size make 1 whole. {n} ÷ {d} = {w} R {k}.", f"{fr(n, d)} = {w} {fr(k, d)}."],
                    [W(f"{k} {fr(w, d)}", "switched the whole number and the numerator"), W(f"{w + 1} {fr(k, d)}", "counted one whole too many"), W(f"{w} {fr(k + 1, d)}" if k + 1 < d else f"{w} {fr(k - 1, d)}", "made a subtraction mistake"), W(f"{n} {fr(1, d)}", "did not group the pieces into wholes")],
                    EX(fr(n, d)), claim=f"{fr(n, d)} as a mixed number")
    return Item(f"Write {w} {fr(k, d)} as a fraction greater than 1.", fr(n, d), [f"Each whole is {fr(d, d)}. {w} wholes = {fr(w * d, d)}.", f"{fr(w * d, d)} + {fr(k, d)} = {fr(n, d)}."],
                [W(fr(w + k, d), "added the whole number to the numerator"), W(fr(w * k, d), "multiplied the whole number by the numerator"), W(fr(n + d, d), "counted one whole too many"), W(fr(w * d, d), "forgot to add the fraction part")],
                FN("frac_with_den", f=fr(n, d), den=d), claim=f"{w} {fr(k, d)} as a fraction")


@fam("012")
def dc_wholes(r, L):
    d = den(r, L)
    w = r.randint(1, 3 if L < 2 else 6)
    return Item(f"Fill in the blank: {w} = ___/{d}. (Write only the missing numerator.)", str(w * d), [f"One whole is {fr(d, d)}.", f"{w} wholes = {w} × {d} = {w * d} pieces, so {w} = {fr(w * d, d)}."],
                [W(str(w), "used the whole number as the numerator"), W(str(d), "wrote the numerator for only one whole"), W(str(w + d), "added instead of multiplying"), W(str(w * d + 1), "made a multiplication mistake")],
                EX(f"{w} × {d}"), qtype="fill-blank")


@fam("12")
def dc_count_ways(r, L):
    d = den(r, L)
    n = r.randint(4, min(d - 1, 9))
    ways = [f"{fr(x, d)} + {fr(n - x, d)}" for x in range(1, n // 2 + 1)]
    return Item(f"{name(r)} writes {fr(n, d)} as a sum of two fractions that both have a denominator of {d} and numerators of at least 1. The order of the two fractions does not matter. How many different sums are possible?", str(len(ways)),
                ["List them in order: " + "; ".join(ways) + ".", f"There are {len(ways)} different sums."],
                [W(str(n - 1), "counted the same pair twice in a different order"), W(str(n), "used the numerator"), W(str(len(ways) + 1), "counted a sum with a numerator of 0"), W(str(d), "used the denominator")],
                FN("two_part_ways", n=n), qtype="multi-step", tags={"reasoning", "challenge"})


# ============================================================== S2 Adding and Subtracting Fractions with Like Denominators
def like_pair(r, L, over=False):
    d = den(r, L)
    for _ in range(40):
        a, b = r.randint(1, d - 1), r.randint(1, d - 1)
        if (a + b > d) == over and a + b != d and a != b:
            return a, b, d
    raise Reject()


def add_wr(a, b, d, unit=""):
    u = (" " + unit) if unit else ""
    return [W(fr(a + b, 2 * d) + u, "added the denominators too"), W(mx(abs(a - b), d) + u, "subtracted instead of adding"), W(mx(a + b + 1, d) + u, "made an addition mistake"), W(fr(a * b, d) + u if a * b != a + b else fr(a + b, d + 1) + u, "multiplied the numerators")]


def sub_wr(a, b, d, unit=""):
    u = (" " + unit) if unit else ""
    return [W(mx(a + b, d) + u, "added instead of subtracting"), W(mx(a - b + 1, d) + u, "made a subtraction mistake"), W(fr(a, d) + u, "did not subtract"), W(fr(a - b, 2 * d) + u, "changed the denominator")]


@fam("012")
def al_add(r, L):
    a, b, d = like_pair(r, L, over=(L == 2 and r.random() < 0.5))
    return Item(f"Add: {fr(a, d)} + {fr(b, d)}", mx(a + b, d), [f"The denominators are the same, so add the numerators: {a} + {b} = {a + b}.", f"{fr(a, d)} + {fr(b, d)} = {fr(a + b, d)}" + (f" = {mx(a + b, d)}." if a + b > d else ".")],
                add_wr(a, b, d), EX(f"{a}/{d} + {b}/{d}"), claim=f"{fr(a, d)} + {fr(b, d)}")


@fam("012")
def al_sub(r, L):
    a, b, d = like_pair(r, L)
    a, b = max(a, b), min(a, b)
    return Item(f"Subtract: {fr(a, d)} − {fr(b, d)}", fr(a - b, d), [f"The denominators are the same, so subtract the numerators: {a} − {b} = {a - b}.", f"{fr(a, d)} − {fr(b, d)} = {fr(a - b, d)}."],
                sub_wr(a, b, d), EX(f"{a}/{d} − {b}/{d}"), claim=f"{fr(a, d)} − {fr(b, d)}")


@fam("012")
def al_missing(r, L):
    a, b, d = like_pair(r, L)
    s = a + b
    return Item(f"Find the missing fraction: {fr(a, d)} + ___ = {mx(s, d) if s < d else fr(s, d)}", fr(b, d), [f"Subtract the numerators: {s} − {a} = {b}.", f"The missing fraction is {fr(b, d)}."],
                [W(mx(s + a, d), "added instead of subtracting"), W(fr(b, 2 * d), "changed the denominator"), W(fr(b + 1, d), "made a subtraction mistake"), W(fr(a, d), "repeated the addend")],
                EX(f"{s}/{d} − {a}/{d}"), qtype="fill-blank")


@fam("012")
def al_from_one(r, L):
    d = den(r, L)
    a = r.randint(1, d - 1)
    return Item(f"Subtract: 1 − {fr(a, d)}", fr(d - a, d), [f"Write 1 as {fr(d, d)}.", f"{fr(d, d)} − {fr(a, d)} = {fr(d - a, d)}."],
                [W(fr(a, d), "did not subtract"), W(fr(a - 1, d) if a > 1 else fr(1, d + 1), "subtracted 1 from the numerator"), W(fr(d - a + 1, d), "made a subtraction mistake"), W(fr(1, d), "used a unit fraction")],
                EX(f"1 − {a}/{d}"), qtype="conceptual", claim=f"1 − {fr(a, d)}")


@fam("012")
def al_word_add(r, L):
    a, b, d = like_pair(r, L, over=(L == 2 and r.random() < 0.5))
    t = pick(r, FOODS)
    n1 = name(r)
    verb = pick(r, [("used", "use"), ("walked", "walk")] if t[2] in ("", "of ribbon", "of rope", "of flour") else [("bought", "buy")])
    if t[0] in ("mile",):
        s = f"{n1} walked {fr(a, d)} mile before lunch and {fr(b, d)} mile after lunch. How far did {n1} walk in all?"
    elif t[0] == "hour":
        s = f"{n1} practiced piano for {fr(a, d)} hour on Monday and {fr(b, d)} hour on Tuesday. How long did {n1} practice in all?"
    else:
        s = f"{n1} used {fr(a, d)} {t[0]} {t[2]} for one project and {fr(b, d)} {t[0]} {t[2]} for another. How much did {n1} use in all?"
    u = t[1] if a + b > d else t[0]
    return Item(s, f"{mx(a + b, d)} {u}", ["“In all” means add. The denominators are the same.", f"{fr(a, d)} + {fr(b, d)} = {fr(a + b, d)}" + (f" = {mx(a + b, d)}" if a + b > d else "") + f" {u}."],
                add_wr(a, b, d, u), EX(f"{a}/{d} + {b}/{d}", unit=u), qtype="word-problem")


@fam("012")
def al_word_sub(r, L):
    a, b, d = like_pair(r, L)
    a, b = max(a, b), min(a, b)
    n1 = name(r)
    s = pick(r, [(f"A water bottle holds {fr(a, d)} liter. {n1} drinks {fr(b, d)} liter. How much water is left?", "liter"),
                 (f"{n1} has {fr(a, d)} yard of fabric and uses {fr(b, d)} yard. How much fabric is left?", "yard"),
                 (f"A trail is {fr(a, d)} mile long. {n1} has hiked {fr(b, d)} mile. How much farther is it to the end of the trail?", "mile"),
                 (f"A recipe needs {fr(a, d)} cup of sugar. {n1} has {fr(b, d)} cup. How much more sugar is needed?", "cup")])
    return Item(s[0], f"{fr(a - b, d)} {s[1]}", ["Subtract to find what is left. The denominators are the same.", f"{fr(a, d)} − {fr(b, d)} = {fr(a - b, d)} {s[1]}."],
                sub_wr(a, b, d, s[1]), EX(f"{a}/{d} − {b}/{d}", unit=s[1]), qtype="word-problem")


@fam("012")
def al_model(r, L):
    a, b, d = like_pair(r, min(L, 1))
    need(d <= 12)
    alt = f"Two fraction bars of the same length, each cut into {d} equal parts. The first bar has {a} parts shaded. The second bar has {b} parts shaded."
    return Item(f"Each bar is one whole cut into {d} equal parts. What is the total amount shaded in both bars?", mx(a + b, d),
                [f"The bars show {fr(a, d)} and {fr(b, d)}.", f"{fr(a, d)} + {fr(b, d)} = {fr(a + b, d)}."], add_wr(a, b, d),
                FN("bars_sum", bars=[[d, a], [d, b]]), qtype="visual", diagram=Diagram("fraction_bars", {"bars": [{"parts": d, "shaded": a}, {"parts": d, "shaded": b}]}, alt), tags={"modeling"})


@fam("12")
def al_three(r, L):
    d = den(r, L)
    a, b = r.randint(2, d - 1), r.randint(2, d - 1)
    c = r.randint(1, a + b - 1)
    v = a + b - c
    return Item(f"Find the value: {fr(a, d)} + {fr(b, d)} − {fr(c, d)}", mx(v, d), [f"Work with the numerators: {a} + {b} − {c} = {v}.", f"The answer is {fr(v, d)}" + (f" = {mx(v, d)}." if v >= d else ".")],
                [W(mx(a + b + c, d), "added all three fractions"), W(mx(a + b, d), "forgot to subtract"), W(fr(v, 3 * d), "combined the denominators"), W(mx(v + 1, d), "made a computation mistake")],
                EX(f"{a}/{d} + {b}/{d} − {c}/{d}"), qtype="multi-step", tags={"multistep"})


# ============================================================== S3 Adding and Subtracting Mixed Numbers
def mixed_pair(r, L, regroup):
    d = den(r, L)
    for _ in range(60):
        w1, w2 = r.randint(1, 4 if L == 0 else 9), r.randint(1, 3 if L == 0 else 6)
        a, b = r.randint(1, d - 1), r.randint(1, d - 1)
        if (a + b >= d) == regroup:
            return w1, a, w2, b, d
    raise Reject()


@fam("012")
def mxa_add(r, L):
    w1, a, w2, b, d = mixed_pair(r, L, regroup=(L > 0 and r.random() < 0.6))
    tot = (w1 + w2) * d + a + b
    steps = [f"Add the wholes: {w1} + {w2} = {w1 + w2}. Add the fractions: {fr(a, d)} + {fr(b, d)} = {fr(a + b, d)}."]
    if a + b >= d:
        steps.append(f"{fr(a + b, d)} = {mx(a + b, d)}, so regroup: {w1 + w2} + {mx(a + b, d)} = {mx(tot, d)}.")
    else:
        steps.append(f"The sum is {mx(tot, d)}.")
    return Item(f"Add: {w1} {fr(a, d)} + {w2} {fr(b, d)}", mx(tot, d), steps,
                [W(f"{w1 + w2} {fr(a + b, 2 * d)}", "added the denominators"), W(f"{w1 + w2} {fr(a + b, d)}" if a + b >= d else mx(tot + d, d), "did not regroup the fraction" if a + b >= d else "added an extra whole"),
                 W(mx(tot - d, d) if tot - d > 0 else mx(tot + 1, d), "lost a whole when regrouping"), W(mx(tot + 1, d), "made an addition mistake")],
                EX(f"{w1} + {a}/{d} + {w2} + {b}/{d}"), claim=f"{w1} {fr(a, d)} + {w2} {fr(b, d)}")


@fam("012")
def mxa_sub(r, L):
    d = den(r, L)
    w1 = r.randint(3, 6 if L == 0 else 12)
    w2 = r.randint(1, w1 - 1)
    a, b = r.randint(1, d - 1), r.randint(1, d - 1)
    regroup = L > 0 and r.random() < 0.6
    need((a < b) == regroup and a != b)
    tot = (w1 - w2) * d + a - b
    if regroup:
        steps = [f"{fr(a, d)} is less than {fr(b, d)}, so regroup 1 whole: {w1} {fr(a, d)} = {w1 - 1} {fr(a + d, d)}.", f"{w1 - 1} − {w2} = {w1 - 1 - w2} and {fr(a + d, d)} − {fr(b, d)} = {fr(a + d - b, d)}. The difference is {mx(tot, d)}."]
    else:
        steps = [f"Subtract the wholes: {w1} − {w2} = {w1 - w2}. Subtract the fractions: {fr(a, d)} − {fr(b, d)} = {fr(a - b, d)}.", f"The difference is {mx(tot, d)}."]
    return Item(f"Subtract: {w1} {fr(a, d)} − {w2} {fr(b, d)}", mx(tot, d), steps,
                [W(f"{w1 - w2} {fr(abs(a - b), d)}" if regroup else mx(tot + d, d), "subtracted the smaller fraction from the larger one without regrouping" if regroup else "did not subtract the wholes correctly"),
                 W(mx((w1 + w2) * d + a + b, d), "added instead of subtracting"), W(mx(tot + 1, d), "made a subtraction mistake"), W(mx(tot + d, d), "forgot that 1 whole was regrouped")],
                EX(f"{w1} + {a}/{d} − {w2} − {b}/{d}"), claim=f"{w1} {fr(a, d)} − {w2} {fr(b, d)}")


@fam("012")
def mxa_whole_minus(r, L):
    d = den(r, L)
    w1 = r.randint(2, 5 if L == 0 else 10)
    w2 = r.randint(0, w1 - 2)
    b = r.randint(1, d - 1)
    tot = w1 * d - w2 * d - b
    sub_txt = f"{w2} {fr(b, d)}" if w2 else fr(b, d)
    return Item(f"Subtract: {w1} − {sub_txt}", mx(tot, d), [f"Rename {w1} as {w1 - 1} {fr(d, d)}.", f"{w1 - 1} {fr(d, d)} − {sub_txt} = {mx(tot, d)}."],
                [W(f"{w1 - w2} {fr(b, d)}", "kept the fraction instead of subtracting it"), W(mx(tot + d, d), "forgot that 1 whole was regrouped"), W(mx(tot + 1, d), "made a subtraction mistake"), W(mx(tot + 2 * b, d), "added the fraction instead of subtracting")],
                EX(f"{w1} − {w2} − {b}/{d}"), qtype="conceptual", claim=f"{w1} − {sub_txt}")


@fam("012")
def mxa_word(r, L):
    w1, a, w2, b, d = mixed_pair(r, L, regroup=(L == 2))
    n1 = name(r)
    tot = (w1 + w2) * d + a + b
    s = pick(r, [(f"{n1} ran {w1} {fr(a, d)} miles on Saturday and {w2} {fr(b, d)} miles on Sunday. How many miles did {n1} run in all?", "miles"),
                 (f"A recipe uses {w1} {fr(a, d)} cups of flour and {w2} {fr(b, d)} cups of oats. How many cups is that altogether?", "cups"),
                 (f"One board is {w1} {fr(a, d)} feet long. Another board is {w2} {fr(b, d)} feet long. What is the total length of the two boards?", "feet")])
    return Item(s[0], f"{mx(tot, d)} {s[1]}", [f"Add the wholes and add the fractions: {w1 + w2} and {fr(a + b, d)}.", f"The total is {mx(tot, d)} {s[1]}."],
                [W(f"{w1 + w2} {fr(a + b, 2 * d)} {s[1]}", "added the denominators"), W(f"{mx(tot + d, d)} {s[1]}", "added an extra whole"), W(f"{mx(abs((w1 - w2) * d + a - b), d)} {s[1]}", "subtracted instead of adding"), W(f"{mx(tot + 1, d)} {s[1]}", "made an addition mistake")],
                EX(f"{w1} + {a}/{d} + {w2} + {b}/{d}", unit=s[1]), qtype="word-problem")


@fam("012")
def mxa_word_sub(r, L):
    d = den(r, L)
    w1, w2 = r.randint(4, 9), r.randint(1, 3)
    a, b = r.randint(1, d - 1), r.randint(1, d - 1)
    need(a != b and (a > b or L > 0))
    tot = (w1 - w2) * d + a - b
    n1 = name(r)
    s = pick(r, [(f"{n1} had {w1} {fr(a, d)} yards of yarn and used {w2} {fr(b, d)} yards. How many yards of yarn are left?", "yards"),
                 (f"A jug holds {w1} {fr(a, d)} quarts of lemonade. The class drinks {w2} {fr(b, d)} quarts. How many quarts are left?", "quarts"),
                 (f"A hiking trail is {w1} {fr(a, d)} miles long. {n1} has hiked {w2} {fr(b, d)} miles. How many miles are left?", "miles")])
    return Item(s[0], f"{mx(tot, d)} {s[1]}", ["Subtract the mixed numbers. Regroup 1 whole if the first fraction is smaller.", f"{w1} {fr(a, d)} − {w2} {fr(b, d)} = {mx(tot, d)} {s[1]}."],
                [W(f"{mx((w1 + w2) * d + a + b, d)} {s[1]}", "added instead of subtracting"), W(f"{mx(tot + d, d)} {s[1]}", "forgot that 1 whole was regrouped"), W(f"{w1 - w2} {fr(abs(a - b), d)} {s[1]}" if a < b else f"{mx(tot + 1, d)} {s[1]}", "subtracted without regrouping" if a < b else "made a subtraction mistake")],
                EX(f"{w1} + {a}/{d} − {w2} − {b}/{d}", unit=s[1]), qtype="word-problem")


@fam("012", mode="mc")
def mxa_rename(r, L):
    d = den(r, L)
    w = r.randint(2, 9)
    a = r.randint(1, d - 2)
    good = f"{w - 1} {fr(a + d, d)}"
    return Item(f"To subtract from {w} {fr(a, d)}, you sometimes need to regroup 1 whole. Which is another name for {w} {fr(a, d)}?", good, [f"Take 1 whole from {w} and write it as {fr(d, d)}.", f"{fr(d, d)} + {fr(a, d)} = {fr(a + d, d)}, so {w} {fr(a, d)} = {good}."],
                [W(f"{w - 1} {fr(a + 1, d)}", "added 1 to the numerator instead of a whole"), W(f"{w - 1} {fr(a + 10, d)}", "added 10 as if regrouping whole numbers"), W(f"{w} {fr(a + d, d)}", "did not take 1 from the whole number")],
                FN("mixed_equal", f=f"{w} {fr(a, d)}"), qtype="conceptual", tags={"reasoning", "multiple-representations"})


# ============================================================== S4 Multiplying a Fraction by a Whole Number
def mult_case(r, L):
    d = den(r, L)
    a = r.randint(1 if L == 0 else 2, d - 1)
    n = r.randint(2, 5 if L == 0 else 9)
    return n, a, d


def mw_wr(n, a, d, unit=""):
    u = (" " + unit) if unit else ""
    return [W(fr(n * a, n * d) + u, "multiplied the denominator too"), W(mx(n + a, d) + u, "added the whole number to the numerator"), W(fr(a, n * d) + u, "multiplied only the denominator"), W(mx(n * a + 1, d) + u, "made a multiplication mistake")]


@fam("012")
def mw_unit_count(r, L):
    d = den(r, L)
    a = r.randint(2, d - 1 if L < 2 else 2 * d - 1)
    return Item(f"Fill in the blank: {fr(a, d)} = ___ × {fr(1, d)}", str(a), [f"{fr(a, d)} is {a} copies of {fr(1, d)}.", f"{fr(a, d)} = {a} × {fr(1, d)}."],
                [W(str(d), "used the denominator"), W(str(a * d), "multiplied the numerator and denominator"), W(str(a + d), "added the numerator and denominator"), W(str(a - 1), "miscounted the unit fractions")],
                FN("unit_multiple", f=fr(a, d)), qtype="conceptual")


@fam("012")
def mw_basic(r, L):
    n, a, d = mult_case(r, L)
    return Item(f"Multiply: {n} × {fr(a, d)}", mx(n * a, d), [f"{n} × {fr(a, d)} is {n} × {a} copies of {fr(1, d)}.", f"{n} × {a} = {n * a}, so the product is {fr(n * a, d)}" + (f" = {mx(n * a, d)}." if n * a >= d else ".")],
                mw_wr(n, a, d), EX(f"{n} × {a}/{d}"), claim=f"{n} × {fr(a, d)}")


@fam("012")
def mw_as_unit(r, L):
    n, a, d = mult_case(r, max(L, 1))
    return Item(f"Fill in the blank: {n} × {fr(a, d)} = ___ × {fr(1, d)}", str(n * a), [f"{fr(a, d)} = {a} × {fr(1, d)}.", f"So {n} × {fr(a, d)} = ({n} × {a}) × {fr(1, d)} = {n * a} × {fr(1, d)}."],
                [W(str(n), "kept the whole number"), W(str(n + a), "added instead of multiplying"), W(str(n * d), "multiplied by the denominator"), W(str(a), "used only the numerator")],
                EX(f"{n} × {a}"), qtype="conceptual", tags={"reasoning"})


@fam("012", mode="mc")
def mw_repeated(r, L):
    n, a, d = mult_case(r, L)
    need(n <= 5 and n != a)
    good = " + ".join([fr(a, d)] * n)
    return Item(f"Which addition has the same value as {n} × {fr(a, d)}?", good, [f"{n} × {fr(a, d)} means {n} groups of {fr(a, d)}.", f"{good} = {fr(n * a, d)}."],
                [W(" + ".join([fr(a, d)] * (n - 1)) if n > 2 else " + ".join([fr(a, d)] * (n + 1)), "used the wrong number of groups"), W(f"{n} + {fr(a, d)}", "added the whole number instead of multiplying"),
                 W(" + ".join([fr(a, n * d)] * n), "multiplied the denominator")], FN("expr_eq", e=f"{n} × {a}/{d}"), qtype="conceptual", tags={"connections"})


@fam("012")
def mw_word(r, L):
    n, a, d = mult_case(r, L)
    n1 = name(r)
    s = pick(r, [(f"Each serving of trail mix uses {fr(a, d)} cup of raisins. How many cups of raisins are needed for {n} servings?", "cups"),
                 (f"{n1} walks {fr(a, d)} mile to school each day. How many miles does {n1} walk to school in {n} days?", "miles"),
                 (f"Each bow uses {fr(a, d)} yard of ribbon. How many yards of ribbon are needed for {n} bows?", "yards"),
                 (f"A puppy eats {fr(a, d)} pound of food each day. How many pounds of food does it eat in {n} days?", "pounds")])
    v = n * a
    u = s[1] if v > d else s[1][:-1]
    return Item(s[0], f"{mx(v, d)} {u}", [f"Multiply: {n} × {fr(a, d)} = {fr(v, d)}.", f"{fr(v, d)} = {mx(v, d)} {u}." if v >= d else f"The answer is {fr(v, d)} {u}."],
                mw_wr(n, a, d, u), EX(f"{n} × {a}/{d}", unit=u), qtype="word-problem")


@fam("012", mode="mc")
def mw_between(r, L):
    n, a, d = mult_case(r, max(L, 1))
    v = n * a
    need(v % d and v > d)
    lo = v // d
    f = lambda x: f"between {x} and {x + 1}"
    return Item(f"{name(r)} needs {n} pieces of rope that are each {fr(a, d)} meter long. The total length is between which two whole numbers of meters?", f(lo),
                [f"{n} × {fr(a, d)} = {fr(v, d)} = {mx(v, d)}.", f"{mx(v, d)} is {f(lo)}."],
                [W(f(lo + 1), "rounded up too far"), W(f(lo - 1) if lo > 1 else f(lo + 2), "miscounted the wholes"), W(f(v), "used the numerator as the number of meters")],
                FN("value_between", e=f"{n} × {a}/{d}"), qtype="real-world", tags={"reasoning"})


@fam("012")
def mw_number_line(r, L):
    d = pick(r, [3, 4, 5, 6])
    a = r.randint(1, 2 if d < 5 else 3)
    n = r.randint(2, 4)
    need(n * a < 3 * d)
    hi = (n * a) // d + 1
    jumps = [[fr(i * a, d), fr((i + 1) * a, d)] for i in range(n)]
    alt = f"A number line from 0 to {hi} with tick marks every {fr(1, d)}. There are {n} equal jumps starting at 0. Each jump is {fr(a, d)} long."
    return Item(f"The number line shows {n} jumps of {fr(a, d)}, starting at 0. At what number does the last jump end?", mx(n * a, d),
                [f"{n} jumps of {fr(a, d)} is {n} × {fr(a, d)}.", f"{n} × {fr(a, d)} = {fr(n * a, d)}" + (f" = {mx(n * a, d)}." if n * a >= d else ".")], mw_wr(n, a, d),
                FN("jumps_end", jumps=jumps), qtype="visual", diagram=Diagram("number_line", {"lo": "0", "hi": str(hi), "den": d, "labels": "whole", "jumps": jumps}, alt), tags={"modeling"})


# ============================================================== S5 Tenths and Hundredths as Fractions and Decimals
def dtxt(n, places):
    return f"{n // 10 ** places}.{n % 10 ** places:0{places}d}"


@fam("012")
def th_frac_to_dec(r, L):
    if r.random() < 0.4:
        n = r.randint(1, 9) if L < 2 else r.randint(11, 39)
        need(n % 10)
        return Item(f"Write {fr(n, 10)} as a decimal.", dtxt(n, 1), [f"{n} tenths: the last digit goes in the tenths place.", f"{fr(n, 10)} = {dtxt(n, 1)}."],
                    [W(dtxt(n, 2), "wrote hundredths instead of tenths"), W(f"{n}.0", "wrote the numerator as a whole number"), W(f"0.{n}0" if n < 10 else dtxt(n * 10 + 1, 2), "placed the digits incorrectly")] if n >= 10 else
                    [W(dtxt(n, 2), "wrote hundredths instead of tenths"), W(f"{n}.0", "wrote the numerator as a whole number"), W(f"{n}.10", "copied the numerator and denominator around the decimal point")],
                    EX(f"{n}/10", form="dec"), claim=f"{fr(n, 10)} as a decimal")
    n = r.randint(1, 99) if L < 2 else r.randint(101, 399)
    need(n % 10)
    return Item(f"Write {fr(n, 100)} as a decimal.", dtxt(n, 2), [f"{n} hundredths: the last digit goes in the hundredths place.", f"{fr(n, 100)} = {dtxt(n, 2)}."],
                [W(dtxt(n, 1) if n >= 10 else f"0.{n}", "wrote tenths instead of hundredths"), W(f"{n}.0", "wrote the numerator as a whole number"), W(f"{n}.100", "copied the numerator and denominator around the decimal point"), W(dtxt(n, 3) if n >= 10 else f"0.00{n}", "used too many decimal places")],
                EX(f"{n}/100", form="dec"), claim=f"{fr(n, 100)} as a decimal")


@fam("012")
def th_dec_to_frac(r, L):
    if r.random() < 0.4:
        n = r.randint(1, 9)
        return Item(f"Write 0.{n} as a fraction with a denominator of 10.", fr(n, 10), [f"The digit {n} is in the tenths place.", f"0.{n} = {fr(n, 10)}."],
                    [W(fr(n, 100), "used hundredths instead of tenths"), W(fr(10, n), "switched the numerator and denominator"), W(fr(1, n) if n > 1 else fr(1, 100), "wrote a unit fraction"), W(fr(n * 10, 10), "multiplied the numerator by 10")],
                    FN("frac_with_den", f=fr(n, 10), den=10), claim=f"0.{n} as a fraction")
    n = r.randint(11, 99) if L else r.randint(1, 60)
    need(n % 10)
    return Item(f"Write {dtxt(n, 2)} as a fraction with a denominator of 100.", fr(n, 100), [f"The last digit is in the hundredths place, so the decimal is {n} hundredths.", f"{dtxt(n, 2)} = {fr(n, 100)}."],
                [W(fr(n, 10), "used tenths instead of hundredths"), W(fr(100, n), "switched the numerator and denominator"), W(fr(n // 10, 100) if n >= 10 else fr(n * 10, 100), "used only one of the digits"), W(fr(n, 1000), "used too many places")],
                FN("frac_with_den", f=fr(n, 100), den=100), claim=f"{dtxt(n, 2)} as a fraction")


@fam("012")
def th_grid(r, L):
    n = r.randint(3, 97)
    alt = f"A 10 by 10 grid of 100 small squares. {n} of the squares are shaded."
    ask = r.random() < 0.5
    dg = Diagram("hundred_grid", {"shaded": n}, alt)
    if ask:
        return Item("The large square is one whole. It is divided into 100 equal parts. What decimal names the shaded part?", dtxt(n, 2),
                    [f"{n} of the 100 squares are shaded.", f"{n} hundredths = {dtxt(n, 2)}."],
                    [W(dtxt(100 - n, 2), "named the unshaded part"), W(f"{n}.0", "wrote the count as a whole number"), W(dtxt(n, 1) if n % 10 else dtxt(n // 10, 2), "used the wrong place value")],
                    FN("grid_decimal", shaded=n), qtype="visual", diagram=dg, tags={"modeling"})
    return Item("The large square is one whole. It is divided into 100 equal parts. What fraction of the whole is shaded? Use a denominator of 100.", fr(n, 100),
                [f"{n} of the 100 squares are shaded.", f"The fraction is {fr(n, 100)}."],
                [W(fr(100 - n, 100), "named the unshaded part"), W(fr(n, 10), "used tenths instead of hundredths"), W(fr(100, n), "switched the numerator and denominator")],
                FN("frac_with_den", f=fr(n, 100), den=100), qtype="visual", diagram=dg, tags={"modeling"})


@fam("012")
def th_add(r, L):
    a = r.randint(1, 8)
    b = r.randint(1, 9) if L == 0 else r.randint(1, 99 - 10 * a)
    need(b % 10)
    s = 10 * a + b
    need(s < 100 or L == 2)
    return Item(f"Add: {fr(a, 10)} + {fr(b, 100)}. Write the sum with a denominator of 100.", fr(s, 100), [f"Rename tenths as hundredths: {fr(a, 10)} = {fr(10 * a, 100)}.", f"{fr(10 * a, 100)} + {fr(b, 100)} = {fr(s, 100)}."],
                [W(fr(a + b, 110), "added the numerators and the denominators"), W(fr(a + b, 100), "did not rename the tenths as hundredths"), W(fr(a + b, 10), "used tenths for both fractions"), W(fr(s + 10, 100), "made an addition mistake")],
                FN("frac_with_den", f=f"{s}/100", den=100), claim=f"{fr(a, 10)} + {fr(b, 100)}")


@fam("012", mode="mc")
def th_equal(r, L):
    n = r.randint(1, 9)
    good, bad = f"0.{n}0", [f"0.0{n}", f"{n}.0", f"0.{n}{n}"]
    return Item(f"Which decimal is equal to 0.{n}?", good, [f"0.{n} = {fr(n, 10)} = {fr(n * 10, 100)}.", f"{fr(n * 10, 100)} = {good}. Writing a zero at the end does not change the value."],
                [W(bad[0], f"this is {n} hundredths, not {n} tenths"), W(bad[1], f"this is {n} ones"), W(bad[2], "this has extra hundredths")], FN("dec_equal", x=f"0.{n}"), qtype="conceptual", tags={"misconception"})


@fam("012")
def th_words(r, L):
    if r.random() < 0.45:
        n = r.randint(1, 9)
        w, good = f"{words(n)} tenth{'s' if n > 1 else ''}", f"0.{n}"
        bad = [f"0.0{n}", f"{n}.0", f"{n}.10"]
    else:
        n = r.randint(11, 99) if L else r.randint(1, 30)
        need(n % 10)
        w, good = f"{words(n)} hundredth{'s' if n > 1 else ''}", dtxt(n, 2)
        bad = [dtxt(n, 1) if n >= 10 else f"0.{n}", f"{n}.0", f"{n}.100", f"0.00{n}" if n < 10 else dtxt(n, 3)]
    if L == 2:
        k = r.randint(1, 9)
        w, good = f"{words(k)} and {w}", f"{k}{good[1:]}"
        bad = [f"{k}{b[1:]}" if b.startswith("0.") else f"{k}{b}" for b in bad]
    return Item(f"Write this number as a decimal: {w}", good, ["The last word tells the place of the last digit.", f"{w} = {good}."],
                [W(b, "used the wrong place value") for b in bad[:3]], FN("dec_from_words", words=w), claim=f"{w} as a decimal")


@fam("012")
def th_number_line(r, L):
    n = r.randint(1, 9) if L < 2 else r.randint(11, 19)
    lo, hi = (0, 1) if n < 10 else (1, 2)
    alt = f"A number line from {lo} to {hi} with tick marks every tenth. Point A is {n - 10 * lo} tick marks to the right of {lo}."
    return Item(f"The number line is divided into tenths. What decimal does point A show?", dtxt(n, 1), [f"Point A is {n - 10 * lo} tenths past {lo}.", f"Point A shows {dtxt(n, 1)}."],
                [W(dtxt(n, 2), "wrote hundredths instead of tenths"), W(dtxt(n + 1, 1), "counted one tick mark too many"), W(dtxt(n - 1, 1), "counted one tick mark too few"), W(f"{n - 10 * lo}.0", "wrote the count as a whole number")],
                FN("nl_value", x=fr(n, 10)), qtype="visual", diagram=Diagram("number_line", {"lo": str(lo), "hi": str(hi), "den": 10, "labels": "whole", "points": [{"x": fr(n, 10), "label": "A"}]}, alt))


@fam("012")
def th_money(r, L):
    dimes, pennies = r.randint(1, 9), r.randint(1, 9)
    c = 10 * dimes + pennies
    if L == 0:
        return Item(f"A penny is {fr(1, 100)} of a dollar. What decimal shows {c} pennies as part of a dollar?", dtxt(c, 2), [f"{c} pennies = {fr(c, 100)} of a dollar.", f"{fr(c, 100)} = {dtxt(c, 2)}."],
                    [W(f"{c}.0", "wrote the count as a whole number"), W(dtxt(c, 1), "used tenths instead of hundredths"), W(dtxt(c, 3), "used too many decimal places")], EX(f"{c}/100", form="dec"), qtype="real-world")
    return Item(f"A dime is {fr(1, 10)} of a dollar and a penny is {fr(1, 100)} of a dollar. {name(r)} has {dimes} dimes and {pennies} pennies. What decimal shows this amount as part of a dollar?", dtxt(c, 2),
                [f"{dimes} dimes = {fr(dimes, 10)} = {fr(10 * dimes, 100)} and {pennies} pennies = {fr(pennies, 100)}.", f"{fr(10 * dimes, 100)} + {fr(pennies, 100)} = {fr(c, 100)} = {dtxt(c, 2)}."],
                [W(dtxt(dimes + pennies, 2), "added the dimes and pennies as if they were the same size"), W(dtxt(10 * pennies + dimes, 2), "switched the tenths and hundredths"), W(f"{dimes}.{pennies}", "wrote dimes as whole dollars"), W(dtxt(dimes + pennies, 1), "added the counts")],
                EX(f"{dimes}/10 + {pennies}/100", form="dec"), qtype="real-world", tags={"modeling"})


# ============================================================== S6 Comparing Decimals
def dec_pair(r, L):
    kind = r.randrange(4 if L else 3)
    if kind == 0:      # tenths vs hundredths, the classic misconception
        t = r.randint(1, 9)
        h = r.randint(1, 99)
        need(h % 10 and h != 10 * t)
        a, b = f"0.{t}", dtxt(h, 2)
    elif kind == 1:
        x, y = r.sample(range(1, 100), 2)
        a, b = dtxt(x, 2), dtxt(y, 2)
    elif kind == 2:
        x, y = r.sample(range(1, 10), 2)
        a, b = f"0.{x}", f"0.{y}"
    else:
        w = r.randint(1, 9)
        x, y = r.randint(1, 99), r.randint(1, 9)
        a, b = f"{w}.{x:02d}", f"{w}.{y}"
    if r.random() < 0.5:
        a, b = b, a
    return a, b


def sym(a, b):
    return "<" if F(a) < F(b) else ">" if F(a) > F(b) else "="


def hund(x):
    return int(F(x) * 100)


@fam("012", mode="sa")
def dcm_compare(r, L):
    a, b = dec_pair(r, L)
    s = sym(a, b)
    return Item(f"Compare. Write <, > or = to make the statement true: {a} ___ {b}", s, [f"Write both as hundredths: {a} = {fr(hund(a), 100)} and {b} = {fr(hund(b), 100)}.", f"{hund(a)} {s} {hund(b)}, so {a} {s} {b}."],
                [W(x, "compared the digits without using place value") for x in "<>=" if x != s], FN("compare", a=a, b=b), claim=f"Compare {a} and {b}")


@fam("012", mode="mc")
def dcm_order(r, L):
    vals = set()
    for k in range(20):
        a, b = dec_pair(sub(r, k), L)
        vals.update([a, b])
    vals = list({F(v): v for v in vals}.values())
    need(len(vals) >= 4)
    fs = r.sample(vals, 3 if L == 0 else 4)
    desc = r.random() < 0.4
    want = sorted(fs, key=F, reverse=desc)
    j = lambda x: ", ".join(x)
    w2, w3 = want[:], want[:]
    w2[0], w2[1] = w2[1], w2[0]
    w3[-1], w3[-2] = w3[-2], w3[-1]
    need(len({j(want), j(want[::-1]), j(w2), j(w3)}) == 4)
    return Item(f"Order the decimals from {'greatest to least' if desc else 'least to greatest'}: {j(fs)}", j(want), ["Write each decimal in hundredths: " + ", ".join(f"{v} = {fr(hund(v), 100)}" for v in fs) + ".", f"In order: {j(want)}."],
                [W(j(want[::-1]), "ordered in the opposite direction"), W(j(w2), "switched two decimals"), W(j(w3), "switched two decimals")], FN("order", values=fs, desc=desc), qtype="ordering")


@fam("012", mode="mc")
def dcm_true(r, L):
    opts = []
    for k in range(12):
        a, b = dec_pair(sub(r, k), L)
        if F(a) != F(b) and (a, b) not in opts:
            opts.append((a, b))
        if len(opts) == 4:
            break
    need(len(opts) == 4)
    gi = r.randrange(4)
    out = [f"{a} {sym(a, b) if k == gi else ('<' if sym(a, b) == '>' else '>')} {b}" for k, (a, b) in enumerate(opts)]
    need(len(set(out)) == 4)
    a, b = opts[gi]
    return Item("Which comparison is true?", out[gi], [f"Compare as hundredths: {a} = {fr(hund(a), 100)} and {b} = {fr(hund(b), 100)}.", f"{out[gi]} is true."],
                [W(t, "the comparison symbol points the wrong way") for k, t in enumerate(out) if k != gi], FN("true_cmp"), qtype="conceptual", tags={"reasoning"})


@fam("012", mode="mc")
def dcm_between(r, L):
    t = r.randint(1, 8)
    lo, hi = f"0.{t}", f"0.{t + 1}"
    good = f"0.{t}{r.randint(1, 9)}"
    bad = [f"0.0{t + 1}", f"0.{t + 1}{r.randint(1, 9)}", f"0.{t - 1}{r.randint(1, 9)}" if t > 1 else f"0.0{r.randint(1, 9)}"]
    need(len(set(bad)) == 3)
    return Item(f"Which decimal is between {lo} and {hi}?", good, [f"In hundredths, {lo} = 0.{t}0 and {hi} = 0.{t + 1}0.", f"{good} is between them."],
                [W(bad[0], f"it is less than {lo}"), W(bad[1], f"it is greater than {hi}"), W(bad[2], f"it is less than {lo}")], FN("between_frac_dec", lo=lo, hi=hi), qtype="conceptual", tags={"reasoning"})


@fam("012", mode="mc")
def dcm_table(r, L):
    vals = set()
    for k in range(20):
        a, b = dec_pair(sub(r, k), max(L, 1))
        vals.update([a, b])
    vals = list({F(v): v for v in vals}.values())
    need(len(vals) >= 4)
    fs = r.sample(vals, 4)
    names = r.sample(NAMES, 4)
    which = pick(r, ["greatest", "least"])
    t = pick(r, [("Long Jump (meters)", "jumped the {w} distance"), ("Rainfall (inches)", "measured the {w} amount of rain"), ("Plant Height (meters)", "has the plant with the {w} height")])
    g = (max if which == "greatest" else min)(range(4), key=lambda i: F(fs[i]))
    rows = [[nm, v] for nm, v in zip(names, fs)]
    alt = f"A table with columns Name and {t[0]}. " + "; ".join(f"{a}: {b}" for a, b in rows) + "."
    return Item(f"The table shows measurements for four students. Who {t[1].format(w=which)}?", names[g], ["Compare the decimals as hundredths.", f"{fs[g]} is the {which}, so the answer is {names[g]}."],
                [W(nm, "compared the digits without using place value") for i, nm in enumerate(names) if i != g], FN("arg_extreme", items=dict(zip(names, fs)), which=which), qtype="real-world",
                diagram=Diagram("table", {"header": ["Name", t[0]], "rows": rows}, alt), tags={"modeling"})


@fam("012", mode="mc")
def dcm_reason(r, L):
    t = r.randint(2, 9)
    h = r.randint(11, 10 * t - 1)
    need(h % 10)
    a, b = f"0.{t}", dtxt(h, 2)
    good = f"{a} = {a}0, and {10 * t} hundredths is greater than {h} hundredths."
    return Item(f"Why is {a} greater than {b}?", good, [f"Write {a} as hundredths: {a} = {a}0.", f"{10 * t} hundredths is greater than {h} hundredths."],
                [W(f"{a} = 0.0{t}, and {t} hundredths is less than {h} hundredths.", f"{a} is not equal to 0.0{t}"), W(f"{b} has more digits, so {b} is greater.", "more digits does not mean a greater decimal"),
                 W(f"{h} is greater than {t}, so {b} is greater.", "compared the digits as whole numbers")], FN("dec_reason", a=a, b=b), qtype="explain", tags={"reasoning", "misconception"})


@fam("12", mode="sa")
def dcm_frac_vs_dec(r, L):
    n = r.randint(1, 9)
    h = r.randint(1, 99)
    need(h % 10)
    a, b = (fr(n, 10), dtxt(h, 2)) if r.random() < 0.5 else (dtxt(h, 2), fr(n, 10))
    va, vb = (F(n, 10), F(h, 100)) if "/" in a else (F(h, 100), F(n, 10))
    s = "<" if va < vb else ">" if va > vb else "="
    return Item(f"Compare. Write <, > or = to make the statement true: {a} ___ {b}", s, [f"{fr(n, 10)} = {fr(10 * n, 100)} = 0.{n}0.", f"Compare hundredths: {int(va * 100)} {s} {int(vb * 100)}, so {a} {s} {b}."],
                [W(x, "did not write both numbers in the same form") for x in "<>=" if x != s], FN("compare", a=a, b=b), qtype="conceptual", tags={"multiple-representations"})


@fam("012", mode="mc")
def dcm_extreme(r, L):
    vals = set()
    for k in range(20):
        a, b = dec_pair(sub(r, k), L)
        vals.update([a, b])
    vals = list({F(v): v for v in vals}.values())
    need(len(vals) >= 4)
    fs = r.sample(vals, 4)
    which = pick(r, ["greatest", "least"])
    g = (max if which == "greatest" else min)(fs, key=F)
    return Item(f"Which decimal is the {which}? {', '.join(fs)}", g, ["Write each decimal in hundredths, then compare.", f"{g} is the {which}."],
                [W(v, "compared the digits without using place value") for v in fs if v != g], FN("extreme_frac_dec", values=fs, which=which), qtype="conceptual")


SKILLS = {
    1: dict(name="Decomposing Fractions", fams=[dc_unit_sum, dc_missing, dc_which, dc_to_mixed, dc_wholes, dc_count_ways]),
    2: dict(name="Adding and Subtracting Fractions with Like Denominators", fams=[al_add, al_sub, al_missing, al_from_one, al_word_add, al_word_sub, al_model, al_three]),
    3: dict(name="Adding and Subtracting Mixed Numbers", fams=[mxa_add, mxa_sub, mxa_whole_minus, mxa_word, mxa_word_sub, mxa_rename]),
    4: dict(name="Multiplying a Fraction by a Whole Number", fams=[mw_unit_count, mw_basic, mw_as_unit, mw_repeated, mw_word, mw_between, mw_number_line]),
    5: dict(name="Tenths and Hundredths as Fractions and Decimals", fams=[th_frac_to_dec, th_dec_to_frac, th_grid, th_add, th_equal, th_words, th_number_line, th_money]),
    6: dict(name="Comparing Decimals", fams=[dcm_compare, dcm_order, dcm_true, dcm_between, dcm_table, dcm_reason, dcm_frac_vs_dec, dcm_extreme]),
}
