"""Unit 11: Organizing and Reading Data (data). 1.MD.C.4. Up to three categories."""
from g1lib import *

UNIT_ID = "data"

SETS = [("Favorite Fruit", ["Apple", "Banana", "Grape"], "children"), ("Our Pets", ["Dogs", "Cats", "Fish"], "pets"),
        ("Weather This Month", ["Sunny", "Rainy", "Cloudy"], "days"), ("Favorite Color", ["Red", "Blue", "Green"], "children"),
        ("Favorite Snack", ["Popcorn", "Pretzels", "Apples"], "children"), ("Recess Games", ["Soccer", "Tag", "Swings"], "children"),
        ("Shapes in a Bag", ["Circles", "Squares", "Triangles"], "shapes"), ("Lunch Choice", ["Pizza", "Tacos", "Soup"], "children"),
        ("Bugs We Saw", ["Ants", "Bees", "Ladybugs"], "bugs"), ("Favorite Season", ["Spring", "Summer", "Winter"], "children")]


def data(r, L, k=3):
    title, cats, unit = pick(r, SETS)
    cats = cats[:k]
    lo, hi = (1, 8) if L == 0 else (3, 14) if L == 1 else (6, 19)
    counts = [r.randint(lo, hi) for _ in cats]
    need(len(set(counts)) == len(counts))
    return title, cats, unit, counts


def view(r, L, title, cats, counts, unit, kinds=("picgraph", "tally", "table")):
    kind = pick(r, list(kinds))
    desc = ", ".join(f"{c} {n}" for c, n in zip(cats, counts))
    if kind == "picgraph":
        return "picture graph", Diagram("picgraph", {"title": title, "cats": cats, "symbols": counts, "key": 1, "icon": "star", "unit": ""},
                                        f"Picture graph titled {title}. Each star stands for 1. {desc}.")
    if kind == "tally":
        return "tally chart", Diagram("tally", {"title": title, "cats": cats, "counts": counts}, f"Tally chart titled {title}. {desc}.")
    return "table", Diagram("table", {"header": [title, "Number"], "rows": [[c, n] for c, n in zip(cats, counts)]},
                            f"Table titled {title}. {desc}.")


def how_many(unit, c):
    if unit == "children":
        return f"How many children chose {c}?"
    if unit == "days":
        return f"How many days were {c.lower()}?"
    return f"How many {c.lower()} are there?"


def how_more(unit, a, b, word):
    if unit == "children":
        return f"How many {word} children chose {a if word == 'more' else b} than {b if word == 'more' else a}?"
    if unit == "days":
        x, y = (a, b) if word == "more" else (b, a)
        return f"How many {word} {x.lower()} days than {y.lower()} days were there?"
    x, y = (a, b) if word == "more" else (b, a)
    return f"How many {word} {x.lower()} than {y.lower()} are there?"


def more_sent(unit, a, b, d):
    if unit == "children":
        return f"{a} has {d} more {'vote' if d == 1 else 'votes'} than {b}."
    if unit == "days":
        return f"There {'was' if d == 1 else 'were'} {d} more {a.lower()} {'day' if d == 1 else 'days'} than {b.lower()} days."
    return f"There {'is' if d == 1 else 'are'} {d} more {a.lower()} than {b.lower()}."


def need_q(unit, a, b):
    if unit == "children":
        return f"How many more votes does {b} need to have as many votes as {a}?"
    if unit == "days":
        return f"How many more {b.lower()} days would make as many {b.lower()} days as {a.lower()} days?"
    return f"How many more {b.lower()} would make as many {b.lower()} as {a.lower()}?"


def cw(ans, counts, extra=()):
    out = [W(x, y) for x, y in extra]
    out += [W(ans + 1, "counted one too many"), W(ans - 1 if ans > 1 else ans + 2, "counted one too few")]
    out += [W(c, "read a different category") for c in counts if c != ans][:2]
    return out


