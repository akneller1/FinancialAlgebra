"""Unit 6: Understanding Fractions (understanding-fractions). Denominators 2, 3, 4, 6, 8 (Grade 3 scope)."""
from g3lib import *

UNIT_ID = "understanding-fractions"


def den(r, L):
    return pick(r, [2, 3, 4]) if L == 0 else pick(r, [3, 4, 6, 8]) if L == 1 else pick(r, [4, 6, 8, 3])


def model(r, b, a, kind=None):
    kind = kind or pick(r, ["bar", "circle"])
    if kind == "bar":
        return Diagram("fraction_bars", {"bars": [{"parts": b, "shaded": a}]}, f"A bar cut into {b} equal parts with {a} {'part' if a == 1 else 'parts'} shaded.")
    return Diagram("fraction_circle", {"parts": b, "shaded": a}, f"A circle cut into {b} equal parts with {a} {'part' if a == 1 else 'parts'} shaded.")


# ============================================================== S1 Unit Fractions and Equal Parts
@fam("012")
def ue_name(r, L):
    b = den(r, L)
    return Item("The whole is cut into equal parts. What fraction of the whole is shaded?", fr(1, b),
                [f"There are {b} equal parts and 1 is shaded.", f"One of {b} equal parts is 1/{b}."],
                [W(fr(1, b - 1) if b > 2 else fr(1, 3), "counted the parts that are not shaded"), W(fr(b, 1), "switched the numerator and denominator"), W(fr(1, b + 1), "counted one part too many")],
                EX(f"1/{b}"), qtype="visual", diagram=model(r, b, 1))


@fam("012", mode="mc")
def ue_equal(r, L):
    b = pick(r, [2, 3, 4])
    eq = r.random() < 0.5
    if eq:
        d = pick(r, [{"shape": "rect", "cuts": "v", "widths": [1] * b}, {"shape": "circle", "n": b}] + ([{"shape": "square", "cuts": "grid", "rows": 2, "cols": 2}, {"shape": "square", "cuts": "diag4"}] if b == 4 else []) + ([{"shape": "hexagon", "cuts": "rhomb3"}] if b == 3 else []))
        alt = f"A shape cut into {b} equal parts."
    else:
        ws = [1] * b
        ws[r.randrange(b)] = 2
        d = pick(r, [{"shape": "rect", "cuts": "v", "widths": ws}, {"shape": "circle", "angles": [360 * w / sum(ws) for w in ws]}])
        alt = f"A shape cut into {b} parts. The parts are not the same size."
    d["shade"] = [0]
    name_ = DEN_WORD[b]
    good = f"Yes. It has {b} equal parts." if eq else f"No. The {b} parts are not equal."
    bad = ([f"No. The parts must be the same shape.", f"No. It needs {b + 1} parts.", f"Yes, but only because there are {b} parts."] if eq else
           [f"Yes. It has {b} parts.", f"Yes. Each part is 1/{b}.", f"No. It needs {b + 1} parts."])
    return mc_key(f"Is this shape divided into {name_}?", good, bad, [f"{name_.capitalize()} means {b} EQUAL parts.", good], qtype="visual", tags={"reasoning"},
                  diagram=Diagram("partition", d, alt), r=r)


@fam("012")
def ue_word(r, L):
    b = den(r, L)
    t = pick(r, ["A pizza is cut into {b} equal slices. {nm} eats 1 slice. What fraction of the pizza does {nm} eat?",
                 "A garden is split into {b} equal parts. Carrots grow in 1 part. What fraction of the garden has carrots?",
                 "A ribbon is cut into {b} equal pieces. {nm} uses 1 piece. What fraction of the ribbon does {nm} use?"])
    return Item(t.format(b=b, nm=name(r)), fr(1, b), [f"The whole has {b} equal parts.", f"1 part is 1/{b} of the whole."],
                [W(fr(b, 1), "switched the numerator and denominator"), W(fr(1, b - 1) if b > 2 else fr(1, 3), "counted the other parts"), W(fr(1, b + 1), "counted one extra part")],
                EX(f"1/{b}"), qtype="word-problem")


@fam("012")
def ue_how_many(r, L):
    b = den(r, L)
    return Item(f"How many copies of 1/{b} make one whole?", b, [f"1/{b} is one of {b} equal parts.", f"{b} parts of size 1/{b} make 1 whole."],
                [W(1, "thought one part is the whole"), W(b - 1, "counted one part too few"), W(b + 1, "counted one part too many")], FN("units_in_whole", d=b), qtype="conceptual")


