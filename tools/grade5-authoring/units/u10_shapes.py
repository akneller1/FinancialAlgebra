"""Unit 10: Geometry and Classifying Shapes (classifying-shapes).

Definitions used (and stated to students where they matter): a trapezoid has exactly one pair of parallel sides in every
figure shown here, and no question depends on the inclusive or exclusive trapezoid / kite definition."""
from g5lib import *
import math

UNIT_ID = "classifying-two-dimensional-figures"

# triangles: points, side lengths (rounded for classification), angles in degrees
TRI = {
    "equilateral": dict(pts=[[0, 0], [4, 0], [2, 3.464]], sides=[4, 4, 4], angles=[60, 60, 60], ticks=[[0, 1], [1, 1], [2, 1]]),
    "isosceles acute": dict(pts=[[0, 0], [4, 0], [2, 5]], sides=[4, 5.39, 5.39], angles=[68, 68, 44], ticks=[[1, 1], [2, 1]]),
    "isosceles right": dict(pts=[[0, 0], [4, 0], [0, 4]], sides=[4, 5.66, 4], angles=[90, 45, 45], ticks=[[0, 1], [2, 1]], right=[0]),
    "isosceles obtuse": dict(pts=[[0, 0], [6, 0], [3, 1.4]], sides=[6, 3.31, 3.31], angles=[25, 25, 130], ticks=[[1, 1], [2, 1]]),
    "scalene right": dict(pts=[[0, 0], [4, 0], [0, 3]], sides=[4, 5, 3], angles=[90, 37, 53], right=[0]),
    "scalene obtuse": dict(pts=[[0, 0], [6, 0], [-2, 2.5]], sides=[6, 8.4, 3.2], angles=[129, 17, 34]),
    "scalene acute": dict(pts=[[0, 0], [6, 0], [2, 4]], sides=[6, 5.66, 4.47], angles=[63, 45, 72]),
}
# quadrilaterals with guaranteed properties
QUAD = {
    "square": dict(pts=[[0, 0], [4, 0], [4, 4], [0, 4]], q=dict(parallel_pairs=2, all_sides_equal=True, right_angles=True), ticks=[[0, 1], [1, 1], [2, 1], [3, 1]], right=[0, 1, 2, 3], arrows=[[0, 1], [2, 1], [1, 2], [3, 2]]),
    "rectangle": dict(pts=[[0, 0], [6, 0], [6, 3], [0, 3]], q=dict(parallel_pairs=2, all_sides_equal=False, right_angles=True), ticks=[[0, 1], [2, 1], [1, 2], [3, 2]], right=[0, 1, 2, 3]),
    "rhombus": dict(pts=[[0, 0], [5, 0], [8, 4], [3, 4]], q=dict(parallel_pairs=2, all_sides_equal=True, right_angles=False), ticks=[[0, 1], [1, 1], [2, 1], [3, 1]], arrows=[[0, 1], [2, 1], [1, 2], [3, 2]]),
    "parallelogram": dict(pts=[[0, 0], [5, 0], [6.5, 3], [1.5, 3]], q=dict(parallel_pairs=2, all_sides_equal=False, right_angles=False), ticks=[[0, 1], [2, 1], [1, 2], [3, 2]], arrows=[[0, 1], [2, 1], [1, 2], [3, 2]]),
    "trapezoid": dict(pts=[[0, 0], [7, 0], [5, 3], [1.5, 3]], q=dict(parallel_pairs=1, all_sides_equal=False, right_angles=False), arrows=[[0, 1], [2, 1]]),
    "kite": dict(pts=[[0, 0], [2, -2.5], [4, 0], [2, 1.2]], q=dict(parallel_pairs=0, all_sides_equal=False, right_angles=False, kite=True), ticks=[[0, 1], [1, 1], [2, 2], [3, 2]]),
    "quadrilateral": dict(pts=[[0, 0], [5, 0.6], [4.3, 3.4], [0.8, 2.2]], q=dict(parallel_pairs=0, all_sides_equal=False, right_angles=False)),
}
POLY = {3: "triangle", 4: "quadrilateral", 5: "pentagon", 6: "hexagon", 8: "octagon"}
SAFE_NAMES = ["square", "rectangle", "rhombus", "parallelogram", "quadrilateral"]


