"""Unit 6: Fractions and Equivalent Fractions (4.NF.A.1, 4.NF.A.2)."""
from g4lib import *
from math import gcd

UNIT_ID = "fractions-equivalent-fractions"
DENS = {0: [2, 3, 4, 6, 8], 1: [2, 3, 4, 5, 6, 8, 10, 12], 2: [3, 4, 5, 6, 8, 10, 12]}
ALLOWED = [2, 3, 4, 5, 6, 8, 10, 12, 100]
DEN_WORD = {2: "halves", 3: "thirds", 4: "fourths", 5: "fifths", 6: "sixths", 8: "eighths", 10: "tenths", 12: "twelfths", 100: "hundredths"}


def fr(n, d):
    return f"{n}/{d}"


def proper(r, L, simplest=False):
    for _ in range(40):
        d = pick(r, DENS[L])
        n = r.randint(1, d - 1)
        if not simplest or gcd(n, d) == 1:
            return n, d
    raise Reject()


def equiv_pair(r, L):
    """(n, d, k) with d*k an allowed denominator."""
    for _ in range(60):
        n, d = proper(r, L, simplest=True)
        ks = [k for k in (2, 3, 4, 5, 6, 10) if d * k in ALLOWED + [16, 20, 24]]
        if ks:
            return n, d, pick(r, ks)
    raise Reject()


def val(n, d):
    return F(n, d)


# ============================================================== S1 Understanding Equivalent Fractions
@fam("012")
def ue_bars(r, L):
    n, d, k = equiv_pair(r, L)
    need(d * k <= 12)
    alt = f"Two fraction bars of the same length. The top bar has {d} equal parts with {n} shaded. The bottom bar has {d * k} equal parts with {n * k} shaded."
    return Item(f"The top bar shows {fr(n, d)}. The bottom bar is the same whole cut into {d * k} equal parts, with the same amount shaded. What fraction does the bottom bar show?", fr(n * k, d * k),
                [f"Each part of the top bar was split into {k} smaller parts.", f"{n} × {k} = {n * k} shaded parts out of {d} × {k} = {d * k}: {fr(n * k, d * k)}."],
                [W(fr(n, d * k), "changed the denominator but not the numerator"), W(fr(n + k, d + k), "added instead of multiplying"), W(fr(n * k, d), "changed the numerator but not the denominator"), W(fr(d * k - n * k, d * k), "counted the unshaded parts")],
                FN("bars_fraction", n=n, d=d, parts=d * k), qtype="visual",
                diagram=Diagram("fraction_bars", {"bars": [{"parts": d, "shaded": n}, {"parts": d * k, "shaded": n * k}]}, alt), tags={"modeling"})


@fam("012", mode="mc")
def ue_model_choice(r, L):
    n, d, k = equiv_pair(r, L)
    N, D = n * k, d * k
    need(D <= 12)
    circle = r.random() < 0.5 and D <= 12
    alt = (f"A circle cut into {D} equal parts with {N} parts shaded." if circle else f"A fraction bar cut into {D} equal parts with {N} parts shaded.")
    dg = Diagram("fraction_circle", {"parts": D, "shaded": N}, alt) if circle else Diagram("fraction_bars", {"bars": [{"parts": D, "shaded": N}]}, alt)
    bad = [fr(n + 1, d) if n + 1 < d else fr(n, d + 1), fr(D - N, D) if D - N != N else fr(N - 1, D), fr(n, D)]
    need(all(F(b) != F(n, d) for b in bad) and len(set(bad)) == 3)
    return Item(f"The model shows {fr(N, D)} shaded. Which fraction is equivalent to the shaded part?", fr(n, d), [f"Group the parts: {N} ÷ {k} = {n} and {D} ÷ {k} = {d}.", f"{fr(N, D)} = {fr(n, d)}."],
                [W(bad[0], "this fraction names a different amount"), W(bad[1], "this is the unshaded part or a different amount"), W(bad[2], "changed only one part of the fraction")],
                FN("equiv_frac", f=fr(N, D)), qtype="visual", diagram=dg, tags={"modeling"})


@fam("012", mode="mc")
def ue_number_line(r, L):
    n, d, k = equiv_pair(r, L)
    N, D = n * k, d * k
    need(D <= 12)
    alt = f"A number line from 0 to 1 with tick marks every {fr(1, D)}. Point A is at {fr(N, D)}."
    bad = [fr(n, d + 1), fr(n + 1, d) if n + 1 < d else fr(1, d + 2), fr(N, d) if N < d else fr(n, D)]
    need(all(F(b) != F(n, d) for b in bad) and len(set(bad)) == 3)
    return Item(f"Point A is at {fr(N, D)} on the number line. Which fraction names the same point?", fr(n, d), [f"Equivalent fractions name the same point on a number line.", f"{fr(N, D)} = {fr(n, d)} because {N} ÷ {k} = {n} and {D} ÷ {k} = {d}."],
                [W(b, "this fraction is at a different point") for b in bad], FN("equiv_frac", f=fr(N, D)), qtype="visual",
                diagram=Diagram("number_line", {"lo": "0", "hi": "1", "den": D, "labels": "whole", "points": [{"x": fr(N, D), "label": "A"}]}, alt), tags={"multiple-representations"})


