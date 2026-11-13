"""Unit 11: Perimeter and Shapes (perimeter-shapes)."""
from g3lib import *

UNIT_ID = "perimeter-shapes"
LIN = ["centimeters", "inches", "feet", "meters", "units"]

# Shape catalog (coordinates are exact; the verifier classifies them from the coordinates).
SHAPES = {
    "square": dict(pts=[[0, 0], [4, 0], [4, 4], [0, 4]], ticks=[[0, 1], [1, 1], [2, 1], [3, 1]], right=[0, 1, 2, 3]),
    "rectangle": dict(pts=[[0, 0], [7, 0], [7, 3], [0, 3]], ticks=[[0, 1], [1, 2], [2, 1], [3, 2]], right=[0, 1, 2, 3]),
    "rhombus": dict(pts=[[0, 0], [5, 0], [8, 4], [3, 4]], ticks=[[0, 1], [1, 1], [2, 1], [3, 1]], right=[]),
    "trapezoid": dict(pts=[[0, 0], [8, 0], [6, 3], [2, 3]], ticks=[], right=[]),
    "kite": dict(pts=[[0, 3], [3, 0], [9, 3], [3, 6]], ticks=[[0, 1], [1, 2], [2, 2], [3, 1]], right=[]),
    "quadrilateral": dict(pts=[[0, 0], [6, 0], [5, 4], [1, 3]], ticks=[], right=[]),
    "triangle": dict(pts=[[0, 0], [6, 0], [2, 4]], ticks=[], right=[]),
    "pentagon": dict(pts=[[2, 0], [6, 0], [8, 3], [4, 6], [0, 3]], ticks=[], right=[]),
    "hexagon": dict(pts=[[2, 0], [6, 0], [8, 3], [6, 6], [2, 6], [0, 3]], ticks=[], right=[]),
}
DESC = {"square": "4 equal sides and 4 right angles", "rectangle": "4 right angles, opposite sides equal", "rhombus": "4 equal sides, no right angles",
        "trapezoid": "4 sides, one pair of parallel sides", "kite": "4 sides, two pairs of equal sides next to each other", "quadrilateral": "4 sides of different lengths",
        "triangle": "3 sides", "pentagon": "5 sides", "hexagon": "6 sides"}


def poly_shape(r, n, lo, hi):
    """A convex polygon drawn to scale with whole-number side labels that match the drawing (rounded)."""
    import math as _m
    for _ in range(50):
        angs = sorted(r.uniform(0, 2 * _m.pi) for _ in range(n))
        gaps = [(angs[(i + 1) % n] - angs[i]) % (2 * _m.pi) for i in range(n)]
        if min(gaps) < 0.6 or max(gaps) > _m.pi * 0.95:
            continue
        pts = [[_m.cos(a), _m.sin(a)] for a in angs]
        lens = [_m.dist(pts[i], pts[(i + 1) % n]) for i in range(n)]
        k = r.uniform(lo, hi) / (sum(lens) / n)
        sides = [max(1, round(k * x)) for x in lens]
        if max(sides) < sum(sides) - max(sides) and all(abs(sd - k * x) <= 0.5 for sd, x in zip(sides, lens)):
            return [[round(x * k, 3), round(y * k, 3)] for x, y in pts], sides
    raise Reject()


# ============================================================== S1 Finding Perimeter
@fam("012")
def pe_rect(r, L):
    w, h = (r.randint(2, 6), r.randint(2, 5)) if L == 0 else (r.randint(4, 15), r.randint(3, 12)) if L == 1 else (r.randint(12, 45), r.randint(8, 30))
    need(w != h)
    u = pick(r, LIN)
    alt = f"A rectangle. One long side is labeled {w} {u} and one short side is labeled {h} {u}."
    return Item("Find the perimeter of the rectangle.", f"{2 * (w + h)} {u}", [f"Opposite sides of a rectangle are equal: {w}, {h}, {w}, {h}.", f"{w} + {h} + {w} + {h} = {2 * (w + h)} {u}."],
                [W(f"{w + h} {u}", "added only the two labeled sides"), W(f"{w * h} {u}", "found the area"), W(f"{2 * w + h} {u}", "missed a side")],
                EX(f"2*{w}+2*{h}", unit=u), qtype="visual", diagram=Diagram("rects", {"w": 7, "h": 4, "wt": f"{w} {u}", "ht": f"{h} {u}"}, alt + " (not drawn to scale)"))


