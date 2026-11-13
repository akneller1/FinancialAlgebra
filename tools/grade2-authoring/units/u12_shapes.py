"""Unit 12: Shapes and Equal Shares (shapes-equal-shares). 2.G.A.1, 2.G.A.2, 2.G.A.3."""
import math
from g2lib import *

UNIT_ID = "shapes-equal-shares"

PNAME = {3: "triangle", 4: "quadrilateral", 5: "pentagon", 6: "hexagon"}


def poly_pts(r, n, regular=False):
    """Convex polygon with n corners on a small integer grid (no three corners in a line)."""
    for _ in range(200):
        a0 = r.uniform(0, 2 * math.pi)
        if regular:
            angs = [a0 + 2 * math.pi * k / n for k in range(n)]
            rad = [3.0] * n
        else:
            angs = sorted(a0 + 2 * math.pi * (k + r.uniform(-0.3, 0.3)) / n for k in range(n))
            rad = [r.uniform(2.2, 3.4) for _ in range(n)]
        pts = [(round(3.5 + rr * math.cos(a)), round(3.5 + rr * math.sin(a))) for a, rr in zip(angs, rad)]
        if len(set(pts)) != n:
            continue
        ok = True
        sgn = None
        for i in range(n):
            (x1, y1), (x2, y2), (x3, y3) = pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
            cr = (x2 - x1) * (y3 - y2) - (y2 - y1) * (x3 - x2)
            if cr == 0 or (sgn is not None and (cr > 0) != sgn):
                ok = False
                break
            sgn = cr > 0
        if ok:
            mx, my = min(p[0] for p in pts), min(p[1] for p in pts)
            return [[x - mx, y - my] for x, y in pts]
    raise Need()


def shape_d(pts, alt, fill="blue"):
    return Diagram("draw_shape", {"pts": pts, "fill": fill}, alt)


def row_d(r, ns):
    items = [{"pts": poly_pts(sub(r, 20 + k), n), "label": "ABCD"[k]} for k, n in enumerate(ns)]
    alt = "Four shapes labeled A to D. " + " ".join(f"Shape {it['label']} has {n} straight sides." for it, n in zip(items, ns))
    return items, Diagram("shape_row", {"items": items}, alt)


# ============================================================== S1 Naming Shapes by Sides and Angles
@fam("012")
def sn_name(r, L):
    n = pick(r, [3, 4, 5, 6])
    pts = poly_pts(r, n, regular=(L == 0 and r.random() < 0.5))
    alt = f"A closed shape with {n} straight sides and {n} corners."
    return Item("What is the name of this shape?", PNAME[n], [f"Count the sides: {n}. Count the angles: {n}.", f"A shape with {n} sides is a {PNAME[n]}."],
                [W(PNAME[3 + (n - 2) % 4], "miscounted the sides"), W(PNAME[(n - 2) % 4 + 3] if (n - 2) % 4 + 3 != n else "circle", "named the shape by how it looks")],
                FN("poly_name", pts=pts), qtype="visual", diagram=shape_d(pts, alt))


@fam("012")
def sn_count(r, L):
    n = pick(r, [3, 4, 5, 6])
    pts = poly_pts(r, n)
    what = pick(r, ["sides", "angles", "vertices"]) if L else pick(r, ["sides", "angles"])
    alt = f"A closed shape with {n} straight sides and {n} corners."
    return Item(f"How many {what} does this shape have?", n, [f"Touch and count each {'side' if what == 'sides' else 'corner'} once.", f"It has {n} {what}."],
                [W(n + 1, "counted one twice"), W(n - 1, "missed one"), W(2 * n, "counted sides and angles together")], FN("poly_count", pts=pts), qtype="visual", diagram=shape_d(pts, alt, "green"))


@fam("012", mode="mc")
def sn_which(r, L):
    ns = r.sample([3, 4, 5, 6], 4)
    want = pick(r, ns)
    items, dg = row_d(r, ns)
    lab = "ABCD"[ns.index(want)]
    it = mc_key(f"Which shape is a {PNAME[want]}?", lab, [x for x in "ABCD" if x != lab], [f"A {PNAME[want]} has {want} sides.", f"Shape {lab} has {want} sides."], qtype="visual", diagram=dg, r=r)
    it.check = FN("shape_label", items=items, sides=want)
    return it


