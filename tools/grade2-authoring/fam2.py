"""Grade 2 (math2) question families with a real difficulty ladder.

Every family takes the level L (0 = Remedial, 1 = Standard, 2 = Advanced) and changes three
things with it: the size of the numbers, whether composing/decomposing (regrouping) is needed,
and how many steps or what form the task takes. The Grade 1 families are still imported for
reference, but Grade 2 items are built here so the ladder is explicit and testable
(`level_audit.py` measures it).

Each item stores its inputs in the check, never the answer, so verify2.py can recompute.
"""
from families import *          # noqa: F401,F403  (helpers: num, name, obj, wrong_numbers, Item, ...)
import re

from g1lib import Item, Diagram, FN, EX, KEY, need, Reject
from families import wrong_numbers, name, obj, num, clock_text

THINGS = ["pencils", "markers", "stickers", "shells", "blocks", "beads", "cards", "tiles",
          "marbles", "crayons", "books", "buttons", "stamps", "coins", "apples", "leaves"]


def band(L, low, mid, high):
    return (low, mid, high)[L]


def _w(ans, cands):
    return wrong_numbers(ans, cands)


def tw(n, word):
    return f"{n} {word}" if int(n) == 1 else f"{n} {word}s"


# ------------------------------------------------------------------ two-digit addition
def add2_items(compose=None):
    """L0 no regrouping, L1 mixed, L2 always regrouping with larger tens."""
    def f(r, L):
        comp = (L == 2) if compose is None else compose
        if L == 0:
            a_t, b_t = r.randint(1, 3), r.randint(1, 2)
            a_o, b_o = r.randint(1, 6), r.randint(1, 3)
        elif L == 1:
            a_t, b_t = r.randint(2, 5), r.randint(1, 4)
            a_o, b_o = r.randint(1, 8), r.randint(1, 8)
            if comp:
                b_o = r.randint(max(1, 10 - a_o), 9)
            else:
                b_o = r.randint(1, max(1, 9 - a_o))
        else:
            a_t, b_t = r.randint(3, 7), r.randint(2, 4)
            a_o = r.randint(2, 9)
            b_o = r.randint(max(2, 10 - a_o), 9) if comp else r.randint(1, max(1, 9 - a_o))
        a, b = a_t * 10 + a_o, b_t * 10 + b_o
        need(a + b <= 100 and b >= 10)
        need(a_o + b_o >= 10 if comp else a_o + b_o < 10)
        style = r.randrange(3)
        prompt = [f"{a} + {b} = ?", f"Add {a} and {b}."][style % 2]
        if style == 2:
            prompt = f"{name(r)} has {a} {obj(r)}. {name(r)} gets {b} more. How many in all?"
        steps = [f"Add the ones: {a_o} + {b_o} = {a_o + b_o}."]
        if a_o + b_o >= 10:
            steps.append(f"{a_o + b_o} ones is 1 ten and {a_o + b_o - 10} ones.")
        steps.append(f"{a} + {b} = {a + b}.")
        dg = None
        if L == 2 and r.random() < 0.3:
            s = a + b
            dg = Diagram("baseten3", {"hundreds": s // 100, "tens": (s // 10) % 10, "ones": s % 10,
                                      "caption": f"{a} + {b}"},
                         f"Base-ten blocks for {a} plus {b}: {s // 100} hundreds, {(s // 10) % 10} tens, {s % 10} ones.")
        return Item(prompt, num(a + b), steps, _w(a + b, [a + b - 10, a + b + 10, abs(a - b), a + b - 1]),
                    check=FN("add", a=a, b=b), qtype="procedural", tags=("place-value",), diagram=dg)
    return f


def sub2_items(regroup=None):
    """L0 no decomposing, L1 mixed, L2 always decomposing a ten."""
    def f(r, L):
        reg = (L == 2) if regroup is None else regroup
        if L == 0:
            b_t, a_t = r.randint(1, 2), r.randint(3, 5)
            b_o, a_o = r.randint(1, 5), r.randint(6, 9)
        elif L == 1:
            b_t, a_t = r.randint(1, 3), r.randint(4, 7)
            b_o = r.randint(2, 9)
            a_o = r.randint(0, b_o - 1) if reg else r.randint(b_o, 9)
        else:
            b_t, a_t = r.randint(2, 4), r.randint(5, 8)
            b_o = r.randint(3, 9)
            a_o = r.randint(0, b_o - 1) if reg else r.randint(b_o, 9)
        a, b = a_t * 10 + a_o, b_t * 10 + b_o
        need(a - b > 0 and a <= 100)
        need(a_o < b_o if reg else a_o >= b_o)
        style = r.randrange(3)
        prompt = [f"{a} \u2212 {b} = ?", f"Subtract {b} from {a}."][style % 2]
        if style == 2:
            prompt = f"{name(r)} has {a} {obj(r)} and gives {b} away. How many are left?"
        steps = []
        if a_o < b_o:
            steps.append("There are not enough ones, so break 1 ten into 10 ones.")
        steps.append(f"Subtract ones, then tens: {a} \u2212 {b} = {a - b}.")
        return Item(prompt, num(a - b), steps, _w(a - b, [a - b + 10, a - b - 10, a + b, a - b + 1]),
                    check=FN("sub", a=a, b=b), qtype="procedural", tags=("place-value",))
    return f


# ------------------------------------------------------------------ three-digit work
def add3_items(rename=None, styles=None):
    """L0 no composing, L1 compose a ten, L2 compose a ten and a hundred."""
    def f(r, L):
        ren = (L >= 1) if rename is None else rename
        a_h = band(L, r.randint(1, 2), r.randint(2, 4), r.randint(4, 7))
        b_h = r.randint(1, 2)
        if not ren:
            a_t, b_t = r.randint(1, 4), r.randint(1, 4)
            a_o, b_o = r.randint(1, 4), r.randint(1, 4)
        elif L == 1:
            a_t, b_t = r.randint(1, 4), r.randint(1, 4)
            a_o = r.randint(2, 9)
            b_o = r.randint(10 - a_o, 9)
        else:
            a_t = r.randint(2, 8)
            b_t = r.randint(10 - a_t, 9)
            a_o = r.randint(2, 9)
            b_o = r.randint(10 - a_o, 9)
        a, b = a_h * 100 + a_t * 10 + a_o, b_h * 100 + b_t * 10 + b_o
        need(b >= 100 and a + b <= 1000)
        need((a_o + b_o >= 10) if ren else (a_o + b_o < 10))
        need((a_t + b_t >= 10) if (ren and L == 2) else (a_t + b_t < 10))
        style = r.choice(styles) if styles else r.randrange(3)
        prompt = [f"{a} + {b} = ?", f"Add {a} and {b}.",
                  f"{name(r)} reads {a} pages, then {b} more. How many pages in all?"][style]
        steps = [f"Add the ones: {a_o} + {b_o} = {a_o + b_o}."]
        steps.append("Compose a ten or a hundred when a place has ten or more." if ren
                     else "No place needs composing.")
        steps.append(f"{a} + {b} = {a + b}.")
        return Item(prompt, num(a + b), steps, _w(a + b, [a + b - 10, a + b + 10, a - b if a > b else a + b + 100]),
                    check=FN("add", a=a, b=b), qtype="procedural", tags=("addition",))
    return f


