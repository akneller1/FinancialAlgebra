"""Unit 12: Shapes and Equal Shares (shapes-equal-shares). 1.G.A.1, 1.G.A.2, 1.G.A.3."""
from g1lib import *

UNIT_ID = "shapes-equal-shares"

NAME = {"triangle": "triangle", "triangle2": "triangle", "square": "square", "rectangle": "rectangle", "trapezoid": "trapezoid",
        "hexagon": "hexagon", "circle": "circle", "halfcircle": "half-circle", "quartercircle": "quarter-circle"}
SIDES = {"triangle": 3, "triangle2": 3, "square": 4, "rectangle": 4, "trapezoid": 4, "hexagon": 6}
COLORS = ["blue", "orange", "green", "pink", "purple", "yellow"]


def kinds(L):
    return ["triangle", "square", "rectangle"] if L == 0 else ["triangle", "triangle2", "square", "rectangle", "trapezoid", "hexagon"]


def one(r, k, L):
    return {"kind": k, "rot": 0 if L == 0 else pick(r, [0, 0, 20, 45, 90, 180]), "size": pick(r, [0.6, 0.8, 1.0]), "color": pick(r, COLORS)}


# ============================================================== S1 Defining Attributes of Shapes
@fam("012")
def a_sides(r, L):
    k = pick(r, kinds(L))
    it = one(r, k, L)
    what = pick(r, ["sides", "corners"])
    n = SIDES[k]
    alt = f"One {it['color']} {NAME[k]}" + (f", turned" if it["rot"] else "") + "."
    return Item(pick(r, [f"How many {what} does this shape have?", f"Count the {what} of the shape. How many?"]), n,
                [f"Count each {what[:-1]} once. Touch them as you count.", f"The shape has {n} {what}."],
                [W(n + 1, f"counted a {what[:-1]} twice"), W(n - 1, f"missed a {what[:-1]}"), W(4 if n != 4 else 3, "guessed from how the shape looks"), W(n + 2, "made a counting mistake")],
                FN("shape_count", kind=k, what=what), qtype="visual", diagram=Diagram("shapes1", {"items": [it]}, alt))


@fam("012", mode="mc")
def a_which(r, L):
    want = pick(r, ["triangle", "square", "rectangle"] if L == 0 else ["triangle", "square", "rectangle", "trapezoid", "hexagon"])
    pool = [k for k in kinds(max(L, 1)) if NAME[k] != want]
    items = [dict(one(r, want if want != "triangle" else pick(r, ["triangle", "triangle2"]), L))]
    others = r.sample(pool, 2)
    items += [one(r, k, L) for k in others]
    if L >= 1 and want in ("triangle", "square", "rectangle"):
        items.append({"kind": "triangle" if want == "triangle" else "square" if want == "square" else "rectangle", "open": True, "color": "blue"})
    else:
        items.append(one(r, pick(r, ["circle", "halfcircle"]), L))
    r.shuffle(items)
    for i, it in enumerate(items):
        it["label"] = "ABCD"[i]
    good = [it["label"] for it in items if NAME[it["kind"]] == want and not it.get("open")]
    need(len(good) == 1)
    alt = "Four shapes: " + "; ".join(f"{it['label']} is {'an open figure with a gap' if it.get('open') else 'a ' + NAME[it['kind']]}" for it in items) + "."
    bad = [it["label"] for it in items if it["label"] != good[0]]
    m = mc_key(f"Which shape is a {want}?", good[0], bad, [f"A {want} is closed and has {SIDES.get([k for k, v in NAME.items() if v == want][0], 0)} straight sides." if want != "circle" else "", f"Shape {good[0]} is the {want}."],
               qtype="visual", diagram=Diagram("shapes1", {"items": items}, alt), r=r)
    m.check = FN("shape_label", items=items, rule={"kinds": [k for k, v in NAME.items() if v == want]})
    return m