@fam("12", mode="mc")
def ue_name_word(r, L):
    b = den(r, L)
    good = f"one‑{DEN_ONE[b]}"
    others = [x for x in [2, 3, 4, 6, 8] if x != b]
    bad = [f"one‑{DEN_ONE[x]}" for x in r.sample(others, 3)]
    return mc_key(f"A whole is cut into {b} equal parts. What is the name of each part?", good, bad, [f"{b} equal parts are {DEN_WORD[b]}.", f"Each part is one‑{DEN_ONE[b]}, 1/{b}."], r=r)


@fam("2")
def ue_part_to_whole(r, L):
    b = den(r, L)
    return Item(f"A bar shows 1/{b} of a whole. The part is 3 inches long. How many inches long is the whole bar?", f"{3 * b} inches",
                [f"The whole is {b} parts of 1/{b}.", f"{b} × 3 = {3 * b} inches."],
                [W(f"3 inches", "thought the part is the whole"), W(f"{3 + b} inches", "added"), W(f"{3 * (b - 1)} inches", "used one part too few")], EX(f"{b}*3", unit="inches"), qtype="multi-step", tags={"reasoning"})


@fam("2", mode="mc")
def ue_error(r, L):
    b = pick(r, [3, 4])
    ws = [1] * b
    ws[0] = 2
    good = f"No. The parts are not equal, so a part is not 1/{b}."
    bad = [f"Yes. There are {b} parts, so each is 1/{b}.", f"No. Each part is 1/{b + 1}.", f"Yes. The shaded part is 1/{b} because it is the biggest."]
    alt = f"A rectangle cut into {b} parts; the first part is twice as wide as the others and is shaded."
    return mc_key(f"{name(r)} says the shaded part is 1/{b} of the rectangle. Is that right?", good, bad,
                  ["A unit fraction names one of several EQUAL parts.", "The shaded part is bigger than the other parts."], qtype="error-analysis", tags={"misconception"},
                  diagram=Diagram("partition", {"shape": "rect", "cuts": "v", "widths": ws, "shade": [0]}, alt), r=r)


# ============================================================== S2 Fractions Made from Unit Fractions
@fam("012")
def ua_name(r, L):
    b = den(r, L)
    a = r.randint(2, b) if b > 2 else 1
    need(a < b or L)
    return Item("What fraction of the whole is shaded?", fr(a, b), [f"There are {b} equal parts; {a} are shaded.", f"{a} parts of size 1/{b} is {a}/{b}."],
                [W(fr(a, b - a) if b - a else fr(a, 1), "wrote shaded parts over unshaded parts"), W(fr(b - a, b) if b != 2 * a else fr(b, a), "counted the parts that are not shaded"), W(fr(b, a), "switched the numerator and denominator")],
                EX(f"{a}/{b}"), qtype="visual", diagram=model(r, b, a))


@fam("012")
def ua_copies(r, L):
    b = den(r, L)
    a = r.randint(2, b) if L < 2 else r.randint(2, 2 * b - 1)
    ask = pick(r, ["count", "frac"])
    if ask == "count":
        return Item(f"{a}/{b} is how many copies of 1/{b}?", a, [f"The numerator tells how many unit fractions.", f"{a}/{b} = {a} copies of 1/{b}."],
                    [W(b, "gave the denominator"), W(a + 1, "counted one extra"), W(1, "thought there is only one part")], FN("copies", n=a, d=b), qtype="conceptual")
    return Item(f"What fraction is {a} copies of 1/{b}?", fr(a, b), [f"{a} parts of size 1/{b}.", f"That is {a}/{b}."],
                [W(fr(a, a + b), "added the numerator to the denominator"), W(fr(b, a), "switched numerator and denominator"), W(fr(1, b), "gave only one unit fraction"), W(fr(a + 1, b), "counted one extra copy")],
                EX(f"{a}/{b}"), qtype="conceptual")


