"""Unit 3: Addition and Subtraction within 20 (add-subtract-20). 1.OA.C.6, 1.OA.B.3, 1.OA.B.4."""
from g1lib import *

UNIT_ID = "add-subtract-20"


def pair20(r, L):
    """L0: 10 + a, 9 + a or a double; L1: one-digit addends crossing ten (sum 11-15); L2: sums 13-18."""
    if L == 0:
        k = pick(r, ["ten", "nine", "double"])
        if k == "ten":
            a, b = 10, r.randint(1, 9)
        elif k == "nine":
            a, b = 9, r.randint(2, 9)
        else:
            a = r.randint(2, 9)
            b = a
        if r.random() < 0.5:
            a, b = b, a
        return a, b
    if L == 1:
        a, b = r.randint(3, 9), r.randint(3, 9)
        need(11 <= a + b <= 15)
    else:
        a, b = r.randint(5, 9), r.randint(5, 9)
        need(13 <= a + b <= 18)
    return a, b


def add_w(a, b, u=""):
    s = a + b
    u = (" " + u) if u else ""
    out = [W(f"{s - 1}{u}", "counted on and included the first number"), W(f"{s + 1}{u}", "counted one too many"),
           W(f"{abs(a - b)}{u}", "subtracted instead of adding"), W(f"{s - 10}{u}" if s > 10 else f"{s + 10}{u}", "lost the ten"),
           W(f"{s + 2}{u}", "made a counting mistake")]
    return out


def sub_w(w, p, u=""):
    d = w - p
    u = (" " + u) if u else ""
    out = [W(f"{d + 1}{u}", "counted back and included the starting number"), W(f"{w + p}{u}", "added instead of subtracting")]
    if w > 10 and w % 10 < p % 10 and p < 10:
        out.append(W(f"{10 + (p - w % 10)}{u}", "subtracted the smaller ones digit from the larger one"))
    out += [W(f"{d - 1}{u}", "counted back one too many"), W(f"{d + 10}{u}" if d + 10 <= 20 else f"{p}{u}", "forgot to go back past ten" if d + 10 <= 20 else "gave the number taken away")]
    return out


# ============================================================== S1 Adding within 20 with Strategies
@fam("012")
def a_fact(r, L):
    a, b = pair20(r, L)
    return Item(pick(r, [f"What is {a} + {b}?", f"Add: {a} + {b} = ___", f"Find the sum: {a} + {b}"]), a + b,
                [("Make a ten, use a double, or count on." if a != 10 and b != 10 else "10 and some ones is a teen number."), f"{a} + {b} = {a + b}."],
                add_w(a, b), EX(f"{a}+{b}"), claim=f"{a} + {b}")


@fam("12")
def a_make10(r, L):
    a, b = pair20(r, L)
    a, b = max(a, b), min(a, b)
    need(a >= 7 and a + b > 10 and a < 10)
    k = 10 - a
    eq = f"{a} + {b} = 10 + ___"
    return Item(f"Make a ten. {a} + {k} = 10. So {eq}", b - k, [f"Break {b} into {k} and {b - k}.", f"10 + {b - k} = {a + b}, so the missing number is {b - k}."],
                [W(b, "did not break apart the second number"), W(k, "wrote the part that makes ten"), W(a + b, "wrote the whole sum"), W(b - k + 1, "made a counting mistake")],
                FN("blank_eq", eq=eq), qtype="compare-strategies", tags={"connections"})


@fam("012")
def a_double(r, L):
    a = r.randint(2, 6) if L == 0 else r.randint(5, 9)
    d = 0 if L == 0 else 1 if L == 1 else pick(r, [1, -1])
    if L == 0:
        return Item(pick(r, [f"Double {a}. What is {a} + {a}?", f"What is the double {a} + {a}?"]), 2 * a, ["A double adds a number to itself.", f"{a} + {a} = {2 * a}."],
                    [W(2 * a - 1, "counted one too few"), W(2 * a + 1, "counted one too many"), W(a, "did not double"), W(a + 1, "added 1 instead")], EX(f"{a}+{a}"), claim=f"{a} + {a}")
    b = a + d
    need(1 <= b <= 9)
    return Item(f"Use the double {a} + {a} = {2 * a} to find {a} + {b}.", a + b,
                [f"{a} + {b} is {abs(d)} {'more' if d > 0 else 'less'} than {a} + {a}.", f"{2 * a} {'+' if d > 0 else '−'} 1 = {a + b}."],
                [W(2 * a, "used only the double"), W(2 * a - d, "went the wrong way from the double"), W(2 * b, "doubled the other number"), W(a + b + 2, "made a counting mistake")],
                EX(f"{a}+{b}"), qtype="compare-strategies", tags={"connections"})