def regular(n, irregular=False, r=None):
    pts = []
    for i in range(n):
        a = math.pi / 2 + 2 * math.pi * i / n
        rad = 3 * (1 + (0.35 if irregular and i % 2 else 0))
        pts.append([round(rad * math.cos(a), 3), round(rad * math.sin(a), 3)])
    return pts


def quad_diag(name, extra_alt=""):
    d = QUAD[name]
    data = {"pts": d["pts"], "ticks": d.get("ticks", []), "arrows": d.get("arrows", []), "right": d.get("right", []), "fill": pick_fill(name)}
    marks = []
    if d.get("right"):
        marks.append(f"{len(d['right'])} right-angle marks")
    if d.get("arrows"):
        marks.append(f"{len(d['arrows']) // 2} pair{'s' if len(d['arrows']) > 2 else ''} of parallel sides marked with arrows")
    if d.get("ticks"):
        marks.append("tick marks showing " + ("all four sides equal" if d["q"]["all_sides_equal"] else "which sides are equal"))
    alt = f"A four-sided figure with " + (", ".join(marks) if marks else "no equal sides, no parallel sides and no right angles marked") + "." + extra_alt
    return Diagram("shape", data, alt)


def pick_fill(name):
    return {"square": "blue", "rectangle": "green", "rhombus": "pink", "parallelogram": "orange", "trapezoid": "purple", "kite": "teal", "quadrilateral": "yellow"}.get(name, "blue")


# ============================================================== S1 Polygons and Their Attributes
@fam("012", mode="mc")
def pa_name(r, L):
    n = pick(r, list(POLY))
    irr = r.random() < 0.5
    good = POLY[n]
    bad = [v for k, v in POLY.items() if k != n]
    r.shuffle(bad)
    alt = f"A {'regular' if not irr else 'non-regular'} polygon with {n} sides."
    return mc_key("What is the name of this polygon?", good, bad[:3], [f"Count the sides: {n}.", f"A polygon with {n} sides is a {good}."], r=r, qtype="visual",
                  diagram=Diagram("shape", {"pts": regular(n, irr), "fill": pick(r, ["blue", "green", "orange", "pink"])}, alt))


@fam("012")
def pa_parallel(r, L):
    name = pick(r, ["square", "rectangle", "rhombus", "parallelogram", "trapezoid", "kite", "quadrilateral"])
    d = QUAD[name]
    shown = dict(d)
    if name == "rectangle":
        shown = dict(d, arrows=[[0, 1], [2, 1], [1, 2], [3, 2]])
    k = len(shown.get("arrows", [])) // 2
    data = {"pts": d["pts"], "arrows": shown.get("arrows", []), "ticks": [], "right": d.get("right", []), "fill": pick_fill(name)}
    alt = f"A quadrilateral with {k} pair{'s' if k != 1 else ''} of sides marked parallel with arrows." if k else "A quadrilateral with no sides marked parallel."
    return Item("Arrows mark sides that are parallel. How many pairs of parallel sides does the figure have?", str(k),
                ["Sides with the same arrow marks are parallel.", f"There {'is' if k == 1 else 'are'} {k} pair{'s' if k != 1 else ''}."],
                [W(str(k * 2), "counted parallel sides instead of pairs"), W(str((k + 1) % 3), "miscounted the arrow marks"), W("4", "counted all the sides")],
                FN("count_marks", data=data, what="parallel_pairs"), qtype="visual", diagram=Diagram("shape", data, alt))


@fam("012")
def pa_right(r, L):
    name = pick(r, list(QUAD))
    d = QUAD[name]
    k = len(d.get("right", []))
    alt = f"A quadrilateral with {k} right-angle mark{'s' if k != 1 else ''}."
    data = {"pts": d["pts"], "right": d.get("right", []), "fill": pick_fill(name)}
    return Item("How many right angles are marked in the figure?", str(k), ["A small square at a corner marks a right angle.", f"There {'is' if k == 1 else 'are'} {k}."],
                [W(str(4 - k) if 4 - k != k else "2", "counted the corners without marks"), W("4", "assumed every corner is a right angle") if k != 4 else W("0", "did not see the marks"), W(str(k + 1), "miscounted")],
                FN("count_marks", data=data, what="right"), qtype="visual", diagram=Diagram("shape", data, alt))


