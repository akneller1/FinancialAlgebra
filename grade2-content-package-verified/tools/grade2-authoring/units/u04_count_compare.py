"""Unit 4: Counting and Comparing to 1,000 (count-compare-1000). 2.NBT.A.2, 2.NBT.A.4, 2.NBT.B.8."""
from g2lib import *

UNIT_ID = "count-compare-1000"


def edge(r, L):
    """A number near a ten (L0), a hundred (L1), or anywhere (L2), 100-998."""
    if L == 0:
        return r.randint(10, 98) * 10 + pick(r, [7, 8, 9])
    if L == 1:
        return r.randint(1, 9) * 100 + pick(r, [-3, -2, -1])
    return r.randint(1, 9) * 100 + pick(r, [-2, -1, 1, 2, 9, 10])


def seq_text(seq, k):
    return ", ".join("?" if i == k else str(v) for i, v in enumerate(seq))


# ============================================================== S1 Counting within 1,000
@fam("012")
def cn_after(r, L):
    n = edge(r, L)
    need(100 <= n <= 998)
    way = "after" if L < 2 or r.random() < 0.5 else "before"
    a = n + 1 if way == "after" else n - 1
    return Item(f"What number comes just {way} {n}?", a, [f"Count {'on' if way == 'after' else 'back'} by one from {n}.", f"The number just {way} {n} is {a}."],
                [W(n + 10 if way == "after" else n - 10, "changed the tens instead of the ones"), W(int(str(n)[:-1] + str((n + 1) % 10)) if way == "after" and n % 10 == 9 else a + 100, "did not cross the ten" if way == "after" and n % 10 == 9 else "changed the hundreds"),
                 W(n - 1 if way == "after" else n + 1, "counted the wrong way")],
                FN("neighbor", n=n, way=way), qtype="procedural", claim=f"The number just {way} {n}")


@fam("012")
def cn_seq(r, L):
    n = edge(r, L)
    step = 1 if L < 2 else pick(r, [1, -1])
    seq = [n - 2 * step + i * step for i in range(5)]
    need(all(100 <= v <= 1000 for v in seq))
    k = r.randint(1, 4)
    shown = seq_text(seq, k)
    return Item(f"Count {'on' if step == 1 else 'back'} by ones. What number is missing? {shown}", seq[k], [f"Each number is 1 {'more' if step == 1 else 'less'} than the one before.", f"The missing number is {seq[k]}."],
                [W(seq[k] + 10 * step, "changed the tens"), W(seq[k] - step, "repeated a number"), W(seq[k] + step, "skipped a number"), W(seq[k] - 100 if seq[k] >= 200 else seq[k] + 100, "changed the hundreds")],
                FN("skip_missing", seq=shown, step=step), qtype="procedural")


@fam("012")
def cn_chart(r, L):
    start = r.randint(10, 89) * 10 + 1 if L else r.randint(10, 49) * 10 + 1
    rows = 3
    v = start + r.randint(0, rows * 10 - 1)
    need(v % 10 not in (1,) or L > 0)
    alt = f"Part of a counting chart from {start} to {start + 29}, ten numbers in each row. One box shows a question mark."
    return Item("What number belongs in the box with the question mark?", v, ["Each box is 1 more than the box to its left and 10 more than the box above it.", f"The missing number is {v}."],
                [W(v + 10, "used the row below"), W(v - 10, "used the row above"), W(v + 1, "used the box to the right"), W(v - 1, "used the box to the left")],
                FN("chart_hidden", start=start, per_row=10, rows=rows, hide=[v]), qtype="visual", diagram=Diagram("chart", {"start": start, "rows": rows, "hide": [v]}, alt))


@fam("012")
def cn_between(r, L):
    n = edge(r, L)
    need(101 <= n <= 998)
    return Item(f"What number is between {n - 1} and {n + 1}?", n, [f"Count {n - 1}, ___, {n + 1}.", f"The number between them is {n}."],
                [W(n + 10, "changed the tens"), W(n - 1, "gave the first number"), W(n + 1, "gave the last number"), W(n - 100 if n > 199 else n + 100, "changed the hundreds")],
                FN("between_one", lo=n - 1, hi=n + 1), qtype="procedural", claim=f"The number between {n - 1} and {n + 1}")