@fam("012", mode="mc")
def a_defining(r, L):
    k = pick(r, ["triangle", "square", "rectangle", "hexagon"] if L else ["triangle", "square"])
    rule = {"triangle": "It is closed and has 3 straight sides.", "square": "It is closed and has 4 equal straight sides and 4 square corners.",
            "rectangle": "It is closed and has 4 straight sides and 4 square corners.", "hexagon": "It is closed and has 6 straight sides."}[k]
    bad = [f"It is {pick(r, ['red', 'blue', 'green', 'yellow'])}.", f"It is {pick(r, ['big', 'small', 'tiny', 'large'])}.", pick(r, ["It points up.", "It is turned.", "It is on the left."])]
    return mc_key(f"What makes a shape a {k}?", rule, bad, ["Color, size, and which way a shape is turned do not change its name.", rule], qtype="conceptual", tags={"misconception"}, r=r)


@fam("012", mode="mc")
def a_turned(r, L):
    k = pick(r, ["triangle", "square", "rectangle", "trapezoid", "hexagon"] if L else ["triangle", "square", "rectangle"])
    change = pick(r, ["turned upside down", "made bigger", "colored red", "turned on its side", "made smaller"])
    good = f"Yes. It still has {SIDES[k]} sides and {SIDES[k]} corners."
    bad = [f"No. A {k} cannot be {change}.", f"No. It has a new number of sides.", f"Yes. But now it has {SIDES[k] + 1} sides."]
    return mc_key(f"A {k} is {change}. Is it still a {k}?", good, bad, ["Turning, size, and color do not change the sides and corners.", good], qtype="conceptual", tags={"misconception"}, r=r)


@fam("012", mode="mc")
def a_open(r, L):
    k = pick(r, ["triangle", "square", "rectangle"])
    alt = f"A figure made of {SIDES[k]} straight lines with a gap, so it is not closed."
    good = f"No. It is not closed."
    bad = [f"Yes. It has {SIDES[k]} straight sides.", f"Yes. It looks like a {k}.", "No. It is too small."]
    return mc_key(f"Is this figure a {k}?", good, bad, [f"A {k} must be closed.", "This figure has a gap, so it is not a closed shape."], qtype="visual", tags={"misconception"},
                  diagram=Diagram("shapes1", {"items": [{"kind": k, "open": True, "color": "blue"}]}, alt), r=r)


@fam("12")
def a_draw(r, L):
    k = pick(r, ["triangle", "square", "rectangle", "trapezoid", "hexagon"])
    n = SIDES[k]
    what = pick(r, ["sides", "corners"])
    return Item(f"{name(r)} wants to draw a {k}. How many straight {what} must the drawing have?", n, [f"A {k} has {n} {what}.", f"So the drawing needs {n} {what}."],
                [W(n + 1, "counted a side twice"), W(n - 1, "missed a side"), W(4 if n != 4 else 3, "guessed")], FN("shape_count", kind=k, what=what), qtype="conceptual")


# ============================================================== S2 Naming Two- and Three-Dimensional Shapes
@fam("012")
def n_name2d(r, L):
    pool = ["triangle", "square", "rectangle", "circle"] if L == 0 else ["triangle", "triangle2", "square", "rectangle", "trapezoid", "hexagon", "circle", "halfcircle", "quartercircle"]
    k = pick(r, pool)
    it = one(r, k, L)
    alt = f"One {it['color']} shape." + (" It is turned." if it["rot"] else "")
    alt = f"A {it['color']} {NAME[k]}" + (", turned" if it["rot"] else "") + "."
    wr = {"triangle": "square", "triangle2": "square", "square": "rectangle", "rectangle": "square", "circle": "oval", "trapezoid": "triangle", "hexagon": "circle",
          "halfcircle": "circle", "quartercircle": "triangle"}
    return Item(pick(r, ["What is the name of this shape?", "Name this shape."]), NAME[k], ["Count the sides and corners, and look for curves.", f"It is a {NAME[k]}."],
                [W(wr[k], "named it by how it looks"), W("diamond" if k == "square" else "pentagon", "named it by how it is turned" if k == "square" else "counted the sides wrong")],
                FN("shape_name", kind=k), qtype="visual", diagram=Diagram("shapes1", {"items": [it]}, alt))


SOLIDS = {"cube": "cube", "prism": "rectangular prism", "cylinder": "cylinder", "cone": "cone", "sphere": "sphere"}


