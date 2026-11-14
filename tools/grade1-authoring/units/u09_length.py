"""Unit 9: Measuring Length (measuring-length). 1.MD.A.1, 1.MD.A.2."""
from g1lib import *

UNIT_ID = "measuring-length"

OBJ = ["Pencil", "Crayon", "Ribbon", "Rope", "Straw", "Marker", "Stick", "Brush", "Spoon", "Ruler", "Yarn", "Snake"]
COL = ["blue", "orange", "green", "pink", "purple", "yellow"]


def objs(r, k, L, aligned=True):
    names = r.sample(OBJ, k)
    lens = r.sample(range(3, 13), k)
    if L == 0 and k == 2:
        need(abs(lens[0] - lens[1]) >= 3)
    if L >= 1 and k == 3:
        need(min(abs(a - b) for i, a in enumerate(lens) for b in lens[i + 1:]) <= (2 if L == 1 else 1))
    items = [{"label": n, "len": l, "color": COL[i % 6]} for i, (n, l) in enumerate(zip(names, lens))]
    if not aligned:
        for it in items:
            it["start"] = r.randint(0, 3)
    return items, dict(zip(names, lens))


# ============================================================== S1 Comparing and Ordering Lengths
@fam("012")
def lo_extreme(r, L):
    items, lens = objs(r, 2 if L == 0 else 3, L)
    want = pick(r, ["longest", "shortest"]) if L else pick(r, ["longer", "shorter"])
    w2 = "longest" if want in ("longest", "longer") else "shortest"
    g = (max if w2 == "longest" else min)(lens, key=lens.get)
    alt = "Objects lined up at the left: " + ", ".join(f"{k} {v} units long" for k, v in lens.items()) + "."
    o = [k for k in lens if k != g]
    return Item(pick(r, [f"Which object is {want}?", f"Look at the objects. Which one is {want}?"]), g,
                ["The ends are lined up at the left, so compare the right ends.", f"The {g.lower()} is {want}."],
                [W(x, "chose the wrong end of the order") for x in o], FN("len_pick", lens=lens, want=w2), qtype="visual", mode="any",
                diagram=Diagram("lengths", {"items": items}, alt))


@fam("012")
def lo_order(r, L):
    items, lens = objs(r, 3, L)
    want = pick(r, ["shortest first", "longest first"])
    order = sorted(lens, key=lens.get, reverse=want == "longest first")
    alt = "Objects lined up at the left: " + ", ".join(f"{k} {v} units long" for k, v in lens.items()) + "."
    ans = ", ".join(order)
    return Item(f"Put the objects in order from {'shortest to longest' if want == 'shortest first' else 'longest to shortest'}.", ans,
                ["Compare where each object ends.", f"The order is {ans}."], [W(", ".join(order[::-1]), "put them in the opposite order"), W(", ".join(lens), "kept the order shown")],
                FN("len_order", lens=lens, want=want), qtype="visual", mode="sa", diagram=Diagram("lengths", {"items": items}, alt))


@fam("012", mode="mc")
def lo_order_mc(r, L):
    items, lens = objs(r, 3, max(L, 1))
    want = "shortest first"
    order = sorted(lens, key=lens.get)
    good = ", ".join(order)
    bad = [", ".join(order[::-1]), ", ".join([order[1], order[0], order[2]]), ", ".join([order[0], order[2], order[1]])]
    alt = "Objects lined up at the left: " + ", ".join(f"{k} {v} units long" for k, v in lens.items()) + "."
    it = mc_key("Which list is in order from shortest to longest?", good, bad, ["Find the shortest, then the next, then the longest.", f"{good}."],
                qtype="visual", diagram=Diagram("lengths", {"items": items}, alt), r=r)
    it.check = FN("len_order", lens=lens, want=want)
    return it


