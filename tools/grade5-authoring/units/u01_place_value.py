"""Unit 1: Place Value and Number Sense (place-value-decimals)."""
from g5lib import *

UNIT_ID = "place-value-number-sense"
PLACES = ["thousandths", "hundredths", "tenths", "ones", "tens", "hundreds", "thousands", "ten thousands"]
EXP = {"thousandths": -3, "hundredths": -2, "tenths": -1, "ones": 0, "tens": 1, "hundreds": 2, "thousands": 3, "ten thousands": 4}
SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def p10(n):
    return "10" + str(n).translate(SUP)


def rand_num(r, L, need_place=None):
    """A number with distinct-ish nonzero digits. L0: whole to thousands; L1: to hundredths; L2: to thousandths."""
    lo_e = {0: 0, 1: -2, 2: -3}[L]
    hi_e = {0: 3, 1: 3, 2: 4}[L]
    digits = {}
    for e in range(lo_e, hi_e + 1):
        digits[e] = r.randint(1, 9) if e in (hi_e, lo_e) else r.randint(0, 9)
    v = sum(F(d) * F(10) ** e for e, d in digits.items())
    return v, digits, lo_e


def place_for(e):
    return [p for p, x in EXP.items() if x == e][0]


# ============================================================== S1 Place Value Patterns
@fam("012")
def s1_digit_value(r, L):
    v, dg, lo = rand_num(r, L)
    es = [e for e, d in dg.items() if d != 0 and list(dg.values()).count(d) == 1]
    need(es)
    e = pick(r, es)
    d = dg[e]
    val = F(d) * F(10) ** e
    near = [F(d) * F(10) ** (e + 1), F(d) * F(10) ** (e - 1), F(d)]
    return Item(f"What is the value of the digit {d} in {dec(v)}?", dec(val),
                [f"The {d} is in the {place_for(e)} place.", f"Its value is {d} × {dec(F(10) ** e)} = {dec(val)}."],
                wrongs(dec(val), [W(dec(near[0]), "used the place one to the left"), W(dec(near[1]), "used the place one to the right"),
                                  W(str(d), "gave the digit instead of its value"), W(dec(F(d) * F(10) ** (e + 2)), "counted places from the wrong end")]),
                FN("digit_value", n=dec(v), place=place_for(e)), qtype="procedural", claim=f"Value of {d} in {dec(v)}")


@fam("012")
def s1_times(r, L):
    d = r.randint(1, 9)
    if L == 0:
        e1 = r.randint(1, 3)
        e2 = e1 - 1
    elif L == 1:
        e1 = r.randint(-1, 2)
        e2 = e1 - pick(r, [1, 1, -1])
    else:
        e1 = r.randint(-2, 3)
        e2 = e1 - pick(r, [2, -1, -2, 1])
    need(e1 != e2 and -3 <= e2 <= 3)
    n_digits = range(min(e1, e2, 0), max(e1, e2, 0) + 1)
    v = sum(F(d) * F(10) ** e for e in n_digits)
    a, b = F(d) * F(10) ** e1, F(d) * F(10) ** e2
    ratio = a / b
    ans = dec(ratio) if ratio >= 1 else frac(ratio)
    return Item(f"In the number {dec(v)}, every digit is {d}. The {d} in the {place_for(e1)} place is how many times as much as the {d} in the {place_for(e2)} place?",
                ans, [f"The first {d} is worth {dec(a)}; the second is worth {dec(b)}.", f"{dec(a)} ÷ {dec(b)} = {ans}."],
                wrongs(ans, [W(frac(1 / ratio) if ratio >= 1 else dec(1 / ratio), "flipped the comparison"), W(dec(ratio * 10) if ratio >= 1 else frac(ratio / 10), "moved one place too many"),
                             W(str(abs(e1 - e2)), "counted the places instead of finding the multiplier"), W(dec(ratio / 10) if ratio >= 10 else frac(ratio * 10) if ratio < 1 else "100", "moved one place too few")]),
                FN("times", a=dec(a), b=dec(b)), qtype="conceptual", tags={"reasoning"})


@fam("012")
def s1_tenth_of(r, L):
    if L == 0:
        x = F(r.randint(1, 9) * 10 ** r.randint(1, 3))
    elif L == 1:
        x = F(r.randint(1, 99), pick(r, [1, 10]))
    else:
        x = F(r.randint(1, 999), pick(r, [10, 100]))
    kind = pick(r, ["times", "tenth"])
    if kind == "times":
        y = x * 10
        prompt = f"What number is 10 times as much as {dec(x)}?"
        steps = [f"Each digit moves one place to the left.", f"{dec(x)} × 10 = {dec(y)}."]
        bad = [W(dec(x / 10), "found 1/10 instead of 10 times"), W(dec(x * 100), "moved two places"), W(dec(x + 10), "added 10 instead of multiplying")]
        chk = EX(f"{dec(x)}*10")
    else:
        y = x / 10
        prompt = f"What number is 1/10 of {dec(x)}?"
        steps = [f"Each digit moves one place to the right.", f"{dec(x)} ÷ 10 = {dec(y)}."]
        bad = [W(dec(x * 10), "multiplied by 10 instead of dividing"), W(dec(x / 100), "moved two places"), W(dec(x - F(1, 10)) if x > F(1, 10) else dec(x + 1), "subtracted instead of dividing")]
        chk = EX(f"{dec(x)}/10")
    return Item(prompt, dec(y), steps, wrongs(dec(y), bad), chk, qtype="numerical")


