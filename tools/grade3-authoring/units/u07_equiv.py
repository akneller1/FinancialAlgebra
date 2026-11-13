"""Unit 7: Equivalent and Comparing Fractions (equivalent-comparing-fractions). Denominators 2, 3, 4, 6, 8."""
from g3lib import *

UNIT_ID = "equivalent-comparing-fractions"
# a/b = c/d with d a multiple of b and d <= 8 (Grade 3 denominators). Fractions greater than 1 only above Remedial.
PAIRS = [(1, 2, 2, 4), (1, 2, 3, 6), (1, 2, 4, 8), (1, 3, 2, 6), (2, 3, 4, 6), (1, 4, 2, 8), (3, 4, 6, 8), (2, 4, 4, 8),
         (2, 2, 4, 4), (3, 3, 6, 6), (4, 4, 8, 8), (2, 2, 6, 6), (3, 2, 6, 4), (4, 3, 8, 6), (5, 4, 10, 8), (3, 2, 12, 8), (5, 2, 10, 4), (7, 4, 14, 8)]


def pair(r, L):
    opts = [p for p in PAIRS if (p[0] <= p[1] if L == 0 else True) and (p[0] < p[1] or L)]
    if L == 0:
        opts = [p for p in PAIRS if p[0] < p[1]] + [(2, 2, 4, 4)]
    return pick(r, opts)


# ============================================================== S1 Equivalent Fractions with Models
@fam("012")
def em_bars(r, L):
    a, b, c, d = pair(r, L)
    if r.random() < 0.5:
        alt = f"Two bars of the same length. The top bar is cut into {b} equal parts with {a} shaded. The bottom bar is cut into {d} equal parts with {c} shaded."
        dg, q = Diagram("fraction_bars", {"bars": [{"parts": b, "shaded": a}, {"parts": d, "shaded": c}]}, alt), f"Both bars are the same whole. The top bar shows {a}/{b}. What fraction does the bottom bar show?"
    else:
        alt = f"Two circles of the same size. The left circle is cut into {b} equal parts with {a} shaded. The right circle is cut into {d} equal parts with {c} shaded."
        dg, q = Diagram("circles2", {"a": [b, a], "b": [d, c]}, alt), f"Both circles are the same whole. The left circle shows {a}/{b}. What fraction does the right circle show?"
    need(a <= b and c <= d)
    return Item(q, fr(c, d),
                [f"The second model has {d} equal parts and {c} are shaded.", f"The shaded parts are the same size, so {a}/{b} = {c}/{d}."],
                [W(fr(c, b), "kept the top denominator"), W(fr(a, d), "kept the top numerator"), W(fr(d - c, d) if d - c != c else fr(c + 1, d), "counted the unshaded parts")],
                FN("frac_text", n=c, d=d), qtype="visual", diagram=dg)


@fam("012")
def em_shade(r, L):
    a, b, c, d = pair(r, L)
    alt = f"Two bars of the same length. The top bar is cut into {b} equal parts with {a} shaded. The bottom bar is cut into {d} equal parts with none shaded."
    return Item(f"The top bar shows {a}/{b}. How many parts of the bottom bar should be shaded to show the same amount?", c,
                [f"Each of the top parts matches {d // b} bottom parts.", f"{a} × {d // b} = {c} parts, so {a}/{b} = {c}/{d}."],
                [W(a, "shaded the same number of parts"), W(c + 1, "shaded one part too many"), W(d - c if d - c != c else c - 1, "counted the wrong parts")],
                FN("equiv_num", a=a, b=b, d=d), qtype="visual",
                diagram=Diagram("fraction_bars", {"bars": [{"parts": b, "shaded": a}, {"parts": d, "shaded": 0}]}, alt))


@fam("012")
def em_line(r, L):
    a, b, c, d = pair(r, L)
    alt = f"A number line from 0 to 1 cut into {d} equal parts. Point P is {c} parts from 0."
    return Item(f"Point P is at {a}/{b}. The line is marked in {DEN_WORD[d]}. Which fraction in {DEN_WORD[d]} names the same point?", fr(c, d),
                [f"Count the {DEN_WORD[d]} from 0 to P: {c}.", f"P is at {c}/{d}, so {a}/{b} = {c}/{d}."],
                [W(fr(a, d), "kept the numerator"), W(fr(c + 1, d), "counted the tick mark at 0"), W(fr(c, d + 1), "counted tick marks")],
                FN("frac_text", n=c, d=d), qtype="visual", diagram=Diagram("numline", {"den": d, "hi": 1, "labels": "wholes", "points": [{"n": c, "label": "P"}]}, alt))


