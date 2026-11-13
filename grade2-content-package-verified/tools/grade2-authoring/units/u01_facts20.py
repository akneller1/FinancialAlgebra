"""Unit 1: Addition and Subtraction within 20 (add-subtract-20). 2.OA.B.2."""
from g2lib import *

UNIT_ID = "add-subtract-20"


def pair(r, L, lo=None):
    """Two one-digit addends. L0: sums 6-13, L1: any sum 11-18 (crossing ten), L2: any one-digit pair with sum >= 11."""
    if L == 0:
        a, b = r.randint(2, 9), r.randint(2, 9)
        need(6 <= a + b <= 13)
    elif L == 1:
        a, b = r.randint(3, 9), r.randint(3, 9)
        need(11 <= a + b <= 18)
    else:
        a, b = r.randint(4, 9), r.randint(5, 9)
        need(a + b >= 12)
    return a, b


def add_wrongs(a, b):
    s = a + b
    return [W(s - 1, "counted on and included the first number"), W(s + 1, "counted one too many"), W(abs(a - b), "subtracted instead of adding"),
            W(s + 10, "added an extra ten"), W(s - 2, "made a counting mistake")]


# ============================================================== S1 Adding within 20 with Strategies
@fam("012")
def ad_fact(r, L):
    a, b = pair(r, L)
    return Item(f"What is {a} + {b}?", a + b, [f"Start at {max(a, b)} and add {min(a, b)}, or make a ten.", f"{a} + {b} = {a + b}."],
                add_wrongs(a, b), EX(f"{a}+{b}"), qtype="procedural", claim=f"{a} + {b}")


@fam("012")
def ad_make10(r, L):
    a, b = pair(r, max(L, 1))
    need(a >= 7 and a + b > 10)
    k = 10 - a
    eq = f"{a} + {b} = 10 + ___"
    return Item(f"Make a ten to add. {a} + {k} = 10, so {eq}", b - k,
                [f"Break {b} into {k} and {b - k}.", f"{a} + {k} = 10 and 10 + {b - k} = {a + b}, so the missing number is {b - k}."],
                [W(b, "did not break apart the second number"), W(k, "wrote the part that makes ten"), W(a + b, "wrote the whole sum"), W(b - k + 1, "made a counting mistake")],
                FN("blank_eq", eq=eq), qtype="compare-strategies", tags={"connections"})


@fam("012")
def ad_double(r, L):
    a = r.randint(2, 6) if L == 0 else r.randint(4, 9)
    d = 1 if L < 2 else pick(r, [1, 1, 2])
    need(a + d <= 9)
    return Item(f"Use the double {a} + {a} = {2 * a} to find {a} + {a + d}.", 2 * a + d,
                [f"{a} + {a + d} is {d} more than {a} + {a}.", f"{2 * a} + {d} = {2 * a + d}."],
                [W(2 * a, "used only the double"), W(2 * a - d, "subtracted instead of adding"), W(2 * (a + d), "doubled the bigger number"), W(2 * a + d + 1, "counted one too many")],
                EX(f"{a}+{a + d}"), qtype="compare-strategies", tags={"connections"})


@fam("01")
def ad_dots(r, L):
    a, b = pair(r, L)
    alt = f"Two circles of dots. The first circle has {a} dots and the second circle has {b} dots."
    return Item("How many dots are there in all?", a + b, [f"There are {a} dots and {b} dots.", f"{a} + {b} = {a + b}."],
                add_wrongs(a, b), EX(f"{a}+{b}"), qtype="visual",
                diagram=Diagram("groups", {"counts": [a, b]}, alt))


