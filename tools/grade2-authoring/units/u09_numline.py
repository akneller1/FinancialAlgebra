"""Unit 9: Length Problems and the Number Line (length-number-line). 2.MD.B.5, 2.MD.B.6."""
from g2lib import *

UNIT_ID = "length-number-line"

UNITS_ = ["inches", "centimeters", "feet", "meters"]


def lens(r, L):
    if L == 0:
        a, b = r.randint(8, 35), r.randint(5, 20)
        need(a + b <= 50)
    else:
        a, b = r.randint(15, 65), r.randint(9, 35)
        need(a + b <= 100)
        need(L < 2 or (a % 10 + b % 10 >= 10))
    return a, b


def lw(ans, u, extra=()):
    return [W(f"{ans + 10} {u}", "made a regrouping mistake"), W(f"{ans - 1} {u}", "made a counting mistake")] + list(extra)


# ============================================================== S1 Length Word Problems
@fam("012")
def lw_join(r, L):
    a, b = lens(r, L)
    u = pick(r, UNITS_[:2] if L == 0 else UNITS_)
    t = pick(r, ["{nm} tapes a {a}-{u1} strip of paper to a {b}-{u1} strip, end to end. How long is the new strip?",
                 "A train has a car that is {a} {u} long and a car that is {b} {u} long. How long are the two cars together?",
                 "{nm} ran {a} {u} and then {b} more {u}. How far did {nm} run?"])
    u1 = {"inches": "inch", "centimeters": "centimeter", "feet": "foot", "meters": "meter"}[u]
    return Item(t.format(a=a, b=b, u=u, u1=u1, nm=name(r)), f"{a + b} {u}", [f"Join the lengths: {a} + {b}.", f"{a} + {b} = {a + b} {u}."],
                lw(a + b, u, [W(f"{abs(a - b)} {u}", "subtracted instead of adding"), W(f"{a + b}", "left out the unit")]), EX(f"{a}+{b}", unit=u), qtype="word-problem", tags={"modeling"})


@fam("012")
def lw_cut(r, L):
    a, b = lens(r, L)
    u = pick(r, UNITS_[:2] if L == 0 else UNITS_)
    s = a + b
    t = pick(r, [("A ribbon is {s} {u} long. {nm} cuts off {b} {u}. How long is the ribbon now?", a),
                 ("A rope was {s} {u} long. A piece {b} {u} long broke off. How long is the rope now?", a)])
    return Item(t[0].format(s=s, b=b, u=u, nm=name(r)), f"{t[1]} {u}", [f"Take away the cut piece: {s} − {b}.", f"{s} − {b} = {a} {u}."],
                lw(a, u, [W(f"{s + b} {u}", "added the cut piece")]), EX(f"{s}-{b}", unit=u), qtype="word-problem", tags={"modeling"})


@fam("012")
def lw_compare(r, L):
    a, b = lens(r, L)
    u = pick(r, UNITS_[:2] if L == 0 else UNITS_)
    s = a + b
    n1, n2 = name(r), name(sub(r, 4))
    need(n1 != n2)
    return Item(f"{n1} jumped {s} {u}. {n2} jumped {a} {u}. How much farther did {n1} jump?", f"{b} {u}", [f"Find the difference: {s} − {a}.", f"{s} − {a} = {b} {u}."],
                lw(b, u, [W(f"{s + a} {u}", "added the two jumps")]), EX(f"{s}-{a}", unit=u), qtype="word-problem", tags={"modeling"})


@fam("12")
def lw_start(r, L):
    a, b = lens(r, L)
    u = pick(r, UNITS_)
    return Item(f"{name(r)} cut {b} {u} off a board. Now the board is {a} {u} long. How long was the board at first?", f"{a + b} {u}",
                [f"? − {b} = {a}.", f"{a} + {b} = {a + b} {u}."], lw(a + b, u, [W(f"{abs(a - b)} {u}", "subtracted because the story says “cut off”")]),
                EX(f"{a}+{b}", unit=u), qtype="word-problem", tags={"modeling", "challenge"})