@fam("012", mode="mc")
def em_which_pair(r, L):
    a, b, c, d = pair(r, L)
    need(a % b)
    good = f"{a}/{b} and {c}/{d}"
    bad = [f"{a}/{b} and {a}/{d}", f"{a}/{b} and {a + 1}/{b + 1}", f"{a}/{b} and {c + 1}/{d}"]
    it = mc_key("Which pair of fractions are equivalent?", good, bad, ["Equivalent fractions are the same size or the same point on a number line.", f"{a}/{b} and {c}/{d} cover the same part of the same whole."],
                qtype="conceptual", r=r)
    it.check = FN("equiv_pair")
    return it


@fam("12", mode="mc")
def em_strips(r, L):
    a, b, c, d = pair(r, L)
    alt = f"Fraction strips for the same whole: one strip cut into {b} parts and one cut into {d} parts."
    good = f"{c}/{d}, because {c} {DEN_WORD[d]} end at the same place as {a}/{b}"
    bad = [f"{a}/{d}, because the numerators match", f"{c}/{d + 1}, because there are more parts", f"{c + 1}/{d}, because the bottom strip has more parts"]
    return mc_key(f"Use the fraction strips. Which fraction is equivalent to {a}/{b}?", good, bad, [f"Line up {a}/{b} on the first strip.", f"It ends where {c}/{d} ends."],
                  qtype="visual", tags={"reasoning"}, diagram=Diagram("strips", {"dens": [b, d], "shade": [a, c]}, alt), r=r)


@fam("2", mode="mc")
def em_same_whole(r, L):
    nm1, nm2 = name(r), name(sub(r, 2))
    need(nm1 != nm2)
    good = "No. The pizzas are different sizes, so 1/2 of each is not the same amount."
    bad = ["Yes. 1/2 is always the same amount.", "Yes. Both cut their pizza into 2 parts.", "No. 1/2 of the small pizza is more."]
    return mc_key(f"{nm1} eats 1/2 of a small pizza. {nm2} eats 1/2 of a large pizza. {nm1} says they ate the same amount. Is that right?", good, bad,
                  ["Fractions can only be compared when they refer to the same whole.", "Half of a large pizza is more than half of a small pizza."], qtype="explain", tags={"reasoning"}, r=r)


# ============================================================== S2 Generating Equivalent Fractions
@fam("012")
def ge_blank(r, L):
    a, b, c, d = pair(r, L)
    form = pick(r, ["num", "den"]) if L else "num"
    if form == "num":
        q, ans = f"{a}/{b} = ?/{d}", c
    else:
        q, ans = f"{a}/{b} = {c}/?", d
    return Item(f"Find n: {q.replace('?', 'n')}", ans, [f"Each {DEN_ONE[b]} is split into {d // b} equal parts.", f"{a}/{b} = {c}/{d}."],
                [W(a if form == "num" else b, "copied the number from the first fraction"), W(ans + 1, "counted one extra part"), W(c + (d - b) if form == "num" else d + (c - a) + 1, "added the same number to the top and bottom")],
                FN("equiv_blank", q=q), qtype="fill-blank", claim=q.replace("?", "n"))


@fam("012", mode="mc")
def ge_which(r, L):
    a, b, c, d = pair(r, L)
    need(a % b)
    good = fr(c, d)
    bad = [fr(a + 1, b + 1), fr(a, d), fr(b, a) if b != a else fr(c + 1, d)]
    it = mc_key(f"Which fraction is equivalent to {a}/{b}?", good, bad, [f"Split each {DEN_ONE[b]} into {d // b} equal parts.", f"{a}/{b} = {c}/{d}."], r=r)
    it.check = FN("equiv_to", target=f"{a}/{b}")
    return it


