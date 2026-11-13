"""Unit 6: Word Problems within 100 (word-problems-100). 2.OA.A.1 (with 2.NBT.B.5 computation)."""
from g2lib import *

UNIT_ID = "word-problems-100"


def nums(r, L):
    """part a, part b, whole s with s <= 100 (L0: s <= 50)."""
    if L == 0:
        a, b = r.randint(5, 30), r.randint(4, 20)
        need(a + b <= 50)
    elif L == 1:
        a, b = r.randint(12, 60), r.randint(8, 39)
    else:
        a, b = r.randint(18, 69), r.randint(13, 39)
        need((a % 10 + b % 10) >= 10)
    need(a + b <= 100 and a != b)
    return a, b, a + b


ITEMS = [("marbles", "a jar"), ("stickers", "a book"), ("shells", "a bucket"), ("cards", "a box"), ("beads", "a bag"), ("cubes", "a tub")]


def common(ans, unit, extra=()):
    return [W(f"{ans + 10} {unit}", "made a regrouping mistake"), W(f"{ans - 1} {unit}", "made a counting mistake")] + list(extra)


def story_eq_opts(r, a, b, s, kind):
    """Equation with ? for the unknown, and three that do not match."""
    if kind == "result_add":
        good, bad = f"{a} + {b} = ?", [f"{max(a, b)} − {min(a, b)} = ?", f"{a} + ? = {b}" if a < b else f"? + {b} = {a}", f"{a} + {a} = ?"]
    elif kind == "result_take":
        good, bad = f"{s} − {b} = ?", [f"{s} + {b} = ?", f"? − {s} = {b}", f"{b} − ? = {s}"]
    elif kind == "change_add":
        good, bad = f"{a} + ? = {s}", [f"{a} + {s} = ?", f"? − {a} = {s}", f"{s} + ? = {a}"]
    elif kind == "change_take":
        good, bad = f"{s} − ? = {a}", [f"{s} + {a} = ?", f"{a} − ? = {s}", f"? − {s} = {a}"]
    elif kind == "start_add":
        good, bad = f"? + {b} = {s}", [f"{b} + {s} = ?", f"? − {b} = {s}", f"{s} + ? = {b}"]
    else:   # start_take
        good, bad = f"? − {b} = {a}", [f"{a} − {b} = ?" if a > b else f"{b} − {a} = ?", f"? + {a} = {b}" if b > a else f"{b} + ? = {a}", f"{b} − ? = {a}"]
    return good, bad


# ============================================================== S1 Add To and Take From Problems
@fam("012")
def at_result(r, L):
    a, b, s = nums(r, L)
    unit, place = pick(r, ITEMS)
    nm = name(r)
    if r.random() < 0.5:
        q, ans, e = f"{nm} has {a} {unit}. {nm} gets {b} more {unit}. How many {unit} does {nm} have now?", s, f"{a}+{b}"
        steps = [f"This is an add-to story: {a} + {b} = ?", f"{a} + {b} = {s} {unit}."]
        ex = [W(f"{abs(a - b)} {unit}", "subtracted instead of adding")]
    else:
        q, ans, e = f"{nm} has {s} {unit}. {nm} gives away {b} {unit}. How many {unit} does {nm} have now?", a, f"{s}-{b}"
        steps = [f"This is a take-from story: {s} − {b} = ?", f"{s} − {b} = {a} {unit}."]
        ex = [W(f"{s + b} {unit}", "added instead of subtracting")]
    return Item(q, f"{ans} {unit}", steps, common(ans, unit, ex), EX(e, unit=unit), qtype="word-problem", tags={"modeling"})


@fam("012")
def at_change(r, L):
    a, b, s = nums(r, L)
    unit, place = pick(r, ITEMS)
    nm = name(r)
    if r.random() < 0.5:
        q = f"{nm} had {a} {unit}. {nm} got some more. Now {nm} has {s} {unit}. How many {unit} did {nm} get?"
        ans, eq, steps = b, f"{a} + ___ = {s}", [f"Write {a} + ? = {s}.", f"{s} − {a} = {b} {unit}."]
    else:
        q = f"There were {s} {unit} in {place}. {nm} took some out. Now there are {a} {unit} in {place}. How many {unit} did {nm} take out?"
        ans, eq, steps = b, f"{s} − ___ = {a}", [f"Write {s} − ? = {a}.", f"{s} − {a} = {b} {unit}."]
    return Item(q, f"{ans} {unit}", steps, common(ans, unit, [W(f"{a + s} {unit}", "added the two numbers in the story"), W(f"{s} {unit}", "gave a number from the story")]),
                FN("blank_eq", eq=eq, unit=unit), qtype="word-problem", tags={"modeling"})