@fam("012", mode="mc")
def lo_line_up(r, L):
    nm = name(r)
    good = "Line up the ends at the same starting line."
    bad = ["Look at which one has more color.", "Hold them at different heights.", "Pick the one that is on top."]
    if L == 2:
        good = "No. Their ends do not start at the same line."
        bad = ["Yes. The higher one is always longer.", "Yes. It looks longer, so it is longer.", "No. Lengths cannot be compared."]
        return mc_key(f"{nm} puts a crayon next to a pencil on a table. Their ends do not start at the same place. {nm} says the pencil is longer because it sticks out farther. Can {nm} be sure?",
                      good, bad, ["To compare lengths, start both at the same line.", good], qtype="explain", tags={"reasoning", "misconception"}, r=r)
    return mc_key(f"{nm} wants to see which of two sticks is longer. What should {nm} do first?", good, bad,
                  ["Compare lengths from the same starting line.", good], qtype="conceptual", r=r)


@fam("012")
def lo_text(r, L):
    a, b, c = r.sample(OBJ, 3)
    if L == 0:
        want = pick(r, ["shorter", "longer"])
        return Item(f"The {a.lower()} is longer than the {b.lower()}. Which is {want}?", a if want == "longer" else b,
                    [f"The {a.lower()} is longer.", f"So the {b.lower()} is shorter."], [W(b if want == "longer" else a, "mixed up longer and shorter")],
                    FN("indirect", facts=[[a, b]], want="cmp" if want == "longer" else "cmp_short", pair=[a, b]), mode="sa")
    want = pick(r, ["longest", "shortest"])
    facts = [[a, b], [a, c]] if L == 1 else [[b, c], [a, b]]
    if L == 1:
        need(want == "longest")
    t = " ".join(f"The {x.lower()} is longer than the {y.lower()}." for x, y in facts)
    g = a if want == "longest" else c
    return Item(f"{t} Which is the {want}?", g, ["Use the clues to order the objects.", f"The {g.lower()} is the {want}."],
                [W(x, "did not use both clues") for x in (a, b, c) if x != g], FN("indirect", facts=facts, want=want), qtype="reasoning", mode="sa")


@fam("2")
def lo_grid(r, L):
    items, lens = objs(r, 3, 2, aligned=False)
    want = pick(r, ["longest", "shortest"])
    g = (max if want == "longest" else min)(lens, key=lens.get)
    alt = "Objects on a grid that do not start at the same place: " + ", ".join(f"{it['label']} starts at {it['start']} and is {it['len']} units long" for it in items) + "."
    return Item(f"The objects do not start at the same place. Count the grid squares. Which object is {want}?", g,
                ["Count the squares each object covers.", f"The {g.lower()} is {lens[g]} squares long, so it is the {want}."],
                [W(x, "compared where the objects end") for x in lens if x != g], FN("len_pick", lens=lens, want=want), qtype="visual", tags={"reasoning"},
                mode="sa", diagram=Diagram("lengths", {"items": items, "grid": True, "line": False}, alt))


# ============================================================== S2 Comparing Lengths Indirectly
PAIRS = [("rug", "string", "desk"), ("door", "rope", "bed"), ("bus", "truck", "car"), ("snake", "stick", "worm"), ("couch", "yarn", "chair"),
         ("table", "tape", "box"), ("train", "bus", "van"), ("hall", "rope", "room"), ("board", "ribbon", "book"), ("slide", "rope", "bench")]


@fam("012")
def in_cmp(r, L):
    big, mid, small = pick(r, PAIRS)
    if L == 0:
        t = f"The {big} is longer than the {mid}. The {mid} is longer than the {small}. Is the {big} longer or shorter than the {small}?"
        ans, wrong = "longer", "shorter"
        chk = FN("indirect_word", facts=[[big, mid], [mid, small]], pair=[big, small])
    else:
        t = pick(r, [f"A {mid} is shorter than the {big}. The {mid} is longer than the {small}. Which is longer, the {big} or the {small}?",
                     f"The {small} is shorter than the {mid}. The {big} is longer than the {mid}. Which is longer, the {small} or the {big}?"])
        ans, wrong = big, small
        chk = FN("indirect", facts=[[big, mid], [mid, small]], want="cmp", pair=[big, small])
    return Item(t, ans, [f"The {big} is longer than the {mid}, and the {mid} is longer than the {small}.", f"So the {big} is longer than the {small}."],
                [W(wrong, "did not use the middle object to compare")], chk, qtype="reasoning", tags={"reasoning"}, mode="sa")