@fam("012", mode="mc")
def s1_place_name(r, L):
    v, dg, lo = rand_num(r, L)
    es = [e for e, d in dg.items() if d != 0 and list(dg.values()).count(d) == 1]
    need(es)
    e = pick(r, es)
    good = place_for(e)
    bad = [place_for(x) for x in (e + 1, e - 1, -e) if x in EXP.values() and x != e]
    if e == 1:
        bad.append("tenths")
    if e == -1:
        bad.append("tens")
    bad = [b for b in dict.fromkeys(bad) if b != good][:3]
    need(len(bad) == 3)
    opts = [(good, True)] + [(b, False) for b in bad]
    r.shuffle(opts)
    return Item(f"In {dec(v)}, which place is the digit {dg[e]} in?", good,
                ["Name the places from the decimal point: ones, tenths, hundredths, thousandths to the right; ones, tens, hundreds to the left.",
                 f"The {dg[e]} is in the {good} place."], check=FN("place_of", n=dec(v), digit=dg[e]), options=opts, mode="mc", qtype="conceptual")


@fam("012")
def s1_chart(r, L):
    v, dg, lo = rand_num(r, L)
    places = [place_for(e) for e in sorted(dg, reverse=True)]
    es = [e for e, d in dg.items() if d != 0]
    e = pick(r, es)
    val = F(dg[e]) * F(10) ** e
    data = {"places": places, "digits": {place_for(k): x for k, x in dg.items()}, "highlight": place_for(e)}
    alt = f"Place-value chart showing {dec(v)} with the {place_for(e)} place highlighted."
    return Item("The place-value chart shows a number. What is the value of the highlighted digit?", dec(val),
                [f"The highlighted digit {dg[e]} is in the {place_for(e)} place.", f"Value: {dg[e]} × {dec(F(10) ** e)} = {dec(val)}."],
                wrongs(dec(val), [W(str(dg[e]), "gave the digit, not its value"), W(dec(val * 10), "used the place to the left"), W(dec(val / 10), "used the place to the right")]),
                FN("digit_value", n=dec(v), place=place_for(e)), qtype="visual", diagram=Diagram("place_chart", data, alt))


@fam("012")
def s1_blocks(r, L):
    fl, rd, un = r.randint(0 if L else 1, 3), r.randint(1, 9), r.randint(1, 9)
    whole = "flat" if L else "unit"
    if L == 0:
        v = fl * 100 + rd * 10 + un
        q = "Each small cube is 1. What number do the base-ten blocks show?"
        expr = f"{fl}*100+{rd}*10+{un}"
        bad = [W(str(fl + rd + un), "counted blocks instead of their values"), W(dec(fl * 100 + un * 10 + rd), "swapped tens and ones"), W(dec(fl * 10 + rd * 100 + un), "swapped hundreds and tens")]
    else:
        v = fl + F(rd, 10) + F(un, 100)
        q = "A flat is 1 whole, a rod is 1 tenth, and a small cube is 1 hundredth. What decimal do the blocks show?"
        expr = f"{fl}+{rd}/10+{un}/100"
        bad = [W(dec(fl * 100 + rd * 10 + un), "read the blocks as whole numbers"), W(dec(fl + F(un, 10) + F(rd, 100)), "swapped tenths and hundredths"), W(dec(fl + F(rd, 100) + F(un, 1000)), "made each block 10 times too small")]
    alt = f"Base-ten blocks: {fl} flats, {rd} rods and {un} small cubes."
    it = Item(q, dec(v), [f"{fl} flats, {rd} rods, {un} small cubes.", f"Total: {dec(v)}."], wrongs(dec(v), bad), EX(expr), qtype="visual",
              diagram=Diagram("base_ten", {"flats": fl, "rods": rd, "units": un}, alt))
    it.consts = [fl, rd, un]
    return it


@fam("012")
def s1_missing(r, L):
    x = F(r.randint(1, 99), pick(r, [10, 100] if L else [1]))
    k = pick(r, [10, 100]) if L == 2 else 10
    up = r.random() < 0.5
    if up:
        y = x * k
        prompt = f"Fill in the blank: ___ is {k} times as much as {dec(x)}."
        chk = EX(f"{dec(x)}*{k}")
        bad = [W(dec(x / k), "divided instead of multiplying"), W(dec(x * k * 10), "moved one place too many"), W(dec(x + k), "added instead of multiplying")]
    else:
        y = x / k
        prompt = f"Fill in the blank: ___ is 1/{k} of {dec(x)}."
        chk = EX(f"{dec(x)}/{k}")
        bad = [W(dec(x * k), "multiplied instead of dividing"), W(dec(x / k / 10), "moved one place too many"), W(dec(x - 1) if x > 1 else dec(x * 10), "subtracted instead of dividing")]
    return Item(prompt, dec(y), [f"{'Multiply' if up else 'Divide'} by {k}: each digit moves {'left' if up else 'right'} {1 if k == 10 else 2} place{'s' if k == 100 else ''}.", f"The answer is {dec(y)}."],
                wrongs(dec(y), bad), chk, qtype="fill-blank")


