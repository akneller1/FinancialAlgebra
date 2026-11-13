"""Unit 7: Addition and Subtraction within 1,000 (add-subtract-1000). 2.NBT.B.7, 2.NBT.B.9."""
from g2lib import *

UNIT_ID = "add-subtract-1000"


def digits(n):
    return n // 100, n // 10 % 10, n % 10


def add_pair(r, L, regroup):
    a, b = (r.randint(101, 399), r.randint(101, 299)) if L == 0 else (r.randint(101, 699), r.randint(101, 399)) if L == 1 else (r.randint(250, 799), r.randint(150, 399))
    need(a + b <= 1000)
    ro, rt = a % 10 + b % 10 >= 10, a // 10 % 10 + b // 10 % 10 + (1 if a % 10 + b % 10 >= 10 else 0) >= 10
    if regroup == "none":
        need(not ro and not rt)
    elif regroup == "one":
        need(ro != rt)
    else:
        need(ro or rt)
        need(L < 2 or (ro and rt) or r.random() < 0.3)
    return a, b


def add_w(a, b):
    s = a + b
    nc = sum(((x + y) % 10) * p for x, y, p in zip(digits(a), digits(b), (100, 10, 1)))
    ro = a % 10 + b % 10 >= 10
    rt = a // 10 % 10 + b // 10 % 10 + ro >= 10
    out = []
    if nc != s:
        out.append(W(nc, "did not make a new ten or hundred"))
    out += [W(s + 10, "added an extra ten"), W(s - 10, "forgot a new ten" if ro else "made a mistake in the tens"), W(s + 100, "added an extra hundred"),
            W(s - 100, "forgot a new hundred" if rt else "made a mistake in the hundreds"), W(abs(a - b), "subtracted instead of adding")]
    return out


def sub_pair(r, L, regroup):
    a, b = (r.randint(250, 599), r.randint(101, 299)) if L == 0 else (r.randint(250, 999), r.randint(101, 499)) if L == 1 else (r.randint(500, 999), r.randint(150, 599))
    need(a - b >= 20)
    ro, rt = a % 10 < b % 10, a // 10 % 10 - (1 if a % 10 < b % 10 else 0) < b // 10 % 10
    if regroup == "none":
        need(not ro and not rt)
    else:
        need(ro or rt)
        need(L < 2 or (ro and rt) or r.random() < 0.25)
    return a, b


def sub_w(a, b):
    d = a - b
    sm = sum(abs(x - y) * p for x, y, p in zip(digits(a), digits(b), (100, 10, 1)))
    ro = a % 10 < b % 10
    rt = a // 10 % 10 - ro < b // 10 % 10
    out = []
    if sm != d:
        out.append(W(sm, "subtracted the smaller digit from the larger digit"))
    out += [W(d + 10, "broke apart a ten but did not take it away" if ro else "made a mistake in the tens"),
            W(d + 100, "broke apart a hundred but did not take it away" if rt else "made a mistake in the hundreds"),
            W(a + b if a + b <= 1000 else d - 10, "added instead of subtracting" if a + b <= 1000 else "took away an extra ten"), W(d - 10, "took away an extra ten")]
    return out


# ============================================================== S1 Adding Three-Digit Numbers with Models
@fam("012")
def m_blocks(r, L):
    a, b = add_pair(r, L, "none" if L == 0 else "one")
    h, t, o = (x + y for x, y in zip(digits(a), digits(b)))
    need(h <= 9)
    alt = f"Base-ten blocks for {a} + {b} put together: {h} hundred flats, {t} tens rods, and {o} ones cubes."
    return Item(f"The blocks show {a} + {b} put together. Trade if you have 10 or more of one kind of block. What is the sum?", a + b,
                [f"{pl(h, 'hundred')}, {pl(t, 'ten')}, {pl(o, 'one')}.", f"The sum is {a + b}."], add_w(a, b), EX(f"{h}×100+{t}×10+{o}"), qtype="visual",
                diagram=Diagram("blocks", {"h": h, "t": t, "o": o}, alt))