@fam("012")
def ad_word(r, L):
    a, b = pair(r, L)
    t = pick(r, [("{nm} has {a} red beads and {b} blue beads. How many beads does {nm} have?", "beads"),
                 ("There are {a} ducks in the pond. {b} more ducks swim over. How many ducks are in the pond now?", "ducks"),
                 ("{nm} read {a} pages in the morning and {b} pages at night. How many pages did {nm} read?", "pages"),
                 ("A bus has {a} children. At the next stop, {b} more children get on. How many children are on the bus now?", "children")])
    return Item(t[0].format(a=a, b=b, nm=name(r)), f"{a + b} {t[1]}", [f"Add {a} + {b}.", f"{a} + {b} = {a + b} {t[1]}."],
                [W(f"{w} {t[1]}", y) for w, y in add_wrongs(a, b)], EX(f"{a}+{b}", unit=t[1]), qtype="word-problem", tags={"modeling"})


@fam("12")
def ad_three(r, L):
    a, b, c = r.randint(2, 9), r.randint(2, 9), r.randint(2, 9)
    need(a + b + c <= 20 and (a + b == 10 or a + c == 10 or b + c == 10 or L == 2))
    return Item(f"Add: {a} + {b} + {c}", a + b + c, ["Look for two numbers that make a ten, then add the third number.", f"{a} + {b} + {c} = {a + b + c}."],
                [W(a + b, "left out an addend"), W(b + c, "left out an addend"), W(a + b + c - 1, "made a counting mistake"), W(a + b + c + 10, "added an extra ten")],
                EX(f"{a}+{b}+{c}"), qtype="procedural", claim=f"{a} + {b} + {c}")


@fam("012", mode="mc")
def ad_same(r, L):
    a, b = pair(r, max(L, 1))
    need(a != b and a + b > 10)
    good = f"{b} + {a}"
    bad = [f"{a} + {b + 1}", f"{a - 1} + {b - 1}" if L < 2 else f"{a} − {b}" if a > b else f"{b} − {a}", f"10 + {a + b - 9}"]
    good2 = f"10 + {a + b - 10}"
    it = mc_key(f"Which has the same sum as {a} + {b}?", good if L < 2 else good2, bad, [f"{a} + {b} = {a + b}.", f"{good if L < 2 else good2} = {a + b} too."], r=r)
    it.check = FN("same_value", target=f"{a}+{b}")
    return it


@fam("2")
def ad_two_ways(r, L):
    a, b = pair(r, 2)
    need(a != b)
    return Item(f"{name(r)} says {a} + {b} is the same as 10 + ___. What number goes in the blank?", a + b - 10,
                [f"{a} + {b} = {a + b}.", f"{a + b} = 10 + {a + b - 10}, so the number is {a + b - 10}."],
                [W(a + b, "wrote the whole sum"), W(b, "copied an addend"), W(10 - a, "found what makes ten with the first number"), W(a + b - 9, "made a counting mistake")],
                FN("blank_eq", eq=f"{a} + {b} = 10 + ___"), qtype="explain", tags={"reasoning"})


# ============================================================== S2 Subtracting within 20 with Strategies
def sub_pair(r, L):
    a, b = pair(r, L)
    return a + b, b