@fam("012", mode="mc")
def in_string(r, L):
    big, mid, small = pick(r, PAIRS)
    nm = name(r)
    t = (f"{nm} uses a piece of {mid}. The {mid} is longer than the {small}, but shorter than the {big}. Which is longer, the {small} or the {big}?" if L < 2 else
         f"{nm} cuts a piece of {mid} as long as the {small}. The piece does not reach the end of the {big}. Which is longer, the {small} or the {big}?")
    good = f"The {big}"
    bad = [f"The {small}", "They are the same length.", f"The {mid}"]
    it = mc_key(t, good, bad, [f"The {mid} is between them.", f"The {big} is longer."], qtype="reasoning", tags={"reasoning"}, r=r)
    return it


@fam("012")
def in_extreme(r, L):
    a, b, c = r.sample(["Ana", "Ben", "Kim", "Max", "Mia", "Sam", "Tom", "Zoe"], 3)
    obj = pick(r, ["snake", "ribbon", "worm", "jump rope", "train"])
    want = pick(r, ["longest", "shortest"])
    if L == 0:
        facts = [[a, b], [b, c]]
        t = f"{a}'s {obj} is longer than {b}'s. {b}'s {obj} is longer than {c}'s. Whose {obj} is the {want}?"
    elif L == 1:
        facts = [[b, c], [a, b]]
        t = f"{b}'s {obj} is longer than {c}'s. {a}'s {obj} is longer than {b}'s. Whose {obj} is the {want}?"
    else:
        facts = [[a, b], [b, c]]
        t = f"{c}'s {obj} is shorter than {b}'s. {b}'s {obj} is shorter than {a}'s. Whose {obj} is the {want}?"
    g = a if want == "longest" else c
    return Item(t, g, ["Put the three in order using the clues.", f"From longest to shortest: {a}, {b}, {c}. So {g}."],
                [W(x, "did not use both clues") for x in (a, b, c) if x != g], FN("indirect", facts=facts, want=want), qtype="reasoning", tags={"reasoning"}, mode="sa")


@fam("012", mode="mc")
def in_order(r, L):
    big, mid, small = pick(r, PAIRS)
    good = f"{big}, {mid}, {small}"
    bad = [f"{small}, {mid}, {big}", f"{mid}, {big}, {small}", f"{big}, {small}, {mid}"]
    it = mc_key(f"The {mid} is shorter than the {big}. The {small} is shorter than the {mid}. Which list goes from longest to shortest?", good, bad,
                ["Use each clue.", f"Longest to shortest: {good}."], qtype="reasoning", tags={"reasoning"}, r=r)
    return it


@fam("012", mode="mc")
def in_why(r, L):
    big, mid, small = pick(r, PAIRS)
    nm = name(r)
    good = f"Compare each one to the {mid}."
    bad = [f"Carry the {big} next to the {small}.", "Guess by looking.", f"Compare the {big} to itself."]
    if L == 2:
        good = f"The {big}, because the {mid} fits along the {small} with extra, and the {big} is longer than the {mid}."
        bad = [f"The {small}, because it is closer.", "They are the same, because the string touches both.", f"The {mid}, because it is in the middle."]
        return mc_key(f"The {big} and the {small} cannot be moved. The {mid} is longer than the {small}. The {mid} is shorter than the {big}. Which is longer, and why?",
                      good, bad, [f"The {mid} is between them.", good], qtype="explain", tags={"reasoning"}, r=r)
    return mc_key(f"{nm} cannot move the {big} or the {small}. How can {nm} use a {mid} to compare them?", good, bad,
                  [f"Hold the {mid} next to each one.", good], qtype="conceptual", r=r)


