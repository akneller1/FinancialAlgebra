"""Unit 8: Volume and Three-Dimensional Figures (volume)."""
from g5lib import *

UNIT_ID = "volume-three-dimensional-figures"
UNITS = [("cm", "cubic centimeters", "centimeters"), ("in", "cubic inches", "inches"), ("ft", "cubic feet", "feet"), ("m", "cubic meters", "meters")]


def dims(r, L):
    if L == 0:
        return r.randint(2, 5), r.randint(2, 4), r.randint(1, 3)
    if L == 1:
        return r.randint(3, 9), r.randint(2, 7), r.randint(2, 6)
    return r.randint(5, 15), r.randint(3, 12), r.randint(2, 10)


def vol_wrongs(l, w, h, unit):
    return [W(f"{comma(l + w + h)} {unit}", "added the edge lengths"), W(f"{comma(l * w)} {unit}", "found the area of the base only"),
            W(f"{comma(2 * (l * w + l * h + w * h))} {unit}", "found the surface area (covered the outside)"), W(f"{comma(l * w * h + l * w)} {unit}", "counted one layer twice")]


# ============================================================== S1 Understanding Volume and Unit Cubes
@fam("012")
def uv_count(r, L):
    l, w, h = r.randint(2, 4), r.randint(1, 3), r.randint(1, 3) if L == 0 else r.randint(2, 3)
    alt = f"A rectangular prism built from unit cubes: {l} cubes long, {w} cubes deep, {h} cubes tall."
    return Item("The solid is built from unit cubes with no gaps or overlaps. What is its volume in cubic units?", f"{l * w * h} cubic units",
                [f"Each layer has {l} × {w} = {l * w} cubes, and there are {h} layer{'s' if h > 1 else ''}.", f"{l * w} × {h} = {l * w * h} cubic units."],
                [W(f"{l * w} cubic units", "counted only one layer"), W(f"{l + w + h} cubic units", "added the edge lengths"), W(f"{l * h + l * w if w > 1 else l * h + h} cubic units", "counted only the cubes you can see on the front and top")],
                FN("volume_cubes", blocks=[{"l": l, "w": w, "h": h}], unit="cubic units"), qtype="visual",
                diagram=Diagram("cubes", {"blocks": [{"l": l, "w": w, "h": h}]}, alt))


@fam("012")
def uv_layers(r, L):
    per = r.randint(4, 20) if L < 2 else r.randint(12, 60)
    n = r.randint(2, 6) if L < 2 else r.randint(3, 12)
    return Item(f"A box is packed with unit cubes. Each layer has {per} cubes, and there are {n} layers. What is the volume of the box?", f"{per * n} cubic units",
                [f"Volume = cubes per layer × number of layers.", f"{per} × {n} = {per * n} cubic units."],
                [W(f"{per + n} cubic units", "added instead of multiplying"), W(f"{per} cubic units", "counted one layer"), W(f"{per * (n - 1)} cubic units", "left out a layer")],
                EX(f"{per}*{n}", unit="cubic units"), qtype="conceptual")


@fam("012", mode="mc")
def uv_unit(r, L):
    which = r.randrange(4)
    if which == 0:
        return mc_key("What is a unit cube?", "A cube with edges 1 unit long; its volume is 1 cubic unit.", ["A square with sides 1 unit long.", "Any cube, no matter its size.", "A cube with a volume of 10 cubic units."],
                      ["A unit cube has edge length 1 unit.", "Its volume is 1 cubic unit, so it can measure volume."], r=r, qtype="conceptual")
    if which == 1:
        good = pick(r, ["cubic centimeters", "cubic inches", "cubic feet"])
        flat = good.replace("cubic", "square")
        return mc_key("Which unit could be used to measure the volume of a box?", good, [flat, good.replace("cubic ", ""), "degrees"],
                      ["Volume measures the space inside a solid figure.", f"It is measured in cubic units, such as {good}."], r=r, qtype="conceptual")
    if which == 2:
        n = r.randint(12, 60)
        return mc_key(f"A box is filled with {n} unit cubes, with no gaps and no overlaps. What is its volume?", f"{n} cubic units", [f"{n} square units", f"{n} units", f"{n * 2} cubic units"],
                      ["Each unit cube is 1 cubic unit.", f"{n} cubes = {n} cubic units."], r=r, qtype="conceptual")
    return mc_key("Why must there be no gaps or overlaps when you fill a box with unit cubes to find its volume?",
                  "Gaps leave space uncounted and overlaps count space twice, so the count would be wrong.",
                  ["So the box looks neat.", "Because cubes must always be stacked in rows of 10.", "Gaps and overlaps do not change the count."],
                  ["Volume counts the space inside exactly once.", "Gaps miss space; overlaps double-count it."], r=r, qtype="explain", tags={"reasoning"})