# ============================================================== S1 Sorting and Tally Marks
@fam("012")
def s_sort(r, L):
    kinds = pick(r, [["circle", "square", "triangle"], ["red", "blue", "green"], ["big", "small", "medium"]][:2 if L == 0 else 3])
    k = 2 if L == 0 else 3
    n = r.randint(5, 8) if L == 0 else r.randint(8, 12) if L == 1 else r.randint(12, 16)
    seq = [pick(r, kinds[:k]) for _ in range(n)]
    want = pick(r, kinds[:k])
    cnt = seq.count(want)
    need(cnt >= 1 and len(set(seq)) == k)
    noun = "shapes" if kinds[0] == "circle" else "blocks"
    word = f"{want}s" if noun == "shapes" else f"{want} blocks"
    singular_word = want if noun == "shapes" else f"{want} block"
    return Item(f"Sort the {noun}: {', '.join(seq)}. How many {word} are there?", cnt,
                [f"Make a group for each kind and count the {word}.", f"There {'is' if cnt == 1 else 'are'} {cnt} {singular_word if cnt == 1 else word}."],
                [W(n, "counted all the objects"), W(n - cnt, "counted the other groups"), W(cnt + 1, "counted one twice"), W(cnt - 1 if cnt > 1 else cnt + 2, "missed one")],
                FN("list_count", items=seq, want=want), qtype="procedural")