@fam("012")
def ge_word(r, L):
    a, b, c, d = pair(r, L)
    nm = name(r)
    return Item(f"{nm} ate {a}/{b} of a sandwich. {name(sub(r, 3))} cut the same size sandwich into {d} equal pieces. How many pieces must be eaten to eat the same amount as {nm}?", f"{c} pieces",
                [f"{d} pieces are {DEN_WORD[d]}. {a}/{b} = {c}/{d}.", f"So {c} pieces."],
                [W(f"{a} pieces", "used the same number of pieces"), W(f"{c + 1} pieces", "counted one extra"), W(f"{d} pieces", "ate the whole sandwich")],
                FN("equiv_num", a=a, b=b, d=d, unit="pieces"), qtype="word-problem")


@fam("12", mode="mc")
def ge_explain(r, L):
    a, b, c, d = pair(r, L)
    k = d // b
    good = f"Each 1/{b} can be cut into {k} pieces of 1/{d}, so {a}/{b} is {c} pieces of 1/{d}."
    bad = [f"You add {k} to the top and bottom.", f"{c}/{d} has bigger numbers, so it is bigger.", f"The denominators are both even."]
    return mc_key(f"Why is {a}/{b} = {c}/{d}?", good, bad, [f"Cut each part into {k} smaller equal parts.", good], qtype="explain", tags={"reasoning"}, r=r)


@fam("2", mode="mc")
def ge_error(r, L):
    a, b = pick(r, [(1, 2), (1, 3), (2, 3), (1, 4)])
    wrong = fr(a + 1, b + 1)
    nm = name(r)
    good = f"No. Adding 1 to the top and bottom does not keep the size the same. {a}/{b} = {a * 2}/{b * 2}."
    bad = [f"Yes. Adding the same number keeps the fraction the same.", f"No. {a}/{b} = {a + 2}/{b + 2}.", f"Yes. The pieces are the same size."]
    return mc_key(f"{nm} says {a}/{b} = {wrong} because 1 was added to the top and bottom. Is that right?", good, bad,
                  [f"Draw {a}/{b} and {wrong}: they are not the same size.", f"Split each part into 2: {a}/{b} = {a * 2}/{b * 2}."], qtype="error-analysis", tags={"misconception"}, r=r)


@fam("2")
def ge_two(r, L):
    q, eq, ans = pick(r, [("1/2 = k/4 = n/8. What is n?", "1/2 = ?/8", 4), ("2/8 = n/4. What is n?", "2/8 = ?/4", 1),
                          ("6/8 = n/4. What is n?", "6/8 = ?/4", 3), ("4/6 = n/3. What is n?", "4/6 = ?/3", 2),
                          ("2/4 = n/2. What is n?", "2/4 = ?/2", 1)])
    return Item(q, ans, ["Use fraction strips or a number line with the same whole.", f"{eq.replace('?', str(ans))}."],
                [W(ans * 2, "doubled instead of halving") if ans != 4 else W(2, "used the fourths numerator"), W(ans + 1, "counted one extra part"), W(ans + 4, "added to the denominator")],
                FN("equiv_blank", q=eq), qtype="multi-step", tags={"reasoning"})


# ============================================================== S3 Whole Numbers as Fractions
@fam("012")
def wn_write(r, L):
    n = r.randint(2, 8)
    form = pick(r, ["over1", "num"]) if L else "over1"
    if form == "over1":
        q, ans = f"Write {n} as a fraction with a denominator of 1: {n} = k/1. What is k?", n
    else:
        b = pick(r, [2, 3, 4]) if L < 2 else pick(r, [2, 3, 4, 6, 8])
        n = r.randint(1, 4)
        q, ans = f"Write {n} as a fraction with a denominator of {b}: {n} = k/{b}. What is k?", n * b
    return Item(q, ans, ["A whole number counts wholes.", f"{q.split(': ')[1].split('.')[0].replace('k', str(ans))}."],
                [W(1, "wrote 1 instead of the number of wholes"), W(ans + 1, "counted one extra"), W(n if ans != n else n * 2, "did not count the parts in each whole")],
                FN("equiv_blank", q=q.split(": ")[1].split(".")[0].replace("k", "?")), qtype="fill-blank")


