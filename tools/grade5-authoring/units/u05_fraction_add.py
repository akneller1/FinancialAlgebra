"""Unit 5: Fraction Concepts and Operations (fraction-add-subtract)."""
from g5lib import *
from math import gcd

UNIT_ID = "fraction-addition-subtraction"
DENS = {0: [2, 3, 4, 5, 6, 8, 10], 1: [2, 3, 4, 5, 6, 8, 9, 10, 12], 2: [3, 4, 5, 6, 7, 8, 9, 10, 12, 15]}


def lcm(a, b):
    return a * b // gcd(a, b)


def proper(r, dens):
    d = pick(r, dens)
    return F(r.randint(1, d - 1), d)


def pair(r, L):
    """Two proper fractions with unlike denominators. L0: one denominator divides the other."""
    for _ in range(40):
        a, b = proper(r, DENS[L]), proper(r, DENS[L])
        if a.denominator == b.denominator or a == b:
            continue
        da, db = a.denominator, b.denominator
        related = max(da, db) % min(da, db) == 0
        if L == 0 and not related:
            continue
        if L == 2 and related:
            continue
        return a, b
    raise Reject()


def fs(x):
    """Fraction text as written in problems (simplest proper or mixed)."""
    return mixed(x)


def add_wrongs(a, b, op="+"):
    na, da, nb, db = a.numerator, a.denominator, b.numerator, b.denominator
    out = []
    if op == "+":
        out.append(W(f"{na + nb}/{da + db}", "added the numerators and added the denominators"))
        out.append(W(fs(F(na + nb, max(da, db))), "added the numerators without finding a common denominator"))
        out.append(W(fs(F(na * db + nb, da * db)), "renamed only one fraction"))
        out.append(W(fs(a + b + 1) if a + b < 1 else fs(a + b - F(1, lcm(da, db))), "made a mistake when regrouping"))
    else:
        if na - nb > 0 and da != db:
            out.append(W(f"{abs(na - nb)}/{abs(da - db)}", "subtracted the numerators and subtracted the denominators"))
        out.append(W(fs(F(abs(na - nb), max(da, db))) if na != nb else fs(F(1, max(da, db))), "subtracted the numerators without finding a common denominator"))
        out.append(W(fs(a + b), "added instead of subtracting"))
        out.append(W(fs(F(abs(na * db - nb), da * db)) if na * db != nb else fs(a - b + F(1, lcm(da, db))), "renamed only one fraction"))
    return out


# ============================================================== S1 Equivalent Fractions and Common Denominators
@fam("012")
def e_missing(r, L):
    a = proper(r, DENS[L])
    a = F(a.numerator, a.denominator)
    k = r.randint(2, 6 if L < 2 else 9)
    top = r.random() < 0.5
    n, d = a.numerator, a.denominator
    if top:
        return Item(f"Find the missing numerator n: {n}/{d} = n/{d * k}", str(n * k), [f"{d} × {k} = {d * k}, so multiply the numerator by {k} too.", f"{n} × {k} = {n * k}."],
                    [W(str(n + d * k - d), "added instead of multiplying"), W(str(n * k + k), "multiplied and then added"), W(str(d * k - d + n - 1) if n * k != d * k - d + n - 1 else str(n), "kept the numerator the same")],
                    FN("equiv_blank", left=f"{n}/{d}", right=f"?/{d * k}"), qtype="fill-blank")
    return Item(f"Find the missing denominator n: {n}/{d} = {n * k}/n", str(d * k), [f"{n} × {k} = {n * k}, so multiply the denominator by {k} too.", f"{d} × {k} = {d * k}."],
                [W(str(d + n * k - n), "added instead of multiplying"), W(str(d * k + 1), "made a multiplication slip"), W(str(n * k * d), "multiplied by the wrong number")],
                FN("equiv_blank", left=f"{n}/{d}", right=f"{n * k}/?"), qtype="fill-blank")