@fam("012")
def pe_poly(r, L):
    n = pick(r, [3, 4, 5, 6]) if L else pick(r, [3, 4])
    pts, sides = poly_shape(r, n, 3, 9) if L < 2 else poly_shape(r, n, 12, 60)
    u = pick(r, LIN)
    nm = {3: "triangle", 4: "quadrilateral", 5: "pentagon", 6: "hexagon"}[n]
    alt = f"A {nm} with sides labeled " + ", ".join(f"{s} {u}" for s in sides) + "."
    return Item(f"Find the perimeter of the {nm}.", f"{sum(sides)} {u}", ["Add all the side lengths.", f"{' + '.join(map(str, sides))} = {sum(sides)} {u}."],
                [W(f"{sum(sides) - sides[-1]} {u}", "missed a side"), W(f"{sum(sides) + sides[0]} {u}", "added a side twice"), W(f"{sum(sides) - 10} {u}", "made an adding error")],
                EX("+".join(map(str, sides)), unit=u), qtype="visual", diagram=Diagram("shape", {"pts": pts, "side_labels": [[i, f"{s} {u}" if n < 6 else str(s)] for i, s in enumerate(sides)], "fill": "green"}, alt))


@fam("012")
def pe_grid(r, L):
    from u10_area import lshape_cells, rect_cells, perim_cells
    if L == 0:
        h, w = r.randint(2, 4), r.randint(2, 6)
        cells = rect_cells(1, 1, h, w)
        R, C = h + 2, w + 2
    else:
        cells, H, Wd = lshape_cells(r, L)
        cells = [[i + 1, j + 1] for i, j in cells]
        R, C = H + 2, Wd + 2
    p = perim_cells(cells)
    alt = f"A figure of {len(cells)} unit squares on a grid; each square side is 1 unit."
    return Item("Each side of a small square is 1 unit. What is the perimeter of the shaded figure?", f"{p} units",
                ["Count the unit lengths all the way around the outside.", f"The perimeter is {p} units."],
                [W(f"{len(cells)} units", "counted the squares inside (area)"), W(f"{p - 2} units", "missed some sides"), W(f"{p + 4} units", "counted the corners twice")],
                FN("grid_perim", cells=cells, unit="units"), qtype="visual",
                diagram=Diagram("grid", {"rows": R, "cols": C, "cells": cells, "label": "", "tiled": False}, alt))


@fam("012")
def pe_word(r, L):
    w, h = (r.randint(3, 9), r.randint(2, 7)) if L < 2 else (r.randint(15, 60), r.randint(10, 40))
    t = pick(r, [("A garden is {w} feet long and {h} feet wide. How many feet of fence go all the way around it?", "feet"),
                 ("A picture frame is {w} inches long and {h} inches wide. How much ribbon goes around the edge?", "inches"),
                 ("A playground is {w} meters long and {h} meters wide. How far is it around the playground?", "meters")])
    return Item(t[0].format(w=w, h=h), f"{2 * (w + h)} {t[1]}", [f"Go around: {w} + {h} + {w} + {h}.", f"The perimeter is {2 * (w + h)} {t[1]}."],
                [W(f"{w + h} {t[1]}", "added only two sides"), W(f"{w * h} {t[1]}", "found the area"), W(f"{2 * w + h} {t[1]}", "missed a side")],
                EX(f"2*{w}+2*{h}", unit=t[1]), qtype="word-problem", tags={"modeling"})


@fam("12")
def pe_square(r, L):
    s = r.randint(3, 12) if L == 1 else r.randint(13, 25)
    u = pick(r, LIN)
    return Item(f"A square has sides that are {s} {u} long. What is its perimeter?", f"{4 * s} {u}", ["A square has 4 equal sides.", f"4 × {s} = {4 * s} {u}."],
                [W(f"{s * s} {u}", "found the area"), W(f"{2 * s} {u}", "added only two sides"), W(f"{s + 4} {u}", "added 4 instead of multiplying")],
                EX(f"{s}+{s}+{s}+{s}", unit=u), qtype="procedural")


@fam("2", mode="mc")
def pe_error(r, L):
    w, h = r.randint(4, 12), r.randint(3, 9)
    need(w != h)
    good = f"{2 * (w + h)} units, because all four sides must be added"
    bad = [f"{w + h} units, because only two sides are labeled", f"{w * h} units, because you multiply the sides", f"{2 * w + h} units, because the top and bottom are the same"]
    return mc_key(f"A rectangle is {w} units long and {h} units wide. {name(r)} says the perimeter is {w + h} units. What is the correct perimeter?", good, bad,
                  ["Perimeter is the distance all the way around.", f"{w} + {h} + {w} + {h} = {2 * (w + h)}."], qtype="error-analysis", tags={"misconception"}, r=r)


