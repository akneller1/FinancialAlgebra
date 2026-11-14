"""Unit 4: The Equal Sign and Missing Numbers (equal-sign). 1.OA.D.7, 1.OA.D.8."""
from g1lib import *
import re

UNIT_ID = "equal-sign"


def val(e):
    return eval(e.replace("−", "-"))


def side_text(e):
    return e


def tf_options(r, lhs, rhs):
    a, b = val(lhs), val(rhs)
    ok = a == b
    good = f"True. Both sides are {a}." if ok else f"False. One side is {a} and the other side is {b}."
    bad = []
    if ok:
        bad = [f"False. One side is {a} and the other side is {a + 1}.", f"False. The answer must come after the equal sign.", f"True. Both sides are {a + 1}."]
    else:
        bad = [f"True. Both sides are {a}.", f"True. Both sides are {b}.", f"False. One side is {a} and the other side is {b + 1}."]
    return good, bad


# ============================================================== S1 True or False Equations
def eq_pick(r, L, kind):
    hi = 10 if L == 0 else 20
    a, b = r.randint(1, hi // 2 + 2), r.randint(1, hi // 2)
    need(a + b <= hi)
    s = a + b
    off = pick(r, [0, 0, 1, -1, 2])
    if kind == "sum":
        return f"{a} + {b}", str(s + off)
    if kind == "rev":
        return str(s + off), f"{a} + {b}"
    if kind == "same":
        return str(s), str(s + pick(r, [0, 0, 1]))
    if kind == "sub":
        return f"{s} − {b}", str(a + off)
    if kind == "both":
        c = r.randint(1, s - 1)
        return f"{a} + {b}", f"{c} + {s - c + off}"
    need(s < hi)
    c = r.randint(1, min(9, hi - s))
    return f"{a} + {b}", f"{s + c} − {c - off}" if c - off > 0 else f"{s + c} − {c}"


@fam("012", mode="mc")
def t_mc(r, L):
    kind = pick(r, ["sum", "rev", "same", "sub"] if L == 0 else ["sum", "rev", "sub", "both"] if L == 1 else ["rev", "both", "mix", "sub"])
    lhs, rhs = eq_pick(r, L, kind)
    need(val(rhs) >= 0)
    good, bad = tf_options(r, lhs, rhs)
    eq = f"{lhs} = {rhs}"
    it = mc_key(pick(r, [f"Is this equation true or false? {eq}", f"True or false? {eq}", f"Look at both sides. Is {eq} true?"]), good, bad,
                [f"Find the amount on each side: {lhs} is {val(lhs)} and {rhs} is {val(rhs)}.", good], qtype="reasoning", tags={"reasoning"}, r=r)
    it.check = FN("eq_tf", eq=eq)
    return it


@fam("012", mode="sa")
def t_word(r, L):
    kind = pick(r, ["sum", "rev", "same"] if L == 0 else ["rev", "sub", "both"] if L == 1 else ["both", "mix"])
    lhs, rhs = eq_pick(r, L, kind)
    need(val(rhs) >= 0)
    eq = f"{lhs} = {rhs}"
    ok = val(lhs) == val(rhs)
    return Item(f"Write true or false: {eq}", "true" if ok else "false", [f"{lhs} is {val(lhs)} and {rhs} is {val(rhs)}.", f"The sides are {'the same' if ok else 'not the same'}, so it is {'true' if ok else 'false'}."],
                [W("false" if ok else "true", "thought the equal sign means the answer comes next" if ok and kind in ("rev", "same") else "did not find both sides")],
                FN("eq_word", eq=eq), qtype="reasoning", tags={"reasoning"})


@fam("012", mode="mc")
def t_which_true(r, L):
    hi = 10 if L == 0 else 20
    a, b = r.randint(1, hi // 2), r.randint(1, hi // 2)
    s = a + b
    forms = [(f"{s} = {a} + {b}", True), (f"{a} + {b} = {s + 1}", False), (f"{s} = {a} + {b + 1}", False), (f"{a} + {b} = {b} + {a + 1}", False)]
    if L >= 1:
        c = r.randint(1, s - 1)
        forms = [(f"{a} + {b} = {c} + {s - c}", True), (f"{a} + {b} = {c} + {s - c + 1}", False), (f"{s} = {a} + {b + 2}", False), (f"{a} + {b} = {s} + {c}", False)]
    if L == 2:
        forms = [(f"{s} − {b} = {a}", True)] + [x for x in forms if not x[1]]
    good = forms[0][0]
    bad = [f for f, _ in forms[1:]]
    need(len(set(bad)) == 3)
    it = mc_key(pick(r, ["Which equation is true?", "Which one is a true equation?"]), good, bad, ["Find the amount on each side.", f"{good} has the same amount on both sides."], qtype="reasoning", r=r)
    it.check = FN("true_eq")
    return it


@fam("12", mode="mc")
def t_which_false(r, L):
    a, b = r.randint(2, 9), r.randint(2, 9)
    s = a + b
    c = r.randint(1, s - 1)
    trues = [f"{s} = {a} + {b}", f"{b} + {a} = {s}", f"{a} + {b} = {c} + {s - c}", f"{s} − {a} = {b}", f"{s} = {s}"]
    good = pick(r, [f"{a} + {b} = {s} + {a}", f"{s} − {a} = {a}" if a != b else f"{s} = {s - 1} + {a}", f"{a} + {b} = {c} + {s - c + 2}"])
    need(val(good.split("=")[0]) != val(good.split("=")[1]))
    it = mc_key("Which equation is false?", good, r.sample(trues, 3), ["Find the amount on each side.", f"The sides of {good} are not the same."], qtype="reasoning", r=r)
    it.check = FN("false_eq")
    return it


@fam("012")
def t_side(r, L):
    a, b = r.randint(1, 5 if L == 0 else 9), r.randint(1, 5 if L == 0 else 9)
    s = a + b
    c = r.randint(1, s - 1)
    eq = f"{a} + {b} = {c} + {s - c}" if L else f"{s} = {a} + {b}"
    side = f"{c} + {s - c}" if L else f"{a} + {b}"
    return Item(f"{eq} is true. How much is on each side?", s, [f"{side} = {s}.", f"Each side is {s}."],
                [W(s + 1, "made a counting mistake"), W(c if L else a, "gave one number"), W(2 * s, "added both sides"), W(s - 1, "made a counting mistake")],
                EX(side.replace("−", "-")), qtype="reasoning", tags={"reasoning"})


@fam("012", mode="sa")
def t_pic(r, L):
    hi = 10 if L == 0 else 20
    a, b = r.randint(1, hi // 2), r.randint(1, hi // 2)
    s = a + b
    c = r.randint(1, s - 1)
    d = s - c + pick(r, [0, 0, 1, -1])
    need(d > 0 and c != a)
    eq = f"{a} + {b} = {c} + {d}"
    ok = a + b == c + d
    alt = f"Two bars. The top bar has parts {a} and {b}. The bottom bar has parts {c} and {d}."
    return Item(f"The bars show {eq}. Write true or false.", "true" if ok else "false",
                [f"Top: {a} + {b} = {s}. Bottom: {c} + {d} = {c + d}.", f"The bars are {'the same' if ok else 'not the same'} length, so it is {'true' if ok else 'false'}."],
                [W("false" if ok else "true", "did not compare both sides")], FN("eq_word", eq=eq), qtype="visual", tags={"reasoning"},
                diagram=Diagram("bars", {"rows": [{"label": "", "parts": [[a, str(a)], [b, str(b)]]}, {"label": "", "parts": [[c, str(c)], [d, str(d)]]}]}, alt))


# ============================================================== S2 Finding the Missing Number
def mn_eq(r, L):
    hi = 10 if L == 0 else 20
    a, b = r.randint(1, hi - 2), r.randint(1, hi - 2)
    need(a + b <= hi and (L == 0 or a + b > 8))
    s = a + b
    forms = ([f"{a} + ___ = {s}", f"{s} − {a} = ___", f"___ = {a} + {b}"] if L == 0 else
             [f"{a} + ___ = {s}", f"___ + {b} = {s}", f"{s} − ___ = {b}", f"{s} = {a} + ___"] if L == 1 else
             [f"___ − {a} = {b}", f"{s} = ___ + {b}", f"{b} = {s} − ___", f"___ − {b} = {a}"])
    eq = pick(r, forms)
    for x in range(0, 21):
        if eval(eq.replace("___", str(x)).replace("−", "-").replace("=", "==")):
            return eq, x, (a, b, s)
    raise Reject()


def mn_wrongs(x, a, b, s, eq):
    nums = [int(t) for t in re.findall(r"\d+", eq)]
    out = [W(sum(nums), "added all the numbers shown"), W(x + 1, "counted one too many"), W(x - 1, "counted one too few") if x > 0 else W(x + 2, "made a counting mistake")]
    out += [W(n, "copied a number from the equation") for n in nums if n != x][:2]
    return out


@fam("012")
def m_blank(r, L):
    eq, x, (a, b, s) = mn_eq(r, L)
    return Item(pick(r, [f"What number makes this true? {eq}", f"Find the missing number: {eq}", f"Fill in the blank: {eq}"]), x,
                [f"Ask: what number makes both sides the same?", f"{eq.replace('___', str(x))} is true."], mn_wrongs(x, a, b, s, eq), FN("blank_eq", eq=eq), claim=eq)


@fam("012", mode="mc")
def m_mc(r, L):
    eq, x, (a, b, s) = mn_eq(r, L)
    return Item(pick(r, [f"Which number makes {eq} true?", f"Choose the missing number: {eq}"]), x, [f"Try each number in the blank.", f"{eq.replace('___', str(x))} is true."],
                mn_wrongs(x, a, b, s, eq), FN("blank_eq", eq=eq))


@fam("012")
def m_think(r, L):
    hi = 10 if L == 0 else 20
    a, k = r.randint(2 if L < 2 else 6, hi - 3), r.randint(2, 9)
    need(a + k <= hi)
    t = pick(r, ["add", "sub"] if L < 2 else ["sub", "start"])
    if t == "add":
        p, ans, eq = f"My secret number plus {k} is {a + k}. What is my secret number?", a, f"___ + {k} = {a + k}"
    elif t == "sub":
        p, ans, eq = f"I start with {a + k}. I take away a number and get {a}. What number did I take away?", k, f"{a + k} − ___ = {a}"
    else:
        p, ans, eq = f"My secret number minus {k} is {a}. What is my secret number?", a + k, f"___ − {k} = {a}"
    return Item(p, ans, [f"Write it as {eq}.", f"{eq.replace('___', str(ans))} is true, so the number is {ans}."],
                ([W(a + 2 * k, "added instead of subtracting"), W(a + k, "copied the total")] if t == "add" else
                 [W(2 * a + k, "added instead of subtracting"), W(a, "copied the number left")] if t == "sub" else
                 [W(abs(a - k), "subtracted instead of adding"), W(a, "copied the number left")]) + [W(ans + 1, "counted one too many"), W(ans - 1, "counted one too few")],
                FN("blank_eq", eq=eq), qtype="word-problem", tags={"reasoning"})


@fam("01")
def m_bars(r, L):
    hi = 10 if L == 0 else 20
    a, b = r.randint(1, hi - 2), r.randint(1, hi - 2)
    need(a + b <= hi)
    s = a + b
    alt = f"A bar for {s} split into {a} and an unknown part."
    eq = f"{a} + ___ = {s}"
    return Item(f"The bar shows {eq}. What is the missing part?", b, [f"{a} and what make {s}?", f"{a} + {b} = {s}."],
                [W(s + a, "added the whole and the part"), W(a, "copied the part"), W(s, "copied the whole"), W(b + 1, "counted one too many")],
                FN("blank_eq", eq=eq), qtype="visual",
                diagram=Diagram("bars", {"rows": [{"label": "", "parts": [[s, str(s)]]}, {"label": "", "parts": [[a, str(a)], [b, "?"]]}]}, alt))


@fam("012")
def m_frame(r, L):
    s = r.randint(4, 10) if L == 0 else r.randint(11, 20)
    a = r.randint(1, s - 1)
    need(L < 2 or a > 10)
    alt = f"{'Ten frame' if s <= 10 else 'Two ten frames'} with {a} counters."
    eq = f"{a} + ___ = {s}"
    return Item(f"The picture shows {a} counters. How many more make {s}? {eq}", s - a, [f"Count on from {a} to {s}.", f"{a} + {s - a} = {s}."],
                [W(s + a, "added the numbers"), W(a, "counted the counters shown"), W(s, "copied the total"), W(s - a + 1, "counted one too many")],
                FN("blank_eq", eq=eq), qtype="visual", diagram=Diagram("tenframe", {"frames": 1 if s <= 10 else 2, "a": a}, alt))


@fam("12", mode="mc")
def m_which_eq(r, L):
    a, b = r.randint(3, 9), r.randint(3, 9)
    s = a + b
    th, nm = thing(r), name(r)
    good = f"{a} + ___ = {s}"
    bad = [f"{a} + {s} = ___", f"___ − {a} = {s}", f"{s} + ___ = {a}"]
    it = mc_key(f"{nm} has {a} {th[1]}. {nm} gets some more and now has {s}. Which equation shows the story?", good, bad,
                [f"{a} and some more make {s}.", f"The equation is {good}."], qtype="conceptual", tags={"modeling"}, r=r)
    return it


# ============================================================== S3 Balancing Both Sides
def bal(r, L):
    if L == 0:
        a, b = r.randint(1, 5), r.randint(1, 5)
        c = r.randint(1, a + b - 1)
        return f"{a} + {b} = {c} + ___", a + b - c, a + b
    a, b = r.randint(2, 9), r.randint(2, 9)
    s = a + b
    c = r.randint(1, 9)
    need(c != a and c != b and s - c > 0)
    if L == 1:
        return pick(r, [f"{a} + {b} = {c} + ___", f"{a} + {b} = ___ + {c}"]), s - c, s
    k = r.randint(1, 9)
    form = pick(r, ["subadd", "addsub", "rev"])
    if form == "subadd":
        need(s + k <= 20)
        return f"{s + k} − {k} = {c} + ___", s - c, s
    if form == "addsub":
        need(s + c <= 20)
        return f"{a} + {b} = ___ − {c}", s + c, s
    return f"{c} + ___ = {a} + {b}", s - c, s


@fam("012")
def b_blank(r, L):
    eq, x, s = bal(r, L)
    nums = [int(t) for t in re.findall(r"\d+", eq)]
    return Item(pick(r, [f"What number makes both sides the same? {eq}", f"Find the missing number: {eq}", f"Make it true: {eq}"]), x,
                [f"The side you know is {s}.", f"{eq.replace('___', str(x))} is true."],
                [W(s, "wrote the total of the other side"), W(sum(nums), "added all the numbers"), W(x + 1, "counted one too many"), W(x - 1 if x > 1 else x + 2, "made a counting mistake")],
                FN("blank_eq", eq=eq), qtype="reasoning", tags={"reasoning"}, claim=eq)


@fam("012", mode="mc")
def b_mc(r, L):
    eq, x, s = bal(r, L)
    nums = [int(t) for t in re.findall(r"\d+", eq)]
    return Item(pick(r, [f"Which number makes {eq} true?", f"Pick the number for the blank: {eq}"]), x, [f"One side is {s}.", f"{eq.replace('___', str(x))} is true."],
                [W(s, "wrote the total of the other side"), W(sum(nums), "added all the numbers"), W(x + 1, "counted one too many"), W(x + 2, "made a counting mistake")],
                FN("blank_eq", eq=eq), qtype="reasoning", tags={"reasoning"})


@fam("01")
def b_bars(r, L):
    a, b = (r.randint(1, 5), r.randint(1, 5)) if L == 0 else (r.randint(3, 9), r.randint(3, 9))
    s = a + b
    c = r.randint(1, s - 1)
    need(c not in (a, b))
    eq = f"{a} + {b} = {c} + ___"
    alt = f"Two bars of the same length. The top bar has parts {a} and {b}. The bottom bar has parts {c} and an unknown part."
    return Item(f"The two bars are the same length. What number makes {eq} true?", s - c, [f"Both bars show {s}.", f"{c} + {s - c} = {s}."],
                [W(s, "wrote the total"), W(s + c, "added all the numbers"), W(s - c + 1, "counted one too many"), W(c, "copied a number")],
                FN("blank_eq", eq=eq), qtype="visual", tags={"reasoning"},
                diagram=Diagram("bars", {"rows": [{"label": "", "parts": [[a, str(a)], [b, str(b)]]}, {"label": "", "parts": [[c, str(c)], [s - c, "?"]]}]}, alt))


@fam("12")
def b_story(r, L):
    a, b = r.randint(3, 9), r.randint(3, 9)
    c = r.randint(2, 9)
    s = a + b
    need(s - c > 0 and c not in (a, b))
    n1, n2 = r.sample(NAMES, 2)
    th = thing(r)
    return Item(f"{n1} has {a} red {th[1]} and {b} blue {th[1]}. {n2} has {c} {th[1]}. How many more does {n2} need to have the same number as {n1}?",
                f"{s - c} {th[1]}", [f"{n1} has {a} + {b} = {s}.", f"{c} + {s - c} = {s}, so {n2} needs {s - c} more."],
                [W(f"{s} {th[1]}", "gave the total"), W(f"{s + c} {th[1]}", "added all the numbers"), W(f"{s - c + 1} {th[1]}", "counted one too many"), W(f"{abs(a - c)} {th[1]}", "used only one color")],
                EX(f"{a}+{b}-{c}", unit=th[1]), qtype="word-problem", tags={"modeling", "multistep"})


@fam("2", mode="mc")
def b_why(r, L):
    a, b = r.randint(3, 9), r.randint(3, 9)
    c = r.randint(2, 8)
    s = a + b
    need(s - c > 0 and c not in (a, b))
    eq = f"{a} + {b} = {c} + ___"
    good = f"{s - c}, because {c} + {s - c} = {s}"
    bad = [f"{s}, because {a} + {b} = {s}", f"{s + c}, because I add all the numbers", f"{s - c + 1}, because {c} + {s - c + 1} = {s}"]
    it = mc_key(f"{eq}. Which answer and reason are correct?", good, bad, [f"The left side is {s}.", f"{c} + {s - c} = {s}."], qtype="explain", tags={"reasoning"}, r=r)
    return it


@fam("012", mode="mc")
def b_pairs(r, L):
    a, b = (r.randint(1, 5), r.randint(1, 5)) if L == 0 else (r.randint(3, 9), r.randint(3, 9))
    s = a + b
    c = r.randint(1, s - 1)
    need(c not in (a, b))
    good = f"{c} + {s - c}"
    bad = [f"{c} + {s - c + 1}", f"{c + 1} + {s - c + 1}", f"{s} + {c}"]
    it = mc_key(f"Which fills the blank to make it true? {a} + {b} = ___", good, bad, [f"{a} + {b} = {s}.", f"{good} is also {s}."], qtype="reasoning", r=r)
    it.check = FN("same_value", target=f"{a}+{b}")
    return it


@fam("01", mode="mc")
def b_more(r, L):
    hi = 10 if L == 0 else 18
    a, b, c, d = (r.randint(1, hi // 2) for _ in range(4))
    x, y = a + b, c + d
    need(abs(x - y) <= 2 and (a, b) != (c, d) and (a, b) != (d, c))
    good = f"{a} + {b}" if x > y else f"{c} + {d}" if y > x else "They are the same."
    opts = [f"{a} + {b}", f"{c} + {d}", "They are the same."]
    bad = [o for o in opts if o != good] + [f"{a} + {d}" if f"{a} + {d}" not in opts else f"{b} + {c + 1}"]
    it = mc_key(f"Which is more: {a} + {b} or {c} + {d}?", good, bad, [f"{a} + {b} = {x} and {c} + {d} = {y}.", f"The answer is: {good}"], qtype="reasoning", r=r)
    return it


SKILLS = {
    1: dict(name="True or False Equations", fams=[t_mc, t_word, t_which_true, t_which_false, t_side, t_pic]),
    2: dict(name="Finding the Missing Number", fams=[m_blank, m_mc, m_think, m_bars, m_which_eq, m_frame]),
    3: dict(name="Balancing Both Sides", fams=[b_blank, b_mc, b_bars, b_story, b_why, b_pairs, b_more]),
}
