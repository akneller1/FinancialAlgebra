"""Unit 10: Area (area)."""
from g3lib import *

UNIT_ID = "area"
UNITS_SQ = [("square centimeter", "square centimeters"), ("square inch", "square inches"), ("square foot", "square feet"), ("square meter", "square meters"), ("square unit", "square units")]


def rect_cells(r0, c0, h, w):
    return [[r0 + i, c0 + j] for i in range(h) for j in range(w)]


def lshape_cells(r, L):
    Wd, H = r.randint(4, 7), r.randint(3, 5)
    a, b = r.randint(1, Wd - 2), r.randint(1, H - 1)
    cells = [[i, j] for i in range(H) for j in range(Wd) if not (i < b and j >= a)]
    return cells, H, Wd


def grid_d(cells, rows, cols, label="= 1 square unit", tiled=True):
    n = len(cells)
    alt = f"A figure on a grid of unit squares made of {n} shaded squares" + (" with no gaps or overlaps." if tiled else ".") + (f" Key: one square {label[2:]}." if label else "")
    return Diagram("grid", {"rows": rows, "cols": cols, "cells": cells, "label": label, "tiled": tiled}, alt)


# ============================================================== S1 Understanding Area and Unit Squares
@fam("012")
def au_count(r, L):
    if L == 0:
        h, w = r.randint(2, 4), r.randint(2, 5)
        cells, R, C = rect_cells(1, 1, h, w), h + 2, w + 2
    else:
        cells, H, Wd = lshape_cells(r, L)
        cells = [[i + 1, j + 1] for i, j in cells]
        R, C = H + 2, Wd + 2
    n = len(cells)
    return Item("Each small square is 1 square unit. What is the area of the shaded figure?", f"{n} square units",
                ["Count the unit squares that cover the figure with no gaps or overlaps.", f"There are {n} unit squares, so the area is {n} square units."],
                [W(f"{n - 1} square units", "missed a square"), W(f"{perim_cells(cells)} square units", "counted the unit lengths around the edge"), W(f"{n + 2} square units", "counted some squares twice")],
                FN("cells", cells=cells, unit="square units"), qtype="visual", diagram=grid_d(cells, R, C))


def perim_cells(cells):
    s = {tuple(c) for c in cells}
    return sum(1 for (i, j) in s for d in ((1, 0), (-1, 0), (0, 1), (0, -1)) if (i + d[0], j + d[1]) not in s)


@fam("012", mode="mc")
def au_gaps(r, L):
    n = r.randint(8, 20)
    nm = name(r)
    good = "No. The tiles must cover the shape with no gaps or overlaps."
    bad = [f"Yes. The area is {n} square units.", f"Yes, because {n} tiles were used.", "No. Tiles can never measure area."]
    return mc_key(f"{nm} covers a shape with {n} square tiles. Some tiles overlap and there are gaps. Is the area {n} square units?", good, bad,
                  ["Area is the number of unit squares that cover a shape with no gaps and no overlaps.", "Gaps and overlaps make the count wrong."], qtype="conceptual", tags={"reasoning"}, r=r)


@fam("012", mode="mc")
def au_unit_square(r, L):
    q, good, bad = pick(r, [("What is a unit square?", "a square with sides that are each 1 unit long", ["any square on a grid", "a square with an area of 4 units", "a rectangle that is 1 unit long"]),
                            ("How much area does one unit square have?", "1 square unit", ["4 square units", "1 unit", "4 units"]),
                            ("What does area measure?", "how many unit squares cover a flat shape", ["the length around a shape", "how heavy a shape is", "how many sides a shape has"])])
    return mc_key(q, good, bad, ["A unit square has side length 1 unit. Its area is 1 square unit.", good[0].upper() + good[1:] + "."], qtype="conceptual", r=r)


@fam("012")
def au_n(r, L):
    n = r.randint(6, 30) if L else r.randint(4, 12)
    thing = pick(r, ["a rug", "a tabletop", "a poster", "a garden bed", "a game board"])
    return Item(f"{thing.capitalize()} is covered by {n} unit squares with no gaps or overlaps. What is its area?", f"{n} square units",
                ["A figure covered by n unit squares has an area of n square units.", f"The area is {n} square units."],
                [W(f"{n} units", "used a length unit instead of a square unit"), W(f"{n - 1} square units", "miscounted"), W(f"{n * 4} square units", "counted the sides of the squares")],
                FN("cells", count=n, unit="square units"), qtype="conceptual")


