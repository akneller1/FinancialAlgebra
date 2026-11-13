"""Unit 3: Place Value to 1,000 (place-value-1000). 2.NBT.A.1, 2.NBT.A.1.a, 2.NBT.A.1.b, 2.NBT.A.3."""
from g2lib import *

UNIT_ID = "place-value-1000"


def three(r, L, zero=None):
    if L == 0:
        n = r.randint(101, 599)
    elif L == 1:
        n = r.randint(101, 999)
    else:
        n = pick(r, [r.randint(1, 9) * 100 + r.randint(1, 9), r.randint(1, 9) * 100 + r.randint(1, 9) * 10, r.randint(101, 999)])
    need(n % 100 != 0)
    if zero is not None:
        need((n // 10 % 10 == 0 or n % 10 == 0) == zero)
    return n


# ============================================================== S1 A Hundred Is Ten Tens
@fam("012")
def hu_tens_in(r, L):
    t = 10 if L == 0 else r.randint(11, 19) if L == 1 else r.randint(11, 39)
    n = 10 * t
    return Item(f"How many tens are in {n}?", t, [f"Count by tens: 10, 20, 30, … {n}." if n == 100 else f"{n} is {pl(n // 100, 'hundred')} and {pl(t % 10, 'ten')}; 1 hundred = 10 tens.", f"There are {t} tens in {n}."],
                [W(t // 10 if t >= 10 else 1, "counted only the hundreds"), W(t % 10, "counted only the tens digit"), W(n, "gave the number, not the tens"), W(t + 1, "counted one extra ten")],
                FN("tens_in", n=n), qtype="conceptual", claim=f"Tens in {n}")


@fam("012")
def hu_trade(r, L):
    t = r.randint(10, 19) if L == 0 else r.randint(11, 29)
    need(t % 10 or L == 0)
    alt = f"Base-ten blocks: {t} tens rods."
    return Item(f"The picture shows {t} tens. Trade 10 tens for 1 hundred. What number do the blocks show?", 10 * t,
                [f"{t} tens = {pl(t // 10, 'hundred')} and {pl(t % 10, 'ten')}.", f"That is {10 * t}."],
                [W(t, "gave the number of rods"), W(100 * (t // 10) + t % 10, "counted the leftover tens as ones"), W(10 * t + 10, "counted one extra ten"), W(1000 + 10 * (t % 10) if t >= 10 else 0, "counted 10 tens as 1,000")],
                FN("tens_value", tens=t), qtype="visual", diagram=Diagram("blocks", {"t": t}, alt))


@fam("012", mode="mc")
def hu_same(r, L):
    k = 1 if L == 0 else r.randint(1, 4)
    good = f"{10 * k} tens"
    bad = [f"{10 * k} ones", f"{k} ten" if k == 1 else f"{k} tens", f"{100 * k} tens"]
    it = mc_key(f"Which is the same as {pl(k, 'hundred')}?", good, bad, [f"1 hundred = 10 tens.", f"{pl(k, 'hundred')} = {good}."], r=r)
    it.check = FN("same_amount", value=100 * k)
    return it


@fam("012")
def hu_bags(r, L):
    k = 10 if L == 0 else r.randint(10, 19) if L == 1 else r.randint(12, 30)
    t = pick(r, [("bags", "marbles"), ("boxes", "crayons"), ("packs", "stickers"), ("cups", "beads")])
    return Item(f"{name(r)} has {k} {t[0]} with 10 {t[1]} in each. How many {t[1]} is that?",
                f"{10 * k} {t[1]}", [f"{k} tens = {pl(k // 10, 'hundred')} and {pl(k % 10, 'ten')}.", f"That is {10 * k} {t[1]}."],
                [W(f"{k} {t[1]}", "gave the number of " + t[0]), W(f"{k + 10} {t[1]}", "added instead of counting tens"), W(f"{10 * k + 10} {t[1]}", "counted one extra ten")],
                FN("tens_value", tens=k, unit=t[1]), qtype="word-problem", tags={"modeling"})


@fam("012")
def hu_need(r, L):
    have = r.randint(3, 9) if L < 2 else r.randint(11, 28)
    target = 100 if L < 2 else 100 * (have // 10 + 1)
    need(target > 10 * have)
    return Item(f"{name(r)} has {have} tens. How many more tens are needed to make {target}?",
                target // 10 - have, [f"{target} = {target // 10} tens.", f"{target // 10} − {have} = {target // 10 - have} more tens."],
                [W(target - have, "subtracted tens from ones"), W(target // 10 + have, "added instead of subtracting"), W(10 - have % 10 + 1, "made a counting mistake")],
                FN("more_tens", have=have, target=target), qtype="explain", tags={"reasoning"})


@fam("01")
def hu_count(r, L):
    start = r.randint(3, 6) * 10 if L == 0 else r.randint(5, 13) * 10
    seq = [start + 10 * i for i in range(5)]
    need(100 in seq or L == 1)
    need(L == 0 or seq[0] < 100 < seq[-1] or seq[0] >= 100)
    k = r.randint(1, 4)
    shown = ", ".join("?" if i == k else str(v) for i, v in enumerate(seq))
    return Item(f"Count by tens. What number is missing? {shown}", seq[k], ["Each number is 10 more than the one before.", f"The missing number is {seq[k]}."],
                [W(seq[k] + 1 if seq[k] % 100 else 1000, "counted by ones" if seq[k] % 100 else "wrote ten tens as 1,000"), W(seq[k] - 1, "counted by ones"), W(seq[k] + 10, "skipped a ten"), W(seq[k - 1] + 100, "counted by hundreds")],
                FN("skip_missing", seq=shown, step=10), qtype="procedural")


@fam("2", mode="mc")
def hu_explain(r, L):
    t = r.randint(11, 19)
    n = 10 * t
    good = f"{n} is 1 hundred and {pl(t - 10, 'ten')}, and 1 hundred is 10 tens, so there are {t} tens."
    bad = [f"{n} has the digit {t % 10} in the tens place, so there are {t % 10} tens.", f"{n} has 1 hundred, so there is 1 ten.", f"{n} has {n} tens because it ends in 0."]
    it = mc_key(f"How many tens are in {n}? Choose the best explanation.", good, bad, [f"1 hundred = 10 tens.", f"10 + {t - 10} = {t} tens."], qtype="explain", tags={"reasoning"}, r=r)
    it.check = FN("tens_reason", n=n)
    return it


# ============================================================== S2 Hundreds, Tens, and Ones
@fam("012")
def pv_blocks(r, L):
    n = three(r, min(L, 1))
    need(n // 100 <= 9)
    h, t, o = n // 100, n // 10 % 10, n % 10
    alt = f"Base-ten blocks: {pl(h, 'hundred')} flat{'s' if h != 1 else ''}, {t} tens rod{'s' if t != 1 else ''}, and {o} ones cube{'s' if o != 1 else ''}."
    return Item("What number do the base-ten blocks show?", n, [f"{pl(h, 'hundred')}, {pl(t, 'ten')}, and {pl(o, 'one')}.", f"{h * 100} + {t * 10} + {o} = {n}."],
                [W(h + t + o, "counted the blocks instead of their values"), W(int(f"{o}{t}{h}") if o else n + 100, "read the places in the wrong order"), W(n + 10, "counted one extra ten"), W(n - 100, "missed a hundred")],
                EX(f"{h}×100+{t}×10+{o}"), qtype="visual", diagram=Diagram("blocks", {"h": h, "t": t, "o": o}, alt))


@fam("012")
def pv_value(r, L):
    n = three(r, L)
    place = pick(r, ["hundreds", "tens", "ones"] if L else ["hundreds", "tens"])
    d = {"hundreds": n // 100, "tens": n // 10 % 10, "ones": n % 10}[place]
    need(d != 0 and str(n).count(str(d)) == 1)
    v = d * {"hundreds": 100, "tens": 10, "ones": 1}[place]
    return Item(f"What is the value of the digit {d} in {n}?", v, [f"The {d} is in the {place} place.", f"Its value is {v}."],
                [W(d if v != d else d * 10, "gave the digit, not its value"), W(d * 10 if place == "hundreds" else d * 100, "used the wrong place"), W(n, "gave the whole number")],
                FN("digit_value", n=str(n), place=place), qtype="conceptual", claim=f"Value of the {d} in {n}")


@fam("012")
def pv_hto(r, L):
    n = three(r, L, zero=(L == 2) or None)
    return Item(f"How many hundreds, tens, and ones are in {n}?", hto(n),
                [f"Look at each digit of {n}.", f"{n} = {n // 100 * 100} + {n // 10 % 10 * 10} + {n % 10}, so it is {hto(n)}."],
                [W(hto(int(str(n)[::-1])) if str(n)[-1] != "0" else hto(n + 100), "read the digits in the wrong order"), W(hto(n + 10) if n % 100 < 90 else hto(n - 10), "misread a digit")],
                FN("hto", n=n), qtype="procedural", claim=f"Hundreds, tens, and ones in {n}")


@fam("012")
def pv_build(r, L):
    n = three(r, L, zero=(L == 2) or None)
    h, t, o = n // 100, n // 10 % 10, n % 10
    return Item(f"What number has {hto(n)}?", n, ["Write a digit for each place.", f"{h} in the hundreds place, {t} in the tens place, {o} in the ones place: {n}."],
                [W(int(f"{h}{o}"), "left out the zero") if t == 0 else W(h * 100 + o * 10 + t if t != o else n + 1, "mixed up the tens and ones"),
                 W(h + t + o, "added the digits"), W(h * 100 + t * 10 + o + 100, "made a place-value mistake")],
                EX(f"{h}×100+{t}×10+{o}"), qtype="procedural", claim=f"The number with {hto(n)}")


@fam("01")
def pv_chart_read(r, L):
    n = three(r, L)
    alt = f"A place-value chart. Hundreds: {n // 100}. Tens: {n // 10 % 10}. Ones: {n % 10}."
    return Item("What number is shown in the place-value chart?", n, ["Read the digits from the hundreds to the ones.", f"The number is {n}."],
                [W(n // 100 + n // 10 % 10 + n % 10, "added the digits"), W(int(str(n)[::-1]) if n % 10 else n + 1, "read the chart backward"), W(n + 100, "made a place-value mistake")],
                EX(f"{n // 100}×100+{n // 10 % 10}×10+{n % 10}"), qtype="visual",
                diagram=Diagram("pv_chart", {"hundreds": n // 100, "tens": n // 10 % 10, "ones": n % 10}, alt))


@fam("012", mode="mc")
def pv_place(r, L):
    n = three(r, L)
    need(len(set(str(n))) == 3)
    place = pick(r, ["hundreds", "tens", "ones"])
    d = {"hundreds": n // 100, "tens": n // 10 % 10, "ones": n % 10}[place]
    others = [x for x in str(n) if x != str(d)]
    it = mc_key(f"Which digit is in the {place} place in {n}?", str(d), others + [str((d + 5) % 10) if str((d + 5) % 10) not in str(n) else str((d + 3) % 10)],
                ["Hundreds, tens, ones go from left to right.", f"The {place} digit is {d}."], r=r)
    it.check = FN("digit_in", n=n, place=place)
    return it


@fam("2")
def pv_unusual(r, L):
    h, t, o = r.randint(1, 7), r.randint(11, 19), r.randint(0, 9)
    n = 100 * h + 10 * t + o
    need(n < 1000)
    return Item(f"What number is {pl(h, 'hundred')}, {t} tens, and {pl(o, 'one')}?", n,
                [f"{t} tens = 1 hundred and {pl(t - 10, 'ten')}.", f"{100 * h} + {10 * t} + {o} = {n}."],
                [W(int(f"{h}{t}{o}"), "wrote the numbers side by side"), W(100 * h + 10 * (t - 10) + o, "dropped the extra hundred"), W(h + t + o, "added the numbers")],
                EX(f"{h}×100+{t}×10+{o}"), qtype="explain", tags={"reasoning"})


@fam("2", mode="mc")
def pv_error(r, L):
    h, o = r.randint(1, 9), r.randint(1, 9)
    n = 100 * h + o
    nm = name(r)
    good = f"No. The 0 is in the tens place, so {n} has 0 tens. It has {pl(h, 'hundred')} and {pl(o, 'one')}."
    bad = [f"Yes. {n} has {pl(h, 'ten')}.", f"No. {n} has {pl(o, 'ten')}.", f"Yes. The zero does not count, so the {h} is in the tens place."]
    it = mc_key(f"{nm} says {n} has {pl(h, 'ten')}. Is {nm} right?", good, bad, [f"{n} = {100 * h} + {o}.", f"There are {pl(h, 'hundred')}, 0 tens, and {pl(o, 'one')}."], qtype="error-analysis", tags={"misconception"}, r=r)
    it.check = FN("zero_tens", n=n)
    return it


# ============================================================== S3 Counting Hundreds
@fam("012")
def ch_flats(r, L):
    h = r.randint(1, 5) if L == 0 else r.randint(2, 9)
    alt = f"Base-ten blocks: {pl(h, 'hundred')} flat{'s' if h != 1 else ''}."
    return Item("Each flat is 1 hundred. What number do the blocks show?", 100 * h, [f"Count by hundreds: {', '.join(str(100 * i) for i in range(1, h + 1))}.", f"{pl(h, 'hundred')} = {100 * h}."],
                [W(h, "counted the flats as ones"), W(10 * h, "counted the flats as tens"), W(100 * h + 100, "counted one extra hundred"), W(1000 * h if h < 2 else 100 * h - 100, "made a counting mistake")],
                FN("hundreds_value", h=h), qtype="visual", diagram=Diagram("blocks", {"h": h}, alt))


@fam("012")
def ch_write(r, L):
    h = r.randint(1, 9)
    form = pick(r, ["num", "h"]) if L else "num"
    if form == "num":
        return Item(f"Write the number for {pl(h, 'hundred')}, 0 tens, and 0 ones.", 100 * h, [f"Put {h} in the hundreds place and 0 in the tens and ones places.", f"The number is {100 * h}."],
                    [W(h, "left out the zeros"), W(10 * h, "left out a zero"), W(1000 * h if h < 2 else 100 * (h + 1), "wrote too many zeros" if h < 2 else "made a counting mistake")],
                    FN("hundreds_value", h=h), qtype="procedural", claim=f"{pl(h, 'hundred')} as a number")
    return Item(f"{100 * h} is how many hundreds?", h, [f"{100 * h} has {h} in the hundreds place and zeros in the tens and ones places.", f"{100 * h} = {pl(h, 'hundred')}."],
                [W(10 * h, "counted tens instead of hundreds"), W(100 * h, "gave the number"), W(h + 1, "made a counting mistake")],
                FN("hundreds_count", n=100 * h), qtype="procedural", claim=f"Hundreds in {100 * h}")


@fam("012")
def ch_count(r, L):
    start = r.randint(1, 4) * 100 if L == 0 else r.randint(1, 5) * 100
    seq = [start + 100 * i for i in range(5)]
    k = r.randint(1, 4)
    shown = ", ".join("?" if i == k else str(v) for i, v in enumerate(seq))
    return Item(f"Count by hundreds. What number is missing? {shown}", seq[k], ["Each number is 100 more than the one before.", f"The missing number is {seq[k]}."],
                [W(seq[k - 1] + 10, "counted by tens"), W(seq[k - 1] + 1, "counted by ones"), W(seq[k] + 100, "skipped a hundred"), W(seq[k] // 100, "wrote only the hundreds digit")],
                FN("skip_missing", seq=shown, step=100), qtype="procedural")


@fam("012")
def ch_story(r, L):
    h = r.randint(2, 5) if L == 0 else r.randint(3, 9)
    t = pick(r, [("boxes", "paper clips"), ("crates", "apples"), ("bags", "beads"), ("rolls", "tickets")])
    return Item(f"A store has {h} {t[0]}. Each one holds 100 {t[1]}. How many {t[1]} are there?", f"{100 * h} {t[1]}",
                [f"Count by hundreds {h} times.", f"{pl(h, 'hundred')} = {100 * h} {t[1]}."],
                [W(f"{h + 100} {t[1]}", "added instead of counting hundreds"), W(f"{10 * h} {t[1]}", "counted tens"), W(f"{100 * h + 100} {t[1]}", "counted one extra hundred")],
                FN("hundreds_value", h=h, unit=t[1]), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def ch_which(r, L):
    h = r.randint(2, 9)
    good = pl(h, "hundred")
    bad = [pl(h, "ten"), pl(h * 10, "hundred"), pl(h * 100, "ten")] if L else [pl(h, "ten"), pl(h, "one"), pl(h * 10, "hundred")]
    it = mc_key(f"Which is the same as {100 * h}?", good, bad, [f"{100 * h} has {h} in the hundreds place.", f"{100 * h} = {good}."], r=r)
    it.check = FN("same_amount", value=100 * h)
    return it


@fam("12")
def ch_tens(r, L):
    h = r.randint(2, 9)
    return Item(f"How many tens make {100 * h}?", 10 * h, [f"1 hundred = 10 tens, so {pl(h, 'hundred')} = {h} groups of 10 tens.", f"{100 * h} is {10 * h} tens."],
                [W(h, "counted hundreds, not tens"), W(100 * h, "gave the number"), W(10 * h + 10, "counted one extra ten")],
                FN("tens_in", n=100 * h), qtype="conceptual", claim=f"Tens in {100 * h}")


@fam("2", mode="mc")
def ch_explain(r, L):
    h = r.randint(2, 9)
    nm = name(r)
    good = f"No. {100 * h} means {pl(h, 'hundred')}, 0 tens, and 0 ones, so the 0s are needed."
    bad = [f"Yes. {pl(h, 'hundred')} is the same as {h}.", f"Yes. Zeros have no value, so they can be left out.", f"No. It should be {1000 * h:,}."]
    it = mc_key(f"{nm} says {pl(h, 'hundred')} is written as {h}. Is {nm} right?", good, bad, [f"{pl(h, 'hundred')} = {100 * h}.", "The zeros show 0 tens and 0 ones."], qtype="error-analysis", tags={"misconception"}, r=r)
    it.check = FN("hundreds_reason", h=h)
    return it


@fam("2")
def ch_more(r, L):
    a, b = r.randint(1, 6), r.randint(1, 3)
    need(a + b <= 9)
    return Item(f"{name(r)} has {pl(a, 'hundred')} flats and gets {pl(b, 'hundred')} more. What number is that?", 100 * (a + b),
                [f"{a} + {b} = {a + b} hundreds.", f"{pl(a + b, 'hundred')} = {100 * (a + b)}."],
                [W(a + b, "left out the zeros"), W(100 * a + b, "added ones instead of hundreds"), W(100 * (a + b + 1), "counted one extra hundred")],
                FN("hundreds_value", h=a + b), qtype="multi-step", tags={"multistep"})


# ============================================================== S4 Numerals, Number Names, and Expanded Form
@fam("012")
def nn_numeral(r, L):
    n = three(r, L, zero=(L == 2) or None)
    return Item(f"Write the number in digits: {words(n)}", n, ["Find the hundreds, tens, and ones in the name.", f"{words(n)} = {n}."],
                [W(int(f"{n // 100}00{n % 100}") if n % 100 else n * 10, "wrote the hundreds as 00 and then the rest"), W(n // 100 * 10 + n % 10 if n // 10 % 10 == 0 else n + 10, "left out a zero" if n // 10 % 10 == 0 else "misread the tens"), W(n - 100, "misread the hundreds")],
                FN("from_words", words=words(n)), qtype="procedural", claim=f"{words(n)} in digits")


@fam("012")
def nn_words(r, L):
    n = three(r, L, zero=(L == 2) or None)
    return Item(f"Write {n} in words.", words(n), ["Say the hundreds, then the tens and ones.", f"{n} is {words(n)}."],
                [W(words(n // 100) + " hundred " + words(n % 100 + 10) if n % 100 < 90 and n % 100 else words(n + 100) if n < 900 else words(n - 100), "misread a digit")],
                FN("word_form", n=str(n)), qtype="procedural", claim=f"{n} in words")


@fam("012")
def nn_expanded(r, L):
    n = three(r, L, zero=(L == 2) or None)
    return Item(f"Write {n} in expanded form.", expanded(n), ["Write the value of each digit and add them.", f"{n} = {expanded(n)}."],
                [W(" + ".join(str(int(x)) for x in str(n) if x != "0"), "wrote digits instead of values"), W(f"{n // 100 * 100} + {n % 100 * 10}" if n % 100 else f"{n}", "used the wrong value for a place")],
                FN("expanded", n=str(n)), qtype="procedural", claim=f"{n} in expanded form")


@fam("012")
def nn_from_exp(r, L):
    n = three(r, L, zero=(L == 2) or None)
    e = expanded(n)
    return Item(f"What number is {e}?", n, ["Put each value in its place.", f"{e} = {n}."],
                [W(sum(int(x) for x in str(n)), "added the digits"), W(int(e.replace(' + ', '')) if len(e.replace(' + ', '')) < 5 else n + 100, "wrote the parts side by side"), W(n + 10, "made a place-value mistake")],
                EX(e.replace(" ", "")), qtype="procedural", claim=f"{e}")


@fam("012", mode="mc")
def nn_mc(r, L):
    n = three(r, L)
    need(n // 10 % 10 and n % 10 and len(set(str(n))) == 3)
    h, t, o = n // 100, n // 10 % 10, n % 10
    good = expanded(n)
    bad = [f"{h} + {t} + {o}", f"{h * 100} + {o * 10} + {t}", f"{h * 100} + {t * 100} + {o}" if L else f"{h * 10} + {t * 10} + {o}"]
    it = mc_key(f"Which shows {n} in expanded form?", good, bad, ["Each part is the value of one digit.", f"{n} = {good}."], r=r)
    it.check = FN("expanded", n=str(n))
    return it


@fam("2")
def nn_mixed(r, L):
    n = three(r, 2)
    parts = [p for p in (n // 100 * 100, n // 10 % 10 * 10, n % 10) if p]
    need(len(parts) == 3)
    r.shuffle(parts)
    need(parts[0] != n // 100 * 100)
    e = " + ".join(str(p) for p in parts)
    return Item(f"What number is {e}?", n, ["Put each value in its place, even when the parts are out of order.", f"{e} = {n}."],
                [W(int("".join(str(p)[0] for p in parts)), "wrote the parts in the order shown"), W(sum(int(x) for x in str(n)), "added the digits"), W(n + 100, "made a place-value mistake")],
                EX(e.replace(" ", "")), qtype="explain", tags={"reasoning"})


@fam("2", mode="mc")
def nn_error(r, L):
    h, o = r.randint(2, 9), r.randint(1, 9)
    n = 100 * h + o
    nm = name(r)
    wrong = f"{h}00{o}"
    good = f"{n}, because there are {pl(h, 'hundred')}, 0 tens, and {pl(o, 'one')}"
    bad = [f"{wrong}, because you write {100 * h} and then {o}", f"{h}{o}, because there are no tens", f"{h}{o}0, because the {o} goes in the tens place"]
    it = mc_key(f"{nm} wrote “{words(n)}” as {wrong}. What is the correct number?", good, bad, [f"“{words(n).capitalize()}” is {pl(h, 'hundred')} and {pl(o, 'one')}.", f"Use a 0 to hold the tens place: {n}."], qtype="error-analysis", tags={"misconception"}, r=r)
    it.check = FN("numeral_reason", n=n)
    return it


@fam("12", mode="mc")
def nn_match(r, L):
    n = three(r, L)
    need(n // 10 % 10 != n % 10 and n % 10 and n // 10 % 10)
    good = words(n)
    swp = n // 100 * 100 + n % 10 * 10 + n // 10 % 10
    bad = [words(swp), words(n + 100) if n < 900 else words(n - 100), words(n // 100 * 100 + n % 10)]
    it = mc_key(f"Which is the number name for {n}?", good, bad, ["Read the hundreds, then the tens and ones.", f"{n} is {good}."], r=r)
    it.check = FN("word_form", n=str(n))
    return it


SKILLS = {
    1: dict(name="A Hundred Is Ten Tens", fams=[hu_tens_in, hu_trade, hu_same, hu_bags, hu_need, hu_count, hu_explain]),
    2: dict(name="Hundreds, Tens, and Ones", fams=[pv_blocks, pv_value, pv_hto, pv_build, pv_chart_read, pv_place, pv_unusual, pv_error]),
    3: dict(name="Counting Hundreds", fams=[ch_flats, ch_write, ch_count, ch_story, ch_which, ch_tens, ch_explain, ch_more]),
    4: dict(name="Numerals, Number Names, and Expanded Form", fams=[nn_numeral, nn_words, nn_expanded, nn_from_exp, nn_mc, nn_mixed, nn_error, nn_match]),
}