@fam("012")
def at_start(r, L):
    a, b, s = nums(r, L)
    unit, place = pick(r, ITEMS)
    nm = name(r)
    if r.random() < 0.5:
        q = f"{nm} had some {unit}. {nm} found {b} more. Now {nm} has {s} {unit}. How many {unit} did {nm} have at first?"
        ans, eq, wrong = a, f"___ + {b} = {s}", W(f"{s + b} {unit}", "added because the story says “more”")
    else:
        q = f"{nm} had some {unit}. {nm} gave {b} to a friend. Now {nm} has {a} {unit}. How many {unit} did {nm} have at first?"
        ans, eq, wrong = s, f"___ − {b} = {a}", W(f"{abs(a - b)} {unit}", "subtracted because the story says “gave”")
    return Item(q, f"{ans} {unit}", [f"Write {eq.replace('___', '?')}.", f"{eq.replace('___', str(ans))}, so {nm} had {ans} {unit} at first."],
                common(ans, unit, [wrong]), FN("blank_eq", eq=eq, unit=unit), qtype="word-problem", tags={"modeling", "challenge"})


@fam("012", mode="mc")
def at_eq(r, L):
    a, b, s = nums(r, L)
    unit, place = pick(r, ITEMS)
    nm = name(r)
    kinds = ["result_add", "result_take", "change_add"] if L == 0 else ["result_add", "result_take", "change_add", "change_take"] if L == 1 else ["change_add", "change_take", "start_add", "start_take"]
    kind = pick(r, kinds)
    stories = {"result_add": (f"{nm} has {a} {unit}. {nm} gets {b} more. How many {unit} now?", s),
               "result_take": (f"{nm} has {s} {unit}. {nm} uses {b}. How many {unit} are left?", a),
               "change_add": (f"{nm} has {a} {unit}. {nm} gets some more and now has {s}. How many did {nm} get?", b),
               "change_take": (f"{nm} has {s} {unit}. {nm} gives some away and now has {a}. How many did {nm} give away?", b),
               "start_add": (f"{nm} had some {unit}. {nm} got {b} more and now has {s}. How many did {nm} have at first?", a),
               "start_take": (f"{nm} had some {unit}. {nm} gave away {b} and now has {a}. How many did {nm} have at first?", s)}
    q, ans = stories[kind]
    good, bad = story_eq_opts(r, a, b, s, kind)
    need(len(set(bad)) == 3 and good not in bad)
    it = mc_key(f"{q} Which equation matches the story? (? stands for the unknown number.)", good, bad, ["Decide what is known and what is unknown in the story.", f"{good}; the unknown is {ans}."], qtype="word-problem", tags={"modeling"}, r=r)
    it.check = FN("story_eq", ans=ans, given=sorted([x for x in (a, b, s) if x != ans]))
    return it


@fam("01")
def at_line(r, L):
    a, b, s = nums(r, L)
    need(b <= 30)
    lo, hi = a // 10 * 10, -(-s // 10) * 10
    nm = name(r)
    alt = f"A number line from {lo} to {hi}. A jump of {b} goes from {a} to a point marked with a question mark."
    return Item(f"{nm} had {a} points and won {b} more points. The number line shows the jump. How many points does {nm} have now?", f"{s} points",
                [f"Start at {a} and jump {b}.", f"{a} + {b} = {s} points."], common(s, "points", [W(f"{abs(a - b)} points", "jumped the wrong way")]),
                EX(f"{a}+{b}", unit="points"), qtype="visual",
                diagram=Diagram("jline", {"lo": lo, "hi": hi if hi > lo else lo + 10, "step": 1, "label_every": 10, "jumps": [[a, s, f"+{b}"]], "points": [{"v": s, "label": "?"}]}, alt))