@fam("012")
def ua_word(r, L):
    b = den(r, L)
    a = r.randint(2, b - 1) if b > 2 else 1
    t = pick(r, ["A cake is cut into {b} equal pieces. {nm} eats {a} pieces. What fraction of the cake does {nm} eat?",
                 "A fence has {b} equal sections. {nm} paints {a} sections. What fraction of the fence is painted?",
                 "A chocolate bar has {b} equal pieces. {nm} shares {a} pieces. What fraction of the bar is shared?"])
    return Item(t.format(a=a, b=b, nm=name(r)), fr(a, b), [f"The whole has {b} equal parts; {a} are used.", f"{a}/{b}."],
                [W(fr(a, b - a) if b - a != a else fr(b, a), "wrote used parts over unused parts"), W(fr(b - a, b), "found the part that is left"), W(fr(b, a), "switched numerator and denominator")],
                EX(f"{a}/{b}"), qtype="word-problem")


@fam("012")
def ua_not_shaded(r, L):
    b = den(r, L)
    need(b > 2)
    a = r.randint(1, b - 1)
    need(b - a != a)
    return Item("What fraction of the whole is NOT shaded?", fr(b - a, b), [f"There are {b} equal parts; {a} are shaded, so {b - a} are not.", f"{b - a}/{b}."],
                [W(fr(a, b), "named the shaded part"), W(fr(b - a, a), "wrote unshaded over shaded"), W(fr(b, b - a), "switched numerator and denominator")],
                EX(f"({b}-{a})/{b}"), qtype="visual", diagram=model(r, b, a))


@fam("2")
def ua_more_than_one(r, L):
    b = pick(r, [2, 3, 4, 6])
    a = r.randint(b + 1, 2 * b - 1)
    alt = f"Two bars, each a whole cut into {b} equal parts. The first bar is fully shaded and {a - b} parts of the second bar are shaded."
    return Item(f"Each bar is one whole. How many {DEN_WORD[b]} are shaded in all? Write the fraction.", fr(a, b),
                [f"Count all the shaded parts of size 1/{b}: {a}.", f"{a} copies of 1/{b} is {a}/{b}."],
                [W(fr(a, 2 * b), "used all the parts of both bars as the denominator"), W(fr(a - b, b), "counted only the second bar"), W(fr(b, a), "switched numerator and denominator")],
                EX(f"({b}+{a - b})/{b}"), qtype="visual", tags={"reasoning"},
                diagram=Diagram("fraction_bars", {"bars": [{"parts": b, "shaded": b}, {"parts": b, "shaded": a - b}]}, alt))


@fam("2", mode="mc")
def ua_error(r, L):
    b = pick(r, [4, 6, 8])
    a = r.randint(1, b - 1)
    need(b - a != a)
    good = f"{a}/{b}, because {a} of the {b} equal parts {'is' if a == 1 else 'are'} shaded"
    bad = [f"{a}/{b - a}, because {a} are shaded and {b - a} are not", f"{b - a}/{b}, because {b - a} parts are white", f"{b}/{a}, because there are {b} parts"]
    return mc_key(f"{name(r)} says the model shows {a}/{b - a}. What fraction does it really show?", good, bad,
                  ["The denominator counts ALL the equal parts.", f"{a} of {b} parts: {a}/{b}."], qtype="error-analysis", tags={"misconception"}, diagram=model(r, b, a, "bar"), r=r)


# ============================================================== S3 Unit Fractions on a Number Line
def nl(b, hi=1, n=None, label="A", jumps=0, labels="wholes"):
    d = {"den": b, "hi": hi, "labels": labels}
    if n is not None:
        d["points"] = [{"n": n, "label": label}]
    if jumps:
        d["jumps"] = jumps
    return d


def ud(r, L):
    return pick(r, [2, 3, 4, 6]) if L == 0 else pick(r, [2, 3, 4, 6, 8])


@fam("012")
def nu_point(r, L):
    b = ud(r, L)
    hi = pick(r, [1, 1, 2, 3])
    lab = pick(r, ["A", "B", "P", "M", "K"])
    alt = f"A number line from 0 to {hi}. Each whole is cut into {b} equal parts. Point {lab} is at the first tick mark after 0."
    return Item(f"What fraction is at point {lab}?", fr(1, b), [f"The space from 0 to 1 is cut into {b} equal parts.", f"Point {lab} is 1 part from 0, so it is at 1/{b}."],
                [W(fr(1, b + 1), "counted the tick marks instead of the spaces"), W(fr(1, b - 1) if b > 2 else fr(1, 3), "miscounted the spaces"), W(fr(b, 1), "switched numerator and denominator"),
                 W(fr(1, hi * b) if hi > 1 else fr(2, b), "used the whole line as one whole" if hi > 1 else "counted two parts")],
                EX(f"1/{b}"), qtype="visual", diagram=Diagram("numline", nl(b, hi=hi, n=1, label=lab), alt))