@fam("012", mode="mc")
def pa_regular(r, L):
    n = pick(r, [5, 6, 8])
    items = [{"pts": regular(n), "label": "A"}, {"pts": regular(n, True), "label": "B"}, {"pts": QUAD["rectangle"]["pts"], "label": "C", "right": [0, 1, 2, 3]},
             {"pts": TRI["scalene acute"]["pts"], "label": "D"}]
    order = [0, 1, 2, 3]
    r.shuffle(order)
    labs = "ABCD"
    shown = [dict(items[i], label=labs[k]) for k, i in enumerate(order)]
    good = labs[order.index(0)]
    alt = "Four shapes labeled A to D: " + "; ".join(f"{s['label']}: " + ["a regular polygon", "a polygon with unequal sides", "a rectangle", "a scalene triangle"][order[k]] for k, s in enumerate(shown)) + "."
    return mc_key("A regular polygon has all sides equal and all angles equal. Which shape is a regular polygon?", f"Shape {good}", [f"Shape {x}" for x in labs if x != good],
                  ["Check every side and every angle.", f"Shape {good} has all sides and all angles equal."], r=r, qtype="visual",
                  diagram=Diagram("shape_row", {"items": shown}, alt))


@fam("012", mode="mc")
def pa_attribute(r, L):
    items = [("Which attribute do ALL quadrilaterals have?", "four sides and four angles", ["four right angles", "two pairs of parallel sides", "four equal sides"]),
             ("Which attribute do ALL parallelograms have?", "two pairs of parallel sides", ["four right angles", "four equal sides", "exactly one pair of parallel sides"]),
             ("Which attribute do ALL rectangles have?", "four right angles", ["four equal sides", "no parallel sides", "exactly three right angles"]),
             ("Which attribute do ALL rhombuses have?", "four equal sides", ["four right angles", "no parallel sides", "exactly one pair of equal sides"]),
             ("What does it mean for two sides to be perpendicular?", "They meet to form a right angle.", ["They never meet.", "They are the same length.", "They form an obtuse angle."]),
             ("What does it mean for two sides to be parallel?", "They are always the same distance apart and never meet.", ["They meet at a right angle.", "They are the same length.", "They cross in the middle."])]
    q, good, bad = pick(r, items)
    return mc_key(q, good, bad, ["Think about the definition of the category.", good], r=r, qtype="conceptual")


@fam("012")
def pa_sides(r, L):
    n = pick(r, list(POLY))
    k = r.randint(2, 6)
    return Item(f"{name(r)} draws {k} {POLY[n]}s. How many sides are there in all?", str(n * k), [f"{'An' if POLY[n][0] in 'aeiou' else 'A'} {POLY[n]} has {n} sides.", f"{k} × {n} = {n * k} sides."],
                [W(str(n + k), "added instead of multiplying"), W(str(n), "counted one shape"), W(str((n + 1) * k), "used the wrong number of sides")],
                FN("poly_sides", name=POLY[n], count=k), qtype="real-world")


# ============================================================== S2 Classifying Triangles
def tri_from_angles(A, B, base=6.0):
    """Vertices for a triangle with angles A (at vertex 0) and B (at vertex 1) on a horizontal base."""
    C = 180 - A - B
    ra, rb, rc = math.radians(A), math.radians(B), math.radians(C)
    side_b = base * math.sin(rb) / math.sin(rc)      # side from vertex 0 to vertex 2
    p2 = [round(side_b * math.cos(ra), 3), round(side_b * math.sin(ra), 3)]
    pts = [[0, 0], [base, 0], p2]
    s0 = base
    s1 = math.dist(pts[1], pts[2])
    s2 = math.dist(pts[2], pts[0])
    return pts, [round(s0, 1), round(s1, 1), round(s2, 1)], [A, B, C]


def tri_from_sides(a, b, c):
    """Vertices for a triangle with side0 = a (base), side1 = b (vertex1 to vertex2), side2 = c (vertex2 to vertex0)."""
    x = (c * c - b * b + a * a) / (2 * a)
    y = math.sqrt(max(c * c - x * x, 0))
    return [[0, 0], [a, 0], [round(x, 3), round(y, 3)]]


