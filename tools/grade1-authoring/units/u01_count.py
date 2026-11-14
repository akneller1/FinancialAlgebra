"""Unit 1: Counting and Numbers to 120 (count-120). 1.NBT.A.1, 1.OA.C.5."""
from g1lib import *

UNIT_ID = "count-120"


def near(n, hi=120):
    out = [W(n + 1, "counted one object twice"), W(n - 1, "skipped an object"), W(n + 2, "made a counting mistake")]
    if n > 10:
        out += [W(n + 10, "counted a group of ten twice"), W(n - 10, "missed a group of ten")]
    else:
        out += [W(n - 2, "skipped two objects")]
    return out


# ============================================================== S1 Counting Objects
@fam("01")
def co_frames(r, L):
    n = r.randint(4, 10) if L == 0 else r.randint(11, 20)
    alt = f"Ten frame{'s' if n > 10 else ''} with {n} red counters."
    return Item(pick(r, ["How many counters are in the ten frames?", "How many counters do you see?", "Count the counters. How many are there?"]) if n > 10
                else pick(r, ["How many counters are in the ten frame?", "Count the dots in the ten frame. How many?", "How many red counters are there?"]), n,
                ["Count the counters. A full ten frame has 10." if n > 10 else "Touch each counter as you count.", f"There are {n} counters."],
                [w for w in near(n) if 0 < int(w[0]) <= 30], FN("count_n", n=n), qtype="visual",
                diagram=Diagram("tenframe", {"frames": 2 if n > 10 else 1, "a": n}, alt))


@fam("012")
def co_rows(r, L):
    per = 5 if L < 2 else 10
    n = r.randint(3, 10) if L == 0 else r.randint(11, 20) if L == 1 else r.randint(21, 40)
    alt = f"{n} blue counters in rows of {per}."
    return Item(pick(r, ["How many counters are there?", "Count the blue counters. How many are there?", "How many dots are in the picture?"]), n, [f"Count the rows of {per}, then count the rest.", f"There are {n} counters."],
                [w for w in near(n) if 0 < int(w[0]) <= 50], FN("count_n", n=n), qtype="visual",
                diagram=Diagram("crossrow", {"n": n, "per": per, "color": "blue"}, alt))


@fam("12")
def co_blocks(r, L):
    t, o = (r.randint(2, 5), r.randint(0, 9)) if L == 1 else (r.randint(6, 9), r.randint(1, 9))
    n = 10 * t + o
    alt = f"Base-ten blocks: {t} tens rods and {o} ones cubes."
    return Item(pick(r, ["Each rod is 10 cubes. How many cubes are there in all?", "Count the tens and ones. How many cubes are shown?", "How many cubes do the blocks show?"]), n,
                [f"Count the rods by tens: {', '.join(str(10 * k) for k in range(1, t + 1))}.", f"Then count on {o} ones: {n}."],
                [W(t + o, "counted each rod as 1"), W(10 * o + t, "switched the tens and the ones"), W(n + 10, "counted a rod twice"),
                 W(n - 1, "skipped a cube")], FN("count_n", n=n), qtype="visual",
                diagram=Diagram("blocks", {"t": t, "o": o}, alt))


@fam("12")
def co_bags(r, L):
    t = r.randint(2, 6) if L == 1 else r.randint(7, 11)
    o = r.randint(1, 9)
    th = thing(r)
    n = 10 * t + o
    return Item(f"There are {t} bags with 10 {th[1]} in each bag. There are {o} more {th[1]}. How many {th[1]} are there?",
                f"{n} {th[1]}", [f"{t} bags of 10 is {10 * t}.", f"{10 * t} and {o} more is {n} {th[1]}."],
                [W(f"{t + o} {th[1]}", "counted each bag as 1"), W(f"{10 * o + t} {th[1]}", "switched the tens and the ones"),
                 W(f"{n + 10} {th[1]}", "counted one bag twice"), W(f"{n - 1} {th[1]}", "made a counting mistake")],
                EX(f"10*{t}+{o}", unit=th[1]), qtype="word-problem", tags={"modeling"})