@fam("012", mode="mc")
def n_solid_pick(r, L):
    ks = r.sample(list(SOLIDS), 4 if L else 3)
    want = pick(r, ks)
    items = [{"kind": k, "label": "ABCD"[i]} for i, k in enumerate(ks)]
    good = [it["label"] for it in items if it["kind"] == want][0]
    bad = [it["label"] for it in items if it["label"] != good]
    if len(bad) < 3:
        bad.append("Not any of them")
    alt = "Solids: " + "; ".join(f"{it['label']} is a {SOLIDS[it['kind']]}" for it in items) + "."
    m = mc_key(f"Which solid is a {SOLIDS[want]}?", good, bad, ["Look at the faces and curved surfaces.", f"Solid {good} is the {SOLIDS[want]}."],
               qtype="visual", diagram=Diagram("solids", {"items": items}, alt), r=r)
    m.check = FN("solid_lbl", items=items, want=want)
    return m


@fam("012")
def n_solid_name(r, L):
    k = pick(r, list(SOLIDS) if L else ["cube", "cylinder", "cone", "sphere"])
    alt = f"A {SOLIDS[k]}."
    wr = {"cube": "square", "prism": "rectangle", "cylinder": "circle", "cone": "triangle", "sphere": "circle"}
    return Item(pick(r, ["What is the name of this solid shape?", "Name this 3‑D shape."]), SOLIDS[k], ["Look for flat faces, curved surfaces, and points.", f"It is a {SOLIDS[k]}."],
                [W(wr[k], "used a flat shape name"), W("cube" if k != "cube" else "rectangular prism", "mixed up two solids")],
                FN("shape_name", kind=k), qtype="visual", diagram=Diagram("solids", {"items": [{"kind": k, "label": ""}]}, alt))


RIDDLES = [("I have 3 straight sides and 3 corners. What shape am I?", "triangle"),
           ("I have 4 straight sides that are all the same length and 4 square corners. What shape am I?", "square"),
           ("I have 4 straight sides and 4 square corners. Two of my sides are longer than the other two. What shape am I?", "rectangle"),
           ("I am round and have no corners. I am flat. What shape am I?", "circle"),
           ("I have 6 straight sides and 6 corners. What shape am I?", "hexagon"),
           ("I am a solid. I have 6 flat faces that are all squares. What am I?", "cube"),
           ("I am a solid. I have 2 flat circle faces and a curved side. What am I?", "cylinder"),
           ("I am a solid. I have 1 flat circle face and a point at the top. What am I?", "cone"),
           ("I am a circle cut in half. I have one straight side and one curved side. What shape am I?", "half-circle"),
           ("I am a solid like a box. My faces are rectangles. What am I?", "rectangular prism"),
           ("I have 4 straight sides. Only two of my sides go the same way. I look like a pattern block. What shape am I?", "trapezoid"),
           ("I am a solid that is round all over, like a ball. What am I?", "sphere")]


@fam("012")
def n_riddle(r, L):
    p, a = pick(r, RIDDLES[:8] if L == 0 else RIDDLES)
    return Item(p, a, ["Use the clues about sides, corners, faces, and curves.", f"The answer is a {a}."],
                [W("square" if a != "square" else "rectangle", "used only one clue"), W("circle" if a not in ("circle", "sphere") else "oval", "did not use the clues")],
                KEY(a), qtype="reasoning", tags={"reasoning"})


@fam("012", mode="mc")
def n_name_mc(r, L):
    pool = ["triangle", "square", "rectangle", "circle"] if L == 0 else ["trapezoid", "hexagon", "halfcircle", "quartercircle", "rectangle", "triangle2"]
    k = pick(r, pool)
    it = one(r, k, L)
    alt = f"A {it['color']} {NAME[k]}" + (", turned" if it["rot"] else "") + "."
    good = NAME[k]
    bad = [x for x in ["triangle", "square", "rectangle", "circle", "trapezoid", "hexagon", "half-circle", "quarter-circle"] if x != good]
    m = mc_key(pick(r, ["Which name matches the shape?", "What shape is this?"]), good, r.sample(bad, 3), ["Count sides and corners and look for curves.", f"It is a {good}."],
               qtype="visual", diagram=Diagram("shapes1", {"items": [it]}, alt), r=r)
    m.check = FN("shape_name", kind=k)
    return m


