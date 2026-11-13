"""Unit 4: Rounding, Addition, and Subtraction within 1,000 (addition-subtraction-1000)."""
from g3lib import *

UNIT_ID = "addition-subtraction-1000"


def r10(n):
    return (n + 5) // 10 * 10


def r100(n):
    return (n + 50) // 100 * 100


def rnd(n, place):
    return r10(n) if place == "tens" else r100(n)


# ============================================================== S1 Rounding to the Nearest 10
def num10(r, L):
    if L == 0:
        return r.randint(11, 98)
    if L == 1:
        return r.randint(101, 989)
    n = r.randint(100, 995)
    return pick(r, [n, n // 10 * 10 + 5, n // 100 * 100 + 95 if n % 1000 < 900 else n, n // 10 * 10 + 4])


def round_wrongs(n, place):
    s = 10 if place == "tens" else 100
    lo = n // s * s
    out = [W(lo if rnd(n, place) != lo else lo + s, "rounded the wrong way"), W(n // 10 * 10 if place == "hundreds" else n // 100 * 100, "rounded to the wrong place")]
    if place == "tens":
        out.append(W(r100(n), "rounded to the nearest hundred"))
    else:
        out.append(W(r10(n), "rounded to the nearest ten"))
    out.append(W(lo + 2 * s, "jumped past the nearest " + ("ten" if s == 10 else "hundred")))
    return out


@fam("012")
def ro10(r, L):
    n = num10(r, L)
    need(n % 10)
    a = r10(n)
    return Item(f"Round {comma(n)} to the nearest 10.", comma(a),
                [f"{comma(n)} is between {comma(n // 10 * 10)} and {comma(n // 10 * 10 + 10)}.", f"The ones digit is {n % 10}, so {comma(n)} rounds to {comma(a)}."],
                round_wrongs(n, "tens"), FN("round_to", x=n, place="tens"), qtype="procedural", claim=f"{comma(n)} rounded to the nearest 10")


@fam("01")
def ro10_line(r, L):
    n = num10(r, L)
    need(n % 10 and n % 10 != 5)
    lo = n // 10 * 10
    alt = f"A number line from {lo} to {lo + 10} with a tick for every 1. A point is at {n}."
    return Item(f"The point on the number line shows {comma(n)}. Which ten is it closer to?", comma(r10(n)),
                [f"{comma(n)} is between {comma(lo)} and {comma(lo + 10)}.", f"It is closer to {comma(r10(n))}."],
                [W(comma(lo + 10 if r10(n) == lo else lo), "chose the farther ten"), W(comma(lo + 5), "chose the halfway mark"), W(comma(n), "did not round")],
                FN("round_to", x=n, place="tens"), qtype="visual",
                diagram=Diagram("wholeline", {"lo": lo, "hi": lo + 10, "step": 1, "label_every": 5, "points": [{"v": n, "label": "?"}]}, alt))


@fam("012", mode="mc")
def ro10_which(r, L):
    t = r.randint(2, 9) * 10 if L == 0 else r.randint(11, 98) * 10
    good = t + pick(r, [-5, -4, -3, -2, 1, 2, 3, 4])
    bad = [t + 5, t - 6, t + 10] if L else [t + 6, t - 7, t + 12]
    it = mc_key(f"Which number rounds to {comma(t)} when rounded to the nearest 10?", comma(good), [comma(x) for x in bad],
                [f"Numbers from {comma(t - 5)} to {comma(t + 4)} round to {comma(t)}.", f"{comma(good)} rounds to {comma(t)}."], r=r)
    it.check = FN("rounds_to", target=t, place="tens")
    return it


@fam("012")
def ro10_story(r, L):
    n = num10(r, L)
    need(n % 10)
    t = pick(r, [("There are {n} people at the game. About how many people is that, to the nearest 10?", "people"),
                 ("A book has {n} pages. About how many pages is that, to the nearest 10?", "pages"),
                 ("{nm} counted {n} cars in the parking lot. About how many cars is that, to the nearest 10?", "cars")])
    return Item(t[0].format(n=comma(n), nm=name(r)), f"{comma(r10(n))} {t[1]}", [f"{comma(n)} is between {comma(n // 10 * 10)} and {comma(n // 10 * 10 + 10)}.", f"It rounds to {comma(r10(n))}."],
                [W(f"{w[0]} {t[1]}", w[1]) for w in round_wrongs(n, "tens")], FN("round_to", x=n, place="tens", unit=t[1]), qtype="word-problem")


@fam("2")
def ro10_range(r, L):
    t = r.randint(11, 98) * 10
    which = pick(r, ["greatest", "least"])
    a = t + 4 if which == "greatest" else t - 5
    return Item(f"What is the {which} whole number that rounds to {comma(t)} when rounded to the nearest 10?", comma(a),
                [f"Numbers from {comma(t - 5)} to {comma(t + 4)} round to {comma(t)}.", f"The {which} is {comma(a)}."],
                [W(comma(t + 5 if which == "greatest" else t - 4), "forgot that 5 rounds up"), W(comma(t + 9 if which == "greatest" else t - 9), "used the whole ten"), W(comma(t), "gave the rounded number")],
                FN("round_extreme", target=t, place="tens", which=which), qtype="explain", tags={"reasoning"})


@fam("2", mode="mc")
def ro10_error(r, L):
    n = r.randint(101, 989)
    need(n % 10 >= 5 and n % 10 != 0)
    wrong = n // 100 * 100
    good = f"It should be {comma(r10(n))}. Look at the ones digit to round to the nearest 10."
    bad = [f"It is correct. {comma(wrong)} is the nearest 10.", f"It should be {comma(n // 10 * 10)}. Always round down.", f"It should be {comma(r100(n) if r100(n) != wrong else wrong + 100)}. Round up to the next hundred."]
    return mc_key(f"{name(r)} rounded {comma(n)} to the nearest 10 and got {comma(wrong)}. What is the correct answer?", good, bad,
                  [f"{comma(wrong)} is a hundred, not the nearest ten.", f"{comma(n)} is between {comma(n // 10 * 10)} and {comma(n // 10 * 10 + 10)}; the ones digit is {n % 10}, so round to {comma(r10(n))}."],
                  qtype="error-analysis", tags={"misconception"}, r=r)


# ============================================================== S2 Rounding to the Nearest 100
def num100(r, L):
    if L == 0:
        return r.randint(101, 899)
    if L == 1:
        return r.randint(101, 989)
    n = r.randint(100, 999)
    return pick(r, [n, n // 100 * 100 + 50, n // 100 * 100 + 49, 950 + r.randint(0, 49)])


@fam("012")
def ro100(r, L):
    n = num100(r, L)
    need(n % 100)
    a = r100(n)
    return Item(f"Round {comma(n)} to the nearest 100.", comma(a),
                [f"{comma(n)} is between {comma(n // 100 * 100)} and {comma(n // 100 * 100 + 100)}.", f"The tens digit is {n // 10 % 10}, so {comma(n)} rounds to {comma(a)}."],
                round_wrongs(n, "hundreds"), FN("round_to", x=n, place="hundreds"), qtype="procedural", claim=f"{comma(n)} rounded to the nearest 100")


@fam("01")
def ro100_line(r, L):
    n = num100(r, L)
    need(n % 10 == 0 and n % 100 and n % 100 != 50)
    lo = n // 100 * 100
    alt = f"A number line from {lo} to {lo + 100} with a tick for every 10. A point is at {n}."
    return Item(f"The point on the number line shows {comma(n)}. Which hundred is it closer to?", comma(r100(n)),
                [f"{comma(n)} is between {comma(lo)} and {comma(lo + 100)}.", f"It is closer to {comma(r100(n))}."],
                [W(comma(lo + 100 if r100(n) == lo else lo), "chose the farther hundred"), W(comma(lo + 50), "chose the halfway mark"), W(comma(n), "did not round")],
                FN("round_to", x=n, place="hundreds"), qtype="visual",
                diagram=Diagram("wholeline", {"lo": lo, "hi": lo + 100, "step": 10, "label_every": 5, "points": [{"v": n, "label": "?"}]}, alt))


@fam("012", mode="mc")
def ro100_which(r, L):
    t = r.randint(2, 9) * 100
    good = t + pick(r, [-50, -40, -20, -8, 12, 30, 44, 49])
    bad = [t + 50, t - 51, t + 100] if L else [t + 60, t - 70, t + 150]
    it = mc_key(f"Which number rounds to {comma(t)} when rounded to the nearest 100?", comma(good), [comma(x) for x in bad],
                [f"Numbers from {comma(t - 50)} to {comma(t + 49)} round to {comma(t)}.", f"{comma(good)} rounds to {comma(t)}."], r=r)
    it.check = FN("rounds_to", target=t, place="hundreds")
    return it


@fam("012")
def ro100_story(r, L):
    n = num100(r, L)
    need(n % 100)
    t = pick(r, [("A school has {n} students. About how many students is that, to the nearest 100?", "students"),
                 ("A farm has {n} chickens. About how many chickens is that, to the nearest 100?", "chickens"),
                 ("A bike trip is {n} miles long. About how many miles is that, to the nearest 100?", "miles")])
    return Item(t[0].format(n=comma(n)), f"{comma(r100(n))} {t[1]}", [f"{comma(n)} is between {comma(n // 100 * 100)} and {comma(n // 100 * 100 + 100)}.", f"It rounds to {comma(r100(n))}."],
                [W(f"{w[0]} {t[1]}", w[1]) for w in round_wrongs(n, "hundreds")], FN("round_to", x=n, place="hundreds", unit=t[1]), qtype="word-problem")


@fam("2")
def ro100_range(r, L):
    t = r.randint(2, 9) * 100
    which = pick(r, ["greatest", "least"])
    a = t + 49 if which == "greatest" else t - 50
    return Item(f"What is the {which} whole number that rounds to {comma(t)} when rounded to the nearest 100?", comma(a),
                [f"Numbers from {comma(t - 50)} to {comma(t + 49)} round to {comma(t)}.", f"The {which} is {comma(a)}."],
                [W(comma(t + 50 if which == "greatest" else t - 49), "forgot that 50 rounds up"), W(comma(t + 99 if which == "greatest" else t - 99), "used the whole hundred"), W(comma(t + 4 if which == "greatest" else t - 5), "rounded to the nearest 10")],
                FN("round_extreme", target=t, place="hundreds", which=which), qtype="explain", tags={"reasoning"})


@fam("2", mode="mc")
def ro_both(r, L):
    n = r.randint(101, 989)
    need(n % 10 and r10(n) != r100(n))
    good = f"{comma(r10(n))} to the nearest 10 and {comma(r100(n))} to the nearest 100"
    bad = [f"{comma(r100(n))} to the nearest 10 and {comma(r10(n))} to the nearest 100", f"{comma(n // 10 * 10 if n // 10 * 10 != r10(n) else n // 10 * 10 + 10)} to the nearest 10 and {comma(r100(n))} to the nearest 100",
           f"{comma(r10(n))} to the nearest 10 and {comma(n // 100 * 100 if n // 100 * 100 != r100(n) else n // 100 * 100 + 100)} to the nearest 100"]
    return mc_key(f"Round {comma(n)} to the nearest 10 and to the nearest 100.", good, bad,
                  [f"Nearest 10: look at the ones digit {n % 10}. Nearest 100: look at the tens digit {n // 10 % 10}.", good + "."], qtype="compare-strategies", tags={"reasoning"}, r=r)


# ============================================================== S3 Adding within 1,000
def addends(r, L):
    if L == 0:
        a, b = r.randint(110, 450), r.randint(102, 350)
        need((a % 10 + b % 10) < 10 or r.random() < 0.6)
    elif L == 1:
        a, b = r.randint(150, 650), r.randint(120, 340)
    else:
        a, b = r.randint(250, 699), r.randint(198, 299)
    need(a + b <= 1000)
    return a, b


def add_wrongs(a, b):
    s = a + b
    no_carry = int("".join(str((int(x) + int(y)) % 10) for x, y in zip(str(a).zfill(3), str(b).zfill(3))))
    out = []
    if no_carry != s:
        out.append(W(comma(no_carry), "did not regroup"))
    out += [W(comma(s + 10), "added an extra regrouped ten"), W(comma(s - 10), "forgot a regrouped ten"), W(comma(s + 100), "added an extra hundred"), W(comma(abs(a - b)), "subtracted instead of adding")]
    return out


@fam("012")
def ad_std(r, L):
    a, b = addends(r, L)
    return Item(f"Add: {comma(a)} + {comma(b)}", comma(a + b), [f"Add the ones, then the tens, then the hundreds, regrouping when a place has 10 or more.", f"{comma(a)} + {comma(b)} = {comma(a + b)}."],
                add_wrongs(a, b), EX(f"{a}+{b}"), qtype="procedural", claim=f"{comma(a)} + {comma(b)}")


@fam("01")
def ad_expanded(r, L):
    a, b = addends(r, L)
    h, t, o = a // 100 * 100 + b // 100 * 100, a // 10 % 10 * 10 + b // 10 % 10 * 10, a % 10 + b % 10
    return Item(f"{name(r)} adds {comma(a)} + {comma(b)} by place: hundreds {h}, tens {t}, ones {o}. What is the sum?", comma(a + b),
                [f"Add the place values: {h} + {t} + {o}.", f"{h} + {t} + {o} = {comma(a + b)}."],
                [W(comma(h + t), "left out the ones"), W(str(h // 100) + str(t // 10) + str(o) if t < 100 and o < 10 else comma(a + b + 100), "wrote the place totals side by side"), W(comma(a + b - 10), "made an addition mistake")],
                EX(f"{h}+{t}+{o}"), qtype="compare-strategies", tags={"multiple-representations"})


@fam("012")
def ad_word(r, L):
    a, b = addends(r, L)
    t = pick(r, [("A library has {a} picture books and {b} chapter books. How many books is that in all?", "books"),
                 ("{nm} rode {a} miles in June and {b} miles in July. How many miles is that in all?", "miles"),
                 ("A school collected {a} cans on Monday and {b} cans on Tuesday. How many cans did it collect?", "cans")])
    return Item(t[0].format(a=comma(a), b=comma(b), nm=name(r)), f"{comma(a + b)} {t[1]}", [f"Add {comma(a)} + {comma(b)}.", f"{comma(a)} + {comma(b)} = {comma(a + b)} {t[1]}."],
                [W(f"{w[0]} {t[1]}", w[1]) for w in add_wrongs(a, b)], EX(f"{a}+{b}", unit=t[1]), qtype="word-problem", tags={"modeling"})


@fam("12", mode="mc")
def ad_mc(r, L):
    a, b = addends(r, L)
    it = Item(f"What is {comma(a)} + {comma(b)}?", comma(a + b), [f"Line up the places and add, regrouping as needed.", f"{comma(a)} + {comma(b)} = {comma(a + b)}."],
              add_wrongs(a, b), EX(f"{a}+{b}"), qtype="procedural", mode="mc")
    return it


@fam("2")
def ad_missing_digit(r, L):
    a, b = addends(r, L)
    s = a + b
    d = a // 10 % 10
    shown = str(a)[0] + "□" + str(a)[2]
    return Item(f"Find the missing digit: {shown} + {comma(b)} = {comma(s)}", d,
                [f"{comma(s)} − {comma(b)} = {comma(a)}.", f"So the missing digit is {d}."],
                [W((d + 1) % 10, "forgot a regrouped ten"), W((s // 10 % 10), "copied the tens digit of the sum"), W((d + 9) % 10, "regrouped the wrong way")],
                FN("missing_digit", shown=shown, other=b, total=s, op="+"), qtype="explain", tags={"reasoning"})


@fam("2")
def ad_three(r, L):
    a, b, c = r.randint(105, 399), r.randint(105, 299), r.randint(15, 199)
    need(a + b + c <= 1000)
    return Item(f"Add: {comma(a)} + {comma(b)} + {comma(c)}", comma(a + b + c), [f"{comma(a)} + {comma(b)} = {comma(a + b)}.", f"{comma(a + b)} + {comma(c)} = {comma(a + b + c)}."],
                [W(comma(a + b), "left out an addend"), W(comma(a + b + c - 10), "forgot a regrouped ten"), W(comma(a + b + c + 100), "added an extra hundred")], EX(f"{a}+{b}+{c}"), qtype="multi-step", tags={"multistep"})


# ============================================================== S4 Subtracting within 1,000
def subs(r, L):
    if L == 0:
        a, b = r.randint(300, 899), r.randint(100, 299)
        need(a % 10 >= b % 10 or r.random() < 0.4)
    elif L == 1:
        a, b = r.randint(300, 999), r.randint(120, 299)
    else:
        a = pick(r, [r.randint(2, 9) * 100, r.randint(2, 9) * 100 + r.randint(1, 9), r.randint(301, 999)])
        b = r.randint(118, a - 50) if a > 170 else 0
    need(a > b > 0)
    return a, b


def sub_wrongs(a, b):
    d = a - b
    sm = int("".join(str(abs(int(x) - int(y))) for x, y in zip(str(a).zfill(3), str(b).zfill(3))))
    out = []
    if sm != d:
        out.append(W(comma(sm), "subtracted the smaller digit from the larger digit in each place"))
    out += [W(comma(d + 10), "forgot to take away the regrouped ten"), W(comma(d + 100), "forgot to take away the regrouped hundred"), W(comma(a + b), "added instead of subtracting"), W(comma(d - 10), "subtracted an extra ten")]
    return out


@fam("012")
def sb_std(r, L):
    a, b = subs(r, L)
    return Item(f"Subtract: {comma(a)} − {comma(b)}", comma(a - b), ["Subtract ones, tens, then hundreds. Regroup when the top digit is too small.", f"{comma(a)} − {comma(b)} = {comma(a - b)}."],
                sub_wrongs(a, b), EX(f"{a}-{b}"), qtype="procedural", claim=f"{comma(a)} − {comma(b)}")


@fam("012")
def sb_word(r, L):
    a, b = subs(r, L)
    t = pick(r, [("A theater has {a} seats. {b} seats are filled. How many seats are empty?", "seats"),
                 ("{nm} has {a} points. {nm2} has {b} points. How many more points does {nm} have?", "points"),
                 ("A store had {a} pencils. It sold {b} pencils. How many pencils are left?", "pencils")])
    return Item(t[0].format(a=comma(a), b=comma(b), nm=name(r), nm2=name(sub(r, 3))), f"{comma(a - b)} {t[1]}", [f"Subtract {comma(a)} − {comma(b)}.", f"{comma(a)} − {comma(b)} = {comma(a - b)} {t[1]}."],
                [W(f"{w[0]} {t[1]}", w[1]) for w in sub_wrongs(a, b)], EX(f"{a}-{b}", unit=t[1]), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def sb_check(r, L):
    a, b = subs(r, L)
    good = f"{comma(a - b)} + {comma(b)} = {comma(a)}"
    bad = [f"{comma(a - b)} − {comma(b)} = {comma(a - 2 * b)}" if a > 2 * b else f"{comma(a)} + {comma(b)} = {comma(a + b)}", f"{comma(a)} + {comma(b)} = {comma(a + b)}" if a > 2 * b else f"{comma(b)} − {comma(a - b)} = {comma(abs(2 * b - a))}",
           f"{comma(a - b)} + {comma(a)} = {comma(2 * a - b)}"]
    need(len(set(bad)) == 3 and good not in bad)
    return mc_key(f"{name(r)} found {comma(a)} − {comma(b)} = {comma(a - b)}. Which addition equation checks the answer?", good, bad,
                  ["Add the difference to the number subtracted.", f"{comma(a - b)} + {comma(b)} = {comma(a)}, so the answer is correct."], qtype="conceptual", tags={"connections"}, r=r)


@fam("12")
def sb_zeros(r, L):
    a = r.randint(2, 9) * 100 + pick(r, [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    b = r.randint(101, a - 20) if a > 140 else 0
    need(b > 0 and b % 10)
    return Item(f"Subtract: {comma(a)} − {comma(b)}", comma(a - b), [f"There are zeros in the tens place of {comma(a)}, so regroup a hundred into tens, then a ten into ones.", f"{comma(a)} − {comma(b)} = {comma(a - b)}."],
                sub_wrongs(a, b), EX(f"{a}-{b}"), qtype="procedural", claim=f"{comma(a)} − {comma(b)}")


@fam("2")
def sb_missing(r, L):
    a, b = subs(r, L)
    form = pick(r, ["sub", "add"])
    if form == "sub":
        eq = f"{comma(a)} − ___ = {comma(a - b)}"
        ans = b
    else:
        eq = f"___ + {comma(b)} = {comma(a)}"
        ans = a - b
    return Item(f"What number makes the equation true? {eq}", comma(ans), ["Use the relationship between addition and subtraction.", f"{eq.replace('___', comma(ans))}."],
                [W(comma(a + (b if form == 'sub' else 0) + (0 if form == 'sub' else b)), "added instead of subtracting"), W(comma(ans + 10), "forgot a regrouped ten"), W(comma(ans + 100), "forgot a regrouped hundred")],
                FN("blank_eq", eq=eq.replace(",", "")), qtype="fill-blank", tags={"connections"})


@fam("2")
def sb_compare(r, L):
    a, b, c = r.randint(400, 999), r.randint(120, 380), r.randint(150, 390)
    need(a - b - c > 0 and b != c)
    return Item(f"A truck can carry {comma(a)} pounds. It already has boxes of {comma(b)} pounds and {comma(c)} pounds. How many more pounds can it carry?",
                f"{comma(a - b - c)} pounds", [f"{comma(b)} + {comma(c)} = {comma(b + c)} pounds are on the truck.", f"{comma(a)} − {comma(b + c)} = {comma(a - b - c)} pounds."],
                [W(f"{comma(a - b)} pounds", "subtracted only one box"), W(f"{comma(a - b + c)} pounds", "added the second box instead of subtracting it"), W(f"{comma(b + c)} pounds", "found the weight on the truck")],
                EX(f"{a}-{b}-{c}", unit="pounds"), qtype="multi-step", tags={"multistep"})


# ============================================================== S5 Estimating to Check
@fam("012")
def es_sum(r, L):
    place = "hundreds" if L != 1 or r.random() < 0.5 else "tens"
    a, b = r.randint(110, 480), r.randint(110, 480)
    op = pick(r, ["+", "−"]) if L else "+"
    if op == "−":
        a, b = max(a, b) + 200, min(a, b)
    need(a <= 999 and a % 10 and b % 10)
    ra, rb = rnd(a, place), rnd(b, place)
    est = ra + rb if op == "+" else ra - rb
    word = "10" if place == "tens" else "100"
    return Item(f"Estimate {comma(a)} {op} {comma(b)} by rounding each number to the nearest {word}.", comma(est),
                [f"{comma(a)} rounds to {comma(ra)} and {comma(b)} rounds to {comma(rb)}.", f"{comma(ra)} {op} {comma(rb)} = {comma(est)}."],
                [W(comma(a + b if op == '+' else a - b), "found the exact answer instead of estimating"), W(comma(est + (10 if place == 'tens' else 100)), "rounded one number the wrong way"),
                 W(comma(est - (10 if place == 'tens' else 100)), "rounded one number the wrong way"), W(comma(rnd(a, 'tens' if place == 'hundreds' else 'hundreds') + (rb if op == '+' else -rb)), "rounded the numbers to different places")],
                FN("estimate", a=a, b=b, op=op, place=place), qtype="procedural", claim=f"Estimate {comma(a)} {op} {comma(b)}")


@fam("012", mode="mc")
def es_reasonable(r, L):
    a, b = r.randint(210, 480), r.randint(210, 480)
    op = pick(r, ["+", "−"]) if L else "+"
    if op == "−":
        a, b = max(a, b) + 300, min(a, b)
    need(a <= 999)
    exact = a + b if op == "+" else a - b
    ok = r.random() < 0.4
    shown = exact if ok else exact + pick(r, [100, -100, 200])
    ra, rb = r100(a), r100(b)
    est = ra + rb if op == "+" else ra - rb
    need(ok or abs(shown - est) >= 100)
    need(0 < shown <= 999)
    need(abs(exact - est) < 100)
    good = (f"Yes. It is close to the estimate {comma(est)}." if ok else f"No. The estimate is {comma(est)}, so {comma(shown)} is too far away.")
    bad = ([f"No. The estimate is {comma(est)}, so {comma(shown)} is too far away.", f"No. The answer must end in 0.", f"Yes. It is close to {comma(est + 300)}."] if ok else
           [f"Yes. It is close to the estimate {comma(est)}.", f"Yes. Any three-digit answer is reasonable.", f"No. The estimate is {comma(shown)}."])
    it = mc_key(f"{name(r)} says {comma(a)} {op} {comma(b)} = {comma(shown)}. Round to the nearest 100 to estimate. Is the answer reasonable?", good, bad,
                [f"{comma(a)} → {comma(ra)} and {comma(b)} → {comma(rb)}, so the estimate is {comma(est)}.", "Yes, the answer is close to the estimate." if ok else f"The exact answer is {comma(exact)}, so {comma(shown)} is not reasonable."],
                qtype="explain", tags={"reasoning"}, r=r)
    it.check = FN("reasonable", a=a, b=b, op=op, shown=shown)
    return it


@fam("012")
def es_word(r, L):
    a, b = r.randint(120, 480), r.randint(120, 480)
    need(a % 100 and b % 100)
    return Item(f"A farm stand sold {comma(a)} apples on Saturday and {comma(b)} apples on Sunday. Round each number to the nearest 100. About how many apples were sold?",
                f"{comma(r100(a) + r100(b))} apples", [f"{comma(a)} → {comma(r100(a))}; {comma(b)} → {comma(r100(b))}.", f"{comma(r100(a))} + {comma(r100(b))} = {comma(r100(a) + r100(b))} apples."],
                [W(f"{comma(a + b)} apples", "found the exact sum"), W(f"{comma(r10(a) + r10(b))} apples", "rounded to the nearest 10"), W(f"{comma(r100(a) + r100(b) + 100)} apples", "rounded one number up by mistake")],
                FN("estimate", a=a, b=b, op="+", place="hundreds", unit="apples"), qtype="word-problem")


@fam("12", mode="mc")
def es_which(r, L):
    a, b = r.randint(150, 450), r.randint(150, 450)
    need(a % 100 and b % 100 and r100(a) + r100(b) != a + b)
    exact = a + b
    est = r100(a) + r100(b)
    cands = [exact, exact + 100, exact - 100, exact + 200]
    good = comma(exact)
    bad = [comma(x) for x in cands[1:]]
    it = mc_key(f"The estimate for {comma(a)} + {comma(b)} is {comma(est)}. Which exact answer is reasonable AND correct?", good, bad,
                [f"Add exactly: {comma(a)} + {comma(b)} = {comma(exact)}.", f"{comma(exact)} is close to {comma(est)}."], r=r)
    it.check = EX(f"{a}+{b}")
    return it


@fam("2")
def es_two_step(r, L):
    a, b, c = r.randint(310, 690), r.randint(110, 290), r.randint(110, 290)
    need(a + b - c > 0 and a % 100 and b % 100 and c % 100)
    return _es2(a, b, c, r100(a) + r100(b) - r100(c))


def _es2(a, b, c, est):
    it = Item(f"A shop had {comma(a)} toys. It got {comma(b)} more and sold {comma(c)}. Round each number to the nearest 100 to estimate how many toys are left.",
              f"{comma(est)} toys", [f"{comma(a)} → {comma(r100(a))}, {comma(b)} → {comma(r100(b))}, {comma(c)} → {comma(r100(c))}.", f"{comma(r100(a))} + {comma(r100(b))} − {comma(r100(c))} = {comma(est)} toys."],
              [W(f"{comma(a + b - c)} toys", "found the exact answer"), W(f"{comma(r100(a) + r100(b) + r100(c))} toys", "added the toys that were sold"), W(f"{comma(est + 100)} toys", "rounded one number the wrong way")],
              FN("estimate3", a=a, b=b, c=c, unit="toys"), qtype="multi-step", tags={"multistep"})
    return it


SKILLS = {
    1: dict(name="Rounding to the Nearest 10", fams=[ro10, ro10_line, ro10_which, ro10_story, ro10_range, ro10_error]),
    2: dict(name="Rounding to the Nearest 100", fams=[ro100, ro100_line, ro100_which, ro100_story, ro100_range, ro_both]),
    3: dict(name="Adding within 1,000", fams=[ad_std, ad_expanded, ad_word, ad_mc, ad_missing_digit, ad_three]),
    4: dict(name="Subtracting within 1,000", fams=[sb_std, sb_word, sb_check, sb_zeros, sb_missing, sb_compare]),
    5: dict(name="Estimating to Check Sums and Differences", fams=[es_sum, es_reasonable, es_word, es_which, es_two_step]),
}