@fam("012")
def uv_same_volume(r, L):
    v = pick(r, [12, 16, 18, 24, 30, 36])
    l, w = pick(r, [(a, b) for a in range(1, 7) for b in range(1, 7) if v % (a * b) == 0 and v // (a * b) <= 6 and a >= b])
    h = v // (l * w)
    return Item(f"A prism is built from {v} unit cubes. It is {l} cubes long and {w} cubes wide. How many cubes tall is it?", str(h),
                [f"One layer has {l} × {w} = {l * w} cubes.", f"{v} ÷ {l * w} = {h} layers tall."],
                [W(str(v - l - w), "subtracted the length and width"), W(str(v // l), "divided by only the length"), W(str(l * w), "gave the cubes in one layer")],
                EX(f"{v}/({l}*{w})"), qtype="conceptual", tags={"reasoning"})


@fam("012")
def uv_build(r, L):
    l, w, h = r.randint(2, 5), r.randint(2, 4), r.randint(2, 4)
    alt = f"A rectangular prism of unit cubes, {l} long, {w} deep and {h} tall, with its edge counts labeled."
    v = l * w * h
    return Item(f"Each cube in the model is 1 cubic {pick(r, ['centimeter', 'inch'])}. How many cubes make up the prism?", str(v),
                [f"Layers: {h}, each with {l} × {w} = {l * w} cubes.", f"{l * w} × {h} = {v} cubes."],
                [W(str(l * w), "counted one layer"), W(str(l + w + h), "added the labels"), W(str(2 * (l * w + l * h + w * h)), "counted the faces of the outside squares")],
                FN("volume_cubes", blocks=[{"l": l, "w": w, "h": h}]), qtype="visual",
                diagram=Diagram("cubes", {"blocks": [{"l": l, "w": w, "h": h}], "labels": True, "unit_word": "cubes"}, alt))


# ============================================================== S2 Counting Cubes to Find Volume
@fam("012")
def cc_prism(r, L):
    l, w, h = dims(r, 0 if L == 0 else 1)
    need(l <= 6 and w <= 5 and h <= 5)
    u = pick(r, UNITS[:3])
    alt = f"Prism made of 1-{u[2][:-1] if u[2] != 'feet' else 'foot'} cubes: {l} long, {w} deep, {h} tall."
    word = u[2][:-1] if u[2] != "feet" else "foot"
    return Item(f"Each cube is 1 cubic {word}. What is the volume of the prism?", f"{l * w * h} {u[1]}",
                [f"Count one layer: {l} × {w} = {l * w} cubes. There are {h} layers.", f"{l * w} × {h} = {l * w * h} {u[1]}."],
                vol_wrongs(l, w, h, u[1])[:2] + [W(f"{l * w * h} square {u[2]}", "used square units for volume")],
                FN("volume_cubes", blocks=[{"l": l, "w": w, "h": h}], unit=u[1]), qtype="visual",
                diagram=Diagram("cubes", {"blocks": [{"l": l, "w": w, "h": h}], "labels": L == 0, "unit_word": "cubes"}, alt))


@fam("012")
def cc_two(r, L):
    a = (r.randint(2, 4), r.randint(1, 3), r.randint(1, 3))
    b = (r.randint(1, 3), a[1], r.randint(1, 4))
    need(a[2] != b[2])
    blocks = [{"l": a[0], "w": a[1], "h": a[2]}, {"l": b[0], "w": b[1], "h": b[2], "x": a[0], "color": "#ffc27a"}]
    v = a[0] * a[1] * a[2] + b[0] * b[1] * b[2]
    alt = f"A solid of unit cubes made of two rectangular blocks side by side: {a[0]}×{a[1]}×{a[2]} (blue) and {b[0]}×{b[1]}×{b[2]} (orange)."
    return Item("The solid is made of two blocks of unit cubes. What is its total volume in cubic units?", f"{v} cubic units",
                [f"Blue block: {a[0]} × {a[1]} × {a[2]} = {a[0] * a[1] * a[2]}. Orange block: {b[0]} × {b[1]} × {b[2]} = {b[0] * b[1] * b[2]}.", f"Total: {v} cubic units."],
                [W(f"{a[0] * a[1] * a[2]} cubic units", "counted only one block"), W(f"{(a[0] + b[0]) * a[1] * max(a[2], b[2])} cubic units", "treated the solid as one big box"), W(f"{v - a[1]} cubic units", "missed the hidden cubes")],
                FN("volume_cubes", blocks=blocks, unit="cubic units"), qtype="visual", diagram=Diagram("cubes", {"blocks": blocks}, alt))


@fam("012")
def cc_fill(r, L):
    l, w, h = dims(r, L)
    have = r.randint(1, l * w * h - 1)
    v = l * w * h
    return Item(f"A box holds {l} × {w} × {h} unit cubes when full. {have} cubes are already inside. How many more cubes are needed to fill it?", str(v - have),
                [f"Full box: {l} × {w} × {h} = {v} cubes.", f"{v} − {have} = {v - have} more cubes."],
                [W(str(v), "found the full volume only"), W(str(l + w + h), "added the dimensions"), W(str(v + have), "added instead of subtracting")],
                EX(f"{l}*{w}*{h}-{have}"), qtype="word-problem", tags={"multistep"})


@fam("012", mode="sa")
def cc_compare(r, L):
    a, b = dims(r, min(L, 1)), dims(r, min(L, 1))
    va, vb = a[0] * a[1] * a[2], b[0] * b[1] * b[2]
    need(va != vb)
    ans = "Box A" if va > vb else "Box B"
    return Item(f"Box A holds {a[0]} × {a[1]} × {a[2]} unit cubes. Box B holds {b[0]} × {b[1]} × {b[2]} unit cubes. Which box has the greater volume?", ans,
                [f"Box A: {va} cubic units. Box B: {vb} cubic units.", f"{ans} has the greater volume."],
                [W("Box B" if ans == "Box A" else "Box A", "compared only one dimension")],
                FN("extreme", values={"Box A": f"{a[0]}*{a[1]}*{a[2]}", "Box B": f"{b[0]}*{b[1]}*{b[2]}"}, which="max", expr=True), qtype="conceptual", mode="sa")


@fam("012")
def cc_sugar(r, L):
    l, w, h = dims(r, L)
    item = pick(r, ["sugar cubes", "number cubes", "building blocks"])
    return Item(f"{name(r)} fills a box completely with {item}: {l} along the length, {w} along the width, and {h} high. How many {item} fit in the box?", f"{l * w * h} {item}",
                [f"Multiply the counts along each edge.", f"{l} × {w} × {h} = {l * w * h} {item}."],
                [W(f"{l * w} {item}", "counted one layer"), W(f"{l + w + h} {item}", "added the edge counts"), W(f"{l * w * h * 2} {item}", "counted each cube twice")],
                EX(f"{l}*{w}*{h}", unit=item), qtype="real-world")


# ============================================================== S3 Volume Formulas
@fam("012")
def vf_lwh(r, L):
    l, w, h = dims(r, L)
    u = pick(r, UNITS)
    alt = f"Rectangular prism labeled length {l} {u[0]}, width {w} {u[0]}, height {h} {u[0]}."
    v = l * w * h
    return Item("Find the volume of the rectangular prism.", f"{comma(v)} {u[1]}", ["V = l × w × h.", f"V = {l} × {w} × {h} = {comma(v)} {u[1]}."],
                vol_wrongs(l, w, h, u[1]), EX(f"{l}*{w}*{h}", unit=u[1]), qtype="visual",
                diagram=Diagram("prism", {"l": l, "w": w, "h": h, "lt": f"{l} {u[0]}", "wt": f"{w} {u[0]}", "ht": f"{h} {u[0]}"}, alt))


@fam("012")
def vf_Bh(r, L):
    B = r.randint(6, 40) if L < 2 else r.randint(20, 150)
    h = r.randint(2, 9) if L < 2 else r.randint(5, 20)
    u = pick(r, UNITS)
    return Item(f"The base of a rectangular prism has an area of {B} square {u[2]}. The height is {h} {u[2]}. What is the volume?", f"{comma(B * h)} {u[1]}",
                ["V = B × h, where B is the area of the base.", f"V = {B} × {h} = {comma(B * h)} {u[1]}."],
                [W(f"{B + h} {u[1]}", "added the base area and height"), W(f"{B} {u[1]}", "used only the base area"), W(f"{comma(B * h * 2)} {u[1]}", "multiplied by 2")],
                EX(f"{B}*{h}", unit=u[1]), qtype="procedural", claim=f"V with B = {B}, h = {h}")


@fam("012")
def vf_missing(r, L):
    l, w, h = dims(r, L)
    u = pick(r, UNITS)
    v = l * w * h
    return Item(f"A rectangular prism has a volume of {comma(v)} {u[1]}. Its length is {l} {u[2]} and its width is {w} {u[2]}. What is its height?", f"{h} {u[2]}",
                [f"V = l × w × h, so h = V ÷ (l × w).", f"h = {comma(v)} ÷ ({l} × {w}) = {comma(v)} ÷ {l * w} = {h} {u[2]}."],
                [W(f"{comma(v - l - w)} {u[2]}", "subtracted the length and width"), W(f"{comma(v // l) if v % l == 0 else comma(v - l * w)} {u[2]}", "divided by only one dimension"), W(f"{comma(v * l * w)} {u[2]}", "multiplied instead of dividing")],
                EX(f"{v}/({l}*{w})", unit=u[2]), qtype="procedural", tags={"reasoning"})


@fam("012", mode="mc")
def vf_which(r, L):
    l, w, h = dims(r, min(L, 1))
    v = l * w * h
    good = f"{l} × {w} × {h}"
    cands = [(l + 1, w, h), (l, w + 1, h - 1 if h > 1 else h + 2), (l * 2, w, h + 1), (l, w, h + 2), (l + 2, w - 1 if w > 1 else w + 1, h)]
    bad = []
    for a, b, c in cands:
        if a * b * c != v and f"{a} × {b} × {c}" not in bad:
            bad.append(f"{a} × {b} × {c}")
    bad = bad[:3]
    need(len(bad) == 3)
    opts = [(good, True)] + [(x, False) for x in bad]
    r.shuffle(opts)
    return Item(f"Which prism dimensions (length × width × height, in units) give a volume of {v} cubic units?", good,
                [f"Multiply each set of dimensions.", f"{good} = {v}."], check=FN("prisms_with", v=v), options=opts, mode="mc", qtype="conceptual")


@fam("012", mode="mc")
def vf_assoc(r, L):
    a, b, c = r.randint(2, 9), r.randint(2, 9), r.randint(2, 9)
    good = f"({a} × {b}) × {c} = {a} × ({b} × {c}), because the volume is the same no matter which face you use as the base."
    bad = [f"({a} × {b}) × {c} is greater than {a} × ({b} × {c}).", f"({a} × {b}) × {c} = ({a} + {b}) × {c}.", f"You must always multiply length × width first, so only ({a} × {b}) × {c} works."]
    return mc_key(f"A prism is {a} units by {b} units by {c} units. Which statement is true?", good, bad, ["Multiplication can be grouped in any way (associative property).", good], r=r, qtype="explain", tags={"reasoning"})


@fam("012")
def vf_cube(r, L):
    s = r.randint(2, 6) if L < 2 else r.randint(5, 12)
    u = pick(r, UNITS)
    return Item(f"A cube has edges that are {s} {u[2]} long. What is its volume?", f"{comma(s ** 3)} {u[1]}",
                ["Every edge of a cube is the same length.", f"V = {s} × {s} × {s} = {comma(s ** 3)} {u[1]}."],
                [W(f"{s * 3} {u[1]}", "multiplied by 3 instead of cubing"), W(f"{s * s} {u[1]}", "found the area of one face"), W(f"{6 * s * s} {u[1]}", "found the surface area")],
                EX(f"{s}*{s}*{s}", unit=u[1]), qtype="procedural")


# ============================================================== S4 Volume of Composite Figures
def comp_parts(r, L):
    w = r.randint(2, 6)
    la, ha = r.randint(2, 6), r.randint(4, 9)
    lb, hb = r.randint(2, 7), r.randint(1, 3)
    need(ha > hb)
    return w, (la, ha), (lb, hb)


@fam("012")
def comp_sum(r, L):
    w, (la, ha), (lb, hb) = comp_parts(r, L)
    u = pick(r, UNITS)
    va, vb = la * w * ha, lb * w * hb
    alt = f"An L-shaped solid made of two rectangular prisms with the same depth {w} {u[0]}: a tall prism {la} {u[0]} long and {ha} {u[0]} high, and a short prism {lb} {u[0]} long and {hb} {u[0]} high."
    return Item("The solid is made of two rectangular prisms. What is its total volume?", f"{va + vb} {u[1]}",
                [f"Tall prism: {la} × {w} × {ha} = {va}. Short prism: {lb} × {w} × {hb} = {vb}.", f"Total: {va} + {vb} = {va + vb} {u[1]}."],
                [W(f"{(la + lb) * w * ha} {u[1]}", "treated the solid as one big box"), W(f"{va} {u[1]}", "found only one part"), W(f"{la * w * ha * lb * w * hb} {u[1]}", "multiplied the two volumes")],
                FN("volume_comp", parts=[{"l": la, "w": w, "h": ha}, {"l": lb, "w": w, "h": hb}], unit=u[1]), qtype="visual",
                diagram=Diagram("composite", {"a": {"l": la, "w": w, "h": ha, "lt": f"{la} {u[0]}", "wt": f"{w} {u[0]}", "ht": f"{ha} {u[0]}"},
                                              "b": {"l": lb, "w": w, "h": hb, "lt": f"{lb} {u[0]}", "ht": f"{hb} {u[0]}"}}, alt))


@fam("012")
def comp_words(r, L):
    a, b = dims(r, L), dims(r, L)
    u = pick(r, UNITS[:3])
    va, vb = a[0] * a[1] * a[2], b[0] * b[1] * b[2]
    return Item(f"A shelf unit is made of two boxes. One box is {a[0]} by {a[1]} by {a[2]} {u[2]}. The other is {b[0]} by {b[1]} by {b[2]} {u[2]}. What is the total volume?", f"{comma(va + vb)} {u[1]}",
                [f"First box: {va} {u[1]}. Second box: {vb} {u[1]}.", f"Total: {comma(va + vb)} {u[1]}."],
                [W(f"{comma(va)} {u[1]}", "found only one box"), W(f"{comma(sum(a) + sum(b))} {u[1]}", "added all the edge lengths"), W(f"{comma(va * vb)} {u[1]}", "multiplied the volumes")],
                FN("volume_comp", parts=[{"l": a[0], "w": a[1], "h": a[2]}, {"l": b[0], "w": b[1], "h": b[2]}], unit=u[1]), qtype="word-problem", tags={"multistep"})


@fam("012")
def comp_part(r, L):
    w, (la, ha), (lb, hb) = comp_parts(r, L)
    u = pick(r, UNITS)
    va, vb = la * w * ha, lb * w * hb
    return Item(f"A solid made of two rectangular prisms has a total volume of {va + vb} {u[1]}. One prism is {la} × {w} × {ha} {u[2]}. What is the volume of the other prism?", f"{vb} {u[1]}",
                [f"Known prism: {la} × {w} × {ha} = {va} {u[1]}.", f"Other prism: {va + vb} − {va} = {vb} {u[1]}."],
                [W(f"{va} {u[1]}", "gave the known prism's volume"), W(f"{va + vb + va} {u[1]}", "added instead of subtracting"), W(f"{va + vb - la - w - ha} {u[1]}", "subtracted the edge lengths")],
                EX(f"{va + vb}-{la}*{w}*{ha}", unit=u[1]), qtype="multi-step", tags={"reasoning"})


@fam("012", mode="mc")
def comp_expr(r, L):
    w, (la, ha), (lb, hb) = comp_parts(r, L)
    good = f"({la} × {w} × {ha}) + ({lb} × {w} × {hb})"
    bad = [f"({la} + {lb}) × {w} × {ha}", f"({la} × {w} × {ha}) × ({lb} × {w} × {hb})", f"{la} × {w} × {ha} + {lb}"]
    vals = [la * w * ha + lb * w * hb, (la + lb) * w * ha, la * w * ha * lb * w * hb, la * w * ha + lb]
    need(len(set(vals)) == 4)
    opts = [(good, True)] + [(x, False) for x in bad]
    r.shuffle(opts)
    return Item(f"A solid is made of a {la} × {w} × {ha} prism and a {lb} × {w} × {hb} prism that do not overlap. Which expression gives its volume?", good,
                ["Volume is additive: find the volume of each prism and add.", good], check=FN("same_value", target=f"{la}*{w}*{ha}+{lb}*{w}*{hb}"), options=opts, mode="mc", qtype="conceptual")


@fam("12")
def comp_infer(r, L):
    w, (la, ha), (lb, hb) = comp_parts(r, L)
    u = pick(r, UNITS)
    tot_l = la + lb
    va, vb = la * w * ha, lb * w * hb
    alt = f"L-shaped solid of two prisms with depth {w} {u[0]}. The whole bottom is {tot_l} {u[0]} long; the tall part is {la} {u[0]} long and {ha} {u[0]} high; the short part is {hb} {u[0]} high."
    return Item(f"The whole solid is {tot_l} {u[2]} long. The tall part is {la} {u[2]} long. Find the total volume.", f"{va + vb} {u[1]}",
                [f"The short part is {tot_l} − {la} = {lb} {u[2]} long.", f"Volume: {la} × {w} × {ha} + {lb} × {w} × {hb} = {va} + {vb} = {va + vb} {u[1]}."],
                [W(f"{la * w * ha + tot_l * w * hb} {u[1]}", "used the whole length for the short part"), W(f"{tot_l * w * ha} {u[1]}", "treated it as one big box"), W(f"{va} {u[1]}", "found only the tall part")],
                FN("volume_comp", parts=[{"l": la, "w": w, "h": ha}, {"l": f"{tot_l}-{la}", "w": w, "h": hb}], unit=u[1]), qtype="visual", tags={"multistep", "challenge"},
                diagram=Diagram("composite", {"a": {"l": la, "w": w, "h": ha, "lt": f"{la} {u[0]}", "wt": f"{w} {u[0]}", "ht": f"{ha} {u[0]}"},
                                              "b": {"l": lb, "w": w, "h": hb, "lt": "?", "ht": f"{hb} {u[0]}"}, "total": f"{tot_l} {u[0]}"}, alt))


# ============================================================== S5 Volume Word Problems
@fam("012")
def vw_box(r, L):
    l, w, h = dims(r, L)
    t = pick(r, [("A toy box is {l} feet long, {w} feet wide, and {h} feet tall. How much space is inside?", "cubic feet"),
                 ("A fish tank is {l} inches long, {w} inches wide, and {h} inches deep. What is its volume?", "cubic inches"),
                 ("A garden bed is {l} meters long, {w} meters wide, and {h} meters deep. How much soil fills it?", "cubic meters")])
    v = l * w * h
    return Item(t[0].format(l=l, w=w, h=h), f"{comma(v)} {t[1]}", ["Use V = l × w × h.", f"{l} × {w} × {h} = {comma(v)} {t[1]}."],
                vol_wrongs(l, w, h, t[1]), EX(f"{l}*{w}*{h}", unit=t[1]), qtype="real-world", tags={"modeling"})


@fam("012")
def vw_depth(r, L):
    l, w, h = dims(r, L)
    v = l * w * h
    return Item(f"A sandbox holds {comma(v)} cubic feet of sand. It is {l} feet long and {w} feet wide. How deep is the sand?", f"{h} feet",
                [f"Base area: {l} × {w} = {l * w} square feet.", f"Depth: {comma(v)} ÷ {l * w} = {h} feet."],
                [W(f"{comma(v - l * w)} feet", "subtracted the base area"), W(f"{comma(v * l * w)} feet", "multiplied instead of dividing"), W(f"{comma(v // l) if v % l == 0 else comma(v // w)} feet", "divided by only one side")],
                EX(f"{v}/({l}*{w})", unit="feet"), qtype="real-world", tags={"reasoning"})


@fam("012")
def vw_compare(r, L):
    a, b = dims(r, L), dims(r, L)
    va, vb = a[0] * a[1] * a[2], b[0] * b[1] * b[2]
    need(va != vb)
    big, small = max(va, vb), min(va, vb)
    return Item(f"Container A is {a[0]} × {a[1]} × {a[2]} inches. Container B is {b[0]} × {b[1]} × {b[2]} inches. How many more cubic inches does the larger container hold?", f"{comma(big - small)} cubic inches",
                [f"A: {va} cubic inches. B: {vb} cubic inches.", f"{big} − {small} = {comma(big - small)} cubic inches."],
                [W(f"{comma(big)} cubic inches", "gave the larger volume"), W(f"{comma(va + vb)} cubic inches", "added the volumes"), W(f"{abs(sum(a) - sum(b))} cubic inches", "compared the sums of the edges")],
                EX(f"{a[0]}*{a[1]}*{a[2]}-{b[0]}*{b[1]}*{b[2]}" if va > vb else f"{b[0]}*{b[1]}*{b[2]}-{a[0]}*{a[1]}*{a[2]}", unit="cubic inches"), qtype="multi-step", tags={"multistep"})


@fam("012")
def vw_double(r, L):
    l, w, h = dims(r, L)
    k = pick(r, [2, 3]) if L < 2 else pick(r, [2, 3, 4])
    which = pick(r, ["height", "length", "width"])
    v = l * w * h
    return Item(f"A box is {l} × {w} × {h} centimeters. If the {which} is multiplied by {k} and the other edges stay the same, what is the new volume?", f"{comma(v * k)} cubic centimeters",
                [f"Old volume: {comma(v)} cubic centimeters.", f"Multiplying one edge by {k} multiplies the volume by {k}: {comma(v * k)} cubic centimeters."],
                [W(f"{comma(v + k)} cubic centimeters", "added the factor"), W(f"{comma(v * k ** 3)} cubic centimeters", "multiplied every edge"), W(f"{comma(v)} cubic centimeters", "kept the volume the same")],
                EX(f"{l}*{w}*{h}*{k}", unit="cubic centimeters"), qtype="explain", tags={"reasoning"})


@fam("012")
def vw_fit(r, L):
    a, b, c = r.randint(2, 5), r.randint(2, 4), r.randint(1, 3)
    s = pick(r, [2, 3]) if L else 1
    box = (a * s, b * s, c * s)
    n = a * b * c
    word = "1-inch" if s == 1 else f"{s}-inch"
    return Item(f"How many {word} cubes fit exactly inside a box that is {box[0]} × {box[1]} × {box[2]} inches?", str(n),
                [f"Along each edge: {box[0]} ÷ {s} = {a}, {box[1]} ÷ {s} = {b}, {box[2]} ÷ {s} = {c}.", f"{a} × {b} × {c} = {n} cubes."],
                [W(str(box[0] * box[1] * box[2]), "found the volume in cubic inches instead of counting the bigger cubes") if s > 1 else W(str(a * b), "counted one layer"), W(str(box[0] * box[1] * box[2] // s), "divided the volume by the edge length instead of the cube's volume") if s > 1 else W(str(a + b + c), "added"),
                 W(str(a * b * c * s), "multiplied by the cube size")],
                FN("cube_fit", box=list(box), s=s), qtype="real-world", tags={"reasoning"})


SKILLS = {
    1: dict(name="Understanding Volume and Unit Cubes", fams=[uv_count, uv_layers, uv_unit, uv_same_volume, uv_build]),
    2: dict(name="Counting Cubes to Find Volume", fams=[cc_prism, cc_two, cc_fill, cc_compare, cc_sugar]),
    3: dict(name="Volume Formulas", fams=[vf_lwh, vf_Bh, vf_missing, vf_which, vf_assoc, vf_cube]),
    4: dict(name="Volume of Composite Figures", fams=[comp_sum, comp_words, comp_part, comp_expr, comp_infer]),
    5: dict(name="Volume Word Problems", fams=[vw_box, vw_depth, vw_compare, vw_double, vw_fit]),
}