@fam("012", mode="mc")
def ue_why(r, L):
    n, d, k = equiv_pair(r, L)
    N, D = n * k, d * k
    k2 = k + 1 if k < 6 else k - 1
    good = f"Both the numerator and the denominator were multiplied by {k}."
    return Item(f"Why is {fr(n, d)} equivalent to {fr(N, D)}?", good, [f"{n} × {k} = {N} and {d} × {k} = {D}.", "Multiplying the numerator and the denominator by the same number makes more, smaller parts but keeps the same amount."],
                [W(f"Both the numerator and the denominator were multiplied by {k2}.", "used the wrong multiplier"), W(f"The number {N - n} was added to both the numerator and the denominator.", "adding the same number does not make an equivalent fraction"),
                 W(f"Only the denominator was multiplied by {k}.", "both parts must be multiplied")], FN("equiv_reason", a=fr(n, d), b=fr(N, D)), qtype="explain", tags={"reasoning"})


@fam("012")
def ue_split_parts(r, L):
    n, d, k = equiv_pair(r, L)
    return Item(f"A rectangle is cut into {d} equal parts, and {n} of the parts {'is' if n == 1 else 'are'} shaded. Then each part is cut into {k} smaller equal parts. How many of the small parts are shaded?", str(n * k),
                [f"Each shaded part becomes {k} small parts.", f"{n} × {k} = {n * k} small shaded parts (out of {d * k})."],
                [W(str(n + k), "added instead of multiplying"), W(str(d * k), "gave the total number of small parts"), W(str(n), "did not split the shaded parts"), W(str(d * k - n * k), "counted the unshaded parts")],
                EX(f"{n} × {k}"), qtype="conceptual", tags={"reasoning"})


@fam("012", mode="mc")
def ue_not_equivalent(r, L):
    n, d = pick(r, [(1, 2), (1, 3), (2, 3), (1, 4), (3, 4)] if L < 2 else [(2, 3), (3, 4), (2, 5), (3, 5), (5, 6)])
    ks = [k for k in (2, 3, 4, 5) if d * k <= (12 if L == 0 else 24)]
    need(len(ks) >= 3)
    eq = [fr(n * k, d * k) for k in r.sample(ks, 3)]
    k = pick(r, ks)
    good = fr(n * k + 1, d * k) if n * k + 1 < d * k else fr(n * k - 1, d * k)
    return Item(f"Which fraction is NOT equivalent to {fr(n, d)}?", good, [f"Check each fraction by dividing or multiplying the numerator and denominator by the same number.", f"{good} does not equal {fr(n, d)}."],
                [W(e, f"this fraction equals {fr(n, d)}") for e in eq], FN("not_equiv", f=fr(n, d)), qtype="conceptual")


@fam("012", mode="mc")
def ue_true_equation(r, L):
    n, d, k = equiv_pair(r, L)
    good = f"{fr(n, d)} = {fr(n * k, d * k)}"
    bad = [f"{fr(n, d)} = {fr(n + k, d + k)}", f"{fr(n, d)} = {fr(n, d * k)}", f"{fr(n, d)} = {fr(n * k, d)}"]
    need(F(n + k, d + k) != F(n, d))
    return Item("Which equation is true?", good, [f"Multiply the numerator and the denominator by the same number: {n} × {k} = {n * k} and {d} × {k} = {d * k}.", f"{good}."],
                [W(bad[0], "added the same number to the numerator and denominator"), W(bad[1], "changed only the denominator"), W(bad[2], "changed only the numerator")], FN("true_eq"), qtype="conceptual")


# ============================================================== S2 Generating Equivalent Fractions
@fam("012")
def ge_missing(r, L):
    n, d, k = equiv_pair(r, L)
    if r.random() < 0.5:
        return Item(f"Find the missing numerator n: {fr(n, d)} = n/{d * k}", str(n * k), [f"{d} × {k} = {d * k}, so multiply the numerator by {k} too.", f"{n} × {k} = {n * k}."],
                    [W(str(n + d * k - d), "added instead of multiplying"), W(str(n), "kept the numerator the same"), W(str(n * k + k), "multiplied and then added"), W(str(k), "gave the multiplier")],
                    FN("equiv_blank", left=fr(n, d), right=f"?/{d * k}"), qtype="fill-blank")
    return Item(f"Find the missing denominator n: {fr(n, d)} = {n * k}/n", str(d * k), [f"{n} × {k} = {n * k}, so multiply the denominator by {k} too.", f"{d} × {k} = {d * k}."],
                [W(str(d + n * k - n), "added instead of multiplying"), W(str(d), "kept the denominator the same"), W(str(d * k + k), "multiplied and then added"), W(str(k), "gave the multiplier")],
                FN("equiv_blank", left=fr(n, d), right=f"{n * k}/?"), qtype="fill-blank")


