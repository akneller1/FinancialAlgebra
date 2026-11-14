"""Unit 6: Tens and Ones (tens-ones). 1.NBT.B.2, 1.NBT.B.2.a, 1.NBT.B.2.b, 1.NBT.B.2.c."""
from g1lib import *

UNIT_ID = "tens-ones"


def TO(t, o):
    return f"{pl(t, 'ten')} and {pl(o, 'one')}"


def to_wrongs(n):
    t, o = n // 10, n % 10
    out = []
    if o != t:
        out.append(W(TO(o, t), "switched the tens and the ones"))
    out += [W(TO(t + 1, o), "counted one ten too many"), W(TO(t, o + 1) if o < 9 else TO(t, o - 1), "counted the ones wrong"), W(TO(0, n) if n < 20 else TO(t - 1, o), "did not make a ten" if n < 20 else "missed a ten")]
    return out


# ============================================================== S1 A Ten Is Ten Ones
@fam("012")
def a_groups(r, L):
    n = r.randint(10, 19) if L == 0 else r.randint(20, 39) if L == 1 else r.randint(40, 69)
    alt = f"{n} counters in rows of 10."
    return Item(pick(r, ["Make groups of ten. How many tens and how many ones are there?", "How many tens and ones do the counters show?"]), TO(n // 10, n % 10),
                ["Each full row of 10 is one ten.", f"{n} is {TO(n // 10, n % 10)}."], to_wrongs(n), FN("tens_ones", n=n), qtype="visual",
                diagram=Diagram("crossrow", {"n": n, "per": 10, "color": "blue"}, alt))


@fam("012")
def a_ones_in(r, L):
    t = 1 if L == 0 else r.randint(2, 5) if L == 1 else r.randint(5, 9)
    if L == 0:
        p = pick(r, ["How many ones make 1 ten?", "1 ten is the same as how many ones?", "How many cubes are in a tower of ten?"])
        return Item(p, 10, ["A ten is a bundle of ten ones.", "1 ten = 10 ones."],
                    [W(1, "thought a ten is one"), W(100, "thought a ten is 100"), W(9, "counted one too few"), W(11, "counted one too many")], EX("10"), qtype="conceptual")
    return Item(pick(r, [f"How many ones are in {t} tens?", f"{t} tens is the same as how many ones?"]), 10 * t, [f"Each ten is 10 ones.", f"{t} tens = {10 * t} ones."],
                [W(t, "counted each ten as one"), W(t + 10, "added 10"), W(10 * t + 1, "counted one too many"), W(100 * t, "thought each ten is 100")], EX(f"10*{t}"), qtype="conceptual")


@fam("012")
def a_bundle(r, L):
    n = r.randint(11, 19) if L == 0 else r.randint(21, 49) if L == 1 else r.randint(50, 99)
    th = pick(r, [("straw", "straws"), ("stick", "sticks"), ("cube", "cubes")])
    return Item(f"{name(r)} has {n} {th[1]} and makes bundles of 10. How many bundles of 10 can be made?", n // 10,
                [f"{n} is {TO(n // 10, n % 10)}.", f"So {n // 10} bundle{'s' if n >= 20 else ''} of 10 can be made, with {n % 10} left."],
                [W(n % 10, "gave the ones left over"), W(n // 10 + 1, "counted one bundle too many"), W(n, "gave the number of sticks"), W(10, "thought every bundle count is 10")],
                FN("tens_in", n=n // 10 * 10), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def a_which(r, L):
    if L == 0:
        good, bad, p = "10 ones", ["1 one", "100 ones", "5 ones"], "Which is the same as 1 ten?"
    elif L == 1:
        t = r.randint(2, 9)
        good, bad, p = f"{t * 10} ones", [f"{t} ones", f"{t + 10} ones", f"{t}0{t} ones"], f"Which is the same as {t} tens?"
    else:
        t = r.randint(2, 8)
        o = r.randint(10, 19)
        n = 10 * t + o
        good, bad, p = f"{n}", [f"{t}{o}", f"{t + o}", f"{10 * t + o - 10}"], f"What number is {t} tens and {o} ones?"
        it = mc_key(p, good, bad, [f"{o} ones is 1 ten and {o - 10} ones.", f"{t} tens and {o} ones = {n}."], qtype="conceptual", r=r)
        it.check = FN("count_n", n=n)
        return it
    return mc_key(p, good, bad, ["A ten is ten ones.", f"The answer is {good}."], qtype="conceptual", r=r)


@fam("12")
def a_trade(r, L):
    t, o = (r.randint(1, 4), r.randint(10, 15)) if L == 1 else (r.randint(3, 7), r.randint(12, 19))
    n = 10 * t + o
    eq = f"{t} tens and {o} ones = {t + 1} tens and ___ ones"
    return Item(f"Trade 10 ones for 1 ten. {eq}", o - 10, [f"{o} ones is 1 ten and {o - 10} ones.", f"So it is {t + 1} tens and {o - 10} ones, which is {n}."],
                [W(o, "did not trade"), W(o + 10, "added a ten to the ones"), W(10, "wrote the ten"), W(o - 9, "made a counting mistake")],
                EX(f"{o}-10"), qtype="conceptual", tags={"reasoning"})


@fam("0")
def a_frame(r, L):
    o = r.randint(0, 9)
    alt = f"Two ten frames. The first is full. The second has {o} counters."
    return Item("How many tens and ones do the ten frames show?", TO(1, o), ["The full ten frame is 1 ten.", f"There are {o} more ones, so it is {10 + o}."],
                to_wrongs(10 + o), FN("tens_ones", n=10 + o), qtype="visual", diagram=Diagram("tenframe", {"frames": 2, "a": 10 + o}, alt))


# ============================================================== S2 Teen Numbers
@fam("012")
def tn_build(r, L):
    o = r.randint(1, 9)
    forms = ([f"What number is 1 ten and {pl(o, 'one')}?", f"10 + {o} = ___"] if L == 0 else
             [f"What number is 1 ten and {pl(o, 'one')}?", f"10 + {o} = ___", f"{o} + 10 = ___"] if L == 1 else
             [f"What number is {pl(o, 'one')} and 1 ten?", f"{o} ones plus 1 ten is what number?", f"___ = {o} + 10"])
    p = pick(r, forms)
    return Item(p, 10 + o, [f"1 ten is 10. 10 and {o} more is {10 + o}.", f"The number is {10 + o}."],
                [W(10 * o + 1, "switched the tens and the ones"), W(o, "left out the ten"), W(11 + o, "counted one too many"), W(f"10{o}", "wrote 10 and then the ones")],
                EX(f"10+{o}"), claim=p if "___" in p else None)


@fam("012")
def tn_split(r, L):
    o = r.randint(1, 9)
    n = 10 + o
    eq = pick(r, [f"{n} = 10 + ___", f"{n} = 1 ten and ___ ones"] if L < 2 else [f"{n} = ___ + {o}", f"{n} − 10 = ___", f"{n} − {o} = ___"])
    ans = o if "10 +" in eq or "1 ten" in eq or "− 10" in eq else 10
    return Item(pick(r, [f"Fill in the blank: {eq}", f"What number goes in the blank? {eq}"]), ans,
                [f"{n} is 1 ten and {o} ones.", f"{n} = 10 + {o}."],
                [W(n, "copied the number"), W(1, "wrote the tens digit"), W(n + 10 if ans == 10 else o + 1, "made a mistake with the ten" if ans == 10 else "counted one too many"), W(o + 10 if ans != 10 else o, "mixed up the ten and the ones")],
                FN("blank_eq", eq=eq.replace("1 ten and ___ ones", "10 + ___")), claim=eq)


@fam("012")
def tn_frames(r, L):
    o = r.randint(1, 9)
    alt = f"Two ten frames. The first is full. The second has {o} counters."
    p = pick(r, ["What teen number do the ten frames show?", "Write the number shown in the ten frames."] if L < 2 else
             ["How many more counters are needed to make 20?", "What number is shown? How many ones is that in all?"])
    if "make 20" in p:
        return Item(p, 10 - o, [f"The frames show {10 + o}.", f"{10 + o} + {10 - o} = 20."],
                    [W(10 + o, "gave the number shown"), W(o, "counted the second frame"), W(11 - o, "counted one too many"), W(20, "gave the total")],
                    FN("blank_eq", eq=f"{10 + o} + ___ = 20"), qtype="visual", diagram=Diagram("tenframe", {"frames": 2, "a": 10 + o}, alt))
    return Item(p, 10 + o, ["The full frame is 10.", f"10 and {o} more is {10 + o}."],
                [W(o, "left out the full ten frame"), W(10 * o + 1, "switched the tens and the ones"), W(11 + o, "counted one too many"), W(9 + o, "counted one too few")],
                FN("count_n", n=10 + o), qtype="visual", diagram=Diagram("tenframe", {"frames": 2, "a": 10 + o}, alt))


@fam("012", mode="mc")
def tn_which(r, L):
    o = r.randint(1, 9)
    need(o != 1)
    n = 10 + o
    if L < 2:
        p = pick(r, [f"Which number is 1 ten and {o} ones?", f"Which number is {words(n)}?"])
        good, bad = str(n), [f"{o}1", str(o), f"10{o}"]
    else:
        p = f"Which is the same as {n}?"
        good, bad = f"{o} ones and 1 ten", [f"{o} tens and 1 one", f"1 ten and {o + 1} ones", f"{n} tens"]
    it = mc_key(p, good, bad, [f"{n} has 1 ten and {o} ones.", f"The answer is {good}."], qtype="conceptual", r=r)
    if L < 2:
        it.check = FN("count_n", n=n)
    return it


@fam("012")
def tn_word(r, L):
    o = r.randint(1, 9)
    th = thing(r)
    return Item(f"{name(r)} has a pack of 10 {th[1]} and {o} loose {th[1]}. How many {th[1]} is that?", f"{10 + o} {th[1]}",
                [f"The pack is 1 ten. {o} loose {th[1]} are {o} ones.", f"10 + {o} = {10 + o}."],
                [W(f"{o + 1} {th[1]}", "counted the pack as 1"), W(f"{10 * o + 1} {th[1]}", "switched the tens and the ones"), W(f"{o} {th[1]}", "left out the pack"), W(f"{11 + o} {th[1]}", "counted one too many")],
                EX(f"10+{o}", unit=th[1]), qtype="word-problem", tags={"modeling"})


@fam("2")
def tn_riddle(r, L):
    o = r.randint(2, 8)
    k = pick(r, [1, 2])
    up = r.random() < 0.5
    need(1 <= o + (k if up else -k) <= 9)
    n = 10 + o + (k if up else -k)
    return Item(f"I am a teen number. I have {k} {'more' if up else 'fewer'} ones than {10 + o}. What number am I?", n,
                [f"{10 + o} has {o} ones.", f"{o} {'+' if up else '−'} {k} = {o + (k if up else -k)} ones, so the number is {n}."],
                [W(10 + o, "gave the starting number"), W(10 + o + (-k if up else k), "went the wrong way"), W(o + (k if up else -k), "left out the ten"), W(n + 10, "added a ten")],
                EX(f"{10 + o}{'+' if up else '-'}{k}"), qtype="explain", tags={"reasoning"})


# ============================================================== S3 Counting by Tens
@fam("012")
def ct_tens_in(r, L):
    t = r.randint(1, 5) if L == 0 else r.randint(2, 9)
    p = pick(r, [f"How many tens are in {10 * t}?", f"{10 * t} is how many tens?"] if L < 2 else [f"{10 * t} = ___ tens and 0 ones", f"How many tens and ones make {10 * t}? Write the number of tens."])
    return Item(p, t, [f"{10 * t} has {t} in the tens place and 0 ones.", f"{10 * t} = {t} tens."],
                [W(10 * t, "copied the number"), W(t + 1, "counted one ten too many"), W(0, "gave the ones"), W(t * 100 if t < 2 else t - 1, "counted the tens wrong")], FN("tens_in", n=10 * t))


@fam("012")
def ct_num(r, L):
    t = r.randint(1, 5) if L == 0 else r.randint(2, 9)
    p = pick(r, [f"What number is {pl(t, 'ten')}?", f"{pl(t, 'ten')} and 0 ones is what number?"] if L < 2 else [f"What number is {pl(t, 'ten')} and 0 ones? Write it in words.", f"Write the number word for {pl(t, 'ten')}."])
    if "word" in p:
        return Item(p, words(10 * t), [f"{t} tens is {10 * t}.", f"{10 * t} is {words(10 * t)}."],
                    [W(words(t), "wrote the ones word"), W(words(10 * t + 10) if t < 9 else words(10 * t - 10), "counted one ten wrong"), W(words(10 + t) if t > 1 else "eleven", "mixed up teen and ten words")],
                    FN("num_word", n=10 * t))
    return Item(p, 10 * t, [f"Count by tens: " + ", ".join(str(10 * j) for j in range(1, t + 1)) + ".", f"{pl(t, 'ten')} = {10 * t}."],
                [W(t, "wrote the number of tens"), W(10 * t + 10, "counted one ten too many"), W(t * 100, "added two zeros"), W(10 + t, "made a teen number")], EX(f"10*{t}"))


@fam("012")
def ct_seq(r, L):
    if L < 2:
        s = r.randint(1, 5) * 10
        seq = [s, s + 10, s + 20]
    else:
        s = r.randint(11, 59)
        need(s % 10)
        seq = [s, s + 10, s + 20]
    nxt = seq[-1] + 10
    return Item(pick(r, [f"Count by tens. What comes next? {', '.join(map(str, seq))}, ___", f"Skip count by 10: {', '.join(map(str, seq))}, ___"]), nxt,
                ["Each number is 10 more.", f"{seq[-1]} + 10 = {nxt}."],
                [W(seq[-1] + 1, "counted by ones"), W(seq[-1] + 20, "skipped a ten"), W(seq[-1], "repeated the last number"), W(seq[-1] + 5, "counted by fives")],
                FN("count_words", start=nxt, n=1, step=10))


@fam("012")
def ct_rods(r, L):
    t = r.randint(1, 4) if L == 0 else r.randint(3, 9)
    alt = f"Base-ten blocks: {t} tens rods."
    return Item(pick(r, ["Each rod is 10. What number do the rods show?", "Count the rods by tens. How many cubes are there?"]), 10 * t,
                [f"Count by tens: {', '.join(str(10 * k) for k in range(1, t + 1))}.", f"{t} tens = {10 * t}."],
                [W(t, "counted each rod as 1"), W(10 * t + 10, "counted a rod twice"), W(10 * t - 10, "missed a rod"), W(10 * t + 1, "counted one too many")],
                FN("count_n", n=10 * t), qtype="visual", diagram=Diagram("blocks", {"t": t, "o": 0}, alt))


@fam("012", mode="mc")
def ct_which(r, L):
    t = r.randint(2, 9)
    good = str(10 * t)
    bad = [str(t), f"{t}00", str(10 + t)]
    p = pick(r, [f"Which number is {t} tens and 0 ones?", f"Which number is {words(10 * t)}?"])
    it = mc_key(p, good, bad, [f"{t} tens = {10 * t}.", f"The answer is {10 * t}."], qtype="conceptual", r=r)
    it.check = FN("count_n", n=10 * t)
    return it


@fam("12")
def ct_word(r, L):
    t = r.randint(2, 6) if L == 1 else r.randint(5, 9)
    th = thing(r)
    return Item(f"There are {t} boxes. Each box has 10 {th[1]}. How many {th[1]} are there?", f"{10 * t} {th[1]}",
                [f"Count by tens: " + ", ".join(str(10 * j) for j in range(1, t + 1)) + ".", f"{pl(t, 'ten')} = {10 * t}."],
                [W(f"{t} {th[1]}", "counted each box as 1"), W(f"{10 * t + 10} {th[1]}", "counted one box twice"), W(f"{10 + t} {th[1]}", "added instead of counting by tens"), W(f"{10 * t - 10} {th[1]}", "missed a box")],
                EX(f"10*{t}", unit=th[1]), qtype="word-problem", tags={"modeling"})


# ============================================================== S4 Tens and Ones in Two-Digit Numbers
def tn(r, L):
    if L == 0:
        return r.randint(2, 5) * 10 + r.randint(0, 9)
    if L == 1:
        return r.randint(20, 99)
    n = r.randint(21, 99)
    need(n % 10 != n // 10)
    return n


@fam("012")
def t_split(r, L):
    n = tn(r, L)
    need(n % 10 != n // 10 or L == 0)
    return Item(pick(r, [f"How many tens and ones are in {n}?", f"Write {n} as tens and ones.", f"{n} is how many tens and how many ones?"]), TO(n // 10, n % 10),
                [f"The tens digit is {n // 10} and the ones digit is {n % 10}.", f"{n} = {TO(n // 10, n % 10)}."], to_wrongs(n), FN("tens_ones", n=n))


@fam("012")
def t_build(r, L):
    n = tn(r, L)
    t, o = n // 10, n % 10
    p = pick(r, [f"What number is {TO(t, o)}?", f"Write the number: {TO(t, o)}."] if L < 2 else [f"What number is {pl(o, 'one')} and {pl(t, 'ten')}?", f"Write the number: {pl(o, 'one')} and {pl(t, 'ten')}."])
    return Item(p, n, [f"{t} tens is {10 * t}.", f"{10 * t} + {o} = {n}."],
                [W(10 * o + t, "switched the tens and the ones") if o and o != t else W(n + 1, "counted one too many"), W(t + o, "added the digits"), W(f"{t}0{o}", "wrote the tens and ones as they sound"), W(n + 10, "counted one ten too many")],
                EX(f"10*{t}+{o}"))


@fam("012")
def t_blocks(r, L):
    n = tn(r, L)
    t, o = n // 10, n % 10
    alt = f"Base-ten blocks: {t} tens rods and {o} ones cubes."
    if L == 2 and r.random() < 0.5:
        return Item("How many tens and ones do the blocks show?", TO(t, o), [f"Count the rods: {t}. Count the cubes: {o}.", f"{n} = {TO(t, o)}."],
                    to_wrongs(n), FN("tens_ones", n=n), qtype="visual", diagram=Diagram("blocks", {"t": t, "o": o}, alt))
    return Item(pick(r, ["What number do the blocks show?", "Count the tens and ones. What is the number?"]), n,
                [f"{t} tens and {o} ones.", f"That is {n}."],
                [W(10 * o + t if o and o != t else n + 1, "switched the tens and the ones" if o and o != t else "counted one too many"), W(t + o, "counted each rod as 1"), W(n + 10, "counted a rod twice"), W(n - 1 if o else n + 2, "made a counting mistake")],
                FN("count_n", n=n), qtype="visual", diagram=Diagram("blocks", {"t": t, "o": o}, alt))


@fam("012")
def t_digit(r, L):
    n = tn(r, L)
    need(n % 10 != n // 10)
    place = pick(r, ["tens", "ones"])
    v = n // 10 if place == "tens" else n % 10
    p = pick(r, [f"What digit is in the {place} place in {n}?", f"How many {place} are in {n}?"])
    return Item(p, v, [f"In {n}, the tens digit is {n // 10} and the ones digit is {n % 10}.", f"The {place} digit is {v}."],
                [W(n % 10 if place == "tens" else n // 10, "mixed up the tens and ones places"), W(n, "wrote the whole number"), W(10 * v if v else v + 1, "wrote the value, not the digit" if v else "made a mistake"), W(v + 1, "counted one too many")],
                FN("place_digit", n=n, place=place))


@fam("012", mode="mc")
def t_which(r, L):
    n = tn(r, L)
    t, o = n // 10, n % 10
    need(o != t and o != 0)
    good = str(n)
    bad = [str(10 * o + t), str(t + o), f"{t}0{o}"]
    it = mc_key(pick(r, [f"Which number has {TO(t, o)}?", f"Which number has {o} ones and {t} tens?"]), good, bad, [f"{t} tens and {o} ones is {n}.", f"The answer is {n}."], qtype="conceptual", r=r)
    it.check = FN("count_n", n=n)
    return it


@fam("2")
def t_other(r, L):
    n = r.randint(23, 89)
    t, o = n // 10, n % 10
    k = r.randint(1, t - 1) if t > 1 else 1
    eq = f"{n} = {pl(t - k, 'ten')} and ___ ones"
    return Item(f"{n} can be shown in more than one way. {eq}", 10 * k + o, [f"{n} = {TO(t, o)}.", f"Break {k} ten{'s' if k > 1 else ''} into ones: {10 * k} + {o} = {10 * k + o} ones."],
                [W(o, "did not break a ten into ones"), W(k + o, "broke a ten into 1 one"), W(10 * k, "forgot the ones already there"), W(n, "copied the number")],
                EX(f"{n}-10*{t - k}"), qtype="conceptual", tags={"reasoning"})


SKILLS = {
    1: dict(name="A Ten Is Ten Ones", fams=[a_groups, a_ones_in, a_bundle, a_which, a_trade, a_frame]),
    2: dict(name="Teen Numbers", fams=[tn_build, tn_split, tn_frames, tn_which, tn_word, tn_riddle]),
    3: dict(name="Counting by Tens", fams=[ct_tens_in, ct_num, ct_seq, ct_rods, ct_which, ct_word]),
    4: dict(name="Tens and Ones in Two-Digit Numbers", fams=[t_split, t_build, t_blocks, t_digit, t_which, t_other]),
}
