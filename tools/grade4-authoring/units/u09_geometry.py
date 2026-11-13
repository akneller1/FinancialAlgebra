"""Unit 9: Geometry, Angles, and Symmetry (4.G.A.1-3, 4.MD.C.5-7)."""
from g4lib import *
import math
import figs

UNIT_ID = "geometry-angles-symmetry"
LETTERS = ["A", "B", "C", "D"]
KIND_NAME = {"line": "line", "ray": "ray", "segment": "line segment", "point": "point", "parallel": "parallel lines", "perpendicular": "perpendicular lines",
             "intersecting": "intersecting lines that are not perpendicular", "acute": "acute angle", "right": "right angle", "obtuse": "obtuse angle", "straight": "straight angle"}
KIND_DESC = {"line": "a straight path that goes on forever in both directions (arrows at both ends)", "ray": "a straight path with one endpoint that goes on forever in one direction",
             "segment": "a straight path with two endpoints", "point": "an exact location, shown by a dot", "parallel": "two lines that never meet and stay the same distance apart",
             "perpendicular": "two lines that meet to form right angles", "intersecting": "two lines that cross, but not at right angles",
             "acute": "an angle that is smaller than a right angle (less than 90°)", "right": "an angle that makes a square corner (exactly 90°)", "obtuse": "an angle that is larger than a right angle but smaller than a straight angle",
             "straight": "an angle that forms a straight line (exactly 180°)"}
GROUPS = [["line", "ray", "segment", "point"], ["parallel", "perpendicular", "intersecting", "segment"], ["acute", "right", "obtuse", "straight"], ["ray", "acute", "parallel", "line"], ["perpendicular", "obtuse", "ray", "segment"]]

# polygons for classification (vertex lists, counter-clockwise)
POLYS = {
    "rectangle": [(0, 0), (5, 0), (5, 3), (0, 3)],
    "square": [(0, 0), (3, 0), (3, 3), (0, 3)],
    "parallelogram": [(0, 0), (5, 0), (6.5, 3), (1.5, 3)],
    "rhombus": [(0, 0), (4, 0), (6.4, 3.2), (2.4, 3.2)],
    "trapezoid": [(0, 0), (6, 0), (4.5, 3), (1, 3)],
    "right trapezoid": [(0, 0), (5, 0), (3, 3), (0, 3)],
    "kite": [(2, 0), (4, 3), (2, 4.5), (0, 3)],
    "quadrilateral with no parallel sides": [(0, 0), (5, 0.5), (4, 3.5), (1, 2.5)],
    "right triangle": [(0, 0), (4, 0), (0, 3)],
    "acute triangle": [(0, 0), (5, 0), (2, 4)],
    "obtuse triangle": [(0, 0), (3, 0), (5.5, 2.5)],
    "equilateral triangle": [(0, 0), (4, 0), (2, 3.464)],
    "isosceles right triangle": [(0, 0), (3, 0), (0, 3)],
    "regular pentagon": [(round(2 * math.sin(2 * math.pi * k / 5), 3), round(2 * math.cos(2 * math.pi * k / 5), 3)) for k in range(5, 0, -1)],
    "regular hexagon": [(round(2 * math.cos(2 * math.pi * k / 6), 3), round(2 * math.sin(2 * math.pi * k / 6), 3)) for k in range(6)],
}
QUADS = ["rectangle", "square", "parallelogram", "rhombus", "trapezoid", "right trapezoid", "kite", "quadrilateral with no parallel sides"]
TRIS = ["right triangle", "acute triangle", "obtuse triangle", "equilateral triangle", "isosceles right triangle"]
QPROP = {  # for quad_is: parallel pairs, all sides equal, all right angles
    "rectangle": dict(parallel_pairs=2, all_sides_equal=False, right_angles=True), "square": dict(parallel_pairs=2, all_sides_equal=True, right_angles=True),
    "parallelogram": dict(parallel_pairs=2, all_sides_equal=False, right_angles=False), "rhombus": dict(parallel_pairs=2, all_sides_equal=True, right_angles=False),
    "trapezoid": dict(parallel_pairs=1, all_sides_equal=False, right_angles=False), "right trapezoid": dict(parallel_pairs=1, all_sides_equal=False, right_angles=False),
}


def angles_of(pts):
    n, out = len(pts), []
    for i in range(n):
        a, b, c = pts[i - 1], pts[i], pts[(i + 1) % n]
        v1, v2 = (a[0] - b[0], a[1] - b[1]), (c[0] - b[0], c[1] - b[1])
        out.append(math.degrees(math.acos((v1[0] * v2[0] + v1[1] * v2[1]) / (math.hypot(*v1) * math.hypot(*v2)))))
    return out


def rights(pts):
    return [i for i, a in enumerate(angles_of(pts)) if abs(a - 90) < 0.5]


def par_pairs(pts):
    n = len(pts)
    v = [(pts[(i + 1) % n][0] - pts[i][0], pts[(i + 1) % n][1] - pts[i][1]) for i in range(n)]
    return [(i, j) for i in range(n) for j in range(i + 1, n) if abs(v[i][0] * v[j][1] - v[i][1] * v[j][0]) < 1e-6]


def shape_dg(nm, marks=True, labels=None, fill="blue"):
    pts = POLYS[nm]
    d = {"pts": [list(p) for p in pts], "fill": fill}
    desc = f"A {len(pts)}-sided figure."
    if marks:
        d["right"] = rights(pts)
        d["arrows"] = [[s, k + 1] for k, pair in enumerate(par_pairs(pts)) for s in pair]
        rc, pc = len(d["right"]), len(par_pairs(pts))
        desc += f" {rc} corner{'s are' if rc != 1 else ' is'} marked as a right angle." if rc else " No corners are marked as right angles."
        desc += f" Arrow marks show {pc} pair{'s' if pc != 1 else ''} of parallel sides." if pc else " No sides are marked parallel."
    if labels:
        d["vertex_labels"] = [[i, l] for i, l in enumerate(labels)]
    return Diagram("shape", d, desc)


# ============================================================== S1 Points, Lines, Rays, and Angles
@fam("012", mode="mc")
def pl_identify(r, L):
    g = pick(r, GROUPS[:3] if L == 0 else GROUPS)
    kinds = g[:]
    r.shuffle(kinds)
    i = r.randrange(4)
    alt = "Four figures. " + " ".join(f"Figure {l}: {KIND_DESC[k]}." for l, k in zip(LETTERS, kinds))
    return Item(f"Which figure shows {'an' if KIND_NAME[kinds[i]][0] in 'aeio' else 'a'} {KIND_NAME[kinds[i]]}?".replace("a parallel lines", "parallel lines").replace("a perpendicular lines", "perpendicular lines").replace("an intersecting lines", "intersecting lines"),
                LETTERS[i], [f"Look for {KIND_DESC[kinds[i]]}.", f"Figure {LETTERS[i]} matches."],
                [W(l, f"this figure shows {KIND_NAME[k]}") for l, k in zip(LETTERS, kinds) if l != LETTERS[i]], FN("panel_pick", kinds=kinds, kind=kinds[i]), qtype="visual",
                diagram=Diagram("line_panels", {"items": [{"kind": k, "label": l} for k, l in zip(kinds, LETTERS)]}, alt))