@fam("012")
def ge_simplify(r, L):
    n, d = proper(r, L, simplest=True)
    k = pick(r, [k for k in (2, 3, 4, 5, 6) if d * k <= (12 if L == 0 else 24 if L == 1 else 100)])
    N, D = n * k, d * k
    g = gcd(N, D)
    return Item(f"Write {fr(N, D)} in simplest form.", fr(n, d), [f"The greatest number that divides both {N} and {D} is {g}.", f"{N} ÷ {g} = {n} and {D} ÷ {g} = {d}: {fr(n, d)}."],
                [W(fr(N - (k - 1), D - (k - 1)), "subtracted the same number from the top and bottom"), W(fr(d, n), "flipped the fraction"), W(fr(N // 2, D) if N % 2 == 0 else fr(N, D // 2) if D % 2 == 0 else fr(N + 1, D), "divided only one part"),
                 W(fr(N // 2, D // 2), "did not divide all the way") if g > 2 and g % 2 == 0 else W(fr(1, d), "used a unit fraction")],
                EX(fr(N, D), form="frac"), claim=f"{fr(N, D)} in simplest form")


@fam("012")
def ge_with_denominator(r, L):
    n, d, k = equiv_pair(r, L)
    D = d * k
    return Item(f"Write a fraction equivalent to {fr(n, d)} that has a denominator of {D}.", fr(n * k, D), [f"{d} × {k} = {D}, so multiply the numerator by {k} too.", f"{fr(n, d)} = {fr(n * k, D)}."],
                [W(fr(n, D), "changed the denominator but not the numerator"), W(fr(n + D - d, D), "added instead of multiplying"), W(fr(n * k, d), "changed the numerator but not the denominator"), W(fr(k, D), "wrote the multiplier as the numerator")],
                FN("frac_with_den", f=fr(n, d), den=D), claim=f"{fr(n, d)} written with denominator {D}")


@fam("012", mode="mc")
def ge_list(r, L):
    n, d = pick(r, [(1, 2), (1, 3), (1, 4), (2, 3), (3, 4)] if L < 2 else [(2, 3), (3, 4), (2, 5), (3, 5), (1, 6), (5, 6)])
    ks = [2, 3, 4, 5]
    good = [fr(n * k, d * k) for k in sorted(r.sample(ks, 3))]
    def spoil(lst_, kind):
        x = lst_[:]
        i = r.randrange(3)
        a, b = map(int, x[i].split("/"))
        x[i] = [fr(a + 1, b), fr(a, b + 1), fr(a + 1, b + 1)][kind]
        return x
    b1, b2 = spoil([fr(n * k, d * k) for k in sorted(r.sample(ks, 3))], 0), spoil([fr(n * k, d * k) for k in sorted(r.sample(ks, 3))], 1)
    b3 = [fr(n + j, d + j) for j in (1, 2, 3)]
    j = lambda x: ", ".join(x)
    need(len({j(good), j(b1), j(b2), j(b3)}) == 4 and all(F(x) != F(n, d) for x in b3))
    return Item(f"Which list shows only fractions that are equivalent to {fr(n, d)}?", j(good), [f"Multiply the numerator and denominator of {fr(n, d)} by the same number.", f"{j(good)} are all equal to {fr(n, d)}."],
                [W(j(b1), "one fraction is not equivalent"), W(j(b2), "one fraction is not equivalent"), W(j(b3), "added the same number to the numerator and denominator")], FN("all_equiv", f=fr(n, d)), qtype="conceptual", tags={"reasoning"})


@fam("012")
def ge_multiplier(r, L):
    n, d, k = equiv_pair(r, L)
    D = d * k
    return Item(f"To write {fr(n, d)} as an equivalent fraction with a denominator of {D}, you multiply the numerator and the denominator by the same number. What is that number?", str(k),
                [f"{d} × ? = {D}.", f"{D} ÷ {d} = {k}, so multiply both by {k}."],
                [W(str(D - d), "subtracted to find the change instead of dividing"), W(str(n * k), "gave the new numerator"), W(str(D), "gave the new denominator"), W(str(k + 1), "made a division fact mistake")],
                EX(f"{D} ÷ {d}"), qtype="conceptual")


@fam("012")
def ge_tenths_hundredths(r, L):
    n = r.randint(1, 9)
    if r.random() < 0.6 or L == 0:
        return Item(f"Find the missing numerator n: {n}/10 = n/100", str(n * 10), ["10 × 10 = 100, so multiply the numerator by 10 too.", f"{n} × 10 = {n * 10}."],
                    [W(str(n), "kept the numerator the same"), W(str(n + 90), "added instead of multiplying"), W(str(n * 100), "multiplied by 100"), W("10", "gave the multiplier")], FN("equiv_blank", left=f"{n}/10", right="?/100"), qtype="fill-blank")
    return Item(f"Find the missing numerator n: {n * 10}/100 = n/10", str(n), ["100 ÷ 10 = 10, so divide the numerator by 10 too.", f"{n * 10} ÷ 10 = {n}."],
                [W(str(n * 10), "kept the numerator the same"), W(str(n * 100), "multiplied instead of dividing"), W("10", "gave the divisor"), W(str(n + 1), "made a division mistake")], FN("equiv_blank", left=f"{n * 10}/100", right="?/10"), qtype="fill-blank")


@fam("012")
def ge_word(r, L):
    n, d, k = equiv_pair(r, L)
    D = d * k
    n1, n2 = r.sample(NAMES, 2)
    food = pick(r, ["pizza", "granola bar", "sandwich", "pan of brownies"])
    return Item(f"{n1} ate {fr(n, d)} of a {food}. {n2} ate the same amount of a {food} of the same size that was cut into {D} equal pieces. How many pieces did {n2} eat?", f"{n * k} pieces",
                [f"Find the fraction equal to {fr(n, d)} with a denominator of {D}.", f"{fr(n, d)} = {fr(n * k, D)}, so {n2} ate {n * k} pieces."],
                [W(f"{n} pieces", "used the same numerator without changing it"), W(f"{D - n * k} pieces", "found the pieces that were not eaten"), W(f"{n + D - d} pieces", "added instead of multiplying"), W(f"{D} pieces", "gave the total number of pieces")],
                FN("equiv_blank", left=fr(n, d), right=f"?/{D}", unit="pieces"), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def ge_simplest_which(r, L):
    n, d = proper(r, L, simplest=True)
    need(n > 1)
    bad = []
    for _ in range(30):
        a, b = proper(r, L)
        if gcd(a, b) > 1 and fr(a, b) not in bad:
            bad.append(fr(a, b))
    need(len(bad) >= 3)
    return Item("Which fraction is in simplest form?", fr(n, d), ["A fraction is in simplest form when 1 is the only number that divides both the numerator and the denominator.", f"No number greater than 1 divides both {n} and {d}."],
                [W(b, f"both numbers can be divided by {gcd(*map(int, b.split('/')))}") for b in bad[:3]], FN("is_simplest"), qtype="conceptual")


# ============================================================== S3 Comparing with Common Denominators or Numerators
def sym(a, b):
    return "<" if a < b else ">" if a > b else "="


def cmp_item(r, a, b, steps, qtype="procedural", diagram=None, lead="Compare. Write <, > or = to make the statement true:"):
    s = sym(F(a), F(b))
    return Item(f"{lead} {a} ___ {b}", s, steps + [f"{a} {s} {b}."], [W(x, "compared the fractions incorrectly") for x in "<>=" if x != s], FN("compare", a=a, b=b), qtype=qtype, diagram=diagram, claim=f"Compare {a} and {b}", mode="sa")


@fam("012", mode="sa")
def cd_same_den(r, L):
    d = pick(r, DENS[L] if L else [4, 6, 8]) if L < 2 else pick(r, [8, 10, 12, 100])
    a, b = r.sample(range(1, d), 2)
    return cmp_item(r, fr(a, d), fr(b, d), [f"The denominators are the same, so the parts are the same size. Compare the numerators: {a} {sym(a, b)} {b}."])


@fam("012", mode="sa")
def cd_same_num(r, L):
    d1, d2 = r.sample(DENS[L] + ([100] if L == 2 else []), 2)
    n = r.randint(1, min(d1, d2) - 1)
    return cmp_item(r, fr(n, d1), fr(n, d2), [f"The numerators are the same, so compare the size of the parts. {DEN_WORD[min(d1, d2)].capitalize()} are larger than {DEN_WORD[max(d1, d2)]}."], qtype="conceptual")


def unlike_pair(r, L):
    for _ in range(80):
        (a, b), (c, d) = proper(r, L), proper(r, L)
        if b == d or F(a, b) == F(c, d) and r.random() < 0.85:
            continue
        related = max(b, d) % min(b, d) == 0
        if L == 0 and not related:
            continue
        if L == 2 and related:
            continue
        return a, b, c, d
    raise Reject()


@fam("012", mode="sa")
def cd_common_den(r, L):
    a, b, c, d = unlike_pair(r, L)
    m = b * d // gcd(b, d)
    return cmp_item(r, fr(a, b), fr(c, d), [f"Use a common denominator of {m}: {fr(a, b)} = {fr(a * m // b, m)} and {fr(c, d)} = {fr(c * m // d, m)}.", f"Compare the numerators: {a * m // b} {sym(a * m // b, c * m // d)} {c * m // d}."])


@fam("012", mode="mc")
def cd_who(r, L):
    a, b, c, d = unlike_pair(r, L)
    need(F(a, b) != F(c, d))
    n1, n2 = r.sample(NAMES, 2)
    t = pick(r, [("ran", "mile", "ran farther"), ("read", "of the same book", "read more"), ("painted", "of a fence", "painted more"), ("drank", "liter of water", "drank more")])
    m = b * d // gcd(b, d)
    good = n1 if F(a, b) > F(c, d) else n2
    return Item(f"{n1} {t[0]} {fr(a, b)} {t[1]}. {n2} {t[0]} {fr(c, d)} {t[1]}. Who {t[2]}?", good,
                [f"Use a common denominator of {m}: {fr(a, b)} = {fr(a * m // b, m)} and {fr(c, d)} = {fr(c * m // d, m)}.", f"{fr(max(F(a, b), F(c, d)).numerator, max(F(a, b), F(c, d)).denominator)} is greater, so {good} {t[2]}."],
                [W(n2 if good == n1 else n1, "compared only the numerators or only the denominators"), W("They are equal.", "did not find a common denominator")],
                FN("arg_extreme", items={n1: fr(a, b), n2: fr(c, d)}, which="greatest"), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def cd_true(r, L):
    opts = []
    for k in range(12):
        try:
            a, b, c, d = unlike_pair(sub(r, k), L)
        except Reject:
            continue
        if F(a, b) != F(c, d) and (a, b, c, d) not in opts:
            opts.append((a, b, c, d))
        if len(opts) == 4:
            break
    need(len(opts) == 4)
    gi = r.randrange(4)
    out = []
    for k, (a, b, c, d) in enumerate(opts):
        t = sym(F(a, b), F(c, d))
        out.append(f"{fr(a, b)} {t if k == gi else ('<' if t == '>' else '>')} {fr(c, d)}")
    need(len(set(out)) == 4)
    a, b, c, d = opts[gi]
    m = b * d // gcd(b, d)
    return Item("Which comparison is true?", out[gi], [f"Check with a common denominator: {fr(a, b)} = {fr(a * m // b, m)} and {fr(c, d)} = {fr(c * m // d, m)}.", f"{out[gi]} is true."],
                [W(t, "the comparison symbol points the wrong way") for k, t in enumerate(out) if k != gi], FN("true_cmp"), qtype="conceptual", tags={"reasoning"})


@fam("012", mode="sa")
def cd_model(r, L):
    a, b, c, d = unlike_pair(r, L)
    need(b <= 12 and d <= 12)
    alt = f"Two fraction bars of the same length. The top bar has {b} equal parts with {a} shaded. The bottom bar has {d} equal parts with {c} shaded."
    return cmp_item(r, fr(a, b), fr(c, d), ["The bars are the same length, so compare how far the shading reaches."], qtype="visual",
                    diagram=Diagram("fraction_bars", {"bars": [{"parts": b, "shaded": a, "label": fr(a, b)}, {"parts": d, "shaded": c, "label": fr(c, d)}]}, alt), lead="The bars show two fractions of the same whole. Write <, > or = to compare:")


@fam("012", mode="mc")
def cd_reason(r, L):
    d1, d2 = sorted(r.sample(DENS[L], 2))
    n = r.randint(1, d1 - 1)
    big, small = DEN_WORD[d1], DEN_WORD[d2]
    good = f"{big.capitalize()} are larger pieces than {small}, so {fr(n, d1)} is greater."
    return Item(f"{fr(n, d1)} and {fr(n, d2)} have the same numerator. Which statement correctly compares them?", good,
                [f"Cutting a whole into {d1} parts makes larger pieces than cutting it into {d2} parts.", f"Both fractions have {n} piece{'s' if n > 1 else ''}, so {fr(n, d1)} is greater."],
                [W(f"{small.capitalize()} are larger pieces than {big}, so {fr(n, d2)} is greater.", "thought a larger denominator means larger pieces"), W(f"The numerators are the same, so the fractions are equal.", "ignored the size of the pieces"),
                 W(f"{d2} is greater than {d1}, so {fr(n, d2)} is greater.", "compared the denominators as whole numbers")], FN("cmp_reason", a=fr(n, d1), b=fr(n, d2)), qtype="explain", tags={"reasoning"})


# ============================================================== S4 Comparing Fractions with Benchmarks
def vs_half(n, d):
    return "less than" if 2 * n < d else "greater than" if 2 * n > d else "equal to"


@fam("012", mode="mc")
def bm_half_which(r, L):
    op = pick(r, ["greater than", "less than"])
    pool = [(n, d) for d in DENS[max(L, 1)] for n in range(1, d)]
    goods = [p for p in pool if vs_half(*p) == op]
    bads = [p for p in pool if vs_half(*p) != op]
    g = pick(r, goods)
    b = r.sample(bads, 3)
    need(len({fr(*x) for x in b}) == 3)
    return Item(f"Which fraction is {op} 1/2?", fr(*g), [f"Half of {g[1]} is {F(g[1], 2) if g[1] % 2 else g[1] // 2}.", f"{g[0]} is {'more' if op == 'greater than' else 'less'} than half of {g[1]}, so {fr(*g)} is {op} 1/2."],
                [W(fr(*x), f"{fr(*x)} is {vs_half(*x)} 1/2") for x in b], FN("cmp_to", op=op, ref="1/2"), qtype="conceptual")


@fam("012", mode="mc")
def bm_classify(r, L):
    n, d = proper(r, max(L, 1))
    good = f"{vs_half(n, d)} 1/2"
    return Item(f"Is {fr(n, d)} less than, equal to, or greater than 1/2?", good, [f"Half of {d} is {F(d, 2) if d % 2 else d // 2}.", f"The numerator {n} is {'less than' if 2 * n < d else 'more than' if 2 * n > d else 'exactly'} half of {d}, so {fr(n, d)} is {good}."],
                [W(f"{x} 1/2", "did not compare the numerator with half of the denominator") for x in ("less than", "equal to", "greater than") if f"{x} 1/2" != good], FN("vs_ref", f=fr(n, d), ref="1/2"), qtype="conceptual")


@fam("012", mode="sa")
def bm_compare(r, L):
    pool = [(n, d) for d in DENS[max(L, 1)] for n in range(1, d)]
    lo = pick(r, [p for p in pool if vs_half(*p) == "less than"])
    hi = pick(r, [p for p in pool if vs_half(*p) != "less than"])
    need(lo[1] != hi[1] and lo[0] != hi[0])
    a, b = (lo, hi) if r.random() < 0.5 else (hi, lo)
    return cmp_item(r, fr(*a), fr(*b), [f"Use 1/2 as a benchmark: {fr(*lo)} is less than 1/2 and {fr(*hi)} is {vs_half(*hi)} 1/2."], qtype="conceptual", lead="Use the benchmark 1/2 to compare. Write <, > or =:")


def nearest_bench(v):
    best = min([F(0), F(1, 2), F(1)], key=lambda x: abs(v - x))
    ties = [x for x in [F(0), F(1, 2), F(1)] if abs(v - x) == abs(v - best)]
    need(len(ties) == 1)
    return {F(0): "0", F(1, 2): "1/2", F(1): "1"}[best]


@fam("012", mode="mc")
def bm_closest(r, L):
    n, d = proper(r, max(L, 1))
    need(d >= 5)
    good = nearest_bench(F(n, d))
    return Item(f"Is {fr(n, d)} closest to 0, 1/2, or 1?", good, [f"Compare {n} with 0, with half of {d} (which is {F(d, 2) if d % 2 else d // 2}), and with {d}.", f"{fr(n, d)} is closest to {good}."],
                [W(x, "did not compare the numerator with the denominator") for x in ("0", "1/2", "1") if x != good], FN("closest_bench", f=fr(n, d)), qtype="conceptual")


@fam("012", mode="mc")
def bm_number_line(r, L):
    d = pick(r, [8, 10, 12])
    n = r.randint(1, d - 1)
    good = nearest_bench(F(n, d))
    alt = f"A number line from 0 to 1 with tick marks every {fr(1, d)}. Point P is at {fr(n, d)}."
    return Item(f"Point P is on the number line at {fr(n, d)}. Is point P closest to 0, 1/2, or 1?", good, [f"1/2 is at {fr(d // 2, d)} on this number line.", f"{fr(n, d)} is closest to {good}."],
                [W(x, "did not find where 1/2 is on the number line") for x in ("0", "1/2", "1") if x != good], FN("closest_bench", f=fr(n, d)), qtype="visual",
                diagram=Diagram("number_line", {"lo": "0", "hi": "1", "den": d, "labels": "whole", "points": [{"x": fr(n, d), "label": "P"}]}, alt))


@fam("12", mode="mc")
def bm_reason(r, L):
    pool = [(n, d) for d in DENS[L] for n in range(1, d)]
    lo = pick(r, [p for p in pool if vs_half(*p) == "less than"])
    hi = pick(r, [p for p in pool if vs_half(*p) == "greater than"])
    need(lo[1] != hi[1])
    A, B = fr(*hi), fr(*lo)
    f = lambda x, y: f"{A} is {x} than 1/2 and {B} is {y} than 1/2."
    return Item(f"{name(r)} says that {A} > {B}. Which statement explains why this is true?", f("greater", "less"), [f"{A} is more than half and {B} is less than half.", f"So {A} > {B}."],
                [W(f("less", "greater"), "mixed up the two fractions"), W(f("greater", "greater"), f"{B} is not greater than 1/2"), W(f("less", "less"), f"{A} is not less than 1/2")],
                FN("half_reason", a=A, b=B), qtype="explain", tags={"reasoning"})


@fam("012", mode="mc")
def bm_one(r, L):
    d = pick(r, DENS[max(L, 1)])
    good = fr(d + r.randint(1, d - 1), d)
    bad = set()
    while len(bad) < 3:
        dd = pick(r, DENS[max(L, 1)])
        bad.add(fr(r.randint(1, dd), dd))
    return Item("Which fraction is greater than 1?", good, ["A fraction is greater than 1 when its numerator is greater than its denominator.", f"In {good}, the numerator is greater than the denominator."],
                [W(x, "the numerator is not greater than the denominator") for x in sorted(bad)], FN("cmp_to", op="greater than", ref="1"), qtype="conceptual")


# ============================================================== S5 Ordering Fractions
def order_item(r, fs, desc, steps, qtype="ordering"):
    want = sorted(fs, key=lambda x: F(x), reverse=desc)
    j = lambda x: ", ".join(x)
    w2 = want[:]
    w2[0], w2[1] = w2[1], w2[0]
    w3 = want[:]
    w3[-1], w3[-2] = w3[-2], w3[-1]
    need(len({j(want), j(want[::-1]), j(w2), j(w3)}) == 4 and len({F(x) for x in fs}) == len(fs))
    return Item(f"Order the fractions from {'greatest to least' if desc else 'least to greatest'}: {j(fs)}", j(want), steps + [f"In order: {j(want)}."],
                [W(j(want[::-1]), "ordered in the opposite direction"), W(j(w2), "switched two fractions"), W(j(w3), "switched two fractions")], FN("order", values=fs, desc=desc), qtype=qtype, mode="mc")


@fam("012", mode="mc")
def or_same_den(r, L):
    d = pick(r, [6, 8, 10, 12])
    ns = r.sample(range(1, d), 3 if L == 0 else 4)
    return order_item(r, [fr(n, d) for n in ns], r.random() < 0.4, ["The denominators are the same, so order the numerators."])


@fam("012", mode="mc")
def or_same_num(r, L):
    ds = r.sample(DENS[max(L, 1)], 3 if L == 0 else 4)
    n = r.randint(1, min(ds) - 1)
    return order_item(r, [fr(n, d) for d in ds], r.random() < 0.4, ["The numerators are the same. A greater denominator means smaller pieces."])


@fam("12", mode="mc")
def or_unlike(r, L):
    for _ in range(60):
        fs = [proper(r, L) for _ in range(3)]
        m = 1
        for _, d in fs:
            m = m * d // gcd(m, d)
        if m <= 24 and len({F(n, d) for n, d in fs}) == 3 and len({d for _, d in fs}) >= 2:
            break
    else:
        raise Reject()
    return order_item(r, [fr(n, d) for n, d in fs], r.random() < 0.4, [f"Rename with a common denominator of {m}: " + ", ".join(f"{fr(n, d)} = {fr(n * m // d, m)}" for n, d in fs) + "."])


@fam("012", mode="mc")
def or_extreme(r, L):
    for _ in range(60):
        fs = list({proper(r, L) for _ in range(6)})[:4]
        if len(fs) == 4 and len({F(n, d) for n, d in fs}) == 4:
            break
    else:
        raise Reject()
    which = pick(r, ["greatest", "least"])
    g = (max if which == "greatest" else min)(fs, key=lambda p: F(*p))
    return Item(f"Which fraction is the {which}? {', '.join(fr(*p) for p in fs)}", fr(*g), ["Compare with benchmarks such as 1/2, or rename with a common denominator.", f"{fr(*g)} is the {which}."],
                [W(fr(*p), "compared only numerators or only denominators") for p in fs if p != g], FN("extreme_frac", values=[fr(*p) for p in fs], which=which), qtype="conceptual")


@fam("012", mode="mc")
def or_between(r, L):
    lo, hi = pick(r, [(F(1, 4), F(1, 2)), (F(1, 2), F(3, 4)), (F(1, 4), F(3, 4)), (F(1, 3), F(2, 3)), (F(1, 2), F(1))])
    pool = [(n, d) for d in DENS[max(L, 1)] for n in range(1, d)]
    inside = [p for p in pool if lo < F(*p) < hi]
    below = [p for p in pool if F(*p) < lo]
    above = [p for p in pool if F(*p) > hi]
    need(inside and below and len(above) + len(below) >= 3)
    g = pick(r, inside)
    bad = [pick(r, below)] + (r.sample(above, 2) if len(above) >= 2 else r.sample(below, 2))
    need(len({fr(*x) for x in bad}) == 3)
    f = lambda v: fr(v.numerator, v.denominator) if v != 1 else "1"
    return Item(f"Which fraction is between {f(lo)} and {f(hi)}?", fr(*g), [f"The fraction must be greater than {f(lo)} and less than {f(hi)}.", f"{f(lo)} < {fr(*g)} < {f(hi)}."],
                [W(fr(*x), "this fraction is outside the range") for x in bad], FN("between_frac", lo=f(lo), hi=f(hi)), qtype="conceptual", tags={"reasoning"})


@fam("012", mode="mc")
def or_table(r, L):
    for _ in range(60):
        fs = list({proper(r, max(L, 1)) for _ in range(6)})[:4]
        if len(fs) == 4 and len({F(n, d) for n, d in fs}) == 4:
            break
    else:
        raise Reject()
    names = r.sample(NAMES, 4)
    which = pick(r, ["greatest", "least"])
    t = pick(r, [("Distance Walked (miles)", "walked the {w} distance"), ("Juice Left (cups)", "has the {w} amount of juice"), ("Ribbon Used (yards)", "used the {w} amount of ribbon")])
    g = (max if which == "greatest" else min)(range(4), key=lambda i: F(*fs[i]))
    rows = [[nm, fr(*p)] for nm, p in zip(names, fs)]
    alt = f"A table with columns Name and {t[0]}. " + "; ".join(f"{a}: {b}" for a, b in rows) + "."
    return Item(f"The table shows fractions for four students. Who {t[1].format(w=which)}?", names[g], ["Compare the fractions with benchmarks or a common denominator.", f"{fr(*fs[g])} is the {which}, so the answer is {names[g]}."],
                [W(nm, "compared only numerators or only denominators") for i, nm in enumerate(names) if i != g], FN("arg_extreme", items={nm: fr(*p) for nm, p in zip(names, fs)}, which=which),
                qtype="real-world", diagram=Diagram("table", {"header": ["Name", t[0]], "rows": rows}, alt), tags={"modeling"})


@fam("012", mode="mc")
def or_number_line(r, L):
    d = pick(r, [4, 6, 8] if L == 0 else [6, 8, 10, 12])
    ns = sorted(r.sample(range(1, d), 4))
    labs = ["A", "B", "C", "D"]
    i = r.randrange(4)
    k = pick(r, [1, 1, 2]) if d * 2 <= 12 or L else 1
    target = fr(ns[i], d) if k == 1 or gcd(ns[i], d) == 1 else fr(ns[i] // gcd(ns[i], d), d // gcd(ns[i], d))
    alt = f"A number line from 0 to 1 with tick marks every {fr(1, d)}. " + " ".join(f"Point {l} is at {fr(n, d)}." for l, n in zip(labs, ns))
    return Item(f"Which point on the number line shows {target}?", labs[i], [f"The number line is divided into {DEN_WORD[d]}.", f"{target} = {fr(ns[i], d)}, which is point {labs[i]}."],
                [W(l, "counted the tick marks incorrectly") for j, l in enumerate(labs) if j != i], FN("nl_point", points={l: fr(n, d) for l, n in zip(labs, ns)}, target=target), qtype="visual",
                diagram=Diagram("number_line", {"lo": "0", "hi": "1", "den": d, "labels": "whole", "points": [{"x": fr(n, d), "label": l} for l, n in zip(labs, ns)]}, alt))


SKILLS = {
    1: dict(name="Understanding Equivalent Fractions", fams=[ue_bars, ue_model_choice, ue_number_line, ue_why, ue_split_parts, ue_not_equivalent, ue_true_equation]),
    2: dict(name="Generating Equivalent Fractions", fams=[ge_missing, ge_simplify, ge_with_denominator, ge_list, ge_multiplier, ge_tenths_hundredths, ge_word, ge_simplest_which]),
    3: dict(name="Comparing Fractions with Common Denominators or Numerators", fams=[cd_same_den, cd_same_num, cd_common_den, cd_who, cd_true, cd_model, cd_reason]),
    4: dict(name="Comparing Fractions with Benchmarks", fams=[bm_half_which, bm_classify, bm_compare, bm_closest, bm_number_line, bm_reason, bm_one]),
    5: dict(name="Ordering Fractions", fams=[or_same_den, or_same_num, or_unlike, or_extreme, or_between, or_table, or_number_line]),
}