@fam("2", mode="mc")
def at_keyword(r, L):
    a, b, s = nums(r, 2)
    nm = name(r)
    good = f"{s}, because {nm} had {s} before eating {b}"
    bad = [f"{abs(a - b)}, because “ate” means subtract", f"{a}, because that is how many are left", f"{s + b}, because you add all the numbers"]
    it = mc_key(f"{nm} had some grapes. {nm} ate {b} grapes. Now {nm} has {a} grapes. How many grapes did {nm} have at first?", good, bad,
                [f"The start is unknown: ? − {b} = {a}.", f"{a} + {b} = {s}, so {nm} had {s} grapes."], qtype="error-analysis", tags={"misconception"}, r=r)
    it.check = FN("lead_value", value=s)
    return it


# ============================================================== S2 Put Together and Take Apart Problems
PT = [("red apples", "green apples", "apples", "in a basket"), ("boys", "girls", "children", "in the club"), ("cats", "dogs", "pets", "at the shelter"),
      ("blue cars", "red cars", "cars", "in the lot"), ("big fish", "small fish", "fish", "in the tank")]


@fam("012")
def pt_total(r, L):
    a, b, s = nums(r, L)
    x, y, whole, where = pick(r, PT)
    return Item(f"There are {a} {x} and {b} {y} {where}. How many {whole} are {where}?", f"{s} {whole}",
                [f"Put the parts together: {a} + {b}.", f"{a} + {b} = {s} {whole}."], common(s, whole, [W(f"{abs(a - b)} {whole}", "subtracted instead of adding")]),
                EX(f"{a}+{b}", unit=whole), qtype="word-problem", tags={"modeling"})


@fam("012")
def pt_part(r, L):
    a, b, s = nums(r, L)
    x, y, whole, where = pick(r, PT)
    return Item(f"There are {s} {whole} {where}. {a} are {x}. The rest are {y}. How many {y} are there?", f"{b} {y}",
                [f"Write {a} + ? = {s}.", f"{s} − {a} = {b} {y}."], common(b, y, [W(f"{s + a} {y}", "added the total and the part")]),
                EX(f"{s}-{a}", unit=y), qtype="word-problem", tags={"modeling"})


@fam("012")
def pt_bar(r, L):
    a, b, s = nums(r, L)
    x, y, whole, where = pick(r, PT)
    unknown = pick(r, ["whole", "part"]) if L else "part"
    if unknown == "whole":
        rows = [{"parts": [[s, "?"]]}, {"parts": [[a, str(a)], [b, str(b)]]}]
        alt = f"A bar model. The whole bar is unknown. The parts are {a} and {b}."
        q, ans, e = f"The bar model shows {x} and {y} {where}. How many {whole} are there in all?", s, f"{a}+{b}"
        u = whole
    else:
        rows = [{"parts": [[s, str(s)]]}, {"parts": [[a, str(a)], [b, "?"]]}]
        alt = f"A bar model. The whole bar is {s}. One part is {a}. The other part is unknown."
        q, ans, e = f"The bar model shows {s} {whole} {where}. {a} are {x}. How many are {y}?", b, f"{s}-{a}"
        u = y
    return Item(q, f"{ans} {u}", [f"Use the bar: {'add the parts' if unknown == 'whole' else 'whole − part'}.", f"The answer is {ans} {u}."],
                common(ans, u, [W(f"{s + a if unknown == 'part' else abs(a - b)} {u}", "used the wrong operation")]), EX(e, unit=u), qtype="visual",
                diagram=Diagram("bars", {"rows": rows}, alt))


@fam("012", mode="mc")
def pt_eq(r, L):
    a, b, s = nums(r, L)
    x, y, whole, where = pick(r, PT)
    good = f"{a} + ? = {s}"
    bad = [f"{a} + {s} = ?", f"? − {a} = {s}", f"{s} + ? = {a}"]
    it = mc_key(f"There are {s} {whole} {where}. {a} are {x}. The rest are {y}. Which equation can find the number of {y}?", good, bad,
                ["The parts add to the whole.", f"{a} + ? = {s}, so ? = {b}."], qtype="word-problem", tags={"modeling"}, r=r)
    it.check = FN("story_eq", ans=b, given=[a, s])
    return it


@fam("012")
def pt_three(r, L):
    a, b, c = (r.randint(4, 18), r.randint(3, 15), r.randint(3, 15)) if L == 0 else (r.randint(11, 35), r.randint(11, 35), r.randint(11, 30))
    need(a + b + c <= (50 if L == 0 else 100))
    return Item(f"A garden has {a} red flowers, {b} yellow flowers, and {c} white flowers. How many flowers are in the garden?", f"{a + b + c} flowers",
                [f"Add all three parts: {a} + {b} + {c}.", f"{a} + {b} + {c} = {a + b + c} flowers."],
                common(a + b + c, "flowers", [W(f"{a + b} flowers", "left out a part")]), EX(f"{a}+{b}+{c}", unit="flowers"), qtype="word-problem", tags={"modeling"})


