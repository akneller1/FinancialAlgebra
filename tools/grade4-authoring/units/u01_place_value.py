"""Unit 1: Place Value and Number Sense (4.NBT.A.1-3)."""
from g4lib import *

UNIT_ID = "place-value-number-sense"
THINGS = [("stadium", "seats"), ("library", "books"), ("city", "people"), ("farm", "apple trees"), ("website", "visitors"),
          ("factory", "toy cars"), ("museum", "visitors"), ("warehouse", "boxes"), ("park", "trees"), ("school district", "students")]


def digs(L):
    return {0: (4, 5), 1: (5, 6), 2: (6, 6)}[L]


def number(r, L, lo=None, hi=None, nozero=False):
    a, b = digs(L)
    k = r.randint(lo or a, hi or b)
    while True:
        n = r.randint(10 ** (k - 1), 10 ** k - 1)
        if not nozero or "0" not in str(n):
            return n


def unique_digit(r, n):
    s = str(n)
    c = [i for i, ch in enumerate(s) if s.count(ch) == 1 and ch != "0"]
    need(c)
    i = pick(r, c)
    return int(s[i]), len(s) - 1 - i


def sg(place):
    return place[:-1]


# ============================================================== S1 Place Value to One Million
@fam("012")
def pv_digit_value(r, L):
    n = number(r, L)
    d, e = unique_digit(r, n)
    v = d * 10 ** e
    return Item(f"What is the value of the digit {d} in {comma(n)}?", comma(v),
                [f"The digit {d} is in the {PLACE_NAMES[e]} place.", f"{d} × {comma(10 ** e)} = {comma(v)}."],
                [W(str(d), "gave the digit instead of its value"), W(comma(d * 10 ** (e + 1)), "named the place one to the left"),
                 W(comma(d * 10 ** (e - 1)) if e > 1 else comma(d * 100), "named the place one to the right"), W(comma(10 ** e) if d != 1 else comma(2 * 10 ** e), "gave the place value, not the digit's value")],
                FN("digit_value", n=str(n), place=PLACE_NAMES[e]), claim=f"Value of the digit {d} in {comma(n)}")


@fam("012", mode="mc")
def pv_place_name(r, L):
    n = number(r, L)
    d, e = unique_digit(r, n)
    others = [p for i, p in enumerate(PLACE_NAMES[:6]) if i != e]
    r.shuffle(others)
    bad = sorted(others[:3], key=PLACE_NAMES.index)
    return Item(f"In {comma(n)}, which place is the digit {d} in?", PLACE_NAMES[e],
                ["Start at the ones place on the right and move left: ones, tens, hundreds, thousands, ten thousands, hundred thousands.", f"The digit {d} is in the {PLACE_NAMES[e]} place."],
                [W(b, "counted the places incorrectly") for b in bad], FN("place_of", n=str(n), digit=d), qtype="conceptual")


@fam("012")
def pv_ten_times(r, L):
    d = r.randint(1, 9)
    e = r.randint(0, 2 + L)
    gap = 2 if (L == 2 and r.random() < 0.5) else 1
    hi_, lo_ = d * 10 ** (e + gap), d * 10 ** e
    other = [r.randint(0, 9) for _ in range(6)]
    k = e + gap + 1 + (1 if r.random() < 0.4 and e + gap < 5 else 0)
    ds = [other[i] if other[i] != d else (d + 1) % 10 for i in range(k)]
    ds[e], ds[e + gap] = d, d
    if ds[-1] == 0:
        ds[-1] = d if k - 1 in (e, e + gap) else (d % 9) + 1
    n = int("".join(str(x) for x in reversed(ds)))
    need(str(n).count(str(d)) == 2)
    ans = 10 ** gap
    return Item(f"In {comma(n)}, the digit {d} appears twice. How many times as much is the value of the {d} in the {PLACE_NAMES[e + gap]} place as the value of the {d} in the {PLACE_NAMES[e]} place?",
                comma(ans), [f"The {d} in the {PLACE_NAMES[e + gap]} place is worth {comma(hi_)}. The {d} in the {PLACE_NAMES[e]} place is worth {comma(lo_)}.",
                             f"{comma(hi_)} ÷ {comma(lo_)} = {comma(ans)}, so it is {comma(ans)} times as much."],
                [W(comma(hi_ - lo_), "subtracted the two values instead of comparing by multiplication"), W(str(d), "gave the digit"), W("1", "thought the same digit always has the same value"),
                 W(comma(ans * 10), "moved one place too many")],
                FN("times", a=str(hi_), b=str(lo_)), qtype="conceptual", tags={"reasoning"})


