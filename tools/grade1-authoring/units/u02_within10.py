"""Unit 2: Addition and Subtraction within 10 (add-subtract-10). 1.OA.C.6, 1.OA.B.4."""
from g1lib import *

UNIT_ID = "add-subtract-10"


def apair(r, L):
    """Two addends. L0: sum 2-6, L1: sum 5-10, L2: sum 7-10 with no zero and no 1."""
    if L == 0:
        a, b = r.randint(1, 5), r.randint(1, 4)
        need(2 <= a + b <= 6)
    elif L == 1:
        a, b = r.randint(1, 8), r.randint(1, 8)
        need(5 <= a + b <= 10)
    else:
        a, b = r.randint(2, 8), r.randint(2, 8)
        need(7 <= a + b <= 10)
    return a, b


def add_w(a, b, unit=""):
    s = a + b
    u = (" " + unit) if unit else ""
    return [W(f"{s - 1}{u}", "counted on and included the first number"), W(f"{s + 1}{u}", "counted one too many"),
            W(f"{abs(a - b)}{u}", "subtracted instead of adding"), W(f"{max(a, b)}{u}", "did not add the second number"), W(f"{s + 2}{u}", "made a counting mistake")]


def sub_w(w, p, unit=""):
    d = w - p
    u = (" " + unit) if unit else ""
    out = [W(f"{d + 1}{u}", "counted back and included the starting number"), W(f"{w + p}{u}", "added instead of subtracting"),
           W(f"{p}{u}", "gave the number taken away")]
    if d > 0:
        out.append(W(f"{d - 1}{u}", "counted back one too many"))
    out.append(W(f"{w}{u}", "did not take any away"))
    return out


# ============================================================== S1 Adding within 10
@fam("012")
def ad_fact(r, L):
    a, b = apair(r, L)
    if L == 2 and r.random() < 0.5:
        return Item(f"___ = {a} + {b}", a + b, ["The equal sign means both sides are the same.", f"{a} + {b} = {a + b}, so {a + b} = {a} + {b}."],
                    add_w(a, b), FN("blank_eq", eq=f"___ = {a} + {b}"), claim=f"___ = {a} + {b}")
    return Item(pick(r, [f"What is {a} + {b}?", f"Add: {a} + {b} = ___", f"Find the sum of {a} and {b}."]), a + b,
                [f"Start at {max(a, b)} and count on {min(a, b)}.", f"{a} + {b} = {a + b}."], add_w(a, b), EX(f"{a}+{b}"), claim=f"{a} + {b}")


@fam("012")
def ad_frame(r, L):
    a, b = apair(r, L)
    alt = f"Ten frame with {a} red counters and {b} yellow counters."
    return Item(pick(r, ["How many counters are in the ten frame in all?", "Red and yellow counters are in the ten frame. How many in all?",
                         "What addition does the ten frame show? Find the total."]), a + b,
                [f"There are {a} red and {b} yellow counters.", f"{a} + {b} = {a + b}."], add_w(a, b), EX(f"{a}+{b}"), qtype="visual",
                diagram=Diagram("tenframe", {"frames": 1, "a": a, "b": b}, alt))


@fam("012")
def ad_word(r, L):
    a, b = apair(r, L)
    th, nm = thing(r), name(r)
    t = pick(r, [f"{nm} has {a} {th[1]}. {nm} gets {b} more. How many {th[1]} does {nm} have now?",
                 f"There are {a} {th[1]} on a table. {b} more {th[1]} are put on the table. How many {th[1]} are on the table now?",
                 f"{nm} sees {a} {th[1]} and then {b} more {th[1]}. How many {th[1]} does {nm} see in all?"])
    return Item(t, f"{a + b} {th[1]}", [f"Add {a} and {b}.", f"{a} + {b} = {a + b} {th[1]}."], add_w(a, b, th[1]), EX(f"{a}+{b}", unit=th[1]),
                qtype="word-problem", tags={"modeling"})


@fam("01")
def ad_groups(r, L):
    a, b = apair(r, L)
    alt = f"Two circles of dots. One circle has {a} dots and the other has {b} dots."
    return Item(pick(r, ["How many dots are there in all?", "Count all the dots. How many?"]), a + b, [f"There are {a} dots and {b} dots.", f"{a} + {b} = {a + b}."],
                add_w(a, b), EX(f"{a}+{b}"), qtype="visual", diagram=Diagram("groups", {"counts": [a, b]}, alt))