@fam("12")
def au_more(r, L):
    h, w = r.randint(3, 6), r.randint(4, 8)
    placed = r.randint(w, h * w - 3)
    return Item(f"{name(r)} wants to cover a rectangle that is {w} units long and {h} units wide with unit squares. {placed} squares are already placed with no gaps or overlaps. How many more squares are needed?",
                f"{h * w - placed} squares", [f"The rectangle needs {h} × {w} = {h * w} unit squares.", f"{h * w} − {placed} = {h * w - placed} more squares."],
                [W(f"{h * w} squares", "gave the total"), W(f"{h + w - placed if h + w > placed else placed - h - w} squares", "added the sides instead of multiplying"), W(f"{placed} squares", "gave the squares already placed")],
                EX(f"{h}*{w}-{placed}", unit="squares"), qtype="multi-step", tags={"multistep"})


@fam("2", mode="mc")
def au_compare(r, L):
    a, b = r.randint(10, 24), r.randint(10, 24)
    need(a != b)
    good = f"Shape {'A' if a > b else 'B'}, because it is covered by more unit squares"
    bad = [f"Shape {'B' if a > b else 'A'}, because it is longer", "They have the same area because both are covered by squares", f"Shape {'B' if a > b else 'A'}, because it has more sides"]
    return mc_key(f"Shape A is covered by {a} unit squares. Shape B is covered by {b} unit squares of the same size. Which has the greater area?", good, bad,
                  ["Compare the number of same-size unit squares.", f"{max(a, b)} > {min(a, b)}."], qtype="explain", tags={"reasoning"}, r=r)


# ============================================================== S2 Measuring Area by Counting Unit Squares
@fam("012")
def ac_units(r, L):
    one, many = pick(r, UNITS_SQ[:4])
    if L == 0:
        h, w = r.randint(2, 4), r.randint(2, 6)
        cells, R, C = rect_cells(1, 1, h, w), h + 2, w + 2
    else:
        cells, H, Wd = lshape_cells(r, L)
        cells = [[i + 1, j + 1] for i, j in cells]
        R, C = H + 2, Wd + 2
    n = len(cells)
    lin = many.replace("square ", "")
    return Item(f"Each small square is 1 {one}. What is the area of the figure?", f"{n} {many}", [f"Count the squares: {n}.", f"The area is {n} {many}."],
                [W(f"{n} {lin}", "used a length unit instead of a square unit"), W(f"{perim_cells(cells)} {many}", "counted the edges around the figure"), W(f"{n - 1} {many}", "missed a square"), W(f"{n + 2} {many}", "counted some squares twice")],
                FN("cells", cells=cells, unit=many), qtype="visual", diagram=grid_d(cells, R, C, f"= 1 {one}"))


@fam("012", mode="mc")
def ac_mc_units(r, L):
    one, many = pick(r, UNITS_SQ[:4])
    h, w = (r.randint(2, 4), r.randint(2, 6)) if L == 0 else (r.randint(3, 6), r.randint(3, 8))
    cells, R, C = rect_cells(1, 1, h, w), h + 2, w + 2
    n = len(cells)
    lin = many.replace("square ", "")
    good = f"{n} {many}"
    bad = [f"{n} {lin}", f"{perim_cells(cells)} {many}", f"{n + w} {many}"]
    it = mc_key(f"Each small square is 1 {one}. What is the area of the rectangle?", good, bad, [f"Count or multiply: {h} × {w} = {n}.", f"The area is {n} {many}."],
                qtype="visual", diagram=grid_d(cells, R, C, f"= 1 {one}"), r=r)
    it.check = FN("cells", cells=cells, unit=many)
    return it