def sub3_items(decompose=None, styles=None, borrow="ten"):
    """L0 no decomposing, L1 decompose a ten, L2 decompose a hundred or a ten."""
    def f(r, L):
        dec = (L >= 1) if decompose is None else decompose
        a_h = band(L, r.randint(2, 4), r.randint(3, 6), r.randint(6, 9)) if not dec else \
            band(L, r.randint(3, 5), r.randint(4, 7), r.randint(7, 9))
        b_h = r.randint(1, 2)
        if not dec:
            a_t, b_t = r.randint(4, 9), r.randint(1, 3)
            a_o, b_o = r.randint(4, 9), r.randint(1, 3)
        elif L == 1:
            a_t, b_t = r.randint(4, 9), r.randint(1, 3)
            b_o = r.randint(2, 9)
            a_o = r.randint(0, b_o - 1)
        elif borrow == "hundred":
            a_t = r.randint(0, 4)
            b_t = r.randint(a_t + 1, 9)
            b_o = r.randint(2, 9)
            a_o = r.randint(0, b_o - 1)
        else:
            a_t, b_t = r.randint(3, 6), r.randint(1, 2)
            b_o = r.randint(2, 9)
            a_o = r.randint(0, b_o - 1)
        a, b = a_h * 100 + a_t * 10 + a_o, b_h * 100 + b_t * 10 + b_o
        need(a - b > 0 and a <= 1000)
        need((a_o < b_o) if dec else (a_o >= b_o and a_t >= b_t))
        if dec and borrow == "hundred":
            need(a_t < b_t)
        style = r.choice(styles) if styles else r.randrange(3)
        prompt = [f"{a} \u2212 {b} = ?", f"Subtract {b} from {a}.",
                  f"A library has {a} books. {b} are borrowed. How many are left?"][style]
        steps = ["Decompose a hundred or a ten only when a place has too few." if dec
                 else "No place needs decomposing."]
        steps.append(f"{a} \u2212 {b} = {a - b}.")
        return Item(prompt, num(a - b), steps, _w(a - b, [a - b - 10 if a - b > 10 else a - b + 10, a + b, a - b + 100]),
                    check=FN("sub", a=a, b=b), qtype="procedural", tags=("subtraction",))
    return f