# ============================================================== S3 Measuring with Length Units
def unit_word(u, n):
    return ("cube" if n == 1 else "cubes") if u == "cube" else ("paper clip" if n == 1 else "paper clips")


@fam("012")
def mu_count(r, L):
    n = r.randint(2, 6) if L == 0 else r.randint(4, 9) if L == 1 else r.randint(6, 12)
    u = pick(r, ["cube", "clip"])
    ob = pick(r, OBJ)
    alt = f"A {ob.lower()} with {n} {unit_word(u, n)} laid end to end under it, with no gaps or overlaps."
    return Item(pick(r, [f"How long is the {ob.lower()}?", f"The {unit_word(u, 2)} are lined up end to end. How long is the {ob.lower()}?"]), f"{n} {unit_word(u, n)}",
                [f"Count the {unit_word(u, 2)} under the {ob.lower()}.", f"The {ob.lower()} is {n} {unit_word(u, n)} long."],
                [W(f"{n + 1} {unit_word(u, n + 1)}", "counted one twice"), W(f"{n - 1} {unit_word(u, n - 1)}", "skipped one"), W(f"{n + 2} {unit_word(u, n + 2)}", "counted the lines, not the units")],
                FN("units_long", len=n, units=[[i, 1] for i in range(n)], unit=unit_word(u, 2)), qtype="visual",
                diagram=Diagram("measure", {"len": n, "units": [[i, 1] for i in range(n)], "unit": u, "label": ob}, alt))


@fam("012")
def mu_grid(r, L):
    items, lens = objs(r, 2 if L == 0 else 3, L)
    it = pick(r, items)
    alt = "Objects on a grid starting at the same line: " + ", ".join(f"{k} {v} squares long" for k, v in lens.items()) + "."
    return Item(f"Each square is 1 unit. How many units long is the {it['label'].lower()}?", f"{it['len']} units",
                [f"Count the squares the {it['label'].lower()} covers.", f"It is {it['len']} units long."],
                [W(f"{it['len'] + 1} units", "counted the lines"), W(f"{it['len'] - 1} units", "skipped a square"), W(f"{max(lens.values()) if it['len'] != max(lens.values()) else min(lens.values())} units", "measured a different object")],
                FN("len_of", lens=lens, item=it["label"], unit="units"), qtype="visual", diagram=Diagram("lengths", {"items": items, "grid": True}, alt))