@fam("012")
def a_frames(r, L):
    a, b = pair20(r, L)
    need(a + b <= 20)
    alt = f"Two ten frames with {a} red counters and {b} yellow counters."
    return Item(pick(r, ["How many counters are in the two ten frames?", "Red and yellow counters fill the ten frames. How many in all?",
                         "Find the total number of counters."]), a + b, [f"{a} red and {b} yellow. Fill the first ten frame, then count the rest.", f"{a} + {b} = {a + b}."],
                add_w(a, b), EX(f"{a}+{b}"), qtype="visual", diagram=Diagram("tenframe", {"frames": 2, "a": a, "b": b}, alt))


@fam("012")
def a_word(r, L):
    a, b = pair20(r, L)
    th, nm = thing(r), name(r)
    t = pick(r, [f"{nm} has {a} {th[1]}. {nm} finds {b} more. How many {th[1]} does {nm} have now?",
                 f"There are {a} {th[1]} in one box and {b} {th[1]} in another box. How many {th[1]} are there in all?",
                 f"{nm} picks {a} {th[1]} and then {b} more. How many {th[1]} did {nm} pick?"])
    return Item(t, f"{a + b} {th[1]}", [f"Add {a} and {b}.", f"{a} + {b} = {a + b} {th[1]}."], add_w(a, b, th[1]), EX(f"{a}+{b}", unit=th[1]),
                qtype="word-problem", tags={"modeling"})


@fam("2", mode="mc")
def a_same(r, L):
    a, b = pair20(r, 2)
    need(a != b)
    good = f"10 + {a + b - 10}"
    bad = [f"10 + {a + b - 9}", f"10 + {b}", f"10 + {a + b - 11}"]
    need(len(set(bad + [good])) == 4)
    it = mc_key(f"Which has the same sum as {a} + {b}?", good, bad, [f"{a} + {b} = {a + b}.", f"{good} = {a + b} too."], qtype="compare-strategies", r=r)
    it.check = FN("same_value", target=f"{a}+{b}")
    return it


@fam("01")
def a_ten_plus(r, L):
    o = r.randint(1, 9)
    return Item(pick(r, [f"What is 10 + {o}?", f"What is {o} + 10?", f"1 ten and {o} ones make what number?"]), 10 + o,
                [f"10 and {o} more is 1{o}.", f"The answer is {10 + o}."],
                [W(o, "left out the ten"), W(10 * o + 1 if o > 1 else 21, "switched the tens and ones"), W(11 + o, "counted one too many"), W(9 + o, "counted one too few")],
                EX(f"10+{o}"), claim=f"10 + {o}")


# ============================================================== S2 Subtracting within 20 with Strategies
def spair20(r, L):
    if L == 0:
        w = r.randint(11, 19)
        p = pick(r, [w - 10, 10, r.randint(1, w % 10)]) if w % 10 else 10
        need(1 <= p < w)
    elif L == 1:
        w = r.randint(11, 16)
        p = r.randint(3, 9)
        need(w % 10 < p)
    else:
        w = r.randint(13, 18)
        p = r.randint(5, 9)
        need(w % 10 < p)
    return w, p


@fam("012")
def s_fact(r, L):
    w, p = spair20(r, L)
    return Item(pick(r, [f"What is {w} − {p}?", f"Subtract: {w} − {p} = ___", f"Find the difference: {w} − {p}"]), w - p,
                ["Go back to 10 first, or think addition." if L else "Take away the ones or the ten.", f"{w} − {p} = {w - p}."],
                sub_w(w, p), EX(f"{w}-{p}"), claim=f"{w} − {p}")