@fam("012")
def sn_riddle(r, L):
    n = pick(r, [3, 4, 5, 6])
    t = pick(r, ["This shape has {n} sides and {n} angles. What shape is it?", "This closed shape has {n} straight sides. What shape is it?", "This shape has {n} vertices and {n} straight sides. What shape is it?"])
    return Item(t.format(n=n), PNAME[n], [f"Match the number of sides to the name.", f"{n} sides: {PNAME[n]}."],
                [W(PNAME[3 + (n - 2) % 4], "matched the wrong number of sides")], FN("name_sides", n=n), qtype="conceptual", claim=f"Shape with {n} sides")


@fam("12")
def sn_how_many(r, L):
    ns = [pick(r, [3, 4, 5, 6]) for _ in range(4)]
    want = pick(r, ns)
    items, dg = row_d(r, ns)
    k = ns.count(want)
    return Item(f"How many of the shapes are {PNAME[want]}s?", k, [f"Count the sides of each shape. A {PNAME[want]} has {want} sides.", f"{k} of the shapes {'is a' if k == 1 else 'are'} {PNAME[want] if k == 1 else PNAME[want] + 's'}."],
                [W(k + 1, "counted a shape with a different number of sides"), W(4, "counted every shape"), W(k - 1 if k > 1 else 0, "missed one")],
                FN("count_named", items=items, sides=want), qtype="visual", diagram=dg)


@fam("012", mode="mc")
def sn_turned(r, L):
    n = pick(r, [3, 4, 5, 6])
    pts = poly_pts(r, n)
    alt = f"A closed shape with {n} straight sides, turned so that no side is flat on the bottom."
    nm = name(r)
    good = f"It is a {PNAME[n]}, because it still has {n} sides and {n} angles."
    bad = [f"It is not a {PNAME[n]}, because it is turned.", f"It is a {PNAME[3 + (n - 2) % 4]}, because it looks tilted.", f"It is a {PNAME[n]} only when one side is on the bottom."]
    it = mc_key(f"{nm} turned a shape so it looks tipped over. What is the shape now?", good, bad, ["Turning a shape does not change its sides or angles.", good], qtype="error-analysis", tags={"misconception"}, r=r,
                diagram=shape_d(pts, alt, "orange"))
    it.check = FN("turned_name", pts=pts)
    return it


@fam("2")
def sn_total(r, L):
    a, b = r.sample([3, 4, 5, 6], 2)
    c = pick(r, [3, 4, 5, 6])
    return Item(f"{name(r)} drew three shapes: {art(PNAME[a])}, {art(PNAME[b])}, {art(PNAME[c])}. How many sides do the three shapes have in all?", a + b + c,
                [f"{PNAME[a]}: {a}, {PNAME[b]}: {b}, {PNAME[c]}: {c}.", f"{a} + {b} + {c} = {a + b + c} sides."],
                [W(3, "counted the shapes"), W(a + b, "left out a shape"), W(a + b + c + 1, "counted one side twice")],
                FN("sides_total", names=[PNAME[a], PNAME[b], PNAME[c]]), qtype="multi-step", tags={"multistep"})


# ============================================================== S2 Drawing Shapes with Given Attributes
@fam("012", mode="mc")
def da_has(r, L):
    ns = r.sample([3, 4, 5, 6], 4)
    want = pick(r, ns)
    items, dg = row_d(r, ns)
    lab = "ABCD"[ns.index(want)]
    what = pick(r, ["sides", "angles", "vertices"])
    it = mc_key(f"Which shape has exactly {want} {what}?", lab, [x for x in "ABCD" if x != lab], [f"Count the {what} of each shape.", f"Shape {lab} has {want} {what}."], qtype="visual", diagram=dg, r=r)
    it.check = FN("shape_label", items=items, sides=want)
    return it


@fam("012", mode="sa")
def da_draw(r, L):
    n = pick(r, [3, 4, 5, 6])
    what = pick(r, ["sides", "angles", "corners"])
    return Item(f"{name(r)} draws a closed shape with {n} straight {what}. What kind of shape is it?", PNAME[n],
                [f"A closed shape with {n} {what} has {n} sides.", f"It is a {PNAME[n]}."], [W(PNAME[3 + (n - 2) % 4], "used the wrong number of sides")],
                FN("name_sides", n=n), qtype="conceptual")


@fam("012", mode="mc")
def da_must(r, L):
    n = pick(r, [3, 4, 5, 6])
    good = f"It has {n} angles."
    bad = [f"It has {n + 1} angles.", "All of its sides are the same length." if n != 4 else "It is a square.", "It has a curved side."]
    it = mc_key(f"A closed shape has {n} straight sides. Which must be true?", good, bad, ["Each corner of a closed shape joins two sides.", f"{n} sides means {n} angles."], qtype="conceptual", tags={"reasoning"}, r=r)
    it.check = FN("must_angles", n=n)
    return it