@fam("012")
def nu_word(r, L):
    b = ud(r, L)
    t = pick(r, [("The trail from the gate (0) to the pond (1 mile) has {b} equal parts. A bench is at the end of the first part. How far is the bench from the gate?", "mile"),
                 ("A ribbon that is 1 meter long is marked into {b} equal parts. {nm} cuts at the first mark. How long is the piece {nm} cuts?", "meter"),
                 ("A race track from start (0) to finish (1 mile) is split into {b} equal parts. A flag is at the end of the first part. How far is the flag from the start?", "mile")])
    return Item(t[0].format(b=b, nm=name(r)), f"1/{b} {t[1]}", [f"The whole (0 to 1) is cut into {b} equal parts.", f"The first mark is at 1/{b} {t[1]}."],
                [W(f"1/{b + 1} {t[1]}", "counted the marks instead of the parts"), W(f"{b}/1 {t[1]}", "switched numerator and denominator"), W(f"1/{b - 1 if b > 2 else 3} {t[1]}", "miscounted the parts")],
                EX(f"1/{b}", unit=t[1]), qtype="word-problem")


@fam("012", mode="mc")
def nu_which(r, L):
    b = pick(r, [3, 4, 6, 8]) if L else pick(r, [3, 4, 6])
    spots = r.sample(range(2, b + 1), 2) + [1]
    labels = ["A", "B", "C"]
    r.shuffle(labels)
    pts = [{"n": n, "label": l} for n, l in zip(spots, labels)]
    alt = f"A number line from 0 to 1 cut into {b} equal parts, with points " + ", ".join(f"{p['label']} at {p['n']} {'part' if p['n'] == 1 else 'parts'} from 0" for p in sorted(pts, key=lambda p: p["label"])) + "."
    good = labels[2]
    it = mc_key(f"Which point is at 1/{b}?", good, [l for l in ["A", "B", "C", "none of them"] if l != good],
                [f"1/{b} is the end of the first part from 0.", f"Point {good} is 1 part from 0."], qtype="visual",
                diagram=Diagram("numline", {"den": b, "hi": 1, "labels": "wholes", "points": pts}, alt), r=r)
    it.check = FN("point_at", points=pts, n=1)
    return it


@fam("012")
def nu_parts(r, L):
    b = ud(r, L)
    alt = f"A number line from 0 to 1 with {b - 1} tick marks between 0 and 1."
    return Item("Into how many equal parts is the space from 0 to 1 divided?", b, [f"Count the spaces, not the tick marks.", f"There are {b} equal spaces."],
                [W(b - 1, "counted the tick marks between 0 and 1"), W(b + 1, "counted every tick mark"), W(1, "thought the whole is one part")],
                FN("units_in_whole", d=b), qtype="visual", diagram=Diagram("numline", nl(b), alt))


@fam("012")
def nu_jump(r, L):
    b = ud(r, L)
    alt = f"A number line from 0 to 1 with {b} equal jumps drawn from 0 to 1."
    return Item("The jumps from 0 to 1 are all the same size. How long is each jump? Write a fraction.", fr(1, b),
                [f"There are {b} equal jumps from 0 to 1.", f"Each jump is 1/{b}."],
                [W(fr(1, b + 1), "counted tick marks"), W(fr(b, 1), "switched numerator and denominator"), W(fr(1, b - 1) if b > 2 else fr(1, 4), "miscounted the jumps")],
                EX(f"1/{b}"), qtype="visual", diagram=Diagram("numline", nl(b, jumps=b), alt))


@fam("012", mode="mc")
def nu_how_to(r, L):
    b = ud(r, L)
    good = f"Cut 0 to 1 into {b} equal parts and mark the end of the first part."
    bad = [f"Cut 0 to 1 into {b} equal parts and mark the end of the last part.", f"Make {b} tick marks between 0 and 1 and mark the first one.", f"Cut 0 to {b} into equal parts and mark 1."]
    return mc_key(f"How do you show 1/{b} on a number line?", good, bad, [f"The whole is 0 to 1; cut it into {b} equal parts.", f"1/{b} is at the end of the first part from 0."], qtype="conceptual", r=r)