# ============================================================== S3 Composing Shapes
COMP = {"square_tri2": ("triangles", "square"), "square_tri4": ("triangles", "square"), "rect_sq2": ("squares", "rectangle"), "rect_sq3": ("squares", "rectangle"),
        "square_sq4": ("squares", "square"), "rect_tri2": ("triangles", "rectangle"), "square_rect2": ("rectangles", "square"), "hex_tri6": ("triangles", "hexagon"),
        "hex_trap2": ("trapezoids", "hexagon"), "trap_tri3": ("triangles", "trapezoid"), "circle_half2": ("half-circles", "circle"),
        "circle_quarter4": ("quarter-circles", "circle")}
NPIECE = {"square_tri2": 2, "square_tri4": 4, "rect_sq2": 2, "rect_sq3": 3, "square_sq4": 4, "rect_tri2": 2, "square_rect2": 2, "hex_tri6": 6, "hex_trap2": 2,
          "trap_tri3": 3, "circle_half2": 2, "circle_quarter4": 4}
EASY = ["square_tri2", "rect_sq2", "square_sq4", "circle_half2", "square_rect2", "rect_tri2"]


@fam("012")
def c_count(r, L):
    nm = pick(r, EASY if L == 0 else list(COMP))
    piece, whole = COMP[nm]
    n = NPIECE[nm]
    alt = f"A {whole} made of {n} {piece}, with each piece outlined."
    return Item(pick(r, [f"How many {piece} make this {whole}?", f"The {whole} is made of {piece}. How many {piece} are used?"]), n,
                [f"Count each piece once.", f"{n} {piece} make the {whole}."],
                [W(n + 1, "counted a piece twice"), W(n - 1, "missed a piece"), W(1, "counted the whole shape"), W(n * 2, "counted the corners")],
                FN("compose_count", name=nm), qtype="visual", diagram=Diagram("compose", {"name": nm}, alt))


@fam("012", mode="mc")
def c_whole(r, L):
    nm = pick(r, EASY if L == 0 else list(COMP))
    piece, whole = COMP[nm]
    n = NPIECE[nm]
    alt = f"{n} {piece} put together, with each piece outlined."
    bad = [x for x in ["square", "rectangle", "hexagon", "trapezoid", "circle", "triangle"] if x != whole]
    m = mc_key(f"{n} {piece} are put together. What new shape do they make?", whole, r.sample(bad, 3), ["Look at the outside edge of the whole shape.", f"They make a {whole}."],
               qtype="visual", diagram=Diagram("compose", {"name": nm}, alt), r=r)
    m.check = FN("compose_whole", name=nm)
    return m


@fam("12")
def c_copies(r, L):
    nm = pick(r, ["hex_tri6", "hex_trap2", "trap_tri3", "square_tri2", "square_tri4", "rect_sq3"])
    piece, whole = COMP[nm]
    n = NPIECE[nm]
    k = 2
    alt = f"A {whole} made of {n} {piece}."
    return Item(f"This {whole} is made of {piece}. How many {piece} do you need to make {k} {whole}s like this?", k * n,
                [f"One {whole} uses {n} {piece}.", f"{' + '.join([str(n)] * k)} = {k * n}."],
                [W(n, "made only one"), W(n + k, "added instead of using equal groups"), W(k * n + 1, "counted one too many"), W(k, "gave the number of new shapes")],
                FN("compose_count", name=nm, copies=k), qtype="visual", tags={"multistep"}, diagram=Diagram("compose", {"name": nm}, alt))


@fam("012", mode="mc")
def c_which_pieces(r, L):
    opts = [("Two triangles", "square"), ("Two squares", "rectangle"), ("Two half-circles", "circle"), ("Six triangles", "hexagon"), ("Two trapezoids", "hexagon"),
            ("Four quarter-circles", "circle"), ("Three triangles", "trapezoid")]
    good, whole = pick(r, opts[:3] if L == 0 else opts)
    bad = [o for o, w in opts if w != whole][:6]
    m = mc_key(f"Which pieces can be put together to make a {whole}?", good, r.sample(bad, 3), [f"Think about pattern blocks.", f"{good} can make a {whole}."], qtype="conceptual", r=r)
    return m