@fam("012")
def da_more(r, L):
    a, b = r.sample([3, 4, 5, 6], 2)
    if a < b:
        a, b = b, a
    return Item(f"How many more sides does a {PNAME[a]} have than a {PNAME[b]}?", a - b, [f"{PNAME[a]}: {a} sides. {PNAME[b]}: {b} sides.", f"{a} − {b} = {a - b}."],
                [W(a + b, "added the sides"), W(a, "gave the sides of one shape"), W(a - b + 1, "counted one extra")], FN("sides_more", big=PNAME[a], small=PNAME[b]), qtype="procedural")


@fam("12", mode="mc")
def da_quad(r, L):
    ns = [4] + r.sample([3, 5, 6], 3)
    r.shuffle(ns)
    items, dg = row_d(r, ns)
    lab = "ABCD"[ns.index(4)]
    it = mc_key("Which shape is a quadrilateral? (It might not be a square or a rectangle.)", lab, [x for x in "ABCD" if x != lab],
                ["Any closed shape with 4 straight sides is a quadrilateral.", f"Shape {lab} has 4 sides."], qtype="visual", tags={"misconception"}, diagram=dg, r=r)
    it.check = FN("shape_label", items=items, sides=4)
    return it


@fam("012", mode="mc")
def da_not(r, L):
    want = pick(r, [3, 4, 5, 6])
    other = pick(r, [x for x in [3, 4, 5, 6] if x != want])
    ns = [want] * 3 + [other]
    r.shuffle(ns)
    items, dg = row_d(r, ns)
    lab = "ABCD"[ns.index(other)]
    it = mc_key(f"Which shape is NOT a {PNAME[want]}?", lab, [x for x in "ABCD" if x != lab], [f"A {PNAME[want]} has {want} sides.", f"Shape {lab} has {other} sides."], qtype="visual", diagram=dg, r=r)
    it.check = FN("shape_label", items=items, sides=other)
    return it


@fam("2", mode="mc")
def da_error(r, L):
    nm = name(r)
    n = pick(r, [5, 6])
    good = f"No. A {PNAME[n]} can have sides of different lengths; it only needs {n} straight sides."
    bad = [f"Yes. All the sides of a {PNAME[n]} must be the same length.", f"No. A {PNAME[n]} has {n + 1} sides.", f"Yes. Only shapes with equal sides have names."]
    it = mc_key(f"{nm} drew a closed shape with {n} straight sides of different lengths. {nm} says it is not a {PNAME[n]} because the sides are not equal. Is {nm} right?", good, bad,
                ["Shapes are named by the number of sides and angles.", good], qtype="error-analysis", tags={"misconception"}, r=r)
    return it


# ============================================================== S3 Cubes and Their Faces
SOL = ["cube", "prism", "cylinder", "cone", "sphere", "pyramid"]
SOLNAME = {"prism": "box that is not a cube", "cube": "cube", "cylinder": "cylinder", "cone": "cone", "sphere": "sphere", "pyramid": "pyramid"}


def sol_row(r, kinds):
    items = [{"kind": k, "label": "ABCD"[i]} for i, k in enumerate(kinds)]
    alt = "Four solid shapes labeled A to D: " + "; ".join(f"{it['label']} is a {SOLNAME[it['kind']]}" for it in items) + "."
    return items, Diagram("solids", {"items": items}, alt)


@fam("012", mode="mc")
def cb_which(r, L):
    kinds = ["cube"] + r.sample(SOL[1:], 3)
    r.shuffle(kinds)
    items, dg = sol_row(r, kinds)
    lab = "ABCD"[kinds.index("cube")]
    it = mc_key("Which solid is a cube?", lab, [x for x in "ABCD" if x != lab], ["A cube has 6 faces that are all the same size square.", f"Solid {lab} is the cube."], qtype="visual", diagram=dg, r=r)
    it.check = FN("solid_label", items=items, kind="cube")
    return it


@fam("012")
def cb_parts(r, L):
    what = pick(r, ["faces", "edges", "vertices"]) if L else "faces"
    k = r.randint(1, 3) if L == 2 else 1
    v = {"faces": 6, "edges": 12, "vertices": 8}[what]
    q = f"How many {what} does a cube have?" if k == 1 else f"How many {what} do {k} cubes have in all?"
    return Item(q, v * k, [f"A cube has 6 faces, 12 edges, and 8 vertices.", f"{' + '.join([str(v)] * k)} = {v * k}." if k > 1 else f"A cube has {v} {what}."],
                [W(3 * k if v == 6 else 6 * k, "counted only the parts you can see in a picture"), W(4 * k, "counted the parts of one square"), W(v * k + v, "counted an extra cube")],
                FN("cube_parts", what=what, cubes=k), qtype="conceptual", claim=f"{what} on {k} cube(s)")


