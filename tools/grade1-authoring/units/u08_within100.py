"""Unit 8: Adding and Subtracting within 100 (add-subtract-100). 1.NBT.C.4, 1.NBT.C.5, 1.NBT.C.6."""
from g1lib import *

UNIT_ID = "add-subtract-100"


def U(n, th):
    return f"{n} {th[0] if n == 1 else th[1]}"


# ============================================================== S1 10 More and 10 Less
def tm_n(r, L, up):
    n = r.randint(10, 59) if L == 0 else r.randint(10, 89) if L == 1 else r.randint(10, 99)
    if up:
        need(n + 10 <= (99 if L < 2 else 109))
    else:
        need(n - 10 >= (10 if L < 2 else 0))
    if L == 0:
        need(n % 10 != 0)
    return n


def tm_w(n, up):
    m = n + 10 if up else n - 10
    out = [W(n + 1 if up else n - 1, "changed the ones digit"), W(n - 10 if up else n + 10, "went the wrong way"), W(n, "did not change the number")]
    out.append(W(n + 100 if up else (n - 1 if n % 10 else n + 1), "added 100" if up else "counted back by ones"))
    out.append(W(m + 1, "made a counting mistake"))
    return out


@fam("012")
def tm_fact(r, L):
    up = r.random() < 0.5
    n = tm_n(r, L, up)
    m = n + 10 if up else n - 10
    p = pick(r, [f"What is 10 {'more' if up else 'less'} than {n}?", f"What number is 10 {'more' if up else 'less'} than {n}?", f"Find 10 {'more' if up else 'less'} than {n}."])
    return Item(p, m, [f"10 {'more' if up else 'less'} changes the tens digit by 1. The ones stay {n % 10}.", f"10 {'more' if up else 'less'} than {n} is {m}."],
                tm_w(n, up), EX(f"{n}{'+' if up else '-'}10"), claim=f"10 {'more' if up else 'less'} than {n}")


@fam("012")
def tm_eq(r, L):
    up = r.random() < 0.5
    n = tm_n(r, L, up)
    eq = (f"{n} + 10 = ___" if up else f"{n} − 10 = ___") if L < 2 else (pick(r, [f"___ = {n} + 10", f"{n + 10} = ___ + 10"]) if up else pick(r, [f"___ = {n} − 10", f"___ + 10 = {n}"]))
    for x in range(0, 120):
        if eval(eq.replace("___", str(x)).replace("−", "-").replace("=", "==")):
            ans = x
            break
    return Item(pick(r, [f"Fill in the blank: {eq}", f"What number makes this true? {eq}"]), ans, ["Only the tens digit changes by 1.", f"{eq.replace('___', str(ans))}."],
                [W(ans + 1, "changed the ones digit"), W(ans + 20 if ans + 20 < 120 else ans - 20, "changed the tens by 2"), W(ans - 9 if ans >= 9 else ans + 9, "made a mistake with tens and ones"), W(n, "copied the number")],
                FN("blank_eq", eq=eq), claim=eq)