@fam("012", mode="mc")
def ac_choose(r, L):
    thing, good = pick(r, [("the floor of a classroom", "square feet"), ("a postage stamp", "square centimeters"), ("a soccer field", "square meters"), ("a sheet of paper", "square inches"),
                           ("a playground", "square meters"), ("a book cover", "square inches")])
    lin = good.replace("square ", "")
    bad = [lin, "liters", "kilograms"]
    return mc_key(f"Which unit could you use to measure the AREA of {thing}?", good, bad, ["Area is measured in square units.", f"Use {good}."], r=r)


@fam("012")
def ac_unit_name(r, L):
    one, many = pick(r, UNITS_SQ[:4])
    n = r.randint(5, 40)
    side = one.replace("square ", "")
    return Item(f"A shape is covered with {n} squares. Each square is 1 {side} long on each side. What is the area of the shape?", f"{n} {many}",
                [f"A square that is 1 {side} on each side has an area of 1 {one}.", f"{n} of them make {n} {many}."],
                [W(f"{n} {many.replace('square ', '')}", "used a length unit"), W(f"{n * 4} {many}", "counted the sides"), W(f"{n + 1} {many}", "miscounted"), W(f"{n - 1} {many}", "missed a square")],
                FN("cells", count=n, unit=many), qtype="conceptual")


@fam("12", mode="mc")
def ac_compare_units(r, L):
    n = r.randint(6, 15)
    good = f"No. A square inch is bigger than a square centimeter, so the areas are different."
    bad = ["Yes. Both are covered by the same number of squares.", "Yes. The unit does not matter.", "No. Square centimeters are bigger than square inches."]
    return mc_key(f"Shape A is covered by {n} square centimeters. Shape B is covered by {n} square inches. Do they have the same area?", good, bad,
                  ["Compare unit sizes before comparing counts.", "An inch is longer than a centimeter."], qtype="explain", tags={"reasoning"}, r=r)


@fam("2", mode="mc")
def ac_error(r, L):
    one, many = pick(r, UNITS_SQ[:4])
    n = r.randint(10, 30)
    lin = many.replace("square ", "")
    good = f"{n} {many}, because area is measured in square units"
    bad = [f"{n} {lin}, because each side is 1 {lin.rstrip('s') if lin != 'feet' else 'foot'}", f"{n * 4} {many}, because each square has 4 sides", f"{n} {lin} squared, because you multiply"]
    return mc_key(f"{name(r)} counted {n} squares that are each 1 {one} and wrote the area as {n} {lin}. What is the correct answer?", good, bad,
                  ["Area units are square units.", f"The area is {n} {many}."], qtype="error-analysis", tags={"misconception"}, r=r)


# ============================================================== S3 Area of Rectangles
def wh(r, L):
    if L == 0:
        return r.randint(2, 5), r.randint(2, 6)
    if L == 1:
        return r.randint(3, 9), r.randint(3, 9)
    return r.randint(5, 9), r.randint(6, 10)


@fam("012")
def ar_tiled(r, L):
    w, h = wh(r, L)
    need(w != h or L == 0)
    alt = f"A rectangle tiled with unit squares: {h} rows of {w} squares."
    return Item("The rectangle is tiled with unit squares. Find its area. (Count by rows or multiply.)", f"{w * h} square units",
                [f"There are {h} rows with {w} squares in each row.", f"{h} × {w} = {w * h} square units."],
                [W(f"{w + h} square units", "added the side lengths"), W(f"{2 * (w + h)} square units", "found the perimeter"), W(f"{w * h - w} square units", "missed a row")],
                EX(f"{h}*{w}", unit="square units"), qtype="visual", diagram=Diagram("rects", {"w": w, "h": h, "grid": True}, alt))


@fam("012")
def ar_mult(r, L):
    w, h = wh(r, L)
    one, many = pick(r, UNITS_SQ[:4])
    lin = many.replace("square ", "")
    alt = f"A rectangle labeled {w} {lin} long and {h} {lin} wide."
    return Item(f"Find the area of the rectangle.", f"{w * h} {many}", [f"Area = length × width.", f"{w} × {h} = {w * h} {many}."],
                [W(f"{w + h} {many}", "added the side lengths"), W(f"{2 * (w + h)} {many}", "found the perimeter"), W(f"{w * h} {lin}", "used a length unit")],
                EX(f"{w}*{h}", unit=many), qtype="visual", diagram=Diagram("rects", {"w": w, "h": h, "wt": f"{w} {lin}", "ht": f"{h} {lin}"}, alt))