@fam("012", mode="sa")
def cb_face(r, L):
    return Item(pick(r, ["What shape is each face of a cube?", "A cube's faces are all the same shape. What shape are they?", "If you trace one face of a cube, what shape do you get?"]), "square",
                ["Each face of a cube is a flat square.", "The faces are squares."], [W("rectangle that is not a square", "thought of a box"), W("triangle", "thought of a pyramid"), W("circle", "thought of a cylinder")],
                FN("is_word", word="square"), qtype="conceptual")


@fam("012")
def cb_count(r, L):
    kinds = [pick(r, SOL) for _ in range(4)]
    need("cube" in kinds)
    items, dg = sol_row(r, kinds)
    k = kinds.count("cube")
    return Item("How many of the solids are cubes?", k, ["A cube has 6 equal square faces.", f"There {'is' if k == 1 else 'are'} {k}."],
                [W(k + kinds.count("prism"), "counted boxes that are not cubes"), W(4, "counted every solid"), W(k - 1 if k > 1 else k + 1, "miscounted")],
                FN("solid_count", items=items, kind="cube"), qtype="visual", diagram=dg)


@fam("12", mode="mc")
def cb_box(r, L):
    nm = name(r)
    good = "No. Its faces are not all the same size square."
    bad = ["Yes. Every box with 6 faces is a cube.", "Yes. It has 8 vertices, so it is a cube.", "No. A cube has 4 faces."]
    items, dg = sol_row(r, ["prism", "cube", "cylinder", "cone"])
    it = mc_key(f"{nm} says solid A is a cube because it has 6 faces. Is {nm} right?", good, bad, ["A cube's 6 faces are all squares of the same size.", "Solid A has rectangle faces that are not squares."], qtype="error-analysis", tags={"misconception"}, diagram=dg, r=r)
    return it


@fam("012")
def cb_stickers(r, L):
    k = r.randint(2, 4) if L < 2 else r.randint(3, 6)
    return Item(f"{name(r)} puts one sticker on every face of {k} cubes. How many stickers are used?", f"{6 * k} stickers",
                [f"Each cube has 6 faces.", f"{' + '.join(['6'] * k)} = {6 * k} stickers."],
                [W(f"{3 * k} stickers", "counted only the faces you can see"), W(f"{k + 6} stickers", "added the numbers"), W(f"{4 * k} stickers", "thought a cube has 4 faces")],
                FN("cube_parts", what="faces", cubes=k, unit="stickers"), qtype="word-problem", tags={"modeling"})


# ============================================================== S4 Partitioning Rectangles into Squares
def rc_(r, L):
    a = r.randint(2, 3) if L == 0 else r.randint(2, 5)
    b = r.randint(2, 4) if L == 0 else r.randint(3, 6)
    need(L < 2 or a * b >= 12)
    return a, b


def grid_d(a, b):
    alt = f"A rectangle partitioned into {a} rows and {b} columns of same-size squares."
    return Diagram("partition", {"shape": "rect", "cuts": "grid", "rows": a, "cols": b, "shade": []}, alt)


@fam("012")
def pr_count(r, L):
    a, b = rc_(r, L)
    return Item("How many same-size squares are in the rectangle?", a * b, [f"There are {a} rows of {b} squares.", f"{' + '.join([str(b)] * a)} = {a * b}."],
                [W(a + b, "added rows and columns"), W(2 * (a + b) - 4, "counted only the squares around the edge"), W(a * b - b, "missed a row")],
                EX("+".join([str(b)] * a)), qtype="visual", diagram=grid_d(a, b))


@fam("012")
def pr_rows(r, L):
    a, b = rc_(r, L)
    need(a != b)
    return Item("How many rows and how many columns of squares are in the rectangle?", f"{a} rows and {b} columns",
                ["Rows go across. Columns go up and down.", f"There are {a} rows and {b} columns."], [W(f"{b} rows and {a} columns", "mixed up rows and columns")],
                FN("rows_cols", rows=a, cols=b), qtype="visual", diagram=grid_d(a, b))