@fam("012")
def mu_diff(r, L):
    a, b = r.sample(range(2, 8) if L == 0 else range(3, 15 if L == 2 else 11), 2)
    o1, o2 = r.sample(OBJ, 2)
    big, small = max(a, b), min(a, b)
    n1, n2 = (o1, o2) if a > b else (o2, o1)
    return Item(f"The {o1.lower()} is {a} cubes long. The {o2.lower()} is {b} cubes long. How much longer is the {n1.lower()} than the {n2.lower()}?", f"{big - small} cubes",
                [f"Compare: {big} − {small}.", f"The {n1.lower()} is {big - small} cubes longer."],
                [W(f"{a + b} cubes", "added the lengths"), W(f"{big} cubes", "gave the longer length"), W(f"{big - small + 1} cubes", "counted one too many")],
                EX(f"{big}-{small}", unit="cubes"), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def mu_which(r, L):
    items, lens = objs(r, 3, max(L, 1))
    it = pick(r, items)
    alt = "Objects on a grid starting at the same line: " + ", ".join(f"{k} {v} squares long" for k, v in lens.items()) + "."
    good = it["label"]
    bad = [x for x in lens if x != good] + ["Not any of them"]
    m = mc_key(f"Each square is 1 unit. Which object is {it['len']} units long?", good, bad, ["Count the squares under each object.", f"The {good.lower()} is {it['len']} units long."],
               qtype="visual", diagram=Diagram("lengths", {"items": items, "grid": True}, alt), r=r)
    m.check = FN("len_is", lens=lens, n=it["len"])
    return m


@fam("012")
def mu_word(r, L):
    n = r.randint(3, 8) if L == 0 else r.randint(6, 15) if L == 1 else r.randint(12, 20)
    ob = pick(r, ["book", "desk", "lunch box", "shoe", "tray", "chair"])
    u = pick(r, ["cube", "clip"])
    nm = name(r)
    return Item(f"{nm} lays {n} {unit_word(u, n)} end to end along a {ob} with no gaps. They fit from one end to the other. How long is the {ob}?",
                f"{n} {unit_word(u, n)}", [f"Each {unit_word(u, 1)} is one unit.", f"The {ob} is {n} {unit_word(u, n)} long."],
                [W(f"{n - 1} {unit_word(u, n - 1)}", "counted the spaces between units"), W(f"{n + 1} {unit_word(u, n + 1)}", "counted one too many"), W(f"{2 * n} {unit_word(u, 2)}", "counted each unit twice")],
                FN("units_long", len=n, units=[[i, 1] for i in range(n)], unit=unit_word(u, 2)), qtype="word-problem", tags={"modeling"})


# ============================================================== S4 Measuring Correctly
def bad_layout(r, n, kind):
    us = [[i, 1] for i in range(n)]
    if kind == "gap":
        k = r.randint(1, n - 2)
        us = [[i + (0.4 if i >= k else 0), 1] for i in range(n - 1)]
    elif kind == "overlap":
        k = r.randint(1, n - 1)
        us = [[i - (0.4 if i >= k else 0), 1] for i in range(n + 1)]
        us = [[a, w] for a, w in us if a < n]
    elif kind == "size":
        us = [[0, 1], [1, 2]] + [[3 + i, 1] for i in range(n - 3)]
    return us


@fam("012", mode="mc")
def mc_check(r, L):
    n = r.randint(4, 7) if L < 2 else r.randint(5, 9)
    kind = pick(r, ["ok", "gap", "overlap", "size"] if L else ["ok", "gap", "overlap"])
    us = bad_layout(r, n, kind)
    ob = pick(r, OBJ)
    nm = name(r)
    cnt = len(us)
    good = {"ok": f"Yes. The {ob.lower()} is {n} cubes long.", "gap": "No. There are gaps between the cubes.",
            "overlap": "No. The cubes overlap.", "size": "No. The cubes are not all the same size."}[kind]
    opts = {"ok": f"Yes. The {ob.lower()} is {n} cubes long.", "gap": "No. There are gaps between the cubes.", "overlap": "No. The cubes overlap.",
            "size": "No. The cubes are not all the same size."}
    bad = [v for k, v in opts.items() if k != kind]
    alt = f"A {ob.lower()} with {cnt} cubes under it. " + {"ok": "The cubes touch end to end.", "gap": "There is a space between two cubes.",
                                                          "overlap": "Two cubes overlap.", "size": "One cube is bigger than the others."}[kind]
    it = mc_key(f"{nm} measured the {ob.lower()} with cubes. Did {nm} measure the right way?", good, bad[:3],
                ["Units must be the same size and touch end to end with no gaps or overlaps.", good], qtype="visual", tags={"misconception"},
                diagram=Diagram("measure", {"len": n, "units": us, "unit": "cube", "label": ob, "stagger": kind == "overlap"}, alt), r=r)
    it.check = FN("measure_ok", len=n, units=us)
    return it


@fam("012", mode="mc")
def mc_who(r, L):
    n1, n2 = r.sample(NAMES, 2)
    ob = pick(r, ["desk", "rug", "book", "table", "mat"])
    err = pick(r, ["leaves spaces between the paper clips", "lets the paper clips overlap", "uses big and small paper clips", "starts past the end of the " + ob])
    good = n2
    bad = [n1, "Both of them", "Neither of them"]
    it = mc_key(f"{n1} measures a {ob} and {err}. {n2} lines up same-size paper clips end to end with no gaps. Who measured the right way?", good, bad,
                ["Same-size units must touch end to end from one end to the other.", f"{n2} measured the right way."], qtype="conceptual", tags={"misconception"}, r=r)
    return it


@fam("012", mode="mc")
def mc_more_less(r, L):
    n = r.randint(5, 9)
    kind = pick(r, ["gap", "overlap"])
    ob = pick(r, OBJ)
    nm = name(r)
    good = "longer than that" if kind == "gap" else "shorter than that"
    bad = ["longer than that" if kind == "overlap" else "shorter than that", "exactly that length", "too long to measure"]
    word = "spaces between the cubes" if kind == "gap" else "cubes that overlap"
    it = mc_key(f"{nm} measures a {ob.lower()} and leaves {word}. {nm} counts {n} cubes. The {ob.lower()} is really ___.", good, bad,
                ["Gaps leave parts of the object without a cube, so the count is too small." if kind == "gap" else "Overlaps count some length twice, so the count is too big.", f"It is really {good}."],
                qtype="reasoning", tags={"reasoning", "misconception"}, r=r)
    return it


@fam("012")
def mc_fix(r, L):
    n = r.randint(3, 7) if L == 0 else r.randint(5, 10) if L == 1 else r.randint(7, 12)
    ob = pick(r, OBJ)
    alt = f"A {ob.lower()} {n} units long on a grid of same-size squares."
    nm = name(r)
    k = r.randint(1, 3)
    return Item(f"{nm} measured the {ob.lower()} with gaps and got {n - k} cubes. Count the squares to measure the right way. How long is the {ob.lower()}?", f"{n} cubes",
                ["Count each square under the object with no gaps.", f"The {ob.lower()} is {n} cubes long."],
                [W(f"{n - k} cubes", "kept the count with gaps"), W(f"{n + 1} cubes", "counted the lines"), W(f"{n - 1} cubes", "skipped a square")],
                FN("len_of", lens={ob: n}, item=ob, unit="cubes"), qtype="visual",
                diagram=Diagram("lengths", {"items": [{"label": ob, "len": n, "color": "blue"}], "grid": True}, alt))


@fam("12", mode="mc")
def mc_units(r, L):
    ob = pick(r, ["desk", "rug", "table", "door"])
    nm = name(r)
    good = "More paper clips than craft sticks, because paper clips are shorter."
    bad = ["More craft sticks, because craft sticks are longer.", "The same number of each.", "More paper clips, because paper clips are longer."]
    return mc_key(f"{nm} measures a {ob} with paper clips and then with craft sticks. A craft stick is longer than a paper clip. Which takes more?", good, bad,
                  ["Shorter units are needed more times to cover the same length.", good], qtype="reasoning", tags={"reasoning"}, r=r)


@fam("01", mode="mc")
def mc_rule(r, L):
    nm = name(r)
    ob = pick(r, ["desk", "book", "shoe", "rug", "box", "mat", "bench", "door"])
    u = pick(r, ["cubes", "paper clips", "blocks"])
    good = "End to end, with no gaps or overlaps"
    bad = ["With spaces between them", "On top of each other", "In a pile next to the " + ob]
    return mc_key(f"{nm} measures a {ob} with {u}. How should the {u} be placed?", good, bad,
                  ["Same-size units must touch end to end.", "There should be no gaps and no overlaps."], qtype="conceptual", r=r)


SKILLS = {
    1: dict(name="Comparing and Ordering Lengths", fams=[lo_extreme, lo_order, lo_order_mc, lo_line_up, lo_text, lo_grid]),
    2: dict(name="Comparing Lengths Indirectly", fams=[in_cmp, in_string, in_extreme, in_order, in_why]),
    3: dict(name="Measuring with Length Units", fams=[mu_count, mu_grid, mu_diff, mu_which, mu_word]),
    4: dict(name="Measuring Correctly", fams=[mc_check, mc_who, mc_more_less, mc_fix, mc_units, mc_rule]),
}