@fam("012", mode="mc")
def lw_eq(r, L):
    a, b = lens(r, L)
    u = pick(r, UNITS_[:2])
    s = a + b
    good = f"{s} − {b} = ?"
    bad = [f"{s} + {b} = ?", f"{b} − ? = {s}", f"? − {s} = {b}"]
    it = mc_key(f"A string is {s} {u} long. {name(r)} cuts off {b} {u}. Which equation finds how long the string is now? (? is the unknown.)", good, bad,
                ["Cutting off takes length away.", f"{s} − {b} = {a}, so the string is {a} {u}."], qtype="word-problem", tags={"modeling"}, r=r)
    it.check = FN("story_eq", ans=a, given=[b, s])
    return it


@fam("01")
def lw_ruler(r, L):
    a = r.randint(3, 9)
    b = r.randint(2, 12 - a)
    alt = f"A ruler marked in inches from 0 to 12. A green bar goes from 0 to {a}, and a blue bar goes from {a} to {a + b}."
    return Item(f"{name(r)} glued a {a}-inch stick to a {b}-inch stick end to end, as the ruler shows. How long are the sticks together?", f"{a + b} inches",
                [f"{a} + {b}.", f"The sticks reach the {a + b} mark, so they are {a + b} inches long."],
                [W(f"{b} inches", "measured only one stick"), W(f"{a + b + 1} inches", "counted the tick marks"), W(f"{abs(a - b)} inches", "subtracted instead of adding")],
                EX(f"{a}+{b}", unit="inches"), qtype="visual",
                diagram=Diagram("ruler2", {"length": 12, "unit": "inches", "objects": [{"start": 0, "end": a, "label": "stick 1"}, {"start": a, "end": a + b, "label": "stick 2"}]}, alt))


@fam("12")
def lw_path(r, L):
    a, b, c = r.randint(10, 35), r.randint(10, 35), r.randint(10, 30)
    need(a + b + c <= 100)
    u = pick(r, ["feet", "meters"])
    return Item(f"A path has three parts. They are {a} {u}, {b} {u}, and {c} {u} long. How long is the whole path?", f"{a + b + c} {u}",
                [f"Add all three parts: {a} + {b} + {c}.", f"{a} + {b} + {c} = {a + b + c} {u}."], lw(a + b + c, u, [W(f"{a + b} {u}", "left out a part")]),
                EX(f"{a}+{b}+{c}", unit=u), qtype="word-problem", tags={"modeling"})


@fam("2")
def lw_two_step(r, L):
    a, b = lens(r, 2)
    c = r.randint(5, a + b - 5)
    u = pick(r, UNITS_[:2])
    u1 = {"inches": "inch", "centimeters": "centimeter"}[u]
    nm = name(r)
    return Item(f"{nm} had a {a}-{u1} piece of yarn and a {b}-{u1} piece. {nm} used {c} {u} of yarn. How much yarn is left?",
                f"{a + b - c} {u}", [f"Total yarn: {a} + {b} = {a + b}.", f"{a + b} − {c} = {a + b - c} {u}."],
                [W(f"{a + b} {u}", "did only the first step"), W(f"{a - c if a > c else a + b + c} {u}", "used only one piece"), W(f"{a + b + c} {u}", "added all the numbers")],
                EX(f"{a}+{b}-{c}", unit=u), qtype="multi-step", tags={"multistep"})


# ============================================================== S2 Whole Numbers on a Number Line
def line_for(r, L):
    if L == 0:
        lo, hi, st, le = 0, 20, 1, 5
    elif L == 1:
        lo, hi, st, le = 0, 100, 5, 2
    else:
        lo = r.randint(1, 8) * 10
        lo, hi, st, le = lo, lo + 20, 1, 10
    return lo, hi, st, le