@fam("012")
def m_places(r, L):
    a, b = add_pair(r, L, "none" if L == 0 else "any")
    (ah, at_, ao), (bh, bt, bo) = digits(a), digits(b)
    H, T, O = (ah + bh) * 100, (at_ + bt) * 10, ao + bo
    return Item(f"Add {a} + {b} by place. Hundreds: {ah * 100} + {bh * 100} = {H}. Tens: {at_ * 10} + {bt * 10} = {T}. Ones: {ao} + {bo} = {O}. What is the sum?", a + b,
                [f"Add the three place totals: {H} + {T} + {O}.", f"{H} + {T} + {O} = {a + b}."],
                [W(H + T, "left out the ones"), W(int(f"{H // 100}{T // 10}{O}") if T < 100 and O < 10 else a + b + 100, "wrote the totals side by side"), W(a + b - 10, "made an addition mistake")],
                EX(f"{H}+{T}+{O}"), qtype="compare-strategies", tags={"multiple-representations"})


@fam("012")
def m_std(r, L):
    a, b = add_pair(r, L, "none" if L < 2 else "one")
    return Item(f"Add: {a} + {b}", a + b, ["Add hundreds and hundreds, tens and tens, ones and ones.", f"{a} + {b} = {a + b}."], add_w(a, b), EX(f"{a}+{b}"), qtype="procedural", claim=f"{a} + {b}")


@fam("012")
def m_word(r, L):
    a, b = add_pair(r, L, "none" if L == 0 else "any")
    t = pick(r, [("A school has {a} students in the morning classes and {b} students in the afternoon classes. How many students is that?", "students"),
                 ("A zoo had {a} visitors on Saturday and {b} visitors on Sunday. How many visitors came that weekend?", "visitors"),
                 ("{nm} has {a} blocks. {nm} gets {b} more. How many blocks does {nm} have?", "blocks")])
    return Item(t[0].format(a=a, b=b, nm=name(r)), f"{a + b} {t[1]}", [f"Add {a} + {b}.", f"{a} + {b} = {a + b} {t[1]}."],
                [W(f"{w} {t[1]}", y) for w, y in add_w(a, b)], EX(f"{a}+{b}", unit=t[1]), qtype="word-problem", tags={"modeling"})


@fam("012")
def m_chain(r, L):
    a, b = add_pair(r, L, "none" if L == 0 else "any")
    bh, bt, bo = digits(b)
    need(bt and bo)
    return Item(f"Start at {a}. Add {bh * 100}, then add {bt * 10}, then add {bo}. Where do you end?", a + b,
                [f"{a} + {bh * 100} = {a + bh * 100}; {a + bh * 100} + {bt * 10} = {a + bh * 100 + bt * 10}.", f"{a + bh * 100 + bt * 10} + {bo} = {a + b}, which is {a} + {b}."],
                add_w(a, b), EX(f"{a}+{bh * 100}+{bt * 10}+{bo}"), qtype="compare-strategies", tags={"multiple-representations"})


@fam("012", mode="mc")
def m_mc(r, L):
    a, b = add_pair(r, L, "none" if L == 0 else "any")
    return Item(f"What is {a} + {b}?", a + b, ["Add each place.", f"{a} + {b} = {a + b}."], add_w(a, b), EX(f"{a}+{b}"), mode="mc")


@fam("2", mode="mc")
def m_which_parts(r, L):
    a, b = add_pair(r, 2, "any")
    (ah, at_, ao), (bh, bt, bo) = digits(a), digits(b)
    good = f"{ah * 100 + bh * 100} + {at_ * 10 + bt * 10} + {ao + bo}"
    bad = [f"{ah * 100 + bt * 10} + {at_ * 10 + bh * 100} + {ao + bo}", f"{ah + bh} + {at_ + bt} + {ao + bo}", f"{ah * 100 + bh * 100} + {at_ * 10 + bt * 10}"]
    need(len(set(bad + [good])) == 4)
    it = mc_key(f"Which shows adding {a} + {b} by place value (hundreds and hundreds, tens and tens, ones and ones)?", good, bad, ["Add like places.", f"{good} = {a + b}."], qtype="conceptual", tags={"reasoning"}, r=r)
    it.check = FN("place_sum", a=a, b=b)
    return it