@fam("012")
def pv_times_ten_blank(r, L):
    d = r.randint(1, 9) * (1 if L == 0 else pick(r, [1, 1, 11, 12, 25]))
    e = r.randint(1, 2 + L)
    a = d * 10 ** e
    kind = r.randrange(3)
    if kind == 0:
        return Item(f"{comma(a)} is 10 times as much as what number?", comma(a // 10), [f"Divide by 10 to find the number: {comma(a)} ÷ 10 = {comma(a // 10)}.", f"Check: 10 × {comma(a // 10)} = {comma(a)}."],
                    [W(comma(a * 10), "multiplied by 10 instead of dividing"), W(comma(a - 10), "subtracted 10"), W(comma(a // 100) if a % 100 == 0 else comma(a // 10 + 10), "moved two places")],
                    EX(f"{a} ÷ 10"), claim=f"{comma(a)} is 10 times as much as")
    if kind == 1:
        return Item(f"What number is 10 times as much as {comma(a)}?", comma(a * 10), [f"Each digit moves one place to the left: 10 × {comma(a)} = {comma(a * 10)}."],
                    [W(comma(a + 10), "added 10 instead of multiplying"), W(comma(a // 10), "divided by 10"), W(comma(a * 100), "moved two places")], EX(f"10 × {a}"), claim=f"10 times as much as {comma(a)}")
    return Item(f"Fill in the blank: {comma(a * 10)} ÷ 10 = ___", comma(a), [f"Dividing by 10 moves each digit one place to the right: {comma(a * 10)} ÷ 10 = {comma(a)}."],
                [W(comma(a * 100), "multiplied by 10"), W(comma(a * 10 - 10), "subtracted 10"), W(comma(a // 10), "moved two places")], EX(f"{a * 10} ÷ 10"), qtype="fill-blank", claim=f"{comma(a * 10)} ÷ 10")


@fam("012")
def pv_chart(r, L):
    n = number(r, L)
    dg = digits_of(n)
    places = PLACE_NAMES[:len(str(n))][::-1]
    alt = "A place value chart. " + ", ".join(f"{p}: {dg[p]}" for p in places) + "."
    s = str(n)
    sw = int(s[1] + s[0] + s[2:]) if s[1] != "0" and s[0] != s[1] else n + 10 ** (len(s) - 2)
    return Item("What number does the place value chart show? Write it in standard form.", comma(n),
                ["Read the digits from left to right, starting with the greatest place.", f"The number is {comma(n)}."],
                [W(comma(int(s[::-1])) if s[-1] != "0" and s != s[::-1] else comma(n + 1), "read the digits from right to left"), W(comma(sw), "switched two digits"), W(comma(n * 10), "added an extra zero")],
                FN("chart_number", digits=dg), qtype="visual", diagram=Diagram("place_chart", {"digits": {p: dg[p] for p in places}, "places": places}, alt))


@fam("012")
def pv_how_many_units(r, L):
    e = r.randint(1, 2 if L < 2 else 3)
    q = r.randint(11, 99) if L == 0 else r.randint(101, 999)
    n = q * 10 ** e
    unit = PLACE_NAMES[e]
    return Item(f"How many {unit} are in {comma(n)}?", comma(q), [f"1 {sg(unit)} = {comma(10 ** e)}.", f"{comma(n)} ÷ {comma(10 ** e)} = {comma(q)}, so there are {comma(q)} {unit}."],
                [W(str(int(str(n)[-e - 1])), f"gave only the digit in the {unit} place"), W(comma(q * 10), "divided by the wrong place value"), W(comma(q // 10) if q % 10 == 0 else comma(q + 10 ** e), "divided by the wrong place value"), W(comma(n), "did not regroup")],
                FN("units_in", n=str(n), unit=unit), qtype="conceptual", tags={"reasoning"})


@fam("012", mode="mc")
def pv_which_number(r, L):
    d = r.randint(1, 9)
    e = r.randint(1, 3 + L)
    v = d * 10 ** e
    k = max(e + 1, digs(L)[0]) + r.randint(0, 1)
    k = min(k, 6)

    def make(pos):
        ds = [r.choice([x for x in range(1, 10) if x != d]) for _ in range(k)]
        ds[pos] = d
        return int("".join(map(str, reversed(ds))))
    good = make(e)
    cands = [p for p in range(k) if p != e]
    r.shuffle(cands)
    need(len(cands) >= 3)
    bad = [make(p) for p in cands[:3]]
    need(distinct(good, *bad))
    return Item(
        f"In which number does the digit {d} have a value of {comma(v)}?", comma(good),
        [f"A value of {comma(v)} means the {d} is in the {PLACE_NAMES[e]} place.", f"In {comma(good)}, the {d} is in the {PLACE_NAMES[e]} place."],
        [W(comma(b), f"the {d} is in a different place") for b in bad], FN("digit_has_value", digit=d, value=str(v)), qtype="conceptual")


@fam("12")
def pv_word_ten_times(r, L):
    a = r.randint(2, 9) * 10 ** r.randint(1, 3)
    t = pick(r, [("A small box holds {a} paper clips. A large case holds 10 times as many.", "How many paper clips does the large case hold?", "paper clips"),
                 ("A town has {a} people. A nearby city has 10 times as many people.", "How many people live in the city?", "people"),
                 ("A pond holds {a} gallons of water. A lake holds 10 times as much.", "How many gallons does the lake hold?", "gallons")])
    if L == 2 and r.random() < 0.5:
        b = a * 10
        return Item(
                    f"A large tank holds {comma(b)} {t[2]}. That is 10 times as much as a small tank holds. How many {t[2]} does the small tank hold?",
                    f"{comma(a)} {t[2]}", [f"The large amount is 10 times the small amount, so divide by 10.", f"{comma(b)} ÷ 10 = {comma(a)} {t[2]}."],
                    [W(f"{comma(b * 10)} {t[2]}", "multiplied by 10 instead of dividing"), W(f"{comma(b - 10)} {t[2]}", "subtracted 10"), W(f"{comma(a // 10)} {t[2]}", "divided by 100")],
                    EX(f"{b} ÷ 10", unit=t[2]), qtype="word-problem")
    return Item(t[0].replace("{a}", comma(a)) + " " + t[1], f"{comma(a * 10)} {t[2]}", [f"10 times as many means multiply by 10.", f"10 × {comma(a)} = {comma(a * 10)} {t[2]}."],
                [W(f"{comma(a + 10)} {t[2]}", "added 10 instead of multiplying"), W(f"{comma(a * 100)} {t[2]}", "multiplied by 100"), W(f"{comma(a // 10)} {t[2]}", "divided by 10")],
                EX(f"10 × {a}", unit=t[2]), qtype="word-problem")


# ============================================================== S2 Reading and Writing Multi-Digit Numbers
def rw_number(r, L):
    n = number(r, L)
    if r.random() < 0.5:   # put a zero inside so place value matters
        s = list(str(n))
        i = r.randint(1, len(s) - 2)
        s[i] = "0"
        n = int("".join(s))
    return n


def near_numbers(r, n):
    s = str(n)
    out = []
    for _ in range(30):
        i, j = r.sample(range(len(s)), 2)
        t = list(s)
        t[i], t[j] = t[j], t[i]
        if t[0] != "0" and int("".join(t)) != n:
            out.append(int("".join(t)))
    if "0" in s[1:]:
        t = s.replace("0", "", 1) if s[0] != "0" else s
        out.append(int(t))
    out.append(n * 10)
    seen, res = {n}, []
    for x in out:
        if x not in seen and 1000 <= x <= 999999:
            seen.add(x)
            res.append(x)
    return res


@fam("012")
def rw_from_words(r, L):
    n = rw_number(r, L)
    w = words(n)
    nn = near_numbers(r, n)
    need(len(nn) >= 3)
    return Item(f"Write this number in standard form: {w}", comma(n), ["Write the thousands period first, then the hundreds, tens and ones.", f"Use zeros to hold any empty places: {comma(n)}."],
                [W(comma(nn[0]), "put digits in the wrong places"), W(comma(nn[1]), "put digits in the wrong places"), W(comma(nn[2]), "left out or misplaced a zero")],
                FN("words_to_number", words=w), claim=f"Standard form of {w}")


@fam("012", mode="mc")
def rw_to_words(r, L):
    n = rw_number(r, L)
    nn = near_numbers(r, n)
    need(len(nn) >= 3)
    return Item(f"Which is the word form of {comma(n)}?", words(n), ["Read the thousands period, say “thousand,” then read the rest.", f"{comma(n)} is {words(n)}."],
                [W(words(x), "matched the digits to the wrong places") for x in nn[:3]], FN("word_form", n=str(n)), qtype="conceptual")


@fam("012")
def rw_from_expanded(r, L):
    n = rw_number(r, L)
    terms = [int(c) * 10 ** (len(str(n)) - 1 - i) for i, c in enumerate(str(n)) if c != "0"]
    need(len(terms) >= 3)
    e = " + ".join(comma(t) for t in terms)
    s = "".join(str(t)[0] for t in terms)
    return Item(f"Write in standard form: {e}", comma(n), ["Each part tells the value of one digit.", f"Add the parts: {comma(n)}."],
                [W(comma(int(s)) if int(s) != n else comma(n + 1), "wrote the digits side by side without zeros for empty places"), W(comma(n * 10), "added an extra zero"), W(comma(n + terms[-1] * 9), "put a digit in the wrong place")],
                EX(" + ".join(str(t) for t in terms)), claim=e)


@fam("012", mode="mc")
def rw_to_expanded(r, L):
    n = rw_number(r, L)
    s = str(n)
    terms = [int(c) * 10 ** (len(s) - 1 - i) for i, c in enumerate(s) if c != "0"]
    need(len(terms) >= 3)
    good = " + ".join(comma(t) for t in terms)
    b1 = " + ".join(comma(t) for t in terms[:-2] + [terms[-2] * 10, terms[-1]])
    b2 = " + ".join(comma(t // 10 if i == 0 else t) for i, t in enumerate(terms))
    b3 = " + ".join(str(t)[0] for t in terms)
    return Item(f"Which shows {comma(n)} in expanded form?", good, ["Write the value of each nonzero digit.", f"{comma(n)} = {good}."],
                [W(b1, "gave one digit the wrong place value"), W(b2, "gave the first digit the wrong place value"), W(b3, "listed the digits instead of their values")],
                FN("expanded", n=str(n)), qtype="conceptual")


@fam("012")
def rw_missing_part(r, L):
    n = number(r, L, nozero=True)
    s = str(n)
    terms = [int(c) * 10 ** (len(s) - 1 - i) for i, c in enumerate(s)]
    i = r.randrange(len(terms))
    shown = " + ".join("___" if j == i else comma(t) for j, t in enumerate(terms))
    rest = " − ".join(str(t) for j, t in enumerate(terms) if j != i)
    v = terms[i]
    return Item(f"Fill in the blank: {comma(n)} = {shown}", comma(v), [f"The missing part is the value of the digit {s[i]}.", f"The digit {s[i]} is in the {PLACE_NAMES[len(s) - 1 - i]} place, so the missing part is {comma(v)}."],
                [W(s[i], "wrote the digit instead of its value"), W(comma(v * 10), "used the place one to the left"), W(comma(v // 10) if v >= 10 else comma(v * 100), "used the place one to the right")],
                EX(f"{n} − {rest}"), qtype="fill-blank")


@fam("012")
def rw_units_to_number(r, L):
    k = digs(L)[1]
    places = sorted(r.sample(range(k), 3 if L < 2 else 4), reverse=True)
    dg = {PLACE_NAMES[p]: r.randint(1, 9) for p in places}
    n = sum(d * 10 ** PLACE_NAMES.index(p) for p, d in dg.items())
    desc = ", ".join(f"{d} {p if d != 1 else sg(p)}" for p, d in dg.items())
    s = "".join(str(d) for d in dg.values())
    return Item(f"What number has {desc}? Write it in standard form.", comma(n), ["Write each digit in its place.", f"Fill every other place with a zero: {comma(n)}."],
                [W(comma(int(s)), "left out the zeros for empty places"), W(comma(int(s) * 10 ** min(places)) if int(s) * 10 ** min(places) != n else comma(n + 10), "kept the digits together"), W(comma(n * 10), "added an extra zero")],
                FN("chart_number", digits=dg), qtype="conceptual", tags={"reasoning"})


@fam("12", mode="mc")
def rw_other_names(r, L):
    q = r.randint(12, 98)
    need(q % 10)
    e = r.randint(2, 3)
    n = q * 10 ** e
    good = f"{q} {PLACE_NAMES[e]}"
    bad = [f"{q} {PLACE_NAMES[e - 1]}", f"{q * 10} {PLACE_NAMES[e]}", f"{q // 10} {PLACE_NAMES[e + 1]} {q % 10} {PLACE_NAMES[e - 1]}"]
    return Item(f"Which is another way to name {comma(n)}?", good, [f"1 {sg(PLACE_NAMES[e])} = {comma(10 ** e)}.", f"{q} × {comma(10 ** e)} = {comma(n)}, so {comma(n)} is {good}."],
                [W(bad[0], "used a place value that is too small"), W(bad[1], "used too many groups"), W(bad[2], "broke the number apart incorrectly")],
                FN("unit_names", n=str(n)), qtype="conceptual", tags={"reasoning", "multiple-representations"})


# ============================================================== S3 Comparing and Ordering Whole Numbers
def close_pair(r, L):
    a = number(r, L)
    s = list(str(a))
    kind = r.randrange(4 if L else 3)
    if kind == 0:
        i, j = r.sample(range(len(s)), 2)
        s[i], s[j] = s[j], s[i]
    elif kind == 1:
        i = r.randint(1, len(s) - 1)
        s[i] = str((int(s[i]) + r.randint(1, 8)) % 10)
    elif kind == 2:
        i = r.randrange(len(s) - 1)
        s[i] = str(r.randint(1, 9))
    else:
        s = s[:-1]
    need(s[0] != "0")
    b = int("".join(s))
    need(a != b)
    return a, b


@fam("012", mode="sa")
def co_compare(r, L):
    a, b = close_pair(r, L)
    if r.random() < 0.08:
        b = a
    sym = "<" if a < b else ">" if a > b else "="
    sa, sb = str(a), str(b)
    if len(sa) != len(sb):
        why = f"{comma(max(a, b))} has more digits, so it is greater."
    elif a == b:
        why = "Every digit is the same."
    else:
        i = next(k for k in range(len(sa)) if sa[k] != sb[k])
        why = f"The first place where the digits differ is the {PLACE_NAMES[len(sa) - 1 - i]} place: {sa[i]} {'<' if sa[i] < sb[i] else '>'} {sb[i]}."
    return Item(f"Compare. Write <, > or = to make the statement true: {comma(a)} ___ {comma(b)}", sym, ["Line up the digits by place value and compare from the left.", why, f"{comma(a)} {sym} {comma(b)}."],
                [W(x, "compared the digits in the wrong place") for x in "<>=" if x != sym], FN("compare", a=str(a), b=str(b)), claim=f"Compare {comma(a)} and {comma(b)}")


def cluster(r, L, k=4):
    a = number(r, L)
    out = {a}
    for _ in range(60):
        if len(out) == k:
            break
        s = list(str(a))
        i, j = r.sample(range(len(s)), 2)
        if r.random() < 0.6:
            s[i], s[j] = s[j], s[i]
        else:
            s[i] = str(r.randint(0, 9))
        if s[0] != "0":
            out.add(int("".join(s)))
    need(len(out) == k)
    out = list(out)
    r.shuffle(out)
    return out


@fam("012", mode="mc")
def co_extreme(r, L):
    v = cluster(r, L)
    which = pick(r, ["greatest", "least"])
    g = max(v) if which == "greatest" else min(v)
    return Item(f"Which number is the {which}?", comma(g), ["Compare the digits from left to right, starting with the greatest place.", f"The {which} number is {comma(g)}."],
                [W(comma(x), "compared the wrong place first") for x in v if x != g], FN("extreme_of", values=[str(x) for x in v], which=which), qtype="conceptual")


@fam("012", mode="mc")
def co_order(r, L):
    v = cluster(r, L, 3 if L == 0 else 4)
    desc = r.random() < 0.4
    want = sorted(v, reverse=desc)
    txt = lambda xs: ", ".join(comma(x) for x in xs)
    w2 = want[:]
    w2[0], w2[1] = w2[1], w2[0]
    w3 = want[:]
    w3[-1], w3[-2] = w3[-2], w3[-1]
    return Item(f"Order the numbers from {'greatest to least' if desc else 'least to greatest'}: {txt(v)}", txt(want),
                ["Compare the digits from left to right, starting with the greatest place.", f"In order: {txt(want)}."],
                [W(txt(want[::-1]), "ordered in the opposite direction"), W(txt(w2), "switched two numbers"), W(txt(w3), "switched two numbers")],
                FN("order_nums", values=[str(x) for x in v], desc=desc), qtype="ordering")


@fam("012", mode="mc")
def co_between(r, L):
    e = r.randint(2, 2 + L)
    lo = r.randint(11, 98 if L else 40) * 10 ** e
    hi = lo + 10 ** e
    good = r.randint(lo + 1, hi - 1)
    bad = [lo - r.randint(1, 10 ** e // 2), hi + r.randint(1, 10 ** e // 2), good + 10 ** (e + 1)]
    return Item(f"Which number is between {comma(lo)} and {comma(hi)}?", comma(good), [f"The number must be greater than {comma(lo)} and less than {comma(hi)}.", f"{comma(lo)} < {comma(good)} < {comma(hi)}."],
                [W(comma(bad[0]), f"it is less than {comma(lo)}"), W(comma(bad[1]), f"it is greater than {comma(hi)}"), W(comma(bad[2]), "it has a different digit in a greater place")],
                FN("between_num", lo=str(lo), hi=str(hi)), qtype="conceptual")


@fam("012", mode="mc")
def co_table(r, L):
    place, thing = pick(r, THINGS)
    v = cluster(r, L, 4)
    names = r.sample(["Ashford", "Brookside", "Cedar Hill", "Dover", "Elmwood", "Fairview", "Glenview", "Harbor"], 4)
    which = pick(r, ["greatest", "least"])
    g = max(v) if which == "greatest" else min(v)
    rows = [[nm, comma(x)] for nm, x in zip(names, v)]
    good = names[v.index(g)]
    alt = f"A table with columns {place.title()} and number of {thing}. " + "; ".join(f"{a}: {b}" for a, b in rows) + "."
    return Item(f"The table shows the number of {thing} at four places. Which place has the {which} number of {thing}?", good,
                ["Compare the numbers from the greatest place value.", f"{comma(g)} is the {which} number, so the answer is {good}."],
                [W(nm, "compared the wrong place first") for nm in names if nm != good],
                FN("arg_extreme", items={nm: str(x) for nm, x in zip(names, v)}, which=which), qtype="real-world", tags={"modeling"},
                diagram=Diagram("table", {"header": ["Place", thing.title()], "rows": rows}, alt))


@fam("012", mode="mc")
def co_true_statement(r, L):
    opts = []
    for k in range(4):
        a, b = close_pair(sub(r, k), L)
        opts.append((a, b))
    gi = r.randrange(4)
    out = []
    for k, (a, b) in enumerate(opts):
        true_sym = "<" if a < b else ">"
        sym = true_sym if k == gi else (">" if true_sym == "<" else "<")
        out.append(f"{comma(a)} {sym} {comma(b)}")
    need(len(set(out)) == 4)
    return Item("Which comparison is true?", out[gi], ["Check each comparison by comparing digits from the left.", f"{out[gi]} is true."],
                [W(t, "the comparison symbol points the wrong way") for k, t in enumerate(out) if k != gi], FN("true_cmp"), qtype="conceptual", tags={"reasoning"})


@fam("12")
def co_digit_blank(r, L):
    a = number(r, L, 5, 5)
    s = str(a)
    i = r.randint(1, 2)
    limit = a
    shown = s[:i] + "_" + s[i + 1:]
    which = pick(r, ["greatest", "least"])
    op = "<" if which == "greatest" else ">"
    okd = [d for d in range(10) if (int(s[:i] + str(d) + s[i + 1:]) < limit if op == "<" else int(s[:i] + str(d) + s[i + 1:]) > limit)]
    need(okd)
    ans = max(okd) if which == "greatest" else min(okd)
    pretty = shown[:-3] + "," + shown[-3:]
    return Item(f"What is the {which} digit that makes this comparison true? {pretty} {op} {comma(limit)}", str(ans),
                [f"The digits to the left of the blank match, so compare the blank with the digit {s[i]}.", f"The {which} digit that works is {ans}."],
                [W(s[i], "used the same digit, which makes the numbers equal"), W(str(9 if which == "greatest" else 0), f"chose the {which} digit without checking the comparison"), W(str(ans - 1 if which == "greatest" and ans > 0 else ans + 1), "was off by one")],
                FN("blank_digit", pattern=shown, op=op, limit=str(limit), which=which), qtype="conceptual", tags={"reasoning", "challenge"})


# ============================================================== S4 Rounding Whole Numbers
def round_case(r, L):
    n = number(r, L)
    k = len(str(n))
    e = r.randint(1, min(k - 1, 2 + L if L else 3))
    return n, e


def round_wrongs(n, e):
    u = 10 ** e
    lo = n // u * u
    good = rnd_to(n, e)
    return [W(comma(lo if good != lo else lo + u), "rounded in the wrong direction"), W(comma(rnd_to(n, e - 1)) if e > 1 else comma(n), "rounded to the place on the right"),
            W(comma(rnd_to(n, e + 1)), "rounded to the place on the left"), W(comma(good + u), "changed the rounding digit by too much")]


@fam("012")
def rd_round(r, L):
    n, e = round_case(r, L)
    u = 10 ** e
    good = rnd_to(n, e)
    lo = n // u * u
    dd = (n // (u // 10)) % 10
    return Item(f"Round {comma(n)} to the nearest {sg(PLACE_NAMES[e])}.", comma(good),
                [f"{comma(n)} is between {comma(lo)} and {comma(lo + u)}.", f"The digit to the right of the {PLACE_NAMES[e]} place is {dd}. {'5 or more, so round up' if dd >= 5 else 'Less than 5, so round down'}.", f"{comma(n)} rounds to {comma(good)}."],
                round_wrongs(n, e), FN("round", x=str(n), place=PLACE_NAMES[e]), claim=f"{comma(n)} rounded to the nearest {sg(PLACE_NAMES[e])}")


@fam("012")
def rd_halfway(r, L):
    n, e = round_case(r, L)
    u = 10 ** e
    lo = n // u * u
    mid = lo + u // 2
    need(n != mid)
    return Item(f"{comma(n)} is between {comma(lo)} and {comma(lo + u)}. What number is exactly halfway between {comma(lo)} and {comma(lo + u)}?", comma(mid),
                [f"Halfway is {comma(u // 2)} more than {comma(lo)}.", f"{comma(lo)} + {comma(u // 2)} = {comma(mid)}. Numbers at or above {comma(mid)} round up."],
                [W(comma(lo + u // 10), "used one tenth of the way instead of half"), W(comma(n), "used the number itself"), W(comma(lo + u), "used the greater benchmark"), W(comma(mid + u // 2 + u // 10), "added too much")],
                EX(f"({lo} + {lo + u}) ÷ 2"), qtype="conceptual")


@fam("012", mode="mc")
def rd_which_rounds(r, L):
    e = r.randint(1 if L == 0 else 2, 2 + L)
    u = 10 ** e
    target = r.randint(11, 98) * u
    good = target + r.randint(-u // 2, u // 2 - 1)
    need(good != target)
    bad = [target + u // 2 + r.randint(0, u // 4), target - u // 2 - r.randint(1, u // 4), target + u + r.randint(-u // 4, u // 4)]
    return Item(f"Which number rounds to {comma(target)} when rounded to the nearest {sg(PLACE_NAMES[e])}?", comma(good),
                [f"Numbers from {comma(target - u // 2)} to {comma(target + u // 2 - 1)} round to {comma(target)}.", f"{comma(good)} is in that range."],
                [W(comma(bad[0]), f"it rounds up to {comma(target + u)}"), W(comma(bad[1]), f"it rounds down to {comma(target - u)}"), W(comma(bad[2]), f"it is closer to {comma(target + u)}")],
                FN("rounds_to_opt", target=str(target), place=PLACE_NAMES[e]), qtype="conceptual")


@fam("012")
def rd_word(r, L):
    n, e = round_case(r, L)
    place, thing = pick(r, THINGS)
    good = rnd_to(n, e)
    return Item(f"A {place} has {comma(n)} {thing}. A reporter rounds this number to the nearest {sg(PLACE_NAMES[e])}. What number does the reporter write?", comma(good),
                [f"Look at the digit to the right of the {PLACE_NAMES[e]} place.", f"{comma(n)} rounds to {comma(good)}."], round_wrongs(n, e),
                FN("round", x=str(n), place=PLACE_NAMES[e]), qtype="real-world")


@fam("12")
def rd_extreme(r, L):
    e = r.randint(1, 1 + L)
    u = 10 ** e
    target = r.randint(11, 98) * u
    which = pick(r, ["greatest", "least"])
    ans = target + u // 2 - 1 if which == "greatest" else target - u // 2
    return Item(f"What is the {which} whole number that rounds to {comma(target)} when rounded to the nearest {sg(PLACE_NAMES[e])}?", comma(ans),
                [f"Halfway points are {comma(target - u // 2)} and {comma(target + u // 2)}.", f"{comma(target - u // 2)} rounds up to {comma(target)}, and {comma(target + u // 2)} rounds up to {comma(target + u)}.", f"The {which} number is {comma(ans)}."],
                [W(comma(target + u // 2 if which == "greatest" else target - u // 2 - 1), "used a number that rounds to a different value"), W(comma(target + u - 1 if which == "greatest" else target - u + 1), "used the whole distance to the next benchmark"),
                 W(comma(target + 4 if which == "greatest" else target - 5) if e > 1 else comma(target + 9 if which == "greatest" else target - 9), "looked at the wrong place"), W(comma(target), "gave the rounded number itself")],
                FN("round_extreme", target=str(target), place=PLACE_NAMES[e], which=which), qtype="conceptual", tags={"reasoning", "challenge"})


@fam("012", mode="mc")
def rd_which_place(r, L):
    for _ in range(40):
        n = number(r, L, 5, 6)
        k = len(str(n))
        res = {e: rnd_to(n, e) for e in range(1, k)}
        if len(set(res.values())) == len(res):
            break
    else:
        raise Reject()
    es = sorted(res)
    e = pick(r, es)
    bad = [x for x in es if x != e]
    r.shuffle(bad)
    bad = sorted(bad[:3])
    need(len(bad) == 3)
    return Item(f"{comma(n)} was rounded to {comma(res[e])}. To which place was it rounded?", f"nearest {sg(PLACE_NAMES[e])}",
                [f"All the digits to the right of the {PLACE_NAMES[e]} place became zeros.", f"{comma(n)} rounded to the nearest {sg(PLACE_NAMES[e])} is {comma(res[e])}."],
                [W(f"nearest {sg(PLACE_NAMES[x])}", f"that would give {comma(res[x])}") for x in bad], FN("round_place", n=str(n), result=str(res[e])), qtype="conceptual", tags={"reasoning"})


SKILLS = {
    1: dict(name="Place Value to One Million", fams=[pv_digit_value, pv_place_name, pv_ten_times, pv_times_ten_blank, pv_chart, pv_how_many_units, pv_which_number, pv_word_ten_times]),
    2: dict(name="Reading and Writing Multi-Digit Numbers", fams=[rw_from_words, rw_to_words, rw_from_expanded, rw_to_expanded, rw_missing_part, rw_units_to_number, rw_other_names]),
    3: dict(name="Comparing and Ordering Whole Numbers", fams=[co_compare, co_extreme, co_order, co_between, co_table, co_true_statement, co_digit_blank]),
    4: dict(name="Rounding Whole Numbers", fams=[rd_round, rd_halfway, rd_which_rounds, rd_word, rd_extreme, rd_which_place]),
}