@fam("012", mode="mc")
def pl_name(r, L):
    k = pick(r, list(KIND_NAME))
    same = [g for g in GROUPS[:3] if k in g][0]
    bad = [KIND_NAME[x] for x in same if x != k]
    alt = f"One figure: {KIND_DESC[k]}."
    return Item("What is the best name for this figure?", KIND_NAME[k], [f"The figure shows {KIND_DESC[k]}.", f"That is called {'an' if KIND_NAME[k][0] in 'aeio' else 'a'} {KIND_NAME[k]}.".replace("a parallel lines", "parallel lines").replace("a perpendicular lines", "perpendicular lines").replace("an intersecting lines", "intersecting lines")],
                [W(b, "this name describes a different figure") for b in bad], FN("panel_name", kind=k), qtype="visual", diagram=Diagram("line_panels", {"items": [{"kind": k, "label": ""}]}, alt))


@fam("012", mode="mc")
def pl_angle_type(r, L):
    a = pick(r, [90, 180]) if r.random() < 0.2 else r.randint(5, 175)
    typ = "acute" if a < 90 else "right" if a == 90 else "obtuse" if a < 180 else "straight"
    return Item(f"An angle measures {a}°. What type of angle is it?", typ, ["Acute: less than 90°. Right: exactly 90°. Obtuse: between 90° and 180°. Straight: exactly 180°.", f"{a}° is {'an' if typ in ('acute', 'obtuse') else 'a'} {typ} angle."],
                [W(t, "compared the measure with 90° incorrectly") for t in ("acute", "right", "obtuse", "straight") if t != typ], FN("angle_type", deg=a), qtype="conceptual")


@fam("012", mode="mc")
def pl_angle_fig(r, L):
    a = pick(r, [90]) if r.random() < 0.2 else pick(r, list(range(20, 75, 5)) + list(range(105, 165, 5)))
    rot = pick(r, [0, 0, 20, 40]) if L else 0
    typ = "acute" if a < 90 else "right" if a == 90 else "obtuse"
    alt = f"An angle formed by two rays from one point. The opening is {'smaller than a square corner' if a < 90 else 'a square corner' if a == 90 else 'larger than a square corner'}."
    return Item("Look at the angle. Is it smaller than, equal to, or larger than a square corner? What type of angle is shown?", typ, ["A right angle makes a square corner. An acute angle is smaller. An obtuse angle is larger.", f"The angle shown is {'an' if typ != 'right' else 'a'} {typ} angle."],
                [W(t, "did not compare the angle with a square corner") for t in ("acute", "right", "obtuse") if t != typ], FN("angle_type_rays", rays=[rot, rot + a]), qtype="visual",
                diagram=Diagram("angle", {"rays": [rot, rot + a], "sectors": [""], "square": a == 90}, alt))


@fam("012")
def pl_count_right(r, L):
    nm = pick(r, ["rectangle", "right trapezoid", "right triangle", "parallelogram", "trapezoid", "square", "kite", "regular hexagon", "acute triangle"])
    pts = POLYS[nm]
    k = len(rights(pts))
    dg = shape_dg(nm, marks=True)
    return Item("A small square marks each right angle in the figure. How many right angles does the figure have?", str(k), ["Count the corners that show a small square.", f"The figure has {k} right angle{'s' if k != 1 else ''}."],
                [W(str(len(pts)), "counted every corner"), W(str(k + 1), "counted a corner that is not a right angle"), W(str(abs(k - 1)) if k != 1 else "3", "missed a right angle"), W(str(len(pts) - k) if len(pts) - k not in (k, len(pts)) else str(k + 2), "counted the angles that are not right angles")],
                FN("poly_count", pts=[list(p) for p in pts], what="right"), qtype="visual", diagram=dg)


@fam("012")
def pl_count_parallel(r, L):
    nm = pick(r, ["rectangle", "parallelogram", "trapezoid", "right trapezoid", "rhombus", "kite", "regular hexagon", "right triangle", "quadrilateral with no parallel sides"])
    pts = POLYS[nm]
    k = len(par_pairs(pts))
    return Item("Sides with matching arrow marks are parallel. How many pairs of parallel sides does the figure have?", str(k), ["Parallel sides never meet, no matter how far they are extended.", f"The figure has {k} pair{'s' if k != 1 else ''} of parallel sides."],
                [W(str(len(pts)), "counted the sides"), W(str(k + 1), "counted a pair that is not parallel"), W(str(k * 2) if k else "4", "counted each side instead of each pair"), W(str(abs(k - 1)) if k != 1 else "3", "missed a pair")],
                FN("poly_count", pts=[list(p) for p in pts], what="parallel"), qtype="visual", diagram=shape_dg(nm, marks=True))


DEFS = [("Which describes a ray?", "It has one endpoint and goes on forever in one direction.", ["It has two endpoints.", "It goes on forever in both directions.", "It is an exact location with no length."]),
        ("Which describes a line segment?", "It is part of a line with two endpoints.", ["It has one endpoint and goes on forever in one direction.", "It goes on forever in both directions.", "It is two lines that never meet."]),
        ("Which describes a line?", "It is a straight path that goes on forever in both directions.", ["It has two endpoints.", "It has one endpoint.", "It is a curved path."]),
        ("Which describes parallel lines?", "They are always the same distance apart and never cross.", ["They cross at right angles.", "They cross at one point.", "They share an endpoint."]),
        ("Which describes perpendicular lines?", "They cross and form right angles.", ["They never cross.", "They cross and form acute angles only.", "They are the same line."]),
        ("How many endpoints does a ray have?", "1", ["0", "2", "3"]), ("How many endpoints does a line segment have?", "2", ["0", "1", "4"]), ("How many endpoints does a line have?", "0", ["1", "2", "4"]),
        ("Two lines cross and form four right angles. What are the lines called?", "perpendicular lines", ["parallel lines", "rays", "line segments"]),
        ("The rails of a straight railroad track never meet. The rails look like which kind of lines?", "parallel lines", ["perpendicular lines", "intersecting lines", "rays"]),
        ("The corner of a sheet of paper shows which type of angle?", "right angle", ["acute angle", "obtuse angle", "straight angle"]),
        ("The hands of a clock at 3:00 form which type of angle?", "right angle", ["acute angle", "obtuse angle", "straight angle"]),
        ("An angle is formed by two rays. What is shared by the two rays?", "an endpoint", ["a midpoint", "two endpoints", "a parallel line"]),
        ("A beam of light starts at a flashlight and keeps going in one direction. Which figure does it model?", "ray", ["line", "line segment", "point"]),
        ("The edge of a ruler from 0 to 12 inches models which figure?", "line segment", ["line", "ray", "angle"]),
        ("Which pair of lines can form a right angle?", "perpendicular lines", ["parallel lines", "two lines that never meet", "two rays pointing the same direction on one line"])]


