"""Unit 2: Understanding Division (division-meaning)."""
from g3lib import *

UNIT_ID = "division-meaning"
SHARE = [("{T} stickers are shared equally among {g} friends. How many stickers does each friend get?", "stickers"),
         ("{nm} puts {T} apples into {g} bags with the same number in each bag. How many apples are in each bag?", "apples"),
         ("{T} crayons are split equally into {g} boxes. How many crayons are in each box?", "crayons"),
         ("{g} friends share {T} grapes equally. How many grapes does each friend get?", "grapes"),
         ("{nm} plants {T} seeds in {g} equal rows. How many seeds are in each row?", "seeds")]
GROUP = [("{T} students make teams of {n}. How many teams are there?", "teams"),
         ("{nm} has {T} cookies. {nm} puts {n} cookies on each plate. How many plates does {nm} need?", "plates"),
         ("{T} eggs are packed in cartons of {n}. How many cartons are filled?", "cartons"),
         ("A coach has {T} balls. Each bag holds {n} balls. How many bags are filled?", "bags"),
         ("{T} chairs are set up in rows of {n}. How many rows are there?", "rows")]


def tg(r, L):
    """total, number of groups, size of each group"""
    if L == 0:
        g, n = r.randint(2, 5), r.randint(2, 5)
    elif L == 1:
        g, n = r.randint(3, 9), r.randint(3, 9)
    else:
        g, n = r.randint(4, 9), r.randint(6, 10)
    return g * n, g, n


def div_wrongs(T, d, q):
    return [W(T - d, "subtracted instead of dividing"), W(T * d if T * d < 1000 else T + d, "multiplied instead of dividing"),
            W(q + 1, "made a counting or fact error"), W(T + d, "added the numbers")]


# ============================================================== S1 Division as Equal Sharing
@fam("01")
def sh_pic(r, L):
    T, g, n = tg(r, L)
    alt = f"{T} dots shared equally into {g} circles. Each circle has {n} dots."
    return Item(f"{T} dots are shared equally into {g} groups. How many dots are in each group?", n,
                [f"Share the {T} dots one at a time into {g} groups.", f"Each group gets {n}, so {T} ÷ {g} = {n}."],
                [W(g, "gave the number of groups"), W(T - g, "subtracted instead of sharing"), W(n + 1, "shared unequally")],
                EX(f"{T}/{g}"), qtype="visual", diagram=Diagram("groups", {"groups": g, "each": n}, alt))