@fam("012")
def wn_model(r, L):
    n = r.randint(1, 3) if L == 0 else r.randint(2, 3)
    b = pick(r, [2, 3, 4]) if L < 2 else pick(r, [3, 4, 6])
    alt = f"{n} circles, each cut into {b} equal parts, with every part shaded."
    return Item(f"Each circle is one whole. Write the shaded amount as a fraction with denominator {b}, then tell how many wholes it is. Give the number of wholes.", n,
                [f"There are {n * b} shaded parts of size 1/{b}: {n * b}/{b}.", f"{n * b}/{b} = {n} {'whole' if n == 1 else 'wholes'}."],
                [W(n * b, "counted parts, not wholes"), W(b, "gave the number of parts in one whole"), W(n + 1, "counted an extra whole")], FN("wholes_of", n=n * b, d=b), qtype="visual",
                diagram=Diagram("fraction_circle", {"parts": b, "shaded": n * b, "circles": n}, alt))


@fam("012", mode="mc")
def wn_equals_one(r, L):
    b = pick(r, [2, 3, 4, 6, 8])
    n = pick(r, [1, 1, 2, 3])
    good = fr(n * b, b)
    bad = [fr(n, b), fr(n * b + b, b), fr(n * b - 1, b)]
    need(len(set(bad + [good])) == 4)
    word = "1 whole" if n == 1 else f"{n} wholes"
    it = mc_key(f"Which fraction is equal to {word}?", good, bad, [f"Each whole has {b} parts of 1/{b}.", f"{n} × {b} = {n * b}, so {good} = {n}."], r=r)
    it.check = FN("equals_whole", n=n)
    return it


@fam("012")
def wn_value(r, L):
    b = pick(r, [2, 3, 4, 6]) if L else pick(r, [2, 3, 4])
    n = r.randint(1, 4) if L else r.randint(1, 3)
    q = f"{n * b}/{b}"
    v = n
    return Item(f"What whole number is equal to {q}?", v, [f"{b} parts of 1/{b} make 1 whole.", f"{q} = {v}."],
                [W(n * b, "read the numerator as the whole number"), W(0, "thought the fraction is less than 1"), W(v + 1, "counted an extra whole")],
                EX(q), qtype="procedural", claim=f"{q} = ?")


@fam("12", mode="mc")
def wn_three_over_one(r, L):
    n = r.randint(2, 6)
    good = f"{n} wholes, because each whole has 1 part and there are {n} parts"
    bad = [f"1/{n}, because it is one part of {n}", f"{n} thirds", "1 whole, because the bottom number is 1"]
    return mc_key(f"What does {n}/1 mean?", good, bad, ["The denominator 1 means each whole is 1 part.", f"{n} parts of size 1 make {n} wholes."], qtype="conceptual", tags={"reasoning"}, r=r)


@fam("2")
def wn_line(r, L):
    b = pick(r, [2, 3, 4])
    n = pick(r, [2, 3])
    alt = f"A number line from 0 to 3, each whole cut into {b} equal parts. Point W is at the tick mark for {n}."
    return Item(f"The number line is marked in {DEN_WORD[b]}. Point W is at a whole number. Write W as a fraction in {DEN_WORD[b]}.", fr(n * b, b),
                [f"From 0 to W there are {n} wholes of {b} parts each.", f"{n} × {b} = {n * b}, so W = {n * b}/{b}."],
                [W(fr(n, b), "wrote the whole number as the numerator"), W(fr(n * b, 1), "used 1 as the denominator with too many parts"), W(fr(n * b + 1, b), "counted the tick mark at 0")],
                FN("frac_text", n=n * b, d=b), qtype="visual", tags={"reasoning"}, diagram=Diagram("numline", {"den": b, "hi": 3, "labels": [0, b], "points": [{"n": n * b, "label": "W"}]}, alt))


@fam("012")
def wn_parts_in(r, L):
    b = pick(r, [2, 3, 4]) if L == 0 else pick(r, [2, 3, 4, 6, 8])
    n = r.randint(2, 3) if L == 0 else r.randint(2, 5)
    return Item(f"How many {DEN_WORD[b]} make {n} wholes?", n * b, [f"1 whole = {b}/{b}.", f"{n} wholes = {n} × {b} = {n * b} {DEN_WORD[b]}, or {n * b}/{b}."],
                [W(b, "counted the parts in only one whole"), W(n + b, "added"), W(n, "gave the number of wholes")], FN("wholes_parts", n=n, d=b), qtype="conceptual")