@fam("012", mode="mc")
def pl_definitions(r, L):
    q, good, bad = pick(r, DEFS)
    return mc_key(q, good, bad, ["Think about endpoints and whether the figure goes on forever.", f"The answer is: {good}"], qtype="conceptual", r=r)


@fam("12")
def pl_count_angle_types(r, L):
    nm = pick(r, ["parallelogram", "trapezoid", "right trapezoid", "kite", "obtuse triangle", "acute triangle", "rhombus", "regular pentagon", "quadrilateral with no parallel sides", "right triangle"])
    pts = POLYS[nm]
    an = angles_of(pts)
    typ = pick(r, ["acute", "obtuse"])
    k = sum(1 for a in an if (a < 89.5 if typ == "acute" else a > 90.5))
    return Item(f"A small square marks each right angle in the figure. How many {typ} angles does the figure have?", str(k), [f"Compare each corner with a square corner. {'Acute angles are smaller' if typ == 'acute' else 'Obtuse angles are larger'}.", f"The figure has {k} {typ} angle{'s' if k != 1 else ''}."],
                [W(str(len(pts) - k) if len(pts) - k != k else str(k + 1), f"counted the angles that are not {typ}"), W(str(len(pts)), "counted every corner"), W(str(k + 1) if len(pts) - k != k else str(k + 2), "counted one too many"), W(str(abs(k - 1)) if k != 1 else "0", "missed one")],
                FN("poly_count", pts=[list(p) for p in pts], what=typ), qtype="visual", diagram=shape_dg(nm, marks=True), tags={"reasoning"})


# ============================================================== S2 Measuring Angles
def deg(x):
    return f"{x}°"


def ang_wrongs(a):
    return [W(deg(180 - a), "read the protractor from the wrong end") if a != 90 else W(deg(100), "misread the scale"), W(deg(a + 10), "misread the scale by one mark"), W(deg(a - 5) if a > 10 else deg(a + 5), "misread the small marks"), W(deg(a + 90) if a < 90 else deg(a - 90), "confused acute and obtuse")]


@fam("012")
def an_protractor(r, L):
    a = r.randint(2, 16) * 10 if L == 0 else r.randint(3, 34) * 5
    need(a not in (90,))
    alt = f"A protractor on angle ABC. Ray BA points to 0°. Ray BC passes through the {a}° mark."
    return Item("Use the protractor. What is the measure of angle ABC?", deg(a), [f"One ray points to 0°. Read the scale where the other ray crosses it.", f"The angle measures {deg(a)}."], ang_wrongs(a),
                FN("angle_rays", rays=[0, a]), qtype="visual", diagram=Diagram("angle", {"rays": [0, a], "sectors": [""], "protractor": True, "points": ["A", "C"], "vertex": "B"}, alt))


@fam("12")
def an_protractor_offset(r, L):
    a0 = r.randint(2, 6) * 10
    a = r.randint(3, 10) * 10 if L == 1 else r.randint(5, 22) * 5
    need(a0 + a <= 170)
    alt = f"A protractor on angle PQR. Ray QP passes through the {a0}° mark. Ray QR passes through the {a0 + a}° mark."
    return Item(f"Neither ray points to 0°. One ray passes through {deg(a0)} and the other passes through {deg(a0 + a)}. What is the measure of angle PQR?", deg(a),
                [f"Subtract the two readings.", f"{a0 + a} − {a0} = {a}, so the angle measures {deg(a)}."],
                [W(deg(a0 + a), "read only the second ray"), W(deg(a0), "read only the first ray"), W(deg(2 * a0 + a), "added the readings"), W(deg(a + 10), "misread the scale")],
                EX(f"{a0 + a} − {a0}", unit="°"), qtype="visual", diagram=Diagram("angle", {"rays": [a0, a0 + a], "sectors": [""], "protractor": True, "points": ["P", "R"], "vertex": "Q"}, alt), tags={"reasoning"})