def rand_angles(r, kind):
    if kind == "right":
        a = r.randint(20, 70)
        return [90, a, 90 - a]
    if kind == "obtuse":
        big = r.randint(95, 150)
        a = r.randint(10, 180 - big - 10)
        return [big, a, 180 - big - a]
    while True:
        a, b = r.randint(35, 85), r.randint(35, 85)
        c = 180 - a - b
        if 30 < c < 90:
            return [a, b, c]


def rand_sides(r, kind, L):
    hi = 9 if L == 0 else 20
    while True:
        if kind == "equilateral":
            s = r.randint(2, hi)
            return [s, s, s]
        if kind == "isosceles":
            s, t = r.randint(2, hi), r.randint(2, hi)
            if s != t and t < 2 * s:
                return [t, s, s]
        else:
            x = sorted(r.sample(range(2, hi + 1), 3))
            if x[0] + x[1] > x[2]:
                r.shuffle(x)
                return x


@fam("012", mode="sa")
def tri_sides(r, L):
    kind = pick(r, ["equilateral", "isosceles", "scalene"])
    s = rand_sides(r, kind, L)
    pts = tri_from_sides(*s)
    unit = pick(r, ["cm", "in", "ft"])
    labels = [[i, f"{x} {unit}"] for i, x in enumerate(s)]
    data = {"pts": pts, "side_labels": labels, "fill": "orange"}
    alt = "A triangle with side lengths " + ", ".join(t for _, t in labels) + "."
    return Item("Classify the triangle by its sides: equilateral, isosceles, or scalene?", kind,
                ["Equilateral: 3 equal sides. Isosceles: exactly 2 equal sides. Scalene: no equal sides.", f"The sides are {', '.join(map(str, s))}, so it is {kind}."],
                [W("isosceles" if kind != "isosceles" else "scalene", "counted the equal sides incorrectly"), W("equilateral" if kind != "equilateral" else "isosceles", "assumed all sides are equal"),
                 W("acute", "classified by angles instead of sides")],
                FN("tri", sides=s, by="sides"), qtype="visual", diagram=Diagram("shape", data, alt))


@fam("012", mode="sa")
def tri_angles(r, L):
    kind = pick(r, ["acute", "right", "obtuse"])
    a = rand_angles(r, kind)
    order = a[:]
    r.shuffle(order)
    return Item(f"A triangle has angles of {order[0]}°, {order[1]}°, and {order[2]}°. Classify it by its angles: acute, right, or obtuse?", kind,
                ["Right: one 90° angle. Obtuse: one angle greater than 90°. Acute: all angles less than 90°.", f"The largest angle is {max(a)}°, so it is {kind}."],
                [W("acute" if kind != "acute" else "obtuse", "looked at the smallest angle instead of the largest"), W("right" if kind != "right" else "acute", "guessed from the numbers"), W("isosceles", "classified by sides instead of angles")],
                FN("tri", angles=a, by="angles"), qtype="conceptual")


@fam("012", mode="sa")
def tri_drawn(r, L):
    kind = pick(r, ["acute", "right", "obtuse"])
    a = rand_angles(r, kind)
    pts, sides, angs = tri_from_angles(a[0], a[1])
    data = {"pts": pts, "angle_labels": [[i, f"{angs[i]}°"] for i in range(3)], "right": [i for i in range(3) if angs[i] == 90], "fill": "pink"}
    alt = "A triangle with angles labeled " + ", ".join(f"{x}°" for x in angs) + "."
    return Item("Classify the triangle by its angles: acute, right, or obtuse?", kind, [f"The angles are {', '.join(f'{x}°' for x in angs)}.", f"The largest is {max(angs)}°, so it is {kind}."],
                [W("acute" if kind != "acute" else "right", "judged by how the triangle looks instead of the angle measures"), W("obtuse" if kind != "obtuse" else "acute", "misread the largest angle")],
                FN("tri", angles=angs, by="angles"), qtype="visual", diagram=Diagram("shape", data, alt))