@fam("12", mode="mc")
def s1_true_statement(r, L):
    d = r.randint(1, 9)
    e = r.randint(-2, 1)
    v = F(d) * F(10) ** e + F(d) * F(10) ** (e - 1)
    a, b = place_for(e), place_for(e - 1)
    good = f"The {d} in the {a} place is 10 times the {d} in the {b} place."
    bad = [f"The {d} in the {b} place is 10 times the {d} in the {a} place.",
           f"Both {d}s have the same value.", f"The {d} in the {a} place is 1/10 of the {d} in the {b} place."]
    return mc_key(f"Look at the number {dec(v)}. Which statement is true?", good, bad,
                  ["Moving one place to the left makes a digit worth 10 times as much.", good], r=r, qtype="explain", tags={"reasoning"})


# ============================================================== S2 Powers of Ten and Exponents
@fam("012")
def s2_exp_value(r, L):
    n = r.randint(1, 4) if L == 0 else r.randint(2, 7)
    v = 10 ** n
    return Item(f"What is {p10(n)} written in standard form?", comma(v),
                [f"{p10(n)} means {n} tens multiplied together: " + " × ".join(["10"] * n) + ".", f"That is 1 followed by {n} zeros: {comma(v)}."],
                wrongs(comma(v), [W(str(10 * n), "multiplied 10 by the exponent"), W(comma(10 ** (n - 1)), "wrote one zero too few"), W(comma(10 ** (n + 1)), "wrote one zero too many")]),
                EX(f"10^{n}"), qtype="procedural")


@fam("012", mode="mc")
def s2_exp_write(r, L):
    n = r.randint(2, 4) if L == 0 else r.randint(3, 7)
    v = comma(10 ** n)
    good = p10(n)
    bad = [p10(n - 1), p10(n + 1), f"{n}¹⁰"]
    opts = [(good, True)] + [(b, False) for b in bad]
    r.shuffle(opts)
    return Item(f"Which shows {v} using an exponent?", good, [f"{v} has {n} zeros.", f"So {v} = {good}."],
                check=KEY(good), options=opts, mode="mc", qtype="conceptual")


@fam("012")
def s2_multiply(r, L):
    if L == 0:
        a = F(r.randint(2, 99))
        n = r.randint(1, 3)
    elif L == 1:
        a = F(r.randint(11, 999), pick(r, [10, 100]))
        n = r.randint(1, 3)
    else:
        a = F(r.randint(101, 9999), pick(r, [100, 1000]))
        n = r.randint(2, 4)
    use_exp = L > 0 and r.random() < 0.6
    k = 10 ** n
    y = a * k
    shown = p10(n) if use_exp else comma(k)
    it = Item(f"{dec(a)} × {shown} = ?", dec(y),
              [f"Multiplying by {shown} moves each digit {n} place{'s' if n > 1 else ''} to the left.", f"{dec(a)} × {shown} = {dec(y)}."],
              wrongs(dec(y), [W(dec(a * k / 10), f"moved {n - 1} places instead of {n}"), W(dec(a * k * 10), f"moved {n + 1} places instead of {n}"),
                              W(dec(a / k), "moved the digits the wrong way"), W(dec(a) + "0" * n if "." in dec(a) else dec(a * 10 ** (n + 1)), "just wrote zeros at the end")]),
              EX(f"{dec(a)}*10^{n}"), qtype="procedural", claim=f"{dec(a)} × {shown}")
    it.consts = [n]
    return it


@fam("012")
def s2_divide(r, L):
    if L == 0:
        a = F(r.randint(1, 99) * 10 ** r.randint(1, 3))
        n = r.randint(1, 2)
    elif L == 1:
        a = F(r.randint(11, 9999))
        n = r.randint(1, 3)
    else:
        a = F(r.randint(11, 9999), pick(r, [1, 10]))
        n = r.randint(1, 3)
    use_exp = L == 2 and r.random() < 0.6
    k = 10 ** n
    y = a / k
    need(len(dec(y).split(".")[-1]) <= 4 if "." in dec(y) else True)
    shown = p10(n) if use_exp else comma(k)
    it = Item(f"{dec(a)} ÷ {shown} = ?", dec(y),
              [f"Dividing by {shown} moves each digit {n} place{'s' if n > 1 else ''} to the right.", f"{dec(a)} ÷ {shown} = {dec(y)}."],
              wrongs(dec(y), [W(dec(a * k), "multiplied instead of dividing"), W(dec(y * 10), f"moved {n - 1} places"), W(dec(y / 10), f"moved {n + 1} places")]),
              EX(f"{dec(a)}/10^{n}"), qtype="procedural", claim=f"{dec(a)} ÷ {shown}")
    it.consts = [n]
    return it


@fam("012")
def s2_missing_exp(r, L):
    a = F(r.randint(2, 99), 1 if L == 0 else pick(r, [10, 100]))
    n = r.randint(1, 4)
    b = a * 10 ** n
    op = "×"
    if L == 2 and r.random() < 0.5:
        a, b = b, a
        op = "÷"
    it = Item(f"{dec(a)} {op} 10ⁿ = {dec(b)}. What is the value of n?", str(n),
              [f"Compare the digits of {dec(a)} and {dec(b)}.", f"They moved {n} place{'s' if n > 1 else ''}, so the exponent is {n}."],
              wrongs(str(n), [W(str(n + 1), "counted the zeros in the answer instead of the places moved"), W(str(n - 1) if n > 1 else str(n + 2), "miscounted the places moved"), W(comma(10 ** n), "gave the power of ten instead of the exponent")]),
              FN("missing_exp", a=dec(a), b=dec(b), op=op), qtype="fill-blank", tags={"reasoning"})
    return it