@fam("12")
def wn_compare(r, L):
    b = pick(r, [2, 3, 4, 6])
    k = r.randint(1, 4)
    n = r.randint(1, 4)
    s = "<" if k < n else ">" if k > n else "="
    return Item(f"Write <, >, or = : {k * b}/{b} ___ {n}", s, [f"{k * b}/{b} = {k} because {b} {DEN_WORD[b]} make 1 whole.", f"{k} {s} {n}, so {k * b}/{b} {s} {n}."],
                [W("<" if s != "<" else ">", "compared the numerator to the whole number"), W("=" if s != "=" else "<", "did not find the whole number")],
                FN("compare", a=f"{k * b}/{b}", b=str(n)), qtype="procedural", tags={"reasoning"})


# ============================================================== S4 Same Denominator
def same_den(r, L):
    b = pick(r, [3, 4, 6, 8]) if L else pick(r, [3, 4, 6])
    a, c = r.sample(range(1, b + (0 if L < 2 else b // 2)), 2)
    return a, c, b


@fam("012")
def cd_symbol(r, L):
    a, c, b = same_den(r, L)
    s = "<" if a < c else ">"
    return Item(f"Write <, >, or = : {a}/{b} ___ {c}/{b}", s, [f"Both fractions have {DEN_WORD[b]}, so the pieces are the same size.", f"{a} {s} {c}, so {a}/{b} {s} {c}/{b}."],
                [W(">" if s == "<" else "<", "compared the wrong way"), W("=", "thought the denominators make them equal")], FN("compare", a=f"{a}/{b}", b=f"{c}/{b}"), qtype="procedural",
                claim=f"{a}/{b} ___ {c}/{b}")


@fam("012", mode="mc")
def cd_greater(r, L):
    a, c, b = same_den(r, L)
    good = fr(max(a, c), b)
    bad = [fr(min(a, c), b), "They are equal.", "You cannot tell."]
    it = mc_key(f"Which is greater, {a}/{b} or {c}/{b}? (Same whole.)", good, bad, [f"Same denominator: same size pieces.", f"More pieces is more, so {good} is greater."], r=r)
    it.check = FN("pick_greater", a=f"{a}/{b}", b=f"{c}/{b}")
    return it


@fam("012")
def cd_bars(r, L):
    a, c, b = same_den(r, L)
    need(max(a, c) <= b)
    s = "<" if a < c else ">"
    alt = f"Two bars of the same length, each cut into {b} equal parts. The top bar has {a} shaded; the bottom bar has {c} shaded."
    return Item(f"The bars show {a}/{b} and {c}/{b}. Write <, >, or = to compare the top fraction to the bottom fraction.", s,
                [f"Shaded parts: {a} on the top bar and {c} on the bottom bar, all the same size.", f"{a}/{b} {s} {c}/{b}."], [W(">" if s == "<" else "<", "compared the wrong way"), W("=", "thought the same denominator means equal")],
                FN("compare", a=f"{a}/{b}", b=f"{c}/{b}"), qtype="visual", diagram=Diagram("fraction_bars", {"bars": [{"parts": b, "shaded": a}, {"parts": b, "shaded": c}]}, alt))


@fam("012")
def cd_word(r, L):
    a, c, b = same_den(r, L)
    need(max(a, c) < b)
    n1, n2 = name(r), name(sub(r, 5))
    need(n1 != n2)
    return Item(f"{n1} ran {a}/{b} mile. {n2} ran {c}/{b} mile. Who ran farther?", n1 if a > c else n2,
                [f"Same denominator, so compare numerators: {a} and {c}.", f"{max(a, c)}/{b} > {min(a, c)}/{b}, so {n1 if a > c else n2} ran farther."],
                [W(n2 if a > c else n1, "compared the wrong way")], FN("who_more", people={n1: f"{a}/{b}", n2: f"{c}/{b}"}), qtype="word-problem", mode="sa")


@fam("12", mode="mc")
def cd_order(r, L):
    b = pick(r, [6, 8])
    xs = r.sample(range(1, b + (b // 2 if L == 2 else 0)), 3)
    good = ", ".join(fr(x, b) for x in sorted(xs))
    perms = [", ".join(fr(x, b) for x in p) for p in [sorted(xs, reverse=True), [xs[0], xs[2], xs[1]], [sorted(xs)[1], sorted(xs)[0], sorted(xs)[2]]]]
    bad = [p for p in perms if p != good]
    need(len(set(bad)) == 3)
    it = mc_key(f"Order from least to greatest: {', '.join(fr(x, b) for x in xs)}", good, bad, ["Same denominator: order the numerators.", good + "."], qtype="procedural", r=r)
    it.check = FN("order_fracs", values=[fr(x, b) for x in xs])
    return it


@fam("2", mode="mc")
def cd_not_same_whole(r, L):
    a, c, b = same_den(r, L)
    need(a < c and c < b)
    good = f"No. The pieces of the big pizza are bigger, so you cannot compare without the same whole."
    bad = [f"Yes, because {c} > {a}.", f"No, because {a}/{b} > {c}/{b} always.", "Yes, because both have the same denominator."]
    return mc_key(f"{name(r)} has {c}/{b} of a small pizza. {name(sub(r, 6))} has {a}/{b} of a very large pizza. Is it true that the first person must have more pizza?", good, bad,
                  ["Comparing fractions only works when they refer to the same whole.", "The wholes are different sizes here."], qtype="explain", tags={"reasoning"}, r=r)


# ============================================================== S5 Same Numerator
def same_num(r, L):
    a = pick(r, [1, 1, 2]) if L == 0 else r.randint(1, 3) if L == 1 else r.randint(2, 5)
    b, d = r.sample([x for x in [2, 3, 4, 6, 8] if x > a or L == 2], 2)
    return a, b, d


@fam("012")
def cn_symbol(r, L):
    a, b, d = same_num(r, L)
    s = "<" if F(a, b) < F(a, d) else ">"
    return Item(f"Write <, >, or = : {a}/{b} ___ {a}/{d}", s, [f"Same numerator: {a} pieces each.", f"{DEN_WORD[min(b, d)].capitalize()} are bigger pieces than {DEN_WORD[max(b, d)]}, so {a}/{b} {s} {a}/{d}."],
                [W(">" if s == "<" else "<", "thought a bigger denominator means a bigger fraction"), W("=", "thought the same numerator means equal")],
                FN("compare", a=f"{a}/{b}", b=f"{a}/{d}"), qtype="procedural", claim=f"{a}/{b} ___ {a}/{d}")


@fam("012", mode="mc")
def cn_greater(r, L):
    a, b, d = same_num(r, L)
    good = fr(a, min(b, d))
    bad = [fr(a, max(b, d)), "They are equal.", "You cannot tell."]
    it = mc_key(f"Which is greater, {a}/{b} or {a}/{d}? (Same whole.)", good, bad,
                [f"Both have {a} pieces.", f"Pieces of size 1/{min(b, d)} are bigger than pieces of size 1/{max(b, d)}, so {good} is greater."], r=r)
    it.check = FN("pick_greater", a=f"{a}/{b}", b=f"{a}/{d}")
    return it


@fam("012")
def cn_share(r, L):
    b, d = r.sample([2, 3, 4, 6, 8], 2)
    nm = name(r)
    return Item(f"One sandwich is shared equally by {b} friends. Another sandwich of the same size is shared equally by {d} friends. In which group does each friend get a bigger piece: the group of {b} or the group of {d}?",
                f"the group of {min(b, d)}", [f"Sharing with fewer people makes bigger pieces.", f"1/{min(b, d)} > 1/{max(b, d)}."],
                [W(f"the group of {max(b, d)}", "thought more people means bigger pieces")], FN("group_of", b=b, d=d), qtype="word-problem", mode="sa")


@fam("012")
def cn_bars(r, L):
    a, b, d = same_num(r, L)
    need(a <= min(b, d))
    s = "<" if F(a, b) < F(a, d) else ">"
    alt = f"Two bars of the same length. The top bar is cut into {b} equal parts with {a} shaded; the bottom bar is cut into {d} equal parts with {a} shaded."
    return Item(f"The bars show {a}/{b} and {a}/{d}. Write <, >, or = to compare the top fraction to the bottom fraction.", s,
                [f"Both bars have {a} shaded parts, but the parts are different sizes.", f"{a}/{b} {s} {a}/{d}."], [W(">" if s == "<" else "<", "compared denominators like whole numbers"), W("=", "thought the same numerator means equal")],
                FN("compare", a=f"{a}/{b}", b=f"{a}/{d}"), qtype="visual", diagram=Diagram("fraction_bars", {"bars": [{"parts": b, "shaded": a}, {"parts": d, "shaded": a}]}, alt))


@fam("012", mode="mc")
def cn_pieces(r, L):
    b, d = r.sample([2, 3, 4, 6, 8], 2)
    lo, hi = min(b, d), max(b, d)
    good = f"the {DEN_WORD[lo]}, because there are fewer pieces in the whole"
    bad = [f"the {DEN_WORD[hi]}, because {hi} is greater than {lo}", "they are the same size", f"the {DEN_WORD[hi]}, because there are more pieces"]
    return mc_key(f"Two same-size strips are cut into {DEN_WORD[b]} and {DEN_WORD[d]}. Which pieces are bigger?", good, bad,
                  ["The more equal pieces a whole is cut into, the smaller each piece is.", f"1/{lo} > 1/{hi}."], qtype="conceptual", tags={"reasoning"}, r=r)


@fam("12", mode="mc")
def cn_error(r, L):
    a, b, d = same_num(r, L)
    lo, hi = min(b, d), max(b, d)
    good = f"No. {a}/{lo} > {a}/{hi} because 1/{lo} is a bigger piece than 1/{hi}."
    bad = [f"Yes. {hi} > {lo}, so {a}/{hi} > {a}/{lo}.", f"No. They are equal because the numerators match.", f"Yes. More pieces means more."]
    return mc_key(f"{name(r)} says {a}/{hi} > {a}/{lo} because {hi} is greater than {lo}. Is that right?", good, bad,
                  ["When numerators are the same, compare the size of the pieces.", f"{DEN_WORD[lo].capitalize()} are bigger than {DEN_WORD[hi]}."], qtype="error-analysis", tags={"misconception"}, r=r)


@fam("2", mode="mc")
def cn_order(r, L):
    a = r.randint(1, 2)
    ds = r.sample([3, 4, 6, 8], 3)
    good = ", ".join(fr(a, x) for x in sorted(ds))
    perms = [", ".join(fr(a, x) for x in sorted(ds, reverse=True)), ", ".join(fr(a, x) for x in [ds[0], ds[2], ds[1]]), ", ".join(fr(a, x) for x in ds), ", ".join(fr(a, x) for x in [ds[1], ds[0], ds[2]])]
    bad = [p for p in dict.fromkeys(perms) if p != good][:3]
    need(len(bad) == 3)
    it = mc_key(f"Order from greatest to least: {', '.join(fr(a, x) for x in ds)}", good, bad, ["Same numerator: the smaller the denominator, the bigger the pieces.", good + "."], qtype="procedural", r=r)
    it.check = FN("order_fracs", values=[fr(a, x) for x in ds], desc=True)
    return it


SKILLS = {
    1: dict(name="Equivalent Fractions with Models", fams=[em_bars, em_shade, em_line, em_which_pair, em_strips, em_same_whole]),
    2: dict(name="Generating Equivalent Fractions", fams=[ge_blank, ge_which, ge_word, ge_explain, ge_error, ge_two]),
    3: dict(name="Whole Numbers as Fractions", fams=[wn_write, wn_model, wn_equals_one, wn_value, wn_parts_in, wn_compare, wn_three_over_one, wn_line]),
    4: dict(name="Comparing Fractions with the Same Denominator", fams=[cd_symbol, cd_greater, cd_bars, cd_word, cd_order, cd_not_same_whole]),
    5: dict(name="Comparing Fractions with the Same Numerator", fams=[cn_symbol, cn_greater, cn_share, cn_bars, cn_pieces, cn_error, cn_order]),
}