@fam("12")
def cn_next3(r, L):
    n = edge(r, L)
    step = 1 if L == 1 else pick(r, [1, -1])
    need(100 <= n + 3 * step <= 999)
    ans = ", ".join(str(n + step * i) for i in range(1, 4))
    return Item(f"Count {'on' if step == 1 else 'back'} by ones from {n}. Write the next three numbers.", ans, ["Change the ones each time; cross the ten or hundred when you need to.", f"{n}, {ans}."],
                [W(", ".join(str(n + 10 * step * i) for i in range(1, 4)), "counted by tens"), W(", ".join(str(n - step * i) for i in range(1, 4)), "counted the wrong way")],
                FN("pattern_list", start=str(n + step), step=str(step), count=3, op="add"), qtype="procedural")


@fam("012", mode="mc")
def cn_cross(r, L):
    h = r.randint(1, 8)
    n = 100 * h + 99 if L else 10 * r.randint(10, 89) + 9
    good = f"{n}, {n + 1}, {n + 2}"
    bad = [f"{n}, {n // 10}{0}, {n + 2}" if L == 0 else f"{n}, {n + 1}, {n + 1 + 100}", f"{n}, {n + 1 + 9}, {n + 1 + 10}" if L == 0 else f"{n}, {h}{100}, {h}{101}", f"{n}, {n + 10}, {n + 20}"]
    need(len(set(bad)) == 3 and good not in bad)
    it = mc_key(f"Which shows counting on by ones from {n}?", good, bad, [f"After {n} comes {n + 1}.", f"Then {n + 2}."], qtype="conceptual", r=r)
    it.check = FN("count_seq", start=n, step=1)
    return it


@fam("2", mode="mc")
def cn_error(r, L):
    h = r.randint(1, 8)
    n = 100 * h + 98
    nm = name(r)
    wrong = f"{n}, {n + 1}, {h}{100}"
    good = f"No. After {n + 1} comes {n + 2}, which is {pl(h + 1, 'hundred')}."
    bad = [f"Yes. After {n + 1} comes {h}{100}.", f"No. After {n + 1} comes {n + 11}.", f"No. After {n + 1} comes {n}."]
    it = mc_key(f"{nm} counted: {wrong}. Is {nm} right?", good, bad, [f"{n + 1} + 1 = {n + 2}.", f"{n + 2} has {h + 1} hundreds, 0 tens, and 0 ones."], qtype="error-analysis", tags={"misconception"}, r=r)
    it.check = FN("cross_reason", n=n)
    return it


# ============================================================== S2 Skip Counting by 5s, 10s, and 100s
def sk_start(r, L, step):
    if L == 0:
        return r.randint(1, 15) * step if step < 100 else r.randint(1, 4) * 100
    if L == 1:
        return r.randint(10, 150) * 5 if step == 5 else r.randint(10, 80) * 10 if step == 10 else r.randint(1, 4) * 100
    return r.randint(100, 600) if step == 100 else r.randint(100, 900)


@fam("012")
def sk_missing(r, L):
    step = pick(r, [5, 10, 100])
    s0 = sk_start(r, L, step)
    seq = [s0 + step * i for i in range(5)]
    need(seq[-1] <= 1000)
    k = r.randint(1, 4)
    shown = seq_text(seq, k)
    return Item(f"Skip count by {step}s. What number is missing? {shown}", seq[k], [f"Each number is {step} more than the one before.", f"The missing number is {seq[k]}."],
                [W(seq[k - 1] + (10 if step != 10 else 5), "counted by the wrong amount"), W(seq[k - 1] + 1, "counted by ones"), W(seq[k] + step, "skipped a number"), W(seq[k - 1] + (100 if step != 100 else 10), "counted by the wrong amount")],
                FN("skip_missing", seq=shown, step=step), qtype="procedural")