# ============================================================== S2 Adding with New Tens and Hundreds
@fam("012")
def r_std(r, L):
    a, b = add_pair(r, L, "one" if L < 2 else "any")
    return Item(f"Add: {a} + {b}", a + b, ["Add each place. Trade 10 ones for 1 ten or 10 tens for 1 hundred.", f"{a} + {b} = {a + b}."], add_w(a, b), EX(f"{a}+{b}"), qtype="procedural", claim=f"{a} + {b}")


@fam("012")
def r_trade(r, L):
    a, b = add_pair(r, L, "one" if L < 2 else "any")
    h, t, o = (x + y for x, y in zip(digits(a), digits(b)))
    need(h <= 9 and (t >= 10 or o >= 10))
    return Item(f"{a} + {b} has {pl(h, 'hundred')}, {pl(t, 'ten')}, and {pl(o, 'one')}. Trade to make a three-digit number. What is the sum?", a + b,
                [" ".join(x for x in ("Trade 10 ones for 1 ten." if o >= 10 else "", "Trade 10 tens for 1 hundred." if t + (1 if o >= 10 else 0) >= 10 else "") if x), f"The sum is {a + b}."],
                add_w(a, b), EX(f"{h}×100+{t}×10+{o}"), qtype="explain", tags={"reasoning"})


