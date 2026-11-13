"""Unit 5: Addition and Subtraction within 100 (add-subtract-100). 2.NBT.B.5, 2.NBT.B.6, 2.NBT.B.9."""
from g2lib import *

UNIT_ID = "add-subtract-100"


def two(r, L):
    """Two two-digit addends with sum <= 100. L0 no new ten, L1 mixed, L2 always a new ten."""
    a, b = r.randint(12, 79), r.randint(11, 59)
    need(a + b <= 100)
    reg = a % 10 + b % 10 >= 10
    need((L == 0 and not reg) or L == 1 or (L == 2 and reg))
    return a, b


def add_w(a, b):
    s = a + b
    nc = (a // 10 + b // 10) * 10 + (a % 10 + b % 10) % 10
    out = []
    if nc != s:
        out.append(W(nc, "did not add the new ten"))
        out.append(W(int(f"{a // 10 + b // 10}{a % 10 + b % 10}"), "wrote 10 or more ones in the ones place"))
    out += [W(s + 10, "added an extra ten"), W(s - 1, "made a counting mistake"), W(abs(a - b), "subtracted instead of adding"), W(s - 10, "forgot a ten")]
    return out


def sub_w(a, b):
    d = a - b
    sm = abs(a // 10 - b // 10) * 10 + abs(a % 10 - b % 10)
    out = []
    if sm != d:
        out.append(W(sm, "subtracted the smaller digit from the larger digit"))
        out.append(W(d + 10, "broke apart a ten but did not take it away"))
    out += [W(a + b, "added instead of subtracting"), W(d + 1, "made a counting mistake"), W(d - 10, "took away an extra ten")]
    return out


def subs(r, L):
    a, b = r.randint(31, 99), r.randint(12, 69)
    need(a - b >= 5)
    reg = a % 10 < b % 10
    need((L == 0 and not reg) or L == 1 or (L == 2 and reg))
    return a, b


# ============================================================== S1 Adding within 100
@fam("012")
def a_std(r, L):
    a, b = two(r, L)
    return Item(f"Add: {a} + {b}", a + b, ["Add the tens, then the ones. Make a new ten if there are 10 or more ones.", f"{a} + {b} = {a + b}."],
                add_w(a, b), EX(f"{a}+{b}"), qtype="procedural", claim=f"{a} + {b}")


@fam("012")
def a_parts(r, L):
    a, b = two(r, L)
    t, o = (a // 10 + b // 10) * 10, a % 10 + b % 10
    return Item(f"{name(r)} adds {a} + {b} by place value. Tens: {a // 10 * 10} + {b // 10 * 10} = {t}. Ones: {a % 10} + {b % 10} = {o}. What is the sum?", a + b,
                [f"Add the two parts: {t} + {o}.", f"{t} + {o} = {a + b}."],
                [W(int(f"{t // 10}{o}") if o >= 10 else t + o + 10, "wrote the tens and ones side by side" if o >= 10 else "added an extra ten"), W(t, "left out the ones"), W(t + o - 10, "forgot a ten")],
                EX(f"{t}+{o}"), qtype="compare-strategies", tags={"multiple-representations"})


@fam("012")
def a_blocks(r, L):
    a, b = two(r, max(L, 1))
    t, o = a // 10 + b // 10, a % 10 + b % 10
    need(o >= 10 or L < 2)
    alt = f"Base-ten blocks for {a} + {b} put together: {t} tens rods and {o} ones cubes."
    return Item(f"The blocks show {a} + {b} put together. Trade 10 ones for 1 ten if you can. What is the total?", a + b,
                [f"There are {t} tens and {o} ones." + (f" Trade 10 ones for 1 ten: {t + 1} tens and {o - 10} ones." if o >= 10 else ""), f"The total is {a + b}."],
                add_w(a, b), EX(f"{t}×10+{o}"), qtype="visual", diagram=Diagram("blocks", {"t": t, "o": o}, alt))


@fam("012")
def a_word(r, L):
    a, b = two(r, L)
    tt = pick(r, [("A class collected {a} cans on Monday and {b} cans on Tuesday. How many cans did it collect?", "cans"),
                  ("{nm} has {a} stickers. {nm} gets {b} more. How many stickers does {nm} have now?", "stickers"),
                  ("A farmer picked {a} apples in the morning and {b} apples in the afternoon. How many apples did the farmer pick?", "apples")])
    return Item(tt[0].format(a=a, b=b, nm=name(r)), f"{a + b} {tt[1]}", [f"Add {a} + {b}.", f"{a} + {b} = {a + b} {tt[1]}."],
                [W(f"{w} {tt[1]}", y) for w, y in add_w(a, b)], EX(f"{a}+{b}", unit=tt[1]), qtype="word-problem", tags={"modeling"})


@fam("012")
def a_jump(r, L):
    a, b = two(r, L)
    bt, bo = b // 10 * 10, b % 10
    need(bo)
    lo, hi = a // 10 * 10, -(-(a + b) // 10) * 10
    alt = f"A number line from {lo} to {hi}. A jump of {bt} goes from {a} to {a + bt}, then a jump of {bo} goes to a point marked with a question mark."
    return Item(f"The number line shows {a} + {b}: first add {bt}, then add {bo}. Where does it land?", a + b,
                [f"{a} + {bt} = {a + bt}.", f"{a + bt} + {bo} = {a + b}."], add_w(a, b), EX(f"{a}+{bt}+{bo}"), qtype="visual",
                diagram=Diagram("jline", {"lo": lo, "hi": hi, "step": 1, "label_every": 10, "jumps": [[a, a + bt, f"+{bt}"], [a + bt, a + b, f"+{bo}"]], "points": [{"v": a + b, "label": "?"}]}, alt))


@fam("12")
def a_friendly(r, L):
    a, b = two(r, 2)
    need(a % 10 >= 6)
    k = 10 - a % 10
    eq = f"{a} + {b} = {a + k} + ___"
    return Item(f"Make a ten to add. Move {k} from {b} to {a}. {eq}", b - k, [f"{a} + {k} = {a + k}, and {b} − {k} = {b - k}.", f"{a + k} + {b - k} = {a + b}."],
                [W(b + k, "added to both numbers"), W(b, "did not move any"), W(a + b, "wrote the whole sum")],
                FN("blank_eq", eq=eq), qtype="compare-strategies", tags={"connections"})


@fam("2")
def a_digit(r, L):
    a, b = two(r, 2)
    s = a + b
    shown = f"{a // 10}□"
    return Item(f"Find the missing digit: {shown} + {b} = {s}", a % 10, [f"{s} − {b} = {a}.", f"So the missing digit is {a % 10}."],
                [W((a % 10 + 1) % 10, "made an addition mistake"), W(s % 10, "copied the ones digit of the sum"), W(abs(s % 10 - b % 10), "did not think about the new ten")],
                FN("missing_digit", shown=shown, other=b, total=s, op="+"), qtype="explain", tags={"reasoning"})


# ============================================================== S2 Subtracting within 100
@fam("012")
def s_std(r, L):
    a, b = subs(r, L)
    return Item(f"Subtract: {a} − {b}", a - b, ["Subtract the ones, then the tens. If there are not enough ones, break apart a ten.", f"{a} − {b} = {a - b}."],
                sub_w(a, b), EX(f"{a}-{b}"), qtype="procedural", claim=f"{a} − {b}")


@fam("012")
def s_word(r, L):
    a, b = subs(r, L)
    tt = pick(r, [("A box had {a} crayons. {b} crayons were used. How many crayons are left?", "crayons"),
                  ("{nm} had {a} cents. {nm} spent {b} cents. How many cents does {nm} have left?", "cents"),
                  ("There were {a} people on a train. {b} people got off. How many people are still on the train?", "people")])
    return Item(tt[0].format(a=a, b=b, nm=name(r)), f"{a - b} {tt[1]}", [f"Subtract {a} − {b}.", f"{a} − {b} = {a - b} {tt[1]}."],
                [W(f"{w} {tt[1]}", y) for w, y in sub_w(a, b)], EX(f"{a}-{b}", unit=tt[1]), qtype="word-problem", tags={"modeling"})


@fam("012")
def s_blocks(r, L):
    a, b = subs(r, max(L, 1))
    need(a % 10 < b % 10 or L < 2)
    alt = f"Base-ten blocks showing {a}: {a // 10} tens rods and {a % 10} ones cubes."
    return Item(f"The blocks show {a}. Take away {b}. If there are not enough ones, trade 1 ten for 10 ones. How many are left?", a - b,
                [f"{a} = {a // 10} tens and {a % 10} ones" + (f" = {a // 10 - 1} tens and {a % 10 + 10} ones." if a % 10 < b % 10 else "."), f"{a} − {b} = {a - b}."],
                sub_w(a, b), EX(f"{a}-{b}"), qtype="visual", diagram=Diagram("blocks", {"t": a // 10, "o": a % 10}, alt))


@fam("012")
def s_countup(r, L):
    a, b = subs(r, L)
    need(b % 10 and a % 10)
    up1 = 10 - b % 10
    mid = b + up1
    up2 = a // 10 * 10 - mid
    up3 = a % 10
    need(up2 >= 0)
    jumps = [[b, mid, f"+{up1}"]] + ([[mid, mid + up2, f"+{up2}"]] if up2 else []) + [[mid + up2, a, f"+{up3}"]]
    alt = f"An open number line from {b // 10 * 10} to {-(-a // 10) * 10}. Jumps go from {b} to {mid}" + (f", then to {mid + up2}" if up2 else "") + f", then to {a}."
    return Item(f"Count up from {b} to {a} to find {a} − {b}. How much is added in all?", a - b,
                [f"Add the jumps: {up1}" + (f" + {up2}" if up2 else "") + f" + {up3}.", f"That is {a - b}, so {a} − {b} = {a - b}."],
                sub_w(a, b), EX(f"{up1}+{up2}+{up3}"), qtype="compare-strategies", tags={"multiple-representations"},
                diagram=Diagram("jline", {"lo": b // 10 * 10, "hi": -(-a // 10) * 10 if a % 10 else a + 10, "step": 1, "label_every": 10, "jumps": jumps}, alt))


@fam("012", mode="mc")
def s_mc(r, L):
    a, b = subs(r, L)
    it = Item(f"What is {a} − {b}?", a - b, ["Break apart a ten if there are not enough ones.", f"{a} − {b} = {a - b}."], sub_w(a, b), EX(f"{a}-{b}"), mode="mc")
    return it


@fam("12")
def s_tens(r, L):
    a = r.randint(4, 10) * 10
    b = r.randint(11, a - 5)
    need(b % 10)
    return Item(f"Subtract: {a} − {b}", a - b, [f"{a} has 0 ones, so break apart a ten: {a // 10 - 1} tens and 10 ones.", f"{a} − {b} = {a - b}."],
                sub_w(a, b), EX(f"{a}-{b}"), qtype="procedural", claim=f"{a} − {b}")


@fam("2")
def s_digit(r, L):
    a, b = subs(r, 2)
    shown = f"{a // 10}□"
    return Item(f"Find the missing digit: {shown} − {b} = {a - b}", a % 10, [f"{a - b} + {b} = {a}.", f"So the missing digit is {a % 10}."],
                [W((a % 10 + 1) % 10, "made an addition mistake"), W((a - b) % 10, "copied a digit of the answer"), W((b % 10 + (a - b) % 10)  % 10 + 1 if (b % 10 + (a - b) % 10) % 10 + 1 < 10 else 0, "made a counting mistake")],
                FN("missing_digit", shown=shown, other=b, total=a - b, op="−"), qtype="explain", tags={"reasoning"})


# ============================================================== S3 Addition and Subtraction Are Related
def trio(r, L):
    a, b = two(r, L)
    return a, b, a + b


@fam("012", mode="mc")
def rl_check(r, L):
    a, b, s = trio(r, L)
    good = f"{b} + {a} = {s}"
    bad = [f"{s} + {a} = {s + a}", f"{b} − {a} = {b - a}" if b > a else f"{a} − {b} = {a - b}", f"{s} − {b} = {a + 10}"]
    it = mc_key(f"{name(r)} found {s} − {a} = {b}. Which equation checks the answer?", good, bad, ["Add the answer to the number you took away.", f"{b} + {a} = {s}, so the answer is correct."], qtype="conceptual", tags={"connections"}, r=r)
    it.check = FN("check_add", whole=s, part=a, other=b)
    return it


@fam("012")
def rl_add_unknown(r, L):
    a, b, s = trio(r, L)
    eq = f"{a} + ___ = {s}"
    return Item(f"What number makes the equation true? {eq}", b, ["Think subtraction: the total minus the part you know.", f"{s} − {a} = {b}."],
                [W(s + a, "added the numbers shown"), W(b + 10, "made a regrouping mistake"), W(s, "copied the total")],
                FN("blank_eq", eq=eq), qtype="fill-blank", tags={"connections"})


@fam("012")
def rl_sub_unknown(r, L):
    a, b, s = trio(r, L)
    form = pick(r, ["mid", "start"]) if L else "mid"
    eq = f"{s} − ___ = {b}" if form == "mid" else f"___ − {a} = {b}"
    ans = a if form == "mid" else s
    return Item(f"What number makes the equation true? {eq}", ans, ["Use the related addition fact.", f"{eq.replace('___', str(ans))}."],
                [W(s + b if form == "mid" else b - a if b > a else s + 10, "added or subtracted the numbers shown"), W(ans + 10, "made a regrouping mistake"), W(ans - 1, "made a counting mistake")],
                FN("blank_eq", eq=eq), qtype="fill-blank", tags={"connections"})


@fam("01")
def rl_bar(r, L):
    a, b, s = trio(r, L)
    alt = f"A part-part-whole bar. The whole is {s}. One part is {a}. The other part is unknown."
    return Item("Find the missing part of the bar.", b, [f"Missing part = whole − known part: {s} − {a}.", f"{s} − {a} = {b}. Check: {a} + {b} = {s}."],
                sub_w(s, a), EX(f"{s}-{a}"), qtype="visual",
                diagram=Diagram("bars", {"rows": [{"parts": [[s, str(s)]]}, {"parts": [[a, str(a)], [b, "?"]]}]}, alt))


@fam("012", mode="mc")
def rl_correct(r, L):
    a, b, s = trio(r, L)
    ok = r.random() < 0.5
    shown = b if ok else b + pick(r, [10, -10, 1])
    need(shown > 0)
    good = f"{'Yes' if ok else 'No'}. {shown} + {a} = {shown + a}" + ("." if ok else f", not {s}.")
    bad = [f"{'No' if ok else 'Yes'}. {shown} + {a} = {s}." if not ok else f"No. {shown} + {a} = {s + 10}, not {s}.", f"{'Yes' if ok else 'No'}. {shown} − {a} = {abs(shown - a)}.", f"Yes. Subtraction answers cannot be checked."]
    it = mc_key(f"{name(r)} says {s} − {a} = {shown}. Check with addition. Is the answer correct?", good, bad,
                [f"Add {shown} + {a}.", f"{shown} + {a} = {shown + a}" + (f", so the answer is correct." if ok else f", not {s}, so the answer is wrong. It should be {b}.")], qtype="explain", tags={"reasoning"}, r=r)
    it.check = FN("check_claim", whole=s, part=a, shown=shown)
    return it


@fam("12")
def rl_word(r, L):
    a, b, s = trio(r, L)
    tt = pick(r, [("{nm} needs {s} beads to make a necklace. {nm} has {a} beads. How many more beads does {nm} need?", "beads"),
                  ("A book has {s} pages. {nm} has read {a} pages. How many pages are left to read?", "pages")])
    return Item(tt[0].format(s=s, a=a, nm=name(r)), f"{b} {tt[1]}", [f"{a} + ___ = {s}.", f"{s} − {a} = {b} {tt[1]}."],
                [W(f"{w} {tt[1]}", y) for w, y in sub_w(s, a)], EX(f"{s}-{a}", unit=tt[1]), qtype="word-problem", tags={"modeling"})


@fam("2")
def rl_related(r, L):
    a, b, s = trio(r, 2)
    return Item(f"{a} + {b} = {s}. Write a subtraction equation that uses the same three numbers and starts with {s}.", f"{s} − {a} = {b}",
                [f"The whole is {s}; take away one part.", f"{s} − {a} = {b} (or {s} − {b} = {a})."],
                [W(f"{s} − {a} = {b + 10}", "made a regrouping mistake"), W(f"{s} + {a} = {s + a}", "added instead of subtracting")],
                FN("fam_member", nums=[a, b, s]), qtype="explain", tags={"connections"})


# ============================================================== S4 Adding Three or Four Two-Digit Numbers
def addends(r, L, k=None):
    k = k or (3 if L < 2 else pick(r, [3, 4]))
    xs = [r.randint(11, 49 if L < 2 else 59) for _ in range(k)]
    need(sum(xs) <= (100 if L == 0 else 160 if L == 1 else 220))
    return xs


@fam("012")
def f_std(r, L):
    xs = addends(r, L)
    e = " + ".join(map(str, xs))
    return Item(f"Add: {e}", sum(xs), ["Add all the tens, then all the ones, then put them together.", f"{e} = {sum(xs)}."],
                [W(sum(xs[:-1]), "left out an addend"), W(sum(xs) - 10, "forgot a new ten"), W(sum(xs) + 10, "added an extra ten"), W(sum(x // 10 for x in xs) * 10 + sum(x % 10 for x in xs) % 10, "dropped the tens made from the ones")],
                EX("+".join(map(str, xs))), qtype="procedural", claim=e)


@fam("012")
def f_parts(r, L):
    xs = addends(r, L)
    t, o = sum(x // 10 for x in xs) * 10, sum(x % 10 for x in xs)
    e = " + ".join(map(str, xs))
    return Item(f"To add {e}, {name(r)} adds the tens to get {t} and the ones to get {o}. What is the total?", t + o, [f"{t} + {o}.", f"{t} + {o} = {t + o}."],
                [W(t, "left out the ones"), W(t + o - 10, "forgot a new ten"), W(int(f"{t // 10}{o}") if o >= 10 else t + o + 10, "wrote the tens and ones side by side" if o >= 10 else "added an extra ten")],
                EX(f"{t}+{o}"), qtype="compare-strategies", tags={"multiple-representations"})


@fam("012")
def f_word(r, L):
    xs = addends(r, L)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday"][:len(xs)]
    nm = name(r)
    parts = [f"{xs[0]} pages on {days[0]}"] + [f"{x} on {d}" for x, d in zip(xs[1:], days[1:])]
    parts = ", ".join(parts[:-1]) + (", and " if len(parts) > 2 else " and ") + parts[-1]
    return Item(f"{nm} read {parts}. How many pages did {nm} read in all?", f"{sum(xs)} pages",
                [f"Add {' + '.join(map(str, xs))}.", f"{' + '.join(map(str, xs))} = {sum(xs)} pages."],
                [W(f"{sum(xs[:-1])} pages", "left out a day"), W(f"{sum(xs) - 10} pages", "forgot a new ten"), W(f"{sum(xs) + 10} pages", "added an extra ten")],
                EX("+".join(map(str, xs)), unit="pages"), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def f_pair(r, L):
    a = r.randint(11, 39)
    b = 10 * r.randint(1, 3) + (10 - a % 10) % 10
    c = r.randint(11, 39)
    need(a % 10 and (a % 10 + c % 10) % 10 and (b % 10 + c % 10) % 10 and b > 10)
    xs = [a, b, c]
    r.shuffle(xs)
    good = f"{a} + {b}, because the ones make a ten"
    bad = [f"{a} + {c}, because the ones make a ten", f"{b} + {c}, because the ones make a ten", f"{a} + {b} + {c} must be added from left to right"]
    it = mc_key(f"To add {' + '.join(map(str, xs))}, which two numbers are easiest to add first?", good, bad,
                [f"Look for ones digits that make 10: {a % 10} + {b % 10} = 10.", f"{a} + {b} = {a + b}, then add {c} to get {a + b + c}."], qtype="compare-strategies", tags={"reasoning"}, r=r)
    it.check = FN("ten_pair", nums=xs)
    return it


@fam("12")
def f_missing(r, L):
    xs = addends(r, L, 3)
    eq = f"{xs[0]} + {xs[1]} + ___ = {sum(xs)}"
    return Item(f"What number makes the equation true? {eq}", xs[2], [f"{xs[0]} + {xs[1]} = {xs[0] + xs[1]}.", f"{sum(xs)} − {xs[0] + xs[1]} = {xs[2]}."],
                [W(sum(xs) + xs[0] + xs[1] if sum(xs) + xs[0] + xs[1] < 1000 else xs[2] + 1, "added all the numbers"), W(xs[2] + 10, "made a regrouping mistake"), W(xs[0] + xs[1], "added only the first two")],
                FN("blank_eq", eq=eq), qtype="fill-blank", tags={"reasoning"})


@fam("012", mode="mc")
def f_mc(r, L):
    xs = addends(r, L)
    e = " + ".join(map(str, xs))
    return Item(f"What is {e}?", sum(xs), ["Add the tens and the ones.", f"{e} = {sum(xs)}."],
                [W(sum(xs[:-1]), "left out an addend"), W(sum(xs) - 10, "forgot a new ten"), W(sum(xs) + 10, "added an extra ten"), W(sum(xs) + 1, "made a counting mistake")],
                EX("+".join(map(str, xs))), mode="mc")


@fam("2")
def f_four_word(r, L):
    xs = addends(r, 2, 4)
    t = pick(r, [("A school has 4 classes going on a trip. The classes have {a}, {b}, {c}, and {d} students. How many students are going?", "students"),
                 ("{nm} counted birds on 4 days: {a}, {b}, {c}, and {d}. How many birds did {nm} count?", "birds")])
    return Item(t[0].format(a=xs[0], b=xs[1], c=xs[2], d=xs[3], nm=name(r)), f"{sum(xs)} {t[1]}", [f"Add {' + '.join(map(str, xs))}.", f"The total is {sum(xs)} {t[1]}."],
                [W(f"{sum(xs[:3])} {t[1]}", "left out an addend"), W(f"{sum(xs) - 10} {t[1]}", "forgot a new ten"), W(f"{sum(xs) - 20} {t[1]}", "forgot two new tens")],
                EX("+".join(map(str, xs)), unit=t[1]), qtype="word-problem", tags={"modeling", "multistep"})


# ============================================================== S5 Explaining Addition and Subtraction Strategies
@fam("012")
def x_breakapart(r, L):
    a, b = two(r, L)
    bt, bo = b // 10 * 10, b % 10
    need(bo)
    return Item(f"{name(r)} adds {a} + {b} by breaking {b} into {bt} and {bo}. First, {a} + {bt} = {a + bt}. What is {a + bt} + {bo}?", a + b,
                [f"Breaking {b} into tens and ones does not change the total.", f"{a + bt} + {bo} = {a + b}."], add_w(a, b), EX(f"{a + bt}+{bo}"),
                qtype="compare-strategies", tags={"reasoning"})


@fam("012", mode="mc")
def x_order(r, L):
    a, b = two(r, L)
    need(a != b)
    good = f"Yes. Adding in any order gives the same sum: {a} + {b} = {b} + {a} = {a + b}."
    bad = [f"No. {b} + {a} is {a + b + 10}.", f"No. The bigger number must come first.", f"Yes. Both are equal to {a + b - 10}."]
    it = mc_key(f"Is {a} + {b} the same as {b} + {a}?", good, bad, ["Changing the order of the addends does not change the sum.", f"Both are {a + b}."], qtype="explain", tags={"reasoning"}, r=r)
    it.check = FN("order_reason", a=a, b=b)
    return it


@fam("012")
def x_compensate(r, L):
    a, b = two(r, L)
    k = 10 - a % 10
    need(k < 10 and b > k)
    return Item(f"To find {a} + {b}, {name(r)} adds {a + k} + {b - k} instead. What is the sum?", a + b,
                [f"{k} was moved from {b} to {a}, so the total stays the same.", f"{a + k} + {b - k} = {a + b}."],
                [W(a + b + k, "thought the sum got bigger"), W(a + b - k, "thought the sum got smaller"), W(a + b + 2 * k, "added the change twice")],
                EX(f"{a + k}+{b - k}"), qtype="compare-strategies", tags={"reasoning"})


@fam("12")
def x_sub_round(r, L):
    a, b = subs(r, L)
    need(b % 10 >= 7)
    up = 10 - b % 10
    return Item(f"To find {a} − {b}, {name(r)} subtracts {b + up} and then adds {up} back. What is the answer?", a - b,
                [f"{a} − {b + up} = {a - b - up}.", f"{b + up} is {up} more than {b}, so add {up} back: {a - b - up} + {up} = {a - b}."],
                [W(a - b - 2 * up, "subtracted the extra instead of adding it back"), W(a - b - up, "forgot to add back"), W(a - b + 10, "made a regrouping mistake")],
                EX(f"{a}-{b + up}+{up}"), qtype="compare-strategies", tags={"reasoning"})


@fam("012", mode="mc")
def x_error(r, L):
    a, b = subs(r, 2)
    sm = abs(a // 10 - b // 10) * 10 + abs(a % 10 - b % 10)
    nm = name(r)
    good = f"{a - b}. There are not enough ones, so break apart a ten: {a // 10 - 1} tens and {a % 10 + 10} ones."
    bad = [f"{sm}. Subtract the smaller ones digit from the bigger one.", f"{a - b + 10}. Break apart a ten and keep it.", f"{a + b}. Add to check the answer."]
    it = mc_key(f"{nm} says {a} − {b} = {sm} because {b % 10} − {a % 10} = {b % 10 - a % 10}. What is the correct answer and why?", good, bad,
                [f"You cannot take {pl(b % 10, 'one')} from {pl(a % 10, 'one')} without breaking apart a ten.", f"{a} − {b} = {a - b}."], qtype="error-analysis", tags={"misconception"}, r=r)
    it.check = FN("lead_diff", a=a, b=b)
    return it


@fam("2", mode="mc")
def x_same(r, L):
    a, b = two(r, 2)
    need(b % 10 >= 6)
    up = 10 - b % 10
    good = f"{a} + {b + up} − {up}"
    bad = [f"{a} + {b + up} + {up}", f"{a} + {b - b % 10}", f"{a + up} + {b + up}"]
    it = mc_key(f"Which has the same value as {a} + {b}?", good, bad, [f"{b} = {b + up} − {up}.", f"So {a} + {b} = {good} = {a + b}."], qtype="compare-strategies", tags={"reasoning"}, r=r)
    it.check = FN("same_value", target=f"{a}+{b}")
    return it


@fam("012")
def x_countup(r, L):
    a, b = subs(r, L)
    need(b % 10 and a % 10)
    up1 = 10 - b % 10
    up2 = a // 10 * 10 - (b + up1)
    up3 = a % 10
    need(up2 > 0)
    return Item(f"{name(r)} finds {a} − {b} by counting up: {b} + {up1} = {b + up1}, {b + up1} + {up2} = {b + up1 + up2}, {b + up1 + up2} + {up3} = {a}. What is {a} − {b}?", a - b,
                [f"Add the amounts counted up: {up1} + {up2} + {up3}.", f"{up1} + {up2} + {up3} = {a - b}."],
                [W(a, "gave where the counting stopped"), W(up2, "used only the biggest jump"), W(a - b + 10, "made a regrouping mistake")],
                EX(f"{up1}+{up2}+{up3}"), qtype="compare-strategies", tags={"reasoning"})


SKILLS = {
    1: dict(name="Adding within 100", fams=[a_std, a_parts, a_blocks, a_word, a_jump, a_friendly, a_digit]),
    2: dict(name="Subtracting within 100", fams=[s_std, s_word, s_blocks, s_countup, s_mc, s_tens, s_digit]),
    3: dict(name="Addition and Subtraction Are Related", fams=[rl_check, rl_add_unknown, rl_sub_unknown, rl_bar, rl_correct, rl_word, rl_related]),
    4: dict(name="Adding Three or Four Two-Digit Numbers", fams=[f_std, f_parts, f_word, f_pair, f_missing, f_mc, f_four_word]),
    5: dict(name="Explaining Addition and Subtraction Strategies", fams=[x_breakapart, x_order, x_compensate, x_sub_round, x_error, x_same, x_countup]),
}