@fam("012")
def c_tower(r, L):
    a = r.randint(2, 5) if L == 0 else r.randint(3, 9)
    k = 1 if L == 0 else 2
    nm = name(r)
    solid = pick(r, ["cubes", "rectangular prisms"])
    if L == 0:
        return Item(f"{nm} stacks {a} {solid} to make a tower. Then {nm} adds 1 more. How many {solid} are in the tower now?", f"{a + 1} {solid}",
                    [f"{a} and 1 more.", f"{a} + 1 = {a + 1}."], [W(f"{a} {solid}", "did not add the new one"), W(f"{a + 2} {solid}", "counted one too many"), W(f"{a - 1} {solid}", "took one away")],
                    EX(f"{a}+1", unit=solid), qtype="word-problem")
    return Item(f"{nm} makes a tower with {a} {solid}. {nm} makes {k} towers just like it. How many {solid} does {nm} use in all?", f"{a * k} {solid}",
                [f"Each tower has {a}.", f"{' + '.join([str(a)] * k)} = {a * k}."],
                [W(f"{a + k} {solid}", "added the number of towers"), W(f"{a} {solid}", "counted one tower"), W(f"{a * k + 1} {solid}", "counted one too many")],
                EX("+".join([str(a)] * k), unit=solid), qtype="word-problem", tags={"multistep"})


PUT = [("2 squares side by side", "rectangle"), ("4 same-size squares in 2 rows of 2", "square"), ("2 half-circles with their straight sides together", "circle"),
       ("4 quarter-circles with their corners together", "circle"), ("6 pattern-block triangles around one point", "hexagon"), ("2 pattern-block trapezoids with their long sides together", "hexagon"),
       ("3 squares in a row", "rectangle"), ("2 rectangles of the same size, one on top of the other, to make 4 equal sides", "square")]


@fam("012")
def c_put(r, L):
    what, whole = pick(r, PUT[:4] if L == 0 else PUT)
    nm = name(r)
    return Item(f"{nm} puts together {what}. What shape does {nm} make?", whole, ["Picture the outside edge of the new shape.", f"It makes a {whole}."],
                [W("triangle" if whole != "triangle" else "square", "named one of the pieces"), W("oval" if whole == "circle" else "trapezoid", "did not picture the whole shape")],
                KEY(whole), qtype="reasoning", tags={"reasoning"})


# ============================================================== S4 Halves and Fourths
def part(r, L, allow_unequal=True):
    shape = pick(r, ["rect", "circle", "square"])
    k = pick(r, [2, 4])
    eq = (not allow_unequal) or r.random() < 0.7
    if shape == "circle":
        d = {"shape": "circle", "n": k} if eq else {"shape": "circle", "angles": [140, 220] if k == 2 else [60, 120, 90, 90]}
    elif eq:
        d = {"shape": shape, "cuts": pick(r, ["v", "diag2"]) if k == 2 else pick(r, ["v", "grid", "diag4"] if L else ["v", "grid"])}
        if d["cuts"] == "v":
            d["widths"] = [1] * k
        if d["cuts"] == "grid":
            d.update(rows=2, cols=2)
    else:
        d = {"shape": shape, "cuts": "v", "widths": [1, 2] if k == 2 else [1, 1, 2, 1]}
    return d, k, eq


@fam("012")
def h_name(r, L):
    d, k, eq = part(r, L)
    alt = f"A {'rectangle' if d['shape'] == 'rect' else d['shape']} cut into {k} {'equal' if eq else 'unequal'} parts."
    ans = ("halves" if k == 2 else "fourths") if eq else "not equal shares"
    return Item(pick(r, ["What are the parts called? Write halves, fourths, or not equal shares.", "Name the shares: halves, fourths, or not equal shares."]), ans,
                ["Check that the parts are the same size, then count them.", f"There are {k} {'equal' if eq else 'unequal'} parts, so: {ans}."],
                [W("fourths" if ans == "halves" else "halves", "counted the parts wrong"), W(("halves" if k == 2 else "fourths") if not eq else "not equal shares", "did not check that the parts are equal" if not eq else "thought the parts are not equal")],
                FN("share_word", **d), qtype="visual", diagram=Diagram("partition", d, alt))


