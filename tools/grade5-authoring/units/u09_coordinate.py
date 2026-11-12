"""Unit 9: Coordinate Planes and Graphing (coordinate-plane)."""
from g5lib import *

UNIT_ID = "coordinate-plane-graphing"


def pt(x, y):
    return f"({x}, {y})"


def points(r, n, xm=10, ym=10):
    out = set()
    while len(out) < n:
        out.add((r.randint(1, xm), r.randint(1, ym)))
    return list(out)


# ============================================================== S1 The Coordinate System
@fam("012", mode="mc")
def cs_vocab(r, L):
    items = [("What is the point where the x-axis and the y-axis meet called?", "the origin", ["the x-coordinate", "the y-axis", "the ordered pair"]),
             ("In the ordered pair (4, 7), what does the 4 tell you?", "how far to move along the x-axis (right) from the origin", ["how far to move up from the origin", "the number of points on the graph", "where the point crosses the y-axis"]),
             ("In the ordered pair (4, 7), what does the 7 tell you?", "how far to move along the y-axis (up) from the origin", ["how far to move right from the origin", "the distance between two points", "the x-coordinate"]),
             ("What are the coordinates of the origin?", "(0, 0)", ["(1, 1)", "(0, 1)", "(1, 0)"]),
             ("Which line is the horizontal number line on a coordinate plane?", "the x-axis", ["the y-axis", "the origin", "the ordered pair"]),
             ("Why are the x-axis and y-axis drawn perpendicular?", "So every point can be located by moving one direction along each axis, at right angles.", ["So the graph looks like a square.", "Because the axes are always the same length.", "So the origin is in the top corner."])]
    q, good, bad = pick(r, items if L else items[:5])
    return mc_key(q, good, bad, ["The axes are two perpendicular number lines that meet at the origin (0, 0).", good], r=r, qtype="conceptual")


@fam("012")
def cs_moves(r, L):
    x, y = r.randint(0, 10), r.randint(0, 10)
    need(x != y)
    return Item(f"Start at the origin. Move {x} unit{'s' if x != 1 else ''} to the right and {y} unit{'s' if y != 1 else ''} up. What ordered pair names the point?", pt(x, y),
                ["The first coordinate tells how far right; the second tells how far up.", f"The point is {pt(x, y)}."],
                [W(pt(y, x), "switched the order of the coordinates"), W(pt(x + y, 0), "added the moves"), W(pt(x, x), "used the same number twice")],
                FN("pair", x=str(x), y=str(y)), qtype="procedural")


@fam("012")
def cs_axis(r, L):
    k = r.randint(1, 10)
    on_x = r.random() < 0.5
    p = pt(k, 0) if on_x else pt(0, k)
    ans = "the x-axis" if on_x else "the y-axis"
    return Item(f"On which axis does the point {p} lie?", ans,
                [f"A point with y-coordinate 0 is on the x-axis; with x-coordinate 0 it is on the y-axis.", f"{p} is on {ans}."],
                [W("the y-axis" if on_x else "the x-axis", "mixed up which coordinate is 0")], FN("axis_of", p=p), qtype="conceptual", mode="sa")


@fam("012", mode="mc")
def cs_directions(r, L):
    x, y = r.randint(1, 10), r.randint(1, 10)
    need(x != y)
    good = f"Right {x}, then up {y}"
    bad = [f"Right {y}, then up {x}", f"Up {x}, then right {x}", f"Left {x}, then down {y}"]
    return mc_key(f"How do you plot the point {pt(x, y)} starting at the origin?", good, bad, ["The x-coordinate comes first: move right. The y-coordinate is second: move up.", good], r=r, qtype="conceptual")