@fam("012")
def pr_text(r, L):
    a, b = rc_(r, L)
    return Item(f"{name(r)} partitions a rectangle into {a} rows with {b} same-size squares in each row. How many squares are there?", a * b,
                [f"Add {b} once for each row.", f"{' + '.join([str(b)] * a)} = {a * b}."], [W(a + b, "added rows and squares in a row"), W(a * b + b, "added an extra row"), W(a * b - 1, "made a counting mistake")],
                EX("+".join([str(b)] * a)), qtype="procedural", claim=f"{a} rows of {b} squares")


@fam("012", mode="mc")
def pr_equal(r, L):
    k = r.randint(3, 4)
    ws = [1] * k if r.random() < 0.5 else [1] * (k - 1) + [2]
    eq = len(set(ws)) == 1
    alt = f"A rectangle cut into {k} parts by up-and-down lines. " + ("All parts are the same size." if eq else "One part is wider than the others.")
    good = "Yes. All the parts are the same size." if eq else "No. One part is bigger than the others."
    bad = ["No. One part is bigger than the others." if eq else "Yes. All the parts are the same size.", "Yes. Any cut makes equal parts.", "No. Equal parts must be triangles."]
    it = mc_key(f"{name(r)} cut a rectangle into {k} parts. Are the parts equal in size?", good, bad, ["Equal parts are the same size.", good], qtype="visual", r=r,
                diagram=Diagram("partition", {"shape": "rect", "cuts": "v", "widths": ws, "shade": []}, alt))
    it.check = FN("equal_parts", widths=ws)
    return it


@fam("012")
def pr_more_row(r, L):
    a, b = rc_(r, L)
    return Item(f"A rectangle has {a} rows of {b} squares. {name(r)} adds 1 more row of the same squares. How many squares are there now?", (a + 1) * b,
                [f"Now there are {a + 1} rows of {b}.", f"{' + '.join([str(b)] * (a + 1))} = {(a + 1) * b}."], [W(a * b, "forgot the new row"), W(a * b + 1, "added one square instead of one row"), W(a + 1 + b, "added rows and columns")],
                EX("+".join([str(b)] * (a + 1))), qtype="multi-step", tags={"multistep"})


@fam("2")
def pr_missing(r, L):
    a, b = rc_(r, 2)
    return Item(f"A rectangle is partitioned into {a * b} same-size squares in {a} equal rows. How many squares are in each row?", b,
                [f"Find the number that adds {a} times to make {a * b}.", f"{' + '.join([str(b)] * a)} = {a * b}, so each row has {b}."],
                [W(a, "gave the number of rows"), W(a * b - a, "subtracted the rows"), W(b + 1, "made a counting mistake")], FN("rep_unknown", total=a * b, times=a), qtype="explain", tags={"reasoning"})


# ============================================================== S5 Halves, Thirds, and Fourths
SHARE = {2: "halves", 3: "thirds", 4: "fourths"}
ONE = {2: "half", 3: "third", 4: "fourth"}
NUMW = {1: "one", 2: "two", 3: "three", 4: "four"}


def part_d(r, n, shade=(), equal=True):
    shape = pick(r, ["circle", "rect"])
    if shape == "circle":
        angs = None if equal else ([120, 240] if n == 2 else [90, 120, 150] if n == 3 else [60, 90, 90, 120])
        data = {"shape": "circle", "n": n, "shade": list(shade)} if equal else {"shape": "circle", "angles": angs, "shade": list(shade)}
    else:
        ws = [1] * n if equal else ([1, 2] if n == 2 else [1, 1, 2] if n == 3 else [1, 1, 1, 2])
        data = {"shape": "rect", "cuts": "v", "widths": ws, "shade": list(shade)}
    alt = f"A {'circle' if shape == 'circle' else 'rectangle'} cut into {n} {'equal' if equal else 'unequal'} parts" + (f"; {len(shade)} {'part is' if len(shade) == 1 else 'parts are'} shaded." if shade else ".")
    return Diagram("partition", data, alt)


@fam("012")
def hf_name(r, L):
    n = pick(r, [2, 3, 4])
    return Item("The shape is cut into equal shares. What are the shares called: halves, thirds, or fourths?", SHARE[n], [f"Count the equal shares: {n}.", f"{n} equal shares are {SHARE[n]}."],
                [W(SHARE[{2: 3, 3: 4, 4: 2}[n]], "miscounted the shares")], FN("share_name", n=n), qtype="visual", diagram=part_d(r, n))