@fam("12")
def s_back10(r, L):
    w, p = spair20(r, L)
    o = w - 10
    need(o < p)
    return Item(f"Go back to 10. {w} − {o} = 10. Then take away {p - o} more. What is {w} − {p}?", w - p,
                [f"{p} is {o} and {p - o}.", f"{w} − {o} = 10 and 10 − {p - o} = {w - p}."], sub_w(w, p), EX(f"{w}-{p}"),
                qtype="compare-strategies", tags={"connections"})


@fam("012")
def s_think(r, L):
    w, p = spair20(r, L)
    eq = f"{p} + ___ = {w}"
    return Item(f"Think addition. {eq}. So {w} − {p} = ___. What is the missing number?", w - p,
                [f"{p} + {w - p} = {w}.", f"So {w} − {p} = {w - p}."], sub_w(w, p), FN("blank_eq", eq=eq), qtype="compare-strategies", tags={"connections"})


@fam("012")
def s_word(r, L):
    w, p = spair20(r, L)
    th, nm = thing(r), name(r)
    t = pick(r, [f"{nm} has {w} {th[1]}. {nm} gives away {p}. How many {th[1]} are left?",
                 f"There are {w} {th[1]}. {p} of them are taken away. How many {th[1]} are left?",
                 f"{w} {th[1]} are in a bag. {nm} takes out {p}. How many {th[1]} are still in the bag?"])
    return Item(t, f"{w - p} {th[1]}", [f"Subtract {p} from {w}.", f"{w} − {p} = {w - p} {th[1]}."], sub_w(w, p, th[1]), EX(f"{w}-{p}", unit=th[1]),
                qtype="word-problem", tags={"modeling"})


@fam("01")
def s_line(r, L):
    w, p = spair20(r, L)
    alt = "Number line from 0 to 20."
    return Item(f"Use the number line. Start at {w}. Jump back {p}. Where is the end point?", w - p,
                [f"Jump back {w - 10} to get to 10, then the rest." if w - 10 < p else f"Jump back {p} from {w}.", f"{w} − {p} = {w - p}."],
                sub_w(w, p), EX(f"{w}-{p}"), qtype="visual", diagram=Diagram("jline", {"lo": 0, "hi": 20}, alt))


@fam("012")
def s_frames(r, L):
    w, p = spair20(r, L)
    alt = f"Two ten frames with {w} counters. {p} counters are crossed out."
    return Item(pick(r, ["How many counters are not crossed out?", "Some counters are crossed out. How many are left?"]), w - p,
                [f"{w} counters and {p} are crossed out.", f"{w} − {p} = {w - p}."], sub_w(w, p), EX(f"{w}-{p}"), qtype="visual",
                diagram=Diagram("tenframe", {"frames": 2, "a": w, "x": p}, alt))


# ============================================================== S3 Adding in Any Order and Adding Three Numbers
@fam("012")
def o_turn(r, L):
    a, b = pair20(r, max(L, 1))
    need(a != b)
    eq = f"{a} + {b} = {b} + ___" if L < 2 else f"{a} + ___ = {b} + {a}"
    return Item(pick(r, [f"What number makes this true? {eq}", f"{a} + {b} = {a + b}. Fill in the blank: {eq}"]), a if L < 2 else b,
                ["Changing the order of the addends does not change the sum.", f"{a} + {b} = {b} + {a}."],
                [W(a + b, "wrote the sum"), W(b if L < 2 else a, "copied the wrong addend"), W((a if L < 2 else b) + 1, "made a counting mistake"), W(abs(a - b), "subtracted")],
                FN("blank_eq", eq=eq), qtype="conceptual", tags={"reasoning"})


def trio(r, L):
    a, b, c = r.randint(1, 9), r.randint(1, 9), r.randint(1, 9)
    if L == 0:
        need(a + b == 10 and a + b + c <= 15)
    elif L == 1:
        need((a + b == 10 or b + c == 10 or a + c == 10) and a + b + c <= 18 and a + b != 10)
    else:
        need(12 <= a + b + c <= 20 and a + b != 10 and b + c != 10)
    return a, b, c


@fam("012")
def o_three(r, L):
    a, b, c = trio(r, L)
    return Item(pick(r, [f"Add: {a} + {b} + {c}", f"What is {a} + {b} + {c}?", f"Find the sum of {a}, {b}, and {c}."]), a + b + c,
                ["Look for two numbers that make 10. Add them first.", f"{a} + {b} + {c} = {a + b + c}."],
                [W(a + b, "left out an addend"), W(b + c, "left out an addend"), W(a + b + c - 1, "made a counting mistake"), W(a + b + c + 1, "made a counting mistake")],
                EX(f"{a}+{b}+{c}"), claim=f"{a} + {b} + {c}")


