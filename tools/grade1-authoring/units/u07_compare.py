"""Unit 7: Comparing Two-Digit Numbers (compare-numbers). 1.NBT.B.3."""
from g1lib import *

UNIT_ID = "compare-numbers"


def two(r, L):
    """L0: different tens within 10-59; L1: any two-digit pair, tens differ or same; L2: same tens or reversed digits."""
    if L == 0:
        a, b = r.randint(10, 59), r.randint(10, 59)
        need(a // 10 != b // 10)
    elif L == 1:
        a, b = r.randint(10, 99), r.randint(10, 99)
        need(a != b and abs(a - b) < 40)
    else:
        if r.random() < 0.5:
            t = r.randint(1, 9)
            a, b = 10 * t + r.randint(0, 9), 10 * t + r.randint(0, 9)
        else:
            a = r.randint(12, 98)
            b = 10 * (a % 10) + a // 10
        need(a != b and a % 10 and b >= 10)
    return a, b


def cw(a, b, want):
    g = max(a, b) if want == "greater" else min(a, b)
    o = min(a, b) if want == "greater" else max(a, b)
    out = [W(o, f"chose the {'smaller' if want == 'greater' else 'greater'} number")]
    return out


# ============================================================== S1 Comparing Tens and Ones
@fam("012")
def c_pick(r, L):
    a, b = two(r, L)
    want = pick(r, ["greater", "less"])
    g = max(a, b) if want == "greater" else min(a, b)
    o = a + b - g
    return Item(pick(r, [f"Which number is {want}, {a} or {b}?", f"Write the number that is {want}: {a} or {b}."]), g,
                [f"Compare the tens: {a // 10} and {b // 10}." + (" They are the same, so compare the ones." if a // 10 == b // 10 else ""),
                 f"{g} is {want}."], [W(o, "compared the ones digits first" if (a % 10 > b % 10) != (a > b) else "chose the other number")],
                FN("cmp_pick", nums=[a, b], want=want), mode="sa")


@fam("012", mode="mc")
def c_pick_mc(r, L):
    a, b = two(r, L)
    want = pick(r, ["greater", "less"])
    g = max(a, b) if want == "greater" else min(a, b)
    o = a + b - g
    bad = [str(o), "They are equal.", str(10 * (g % 10) + g // 10) if g % 10 and 10 * (g % 10) + g // 10 not in (a, b) else str(g + 10)]
    it = mc_key(pick(r, [f"Which is {want}: {a} or {b}?", f"Look at the tens first. Which number is {want}, {a} or {b}?"]), str(g), bad,
                ["Compare the tens first, then the ones.", f"{g} is {want}."], qtype="procedural", r=r)
    it.check = FN("cmp_pick", nums=[a, b], want=want)
    return it


@fam("012")
def c_table(r, L):
    a, b = two(r, L)
    n1, n2 = r.sample(NAMES, 2)
    want = pick(r, ["more", "fewer"])
    win = (n1 if a > b else n2) if want == "more" else (n1 if a < b else n2)
    alt = f"Table of blocks: {n1} has {a // 10} tens and {a % 10} ones. {n2} has {b // 10} tens and {b % 10} ones."
    return Item(f"The table shows the cubes each child has. Who has {want} cubes?", win,
                [f"{n1} has {a}. {n2} has {b}.", f"{win} has {want} cubes."], [W(n2 if win == n1 else n1, "compared the ones first")],
                FN("who_cmp", vals={n1: a, n2: b}, want=want), qtype="visual", mode="sa",
                diagram=Diagram("table", {"header": ["Name", "Tens", "Ones"], "rows": [[n1, a // 10, a % 10], [n2, b // 10, b % 10]]}, alt))


@fam("012", mode="mc")
def c_word(r, L):
    a, b = two(r, L)
    n1, n2 = r.sample(NAMES, 2)
    th = thing(r)
    want = pick(r, ["more", "fewer"])
    win = (n1 if a > b else n2) if want == "more" else (n1 if a < b else n2)
    other = n2 if win == n1 else n1
    good = f"{win}"
    bad = [other, "They have the same number.", f"{other}, because {max(a % 10, b % 10)} is bigger" if a % 10 != b % 10 else f"{other}, because {other} is first"]
    it = mc_key(f"{n1} has {a} {th[1]}. {n2} has {b} {th[1]}. Who has {want} {th[1]}?", good, bad,
                [f"Compare {a} and {b}: look at the tens first.", f"{win} has {want}."], qtype="word-problem", tags={"modeling"}, r=r)
    it.check = FN("who_cmp", vals={n1: a, n2: b}, want=want)
    return it


@fam("012", mode="mc")
def c_why(r, L):
    a, b = two(r, max(L, 1))
    need(a // 10 != b // 10)
    g, s = max(a, b), min(a, b)
    good = f"{g} has more tens than {s}."
    bad = [f"{g} has more ones than {s}." if g % 10 <= s % 10 else f"{s} has more tens than {g}.", f"{g} is written first.", f"{s} has fewer digits than {g}."]
    return mc_key(f"Why is {g} greater than {s}?", good, bad, [f"{g} has {g // 10} tens and {s} has {s // 10} tens.", good], qtype="explain", tags={"reasoning"}, r=r)


@fam("2")
def c_three(r, L):
    a, b, c = r.sample(range(12, 99), 3)
    need(len({a // 10, b // 10, c // 10}) <= 2)
    want = pick(r, ["greatest", "least"])
    g = max(a, b, c) if want == "greatest" else min(a, b, c)
    o = sorted([a, b, c])[1]
    return Item(f"Which number is the {want}: {a}, {b}, or {c}?", g, ["Compare the tens first. If they match, compare the ones.", f"The {want} is {g}."],
                [W(o, "chose the middle number"), W(max(a, b, c) if want == "least" else min(a, b, c), "chose the wrong end")],
                FN("pick_num", nums=[a, b, c], want=want), mode="sa")


# ============================================================== S2 Using >, =, and <
@fam("012")
def s_symbol(r, L):
    a, b = two(r, L)
    if L >= 1 and r.random() < 0.15:
        b = a
    sym = "<" if a < b else ">" if a > b else "="
    return Item(pick(r, [f"Write >, <, or =. {a} ___ {b}", f"Which symbol goes in the blank: >, <, or =? {a} ___ {b}"]), sym,
                [f"Compare {a} and {b}.", f"{a} {sym} {b}."], [W(">" if sym == "<" else "<", "pointed the symbol the wrong way"), W("=", "thought the numbers are the same")],
                FN("compare", a=str(a), b=str(b)), mode="sa")


@fam("012", mode="mc")
def s_true(r, L):
    a, b = two(r, L)
    sym = "<" if a < b else ">"
    good = f"{a} {sym} {b}"
    bad = [f"{a} {'>' if sym == '<' else '<'} {b}", f"{a} = {b}", f"{b} {sym} {a}"]
    it = mc_key(pick(r, ["Which is true?", "Which comparison is correct?"]), good, bad, [f"Compare {a} and {b}.", f"{good} is true."], qtype="procedural", r=r)
    it.check = FN("true_cmp")
    return it


@fam("012", mode="mc")
def s_read(r, L):
    a, b = two(r, L)
    sym = "<" if a < b else ">"
    word = "less than" if sym == "<" else "greater than"
    good = f"{a} is {word} {b}."
    bad = [f"{a} is {'greater than' if sym == '<' else 'less than'} {b}.", f"{a} is equal to {b}.", f"{b} is {word} {a}."]
    return mc_key(f"What does {a} {sym} {b} mean?", good, bad, [f"The symbol {sym} means {word}.", good], qtype="conceptual", r=r)


@fam("012")
def s_write(r, L):
    a, b = two(r, L)
    sym = "<" if a < b else ">"
    return Item(f"Compare {a} and {b}. Write {a}, then >, <, or =, then {b}.", f"{a} {sym} {b}",
                [f"Compare the tens, then the ones.", f"{a} {sym} {b}."], [W(f"{a} {'>' if sym == '<' else '<'} {b}", "pointed the symbol the wrong way"), W(f"{a} = {b}", "thought the numbers are equal")],
                FN("cmp_stmt", a=a, b=b), mode="sa")


@fam("2")
def s_tens_ones(r, L):
    a, b = two(r, 2)
    sym = "<" if a < b else ">"
    left = f"{pl(a // 10, 'ten')} and {pl(a % 10, 'one')}"
    return Item(f"Write >, <, or =. {left} ___ {b}", sym, [f"{left} is {a}.", f"{a} {sym} {b}."],
                [W(">" if sym == "<" else "<", "pointed the symbol the wrong way"), W("=", "thought the amounts are the same")], FN("compare", a=str(a), b=str(b)), mode="sa")


@fam("01")
def s_blocks(r, L):
    a, b = two(r, L)
    sym = "<" if a < b else ">"
    alt = f"Base-ten blocks: {a // 10} tens rods and {a % 10} ones cubes."
    return Item(f"The blocks show a number. Compare it to {b}. Write >, <, or =: blocks ___ {b}", sym,
                [f"The blocks show {a}.", f"{a} {sym} {b}."], [W(">" if sym == "<" else "<", "pointed the symbol the wrong way"), W("=", "thought they are the same")],
                FN("compare", a=str(a), b=str(b)), qtype="visual", mode="sa", diagram=Diagram("blocks", {"t": a // 10, "o": a % 10}, alt))


# ============================================================== S3 Reasoning about Comparisons
@fam("012", mode="mc")
def r_digit(r, L):
    t = r.randint(2, 8)
    o = r.randint(2, 7)
    sym = pick(r, [">", "<"])
    tmpl = f"{t}? {sym} {10 * t + o}"
    ok = [d for d in range(10) if (10 * t + d > 10 * t + o if sym == ">" else 10 * t + d < 10 * t + o)]
    no = [d for d in range(10) if d not in ok]
    need(ok and len(no) >= 3)
    g = pick(r, ok)
    bad = r.sample(no, 3)
    it = mc_key(f"Which digit can replace the ? to make this true? {tmpl}", str(g), [str(x) for x in bad],
                [f"The tens are the same, so the ones must be {'more' if sym == '>' else 'less'} than {o}.", f"{10 * t + g} {sym} {10 * t + o}."], qtype="reasoning", tags={"reasoning"}, r=r)
    it.check = FN("digit_fill", tmpl=tmpl)
    return it


@fam("012", mode="mc")
def r_pick(r, L):
    a = r.randint(25, 85)
    sym = pick(r, [">", "<"])
    if L == 0:
        cands = [a + 20, a - 20, a - 15, a - 25] if sym == ">" else [a - 20, a + 20, a + 15, a + 25]
    else:
        cands = [a + 3, a - 3, a - 10, a - 1] if sym == ">" else [a - 3, a + 3, a + 10, a + 1]
    need(all(10 <= x <= 99 for x in cands))
    good = cands[0]
    it = mc_key(f"Which number makes this true? ___ {sym} {a}", str(good), [str(x) for x in cands[1:]],
                [f"The number must be {'greater' if sym == '>' else 'less'} than {a}.", f"{good} {sym} {a}."], qtype="reasoning", r=r)
    it.check = FN("pick_num", nums=cands, want=sym, blank=0, other=a)
    return it


@fam("012")
def r_between(r, L):
    a = r.randint(10, 40) if L == 0 else r.randint(20, 90)
    k = r.randint(3, 6)
    need(a + k <= 99)
    return Item(f"Write a number that is greater than {a} and less than {a + k}.", a + 1, [f"Count on from {a}: " + ", ".join(str(a + i) for i in range(1, k)) + ".",
                                                                                      f"Any of these works, such as {a + 1}."],
                [W(a, "used the first number"), W(a + k, "used the last number"), W(a - 1, "went the wrong way")], FN("between_nums", lo=a, hi=a + k), qtype="reasoning", mode="sa")


@fam("012")
def r_order(r, L):
    a, b = two(r, max(L, 1))
    c = r.randint(10, 99)
    need(len({a, b, c}) == 3)
    vals = [a, b, c]
    s = sorted(vals)
    need(vals != s and vals != s[::-1])
    want = pick(r, ["least to greatest", "greatest to least"])
    ans = ", ".join(map(str, s if want == "least to greatest" else s[::-1]))
    return Item(f"Write the numbers in order from {want}: {a}, {b}, {c}", ans, ["Compare the tens first, then the ones.", f"In order: {ans}."],
                [W(", ".join(map(str, s[::-1] if want == "least to greatest" else s)), "put them in the other order"), W(", ".join(map(str, vals)), "did not change the order")],
                FN("order_nums", vals=vals, want=want), qtype="procedural", mode="sa")


@fam("012", mode="mc")
def r_claim(r, L):
    t1 = r.randint(2, 7)
    a = 10 * t1 + r.randint(6, 9)
    b = 10 * (t1 + 1) + r.randint(0, 3)
    nm = name(r)
    good = f"No. {b} has more tens, so {b} is greater."
    bad = [f"Yes. {a % 10} is greater than {b % 10}.", f"Yes. {a} has more ones.", f"No. The numbers are equal."]
    return mc_key(f"{nm} says {a} > {b} because {a % 10} > {b % 10}. Is {nm} right?", good, bad,
                  [f"Compare the tens first: {t1} tens and {t1 + 1} tens.", good], qtype="error-analysis", tags={"misconception", "reasoning"}, r=r)


@fam("2")
def r_make(r, L):
    d = r.sample(range(1, 10), 2)
    want = pick(r, ["greatest", "least"])
    hi, lo = max(d), min(d)
    ans = 10 * hi + lo if want == "greatest" else 10 * lo + hi
    other = 10 * lo + hi if want == "greatest" else 10 * hi + lo
    return Item(f"Use the digits {d[0]} and {d[1]} one time each. What is the {want} two-digit number you can make?", ans,
                [f"Put the {'bigger' if want == 'greatest' else 'smaller'} digit in the tens place.", f"The {want} number is {ans}."],
                [W(other, "put the wrong digit in the tens place"), W(d[0] + d[1], "added the digits"), W(10 * d[0] + d[1] if 10 * d[0] + d[1] != ans else 10 * d[1] + d[0], "kept the digits in the order given")],
                FN("make_num", d=d, want=want), qtype="reasoning", tags={"reasoning"})


SKILLS = {
    1: dict(name="Comparing Tens and Ones", fams=[c_pick, c_pick_mc, c_table, c_word, c_why, c_three]),
    2: dict(name="Using >, =, and <", fams=[s_symbol, s_true, s_read, s_write, s_tens_ones, s_blocks]),
    3: dict(name="Reasoning about Comparisons", fams=[r_digit, r_pick, r_between, r_order, r_claim, r_make]),
}