@fam("012", mode="mc")
def ad_which_sum(r, L):
    s = r.randint(4, 6) if L == 0 else r.randint(6, 10)
    a = r.randint(1, s - 1)
    good = f"{a} + {s - a}"
    bads = []
    for d in (1, -1, 2):
        x = r.randint(1, max(1, s - 2))
        y = s - x + d
        if y >= 0 and f"{x} + {y}" not in bads and x + y != s:
            bads.append(f"{x} + {y}")
    need(len(bads) == 3)
    it = mc_key(pick(r, [f"Which addition has a sum of {s}?", f"Which one makes {s}?"]), good, bads, [f"Add each pair.", f"{good} = {s}."], qtype="procedural", r=r)
    it.check = FN("same_value", target=str(s))
    return it


@fam("12")
def ad_line(r, L):
    a, b = apair(r, L)
    alt = "Number line from 0 to 10."
    return Item(f"Use the number line. Start at {a} and jump {b} to the right. Where do you land?", a + b,
                [f"Make {pl(b, 'jump')} of 1 from {a}.", f"{a} + {b} = {a + b}."], add_w(a, b), EX(f"{a}+{b}"), qtype="visual",
                diagram=Diagram("jline", {"lo": 0, "hi": 10}, alt))


@fam("2")
def ad_zero_one(r, L):
    a = r.randint(3, 9)
    k = pick(r, [0, 1])
    need(a + k <= 10)
    return Item(f"{name(r)} says {a} + {k} is {a + k + (1 if k == 0 else -1)}. What is the right sum?", a + k,
                [("Adding 0 does not change the number." if k == 0 else "Adding 1 gives the next number."), f"{a} + {k} = {a + k}."],
                [W(a + k + (1 if k == 0 else -1), "agreed with the wrong answer"), W(a + k + 2, "made a counting mistake"), W(k, "wrote the number added"), W(a - k if k else a + 10, "subtracted")],
                EX(f"{a}+{k}"), qtype="explain", tags={"reasoning"})


# ============================================================== S2 Subtracting within 10
def spair(r, L):
    if L == 0:
        w = r.randint(3, 6)
        p = r.randint(1, min(3, w - 1))
    elif L == 1:
        w = r.randint(5, 10)
        p = r.randint(1, w - 1)
    else:
        w = r.randint(7, 10)
        p = r.randint(3, w - 1)
    return w, p


@fam("012")
def sb_fact(r, L):
    w, p = spair(r, L)
    if L == 2 and r.random() < 0.4:
        return Item(f"___ = {w} − {p}", w - p, ["Both sides must be the same.", f"{w} − {p} = {w - p}."], sub_w(w, p),
                    FN("blank_eq", eq=f"___ = {w} − {p}"), claim=f"___ = {w} − {p}")
    return Item(pick(r, [f"What is {w} − {p}?", f"Subtract: {w} − {p} = ___", f"Take {p} away from {w}. What is left?"]), w - p,
                [f"Start at {w} and count back {p}.", f"{w} − {p} = {w - p}."], sub_w(w, p), EX(f"{w}-{p}"), claim=f"{w} − {p}")


@fam("012")
def sb_cross(r, L):
    w, p = spair(r, L)
    alt = f"{w} counters. {p} of them are crossed out."
    return Item(pick(r, ["Some counters are crossed out. How many are left?", "The crossed out counters are taken away. How many are left?",
                         "What subtraction does the picture show? How many are left?"]), w - p,
                [f"There are {w} counters and {p} are crossed out.", f"{w} − {p} = {w - p}."], sub_w(w, p), EX(f"{w}-{p}"), qtype="visual",
                diagram=Diagram("crossrow", {"n": w, "x": p}, alt))


