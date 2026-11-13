"""Grade 1 question families.

Every family is a function f(r, L) -> Item where r is a seeded random.Random and L is the
level (0 = Remedial, 1 = Standard, 2 = Advanced).  Each item carries a check that the
independent verifier re-derives from the stored inputs; the family never stores its own
answer as the check.

Design rules for Grade 1:
  * numbers stay inside the source outline's Grade 1 ranges (facts to 10 / within 20,
    two-digit numbers to 99, sums within 100, lengths within 120);
  * prompts are short sentences with a small reading load, and every abstract question has a
    concrete picture, object, or story where the skill allows it;
  * wrong answers are real Grade 1 misconceptions (counting the wrong group, off by one,
    adding instead of subtracting, ignoring a regroup, naming a shape by its look).
"""
import random
from g1lib import Item, Diagram, Reject, need, pick, name, sub, FN, EX, fam, _norm, W

# ------------------------------------------------------------------ vocabulary pools
OBJECTS = [("apple", "apples"), ("star", "stars"), ("block", "blocks"), ("sticker", "stickers"),
           ("flower", "flowers"), ("ball", "balls"), ("crayon", "crayons"), ("book", "books"),
           ("shell", "shells"), ("car", "cars"), ("cookie", "cookies"), ("pencil", "pencils"),
           ("fish", "fish"), ("bug", "bugs"), ("leaf", "leaves"), ("marble", "marbles"),
           ("kite", "kites"), ("hat", "hats"), ("seed", "seeds"), ("button", "buttons")]
COLORS = ["blue", "orange", "green", "purple", "teal"]
SHAPE_WORDS = ["circle", "triangle", "square", "rectangle", "hexagon"]
SOLIDS = ["cube", "cylinder", "sphere", "cone"]
CATEGORIES = [("red", "blue"), ("cats", "dogs"), ("cars", "trucks"), ("apples", "pears"),
              ("circles", "squares"), ("big", "small")]

SIDES = {"triangle": 3, "square": 4, "rectangle": 4, "hexagon": 6, "circle": 0}
CORNERS = {"triangle": 3, "square": 4, "rectangle": 4, "hexagon": 6, "circle": 0}


def obj(r, plural=None):
    o = pick(r, OBJECTS)
    return o[1] if plural is not False else o[0]


def num(n):
    return str(int(n))


def tw(n, word):
    return f"{n} {word}" if int(n) == 1 else f"{n} {word}s"


def a_an(word):
    return ("an " if word[:1].lower() in "aeiou" else "a ") + word


def ntext(n, singular, plural=None):
    return f"{int(n)} {singular if int(n) == 1 else (plural or singular + 's')}"


# ------------------------------------------------------------------ answer text helpers
def parts_text(n):
    n = int(n)
    return f"1 ten and {n - 10} ones"


def list_text(vals):
    return ", ".join(str(int(v)) for v in vals)


def clock_text(h, m):
    return f"{int(h)}:{int(m):02d}"


def wrong_numbers(correct, cands, why="used the wrong number"):
    """(text, reason) pairs, distinct from the key, at most 6."""
    out, seen = [], {_norm(num(correct))}
    for c in cands:
        t = num(c)
        if t in seen:
            continue
        seen.add(t)
        out.append((t, why if not isinstance(c, tuple) else c[1]))
    return out


