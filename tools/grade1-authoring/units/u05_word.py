"""Unit 5: Word Problems within 20 (word-problems-20). 1.OA.A.1, 1.OA.A.2, 1.OA.D.8."""
from g1lib import *

UNIT_ID = "word-problems-20"


def nums(r, L, lo_sum=None):
    """Two numbers a, b with total by level: L0 <= 10, L1 <= 20 (11-20), L2 13-20."""
    if L == 0:
        a, b = r.randint(1, 7), r.randint(1, 6)
        need(3 <= a + b <= 10)
    elif L == 1:
        a, b = r.randint(2, 12), r.randint(2, 9)
        need(9 <= a + b <= 20)
    else:
        a, b = r.randint(4, 14), r.randint(4, 9)
        need(13 <= a + b <= 20)
    return a, b


def U(n, th):
    return f"{n} {th[0] if n == 1 else th[1]}"


def ws(ans, th, extra):
    out = [W(U(x, th), y) for x, y in extra if x >= 0 and x != ans]
    out += [W(U(ans + 1, th), "counted one too many")]
    if ans > 1:
        out.append(W(U(ans - 1, th), "counted one too few"))
    return out


# ============================================================== S1 Add To and Take From
@fam("012")
def at_add(r, L):
    a, b = nums(r, L)
    th, nm = thing(r), name(r)
    an = animal(r)
    t = pick(r, [f"{nm} has {U(a, th)}. {nm} gets {b} more. How many {th[1]} does {nm} have now?",
                 f"There {'is' if a == 1 else 'are'} {U(a, an)} in the yard. {b} more come. How many {an[1]} are in the yard now?",
                 f"{nm} had {U(a, th)}. Then {nm} found {b} more. How many {th[1]} does {nm} have now?"])
    if "yard" in t:
        th = an
    return Item(t, U(a + b, th), [f"Some more were added, so add: {a} + {b}.", f"{a} + {b} = {a + b}."],
                ws(a + b, th, [(abs(a - b), "subtracted instead of adding"), (a, "did not add the second number")]), EX(f"{a}+{b}", unit=th[1]),
                qtype="word-problem", tags={"modeling"})


