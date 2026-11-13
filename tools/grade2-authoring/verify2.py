"""Independent verifier for the Grade 2 (math2) banks.

Runs the shared Grade 1 verifier (same checks: counts, answer reconstruction from stored
inputs, options, standards, duplicates, diagram files) against math2, and registers the extra
check kinds that only Grade 2 families use.

Usage: python3 verify2.py [repo_root]
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
G1 = os.path.abspath(os.path.join(HERE, "..", "grade1-authoring"))
sys.path.insert(0, HERE)
sys.path.insert(0, G1)

os.environ["G1_OUTLINE"] = "outline2"
os.environ["G1_OUT"] = os.path.join(HERE, "out")

import verify1
from verify1 import num_eq, norm, as_int, err

SIDES = {"triangle": 3, "square": 4, "rectangle": 4, "quadrilateral": 4, "trapezoid": 4, "rhombus": 4,
         "parallelogram": 4, "pentagon": 5, "hexagon": 6, "octagon": 8}
PARTS = {2: ("halves", "half"), 3: ("thirds", "third"), 4: ("fourths", "fourth", "quarters", "quarter"),
         6: ("sixths", "sixth"), 8: ("eighths", "eighth")}


def h_digit_value3(c, t):
    n = int(c["n"])
    which = c["which"]
    val = {"hundreds": (n // 100) * 100, "tens": (n // 10 % 10) * 10, "ones": n % 10}[which]
    return num_eq(t, val)


def h_expanded3(c, t):
    n = int(c["n"])
    h, r = divmod(n, 100)
    tt, o = divmod(r, 10)
    parts = [f"{h * 100}"] + ([f"{tt * 10}"] if tt else []) + ([f"{o}"] if o else [])
    return norm(t).replace(" ", "") == norm(" + ".join(parts)).replace(" ", "")


def h_skip_seq(c, t):
    vals = [int(v) for v in c["values"]]
    step = int(c["step"])
    if any(vals[i + 1] - vals[i] != step for i in range(len(vals) - 1)):
        return False
    return num_eq(t, int(c["missing"]))


def h_round10(c, t):
    n = int(c["n"])
    down = n // 10 * 10
    want = down if n - down < 5 else down + 10
    return num_eq(t, want)


def h_round_sum(c, t):
    a, b = int(c["a"]), int(c["b"])
    return num_eq(t, (a // 10 * 10) + (b // 10 * 10))


def h_money_cents(c, t):
    s = str(t).strip().replace(" ", "")
    cents = None
    if s.startswith("$"):
        try:
            cents = round(float(s[1:]) * 100)
        except ValueError:
            return False
    elif s.endswith("\u00a2"):
        v = as_int(s[:-1])
        cents = v
    elif re.fullmatch(r"\d+", s):
        cents = int(s)
    elif "cent" in s:
        v = as_int(re.sub(r"[^0-9]", "", s))
        cents = v
    return cents is not None and int(cents) == int(c["cents"])


def h_part_name(c, t):
    parts = int(c["parts"])
    words = PARTS.get(parts, ())
    return norm(t) in {norm(w) for w in words}


def h_polygon_sides(c, t):
    return num_eq(t, SIDES[str(c["kind"])])


def h_polygon_corners(c, t):
    return num_eq(t, SIDES[str(c["kind"])])


def h_array_cols(c, t):
    return num_eq(t, int(c["cols"]))


def h_array_total(c, t):
    return num_eq(t, int(c["rows"]) * int(c["cols"]))


def h_array_rows(c, t):
    return num_eq(t, int(c["rows"]))


def h_even_odd(c, t):
    n = int(c["n"])
    return norm(t) == ("even" if n % 2 == 0 else "odd")


def h_longer_lbl(c, t):
    a, b = int(c["a"]), int(c["b"])
    return norm(t) == norm(f"the {c['left']}" if a > b else f"the {c['right']}")


def h_shorter_lbl(c, t):
    a, b = int(c["a"]), int(c["b"])
    return norm(t) == norm(f"the {c['left']}" if a < b else f"the {c['right']}")


def h_tape_diff(c, t):
    return num_eq(t, abs(int(c["a"]) - int(c["b"])))


def h_lineplot_at(c, t):
    vals = [int(v) for v in c["values"]]
    return num_eq(t, vals.count(int(c["value"])))


def h_lineplot_total(c, t):
    return num_eq(t, sum(int(v) for v in c["values"]))


def h_lineplot_least(c, t):
    vals = [int(v) for v in c["values"]]
    return num_eq(t, min(vals))


def h_lineplot_diff(c, t):
    vals = [int(v) for v in c["values"]]
    return num_eq(t, vals.count(int(c["a"])) - vals.count(int(c["b"])))


def h_lineplot_mode(c, t):
    vals = [int(v) for v in c["values"]]
    counts = {v: vals.count(v) for v in set(vals)}
    best = max(counts.values())
    if list(counts.values()).count(best) != 1:
        return False
    return num_eq(t, [v for v, k in counts.items() if k == best][0])


def h_repeat_add(c, t):
    groups, each = int(c["groups"]), int(c["each"])
    want = " + ".join([str(each)] * groups)
    return norm(t).replace(" ", "") == norm(want).replace(" ", "")


def h_fraction_shaded(c, t):
    return norm(t).replace(" ", "") == f"{int(c['shaded'])}/{int(c['parts'])}"


def h_clock_ampm(c, t):
    return norm(t) == norm(f"{int(c['h'])}:{int(c['m']):02d} {c['part']}")


def h_round100(c, t):
    n = int(c["n"])
    down = n // 100 * 100
    return num_eq(t, down if n - down < 50 else down + 100)


def h_build3(c, t):
    return num_eq(t, int(c["n"]))


def h_graph_least(c, t):
    rows = [(str(r[0]), int(r[1])) for r in c["rows"]]
    least = min(v for _, v in rows)
    if sum(1 for _, v in rows if v == least) != 1:
        return False
    return norm(t) == norm([k for k, v in rows if v == least][0])


def h_graph_diff(c, t):
    rows = [(str(r[0]), int(r[1])) for r in c["rows"]]
    return num_eq(t, max(v for _, v in rows) - min(v for _, v in rows))


def h_strategy(c, t):
    """Make-a-ten is the right method only when the ones digits pass ten."""
    a, b = int(c["a"]), int(c["b"])
    best = (a % 10) + (b % 10) >= 10
    return norm(t).startswith("make ten") if best else False


verify1.HANDLERS.update({
    "strategy": h_strategy, "digit_value3": h_digit_value3, "expanded3": h_expanded3, "skip_seq": h_skip_seq,
    "round10": h_round10, "round_sum": h_round_sum, "money_cents": h_money_cents,
    "part_name": h_part_name, "polygon_sides": h_polygon_sides, "polygon_corners": h_polygon_corners,
    "array_total": h_array_total, "array_cols": h_array_cols, "array_rows": h_array_rows, "even_odd": h_even_odd,
    "longer_lbl": h_longer_lbl, "shorter_lbl": h_shorter_lbl, "tape_diff": h_tape_diff,
    "lineplot_at": h_lineplot_at, "lineplot_least": h_lineplot_least, "lineplot_diff": h_lineplot_diff, "lineplot_total": h_lineplot_total, "lineplot_mode": h_lineplot_mode,
    "repeat_add": h_repeat_add, "round100": h_round100, "build3": h_build3,
    "graph_least": h_graph_least, "graph_diff": h_graph_diff, "fraction_shaded": h_fraction_shaded, "clock_ampm": h_clock_ampm,
})

if __name__ == "__main__":
    sys.exit(verify1.main())