@fam("012")
def sk_next3(r, L):
    step = pick(r, [5, 10, 100])
    s0 = sk_start(r, L, step)
    need(s0 + 3 * step <= 1000)
    ans = ", ".join(str(s0 + step * i) for i in range(1, 4))
    return Item(f"Count by {step}s from {s0}. Write the next three numbers.", ans, [f"Add {step} each time.", f"{s0}, {ans}."],
                [W(", ".join(str(s0 + (10 if step != 10 else 5) * i) for i in range(1, 4)), "counted by the wrong amount"), W(", ".join(str(s0 + i) for i in range(1, 4)), "counted by ones")],
                FN("pattern_list", start=str(s0 + step), step=str(step), count=3, op="add"), qtype="procedural", claim=f"Next three numbers counting by {step}s from {s0}")


@fam("012")
def sk_by(r, L):
    step = pick(r, [5, 10, 100])
    s0 = sk_start(r, L, step)
    seq = [s0 + step * i for i in range(4)]
    need(seq[-1] <= 1000)
    return Item(f"What number is this pattern counting by? {', '.join(map(str, seq))}", step, ["Find how much each number grows.", f"{seq[1]} − {seq[0]} = {step}, so it counts by {step}s."],
                [W(1 if step != 1 else 2, "looked only at the ones digit"), W(10 if step != 10 else 100, "looked at the wrong place"), W(seq[-1], "gave the last number")],
                FN("step_of", seq=seq), qtype="conceptual")


@fam("012")
def sk_story(r, L):
    step = pick(r, [5, 10]) if L < 2 else pick(r, [5, 10, 100])
    k = r.randint(3, 8) if L == 0 else r.randint(5, 12)
    t = {5: ("bags", "apples"), 10: ("packs", "pencils"), 100: ("boxes", "paper clips")}[step]
    need(step * k <= 1000)
    return Item(f"Each of the {t[0]} has {step} {t[1]}. Count by {step}s to find how many {t[1]} are in {k} {t[0]}.", f"{step * k} {t[1]}",
                [f"Count by {step}s {k} times: {', '.join(str(step * i) for i in range(1, k + 1))}.", f"There are {step * k} {t[1]}."],
                [W(f"{step * (k - 1)} {t[1]}", "stopped one count early"), W(f"{step * (k + 1)} {t[1]}", "counted one too many"), W(f"{step + k} {t[1]}", "added the two numbers")],
                FN("count_by", step=step, times=k, unit=t[1]), qtype="word-problem", tags={"modeling"})


@fam("01")
def sk_line(r, L):
    step = pick(r, [5, 10])
    s0 = r.randint(2, 15) * step if L == 0 else r.randint(20, 120) * 5 // step * step + (5 if step == 10 and r.random() < 0.5 else 0)
    k = r.randint(3, 5)
    end = s0 + k * step
    lo = s0 // 10 * 10 - (10 if step == 5 else 10)
    hi = lo + 80 if step == 10 else lo + 40
    need(end <= hi - 5 and lo >= 0)
    alt = f"A number line from {lo} to {hi}. Starting at {s0}, there are {k} jumps of {step}. A question mark marks where the last jump lands."
    return Item(f"Start at {s0} and make {k} jumps of {step}. Where do you land?", end, [f"Count by {step}s from {s0}.", f"You land on {end}."],
                [W(end - step, "made one jump too few"), W(end + step, "made one jump too many"), W(s0 + k, "jumped by ones")],
                FN("jumps_land", start=s0, step=step, jumps=k), qtype="visual",
                diagram=Diagram("jline", {"lo": lo, "hi": hi, "step": 5 if step == 5 else 5, "label_every": 2, "jumps": [[s0 + step * i, s0 + step * (i + 1), ""] for i in range(k)], "points": [{"v": end, "label": "?"}]}, alt))