@fam("12")
def tri_both(r, L):
    ang_kind = pick(r, ["acute", "right", "obtuse"])
    side_kind = pick(r, ["isosceles", "scalene"])
    if side_kind == "isosceles":
        base_ang = {"acute": r.randint(46, 80), "right": 45, "obtuse": r.randint(15, 40)}[ang_kind]
        A = B = base_ang
    else:
        A, B, _ = rand_angles(r, ang_kind)
        if ang_kind != "acute":
            big = max(A, B, 180 - A - B)
            rest = sorted([A, B, 180 - A - B])[:2]
            A, B = rest[0], rest[1]    # put the large angle at the top vertex
    pts, sides, angs = tri_from_angles(A, B)
    need(max(angs) < 180 and min(angs) > 0)
    need(ang_kind == ("right" if 90 in angs else "obtuse" if max(angs) > 90 else "acute"))
    need((len(set(sides)) == 2) if side_kind == "isosceles" else (len(set(sides)) == 3))
    ans = f"{ang_kind} {side_kind}"
    labels = [[i, f"{s}"] for i, s in enumerate(sides)]
    data = {"pts": pts, "right": [i for i in range(3) if angs[i] == 90], "side_labels": labels, "angle_labels": [[i, f"{angs[i]}°"] for i in range(3)], "fill": "green"}
    alt = "A triangle with side lengths " + ", ".join(t for _, t in labels) + " units and angles " + ", ".join(f"{x}°" for x in angs) + "."
    return Item("Classify the triangle by its angles AND its sides (for example, “acute scalene”). Side lengths are in units.", ans,
                [f"Largest angle {max(angs)}°: {ang_kind}. Sides {', '.join(map(str, sides))}: {'two are equal' if side_kind == 'isosceles' else 'none are equal'}, so {side_kind}.", f"It is {ans}."],
                [W(f"{ang_kind} {'scalene' if side_kind == 'isosceles' else 'isosceles'}", "misjudged the equal sides"), W(f"{'acute' if ang_kind != 'acute' else 'obtuse'} {side_kind}", "misjudged the angles"),
                 W(f"{side_kind} {ang_kind}", "wrote the words in the wrong order")],
                FN("tri_both", sides=sides, angles=angs), qtype="visual", diagram=Diagram("shape", data, alt))


@fam("012", mode="mc")
def tri_row(r, L):
    kinds = r.sample(list(TRI), 4)
    target = pick(r, ["right", "obtuse", "equilateral", "scalene"] if L else ["right", "equilateral"])
    def has(k):
        a = TRI[k]["angles"]
        return {"right": 90 in a, "obtuse": max(a) > 90, "equilateral": k == "equilateral", "scalene": k.startswith("scalene")}[target]
    hits = [k for k in kinds if has(k)]
    need(len(hits) == 1)
    labs = "ABCD"
    items = [{"pts": TRI[k]["pts"], "label": labs[i], "ticks": TRI[k].get("ticks", []), "right": TRI[k].get("right", [])} for i, k in enumerate(kinds)]
    good = f"Triangle {labs[kinds.index(hits[0])]}"
    alt = "Four triangles labeled A to D: " + "; ".join(f"{labs[i]} is {k}" for i, k in enumerate(kinds)) + "."
    return mc_key(f"Which triangle is {target}?", good, [f"Triangle {x}" for x in labs if f"Triangle {x}" != good],
                  ["Use the tick marks and right-angle marks.", f"{good} is {target}."], r=r, qtype="visual", diagram=Diagram("shape_row", {"items": items}, alt))


@fam("012", mode="mc")
def tri_can(r, L):
    items = [("Can a triangle have two right angles?", "No. Two right angles would make the two sides parallel, so they could never meet to close the triangle.", ["Yes, if the third angle is small.", "Yes, every square has two.", "No, because triangles have no angles."]),
             ("Can a right triangle also be isosceles?", "Yes. It can have a right angle and two equal sides.", ["No. Right triangles are always scalene.", "No. Isosceles triangles are always acute.", "Yes, but only if all three sides are equal."]),
             ("Can an obtuse triangle also be equilateral?", "No. An equilateral triangle has three equal angles, so none can be obtuse.", ["Yes, if the sides are long enough.", "Yes, every equilateral triangle is obtuse.", "No, because obtuse triangles have no equal sides."]),
             ("Can a scalene triangle be a right triangle?", "Yes. It can have a right angle and three different side lengths.", ["No. Right triangles always have two equal sides.", "No. Scalene triangles are always obtuse.", "Yes, but only if it has two right angles."])]
    q, good, bad = pick(r, items)
    return mc_key(q, good, bad, ["Use the definitions of each category.", good], r=r, qtype="explain", tags={"reasoning"})