@fam("012")
def sb_frame(r, L):
    w, p = spair(r, L)
    alt = f"Ten frame with {w} red counters. {p} of them are crossed out."
    return Item(pick(r, ["How many counters are not crossed out?", "Count the counters that are left. How many?"]), w - p,
                [f"{w} counters, {p} crossed out.", f"{w} − {p} = {w - p}."], sub_w(w, p), EX(f"{w}-{p}"), qtype="visual",
                diagram=Diagram("tenframe", {"frames": 1, "a": w, "x": p}, alt))


@fam("012")
def sb_word(r, L):
    w, p = spair(r, L)
    th, nm = thing(r), name(r)
    t = pick(r, [f"{nm} has {w} {th[1]}. {nm} gives {p} to a friend. How many {th[1]} does {nm} have now?",
                 f"There are {w} {th[1]} in a box. {nm} takes out {p}. How many {th[1]} are still in the box?",
                 f"{w} {th[1]} are on the mat. {p} roll away. How many {th[1]} are on the mat now?"])
    return Item(t, f"{w - p} {th[1]}", [f"Take {p} away from {w}.", f"{w} − {p} = {w - p} {th[1]}."], sub_w(w, p, th[1]),
                EX(f"{w}-{p}", unit=th[1]), qtype="word-problem", tags={"modeling"})


@fam("12")
def sb_think_add(r, L):
    w, p = spair(r, L)
    return Item(f"Think addition to subtract. {p} + ___ = {w}, so {w} − {p} = ___. What number goes in both blanks?", w - p,
                [f"{p} + {w - p} = {w}.", f"So {w} − {p} = {w - p}."], sub_w(w, p), FN("blank_eq", eq=f"{p} + ___ = {w}"),
                qtype="compare-strategies", tags={"connections"})


@fam("01")
def sb_line(r, L):
    w, p = spair(r, L)
    alt = "Number line from 0 to 10."
    return Item(f"Use the number line. Start at {w} and jump back {p}. Where do you land?", w - p,
                [f"Make {pl(p, 'jump')} to the left from {w}.", f"{w} − {p} = {w - p}."], sub_w(w, p), EX(f"{w}-{p}"), qtype="visual",
                diagram=Diagram("jline", {"lo": 0, "hi": 10}, alt))


@fam("2", mode="mc")
def sb_which(r, L):
    d = r.randint(2, 6)
    w = r.randint(d + 2, 10)
    good = f"{w} − {w - d}"
    bad = []
    for x in range(10, 2, -1):
        y = r.randint(1, x - 1)
        if x - y != d and abs(x - y - d) <= 2 and f"{x} − {y}" not in bad:
            bad.append(f"{x} − {y}")
        if len(bad) == 3:
            break
    need(len(bad) == 3)
    it = mc_key(f"Which subtraction has a difference of {d}?", good, bad, ["Subtract each one.", f"{good} = {d}."], qtype="procedural", r=r)
    it.check = FN("same_value", target=str(d))
    return it


# ============================================================== S3 Making Ten
@fam("012")
def mt_partner(r, L):
    a = r.randint(5, 9) if L == 0 else r.randint(1, 9)
    if L == 2:
        eq = pick(r, [f"10 = {a} + ___", f"___ + {a} = 10", f"10 − {a} = ___"])
    else:
        eq = f"{a} + ___ = 10"
    return Item(pick(r, [f"What number makes this true? {eq}", f"Find the missing number: {eq}"]), 10 - a,
                [f"Count on from {a} to 10.", f"{a} + {10 - a} = 10."],
                [W(10 + a, "added the numbers"), W(a, "copied the number given"), W(9 - a, "counted one too few"), W(11 - a, "counted on and included the first number")],
                FN("blank_eq", eq=eq), claim=eq)


@fam("012")
def mt_frame(r, L):
    a = r.randint(4, 9) if L == 0 else r.randint(1, 9)
    alt = f"Ten frame with {a} counters and {10 - a} empty boxes."
    return Item(pick(r, ["How many more counters are needed to fill the ten frame?", "How many empty boxes are in the ten frame?",
                         "The ten frame needs 10 counters. How many more are needed?"]), 10 - a,
                [f"There are {a} counters.", f"{a} + {10 - a} = 10, so {10 - a} more."],
                [W(a, "counted the counters, not the empty boxes"), W(10, "gave the total"), W(9 - a, "counted one too few"), W(11 - a, "counted one too many")],
                FN("blank_eq", eq=f"{a} + ___ = 10"), qtype="visual", diagram=Diagram("tenframe", {"frames": 1, "a": a}, alt))