@fam("12")
def nu_two_wholes(r, L):
    b = den(r, L)
    alt = f"A number line from 0 to 2. Each whole is cut into {b} equal parts. Point A is at the first tick mark after 0."
    return Item("The number line goes from 0 to 2. What fraction is at point A?", fr(1, b), [f"Each whole (0 to 1) is cut into {b} equal parts.", f"A is one part from 0: 1/{b}."],
                [W(fr(1, 2 * b), "used the whole line 0 to 2 as the whole"), W(fr(1, b + 1), "counted tick marks"), W(fr(2, b), "counted 2 parts")],
                EX(f"1/{b}"), qtype="visual", tags={"reasoning"}, diagram=Diagram("numline", nl(b, hi=2, n=1), alt))


@fam("2", mode="mc")
def nu_error(r, L):
    b = den(r, L)
    good = f"1/{b}, because there are {b} equal spaces between 0 and 1"
    bad = [f"1/{b - 1}, because there are {b - 1} tick marks between 0 and 1", f"1/{b + 1}, because there are {b + 1} tick marks", f"{b}/1, because there are {b} spaces"]
    need(b > 2)
    alt = f"A number line from 0 to 1 cut into {b} equal parts. Point A is at the first tick mark after 0."
    return mc_key(f"{name(r)} says point A is at 1/{b - 1}. What is the correct fraction and why?", good, bad, ["Count spaces, not tick marks.", f"There are {b} equal spaces, so A is at 1/{b}."],
                  qtype="error-analysis", tags={"misconception"}, diagram=Diagram("numline", nl(b, n=1), alt), r=r)


# ============================================================== S4 Fractions on a Number Line
@fam("012")
def na_point(r, L):
    b = pick(r, [3, 4, 6, 8])
    hi = pick(r, [1, 2]) if L < 2 else 2
    a = r.randint(2, b - 1) if L == 0 else r.randint(2, hi * b - 1)
    need(a % b)
    lab = pick(r, ["A", "B", "P", "M", "K"])
    alt = f"A number line from 0 to {hi}. Each whole is cut into {b} equal parts. Point {lab} is {a} parts from 0."
    return Item(f"What fraction is at point {lab}?", fr(a, b), [f"Each part is 1/{b}.", f"{lab} is {a} parts from 0, so it is at {a}/{b}."],
                [W(fr(a, b + 1), "counted the tick marks in a whole"), W(fr(a + 1, b), "counted the tick mark at 0"), W(fr(a, hi * b) if hi > 1 else fr(b - a, b) if b - a != a else fr(a, b - 1), "used the wrong whole or counted from 1")],
                EX(f"{a}/{b}"), qtype="visual", diagram=Diagram("numline", nl(b, hi=hi, n=a, label=lab), alt))


@fam("012")
def na_word(r, L):
    b = pick(r, [3, 4, 6, 8])
    a = r.randint(2, b - 1) if L < 2 else r.randint(b + 1, 2 * b - 1)
    t = pick(r, [("A path to the park is 1 mile long and is marked in {w}. {nm} walks {a} parts. How far does {nm} walk?", "mile"),
                 ("A board that is 1 meter long is marked in {w}. {nm} paints {a} parts from the left end. How much of the board is painted, in meters?", "meter"),
                 ("A swim lane is marked in {w} of a lap. {nm} swims {a} of those parts. How many laps is that? Write a fraction.", "lap")])
    q = t[0].format(w=DEN_WORD[b], a=a, nm=name(r))
    it = Item(q, f"{a}/{b} {t[1]}", [f"Each part is 1/{b}.", f"{a} parts is {a}/{b} {t[1]}."],
                [W(f"{a}/{b + 1} {t[1]}", "counted tick marks"), W(f"1/{b} {t[1]}", "gave one part"), W(f"{b}/{a} {t[1]}", "switched numerator and denominator")],
                EX(f"{a}/{b}", unit=t[1]), qtype="word-problem")
    it.consts = [b]   # the denominator is named in words ("fourths")
    return it


@fam("012")
def na_jumps(r, L):
    b = pick(r, [3, 4, 6, 8])
    hi = 1 if L == 0 else 2
    a = r.randint(2, hi * b - 1)
    need(a != b)
    alt = f"A number line from 0 to {hi}, each whole cut into {b} equal parts. {a} jumps of 1/{b} are drawn from 0."
    return Item(f"Each jump is 1/{b}. Where does the last jump end? Write a fraction.", fr(a, b),
                [f"Count the jumps: {a}.", f"{a} jumps of 1/{b} end at {a}/{b}."],
                [W(fr(1, b), "gave the size of one jump"), W(fr(a, b + 1), "counted tick marks"), W(fr(a - 1, b), "missed a jump")], EX(f"{a}/{b}"), qtype="visual",
                diagram=Diagram("numline", nl(b, hi=hi, jumps=a), alt))