@fam("012")
def nl_point(r, L):
    lo, hi, st, le = line_for(r, L)
    v = lo + st * r.randint(1, (hi - lo) // st - 1)
    need(((v - lo) // st) % le != 0)
    alt = f"A number line from {lo} to {hi} with a tick every {st}; every {le * st} is labeled. A point is at an unlabeled tick."
    return Item("What number is at the point?", v, [f"Each tick is {st} more than the one before it.", f"Count from the nearest label: the point is at {v}."],
                [W(v + st, "counted one tick too many"), W(v - st, "counted one tick too few"), W(lo + (v - lo) // st, "counted ticks by ones") if st > 1 else W(v + 10, "used the wrong label")],
                FN("point_val", v=v), qtype="visual",
                diagram=Diagram("jline", {"lo": lo, "hi": hi, "step": st, "label_every": le, "points": [{"v": v, "label": "?"}]}, alt))


@fam("012")
def nl_length(r, L):
    hi = 20 if L == 0 else 30
    v = r.randint(3, hi - 2)
    return Item(f"A length starts at 0 on the number line and ends at {v}. How many units long is it?", v, [f"Count the spaces from 0 to {v}.", f"It is {v} units long."],
                [W(v + 1, "counted the tick marks instead of the spaces"), W(v - 1, "started counting at 1"), W(hi - v, "counted from the wrong end")],
                FN("point_val", v=v), qtype="conceptual", tags={"reasoning"})


@fam("012", mode="mc")
def nl_which(r, L):
    lo, hi, st, le = line_for(r, L)
    vals = r.sample(range(lo + st, hi, st), 4)
    labels = ["A", "B", "C", "D"]
    pts = dict(zip(labels, vals))
    want = pick(r, labels)
    alt = f"A number line from {lo} to {hi} with a tick every {st}; every {le * st} is labeled. Points: " + ", ".join(f"{k} at {v}" for k, v in pts.items()) + "."
    it = mc_key(f"Which point shows {pts[want]}?", want, [k for k in labels if k != want], [f"Find {pts[want]} on the line.", f"Point {want} is at {pts[want]}."], qtype="visual", r=r,
                diagram=Diagram("jline", {"lo": lo, "hi": hi, "step": st, "label_every": le, "points": [{"v": v, "label": k} for k, v in pts.items()]}, alt))
    it.check = FN("point_label", points=pts, v=pts[want])
    return it


@fam("012")
def nl_between(r, L):
    a = r.randint(1, 9) * 10 if L else r.randint(0, 1) * 10
    k = pick(r, [5]) if L == 0 else pick(r, [2, 5, 8])
    v = a + k
    alt = f"A number line from {a} to {a + 10} with a tick for every 1. Only {a} and {a + 10} are labeled. A point is at {v}."
    return Item(f"The number line shows {a} to {a + 10}. What number is at the point?", v, [f"There are 10 equal spaces from {a} to {a + 10}.", f"The point is {k} spaces after {a}, at {v}."],
                [W(v + 1, "counted the tick marks"), W(a + 10 - k, "counted from the wrong end"), W(k, "counted spaces from the wrong place")],
                FN("point_val", v=v), qtype="visual",
                diagram=Diagram("jline", {"lo": a, "hi": a + 10, "step": 1, "labels": [a, a + 10], "points": [{"v": v, "label": "?"}]}, alt))


@fam("012")
def nl_missing_label(r, L):
    st = pick(r, [5, 10])
    lo = r.randint(0, 5) * 10
    hi = lo + st * 8
    v = lo + st * r.randint(1, 7)
    alt = f"A number line from {lo} to {hi} with equally spaced ticks every {st}. Every tick is labeled except one, which shows a question mark."
    labels = [x for x in range(lo, hi + 1, st) if x != v]
    return Item("The ticks on the number line are equally spaced. What number goes where the question mark is?", v, [f"The labels go up by {st}.", f"The missing number is {v}."],
                [W(v + st, "skipped a number"), W(v - st + 1, "counted by ones"), W(v + 1, "counted by ones")],
                FN("point_val", v=v), qtype="visual",
                diagram=Diagram("jline", {"lo": lo, "hi": hi, "step": st, "labels": labels, "points": [{"v": v, "label": "?"}]}, alt))


@fam("2", mode="mc")
def nl_error(r, L):
    v = r.randint(4, 15)
    nm = name(r)
    good = f"No. Count the spaces from 0, not the tick marks. The length is {v}."
    bad = [f"Yes. There are {v + 1} tick marks.", f"No. The length is {v - 1}, because you start at 1.", f"Yes. Count every mark you see."]
    it = mc_key(f"{nm} says a bar from 0 to {v} on a number line is {v + 1} units long because there are {v + 1} tick marks. Is {nm} right?", good, bad,
                [f"Length is the number of spaces (units).", f"From 0 to {v} there are {v} spaces."], qtype="error-analysis", tags={"misconception"}, r=r)
    it.check = FN("lead_len", v=v)
    return it


# ============================================================== S3 Adding and Subtracting on a Number Line
def jump_nums(r, L):
    if L == 0:
        a, b = r.randint(2, 12), r.randint(2, 8)
        need(a + b <= 20)
        lo, hi, le = 0, 20, 5
    else:
        a, b = r.randint(15, 70), r.randint(5, 30)
        need(a + b <= 100)
        lo, hi, le = a // 10 * 10, -(-(a + b) // 10) * 10, 10
        need(hi - lo <= 50)
    return a, b, lo, hi, le


@fam("012")
def nj_land(r, L):
    a, b, lo, hi, le = jump_nums(r, L)
    op = pick(r, ["+", "−"]) if L else "+"
    start, end = (a, a + b) if op == "+" else (a + b, a)
    alt = f"A number line from {lo} to {hi}. An arrow starts at {start} and jumps {'forward' if op == '+' else 'back'} {b} to a point marked with a question mark."
    return Item(f"The number line shows {start} {op} {b}. Where does the jump land?", end, [f"Start at {start} and jump {'forward' if op == '+' else 'back'} {b}.", f"{start} {op} {b} = {end}."],
                [W(start - b if op == "+" and start > b else start + b, "jumped the wrong way"), W(end + 1 if op == "+" else end - 1, "counted the starting tick"), W(end + 10 if op == "+" else end - 10, "made a counting mistake") if end - 10 > 0 else W(end + 2, "made a counting mistake")],
                EX(f"{start}{'+' if op == '+' else '-'}{b}"), qtype="visual",
                diagram=Diagram("jline", {"lo": lo, "hi": hi, "step": 1, "label_every": le, "jumps": [[start, end, f"{'+' if op == '+' else '−'}{b}"]], "points": [{"v": end, "label": "?"}]}, alt))


@fam("012")
def nj_eq(r, L):
    a, b, lo, hi, le = jump_nums(r, L)
    op = pick(r, ["+", "−"])
    start, end = (a, a + b) if op == "+" else (a + b, a)
    alt = f"A number line from {lo} to {hi}. An arrow starts at {start} and jumps {'forward' if op == '+' else 'back'} {b}, landing on {end}."
    eq = f"{start} {op} {b} = {end}"
    return Item("Write the equation that the number line shows.", eq, [f"It starts at {start}, jumps {'forward' if op == '+' else 'back'} {b}, and lands on {end}.", eq + "."],
                [W(f"{start} {'−' if op == '+' else '+'} {b} = {end}", "used the wrong operation"), W(f"{end} {op} {b} = {start}", "started at the wrong end")],
                FN("jump_eq", start=start, end=end), qtype="visual",
                diagram=Diagram("jline", {"lo": lo, "hi": hi, "step": 1, "label_every": le, "jumps": [[start, end, f"{'+' if op == '+' else '−'}{b}"]], "points": [{"v": end, "label": ""}]}, alt))


@fam("012")
def nj_size(r, L):
    a, b, lo, hi, le = jump_nums(r, L)
    alt = f"A number line from {lo} to {hi}. A jump goes from {a} to {a + b}; its size is marked with a question mark."
    return Item(f"A jump on the number line starts at {a} and lands on {a + b}. How long is the jump?", b, [f"Count up from {a} to {a + b}.", f"{a + b} − {a} = {b}."],
                [W(a + b, "gave where it landed"), W(b + 1, "counted the tick marks"), W(2 * a + b if 2 * a + b <= 100 else b - 1, "added the numbers")],
                EX(f"{a + b}-{a}"), qtype="visual",
                diagram=Diagram("jline", {"lo": lo, "hi": hi, "step": 1, "label_every": le, "jumps": [[a, a + b, "?"]]}, alt))


@fam("012")
def nj_two(r, L):
    a, b, lo, hi, le = jump_nums(r, max(L, 1))
    bt, bo = b // 10 * 10, b % 10
    need(bt and bo)
    alt = f"A number line from {lo} to {hi}. A jump of {bt} goes from {a} to {a + bt}, then a jump of {bo} goes to a point marked with a question mark."
    return Item(f"The number line shows {a} + {b} in two jumps. Where does the second jump land?", a + b, [f"{a} + {bt} = {a + bt}.", f"{a + bt} + {bo} = {a + b}."],
                [W(a + bt, "stopped after the first jump"), W(a + bo, "made only the ones jump"), W(a + b + 10, "made an extra jump of 10")],
                EX(f"{a}+{bt}+{bo}"), qtype="visual",
                diagram=Diagram("jline", {"lo": lo, "hi": hi, "step": 1, "label_every": le, "jumps": [[a, a + bt, f"+{bt}"], [a + bt, a + b, f"+{bo}"]], "points": [{"v": a + b, "label": "?"}]}, alt))


@fam("012", mode="mc")
def nj_describe(r, L):
    a, b, lo, hi, le = jump_nums(r, L)
    op = pick(r, ["+", "−"]) if L else "+"
    start = a if op == "+" else a + b
    good = f"Start at {start} and jump {'forward' if op == '+' else 'back'} {b}."
    bad = [f"Start at {start} and jump {'back' if op == '+' else 'forward'} {b}.", f"Start at {b} and jump {'forward' if op == '+' else 'back'} {start}.", f"Start at 0 and jump {'forward' if op == '+' else 'back'} {b}."]
    it = mc_key(f"How would you show {start} {op} {b} on a number line?", good, bad, ["Start at the first number.", f"{'Adding' if op == '+' else 'Subtracting'} moves {'forward (to the right)' if op == '+' else 'back (to the left)'}."], qtype="conceptual", r=r)
    it.check = FN("jump_desc", start=start, size=b, op=op)
    return it


@fam("2")
def nj_back_two(r, L):
    a = r.randint(50, 95)
    b = r.randint(21, 39)
    need(a - b > 10 and b % 10 and a % 10 < b % 10)
    bt, bo = b // 10 * 10, b % 10
    return Item(f"Show {a} − {b} on a number line by jumping back {bt} and then back {bo}. Where do you land?", a - b, [f"{a} − {bt} = {a - bt}.", f"{a - bt} − {bo} = {a - b}."],
                [W(a - bt, "made only the first jump"), W(a - b + 10, "jumped back too little"), W(a - bt + bo, "jumped the second way by mistake")],
                EX(f"{a}-{bt}-{bo}"), qtype="explain", tags={"reasoning"})


SKILLS = {
    1: dict(name="Length Word Problems", fams=[lw_join, lw_cut, lw_compare, lw_start, lw_eq, lw_ruler, lw_path, lw_two_step]),
    2: dict(name="Whole Numbers on a Number Line", fams=[nl_point, nl_length, nl_which, nl_between, nl_missing_label, nl_error]),
    3: dict(name="Adding and Subtracting on a Number Line", fams=[nj_land, nj_eq, nj_size, nj_two, nj_describe, nj_back_two]),
}