@fam("012")
def an_fraction_turn(r, L):
    n, d = pick(r, [(1, 4), (1, 2), (3, 4), (1, 1)] if L == 0 else [(1, 4), (1, 2), (3, 4), (1, 3), (1, 6), (1, 8), (1, 12)] if L == 1 else [(2, 3), (5, 6), (3, 8), (5, 12), (1, 10), (1, 9), (1, 5)])
    v = 360 * n // d
    turn = "a full turn" if n == d else f"{n}/{d} of a full turn"
    return Item(f"A full turn around a circle is 360°. An angle turns through {turn}. What is the measure of the angle?", deg(v), [f"Find {n}/{d} of 360." if n != d else "A full turn is the whole circle.", f"360 ÷ {d} = {360 // d}" + (f", and {n} × {360 // d} = {v}" if n > 1 else "") + f". The angle measures {deg(v)}."],
                [W(deg(360 // d) if n > 1 else deg(360 * d) if 360 * d != v else deg(v + 10), "used only the denominator" if n > 1 else "multiplied by the denominator"), W(deg(100 * n // d), "used 100° for a full turn"), W(deg(180 * n // d) if n != d else deg(180), "used 180° for a full turn"), W(deg(v + 30), "made a computation mistake")],
                EX(f"360 × {n}/{d}", unit="°"), qtype="conceptual")


@fam("012")
def an_one_degree(r, L):
    a = r.randint(15, 175)
    if r.random() < 0.5:
        return Item(f"A one‑degree angle turns through 1/360 of a circle. An angle turns through {a} one‑degree angles. What is the measure of the angle?", deg(a), ["Each one‑degree angle adds 1°.", f"{a} one‑degree angles make {deg(a)}."],
                    [W(deg(360 - a), "subtracted from 360°"), W(deg(a + 1), "counted an extra degree"), W(deg(360), "gave the full circle"), W(deg(1), "gave the size of one small angle")], FN("unit_degrees", n=a), qtype="conceptual")
    return Item(f"How many one‑degree angles fit together, without gaps or overlaps, to make an angle of {deg(a)}?", str(a), ["An angle of n degrees is made of n one‑degree angles.", f"{deg(a)} is made of {a} one‑degree angles."],
                [W(str(360 - a), "subtracted from 360"), W(str(360), "gave the number in a full circle"), W(str(a - 1), "counted one too few"), W("1", "gave the size of one small angle")], FN("unit_degrees", n=a, bare=True), qtype="conceptual")


@fam("012")
def an_clock_turn(r, L):
    s = r.randint(1, 12)
    k = r.randint(1, 3) if L == 0 else r.randint(2, 6) if L == 1 else r.randint(5, 11)
    e = (s + k - 1) % 12 + 1
    return Item(f"A clock face is a circle split into 12 equal parts, so moving from one number to the next is a turn of 30°. The minute hand moves from the {s} to the {e}. Through how many degrees does it turn?", deg(30 * k),
                [f"From the {s} to the {e} is {k} part{'s' if k != 1 else ''}.", f"{k} × 30 = {30 * k}, so the hand turns {deg(30 * k)}."],
                [W(deg(k), "counted the parts but did not multiply by 30°"), W(deg(30 * (k + 1)), "counted one part too many"), W(deg(5 * k), "used the minutes instead of the degrees"), W(deg(360 - 30 * k) if 360 - 30 * k != 30 * k else deg(30 * k + 15), "measured the turn in the other direction")],
                FN("clock_turn", start=s, end=e), qtype="real-world", tags={"modeling"})


@fam("012", mode="mc")
def an_estimate(r, L):
    a = pick(r, [30, 45, 60, 120, 135, 150] if L < 2 else [20, 40, 70, 110, 140, 160])
    sets = {30: [90, 120, 170], 45: [100, 135, 170], 60: [10, 110, 160], 120: [20, 60, 175], 135: [15, 45, 85], 150: [10, 60, 95], 20: [70, 110, 160], 40: [95, 130, 170], 70: [15, 120, 165], 110: [20, 60, 170], 140: [20, 50, 95], 160: [20, 70, 110]}
    alt = f"An angle formed by two rays. The opening is {'narrower' if a < 90 else 'wider'} than a square corner."
    return Item("Use a right angle (90°) as a benchmark. Which is the best estimate for the measure of this angle?", deg(a), [f"The angle is {'smaller' if a < 90 else 'larger'} than a right angle.", f"The best estimate is {deg(a)}."],
                [W(deg(x), "this estimate does not match how the angle compares with 90°") for x in sets[a]], FN("angle_estimate", rays=[0, a]), qtype="visual", diagram=Diagram("angle", {"rays": [0, a], "sectors": [""]}, alt))


@fam("012")
def an_vs_right(r, L):
    a = r.randint(95, 175) if r.random() < 0.5 else r.randint(10, 85)
    if a > 90:
        return Item(f"A right angle measures 90°. How many degrees greater than a right angle is an angle of {deg(a)}?", deg(a - 90), [f"Subtract: {a} − 90 = {a - 90}.", f"It is {deg(a - 90)} greater."],
                    [W(deg(a + 90), "added instead of subtracting"), W(deg(180 - a), "compared with a straight angle"), W(deg(a - 80), "made a subtraction mistake"), W(deg(a), "gave the angle itself")], EX(f"{a} − 90", unit="°"), qtype="conceptual")
    return Item(f"A right angle measures 90°. How many degrees less than a right angle is an angle of {deg(a)}?", deg(90 - a), [f"Subtract: 90 − {a} = {90 - a}.", f"It is {deg(90 - a)} less."],
                [W(deg(a + 90), "added instead of subtracting"), W(deg(180 - a), "compared with a straight angle"), W(deg(100 - a), "made a subtraction mistake"), W(deg(a), "gave the angle itself")], EX(f"90 − {a}", unit="°"), qtype="conceptual")


@fam("12")
def an_turn_to_fraction(r, L):
    n, d = pick(r, [(1, 4), (1, 2), (3, 4), (1, 3), (1, 6), (1, 8), (1, 12), (2, 3), (1, 10), (1, 9), (1, 5)])
    v = 360 * n // d
    return Item(f"A full turn is 360°. An angle of {deg(v)} is what fraction of a full turn? Write the fraction in simplest form.", f"{n}/{d}", [f"Write the fraction {v}/360.", f"Divide the numerator and denominator by {360 // d}: {n}/{d}."],
                [W(f"{d}/{n}" if n > 1 else f"1/{d + 1}", "switched the numerator and denominator" if n > 1 else "made a division mistake"), W(f"1/{v}" if v not in (d,) else f"1/{d + 2}", "used the angle measure as the denominator"), W(f"{n}/{d * 2}", "used 720° for a full turn"), W(f"{v}/100", "used 100 as the whole")],
                EX(f"{v}/360", form="frac"), qtype="conceptual", tags={"reasoning"})


# ============================================================== S3 Adding and Subtracting Angle Measures
def two_parts(r, L, total=None):
    if total:
        a = r.randint(15, total - 15) if L else r.randint(2, (total - 10) // 10) * 10
        return a, total - a
    a = r.randint(2, 7) * 10 if L == 0 else r.randint(15, 80)
    b = r.randint(2, 7) * 10 if L == 0 else r.randint(15, 80)
    need(a + b < 175 and a != b)
    return a, b


def parts_dg(parts, labels, pts=("P", "Q", "R", "T"), vertex="S", rot=0):
    rays = [rot]
    for p in parts:
        rays.append(rays[-1] + p)
    alt = f"Rays from point {vertex} form {len(parts)} angles next to each other. " + " ".join(f"The {ordinal(i + 1)} angle is labeled {l}." for i, l in enumerate(labels))
    return Diagram("angle", {"rays": rays, "sectors": labels, "points": list(pts[:len(rays)]), "vertex": vertex, "square": False}, alt)


@fam("012")
def aa_add(r, L):
    a, b = two_parts(r, L)
    return Item(f"Angle PSQ measures {deg(a)} and angle QSR measures {deg(b)}. The two angles share ray SQ and do not overlap. What is the measure of angle PSR?", deg(a + b),
                ["The large angle is made of the two smaller angles, so add.", f"{a} + {b} = {a + b}, so angle PSR measures {deg(a + b)}."],
                [W(deg(abs(a - b)), "subtracted instead of adding"), W(deg(180 - a - b), "subtracted from 180°"), W(deg(a + b + 10), "made an addition mistake"), W(deg(max(a, b)), "gave only the larger angle")],
                EX(f"{a} + {b}", unit="°"), qtype="visual", diagram=parts_dg([a, b], [deg(a), deg(b)]))


@fam("012")
def aa_missing(r, L):
    a, b = two_parts(r, L)
    return Item(f"Angle PSR measures {deg(a + b)}. Ray SQ splits it into two angles. Angle PSQ measures {deg(a)}. What is the measure of angle QSR?", deg(b),
                ["The two smaller angles add up to the whole angle, so subtract.", f"{a + b} − {a} = {b}, so angle QSR measures {deg(b)}."],
                [W(deg(2 * a + b), "added instead of subtracting"), W(deg(abs(180 - a - b)) if abs(180 - a - b) != b else deg(b + 5), "subtracted from 180°"), W(deg(b + 10), "made a subtraction mistake"), W(deg(a), "repeated the known part")],
                EX(f"{a + b} − {a}", unit="°"), qtype="visual", diagram=parts_dg([a, b], [deg(a), "?"]))


@fam("012")
def aa_right(r, L):
    a, b = two_parts(r, L, 90)
    alt_s = f"A right angle is split into two angles by a ray."
    return Item(f"A right angle (90°) is split into two smaller angles. One of them measures {deg(a)}. What is the measure of the other angle?", deg(b),
                ["The two parts add up to 90°.", f"90 − {a} = {b}, so the other angle measures {deg(b)}."],
                [W(deg(180 - a), "subtracted from 180° instead of 90°"), W(deg(90 + a), "added instead of subtracting"), W(deg(b + 10), "made a subtraction mistake"), W(deg(a), "repeated the known part")],
                EX(f"90 − {a}", unit="°"), qtype="visual", diagram=parts_dg([a, b], [deg(a), "?"]))


@fam("012")
def aa_straight(r, L):
    if L == 2:
        a = r.randint(20, 70)
        b = r.randint(20, 70)
        c = 180 - a - b
        need(c >= 20)
        return Item(f"Three angles fit together along a straight line (180°). Two of the angles measure {deg(a)} and {deg(b)}. What is the measure of the third angle?", deg(c),
                    [f"The three angles add up to 180°. {a} + {b} = {a + b}.", f"180 − {a + b} = {c}, so the third angle measures {deg(c)}."],
                    [W(deg(a + b), "added the two known angles and stopped"), W(deg(abs(90 - a - b)) if abs(90 - a - b) not in (c, 0) else deg(c + 5), "used 90° for a straight line"), W(deg(180 - a), "subtracted only one angle"), W(deg(360 - a - b), "used 360° for a straight line")],
                    EX(f"180 − {a} − {b}", unit="°"), qtype="visual", diagram=parts_dg([a, b, c], [deg(a), deg(b), "?"]), tags={"multistep"})
    a, b = two_parts(r, L, 180)
    return Item(f"Two angles fit together along a straight line (180°). One angle measures {deg(a)}. What is the measure of the other angle?", deg(b),
                ["The two angles add up to 180°.", f"180 − {a} = {b}, so the other angle measures {deg(b)}."],
                [W(deg(abs(90 - a)) if abs(90 - a) not in (b, 0) else deg(b + 5), "subtracted from 90° instead of 180°"), W(deg(180 + a), "added instead of subtracting"), W(deg(b + 10), "made a subtraction mistake"), W(deg(360 - a), "subtracted from 360°")],
                EX(f"180 − {a}", unit="°"), qtype="visual", diagram=parts_dg([a, b], [deg(a), "?"]))


@fam("012")
def aa_word(r, L):
    kind = r.randrange(3)
    if kind == 0:
        a, b = two_parts(r, L)
        return Item(f"A door is opened to an angle of {deg(a)}. Then it is pushed open {deg(b)} more. What angle does the open door make now?", deg(a + b), ["Add the two turns.", f"{a} + {b} = {a + b}, so the angle is {deg(a + b)}."],
                    [W(deg(abs(a - b)), "subtracted instead of adding"), W(deg(a + b + 10), "made an addition mistake"), W(deg(180 - a - b), "subtracted from 180°"), W(deg(a), "ignored the second turn")], EX(f"{a} + {b}", unit="°"), qtype="real-world", tags={"modeling"})
    if kind == 1:
        n = pick(r, [2, 3, 4] if L < 2 else [3, 5, 7])
        each = pick(r, [30, 45, 60, 36, 40, 20])
        need(n * each <= 360)
        return Item(f"A pizza is cut into equal slices. The tip of each slice forms an angle of {deg(each)}. {name(r)} puts {n} slices side by side. What angle is formed by the {n} slices together?", deg(n * each),
                    [f"Add {deg(each)} for each slice, or multiply.", f"{n} × {each} = {n * each}, so the angle is {deg(n * each)}."],
                    [W(deg(each + n), "added the number of slices to the angle"), W(deg(n * each + each), "counted an extra slice"), W(deg(360 - n * each) if 360 - n * each not in (n * each, 0) else deg(n * each + 10), "found the rest of the pizza"), W(deg(each), "gave the angle of one slice")],
                    EX(f"{n} × {each}", unit="°"), qtype="real-world", tags={"modeling"})
    a, b = two_parts(r, L)
    return Item(f"A fan blade turns {deg(a + b)} in all. First it turns {deg(a)}. How many more degrees does it turn?", deg(b), ["Subtract the first turn from the total turn.", f"{a + b} − {a} = {b}, so it turns {deg(b)} more."],
                [W(deg(2 * a + b), "added instead of subtracting"), W(deg(b + 10), "made a subtraction mistake"), W(deg(a), "repeated the first turn"), W(deg(abs(360 - a - b)), "subtracted from 360°")], EX(f"{a + b} − {a}", unit="°"), qtype="real-world", tags={"modeling"})


@fam("012", mode="mc")
def aa_equation(r, L):
    total = pick(r, [90, 180]) if r.random() < 0.6 else None
    a, b = two_parts(r, L, total)
    T = a + b
    good = f"{a} + x = {T}"
    desc = {90: "A right angle", 180: "A straight angle"}.get(T, f"An angle of {deg(T)}")
    return Item(f"{desc} is split into two smaller angles. One angle measures {deg(a)} and the other measures x degrees. Which equation can be used to find x?", good,
                [f"The two parts add up to the whole angle, {deg(T)}.", f"{good}, so x = {b}."],
                [W(f"{a} + {T} = x", "added the whole angle to the part"), W(f"x − {a} = {T}", "subtracted the part from the unknown"), W(f"{a} × x = {T}", "used multiplication")],
                FN("eq_with", n=str(b), letter="x"), qtype="conceptual", tags={"modeling", "reasoning"})


@fam("12")
def aa_equal_parts(r, L):
    n = pick(r, [2, 3, 4, 5, 6])
    each = r.randint(3, 16) * 5 if L == 1 else r.randint(11, 44)
    T = n * each
    need(T <= 180)
    return Item(f"An angle of {deg(T)} is split into {n} equal angles. What is the measure of each smaller angle?", deg(each), [f"Divide the whole angle by {n}.", f"{T} ÷ {n} = {each}, so each angle measures {deg(each)}."],
                [W(deg(T - n), "subtracted instead of dividing"), W(deg(T * n), "multiplied instead of dividing"), W(deg(each + 5), "made a division mistake"), W(deg(180 // n) if 180 // n != each else deg(each + 10), "divided 180° instead of the given angle")],
                EX(f"{T} ÷ {n}", unit="°"), qtype="conceptual", tags={"reasoning"})


# ============================================================== S4 Classifying Triangles and Quadrilaterals
def tri_angles(r, kind, L):
    if kind == "right":
        a = r.randint(15, 75) if L else r.randint(2, 7) * 10
        return [90, a, 90 - a]
    if kind == "obtuse":
        o = r.randint(95, 150)
        a = r.randint(10, 170 - o)
        return [o, a, 180 - o - a]
    while True:
        a, b = r.randint(35, 85), r.randint(35, 85)
        if 180 - a - b < 90 and 180 - a - b > 10:
            return [a, b, 180 - a - b]


@fam("012", mode="mc")
def cl_triangle_angles(r, L):
    kind = pick(r, ["right", "obtuse", "acute"])
    an = tri_angles(r, kind, L)
    r.shuffle(an)
    return Item(f"The angles of a triangle measure {deg(an[0])}, {deg(an[1])} and {deg(an[2])}. Classify the triangle by its angles.", kind,
                [{"right": "One angle is exactly 90°.", "obtuse": f"One angle, {deg(max(an))}, is greater than 90°.", "acute": "All three angles are less than 90°."}[kind], f"It is {'an' if kind != 'right' else 'a'} {kind} triangle."],
                [W(k, "did not check all three angles against 90°") for k in ("right", "obtuse", "acute") if k != kind], FN("tri", angles=an, by="angles"), qtype="conceptual")


@fam("012", mode="mc")
def cl_right_triangle_which(r, L):
    others = r.sample(["acute triangle", "obtuse triangle", "equilateral triangle"], 3)
    names_ = others + [pick(r, ["right triangle", "isosceles right triangle"])]
    r.shuffle(names_)
    gi = [i for i, n in enumerate(names_) if "right" in n][0]
    items = [{"pts": [list(p) for p in POLYS[n]], "label": l, "right": rights(POLYS[n])} for n, l in zip(names_, LETTERS)]
    alt = "Four triangles labeled A to D. " + " ".join(f"Triangle {l} {'has one corner marked as a right angle' if 'right' in n else 'has no right angle'}." for n, l in zip(names_, LETTERS))
    return Item("A right triangle has one right angle. Which triangle is a right triangle?", LETTERS[gi], ["Look for the corner that shows a small square.", f"Triangle {LETTERS[gi]} has a right angle."],
                [W(l, "this triangle has no right angle") for i, l in enumerate(LETTERS) if i != gi], FN("row_pick", items=[it["pts"] for it in items], labels=LETTERS, prop="right"), qtype="visual", diagram=Diagram("shape_row", {"items": items}, alt))


QDESC = {"rectangle": "2 pairs of parallel sides and 4 right angles. Its sides are not all the same length", "square": "2 pairs of parallel sides, 4 right angles, and 4 sides of equal length",
         "parallelogram": "2 pairs of parallel sides and no right angles. Its sides are not all the same length", "rhombus": "2 pairs of parallel sides, 4 sides of equal length, and no right angles",
         "trapezoid": "exactly 1 pair of parallel sides"}


@fam("012", mode="mc")
def cl_quad_describe(r, L):
    nm = pick(r, list(QDESC))
    bad = [x for x in QDESC if x != nm]
    r.shuffle(bad)
    return Item(f"A quadrilateral has {QDESC[nm]}. What is the most specific name for it?", nm, ["Match the description to the properties of each quadrilateral.", f"The figure is a {nm}."],
                [W(b, "this figure has different properties") for b in bad[:3]], FN("quad_is", q=QPROP[nm], most=True), qtype="conceptual", tags={"reasoning"})


@fam("012", mode="mc")
def cl_quad_figure(r, L):
    nm = pick(r, ["rectangle", "square", "parallelogram", "rhombus", "trapezoid"])
    pts = POLYS[nm]
    d = shape_dg(nm, marks=True).data
    if nm in ("square", "rhombus"):
        d["ticks"] = [[i, 1] for i in range(4)]
    elif nm in ("rectangle", "parallelogram"):
        d["ticks"] = [[0, 1], [2, 1], [1, 2], [3, 2]]
    alt = f"A quadrilateral with {QDESC[nm]}. Arrow marks show parallel sides, tick marks show sides of equal length, and small squares show right angles."
    bad = [x for x in QDESC if x != nm]
    r.shuffle(bad)
    return Item("Arrow marks show parallel sides. Tick marks show sides of equal length. Small squares show right angles. What is the most specific name for this figure?", nm,
                [f"The figure has {QDESC[nm]}.", f"It is a {nm}."], [W(b, "this name does not match the marks on the figure") for b in bad[:3]],
                FN("quad_pts", pts=[list(p) for p in pts]), qtype="visual", diagram=Diagram("shape", d, alt))


ALWAYS = [("Which statement is always true?", "A square has 4 right angles.", ["A rhombus has 4 right angles.", "A trapezoid has 2 pairs of parallel sides.", "A parallelogram has exactly 1 pair of parallel sides."]),
          ("Which statement is always true?", "A rectangle has 2 pairs of parallel sides.", ["A trapezoid has 4 right angles.", "A right triangle has 2 right angles.", "A rhombus has no parallel sides."]),
          ("Which statement is always true?", "A right triangle has exactly 1 right angle.", ["An acute triangle has 1 right angle.", "An obtuse triangle has 2 obtuse angles.", "A right triangle has 3 right angles."]),
          ("Which statement is always true?", "A rhombus has 4 sides of equal length.", ["A rectangle has 4 sides of equal length.", "A trapezoid has 4 sides of equal length.", "A parallelogram has 4 right angles."]),
          ("Which figure always has perpendicular sides?", "rectangle", ["rhombus", "parallelogram", "obtuse triangle"]),
          ("Which figure always has perpendicular sides?", "right triangle", ["acute triangle", "obtuse triangle", "equilateral triangle"]),
          ("Which figure never has parallel sides?", "triangle", ["rectangle", "rhombus", "trapezoid"]),
          ("Which figure always has 2 pairs of parallel sides?", "parallelogram", ["trapezoid with exactly 1 pair of parallel sides", "right triangle", "kite with no parallel sides"]),
          ("An acute triangle has how many acute angles?", "3", ["0", "1", "2"]), ("An obtuse triangle has how many obtuse angles?", "1", ["0", "2", "3"]),
          ("A square is always which other kind of figure?", "rectangle", ["trapezoid with exactly 1 pair of parallel sides", "right triangle", "obtuse triangle"]),
          ("Which statement about a right triangle is true?", "Two of its sides are perpendicular.", ["Two of its sides are parallel.", "All of its angles are right angles.", "It has an obtuse angle."]),
          ("A triangle has an angle of 100°. What kind of triangle is it?", "obtuse triangle", ["right triangle", "acute triangle", "equilateral triangle"]),
          ("Every angle of a triangle is less than 90°. What kind of triangle is it?", "acute triangle", ["right triangle", "obtuse triangle", "straight triangle"]),
          ("Which property do a rectangle and a rhombus always share?", "2 pairs of parallel sides", ["4 right angles", "4 sides of equal length", "exactly 1 pair of parallel sides"]),
          ("Which property do a square and a rectangle always share?", "4 right angles", ["4 sides of equal length", "no parallel sides", "exactly 1 pair of parallel sides"])]


@fam("012", mode="mc")
def cl_always(r, L):
    q, good, bad = pick(r, ALWAYS)
    return mc_key(q, good, bad, ["Think about the parallel sides, perpendicular sides and angle sizes of each figure.", f"The answer is: {good}"], qtype="conceptual", tags={"reasoning"}, r=r)


@fam("012", mode="mc")
def cl_row_property(r, L):
    prop = pick(r, ["perpendicular", "parallel", "none_parallel"] if L else ["perpendicular", "parallel"])
    if prop == "perpendicular":
        good = pick(r, ["rectangle", "right triangle", "right trapezoid", "square"])
        bad = r.sample(["parallelogram", "rhombus", "acute triangle", "obtuse triangle", "regular hexagon", "trapezoid", "equilateral triangle"], 3)
        q, why = "Which figure has at least one pair of perpendicular sides?", "Perpendicular sides meet at a right angle."
    elif prop == "parallel":
        good = pick(r, ["parallelogram", "trapezoid", "rhombus", "rectangle", "regular hexagon"])
        bad = r.sample(["right triangle", "acute triangle", "obtuse triangle", "kite", "quadrilateral with no parallel sides", "regular pentagon"], 3)
        q, why = "Which figure has at least one pair of parallel sides?", "Parallel sides never meet."
    else:
        good = pick(r, ["kite", "quadrilateral with no parallel sides"])
        bad = r.sample(["parallelogram", "trapezoid", "rhombus", "rectangle", "square", "right trapezoid"], 3)
        q, why = "All four figures are quadrilaterals. Which one has NO parallel sides?", "Check each pair of opposite sides."
    names_ = bad + [good]
    r.shuffle(names_)
    gi = names_.index(good)
    items = [{"pts": [list(p) for p in POLYS[n]], "label": l, "right": rights(POLYS[n]), "arrows": [[s, k + 1] for k, pair in enumerate(par_pairs(POLYS[n])) for s in pair]} for n, l in zip(names_, LETTERS)]
    alt = "Four figures labeled A to D. " + " ".join(f"Figure {l} is a {n}." for n, l in zip(names_, LETTERS))
    return Item(q + " Small squares show right angles. Arrow marks show parallel sides.", LETTERS[gi], [why, f"Figure {LETTERS[gi]} is the answer."],
                [W(l, "this figure does not have the property") for i, l in enumerate(LETTERS) if i != gi], FN("row_pick", items=[it["pts"] for it in items], labels=LETTERS, prop=prop), qtype="visual", diagram=Diagram("shape_row", {"items": items}, alt), tags={"reasoning"})


@fam("12")
def cl_third_angle(r, L):
    kind = pick(r, ["right", "obtuse", "acute"])
    an = tri_angles(r, kind, L)
    a, b, c = an[0], an[1], an[2]
    return Item(f"The three angles of any triangle add up to 180°. Two angles of a triangle measure {deg(a)} and {deg(b)}. What is the measure of the third angle?", deg(c),
                [f"{a} + {b} = {a + b}.", f"180 − {a + b} = {c}. The third angle is {deg(c)}, so the triangle is {'an' if kind != 'right' else 'a'} {kind} triangle."],
                [W(deg(a + b), "added the two angles and stopped"), W(deg(abs(90 - a - b)) if abs(90 - a - b) not in (c, 0) else deg(c + 5), "used 90° as the total"), W(deg(360 - a - b), "used 360° as the total"), W(deg(c + 10), "made a subtraction mistake")],
                EX(f"180 − {a} − {b}", unit="°"), qtype="multi-step", tags={"multistep", "challenge"})


# ============================================================== S5 Lines of Symmetry
SYM = figs.SYM_SHAPES
SYM_LINES = {"square": [0, 45, 90, 135], "rectangle": [0, 90], "equilateral triangle": [90, 30, 150], "isosceles triangle": [90], "scalene triangle": [], "rhombus": [0, 90], "parallelogram": [],
             "isosceles trapezoid": [90], "kite": [90], "regular pentagon": [90, 18, 54, 126, 162], "regular hexagon": [0, 30, 60, 90, 120, 150], "arrow": [0], "letter T": [90], "letter L": [], "plus sign": [0, 45, 90, 135],
             "right triangle": [], "letter H": [0, 90], "heart": [90], "regular octagon": [0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5]}
SYM_POOL = {0: ["square", "rectangle", "isosceles triangle", "arrow", "letter T", "letter L", "heart", "parallelogram", "letter H", "kite"],
            1: ["square", "rectangle", "equilateral triangle", "isosceles triangle", "scalene triangle", "rhombus", "parallelogram", "isosceles trapezoid", "kite", "arrow", "letter T", "letter L", "plus sign", "right triangle", "letter H", "heart"],
            2: list(SYM_LINES)}
FOLD = ["Yes. The two parts match exactly when the figure is folded on the line.", "No. The two parts do not match when the figure is folded on the line.",
        "Yes. Every line through the middle of a figure is a line of symmetry.", "No. A line of symmetry must run straight up and down."]


def pts_of(nm):
    return [[round(x, 4), round(y, 4)] for x, y in SYM[nm]]


@fam("012", mode="mc")
def sy_is_line(r, L):
    nm = pick(r, SYM_POOL[L])
    lines = SYM_LINES[nm]
    cands = [a for a in (0, 45, 90, 135) if a not in lines]
    is_sym = r.random() < 0.5 and lines
    if is_sym:
        a = pick(r, [x for x in lines if x == int(x)])
    else:
        need(cands)
        a = pick(r, cands)
    good = FOLD[0] if is_sym else FOLD[1]
    alt = f"A {nm} with a dashed line through its center. The dashed line is {'horizontal' if a == 0 else 'vertical' if a == 90 else 'slanted'}."
    return Item("Is the dashed line a line of symmetry for the figure?", good, ["Imagine folding the figure on the dashed line.", good],
                [W(f, "this does not describe what happens when the figure is folded") for f in FOLD if f != good], FN("sym_fold", pts=pts_of(nm), angle=a), qtype="visual",
                diagram=Diagram("sym_shape", {"shape": nm, "lines": [a]}, alt))


@fam("012")
def sy_count(r, L):
    nm = pick(r, SYM_POOL[L])
    k = len(SYM_LINES[nm])
    alt = f"A {nm}, drawn by itself with no fold lines marked."
    return Item("How many lines of symmetry does this figure have?", str(k), ["Look for every line that folds the figure into two matching parts.", f"The figure has {k} line{'s' if k != 1 else ''} of symmetry."],
                [W(str(k + 1), "counted a line that does not make matching parts"), W(str(abs(k - 1)) if k != 1 else "0", "missed a line of symmetry"), W(str(len(SYM[nm])) if len(SYM[nm]) not in (k, k + 1) else str(k + 2), "counted the sides"), W(str(k * 2) if k > 1 else str(k + 3), "counted each line twice")],
                FN("sym_count", pts=pts_of(nm)), qtype="visual", diagram=Diagram("sym_shape", {"shape": nm, "lines": []}, alt))


@fam("012", mode="mc")
def sy_which_line(r, L):
    nm = pick(r, [n for n in SYM_POOL[L] if SYM_LINES[n]])
    lines = [x for x in SYM_LINES[nm] if x == int(x)]
    non = [a for a in (0, 30, 45, 60, 90, 120, 135, 150) if a not in SYM_LINES[nm]]
    need(len(non) >= 2 and lines)
    g = pick(r, lines)
    drawn = r.sample(non, 2) + [g]
    r.shuffle(drawn)
    labs = ["1", "2", "3"]
    gi = drawn.index(g)
    alt = f"A {nm} with three dashed lines through its center, labeled 1, 2 and 3."
    return Item("Three dashed lines are drawn through the figure. Which one is a line of symmetry?", f"Line {labs[gi]}", ["Imagine folding the figure on each line.", f"Only Line {labs[gi]} makes two matching parts."],
                [W(f"Line {l}", "the two parts do not match when folded on this line") for i, l in enumerate(labs) if i != gi], FN("sym_which", pts=pts_of(nm), angles=drawn, labels=labs), qtype="visual",
                diagram=Diagram("sym_shape", {"shape": nm, "lines": drawn, "line_labels": labs}, alt))


@fam("012", mode="mc")
def sy_which_shape(r, L):
    cond = pick(r, ["none", "exactly one", "more than one"])
    pool = SYM_POOL[max(L, 1)]
    test = {"none": lambda k: k == 0, "exactly one": lambda k: k == 1, "more than one": lambda k: k > 1}[cond]
    goods = [n for n in pool if test(len(SYM_LINES[n]))]
    bads = [n for n in pool if not test(len(SYM_LINES[n]))]
    good = pick(r, goods)
    names_ = r.sample(bads, 3) + [good]
    r.shuffle(names_)
    gi = names_.index(good)
    alt = "Four figures labeled A to D. " + " ".join(f"Figure {l} is a {n}." for n, l in zip(names_, LETTERS))
    q = {"none": "Which figure has NO lines of symmetry?", "exactly one": "Which figure has exactly 1 line of symmetry?", "more than one": "Which figure has more than 1 line of symmetry?"}[cond]
    return Item(q, LETTERS[gi], ["Count the lines of symmetry for each figure.", f"Figure {LETTERS[gi]} has {len(SYM_LINES[good])}."],
                [W(l, f"this figure has {len(SYM_LINES[n])} line{'s' if len(SYM_LINES[n]) != 1 else ''} of symmetry") for i, (n, l) in enumerate(zip(names_, LETTERS)) if i != gi],
                FN("sym_row", items=[pts_of(n) for n in names_], labels=LETTERS, cond=cond), qtype="visual", diagram=Diagram("sym_row", {"items": [{"shape": n, "label": l} for n, l in zip(names_, LETTERS)]}, alt), tags={"reasoning"})


@fam("012")
def sy_named(r, L):
    nm = pick(r, ["square", "rectangle", "equilateral triangle", "rhombus", "regular pentagon", "regular hexagon"] if L < 2 else ["regular pentagon", "regular hexagon", "regular octagon", "square", "equilateral triangle"])
    k = len(SYM_LINES[nm])
    art = "an" if nm[0] in "aeio" else "a"
    extra = " (not a square)" if nm in ("rectangle", "rhombus") else ""
    return Item(f"How many lines of symmetry does {art} {nm}{extra} have?", str(k), [f"Picture every fold that makes two matching halves of the {nm}.", f"There are {k} lines of symmetry."],
                [W(str(k + 2), "counted lines that do not make matching halves"), W(str(k - 1), "missed a line of symmetry"), W(str(k * 2), "counted each line twice"), W("1", "found only one line")],
                FN("sym_count", pts=pts_of(nm)), qtype="conceptual", claim=f"Number of lines of symmetry: {nm}{extra}")


@fam("012")
def sy_fold_measure(r, L):
    half = r.randint(6, 30) if L < 2 else r.randint(25, 90)
    u = pick(r, ["square centimeters", "square inches"])
    if r.random() < 0.5:
        return Item(f"A figure has a line of symmetry. The part of the figure on one side of the line has an area of {half} {u}. What is the area of the whole figure?", f"{2 * half} {u}",
                    ["A line of symmetry splits a figure into two matching parts with equal areas.", f"2 × {half} = {2 * half} {u}."],
                    [W(f"{half} {u}", "gave the area of one part"), W(f"{half + 2} {u}", "added 2 instead of doubling"), W(f"{4 * half} {u}", "doubled twice"), W(f"{half * half} {u}", "multiplied the area by itself")],
                    EX(f"2 × {half}", unit=u), qtype="conceptual", tags={"reasoning"})
    return Item(f"A figure that has an area of {2 * half} {u} is folded on its line of symmetry. What is the area of each matching part?", f"{half} {u}",
                ["A line of symmetry splits a figure into two matching parts with equal areas.", f"{2 * half} ÷ 2 = {half} {u}."],
                [W(f"{2 * half} {u}", "gave the area of the whole figure"), W(f"{4 * half} {u}", "doubled instead of halving"), W(f"{2 * half - 2} {u}", "subtracted 2 instead of dividing"), W(f"{half + 1} {u}", "made a division mistake")],
                EX(f"{2 * half} ÷ 2", unit=u), qtype="conceptual", tags={"reasoning"})


SKILLS = {
    1: dict(name="Points, Lines, Rays, and Angles", fams=[pl_identify, pl_name, pl_angle_type, pl_angle_fig, pl_count_right, pl_count_parallel, pl_definitions, pl_count_angle_types]),
    2: dict(name="Measuring Angles", fams=[an_protractor, an_protractor_offset, an_fraction_turn, an_one_degree, an_clock_turn, an_estimate, an_vs_right, an_turn_to_fraction]),
    3: dict(name="Adding and Subtracting Angle Measures", fams=[aa_add, aa_missing, aa_right, aa_straight, aa_word, aa_equation, aa_equal_parts]),
    4: dict(name="Classifying Triangles and Quadrilaterals", fams=[cl_triangle_angles, cl_right_triangle_which, cl_quad_describe, cl_quad_figure, cl_always, cl_row_property, cl_third_angle]),
    5: dict(name="Lines of Symmetry", fams=[sy_is_line, sy_count, sy_which_line, sy_which_shape, sy_named, sy_fold_measure]),
}