@fam("012", mode="mc")
def h_shaded(r, L):
    d, k, eq = part(r, L, allow_unequal=False)
    d = dict(d, shade=[0])
    alt = f"A {'rectangle' if d['shape'] == 'rect' else d['shape']} cut into {k} equal parts. One part is shaded."
    good = "half of the shape" if k == 2 else pick(r, ["a fourth of the shape", "a quarter of the shape"])
    bad = ["a fourth of the shape" if k == 2 else "half of the shape", "all of the shape", "none of the shape" if L == 0 else ("two halves of the shape" if k == 4 else "two fourths of the shape")]
    m = mc_key(pick(r, ["How much of the shape is shaded?", "What part of the shape is shaded?"]), good, bad, [f"There are {k} equal shares and 1 is shaded.", f"So {good} is shaded."],
               qtype="visual", diagram=Diagram("partition", d, alt), r=r)
    m.check = FN("share_of", **{x: y for x, y in d.items() if x != "shade"})
    return m


@fam("012")
def h_count(r, L):
    d, k, eq = part(r, L, allow_unequal=False)
    word = "halves" if k == 2 else "fourths"
    alt = f"A {'rectangle' if d['shape'] == 'rect' else d['shape']} cut into {k} equal parts."
    return Item(pick(r, ["How many equal shares does the shape have?", "Count the equal shares. How many are there?"]), k,
                ["Count each part.", f"There are {k} equal shares, called {word}."],
                [W(k + 1, "counted the lines"), W(k - 1, "counted the cut lines only"), W(2 if k == 4 else 4, "mixed up halves and fourths"), W(1, "counted the whole")],
                FN("share_n", **d), qtype="visual", diagram=Diagram("partition", d, alt))


@fam("012")
def h_word(r, L):
    food = pick(r, ["pizza", "sandwich", "pancake", "cracker", "tortilla", "brownie", "cookie"])
    k = pick(r, [2, 4])
    nm = name(r)
    good = "half" if k == 2 else "fourth"
    return Item(f"{nm} cuts a {food} into {k} equal shares. What is one share called? Write half or fourth.", good,
                [f"{k} equal shares are {'halves' if k == 2 else 'fourths'}.", f"One share is one {good} of the {food}."],
                [W("fourth" if k == 2 else "half", "mixed up halves and fourths"), W("whole", "thought one share is the whole")],
                KEY(good, f"a {good}", f"one {good}", *([] if k == 2 else ["quarter", "a quarter", "one quarter"])), qtype="word-problem", tags={"modeling"}, mode="sa")


@fam("012", mode="mc")
def h_which(r, L):
    k = pick(r, [2, 4])
    good_d = {"shape": "rect", "cuts": "v", "widths": [1] * k} if r.random() < 0.5 else {"shape": "circle", "n": k}
    bad_d = {"shape": "rect", "cuts": "v", "widths": [1, 2] if k == 2 else [1, 1, 2, 1]} if good_d["shape"] == "circle" else {"shape": "circle", "angles": [140, 220] if k == 2 else [60, 120, 90, 90]}
    a_good = r.random() < 0.5
    dA, dB = (good_d, bad_d) if a_good else (bad_d, good_d)
    word = "halves" if k == 2 else "fourths"
    alt = f"Shape A is cut into {k} {'equal' if a_good else 'unequal'} parts. Shape B is cut into {k} {'unequal' if a_good else 'equal'} parts."
    good = "Shape A" if a_good else "Shape B"
    m = mc_key(f"Which shape is cut into {word}?", good, ["Shape B" if a_good else "Shape A", "Both shapes", "Neither shape"],
               [f"{word.capitalize()} must be equal shares.", f"{good} has {k} equal shares."], qtype="visual", tags={"misconception"},
               diagram=Diagram("partition_pair", {"a": dict(dA, shade=[]), "b": dict(dB, shade=[])}, alt), r=r)
    m.check = FN("pair_equal", a=dA, b=dB)
    return m