# ============================================================== S3 Classifying Quadrilaterals
@fam("012", mode="sa")
def q_most(r, L):
    name_ = pick(r, list(QUAD))
    return Item("What is the most specific name for this quadrilateral? Use the marks: tick marks show equal sides, arrows show parallel sides, and squares show right angles.", name_,
                [describe(name_), f"The most specific name is {name_}."],
                [W({"square": "rectangle", "rectangle": "parallelogram", "rhombus": "square", "parallelogram": "rectangle", "trapezoid": "parallelogram", "kite": "rhombus", "quadrilateral": "trapezoid"}[name_], "did not check every mark"),
                 W("quadrilateral" if name_ != "quadrilateral" else "square", "gave a name that is too general" if name_ != "quadrilateral" else "assumed equal sides")],
                FN("quad_is", q=QUAD[name_]["q"], most=True), qtype="visual", diagram=quad_diag(name_))


def describe(n):
    q = QUAD[n]["q"]
    s = [f"{q['parallel_pairs']} pair{'s' if q['parallel_pairs'] != 1 else ''} of parallel sides"]
    s.append("4 right angles" if q["right_angles"] else "no right angles")
    s.append("4 equal sides" if q["all_sides_equal"] else ("2 pairs of equal adjacent sides" if q.get("kite") else "not all sides equal"))
    return "It has " + ", ".join(s) + "."


@fam("012", mode="mc")
def q_also(r, L):
    name_ = pick(r, ["square", "rectangle", "rhombus"])
    q = QUAD[name_]["q"]
    good = {"square": pick(r, ["rectangle", "rhombus", "parallelogram"]), "rectangle": "parallelogram", "rhombus": "parallelogram"}[name_]
    bad_pool = [n for n in SAFE_NAMES + ["kite", "trapezoid"] if n not in (name_, good) and n not in ("kite", "trapezoid")]
    bad_pool = [n for n in bad_pool if n not in quad_names_gen(q)] + ["triangle", "pentagon"]
    return mc_key(f"The figure is a {name_}. Which other name also describes it?", good, bad_pool[:3],
                  [describe(name_), f"Every {name_} is also a {good}."], r=r, qtype="visual", diagram=quad_diag(name_))


def quad_names_gen(q):
    out = {"quadrilateral"}
    if q["parallel_pairs"] == 2:
        out.add("parallelogram")
        if q["right_angles"]:
            out.add("rectangle")
        if q["all_sides_equal"]:
            out.add("rhombus")
        if q["right_angles"] and q["all_sides_equal"]:
            out.add("square")
    return out


@fam("012", mode="sa")
def q_from_props(r, L):
    name_ = pick(r, ["square", "rectangle", "rhombus", "parallelogram", "trapezoid"])
    props = {"square": "four right angles and four equal sides", "rectangle": "four right angles and two pairs of parallel sides, but its sides are not all equal",
             "rhombus": "four equal sides but no right angles", "parallelogram": "two pairs of parallel sides, no right angles, and sides that are not all equal",
             "trapezoid": "exactly one pair of parallel sides"}[name_]
    return Item(f"A quadrilateral has {props}. What is the most specific name for it?", name_, [describe(name_), f"It is a {name_}."],
                [W({"square": "rhombus", "rectangle": "square", "rhombus": "square", "parallelogram": "rectangle", "trapezoid": "parallelogram"}[name_], "matched only some of the properties"), W("quadrilateral", "gave a name that is too general")],
                FN("quad_is", q=QUAD[name_]["q"], most=True), qtype="conceptual")