@fam("012", mode="mc")
def cs_swap(r, L):
    x, y = r.sample(range(1, 11), 2)
    good = f"No. {pt(x, y)} is {x} right and {y} up, but {pt(y, x)} is {y} right and {x} up."
    bad = [f"Yes, because they use the same numbers.", f"Yes, because order does not matter in an ordered pair.", f"No, because {pt(y, x)} is not on the grid."]
    return mc_key(f"Do {pt(x, y)} and {pt(y, x)} name the same point?", good, bad, ["The order of the coordinates matters.", good], r=r, qtype="explain", tags={"reasoning"})


@fam("012")
def cs_from_point(r, L):
    x, y = r.randint(1, 8), r.randint(1, 8)
    dx, dy = r.randint(1, 5), r.randint(1, 5)
    return Item(f"Point A is at {pt(x, y)}. Point B is {dx} unit{'s' if dx > 1 else ''} to the right of A and {dy} unit{'s' if dy > 1 else ''} up from A. What are the coordinates of B?", pt(x + dx, y + dy),
                [f"Add {dx} to the x-coordinate and {dy} to the y-coordinate.", f"B = {pt(x + dx, y + dy)}."],
                [W(pt(x + dy, y + dx), "added the moves to the wrong coordinates"), W(pt(dx, dy), "started from the origin instead of point A"), W(pt(x - dx if x > dx else x + 2 * dx, y + dy), "moved left instead of right")],
                FN("pair", x=f"{x}+{dx}", y=f"{y}+{dy}"), qtype="procedural")


# ============================================================== S2 Plotting and Reading Points
def labeled(r, n, xm=10, ym=10):
    pts = points(r, n, xm, ym)
    labs = "ABCDEFG"[:n]
    return {labs[i]: list(p) for i, p in enumerate(pts)}


@fam("012")
def pr_read(r, L):
    P = labeled(r, 3 if L == 0 else 4)
    lab = pick(r, list(P))
    x, y = P[lab]
    need(x != y)
    alt = "Coordinate grid from 0 to 10 with points " + ", ".join(f"{k} at {pt(*v)}" for k, v in P.items()) + "."
    return Item(f"What are the coordinates of point {lab}?", pt(x, y), [f"From the origin, point {lab} is {x} right and {y} up.", f"{lab} = {pt(x, y)}."],
                [W(pt(y, x), "switched the x- and y-coordinates"), W(pt(x + 1, y), "counted one grid line too many"), W(pt(x, y - 1), "counted the boxes instead of the lines")],
                FN("pair", x=str(x), y=str(y)), qtype="visual",
                diagram=Diagram("coord", {"xmax": 10, "ymax": 10, "points": [{"x": v[0], "y": v[1], "label": k} for k, v in P.items()]}, alt))


@fam("012", mode="sa")
def pr_which(r, L):
    P = labeled(r, 4)
    lab = pick(r, list(P))
    x, y = P[lab]
    need(x != y and [y, x] not in P.values())
    alt = "Coordinate grid from 0 to 10 with points " + ", ".join(f"{k} at {pt(*v)}" for k, v in P.items()) + "."
    others = [k for k in P if k != lab]
    return Item(f"Which point is located at {pt(x, y)}?", f"point {lab}", [f"Move {x} right and {y} up from the origin.", f"Point {lab} is there."],
                [W(f"point {others[0]}", "moved up first, then right"), W(f"point {others[1]}", "misread the grid")], FN("point_at", points=P, x=str(x), y=str(y)), qtype="visual", mode="sa",
                diagram=Diagram("coord", {"xmax": 10, "ymax": 10, "points": [{"x": v[0], "y": v[1], "label": k} for k, v in P.items()]}, alt))


@fam("012")
def pr_distance(r, L):
    horiz = r.random() < 0.5
    a = r.randint(1, 9)
    b1, b2 = sorted(r.sample(range(0, 11), 2))
    A, B = ((b1, a), (b2, a)) if horiz else ((a, b1), (a, b2))
    return Item(f"Point A is at {pt(*A)} and point B is at {pt(*B)}. How many units apart are they?", f"{b2 - b1} units",
                [f"The {'y' if horiz else 'x'}-coordinates are the same, so subtract the other coordinates.", f"{b2} − {b1} = {b2 - b1} units."],
                [W(f"{b1 + b2} units", "added the coordinates"), W(f"{b2 - b1 + 1} units", "counted the grid lines instead of the spaces"), W(f"{a} units", "used the matching coordinate")],
                EX(f"{b2}-{b1}", unit="units"), qtype="procedural")