@fam("012", mode="mc")
def h_food(r, L):
    food = pick(r, ["pizza", "sandwich", "pancake", "cracker", "tortilla", "brownie", "pie", "waffle", "pan of cornbread"])
    k = pick(r, [2, 4])
    nm = name(r)
    eat = 1 if L < 2 else r.randint(1, k)
    w = {2: "half", 4: pick(r, ["fourth", "quarter"])}[k]
    if eat == 1:
        good = f"one {w} of the {food}"
    elif eat == k:
        good = f"the whole {food}"
    else:
        good = f"{eat} {w}s of the {food}" if k == 4 else f"{eat} halves of the {food}"
    other = {2: "fourth", 4: "half"}[k]
    bad = [f"one {other} of the {food}", f"the whole {food}" if eat != k else f"one {w} of the {food}", f"{k} {food}s"]
    return mc_key(f"{nm} cuts a {food} into {k} equal shares and eats {eat} of them. How much of the {food} did {nm} eat?", good, bad,
                  [f"{k} equal shares are {'halves' if k == 2 else 'fourths'}.", f"{nm} ate {good}."], qtype="word-problem", tags={"modeling"}, r=r)


@fam("012")
def h_fold(r, L):
    shp = pick(r, ["square", "rectangle", "circle"])
    nm = name(r)
    twice = r.random() < 0.5 if L else False
    n = 4 if twice else 2
    p = f"{nm} folds a paper {shp} in half" + (" and then in half again" if twice else "") + ". Then {nm} opens it. How many equal shares are there?".replace("{nm}", nm)
    return Item(p, n, ["Each fold in half doubles the number of equal shares." if twice else "Folding in half makes 2 equal shares.", f"There are {n} equal shares."],
                [W(2 if twice else 4, "mixed up halves and fourths"), W(3, "counted the folds and the paper"), W(1, "counted the paper only")],
                FN("count_n", n=n), qtype="reasoning")


# ============================================================== S5 More Shares Are Smaller Shares
@fam("012", mode="mc")
def m_bigger(r, L):
    food = pick(r, ["pizza", "sandwich", "pancake", "cracker", "pie", "orange", "granola bar"])
    n1, n2 = r.sample(NAMES, 2)
    a, b = pick(r, [(2, 4), (4, 2)])
    w = {2: "half", 4: "fourth"}
    good = f"{n1}'s share" if a < b else f"{n2}'s share"
    bad = [f"{n2}'s share" if a < b else f"{n1}'s share", "They are the same size.", "You cannot tell."]
    m = mc_key(f"Two {food}s are the same size. {n1} gets one {w[a]} of the first {food}. {n2} gets one {w[b]} of the second {food}. Whose share is bigger?", good, bad,
               ["The more equal shares a whole is cut into, the smaller each share is.", f"A half is bigger than a fourth, so {good} is bigger."], qtype="reasoning", tags={"misconception"}, r=r)
    m.check = FN("bigger_piece", a=a, b=b, names=[f"{n1}'s share", f"{n2}'s share"])
    return m


@fam("012")
def m_whole(r, L):
    word = pick(r, ["halves", "fourths", "quarters"])
    n = 2 if word == "halves" else 4
    food = pick(r, ["pizza", "sandwich", "pie", "cake", "waffle"])
    p = pick(r, [f"How many {word} make one whole {food}?", f"A {food} is cut into {word}. How many {word} are in the whole {food}?"])
    return Item(p, n, [f"{word.capitalize()} means the whole is cut into {n} equal shares.", f"{n} {word} make one whole."],
                [W(4 if n == 2 else 2, "mixed up halves and fourths"), W(1, "thought one share is the whole"), W(n + 1, "counted one too many")],
                FN("shares_whole", word=word), qtype="conceptual")