@fam("012")
def hf_shaded(r, L):
    n = pick(r, [2, 3, 4])
    k = 1 if L == 0 else r.randint(1, n - 1)
    ans = f"{NUMW[k]} {ONE[n] if k == 1 else SHARE[n]}"
    return Item("What part of the shape is shaded? Use words like one half or two thirds.", ans, [f"There are {n} equal shares, so each is one {ONE[n]}.", f"{k} {'share is' if k == 1 else 'shares are'} shaded: {ans}."],
                [W(f"{NUMW[n - k]} {ONE[n] if n - k == 1 else SHARE[n]}", "named the part that is not shaded") if n - k != k else W(f"one {ONE[{2: 3, 3: 4, 4: 2}[n]]}", "miscounted the shares"), W(f"one {ONE[{2: 3, 3: 4, 4: 2}[n]]}", "miscounted the shares")],
                FN("share_shaded", n=n, part=k), qtype="visual", diagram=part_d(r, n, shade=range(k)))


@fam("012", mode="sa")
def hf_equal(r, L):
    n = pick(r, [2, 3, 4])
    eq = r.random() < 0.5
    return Item(f"Is the shape cut into {SHARE[n]}? Write yes or no.", "yes" if eq else "no", ["Shares must be equal in size to be halves, thirds, or fourths.", f"The parts are {'equal' if eq else 'not equal'}, so the answer is {'yes' if eq else 'no'}."],
                [W("no" if eq else "yes", "counted the parts without checking that they are equal")], FN("is_word", word="yes" if eq else "no"), qtype="visual", tags={"misconception"},
                diagram=part_d(r, n, equal=eq))


@fam("012", mode="mc")
def hf_bigger(r, L):
    a, b = r.sample([2, 3, 4], 2)
    obj = pick(r, ["pizza", "sandwich", "cake", "pan of corn bread"])
    big = a if a < b else b
    good = f"one {ONE[big]}"
    bad = [f"one {ONE[a if big == b else b]}", "They are the same size.", "You cannot tell."]
    it = mc_key(f"Two {obj}s are the same size. One is cut into {SHARE[a]} and the other into {SHARE[b]}. Which is bigger: one {ONE[a]} or one {ONE[b]}?", good, bad,
                ["When the same whole is cut into more equal shares, each share is smaller.", f"One {ONE[big]} is bigger."], qtype="conceptual", tags={"reasoning", "misconception"}, r=r)
    it.check = FN("bigger_share", a=a, b=b)
    return it


@fam("012")
def hf_story(r, L):
    n = pick(r, [2, 3, 4])
    obj = pick(r, ["sandwich", "pizza", "granola bar", "pancake"])
    return Item(f"{NUMW[n].capitalize()} friends share {art(obj)} equally. What is each friend's share called?", f"one {ONE[n]}", [f"The {obj} is cut into {n} equal shares.", f"Each share is one {ONE[n]}."],
                [W(f"one {ONE[{2: 3, 3: 4, 4: 2}[n]]}", "used the wrong number of shares"), W(SHARE[n], "named all the shares instead of one")], FN("share_one", n=n), qtype="word-problem", tags={"modeling"})


@fam("12", mode="mc")
def hf_cuts(r, L):
    n = pick(r, [2, 3, 4])
    good = f"{n} equal shares"
    bad = [f"{n + 1} equal shares", f"{n} shares of any size", f"{n - 1 if n > 2 else 4} equal shares"]
    it = mc_key(f"To cut a rectangle into {SHARE[n]}, how many shares do you make?", good, bad, [f"{SHARE[n].capitalize()} means {n} equal shares.", good], qtype="conceptual", r=r)
    it.check = FN("cuts_for", n=n)
    return it


@fam("012")
def hf_colored(r, L):
    n = pick(r, [2, 3, 4])
    k = 1 if L == 0 else r.randint(1, n - 1)
    obj = pick(r, ["flag", "card", "paper square", "cracker", "tile"])
    nm = name(r)
    ans = f"{NUMW[k]} {ONE[n] if k == 1 else SHARE[n]}"
    return Item(f"{nm} cut a {obj} into {n} equal shares and colored {k} of them. What part of the {obj} did {nm} color?", ans,
                [f"{n} equal shares are {SHARE[n]}.", f"{k} {'share' if k == 1 else 'shares'} colored: {ans}."],
                [W(f"{NUMW[n - k]} {ONE[n] if n - k == 1 else SHARE[n]}" if n - k != k else f"one {ONE[{2: 3, 3: 4, 4: 2}[n]]}", "named the part not colored" if n - k != k else "used the wrong share name"),
                 W(f"{NUMW[k]} {ONE[{2: 3, 3: 4, 4: 2}[n]] if k == 1 else SHARE[{2: 3, 3: 4, 4: 2}[n]]}", "used the wrong share name")],
                FN("share_shaded", n=n, part=k), qtype="word-problem", tags={"modeling"})