@fam("012")
def ar_word(r, L):
    w, h = wh(r, L)
    t = pick(r, [("A rug is {w} feet long and {h} feet wide. What is its area?", "square feet"), ("A garden is {w} meters long and {h} meters wide. What is the area of the garden?", "square meters"),
                 ("A photo is {w} inches long and {h} inches wide. What is its area?", "square inches"), ("A sticker sheet is {w} centimeters long and {h} centimeters wide. What is its area?", "square centimeters")])
    return Item(t[0].format(w=w, h=h), f"{w * h} {t[1]}", [f"Multiply the side lengths: {w} × {h}.", f"The area is {w * h} {t[1]}."],
                [W(f"{w + h} {t[1]}", "added the side lengths"), W(f"{2 * (w + h)} {t[1]}", "found the perimeter"), W(f"{w * h} {t[1].replace('square ', '')}", "used a length unit")],
                EX(f"{w}*{h}", unit=t[1]), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def ar_equation(r, L):
    w, h = wh(r, L)
    need(w != h)
    good = f"{h} × {w} = {w * h}"
    bad = [f"{h} + {w} = {h + w}", f"{h} + {w} + {h} + {w} = {2 * (h + w)}", f"{h} × {h} = {h * h}"]
    alt = f"A rectangle tiled with unit squares: {h} rows of {w} squares."
    return mc_key("Which equation gives the area of the tiled rectangle?", good, bad, [f"{h} rows of {w} unit squares.", f"{h} × {w} = {w * h} square units."], qtype="visual",
                  diagram=Diagram("rects", {"w": w, "h": h, "grid": True}, alt), r=r)


@fam("12")
def ar_side(r, L):
    w, h = wh(r, L)
    one, many = pick(r, UNITS_SQ[:4])
    lin = many.replace("square ", "")
    return Item(f"A rectangle has an area of {w * h} {many}. One side is {w} {lin}. How long is the other side?", f"{h} {lin}",
                [f"Area = side × side, so {w} × ? = {w * h}.", f"{w * h} ÷ {w} = {h} {lin}."],
                [W(f"{w * h - w} {lin}", "subtracted instead of dividing"), W(f"{h + 1} {lin}", "used a nearby fact"), W(f"{(w * h - 2 * w) // 2 if (w * h - 2 * w) > 0 and (w * h) % 2 == 0 else h + 2} {lin}", "used the perimeter rule")],
                EX(f"{w * h}/{w}", unit=lin), qtype="multi-step", tags={"reasoning"})


@fam("2")
def ar_partial(r, L):
    w, h = wh(r, L)
    return Item(f"Tiles are placed along the top and down the left side of a rectangle: {w} tiles across and {h} tiles down (the corner tile counts in both). How many tiles will cover the whole rectangle?",
                f"{w * h} tiles", [f"The rectangle has {h} rows of {w} tiles.", f"{h} × {w} = {w * h} tiles."],
                [W(f"{w + h - 1} tiles", "counted only the tiles already placed"), W(f"{w + h} tiles", "added the side lengths"), W(f"{w * h - w} tiles", "missed a row")],
                EX(f"{h}*{w}", unit="tiles"), qtype="multi-step", tags={"reasoning"})


# ============================================================== S4 Area and the Distributive Property
def split(r, L):
    h = r.randint(2, 5) if L == 0 else r.randint(3, 8) if L == 1 else r.randint(6, 9)
    a = pick(r, [5, 10]) if L < 2 else pick(r, [5, 4, 6])
    b = r.randint(2, 5) if L < 2 else r.randint(3, 6)
    need(a + b <= 14)
    return h, a, b


def split_d(h, a, b, grid=False):
    alt = f"A rectangle {h} units tall and {a + b} units long, split by a dashed line into a {h} by {a} part and a {h} by {b} part."
    return Diagram("rects", {"w": a + b, "h": h, "split": a, "wta": str(a), "wtb": str(b), "ht": str(h), "grid": grid}, alt)


@fam("012")
def ad_total(r, L):
    h, a, b = split(r, L)
    return Item(f"Find the total area of the rectangle by adding the areas of the two parts.", f"{h * (a + b)} square units",
                [f"Left part: {h} × {a} = {h * a}. Right part: {h} × {b} = {h * b}.", f"{h * a} + {h * b} = {h * (a + b)} square units."],
                [W(f"{h * a + b} square units", "added the side length instead of the area of the second part"), W(f"{h * a} square units", "found only one part"), W(f"{h + a + b} square units", "added the side lengths")],
                EX(f"{h}*{a}+{h}*{b}", unit="square units"), qtype="visual", tags={"multiple-representations"}, diagram=split_d(h, a, b))


@fam("012", mode="mc")
def ad_expr(r, L):
    h, a, b = split(r, L)
    good = f"({h} × {a}) + ({h} × {b})"
    bad = [f"({h} × {a}) + {b}", f"({h} + {a}) × ({h} + {b})", f"({h} × {a}) × ({h} × {b})"]
    it = mc_key("Which expression shows the area of the whole rectangle as the sum of its two parts?", good, bad,
                [f"Each part is a rectangle with height {h}.", f"{good} = {h} × {a + b}."], qtype="visual", tags={"multiple-representations"}, diagram=split_d(h, a, b), r=r)
    it.check = FN("same_value", target=f"{h}*({a}+{b})")
    return it


@fam("012")
def ad_fill(r, L):
    h, a, b = split(r, L)
    eq = f"{h} × {a + b} = ({h} × {a}) + ({h} × ___)"
    return Item(f"The rectangle is split into two parts. Complete the equation: {eq}", b, [f"The long side {a + b} is split into {a} and {b}.", f"{h} × {a + b} = ({h} × {a}) + ({h} × {b})."],
                [W(a + b, "used the whole side"), W(h * b, "wrote the area of the part"), W(a, "repeated the first part")], FN("blank_eq", eq=eq), qtype="visual", diagram=split_d(h, a, b))


@fam("012")
def ad_part(r, L):
    h, a, b = split(r, L)
    which = pick(r, ["left", "right"])
    v = h * (a if which == "left" else b)
    return Item(f"What is the area of the {which} part of the rectangle?", f"{v} square units", [f"The {which} part is {h} by {a if which == 'left' else b}.", f"{h} × {a if which == 'left' else b} = {v} square units."],
                [W(f"{h * (a + b)} square units", "found the whole rectangle"), W(f"{h + (a if which == 'left' else b)} square units", "added the sides"), W(f"{h * (b if which == 'left' else a)} square units", "used the other part")],
                EX(f"{h}*{a if which == 'left' else b}", unit="square units"), qtype="visual", diagram=split_d(h, a, b))


@fam("12", mode="mc")
def ad_choose(r, L):
    h = r.randint(6, 9)
    n = r.randint(7, 9)
    good = f"{h} × 5 and {h} × {n - 5}"
    bad = [f"{h} × 5 and {n - 5}", f"{h} + 5 and {h} + {n - 5}", f"{h} × {n} and {h} × 5"]
    it = mc_key(f"A rectangle is {h} units by {n} units. {name(r)} splits the {n}-unit side into 5 and {n - 5}. Which two areas should be added?", good, bad,
                [f"{n} = 5 + {n - 5}.", f"{h} × {n} = ({h} × 5) + ({h} × {n - 5}) = {h * n}."], qtype="compare-strategies", tags={"reasoning"}, r=r)
    it.check = FN("pair_sum", target=f"{h}*{n}")
    return it


@fam("2")
def ad_word(r, L):
    h, a, b = split(r, 2)
    return Item(f"A garden is {h} feet wide. It has a vegetable part {a} feet long and a flower part {b} feet long, side by side. What is the area of the whole garden?",
                f"{h * (a + b)} square feet", [f"Vegetables: {h} × {a} = {h * a}. Flowers: {h} × {b} = {h * b}.", f"{h * a} + {h * b} = {h * (a + b)} square feet."],
                [W(f"{h * a + b} square feet", "did not multiply the second part"), W(f"{h * a} square feet", "found only one part"), W(f"{2 * (h + a + b)} square feet", "found the perimeter")],
                EX(f"{h}*({a}+{b})", unit="square feet"), qtype="word-problem", tags={"modeling", "multistep"})


# ============================================================== S5 Area of Rectilinear Figures
def lpoly(r, L):
    Wd, H = r.randint(5, 10), r.randint(4, 9)
    a, h1 = r.randint(2, Wd - 2), r.randint(2, H - 2)
    pts = [[0, 0], [Wd, 0], [Wd, h1], [a, h1], [a, H], [0, H]]
    return Wd, H, a, h1, pts


@fam("01")
def rl_grid(r, L):
    cells, H, Wd = lshape_cells(r, L)
    cells = [[i + 1, j + 1] for i, j in cells]
    n = len(cells)
    return Item("Find the area of the figure. Split it into rectangles if that helps.", f"{n} square units",
                ["Split the figure into two rectangles and count or multiply each.", f"The area is {n} square units."],
                [W(f"{perim_cells(cells)} square units", "found the perimeter"), W(f"{H * Wd} square units", "used the whole rectangle around the figure"), W(f"{n - 2} square units", "missed some squares")],
                FN("cells", cells=cells, unit="square units"), qtype="visual", diagram=grid_d(cells, H + 2, Wd + 2))


@fam("012")
def rl_labels(r, L):
    Wd, H, a, h1, pts = lpoly(r, L)
    area = Wd * h1 + a * (H - h1)
    labels = [[0, f"{Wd} m"], [1, f"{h1} m"], [2, f"{Wd - a} m"], [3, f"{H - h1} m"], [4, f"{a} m"], [5, f"{H} m"]] if L == 0 else \
        [[0, f"{Wd} m"], [1, f"{h1} m"], [4, f"{a} m"], [5, f"{H} m"]]
    alt = f"An L-shaped figure with right angles. Sides: bottom {Wd} m, right {h1} m, " + ("inside step " + f"{Wd - a} m and {H - h1} m, " if L == 0 else "") + f"top {a} m, left {H} m."
    return Item("Find the area of the figure. All corners are right angles.", f"{area} square meters",
                [f"Split it: a bottom rectangle {Wd} × {h1} = {Wd * h1} and a top rectangle {a} × {H - h1} = {a * (H - h1)}.", f"{Wd * h1} + {a * (H - h1)} = {area} square meters."],
                [W(f"{Wd * H} square meters", "multiplied the longest sides as if it were a rectangle"), W(f"{2 * (Wd + H)} square meters", "found the perimeter"), W(f"{Wd * h1 + a * H} square meters", "counted the overlap twice")],
                FN("poly_area", pts=pts, unit="square meters"), qtype="visual",
                diagram=Diagram("shape", {"pts": pts, "side_labels": labels, "right": [0, 1, 2, 4, 5], "fill": "orange"}, alt))


@fam("012", mode="mc")
def rl_expr(r, L):
    Wd, H, a, h1, pts = lpoly(r, L)
    good = f"({Wd} × {h1}) + ({a} × {H - h1})"
    bad = [f"{Wd} × {H}", f"({Wd} × {h1}) + ({a} × {H})", f"({Wd} + {h1}) + ({a} + {H - h1})"]
    alt = f"An L-shaped figure with right angles. Bottom {Wd}, right {h1}, inner step {Wd - a} and {H - h1}, top {a}, left {H}."
    it = mc_key("Which expression gives the area of the figure? All corners are right angles.", good, bad,
                [f"Bottom rectangle: {Wd} × {h1}. Top rectangle: {a} × {H - h1}.", "Add the two areas."], qtype="visual", tags={"multiple-representations"},
                diagram=Diagram("shape", {"pts": pts, "side_labels": [[0, str(Wd)], [1, str(h1)], [2, str(Wd - a)], [3, str(H - h1)], [4, str(a)], [5, str(H)]], "right": [0, 1, 2, 4, 5], "fill": "teal"}, alt), r=r)
    it.check = FN("expr_poly_area", pts=pts)
    return it


@fam("012")
def rl_word(r, L):
    Wd, H, a, h1, pts = lpoly(r, L)
    area = Wd * h1 + a * (H - h1)
    return Item(f"A room is made of a rectangle {Wd} feet by {h1} feet and a rectangle {a} feet by {H - h1} feet that do not overlap. What is the area of the room?",
                f"{area} square feet", [f"{Wd} × {h1} = {Wd * h1} and {a} × {H - h1} = {a * (H - h1)}.", f"{Wd * h1} + {a * (H - h1)} = {area} square feet."],
                [W(f"{Wd * h1} square feet", "found only one rectangle"), W(f"{Wd + h1 + a + H - h1} square feet", "added the side lengths"), W(f"{Wd * h1 * a * (H - h1)} square feet" if Wd * h1 * a * (H - h1) < 2000 else f"{area + 10} square feet", "multiplied the two areas")],
                EX(f"{Wd}*{h1}+{a}*{H - h1}", unit="square feet"), qtype="word-problem", tags={"modeling"})


@fam("2")
def rl_missing(r, L):
    Wd, H, a, h1, pts = lpoly(r, L)
    area = Wd * h1 + a * (H - h1)
    alt = f"An L-shaped figure with right angles. Only four sides are labeled: bottom {Wd} m, right {h1} m, top {a} m, left {H} m."
    return Item(f"Two side lengths are not labeled. Find the area of the figure. All corners are right angles.", f"{area} square meters",
                [f"The missing step heights: {H} − {h1} = {H - h1}. Split into {Wd} × {h1} and {a} × {H - h1}.", f"{Wd * h1} + {a * (H - h1)} = {area} square meters."],
                [W(f"{Wd * H} square meters", "treated the figure as a rectangle"), W(f"{Wd * h1 + a * H} square meters", "used the full height for the top part"), W(f"{2 * (Wd + H)} square meters", "found the perimeter")],
                FN("poly_area", pts=pts, unit="square meters"), qtype="multi-step", tags={"multistep", "reasoning"},
                diagram=Diagram("shape", {"pts": pts, "side_labels": [[0, f"{Wd} m"], [1, f"{h1} m"], [4, f"{a} m"], [5, f"{H} m"]], "right": [0, 1, 2, 4, 5], "fill": "pink"}, alt))


@fam("2")
def rl_cut_out(r, L):
    Wd, H = r.randint(6, 10), r.randint(5, 8)
    cw, ch = r.randint(2, Wd - 3), r.randint(2, H - 3)
    return Item(f"A rectangle {Wd} feet by {H} feet has a {cw} foot by {ch} foot rectangle cut out of one corner. What is the area of the shape that is left?",
                f"{Wd * H - cw * ch} square feet", [f"Whole rectangle: {Wd} × {H} = {Wd * H}. Cut-out: {cw} × {ch} = {cw * ch}.", f"{Wd * H} − {cw * ch} = {Wd * H - cw * ch} square feet."],
                [W(f"{Wd * H} square feet", "forgot to subtract the cut-out"), W(f"{Wd * H + cw * ch} square feet", "added the cut-out"), W(f"{(Wd - cw) * (H - ch)} square feet", "subtracted the side lengths first")],
                EX(f"{Wd}*{H}-{cw}*{ch}", unit="square feet"), qtype="multi-step", tags={"multistep", "reasoning"})


SKILLS = {
    1: dict(name="Understanding Area and Unit Squares", fams=[au_count, au_gaps, au_unit_square, au_n, au_more, au_compare]),
    2: dict(name="Measuring Area by Counting Unit Squares", fams=[ac_units, ac_mc_units, ac_choose, ac_unit_name, ac_compare_units, ac_error]),
    3: dict(name="Area of Rectangles: Tile and Multiply", fams=[ar_tiled, ar_mult, ar_word, ar_equation, ar_side, ar_partial]),
    4: dict(name="Area and the Distributive Property", fams=[ad_total, ad_expr, ad_fill, ad_part, ad_choose, ad_word]),
    5: dict(name="Area of Rectilinear Figures", fams=[rl_grid, rl_labels, rl_expr, rl_word, rl_missing, rl_cut_out]),
}