@fam("012")
def tm_blocks(r, L):
    up = r.random() < 0.5
    n = tm_n(r, L, up)
    need(n < 100)
    alt = f"Base-ten blocks: {n // 10} tens rods and {n % 10} ones cubes."
    return Item(f"The blocks show a number. What number is 10 {'more' if up else 'less'}?", n + 10 if up else n - 10,
                [f"The blocks show {n}. {'Add' if up else 'Take away'} one rod.", f"The new number is {n + 10 if up else n - 10}."], tm_w(n, up),
                EX(f"10*{n // 10}+{n % 10}{'+' if up else '-'}10"), qtype="visual", diagram=Diagram("blocks", {"t": n // 10, "o": n % 10}, alt))


@fam("012")
def tm_chart(r, L):
    row0 = r.randint(1, 7) * 10 + 1 if L < 2 else r.randint(5, 8) * 10 + 1
    v = row0 + r.randint(0, 9)
    up = r.random() < 0.5
    alt = f"Part of a hundred chart from {row0} to {row0 + 29}. Some boxes are empty."
    m = v + 10 if up else v - 10
    need(row0 <= m <= row0 + 29 and row0 <= v <= row0 + 29)
    blank = [x for x in range(row0, row0 + 30) if x in (m,)]
    return Item(f"On the hundred chart, what number is just {'below' if up else 'above'} {v}?", m,
                [f"Moving {'down' if up else 'up'} one row is 10 {'more' if up else 'less'}.", f"{v} {'+' if up else '−'} 10 = {m}."], tm_w(v, up),
                EX(f"{v}{'+' if up else '-'}10"), qtype="visual", diagram=Diagram("chart", {"start": row0, "per_row": 10, "rows": 3, "blank": blank}, alt))


@fam("012", mode="mc")
def tm_mc(r, L):
    up = r.random() < 0.5
    n = tm_n(r, L, up)
    m = n + 10 if up else n - 10
    return Item(f"Which number is 10 {'more' if up else 'less'} than {n}?", m, ["Change only the tens digit.", f"The answer is {m}."], tm_w(n, up), EX(f"{n}{'+' if up else '-'}10"))


@fam("12")
def tm_word(r, L):
    n = tm_n(r, L, True)
    th, nm = thing(r), name(r)
    up = r.random() < 0.6
    if not up:
        need(n >= 20)
    t = (f"{nm} has {U(n, th)}. {nm} gets a pack of 10 more. How many {th[1]} does {nm} have now?" if up else
         f"{nm} has {U(n, th)}. {nm} gives a pack of 10 to a friend. How many {th[1]} does {nm} have now?")
    m = n + 10 if up else n - 10
    return Item(t, U(m, th), [f"10 {'more' if up else 'less'} than {n}.", f"{n} {'+' if up else '−'} 10 = {m}."], [W(U(x, th), y) for x, y in tm_w(n, up)],
                EX(f"{n}{'+' if up else '-'}10", unit=th[1]), qtype="word-problem", tags={"modeling"})


@fam("2", mode="mc")
def tm_why(r, L):
    n = r.randint(21, 88)
    need(n % 10)
    good = f"{n + 10}, because the tens go up by 1 and the ones stay {n % 10}."
    bad = [f"{n + 1}, because the ones go up by 1.", f"{n + 100}, because 10 more adds a zero.", f"{n + 10}, because the ones go up by 10."]
    return mc_key(f"What is 10 more than {n}, and why?", good, bad, [f"{n} has {n // 10} tens. 10 more has {n // 10 + 1} tens.", good], qtype="explain", tags={"reasoning"}, r=r)


# ============================================================== S2 Adding and Subtracting Tens
def dec(r, L):
    if L == 0:
        a, b = r.randint(1, 5) * 10, r.randint(1, 4) * 10
        need(a + b <= 90)
    elif L == 1:
        a, b = r.randint(1, 8) * 10, r.randint(1, 8) * 10
        need(a + b <= 90)
    else:
        a, b = r.randint(2, 8) * 10, r.randint(2, 7) * 10
        need(a + b <= 100 or True)
        need(a + b <= 90)
    return a, b


@fam("012")
def d_add(r, L):
    a, b = dec(r, L)
    if L >= 1 and r.random() < 0.5:
        o = r.randint(1, 9)
        a += o
        need(a + b <= 99)
    return Item(pick(r, [f"What is {a} + {b}?", f"Add: {a} + {b} = ___", f"Find the sum of {a} and {b}."]), a + b,
                [f"Add the tens: {a // 10} tens + {b // 10} tens = {a // 10 + b // 10} tens.", f"{a} + {b} = {a + b}."],
                [W(a // 10 + b // 10 if a % 10 == 0 else a + b // 10, "added digits instead of tens" if a % 10 == 0 else "added the tens to the ones"),
                 W(a + b + 10, "counted one ten too many"), W(a + b - 10, "counted one ten too few"), W(abs(a - b), "subtracted instead of adding")],
                EX(f"{a}+{b}"), claim=f"{a} + {b}")


@fam("012")
def d_sub(r, L):
    a, b = dec(r, L)
    w = a + b
    return Item(pick(r, [f"What is {w} − {b}?", f"Subtract: {w} − {b} = ___", f"Take {b} away from {w}. What is left?"]), a,
                [f"{w // 10} tens − {b // 10} tens = {a // 10} tens.", f"{w} − {b} = {a}."],
                [W(a // 10, "wrote the number of tens, not the number"), W(w + b, "added instead of subtracting"), W(a + 10, "counted one ten too few"), W(a - 10 if a > 10 else a + 20, "made a mistake with the tens")],
                EX(f"{w}-{b}"), claim=f"{w} − {b}")


@fam("012")
def d_blocks(r, L):
    a, b = dec(r, L)
    o = 0 if L == 0 else r.randint(1, 9)
    need(a + o + b <= 99)
    alt = f"Base-ten blocks: {(a + o) // 10} tens rods and {o} ones cubes."
    return Item(f"The blocks show a number. Add {b} to it. What is the sum?", a + o + b,
                [f"The blocks show {a + o}. Add {b // 10} more tens.", f"{a + o} + {b} = {a + o + b}."],
                [W(a + o + b // 10, "added the tens as ones"), W(a + o + b + 10, "counted one ten too many"), W(a + o, "did not add"), W(a + b, "lost the ones") if o else W(a + b - 10, "counted one ten too few")],
                EX(f"10*{(a + o) // 10}+{o}+{b}"), qtype="visual", diagram=Diagram("blocks", {"t": (a + o) // 10, "o": o}, alt))


@fam("012")
def d_word(r, L):
    a, b = dec(r, L)
    th, nm = thing(r), name(r)
    if r.random() < 0.5:
        return Item(f"{nm} has {U(a, th)}. {nm} gets {b} more. How many {th[1]} does {nm} have now?", U(a + b, th),
                    [f"Add tens: {a} + {b}.", f"{a} + {b} = {a + b}."],
                    [W(U(a + b - 10, th), "counted one ten too few"), W(U(abs(a - b), th), "subtracted instead of adding"), W(U(a // 10 + b // 10, th), "added the tens digits only"), W(U(a + b + 10, th), "counted one ten too many")],
                    EX(f"{a}+{b}", unit=th[1]), qtype="word-problem", tags={"modeling"})
    w = a + b
    return Item(f"{nm} has {U(w, th)}. {nm} gives away {b}. How many {th[1]} are left?", U(a, th), [f"Subtract tens: {w} − {b}.", f"{w} − {b} = {a}."],
                [W(U(w + b, th), "added instead of subtracting"), W(U(a // 10, th), "wrote the number of tens"), W(U(a + 10, th), "counted one ten too few"), W(U(b, th), "gave the number given away")],
                EX(f"{w}-{b}", unit=th[1]), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def d_mc(r, L):
    a, b = dec(r, L)
    w = a + b
    return Item(pick(r, [f"Which is the answer to {w} − {b}?", f"Choose the difference: {w} − {b}"]), a, [f"{w // 10} tens − {b // 10} tens.", f"{w} − {b} = {a}."],
                [W(a // 10, "wrote the number of tens"), W(w + b, "added instead of subtracting"), W(a + 10, "counted one ten too few"), W(a - 10 if a > 10 else a + 20, "made a mistake with the tens")],
                EX(f"{w}-{b}"))


@fam("2")
def d_missing(r, L):
    a, b = dec(r, 2)
    w = a + b
    eq = pick(r, [f"{a} + ___ = {w}", f"{w} − ___ = {a}", f"___ − {b} = {a}", f"___ + {b} = {w}"])
    ans = w if eq.startswith("___ −") else (b if ("+ ___" in eq or "− ___" in eq) else a)
    return Item(f"What number makes this true? {eq}", ans, ["Think in tens.", f"{eq.replace('___', str(ans))} is true."],
                [W(ans // 10, "wrote the number of tens"), W(ans + 10, "counted one ten too many"), W(w + a if ans != w else a, "added the numbers shown" if ans != w else "copied a number"), W(ans - 10, "counted one ten too few")],
                FN("blank_eq", eq=eq), claim=eq)


# ============================================================== S3 Adding a Two-Digit and a One-Digit Number (no new ten)
def no_new(r, L):
    if L == 0:
        a = r.randint(11, 45)
        b = r.randint(1, 5)
    elif L == 1:
        a = r.randint(21, 85)
        b = r.randint(2, 8)
    else:
        a = r.randint(41, 92)
        b = r.randint(3, 8)
    need(a % 10 + b <= 9 and a % 10 != 0 or (a % 10 == 0 and L == 0))
    need(a % 10 + b <= 9)
    return a, b


def nn_w(a, b, u=""):
    s = a + b
    u = (" " + u) if u else ""
    return [W(f"{a + 10 * b}{u}", "added the ones to the tens"), W(f"{s + 10}{u}", "added an extra ten"), W(f"{s - 1}{u}", "counted on and included the first number"),
            W(f"{s + 1}{u}", "counted one too many"), W(f"{a // 10 + a % 10 + b}{u}", "added all the digits")]


@fam("012")
def n_fact(r, L):
    a, b = no_new(r, L)
    eq = pick(r, [f"{a} + {b}", f"{b} + {a}"]) if L > 0 else f"{a} + {b}"
    return Item(pick(r, [f"What is {eq}?", f"Add: {eq} = ___", f"Find the sum: {eq}"]), a + b,
                [f"Add the ones: {a % 10} + {b} = {a % 10 + b}. Keep the {a // 10} tens.", f"{eq} = {a + b}."], nn_w(a, b), EX(eq.replace(" ", "")), claim=eq)


@fam("012")
def n_blocks(r, L):
    a, b = no_new(r, L)
    alt = f"Base-ten blocks: {a // 10} tens rods and {a % 10} ones cubes."
    return Item(f"The blocks show a number. Add {b} more ones. What is the sum?", a + b, [f"The blocks show {a}. Add {b} ones.", f"{a} + {b} = {a + b}."],
                nn_w(a, b), EX(f"10*{a // 10}+{a % 10}+{b}"), qtype="visual", diagram=Diagram("blocks", {"t": a // 10, "o": a % 10}, alt))


@fam("012")
def n_word(r, L):
    a, b = no_new(r, L)
    th, nm = thing(r), name(r)
    t = pick(r, [f"{nm} has {U(a, th)}. {nm} gets {b} more. How many {th[1]} does {nm} have now?",
                 f"There are {U(a, th)} in a jar. {nm} puts in {b} more. How many {th[1]} are in the jar?"])
    return Item(t, U(a + b, th), [f"Add ones to ones: {a % 10} + {b}.", f"{a} + {b} = {a + b}."], nn_w(a, b, th[1]), EX(f"{a}+{b}", unit=th[1]),
                qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def n_mc(r, L):
    a, b = no_new(r, L)
    return Item(pick(r, [f"Which is the sum of {a} and {b}?", f"Choose the answer: {a} + {b}"]), a + b, ["Add ones to ones and keep the tens.", f"{a} + {b} = {a + b}."], nn_w(a, b), EX(f"{a}+{b}"))


@fam("012")
def n_missing(r, L):
    a, b = no_new(r, L)
    eq = pick(r, [f"{a} + ___ = {a + b}", f"___ + {b} = {a + b}"])
    ans = b if eq.startswith(f"{a} +") else a
    return Item(f"What number makes this true? {eq}", ans, ["Compare the ones digits.", f"{eq.replace('___', str(ans))} is true."],
                [W(a + b + (b if ans == b else a), "added the numbers shown"), W(ans + 1, "counted one too many"), W(ans + 10, "added a ten"), W(ans - 1, "counted one too few")],
                FN("blank_eq", eq=eq), claim=eq)


@fam("2", mode="mc")
def n_place(r, L):
    a, b = no_new(r, 2)
    good = f"Add {b} to the {a % 10} ones. Keep the {a // 10} tens."
    bad = [f"Add {b} to the {a // 10} tens. Keep the {a % 10} ones.", f"Add {b} to both digits.", f"Write {b} after {a}."]
    return mc_key(f"How can you add {a} + {b}?", good, bad, ["Add ones to ones and tens to tens.", f"{a} + {b} = {a + b}."], qtype="explain", tags={"reasoning"}, r=r)


# ============================================================== S4 Making a New Ten
def new10(r, L):
    if L == 0:
        a = r.randint(1, 4) * 10 + r.randint(7, 9)
        b = r.randint(2, 5)
    elif L == 1:
        a = r.randint(1, 7) * 10 + r.randint(5, 9)
        b = r.randint(3, 9)
    else:
        a = r.randint(3, 8) * 10 + r.randint(4, 9)
        b = r.randint(6, 9)
    need(a % 10 + b >= 10 and a + b <= 99)
    return a, b


def nt_w(a, b, u=""):
    s = a + b
    u = (" " + u) if u else ""
    return [W(f"{s - 10}{u}", "did not make a new ten"), W(f"{a // 10}{a % 10 + b}{u}", "wrote the ones sum as two digits"), W(f"{s + 1}{u}", "counted one too many"),
            W(f"{s - 1}{u}", "counted on and included the first number"), W(f"{s + 10}{u}", "added an extra ten")]


@fam("012")
def t_fact(r, L):
    a, b = new10(r, L)
    eq = pick(r, [f"{a} + {b}", f"{b} + {a}"])
    return Item(pick(r, [f"What is {eq}?", f"Add: {eq} = ___", f"Find the sum: {eq}"]), a + b,
                [f"{a % 10} + {b} = {a % 10 + b}. That is a new ten and {a % 10 + b - 10} ones.", f"{eq} = {a + b}."], nt_w(a, b), EX(eq.replace(" ", "")), claim=eq)


@fam("012")
def t_steps(r, L):
    a, b = new10(r, L)
    k = 10 - a % 10
    up = (a // 10 + 1) * 10
    form = pick(r, ["first", "rest"]) if L < 2 else "rest"
    if form == "first":
        eq = f"{a} + ___ = {up}"
        return Item(f"To add {a} + {b}, first make the next ten. {eq}", k, [f"{a} + {k} = {up}.", f"Then add the {b - k} left: {up} + {b - k} = {a + b}."],
                    [W(b, "used the whole number"), W(10, "wrote ten"), W(k + 1, "counted one too many"), W(b - k, "wrote the part that is left")],
                    FN("blank_eq", eq=eq), qtype="compare-strategies", tags={"connections"})
    return Item(f"{a} + {k} = {up}. Then {up} + {b - k} = ___. What is {a} + {b}?", a + b, [f"Break {b} into {k} and {b - k}.", f"{up} + {b - k} = {a + b}."],
                nt_w(a, b), EX(f"{a}+{b}"), qtype="compare-strategies", tags={"connections"})


@fam("012")
def t_blocks(r, L):
    a, b = new10(r, L)
    alt = f"Base-ten blocks: {a // 10} tens rods and {a % 10} ones cubes."
    return Item(f"The blocks show a number. Add {b} ones. Make a new ten if you can. What is the sum?", a + b,
                [f"The blocks show {a}. {a % 10} ones + {b} ones = {a % 10 + b} ones = 1 ten and {a % 10 + b - 10} ones.", f"{a} + {b} = {a + b}."],
                nt_w(a, b), EX(f"10*{a // 10}+{a % 10}+{b}"), qtype="visual", diagram=Diagram("blocks", {"t": a // 10, "o": a % 10}, alt))


@fam("012")
def t_word(r, L):
    a, b = new10(r, L)
    th, nm = thing(r), name(r)
    t = pick(r, [f"{nm} has {U(a, th)}. {nm} finds {b} more. How many {th[1]} does {nm} have now?",
                 f"A class has {U(a, th)}. They get {b} more. How many {th[1]} does the class have?"])
    return Item(t, U(a + b, th), [f"{a} + {b}: the ones make a new ten.", f"{a} + {b} = {a + b}."], nt_w(a, b, th[1]), EX(f"{a}+{b}", unit=th[1]),
                qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def t_mc(r, L):
    a, b = new10(r, L)
    return Item(pick(r, [f"Which is the sum of {a} and {b}?", f"Choose the answer: {a} + {b}"]), a + b, ["Make a new ten with the ones.", f"{a} + {b} = {a + b}."], nt_w(a, b), EX(f"{a}+{b}"))


@fam("2", mode="mc")
def t_new_ten(r, L):
    a, b = new10(r, 2)
    need(a % 10 + b != 10)
    good = f"Yes. {a % 10} + {b} = {a % 10 + b}, which is 1 ten and {a % 10 + b - 10} ones."
    bad = [f"No. You only add the ones.", f"Yes. {a % 10} + {b} = {a % 10 + b}, so write {a // 10}{a % 10 + b}.", f"No. {b} is less than 10."]
    return mc_key(f"When you add {a} + {b}, do you make a new ten?", good, bad, [f"{a % 10} + {b} = {a % 10 + b}.", f"{a} + {b} = {a + b}."], qtype="explain", tags={"reasoning"}, r=r)


# ============================================================== S5 Adding Two-Digit Numbers with Models
def tt(r, L):
    if L == 0:
        a, b = r.randint(11, 45), r.randint(11, 44)
        need(a % 10 + b % 10 <= 9 and a + b <= 80)
    elif L == 1:
        a, b = r.randint(12, 68), r.randint(12, 48)
        need(a % 10 + b % 10 <= 9 and a + b <= 99)
    else:
        a, b = r.randint(15, 68), r.randint(15, 39)
        need(a % 10 + b % 10 >= 10 and a + b <= 99)
    need(a % 10 and b % 10)
    return a, b


def tt_w(a, b, u=""):
    s = a + b
    u = (" " + u) if u else ""
    out = [W(f"{s + 10}{u}", "counted one ten too many"), W(f"{s - 10}{u}", "did not make a new ten" if a % 10 + b % 10 >= 10 else "counted one ten too few"),
           W(f"{a + b // 10 + 10 * (b % 10)}{u}", "added tens to ones"), W(f"{s + 1}{u}", "counted one too many")]
    if a % 10 + b % 10 >= 10:
        out.insert(0, W(f"{a // 10 + b // 10}{a % 10 + b % 10}{u}", "wrote the ones sum as two digits"))
    return out


@fam("012")
def w_fact(r, L):
    a, b = tt(r, L)
    return Item(pick(r, [f"What is {a} + {b}?", f"Add: {a} + {b} = ___", f"Find the sum of {a} and {b}."]), a + b,
                [f"Tens: {a // 10 * 10} + {b // 10 * 10} = {a // 10 * 10 + b // 10 * 10}. Ones: {a % 10} + {b % 10} = {a % 10 + b % 10}.", f"{a} + {b} = {a + b}."],
                tt_w(a, b), EX(f"{a}+{b}"), claim=f"{a} + {b}")


@fam("012")
def w_split(r, L):
    a, b = tt(r, L)
    part = pick(r, ["tens", "ones"])
    if part == "tens":
        return Item(f"To add {a} + {b}, add the tens first. {a // 10 * 10} + {b // 10 * 10} = ___", a // 10 * 10 + b // 10 * 10,
                    [f"{a // 10} tens + {b // 10} tens = {a // 10 + b // 10} tens.", f"That is {a // 10 * 10 + b // 10 * 10}."],
                    [W(a // 10 + b // 10, "wrote the number of tens"), W(a + b, "added the whole numbers"), W(a // 10 * 10 + b // 10 * 10 + 10, "counted one ten too many"), W(abs(a - b) // 10 * 10 or 10, "subtracted")],
                    EX(f"{a // 10 * 10}+{b // 10 * 10}"), qtype="compare-strategies", tags={"connections"})
    return Item(f"To add {a} + {b}, add the ones. {a % 10} + {b % 10} = ___. Then what is {a} + {b}?", a + b,
                [f"Ones: {a % 10} + {b % 10} = {a % 10 + b % 10}.", f"Tens: {a // 10 * 10 + b // 10 * 10}. Total: {a + b}."], tt_w(a, b), EX(f"{a}+{b}"),
                qtype="compare-strategies", tags={"connections"})


@fam("012")
def w_table(r, L):
    a, b = tt(r, L)
    alt = f"Table: first number {a // 10} tens and {a % 10} ones; second number {b // 10} tens and {b % 10} ones."
    return Item("The table shows two numbers as tens and ones. What is the sum of the two numbers?", a + b,
                [f"The numbers are {a} and {b}.", f"{a} + {b} = {a + b}."], tt_w(a, b), EX(f"10*{a // 10}+{a % 10}+10*{b // 10}+{b % 10}"), qtype="visual",
                diagram=Diagram("table", {"header": ["", "Tens", "Ones"], "rows": [["First", a // 10, a % 10], ["Second", b // 10, b % 10]]}, alt))


@fam("012")
def w_word(r, L):
    a, b = tt(r, L)
    th, n1 = thing(r), name(r)
    t = pick(r, [f"{n1} has {U(a, th)}. A friend gives {n1} {b} more. How many {th[1]} does {n1} have now?",
                 f"A class has {U(a, th)} in one bin and {U(b, th)} in another bin. How many {th[1]} are there in all?"])
    return Item(t, U(a + b, th), [f"Add tens and tens, ones and ones.", f"{a} + {b} = {a + b}."], tt_w(a, b, th[1]), EX(f"{a}+{b}", unit=th[1]),
                qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def w_mc(r, L):
    a, b = tt(r, L)
    return Item(pick(r, [f"Which is the sum of {a} and {b}?", f"Choose the answer: {a} + {b}"]), a + b, ["Add tens and tens, ones and ones.", f"{a} + {b} = {a + b}."], tt_w(a, b), EX(f"{a}+{b}"))


SKILLS = {
    1: dict(name="10 More and 10 Less", fams=[tm_fact, tm_eq, tm_blocks, tm_chart, tm_mc, tm_word, tm_why]),
    2: dict(name="Adding and Subtracting Tens", fams=[d_add, d_sub, d_blocks, d_word, d_mc, d_missing]),
    3: dict(name="Adding a Two-Digit and a One-Digit Number", fams=[n_fact, n_blocks, n_word, n_mc, n_missing, n_place]),
    4: dict(name="Making a New Ten", fams=[t_fact, t_steps, t_blocks, t_word, t_mc, t_new_ten]),
    5: dict(name="Adding Two-Digit Numbers with Models", fams=[w_fact, w_split, w_table, w_word, w_mc]),
}