@fam("12")
def pr_vertex(r, L):
    x1, x2 = sorted(r.sample(range(1, 10), 2))
    y1, y2 = sorted(r.sample(range(1, 10), 2))
    corners = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
    miss = r.randrange(4)
    shown = [c for i, c in enumerate(corners) if i != miss]
    m = corners[miss]
    alt = "Coordinate grid with three corners of a rectangle at " + ", ".join(pt(*c) for c in shown) + "."
    return Item(f"Three corners of a rectangle are at {', '.join(pt(*c) for c in shown)}. What are the coordinates of the fourth corner?", pt(*m),
                ["Opposite sides of a rectangle are parallel to the axes here, so each x-value and each y-value is used twice.", f"The missing corner is {pt(*m)}."],
                [W(pt(m[1], m[0]), "switched the coordinates"), W(pt(x2 + (x2 - x1), y2), "extended a side too far"), W(pt(m[0], (y1 + y2) // 2 if (y1 + y2) // 2 not in (y1, y2) else m[1] + 1), "guessed the height")],
                FN("rect_corner", given=[list(c) for c in shown]), qtype="visual", tags={"reasoning"},
                diagram=Diagram("coord", {"xmax": 10, "ymax": 10, "points": [{"x": c[0], "y": c[1], "label": ""} for c in shown]}, alt))


@fam("012")
def pr_move(r, L):
    x, y = r.randint(2, 8), r.randint(2, 8)
    dx = r.randint(-x + 0, 10 - x) if L else r.randint(1, 10 - x)
    dy = r.randint(-y, 10 - y) if L else r.randint(1, 10 - y)
    need(dx and dy)
    h = f"{abs(dx)} unit{'s' if abs(dx) > 1 else ''} {'right' if dx > 0 else 'left'}"
    v = f"{abs(dy)} unit{'s' if abs(dy) > 1 else ''} {'up' if dy > 0 else 'down'}"
    return Item(f"A point at {pt(x, y)} moves {h} and {v}. What are its new coordinates?", pt(x + dx, y + dy),
                [f"Right/left changes the x-coordinate; up/down changes the y-coordinate.", f"New point: {pt(x + dx, y + dy)}."],
                [W(pt(x + dy, y + dx), "changed the wrong coordinates"), W(pt(x - dx, y - dy), "moved in the opposite directions"), W(pt(abs(dx), abs(dy)), "gave only the moves")],
                FN("pair", x=f"{x}+({dx})", y=f"{y}+({dy})"), qtype="procedural")


# ============================================================== S3 Real-World Problems on the Coordinate Plane
PLACES = ["Library", "Park", "School", "Pool", "Store", "Zoo", "Museum", "Farm"]


@fam("012")
def rw_map(r, L):
    names = r.sample(PLACES, 4)
    pts = points(r, 4)
    P = {n: list(p) for n, p in zip(names, pts)}
    who = pick(r, names)
    x, y = P[who]
    need(x != y)
    alt = "Town map on a coordinate grid (each unit is 1 block): " + ", ".join(f"{k} at {pt(*v)}" for k, v in P.items()) + "."
    return Item(f"The map shows a town on a coordinate grid. What are the coordinates of the {who}?", pt(x, y), [f"The {who} is {x} blocks east and {y} blocks north of the origin.", pt(x, y)],
                [W(pt(y, x), "switched the order of the coordinates"), W(pt(x, y + 1), "miscounted one block"), W(pt(x - 1, y), "started counting at 1 instead of 0")],
                FN("pair", x=str(x), y=str(y)), qtype="visual",
                diagram=Diagram("coord", {"xmax": 10, "ymax": 10, "points": [{"x": v[0], "y": v[1], "label": k} for k, v in P.items()], "xlab": "Blocks east", "ylab": "Blocks north"}, alt))


@fam("012")
def rw_graph(r, L):
    rate = r.randint(2, 9) if L < 2 else r.randint(5, 15)
    n = r.randint(4, 6)
    data = [[i, i * rate] for i in range(n + 1)]
    ask = r.randint(1, n)
    scale = 10 if rate * n > 50 else 5 if rate * n > 10 else 1
    ym = (rate * n + scale - 1) // scale
    need(ym <= 12)
    ctx = pick(r, [("Hours", "Miles", "miles", "a cyclist rides"), ("Weeks", "Dollars saved", "dollars", "Nia saves"), ("Minutes", "Pages read", "pages", "Eli reads")])
    pts_scaled = [{"x": p[0], "y": frac(F(p[1], scale)), "label": ""} for p in data]
    alt = f"Graph with x-axis {ctx[0]} (0 to {n}) and y-axis {ctx[1]} (counting by {scale}); points at " + ", ".join(pt(*p) for p in data) + "."
    it = Item(f"The graph shows how far {ctx[3]} over time. Each point is ({ctx[0].lower()}, {ctx[2]}). How many {ctx[2]} after {ask} {ctx[0].lower()[:-1] if ask == 1 else ctx[0].lower()}?",
              f"{ask * rate} {ctx[2]}", [f"Find {ask} on the x-axis and go up to the point.", f"The point is {pt(ask, ask * rate)}, so the answer is {ask * rate} {ctx[2]}."],
              [W(f"{(ask + 1) * rate} {ctx[2]}", "read the next point"), W(f"{ask} {ctx[2]}", "gave the x-coordinate"), W(f"{ask * scale} {ctx[2]}", "read the grid lines without the scale")],
              FN("graph_value", data=data, x=ask, unit=ctx[2]), qtype="visual",
              diagram=Diagram("coord", {"xmax": n, "ymax": ym, "points": pts_scaled, "path": [[p[0], frac(F(p[1], scale))] for p in data], "yscale": scale, "xlab": ctx[0], "ylab": ctx[1]}, alt))
    return it


@fam("012", mode="mc")
def rw_meaning(r, L):
    x, y = r.randint(2, 9), r.randint(10, 60)
    ctx = pick(r, [("hours worked", "dollars earned", f"After {x} hours of work, {y} dollars were earned.", f"After {y} hours of work, {x} dollars were earned."),
                   ("days", "centimeters a plant has grown", f"After {x} days, the plant has grown {y} centimeters.", f"After {y} days, the plant has grown {x} centimeters."),
                   ("games played", "points scored in all", f"After {x} games, {y} points have been scored in all.", f"After {y} games, {x} points have been scored in all.")])
    good = ctx[2]
    bad = [ctx[3], f"{x} and {y} are added to find the total.", f"There were {x + y} {ctx[0]} in all."]
    return mc_key(f"On a graph, x is the number of {ctx[0]} and y is the number of {ctx[1]}. What does the point ({x}, {y}) mean?", good, bad,
                  ["The x-coordinate goes with the x-axis label; the y-coordinate goes with the y-axis label.", good], r=r, qtype="conceptual", tags={"connections"})


@fam("012")
def rw_route(r, L):
    x1, y1 = r.randint(0, 5), r.randint(0, 5)
    x2 = x1 + r.randint(1, 5)
    y2 = y1 + r.randint(1, 5)
    nm = name(r)
    tot = (x2 - x1) + (y2 - y1)
    return Item(f"{nm} walks along the streets of a grid from {pt(x1, y1)} to {pt(x2, y1)}, then to {pt(x2, y2)}. Each unit is 1 block. How many blocks does {nm} walk?", f"{tot} blocks",
                [f"First part: {x2} − {x1} = {x2 - x1} blocks. Second part: {y2} − {y1} = {y2 - y1} blocks.", f"Total: {tot} blocks."],
                [W(f"{x2 + y2} blocks", "added the ending coordinates"), W(f"{x2 - x1} blocks", "counted only the first part"), W(f"{x1 + y1 + x2 + y2} blocks", "added all the coordinates")],
                EX(f"({x2}-{x1})+({y2}-{y1})", unit="blocks"), qtype="real-world", tags={"multistep"})


@fam("012", mode="sa")
def rw_compare(r, L):
    days = r.sample(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], 3)
    vals = r.sample(range(1, 10), 3)
    P = {d: [i + 1, v] for i, (d, v) in enumerate(zip(days, vals))}
    best = days[vals.index(max(vals))]
    alt = "Graph: x is the day number, y is centimeters of snow; points " + ", ".join(f"{d} at {pt(*P[d])}" for d in days) + "."
    return Item(f"The graph shows snowfall. Day 1 is {days[0]}, day 2 is {days[1]}, and day 3 is {days[2]}. Which day had the most snow?", best,
                ["The day with the highest point has the most snow.", f"The highest point is {pt(*P[best])}, so {best}."],
                [W(days[vals.index(min(vals))], "chose the lowest point"), W(days[2] if best != days[2] else days[0], "chose the point farthest to the right")],
                FN("extreme", values={d: str(P[d][1]) for d in days}, which="max"), qtype="visual", mode="sa",
                diagram=Diagram("coord", {"xmax": 4, "ymax": 10, "points": [{"x": P[d][0], "y": P[d][1], "label": d[:3]} for d in days], "xlab": "Day", "ylab": "Snow (cm)"}, alt))


# ============================================================== S4 Graphing Patterns and Relationships
@fam("012")
def gp_next(r, L):
    a = r.randint(1, 3)
    b = a * r.randint(2, 3)
    n = r.randint(3, 5)
    pts_ = [[a * i, b * i] for i in range(n)]
    xm, ym = a * n + 1, b * n + 1
    need(xm <= 15 and ym <= 15)
    alt = f"Points from two patterns graphed as ordered pairs: " + ", ".join(pt(*p) for p in pts_) + "."
    return Item(f"Pattern A starts at 0 and adds {a}. Pattern B starts at 0 and adds {b}. Their terms are graphed as ordered pairs (A, B). What is the next ordered pair?", pt(a * n, b * n),
                [f"Next A term: {a * (n - 1)} + {a} = {a * n}. Next B term: {b * (n - 1)} + {b} = {b * n}.", f"Next pair: {pt(a * n, b * n)}."],
                [W(pt(b * n, a * n), "switched the order"), W(pt(a * n, b * (n - 1) + a), "added A's rule to the B term"), W(pt(a * (n + 1), b * (n + 1)), "skipped a term")],
                FN("pattern_pair", a=a, b=b, n=n + 1), qtype="visual",
                diagram=Diagram("coord", {"xmax": xm, "ymax": ym, "points": [{"x": p[0], "y": p[1], "label": ""} for p in pts_], "step": 1 if ym <= 12 else 2}, alt))


@fam("012", mode="mc")
def gp_rule(r, L):
    m = r.randint(2, 5)
    pts_ = [(i, i * m) for i in range(4)]
    good = f"Each y-coordinate is {m} times the x-coordinate."
    bad = [f"Each y-coordinate is {m} more than the x-coordinate.", f"Each x-coordinate is {m} times the y-coordinate.", f"Each y-coordinate is {m + 1} times the x-coordinate."]
    alt = "Graph with points " + ", ".join(pt(*p) for p in pts_) + "."
    return mc_key("Which rule describes the points on the graph?", good, bad, [f"Look at the pairs: {', '.join(pt(*p) for p in pts_)}.", good], r=r, qtype="visual",
                  diagram=Diagram("coord", {"xmax": 5, "ymax": m * 3 + 2 if m * 3 + 2 <= 15 else 15, "points": [{"x": p[0], "y": p[1], "label": ""} for p in pts_], "step": 1 if m * 3 + 2 <= 12 else 2}, alt))


@fam("012")
def gp_predict(r, L):
    m = r.randint(2, 6)
    k = r.randint(0, 4) if L == 2 else 0
    x = r.randint(6, 12)
    pts_ = [pt(i, i * m + k) for i in range(4)]
    it = Item(f"The points {', '.join(pts_)} follow a pattern. If the pattern continues, what is y when x = {x}?", str(x * m + k),
                [f"Each time x goes up by 1, y goes up by {m}{' (starting at ' + str(k) + ')' if k else ''}.", f"When x = {x}, y = {x} × {m}{' + ' + str(k) if k else ''} = {x * m + k}."],
                [W(str(x + m + k), "added instead of multiplying"), W(str((x - 1) * m + k), "stopped one step early"), W(str(x * m), "forgot the starting value") if k else W(str(x * (m + 1)), "used the wrong multiplier")],
                EX(f"{x}*{m}+{k}"), qtype="procedural", tags={"connections"})
    it.consts = [m, k]
    return it


@fam("012", mode="mc")
def gp_not_on(r, L):
    a, b = r.randint(1, 3), r.randint(2, 4)
    b = a * b
    good_pts = [pt(a * i, b * i) for i in range(1, 5)]
    bad_pt = pt(a * 2, b * 2 + 1)
    need(bad_pt not in good_pts)
    opts = [(bad_pt, True)] + [(p, False) for p in r.sample(good_pts, 3)]
    need(len({t for t, _ in opts}) == 4)
    r.shuffle(opts)
    return Item(f"Pattern A: start at 0, add {a}. Pattern B: start at 0, add {b}. Which ordered pair (A, B) would NOT be on the graph?", bad_pt,
                [f"Every pair on the graph has B = {b // a} × A.", f"{bad_pt} does not follow that rule."],
                check=FN("not_pattern_pair", a=a, b=b), options=opts, mode="mc", qtype="explain", tags={"reasoning"})


@fam("012", mode="mc")
def gp_table(r, L):
    m = r.randint(2, 5)
    xs = sorted(r.sample(range(1, 9), 3))
    rows = [[str(x), str(x * m)] for x in xs]
    j = r.randrange(3)
    good = pt(xs[j], xs[j] * m)
    bad = [pt(xs[j] * m, xs[j]), pt(xs[j], xs[j] + m), pt(xs[j] + 1, xs[j] * m)]
    need(len(set(bad + [good])) == 4)
    alt = "Table of x and y values: " + "; ".join(f"x = {a}, y = {b}" for a, b in rows) + "."
    opts = [(good, True)] + [(x, False) for x in bad]
    r.shuffle(opts)
    return Item("Which ordered pair comes from the table and could be graphed?", good, ["Each row gives (x, y).", f"{good} is in the table."],
                check=FN("pair_in_table", rows=rows), options=opts, mode="mc", qtype="visual",
                diagram=Diagram("table", {"header": ["x", "y"], "rows": rows}, alt))


SKILLS = {
    1: dict(name="The Coordinate System", fams=[cs_vocab, cs_moves, cs_axis, cs_directions, cs_swap, cs_from_point]),
    2: dict(name="Plotting and Reading Points", fams=[pr_read, pr_which, pr_distance, pr_vertex, pr_move]),
    3: dict(name="Real-World Problems on the Coordinate Plane", fams=[rw_map, rw_graph, rw_meaning, rw_route, rw_compare]),
    4: dict(name="Graphing Patterns and Relationships", fams=[gp_next, gp_rule, gp_predict, gp_not_on, gp_table]),
}