@fam("2")
def pt_part3(r, L):
    a, b, c = r.randint(11, 30), r.randint(11, 30), r.randint(11, 30)
    s = a + b + c
    need(s <= 100)
    return Item(f"A team has {s} players. {a} are in first grade and {b} are in second grade. The rest are in third grade. How many players are in third grade?", f"{c} players",
                [f"{a} + {b} = {a + b} players are in first or second grade.", f"{s} − {a + b} = {c} players."],
                common(c, "players", [W(f"{s - a} players", "subtracted only one part"), W(f"{s + a + b if s + a + b < 1000 else s} players", "added all the numbers")]),
                EX(f"{s}-{a}-{b}", unit="players"), qtype="multi-step", tags={"multistep"})


# ============================================================== S3 Compare Problems
@fam("012")
def cm_diff(r, L):
    a, b, s = nums(r, L)
    n1, n2 = name(r), name(sub(r, 3))
    need(n1 != n2)
    word = pick(r, ["more", "fewer"]) if L else "more"
    t = pick(r, ["shells", "stamps", "books", "coins"])
    q = (f"{n1} has {s} {t}. {n2} has {a} {t}. How many more {t} does {n1} have than {n2}?" if word == "more" else
         f"{n1} has {s} {t}. {n2} has {a} {t}. How many fewer {t} does {n2} have than {n1}?")
    return Item(q, f"{b} {t}", [f"Find the difference: {s} − {a}.", f"{s} − {a} = {b} {t}."],
                common(b, t, [W(f"{s + a} {t}", "added because the question says “more”" if word == "more" else "added the two amounts")]),
                EX(f"{s}-{a}", unit=t), qtype="word-problem", tags={"modeling"})


@fam("012")
def cm_bigger(r, L):
    a, b, s = nums(r, L)
    n1, n2 = name(r), name(sub(r, 3))
    need(n1 != n2)
    t = pick(r, ["inches of string", "pennies", "points", "rocks"])
    unit = t.split(" ")[0]
    return Item(f"{n1} has {a} {t}. {n2} has {b} more {t.split(' of ')[0]} than {n1}. How many {t.split(' of ')[0]} does {n2} have?", f"{s} {unit}",
                [f"{n2} has the same as {n1} and {b} more: {a} + {b}.", f"{a} + {b} = {s} {unit}."],
                common(s, unit, [W(f"{abs(a - b)} {unit}", "subtracted instead of adding")]), EX(f"{a}+{b}", unit=unit), qtype="word-problem", tags={"modeling"})


@fam("012")
def cm_smaller(r, L):
    a, b, s = nums(r, L)
    n1, n2 = name(r), name(sub(r, 3))
    need(n1 != n2)
    t = pick(r, ["pages", "laps", "points", "cards"])
    return Item(f"{n1} has {s} {t}. {n2} has {b} fewer {t} than {n1}. How many {t} does {n2} have?", f"{a} {t}",
                [f"{n2} has {b} fewer, so subtract: {s} − {b}.", f"{s} − {b} = {a} {t}."],
                common(a, t, [W(f"{s + b} {t}", "added instead of subtracting")]), EX(f"{s}-{b}", unit=t), qtype="word-problem", tags={"modeling"})


@fam("2")
def cm_tricky(r, L):
    a, b, s = nums(r, 2)
    n1, n2 = name(r), name(sub(r, 3))
    need(n1 != n2)
    return Item(f"{n1} has {s} stickers. {n1} has {b} more stickers than {n2}. How many stickers does {n2} have?", f"{a} stickers",
                [f"{n1} has more, so {n2} has fewer: {s} − {b}.", f"{s} − {b} = {a} stickers."],
                common(a, "stickers", [W(f"{s + b} stickers", "added because the story says “more”")]), EX(f"{s}-{b}", unit="stickers"),
                qtype="word-problem", tags={"modeling", "misconception", "challenge"})