@fam("012", mode="mc")
def mt_pair(r, L):
    a = r.randint(1, 9)
    good = f"{a} and {10 - a}"
    bad = []
    for d in (1, -1, 2, -2):
        b = 10 - a + d
        if 0 <= b <= 10 and f"{a} and {b}" not in bad:
            bad.append(f"{a} and {b}")
    r.shuffle(bad)
    it = mc_key(pick(r, ["Which two numbers make 10?", "Which pair adds to 10?"]), good, bad[:3], ["Add each pair.", f"{a} + {10 - a} = 10."], qtype="procedural", r=r)
    it.check = FN("pair_ten", total=10)
    return it


@fam("012")
def mt_word(r, L):
    a = r.randint(4, 9) if L == 0 else r.randint(1, 9)
    th, nm = thing(r), name(r)
    t = pick(r, [f"{nm} has {a} {th[1]}. {nm} wants 10. How many more {th[1]} does {nm} need?",
                 f"A box holds 10 {th[1]}. There are {a} in the box. How many more {th[1]} will fill the box?"])
    return Item(t, f"{10 - a} {th[1]}", [f"{a} + ___ = 10.", f"{a} + {10 - a} = 10, so {10 - a} more {th[1]}."],
                [W(f"{10 + a} {th[1]}", "added the numbers"), W(f"{a} {th[1]}", "gave the number already there"),
                 W(f"{9 - a} {th[1]}", "counted one too few"), W(f"{11 - a} {th[1]}", "counted one too many")],
                EX(f"10-{a}", unit=th[1]), qtype="word-problem", tags={"modeling"})


@fam("2")
def mt_three(r, L):
    a, b = r.randint(1, 5), r.randint(1, 5)
    need(a + b <= 8)
    eq = f"{a} + {b} + ___ = 10"
    return Item(f"What number makes this true? {eq}", 10 - a - b, [f"{a} + {b} = {a + b}.", f"{a + b} + {10 - a - b} = 10."],
                [W(10 - a, "left out an addend"), W(10 - b, "left out an addend"), W(a + b, "wrote the sum of the two numbers"), W(11 - a - b, "made a counting mistake")],
                FN("blank_eq", eq=eq), qtype="multi-step", tags={"multistep"})


@fam("012")
def mt_from10(r, L):
    a = r.randint(5, 9) if L == 0 else r.randint(1, 9)
    return Item(pick(r, [f"What is 10 − {a}?", f"Take {a} away from 10. How many are left?"]), 10 - a,
                [f"Think: {a} + ___ = 10.", f"{a} + {10 - a} = 10, so 10 − {a} = {10 - a}."], sub_w(10, a), EX(f"10-{a}"), claim=f"10 − {a}")


@fam("01")
def mt_full(r, L):
    a = r.randint(2, 8)
    alt = f"A full ten frame with {a} red counters and {10 - a} yellow counters."
    return Item("The ten frame is full. How many yellow counters are there?", 10 - a, [f"There are {a} red counters and 10 in all.", f"{a} + {10 - a} = 10."],
                [W(a, "counted the red counters"), W(10, "counted all the counters"), W(9 - a, "counted one too few"), W(11 - a, "counted one too many")],
                FN("blank_eq", eq=f"{a} + ___ = 10"), qtype="visual", diagram=Diagram("tenframe", {"frames": 1, "a": a, "b": 10 - a}, alt))


# ============================================================== S4 Number Partners within 10
@fam("012")
def np_missing(r, L):
    w = r.randint(3, 6) if L == 0 else r.randint(5, 10)
    a = r.randint(1, w - 1)
    eq = f"{a} + ___ = {w}" if L < 2 else pick(r, [f"{w} = {a} + ___", f"___ + {a} = {w}", f"{w} − ___ = {a}"])
    return Item(pick(r, [f"What is the missing number? {eq}", f"Find the number that makes it true: {eq}"]), w - a,
                [f"Think: {a} and what make {w}?", f"{a} + {w - a} = {w}."],
                [W(w + a, "added the numbers"), W(w, "copied the total"), W(w - a + 1, "counted one too many"), W(a, "copied the part")],
                FN("blank_eq", eq=eq), claim=eq)