@fam("012", mode="mc")
def q_which_shape(r, L):
    target = pick(r, ["square", "rectangle", "rhombus", "trapezoid", "parallelogram"])
    others = r.sample([n for n in QUAD if n != target and not (target == "parallelogram" and n in ("rectangle", "rhombus", "square"))], 3)
    kinds = [target] + others
    r.shuffle(kinds)
    labs = "ABCD"
    items = [{"pts": QUAD[k]["pts"], "label": labs[i], "ticks": QUAD[k].get("ticks", []), "arrows": QUAD[k].get("arrows", []), "right": QUAD[k].get("right", [])} for i, k in enumerate(kinds)]
    good = f"Shape {labs[kinds.index(target)]}"
    alt = "Four quadrilaterals labeled A to D with marks: " + "; ".join(f"{labs[i]} is a {k}" for i, k in enumerate(kinds)) + "."
    return mc_key(f"Which shape is a {target}{' (with no right angles)' if target in ('parallelogram', 'rhombus') else ''}?", good, [f"Shape {x}" for x in labs if f"Shape {x}" != good],
                  ["Read the marks on each shape.", f"{good} is a {target}."], r=r, qtype="visual", diagram=Diagram("shape_row", {"items": items}, alt))


@fam("012")
def q_count_sides(r, L):
    name_ = pick(r, ["square", "rhombus", "rectangle", "parallelogram"])
    s = r.randint(3, 15)
    t = r.randint(3, 15)
    need(s != t)
    if name_ in ("square", "rhombus"):
        per = 4 * s
        q = f"A {name_} has one side that is {s} inches long. What is its perimeter?"
        steps = [f"All four sides of a {name_} are equal.", f"4 × {s} = {per} inches."]
        chk = FN("quad_perimeter", kind=name_, s=s)
        bad = [W(f"{s * 2} inches", "counted only two sides"), W(f"{s * s} inches", "found the area"), W(f"{s + 4} inches", "added 4")]
    else:
        per = 2 * (s + t)
        q = f"A {name_} has sides of {s} inches and {t} inches. What is its perimeter?"
        steps = [f"Opposite sides of a {name_} are equal.", f"2 × ({s} + {t}) = {per} inches."]
        chk = FN("quad_perimeter", kind=name_, s=s, t=t)
        bad = [W(f"{s + t} inches", "added only two sides"), W(f"{s * t} inches", "multiplied the sides"), W(f"{4 * s} inches", "assumed all sides are equal")]
    return Item(q, f"{per} inches", steps, bad, chk, qtype="real-world", tags={"connections"})


# ============================================================== S4 Shape Hierarchies
CATS = ["squares", "rectangles", "rhombuses", "parallelograms", "quadrilaterals"]
SUB = {"squares": {"rectangles", "rhombuses", "parallelograms", "quadrilaterals"}, "rectangles": {"parallelograms", "quadrilaterals"},
       "rhombuses": {"parallelograms", "quadrilaterals"}, "parallelograms": {"quadrilaterals"}, "quadrilaterals": set()}


@fam("012", mode="mc")
def h_all_are(r, L):
    trues = [(a, b) for a in CATS for b in SUB[a]]
    falses = [(a, b) for a in CATS for b in CATS if a != b and b not in SUB[a]]
    a, b = pick(r, trues)
    good = f"All {a} are {b}."
    bad = [f"All {x} are {y}." for x, y in r.sample(falses, 3)]
    return mc_key("Which statement is true?", good, bad, ["Members of a category belong to every larger category above it.", good], r=r, qtype="conceptual", tags={"reasoning"})


@fam("012", mode="mc")
def h_false(r, L):
    trues = [(a, b) for a in CATS for b in SUB[a]]
    falses = [(a, b) for a in CATS for b in CATS if a != b and b not in SUB[a] and a != "quadrilaterals"]
    a, b = pick(r, falses)
    good = f"All {a} are {b}."
    bad = [f"All {x} are {y}." for x, y in r.sample(trues, 3)]
    return Item("Which statement is FALSE?", good, [f"Not every one of the {a} has the properties of {b}.", f"So “{good}” is false."],
                check=FN("all_are_false"), options=[(good, True)] + [(x, False) for x in bad], mode="mc", qtype="explain", tags={"reasoning"})