@fam("012")
def s2_zeros(r, L):
    a = r.randint(2, 99) if L < 2 else pick(r, [r.randint(2, 9) * 10, r.randint(11, 99)])
    n = r.randint(2, 5)
    v = a * 10 ** n
    z = len(str(v)) - len(str(v).rstrip("0"))
    it = Item(f"How many zeros are at the end of the product {a} × {p10(n)}?", str(z),
              [f"{a} × {p10(n)} = {comma(v)}.", f"{comma(v)} ends in {z} zeros" + (f" ({a} already ends in a zero)." if a % 10 == 0 else ".")],
              wrongs(str(z), [W(str(n), "forgot the zero already in the first factor") if a % 10 == 0 else W(str(n + 1), "added an extra zero"), W(str(n - 1), "wrote one zero too few"), W(str(z + 2), "counted the digits instead of the zeros")]),
              FN("zero_count", e=f"{a}*10^{n}"), qtype="conceptual", tags={"reasoning"})
    it.consts = [n]
    return it


@fam("012", mode="mc")
def s2_shift(r, L):
    n = r.randint(1, 3)
    op = pick(r, ["multiply", "divide"]) if L else "multiply"
    a = dec(F(r.randint(101, 999), 100))
    good = f"{n} place{'s' if n > 1 else ''} to the {'right' if op == 'multiply' else 'left'}"
    bad = [f"{n} place{'s' if n > 1 else ''} to the {'left' if op == 'multiply' else 'right'}", f"{n + 1} places to the {'right' if op == 'multiply' else 'left'}", "It does not move."]
    return mc_key(f"When you {op} {a} by {p10(n)}, how does the decimal point move?", good, bad,
                  [f"{'Multiplying' if op == 'multiply' else 'Dividing'} by {p10(n)} makes the number {'larger' if op == 'multiply' else 'smaller'}.", f"The decimal point moves {good}."], r=r, qtype="conceptual")