@fam("012")
def e_simplify(r, L):
    a = proper(r, DENS[L])
    k = r.randint(2, 6) if L < 2 else r.randint(3, 12)
    n, d = a.numerator * k, a.denominator * k
    g = gcd(n, d)
    part = F(n // (g // pick(r, [x for x in range(2, g + 1) if g % x == 0])), d // (g // 1)) if False else None
    divs = [x for x in range(2, g) if g % x == 0]
    half = f"{n // divs[0]}/{d // divs[0]}" if divs else f"{n}/{d}"
    return Item(f"Write {n}/{d} in simplest form.", frac(a), [f"The greatest common factor of {n} and {d} is {g}.", f"{n} ÷ {g} = {a.numerator} and {d} ÷ {g} = {a.denominator}: {frac(a)}."],
                [W(f"{n - (k - 1)}/{d - (k - 1)}", "subtracted the same number from the top and bottom"), W(f"{a.denominator}/{a.numerator}", "flipped the fraction"), W(f"{n // 2}/{d}" if n % 2 == 0 else f"{n}/{d // 2}" if d % 2 == 0 else f"{n + 1}/{d}", "divided only one part")],
                EX(f"{n}/{d}", form="frac"), qtype="procedural", claim=f"{n}/{d} in simplest form")


@fam("012")
def e_lcd(r, L):
    a, b = pair(r, L)
    da, db = a.denominator, b.denominator
    v = lcm(da, db)
    return Item(f"What is the least common denominator of {frac(a)} and {frac(b)}?", str(v),
                [f"List multiples of {da} and {db}.", f"The least number that both divide is {v}."],
                [W(str(da * db), "multiplied the denominators (a common denominator, but not the least)") if da * db != v else W(str(da + db), "added the denominators"),
                 W(str(da + db), "added the denominators"), W(str(max(da, db)), "used the larger denominator"), W(str(gcd(da, db)) if gcd(da, db) > 1 else str(v * 2), "found a common factor instead of a common multiple")],
                FN("lcd", a=frac(a), b=frac(b)), qtype="procedural")


@fam("012", mode="mc")
def e_which(r, L):
    a = proper(r, DENS[L])
    k = r.randint(2, 5)
    good = f"{a.numerator * k}/{a.denominator * k}"
    bad = [f"{a.numerator + k}/{a.denominator + k}", f"{a.numerator * k}/{a.denominator + k}", f"{a.denominator * k}/{a.numerator * k}"]
    bad = [b for b in dict.fromkeys(bad) if F(b) != a]
    need(len(bad) == 3)
    opts = [(good, True)] + [(b, False) for b in bad]
    r.shuffle(opts)
    return Item(f"Which fraction is equivalent to {frac(a)}?", good, ["Multiply the numerator and denominator by the same number.", f"{frac(a)} = {good}."],
                check=FN("equiv_to", target=frac(a)), options=opts, mode="mc", qtype="conceptual")


@fam("012")
def e_bars(r, L):
    a = proper(r, [2, 3, 4, 5, 6] if L < 2 else [3, 4, 5, 6])
    k = r.randint(2, 3 if L == 0 else 4)
    n, d = a.numerator, a.denominator
    alt = f"Two fraction bars of the same length. The top bar has {d} equal parts with {n} shaded. The bottom bar has {d * k} equal parts with {n * k} shaded."
    return Item(f"The top bar shows {frac(a)}. The bottom bar is the same whole cut into {d * k} parts and shaded the same amount. What fraction does the bottom bar show?", f"{n * k}/{d * k}",
                [f"Each part of the top bar was split into {k} parts.", f"{n} × {k} = {n * k} shaded out of {d * k}: {n * k}/{d * k}."],
                [W(f"{n}/{d * k}", "counted the shaded parts of the top bar"), W(f"{n * k}/{d}", "kept the old number of parts"), W(f"{d * k - n * k}/{d * k}", "counted the unshaded parts")],
                FN("frac_text_equal", n=n * k, d=d * k), qtype="visual",
                diagram=Diagram("fraction_bars", {"bars": [{"parts": d, "shaded": n, "label": frac(a)}, {"parts": d * k, "shaded": n * k, "label": "?"}]}, alt))


@fam("012", mode="sa")
def e_compare(r, L):
    a, b = pair(r, L)
    need(a != b)
    sym = "<" if a < b else ">"
    D = lcm(a.denominator, b.denominator)
    return Item(f"Compare. Write <, >, or =.\n{frac(a)} ___ {frac(b)}", sym,
                [f"Rename with the common denominator {D}: {a.numerator * D // a.denominator}/{D} and {b.numerator * D // b.denominator}/{D}.", f"So {frac(a)} {sym} {frac(b)}."],
                [W(">" if sym == "<" else "<", "compared only the denominators")], FN("compare", a=frac(a), b=frac(b)), qtype="procedural", mode="sa")


# ============================================================== S2 Adding Fractions with Unlike Denominators
@fam("012")
def a_basic(r, L):
    a, b = pair(r, L)
    s = a + b
    D = lcm(a.denominator, b.denominator)
    return Item(f"Add: {frac(a)} + {frac(b)}", fs(s),
                [f"Common denominator {D}: {a.numerator * D // a.denominator}/{D} + {b.numerator * D // b.denominator}/{D} = {a.numerator * D // a.denominator + b.numerator * D // b.denominator}/{D}.",
                 f"Simplify: {fs(s)}."], add_wrongs(a, b), EX(f"{frac(a)}+{frac(b)}", form="mixed"), qtype="procedural", claim=f"{frac(a)} + {frac(b)}")


@fam("12")
def a_three(r, L):
    a, b = pair(r, L)
    c = proper(r, [2, 3, 4, 6])
    s = a + b + c
    return Item(f"Add: {frac(a)} + {frac(b)} + {frac(c)}", fs(s),
                [f"Use a common denominator for all three: {lcm(lcm(a.denominator, b.denominator), c.denominator)}.", f"The sum is {fs(s)}."],
                [W(f"{a.numerator + b.numerator + c.numerator}/{a.denominator + b.denominator + c.denominator}", "added the tops and the bottoms"), W(fs(a + b), "left out the third fraction"), W(fs(s - F(1, 1)) if s > 1 else fs(s + 1), "made a regrouping mistake")],
                EX(f"{frac(a)}+{frac(b)}+{frac(c)}", form="mixed"), qtype="multi-step", tags={"multistep"})


@fam("012")
def a_model(r, L):
    da = pick(r, [2, 3, 4])
    db = pick(r, [x for x in [2, 3, 4, 6, 8] if x != da])
    a, b = F(r.randint(1, da - 1), da), F(r.randint(1, db - 1), db)
    D = lcm(da, db)
    need(D <= 12 and a + b <= 1)
    s = a + b
    alt = f"Fraction bars: one bar shows {frac(a)}, one shows {frac(b)}, and a third bar is cut into {D} equal parts with {int(s * D)} shaded."
    return Item(f"The model shows {frac(a)} + {frac(b)} using a bar cut into {D}ths. What is the sum?", fs(s),
                [f"{frac(a)} = {int(a * D)}/{D} and {frac(b)} = {int(b * D)}/{D}.", f"{int(a * D)}/{D} + {int(b * D)}/{D} = {int(s * D)}/{D} = {fs(s)}."],
                add_wrongs(a, b), EX(f"{frac(a)}+{frac(b)}", form="mixed"), qtype="visual",
                diagram=Diagram("fraction_bars", {"bars": [{"parts": da, "shaded": a.numerator, "label": frac(a)}, {"parts": db, "shaded": b.numerator, "label": frac(b)},
                                                           {"parts": D, "shaded": int(s * D), "label": "sum"}]}, alt))


@fam("012")
def a_missing(r, L):
    a, b = pair(r, L)
    s = a + b
    return Item(f"Fill in the blank: {frac(a)} + ___ = {fs(s)}", frac(b), [f"Subtract: {fs(s)} − {frac(a)}.", f"The missing fraction is {frac(b)}."],
                [W(fs(s + a), "added instead of subtracting"), W(f"{abs(s.numerator - a.numerator)}/{abs(s.denominator - a.denominator)}" if s.denominator != a.denominator and s.numerator != a.numerator else fs(s - a + F(1, 12)), "subtracted the tops and the bottoms"),
                 W(fs(F(abs(s.numerator - a.numerator) or 1, max(s.denominator, a.denominator))), "did not use a common denominator")],
                EX(f"{fs(s).replace(' ', '+')}-{frac(a)}", form="mixed"), qtype="fill-blank")


CTX_ADD = [("{n} uses {a} cup of flour and {b} cup of sugar. How many cups is that in all?", "cups"),
           ("{n} walked {a} mile to the park and {b} mile to the library. How far did {n} walk?", "miles"),
           ("A gardener used {a} bag of soil on Monday and {b} bag on Tuesday. How many bags were used?", "bags"),
           ("{n} read for {a} hour before dinner and {b} hour after dinner. How long did {n} read?", "hours")]


@fam("012")
def a_word(r, L):
    a, b = pair(r, L)
    t, unit = pick(r, CTX_ADD)
    s = a + b
    return Item(t.format(n=name(r), a=frac(a), b=frac(b)), f"{fs(s)} {unit}", [f"Add {frac(a)} + {frac(b)} with a common denominator.", f"{frac(a)} + {frac(b)} = {fs(s)} {unit}."],
                [W(f"{w[0]} {unit}", w[1]) for w in add_wrongs(a, b)], EX(f"{frac(a)}+{frac(b)}", unit=unit, form="mixed"), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def a_first_step(r, L):
    a, b = pair(r, L)
    D = lcm(a.denominator, b.denominator)
    good = f"{a.numerator * D // a.denominator}/{D} + {b.numerator * D // b.denominator}/{D}"
    bad = [f"{a.numerator + b.numerator}/{a.denominator + b.denominator}", f"{a.numerator}/{D} + {b.numerator}/{D}", f"{a.denominator}/{a.numerator} + {b.denominator}/{b.numerator}"]
    bad = [x for x in dict.fromkeys(bad) if x != good]
    need(len(bad) == 3)
    return mc_key(f"Which shows a correct first step to add {frac(a)} + {frac(b)}?", good, bad,
                  [f"Rename both fractions with a common denominator, such as {D}.", good], r=r, qtype="compare-strategies", tags={"reasoning"})


# ============================================================== S3 Subtracting Fractions with Unlike Denominators
def sub_pair(r, L):
    a, b = pair(r, L)
    if a < b:
        a, b = b, a
    return a, b


@fam("012")
def s_basic(r, L):
    a, b = sub_pair(r, L)
    v = a - b
    D = lcm(a.denominator, b.denominator)
    return Item(f"Subtract: {frac(a)} − {frac(b)}", fs(v),
                [f"Common denominator {D}: {a.numerator * D // a.denominator}/{D} − {b.numerator * D // b.denominator}/{D}.", f"= {int(v * D)}/{D} = {fs(v)}."],
                add_wrongs(a, b, "-"), EX(f"{frac(a)}-{frac(b)}", form="mixed"), qtype="procedural", claim=f"{frac(a)} − {frac(b)}")


@fam("012")
def s_from_whole(r, L):
    w = 1 if L < 2 else r.randint(2, 4)
    b = proper(r, DENS[L])
    v = w - b
    return Item(f"Subtract: {w} − {frac(b)}", fs(v), [f"Write {w} as {w * b.denominator}/{b.denominator}.", f"{w * b.denominator}/{b.denominator} − {frac(b)} = {fs(v)}."],
                [W(fs(F(b.denominator - b.numerator + 1, b.denominator)) if w == 1 else fs(F(w - 1) + b), "subtracted from the wrong number of parts"), W(f"{w - b.numerator}/{b.denominator}" if w > b.numerator else fs(v + 1), "subtracted the numerator from the whole number"),
                 W(fs(b), "gave the part taken away"), W(fs(v + 1) if w > 1 else fs(F(b.denominator - b.numerator, 1)), "forgot to regroup a whole")],
                EX(f"{w}-{frac(b)}", form="mixed"), qtype="procedural")


@fam("012")
def s_model(r, L):
    D = pick(r, [6, 8, 10, 12])
    da = pick(r, [x for x in [2, 3, 4, 5, 6] if D % x == 0])
    db = pick(r, [x for x in [2, 3, 4, 6, 8, 12, 10, 5] if D % x == 0 and x != da])
    a, b = F(r.randint(1, da - 1), da), F(r.randint(1, db - 1), db)
    need(a > b and lcm(da, db) == D)
    v = a - b
    alt = f"A fraction bar cut into {D} equal parts with {int(a * D)} parts shaded; {int(b * D)} of the shaded parts are crossed out."
    return Item(f"The bar is cut into {D} equal parts. It shows {frac(a)} with {frac(b)} taken away. What is {frac(a)} − {frac(b)}?", fs(v),
                [f"{frac(a)} = {int(a * D)}/{D} and {frac(b)} = {int(b * D)}/{D}.", f"{int(a * D)}/{D} − {int(b * D)}/{D} = {int(v * D)}/{D} = {fs(v)}."],
                add_wrongs(a, b, "-"), EX(f"{frac(a)}-{frac(b)}", form="mixed"), qtype="visual",
                diagram=Diagram("fraction_bars", {"bars": [{"parts": D, "shaded": int(a * D), "label": frac(a)}, {"parts": D, "shaded": int(v * D), "label": "left"}]}, alt))


CTX_SUB = [("A pitcher had {a} gallon of juice. {n} poured out {b} gallon. How much juice is left?", "gallon"),
           ("{n} has {a} yard of ribbon and uses {b} yard for a bow. How much ribbon is left?", "yard"),
           ("A trail is {a} mile long. {n} has walked {b} mile. How much farther must {n} walk?", "mile"),
           ("{n} had {a} of a pizza and ate {b} of the pizza. How much of the pizza is left?", "of the pizza")]


@fam("012")
def s_word(r, L):
    a, b = sub_pair(r, L)
    t, unit = pick(r, CTX_SUB)
    v = a - b
    return Item(t.format(n=name(r), a=frac(a), b=frac(b)), f"{fs(v)} {unit}", [f"Subtract {frac(a)} − {frac(b)} using a common denominator.", f"= {fs(v)} {unit}."],
                [W(f"{w[0]} {unit}", w[1]) for w in add_wrongs(a, b, "-")], EX(f"{frac(a)}-{frac(b)}", unit=unit, form="mixed"), qtype="word-problem", tags={"modeling"})


@fam("012")
def s_how_much_more(r, L):
    a, b = sub_pair(r, L)
    n1, n2 = name(r), name(r)
    need(n1 != n2)
    thing = pick(r, [("ran", "mile"), ("drank", "liter of water"), ("painted", "of the fence")])
    v = a - b
    return Item(f"{n1} {thing[0]} {frac(a)} {thing[1]}. {n2} {thing[0]} {frac(b)} {thing[1]}. How much more did {n1} do than {n2}?", fs(v),
                [f"Find the difference: {frac(a)} − {frac(b)}.", f"= {fs(v)}."],
                add_wrongs(a, b, "-"), EX(f"{frac(a)}-{frac(b)}", form="mixed"), qtype="word-problem")


@fam("012", mode="mc")
def s_check(r, L):
    a, b = sub_pair(r, L)
    v = a - b
    good = f"{fs(v)} + {frac(b)} = {frac(a)}"
    bad = [f"{fs(v)} − {frac(b)} = {frac(a)}", f"{frac(a)} + {frac(b)} = {fs(v)}", f"{fs(v)} + {frac(a)} = {frac(b)}"]
    return mc_key(f"{name(r)} found {frac(a)} − {frac(b)} = {fs(v)}. Which equation checks the answer?", good, bad,
                  ["Addition undoes subtraction: difference + part taken away = starting amount.", good], r=r, qtype="conceptual")


# ============================================================== S4 Adding and Subtracting Mixed Numbers
def mix_pair(r, L, sub_=False):
    a, b = pair(r, max(L, 0))
    wa, wb = r.randint(1, 6), r.randint(1, 4)
    A, B = wa + a, wb + b
    if sub_:
        if A < B:
            A, B = B, A
        need(A - B > 0)
        if L == 0:
            need((A - int(A)) >= (B - int(B)))   # no regrouping at the remedial level
        if L == 2:
            need((A - int(A)) < (B - int(B)))    # regrouping required
    return A, B


@fam("012")
def m_add(r, L):
    A, B = mix_pair(r, L)
    s = A + B
    wa, fa, wb, fb = int(A), A - int(A), int(B), B - int(B)
    return Item(f"Add: {fs(A)} + {fs(B)}", fs(s),
                [f"Add the whole numbers: {wa} + {wb} = {wa + wb}. Add the fractions: {frac(fa)} + {frac(fb)} = {fs(fa + fb)}.", f"Combine: {fs(s)}."],
                [W(f"{wa + wb} {fa.numerator + fb.numerator}/{fa.denominator + fb.denominator}", "added the numerators and the denominators"), W(fs(wa + wb + (fa + fb - 1)) if fa + fb > 1 else fs(s + 1), "forgot to regroup the extra whole" if fa + fb > 1 else "added an extra whole"),
                 W(fs(F(wa + wb) + fa), "left out one fraction"), W(fs(s - 1), "lost a whole when regrouping")],
                EX(f"{fs(A).replace(' ', '+')}+{fs(B).replace(' ', '+')}", form="mixed"), qtype="procedural", claim=f"{fs(A)} + {fs(B)}")


@fam("012")
def m_sub(r, L):
    A, B = mix_pair(r, L, True)
    v = A - B
    wa, fa, wb, fb = int(A), A - int(A), int(B), B - int(B)
    bad = [W(fs(F(wa - wb) + abs(fa - fb)), "subtracted the smaller fraction from the larger one instead of regrouping") if fa < fb else W(fs(v + 1), "subtracted the whole numbers incorrectly"),
           W(fs(A + B), "added instead of subtracting"), W(fs(v - 1) if v > 1 else fs(v + 2), "regrouped but forgot to take away the whole")]
    return Item(f"Subtract: {fs(A)} − {fs(B)}", fs(v),
                [f"Use a common denominator{' and regroup 1 whole from ' + str(wa) if fa < fb else ''}.", f"{fs(A)} − {fs(B)} = {fs(v)}."],
                bad, EX(f"{fs(A).replace(' ', '+')}-({fs(B).replace(' ', '+')})", form="mixed"), qtype="procedural", claim=f"{fs(A)} − {fs(B)}")


@fam("012")
def m_improper(r, L):
    d = pick(r, DENS[L])
    w = r.randint(1, 9)
    n = r.randint(1, d - 1)
    need(gcd(n, d) == 1)
    v = w + F(n, d)
    to_imp = r.random() < 0.5
    if to_imp:
        return Item(f"Write {w} {n}/{d} as a fraction greater than 1 (an improper fraction).", f"{w * d + n}/{d}",
                    [f"{w} wholes = {w * d}/{d}.", f"{w * d}/{d} + {n}/{d} = {w * d + n}/{d}."],
                    [W(f"{w * n + d}/{d}", "multiplied the whole number by the numerator"), W(f"{w + n}/{d}", "added the whole number to the numerator"), W(f"{w * d + n}/{w * d}", "changed the denominator")],
                    FN("improper", n=w * d + n, d=d), qtype="procedural", tags={"multiple-representations"})
    return Item(f"Write {w * d + n}/{d} as a mixed number.", f"{w} {n}/{d}", [f"{w * d + n} ÷ {d} = {w} R {n}.", f"So {w * d + n}/{d} = {w} {n}/{d}."],
                [W(f"{w} {d - n}/{d}" if d - n != n else f"{w + 1} {n}/{d}", "used the wrong remainder"), W(f"{w + 1} {n}/{d}", "miscounted the wholes"), W(f"{n} {w}/{d}" if w < d else f"{w - 1} {n}/{d}", "swapped the quotient and remainder")],
                EX(f"{w * d + n}/{d}", form="mixed"), qtype="procedural", tags={"multiple-representations"})


@fam("012")
def m_word(r, L):
    A, B = mix_pair(r, L, sub_=r.random() < 0.5)
    op = "-" if A > B and r.random() < 0.5 else "+"
    if op == "-" and A < B:
        A, B = B, A
    v = A + B if op == "+" else A - B
    t = pick(r, [("A plant was {A} inches tall. It grew {B} inches. How tall is it now?", "inches", "+"),
                 ("{n} has {A} cups of rice and uses {B} cups. How much rice is left?", "cups", "-"),
                 ("{n} biked {A} miles on Saturday and {B} miles on Sunday. How far did {n} bike?", "miles", "+"),
                 ("A board is {A} feet long. {n} cuts off {B} feet. How long is the board now?", "feet", "-")])
    need(t[2] == op or (op == "+" and t[2] == "+") or (op == "-" and t[2] == "-"))
    return Item(t[0].format(A=fs(A), B=fs(B), n=name(r)), f"{fs(v)} {t[1]}", [f"{'Add' if op == '+' else 'Subtract'} the mixed numbers.", f"{fs(A)} {'+' if op == '+' else '−'} {fs(B)} = {fs(v)} {t[1]}."],
                [W(f"{fs(A - B if op == '+' else A + B)} {t[1]}", "used the wrong operation"), W(f"{fs(v + 1)} {t[1]}", "made a regrouping mistake"), W(f"{fs(v - F(1, lcm((A - int(A)).denominator, (B - int(B)).denominator)))} {t[1]}" if v > 1 else f"{fs(v + 2)} {t[1]}", "made a mistake adding the fractions")],
                EX(f"{fs(A).replace(' ', '+')}{op}({fs(B).replace(' ', '+')})", unit=t[1], form="mixed"), qtype="word-problem", tags={"modeling"})


@fam("012")
def m_regroup(r, L):
    w = r.randint(2, 9)
    d = pick(r, [3, 4, 5, 6, 8])
    n = r.randint(1, d - 1)
    return Item(f"Fill in the blank to regroup one whole: {w} {n}/{d} = {w - 1} ___/{d}", str(d + n),
                [f"One whole is {d}/{d}.", f"{d}/{d} + {n}/{d} = {d + n}/{d}, so {w} {n}/{d} = {w - 1} {d + n}/{d}."],
                [W(str(n + 1), "added only 1 to the numerator"), W(str(n + 10), "regrouped a ten instead of one whole"), W(str(d - n), "subtracted instead of adding")],
                FN("regroup", w=w, n=n, d=d), qtype="fill-blank", tags={"reasoning"})


# ============================================================== S5 Estimating with Benchmark Fractions
def bench(x):
    """Nearest of 0, 1/2, 1 (or whole/half) — ties are avoided by the families."""
    return F(round(x * 2), 2)


def safe(x):
    q = x * 4
    return q.denominator != 1 or (q.numerator % 2 == 0)


@fam("012")
def b_nearest(r, L):
    d = pick(r, [5, 6, 7, 8, 9, 10, 12])
    n = r.randint(1, d - 1)
    x = F(n, d)
    need(x * 4 not in (1, 3) and x != F(1, 2))
    b = bench(x)
    return Item(f"Is {frac(x)} closest to 0, 1/2, or 1?", fs(b),
                [f"Half of {d} is {F(d, 2) if d % 2 else d // 2}. Compare {n} with that and with {d}.", f"{frac(x)} is closest to {fs(b)}."],
                [W(fs(F(1, 2)) if b != F(1, 2) else "1", "compared only the numerators"), W("0" if b != 0 else "1", "thought a small numerator means close to 0"), W("1" if b != 1 else "0", "thought a big denominator means close to 1")],
                FN("benchmark", x=frac(x)), qtype="conceptual", mode="sa")


@fam("012")
def b_sum(r, L):
    for _ in range(30):
        a, b = proper(r, [5, 6, 7, 8, 9, 10, 12]), proper(r, [5, 6, 7, 8, 9, 10, 12])
        if a * 4 not in (1, 3) and b * 4 not in (1, 3) and a.denominator != b.denominator:
            break
    else:
        raise Reject()
    op = pick(r, ["+", "−"]) if L else "+"
    if op == "−" and a < b:
        a, b = b, a
    ba, bb = bench(a), bench(b)
    v = ba + bb if op == "+" else ba - bb
    need(v >= 0)
    return Item(f"Use benchmarks (0, 1/2, or 1) to estimate {frac(a)} {op} {frac(b)}.", fs(v),
                [f"{frac(a)} is about {fs(ba)} and {frac(b)} is about {fs(bb)}.", f"{fs(ba)} {op} {fs(bb)} = {fs(v)}."],
                [W(fs(a + b if op == "+" else a - b), "found the exact answer instead of estimating"), W(fs(v + F(1, 2)), "rounded one fraction the wrong way"), W(fs(v + 1), "rounded both fractions up")],
                FN("bench_sum", a=frac(a), b=frac(b), op=op), qtype="procedural")


@fam("012")
def b_vs_one(r, L):
    a, b = pair(r, max(L, 1))
    s = a + b
    need(s != 1)
    ans = "greater than 1" if s > 1 else "less than 1"
    return Item(f"Without finding the exact sum, is {frac(a)} + {frac(b)} greater than 1 or less than 1?", ans,
                [f"Compare each fraction with 1/2: {frac(a)} is {'more' if a > F(1, 2) else 'less' if a < F(1, 2) else 'equal to'} than 1/2 and {frac(b)} is {'more' if b > F(1, 2) else 'less' if b < F(1, 2) else 'equal to'} than 1/2.",
                 f"The exact sum is {fs(s)}, which is {ans}."],
                [W("less than 1" if s > 1 else "greater than 1", "compared denominators instead of using benchmarks")], FN("sum_cmp", a=frac(a), b=frac(b)), qtype="explain", mode="sa", tags={"reasoning"})


@fam("012", mode="mc")
def b_reasonable(r, L):
    a, b = pair(r, max(L, 1))
    s = a + b
    wrong = F(a.numerator + b.numerator, a.denominator + b.denominator)
    need(wrong != s and wrong < max(a, b))
    nm = name(r)
    good = f"Not reasonable. {frac(wrong)} is less than {frac(max(a, b))}, but adding a positive fraction should make the sum larger than each fraction."
    bad = [f"Reasonable. The numerators and denominators were both added.", f"Reasonable. {frac(wrong)} is between {frac(min(a, b))} and {frac(max(a, b))}.", f"Not reasonable. The sum must be exactly 1."]
    return mc_key(f"{nm} says {frac(a)} + {frac(b)} = {frac(wrong)}. Is the answer reasonable?", good, bad,
                  [f"The actual sum is {fs(s)}.", good], r=r, qtype="explain", tags={"reasoning", "error-analysis"})


@fam("012")
def b_numberline(r, L):
    d = pick(r, [6, 8, 10, 12])
    n = r.randint(1, d - 1)
    x = F(n, d)
    need(x * 4 not in (1, 3) and x != F(1, 2))
    alt = f"Number line from 0 to 1 divided into {d} equal parts. Point P is at the {n}th mark."
    b = bench(x)
    it = Item("Point P is on the number line. Which benchmark is P closest to: 0, 1/2, or 1?", fs(b),
              [f"P is at {frac(x)}.", f"{frac(x)} is closest to {fs(b)}."],
              [W("1/2" if b != F(1, 2) else "1", "estimated the location carelessly"), W("0" if b != 0 else "1", "read the number line from the wrong end")],
              FN("benchmark", x=frac(x)), qtype="visual", mode="sa",
              diagram=Diagram("number_line", {"lo": "0", "hi": "1", "den": d, "labels": "whole", "points": [{"x": frac(x), "label": "P"}]}, alt))
    it.consts = [n]
    return it


# ============================================================== S6 Fraction Word Problems
@fam("012")
def w_left(r, L):
    a, b = pair(r, L)
    need(a + b < 1)
    v = 1 - a - b
    what = pick(r, [("pizza", "ate", "of the pizza"), ("garden", "planted with tomatoes and peppers", "of the garden"), ("book", "read on two days", "of the book")])
    nm = name(r)
    if what[0] == "pizza":
        q = f"{nm} ate {frac(a)} of a pizza and a friend ate {frac(b)} of it. What fraction of the pizza is left?"
    elif what[0] == "garden":
        q = f"In a garden, {frac(a)} is planted with tomatoes and {frac(b)} with peppers. What fraction of the garden is left to plant?"
    else:
        q = f"{nm} read {frac(a)} of a book on Monday and {frac(b)} of it on Tuesday. What fraction of the book is left to read?"
    return Item(q, fs(v), [f"Fraction used: {frac(a)} + {frac(b)} = {fs(a + b)}.", f"Left: 1 − {fs(a + b)} = {fs(v)}."],
                [W(fs(a + b), "found the part used, not the part left"), W(fs(1 - a), "subtracted only one fraction"), W(f"{a.denominator + b.denominator - a.numerator - b.numerator}/{a.denominator + b.denominator}", "added tops and bottoms")],
                EX(f"1-{frac(a)}-{frac(b)}", form="mixed"), qtype="multi-step", tags={"multistep", "modeling"})


@fam("012")
def w_total(r, L):
    A, B = mix_pair(r, L) if L else pair(r, L)
    t = pick(r, [("A recipe needs {A} cups of milk and {B} cups of water. How much liquid is that?", "cups"),
                 ("{n} hiked {A} miles in the morning and {B} miles in the afternoon. How far did {n} hike?", "miles"),
                 ("A puppy gained {A} pounds in March and {B} pounds in April. How much did it gain in all?", "pounds")])
    v = A + B
    return Item(t[0].format(A=fs(A), B=fs(B), n=name(r)), f"{fs(v)} {t[1]}", [f"Add {fs(A)} + {fs(B)}.", f"= {fs(v)} {t[1]}."],
                [W(f"{fs(abs(A - B))} {t[1]}", "subtracted instead of adding"), W(f"{fs(v + 1)} {t[1]}", "added an extra whole"), W(f"{fs(v - F(1, 2)) if v > F(1, 2) else fs(v + F(1, 2))} {t[1]}", "made a mistake with the common denominator")],
                EX(f"{fs(A).replace(' ', '+')}+{fs(B).replace(' ', '+')}", unit=t[1], form="mixed"), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def w_equation(r, L):
    a, b = pair(r, L)
    nm = name(r)
    if a < b:
        a, b = b, a
    q = f"{nm} had {frac(a)} of a bag of popcorn and ate {frac(b)} of the bag. Which equation shows how much is left?"
    good = f"{frac(a)} − {frac(b)} = p"
    bad = [f"{frac(a)} + {frac(b)} = p", f"{frac(b)} − {frac(a)} = p", f"{frac(a)} × {frac(b)} = p"]
    return mc_key(q, good, bad, ["Eating some takes it away, so subtract.", good], r=r, qtype="word-problem", tags={"modeling"})


@fam("012")
def w_compare(r, L):
    a, b = sub_pair(r, L)
    n1, n2 = name(r), name(r)
    need(n1 != n2)
    v = a - b
    return Item(f"A snail owned by {n1} crawled {frac(a)} meter. A snail owned by {n2} crawled {frac(b)} meter. How much farther did the first snail crawl?", f"{fs(v)} meter",
                [f"Find the difference: {frac(a)} − {frac(b)}.", f"= {fs(v)} meter."],
                [W(f"{w[0]} meter", w[1]) for w in add_wrongs(a, b, "-")], EX(f"{frac(a)}-{frac(b)}", unit="meter", form="mixed"), qtype="word-problem")


@fam("12")
def w_two_step(r, L):
    A, B = mix_pair(r, L)
    C = proper(r, [2, 4, 8])
    tot = A + B
    need(tot - C > 0)
    v = tot - C
    return Item(f"{name(r)} bought {fs(A)} pounds of apples and {fs(B)} pounds of pears, then used {frac(C)} pound of the fruit in a pie. How many pounds of fruit are left?", f"{fs(v)} pounds",
                [f"Total bought: {fs(A)} + {fs(B)} = {fs(tot)}.", f"Left: {fs(tot)} − {frac(C)} = {fs(v)} pounds."],
                [W(f"{fs(tot)} pounds", "forgot to subtract the fruit used"), W(f"{fs(tot + C)} pounds", "added the fruit used"), W(f"{fs(A - C)} pounds", "used only the apples")],
                EX(f"{fs(A).replace(' ', '+')}+{fs(B).replace(' ', '+')}-{frac(C)}", unit="pounds", form="mixed"), qtype="multi-step", tags={"multistep"})


SKILLS = {
    1: dict(name="Equivalent Fractions and Common Denominators", fams=[e_missing, e_simplify, e_lcd, e_which, e_bars, e_compare]),
    2: dict(name="Adding Fractions with Unlike Denominators", fams=[a_basic, a_three, a_model, a_missing, a_word, a_first_step]),
    3: dict(name="Subtracting Fractions with Unlike Denominators", fams=[s_basic, s_from_whole, s_model, s_word, s_how_much_more, s_check]),
    4: dict(name="Adding and Subtracting Mixed Numbers", fams=[m_add, m_sub, m_improper, m_word, m_regroup]),
    5: dict(name="Estimating with Benchmark Fractions", fams=[b_nearest, b_sum, b_vs_one, b_reasonable, b_numberline]),
    6: dict(name="Fraction Word Problems", fams=[w_left, w_total, w_equation, w_compare, w_two_step]),
}