@fam("012")
def sh_word(r, L):
    T, g, n = tg(r, L)
    t, unit = pick(r, SHARE)
    return Item(t.format(T=T, g=g, nm=name(r)), f"{n} {unit}", [f"Share {T} into {g} equal groups.", f"{T} ÷ {g} = {n}, because {g} × {n} = {T}."],
                [W(f"{w[0]} {unit}", w[1]) for w in div_wrongs(T, g, n)], EX(f"{T}/{g}", unit=unit), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def sh_equation(r, L):
    T, g, n = tg(r, L)
    t, unit = pick(r, SHARE)
    good = f"{T} ÷ {g} = {n}"
    bad = [f"{T} − {g} = {T - g}", f"{T} ÷ {n} = {g + 1}", f"{g} × {T} = {g * T}"]
    return mc_key(t.format(T=T, g=g, nm=name(r)) + " Which equation shows the answer?", good, bad,
                  [f"The total {T} is shared into {g} groups.", f"{T} ÷ {g} = {n}."], qtype="word-problem", r=r)


@fam("012", mode="mc")
def sh_meaning(r, L):
    T, g, n = tg(r, L)
    good = f"the number of {pick(r, ['apples'])} in each bag"
    bad = ["the number of bags", "the total number of apples", "the number of apples left over"]
    return mc_key(f"{T} apples are shared equally into {g} bags. {T} ÷ {g} = {n}. What does {n} tell you?", good, bad,
                  [f"{T} is the total and {g} is the number of bags.", f"{n} is how many apples are in each bag."], qtype="conceptual", r=r)


@fam("012")
def sh_tape(r, L):
    T, g, n = tg(r, L)
    alt = f"A tape diagram with {g} equal parts, each labeled with a question mark. The total is labeled {T}."
    return Item(f"The tape diagram shows {T} split into {g} equal parts. What number belongs in each part?", n,
                [f"{g} equal parts make {T}.", f"{T} ÷ {g} = {n}, because {g} × {n} = {T}."],
                [W(g, "gave the number of parts"), W(T - g, "subtracted"), W(n + 1, "used a wrong fact")],
                EX(f"{T}/{g}"), qtype="visual", diagram=Diagram("tape", {"parts": g, "each": "?", "total_label": str(T)}, alt))


@fam("2")
def sh_compare(r, L):
    T = pick(r, [12, 18, 24, 30, 36, 48, 60])
    gs = [d for d in range(2, 11) if T % d == 0 and T // d <= 10]
    need(len(gs) >= 2)
    a, b = sorted(r.sample(gs, 2))
    return Item(f"{T} cards are shared equally among {a} friends. Another {T} cards are shared equally among {b} friends. "
                f"How many more cards does each friend get in the first group?", f"{T // a - T // b} cards",
                [f"{T} ÷ {a} = {T // a} and {T} ÷ {b} = {T // b}.", f"{T // a} − {T // b} = {T // a - T // b} cards."],
                [W(f"{b - a} cards", "subtracted the numbers of friends"), W(f"{T // a} cards", "stopped after one division"), W(f"{T // a + T // b} cards", "added the shares")],
                EX(f"{T}/{a}-{T}/{b}", unit="cards"), qtype="multi-step", tags={"multistep", "reasoning"})


@fam("2", mode="mc")
def sh_fair(r, L):
    g, n = r.randint(3, 5), r.randint(4, 8)
    shares = [n] * g
    i = r.randrange(g)
    shares[i] -= 1
    j = (i + 1) % g
    shares[j] += 1
    T = g * n
    good = f"No. Each friend should get {n}."
    bad = [f"Yes. The {T} crackers were all given out.", f"No. Each friend should get {n + 1}.", f"Yes. Each friend got about the same."]
    return mc_key(f"{name(r)} shares {T} crackers among {g} friends like this: {', '.join(map(str, shares))}. Is this equal sharing?", good, bad,
                  ["Equal sharing means every group gets the same number.", f"{T} ÷ {g} = {n}, so each friend should get {n}."], qtype="explain", tags={"reasoning"}, r=r)


# ============================================================== S2 Division as Equal Grouping
@fam("012")
def gr_word(r, L):
    T, g, n = tg(r, L)
    t, unit = pick(r, GROUP)
    return Item(t.format(T=T, n=n, nm=name(r)), f"{g} {unit}", [f"Make groups of {n} from {T}.", f"{T} ÷ {n} = {g}, because {g} × {n} = {T}."],
                [W(f"{w[0]} {unit}", w[1]) for w in div_wrongs(T, n, g)], EX(f"{T}/{n}", unit=unit), qtype="word-problem", tags={"modeling"})


@fam("01")
def gr_pic(r, L):
    T, g, n = tg(r, L)
    need(g <= 8)
    alt = f"{T} dots put into circles of {n}. There are {g} circles."
    return Item(f"{T} dots are put into groups of {n}. How many groups are there?", g,
                [f"Count the groups of {n}.", f"There are {g} groups, so {T} ÷ {n} = {g}."],
                [W(n, "gave the size of each group"), W(T - n, "subtracted once instead of dividing"), W(g + 1, "counted an extra group")],
                EX(f"{T}/{n}"), qtype="visual", diagram=Diagram("groups", {"groups": g, "each": n}, alt))


@fam("012", mode="mc")
def gr_meaning(r, L):
    T, g, n = tg(r, L)
    good = "the number of boxes"
    bad = ["the number of pencils in each box", "the total number of pencils", "the number of pencils left over"]
    return mc_key(f"{T} pencils are packed in boxes of {n}. {T} ÷ {n} = {g}. What does {g} tell you?", good, bad,
                  [f"{T} is the total and {n} is how many go in each box.", f"{g} is how many boxes are filled."], qtype="conceptual", r=r)


@fam("012")
def gr_repeated_sub(r, L):
    T, g, n = tg(r, L)
    need(g <= 6)
    s = f"{T}" + "".join(f" − {n}" for _ in range(g)) + " = 0"
    return Item(f"{name(r)} writes {s}. How many groups of {n} are in {T}?", g,
                [f"Count how many times {n} is subtracted.", f"{n} is subtracted {g} times, so {T} ÷ {n} = {g}."],
                [W(n, "gave the size of each group"), W(g + 1, "counted the total as a group"), W(T - n, "subtracted only once")],
                FN("repsub_groups", expr=s), qtype="fill-blank", tags={"connections"})


@fam("12", mode="mc")
def gr_which_kind(r, L):
    T, g, n = tg(r, L)
    if r.random() < 0.5:
        t, unit = pick(r, GROUP)
        story = t.format(T=T, n=n, nm=name(r))
        good, bad = "the number of groups", ["the number in each group", "the total", "the number left over"]
    else:
        t, unit = pick(r, SHARE)
        story = t.format(T=T, g=g, nm=name(r))
        good, bad = "the number in each group", ["the number of groups", "the total", "the number left over"]
    return mc_key(f"{story} What is the unknown in this story?", good, bad,
                  ["Find which number the story gives and which it asks for.", f"The story asks for {good}."], qtype="conceptual", tags={"reasoning"}, r=r)


@fam("2")
def gr_two_sizes(r, L):
    T = pick(r, [24, 30, 36, 40, 48, 60])
    ds = [d for d in range(2, 11) if T % d == 0 and T // d <= 10]
    need(len(ds) >= 2)
    a, b = sorted(r.sample(ds, 2))
    return Item(f"{name(r)} has {T} beads. Strings of {a} beads or strings of {b} beads can be made. How many more strings can be made with {a} beads on each string?",
                f"{T // a - T // b} strings", [f"{T} ÷ {a} = {T // a} strings and {T} ÷ {b} = {T // b} strings.", f"{T // a} − {T // b} = {T // a - T // b} strings."],
                [W(f"{b - a} strings", "subtracted the string sizes"), W(f"{T // a} strings", "stopped after one division"), W(f"{T // a + T // b} strings", "added the numbers of strings")],
                EX(f"{T}/{a}-{T}/{b}", unit="strings"), qtype="multi-step", tags={"multistep"})


@fam("2", mode="mc")
def gr_same_numbers(r, L):
    T, g, n = tg(r, L)
    need(g != n)
    good = f"In story A, {g} is the number in each group. In story B, {g} is the number of groups."
    bad = [f"{g} means the same thing in both stories.", f"In both stories, {g} is the total.", f"In story A, {g} is the number of groups. In story B, {g} is the number in each group."]
    return mc_key(f"Story A: {T} toys are shared equally by {n} kids. Story B: {T} toys are put in boxes of {n}. Both answers are {g}. Which is true?",
                  good, bad, [f"Story A shares into {n} groups, so {g} is how many each kid gets.", f"Story B makes groups of {n}, so {g} is how many boxes."],
                  qtype="compare-strategies", tags={"reasoning"}, r=r)


# ============================================================== S3 Division as an Unknown Factor
def fact(r, L):
    if L == 0:
        a, b = pick(r, [2, 5, 10]), r.randint(2, 9)
    elif L == 1:
        a, b = r.randint(2, 9), r.randint(2, 9)
    else:
        a, b = r.randint(6, 9), r.randint(6, 10)
    return a, b


@fam("012")
def uf_related(r, L):
    a, b = fact(r, L)
    return Item(f"Use {a} × {b} = {a * b} to find {a * b} ÷ {b}.", a, [f"{a * b} ÷ {b} asks: {b} times what number is {a * b}?", f"{a} × {b} = {a * b}, so {a * b} ÷ {b} = {a}."],
                [W(b, "gave the divisor"), W(a * b, "gave the product"), W(a + 1, "used a nearby fact")], EX(f"{a * b}/{b}"), qtype="procedural", tags={"connections"},
                claim=f"{a * b} ÷ {b}")


@fam("012")
def uf_missing(r, L):
    a, b = fact(r, L)
    return Item(f"To find {a * b} ÷ {a}, think {a} × ___ = {a * b}. What number goes in the blank?", b,
                [f"Find the missing factor: {a} × {b} = {a * b}.", f"So {a * b} ÷ {a} = {b}."],
                [W(a, "repeated the known factor"), W(a * b - a, "subtracted instead"), W(b + 1, "used a nearby fact")], EX(f"{a * b}/{a}"), qtype="fill-blank")


@fam("012")
def uf_fact(r, L):
    a, b = fact(r, L)
    return Item(f"Divide: {a * b} ÷ {a}", b, [f"Think: {a} × ? = {a * b}.", f"{a} × {b} = {a * b}, so {a * b} ÷ {a} = {b}."],
                [W(a * b - a, "subtracted instead of dividing"), W(b + 1, "used a nearby fact"), W(b - 1, "used a nearby fact"), W(a, "gave the divisor")],
                EX(f"{a * b}/{a}"), qtype="procedural", claim=f"{a * b} ÷ {a}")


@fam("012", mode="mc")
def uf_family(r, L):
    a, b = fact(r, L)
    need(a != b)
    P = a * b
    good = f"{a} ÷ {P} = {b}"
    bad = [f"{a} × {b} = {P}", f"{P} ÷ {a} = {b}", f"{b} × {a} = {P}"]
    it = mc_key(f"Which equation is NOT in the fact family for {a}, {b}, and {P}?", good, bad,
                  [f"The product {P} comes first in a division equation.", f"{good} is not true."], qtype="conceptual", tags={"reasoning"}, r=r)
    it.check = FN("false_eq")
    return it


@fam("12", mode="mc")
def uf_which_mult(r, L):
    a, b = fact(r, L)
    need(a != b)
    P = a * b
    good = f"{b} × {a} = {P}"
    bad = [f"{b} × {P} = {a * P}" if a * P < 1000 else f"{b} + {a} = {a + b}", f"{P} × {a} = {P * a}" if P * a < 1000 else f"{P} − {a} = {P - a}", f"{b} + {P} = {b + P}"]
    return mc_key(f"Which multiplication fact helps you find {P} ÷ {b}?", good, bad,
                  [f"{P} ÷ {b} asks for the factor that goes with {b} to make {P}.", f"{b} × {a} = {P}, so {P} ÷ {b} = {a}."], qtype="conceptual", tags={"connections"}, r=r)


@fam("2")
def uf_two_unknowns(r, L):
    a, b = fact(r, L)
    need(a != b)
    P = a * b
    return Item(f"{a} × □ = {P} and {P} ÷ □ = △. What number is △?", a,
                [f"First, {a} × {b} = {P}, so □ = {b}.", f"Then {P} ÷ {b} = {a}, so △ = {a}."],
                [W(b, "gave □ instead of △"), W(P, "gave the product"), W(a + b, "added the factors")], EX(f"{P}/({P}/{a})"), qtype="multi-step", tags={"multistep", "reasoning"})


# ============================================================== S4 Division Word Problems
@fam("012")
def dw_share(r, L):
    T, g, n = tg(r, L)
    t = pick(r, [("A ribbon {T} inches long is cut into {g} equal pieces. How long is each piece?", "inches"),
                 ("{T} liters of water fill {g} tanks equally. How many liters go in each tank?", "liters"),
                 ("{nm} earns {T} dollars in {g} weeks, the same amount each week. How many dollars does {nm} earn each week?", "dollars")] + SHARE)
    return Item(t[0].format(T=T, g=g, nm=name(r)), f"{n} {t[1]}", [f"The total is {T}. There are {g} equal parts.", f"{T} ÷ {g} = {n} {t[1]}."],
                [W(f"{w[0]} {t[1]}", w[1]) for w in div_wrongs(T, g, n)], EX(f"{T}/{g}", unit=t[1]), qtype="word-problem", tags={"modeling"})


@fam("012")
def dw_group(r, L):
    T, g, n = tg(r, L)
    t = pick(r, [("A ribbon is {T} feet long. {nm} cuts pieces that are {n} feet long. How many pieces can {nm} cut?", "pieces")] + GROUP)
    return Item(t[0].format(T=T, n=n, nm=name(r)), f"{g} {t[1]}", [f"Make groups of {n} from {T}.", f"{T} ÷ {n} = {g} {t[1]}."],
                [W(f"{w[0]} {t[1]}", w[1]) for w in div_wrongs(T, n, g)], EX(f"{T}/{n}", unit=t[1]), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def dw_equation(r, L):
    T, g, n = tg(r, L)
    t, unit = pick(r, SHARE)
    good = f"{T} ÷ {g} = n"
    bad = [f"{T} × {g} = n", f"{T} − {g} = n", f"{g} ÷ {T} = n"]
    return mc_key(t.format(T=T, g=g, nm=name(r)) + " Which equation can you use to find n, the answer?", good, bad,
                  [f"The total {T} is split into {g} equal groups.", f"{T} ÷ {g} = n, and n = {n}."], qtype="word-problem", r=r)


@fam("12", mode="mc")
def dw_choose_op(r, L):
    T, g, n = tg(r, L)
    if r.random() < 0.5:
        q = f"{name(r)} has {g} boxes with {n} markers in each box. How many markers are there?"
        good, why = f"{g} × {n} = {T}", "The total is unknown, so multiply."
        bad = [f"{T} ÷ {g} = {n}", f"{g} + {n} = {g + n}", f"{n} − {g} = {n - g}" if n > g else f"{g} − {n} = {g - n}"]
    else:
        q = f"{name(r)} has {T} markers. {name(sub(r, 1))} puts them in {g} boxes equally. How many markers are in each box?"
        good, why = f"{T} ÷ {g} = {n}", "The total is known and the number in each box is unknown, so divide."
        bad = [f"{g} × {T} = {g * T}", f"{T} − {g} = {T - g}", f"{T} + {g} = {T + g}"]
    need(len(set(bad + [good])) == 4)
    return mc_key(q + " Which equation solves the problem?", good, bad, ["Decide what is known and what is unknown.", why], qtype="explain", tags={"reasoning"}, r=r)


@fam("2")
def dw_two_step(r, L):
    g, n = r.randint(3, 6), r.randint(3, 8)
    extra = r.randint(2, 9)
    T = g * n
    return Item(f"{name(r)} had {T + extra} stickers and gave away {extra}. Then the rest were shared equally into {g} albums. How many stickers are in each album?",
                f"{n} stickers", [f"{T + extra} − {extra} = {T} stickers are left.", f"{T} ÷ {g} = {n} stickers in each album."],
                [W(f"{(T + extra) // g if (T + extra) % g == 0 and (T + extra) // g != n else T} stickers", "forgot to take away the stickers given away"),
                 W(f"{T} stickers", "stopped after the first step"), W(f"{n + extra} stickers", "added the extra stickers after dividing")],
                EX(f"({T + extra}-{extra})/{g}", unit="stickers"), qtype="multi-step", tags={"multistep"})


@fam("2")
def dw_measure(r, L):
    n = r.randint(3, 9)
    g = r.randint(4, 10)
    T = g * n
    return Item(f"A water jug holds {T} liters. A pail holds {n} liters. How many pails of water does it take to fill the jug?",
                f"{g} pails", [f"How many groups of {n} liters make {T} liters?", f"{T} ÷ {n} = {g} pails."],
                [W(f"{T - n} pails", "subtracted instead of dividing"), W(f"{T * n} pails" if T * n < 1000 else f"{T + n} pails", "multiplied instead of dividing"), W(f"{g + 1} pails", "used a nearby fact")],
                EX(f"{T}/{n}", unit="pails"), qtype="word-problem", tags={"modeling"})


SKILLS = {
    1: dict(name="Division as Equal Sharing", fams=[sh_pic, sh_word, sh_equation, sh_meaning, sh_tape, sh_compare, sh_fair]),
    2: dict(name="Division as Equal Grouping", fams=[gr_word, gr_pic, gr_meaning, gr_repeated_sub, gr_which_kind, gr_two_sizes, gr_same_numbers]),
    3: dict(name="Division as an Unknown Factor", fams=[uf_related, uf_missing, uf_fact, uf_family, uf_which_mult, uf_two_unknowns]),
    4: dict(name="Division Word Problems", fams=[dw_share, dw_group, dw_equation, dw_choose_op, dw_two_step, dw_measure]),
}