@fam("012", mode="mc")
def h_inherit(r, L):
    items = [("All rectangles have four right angles. Squares are rectangles. What must be true?", "All squares have four right angles.", ["Some squares have no right angles.", "All rectangles are squares.", "Squares have exactly two right angles."]),
             ("All parallelograms have two pairs of parallel sides. Rhombuses are parallelograms. What must be true?", "All rhombuses have two pairs of parallel sides.", ["All parallelograms are rhombuses.", "Rhombuses have no parallel sides.", "Rhombuses have exactly one pair of parallel sides."]),
             ("All rhombuses have four equal sides. Squares are rhombuses. What must be true?", "All squares have four equal sides.", ["All rhombuses are squares.", "Squares have only two equal sides.", "Some squares have no equal sides."]),
             ("All quadrilaterals have four sides. Trapezoids are quadrilaterals. What must be true?", "All trapezoids have four sides.", ["All quadrilaterals are trapezoids.", "Trapezoids have three sides.", "Trapezoids have four right angles."]),
             ("Opposite sides of every parallelogram are equal. A rectangle is a parallelogram. What must be true?", "Opposite sides of every rectangle are equal.", ["All four sides of every rectangle are equal.", "Every parallelogram is a rectangle.", "A rectangle has no equal sides."])]
    q, good, bad = pick(r, items)
    return mc_key(q, good, bad, ["Attributes of a category belong to every subcategory.", good], r=r, qtype="explain", tags={"reasoning"})


@fam("012", mode="mc")
def h_counter(r, L):
    items = [("Lena says, “All rhombuses are squares.” Which shape shows that this is wrong?", "a rhombus with no right angles", ["a square", "a rectangle with unequal sides", "a triangle"]),
             ("Omar says, “All rectangles are squares.” Which shape shows that this is wrong?", "a rectangle whose sides are not all equal", ["a square", "a rhombus", "a pentagon"]),
             ("Kai says, “All parallelograms are rectangles.” Which shape shows that this is wrong?", "a parallelogram with no right angles", ["a square", "a rectangle", "a circle"]),
             ("Uma says, “All quadrilaterals are parallelograms.” Which shape shows that this is wrong?", "a quadrilateral with no parallel sides", ["a square", "a rhombus", "a rectangle"])]
    q, good, bad = pick(r, items)
    return mc_key(q, good, bad, ["A counterexample is one shape that is in the first group but not the second.", good], r=r, qtype="explain", tags={"reasoning", "error-analysis"})


@fam("012", mode="mc")
def h_shared(r, L):
    items = [("Which attribute do parallelograms, rectangles, rhombuses, and squares ALL share?", "two pairs of parallel sides", ["four right angles", "four equal sides", "exactly one pair of parallel sides"]),
             ("Which attribute do rectangles and squares share that rhombuses do not always have?", "four right angles", ["four equal sides", "two pairs of parallel sides", "four sides"]),
             ("Which attribute do rhombuses and squares share that rectangles do not always have?", "four equal sides", ["four right angles", "two pairs of parallel sides", "four angles"])]
    q, good, bad = pick(r, items)
    return mc_key(q, good, bad, ["Compare the properties that each category guarantees.", good], r=r, qtype="conceptual", tags={"reasoning"})


@fam("012")
def h_yes_no(r, L):
    a, b = pick(r, [(a, b) for a in CATS for b in CATS if a != b])
    ans = "yes" if b in SUB[a] else "no"
    sg = {"squares": "square", "rectangles": "rectangle", "rhombuses": "rhombus", "parallelograms": "parallelogram", "quadrilaterals": "quadrilateral"}
    return Item(f"Is every {sg[a]} also a {sg[b]}? Answer yes or no.", ans,
                [f"Check whether {a} always have every property of {b}.", f"The answer is {ans}."],
                [W("no" if ans == "yes" else "yes", "reversed the categories")], FN("is_every", a=a, b=b), qtype="conceptual", mode="sa", tags={"reasoning"})


SKILLS = {
    1: dict(name="Polygons and Their Attributes", fams=[pa_name, pa_parallel, pa_right, pa_regular, pa_attribute, pa_sides]),
    2: dict(name="Classifying Triangles", fams=[tri_sides, tri_angles, tri_drawn, tri_both, tri_row, tri_can]),
    3: dict(name="Classifying Quadrilaterals", fams=[q_most, q_also, q_from_props, q_which_shape, q_count_sides]),
    4: dict(name="Shape Hierarchies", fams=[h_all_are, h_false, h_inherit, h_counter, h_shared, h_yes_no]),
}