@fam("012", mode="mc")
def sk_which(r, L):
    step = pick(r, [5, 10, 100])
    s0 = sk_start(r, L, step)
    seqs = {d: ", ".join(str(s0 + d * i) for i in range(4)) for d in (1, 5, 10, 100)}
    need(s0 + 300 <= 1000)
    good = seqs[step]
    bad = [v for d, v in seqs.items() if d != step]
    it = mc_key(f"Which shows counting by {step}s?", good, bad, [f"Each number must be {step} more than the one before.", good + "."], r=r)
    it.check = FN("seq_by", step=step)
    return it


@fam("2", mode="mc")
def sk_error(r, L):
    h = r.randint(1, 8)
    s0 = 100 * h + 80
    nm = name(r)
    good = f"{s0 + 20}, because {s0 + 10} + 10 = {s0 + 20}"
    bad = [f"{h}{100}, because the tens go up after 9", f"{s0 + 11}, because you count on by ones", f"{s0 + 10 + 100}, because you cross a hundred"]
    it = mc_key(f"{nm} counts by 10s: {s0}, {s0 + 10}, ___. What number comes next?", good, bad, [f"Add 10 to {s0 + 10}.", f"{s0 + 10} + 10 = {s0 + 20}, which is {pl(h + 1, 'hundred')}."], qtype="error-analysis", tags={"misconception"}, r=r)
    it.check = FN("next_by10", n=s0 + 10)
    return it


# ============================================================== S3 Comparing Three-Digit Numbers
def cmp_pair(r, L):
    a = r.randint(101, 999)
    if L == 0:
        b = a + pick(r, [-200, -100, 100, 200, 300])
    elif L == 1:
        b = a + pick(r, [-20, -10, 10, 20, -1, 1]) * pick(r, [1, 3])
    else:
        h, t, o = a // 100, a // 10 % 10, a % 10
        b = pick(r, [h * 100 + o * 10 + t, t * 100 + h * 10 + o, a + pick(r, [-9, 9, 90, -90])])
    need(100 <= b <= 999 and a != b)
    return a, b


@fam("012")
def cp_sym(r, L):
    a, b = cmp_pair(r, L)
    s = ">" if a > b else "<"
    return Item(f"Compare. Write >, =, or <. {a} ___ {b}", s, ["Compare the hundreds first, then the tens, then the ones.", f"{a} {s} {b}."],
                [W("<" if s == ">" else ">", "read the symbol backward"), W("=", "thought the numbers are equal")], FN("compare", a=str(a), b=str(b)), qtype="procedural", claim=f"{a} ___ {b}")


@fam("012")
def cp_greater(r, L):
    a, b = cmp_pair(r, L)
    want = pick(r, ["greater", "less"])
    ans = max(a, b) if want == "greater" else min(a, b)
    return Item(f"Which number is {want}: {a} or {b}?", ans, ["Compare the digits from the hundreds place.", f"{ans} is {want}."],
                [W(min(a, b) if want == "greater" else max(a, b), "compared from the ones place")], FN("cmp_pick", nums=[a, b], want=want), qtype="procedural")


@fam("012", mode="mc")
def cp_true(r, L):
    a, b = cmp_pair(r, L)
    hi, lo = max(a, b), min(a, b)
    good = f"{hi} > {lo}" if r.random() < 0.5 else f"{lo} < {hi}"
    bad = [f"{lo} > {hi}", f"{hi} < {lo}", f"{hi} = {lo}"]
    it = mc_key(f"Which comparison of {a} and {b} is true?", good, bad, [f"{hi} is greater than {lo}.", good + "."], r=r)
    it.check = FN("true_cmp")
    return it


@fam("012")
def cp_order(r, L):
    a = r.randint(101, 899)
    h, t, o = a // 100, a // 10 % 10, a % 10
    need(len({h, t, o}) == 3 and 0 not in (h, t, o))
    vals = list({a, h * 100 + o * 10 + t, t * 100 + h * 10 + o} if L else {a, a + 100, a - 50 if a > 160 else a + 50})
    need(len(vals) == 3)
    r.shuffle(vals)
    desc = L == 2 and r.random() < 0.5
    ans = ", ".join(str(v) for v in sorted(vals, reverse=desc))
    return Item(f"Write the numbers in order from {'greatest to least' if desc else 'least to greatest'}: {', '.join(map(str, vals))}", ans,
                ["Compare the hundreds, then the tens, then the ones.", f"In order: {ans}."],
                [W(", ".join(str(v) for v in sorted(vals, reverse=not desc)), "ordered the wrong way"), W(", ".join(str(v) for v in sorted(vals, key=lambda x: x % 10, reverse=desc)), "ordered by the ones digits")],
                FN("order", values=[str(v) for v in vals], desc=desc), qtype="procedural")