@fam("012", mode="mc")
def na_which_letter(r, L):
    b = den(r, L)
    hi = 1 if L < 2 else 2
    spots = r.sample([k for k in range(1, hi * b) if k != b], 3) if hi * b - 1 >= 3 else None
    need(spots)
    target = spots[0]
    labels = ["A", "B", "C"]
    r.shuffle(labels)
    pts = [{"n": n, "label": l} for n, l in zip(spots, labels)]
    alt = f"A number line from 0 to {hi}, each whole cut into {b} equal parts, with points " + ", ".join(f"{p['label']} at {p['n']} {'part' if p['n'] == 1 else 'parts'} from 0" for p in sorted(pts, key=lambda p: p["label"])) + "."
    good = labels[0]
    it = mc_key(f"Which point is at {target}/{b}?", good, [l for l in ["A", "B", "C", "none of them"] if l != good],
                [f"Count {target} parts of 1/{b} from 0.", f"Point {good} is at {target}/{b}."], qtype="visual",
                diagram=Diagram("numline", {"den": b, "hi": hi, "labels": "wholes", "points": pts}, alt), r=r)
    it.check = FN("point_at", points=pts, n=target)
    return it


@fam("12")
def na_greater_one(r, L):
    b = pick(r, [2, 3, 4, 6])
    a = r.randint(b + 1, 2 * b - 1)
    alt = f"A number line from 0 to 2, each whole cut into {b} equal parts. Point A is {a} parts from 0, past 1."
    return Item("Point A is past 1. What fraction is at point A? Use the same denominator for the whole line.", fr(a, b),
                [f"Each part is 1/{b}. From 0 to 1 there are {b} parts.", f"A is {a} parts from 0: {a}/{b}."],
                [W(fr(a - b, b), "started counting again at 1"), W(fr(a, 2 * b), "used 0 to 2 as the whole"), W(fr(a + 1, b), "counted the tick mark at 0")],
                EX(f"{a}/{b}"), qtype="visual", diagram=Diagram("numline", nl(b, hi=2, n=a), alt))


@fam("12", mode="mc")
def na_mark_one(r, L):
    b = den(r, L)
    good = f"{b}/{b}"
    bad = [f"1/{b}", f"{b - 1}/{b}", f"{b + 1}/{b}"]
    it = mc_key(f"A number line from 0 to 2 is marked in {DEN_WORD[b]}. Which fraction names the tick mark at 1?", good, bad,
                [f"From 0 to 1 there are {b} parts of 1/{b}.", f"So 1 = {b}/{b}."], qtype="conceptual", r=r)
    it.check = EX(f"{b}/{b}")
    return it


@fam("2")
def na_distance(r, L):
    b = pick(r, [4, 6, 8])
    a1 = r.randint(1, b - 2)
    a2 = r.randint(a1 + 1, 2 * b - 1)
    return Item(f"On a number line marked in {DEN_WORD[b]}, how many jumps of 1/{b} are there from {a1}/{b} to {a2}/{b}?", a2 - a1,
                [f"Count the parts between the two points: {a2} − {a1}.", f"There are {a2 - a1} jumps of 1/{b}."],
                [W(a2 - a1 + 1, "counted tick marks instead of jumps"), W(a2, "counted from 0"), W(a1 + a2, "added")], FN("jumps_between", a1=a1, a2=a2), qtype="multi-step", tags={"reasoning"})


SKILLS = {
    1: dict(name="Unit Fractions and Equal Parts", fams=[ue_name, ue_equal, ue_word, ue_how_many, ue_name_word, ue_part_to_whole, ue_error]),
    2: dict(name="Fractions Made from Unit Fractions", fams=[ua_name, ua_copies, ua_word, ua_not_shaded, ua_more_than_one, ua_error]),
    3: dict(name="Unit Fractions on a Number Line", fams=[nu_point, nu_word, nu_which, nu_parts, nu_jump, nu_how_to, nu_two_wholes, nu_error]),
    4: dict(name="Fractions on a Number Line", fams=[na_point, na_word, na_jumps, na_which_letter, na_greater_one, na_mark_one, na_distance]),
}