# ============================================================== S2 Finding an Unknown Side Length
@fam("012")
def us_poly(r, L):
    n = pick(r, [3, 4]) if L == 0 else pick(r, [4, 5, 6])
    pts, sides = poly_shape(r, n, 3, 9) if L < 2 else poly_shape(r, n, 10, 40)
    k = r.randrange(n)
    P = sum(sides)
    u = pick(r, LIN)
    nm = {3: "triangle", 4: "quadrilateral", 5: "pentagon", 6: "hexagon"}[n]
    labels = [[i, (f"{s} {u}" if n < 6 else str(s)) if i != k else "?"] for i, s in enumerate(sides)]
    alt = f"A {nm} with sides " + ", ".join("?" if i == k else f"{s}" for i, s in enumerate(sides)) + f" {u}. The perimeter is {P} {u}."
    known = sum(s for i, s in enumerate(sides) if i != k)
    return Item(f"The perimeter of the {nm} is {P} {u}. What is the length of the side marked ?", f"{sides[k]} {u}",
                [f"Add the known sides: {known}.", f"{P} − {known} = {sides[k]} {u}."],
                [W(f"{P + known} {u}", "added instead of subtracting"), W(f"{known} {u}", "gave the sum of the known sides"), W(f"{P - sides[(k + 1) % n]} {u}", "subtracted only one side")],
                EX(f"{P}-" + "-".join(str(x) for i, x in enumerate(sides) if i != k), unit=u), qtype="visual", diagram=Diagram("shape", {"pts": pts, "side_labels": labels, "fill": "blue"}, alt))


@fam("012")
def us_rect(r, L):
    w, h = (r.randint(3, 9), r.randint(2, 7)) if L < 2 else (r.randint(10, 30), r.randint(6, 20))
    need(w != h)
    P = 2 * (w + h)
    u = pick(r, LIN)
    return Item(f"A rectangle has a perimeter of {P} {u}. Its length is {w} {u}. What is its width?", f"{h} {u}",
                [f"Two lengths: {w} + {w} = {2 * w}. {P} − {2 * w} = {2 * h} for the two widths.", f"{2 * h} ÷ 2 = {h} {u}."],
                [W(f"{P - w} {u}", "subtracted only one length"), W(f"{P - 2 * w} {u}", "forgot that there are two widths"), W(f"{P // w if P % w == 0 and P // w != h else h + 1} {u}", "divided by the length")],
                EX(f"({P}-2*{w})/2", unit=u), qtype="multi-step", tags={"multistep"})


@fam("012")
def us_square(r, L):
    s = r.randint(2, 9) if L < 2 else r.randint(10, 25)
    u = pick(r, LIN)
    return Item(f"A square has 4 equal sides and a perimeter of {4 * s} {u}. How long is each side?", f"{s} {u}", ["A square has 4 equal sides.", f"{4 * s} ÷ 4 = {s} {u}."],
                [W(f"{4 * s - 4} {u}", "subtracted 4"), W(f"{2 * s} {u}", "divided by 2"), W(f"{4 * s} {u}", "gave the perimeter")],
                EX(f"{4 * s}/4", unit=u), qtype="procedural")


@fam("12")
def us_fence(r, L):
    w, h = r.randint(6, 20), r.randint(4, 15)
    need(w != h)
    have = 2 * w + h
    return Item(f"A garden is {w} feet long and {h} feet wide. {name(r)} has already put fence on three sides: both long sides and one short side. How many more feet of fence are needed?",
                f"{h} feet", [f"Fence used: {w} + {w} + {h} = {have}. Whole perimeter: {2 * (w + h)}.", f"{2 * (w + h)} − {have} = {h} feet."],
                [W(f"{2 * (w + h)} feet", "gave the whole perimeter"), W(f"{w} feet", "used a long side"), W(f"{have} feet", "gave the fence already used")],
                EX(f"2*{w}+2*{h}-(2*{w}+{h})", unit="feet"), qtype="multi-step", tags={"reasoning"})