@fam("012")
def cp_story(r, L):
    a, b = cmp_pair(r, L)
    n1, n2 = name(r), name(sub(r, 5))
    need(n1 != n2)
    t = pick(r, ["points in a game", "steps on a walk", "pages in a book"])
    big = n1 if a > b else n2
    return Item(f"{n1} has {a} {t.split(' ')[0]} and {n2} has {b} {t.split(' ')[0]}. Who has more?", big, [f"Compare {a} and {b}.", f"{max(a, b)} > {min(a, b)}, so {big} has more."],
                [W(n2 if big == n1 else n1, "compared the wrong digits")], FN("who_more2", people={n1: a, n2: b}), qtype="word-problem")


@fam("12")
def cp_words(r, L):
    a, b = cmp_pair(r, L)
    s = ">" if a > b else "<"
    return Item(f"Compare. Write >, =, or <. {hto(a)} ___ {b}", s, [f"{hto(a)} is {a}.", f"{a} {s} {b}."],
                [W("<" if s == ">" else ">", "read the symbol backward"), W("=", "thought the numbers are equal")], FN("compare", a=str(a), b=str(b)), qtype="conceptual")


@fam("2")
def cp_digit(r, L):
    h, o = r.randint(1, 9), r.randint(0, 9)
    other = r.randint(100, 999)
    need(other // 100 == h and 1 <= other // 10 % 10 <= 8)
    want = pick(r, ["greatest", "least"])
    shown = f"{h}□{o}"
    if want == "greatest":
        ans = max(d for d in range(10) if h * 100 + d * 10 + o < other)
        q = f"What is the greatest digit that can go in the box to make {shown} < {other} true?"
    else:
        ans = min(d for d in range(10) if h * 100 + d * 10 + o > other)
        q = f"What is the least digit that can go in the box to make {shown} > {other} true?"
    return Item(q, ans, ["The hundreds are the same, so compare the tens and ones.", f"The {want} digit that works is {ans}."],
                [W(other // 10 % 10, "used the tens digit of the other number"), W(ans + (1 if want == "greatest" else -1), "did not check the ones digit"), W(9 if want == "greatest" else 0, "chose the biggest or smallest digit")],
                FN("cmp_digit", h=h, o=o, other=other, want=want), qtype="explain", tags={"reasoning"})


@fam("2", mode="mc")
def cp_error(r, L):
    h = r.randint(1, 8)
    a = h * 100 + r.randint(80, 99)
    b = (h + 1) * 100 + r.randint(1, 19)
    nm = name(r)
    good = f"{b}, because {h + 1} hundreds is more than {h} hundreds"
    bad = [f"{a}, because it has more tens", f"{a}, because it has bigger digits", f"They are equal, because both have 3 digits"]
    it = mc_key(f"{nm} says {a} is greater than {b} because 9 is a big digit. Which number is really greater?", good, bad,
                ["Compare the hundreds first.", f"{h + 1} hundreds > {h} hundreds, so {b} > {a}."], qtype="error-analysis", tags={"misconception"}, r=r)
    it.check = FN("cmp_reason", a=a, b=b)
    return it


@fam("012", mode="mc")
def cp_greatest(r, L):
    a, b = cmp_pair(r, L)
    c, d = cmp_pair(r, L)
    vals = [a, b, c, d]
    need(len(set(vals)) == 4)
    want = pick(r, ["greatest", "least"])
    best = max(vals) if want == "greatest" else min(vals)
    it = mc_key(f"Which number is the {want}?", str(best), [str(v) for v in vals if v != best],
                ["Compare the hundreds first, then the tens, then the ones.", f"{best} is the {want}."], qtype="procedural", r=r)
    it.check = FN("extreme", values={str(v): str(v) for v in vals}, which="max" if want == "greatest" else "min")
    return it


@fam("12", mode="mc")
def cp_which_place(r, L):
    a, b = cmp_pair(r, L)
    sa, sb = str(a), str(b)
    k = next(i for i in range(3) if sa[i] != sb[i])
    places = ["hundreds", "tens", "ones"]
    s = ">" if a > b else "<"
    good = f"{a} {s} {b}, because the {places[k]} digits are different and {sa[k]} {s} {sb[k]}"
    bad = [f"{a} {'<' if s == '>' else '>'} {b}, because the ones digits are {sa[2]} and {sb[2]}", f"{a} = {b}, because they have the same digits" if sorted(sa) == sorted(sb) else f"{a} = {b}, because both have 3 digits",
           f"{a} {'<' if s == '>' else '>'} {b}, because {sa[k]} {'<' if s == '>' else '>'} {sb[k]}"]
    need(len(set(bad)) == 3)
    it = mc_key(f"Compare {a} and {b}. Choose the correct comparison and reason.", good, bad, ["Start with the hundreds; move right only when the digits are the same.", good + "."], qtype="explain", tags={"reasoning"}, r=r)
    it.check = FN("cmp_place", a=a, b=b)
    return it


# ============================================================== S4 Adding and Subtracting 10 and 100
def tt_num(r, L, op, k):
    n = r.randint(100, 900)
    if L >= 1 and k == 10 and r.random() < 0.6:
        n = n // 100 * 100 + (90 + n % 10 if op == "+" else n % 10)
    need(100 <= n <= 900)
    v = n + k if op == "+" else n - k
    need(0 < v <= 1000)
    return n, v


def tt_wrongs(n, op, k):
    o = 1 if op == "+" else -1
    return [W(n + o * (100 if k == 10 else 10), "changed the wrong place"), W(n + o, "changed the ones"), W(n - o * k, "added instead of subtracting" if op == "−" else "subtracted instead of adding"),
            W(int(str(n)[0] + str((n // 10 % 10 + o) % 10) + str(n)[2]) if k == 10 else n + o * k + 10, "did not regroup the hundreds" if k == 10 else "changed an extra ten")]


@fam("012")
def tt_more(r, L):
    op, k = pick(r, ["+", "−"]), pick(r, [10, 100])
    n, v = tt_num(r, L, op, k)
    word = "more" if op == "+" else "less"
    return Item(f"What is {k} {word} than {n}?", v, [f"{'Add' if op == '+' else 'Subtract'} {k}: the {'tens' if k == 10 else 'hundreds'} digit changes by 1.", f"{n} {op} {k} = {v}."],
                tt_wrongs(n, op, k), EX(f"{n}{'+' if op == '+' else '-'}{k}"), qtype="procedural", claim=f"{k} {word} than {n}")


@fam("012")
def tt_eq(r, L):
    op, k = pick(r, ["+", "−"]), pick(r, [10, 100])
    n, v = tt_num(r, L, op, k)
    return Item(f"{n} {op} {k} = ___", v, [f"Only the {'tens' if k == 10 else 'hundreds'} digit changes, unless you cross a hundred.", f"{n} {op} {k} = {v}."],
                tt_wrongs(n, op, k), EX(f"{n}{'+' if op == '+' else '-'}{k}"), qtype="procedural", claim=f"{n} {op} {k}")


@fam("01")
def tt_chart(r, L):
    start = r.randint(10, 80) * 10 + 1
    v = start + 10 + r.randint(0, 9)
    way = pick(r, ["more", "less"])
    ans = v + 10 if way == "more" else v - 10
    alt = f"Part of a counting chart from {start} to {start + 29}, ten numbers in each row. The number {v} is shaded."
    return Item(f"Find the shaded number. What number is 10 {way} than it?", ans, [f"In the chart, 10 {way} is the box just {'below' if way == 'more' else 'above'}.", f"{v} {'+' if way == 'more' else '−'} 10 = {ans}."],
                [W(v + 1 if way == "more" else v - 1, "moved one box instead of one row"), W(v + 100 if way == "more" else v - 100, "changed the hundreds"), W(v, "gave the shaded number")],
                EX(f"{v}{'+' if way == 'more' else '-'}10"), qtype="visual", diagram=Diagram("chart", {"start": start, "rows": 3, "shade": [v]}, alt))


@fam("012")
def tt_story(r, L):
    op, k = pick(r, ["+", "−"]), pick(r, [10, 100])
    n, v = tt_num(r, L, op, k)
    nm = name(r)
    t = (f"{nm} has {n} points. {nm} earns {k} more points. How many points does {nm} have now?" if op == "+" else
         f"A shop has {n} stickers. It sells {k} stickers. How many stickers are left?")
    u = "points" if op == "+" else "stickers"
    return Item(t, f"{v} {u}", [f"{'Add' if op == '+' else 'Subtract'} {k}: {n} {op} {k}.", f"{n} {op} {k} = {v} {u}."], [W(f"{w} {u}", y) for w, y in tt_wrongs(n, op, k)],
                EX(f"{n}{'+' if op == '+' else '-'}{k}", unit=u), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def tt_which(r, L):
    op, k = pick(r, ["+", "−"]), pick(r, [10, 100])
    n, v = tt_num(r, L, op, k)
    word = "more" if op == "+" else "less"
    bad = [w for w, _ in tt_wrongs(n, op, k)][:3]
    need(len(set(bad)) == 3 and str(v) not in bad)
    it = mc_key(f"Which number is {k} {word} than {n}?", str(v), bad, [f"{n} {op} {k} = {v}.", f"The answer is {v}."], r=r)
    it.check = EX(f"{n}{'+' if op == '+' else '-'}{k}")
    return it


@fam("2")
def tt_unknown(r, L):
    op, k = pick(r, ["+", "−"]), pick(r, [10, 100])
    n, v = tt_num(r, 2, op, k)
    eq = f"___ {op} {k} = {v}"
    return Item(f"What number makes the equation true? {eq}", n, [f"Undo the {'adding' if op == '+' else 'subtracting'}: {v} {'−' if op == '+' else '+'} {k}.", f"{n} {op} {k} = {v}."],
                [W(v + k if op == "+" else v - k, "did the same operation again"), W(v, "copied the answer"), W(n + 1, "changed the ones")],
                FN("blank_eq", eq=eq), qtype="fill-blank", tags={"reasoning"})


@fam("2")
def tt_chain(r, L):
    n = r.randint(200, 700)
    a, b = pick(r, [(100, 10), (10, 100), (100, 100), (10, 10)])
    v = n + a - b
    return Item(f"Start at {n}. Add {a}, then subtract {b}. Where do you end?", v, [f"{n} + {a} = {n + a}.", f"{n + a} − {b} = {v}."],
                [W(n + a + b, "added both numbers"), W(n + a, "did only the first step"), W(n - a + b, "subtracted first and then added")],
                EX(f"{n}+{a}-{b}"), qtype="multi-step", tags={"multistep"})


SKILLS = {
    1: dict(name="Counting within 1,000", fams=[cn_after, cn_seq, cn_chart, cn_between, cn_next3, cn_cross, cn_error]),
    2: dict(name="Skip Counting by 5s, 10s, and 100s", fams=[sk_missing, sk_next3, sk_by, sk_story, sk_line, sk_which, sk_error]),
    3: dict(name="Comparing Three-Digit Numbers", fams=[cp_sym, cp_greater, cp_true, cp_order, cp_story, cp_words, cp_digit, cp_error, cp_greatest, cp_which_place]),
    4: dict(name="Adding and Subtracting 10 and 100", fams=[tt_more, tt_eq, tt_chart, tt_story, tt_which, tt_unknown, tt_chain]),
}