# ------------------------------------------------------------------ generic arithmetic
def add_items(lo=0, hi=10, *, diagram=None, story=False, ctx="sum", sums_to=None):
    """a + b with optional objects/number line."""
    def f(r, L):
        top = hi if L else max(5, hi // 2)
        a = r.randint(lo, max(lo, top - 1))
        b = r.randint(lo, max(lo, top - a)) if sums_to else r.randint(lo, max(lo, top - 1))
        a, b = max(a, 0), max(b, 0)
        need(a + b > 0)
        thing = obj(r)
        nm = name(r)
        style = r.randrange(4)
        if story and style == 0:
            prompt = f"{nm} has {a} {thing}. {nm} gets {b} more. How many {thing} does {nm} have now?"
        elif story and style == 1:
            prompt = f"There are {a} {thing} on the table. {name(r)} puts {b} more on the table. How many {thing} are there in all?"
        elif ctx == "counters" and style == 2:
            prompt = f"How many dots are there in all?\n{a} dots and {b} dots"
        else:
            prompt = f"{a} + {b} = ?"
        dg = None
        if diagram == "tenframe":
            dg = Diagram("tenframe", {"filled": [min(a, 10), min(b, 10)], "caption": f"{a} + {b}"},
                         f"Two ten-frames: one with {min(a, 10)} counters and one with {min(b, 10)} counters.")
        elif diagram == "counters" or (diagram and style % 2 == 0):
            dg = Diagram("counters", {"groups": [{"count": a, "color": "blue"}, {"count": b, "color": "orange"}],
                                      "caption": f"{a} and {b}"}, f"Two groups of counters: {a} blue counters and {b} orange counters.")
        elif diagram == "numberline":
            dg = Diagram("numberline", {"min": 0, "max": max(10, a + b), "jumps": [[a, a + b, 0, f"+{b}"]]},
                         f"A number line from 0 to {max(10, a + b)} with a jump of {b} starting at {a}.")
        return Item(prompt, num(a + b), [f"Start with {a} and add {b}.", f"{a} + {b} = {a + b}."],
                    wrong_numbers(a + b, [a - b, a + b + 1, a + b - 1, a * b if a * b != a + b else a + b + 2, abs(a - b)],
                                  "added or counted incorrectly"),
                    check=FN("add", a=a, b=b), qtype="procedural", tags=("fluency",), diagram=dg)
    return f


def sub_items(lo=0, hi=10, *, diagram=None, story=False, ctx="difference"):
    def f(r, L):
        top = hi if L else max(5, hi // 2)
        a = r.randint(1, top)
        b = r.randint(0, a)
        need(a - b >= 0)
        thing = obj(r)
        nm = name(r)
        style = r.randrange(4)
        if story and style == 0:
            prompt = f"{nm} has {a} {thing}. {nm} gives away {b}. How many {thing} does {nm} have left?"
        elif story and style == 1:
            prompt = f"There are {a} {thing}. {b} of them are used. How many {thing} are left?"
        elif ctx == "take away":
            prompt = f"Start with {a}. Take away {b}. How many are left?"
        else:
            prompt = f"{a} − {b} = ?"
        dg = None
        if diagram == "counters":
            dg = Diagram("counters", {"groups": [{"count": a, "color": "blue"}], "caption": f"Start with {a}"},
                         f"{a} counters in one group.")
        elif diagram == "numberline":
            dg = Diagram("numberline", {"min": 0, "max": max(10, a), "jumps": [[a - b, a, 0, f"−{b}"]]},
                         f"A number line from 0 to {max(10, a)} with a jump back of {b} from {a}.")
        return Item(prompt, num(a - b), [f"Start with {a}.", f"Take away {b}: {a} − {b} = {a - b}."],
                    wrong_numbers(a - b, [a + b, a - b + 1, a - b - 1, b - a if b > a else a - b + 2, a],
                                  "added instead of subtracted, or miscounted"),
                    check=FN("sub", a=a, b=b), qtype="procedural", tags=("fluency",), diagram=dg)
    return f


def add1_items(*, back=False):
    """Add or subtract 1 or 2 (count on / count back)."""
    def f(r, L):
        top = 20 if L else 10
        a = r.randint(1, top)
        k = r.choice([1, 2])
        if back:
            a = max(a, k + 1)
            ans = a - k
            prompt = f"Count back {k} from {a}. What number do you land on?"
            chk = FN("sub", a=a, b=k)
            dg = Diagram("numberline", {"min": 0, "max": max(20, a), "jumps": [[ans, a, 0, f"−{k}"]]},
                         f"A number line from 0 to {max(20, a)} with an arrow jumping back {k} from {a}.")
        else:
            ans = a + k
            prompt = f"Count on {k} from {a}. What number do you land on?"
            chk = FN("add", a=a, b=k)
            dg = Diagram("numberline", {"min": 0, "max": max(20, ans), "jumps": [[a, ans, 0, f"+{k}"]]},
                         f"A number line from 0 to {max(20, ans)} with an arrow jumping forward {k} from {a}.")
        return Item(prompt, num(ans), [f"Start at {a}.", f"{'Count back' if back else 'Count on'} {k} to reach {ans}."],
                    wrong_numbers(ans, [a, ans + 1, ans - 1, a + k + 1 if not back else a - k - 1]),
                    check=chk, qtype="procedural", tags=("count-on",), diagram=dg)
    return f


def missing_addend_items(hi=10):
    def f(r, L):
        top = hi if L else max(6, hi // 2)
        total = r.randint(2, top)
        known = r.randint(1, total - 1)
        unknown = total - known
        thing = obj(r)
        style = r.randrange(3)
        if style == 0:
            prompt = f"{known} + ? = {total}\nWhat number goes in the box?"
        elif style == 1:
            prompt = f"{name(r)} has {known} {thing} and needs {total} {thing} in all. How many more {thing} are needed?"
        else:
            prompt = f"There are {total} {thing} in all. {known} are in a bag. How many {thing} are not in the bag?"
        return Item(prompt, num(unknown), [f"The total is {total} and one part is {known}.", f"{total} − {known} = {unknown}."],
                    wrong_numbers(unknown, [total + known, unknown + 1, total, known], "used the wrong part or the total"),
                    check=FN("missing_part", total=total, part=known), qtype="procedural", tags=("unknown",),
                    diagram=(Diagram("tenframe", {"filled": [known], "caption": f"{known} of the {total}"},
                                     f"A ten-frame with {known} counters filled.")
                             if style == 2 and total <= 10 else None))
    return f


def three_addend_items(hi=20):
    def f(r, L):
        top = 8 if L else 5
        a, b, c = (r.randint(1, top) for _ in range(3))
        need(a + b + c <= hi)
        nm = name(r)
        thing = obj(r)
        prompt = r.choice([
            f"{nm} sees {a} {thing}, then {b} more, then {c} more. How many {thing} in all?",
            f"{a} + {b} + {c} = ?",
            f"There are {a} birds on a wire, {b} on a fence, and {c} on a tree. How many birds in all?",
        ])
        return Item(prompt, num(a + b + c), [f"Add two numbers first: {a} + {b} = {a + b}.", f"Then add the third: {a + b} + {c} = {a + b + c}."],
                    wrong_numbers(a + b + c, [a + b, a + b + c + 1, a + b + c - 1, max(a, b, c) + a]),
                    check=FN("add3", a=a, b=b, c=c), qtype="procedural", tags=("multistep",), diagram=None)
    return f


def fact_family_items(hi=10, limit=None):
    """Related addition/subtraction facts (1.OA.B.3, 1.OA.C.6)."""
    def f(r, L):
        top = hi if L else max(6, hi // 2)
        a, b = r.randint(1, top - 1), r.randint(1, top - 1)
        s = a + b
        need(s <= (int(limit) if limit else top))
        style = r.randrange(3)
        if style == 0:
            prompt = f"If {a} + {b} = {s}, what is {s} − {b}?"
            ans, chk = a, FN("sub", a=s, b=b)
        elif style == 1:
            prompt = f"If {s} − {b} = {a}, what is {a} + {b}?"
            ans, chk = s, FN("add", a=a, b=b)
        else:
            prompt = f"Which fact belongs to the same fact family as {a} + {b} = {s}?"
            ans, chk = f"{s} − {b} = {a}", FN("related", a=a, b=b)
        return Item(prompt, num(ans) if not isinstance(ans, str) else ans,
                    [f"A fact family uses the same three numbers: {a}, {b}, and {s}.", f"{a} + {b} = {s}, so {s} − {b} = {a}."],
                    wrong_numbers(a, [s, b, s + b, a + b + s]) if not isinstance(ans, str) else
                    [(f"{a} + {b} = {b}", "used the wrong sum"), (f"{s} + {b} = {a}", "added instead of subtracting"),
                     (f"{a} − {b} = {s}", "subtracted the smaller from the larger")],
                    check=chk, qtype="conceptual", tags=("connections",))
    return f


def make_ten_items():
    """Make-ten strategy for sums within 20 (1.OA.C.6)."""
    def f(r, L):
        a = r.randint(6, 9) if not L else r.randint(7, 9)
        b = r.randint(3, 9)
        need(a + b > 10 and a + b <= 18)
        need_to = 10 - a
        ans = a + b
        prompt = r.choice([
            f"Make a ten to add. {a} + {b} = ?",
            f"Use a ten-frame to add {a} + {b}.",
            f"{a} + {b} = ?\nMake ten first.",
        ])
        dg = Diagram("tenframe", {"filled": [a, b], "caption": f"{a} + {b}"},
                     f"Two ten-frames: one shows {a} counters and one shows {b} counters.")
        return Item(prompt, num(ans),
                    [f"{a} needs {10 - a} more to make 10.", f"Break {b} into {10 - a} and {b - (10 - a)}.",
                     f"10 + {b - (10 - a)} = {ans}."],
                    wrong_numbers(ans, [a + b + 1, a + b - 1, a - b + 10, 10 + b]),
                    check=FN("add", a=a, b=b), qtype="procedural", tags=("make-ten",), diagram=dg)
    return f


def teen_items():
    """Teen numbers as one ten and extra ones (1.NBT.B.2.b)."""
    def f(r, L):
        n = r.randint(11, 19)
        style = r.randrange(3)
        if style == 0:
            prompt = f"How many tens and ones are in {n}?"
            ans = parts_text(n)
            chk = FN("teen_parts", n=n)
            dg = Diagram("baseten", {"tens": 1, "ones": n - 10}, f"One ten rod and {n - 10} one cubes, showing {n}.")
        elif style == 1:
            prompt = f"A ten-frame is full and {n - 10} more counters are outside it. What number is shown?"
            ans, chk = num(n), FN("add", a=10, b=n - 10)
            dg = Diagram("tenframe", {"filled": [10], "caption": f"10 and {n - 10} more"}, f"A full ten-frame with {n - 10} counters beside it.")
        else:
            prompt = f"10 + {n - 10} = ?"
            ans, chk = num(n), FN("add", a=10, b=n - 10)
            dg = None
        return Item(prompt, ans, [f"{n} is 10 and {n - 10} more.", f"10 + {n - 10} = {n}."],
                    [(parts_text(n + 1), "made a ten and one too many ones"), (parts_text(n - 1), "counted one fewer one"),
                     (f"{n - 10} tens and 1 one", "swapped the tens and ones")] if style == 0 else
                    wrong_numbers(n, [n + 1, n - 1, 10 + n, n - 10]),
                    check=chk, qtype="conceptual", tags=("place-value",), diagram=dg)
    return f


def make_ten_fill_items():
    """Fill unknowns in equations involving 10 (1.OA.D.8)."""
    def f(r, L):
        style = r.randrange(3)
        if style == 0:
            a = r.randint(1, 9)
            prompt = f"{a} + ? = 10\nWhat number goes in the box?"
            ans, chk = num(10 - a), FN("missing_part", total=10, part=a)
        elif style == 1:
            a = r.randint(1, 9)
            prompt = f"10 − ? = {a}\nWhat number goes in the box?"
            ans, chk = num(10 - a), FN("missing_part", total=10, part=a)
        else:
            a = r.randint(1, 9)
            prompt = f"? + {a} = 10\nWhat number goes in the box?"
            ans, chk = num(10 - a), FN("missing_part", total=10, part=a)
        return Item(prompt, ans, [f"Together the two parts make 10.", f"10 − {a} = {10 - a}."],
                    wrong_numbers(10 - a, [10 + a, 10 - a + 1, a, 10]),
                    check=chk, qtype="procedural", tags=("unknown",),
                    diagram=Diagram("tenframe", {"filled": [a], "caption": f"{a} and how many more make 10?"},
                                    f"A ten-frame with {a} counters and the rest empty."))
    return f


def subtract_teen_items():
    """Subtract from teen numbers with ten-frames (1.OA.C.6)."""
    def f(r, L):
        n = r.randint(11, 18)
        b = r.randint(1, min(9, n - 10))
        ans = n - b
        prompt = r.choice([f"{n} − {b} = ?", f"Start with {n} and take away {b}. How many are left?"])
        dg = Diagram("tenframe", {"filled": [10, n - 10], "caption": f"{n} take away {b}"},
                     f"A full ten-frame and {n - 10} more counters, showing {n}.")
        return Item(prompt, num(ans), [f"{n} is 10 and {n - 10}.", f"Take {b} from the {n - 10} ones: {n - 10} − {b} = {n - 10 - b}.",
                                      f"10 + {n - 10 - b} = {ans}."],
                    wrong_numbers(ans, [n + b, ans - 1, ans + 1, 10 - b]),
                    check=FN("sub", a=n, b=b), qtype="procedural", tags=("make-ten",), diagram=dg)
    return f


def count_on_difference_items():
    """Count on / make ten to find a difference (1.OA.C.6)."""
    def f(r, L):
        b = r.randint(2, 9)
        ans = r.randint(1, 9)
        a = b + ans
        need(a <= 20)
        prompt = r.choice([f"{a} − {b} = ?", f"How many more is {a} than {b}?"])
        return Item(prompt, num(ans), [f"Count on from {b} to {a}.", f"{b} + {ans} = {a}, so {a} − {b} = {ans}."],
                    wrong_numbers(ans, [a + b, ans + 1, b - ans if b > ans else ans + 2, a]),
                    check=FN("sub", a=a, b=b), qtype="procedural", tags=("reasoning",),
                    diagram=Diagram("numberline", {"min": 0, "max": max(20, a), "jumps": [[b, a, 0, f"+{ans}"]]},
                                    f"A number line from 0 to {max(20, a)} with a jump from {b} to {a}."))
    return f


# ------------------------------------------------------------------ comparing and ordering
def compare_groups_items(kind="which"):
    def f(r, L):
        top = 10 if L else 6
        a = r.randint(1, top)
        b = r.randint(1, top)
        need(a != b)
        thing = obj(r)
        if kind == "more":
            ans = num(max(a, b) - min(a, b))
            prompt = f"How many more {thing} are in the group with more?"
            chk = FN("more_count", a=a, b=b)
        elif kind == "fewer":
            ans = num(max(a, b) - min(a, b))
            prompt = f"How many fewer are in the group with fewer?"
            chk = FN("more_count", a=a, b=b)
        else:
            ans = "left" if a > b else "right"
            prompt = f"Which group has more {thing}?"
            chk = FN("which_group", a=a, b=b)
        dg = Diagram("comparegroups", {"left": {"count": a, "label": f"Group A", "color": "blue"},
                                      "right": {"count": b, "label": f"Group B", "color": "orange"}},
                     f"Group A has {a} counters. Group B has {b} counters.")
        return Item(prompt, ans, [f"Group A has {a}. Group B has {b}.", f"{max(a, b)} is more than {min(a, b)}; the difference is {max(a, b) - min(a, b)}."],
                    wrong_numbers(max(a, b) - min(a, b), [a + b, max(a, b), min(a, b), abs(a - b) + 1])
                    if kind != "which" else [("right" if a > b else "left", "chose the group with fewer")],
                    check=chk, qtype="conceptual", tags=("compare",), diagram=dg)
    return f


def compare_numbers_items(hi=99, symbol=False):
    def f(r, L):
        top = hi if L else max(20, hi // 3)
        a = r.randint(10, top)
        b = r.randint(10, top)
        need(a != b)
        if symbol:
            ans = ">" if a > b else "<"
            prompt = f"Which sign makes this true?\n{a} ? {b}"
            chk = FN("symbol", a=a, b=b)
            wrong = [("<", "put the smaller number first"), (">", "put the larger number first"), ("=", "said the numbers are equal")]
            wrong = [w for w in wrong if w[0] != ans]
        else:
            prompt = r.choice([f"Which number is greater, {a} or {b}?", f"Which number is less, {a} or {b}?"])
            less = "less" in prompt
            want = min(a, b) if less else max(a, b)
            ans = num(want)
            chk = FN("which_number", a=a, b=b, which="less" if less else "greater")
            other = max(a, b) if less else min(a, b)
            wrong = wrong_numbers(want, [other, abs(a - b), a + b])
        return Item(prompt, ans, [f"Compare the tens first, then the ones.", f"{max(a, b)} is greater than {min(a, b)}."],
                    wrong, check=chk, qtype="conceptual", tags=("place-value", "compare"),
                    diagram=Diagram("numbercards", {"cards": [num(a), "?" if symbol else num(b)], "caption": "Compare the numbers"},
                                    f"Two number cards: {a} and {b}.") if symbol else None)
    return f


def order_numbers_items(hi=99, n=3):
    def f(r, L):
        top = hi if L else max(20, hi // 3)
        vals = r.sample(range(11, top + 1), n)
        asc = r.random() < 0.5
        ans = list_text(sorted(vals) if asc else sorted(vals, reverse=True))
        prompt = ("Put these numbers in order from least to greatest.\n" if asc else "Put these numbers in order from greatest to least.\n") + ", ".join(num(v) for v in vals)
        return Item(prompt, ans, [f"Line up the tens, then the ones.", f"The order is {ans}."],
                    [(list_text(sorted(vals, reverse=asc)), "ordered the other way"),
                     (list_text(sorted(vals)[::-1] if asc else sorted(vals)), "ordered the other way")],
                    check=FN("sorted", values=vals, direction="asc" if asc else "desc"), qtype="procedural",
                    tags=("place-value", "order"))
    return f


# ------------------------------------------------------------------ counting and place value
def count_items(hi=20, by=1):
    def f(r, L):
        top = hi if L else max(10, hi // 2)
        n = r.randrange(max(1, top // 2), top + 1, max(by, 1))
        thing = obj(r)
        if by == 1:
            prompt = r.choice([f"How many {thing} are there?", f"Count the {thing}. How many are there?"])
        else:
            prompt = f"Count by {by}s. How many {thing} are there?"
        dg = Diagram("counters", {"groups": [{"count": n, "color": "blue"}], "caption": f"Count the {thing}"},
                     f"{n} {thing} arranged in rows.")
        return Item(prompt, num(n), [f"Count each {thing[0:-1] if by == 1 else 'group'}.", f"There are {n} {thing}."],
                    wrong_numbers(n, [n + 1, n - 1, n + by, n - by]),
                    check=FN("count", n=n), qtype="visual", tags=("counting",), diagram=dg)
    return f


def count_by_items(step=10, hi=120):
    def f(r, L):
        start = 0 if r.random() < 0.5 else step
        k = r.randint(1, (hi - start) // step)
        ans = start + k * step
        prompt = r.choice([f"Count by {step}s. What number comes after {ans - step}?",
                           f"Keep counting by {step}s: {max(ans - step * 2, 0)}, {ans - step}, ___"])
        return Item(prompt, num(ans), [f"Add {step} each time.", f"{ans - step} + {step} = {ans}."],
                    wrong_numbers(ans, [ans + 1, ans - 1, ans + step, ans - step]),
                    check=FN("add", a=ans - step, b=step), qtype="procedural", tags=("counting",),
                    diagram=Diagram("numberline", {"min": 0, "max": max(hi, ans), "step": step, "marks": [ans]},
                                    f"A number line counting by {step}s with {ans} marked."))
    return f


def base_ten_items(kind="value"):
    def f(r, L):
        top = 99 if L else 49
        tens = r.randint(1, min(9, top // 10))
        ones = r.randint(0, 9)
        n = tens * 10 + ones
        if kind == "build":
            ones = r.randint(1, 9)
            n = tens * 10 + ones
            prompt = f"How many ones are needed to build {n} with {tens} tens?"
            ans, chk = num(ones), FN("ones_of", n=n, tens=tens)
            wrong = wrong_numbers(ones, [tens, n, ones + 1])
        elif kind == "regroup":
            prompt = f"How many ones are in 1 ten?"
            ans, chk = "10", FN("ten_ones", tens=1)
            wrong = wrong_numbers(10, [1, 100, 11])
            tens, ones = 1, 0
        else:
            prompt = r.choice([f"What number do the blocks show?", f"How many is {tens} tens and {ones} ones?"])
            ans, chk = num(n), FN("tens_ones", tens=tens, ones=ones)
            wrong = wrong_numbers(n, [ones * 10 + tens, tens + ones, n + 10, n - 10])
        return Item(prompt, ans, [f"{tens} tens is {tens * 10}.", f"{tens * 10} + {ones} = {n}."],
                    wrong, check=chk, qtype="visual", tags=("place-value",),
                    diagram=Diagram("baseten", {"tens": tens, "ones": ones, "caption": ""},
                                    f"{tens} tens rods and {ones} ones cubes."))
    return f


def digit_value_items():
    def f(r, L):
        tens = r.randint(1, 9)
        ones = r.randint(1, 9)
        while ones == tens:            # "the digit 3 in 33" would be ambiguous
            ones = r.randint(1, 9)
        n = tens * 10 + ones
        which = r.choice(["tens", "ones"])
        ans = num(tens * 10 if which == "tens" else ones)
        prompt = f"What is the value of the digit {tens if which == 'tens' else ones} in {n}?"
        chk = FN("digit_value", n=n, which=which)
        return Item(prompt, ans, [f"The digits of {n} are {tens} tens and {ones} ones.", f"The {which} digit is worth {ans}."],
                    wrong_numbers(tens * 10 if which == "tens" else ones,
                                  [ones if which == "tens" else tens * 10, n, tens * 10 + ones]),
                    check=chk, qtype="conceptual", tags=("place-value",),
                    diagram=Diagram("placevalue", {"tens": tens, "ones": ones, "caption": f"The number {n}"},
                                    f"A place value chart showing {tens} tens and {ones} ones for the number {n}."))
    return f


def tens_ones_equiv_items():
    """Equivalent tens-and-ones decompositions (1.NBT.B.2.a)."""
    def f(r, L):
        tens = r.randint(1, 6)
        ones = r.randint(1, 8)
        n = tens * 10 + ones
        alt_tens, alt_ones = tens - 1, ones + 10
        ans = num(alt_ones)
        prompt = (f"{n} is {tw(tens, 'ten')} and {tw(ones, 'one')}. "
                  f"It is also {tw(alt_tens, 'ten')} and how many ones?")
        return Item(prompt, ans, [f"Trade one ten for 10 ones.", f"{ones} + 10 = {alt_ones}, so {n} is {alt_tens} tens and {alt_ones} ones."],
                    wrong_numbers(alt_ones, [ones, ones + 1, alt_tens * 10 + ones]),
                    check=FN("equiv_ones", n=n, tens=alt_tens), qtype="conceptual", tags=("place-value", "reasoning"),
                    diagram=Diagram("baseten", {"tens": tens, "ones": ones, "caption": f"Show {n} a new way"},
                                    f"{tens} tens rods and {ones} ones cubes showing {n}."))
    return f


def add_multiple_of_ten_items():
    def f(r, L):
        tens = r.randint(1, 8)
        ones = r.randint(0, 9)
        k = r.randint(1, 4)
        n = tens * 10 + ones
        add = r.random() < 0.5
        if add:
            ans = n + k * 10
            prompt = f"{n} + {k * 10} = ?"
            chk = FN("add", a=n, b=k * 10)
        else:
            n = max(n, k * 10 + ones)
            ans = n - k * 10
            prompt = f"{n} − {k * 10} = ?"
            chk = FN("sub", a=n, b=k * 10)
        need(ans >= 0)
        return Item(prompt, num(ans), [f"Add or subtract the tens: {tens} tens {'+' if add else '−'} {k} tens.",
                                       f"The ones digit stays {ones}."],
                    wrong_numbers(ans, [ans + 10, ans - 10, ans + 1, ans - 1 if ans > 0 else ans + 2]),
                    check=chk, qtype="procedural", tags=("place-value",),
                    diagram=Diagram("placevalue", {"tens": max(ans // 10, 0), "ones": ans % 10, "caption": ""},
                                    f"A place value chart for {ans}."))
    return f


def add_two_digit_items(compose=False, hi=100):
    def f(r, L):
        a_t = r.randint(1, 4)
        a_o = r.randint(1, 7)
        b_t = r.randint(1, 3)
        b_o = r.randint(1, 9 if compose else max(1, 9 - a_o))
        a, b = a_t * 10 + a_o, b_t * 10 + b_o
        if compose:
            need(a_o + b_o >= 10)
        need(a + b <= hi)
        prompt = r.choice([f"{a} + {b} = ?", f"Add {a} and {b}.", f"{name(r)} has {a} stickers and gets {b} more. How many stickers in all?"])
        dg = Diagram("baseten", {"tens": (a + b) // 10, "ones": (a + b) % 10, "caption": f"{a} + {b}"},
                     f"Base-ten blocks for {a} and {b} combined, showing {(a + b) // 10} tens and {(a + b) % 10} ones.")
        steps = [f"Add the ones: {a_o} + {b_o} = {a_o + b_o}."]
        if a_o + b_o >= 10:
            steps.append(f"{a_o + b_o} ones makes 1 ten and {a_o + b_o - 10} ones.")
        steps.append(f"{a} + {b} = {a + b}.")
        return Item(prompt, num(a + b), steps,
                    wrong_numbers(a + b, [a + b - 10, a + b + 10, a + b - 1, abs(a - b)]),
                    check=FN("add", a=a, b=b), qtype="procedural", tags=("place-value",), diagram=dg)
    return f


def number_riddle_items():
    def f(r, L):
        tens = r.randint(1, 9)
        ones = r.randint(1, 9)
        n = tens * 10 + ones
        style = r.randrange(3)
        if style == 0:
            prompt = f"I have {tens} tens and {ones} ones. What number am I?"
            chk = FN("tens_ones", tens=tens, ones=ones)
        elif style == 1:
            prompt = f"I am greater than {n - 5} and less than {n + 5}. My ones digit is {ones}. What number am I?"
            chk = FN("tens_ones", tens=tens, ones=ones)
        else:
            prompt = f"I have {ones} ones. I have {tens} tens. What number am I?"
            chk = FN("tens_ones", tens=tens, ones=ones)
        return Item(prompt, num(n), [f"{tens} tens is {tens * 10}.", f"{tens * 10} + {ones} = {n}."],
                    wrong_numbers(n, [ones * 10 + tens, n + 10, n - 1]),
                    check=chk, qtype="conceptual", tags=("place-value", "reasoning"),
                    diagram=Diagram("baseten", {"tens": tens, "ones": ones, "caption": "What number?"},
                                    f"{tens} tens rods and {ones} ones cubes."))
    return f


# ------------------------------------------------------------------ story problems
def story_items(kind="join"):
    """kind: join | separate | compare | partwhole | start-unknown | change-unknown."""
    def f(r, L):
        top = 10 if not L else 20
        a = r.randint(2, top - 2)
        b = r.randint(1, min(9, top - a)) if kind in ("join", "separate") else r.randint(1, 9)
        nm, nm2 = name(r), name(r)
        thing = obj(r)
        if kind == "join":
            ans, chk = a + b, FN("add", a=a, b=b)
            prompt = f"{nm} has {a} {thing}. {nm2} gives {nm} {b} more. How many {thing} does {nm} have now?"
        elif kind == "separate":
            ans, chk = a - b, FN("sub", a=a, b=b)
            prompt = f"{nm} has {a} {thing}. {nm} gives {b} away. How many {thing} does {nm} have left?"
        elif kind == "compare":
            a = max(a, b + 1)
            ans, chk = a - b, FN("sub", a=a, b=b)
            prompt = f"{nm} has {a} {thing}. {nm2} has {b} {thing}. How many more {thing} does {nm} have than {nm2}?"
        elif kind == "partwhole":
            total = a + b
            ans, chk = total, FN("add", a=a, b=b)
            prompt = f"{nm} has {a} red {thing} and {b} blue {thing}. How many {thing} does {nm} have in all?"
        elif kind == "start-unknown":
            start = a + b
            ans, chk = start - b, FN("sub", a=start, b=b)
            prompt = f"{nm} had some {thing}. {nm2} gave {nm} {b} more. Now {nm} has {start} {thing}. How many {thing} did {nm} start with?"
        else:  # change-unknown
            start = a + b
            ans, chk = b, FN("sub", a=start, b=a)
            prompt = f"{nm} had {start} {thing}. Now {nm} has {a} {thing}. How many {thing} did {nm} lose?"
        need(ans >= 0)
        return Item(prompt, num(ans), [f"Use the numbers in the story: {a} and {b}.", f"The answer is {ans}."],
                    wrong_numbers(ans, [a + b, max(a, b), abs(a - b) + 1, ans + 1]),
                    check=chk, qtype="word-problem", tags=("story",),
                    diagram=Diagram("comparegroups" if kind == "compare" else "counters",
                                    ({"left": {"count": max(a, b), "label": f"{nm}", "color": "blue"},
                                      "right": {"count": min(a, b), "label": f"{nm2}", "color": "orange"}}
                                     if kind == "compare" else
                                     {"groups": [{"count": a, "color": "blue"}, {"count": b, "color": "orange"}],
                                      "caption": f"{a} and {b}"}),
                                    f"Two groups of counters showing {a} and {b}." if kind != "compare" else f"One group of {max(a, b)} counters and one group of {min(a, b)} counters."))
    return f


def equation_items():
    def f(r, L):
        a, b = r.randint(1, 5), r.randint(1, 5)
        style = r.randrange(3)
        if style == 0:
            prompt = f"Which equation matches this story?\n{name(r)} has {a} {obj(r)} and gets {b} more."
            ans = f"{a} + {b} = {a + b}"
            chk = FN("eq_text", kind="add", a=a, b=b)
        elif style == 1:
            prompt = f"Which equation matches this story?\n{name(r)} has {a + b} {obj(r)} and gives away {b}."
            ans = f"{a + b} − {b} = {a}"
            chk = FN("eq_text", kind="sub", a=a + b, b=b)
        else:
            prompt = f"Which equation shows {a} and {b} make {a + b}?"
            ans = f"{a} + {b} = {a + b}"
            chk = FN("eq_text", kind="add", a=a, b=b)
        return Item(prompt, ans, [f"The story uses {a} and {b}.", f"The matching equation is {ans}."],
                    [(f"{a} − {b} = {a - b}", "subtracted instead of adding"),
                     (f"{a} + {b} = {a + b + 1}", "used the wrong total"),
                     (f"{a + b} + {b} = {a}", "added where it should subtract")],
                    check=chk, qtype="conceptual", tags=("equation",))
    return f


def equal_sign_items():
    def f(r, L):
        a = r.randint(1, 6)
        b = r.randint(1, 6)
        style = r.randrange(3)
        if style == 0:
            prompt = f"What does = mean in {a} + {b} = {a + b}?"
            ans = "the same as"
            chk = FN("equals_word", a=a, b=b)
        elif style == 1:
            prompt = f"Which number makes this true?\n{a} + {b} = ? + {b}"
            ans = num(a)
            chk = FN("missing_same", a=a, b=b)
        else:
            prompt = f"Is this true or false?\n{a} + {b} = {a + b}"
            ans = "true"
            chk = FN("true_eq", a=a, b=b)
        return Item(prompt, ans, [f"Both sides of = must be equal.", f"The answer is {ans}."],
                    [("the answer", "read = as 'the answer is' instead of 'the same as'"),
                     ("add", "thought = means add"), ("false", "thought the equation was false")],
                    check=chk, qtype="conceptual", tags=("equation", "reasoning"))
    return f


def true_false_equation_items():
    def f(r, L):
        a, b = r.randint(1, 9), r.randint(1, 9)
        make_true = r.random() < 0.5
        total = a + b if make_true else a + b + r.choice([-1, 1, 2])
        ans = "true" if total == a + b else "false"
        prompt = f"Is this equation true or false?\n{a} + {b} = {total}"
        chk = FN("tf_eq", a=a, b=b, shown=total)
        return Item(prompt, ans, [f"{a} + {b} = {a + b}.", f"So the equation is {ans}."],
                    [("true" if ans == "false" else "false", "did not check both sides")],
                    check=chk, qtype="conceptual", tags=("reasoning",))
    return f


def explain_strategy_items():
    def f(r, L):
        a = r.randint(6, 9)
        b = r.randint(2, 9)
        style = r.randrange(2)
        if style == 0:
            prompt = f"To add {a} + {b}, one way is to make 10. What number is added to {a} first?"
            ans = num(10 - a)
            chk = FN("missing_part", total=10, part=a)
        else:
            prompt = f"Which strategy helps you find {a} + {b} quickly?"
            ans = "make 10"
            chk = FN("strategy", a=a, b=b)
        return Item(prompt, ans, [f"{a} is close to 10.", f"{a} + {10 - a} = 10, then add the rest."],
                    [("count by 5", "used a strategy that does not fit the numbers"), ("make 10", "chose another strategy")],
                    check=chk, qtype="conceptual", tags=("reasoning", "make-ten"))
    return f


def partition_numbers_items():
    """Partition numbers within 10 into parts (1.OA.B.4)."""
    def f(r, L):
        total = r.randint(4, 10 if L else 8)
        part = r.randint(1, total - 1)
        other = total - part
        style = r.randrange(2)
        if style == 0:
            prompt = f"Break {total} into two parts. One part is {part}. What is the other part?"
            chk = FN("missing_part", total=total, part=part)
        else:
            prompt = f"{total} = {part} + ?\nWhat number goes in the box?"
            chk = FN("missing_part", total=total, part=part)
        return Item(prompt, num(other), [f"{part} and {other} make {total}.", f"{total} − {part} = {other}."],
                    wrong_numbers(other, [total + part, other + 1, total]),
                    check=chk, qtype="procedural", tags=("unknown",),
                    diagram=Diagram("counters", {"groups": [{"count": part, "color": "blue"}, {"count": other, "color": "orange"}],
                                                 "caption": f"{part} and ? make {total}"},
                                    f"{total} counters split into a group of {part} and another group."))
    return f


# ------------------------------------------------------------------ data
def tally_items(kind="read"):
    def f(r, L):
        cats = r.sample(["red", "blue", "green", "yellow"], k=r.choice([2, 3]))
        counts = r.sample(range(1, 9), k=len(cats))       # distinct counts: "most" is unique
        if kind == "total":
            ans, chk = sum(counts), FN("tally_total", rows=list(zip(cats, counts)))
            prompt = "How many tally marks are there in all?"
        elif kind == "compare":
            i, j = r.sample(range(len(cats)), 2)
            need(counts[i] != counts[j])
            ans = cats[i] if counts[i] > counts[j] else cats[j]
            chk = FN("tally_most", rows=list(zip(cats, counts)))
            prompt = "Which color has the most tally marks?"
        elif kind == "count_one":
            i = r.randrange(len(cats))
            ans, chk = counts[i], FN("tally_one", rows=list(zip(cats, counts)), label=cats[i])
            prompt = f"How many tally marks are next to {cats[i]}?"
        else:
            i = r.randrange(len(cats))
            ans, chk = counts[i], FN("tally_one", rows=list(zip(cats, counts)), label=cats[i])
            prompt = f"How many children chose {cats[i]}?"
        return Item(prompt, num(ans) if isinstance(ans, int) else ans,
                    [f"The tally marks show {', '.join(f'{c}: {n}' for c, n in zip(cats, counts))}.",
                     f"The answer is {ans}."],
                    wrong_numbers(ans, [sum(counts), max(counts) + 1, min(counts)]) if isinstance(ans, int)
                    else [("red", "chose a different color")],
                    check=chk, qtype="visual", tags=("data",),
                    diagram=Diagram("tally", {"rows": list(zip(cats, counts)), "caption": "Our favorite colors"},
                                    f"A tally chart: {', '.join(f'{c} has {n} tally marks' for c, n in zip(cats, counts))}."))
    return f


def graph_items(kind="pictograph"):
    def f(r, L):
        labels = r.sample(["apples", "bananas", "grapes", "pears", "cats", "dogs", "fish", "birds"], k=3)
        counts = r.sample(range(1, 9), k=len(labels))     # distinct counts: "most" is unique
        key = 1
        i = r.randrange(len(labels))
        style = r.randrange(3)
        rows = list(zip(labels, counts))
        if style == 0:
            ans, chk = counts[i], FN("graph_one", rows=rows, label=labels[i])
            prompt = f"How many {labels[i]} are shown?"
        elif style == 1:
            ans, chk = sum(counts), FN("graph_sum", rows=rows)
            prompt = "How many in all?"
        else:
            need(counts.count(max(counts)) == 1)
            ans, chk = labels[counts.index(max(counts))], FN("graph_most", rows=rows)
            prompt = "Which one has the most?"
        return Item(prompt, num(ans) if isinstance(ans, int) else ans,
                    [f"The graph shows {', '.join(f'{l}: {c}' for l, c in rows)}.", f"The answer is {ans}."],
                    wrong_numbers(ans, [sum(counts), max(counts) + 1, min(counts)]) if isinstance(ans, int)
                    else [(labels[0], "chose a different row")],
                    check=chk, qtype="visual", tags=("data",),
                    diagram=Diagram(kind, {"rows": rows, "caption": "Our favorite fruit", "key": key, "symbol": "star" if kind == "pictograph" else "dot"},
                                    f"A {'picture' if kind == 'pictograph' else 'bar'} graph: {', '.join(f'{l} has {c}' for l, c in rows)}."))
    return f


def sort_items():
    def f(r, L):
        cats = r.choice([("red", "blue"), ("stars", "circles"), ("apples", "pears")])
        a, b = r.randint(2, 7), r.randint(2, 7)
        items = ["red"] * a + ["blue"] * b if cats[0] == "red" else None
        style = r.randrange(2)
        if style == 0:
            ans, chk = num(a) if cats[0] == "red" else num(a), FN("count", n=a)
            prompt = f"How many {cats[0]} are in the box?"
            wrong = wrong_numbers(a, [b, a + b, a + 1])
        else:
            ans, chk = num(a + b), FN("count", n=a + b)
            prompt = "How many things are in the box in all?"
            wrong = wrong_numbers(a + b, [a, b, a + b + 1])
        dg = Diagram("sortbox", {"items": (["red"] * a + ["blue"] * b) if cats[0] == "red" else
                                 (["blue"] * a + ["orange"] * b), "caption": "A box of shapes"},
                     f"A box holding {a} {cats[0]} and {b} {cats[1]}.")
        return Item(prompt, ans, [f"Count each group.", f"There are {a} {cats[0]} and {b} {cats[1]}."],
                    wrong, check=chk, qtype="visual", tags=("data", "counting"), diagram=dg)
    return f


# ------------------------------------------------------------------ geometry
def shape_identify_items():
    def f(r, L):
        style = r.randrange(2)
        # the attribute wording must name exactly one shape, so 4-sided shapes are only
        # used in the picture-identification variant
        kind = r.choice(SHAPE_WORDS) if style == 0 else r.choice(["triangle", "hexagon", "circle"])
        others = [s for s in SHAPE_WORDS if s != kind]
        if style == 0:
            prompt = "What shape is shown?"
            ans = kind
            chk = FN("shape_name", kind=kind)
            dg = Diagram("shapes", {"shapes": [{"type": kind, "color": pick(r, COLORS)}]},
                         f"One {kind} drawn in colour.")
        else:
            prompt = f"Which shape has {SIDES[kind]} sides?" if kind != "circle" else "Which shape has no corners?"
            ans = kind
            chk = FN("shape_attr_name", sides=SIDES[kind] if kind != "circle" else 0)
            dg = Diagram("shapes", {"shapes": [{"type": s, "color": pick(r, COLORS)} for s in r.sample(others, 3)]},
                         "Three shapes of different kinds.")
        return Item(prompt, ans, [f"A {kind} is the shape that matches.", f"The answer is {kind}."],
                    [(s, "confused it with another shape") for s in others[:3]],
                    check=chk, qtype="visual", tags=("geometry",), diagram=dg)
    return f


def shape_attr_items(kind="sides"):
    def f(r, L):
        shape = r.choice([s for s in SHAPE_WORDS if SIDES[s] > 0])
        n = SIDES[shape] if kind == "sides" else CORNERS[shape]
        prompt = f"How many {kind} does a {shape} have?"
        chk = FN("shape_" + kind, kind=shape)
        return Item(prompt, num(n), [f"A {shape} has {n} {kind}.", f"The answer is {n}."],
                    wrong_numbers(n, [n + 1, n - 1, n + 2]),
                    check=chk, qtype="conceptual", tags=("geometry",),
                    diagram=Diagram("shapes", {"shapes": [{"type": shape, "color": "blue"}]}, f"One {shape}."))
    return f


def solid_items():
    def f(r, L):
        solid = r.choice(SOLIDS)
        style = r.randrange(2)
        if style == 0:
            prompt = "What solid shape is shown?"
            ans = solid
            chk = FN("solid_name", kind=solid)
        else:
            prompt = f"Which solid shape is like a ball?"
            ans = "sphere"
            chk = FN("solid_name", kind="sphere")
            solid = "sphere"
        return Item(prompt, ans, [f"The shape is a {solid}.", f"The answer is {solid}."],
                    [(s, "chose another solid") for s in SOLIDS if s != solid][:3],
                    check=chk, qtype="visual", tags=("geometry",),
                    diagram=Diagram("shapes", {"shapes": [{"type": solid, "color": "teal"}]}, f"One {solid}."))
    return f


def partition_items(kind="rect"):
    def f(r, L):
        parts = r.choice([2, 4])
        shape = "circle" if kind == "circle" else "rectangle"
        shaded = r.randint(1, parts)
        word = {2: "halves", 4: "fourths"}[parts]
        style = r.randrange(3)
        if style == 0:
            ans = num(parts)
            prompt = f"How many equal parts is this {shape} cut into?"
            chk = FN("partition_count", parts=parts)
        elif style == 1:
            ans = word
            prompt = f"The {shape} is cut into {parts} equal parts. What are the parts called?"
            chk = FN("partition_word", parts=parts)
        else:
            ans = word
            prompt = "How much of the shape is shaded?"
            chk = FN("partition_word", parts=parts)
        return Item(prompt, ans, [f"There are {parts} equal parts.", f"The parts are {word}."],
                    [(w, "used the wrong part name") for w in (["thirds", "fourths"] if parts == 2 else ["halves", "thirds"])] +
                    [(num(parts + 1), "counted the parts incorrectly")],
                    check=chk, qtype="visual", tags=("geometry",),
                    diagram=Diagram("partition", {"shape": shape, "parts": parts, "shaded": shaded,
                                                  "caption": f"{parts} equal parts"},
                                    f"A {shape} cut into {parts} equal parts, with {shaded} shaded."))
    return f


def equal_parts_items():
    def f(r, L):
        style = r.randrange(2)
        if style == 0:
            prompt = "Which shape is cut into equal parts?"
            ans = "rectangle"
            chk = FN("equal_parts", parts=4, kind="which")
        else:
            prompt = "Why must parts be the same size when we name halves?"
            ans = "equal parts make halves"
            chk = FN("equal_parts", parts=2, kind="why")
        return Item(prompt, ans, [f"Halves must be equal.", f"The answer is {ans}."],
                    [("unequal parts make halves", "thought unequal parts could be halves")],
                    check=chk, qtype="conceptual", tags=("geometry", "reasoning"),
                    diagram=Diagram("partition", {"shape": "rectangle", "parts": 4, "shaded": 1}, "A rectangle cut into four equal parts."))
    return f


def clock_items(half=False):
    def f(r, L):
        h = r.randint(1, 12)
        m = r.choice([0, 30]) if half else 0
        style = r.randrange(3)
        ans = clock_text(h, m)
        if style == 0:
            prompt = "What time is it?"
            chk = FN("clock", h=h, m=m)
        elif style == 1:
            prompt = "Which digital time matches the clock?"
            chk = FN("clock", h=h, m=m)
        else:
            prompt = "Write the time."
            chk = FN("clock", h=h, m=m)
        return Item(prompt, ans, [f"The hour hand is at {h}.", f"The minute hand is at {m}.", f"The time is {ans}."],
                    [(clock_text((h % 12) + 1, m), "moved the hour hand one hour"),
                     (clock_text(h, 30 if m == 0 else 0), "mixed up the minute hand"),
                     (clock_text((h % 12) + 1, 30 if m == 0 else 0), "moved both hands")],
                    check=chk, qtype="visual", tags=("time",),
                    diagram=Diagram("clock", {"hour": h, "minute": m}, f"An analog clock showing {ans}."))
    return f


def digital_items():
    def f(r, L):
        h = r.randint(1, 12)
        m = r.choice([0, 30])
        ans = clock_text(h, m)
        prompt = f"Write the time that reads {ans} on a digital clock as words." if False else "What time is shown?"
        return Item(prompt, ans, [f"The digits are {h} and {m:02d}.", f"The time is {ans}."],
                    [(clock_text((h % 12) + 1, m), "moved the hour on"), (clock_text(h, 30 if m == 0 else 0), "mixed up the minutes")],
                    check=FN("clock", h=h, m=m), qtype="visual", tags=("time",),
                    diagram=Diagram("clock", {"hour": h, "minute": m}, f"An analog clock showing {ans}."))
    return f


# ------------------------------------------------------------------ measurement
def length_compare_items():
    def f(r, L):
        a, b = r.randint(2, 10), r.randint(2, 10)
        need(a != b)
        style = r.randrange(3)
        if style == 0:
            prompt = "Which object is longer?"
            ans = "the pencil" if a > b else "the crayon"
            chk = FN("longer", a=a, b=b)
        elif style == 1:
            prompt = "Which object is shorter?"
            ans = "the pencil" if a < b else "the crayon"
            chk = FN("shorter", a=a, b=b)
        else:
            prompt = f"How many more units long is the longer object?"
            ans = num(abs(a - b))
            chk = FN("more_count", a=a, b=b)
        return Item(prompt, ans, [f"The pencil is {a} units. The crayon is {b} units.", f"The answer is {ans}."],
                    [("the pencil" if ans == "the crayon" else "the crayon", "picked the other object")] if isinstance(ans, str)
                    else wrong_numbers(abs(a - b), [a + b, max(a, b)]),
                    check=chk, qtype="visual", tags=("measurement",),
                    diagram=Diagram("comparegroups", {"left": {"count": a, "label": "Pencil (units)", "color": "blue"},
                                                      "right": {"count": b, "label": "Crayon (units)", "color": "orange"}},
                                    f"The pencil is {a} units long and the crayon is {b} units long."))
    return f


def ruler_items():
    def f(r, L):
        n = r.randint(2, 9 if not L else 12)
        unit = r.choice(["paper clip", "cube", "tile"])
        prompt = f"How many {unit}s long is the object?"
        return Item(prompt, num(n), [f"Count the {unit}s from end to end.", f"The object is {n} {unit}s long."],
                    wrong_numbers(n, [n + 1, n - 1, n + 2]),
                    check=FN("ruler", n=n), qtype="visual", tags=("measurement",),
                    diagram=Diagram("ruler", {"units": max(n + 2, 6), "unit": unit, "show": n},
                                    f"An object covering {n} {unit} units on a ruler."))
    return f


def order_length_items():
    def f(r, L):
        names = r.sample(["string", "ribbon", "rope", "yarn"], 3)
        vals = r.sample(range(3, 12), 3)
        order = sorted(zip(names, vals), key=lambda t: t[1])
        ans = ", ".join(n for n, _ in order)
        prompt = "Put the objects in order from shortest to longest.\n" + ", ".join(f"{n}: {v} units" for n, v in zip(names, vals))
        return Item(prompt, ans, [f"Compare the unit counts: {', '.join(f'{n} {v}' for n, v in zip(names, vals))}.",
                                  f"From shortest to longest: {ans}."],
                    [(", ".join(n for n, _ in order[::-1]), "ordered from longest to shortest")],
                    check=FN("order_len", pairs=list(zip(names, vals))), qtype="conceptual",
                    tags=("measurement", "order"),
                    diagram=Diagram("comparegroups", {"left": {"count": vals[0], "label": f"{names[0]}", "color": "blue"},
                                                      "right": {"count": vals[1], "label": f"{names[1]}", "color": "orange"}},
                                    "Two objects shown with unit counts."))
    return f


def length_word_items():
    def f(r, L):
        a = r.randint(5, 20)
        b = r.randint(2, 9)
        style = r.randrange(2)
        if style == 0:
            prompt = f"A ribbon is {a} cubes long. Another ribbon is {b} cubes longer. How long is the second ribbon?"
            chk = FN("add", a=a, b=b)
            ans = a + b
        else:
            a = a + b
            prompt = f"A ribbon is {a} cubes long. A second ribbon is {b} cubes long. How much longer is the first ribbon?"
            chk = FN("sub", a=a, b=b)
            ans = a - b
        return Item(prompt, num(ans), [f"Compare the two lengths.", f"The answer is {ans} cubes."],
                    wrong_numbers(ans, [a + b, abs(a - b), ans + 1]),
                    check=chk, qtype="word-problem", tags=("measurement", "story"),
                    diagram=Diagram("comparegroups", {"left": {"count": min(a, 20), "label": "Ribbon A", "color": "blue"},
                                                      "right": {"count": min(b, 20), "label": "Ribbon B", "color": "orange"}},
                                    f"Ribbon A is {a} cubes and Ribbon B is {b} cubes."))
    return f


def count_120_items():
    def f(r, L):
        start = r.choice([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        step = r.choice([1, 1, 10])
        n = start + r.randint(1, 9) * step
        need(n <= 120)
        prompt = r.choice([f"What number comes after {n - step}?",
                           f"Count on from {n - step}. What number is next?",
                           f"Write the number that comes next: {n - 2 * step}, {n - step}, ___"])
        return Item(prompt, num(n), [f"Count on by {step}.", f"{n - step} + {step} = {n}."],
                    wrong_numbers(n, [n - 1, n + 1, n - step, n + step]),
                    check=FN("add", a=n - step, b=step), qtype="procedural", tags=("counting",))
    return f


def write_numeral_items():
    def f(r, L):
        tens = r.randint(1, 9)
        ones = r.randint(0, 9)
        n = tens * 10 + ones
        prompt = r.choice([f"Write the number: {tens} tens and {ones} ones.",
                           f"Write the number shown: {tens} tens, {ones} ones."])
        return Item(prompt, num(n), [f"{tens} tens is {tens * 10}.", f"{tens * 10} + {ones} = {n}."],
                    wrong_numbers(n, [ones * 10 + tens, n + 10, n - 1]),
                    check=FN("tens_ones", tens=tens, ones=ones), qtype="procedural", tags=("place-value",),
                    diagram=Diagram("baseten", {"tens": tens, "ones": ones, "caption": ""},
                                    f"{tens} tens rods and {ones} ones cubes."))
    return f


# ------------------------------------------------------------------ extra families
def teen_add_sub_items():
    """Add or subtract ones to or from a teen number without crossing the ten."""
    def f(r, L):
        n = r.randint(11, 18)
        add = r.random() < 0.5
        if add:
            b = r.randint(1, 19 - n)
            ans = n + b
            prompt = r.choice([f"{n} + {b} = ?", f"Start at {n} and count on {b}."])
            chk = FN("add", a=n, b=b)
        else:
            b = r.randint(1, n - 10)
            ans = n - b
            prompt = r.choice([f"{n} − {b} = ?", f"Start at {n} and count back {b}."])
            chk = FN("sub", a=n, b=b)
        return Item(prompt, num(ans), [f"Only the ones change.", f"{n} {'+' if add else '−'} {b} = {ans}."],
                    wrong_numbers(ans, [ans + 1, ans - 1, ans + 10, n]),
                    check=chk, qtype="procedural", tags=("place-value", "fluency"),
                    diagram=Diagram("baseten", {"tens": 1, "ones": ans - 10, "caption": f"{n} {'+' if add else '−'} {b}"},
                                    f"One ten rod and {ans - 10} ones cubes, showing {ans}."))
    return f


def mixed_facts_items(hi=20):
    """Mixed addition and subtraction facts."""
    def f(r, L):
        top = hi if L else 10
        if r.random() < 0.5:
            a = r.randint(1, top - 1)
            b = r.randint(1, top - a)
            prompt = r.choice([f"{a} + {b} = ?", f"{a} plus {b} is what number?"])
            ans, chk = a + b, FN("add", a=a, b=b)
            wrongs = wrong_numbers(a + b, [a + b + 1, a - b if a > b else a + b + 2, a * b])
        else:
            a = r.randint(2, top)
            b = r.randint(1, a)
            prompt = r.choice([f"{a} − {b} = ?", f"{a} minus {b} is what number?"])
            ans, chk = a - b, FN("sub", a=a, b=b)
            wrongs = wrong_numbers(a - b, [a + b, a - b + 1, b])
        return Item(prompt, num(ans), [f"Work carefully with the numbers given.", f"The answer is {ans}."],
                    wrongs, check=chk, qtype="procedural", tags=("fluency",))
    return f


def compose_items():
    """Compose 2-D shapes and solid figures from smaller shapes (1.G.A.2)."""
    def f(r, L):
        style = r.randrange(3)
        if style == 0:
            ans = "hexagon"
            prompt = "Two triangles are put together along one side. What shape can they make?"
            chk = FN("shape_attr_name", sides=6)
        elif style == 1:
            ans = "square"
            prompt = "Two triangles are put together along their longest sides. What shape do they make?"
            chk = FN("shape_attr_name", sides=4)
        else:
            ans = "cylinder"
            prompt = "Two circles and a rectangle can be folded to make which solid?"
            chk = FN("solid_name", kind="cylinder")
        if ans == "cylinder":
            pieces = [{"type": "circle", "color": "blue"}, {"type": "rectangle", "color": "orange"}, {"type": "circle", "color": "blue"}]
            alt = "Two circles and one rectangle, the pieces that fold into a cylinder."
        else:
            pieces = [{"type": "triangle", "color": "blue"}, {"type": "triangle", "color": "orange"}]
            alt = "Two identical triangles side by side."
        return Item(prompt, ans, [f"Picture the pieces joined edge to edge.", f"The pieces can make a {ans}."],
                    [(s, "chose a shape the pieces cannot make") for s in (["square", "circle", "triangle"] if ans == "hexagon" else ["triangle", "rectangle", "circle"])][:3],
                    check=chk, qtype="conceptual", tags=("geometry", "reasoning"),
                    diagram=Diagram("shapes", {"shapes": pieces, "caption": "Join the pieces"}, alt))
    return f


def count_collection_items(hi=120):
    """Organize and count a collection through 120 using tens and ones."""
    def f(r, L):
        tens = r.randint(1, 9 if not L else 11)
        ones = r.randint(0, 9)
        n = tens * 10 + ones
        need(n <= hi)
        style = r.randrange(2)
        if style == 0:
            prompt = f"There are {tens} full boxes of 10 and {ones} more. How many in all?"
            chk = FN("tens_ones", tens=tens, ones=ones)
        else:
            prompt = f"Count the collection: {tens} tens and {ones} ones. What number is it?"
            chk = FN("tens_ones", tens=tens, ones=ones)
        return Item(prompt, num(n), [f"{tens} tens is {tens * 10}.", f"{tens * 10} + {ones} = {n}."],
                    wrong_numbers(n, [tens + ones, ones * 10 + tens, n + 10]),
                    check=chk, qtype="visual", tags=("place-value", "counting"),
                    diagram=Diagram("baseten", {"tens": tens, "ones": ones, "caption": "Count the collection"},
                                    f"{tens} tens rods and {ones} ones cubes."))
    return f


def story_match_items():
    """Given an equation, choose the story that matches it (1.OA.A.1)."""
    def f(r, L):
        a = r.randint(1, 6)
        b = r.randint(1, 6)
        add = r.random() < 0.5
        nm, nm2 = name(r), name(r)
        thing = obj(r)
        if add:
            ans = f"{nm} has {a} {thing} and gets {b} more."
            chk = FN("story_eq", kind="add", a=a, b=b)
            wrongs = [(f"{nm} has {a} {thing} and gives {b} away.", "the equation adds, but this story subtracts"),
                      (f"{nm} has {a + b} {thing} and gives {b} away.", "this story starts with the total")]
            total = a + b
        else:
            total = a + b
            ans = f"{nm} has {total} {thing} and gives {b} away."
            chk = FN("story_eq", kind="sub", a=total, b=b)
            wrongs = [(f"{nm} has {a} {thing} and gets {b} more.", "the equation subtracts, but this story adds"),
                      (f"{nm} has {b} {thing} and gets {a} more.", "this story adds instead")]
        prompt = f"Which story matches {a} + {b} = {total}?" if add else f"Which story matches {total} − {b} = {a}?"
        return Item(prompt, ans, [f"The equation {'adds' if add else 'subtracts'} {a if add else total} and {b}.",
                                  f"The matching story is: {ans}"],
                    wrongs, check=chk, qtype="conceptual", tags=("story", "equation"))
    return f


def one_more_less_items(hi=20):
    """1 or 2 more / less, with several Grade 1 phrasings and a counter picture."""
    def f(r, L):
        top = hi if L else max(10, hi // 2)
        n = r.randint(1, top - 2)
        k = r.choice([1, 1, 2])
        more = r.random() < 0.5
        ans = n + k if more else max(n - k, 0)
        style = r.randrange(6)
        if style == 0:
            prompt = f"What is {k} more than {n}?"
        elif style == 1:
            prompt = f"What is {k} less than {n}?"
        elif style == 2:
            prompt = f"Which number comes just {'after' if k == 1 and more else 'before' if k == 1 else ('after' if more else 'before')} {n}?"
        elif style == 3:
            prompt = f"{n} {'+' if more else '−'} {k} = ?"
        elif style == 4:
            prompt = f"Draw {k} {'more' if more else 'fewer'}. How many will there be?"
        else:
            prompt = f"There are {n} counters. You {'add' if more else 'take away'} {k}. How many counters are there now?"
        dg = Diagram("counters", {"groups": [{"count": n, "color": "blue"}], "caption": f"Start with {n}"},
                     f"{n} counters in a row.")
        chk = FN("add", a=n, b=k) if more else FN("sub", a=n, b=k)
        return Item(prompt, num(ans), [f"Start at {n}.", f"{'Count on' if more else 'Count back'} {k} to reach {ans}."],
                    wrong_numbers(ans, [n, ans + 1, ans - 1, n + k + 1 if more else n - k + 1]),
                    check=chk, qtype="procedural", tags=("count-on", "fluency"), diagram=dg)
    return f


def compose_ten_items():
    """10 ones compose into one ten (1.NBT.B.2.a)."""
    def f(r, L):
        style = r.randrange(6)
        k = r.randint(1, 5 if L else 2)
        if style == 0:
            prompt, ans, chk = "How many ones make one ten?", "10", FN("ten_ones", tens=1)
            wrong = wrong_numbers(10, [1, 100, 5])
        elif style == 1:
            prompt, ans, chk = "You have 10 ones. How many tens can you make?", "1", FN("tens_from_ones", ones=10)
            wrong = wrong_numbers(1, [10, 0, 2])
        elif style == 2:
            prompt, ans, chk = "1 ten = ___ ones", "10", FN("ten_ones", tens=1)
            wrong = wrong_numbers(10, [1, 11, 20])
        elif style == 3:
            prompt, ans, chk = f"How many ones are in {k} tens?", num(k * 10), FN("ten_ones", tens=k)
            wrong = wrong_numbers(k * 10, [k, k * 10 + 10, k * 10 - 10 if k > 1 else 1])
        elif style == 4:
            prompt, ans, chk = f"You trade {k * 10} ones for tens. How many tens do you get?", num(k), FN("tens_from_ones", ones=k * 10)
            wrong = wrong_numbers(k, [k * 10, k + 1, k * 10 + 1])
        else:
            prompt, ans, chk = f"{k} tens is the same as how many ones?", num(k * 10), FN("ten_ones", tens=k)
            wrong = wrong_numbers(k * 10, [k, k + 10, k * 10 + 10])
        return Item(prompt, ans, ["10 ones make 1 ten.", f"The answer is {ans}."], wrong,
                    check=chk, qtype="conceptual", tags=("place-value",),
                    diagram=Diagram("baseten", {"tens": k, "ones": 0, "caption": "Tens and ones"},
                                    f"{k} tens rods."))
    return f


def domain_facts_items(domain="oa"):
    """High-variety, text-only facts for a domain; a reliable filler for narrow skills."""
    from extras import _fact
    def f(r, L):
        fct = _fact(domain, r, L)
        return Item(fct["prompt"], fct["answer"], fct["steps"], fct["wrong"],
                    check=fct["chk"], qtype="procedural", tags=("fluency",))
    f.__name__ = f"facts_{domain}"
    f.levels, f.mode, f.qtype = [0, 1, 2], "any", "procedural"
    return f