@fam("012")
def s_tally_count(r, L):
    n = r.randint(3, 9) if L == 0 else r.randint(8, 15) if L == 1 else r.randint(13, 20)
    cat = pick(r, ["Dogs", "Cats", "Votes", "Birds", "Cars"])
    alt = f"Tally chart with one row, {cat}, showing {n} tally marks in bundles of five."
    return Item(pick(r, [f"How many {cat.lower()} do the tally marks show?", f"Count the tally marks for {cat}. What number do they show?"]), n,
                ["A bundle of 4 marks crossed by a slash is 5. Count by fives, then count on by ones.", f"The tally marks show {n}."],
                [W(n // 5 + n % 5, "counted each bundle as 1"), W(n - 1 if n % 5 else n + 1, "made a counting mistake"), W(n + 5, "counted a bundle twice"), W(n + 1, "counted one too many")],
                FN("data_q", counts={cat: n}, q="value", a=cat), qtype="visual", diagram=Diagram("tally", {"title": "", "cats": [cat], "counts": [n]}, alt))


@fam("012", mode="mc")
def s_bundle(r, L):
    n = r.randint(6, 9) if L == 0 else r.randint(10, 14) if L == 1 else r.randint(15, 20)
    b, o = divmod(n, 5)
    def say(bb, oo):
        s = f"{bb} bundle{'s' if bb != 1 else ''} of 5"
        return s + (f" and {oo} more mark{'s' if oo != 1 else ''}" if oo else "")
    good = say(b, o)
    bad = [say(b + 1, o) if o else say(b, 1), say(max(b - 1, 1), o + 1 if o < 4 else 0) if b > 1 else say(b, o + 1 if o < 4 else 2), f"{n} bundles of 5"]
    need(len({good, *bad}) == 4)
    it = mc_key(f"How do you show {n} with tally marks?", good, bad, ["Each bundle is 5 marks.", f"{n} = {' + '.join(['5'] * b + ([str(o)] if o else []))}, so {good}."], qtype="procedural", r=r)
    it.check = FN("tally_say", n=n)
    return it


@fam("012", mode="mc")
def s_where(r, L):
    groups = pick(r, [(["Fly", "Swim", "Walk"], {"duck": None, "fish": "Swim", "bird": "Fly", "dog": "Walk", "whale": "Swim", "cat": "Walk", "bee": "Fly", "horse": "Walk", "shark": "Swim", "owl": "Fly"}),
                      (["Fruit", "Toy", "Clothes"], {"apple": "Fruit", "ball": "Toy", "sock": "Clothes", "pear": "Fruit", "doll": "Toy", "hat": "Clothes", "grape": "Fruit", "kite": "Toy", "shirt": "Clothes"}),
                      (["Has wheels", "Has wings", "Has legs"], {"bike": "Has wheels", "car": "Has wheels", "plane": "Has wings", "bird": "Has wings", "dog": "Has legs", "table": "Has legs", "bus": "Has wheels", "bee": "Has wings"})])
    cats, table = groups
    items = [k for k, v in table.items() if v]
    it = pick(r, items)
    good = table[it]
    bad = [c for c in cats if c != good] + ["Not any of the groups"]
    nm = name(r)
    return mc_key(f"{nm} sorts things into three groups: {', '.join(cats)}. Which group does {art(it)} go in?", good, bad, [f"Think about the {it}.", f"{Art(it)} goes in {good}."],
                  qtype="conceptual", r=r)


@fam("12")
def s_two_groups(r, L):
    n = r.randint(8, 15) if L == 1 else r.randint(12, 20)
    a = r.randint(3, n - 3)
    nm = name(r)
    th = pick(r, [("button", "buttons"), ("block", "blocks"), ("shell", "shells"), ("bead", "beads")])
    g1, g2 = pick(r, [("big", "small"), ("red", "blue"), ("round", "square")])
    return Item(f"{nm} sorts {n} {th[1]} into two groups, {g1} and {g2}. There are {a} {g1} {th[1]}. How many {g2} {th[1]} are there?", f"{n - a} {th[1]}",
                [f"The two groups make {n}.", f"{a} + {n - a} = {n}, so there are {n - a} {g2} {th[1]}."],
                [W(f"{n + a} {th[1]}", "added the numbers"), W(f"{a} {th[1]}", "gave the other group"), W(f"{n} {th[1]}", "gave the total"), W(f"{n - a + 1} {th[1]}", "counted one too many")],
                EX(f"{n}-{a}", unit=th[1]), qtype="word-problem", tags={"modeling"})


@fam("0")
def s_tally_small(r, L):
    a, b = r.randint(2, 6), r.randint(2, 6)
    need(a != b)
    cats = pick(r, [["Red", "Blue"], ["Yes", "No"], ["Boys", "Girls"], ["Cats", "Dogs"]])
    want = pick(r, cats)
    n = a if want == cats[0] else b
    alt = f"Tally chart: {cats[0]} {a}, {cats[1]} {b}."
    return Item(f"How many tally marks are next to {want}?", n, [f"Find the row for {want} and count the marks.", f"There are {n}."],
                cw(n, [a, b]), FN("data_q", counts={cats[0]: a, cats[1]: b}, q="value", a=want), qtype="visual",
                diagram=Diagram("tally", {"title": "Votes", "cats": cats, "counts": [a, b]}, alt))


# ============================================================== S2 Reading Picture Graphs and Tables
@fam("012")
def g_value(r, L):
    title, cats, unit, counts = data(r, L)
    kind, dg = view(r, L, title, cats, counts, unit)
    i = r.randrange(3)
    return Item(pick(r, [f"Look at the {kind}. {how_many(unit, cats[i])}", f"The {kind} shows {title.lower()}. What number goes with {cats[i]}?"]), counts[i],
                [f"Find the {cats[i]} row.", f"{cats[i]} has {counts[i]}."], cw(counts[i], counts),
                FN("data_q", counts=dict(zip(cats, counts)), q="value", a=cats[i]), qtype="visual", diagram=dg)


@fam("012", mode="mc")
def g_value_mc(r, L):
    title, cats, unit, counts = data(r, L)
    kind, dg = view(r, L, title, cats, counts, unit)
    i = r.randrange(3)
    return Item(f"Use the {kind}. {how_many(unit, cats[i])}", counts[i], [f"Read the {cats[i]} row.", f"It shows {counts[i]}."], cw(counts[i], counts),
                FN("data_q", counts=dict(zip(cats, counts)), q="value", a=cats[i]), qtype="visual", diagram=dg)


@fam("012")
def g_most(r, L):
    title, cats, unit, counts = data(r, L)
    kind, dg = view(r, L, title, cats, counts, unit)
    q = pick(r, ["most", "least"])
    g = cats[counts.index(max(counts) if q == "most" else min(counts))]
    word = "the most" if q == "most" else "the fewest"
    return Item(f"Look at the {kind}. Which has {word}?", g, [f"Compare the three numbers: {', '.join(map(str, counts))}.", f"{g} has {word}."],
                [W(c, "chose the wrong category") for c in cats if c != g], FN("data_q", counts=dict(zip(cats, counts)), q=q), qtype="visual", mode="sa", diagram=dg)


@fam("012", mode="mc")
def g_most_mc(r, L):
    title, cats, unit, counts = data(r, L)
    kind, dg = view(r, L, title, cats, counts, unit)
    q = pick(r, ["most", "least"])
    g = cats[counts.index(max(counts) if q == "most" else min(counts))]
    bad = [c for c in cats if c != g] + ["They are all the same"]
    it = mc_key(f"Use the {kind}. Which has the {'most' if q == 'most' else 'fewest'}?", g, bad, ["Compare the numbers.", f"{g} has the {'most' if q == 'most' else 'fewest'}."],
                qtype="visual", diagram=dg, r=r)
    it.check = FN("data_q", counts=dict(zip(cats, counts)), q=q)
    return it


@fam("012")
def g_text(r, L):
    title, cats, unit, counts = data(r, L)
    i = r.randrange(3)
    o = counts[i] % 5
    p = f"In a tally chart, the row for {cats[i]} has {counts[i] // 5} bundle{'s' if counts[i] // 5 != 1 else ''} of 5" + (f" and {o} more mark{'s' if o != 1 else ''}" if o else "") + ". What number is that?"
    need(counts[i] >= 5)
    return Item(p, counts[i], ["Count each bundle as 5, then add the extra marks.", f"{' + '.join(['5'] * (counts[i] // 5))} + {counts[i] % 5} = {counts[i]}."],
                [W(counts[i] // 5 + counts[i] % 5, "counted each bundle as 1"), W(counts[i] + 1, "counted one too many"), W(counts[i] + 5, "counted a bundle twice"), W(counts[i] - 1, "counted one too few")],
                FN("tally_parts", b=counts[i] // 5, o=counts[i] % 5), qtype="procedural")


# ============================================================== S3 Answering Questions about Data
@fam("012")
def q_total(r, L):
    title, cats, unit, counts = data(r, L)
    kind, dg = view(r, L, title, cats, counts, unit)
    need(sum(counts) <= (20 if L == 0 else 40 if L == 1 else 50))
    return Item(pick(r, [f"How many {unit} are shown in the {kind} in all?", f"Use the {kind}. What is the total number of {unit}?"]), sum(counts),
                [f"Add all three: {counts[0]} + {counts[1]} + {counts[2]}.", f"The total is {sum(counts)}."],
                [W(counts[0] + counts[1], "left out a category"), W(counts[1] + counts[2], "left out a category"), W(sum(counts) + 1, "counted one too many"), W(max(counts), "gave only the biggest")],
                FN("data_q", counts=dict(zip(cats, counts)), q="total"), qtype="visual", diagram=dg)


@fam("012")
def q_diff(r, L):
    title, cats, unit, counts = data(r, L)
    kind, dg = view(r, L, title, cats, counts, unit)
    i, j = r.sample(range(3), 2)
    if counts[i] < counts[j]:
        i, j = j, i
    word = pick(r, ["more", "fewer"])
    p = f"Use the {kind}. {how_more(unit, cats[i], cats[j], word)}"
    d = counts[i] - counts[j]
    return Item(p, d, [f"{cats[i]}: {counts[i]}. {cats[j]}: {counts[j]}.", f"{counts[i]} − {counts[j]} = {d}."],
                [W(counts[i] + counts[j], "added instead of comparing"), W(counts[i], "gave one category"), W(d + 1, "counted one too many"), W(counts[j], "gave the other category")],
                FN("data_q", counts=dict(zip(cats, counts)), q="diff", a=cats[i], b=cats[j]), qtype="visual", tags={"graph"}, diagram=dg)


@fam("012")
def q_two(r, L):
    title, cats, unit, counts = data(r, L)
    kind, dg = view(r, L, title, cats, counts, unit)
    i, j = r.sample(range(3), 2)
    return Item(f"Use the {kind}. How many are {cats[i]} or {cats[j]}? Add them.", counts[i] + counts[j],
                [f"{cats[i]}: {counts[i]}. {cats[j]}: {counts[j]}.", f"{counts[i]} + {counts[j]} = {counts[i] + counts[j]}."],
                [W(abs(counts[i] - counts[j]), "subtracted instead of adding"), W(sum(counts), "added all three"), W(counts[i] + counts[j] + 1, "counted one too many"), W(counts[i], "used only one category")],
                FN("data_q", counts=dict(zip(cats, counts)), q="sum", a=cats[i], b=cats[j]), qtype="visual", tags={"graph"}, diagram=dg)


@fam("012", mode="mc")
def q_claim(r, L):
    title, cats, unit, counts = data(r, L)
    kind, dg = view(r, L, title, cats, counts, unit)
    i, j = r.sample(range(3), 2)
    if counts[i] < counts[j]:
        i, j = j, i
    d = counts[i] - counts[j]
    good = more_sent(unit, cats[i], cats[j], d)
    bad = [more_sent(unit, cats[j], cats[i], d), more_sent(unit, cats[i], cats[j], d + 1), f"{cats[i]} and {cats[j]} have the same number."]
    it = mc_key(f"Use the {kind}. Which sentence is true?", good, bad, [f"{cats[i]}: {counts[i]}. {cats[j]}: {counts[j]}.", good], qtype="visual", tags={"graph", "reasoning"}, diagram=dg, r=r)
    return it


@fam("12")
def q_same(r, L):
    title, cats, unit, counts = data(r, L)
    kind, dg = view(r, L, title, cats, counts, unit)
    i, j = r.sample(range(3), 2)
    if counts[i] < counts[j]:
        i, j = j, i
    d = counts[i] - counts[j]
    return Item(f"Use the {kind}. {need_q(unit, cats[i], cats[j])}", d,
                [f"{cats[j]} has {counts[j]} and {cats[i]} has {counts[i]}.", f"{counts[j]} + {d} = {counts[i]}."],
                [W(counts[i] + counts[j], "added the two numbers"), W(counts[i], "gave the bigger number"), W(d + 1, "counted one too many"), W(counts[j], "gave the smaller number")],
                FN("data_q", counts=dict(zip(cats, counts)), q="diff", a=cats[i], b=cats[j]), qtype="visual", tags={"graph", "reasoning"}, diagram=dg)


@fam("012")
def q_text(r, L):
    title, cats, unit, counts = data(r, L)
    i, j = r.sample(range(3), 2)
    if counts[i] < counts[j]:
        i, j = j, i
    d = counts[i] - counts[j]
    lst = ", ".join(f"{c}: {n}" for c, n in zip(cats, counts))
    return Item(f"A class made a table of {title.lower()}. {lst}. {how_more(unit, cats[i], cats[j], 'more')}", d,
                [f"Compare {counts[i]} and {counts[j]}.", f"{counts[i]} − {counts[j]} = {d}."],
                [W(counts[i] + counts[j], "added instead of comparing"), W(counts[i], "gave one category"), W(d + 1, "counted one too many"), W(sum(counts), "added all three")],
                FN("data_q", counts=dict(zip(cats, counts)), q="diff", a=cats[i], b=cats[j]), qtype="procedural", tags={"graph"})


SKILLS = {
    1: dict(name="Sorting and Tally Marks", fams=[s_sort, s_tally_count, s_bundle, s_where, s_two_groups, s_tally_small]),
    2: dict(name="Reading Picture Graphs and Tables", fams=[g_value, g_value_mc, g_most, g_most_mc, g_text]),
    3: dict(name="Answering Questions about Data", fams=[q_total, q_diff, q_two, q_claim, q_same, q_text]),
}