@fam("012", mode="mc")
def o_ten_first(r, L):
    a, b, c = trio(r, min(L, 1))
    pairs = [(a, b), (b, c), (a, c)]
    good = [f"{x} + {y}" for x, y in pairs if x + y == 10]
    need(len(good) == 1)
    bad = [f"{x} + {y}" for x, y in pairs if x + y != 10]
    bad.append(f"{max(a, b, c)} + {max(a, b, c)}")
    need(len(set(bad)) == 3 and good[0] not in bad)
    it = mc_key(f"To add {a} + {b} + {c}, which two numbers make a ten?", good[0], bad, ["Look for a pair that adds to 10.", f"{good[0]} = 10."],
                qtype="compare-strategies", tags={"connections"}, r=r)
    it.check = FN("same_value", target="10")
    return it


@fam("012", mode="mc")
def o_same(r, L):
    a, b = pair20(r, L)
    need(a != b)
    good = f"{b} + {a}"
    bad = [f"{b} − {a}" if b > a else f"{a} − {b}", f"{a} + {b + 1}", f"{b} + {a - 1}"]
    it = mc_key(pick(r, [f"Which has the same sum as {a} + {b}?", f"Which is equal to {a} + {b}?"]), good, bad,
                ["Changing the order of the addends does not change the sum.", f"{a} + {b} = {b} + {a} = {a + b}."], qtype="conceptual", r=r)
    it.check = FN("same_value", target=f"{a}+{b}")
    return it


@fam("01", mode="mc")
def o_same_story(r, L):
    a, b = pair20(r, 1)
    need(a != b)
    n1, n2 = r.sample(NAMES, 2)
    th = thing(r)
    good = "They have the same number."
    it = mc_key(f"{n1} has {a} red {th[1]} and {b} blue {th[1]}. {n2} has {b} red {th[1]} and {a} blue {th[1]}. Who has more {th[1]}?",
                good, [f"{n1} has more.", f"{n2} has more.", f"{n1} has {abs(a - b)} more."],
                [f"{n1}: {a} + {b} = {a + b}. {n2}: {b} + {a} = {a + b}.", "Changing the order does not change the sum, so they have the same number."],
                qtype="conceptual", tags={"reasoning"}, r=r, why="thinking the order of addends changes the total")
    return it


@fam("012")
def o_regroup(r, L):
    a, b, c = r.randint(2, 8), r.randint(2, 8), r.randint(2, 8)
    need(b + c == 10 and a + b + c <= 20 and a != b)
    eq = f"{a} + {b} + {c} = {a} + ___"
    return Item(f"Add the last two numbers first. What number makes this true? {eq}", 10, [f"{b} + {c} = 10.", f"So {a} + {b} + {c} = {a} + 10 = {a + 10}."],
                [W(a + b + c, "wrote the whole sum"), W(b, "copied an addend"), W(a + b, "added the first two"), W(c, "copied an addend")],
                FN("blank_eq", eq=eq), qtype="conceptual", tags={"reasoning"})


# ============================================================== S4 Related Facts and Fact Families
@fam("012")
def f_related(r, L):
    a, b = pair20(r, max(L, 1)) if L else (r.randint(2, 9), r.randint(2, 9))
    s = a + b
    need(s <= 18)
    p = pick(r, [a, b])
    return Item(pick(r, [f"{a} + {b} = {s}. What is {s} − {p}?", f"Use {a} + {b} = {s} to find {s} − {p}."]), s - p,
                [f"{s} is made of {a} and {b}.", f"{s} − {p} = {s - p}."], sub_w(s, p), EX(f"{s}-{p}"), qtype="compare-strategies", tags={"connections"})


@fam("012", mode="mc")
def f_member(r, L):
    a, b = pair20(r, max(L, 1))
    need(a != b)
    s = a + b
    good = f"{s} − {a} = {b}"
    bad = [f"{a} − {s} = {b}", f"{s} − {a} = {b + 1}", f"{b} − {a} = {s}" if b > a else f"{a} − {b} = {s}"]
    it = mc_key(pick(r, [f"Which subtraction fact uses the same numbers as {a} + {b} = {s}?", f"{a} + {b} = {s}. Which subtraction fact is in the same family?"]), good, bad,
                [f"In subtraction, start with the whole, {s}.", f"{good} is true."], qtype="conceptual", r=r)
    it.check = FN("fam_member", nums=[a, b, s])
    return it