def sub_wrongs(w, p):
    d = w - p
    out = [W(d + 1, "counted back and included the starting number"), W(d - 1, "counted back one too many"), W(w + p, "added instead of subtracting")]
    if w >= 10 and w % 10 < p:
        out.append(W(10 * (w // 10) + (p - w % 10), "subtracted the smaller digit from the larger digit"))
    out.append(W(d + 10, "forgot to cross back over ten"))
    return out


@fam("012")
def sb_fact(r, L):
    w, p = sub_pair(r, L)
    return Item(f"What is {w} − {p}?", w - p, [f"Think: {p} + ___ = {w}.", f"{p} + {w - p} = {w}, so {w} − {p} = {w - p}."],
                sub_wrongs(w, p), EX(f"{w}-{p}"), qtype="procedural", claim=f"{w} − {p}")


@fam("012")
def sb_think_add(r, L):
    w, p = sub_pair(r, L)
    eq = f"{p} + ___ = {w}"
    return Item(f"Think addition to subtract {w} − {p}. {eq}", w - p,
                [f"Count up from {p} to {w}.", f"{p} + {w - p} = {w}, so {w} − {p} = {w - p}."],
                [W(w + p, "added the two numbers"), W(w - p + 1, "counted one too many"), W(w, "copied the whole"), W(w - p - 1, "counted one too few")],
                FN("blank_eq", eq=eq), qtype="compare-strategies", tags={"connections"})


@fam("12")
def sb_back10(r, L):
    w, p = sub_pair(r, L)
    need(w > 10 and p > w - 10)
    k = w - 10
    eq = f"{w} − {p} = 10 − ___"
    return Item(f"Go back through ten. {w} − {k} = 10, so {eq}", p - k,
                [f"Break {p} into {k} and {p - k}.", f"{w} − {k} = 10 and 10 − {p - k} = {w - p}, so the missing number is {p - k}."],
                [W(p, "did not break apart the number"), W(k, "wrote the part that gets to ten"), W(w - p, "wrote the whole difference"), W(p - k + 1, "made a counting mistake")],
                FN("blank_eq", eq=eq), qtype="compare-strategies", tags={"connections"})


@fam("01")
def sb_line(r, L):
    w, p = sub_pair(r, L)
    alt = f"A number line from 0 to 20. An arrow starts at {w} and jumps back {p} to a point marked with a question mark."
    return Item(f"The number line shows {w} − {p}. Where does the jump land?", w - p,
                [f"Start at {w} and jump back {p}.", f"{w} − {p} = {w - p}."], sub_wrongs(w, p), EX(f"{w}-{p}"), qtype="visual",
                diagram=Diagram("jline", {"lo": 0, "hi": 20, "step": 1, "label_every": 5, "jumps": [[w, w - p, f"−{p}"]], "points": [{"v": w - p, "label": "?"}]}, alt))


@fam("012")
def sb_word(r, L):
    w, p = sub_pair(r, L)
    t = pick(r, [("{nm} had {w} stickers. {nm} gave away {p} stickers. How many stickers does {nm} have now?", "stickers"),
                 ("There were {w} birds on a fence. {p} birds flew away. How many birds are on the fence now?", "birds"),
                 ("A plate had {w} grapes. {nm} ate {p} grapes. How many grapes are left?", "grapes"),
                 ("{w} children are at the park. {p} children go home. How many children are still at the park?", "children")])
    return Item(t[0].format(w=w, p=p, nm=name(r)), f"{w - p} {t[1]}", [f"Subtract {w} − {p}.", f"{w} − {p} = {w - p} {t[1]}."],
                [W(f"{x} {t[1]}", y) for x, y in sub_wrongs(w, p)], EX(f"{w}-{p}", unit=t[1]), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def sb_which_add(r, L):
    w, p = sub_pair(r, L)
    need(p != w - p)
    good = f"{p} + {w - p} = {w}"
    bad = [f"{w} + {p} = {w + p}", f"{p} + {w - p + 1} = {w + 1}", f"{w - p} + {w} = {2 * w - p}"]
    it = mc_key(f"Which addition fact helps you find {w} − {p}?", good, bad, [f"The parts {p} and {w - p} make the whole {w}.", f"So {w} − {p} = {w - p}."], qtype="conceptual", tags={"connections"}, r=r)
    it.check = FN("helps_sub", whole=w, part=p)
    return it


@fam("2")
def sb_dist(r, L):
    a, b = r.randint(11, 19), r.randint(11, 19)
    need(abs(a - b) >= 3 and a != b)
    hi, lo = max(a, b), min(a, b)
    return Item(f"{name(r)} scored {lo} points. {name(sub(r, 1))} scored {hi} points. How many more points did {name(sub(r, 1))} score?", f"{hi - lo} points",
                [f"Find the difference: {hi} − {lo}.", f"{hi} − {lo} = {hi - lo} points."],
                [W(f"{hi + lo} points", "added the two scores"), W(f"{hi - lo + 1} points", "counted one too many"), W(f"{hi} points", "gave the bigger score")],
                EX(f"{hi}-{lo}", unit="points"), qtype="word-problem", tags={"modeling"})


# ============================================================== S3 Related Facts and Fact Families
def family(r, L):
    a, b = pair(r, L)
    need(a != b)
    return a, b, a + b


@fam("012")
def ff_missing(r, L):
    a, b, s = family(r, L)
    form = pick(r, ["sub", "sub2"])
    eq = f"{s} − {a} = ___" if form == "sub" else f"{s} − ___ = {a}"
    return Item(f"{a} + {b} = {s}. Use this fact to complete: {eq}", b,
                [f"{a}, {b}, and {s} are in the same fact family.", f"{eq.replace('___', str(b))}."],
                [W(s, "wrote the whole"), W(a, "copied the wrong part"), W(s + a, "added instead of subtracting"), W(b + 1, "made a counting mistake")],
                FN("blank_eq", eq=eq), qtype="fill-blank", tags={"connections"})


@fam("012", mode="mc")
def ff_not(r, L):
    a, b, s = family(r, L)
    good = f"{a} − {b} = {s}" if a > b else f"{b} − {a} = {s}"
    bad = [f"{s} − {a} = {b}", f"{b} + {a} = {s}", f"{s} − {b} = {a}"]
    it = mc_key(f"Which fact is NOT in the fact family for {a}, {b}, and {s}?", good, bad,
                [f"The facts are {a} + {b} = {s}, {b} + {a} = {s}, {s} − {a} = {b}, and {s} − {b} = {a}.", f"{good} is not true."], qtype="conceptual", r=r)
    it.check = FN("false_eq")
    return it


@fam("012", mode="mc")
def ff_member(r, L):
    a, b, s = family(r, L)
    good = f"{s} − {b} = {a}"
    bad = [f"{s} + {b} = {s + b}", f"{a} − {b} = {a - b}" if a > b else f"{b} − {a} = {b - a}", f"{s} − {a} = {b + 1}"]
    need(len(set(bad)) == 3)
    it = mc_key(f"{a} + {b} = {s}. Which subtraction fact is in the same fact family?", good, bad,
                [f"Start with the whole, {s}, and take away one part.", f"{s} − {b} = {a}."], qtype="conceptual", tags={"connections"}, r=r)
    it.check = FN("fam_member", nums=[a, b, s])
    return it


@fam("01")
def ff_bond(r, L):
    a, b, s = family(r, L)
    alt = f"A part-part-whole bar. The whole is {s}. One part is {a}. The other part is unknown."
    return Item(f"The whole is {s} and one part is {a}. What is the other part?", b,
                [f"Find the missing part: {s} − {a}.", f"{s} − {a} = {b}, because {a} + {b} = {s}."],
                [W(s + a, "added the whole and the part"), W(b + 1, "made a counting mistake"), W(s, "gave the whole"), W(b - 1, "counted one too few")],
                EX(f"{s}-{a}"), qtype="visual",
                diagram=Diagram("bars", {"rows": [{"parts": [[s, str(s)]]}, {"parts": [[a, str(a)], [b, "?"]]}]}, alt))


@fam("12")
def ff_count(r, L):
    a, b, s = family(r, L)
    eqs = [f"{a} + {b} = {s}", f"{b} + {a} = {s}", f"{s} − {a} = {b}", f"{s} − {b} = {a}"]
    pick_i = r.randrange(4)
    shown = [e for i, e in enumerate(eqs) if i != pick_i]
    return Item(f"{name(r)} wrote three facts in a fact family: {'; '.join(shown)}. Write the missing fact.", eqs[pick_i],
                [f"The fact family for {a}, {b}, and {s} has four facts.", f"The missing fact is {eqs[pick_i]}."],
                [W(f"{a} − {b} = {s}" if a > b else f"{b} − {a} = {s}", "subtracted a part from a part"), W(f"{s} + {a} = {s + a}", "added to the whole")],
                FN("fam_fact", nums=[a, b, s], have=shown), qtype="fill-blank", tags={"connections"})


@fam("012")
def ff_word(r, L):
    a, b, s = family(r, L)
    t = pick(r, [("There are {s} apples in a bowl. {a} are red and the rest are green. How many apples are green?", "apples"),
                 ("{nm} has {s} cards. {a} cards are blue. The rest are yellow. How many cards are yellow?", "cards"),
                 ("A class has {s} pencils. {a} are sharp. How many are not sharp?", "pencils")])
    return Item(t[0].format(s=s, a=a, nm=name(r)), f"{b} {t[1]}", [f"{a} + ___ = {s}.", f"{a} + {b} = {s}, so the answer is {b} {t[1]}."],
                [W(f"{s + a} {t[1]}", "added the whole and the part"), W(f"{b + 1} {t[1]}", "made a counting mistake"), W(f"{s} {t[1]}", "gave the total")],
                EX(f"{s}-{a}", unit=t[1]), qtype="word-problem", tags={"modeling"})


@fam("2")
def ff_two_unknown(r, L):
    a, b, s = family(r, 2)
    c = r.randint(2, 9)
    need(s - c > 0 and c != a and c != b)
    eq = f"{a} + {b} = {s - c} + ___"
    return Item(f"Find the missing number: {eq}", c,
                [f"{a} + {b} = {s}.", f"{s - c} + {c} = {s}, so the missing number is {c}."],
                [W(s, "wrote the sum of the left side"), W(s + s - c, "added all the numbers"), W(c + 1, "made a counting mistake"), W(s - c, "copied a number")],
                FN("blank_eq", eq=eq), qtype="explain", tags={"reasoning"})


# ============================================================== S4 Missing Numbers in Equations within 20
@fam("012")
def mn_add(r, L):
    a, b = pair(r, L)
    form = pick(r, ["a", "b"]) if L else "b"
    eq = f"{a} + ___ = {a + b}" if form == "b" else f"___ + {b} = {a + b}"
    ans = b if form == "b" else a
    return Item(f"What number makes the equation true? {eq}", ans, ["Count up or think subtraction.", f"{eq.replace('___', str(ans))}."],
                [W(a + b + (a if form == 'b' else b), "added the numbers shown"), W(ans + 1, "made a counting mistake"), W(a + b, "copied the total"), W(ans - 1, "counted one too few")],
                FN("blank_eq", eq=eq), qtype="fill-blank")


@fam("012")
def mn_sub(r, L):
    w, p = sub_pair(r, L)
    form = pick(r, ["mid", "start"]) if L == 2 else "mid"
    eq = f"{w} − ___ = {w - p}" if form == "mid" else f"___ − {p} = {w - p}"
    ans = p if form == "mid" else w
    return Item(f"What number makes the equation true? {eq}", ans, ["Use the related addition fact.", f"{eq.replace('___', str(ans))}."],
                [W(w + w - p if form == "mid" else w - p - p if w - 2 * p > 0 else w + 1, "added or subtracted the numbers shown"), W(ans + 1, "made a counting mistake"), W(w - p, "copied a number"), W(ans - 1, "counted one too few")],
                FN("blank_eq", eq=eq), qtype="fill-blank")


@fam("012", mode="mc")
def mn_true(r, L):
    a, b = pair(r, L)
    good = f"{a} + {b} = {a + b + 1} − 1" if L == 2 else f"{a + b} = {a} + {b}"
    bad = [f"{a} + {b} = {a + b + 1}", f"{a + b} = {a} − {b}" if a > b else f"{a + b} = {b} − {a}", f"{a} + {b} = {a} + {b + 1}"]
    it = mc_key("Which equation is true?", good, bad, ["Find the value of each side.", f"In {good}, both sides equal {a + b}."], r=r)
    it.check = FN("true_eq")
    return it


@fam("012", mode="mc")
def mn_tf(r, L):
    a, b = pair(r, L)
    ok = r.random() < 0.5
    s = a + b if ok else a + b + pick(r, [1, -1, 2])
    eq = f"{a} + {b} = {s}" if L < 2 else f"{s} = {a} + {b}"
    if ok:
        good = f"True. {a} + {b} is {a + b}."
        bad = [f"False. {a} + {b} is {a + b + 1}.", f"True. {a} + {b} is {a + b - 1}.", f"False. {a} + {b} is {a + b - 2}."]
    else:
        good = f"False. {a} + {b} is {a + b}."
        bad = [f"True. {a} + {b} is {s}.", f"False. {a} + {b} is {s + 1}.", f"True. {a} + {b} is {a + b}."]
    it = mc_key(f"Is this equation true or false? {eq}", good, bad,
                [f"{a} + {b} = {a + b}.", f"So {eq} is {'true' if ok else 'false'}."], qtype="explain", tags={"reasoning"}, r=r)
    it.check = FN("eq_truth", eq=eq)
    return it


@fam("12")
def mn_both(r, L):
    a, b = pair(r, L)
    c = r.randint(1, min(9, a + b - 1))
    eq = f"{a} + {b} = ___ + {c}"
    return Item(f"What number makes the equation true? {eq}", a + b - c,
                [f"{a} + {b} = {a + b}.", f"___ + {c} must also be {a + b}, so the number is {a + b - c}."],
                [W(a + b, "wrote the sum of the left side"), W(a + b + c, "added all the numbers"), W(a + b - c + 1, "made a counting mistake")],
                FN("blank_eq", eq=eq), qtype="explain", tags={"reasoning"})


@fam("012")
def mn_story(r, L):
    a, b = pair(r, L)
    t = pick(r, [("{nm} had some marbles. {nm} found {b} more. Now {nm} has {s} marbles. How many marbles did {nm} have at first?", "marbles", "start"),
                 ("{nm} has {a} toy cars. How many more toy cars does {nm} need to have {s}?", "toy cars", "change"),
                 ("There are {a} cups on a table. Some more cups are added. Now there are {s} cups. How many cups were added?", "cups", "change")])
    ans = a if t[2] == "start" else b
    eq = f"___ + {b} = {a + b}" if t[2] == "start" else f"{a} + ___ = {a + b}"
    return Item(t[0].format(a=a, b=b, s=a + b, nm=name(r)), f"{ans} {t[1]}", [f"Write {eq}.", f"{eq.replace('___', str(ans))}, so the answer is {ans} {t[1]}."],
                [W(f"{a + b + (b if t[2] == 'start' else a)} {t[1]}", "added the numbers in the story"), W(f"{ans + 1} {t[1]}", "made a counting mistake"), W(f"{a + b} {t[1]}", "gave the total")],
                FN("blank_eq", eq=eq, unit=t[1]), qtype="word-problem", tags={"modeling"})


@fam("2")
def mn_balance(r, L):
    a, b = pair(r, 2)
    c = r.randint(2, 9)
    d = a + b - c
    need(1 <= d <= 9 and c != a and c != b)
    eq = f"{a} + {b} = {c} + ___"
    alt = f"Two bars of the same length. The top bar has parts {a} and {b}. The bottom bar has parts {c} and an unknown part."
    return Item(f"The two bars are the same length. What number makes {eq} true?", d,
                [f"Both bars must show {a + b}.", f"{c} + {d} = {a + b}, so the number is {d}."],
                [W(a + b, "wrote the total of the left side"), W(a + b + c, "added all the numbers"), W(d + 1, "made a counting mistake")],
                FN("blank_eq", eq=eq), qtype="visual", tags={"reasoning"},
                diagram=Diagram("bars", {"rows": [{"label": "Left", "parts": [[a, str(a)], [b, str(b)]]}, {"label": "Right", "parts": [[c, str(c)], [d, "?"]]}]}, alt))


SKILLS = {
    1: dict(name="Adding within 20 with Strategies", fams=[ad_fact, ad_make10, ad_double, ad_dots, ad_word, ad_three, ad_same, ad_two_ways]),
    2: dict(name="Subtracting within 20 with Strategies", fams=[sb_fact, sb_think_add, sb_back10, sb_line, sb_word, sb_which_add, sb_dist]),
    3: dict(name="Related Facts and Fact Families", fams=[ff_missing, ff_not, ff_member, ff_bond, ff_count, ff_word, ff_two_unknown]),
    4: dict(name="Missing Numbers in Equations within 20", fams=[mn_add, mn_sub, mn_true, mn_tf, mn_both, mn_story, mn_balance]),
}