@fam("012", mode="mc")
def m_more_shares(r, L):
    nm = name(r)
    food = pick(r, ["paper strip", "pizza", "sandwich", "piece of toast"])
    good = "The fourths are smaller."
    bad = ["The fourths are bigger.", "They are the same size.", "The halves are smaller."]
    p = f"{nm} cuts one {food} into halves and a same-size {food} into fourths. Which shares are smaller?"
    if L == 2:
        p = f"{nm} says one fourth of the {food} is bigger than one half of the same {food} because 4 is more than 2. Which is right?"
        good = "A half is bigger, because the whole is cut into fewer shares."
        bad = ["A fourth is bigger, because 4 is more than 2.", "They are the same size.", "A fourth is bigger, because there are more pieces."]
    return mc_key(p, good, bad, ["More equal shares of the same whole means smaller shares.", good], qtype="reasoning", tags={"misconception", "reasoning"}, r=r)


@fam("012")
def m_left(r, L):
    k = pick(r, [2, 4]) if L else 4
    eaten = r.randint(1, k - 1)
    food = pick(r, ["pizza", "pie", "cake", "sandwich", "waffle"])
    word = "halves" if k == 2 else "fourths"
    nm = name(r)
    return Item(f"A {food} is cut into {word}. {nm} eats {eaten} of the shares. How many shares are left?", k - eaten,
                [f"There are {k} {word} in all.", f"{k} − {eaten} = {k - eaten} shares are left."],
                [W(k, "gave all the shares"), W(eaten, "gave the shares eaten"), W(k + eaten, "added"), W(k - eaten + 1, "counted one too many")],
                FN("shares_left", word=word, eaten=eaten), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def m_pair(r, L):
    a_k = pick(r, [2, 4])
    shp = pick(r, ["rect", "circle"])
    dA = {"shape": shp, "cuts": "v", "widths": [1] * a_k} if shp == "rect" else {"shape": "circle", "n": a_k}
    b_k = 6 - a_k
    dB = {"shape": shp, "cuts": "v", "widths": [1] * b_k} if shp == "rect" else {"shape": "circle", "n": b_k}
    want = pick(r, ["smaller", "bigger"])
    smaller = "Shape A" if a_k > b_k else "Shape B"
    good = smaller if want == "smaller" else ("Shape B" if smaller == "Shape A" else "Shape A")
    alt = f"Two same-size {'rectangles' if shp == 'rect' else 'circles'}. Shape A has {a_k} equal shares. Shape B has {b_k} equal shares."
    m = mc_key(f"The shapes are the same size. Which shape has {want} shares?", good, ["Shape B" if good == "Shape A" else "Shape A", "They are the same size.", "You cannot tell."],
               ["More equal shares are smaller shares.", f"{good} has {want} shares."], qtype="visual", tags={"reasoning"},
               diagram=Diagram("partition_pair", {"a": dict(dA, shade=[]), "b": dict(dB, shade=[])}, alt), r=r)
    m.check = FN("bigger_piece", a=a_k, b=b_k, names=["Shape A", "Shape B"]) if want == "bigger" else FN("smaller_piece", a=a_k, b=b_k, names=["Shape A", "Shape B"])
    return m


@fam("12", mode="mc")
def m_describe(r, L):
    k = pick(r, [2, 4])
    word = "halves" if k == 2 else "fourths"
    good = f"{k} {word} make one whole."
    bad = [f"{6 - k} {word} make one whole.", f"1 {word[:-1] if k == 2 else 'fourth'} makes one whole.", f"{k} {word} make two wholes."]
    bad = [b.replace("1 halve", "1 half") for b in bad]
    return mc_key(f"A circle is cut into {word}. Which sentence is true?", good, bad, [f"{word.capitalize()} split one whole into {k} equal shares.", good], qtype="conceptual", r=r)


SKILLS = {
    1: dict(name="Defining Attributes of Shapes", fams=[a_sides, a_which, a_defining, a_turned, a_open, a_draw]),
    2: dict(name="Naming Two- and Three-Dimensional Shapes", fams=[n_name2d, n_solid_pick, n_solid_name, n_riddle, n_name_mc]),
    3: dict(name="Composing Shapes", fams=[c_count, c_whole, c_copies, c_which_pieces, c_tower, c_put]),
    4: dict(name="Halves and Fourths", fams=[h_name, h_shaded, h_count, h_word, h_which, h_food, h_fold]),
    5: dict(name="More Shares Are Smaller Shares", fams=[m_bigger, m_left, m_more_shares, m_whole, m_pair, m_describe]),
}