@fam("012")
def at_take(r, L):
    a, b = nums(r, L)
    w = a + b
    th, nm = thing(r), name(r)
    t = pick(r, [f"{nm} has {U(w, th)}. {nm} gives {b} away. How many {th[1]} does {nm} have now?",
                 f"There are {U(w, th)} on the table. {nm} takes {b}. How many {th[1]} are on the table now?",
                 f"{w} {th[1]} were in a box. {b} fell out. How many {th[1]} are in the box now?"])
    return Item(t, U(a, th), [f"Some were taken away, so subtract: {w} − {b}.", f"{w} − {b} = {a}."],
                ws(a, th, [(w + b, "added instead of subtracting"), (b, "gave the number taken away"), (w, "did not take any away")]), EX(f"{w}-{b}", unit=th[1]),
                qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def at_eq(r, L):
    a, b = nums(r, L)
    th, nm = thing(r), name(r)
    if r.random() < 0.5:
        p = f"{nm} has {U(a, th)} and gets {b} more. Which equation shows the story?"
        good, bad = f"{a} + {b} = ___", [f"{a} − {b} = ___" if a > b else f"{b} − {a} = ___", f"{a} + ___ = {b}", f"{b} − ___ = {a}" if b > a else f"___ − {b} = {a + b + 1}"]
    else:
        w = a + b
        p = f"{nm} has {U(w, th)} and gives away {b}. Which equation shows the story?"
        good, bad = f"{w} − {b} = ___", [f"{w} + {b} = ___", f"{b} − {w} = ___", f"{w} − ___ = {w}"]
    it = mc_key(p, good, bad, ["Did the group get bigger or smaller?", f"The story is {good}."], qtype="conceptual", tags={"modeling"}, r=r)
    return it


@fam("012")
def at_pic(r, L):
    a, b = nums(r, L)
    w = a + b
    th, nm = thing(r), name(r)
    th = pick(r, [("cookie", "cookies"), ("apple", "apples"), ("grape", "grapes")])
    alt = f"{w} counters. {b} of them are crossed out."
    return Item(f"{nm} had {U(w, th)}. {nm} ate {b}. The picture shows the story. How many {th[1]} are left?", U(a, th),
                [f"{w} counters with {b} crossed out.", f"{w} − {b} = {a}."], ws(a, th, [(w + b, "added instead of subtracting"), (b, "counted the crossed-out ones")]),
                EX(f"{w}-{b}", unit=th[1]), qtype="visual", tags={"modeling"}, diagram=Diagram("crossrow", {"n": w, "x": b, "per": 10 if w > 10 else 5}, alt))


@fam("012", mode="mc")
def at_op(r, L):
    a, b = nums(r, L)
    th, nm = thing(r), name(r)
    add = r.random() < 0.5
    if add:
        p = f"{nm} has {U(a, th)}. A friend gives {nm} {b} more. Should you add or subtract to find how many {th[1]} {nm} has now?"
        good = f"Add, because {nm} gets more."
        bad = [f"Subtract, because {nm} gets more.", f"Subtract, because {b} is less than {a}." if b < a else f"Subtract, because {a} is less than {b}.", "Add, because the numbers are small."]
    else:
        p = f"{nm} has {U(a + b, th)}. {nm} loses {b}. Should you add or subtract to find how many {th[1]} are left?"
        good = f"Subtract, because some are taken away."
        bad = ["Add, because there are two numbers.", "Add, because some are taken away.", "Subtract, because the numbers are small."]
    it = mc_key(p, good, bad, ["Think about what happens in the story.", good], qtype="conceptual", tags={"reasoning"}, r=r)
    return it


# ============================================================== S2 Put Together and Take Apart
@fam("012")
def pt_total(r, L):
    a, b = nums(r, L)
    th, nm = thing(r), name(r)
    c1, c2 = r.sample(["red", "blue", "green", "yellow", "big", "small"], 2)
    t = pick(r, [f"{nm} has {a} {c1} {th[0] if a == 1 else th[1]} and {b} {c2} {th[0] if b == 1 else th[1]}. How many {th[1]} does {nm} have?",
                 f"A bag holds {a} {c1} {th[0] if a == 1 else th[1]} and {b} {c2} {th[0] if b == 1 else th[1]}. How many {th[1]} are in the bag?"])
    return Item(t, U(a + b, th), [f"Put the two parts together: {a} + {b}.", f"{a} + {b} = {a + b}."],
                ws(a + b, th, [(abs(a - b), "subtracted instead of adding"), (a, "used only one part")]), EX(f"{a}+{b}", unit=th[1]),
                qtype="word-problem", tags={"modeling"})


@fam("012")
def pt_part(r, L):
    a, b = nums(r, L)
    w = a + b
    th, nm = thing(r), name(r)
    c1, c2 = r.sample(["red", "blue", "green", "yellow"], 2)
    t = pick(r, [f"{nm} has {U(w, th)}. {a} are {c1}. The rest are {c2}. How many {th[1]} are {c2}?",
                 f"There are {U(w, th)} in all. {a} are {c1} and the others are {c2}. How many are {c2}?"])
    return Item(t, U(b, th), [f"The whole is {w} and one part is {a}.", f"{a} + {b} = {w}, so {b} are {c2}."],
                ws(b, th, [(w + a, "added the whole and the part"), (a, "gave the part that was told"), (w, "gave the whole")]), EX(f"{w}-{a}", unit=th[1]),
                qtype="word-problem", tags={"modeling"})


@fam("012")
def pt_bar(r, L):
    a, b = nums(r, L)
    w = a + b
    th = thing(r)
    unk = pick(r, ["whole", "part"])
    if unk == "whole":
        alt = f"A bar model with parts {a} and {b}. The whole is unknown."
        rows = [{"label": "", "parts": [[w, "?"]]}, {"label": "", "parts": [[a, str(a)], [b, str(b)]]}]
        return Item(f"There are {a} big {th[0] if a == 1 else th[1]} and {b} small {th[0] if b == 1 else th[1]}. The bar shows the story. How many {th[1]} in all?", U(w, th),
                    [f"Add the parts: {a} + {b}.", f"{a} + {b} = {w}."], ws(w, th, [(abs(a - b), "subtracted instead of adding")]), EX(f"{a}+{b}", unit=th[1]),
                    qtype="visual", tags={"modeling"}, diagram=Diagram("bars", {"rows": rows}, alt))
    alt = f"A bar model with whole {w} and parts {a} and unknown."
    rows = [{"label": "", "parts": [[w, str(w)]]}, {"label": "", "parts": [[a, str(a)], [b, "?"]]}]
    return Item(f"There are {U(w, th)}. {a} are big. The rest are small. The bar shows the story. How many are small?", U(b, th),
                [f"{a} + ___ = {w}.", f"{w} − {a} = {b}."], ws(b, th, [(w + a, "added the whole and the part"), (w, "gave the whole")]), EX(f"{w}-{a}", unit=th[1]),
                qtype="visual", tags={"modeling"}, diagram=Diagram("bars", {"rows": rows}, alt))


@fam("012", mode="mc")
def pt_eq(r, L):
    a, b = nums(r, L)
    w = a + b
    th, nm = thing(r), name(r)
    p = f"{nm} has {U(w, th)}. {a} are in a cup. The rest are in a box. Which equation can find how many are in the box?"
    good = f"{a} + ___ = {w}"
    bad = [f"{a} + {w} = ___", f"___ − {w} = {a}", f"{w} + ___ = {a}"]
    it = mc_key(p, good, bad, [f"The parts are {a} and the unknown. The whole is {w}.", f"{good}."], qtype="conceptual", tags={"modeling"}, r=r)
    return it


@fam("012", mode="mc")
def pt_ways(r, L):
    w = r.randint(4, 9) if L == 0 else r.randint(8, 15) if L == 1 else r.randint(12, 20)
    th = thing(r)
    a = r.randint(2, w - 2)
    good = f"{a} red and {w - a} blue"
    bad = [f"{a} red and {w - a + 1} blue", f"{a + 1} red and {w - a + 1} blue", f"{w} red and {a} blue"]
    it = mc_key(f"A jar has {U(w, th)}. Some are red and some are blue. Which could be true?", good, bad,
                [f"The two parts must add to {w}.", f"{a} + {w - a} = {w}."], qtype="reasoning", tags={"reasoning"}, r=r)
    it.check = FN("parts_make", total=w)
    return it


# ============================================================== S3 Compare Stories
@fam("012")
def cp_more(r, L):
    a, b = nums(r, L)
    big, small = a + b, a
    need(b >= 1 and small >= 1)
    th = thing(r)
    n1, n2 = r.sample(NAMES, 2)
    t = pick(r, [f"{n1} has {U(big, th)}. {n2} has {U(small, th)}. How many more {th[1]} does {n1} have than {n2}?",
                 f"{n1} has {U(small, th)}. {n2} has {U(big, th)}. How many fewer {th[1]} does {n1} have than {n2}?"])
    return Item(t, U(b, th), [f"Compare {big} and {small}: {small} + ___ = {big}.", f"{big} − {small} = {b}."],
                ws(b, th, [(big + small, "added because the question says more"), (big, "gave the bigger number"), (small, "gave the smaller number")]),
                EX(f"{big}-{small}", unit=th[1]), qtype="word-problem", tags={"modeling"})


@fam("012")
def cp_bigger(r, L):
    a, b = nums(r, L)
    th = thing(r)
    n1, n2 = r.sample(NAMES, 2)
    t = pick(r, [f"{n1} has {U(a, th)}. {n2} has {b} more {th[1]} than {n1}. How many {th[1]} does {n2} have?",
                 f"{n1} read {a} books. {n2} read {b} more books than {n1}. How many books did {n2} read?"])
    unit = "books" if "books than" in t else th[1]
    th2 = ("book", "books") if unit == "books" else th
    return Item(t, U(a + b, th2), [f"{n2} has the same as {n1} and {b} more.", f"{a} + {b} = {a + b}."],
                ws(a + b, th2, [(abs(a - b), "subtracted because the story compares"), (b, "gave only the difference")]), EX(f"{a}+{b}", unit=unit),
                qtype="word-problem", tags={"modeling"})


@fam("012")
def cp_smaller(r, L):
    a, b = nums(r, L)
    big = a + b
    th = thing(r)
    n1, n2 = r.sample(NAMES, 2)
    t = pick(r, [f"{n1} has {U(big, th)}. {n2} has {b} fewer {th[1]} than {n1}. How many {th[1]} does {n2} have?",
                 f"{n1} has {U(big, th)}. {n1} has {b} more than {n2}. How many {th[1]} does {n2} have?"])
    return Item(t, U(a, th), [f"{n2} has {b} fewer than {big}.", f"{big} − {b} = {a}."],
                ws(a, th, [(big + b, "added because the story says more"), (big, "gave the bigger number"), (b, "gave the difference")]),
                EX(f"{big}-{b}", unit=th[1]), qtype="word-problem", tags={"modeling", "misconception"})


@fam("012")
def cp_pic(r, L):
    a, b = nums(r, L)
    big = a + b
    n1, n2 = r.sample(NAMES, 2)
    alt = f"Two bars lined up. {n1}'s bar is {big} long. {n2}'s bar is {a} long."
    return Item(f"{n1} has {big} stickers. {n2} has {a} stickers. The bars show both. How many more stickers does {n1} have?", f"{b} stickers",
                [f"Line up the bars. The extra part is {big} − {a}.", f"{big} − {a} = {b}."],
                [W(f"{big + a} stickers", "added the two numbers"), W(f"{big} stickers", "gave the bigger number"), W(f"{b + 1} stickers", "counted one too many"), W(f"{a} stickers", "gave the smaller number")],
                EX(f"{big}-{a}", unit="stickers"), qtype="visual", tags={"modeling"},
                diagram=Diagram("bars", {"rows": [{"label": n1, "parts": [[big, str(big)]]}, {"label": n2, "parts": [[a, str(a)]]}]}, alt))


@fam("012", mode="mc")
def cp_eq(r, L):
    a, b = nums(r, L)
    big = a + b
    th = thing(r)
    n1, n2 = r.sample(NAMES, 2)
    good = f"{big} − {a} = ___"
    bad = [f"{big} + {a} = ___", f"{a} − {big} = ___", f"{big} + ___ = {a}"]
    it = mc_key(f"{n1} has {U(big, th)}. {n2} has {U(a, th)}. Which equation finds how many more {n1} has?", good, bad,
                [f"Compare: find the difference between {big} and {a}.", f"{good}."], qtype="conceptual", tags={"modeling"}, r=r)
    return it


# ============================================================== S4 Stories with a Missing Start or Change
@fam("012")
def ms_change_add(r, L):
    a, b = nums(r, L)
    th, nm = thing(r), name(r)
    t = pick(r, [f"{nm} has {U(a, th)}. {nm} gets some more. Now {nm} has {a + b}. How many {th[1]} did {nm} get?",
                 f"There were {U(a, th)} on a shelf. Some more were put on the shelf. Now there are {a + b}. How many were put on the shelf?"])
    return Item(t, U(b, th), [f"{a} + ___ = {a + b}.", f"Count on from {a} to {a + b}: that is {b}."],
                ws(b, th, [(2 * a + b, "added the two numbers"), (a + b, "gave the total"), (a, "gave the start")]), EX(f"{a + b}-{a}", unit=th[1]),
                qtype="word-problem", tags={"modeling"})


@fam("012")
def ms_change_sub(r, L):
    a, b = nums(r, L)
    w = a + b
    th, nm = thing(r), name(r)
    t = pick(r, [f"{nm} had {U(w, th)}. {nm} gave some away. Now {nm} has {a}. How many {th[1]} did {nm} give away?",
                 f"There were {U(w, th)} in a basket. Some were taken out. Now there are {a}. How many were taken out?"])
    if r.random() < 0.35:
        th = pick(r, [("bird", "birds"), ("bee", "bees")])
        t = f"There were {U(w, th)} in a tree. Some flew away. Now there are {a}. How many {th[1]} flew away?"
    return Item(t, U(b, th), [f"{w} − ___ = {a}.", f"{w} − {b} = {a}, so {b}."],
                ws(b, th, [(w + a, "added the two numbers"), (a, "gave the number left"), (w, "gave the start")]), EX(f"{w}-{a}", unit=th[1]),
                qtype="word-problem", tags={"modeling"})


@fam("12")
def ms_start_add(r, L):
    a, b = nums(r, L)
    th, nm = thing(r), name(r)
    t = f"{nm} had some {th[1]}. Then {nm} got {b} more. Now {nm} has {a + b}. How many {th[1]} did {nm} have at the start?"
    return Item(t, U(a, th), [f"___ + {b} = {a + b}.", f"{a + b} − {b} = {a}."],
                ws(a, th, [(a + 2 * b, "added because the story says got more"), (a + b, "gave the end amount"), (b, "gave the change")]), EX(f"{a + b}-{b}", unit=th[1]),
                qtype="word-problem", tags={"modeling", "misconception"})


@fam("12")
def ms_start_sub(r, L):
    a, b = nums(r, L)
    th, nm = thing(r), name(r)
    t = f"{nm} had some {th[1]}. {nm} gave {b} away. Now {nm} has {a}. How many {th[1]} did {nm} have at the start?"
    return Item(t, U(a + b, th), [f"___ − {b} = {a}.", f"{a} + {b} = {a + b}."],
                ws(a + b, th, [(abs(a - b), "subtracted because the story says gave away"), (a, "gave the end amount"), (b, "gave the change")]),
                EX(f"{a}+{b}", unit=th[1]), qtype="word-problem", tags={"modeling", "misconception"})


@fam("012", mode="mc")
def ms_eq(r, L):
    a, b = nums(r, L)
    th, nm = thing(r), name(r)
    if L < 2:
        p = f"{nm} has {U(a, th)}. {nm} gets some more. Now {nm} has {a + b}. Which equation shows the story?"
        good, bad = f"{a} + ___ = {a + b}", [f"{a} + {a + b} = ___", f"{a} − ___ = {a + b}", f"___ − {a} = {a + b}"]
    else:
        p = f"{nm} had some {th[1]}. {nm} gave {b} away and has {a} left. Which equation shows the story?"
        good, bad = f"___ − {b} = {a}", [f"{b} − {a} = ___" if b > a else f"{a} − {b} = ___", f"{a} + {b} + ___ = {a}", f"___ + {a} = {b}"]
    it = mc_key(p, good, bad, ["Put the blank where the story has the unknown.", f"{good}."], qtype="conceptual", tags={"modeling"}, r=r)
    return it


@fam("0")
def ms_small(r, L):
    a, b = r.randint(1, 5), r.randint(1, 4)
    need(a + b <= 9)
    th, nm = thing(r), name(r)
    alt = f"Ten frame with {a} red counters and {b} yellow counters."
    return Item(f"{nm} had {U(a, th)} and got some more. Now {nm} has {a + b}. The red counters show the start. How many {th[1]} did {nm} get?", U(b, th),
                [f"The yellow counters are the ones {nm} got.", f"{a} + {b} = {a + b}."], ws(b, th, [(a + b, "gave the total"), (a, "counted the red counters")]),
                EX(f"{a + b}-{a}", unit=th[1]), qtype="visual", tags={"modeling"}, diagram=Diagram("tenframe", {"frames": 1, "a": a, "b": b}, alt))


@fam("0")
def ms_small_sub(r, L):
    a, b = r.randint(1, 5), r.randint(1, 5)
    need(a + b <= 10)
    nm = name(r)
    alt = f"Ten frame with {a + b} counters. {b} of them are crossed out."
    return Item(f"{nm} had {a + b} grapes. {nm} ate some. Now {nm} has {a}. The picture shows the story. How many grapes did {nm} eat?", f"{b} grapes",
                [f"The crossed-out counters are the grapes {nm} ate.", f"{a + b} − {b} = {a}."],
                [W(f"{a} grapes", "gave the number left"), W(f"{a + b} grapes", "gave the start"), W(f"{2 * a + b} grapes", "added the numbers"), W(f"{b + 1} grapes", "counted one too many")],
                EX(f"{a + b}-{a}", unit="grapes"), qtype="visual", tags={"modeling"}, diagram=Diagram("tenframe", {"frames": 1, "a": a + b, "x": b}, alt))


# ============================================================== S5 Stories with Three Numbers
def three(r, L):
    if L == 0:
        a, b, c = r.randint(1, 4), r.randint(1, 4), r.randint(1, 4)
        need(a + b + c <= 10)
    elif L == 1:
        a, b, c = r.randint(2, 8), r.randint(2, 8), r.randint(2, 8)
        need(10 < a + b + c <= 18 and (a + b == 10 or b + c == 10 or a + c == 10 or r.random() < 0.4))
    else:
        a, b, c = r.randint(3, 9), r.randint(3, 9), r.randint(3, 9)
        need(15 <= a + b + c <= 20)
    return a, b, c


@fam("012")
def th_sum(r, L):
    a, b, c = three(r, L)
    th, nm = thing(r), name(r)
    t = pick(r, [f"{nm} has {a} red {th[0] if a == 1 else th[1]}, {b} blue {th[0] if b == 1 else th[1]}, and {c} green {th[0] if c == 1 else th[1]}. How many {th[1]} does {nm} have?",
                 f"{nm} picks {U(a, th)} on Monday, {b} on Tuesday, and {c} on Wednesday. How many {th[1]} in all?",
                 f"There {'is' if a == 1 else 'are'} {ns(a, th)} in one box, {b} in a second box, and {c} in a third box. How many {th[1]} are there?"])
    return Item(t, U(a + b + c, th), ["Add all three numbers. Look for a ten.", f"{a} + {b} + {c} = {a + b + c}."],
                ws(a + b + c, th, [(a + b, "left out a number"), (b + c, "left out a number"), (a + c, "left out a number")]),
                EX(f"{a}+{b}+{c}", unit=th[1]), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def th_eq(r, L):
    a, b, c = three(r, L)
    nm = name(r)
    good = f"{a} + {b} + {c} = ___"
    bad = [f"{a} + {b} = ___", f"{a} + {b} − {c} = ___", f"{a + b} + {c + 1} = ___"]
    it = mc_key(f"{nm} has {U(a, ('cat', 'cats'))}, {U(b, ('dog', 'dogs'))}, and {U(c, ('fish', 'fish'))}. Which equation shows how many pets {nm} has?", good, bad,
                ["All three groups are put together.", f"{good}."], qtype="conceptual", tags={"modeling"}, r=r)
    return it


@fam("012")
def th_missing(r, L):
    a, b, c = three(r, L)
    s = a + b + c
    th, nm = thing(r), name(r)
    return Item(f"{nm} has {U(s, th)}. {a} are red, {b} are blue, and the rest are green. How many are green?", U(c, th),
                [f"{a} + {b} = {a + b}.", f"{a + b} + ___ = {s}, so {c} are green."],
                ws(c, th, [(s + a + b, "added all the numbers"), (s - a, "took away only one part"), (a + b, "gave the red and blue together")]),
                EX(f"{s}-{a}-{b}", unit=th[1]), qtype="multi-step", tags={"multistep"})


@fam("012")
def th_pic(r, L):
    a, b, c = three(r, L)
    alt = f"Three circles of dots with {a}, {b}, and {c} dots."
    return Item(pick(r, ["Each circle shows a group of shells. How many shells are there in all?", "How many dots are in the three circles in all?"]), a + b + c,
                ["Add the three groups.", f"{a} + {b} + {c} = {a + b + c}."], [W(a + b, "left out a group"), W(b + c, "left out a group"), W(a + b + c + 1, "counted one too many"), W(a + b + c - 1, "counted one too few")],
                EX(f"{a}+{b}+{c}"), qtype="visual", diagram=Diagram("groups", {"counts": [a, b, c]}, alt))


@fam("012")
def th_table(r, L):
    a, b, c = three(r, L)
    cats = r.sample(["Apples", "Pears", "Plums", "Grapes", "Limes"], 3)
    alt = f"Table: {cats[0]} {a}, {cats[1]} {b}, {cats[2]} {c}."
    return Item("The table shows the fruit in a basket. How many pieces of fruit are in the basket?", a + b + c,
                ["Add the three numbers in the table.", f"{a} + {b} + {c} = {a + b + c}."],
                [W(a + b, "left out a row"), W(b + c, "left out a row"), W(a + b + c + 1, "counted one too many"), W(a + b + c - 10 if a + b + c > 10 else a + b + c + 10, "lost the ten")],
                EX(f"{a}+{b}+{c}"), qtype="visual", diagram=Diagram("table", {"header": ["Fruit", "Number"], "rows": [[cats[0], a], [cats[1], b], [cats[2], c]]}, alt))


SKILLS = {
    1: dict(name="Add To and Take From Stories", fams=[at_add, at_take, at_eq, at_pic, at_op]),
    2: dict(name="Put Together and Take Apart Stories", fams=[pt_total, pt_part, pt_bar, pt_eq, pt_ways]),
    3: dict(name="Compare Stories", fams=[cp_more, cp_bigger, cp_smaller, cp_pic, cp_eq]),
    4: dict(name="Stories with a Missing Start or Change", fams=[ms_change_add, ms_change_sub, ms_start_add, ms_start_sub, ms_eq, ms_small, ms_small_sub]),
    5: dict(name="Stories with Three Numbers", fams=[th_sum, th_eq, th_missing, th_pic, th_table]),
}