@fam("012")
def hf_unshaded(r, L):
    n = pick(r, [2, 3, 4])
    k = r.randint(1, n - 1)
    u = n - k
    ans = f"{NUMW[u]} {ONE[n] if u == 1 else SHARE[n]}"
    return Item("What part of the shape is NOT shaded?", ans, [f"There are {n} equal shares and {k} {'is' if k == 1 else 'are'} shaded.", f"{u} {'is' if u == 1 else 'are'} not shaded: {ans}."],
                [W(f"{NUMW[k]} {ONE[n] if k == 1 else SHARE[n]}" if k != u else f"{NUMW[n]} {SHARE[n]}", "named the shaded part" if k != u else "named the whole"), W(f"one {ONE[{2: 3, 3: 4, 4: 2}[n]]}", "miscounted the shares")],
                FN("share_shaded", n=n, part=u), qtype="visual", diagram=part_d(r, n, shade=range(k)))


@fam("12")
def hf_again(r, L):
    form = pick(r, ["again", "inhalf"])
    if form == "again":
        return Item(f"{name(r)} cuts a rectangle into halves. Then each half is cut into 2 equal shares. What are the new shares called?", "fourths",
                    ["2 halves, each cut into 2, make 2 + 2 = 4 equal shares.", "4 equal shares are fourths."], [W("halves", "did not count the new cuts"), W("thirds", "counted 3 shares")],
                    FN("share_name", n=4), qtype="explain", tags={"reasoning"})
    obj = pick(r, ["pizza", "pie", "pan of brownies", "sandwich"])
    return Item(f"{art(obj).capitalize()} is cut into fourths. How many fourths make one half of the {obj}?", 2, ["4 fourths make the whole.", "Half of 4 fourths is 2 fourths."],
                [W(4, "gave the whole"), W(1, "thought one fourth is a half"), W(3, "made a counting mistake")], FN("whole_count", n=2), qtype="explain", tags={"reasoning"})


@fam("012")
def hf_how_many(r, L):
    n = pick(r, [2, 3, 4])
    k = 1 if L == 0 else r.randint(1, n)
    obj = pick(r, ["flag", "banner", "garden bed", "poster", "rug"])
    nm = name(r)
    words_ = f"{NUMW[k]} {ONE[n] if k == 1 else SHARE[n]}"
    return Item(f"{nm}'s {obj} is cut into {SHARE[n]}. {nm} wants to paint {words_} of it. How many shares should {nm} paint?", k,
                [f"{SHARE[n].capitalize()} means {n} equal shares.", f"{words_} means {k} of those shares."],
                [W(n, "painted every share") if k != n else W(n - 1, "left out a share"), W(n - k if n - k != k else k + 1, "counted the shares that are not painted"), W(k + 1, "counted one extra")],
                FN("more_shares", n=k, have=0), qtype="word-problem", tags={"modeling"})


# ============================================================== S6 Describing the Whole and Equal Shares
@fam("012")
def wh_count(r, L):
    n = pick(r, [2, 3, 4])
    return Item(f"How many {SHARE[n]} make one whole?", n, [f"{SHARE[n].capitalize()} split a whole into {n} equal shares.", f"{n} {SHARE[n]} make one whole."],
                [W(n - 1, "left out a share"), W(n + 1, "counted an extra share"), W(1, "thought one share is the whole")], FN("whole_count", n=n), qtype="conceptual")


@fam("012", mode="mc")
def wh_words(r, L):
    n = pick(r, [2, 3, 4])
    good = f"{NUMW[n]} {SHARE[n]}"
    bad = [f"{NUMW[n - 1]} {SHARE[n] if n - 1 > 1 else ONE[n]}", f"{NUMW[n]} {SHARE[{2: 3, 3: 4, 4: 2}[n]]}", f"one {ONE[n]}"]
    it = mc_key(f"A whole circle is cut into {SHARE[n]}. How can you describe the whole circle?", good, bad, [f"All {n} {SHARE[n]} together make the whole.", f"The whole is {good}."], qtype="conceptual", r=r)
    it.check = FN("whole_words", n=n)
    return it