@fam("012")
def cm_bars(r, L):
    a, b, s = nums(r, L)
    n1, n2 = name(r), name(sub(r, 3))
    need(n1 != n2)
    alt = f"Two bars lined up at the left. {n1}'s bar is {s}. {n2}'s bar is {a}. The extra part of {n1}'s bar is marked with a question mark."
    return Item(f"The bars compare the number of laps {n1} and {n2} swam. How many more laps did {n1} swim?", f"{b} laps",
                [f"The difference is the extra part: {s} − {a}.", f"{s} − {a} = {b} laps."],
                common(b, "laps", [W(f"{s + a} laps", "added the two bars")]), EX(f"{s}-{a}", unit="laps"), qtype="visual",
                diagram=Diagram("bars", {"rows": [{"label": n1, "parts": [[s, str(s)]]}, {"label": n2, "parts": [[a, str(a)], [b, "?"]]}]}, alt))


@fam("012", mode="mc")
def cm_eq(r, L):
    a, b, s = nums(r, L)
    n1, n2 = name(r), name(sub(r, 3))
    need(n1 != n2)
    good = f"{a} + ? = {s}"
    bad = [f"{a} + {s} = ?", f"? − {s} = {a}", f"{s} + ? = {a}"]
    it = mc_key(f"{n1} has {s} crayons. {n2} has {a} crayons. Which equation finds how many more crayons {n1} has?", good, bad,
                ["The difference is how much to add to the smaller amount to get the bigger amount.", f"{a} + ? = {s}, so ? = {b}."], qtype="word-problem", tags={"modeling"}, r=r)
    it.check = FN("story_eq", ans=b, given=[a, s])
    return it


# ============================================================== S4 Two-Step Word Problems
@fam("012")
def ts_add_sub(r, L):
    a, b = r.randint(15, 45), r.randint(10, 30)
    c = r.randint(5, a + b - 5)
    need(a + b <= 100 and (L or (a + b <= 60)))
    return Item(f"A bus had {a} people. At the first stop, {b} people got on. At the next stop, {c} people got off. How many people are on the bus now?", f"{a + b - c} people",
                [f"First: {a} + {b} = {a + b}.", f"Then: {a + b} − {c} = {a + b - c} people."],
                [W(f"{a + b} people", "did only the first step"), W(f"{a + b + c} people", "added all the numbers"), W(f"{a - b + c if a - b + c > 0 else a + b - c + 10} people", "used the wrong operations")],
                EX(f"{a}+{b}-{c}", unit="people"), qtype="multi-step", tags={"multistep"})


@fam("012")
def ts_sub_sub(r, L):
    a = r.randint(40, 99) if L else r.randint(30, 60)
    b, c = r.randint(8, 25), r.randint(8, 25)
    need(a - b - c > 0)
    nm = name(r)
    return Item(f"{nm} had {a} cents. {nm} spent {b} cents on a pencil and {c} cents on an eraser. How many cents does {nm} have left?", f"{a - b - c} cents",
                [f"{a} − {b} = {a - b}.", f"{a - b} − {c} = {a - b - c} cents."],
                [W(f"{a - b} cents", "did only the first step"), W(f"{b + c} cents", "found how much was spent"), W(f"{a - b + c} cents", "added the second amount")],
                EX(f"{a}-{b}-{c}", unit="cents"), qtype="multi-step", tags={"multistep"})


@fam("12")
def ts_compare_total(r, L):
    a = r.randint(15, 40)
    b = r.randint(5, 20)
    need(a + a + b <= 100)
    n1, n2 = name(r), name(sub(r, 3))
    need(n1 != n2)
    return Item(f"{n1} picked {a} strawberries. {n2} picked {b} more than {n1}. How many strawberries did they pick in all?", f"{a + a + b} strawberries",
                [f"{n2}: {a} + {b} = {a + b}.", f"Together: {a} + {a + b} = {2 * a + b} strawberries."],
                [W(f"{a + b} strawberries", "found only how many " + n2 + " picked"), W(f"{a + b + b} strawberries", "added the extra twice"), W(f"{a + a - b} strawberries", "subtracted instead of adding")],
                EX(f"{a}+{a}+{b}", unit="strawberries"), qtype="multi-step", tags={"multistep"})