@fam("012")
def r_word(r, L):
    a, b = add_pair(r, L, "one" if L == 0 else "any")
    t = pick(r, [("A farm has {a} chickens and {b} ducks. How many birds is that?", "birds"),
                 ("A store sold {a} pencils in May and {b} pencils in June. How many pencils did it sell?", "pencils"),
                 ("{nm} walked {a} steps before lunch and {b} steps after lunch. How many steps did {nm} walk?", "steps")])
    return Item(t[0].format(a=a, b=b, nm=name(r)), f"{a + b} {t[1]}", [f"Add {a} + {b}, trading when a place has 10 or more.", f"{a} + {b} = {a + b} {t[1]}."],
                [W(f"{w} {t[1]}", y) for w, y in add_w(a, b)], EX(f"{a}+{b}", unit=t[1]), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def r_mc(r, L):
    a, b = add_pair(r, L, "one" if L == 0 else "any")
    return Item(f"What is {a} + {b}?", a + b, ["Add each place and make a new ten or hundred when needed.", f"{a} + {b} = {a + b}."], add_w(a, b), EX(f"{a}+{b}"), mode="mc")


@fam("2")
def r_three(r, L):
    a, b, c = r.randint(101, 399), r.randint(101, 299), r.randint(12, 199)
    need(a + b + c <= 1000)
    return Item(f"Add: {a} + {b} + {c}", a + b + c, [f"{a} + {b} = {a + b}.", f"{a + b} + {c} = {a + b + c}."],
                [W(a + b, "left out an addend"), W(a + b + c - 10, "forgot a new ten"), W(a + b + c + 100, "added an extra hundred")], EX(f"{a}+{b}+{c}"), qtype="multi-step", tags={"multistep"})


@fam("2")
def r_digit(r, L):
    a, b = add_pair(r, 2, "any")
    s = a + b
    shown = f"{a // 100}□{a % 10}"
    return Item(f"Find the missing digit: {shown} + {b} = {s}", a // 10 % 10, [f"{s} − {b} = {a}.", f"The missing digit is {a // 10 % 10}."],
                [W((a // 10 + 1) % 10, "forgot a new ten"), W(s // 10 % 10, "copied the tens digit of the sum"), W((a // 10 + 9) % 10, "traded the wrong way")],
                FN("missing_digit", shown=shown, other=b, total=s, op="+"), qtype="explain", tags={"reasoning"})


@fam("012", mode="mc")
def r_error(r, L):
    a, b = add_pair(r, L, "any")
    nc = sum(((x + y) % 10) * p for x, y, p in zip(digits(a), digits(b), (100, 10, 1)))
    need(nc != a + b)
    nm = name(r)
    good = f"{a + b}. {nm} did not add the new ten or hundred made by trading."
    bad = [f"{nc}. {nm} is correct.", f"{a + b + 100}. {nm} forgot to add 100.", f"{abs(a - b)}. {nm} should have subtracted."]
    it = mc_key(f"{nm} added {a} + {b} and got {nc}. What is the correct sum, and what was the mistake?", good, bad, ["Check each place for 10 or more.", f"{a} + {b} = {a + b}."], qtype="error-analysis", tags={"misconception"}, r=r)
    it.check = FN("lead_sum", a=a, b=b)
    return it


# ============================================================== S3 Subtracting Three-Digit Numbers with Models
@fam("012")
def sm_std(r, L):
    a, b = sub_pair(r, L, "none" if L < 2 else "any")
    return Item(f"Subtract: {a} − {b}", a - b, ["Subtract hundreds from hundreds, tens from tens, ones from ones.", f"{a} − {b} = {a - b}."], sub_w(a, b), EX(f"{a}-{b}"), qtype="procedural", claim=f"{a} − {b}")


@fam("012")
def sm_blocks(r, L):
    a, b = sub_pair(r, L, "none" if L == 0 else "any")
    h, t, o = digits(a)
    alt = f"Base-ten blocks showing {a}: {h} hundred flats, {t} tens rods, and {o} ones cubes."
    return Item(f"The blocks show {a}. Take away {b}. How many are left?", a - b,
                [f"Take away {pl(b // 100, 'hundred')}, {pl(b // 10 % 10, 'ten')}, and {pl(b % 10, 'one')}, trading if needed.", f"{a} − {b} = {a - b}."],
                sub_w(a, b), EX(f"{a}-{b}"), qtype="visual", diagram=Diagram("blocks", {"h": h, "t": t, "o": o}, alt))


@fam("012")
def sm_countup(r, L):
    a, b = sub_pair(r, L, "none" if L == 0 else "any")
    need(b % 10 and b % 100 // 10 < 9)
    j1 = 10 - b % 10
    m1 = b + j1
    j2 = (m1 // 100 + 1) * 100 - m1
    m2 = m1 + j2
    j3 = a - m2
    need(j3 > 0)
    return Item(f"Count up to find {a} − {b}: {b} + {j1} = {m1}, {m1} + {j2} = {m2}, {m2} + {j3} = {a}. What is {a} − {b}?", a - b,
                [f"Add the jumps: {j1} + {j2} + {j3}.", f"{j1} + {j2} + {j3} = {a - b}."],
                [W(j3, "used only the last jump"), W(a, "gave where the counting stopped"), W(a - b + 10, "made an addition mistake")],
                EX(f"{j1}+{j2}+{j3}"), qtype="compare-strategies", tags={"multiple-representations"})


@fam("012")
def sm_word(r, L):
    a, b = sub_pair(r, L, "none" if L == 0 else "any")
    t = pick(r, [("A theater has {a} seats. {b} seats are filled. How many seats are empty?", "seats"),
                 ("A library had {a} books. It gave away {b} books. How many books are left?", "books"),
                 ("A game has {a} tickets to win. {nm} won {b} tickets. How many tickets are still left to win?", "tickets")])
    return Item(t[0].format(a=a, b=b, nm=name(r)), f"{a - b} {t[1]}", [f"Subtract {a} − {b}.", f"{a} − {b} = {a - b} {t[1]}."],
                [W(f"{w} {t[1]}", y) for w, y in sub_w(a, b)], EX(f"{a}-{b}", unit=t[1]), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def sm_mc(r, L):
    a, b = sub_pair(r, L, "none" if L == 0 else "any")
    return Item(f"What is {a} − {b}?", a - b, ["Subtract each place.", f"{a} − {b} = {a - b}."], sub_w(a, b), EX(f"{a}-{b}"), mode="mc")


@fam("012", mode="mc")
def sm_check(r, L):
    a, b = sub_pair(r, L, "none" if L == 0 else "any")
    d = a - b
    good = f"{d} + {b} = {a}"
    bad = [f"{a} + {b} = {a + b}" if a + b <= 1000 else f"{a} − {d} = {b + 10}", f"{d} − {b} = {abs(d - b)}", f"{d} + {a} = {d + a}" if d + a <= 1000 else f"{d} + {b} = {a + 10}"]
    need(len(set(bad)) == 3)
    it = mc_key(f"{name(r)} found {a} − {b} = {d}. Which equation checks the answer?", good, bad, ["Add the answer to the number taken away.", f"{d} + {b} = {a}, so the answer is right."], qtype="conceptual", tags={"connections"}, r=r)
    it.check = FN("check_add", whole=a, part=b, other=d)
    return it


@fam("2")
def sm_places(r, L):
    a, b = sub_pair(r, 2, "none")
    (ah, at_, ao), (bh, bt, bo) = digits(a), digits(b)
    return Item(f"{a} − {b}: Hundreds: {ah * 100} − {bh * 100} = ___. Tens: {at_ * 10} − {bt * 10} = ___. Ones: {ao} − {bo} = ___. What is the difference?", a - b,
                [f"{(ah - bh) * 100} + {(at_ - bt) * 10} + {ao - bo}.", f"{a} − {b} = {a - b}."], sub_w(a, b) + [W((ah - bh) * 100 + (at_ - bt) * 10, "left out the ones")],
                EX(f"{a}-{b}"), qtype="compare-strategies", tags={"multiple-representations"})


# ============================================================== S4 Subtracting with Regrouping
@fam("012")
def sr_std(r, L):
    a, b = sub_pair(r, L, "any")
    return Item(f"Subtract: {a} − {b}", a - b, ["If a place does not have enough, break apart a ten or a hundred.", f"{a} − {b} = {a - b}."], sub_w(a, b), EX(f"{a}-{b}"), qtype="procedural", claim=f"{a} − {b}")


@fam("012")
def sr_zeros(r, L):
    a = r.randint(3, 9) * 100 + (0 if L < 2 else pick(r, [0, r.randint(1, 9)]))
    b = r.randint(101, a - 30)
    need(b % 10 and b // 10 % 10)
    return Item(f"Subtract: {a} − {b}", a - b, [f"{a} has 0 tens, so break apart a hundred into 10 tens, then break apart a ten into 10 ones.", f"{a} − {b} = {a - b}."], sub_w(a, b), EX(f"{a}-{b}"), qtype="procedural", claim=f"{a} − {b}")


@fam("012")
def sr_trade(r, L):
    h = r.randint(2, 9)
    form = pick(r, ["tens", "hundreds"]) if L else "tens"
    if form == "tens":
        q, ans = f"To subtract from {h * 100}, write it as {pl(h - 1, 'hundred')}, ___ tens, and 10 ones. What number goes in the blank?", 9
        steps = [f"Break 1 hundred into 10 tens; then break 1 ten into 10 ones.", f"{h * 100} = {(h - 1) * 100} + 90 + 10, so the blank is 9."]
        chk = FN("trade_blank", n=h * 100, hundreds=h - 1, ones=10)
    else:
        q, ans = f"{h * 100} is {pl(h, 'hundred')}. If you break apart 1 hundred, how many tens do you get?", 10
        steps = ["1 hundred = 10 tens.", "You get 10 tens."]
        chk = FN("tens_in", n=100)
    return Item(q, ans, steps, [W(10 if ans == 9 else 1, "did not break apart a ten" if ans == 9 else "thought a hundred is 1 ten"), W(0, "left the tens at 0"), W(100, "used ones instead of tens")],
                chk, qtype="conceptual", tags={"reasoning"})


@fam("012")
def sr_word(r, L):
    a, b = sub_pair(r, L, "any")
    t = pick(r, [("A school has {a} students. {b} students ride the bus. The rest walk. How many students walk?", "students"),
                 ("A puzzle has {a} pieces. {nm} has put in {b} pieces. How many pieces are left?", "pieces"),
                 ("{nm} has {a} points. {nm2} has {b} points. How many more points does {nm} have?", "points")])
    return Item(t[0].format(a=a, b=b, nm=name(r), nm2=name(sub(r, 2))), f"{a - b} {t[1]}", [f"Subtract {a} − {b}, breaking apart when needed.", f"{a} − {b} = {a - b} {t[1]}."],
                [W(f"{w} {t[1]}", y) for w, y in sub_w(a, b)], EX(f"{a}-{b}", unit=t[1]), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def sr_mc(r, L):
    a, b = sub_pair(r, L, "any")
    return Item(f"What is {a} − {b}?", a - b, ["Break apart a ten or a hundred when a place does not have enough.", f"{a} − {b} = {a - b}."], sub_w(a, b), EX(f"{a}-{b}"), mode="mc")


@fam("2")
def sr_missing(r, L):
    a, b = sub_pair(r, 2, "any")
    form = pick(r, ["start", "mid"])
    eq = f"___ − {b} = {a - b}" if form == "start" else f"{a} − ___ = {a - b}"
    ans = a if form == "start" else b
    return Item(f"What number makes the equation true? {eq}", ans, ["Use addition: the parts add to the whole.", f"{eq.replace('___', str(ans))}."],
                [W(abs(a - 2 * b) if form == "start" else 2 * a - b if 2 * a - b <= 1000 else ans + 10, "used the wrong operation"), W(ans + 10, "made a trading mistake"), W(ans - 100, "made a trading mistake")],
                FN("blank_eq", eq=eq), qtype="fill-blank", tags={"reasoning"})


@fam("012", mode="mc")
def sr_error(r, L):
    a, b = sub_pair(r, L, "any")
    sm = sum(abs(x - y) * p for x, y, p in zip(digits(a), digits(b), (100, 10, 1)))
    need(sm != a - b)
    nm = name(r)
    good = f"{a - b}. {nm} subtracted the smaller digit from the larger digit instead of breaking apart."
    bad = [f"{sm}. {nm} is correct.", f"{a - b + 10}. {nm} forgot to take away the trade.", f"{a + b if a + b <= 1000 else a - b - 100}. {nm} should have added."]
    it = mc_key(f"{nm} subtracted {a} − {b} and got {sm}. What is the correct difference, and what was the mistake?", good, bad, ["Check each place: is the top digit big enough?", f"{a} − {b} = {a - b}."], qtype="error-analysis", tags={"misconception"}, r=r)
    it.check = FN("lead_diff2", a=a, b=b)
    return it


SKILLS = {
    1: dict(name="Adding Three-Digit Numbers with Models", fams=[m_blocks, m_places, m_std, m_word, m_chain, m_mc, m_which_parts]),
    2: dict(name="Adding with New Tens and Hundreds", fams=[r_std, r_trade, r_word, r_mc, r_three, r_digit, r_error]),
    3: dict(name="Subtracting Three-Digit Numbers with Models", fams=[sm_std, sm_blocks, sm_countup, sm_word, sm_mc, sm_check, sm_places]),
    4: dict(name="Subtracting with Regrouping", fams=[sr_std, sr_zeros, sr_trade, sr_word, sr_mc, sr_missing, sr_error]),
}