@fam("012")
def wh_left(r, L):
    n = pick(r, [3, 4]) if L else pick(r, [2, 4])
    k = r.randint(1, n - 1)
    obj = pick(r, ["pizza", "pie", "sandwich"])
    nm = name(r)
    left = n - k
    ans = f"{NUMW[left]} {ONE[n] if left == 1 else SHARE[n]}"
    return Item(f"{art(obj).capitalize()} is cut into {SHARE[n]}. {nm} eats {NUMW[k]} {ONE[n] if k == 1 else SHARE[n]}. How much of the {obj} is left?", ans,
                [f"The whole is {NUMW[n]} {SHARE[n]}.", f"{n} − {k} = {left}, so {ans} {'is' if left == 1 else 'are'} left."],
                [W(f"{NUMW[k]} {ONE[n] if k == 1 else SHARE[n]}", "gave the part eaten") if k != left else W(f"{NUMW[n]} {SHARE[n]}", "gave the whole"), W(f"{NUMW[left]} {ONE[{2: 3, 3: 4, 4: 2}[n]] if left == 1 else SHARE[{2: 3, 3: 4, 4: 2}[n]]}", "used the wrong share name")],
                FN("share_shaded", n=n, part=left), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def wh_diff_shapes(r, L):
    n = pick(r, [2, 4])
    cut1, cut2 = ("diag2", "v") if n == 2 else ("diag4", "grid")
    alt = f"Two same-size squares. The first is cut into {SHARE[n]} by {'a diagonal line' if n == 2 else 'both diagonals'}, making triangles. The second is cut into {SHARE[n]} {'by an up-and-down line' if n == 2 else 'into 2 rows and 2 columns'}, making rectangles or squares."
    d2 = {"shape": "square", "cuts": "v", "widths": [1, 1], "shade": [0]} if n == 2 else {"shape": "square", "cuts": "grid", "rows": 2, "cols": 2, "shade": [0]}
    nm = name(r)
    good = f"They are the same size. Each is one {ONE[n]} of the same square, even though the shapes are different."
    bad = [f"The triangle {ONE[n]} is bigger.", f"The other {ONE[n]} is bigger because it is a {'rectangle' if n == 2 else 'square'}.", "They are not halves or fourths because their shapes are different."]
    it = mc_key(f"{nm} cut two same-size squares into {SHARE[n]} in different ways. Compare one {ONE[n]} from each square.", good, bad,
                ["Equal shares of the same whole can have different shapes.", good], qtype="explain", tags={"reasoning", "misconception"}, r=r,
                diagram=Diagram("partition_pair", {"a": {"shape": "square", "cuts": cut1, "shade": [0]}, "b": d2}, alt))
    return it


@fam("012")
def wh_more_needed(r, L):
    n = pick(r, [3, 4])
    k = r.randint(1, n - 1)
    return Item(f"{name(r)} has {NUMW[k]} {ONE[n] if k == 1 else SHARE[n]} of a puzzle mat. How many more {SHARE[n]} are needed to make the whole mat?", n - k,
                [f"The whole is {NUMW[n]} {SHARE[n]}.", f"{n} − {k} = {n - k}."], [W(n, "gave the number in the whole"), W(k, "gave the number already there"), W(n + k, "added instead of subtracting")],
                FN("more_shares", n=n, have=k), qtype="explain", tags={"reasoning"})


@fam("12", mode="mc")
def wh_error(r, L):
    nm = name(r)
    good = "No. A whole cut into 4 equal shares is four fourths, and each fourth is smaller than a half."
    bad = ["Yes. 4 is more than 2, so fourths are bigger.", "Yes. More pieces means bigger pieces.", "No. Fourths and halves are the same size."]
    it = mc_key(f"{nm} says one fourth of a pizza is bigger than one half of the same pizza because 4 is more than 2. Is {nm} right?", good, bad,
                ["More equal shares of the same whole means smaller shares.", "One half is bigger than one fourth."], qtype="error-analysis", tags={"misconception"}, r=r)
    return it


SKILLS = {
    1: dict(name="Naming Shapes by Sides and Angles", fams=[sn_name, sn_count, sn_which, sn_riddle, sn_how_many, sn_turned, sn_total]),
    2: dict(name="Drawing Shapes with Given Attributes", fams=[da_has, da_draw, da_must, da_more, da_quad, da_not, da_error]),
    3: dict(name="Cubes and Their Faces", fams=[cb_which, cb_parts, cb_face, cb_count, cb_box, cb_stickers]),
    4: dict(name="Partitioning Rectangles into Squares", fams=[pr_count, pr_rows, pr_text, pr_equal, pr_more_row, pr_missing]),
    5: dict(name="Halves, Thirds, and Fourths", fams=[hf_name, hf_shaded, hf_equal, hf_bigger, hf_story, hf_cuts, hf_colored, hf_unshaded, hf_again, hf_how_many]),
    6: dict(name="Describing the Whole and Equal Shares", fams=[wh_count, wh_words, wh_left, wh_diff_shapes, wh_more_needed, wh_error]),
}