# ============================================================== S3 Reading and Writing Decimals
ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen",
        "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def w_int(n):
    n = int(n)
    if n < 20:
        return ONES[n]
    if n < 100:
        return TENS[n // 10] + ("-" + ONES[n % 10] if n % 10 else "")
    if n < 1000:
        return ONES[n // 100] + " hundred" + (" " + w_int(n % 100) if n % 100 else "")
    return w_int(n // 1000) + " thousand" + (" " + w_int(n % 1000) if n % 1000 else "")


def w_dec(v):
    s = dec(v).replace(",", "")
    a, _, b = s.partition(".")
    if not b:
        return w_int(a)
    unit = {1: "tenth", 2: "hundredth", 3: "thousandth"}[len(b)]
    fw = w_int(b) + " " + unit + ("s" if int(b) != 1 else "")
    return fw if int(a) == 0 else w_int(a) + " and " + fw


def dec_num(r, L):
    places = {0: pick(r, [1, 2]), 1: pick(r, [2, 3]), 2: 3}[L]
    whole = r.randint(0, 9) if L == 0 else r.randint(0, 99) if L == 1 else r.randint(1, 999)
    fr = r.randint(1, 10 ** places - 1)
    need(fr % 10 != 0)
    return whole + F(fr, 10 ** places)


@fam("012")
def s3_word_to_std(r, L):
    v = dec_num(r, L)
    s = dec(v)
    a, _, b = s.replace(",", "").partition(".")
    bad = [W(dec(int(a) + F(int(b), 10 ** (len(b) + 1))), "put the digits in the wrong place (one place too far right)")]
    if len(b) > 1:
        bad.append(W(dec(int(a) + F(int(b), 10 ** (len(b) - 1))), "used the wrong place name (one place too far left)"))
    bad.append(W(f"{a}{b}" if int(a) else b, "ignored the decimal point"))
    bad.append(W(dec(int(a) + F(int(b[::-1]), 10 ** len(b))) if b[::-1] != b else dec(v + F(1, 10)), "reversed the decimal digits"))
    return Item(f"Write the number in standard form: {w_dec(v)}.", s,
                ["The word “and” marks the decimal point.", f"The last word tells the last place, so the number is {s}."],
                wrongs(s, bad), FN("from_words", words=w_dec(v)), qtype="procedural", claim=f"“{w_dec(v)}” in standard form")


@fam("012", mode="mc")
def s3_std_to_word(r, L):
    v = dec_num(r, L)
    s = dec(v).replace(",", "")
    a, _, b = s.partition(".")
    good = w_dec(v)
    alt = [int(a) + F(int(b), 10 ** (len(b) + 1)), int(a) + F(int(b), 10 ** max(1, len(b) - 1)) if len(b) > 1 else int(a) * 10 + F(int(b), 10 ** len(b))]
    bad = [w_dec(x) for x in alt if is_term(x) and w_dec(x) != good]
    if int(a):
        bad.append(w_int(a) + " point " + " ".join(ONES[int(c)] for c in b))
    else:
        bad.append(w_int(b) + " and " + {1: "tenths", 2: "hundredths", 3: "thousandths"}[len(b)])
    bad = list(dict.fromkeys(bad))[:3]
    need(len(bad) == 3)
    opts = [(good, True)] + [(x, False) for x in bad]
    r.shuffle(opts)
    return Item(f"Which shows {dec(v)} in word form?", good, ["Say the whole number, say “and” for the decimal point, then read the decimal part with its last place name.", good],
                check=FN("word_form", n=dec(v)), options=opts, mode="mc", qtype="conceptual")


def expanded(v, style):
    s = dec(v).replace(",", "")
    a, _, b = s.partition(".")
    terms = []
    for i, c in enumerate(a):
        if c != "0":
            e = len(a) - 1 - i
            terms.append((int(c), e))
    for i, c in enumerate(b):
        if c != "0":
            terms.append((int(c), -(i + 1)))
    if style == "x":
        return " + ".join(f"{d} × {comma(10 ** e)}" if e >= 0 else f"{d} × (1/{10 ** -e})" for d, e in terms)
    return " + ".join(dec(F(d) * F(10) ** e) for d, e in terms)


@fam("012", mode="mc")
def s3_expanded(r, L):
    v = dec_num(r, L)
    need(len([c for c in dec(v).replace(".", "").replace(",", "") if c != "0"]) >= 3)
    style = "plain" if L == 0 else pick(r, ["plain", "x"])
    good = expanded(v, style)
    s = dec(v).replace(",", "")
    a, _, b = s.partition(".")
    sh = [int(a) + F(int(b), 10 ** (len(b) + 1)), int(a) * 10 + F(int(b), 10 ** len(b)), (int(a) + F(int(b), 10 ** len(b))) * 10]
    bad = [expanded(x, style) for x in sh if expanded(x, style) != good]
    bad = list(dict.fromkeys(bad))[:3]
    need(len(bad) == 3)
    opts = [(good, True)] + [(x, False) for x in bad]
    r.shuffle(opts)
    return Item(f"Which shows {dec(v)} in expanded form?", good, ["Write the value of each nonzero digit and add them.", f"{dec(v)} = {good}."],
                check=FN("expanded", n=dec(v)), options=opts, mode="mc", qtype="conceptual", tags={"multiple-representations"})


@fam("012")
def s3_from_expanded(r, L):
    v = dec_num(r, L)
    need(len([c for c in dec(v).replace(".", "").replace(",", "") if c != "0"]) >= 2)
    style = "plain" if L == 0 else "x"
    ex = expanded(v, style)
    s = dec(v).replace(",", "")
    a, _, b = s.partition(".")
    return Item(f"What number is {ex}?", dec(v), ["Put each digit in its place, using 0 for any empty place.", f"The number is {dec(v)}."],
                wrongs(dec(v), [W(dec(int(a) + F(int(b.replace('0', '') or 0), 10 ** len(b.replace('0', '') or '0'))) if "0" in b else dec(v * 10), "left out a zero placeholder"),
                                W(dec(v * 10), "shifted every digit one place left"), W(dec(v / 10), "shifted every digit one place right"), W(a + b if int(a) else b, "ignored the decimal point")]),
                EX(ex.replace(" ", "")), qtype="procedural", tags={"multiple-representations"})


@fam("012")
def s3_grid(r, L):
    g = 1 if L == 0 else r.randint(1, 2)
    sh = r.randint(1, 99) if g == 1 else r.randint(101, 199)
    v = F(sh, 100)
    alt = f"{g} hundred grid{'s' if g > 1 else ''}; each grid is one whole. {sh} small squares are shaded in all."
    return Item("Each large square is 1 whole. What decimal is shaded?", dec(v),
                [f"Each small square is 1 hundredth. {sh} hundredths are shaded.", f"{sh} hundredths = {dec(v)}."],
                wrongs(dec(v), [W(str(sh), "counted squares without using hundredths"), W(dec(F(sh, 10)), "read the squares as tenths"), W(dec(F(100 * g - sh, 100)), "counted the unshaded squares")]),
                EX(f"{sh}/100"), qtype="visual", diagram=Diagram("hundred_grid", {"shaded": sh, "grids": g}, alt))


@fam("012")
def s3_frac_to_dec(r, L):
    d = pick(r, [10, 100]) if L == 0 else pick(r, [10, 100, 1000])
    n = r.randint(1, d * (1 if L < 2 else 3) - 1)
    need(n % 10 != 0)
    v = F(n, d)
    shown = f"{n // d} {n % d}/{d}" if L == 2 and v > 1 else f"{n}/{d}"
    return Item(f"Write {shown} as a decimal.", dec(v), [f"The denominator {d} tells the last place: {'tenths' if d == 10 else 'hundredths' if d == 100 else 'thousandths'}.", f"{shown} = {dec(v)}."],
                wrongs(dec(v), [W(dec(F(n, d * 10)), "used one place too many"), W(dec(F(n, d // 10)) if d > 10 else str(n), "used one place too few"), W(f"{n}.{d}", "wrote the numerator and denominator side by side")]),
                EX(f"{v.numerator // v.denominator}+{n % d}/{d}" if shown != f"{n}/{d}" else f"{n}/{d}"), qtype="procedural", tags={"multiple-representations"})


# ============================================================== S4 Comparing and Ordering Decimals
def close_pair(r, L):
    places = 2 if L == 0 else 3
    w = r.randint(0, 9)
    a = w + F(r.randint(1, 10 ** places - 1), 10 ** places)
    kind = pick(r, ["drop", "swap", "zero"])
    s = dec(a).split(".")[-1] if "." in dec(a) else ""
    if kind == "drop" and len(s) >= 2:
        b = w + F(int(s[:-1] or 0), 10 ** (len(s) - 1))   # 0.45 vs 0.4
    elif kind == "zero":
        b = w + F(int(s[0]), 10) + F(r.randint(1, 9), 100 if places == 2 else 1000)   # tricky place
    else:
        b = w + F(int(s[::-1]), 10 ** len(s)) if s else a + F(1, 10)
    need(a != b and is_term(b))
    return a, b


@fam("012", mode="sa")
def s4_compare(r, L):
    a, b = close_pair(r, L)
    sym = "<" if a < b else ">"
    return Item(f"Compare. Write <, >, or =.\n{dec(a)} ___ {dec(b)}", sym,
                ["Line up the decimal points and compare digits from left to right.", f"{dec(a)} {sym} {dec(b)}."],
                [W(">" if sym == "<" else "<", "compared the number of digits instead of place values")], FN("compare", a=dec(a), b=dec(b)), qtype="procedural", mode="sa")


@fam("012", mode="mc")
def s4_true_cmp(r, L):
    pairs = []
    for k in range(8):
        try:
            pairs.append(close_pair(sub(r, k), L))
        except Reject:
            pass
    need(len(pairs) >= 4)
    good_p = pairs[0]
    a, b = good_p
    good = f"{dec(a)} {'<' if a < b else '>'} {dec(b)}"
    bad = []
    for x, y in pairs[1:]:
        bad.append(f"{dec(x)} {'>' if x < y else '<'} {dec(y)}")
    bad = list(dict.fromkeys(bad))[:3]
    need(len(bad) == 3)
    return mc_key("Which comparison is true?", good, bad, ["Compare each pair place by place, starting with the greatest place.", f"{good} is true."], r=r, qtype="conceptual")


@fam("012")
def s4_order(r, L):
    a, b = close_pair(r, L)
    c = a + F(r.randint(1, 9), 1000 if L else 100)
    d_ = b - F(r.randint(1, 9), 100) if L == 2 else None
    vals = [a, b, c] + ([d_] if d_ is not None and d_ > 0 else [])
    need(len(set(vals)) == len(vals) and all(is_term(v) for v in vals))
    shown = vals[:]
    r.shuffle(shown)
    desc = L == 2 and r.random() < 0.5
    srt = sorted(vals, reverse=desc)
    ans = ", ".join(dec(v) for v in srt)
    by_len = sorted(vals, key=lambda v: (len(dec(v)), v), reverse=desc)
    return Item(f"Order from {'greatest to least' if desc else 'least to greatest'}: {', '.join(dec(v) for v in shown)}", ans,
                ["Line up the decimal points. Write zeros so every number has the same number of places.", f"Order: {ans}."],
                wrongs(ans, [W(", ".join(dec(v) for v in by_len), "ordered by how many digits each number has"), W(", ".join(dec(v) for v in sorted(vals, reverse=not desc)), "ordered in the opposite direction"),
                             W(", ".join(dec(v) for v in shown), "did not reorder the numbers")]),
                FN("order", values=[dec(v) for v in vals], desc=desc), qtype="procedural")


@fam("012", mode="mc")
def s4_between(r, L):
    w = r.randint(0, 20)
    t = r.randint(1, 8)
    lo, hi = w + F(t, 10), w + F(t + 1, 10)
    good = lo + F(r.randint(1, 9), 100)
    if L == 2:
        lo, hi = w + F(t, 10) + F(r.randint(1, 8), 100), None
        hi = lo + F(1, 100)
        good = lo + F(r.randint(1, 9), 1000)
    bad = [hi + F(r.randint(1, 9), 100 if L < 2 else 1000), lo - F(r.randint(1, 9), 100 if L < 2 else 1000), w + F(t * 10 + 5, 1000) if L < 2 else hi + F(5, 1000)]
    bad = [dec(x) for x in bad if not (lo < x < hi) and x > 0]
    bad = list(dict.fromkeys(bad))[:3]
    need(len(bad) == 3 and lo < good < hi)
    opts = [(dec(good), True)] + [(x, False) for x in bad]
    r.shuffle(opts)
    return Item(f"Which number is between {dec(lo)} and {dec(hi)}?", dec(good),
                ["Write each number with the same number of decimal places.", f"{dec(lo)} < {dec(good)} < {dec(hi)}."],
                check=FN("between", lo=dec(lo), hi=dec(hi)), options=opts, mode="mc", qtype="reasoning" if False else "conceptual")


@fam("012")
def s4_numberline(r, L):
    w = r.randint(0, 9)
    t = r.randint(0, 9)
    lo = w + F(t, 10)
    hi = lo + F(1, 10)
    h = r.randint(1, 9)
    x = lo + F(h, 100)
    alt = f"Number line from {dec(lo)} to {dec(hi)} divided into 10 equal parts. Point A is at the {h}th tick after {dec(lo)}."
    it = Item("What decimal is at point A?", dec(x),
                [f"From {dec(lo)} to {dec(hi)} is 1 tenth, split into 10 equal parts, so each part is 1 hundredth.", f"Point A is {h} hundredths past {dec(lo)}: {dec(x)}."],
                wrongs(dec(x), [W(dec(lo + F(h, 10)), "counted each tick as a tenth"), W(dec(lo + F(h, 1000)), "counted each tick as a thousandth"), W(dec(lo + F(h + 1, 100)), "counted one tick too many")]),
                EX(f"{dec(lo)}+{h}/100"), qtype="visual",
                diagram=Diagram("number_line", {"lo": dec(lo), "hi": dec(hi), "den": 100, "label_every": 10, "fmt": "dec", "points": [{"x": frac(x), "label": "A"}],
                                                "labels": "all"}, alt))
    it.consts = [h]
    return it


@fam("012")
def s4_context(r, L):
    nm = [name(r) for _ in range(4)]
    need(len(set(nm)) == 3 or len(set(nm)) == 4)
    nm = list(dict.fromkeys(nm))[:3]
    need(len(nm) == 3)
    a, b = close_pair(r, max(L, 1))
    c = a + F(r.randint(1, 9), 100)
    vals = [a, b, c]
    need(len(set(vals)) == 3)
    ctx = pick(r, [("swam 50 meters", "seconds", "fastest", min), ("jumped", "meters", "farthest", max), ("grew a sunflower", "meters tall", "tallest", max)])
    best = ctx[3](vals)
    who = nm[vals.index(best)]
    other = nm[vals.index(ctx[3] is min and max(vals) or min(vals))]
    desc = "; ".join(f"{n}: {dec(v)} {ctx[1]}" for n, v in zip(nm, vals))
    q = {"swam 50 meters": "Three friends swam 50 meters. Their times were", "jumped": "Three friends did a long jump. Their distances were",
         "grew a sunflower": "Three friends grew sunflowers. The heights were"}[ctx[0]]
    return Item(f"{q}: {desc}. Who was {ctx[2]}?", who, [f"Compare {', '.join(dec(v) for v in vals)} place by place.",
                f"The {'least time' if ctx[3] is min else 'greatest value'} is {dec(best)}, so {who} was {ctx[2]}."],
                wrongs(who, [W(other, "chose the opposite extreme"), W([n for n in nm if n not in (who, other)][0], "compared the number of digits")]),
                FN("extreme", values={n: dec(v) for n, v in zip(nm, vals)}, which="min" if ctx[3] is min else "max"), qtype="real-world", mode="sa")


# ============================================================== S5 Rounding Decimals
RPL = {"whole number": 0, "tenth": -1, "hundredth": -2}


def round_half_up(x, e):
    q = F(10) ** e
    n = x / q
    fl = n.numerator // n.denominator
    return (fl + (1 if n - fl >= F(1, 2) else 0)) * q


@fam("012")
def s5_round(r, L):
    places = 2 if L == 0 else 3
    x = r.randint(0, 99 if L else 20) + F(r.randint(1, 10 ** places - 1), 10 ** places)
    opts = ["whole number", "tenth"] + (["hundredth"] if places == 3 else [])
    p = pick(r, opts)
    e = RPL[p]
    y = round_half_up(x, e)
    need(y != x)
    trunc = F((x / F(10) ** e).numerator // (x / F(10) ** e).denominator) * F(10) ** e
    other = round_half_up(x, e - 1) if e - 1 >= -3 else x
    pl = {"whole number": "the nearest whole number", "tenth": "the nearest tenth", "hundredth": "the nearest hundredth"}[p]
    ans = dec(y, -e if e < 0 else None)
    bad = [W(dec(trunc, -e if e < 0 else None), "dropped the extra digits without rounding up") if trunc != y else W(dec(trunc + F(10) ** e, -e if e < 0 else None), "rounded up when it should round down"),
           W(dec(other), "rounded to the wrong place"), W(dec(y + F(10) ** e, -e if e < 0 else None) if trunc == y else dec(y - F(10) ** e * 2, -e if e < 0 else None) if y - F(10) ** e * 2 > 0 else dec(y + 2 * F(10) ** e), "changed the wrong digit")]
    return Item(f"Round {dec(x)} to {pl}.", ans,
                [f"Look at the digit just to the right of the {p if p != 'whole number' else 'ones'} place.", f"{'5 or more: round up' if y > trunc else 'Less than 5: keep the digit'}. {dec(x)} ≈ {ans}."],
                wrongs(ans, bad), FN("round", x=dec(x), place={"whole number": "ones", "tenth": "tenths", "hundredth": "hundredths"}[p]),
                qtype="procedural", claim=f"{dec(x)} rounded to {pl}")


@fam("012")
def s5_money(r, L):
    x = F(r.randint(101, 9999), 100)
    p = pick(r, ["dollar", "ten cents"]) if L else "dollar"
    e = 0 if p == "dollar" else -1
    y = round_half_up(x, e)
    need(y != x)
    item = pick(r, ["a backpack", "a board game", "a soccer ball", "a puzzle", "art supplies"])
    nm = name(r)
    trunc = F((x / F(10) ** e).numerator // (x / F(10) ** e).denominator) * F(10) ** e
    ans = money(y)
    return Item(f"{nm} buys {item} for {money(x)}. Round the price to the nearest {p}.", ans,
                [f"Look at the digit to the right of the {'ones' if e == 0 else 'tenths'} place.", f"{money(x)} rounds to {ans}."],
                wrongs(ans, [W(money(trunc) if trunc != y else money(trunc + F(10) ** e), "rounded in the wrong direction"), W(money(round_half_up(x, e + 1)), "rounded to the wrong place"), W(money(x + F(1, 100)), "changed the cents by one")]),
                FN("round", x=dec(x), place="ones" if e == 0 else "tenths"), qtype="real-world")


@fam("012", mode="mc")
def s5_could_be(r, L):
    t = r.randint(10, 99) + F(r.randint(1, 9), 10)
    p = "tenth"
    good = t + F(r.randint(-5, 4), 100)
    need(round_half_up(good, -1) == t)
    bad = [t + F(r.randint(5, 9), 100), t - F(r.randint(6, 9), 100), t + F(1, 10) + F(r.randint(0, 4), 100)]
    if L == 2:
        good = t - F(5, 100) + F(r.randint(0, 9), 1000)
        need(round_half_up(good, -1) == t)
        bad = [t - F(5, 100) - F(r.randint(1, 9), 1000), t + F(5, 100) + F(r.randint(0, 9), 1000), t + F(1, 10)]
    bad = [dec(b) for b in bad if round_half_up(b, -1) != t and b > 0]
    bad = list(dict.fromkeys(bad))[:3]
    need(len(bad) == 3)
    opts = [(dec(good), True)] + [(b, False) for b in bad]
    r.shuffle(opts)
    return Item(f"A number rounded to the nearest tenth is {dec(t)}. Which could be the number?", dec(good),
                [f"Numbers from {dec(t - F(5, 100))} up to (but not including) {dec(t + F(5, 100))} round to {dec(t)}.", f"{dec(good)} is in that range."],
                check=FN("rounds_to", target=dec(t), place="tenths"), options=opts, mode="mc", qtype="explain", tags={"reasoning"})


@fam("12")
def s5_extreme(r, L):
    t = r.randint(1, 99) + F(r.randint(1, 9), 10)
    big = r.random() < 0.5
    v = t + F(4, 100) if big else t - F(5, 100)
    word = "greatest" if big else "least"
    return Item(f"What is the {word} number with two decimal places that rounds to {dec(t)} (nearest tenth)?", dec(v, 2),
                [f"Numbers from {dec(t - F(5, 100))} to {dec(t + F(4, 100))} (with two decimal places) round to {dec(t)}.", f"The {word} is {dec(v, 2)}."],
                wrongs(dec(v, 2), [W(dec(t + F(5, 100)) if big else dec(t - F(4, 100)), "used a number that rounds to a different tenth" if big else "did not go down far enough"),
                                   W(dec(t + F(9, 100)) if big else dec(t - F(9, 100)), "went past the halfway point"), W(dec(t, 2), "gave the rounded number itself")]),
                FN("rounds_extreme", target=dec(t), which="max" if big else "min", places=2), qtype="explain", tags={"reasoning", "challenge"}, mode="sa")


@fam("012")
def s5_numberline(r, L):
    w = r.randint(0, 9)
    t = r.randint(0, 9)
    lo = w + F(t, 10)
    hi = lo + F(1, 10)
    h = pick(r, [1, 2, 3, 4, 6, 7, 8, 9]) if L < 2 else r.randint(1, 9)
    x = lo + F(h, 100)
    y = round_half_up(x, -1)
    alt = f"Number line from {dec(lo)} to {dec(hi)} with 10 equal parts. Point P is {h} parts after {dec(lo)}."
    return Item("Point P is on the number line. Round the number at P to the nearest tenth.", dec(y, 1),
                [f"P is at {dec(x)}.", f"{dec(x)} is closer to {dec(y, 1)}" + (" (5 hundredths rounds up)." if h == 5 else ".")],
                wrongs(dec(y, 1), [W(dec(hi if y == lo else lo, 1), "chose the farther tenth"), W(dec(x), "did not round"), W(dec(round_half_up(x, 0)), "rounded to the nearest whole number")]),
                FN("round", x=dec(x), place="tenths"), qtype="visual",
                diagram=Diagram("number_line", {"lo": dec(lo), "hi": dec(hi), "den": 100, "label_every": 10, "fmt": "dec", "points": [{"x": frac(x), "label": "P"}]}, alt))


@fam("012")
def s5_closer(r, L):
    places = 2 if L < 2 else 3
    e = -1 if places == 2 else pick(r, [-1, -2])
    x = r.randint(0, 50) + F(r.randint(1, 10 ** places - 1), 10 ** places)
    q = F(10) ** e
    lo = F((x / q).numerator // (x / q).denominator) * q
    hi = lo + q
    need(x not in (lo, hi) and x - lo != hi - x)
    near = lo if x - lo < hi - x else hi
    far = hi if near == lo else lo
    pl = -e
    return Item(f"Is {dec(x)} closer to {dec(lo, pl)} or {dec(hi, pl)}?", dec(near, pl),
                [f"{dec(x)} is {dec(x - lo)} away from {dec(lo, pl)} and {dec(hi - x)} away from {dec(hi, pl)}.", f"It is closer to {dec(near, pl)}."],
                [W(dec(far, pl), "looked at the wrong digit"), W(dec(x), "did not choose one of the two numbers")],
                FN("closer", x=dec(x), a=dec(lo, pl), b=dec(hi, pl)), qtype="conceptual", mode="sa")


SKILLS = {
    1: dict(name="Place Value Patterns", fams=[s1_digit_value, s1_times, s1_tenth_of, s1_place_name, s1_chart, s1_blocks, s1_missing, s1_true_statement]),
    2: dict(name="Powers of Ten and Exponents", fams=[s2_exp_value, s2_exp_write, s2_multiply, s2_divide, s2_missing_exp, s2_zeros, s2_shift]),
    3: dict(name="Reading and Writing Decimals", fams=[s3_word_to_std, s3_std_to_word, s3_expanded, s3_from_expanded, s3_grid, s3_frac_to_dec]),
    4: dict(name="Comparing and Ordering Decimals", fams=[s4_compare, s4_true_cmp, s4_order, s4_between, s4_numberline, s4_context]),
    5: dict(name="Rounding Decimals", fams=[s5_round, s5_money, s5_could_be, s5_extreme, s5_numberline, s5_closer]),
}