@fam("012")
def ts_need(r, L):
    goal = r.randint(6, 10) * 10 if L else r.randint(3, 5) * 10
    a, b = (r.randint(12, 35), r.randint(10, 30)) if L else (r.randint(5, 15), r.randint(5, 12))
    need(goal - a - b > 0)
    nm = name(r)
    return Item(f"{nm} wants to read {goal} pages. {nm} read {a} pages on Monday and {b} pages on Tuesday. How many more pages does {nm} need to read?", f"{goal - a - b} pages",
                [f"Pages read: {a} + {b} = {a + b}.", f"{goal} − {a + b} = {goal - a - b} pages."],
                [W(f"{a + b} pages", "did only the first step"), W(f"{goal - a} pages", "used only Monday"), W(f"{goal - a + b} pages", "added Tuesday instead of subtracting")],
                EX(f"{goal}-{a}-{b}", unit="pages"), qtype="multi-step", tags={"multistep"})


@fam("012", mode="mc")
def ts_eq(r, L):
    a, b = r.randint(15, 45), r.randint(10, 30)
    c = r.randint(5, a + b - 5)
    need(a + b <= 100)
    good = f"{a} + {b} − {c} = ?"
    bad = [f"{a} + {b} + {c} = ?", f"{a} − {b} − {c} = ?" if a - b - c > 0 else f"{a} − {b} + {c} = ?", f"{a} + {c} − {b} = ?" if a + c - b > 0 else f"{c} − {a} = ?"]
    need(len(set(bad)) == 3)
    it = mc_key(f"A shelf had {a} books. {b} books were added. Then {c} books were taken. Which equation shows how many books are on the shelf now?", good, bad,
                ["Books added: plus. Books taken: minus.", f"{a} + {b} − {c} = {a + b - c}."], qtype="word-problem", tags={"modeling", "multistep"}, r=r)
    it.check = FN("expr_eq", value=a + b - c, nums=[a, b, c])
    return it


@fam("2")
def ts_start(r, L):
    a, b, c = r.randint(20, 50), r.randint(10, 25), r.randint(5, 20)
    end = a - b + c
    need(end > 0 and a + c <= 100)
    nm = name(r)
    return Item(f"{nm} had some toy cars. {nm} gave away {b} cars and then got {c} new cars. Now {nm} has {end} cars. How many cars did {nm} have at first?", f"{a} cars",
                [f"Work backward: {end} − {c} = {end - c}.", f"{end - c} + {b} = {a} cars."],
                [W(f"{end - b + c} cars", "worked backward with the wrong operations"), W(f"{end + b + c} cars", "added all the numbers"), W(f"{end - c} cars", "did only one step")],
                EX(f"{end}-{c}+{b}", unit="cars"), qtype="multi-step", tags={"multistep", "challenge"})


@fam("01")
def ts_two_bars(r, L):
    a, b = r.randint(12, 40), r.randint(5, 20)
    need(2 * a + b <= 100)
    n1, n2 = name(r), name(sub(r, 3))
    need(n1 != n2)
    alt = f"Two bars lined up at the left. {n1}'s bar is {a}. {n2}'s bar is {a} and {b} more."
    return Item(f"The bars show the beads {n1} and {n2} have. {n1} has {a} beads. {n2} has {b} more beads than {n1}. How many beads do they have together?", f"{2 * a + b} beads",
                [f"{n2} has {a} + {b} = {a + b} beads.", f"{a} + {a + b} = {2 * a + b} beads."],
                [W(f"{a + b} beads", "found only one amount"), W(f"{a + a} beads", "forgot the extra beads"), W(f"{2 * a + 2 * b} beads", "added the extra twice")],
                EX(f"{a}+{a}+{b}", unit="beads"), qtype="visual", tags={"multistep"},
                diagram=Diagram("bars", {"rows": [{"label": n1, "parts": [[a, str(a)]]}, {"label": n2, "parts": [[a, str(a)], [b, str(b)]]}]}, alt))


SKILLS = {
    1: dict(name="Add To and Take From Problems", fams=[at_result, at_change, at_start, at_eq, at_line, at_keyword]),
    2: dict(name="Put Together and Take Apart Problems", fams=[pt_total, pt_part, pt_bar, pt_eq, pt_three, pt_part3]),
    3: dict(name="Compare Problems", fams=[cm_diff, cm_bigger, cm_smaller, cm_tricky, cm_bars, cm_eq]),
    4: dict(name="Two-Step Word Problems", fams=[ts_add_sub, ts_sub_sub, ts_compare_total, ts_need, ts_eq, ts_start, ts_two_bars]),
}