@fam("012")
def np_hide(r, L):
    w = r.randint(3, 6) if L == 0 else r.randint(5, 10)
    a = r.randint(1, w - 1)
    th = thing(r)
    return Item(f"There are {w} {th[1]}. Some are under a cup. You can see {a}. How many {th[1]} are under the cup?",
                f"{w - a} {th[1]}", [f"{a} + ___ = {w}.", f"{a} + {w - a} = {w}, so {w - a} are under the cup."],
                [W(f"{w + a} {th[1]}", "added the numbers"), W(f"{a} {th[1]}", "counted the ones you can see"), W(f"{w} {th[1]}", "gave the total"),
                 W(f"{w - a + 1} {th[1]}", "counted one too many")], EX(f"{w}-{a}", unit=th[1]), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def np_bond(r, L):
    w = r.randint(4, 6) if L == 0 else r.randint(6, 10)
    a = r.randint(1, w - 1)
    good = f"{a} and {w - a}"
    bad = []
    for d in (1, -1, 2):
        b = w - a + d
        if b >= 0:
            bad.append(f"{a} and {b}")
    need(len(bad) == 3)
    it = mc_key(pick(r, [f"Which two parts make {w}?", f"{w} can be broken into which two parts?"]), good, bad, ["Add the two parts.", f"{a} + {w - a} = {w}."], qtype="procedural", r=r)
    it.check = FN("pair_ten", total=w)
    return it


@fam("012")
def np_unknown_add(r, L):
    w = r.randint(4, 6) if L == 0 else r.randint(5, 10)
    p = r.randint(2, w - 1)
    return Item(f"To find {w} − {p}, {name(r)} thinks: {p} + what makes {w}? What is {w} − {p}?", w - p,
                [f"{p} + {w - p} = {w}.", f"So {w} − {p} = {w - p}."], sub_w(w, p), EX(f"{w}-{p}"), qtype="compare-strategies", tags={"connections"})


@fam("01")
def np_frame_parts(r, L):
    w = r.randint(4, 7) if L == 0 else r.randint(6, 10)
    a = r.randint(1, w - 1)
    alt = f"Ten frame with {a} red counters and {w - a} yellow counters."
    return Item(f"The ten frame shows {w}. How many yellow counters are there?", w - a,
                [f"There are {a} red counters.", f"{a} + {w - a} = {w}."],
                [W(a, "counted the red counters"), W(w, "counted all the counters"), W(10 - w, "counted the empty boxes"), W(w - a + 1, "counted one too many")],
                FN("blank_eq", eq=f"{a} + ___ = {w}"), qtype="visual", diagram=Diagram("tenframe", {"frames": 1, "a": a, "b": w - a}, alt))


@fam("2", mode="mc")
def np_all_ways(r, L):
    w = r.randint(5, 9)
    a = r.randint(0, w)
    good = f"{a} + {w - a} = {w}"
    bad = [f"{a} + {w - a + 1} = {w}", f"{w} + {a} = {w}" if a else f"{w} + 1 = {w}", f"{max(a - 1, 0)} + {w - a} = {w}" if a else f"{w - 2} + 1 = {w}"]
    it = mc_key(f"Which equation shows a true way to make {w}?", good, bad, ["Check that the two parts add to the total.", f"{a} + {w - a} = {w} is true."], qtype="conceptual", r=r)
    it.check = FN("true_eq")
    return it


SKILLS = {
    1: dict(name="Adding within 10", fams=[ad_fact, ad_frame, ad_word, ad_groups, ad_which_sum, ad_line, ad_zero_one]),
    2: dict(name="Subtracting within 10", fams=[sb_fact, sb_cross, sb_frame, sb_word, sb_think_add, sb_line, sb_which]),
    3: dict(name="Making Ten", fams=[mt_partner, mt_frame, mt_pair, mt_word, mt_three, mt_from10, mt_full]),
    4: dict(name="Number Partners within 10", fams=[np_missing, np_hide, np_bond, np_unknown_add, np_frame_parts, np_all_ways]),
}