@fam("01")
def co_one_more(r, L):
    n = r.randint(3, 9) if L == 0 else r.randint(11, 19)
    k = 1 if L == 0 else pick(r, [1, 2])
    th = thing(r)
    return Item(f"{name(r)} has {n} {th[1]}. {k} more {th[0] if k == 1 else th[1]} {'is' if k == 1 else 'are'} added. How many {th[1]} now?",
                f"{n + k} {th[1]}", [f"Start at {n} and count on {k}.", f"{n} + {k} = {n + k}."],
                [W(f"{n} {th[1]}", "did not add any"), W(f"{n - k} {th[1]}", "counted back instead of on"), W(f"{n + k + 1} {th[1]}", "counted the start number again"),
                 W(f"{n + k - 1} {th[1]}", "counted one too few")], EX(f"{n}+{k}", unit=th[1]), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def co_which_frame(r, L):
    n = r.randint(5, 10) if L == 0 else r.randint(11, 20) if L == 1 else r.randint(12, 20)
    if L < 2:
        alt = f"Ten frame{'s' if n > 10 else ''} with {n} counters."
        it = Item(pick(r, ["Which number tells how many counters?", "Which number matches the counters?"]), n, ["Count each counter once.", f"There are {n}."],
                  [w for w in near(n) if 0 < int(w[0]) <= 30], FN("count_n", n=n), qtype="visual",
                  diagram=Diagram("tenframe", {"frames": 2 if n > 10 else 1, "a": n}, alt))
        return it
    e = 20 - n
    alt = f"Two ten frames with {n} counters and {e} empty boxes."
    return Item("Two ten frames hold 20 in all. How many counters are in these ten frames?", n,
                [f"There are {e} empty boxes.", f"20 − {e} = {n} counters."],
                [W(e, "counted the empty boxes"), W(n + 1, "counted one too many"), W(n - 1, "skipped a counter"), W(20, "said the frames are full")],
                FN("count_n", n=n), qtype="visual", tags={"reasoning"}, diagram=Diagram("tenframe", {"frames": 2, "a": n}, alt))


@fam("2")
def co_groups10(r, L):
    t, o = r.randint(5, 11), r.randint(0, 9)
    n = 10 * t + o
    need(n <= 120 and o != t)
    return Item(f"{name(r)} puts cubes in towers of 10. There are {t} towers and {o} loose cubes. How many cubes are there?",
                f"{n} cubes", [f"{t} towers of 10 is {10 * t}.", f"{10 * t} + {o} = {n} cubes."],
                [W(f"{t + o} cubes", "counted each tower as 1"), W(f"{10 * o + t} cubes", "switched the tens and the ones"),
                 W(f"{n - 10} cubes", "missed a tower"), W(f"{n + 1} cubes", "counted one too many")],
                EX(f"10*{t}+{o}", unit="cubes"), qtype="word-problem", tags={"modeling"})


@fam("0")
def co_color(r, L):
    a, b = r.randint(2, 7), r.randint(2, 7)
    need(a + b <= 10 and a != b)
    want = pick(r, ["red", "yellow"])
    n = a if want == "red" else b
    alt = f"Ten frame with {a} red counters and {b} yellow counters."
    return Item(f"How many {want} counters are in the ten frame?", n, [f"Count only the {want} counters.", f"There are {n} {want} counters."],
                [W(a + b, "counted all the counters"), W(b if want == "red" else a, "counted the other color"), W(n + 1, "counted one twice"),
                 W(10 - a - b, "counted the empty boxes")], FN("count_n", n=n), qtype="visual",
                diagram=Diagram("tenframe", {"frames": 1, "a": a, "b": b}, alt))


# ============================================================== S2 Counting On to 120
def cn_range(r, L):
    return r.randint(2, 28) if L == 0 else r.randint(30, 98) if L == 1 else r.randint(96, 116)


@fam("012")
def cn_next(r, L):
    n = cn_range(r, L)
    if L >= 1:
        need(n % 10 in (7, 8, 9) or r.random() < 0.4)
    seq = f"{n - 2}, {n - 1}, {n}, ___"
    return Item(f"Count on. What number comes next? {seq}", n + 1, [f"After {n} comes {n + 1}.", f"The next number is {n + 1}."],
                [W(n, "repeated the last number"), W(n + 2, "skipped a number"), W(n - 1, "counted back"), W(n + 10, "added ten")]
                + ([W(n // 10 * 10, "went back to the start of the decade")] if n % 10 == 9 else []), FN("neighbor", n=n, way="after"))


@fam("012")
def cn_before(r, L):
    n = cn_range(r, L) + 1
    if L >= 1:
        need(n % 10 in (0, 1) or r.random() < 0.3)
    return Item(pick(r, [f"What number comes just before {n}?", f"Count back. What number is one less than {n}?", f"What number comes right before {n} when you count?"]), n - 1, [f"Count back one from {n}.", f"Just before {n} is {n - 1}."],
                [W(n + 1, "gave the number after"), W(n - 2, "counted back two"), W(n - 10, "counted back ten"), W(n, "repeated the number")],
                FN("neighbor", n=n, way="before"))


@fam("012")
def cn_missing(r, L):
    n = cn_range(r, L) + 1
    seq = f"{n - 1}, ___, {n + 1}, {n + 2}"
    return Item(pick(r, [f"What number is missing? {seq}", f"Fill in the missing number: {seq}"]), n, [f"The number between {n - 1} and {n + 1} is missing.", f"The missing number is {n}."],
                [W(n + 1, "wrote the number after the blank"), W(n - 1, "wrote the number before the blank"), W(n + 10, "added ten"),
                 W(n + 2, "skipped a number")], EX(f"{n - 1}+1"))


@fam("12", mode="sa")
def cn_seq3(r, L):
    n = cn_range(r, L)
    need(L == 1 or n % 10 >= 7)
    ans = f"{n + 1}, {n + 2}, {n + 3}"
    return Item(f"Count on from {n}. Write the next 3 numbers.", ans, [f"Start at {n} and say one more each time.", f"{n}, {ans}."],
                [W(f"{n}, {n + 1}, {n + 2}", "started with the number given"), W(f"{n + 2}, {n + 4}, {n + 6}", "counted by twos"),
                 W(f"{n + 10}, {n + 20}, {n + 30}", "counted by tens")], FN("count_words", start=n + 1, n=3, step=1))


@fam("012")
def cn_chart(r, L):
    row0 = pick(r, [1, 11]) if L == 0 else r.randint(2, 8) * 10 + 1 if L == 1 else pick(r, [91, 101])
    v = row0 + r.randint(0, 19)
    need(v <= 120 and v % 10 != 1)
    alt = f"Part of a number chart from {row0} to {row0 + 19}. One box shows a question mark."
    return Item(pick(r, ["What number is hidden by the question mark?", "Which number belongs in the box with the question mark?"]), v, ["Look at the numbers on each side and above or below.", f"The hidden number is {v}."],
                [W(v + 1, "used the number after"), W(v - 1, "used the number before"), W(v + 10, "used the number below"), W(v - 10, "used the number above")],
                FN("chart_hidden", start=row0, per_row=10, rows=2, hide=[v]), qtype="visual",
                diagram=Diagram("chart", {"start": row0, "per_row": 10, "rows": 2, "hide": [v]}, alt))


@fam("012")
def cn_count_from(r, L):
    n = r.randint(4, 20) if L == 0 else r.randint(20, 90) if L == 1 else r.randint(95, 112)
    k = r.randint(2, 3) if L == 0 else r.randint(3, 5) if L == 1 else r.randint(4, 8)
    need(n + k <= 120)
    return Item(f"{name(r)} starts at {n} and counts on {k} more numbers. What is the last number said?", n + k,
                [f"Count on {k}: " + ", ".join(str(n + i) for i in range(1, k + 1)) + ".", f"The last number is {n + k}."],
                [W(n + k - 1, "counted the start number as one"), W(n + k + 1, "counted one too many"), W(n - k, "counted back"), W(n + 10 * k, "counted by tens")],
                EX(f"{n}+{k}"), qtype="explain")


@fam("2", mode="mc")
def cn_after_100(r, L):
    n = r.randint(99, 118)
    good = str(n + 1)
    bad = [f"100{(n + 1) % 100}" if n + 1 > 100 else "1000", str(n + 10), str(n - 1)]
    bad = [b for b in bad if b != good]
    bad.append("200" if n == 109 else str(n + 2))
    need(len(set(bad)) == len(bad) == 4 or len(set(bad)) >= 3)
    it = mc_key(f"{name(r)} is counting. {n - 1}, {n}, … Which number should come next?", good, list(dict.fromkeys(bad))[:3],
                [f"One more than {n} is {n + 1}.", f"The next number is {n + 1}."], qtype="procedural", r=r)
    it.check = FN("neighbor", n=n, way="after")
    return it


# ============================================================== S3 Reading and Writing Numbers to 120
def rw_n(r, L):
    if L == 0:
        return r.randint(11, 40)
    if L == 1:
        return r.randint(41, 99)
    return r.randint(100, 120)


def num_wrongs(n):
    out = []
    t, o = n // 10 % 10, n % 10
    if n >= 100:
        out += [W(f"100{n % 100}" if n % 100 >= 10 else f"100{n % 100}", "wrote each part as it sounds"), W(f"1{n % 100:02d}0", "added an extra zero"),
                W(str(n - 100 + 10 if n - 100 < 10 else n - 90), "dropped the hundred")]
    else:
        if o and t != o:
            out.append(W(10 * o + t, "switched the tens and the ones"))
        out += [W(f"{t}0{o}" if o else f"{t}00", "wrote each part as it sounds"), W(n + 1, "wrote the next number"), W(n - 10, "wrote the wrong tens")]
    return out


@fam("012")
def rw_word_to_num(r, L):
    n = rw_n(r, L)
    return Item(f"Write the number {words(n)} using digits.", n, [f"{words(n)} has {n // 10} tens and {n % 10} ones." if n < 100 else f"{words(n)} is 100 and {n - 100} more.",
                                                                    f"It is written {n}."],
                num_wrongs(n), FN("num_digits", n=n))


@fam("012", mode="mc")
def rw_num_to_word(r, L):
    n = rw_n(r, L)
    t, o = n // 10 % 10, n % 10
    good = words(n)
    cand = [words(10 * o + t) if o and o != t and 10 * o + t >= 10 and n < 100 else None, words(n + 10) if n + 10 <= 120 else words(n - 20),
            words(n + 1), words(n - 1)]
    bad = [c for c in dict.fromkeys(cand) if c and c != good][:3]
    it = mc_key(f"Which words name the number {n}?", good, bad, [f"{n} is {words(n)}.", f"The words are {good}."], qtype="procedural", r=r)
    it.check = FN("num_word", n=n)
    return it


@fam("012")
def rw_blocks(r, L):
    t = r.randint(1, 3) if L == 0 else r.randint(4, 9) if L == 1 else r.randint(10, 12)
    o = r.randint(0, 9)
    n = 10 * t + o
    need(n <= 120 and (o != t))
    alt = f"Base-ten blocks: {t} tens rods and {o} ones cubes."
    return Item(pick(r, ["Write the number shown by the blocks.", "What number do the tens and ones show?", "How many cubes are shown? Write the number."]), n, [f"{t} tens is {10 * t}." if t < 10 else f"{t} tens is {10 * t} (10 tens is 100).", f"{10 * t} and {o} ones is {n}."],
                [W(t + o, "counted each rod as 1"), W(10 * o + t if o else n + 1, "switched the tens and the ones" if o else "counted one too many"),
                 W(n + 10, "counted a rod twice"), W(n - 1, "skipped a cube")], FN("count_n", n=n), qtype="visual",
                diagram=Diagram("blocks", {"t": t, "o": o}, alt))


@fam("01", mode="mc")
def rw_teen(r, L):
    n = r.randint(13, 19) if L == 0 else r.randint(21, 89)
    need(n % 10 not in (0, n // 10))
    good = str(n)
    bad = [str(10 * (n % 10) + n // 10), f"{n // 10}0{n % 10}", str(n % 10) if L == 0 else str(n + 10)]
    it = mc_key(f"Which is the number {words(n)}?", good, bad, [f"{words(n)} has {n // 10} ten{'s' if n >= 20 else ''} and {n % 10} ones.", f"It is {n}."], qtype="procedural", r=r)
    it.check = FN("num_digits", n=n)
    return it


@fam("12")
def rw_count_write(r, L):
    n = r.randint(21, 60) if L == 1 else r.randint(101, 119)
    th = thing(r)
    t = n // 10
    o = n % 10
    need(o > 0)
    return Item(f"{name(r)} counts {th[1]}: {t} groups of 10 and {o} more. Write the number of {th[1]}.", f"{n} {th[1]}",
                [f"{t} groups of 10 is {10 * t}.", f"{10 * t} and {o} more is {n} {th[1]}."],
                [W(f"{t + o} {th[1]}", "counted each group as 1"), W(f"{10 * o + t} {th[1]}", "switched the tens and the ones"),
                 W(f"{n + 10} {th[1]}", "counted a group twice"), W(f"{n - 1} {th[1]}", "made a counting mistake")],
                EX(f"10*{t}+{o}", unit=th[1]), qtype="word-problem", tags={"modeling"})


@fam("2", mode="mc")
def rw_which_written(r, L):
    n = r.randint(101, 119)
    need(n % 100 >= 1)
    W_ = words(n)[0].upper() + words(n)[1:]
    good = f"{W_} is written {n}."
    bad = [f"{W_} is written 100{n % 100}.", f"{W_} is written {n % 100}.", f"{W_} is written {n + 10}."]
    it = mc_key("Which sentence is correct?", good, bad, [f"{words(n)} is 100 and {n - 100} more.", f"It is written {n}."], qtype="conceptual", r=r)
    return it


@fam("0")
def rw_word_small(r, L):
    n = r.randint(6, 20)
    return Item(f"Write the number {words(n)} using digits.", n, [f"Count to {words(n)}.", f"{words(n)} is {n}."],
                [W(n + 1, "wrote the next number"), W(n - 1, "wrote the number before"), W(10 * (n % 10) + n // 10 if n > 10 and n % 10 else n + 10, "switched the digits" if n > 10 and n % 10 else "added ten")],
                FN("num_digits", n=n))


# ============================================================== S4 Counting On and Back to Add and Subtract
def ob_nums(r, L):
    if L == 0:
        return r.randint(3, 9), r.randint(1, 2)
    if L == 1:
        return r.randint(8, 17), r.randint(1, 3)
    return r.randint(25, 116), r.randint(2, 4)


@fam("012")
def ob_add(r, L):
    a, k = ob_nums(r, L)
    need(a + k <= 120)
    return Item(f"Count on to add. {a} + {k} = ___", a + k, [f"Start at {a}. Count on {k}: " + ", ".join(str(a + i) for i in range(1, k + 1)) + ".", f"{a} + {k} = {a + k}."],
                [W(a + k - 1, "counted the start number as a jump"), W(a + k + 1, "counted one too many"), W(a - k, "counted back"), W(a, "did not count on")],
                FN("blank_eq", eq=f"{a} + {k} = ___"), claim=f"{a} + {k}")


@fam("012")
def ob_sub(r, L):
    a, k = ob_nums(r, L)
    a += 2
    return Item(f"Count back to subtract. {a} − {k} = ___", a - k, [f"Start at {a}. Count back {k}: " + ", ".join(str(a - i) for i in range(1, k + 1)) + ".", f"{a} − {k} = {a - k}."],
                [W(a - k + 1, "counted the start number as a jump"), W(a - k - 1, "counted back one too many"), W(a + k, "counted on instead of back"), W(a, "did not count back")],
                FN("blank_eq", eq=f"{a} − {k} = ___"), claim=f"{a} − {k}")


@fam("01")
def ob_line(r, L):
    a, k = ob_nums(r, L)
    up = r.random() < 0.5
    lo = 0 if L == 0 else 5
    hi = lo + 15 if L == 0 else lo + 20
    b = a + k if up else a - k
    need(lo <= min(a, b) and max(a, b) <= hi)
    alt = f"Number line from {lo} to {hi}. A point is marked at {a}."
    return Item(f"Start at {a} on the number line. Count {'on' if up else 'back'} {k}. Where do you land?", b,
                [f"Make {k} jump{'s' if k > 1 else ''} {'to the right' if up else 'to the left'} from {a}.", f"You land on {b}."],
                [W(a - k if up else a + k, "jumped the wrong way"), W(b + (1 if up else -1), "counted one too many"), W(b - (1 if up else -1), "counted the start as a jump"), W(a, "did not jump")],
                EX(f"{a}{'+' if up else '−'}{k}"), qtype="visual",
                diagram=Diagram("jline", {"lo": lo, "hi": hi, "points": [{"v": a, "label": "Start"}]}, alt))


@fam("012", mode="mc")
def ob_says(r, L):
    a, k = ob_nums(r, L)
    k = max(k, 2)
    up = r.random() < 0.6
    seq = [a + i if up else a - i for i in range(1, k + 1)]
    good = ", ".join(map(str, seq))
    bad = [", ".join(str(a + (i if up else -i)) for i in range(0, k)), ", ".join(str(a - i if up else a + i) for i in range(1, k + 1)),
           ", ".join(str(a + (2 * i if up else -2 * i)) for i in range(1, k + 1))]
    op = "+" if up else "−"
    nm = name(r)
    it = mc_key(f"To find {a} {op} {k}, {nm} counts {'on' if up else 'back'} from {a}. Which numbers does {nm} say?",
                good, bad, [f"Start at {a} and say {k} numbers {'forward' if up else 'backward'}.", f"The numbers are {good}."], qtype="explain", tags={"reasoning"}, r=r)
    it.check = FN("count_words", start=seq[0], n=k, step=1 if up else -1)
    return it


@fam("012")
def ob_story(r, L):
    a, k = ob_nums(r, L)
    th = thing(r)
    nm = name(r)
    up = r.random() < 0.5
    if up:
        p = f"{nm} has {a} {th[1]}. {nm} gets {k} more. Count on. How many {th[1]} does {nm} have now?"
        b = a + k
    else:
        a += 2
        p = f"{nm} has {a} {th[1]}. {nm} gives away {k}. Count back. How many {th[1]} are left?"
        b = a - k
    return Item(p, f"{b} {th[1]}", [f"Start at {a} and count {'on' if up else 'back'} {k}.", f"{a} {'+' if up else '−'} {k} = {b} {th[1]}."],
                [W(f"{a - k if up else a + k} {th[1]}", "counted the wrong way"), W(f"{b + (1 if up else -1)} {th[1]}", "counted one too many"),
                 W(f"{b - (1 if up else -1)} {th[1]}", "counted the start number as a jump"), W(f"{a} {th[1]}", "did not count")],
                EX(f"{a}{'+' if up else '−'}{k}", unit=th[1]), qtype="word-problem", tags={"modeling"})


@fam("2")
def ob_how_many_jumps(r, L):
    a, k = ob_nums(r, L)
    b = a + k
    need(b <= 120)
    nm = name(r)
    return Item(f"{nm} counts on from {a} and stops at {b}. How many numbers did {nm} count on?", k,
                [f"Count from {a}: " + ", ".join(str(a + i) for i in range(1, k + 1)) + ".", f"That is {k} numbers, so {a} + {k} = {b}."],
                [W(k + 1, "counted the start number too"), W(b, "gave the stopping number"), W(k - 1, "counted one too few"), W(a + b, "added the two numbers")],
                FN("blank_eq", eq=f"{a} + ___ = {b}"), qtype="explain", tags={"reasoning"})


SKILLS = {
    1: dict(name="Counting Objects", fams=[co_frames, co_rows, co_blocks, co_bags, co_one_more, co_which_frame, co_groups10, co_color]),
    2: dict(name="Counting On to 120", fams=[cn_next, cn_before, cn_missing, cn_seq3, cn_chart, cn_count_from, cn_after_100]),
    3: dict(name="Reading and Writing Numbers to 120", fams=[rw_word_to_num, rw_num_to_word, rw_blocks, rw_teen, rw_count_write, rw_which_written, rw_word_small]),
    4: dict(name="Counting On and Back to Add and Subtract", fams=[ob_add, ob_sub, ob_line, ob_says, ob_story, ob_how_many_jumps]),
}