def place3_items(kind="value"):
    def f(r, L):
        h = r.randint(*((1, 3) if L == 0 else (4, 6) if L == 1 else (7, 9)))
        t = r.randint(0, 9) if L else r.randint(1, 9)
        o = r.randint(0, 9) if L else r.randint(1, 9)
        n = h * 100 + t * 10 + o
        if kind == "expanded":
            need(sum(1 for v in (h, t, o) if v) >= (3 if L == 2 else 2))
            chunks = [f"{h * 100}"] + ([f"{t * 10}"] if t else []) + ([f"{o}"] if o else [])
            ans = " + ".join(chunks)
            prompt = r.choice([f"Write {n} in expanded form.", f"Which sum shows {n} in expanded form?",
                               f"Break {n} into hundreds, tens and ones.", f"Write {n} as a sum of place values."])
            chk = FN("expanded3", n=n)
            wrong = [(" + ".join(str(v) for v in (h, t, o)), "used the digits, not their values"),
                     (f"{h * 100} + {t * 10}", "left out the ones"), (f"{h * 100} + {o}", "left out the tens")]
            tags = ("place-value",)
        elif kind == "hundred_more":
            step = band(L, 10, 100, 100)
            ans = num(n + step)
            prompt = r.choice([f"What is {step} more than {n}?", f"Add {step} to {n}.", f"{n} plus {step} = ?"])
            chk = FN("add", a=n, b=step)
            wrong = _w(n + step, [n - step if n - step > 0 else n + 1, n + 1, n + 10, n + 100])
            tags = ("place-value", "fluency")
        else:
            which = "hundreds" if (L == 0 and r.random() < 0.6) else r.choice(["hundreds", "tens", "ones"])
            val = {"hundreds": h * 100, "tens": t * 10, "ones": o}[which]
            ans = num(val)
            prompt = r.choice([f"In {n}, what is the value of the digit in the {which} place?",
                               f"What is the value of the {which} digit in {n}?",
                               f"Find the value of the digit in the {which} place of {n}.",
                               f"In {n}, what is the {which} digit worth?"])
            chk = FN("digit_value3", n=n, which=which)
            wrong = _w(val, [{"hundreds": h, "tens": t, "ones": o}[which], val * 10, max(1, val // 10)])
            tags = ("place-value", "reasoning")
        dg = Diagram("place3", {"hundreds": h, "tens": t, "ones": o, "caption": f"{n}"},
                     f"A place value chart for {n}: {h} hundreds, {t} tens and {o} ones.")
        return Item(prompt, ans, [f"{n} is {h} hundreds, {t} tens and {o} ones.", f"The answer is {ans}."],
                    wrong, check=chk, qtype="conceptual", tags=tags, diagram=dg)
    return f


def compare3_items(symbol=False):
    def f(r, L):
        if L == 0:
            a = r.randint(20, 99)
            b = r.randint(100, 300)
        elif L == 1:
            a = r.randint(100, 900)
            b = a + r.choice([-1, 1]) * r.choice([1, 5, 10, 100])
        else:
            a = r.randint(100, 999)
            b = a + r.choice([-1, 1]) * r.choice([1, 2, 10, 20])
        b = max(10, min(999, b))
        need(a != b)
        if symbol:
            ans = ">" if a > b else "<"
            prompt = r.choice([f"Compare. Write >, <, or =.  {a}  ___  {b}",
                               f"Which sign makes this true?  {a}  ___  {b}",
                               f"Compare {a} and {b}. Use >, <, or =.",
                               f"Write >, <, or = in the blank:  {a}  ___  {b}",
                               f"Is {a} greater than, less than, or equal to {b}?"])
            chk = FN("symbol", a=a, b=b)
            wrong = [("<", "picked the wrong sign") if ans == ">" else (">", "picked the wrong sign"),
                     ("=", "the numbers are not equal")]
        else:
            big = max(a, b)
            ans = num(big)
            prompt = f"Which number is greater, {a} or {b}?"
            chk = FN("which_number", a=a, b=b, which="greater")
            wrong = _w(big, [min(a, b), abs(a - b) + 100, big + 10])
        return Item(prompt, ans, ["Compare the hundreds first, then the tens, then the ones.", f"The answer is {ans}."],
                    wrong, check=chk, qtype="conceptual", tags=("compare",))
    return f


def order3_items(n=None):
    def f(r, L):
        k = n or band(L, 3, 3, 4)
        lo = band(L, 20, 100, 300)
        vals = r.sample(range(lo, min(lo + 700, 999)), k)
        ans = ", ".join(str(v) for v in sorted(vals))
        prompt = "Put the numbers in order from least to greatest.\n" + ", ".join(str(v) for v in vals)
        return Item(prompt, ans, [f"Order: {ans}."],
                    [(", ".join(str(v) for v in sorted(vals, reverse=True)), "ordered from greatest to least")],
                    check=FN("sorted", values=vals, direction="asc"), qtype="conceptual", tags=("order",))
    return f


def order_choice_items(n=None):
    """Multiple choice over whole lists, so ordering skills can also be tested by choosing."""
    def f(r, L):
        k = n or band(L, 3, 3, 4)
        lo = band(L, 20, 100, 300)
        vals = r.sample(range(lo, min(lo + 700, 999)), k)
        want = ", ".join(str(v) for v in sorted(vals))
        desc = ", ".join(str(v) for v in sorted(vals, reverse=True))
        swapped = sorted(vals)
        i = r.randrange(k - 1)
        swapped[i], swapped[i + 1] = swapped[i + 1], swapped[i]
        sh = sorted(vals)
        r.shuffle(sh)
        opts = [(want, True)]
        for w in (desc, ", ".join(str(v) for v in swapped), ", ".join(str(v) for v in sh)):
            if w != want and all(w != o[0] for o in opts):
                opts.append((w, False))
        while len(opts) < 4:
            more = sorted(vals)
            r.shuffle(more)
            w = ", ".join(str(v) for v in more)
            if all(w != o[0] for o in opts):
                opts.append((w, False))
        r.shuffle(opts)
        prompt = "Which list is in order from least to greatest?\n" + ", ".join(str(v) for v in vals)
        return Item(prompt, want, ["Compare the hundreds, then the tens, then the ones."],
                    [(w, "this list is not in order from least to greatest") for w, ok in opts if not ok],
                    check=FN("sorted", values=vals, direction="asc"), qtype="conceptual",
                    tags=("place-value", "reasoning"), mode="mc", options=opts)
    return f


def skip_count_items(step=None, limit=None):
    """L0 multiples of 10 from a multiple of the step, L1 by 5s or 10s, L2 by 100 from any number."""
    def f(r, L):
        st = step or band(L, 10, 25, 100)
        if limit:
            st = min(st, 100)
        if L == 2:
            start = r.randint(1, 5) * 100 + r.randint(1, 9) * 10 + r.randint(1, 9)
            if limit:
                start = r.randint(1, max(1, int(limit) // 200)) * 100 + r.randint(1, 9) * 10
            st = 100
        else:
            start = st * r.randint(1, 9)
        seqv = [start + st * k for k in range(5)]
        i = r.randint(1, 4)
        missing = seqv[i]
        shown = ["___" if k == i else str(v) for k, v in enumerate(seqv)]
        prompt = f"Count by {st}s. What number is missing?\n" + ", ".join(shown)
        return Item(prompt, num(missing), [f"The pattern adds {st} each time.", f"The missing number is {missing}."],
                    _w(missing, [missing + st, missing - st, missing + 1]),
                    check=FN("skip_seq", values=seqv, missing=missing, step=st),
                    qtype="procedural", tags=("counting",),
                    diagram=Diagram("numberline", {"min": seqv[0], "max": seqv[-1], "step": st,
                                                   "marks": [v for v in seqv if v != missing]},
                                    f"A number line from {seqv[0]} to {seqv[-1]} counting by {step}s with one number hidden."))
    return f


def numberline_items(kind="jump", limit=None):
    def f(r, L):
        hi = band(L, 100, 200, 1000)
        if limit:
            hi = min(hi, band(L, 40, 70, int(limit)))
        step = 10 if hi <= 200 else 100
        if kind == "locate":
            p = r.randint(1, (hi // step) - 1) * step
            ans = num(p)
            prompt = r.choice(["Which number does the arrow point to?", "What number is the arrow pointing to?",
                               "Read the number line. Which number is marked?", "Where does the arrow land on the number line?"])
            chk = FN("count", n=p)
            wrong = _w(p, [p + step, p - step, p + 1])
            tags = ("counting",)
            jumps = []
        else:
            a = r.randint(step, hi // 2)
            b = r.randint(step, min(hi - a, 90 if hi < 1000 else 300))
            p = None
            ans = num(a + b)
            prompt = r.choice([f"Start at {a}. Jump {b} more. Where do you land?",
                               f"Use the number line: {a} + {b} = ?"])
            chk = FN("add", a=a, b=b)
            wrong = _w(a + b, [a + b + step, a - b if a > b else a + b + 1, a + b - step])
            tags = ("counting", "fluency")
            jumps = [[a, a + b, 0, f"+{b}"]]
        dg = Diagram("numberline", {"min": 0, "max": hi, "step": step, "point": p, "jumps": jumps},
                     f"A number line from 0 to {hi}" +
                     (f" with an arrow at {p}." if kind == "locate" else f" showing a jump of {b} from {a}."))
        return Item(prompt, ans, ["Read the number line.", f"The answer is {ans}."], wrong,
                    check=chk, qtype="visual", tags=tags, diagram=dg)
    return f


# ------------------------------------------------------------------ measurement
def lineplot_items(kind="at"):
    """Reading a line plot: total, most, least, one value, or a difference."""
    CTX = [("pencil lengths in inches", "pencils", "inches"),
           ("ribbon lengths in centimeters", "ribbons", "centimeters"),
           ("plant heights in inches", "plants", "inches"),
           ("string lengths in centimeters", "strings", "centimeters"),
           ("leaf lengths in inches", "leaves", "inches")]
    def f(r, L):
        size = band(L, 6, 8, 10)
        spread = band(L, [2, 3, 4], [2, 3, 4, 5, 6], [3, 4, 5, 6, 7, 8])
        values = [r.choice(spread) for _ in range(size)]
        need(len(set(values)) >= 3)
        where, things, unit = r.choice(CTX)
        head = f"The line plot shows {where}."
        if kind == "total":
            ans = num(sum(values))
            prompt = r.choice([f"{head} What is the total length of all the {things}?",
                               f"{head} Add all the x marks. What is the total length?"])
            chk = FN("lineplot_total", values=values)
            wrong = _w(sum(values), [sum(values) + 1, len(values), max(values) * len(values)])
        elif kind == "most":
            counts = {v: values.count(v) for v in set(values)}
            best = max(counts.values())
            need(list(counts.values()).count(best) == 1)
            mode = [v for v, c in counts.items() if c == best][0]
            ans = num(mode)
            prompt = r.choice([f"{head} Which length appears most often?",
                               f"{head} Which length has the most x marks?"])
            chk = FN("lineplot_mode", values=values)
            wrong = _w(mode, [max(values), min(values), mode + 1])
        elif kind == "least":
            ans = num(min(values))
            prompt = r.choice([f"{head} Which length appears least often?",
                               f"{head} Which is the shortest length shown?"])
            chk = FN("lineplot_least", values=values)
            wrong = _w(min(values), [max(values), min(values) + 1, min(values) + 2])
        elif kind == "diff":
            ordered = sorted(set(values))
            a, b = ordered[-1], ordered[0]
            ans = num(values.count(a) - values.count(b))
            prompt = f"{head} How many more {things} are {a} {unit} than {b} {unit}?"
            chk = FN("lineplot_diff", values=values, a=a, b=b)
            wrong = _w(values.count(a) - values.count(b),
                       [values.count(a) + values.count(b), values.count(a), a - b])
        else:
            v = r.choice(values)
            ans = num(values.count(v))
            prompt = r.choice([f"{head} How many {things} are {v} {unit} long?",
                               f"{head} How many x marks are above {v}?"])
            chk = FN("lineplot_at", values=values, value=v)
            wrong = _w(values.count(v), [values.count(v) + 1, len(values), v])
        return Item(prompt, ans, ["Read the number of x marks above the value.", f"The answer is {ans}."], wrong,
                    check=chk, qtype="visual", tags=("data", "measurement"),
                    diagram=Diagram("lineplot", {"values": values, "min": min(values), "max": max(values)},
                                    f"A line plot of {where}: " +
                                    ", ".join(f"{v} appears {values.count(v)} times" for v in sorted(set(values))) + "."))
    return f


def measure_unit_items(kind="metric"):
    """Choosing a unit or a tool, plus a rough estimate, in one measurement system."""
    METRIC = [("a pencil", "centimeters", "meters", "a pencil is shorter than a meter", 0, 19, "centimeter ruler"),
              ("a book", "centimeters", "meters", "a book is shorter than a meter", 0, 25, "centimeter ruler"),
              ("a drinking glass", "centimeters", "meters", "a glass is shorter than a meter", 0, 12, "centimeter ruler"),
              ("a spoon", "centimeters", "meters", "a spoon is shorter than a meter", 0, 15, "centimeter ruler"),
              ("a door", "meters", "centimeters", "a door is taller than a meter", 1, 2, "meter stick"),
              ("a desk", "meters", "centimeters", "a desk is about a meter long", 1, 1, "meter stick"),
              ("a sofa", "meters", "centimeters", "a sofa is longer than a meter", 1, 2, "measuring tape"),
              ("a playground", "meters", "centimeters", "a playground is much longer than a meter", 2, 30, "measuring tape"),
              ("a gym", "meters", "centimeters", "a gym is much longer than a meter", 2, 25, "measuring tape"),
              ("a soccer field", "meters", "centimeters", "a field is much longer than a meter", 2, 100, "measuring tape")]
    CUSTOMARY = [("a crayon", "inches", "feet", "a crayon is shorter than a foot", 0, 4, "inch ruler"),
                 ("a shoe", "inches", "feet", "a shoe is shorter than a foot", 0, 9, "inch ruler"),
                 ("a phone", "inches", "feet", "a phone is shorter than a foot", 0, 6, "inch ruler"),
                 ("a fork", "inches", "feet", "a fork is shorter than a foot", 0, 7, "inch ruler"),
                 ("a room", "feet", "inches", "a room is taller than a foot", 1, 8, "yardstick"),
                 ("a door", "feet", "inches", "a door is taller than a foot", 1, 7, "yardstick"),
                 ("a sofa", "feet", "inches", "a sofa is longer than a foot", 1, 6, "measuring tape"),
                 ("a school bus", "feet", "inches", "a bus is much longer than a foot", 2, 35, "measuring tape"),
                 ("a flagpole", "feet", "inches", "a flagpole is much taller than a foot", 2, 20, "measuring tape"),
                 ("a basketball court", "feet", "inches", "a court is much longer than a foot", 2, 94, "measuring tape")]
    pool = METRIC if kind == "metric" else CUSTOMARY
    unit2 = "{0} is too small a unit here" if kind == "metric" else "{0} is too small a unit here"
    def f(r, L):
        _band = {0: (0,), 1: (0, 1), 2: (1, 2)}[L]
        cands = [x for x in pool if x[4] in _band] or pool
        thing, unit, other, why, cls, about, tool = r.choice(cands)
        pick = r.randrange(3)
        if pick == 0:
            ans = unit
            prompt = r.choice([f"Which unit would you use to measure {thing}?",
                               f"What unit fits best for {thing}?",
                               f"Choose the unit you would use for {thing}."])
            wrong = [(other, "chose the unit that is too large or too small")]
            chk = KEY(ans)
        elif pick == 1:
            ans = tool
            wrong_pool = [t for t in ("centimeter ruler", "meter stick", "measuring tape", "inch ruler", "yardstick")
                          if t != tool]
            r.shuffle(wrong_pool)
            prompt = r.choice([f"Which tool would you use to measure {thing}?",
                               f"What would you use to measure {thing}?",
                               f"Choose the tool for measuring {thing}."])
            wrong = [(w, "chose a tool that is too small or too large") for w in wrong_pool[:2]]
            chk = KEY(ans)
        else:
            ans = num(about)
            prompt = r.choice([f"About how many {unit} long is {thing}?",
                               f"Estimate: {thing} is about how many {unit}?"])
            wrong = _w(about, [about * 10, max(1, about * 100), max(1, about // 10)])
            chk = FN("count", n=about)
        return Item(prompt, ans, [f"{why.capitalize()}.", f"A good measure is about {about} {unit}."],
                    wrong, check=chk, qtype="conceptual", tags=("measurement",))
    return f


def measure_compare_items(kind="metric", limit=None):
    def f(r, L):
        unit = "centimeters" if kind == "metric" else "inches"
        lo, hi = band(L, (6, 18), (14, 44), (30, 95))
        a, b = r.randint(lo, hi), r.randint(lo, hi)
        need(a != b)
        left, right = "pencil", "ribbon"
        style = r.randrange(3)
        if style == 0:
            ans = f"the {left}" if a > b else f"the {right}"
            prompt = "Which is longer?"
            chk = FN("longer_lbl", a=a, b=b, left=left, right=right)
            wrong = [(f"the {right}" if a > b else f"the {left}", "picked the shorter object")]
        elif style == 1:
            ans = f"the {left}" if a < b else f"the {right}"
            prompt = "Which is shorter?"
            chk = FN("shorter_lbl", a=a, b=b, left=left, right=right)
            wrong = [(f"the {right}" if a < b else f"the {left}", "picked the longer object")]
        else:
            ans = num(abs(a - b))
            prompt = "How much longer is the longer one?"
            chk = FN("tape_diff", a=a, b=b)
            wrong = _w(abs(a - b), [a + b, max(a, b), abs(a - b) + 1])
        return Item(prompt, ans, [f"The {left} is {a} {unit}. The {right} is {b} {unit}.", f"The answer is {ans}."],
                    wrong, check=chk, qtype="visual", tags=("measurement",),
                    diagram=Diagram("tape", {"unit": max(a, b), "caption": f"Lengths in {unit}",
                                             "rows": [{"label": f"{left} ({a} {unit})", "len": a, "text": f"{a}"},
                                                      {"label": f"{right} ({b} {unit})", "len": b, "text": f"{b}", "color": "orange"}]},
                                    f"A tape diagram: the {left} is {a} {unit} and the {right} is {b} {unit}."))
    return f


# ------------------------------------------------------------------ equal groups
def array_items(kind="total"):
    def f(r, L):
        rows = r.randint(*((2, 4) if L == 0 else (2, 5) if L == 1 else (3, 5)))
        cols = r.randint(*((2, 4) if L == 0 else (2, 5) if L == 1 else (3, 5)))
        total = rows * cols
        thing, where = r.choice([("dots", "The array shows"), ("tiles", "The array shows"),
                                 ("plants", "The garden rows show")])
        if kind == "rows":
            ans = num(rows)
            prompt = r.choice([f"{where} {total} {thing}. How many rows are there?",
                               f"There are {total} {thing} in equal rows. How many rows?",
                               f"How many rows of {thing} does the array show?"])
            chk = FN("array_rows", rows=rows, cols=cols)
            wrong = _w(rows, [cols, total - rows, rows + 1])
        elif kind == "cols":
            ans = num(cols)
            prompt = r.choice([f"{where} {total} {thing}. How many are in each row?",
                               f"There are {total} {thing} in equal rows. How many in each row?",
                               f"How many {thing} are in one row of the array?"])
            chk = FN("array_cols", rows=rows, cols=cols)
            wrong = _w(cols, [rows, total - cols, cols + 1])
        else:
            ans = num(total)
            prompt = r.choice(["How many dots are in this array?",
                               f"There are {rows} rows with {cols} dots in each row. How many dots?",
                               f"Write the total: {rows} rows of {cols}.",
                               f"The array has {rows} rows of {cols}. How many in all?"])
            chk = FN("array_total", rows=rows, cols=cols)
            wrong = _w(total, [rows + cols, total - rows, total + cols])
        return Item(prompt, ans, [f"{rows} rows of {cols} is {rows} \u00d7 {cols} = {total}.", f"The answer is {ans}."],
                    wrong, check=chk, qtype="visual", tags=("geometry", "counting"),
                    diagram=Diagram("array", {"rows": rows, "cols": cols, "caption": ""},
                                    f"An array with {rows} rows and {cols} dots in each row."))
    return f


def repeated_add_items():
    def f(r, L):
        groups = r.randint(*((2, 4) if L == 0 else (2, 4) if L == 1 else (3, 5)))
        each = r.randint(*((2, 4) if L == 0 else (3, 4) if L == 1 else (4, 5)))
        total = groups * each
        thing = r.choice(["dots", "stickers", "tiles", "apples"])
        ans = " + ".join([str(each)] * groups)
        prompt = r.choice([f"There are {groups} groups with {each} {thing} in each group. "
                           "Which repeated addition shows the total?",
                           f"{groups} equal groups of {each}. Which repeated addition matches?",
                           f"Each of {groups} rows has {each} {thing}. Which repeated addition finds the total?"])
        pool = [f"{groups} + {each}", " + ".join([str(each + 1)] * groups),
                " + ".join([str(groups)] * each), " + ".join([str(each)] * (groups + 1)),
                " + ".join([str(each)] * (groups - 1))]
        wrong = []
        for t in pool:
            if t != ans and t not in wrong:
                wrong.append(t)
        return Item(prompt, ans, [f"{groups} groups of {each} is {ans} = {total}."],
                    [(w, "does not match the number of equal groups") for w in wrong],
                    check=FN("repeat_add", groups=groups, each=each), qtype="conceptual",
                    tags=("counting",), mode="mc", options=[(ans, True)] + [(w, False) for w in wrong])
    return f


def even_odd_items():
    def f(r, L):
        n = band(L, r.randint(2, 20), r.randint(10, 99), r.randint(100, 999))
        ans = "even" if n % 2 == 0 else "odd"
        style = r.randrange(7)
        prompt = [f"Is {n} even or odd?", f"Look at {n}. Is it even or odd?",
                  f"{n} counters are put into pairs. Is {n} even or odd?",
                  f"Tell whether {n} is even or odd.",
                  f"Which word describes {n}: even or odd?",
                  f"Sort {n} as even or odd.",
                  f"{n} is even or odd?"][style]
        return Item(prompt, ans, [f"Look at the ones digit: {n % 10}.", f"{n} is {ans}."],
                    [("odd" if ans == "even" else "even", "read the ones digit incorrectly"),
                     ("neither", "did not decide whether the number is even or odd"),
                     ("both", "said the number is even and odd at once")],
                    check=FN("even_odd", n=n), qtype="conceptual", tags=("reasoning", "counting"))
    return f


def doubles_items():
    def f(r, L):
        n = band(L, r.randint(2, 6), r.randint(4, 10), r.randint(8, 20))
        prompt = r.choice([f"What is double {n}?", f"{n} + {n} = ?"])
        return Item(prompt, num(2 * n), [f"Double {n} means {n} + {n}.", f"{n} + {n} = {2 * n}."],
                    _w(2 * n, [2 * n + 1, 2 * n - 2, n + 2]),
                    check=FN("add", a=n, b=n), qtype="procedural", tags=("fluency",))
    return f


# ------------------------------------------------------------------ money and time
COIN_NAME = {1: "penny", 5: "nickel", 10: "dime", 25: "quarter", 100: "dollar"}


def money_items(kind="count"):
    def f(r, L):
        if L == 0:
            coins = [{"value": 1, "count": r.randint(3, 8)}, {"value": 5, "count": r.randint(1, 3)}]
        elif L == 1:
            coins = [{"value": r.choice([5, 10]), "count": r.randint(2, 5)},
                     {"value": 25, "count": r.randint(0, 2)}]
        else:
            coins = [{"value": 25, "count": r.randint(1, 3)}, {"value": 10, "count": r.randint(1, 4)},
                     {"value": 5, "count": r.randint(0, 2)}]
        coins = [c for c in coins if c["count"]]
        cents = sum(c["value"] * c["count"] for c in coins)
        need(cents <= 100)
        ans = f"{cents}\u00a2" if cents < 100 else f"${cents // 100}.{cents % 100:02d}"
        if kind == "word":
            nm = name(r)
            desc = " and ".join(tw(c["count"], COIN_NAME[c["value"]]) for c in coins)
            prompt = f"{nm} has {desc}. How much money is that?"
            chk = FN("money_cents", cents=cents)
        else:
            prompt = r.choice(["How much money is shown?", "Count the coins. What is the total?",
                               "Add the coins. How much is there?", "What is the total value of these coins?"])
            chk = FN("money_cents", cents=cents)
        wrong = _w(cents, [cents + 10, cents - 5 if cents > 5 else cents + 5, cents + 25])
        return Item(prompt, ans, [f"Add the coin values: {cents}\u00a2.", f"The total is {ans}."],
                    wrong, check=chk, qtype="visual", tags=("measurement",),
                    diagram=Diagram("coins", {"coins": coins, "caption": "Coins"},
                                    "Coins: " + ", ".join(f"{c['count']} of {c['value']}c" for c in coins) + "."))
    return f


def time_items(marks=None):
    """L0 hour and half hour, L1 five-minute marks, L2 five-minute marks in words/quarter past."""
    def f(r, L):
        h = r.randint(1, 12)
        if marks:
            m = r.choice(list(marks))
        elif L == 0:
            m = 0
        elif L == 1:
            m = r.choice([0, 15, 30, 45])
        else:
            m = r.choice([5, 10, 15, 20, 25, 35, 40, 45, 50, 55])
            m = m + r.choice([0, 1, 2]) if m not in (15, 30) else m
            m = min(m, 59)
        ans = clock_text(h, m)
        prompt = r.choice(["What time is shown?", "Write the time on the clock.", "Read the clock. What time is it?",
                           "What time does this clock show?", "Tell the time on this clock.", "Read the time and write it."])
        wrong = [(clock_text(h, (m + 5) % 60), "moved the minute hand too far"),
                 (clock_text((h % 12) + 1, m), "moved the hour hand"),
                 (clock_text((h % 12) + 1, (m + 5) % 60), "moved both hands")]
        return Item(prompt, ans, [f"The hour hand is between {h} and {(h % 12) + 1}.",
                                  f"The minute hand is at {m} minutes.", f"The time is {ans}."],
                    wrong, check=FN("clock", h=h, m=m), qtype="visual", tags=("time",),
                    diagram=Diagram("clock", {"hour": h, "minute": m}, f"An analog clock showing {ans}."))
    return f


def time_word_items():
    def f(r, L):
        h = r.randint(1, 11)
        m = band(L, 0, r.choice([0, 30]), r.choice([5, 15, 25, 35, 40, 45, 50, 55]))
        activity = ["eat lunch", "go to recess", "read a story", "line up for the bus", "start math"][r.randrange(5)]
        part = "a.m." if r.random() < 0.5 else "p.m."
        ans = f"{clock_text(h, m)} {part}"
        prompt = f"School {activity}s at {clock_text(h, m)}. Write the time with a.m. or p.m."
        return Item(prompt, ans, [f"{clock_text(h, m)} happens during the school day, so it is {part}.",
                                  f"The answer is {ans}."],
                    [(f"{clock_text(h, m)} {'p.m.' if part == 'a.m.' else 'a.m.'}", "swapped a.m. and p.m.")],
                    check=FN("clock_ampm", h=h, m=m, part=part), qtype="conceptual", tags=("time",))
    return f


# ------------------------------------------------------------------ geometry
def polygon_items(kind="name"):
    def f(r, L):
        pool = {"triangle": 3, "square": 4, "rectangle": 4, "trapezoid": 4}
        if L >= 1:
            pool.update({"pentagon": 5, "hexagon": 6})
        if L >= 2:
            pool.update({"heptagon": 7, "octagon": 8, "quadrilateral": 4})
        k = r.choice(list(pool))
        sides = pool[k]
        if kind == "sides":
            ans = num(sides)
            prompt = r.choice(["How many sides does this shape have?", "Count the sides. How many are there?",
                               "This shape has how many sides?", "How many straight sides does the shape have?",
                               "Count the sides of the shape. What is the number?", "The shape has how many sides?"])
            chk = FN("polygon_sides", kind=k)
            wrong = _w(sides, [sides + 1, sides - 1, sides + 2])
        elif kind == "corners":
            ans = num(sides)
            prompt = r.choice(["How many corners does this shape have?", "Count the corners. How many are there?",
                               "How many vertices does this shape have?", "Count the corners of the shape.",
                               "This shape has how many corners?", "How many corner points does the shape have?"])
            chk = FN("polygon_corners", kind=k)
            wrong = _w(sides, [sides + 1, sides - 1, 0])
        else:
            ans = k
            prompt = r.choice(["What is the name of this shape?", "Name the shape.", "Which shape is shown?",
                               "What is this shape called?", "Write the name of the shape.", "Which polygon is drawn?"])
            chk = KEY(k)
            others = [w for w in pool if w != k]
            r.shuffle(others)
            wrong = [(w, "chose a shape with a different number of sides") for w in others[:3]]
        return Item(prompt, ans, [f"Count the sides: {sides}.", f"The shape is a {k}."], wrong,
                    check=chk, qtype="visual", tags=("geometry",),
                    diagram=Diagram("polygon", {"shapes": [{"type": k, "color": "blue", "label": f"{sides} sides"}],
                                                "caption": "A shape"},
                                    f"A {k} with {sides} sides and {sides} corners."))
    return f


def thirds_items(kind="name"):
    WORD = {2: ("halves", "half"), 3: ("thirds", "third"), 4: ("fourths", "fourth"),
            6: ("sixths", "sixth"), 8: ("eighths", "eighth")}

    def f(r, L):
        parts = r.choice([2, 3] if L == 0 else [3, 4] if L == 1 else [4, 6, 8])
        word, one = WORD[parts]
        others = [w for p, (w, _) in WORD.items() if p != parts]
        r.shuffle(others)
        shape = r.choice(["rectangle", "circle"])
        shaded = r.randint(1, parts)
        if kind == "count":
            ans = num(parts)
            prompt = r.choice([f"The shape is cut into equal parts. How many equal parts are there?",
                               "Count the equal parts. How many are there?"])
            chk = FN("partition_count", parts=parts)
            wrong = _w(parts, [parts + 1, max(1, parts - 1), shaded])
        elif kind == "shaded":
            ans = f"{shaded}/{parts}"
            prompt = "What fraction of the shape is shaded?"
            chk = FN("fraction_shaded", parts=parts, shaded=shaded)
            wrong = [(f"{parts - shaded}/{parts}", "counted the unshaded parts"),
                     (f"{shaded}/{parts + 1}", "counted the parts wrong"),
                     (f"{shaded + 1 if shaded < parts else shaded}/{parts}", "counted the shaded parts wrong")]
        else:
            one_part = r.random() < 0.5
            ans = one if one_part else word
            prompt = (r.choice([f"The shape is cut into {parts} equal parts. What is one part called?",
                                f"One of the {parts} equal parts is called what?"])
                      if one_part else
                      r.choice(["What are the equal parts called?", "Name the equal parts of this shape."]))
            chk = FN("part_name", parts=parts)
            wrong = [(others[0], "used the wrong fraction word"), (others[1], "used another fraction word"),
                     (others[2] if len(others) > 2 else "tenths", "used a fraction word that does not match")]
        return Item(prompt, ans, [f"The whole is cut into {parts} equal parts.", f"One part is one {one}; the parts are {word}."],
                    wrong, check=chk, qtype="visual", tags=("geometry", "reasoning"),
                    diagram=Diagram("partition", {"shape": shape, "parts": parts, "shaded": shaded,
                                                  "caption": f"{parts} equal parts, {shaded} shaded"},
                                    f"A {shape} cut into {parts} equal parts, with {shaded} shaded."))
    return f


# ------------------------------------------------------------------ problem solving
def two_step_items(limit=None):
    def f(r, L):
        top = int(limit) if limit else None
        if L == 0:
            a, b, c = r.randint(6, 15), r.randint(2, 6), r.randint(1, 4)
        elif L == 1:
            a, b, c = r.randint(20, 60), r.randint(5, 25), r.randint(3, 20)
        elif top:
            a = r.randint(20, max(21, top - 20))
            b = r.randint(5, max(6, top - a - 1))
            c = r.randint(1, max(1, a + b - 1))
        else:
            a, b, c = r.randint(60, 180), r.randint(10, 60), r.randint(5, 40)
        if limit:
            need(max(a, a + b) <= limit)
        ans = a + b - c
        need(ans > 0)
        nm, thing = name(r), r.choice(THINGS)
        prompt = (f"{nm} had {a} {thing}. {nm} got {b} more, then gave {c} away. "
                  f"How many {thing} does {nm} have now?")
        return Item(prompt, num(ans), [f"First add: {a} + {b} = {a + b}.", f"Then subtract: {a + b} \u2212 {c} = {ans}."],
                    _w(ans, [a + b, a + b + c, max(1, a - b - c), c]),
                    check=EX(f"{a}+{b}-{c}"), qtype="multi-step", tags=("multistep",))
    return f


def tape_compare_items(limit=None):
    def f(r, L):
        lo, hi = band(L, (10, 40), (30, 90), (60, 180))
        if limit:
            hi = min(hi, limit)
            lo = min(lo, hi - 5)
        if limit:
            hi = min(hi, limit)
            lo = min(lo, hi - 5)
        a = r.randint(lo, hi)
        b = r.randint(max(1, lo // 2), a - 1)
        ans = a - b
        nm, nm2, thing = name(r), name(r), r.choice(THINGS)
        prompt = f"{nm} has {a} {thing}. {nm2} has {b}. How many more {thing} does {nm} have?"
        return Item(prompt, num(ans), [f"Compare: {a} \u2212 {b} = {ans}."],
                    _w(ans, [a + b, b, ans + 10]),
                    check=FN("sub", a=a, b=b), qtype="word-problem", tags=("compare",),
                    diagram=Diagram("tape", {"unit": a, "caption": f"Compare {a} and {b}",
                                             "rows": [{"label": nm, "len": a, "text": f"{a}"},
                                                      {"label": nm2, "len": b, "text": f"{b}", "color": "orange"}]},
                                    f"A tape diagram comparing {a} and {b}."))
    return f


def round_items(kind="ten"):
    def f(r, L):
        if L <= 1:
            n = band(L, r.randint(11, 49), r.randint(11, 99), 0)
            prompt = r.choice([f"Which ten is {n} closest to?", f"Round {n} to the nearest ten."])
            down = n // 10 * 10
            ans = down if n - down < 5 else down + 10
            need(n % 10 != 5)
            chk = FN("round10", n=n)
            wrong = _w(ans, [down + 10 if ans == down else down, ans + 10])
        else:
            n = r.randint(101, 999)
            prompt = r.choice([f"Which hundred is {n} closest to?", f"Round {n} to the nearest hundred."])
            down = n // 100 * 100
            ans = down if n - down < 50 else down + 100
            need(n % 100 != 50)
            chk = FN("round100", n=n)
            wrong = _w(ans, [down + 100 if ans == down else down, ans + 100])
        return Item(prompt, num(ans), [f"{n} is between {down} and {down + (10 if L < 2 else 100)}.",
                                       f"It is closer to {ans}."], wrong,
                    check=chk, qtype="conceptual", tags=("place-value", "reasoning"))
    return f


def estimate_items():
    def f(r, L):
        if L == 0:
            a, b, unit = r.randint(11, 39), r.randint(11, 39), 10
        elif L == 1:
            a, b, unit = r.randint(21, 79), r.randint(21, 79), 10
        else:
            a, b, unit = r.randint(110, 480), r.randint(110, 480), 100
        ra, rb = a // unit * unit, b // unit * unit
        ans = ra + rb
        word = "ten" if unit == 10 else "hundred"
        prompt = f"Estimate the sum by rounding each number to the nearest {word}: {a} + {b}."
        return Item(prompt, num(ans), [f"{a} rounds to {ra} and {b} rounds to {rb}.", f"{ra} + {rb} = {ans}."],
                    _w(ans, [a + b, ans + unit, ans - unit]),
                    check=FN("round_sum", a=a, b=b, unit=unit), qtype="conceptual",
                    tags=("place-value", "reasoning"))
    return f


def strategy_items(limit=None):
    """Make-a-ten is the recommended method, so the ones digits must force it."""
    def f(r, L):
        lo = 1 if L == 0 else 21 if L == 1 else 101
        hi = 5 if L == 0 else 60 if L == 1 else 480
        a = r.randint(lo, hi) // 10 * 10 + r.randint(6, 9)
        b = r.randint(1, 4) * 10 + r.randint(4, 9)
        if L == 0:
            need(a < 10)
        if limit:
            need(a + b <= int(limit))
        methods = [("make ten", f"Break {b} apart so {a} makes the next ten."),
                   ("count on by ones", f"Count on from {a} one at a time."),
                   ("use doubles", f"Double one number and adjust."),
                   ("guess and check", "Try numbers until one works.")]
        r.shuffle(methods)
        ans = "make ten"
        prompt = r.choice([f"Which strategy would you use to find {a} + {b}?",
                           f"Which is the best way to add {a} and {b}?",
                           f"How would you work out {a} + {b} efficiently?",
                           f"Which method works best for {a} + {b}?",
                           f"What is the quickest strategy for {a} + {b}?",
                           f"Choose a strategy for {a} + {b}."])
        wrong = [(m, "a slower method") for m, _ in methods if m != ans]
        return Item(prompt, ans, [f"The ones digits {a % 10} and {b % 10} make more than ten.",
                                  f"Make a ten, then add the rest: {a} + {b} = {a + b}."],
                    wrong, check=FN("strategy", a=a, b=b), qtype="reasoning",
                    tags=("strategy",))
    return f

def fluency_items(limit=None):
    """Fact fluency: L0 within 10, L1 within 20, L2 within 20 with missing parts and three addends."""
    def f(r, L):
        kind = r.randrange(4 if L == 2 else 3)
        top = band(L, 10, 16, 20)
        if limit:
            top = min(top, int(limit))
        if kind == 0:
            a = r.randint(1, top - 1)
            b = r.randint(1, max(1, top - a))
            return Item(f"{a} + {b} = ?", num(a + b), [f"{a} + {b} = {a + b}."],
                        _w(a + b, [a + b + 1, a + b - 1, abs(a - b)]),
                        check=FN("add", a=a, b=b), qtype="procedural", tags=("fluency",))
        if kind == 1:
            a = r.randint(2, top)
            b = r.randint(1, a)
            return Item(f"{a} \u2212 {b} = ?", num(a - b), [f"{a} \u2212 {b} = {a - b}."],
                        _w(a - b, [a + b, a - b + 1, b]),
                        check=FN("sub", a=a, b=b), qtype="procedural", tags=("fluency",))
        if kind == 2:
            total = r.randint(5, top)
            part = r.randint(1, total - 1)
            return Item(f"{part} + ___ = {total}", num(total - part),
                        [f"Subtract the known part: {total} \u2212 {part} = {total - part}."],
                        _w(total - part, [total + part, total - part + 1, part]),
                        check=FN("missing_part", total=total, part=part), qtype="procedural", tags=("fluency", "unknown"))
        a, b, c = r.randint(2, 8), r.randint(2, 8), r.randint(1, 5)
        if limit:
            need(a + b + c <= int(limit))
        return Item(f"{a} + {b} + {c} = ?", num(a + b + c), [f"{a} + {b} = {a + b}.", f"{a + b} + {c} = {a + b + c}."],
                    _w(a + b + c, [a + b + c + 1, a + b, a + b + c - 1]),
                    check=FN("add3", a=a, b=b, c=c), qtype="procedural", tags=("fluency", "multistep"))
    return f


def graph_data_items(kind="bargraph", limit=None):
    """Reading picture/bar graphs; L0 single row, L1 most/fewest, L2 total and difference."""
    CATS = ["dogs", "cats", "fish", "birds", "apples", "pears"]

    def f(r, L):
        cats = CATS[:band(L, 3, 4, 5)]
        if limit:
            cats = cats[:3] if L < 2 else cats[:2]
        high = band(L, 5, 9, 15)
        if limit and len(cats) == 2:
            high = max(high, min(int(limit) - 2, 12))
        if limit:
            high = max(2, min(high, int(limit) // max(1, len(cats))))
        counts = r.sample(range(2, high + 1), len(cats))
        rows = list(zip(cats, counts))
        if limit:
            need(sum(counts) <= int(limit))
        which = r.randrange(3 if L == 0 else 4 if L == 1 else 5)
        if which == 0:
            i = r.randrange(len(rows))
            ans, prompt = num(rows[i][1]), f"How many {rows[i][0]} are on the graph?"
            chk = FN("graph_one", label=rows[i][0], rows=rows)
        elif which == 1:
            best = max(counts)
            need(counts.count(best) == 1)
            ans, prompt = cats[counts.index(best)], "Which one has the most?"
            chk = FN("graph_most", rows=rows)
        elif which == 2:
            least = min(counts)
            need(counts.count(least) == 1)
            ans, prompt = cats[counts.index(least)], "Which one has the fewest?"
            chk = FN("graph_least", rows=rows)
        elif which == 3:
            ans, prompt = num(sum(counts)), "How many in all?"
            chk = FN("graph_sum", rows=rows)
        else:
            ans = num(max(counts) - min(counts))
            prompt = "How many more does the most popular one have than the least popular one?"
            chk = FN("graph_diff", rows=rows)
        wrong = _w(ans, [len(cats), max(counts), sum(counts)]) if str(ans).isdigit() else \
            [(w, "read a different row") for w in cats if w != ans][:2]
        dg_data = {"rows": rows, "caption": "Our favorites"} if kind == "bargraph" else {"rows": rows}
        return Item(prompt, ans, ["Read the graph rows.", f"The answer is {ans}."], wrong,
                    check=chk, qtype="visual", tags=("data",),
                    diagram=Diagram(kind if kind == "bargraph" else "pictograph", dg_data,
                                    "A graph: " + ", ".join(f"{c} has {n}" for c, n in rows) + "."))
    return f


def tally_data_items(kind="total", limit=None):
    CATS = ["red", "blue", "green", "yellow", "orange"]

    def f(r, L):
        cats = CATS[:band(L, 3, 4, 5)]
        if limit:
            cats = cats[:3] if L < 2 else cats[:2]
        high = band(L, 6, 11, 18)
        if limit and len(cats) == 2:
            high = max(high, min(int(limit) - 2, 12))
        if limit:
            high = max(1, min(high, int(limit) // max(1, len(cats))))
        counts = r.sample(range(1, high + 1), len(cats))
        rows = list(zip(cats, counts))
        if kind == "total":
            ans = num(sum(counts))
            prompt = r.choice(["The tally chart shows these counts. How many in all?",
                               "Add the tally marks. What is the total?",
                               "How many marks are there in all?", "What is the total shown in the tally chart?"])
            chk = FN("tally_total", rows=rows)
        elif kind == "count_one":
            i = r.randrange(len(rows))
            ans, prompt = num(rows[i][1]), f"How many marks are next to {rows[i][0]}?"
            chk = FN("tally_one", rows=rows, label=rows[i][0])
        else:
            best = max(counts)
            need(counts.count(best) == 1)
            ans, prompt = cats[counts.index(best)], "Which has the most marks?"
            chk = FN("tally_most", rows=rows)
        return Item(prompt, ans, ["Count the tally marks row by row.", f"The answer is {ans}."],
                    _w(ans, [sum(counts), max(counts), len(cats)]) if str(ans).isdigit() else
                    [(w, "chose another row") for w in cats if w != ans][:2],
                    check=chk, qtype="visual", tags=("data",),
                    diagram=Diagram("tally", {"rows": rows, "caption": "Tally chart"},
                                    "A tally chart: " + ", ".join(f"{c} has {n}" for c, n in rows) + "."))
    return f


def baseten_items(kind="value", limit=None):
    def f(r, L):
        if L == 0:
            tens, ones = r.randint(1, 4), r.randint(1, 9)
            hundreds = 0
        elif L == 1:
            tens, ones = r.randint(3, 9), r.randint(0, 9)
            hundreds = 0
        else:
            hundreds, tens, ones = r.randint(1, 4), r.randint(0, 9), r.randint(0, 9)
        if limit:
            if int(limit) <= 99:
                hundreds = 0
            else:
                hundreds = min(hundreds, int(limit) // 100)
        n = hundreds * 100 + tens * 10 + ones
        if kind == "regroup":
            need(tens >= 10 if L else True)
            ans = num(n)
            prompt = (f"The picture shows {tw(tens, 'ten')} and {tw(ones, 'one')}. "
                      "What number is that?")
            chk = FN("tens_ones", tens=tens, ones=ones)
        elif kind == "build":
            ans = num(n)
            prompt = r.choice(["What number do the blocks show?", f"Count the blocks. What number is shown?",
                               "Write the number the blocks show.", "What number is shown by these tens and ones?",
                               f"How many is {tens} tens and {ones} ones?"])
            chk = FN("tens_ones", tens=tens, ones=ones) if not hundreds else FN("build3", n=n)
        else:
            which = r.choice(["hundreds", "tens", "ones"]) if hundreds else r.choice(["tens", "ones"])
            ans = num({"hundreds": hundreds * 100, "tens": tens * 10, "ones": ones}[which])
            prompt = f"What is the value of the digit in the {which} place?"
            chk = FN("digit_value3", n=n, which=which)
        dg = (Diagram("baseten3", {"hundreds": hundreds, "tens": tens % 10, "ones": ones, "caption": f"{n}"},
                      f"{hundreds} hundreds, {tens} tens and {ones} ones.")
              if hundreds else
              Diagram("baseten", {"tens": tens, "ones": ones, "caption": "Base-ten blocks"},
                      f"{tens} tens rods and {ones} {'one' if ones == 1 else 'ones'} cubes."))
        return Item(prompt, ans, [f"{n} has {hundreds} hundreds, {tens} tens and {ones} ones.", f"The answer is {ans}."],
                    _w(ans, [ones, tens, n + 10] if str(ans).isdigit() else []),
                    check=chk, qtype="visual", tags=("place-value",), diagram=dg)
    return f


def shape_items(kind="name"):
    def f(r, L):
        pool = {"triangle": 3, "square": 4, "rectangle": 4, "trapezoid": 4}
        if L >= 1:
            pool.update({"pentagon": 5})
        if L >= 2:
            pool.update({"hexagon": 6, "quadrilateral": 4})
        k = r.choice(list(pool))
        if kind == "sides":
            ans = num(pool[k])
            prompt = "How many sides does this shape have?"
            chk = FN("polygon_sides", kind=k)
        else:
            ans = k
            prompt = r.choice(["What shape is this?", "Name the shape."])
            chk = KEY(k)
        return Item(prompt, ans, [f"A {k} has {pool[k]} sides."], [(w, "chose another shape") for w in pool if w != k][:3],
                    check=chk, qtype="visual", tags=("geometry",),
                    diagram=Diagram("polygon", {"shapes": [{"type": k, "color": "blue"}], "caption": "A shape"},
                                    f"A {k}."))
    return f


def two_digit_items(op="add", compose=False, styles=None, limit=None):
    """Two-digit add/sub that keeps the structure the skill names."""
    def f(r, L):
        if op == "add":
            a_t = band(L, r.randint(1, 2), r.randint(3, 5), r.randint(6, 8))
            b_t = r.randint(1, 2)
            if compose:
                a_o = r.randint(2, 9)
                b_o = r.randint(10 - a_o, 9)
            else:
                a_o = r.randint(1, 4)
                b_o = r.randint(1, 9 - a_o)
        else:
            a_t = band(L, r.randint(2, 3), r.randint(4, 6), r.randint(7, 9))
            b_t = r.randint(1, 2)
            if compose:
                a_o = r.randint(1, 8)
                b_o = r.randint(a_o + 1, 9)
            else:
                a_o = r.randint(3, 9)
                b_o = r.randint(0, a_o)
        a, b = a_t * 10 + a_o, b_t * 10 + b_o
        ans = a + b if op == "add" else a - b
        need(ans > 0)
        if op == "add":
            need(ans <= 99)
        if limit:
            need(max(a, b) <= int(limit))
        kind = r.choice(list(styles)) if styles else r.randrange(3)
        sign = "+" if op == "add" else "\u2212"
        if kind == 0:
            prompt = f"{a} {sign} {b} = ?"
        elif kind == 1:
            prompt = f"Add {a} and {b}." if op == "add" else f"Subtract {b} from {a}."
        else:
            nm, thing = name(r), obj(r)
            prompt = (f"{nm} has {a} {thing} and gets {b} more. How many {thing} now?"
                      if op == "add" else
                      f"{nm} has {a} {thing} and gives {b} away. How many {thing} are left?")
        return Item(prompt, num(ans), [f"{a} {sign} {b} = {ans}."],
                    _w(ans, [ans + 10, max(1, ans - 10), a + b]),
                    check=FN("add" if op == "add" else "sub", a=a, b=b),
                    qtype="procedural", tags=("two-digit",))
    return f


def _distinct_families():
    """Give every family factory a unique __name__.

    Each factory returns a closure called ``f``; without distinct names the builder
    counts them as one family (shared usage cap, shared failure count), which starves
    skills that lean on several families of the same kind.  Variants carry their
    argument in the name, so ``graph_data_items('pictograph')`` and
    ``graph_data_items('bargraph')`` stay separate.
    """
    import sys as _sys
    mod = _sys.modules[__name__]
    factories = {n: getattr(mod, n) for n in list(vars(mod)) if n.endswith("_items") and callable(getattr(mod, n))}
    for name, fn in factories.items():
        def make(fn=fn, name=name):
            def factory(*args, **kwargs):
                f = fn(*args, **kwargs)
                limit = kwargs.get("limit")
                if limit:
                    inner = f

                    def capped(r, L, _inner=inner, _lim=int(limit)):
                        it = _inner(r, L)
                        if it is not None:
                            nums = [int(x) for x in re.findall(r"\d+", it.prompt + " " + str(it.answer))]
                            if nums and max(nums) > _lim:
                                raise Reject()
                        return it
                    f = capped
                suffix = "_".join(str(a) for a in args if not callable(a))
                try:
                    f.__name__ = f"{name}_{suffix}" if suffix else name
                except AttributeError:  # pragma: no cover - plain functions
                    pass
                return f
            factory.__name__ = name
            return factory
        setattr(mod, name, make())


_distinct_families()