@fam("012")
def f_unknown_add(r, L):
    w, p = spair20(r, L)
    return Item(pick(r, [f"Find {w} − {p}. Use the missing addend in {p} + ___ = {w}.", f"What number makes {p} + ___ = {w} true? Use it to find {w} − {p}."]), w - p, [f"Count on from {p} to {w}.", f"{p} + {w - p} = {w}, so {w} − {p} = {w - p}."],
                sub_w(w, p), FN("blank_eq", eq=f"{p} + ___ = {w}"), qtype="compare-strategies", tags={"connections"})


@fam("12")
def f_bar(r, L):
    a, b = pair20(r, L)
    s = a + b
    alt = f"A bar for {s} split into two parts. One part is {a}. The other part is unknown."
    return Item(f"The whole bar is {s}. One part is {a}. What is the other part?", b, [f"{a} + ___ = {s}.", f"{s} − {a} = {b}."],
                [W(s + a, "added the whole and the part"), W(a, "copied the part"), W(s, "copied the whole"), W(b + 1, "counted one too many")],
                FN("blank_eq", eq=f"{a} + ___ = {s}"), qtype="visual",
                diagram=Diagram("bars", {"rows": [{"label": "", "parts": [[s, str(s)]]}, {"label": "", "parts": [[a, str(a)], [b, "?"]]}]}, alt))


@fam("12", mode="mc")
def f_not(r, L):
    a, b = pair20(r, L)
    need(a != b)
    s = a + b
    facts = [f"{a} + {b} = {s}", f"{b} + {a} = {s}", f"{s} − {a} = {b}", f"{s} − {b} = {a}"]
    good = pick(r, [f"{a} − {b} = {s}" if a > b else f"{b} − {a} = {s}", f"{s} + {a} = {b}"])
    bad = r.sample(facts, 3)
    it = mc_key(f"Which is NOT a fact in the family of {a}, {b}, and {s}?", good, bad, ["Check each fact. The whole is the biggest number.", f"{good} is not true."],
                qtype="conceptual", tags={"misconception"}, r=r)
    it.check = FN("false_eq")
    return it


@fam("0")
def f_small(r, L):
    a, b = r.randint(2, 5), r.randint(2, 5)
    need(a != b)
    s = a + b
    return Item(f"{a} + {b} = {s}. What is {s} − {a}?", b, [f"{s} is {a} and {b}.", f"{s} − {a} = {b}."], sub_w(s, a), EX(f"{s}-{a}"),
                qtype="compare-strategies", tags={"connections"})


@fam("01")
def f_frame(r, L):
    a, b = r.randint(2, 7), r.randint(2, 7)
    need(a + b <= 10 if L == 0 else 10 < a + b <= 14)
    s = a + b
    p = pick(r, [a, b])
    alt = f"{'Ten frame' if s <= 10 else 'Two ten frames'} with {a} red counters and {b} yellow counters."
    return Item(f"The picture shows {a} + {b} = {s}. What is {s} − {p}?", s - p, [f"Take away the {p} {'red' if p == a else 'yellow'} counters.", f"{s} − {p} = {s - p}."],
                sub_w(s, p), EX(f"{s}-{p}"), qtype="visual", diagram=Diagram("tenframe", {"frames": 1 if s <= 10 else 2, "a": a, "b": b}, alt))


SKILLS = {
    1: dict(name="Adding within 20 with Strategies", fams=[a_fact, a_make10, a_double, a_frames, a_word, a_same, a_ten_plus]),
    2: dict(name="Subtracting within 20 with Strategies", fams=[s_fact, s_back10, s_think, s_word, s_line, s_frames]),
    3: dict(name="Adding in Any Order and Adding Three Numbers", fams=[o_turn, o_three, o_ten_first, o_same, o_regroup, o_same_story]),
    4: dict(name="Related Facts and Fact Families", fams=[f_related, f_member, f_unknown_add, f_bar, f_not, f_small, f_frame]),
}