@fam("2", mode="mc")
def us_error(r, L):
    sides = [r.randint(3, 9) for _ in range(4)]
    need(len(set(sides)) >= 3)
    P = sum(sides)
    good = f"{sides[3]} units. Add the three known sides and subtract from {P}."
    bad = [f"{P // 4} units. Divide the perimeter by 4.", f"{P - sides[0]} units. Subtract one side.", f"{P + sum(sides[:3])} units. Add all the numbers."]
    need(P // 4 != sides[3] or P % 4)
    it = mc_key(f"A quadrilateral has a perimeter of {P} units. Three sides are {sides[0]}, {sides[1]}, and {sides[2]} units. {name(r)} divided {P} by 4. What is the missing side?", good, bad,
                ["Dividing by 4 only works when all 4 sides are equal.", f"{P} − {sides[0] + sides[1] + sides[2]} = {sides[3]}."], qtype="error-analysis", tags={"misconception"}, r=r)
    it.check = FN("lead_side", P=P, known=sides[:3])
    return it


# ============================================================== S3 Same Perimeter or Same Area
def rects_with_perim(P):
    return [(w, P // 2 - w) for w in range(1, P // 4 + 1) if P // 2 - w >= w]


def rects_with_area(A):
    return [(w, A // w) for w in range(1, int(A ** 0.5) + 1) if A % w == 0]


@fam("012", mode="mc")
def sp_same_perim(r, L):
    P = pick(r, [12, 14, 16, 18, 20, 24])
    rs = rects_with_perim(P)
    need(len(rs) >= 3)
    a, b = r.sample(rs, 2)
    good = f"{b[1]} by {b[0]}"
    others = [(w, h) for w in range(1, 10) for h in range(w, 12) if 2 * (w + h) != P and w * h != a[0] * a[1]]
    bad = [f"{h} by {w}" for w, h in r.sample(others, 3)]
    it = mc_key(f"A rectangle is {a[1]} by {a[0]}. Which rectangle has the SAME perimeter?", good, bad,
                [f"Perimeter of {a[1]} by {a[0]}: 2 × ({a[1]} + {a[0]}) = {P}.", f"{b[1]} by {b[0]}: 2 × ({b[1]} + {b[0]}) = {P}."], qtype="conceptual", r=r)
    it.check = FN("same_perim", w=a[1], h=a[0])
    return it


@fam("012", mode="mc")
def sp_same_area(r, L):
    A = pick(r, [12, 16, 18, 20, 24, 36])
    rs = rects_with_area(A)
    need(len(rs) >= 2)
    a, b = r.sample(rs, 2)
    good = f"{b[1]} by {b[0]}"
    others = [(w, h) for w in range(1, 10) for h in range(w, 12) if w * h != A]
    bad = [f"{h} by {w}" for w, h in r.sample(others, 3)]
    it = mc_key(f"A rectangle is {a[1]} by {a[0]}. Which rectangle has the SAME area?", good, bad,
                [f"Area of {a[1]} by {a[0]}: {a[1]} × {a[0]} = {A}.", f"{b[1]} × {b[0]} = {A}."], qtype="conceptual", r=r)
    it.check = FN("same_area", w=a[1], h=a[0])
    return it


@fam("012")
def sp_compute_both(r, L):
    P = pick(r, [12, 16, 20]) if L == 0 else pick(r, [14, 18, 22, 24])
    rs = rects_with_perim(P)
    a, b = r.sample(rs, 2)
    ask = pick(r, ["diff"]) if L else "which"
    if a[0] * a[1] == b[0] * b[1]:
        raise Reject()
    if ask == "which":
        big = a if a[0] * a[1] > b[0] * b[1] else b
        return Item(f"Rectangle A is {a[1]} by {a[0]}. Rectangle B is {b[1]} by {b[0]}. Both have a perimeter of {P}. Which rectangle has the greater area, A or B?",
                    "A" if big == a else "B", [f"A: {a[1]} × {a[0]} = {a[0] * a[1]}. B: {b[1]} × {b[0]} = {b[0] * b[1]}.", f"Rectangle {'A' if big == a else 'B'} has the greater area."],
                    [W("B" if big == a else "A", "compared side lengths instead of areas")], FN("bigger_area", A=[a[1], a[0]], B=[b[1], b[0]]), qtype="conceptual", mode="sa")
    return Item(f"Rectangle A is {a[1]} by {a[0]}. Rectangle B is {b[1]} by {b[0]}. They have the same perimeter. How much greater is the larger area than the smaller area?",
                f"{abs(a[0] * a[1] - b[0] * b[1])} square units", [f"A: {a[0] * a[1]}. B: {b[0] * b[1]}.", f"The difference is {abs(a[0] * a[1] - b[0] * b[1])} square units."],
                [W("0 square units", "thought same perimeter means same area"), W(f"{P} square units", "gave the perimeter"), W(f"{max(a[0] * a[1], b[0] * b[1])} square units", "gave one area")],
                EX(f"{a[1]}*{a[0]}-{b[1]}*{b[0]}" if a[0] * a[1] > b[0] * b[1] else f"{b[1]}*{b[0]}-{a[1]}*{a[0]}", unit="square units"), qtype="multi-step", tags={"multistep"})


@fam("012", mode="mc")
def sp_true(r, L):
    good, bad = pick(r, [("Two rectangles can have the same perimeter but different areas.", ["Rectangles with the same perimeter always have the same area.", "Rectangles with the same area always have the same perimeter.", "Area and perimeter are the same thing."]),
                         ("Two rectangles can have the same area but different perimeters.", ["Rectangles with the same area always have the same perimeter.", "A longer rectangle always has a greater area.", "Area and perimeter are the same thing."])])
    return mc_key("Which statement is true?", good, bad, ["Try examples: 1 by 5 and 2 by 4 both have perimeter 12, but areas 5 and 8.", good], qtype="conceptual", tags={"reasoning"}, r=r)


@fam("12")
def sp_count(r, L):
    P = pick(r, [12, 14, 16, 18, 20])
    rs = rects_with_perim(P)
    return Item(f"How many different rectangles with whole-number side lengths have a perimeter of {P} units? (2 by 4 and 4 by 2 count as the same rectangle.)", len(rs),
                [f"Length + width must be {P // 2}.", "Pairs: " + ", ".join(f"{h} by {w}" for w, h in rs) + f": {len(rs)} rectangles."],
                [W(len(rs) + 1, "counted a rectangle with a side of 0"), W(2 * len(rs), "counted turned-around rectangles twice"), W(len(rs) - 1, "missed one")], FN("count_rects", P=P), qtype="explain", tags={"reasoning"})


@fam("2")
def sp_max_area(r, L):
    P = pick(r, [12, 16, 20, 24])
    rs = rects_with_perim(P)
    best = max(rs, key=lambda x: x[0] * x[1])
    return Item(f"{name(r)} has {P} feet of fence to make a rectangular pen with whole-number sides. What is the greatest area the pen can have?", f"{best[0] * best[1]} square feet",
                ["List the rectangles: " + ", ".join(f"{h} by {w} (area {w * h})" for w, h in rs) + ".", f"The greatest area is {best[0] * best[1]} square feet."],
                [W(f"{P} square feet", "gave the perimeter"), W(f"{rs[0][0] * rs[0][1]} square feet", "used the longest, thinnest rectangle"), W(f"{(P // 4) ** 2 + 1} square feet", "made a multiplying error")],
                FN("max_area", P=P, unit="square feet"), qtype="multi-step", tags={"multistep", "reasoning"})


@fam("2")
def sp_min_perim(r, L):
    A = pick(r, [12, 16, 18, 24, 36])
    rs = rects_with_area(A)
    best = min(rs, key=lambda x: x[0] + x[1])
    return Item(f"A rectangle has an area of {A} square units and whole-number sides. What is the smallest perimeter it can have?", f"{2 * sum(best)} units",
                ["List the rectangles: " + ", ".join(f"{h} by {w} (perimeter {2 * (w + h)})" for w, h in rs) + ".", f"The smallest perimeter is {2 * sum(best)} units."],
                [W(f"{A} units", "gave the area"), W(f"{2 * sum(rs[0])} units", "used the longest, thinnest rectangle"), W(f"{sum(best)} units", "added only two sides")],
                FN("min_perim", A=A, unit="units"), qtype="multi-step", tags={"multistep", "reasoning"})


# ============================================================== S4 Shape Attributes and Quadrilaterals
def row_of(names, r):
    labels = ["A", "B", "C", "D"]
    items = []
    for lab, nm in zip(labels, names):
        sp = SHAPES[nm]
        items.append({"pts": sp["pts"], "label": lab, "right": sp["right"], "ticks": sp["ticks"]})
    alt = "Four shapes. " + " ".join(f"{lab}: {DESC[nm]}{' (right angles marked)' if SHAPES[nm]['right'] else ''}." for lab, nm in zip(labels, names))
    return Diagram("shape_row", {"items": items}, alt)


@fam("012", mode="mc")
def qa_not_quad(r, L):
    odd = pick(r, ["triangle", "pentagon", "hexagon"])
    quads = r.sample(["square", "rectangle", "rhombus", "trapezoid", "kite", "quadrilateral"], 3)
    names = quads + [odd]
    r.shuffle(names)
    good = "ABCD"[names.index(odd)]
    it = mc_key("Which shape is NOT a quadrilateral?", good, [x for x in "ABCD" if x != good], ["A quadrilateral has exactly 4 sides.", f"Shape {good} is a {odd}."],
                qtype="visual", diagram=row_of(names, r), r=r)
    it.check = FN("shape_pick", shapes=[SHAPES[n]["pts"] for n in names], want="not_quad")
    return it


@fam("012", mode="mc")
def qa_which(r, L):
    target = pick(r, ["square", "rhombus", "rectangle"]) if L < 2 else pick(r, ["rhombus_not_square", "rectangle_not_square", "neither"])
    pool = ["square", "rectangle", "rhombus", "trapezoid", "kite", "quadrilateral"]
    if target == "square":
        names = ["square"] + r.sample(["rhombus", "trapezoid", "kite", "quadrilateral"], 3)
    elif target == "rhombus":
        names = ["rhombus"] + r.sample(["rectangle", "trapezoid", "kite", "quadrilateral"], 3)
    elif target == "rectangle":
        names = ["rectangle"] + r.sample(["rhombus", "trapezoid", "kite", "quadrilateral"], 3)
    elif target == "rhombus_not_square":
        names = ["rhombus", "square", "rectangle", pick(r, ["trapezoid", "kite"])]
    elif target == "rectangle_not_square":
        names = ["rectangle", "square", "rhombus", pick(r, ["trapezoid", "kite"])]
    else:
        names = [pick(r, ["trapezoid", "kite", "quadrilateral"]), "square", "rectangle", "rhombus"]
    r.shuffle(names)
    q = {"square": "Which shape is a square?", "rhombus": "Which shape is a rhombus?", "rectangle": "Which shape is a rectangle?",
         "rhombus_not_square": "Which shape is a rhombus but NOT a square?", "rectangle_not_square": "Which shape is a rectangle but NOT a square?",
         "neither": "Which quadrilateral is NOT a rhombus, a rectangle, or a square?"}[target]
    key_name = {"rhombus_not_square": "rhombus", "rectangle_not_square": "rectangle"}.get(target, target)
    if target == "neither":
        key_name = [n for n in names if n not in ("square", "rectangle", "rhombus")][0]
    good = "ABCD"[names.index(key_name)]
    it = mc_key(q, good, [x for x in "ABCD" if x != good], ["Check the sides (tick marks show equal sides) and the corners (squares show right angles).", f"Shape {good}: {DESC[key_name]}."],
                qtype="visual", diagram=row_of(names, r), r=r)
    it.check = FN("shape_pick", shapes=[SHAPES[n]["pts"] for n in names], want=target)
    return it


@fam("012", mode="mc")
def qa_also(r, L):
    q, good, bad = pick(r, [("Every square is also a kind of ___.", "rectangle", ["triangle", "pentagon", "trapezoid only"]),
                            ("Every square is also a kind of ___.", "rhombus", ["triangle", "hexagon", "kite only"]),
                            ("Every rhombus is also a kind of ___.", "quadrilateral", ["square", "rectangle", "triangle"]),
                            ("Every rectangle is also a kind of ___.", "quadrilateral", ["square", "rhombus", "pentagon"])])
    return mc_key(q, good, bad, ["A shape belongs to every category whose attributes it has.", f"{q.replace('___', good)}"], qtype="conceptual", tags={"reasoning"}, r=r)


@fam("012", mode="mc")
def qa_attribute(r, L):
    a, b, good, bad = pick(r, [("rhombuses", "squares", "4 equal sides", ["4 right angles always", "3 sides", "no equal sides"]),
                               ("rectangles", "squares", "4 right angles", ["4 equal sides always", "5 sides", "no right angles"]),
                               ("rhombuses", "rectangles", "4 sides", ["4 right angles", "4 equal sides", "3 right angles"]),
                               ("squares", "rectangles", "4 right angles", ["4 equal sides", "5 sides", "only 2 right angles"])])
    return mc_key(f"What attribute do ALL {a} and ALL {b} share?", good, bad, ["List the attributes each category must have.", f"Both always have {good}."], qtype="conceptual", tags={"reasoning"}, r=r)


@fam("12")
def qa_count(r, L):
    nm = pick(r, ["triangle", "quadrilateral", "pentagon", "hexagon"])
    k = r.randint(2, 6)
    n = {"triangle": 3, "quadrilateral": 4, "pentagon": 5, "hexagon": 6}[nm]
    return Item(f"How many sides do {k} {nm}s have in all?", k * n, [f"A {nm} has {n} sides.", f"{k} × {n} = {k * n} sides."],
                [W(k + n, "added"), W(k * (n - 1), "used the wrong number of sides"), W(n, "counted one shape")], FN("poly_sides", name=nm, count=k), qtype="procedural")


@fam("2", mode="mc")
def qa_error(r, L):
    good = "No. A square has 4 right angles and opposite sides equal, so it is a rectangle too."
    bad = ["Yes. Squares and rectangles are different shapes.", "Yes. A rectangle must have two long sides.", "No. A square is a rhombus, so it cannot be a rectangle."]
    return mc_key(f"{name(r)} says a square is NOT a rectangle. Is that right?", good, bad, ["Check the attributes of a rectangle: 4 sides, 4 right angles.", "A square has all of them."],
                  qtype="error-analysis", tags={"misconception"}, r=r)


# ============================================================== S5 Partitioning Shapes into Equal Areas
PARTS = [({"shape": "rect", "cuts": "v", "widths": [1, 1]}, 2), ({"shape": "rect", "cuts": "v", "widths": [1, 1, 1]}, 3), ({"shape": "rect", "cuts": "v", "widths": [1, 1, 1, 1]}, 4),
         ({"shape": "square", "cuts": "grid", "rows": 2, "cols": 2}, 4), ({"shape": "square", "cuts": "diag4"}, 4), ({"shape": "rect", "cuts": "diag2"}, 2),
         ({"shape": "circle", "n": 3}, 3), ({"shape": "circle", "n": 4}, 4), ({"shape": "circle", "n": 6}, 6), ({"shape": "circle", "n": 8}, 8), ({"shape": "hexagon", "cuts": "tri6"}, 6),
         ({"shape": "hexagon", "cuts": "rhomb3"}, 3), ({"shape": "hexagon", "cuts": "trap2"}, 2), ({"shape": "rect", "cuts": "grid", "rows": 2, "cols": 3}, 6),
         ({"shape": "rect", "cuts": "grid", "rows": 2, "cols": 4}, 8), ({"shape": "triangle", "cuts": "mid2"}, 2), ({"shape": "rect", "cuts": "v", "widths": [1] * 6}, 6)]
UNEQUAL = [({"shape": "rect", "cuts": "v", "widths": [1, 2, 1]}, 3), ({"shape": "circle", "angles": [180, 90, 90]}, 3), ({"shape": "triangle", "cuts": "off2"}, 2),
           ({"shape": "rect", "cuts": "v", "widths": [2, 1]}, 2), ({"shape": "circle", "angles": [120, 60, 90, 90]}, 4), ({"shape": "rect", "cuts": "v", "widths": [1, 1, 2]}, 3)]


def cut_words(spec):
    c = spec.get("cuts")
    if spec["shape"] == "circle":
        return "cut through the center" if not spec.get("angles") else "cut through the center into pieces of different sizes"
    return {"v": "by straight lines from top to bottom", "grid": f"into {spec.get('rows')} rows and {spec.get('cols')} columns", "diag2": "along one diagonal",
            "diag4": "along both diagonals", "tri6": "into 6 triangles from the center", "rhomb3": "into 3 rhombuses", "trap2": "into 2 trapezoids", "mid2": "from the top corner to the middle of the base",
            "off2": "from the top corner to a point that is not the middle of the base"}.get(c, "")


def part_d(spec, shade, equal=True):
    d = dict(spec)
    d["shade"] = shade
    n = len(_areas(spec))
    nm = spec["shape"] if spec["shape"] != "rect" else "rectangle"
    alt = f"A {nm} cut {cut_words(spec)} into {n} {'equal parts' if equal else 'parts that are not all the same size'}; {len(shade)} {'part is' if len(shade) == 1 else 'parts are'} shaded."
    return Diagram("partition", d, alt)


def _areas(spec):
    s = spec["shape"]
    if s in ("rect", "square"):
        return spec["widths"] if spec["cuts"] == "v" else [1] * (spec["rows"] * spec["cols"]) if spec["cuts"] == "grid" else [1] * (2 if spec["cuts"] == "diag2" else 4)
    if s == "circle":
        return spec.get("angles") or [1] * spec["n"]
    if s == "hexagon":
        return [1] * {"tri6": 6, "rhomb3": 3, "trap2": 2}[spec["cuts"]]
    return [1, 1]


@fam("012")
def pa_unit(r, L):
    spec, n = pick(r, PARTS if L else [p for p in PARTS if p[1] <= 4])
    return Item("The shape is split into parts with equal area. What fraction of the whole area is the shaded part?", fr(1, n),
                [f"There are {n} parts with equal area.", f"One part is 1/{n} of the whole area."],
                [W(fr(1, n - 1) if n > 2 else fr(1, 3), "counted the unshaded parts"), W(fr(n, 1), "switched the numerator and denominator"), W(fr(1, n + 1), "miscounted the parts")],
                FN("partition_frac", spec=spec, shade=[0]), qtype="visual", diagram=part_d(spec, [0]))


@fam("012", mode="mc")
def pa_equal(r, L):
    if r.random() < 0.5:
        spec, n = pick(r, PARTS)
        good = f"Yes. The {n} parts have equal area."
        bad = [f"No. The parts are different shapes.", f"No. There should be {n + 1} parts.", "No. The parts are not equal."]
        d = part_d(spec, [0])
        eq = True
    else:
        spec, n = pick(r, UNEQUAL)
        good = "No. The parts do not have equal area."
        bad = [f"Yes. There are {n} parts.", f"Yes. Each part is 1/{n}.", "Yes. All the lines are straight."]
        d = part_d(spec, [0], equal=False)
        eq = False
    it = mc_key("Is the shape split into parts with equal area?", good, bad, ["Equal parts must cover the same amount of space.", good], qtype="visual", tags={"reasoning"}, diagram=d, r=r)
    it.check = FN("partition_equal", spec=spec)
    return it


@fam("012")
def pa_grid_count(r, L):
    rows, cols = pick(r, [(2, 4), (2, 6), (3, 4), (4, 4), (2, 3), (3, 6)])
    n = pick(r, [k for k in (2, 3, 4, 6) if (rows * cols) % k == 0 and k < rows * cols])
    total = rows * cols
    return Item(f"A rectangle is made of {total} unit squares. It is split into {n} parts with equal area. How many unit squares are in each part?", total // n,
                [f"Equal area means each part has the same number of unit squares.", f"{total} ÷ {n} = {total // n} unit squares."],
                [W(n, "gave the number of parts"), W(total - n, "subtracted"), W(total // n + 1, "used a nearby fact")], EX(f"{total}/{n}"), qtype="procedural", tags={"connections"})


@fam("12")
def pa_shaded_more(r, L):
    spec, n = pick(r, [p for p in PARTS if p[1] >= 3])
    k = r.randint(2, n - 1)
    return Item("The shape is split into parts with equal area. What fraction of the whole area is shaded?", fr(k, n), [f"There are {n} equal parts and {k} are shaded.", f"{k} parts of 1/{n} is {k}/{n}."],
                [W(fr(k, n - k) if n - k != k else fr(k + 1, n), "wrote shaded parts over unshaded parts"), W(fr(1, n), "named only one part"), W(fr(n - k, n) if n - k != k else fr(k, n + 1), "named the unshaded parts")],
                FN("partition_frac", spec=spec, shade=list(range(k))), qtype="visual", diagram=part_d(spec, list(range(k))))


@fam("2", mode="mc")
def pa_diff_shapes(r, L):
    good = "Yes. Both triangles are half of the square, so they have equal area."
    bad = ["No. Equal parts must be squares.", "No. The triangles are bigger than half.", "Yes, but only because they have 3 sides."]
    return mc_key("A square is cut along one diagonal into 2 triangles. Is each triangle 1/2 of the area of the square?", good, bad,
                  ["The diagonal cuts the square into two matching halves.", "Each half has equal area, so each is 1/2."], qtype="explain", tags={"reasoning"},
                  diagram=Diagram("partition", {"shape": "square", "cuts": "diag2", "shade": [0]}, "A square cut along one diagonal into 2 triangles; one triangle is shaded."), r=r)


@fam("2")
def pa_two_ways(r, L):
    total = pick(r, [12, 16, 24])
    a, b = r.sample([k for k in (2, 3, 4, 6, 8) if total % k == 0], 2)
    return Item(f"A rectangle made of {total} unit squares is split into {a} equal parts. Another copy is split into {b} equal parts. How many more unit squares are in each part of the first rectangle than the second?",
                abs(total // a - total // b), [f"{total} ÷ {a} = {total // a} and {total} ÷ {b} = {total // b}.", f"The difference is {abs(total // a - total // b)} unit squares."],
                [W(abs(a - b), "subtracted the numbers of parts"), W(total // min(a, b), "found only one part size"), W(total // a + total // b, "added the part sizes")],
                EX(f"{total}/{a}-{total}/{b}" if total // a > total // b else f"{total}/{b}-{total}/{a}"), qtype="multi-step", tags={"multistep"})


SKILLS = {
    1: dict(name="Finding Perimeter", fams=[pe_rect, pe_poly, pe_grid, pe_word, pe_square, pe_error]),
    2: dict(name="Finding an Unknown Side Length", fams=[us_poly, us_rect, us_square, us_fence, us_error]),
    3: dict(name="Same Perimeter or Same Area", fams=[sp_same_perim, sp_same_area, sp_compute_both, sp_true, sp_count, sp_max_area, sp_min_perim]),
    4: dict(name="Shape Attributes and Quadrilaterals", fams=[qa_not_quad, qa_which, qa_also, qa_attribute, qa_count, qa_error]),
    5: dict(name="Partitioning Shapes into Equal Areas", fams=[pa_unit, pa_equal, pa_grid_count, pa_shaded_more, pa_diff_shapes, pa_two_ways]),
}
