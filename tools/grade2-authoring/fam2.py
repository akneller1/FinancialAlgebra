"""Grade 2 (math2) question families.

The Grade 1 families are imported wholesale (`from families import *`) because the Grade 2
outline re-teaches fluency within 20, tally charts, picture graphs, base-ten blocks, clocks,
rulers, shapes and partitions. Everything below is Grade 2 only: two-digit regrouping,
three-digit place value, skip counting, number lines, line plots, metric and customary units,
arrays, even/odd, money, time to five minutes, thirds, polygons and two-step problems.

Every item stores its inputs in the check, never the answer, so verify2.py can recompute.
"""
import families
from families import *          # noqa: F401,F403  (reuse the Grade 1 families)
from g1lib import Item, Diagram, FN, EX, KEY, need, rng, Reject
from families import wrong_numbers, name, obj, num, clock_text

THINGS = ["pencils", "markers", "stickers", "shells", "blocks", "beads", "cards", "tiles",
          "marbles", "crayons", "books", "buttons", "stamps", "coins", "apples", "leaves"]


def _w(ans, cands):
    return wrong_numbers(ans, cands)


# ------------------------------------------------------------------ two-digit addition
def add2_items(compose=None, hi=100):
    """Two-digit + two-digit, with or without composing a ten (compose=None mixes both)."""
    def f(r, L):
        if compose is None:
            comp = r.random() < 0.5
        else:
            comp = compose
        a_t, a_o = r.randint(1, 6), r.randint(1, 9)
        b_t = r.randint(1, 4)
        b_o = r.randint(10 - a_o, 9) if comp else r.randint(1, max(1, 9 - a_o))
        a, b = a_t * 10 + a_o, b_t * 10 + b_o
        need(a + b <= hi and b >= 10)
        style = r.randrange(4)
        if style == 0:
            prompt = f"{a} + {b} = ?"
        elif style == 1:
            prompt = f"Add {a} and {b}."
        elif style == 2:
            prompt = f"{name(r)} has {a} {obj(r)}. {name(r)} gets {b} more. How many in all?"
        else:
            prompt = f"Find the sum of {a} and {b}."
        steps = [f"Add the ones: {a_o} + {b_o} = {a_o + b_o}."]
        if a_o + b_o >= 10:
            steps.append(f"{a_o + b_o} ones is 1 ten and {a_o + b_o - 10} ones.")
        steps.append(f"Add the tens and the new ten: {a} + {b} = {a + b}.")
        dg = None
        if style == 0 and r.random() < 0.35:
            s = a + b
            dg = Diagram("baseten3", {"hundreds": s // 100, "tens": (s // 10) % 10, "ones": s % 10,
                                      "caption": f"{a} + {b}"},
                         f"Base-ten blocks showing {a} plus {b} as {s // 100} hundreds, {(s // 10) % 10} tens and {s % 10} ones.")
        return Item(prompt, num(a + b), steps, _w(a + b, [a + b - 10, a + b + 10, a - b if a > b else b - a, a + b - 1]),
                    check=FN("add", a=a, b=b), qtype="procedural", tags=("place-value",), diagram=dg)
    return f


def sub2_items(regroup=None, hi=100):
    """Two-digit - two-digit, with or without decomposing a ten."""
    def f(r, L):
        if regroup is None:
            reg = r.random() < 0.5
        else:
            reg = regroup
        b_t = r.randint(1, 4)
        a_t = r.randint(b_t + 1, 7)
        b_o = r.randint(2, 9)
        a_o = r.randint(0, b_o - 1) if reg else r.randint(b_o, 9)
        a, b = a_t * 10 + a_o, b_t * 10 + b_o
        need(a - b > 0 and a <= hi and b >= 10)
        style = r.randrange(4)
        if style == 0:
            prompt = f"{a} \u2212 {b} = ?"
        elif style == 1:
            prompt = f"Subtract {b} from {a}."
        elif style == 2:
            prompt = f"{name(r)} has {a} {obj(r)} and gives {b} away. How many are left?"
        else:
            prompt = f"Find the difference: {a} \u2212 {b}."
        steps = []
        if reg:
            steps.append(f"There are not enough ones, so break 1 ten into 10 ones.")
            steps.append(f"{a} becomes {a_t - 1} tens and {a_o + 10} ones.")
        steps.append(f"Subtract the ones, then the tens: {a} \u2212 {b} = {a - b}.")
        return Item(prompt, num(a - b), steps, _w(a - b, [a - b + 10, a - b - 10, a + b, a - b + 1]),
                    check=FN("sub", a=a, b=b), qtype="procedural", tags=("place-value",))
    return f


# ------------------------------------------------------------------ three-digit work
def add3_items(compose=None, hi=1000):
    def f(r, L):
        comp = r.random() < 0.5 if compose is None else compose
        a_h, b_h = r.randint(1, 4), r.randint(1, 3)
        a_t, a_o = r.randint(0, 9), r.randint(1, 9)
        b_t, b_o = r.randint(0, 8), (r.randint(10 - a_o, 9) if comp else r.randint(0, 9 - a_o))
        a, b = a_h * 100 + a_t * 10 + a_o, b_h * 100 + b_t * 10 + b_o
        need(a + b <= hi and b >= 100)
        style = r.randrange(3)
        prompt = [f"{a} + {b} = ?", f"Add {a} and {b}.", f"{name(r)} reads {a} pages and then {b} more. How many pages in all?"][style]
        steps = [f"Add hundreds, tens and ones: {a} + {b}."]
        if a_o + b_o >= 10:
            steps.append(f"The ones make a new ten: {a_o} + {b_o} = {a_o + b_o}.")
        steps.append(f"The sum is {a + b}.")
        return Item(prompt, num(a + b), steps, _w(a + b, [a + b - 100, a + b + 100, a + b - 10, a - b if a > b else b - a]),
                    check=FN("add", a=a, b=b), qtype="procedural", tags=("place-value",))
    return f


def sub3_items(hi=1000):
    def f(r, L):
        a_h = r.randint(2, 9)
        b_h = r.randint(1, a_h - 1)
        a_t, a_o = r.randint(0, 9), r.randint(0, 9)
        b_t, b_o = r.randint(0, a_t), (r.randint(0, a_o) if a_o > 0 else 0)
        a, b = a_h * 100 + a_t * 10 + a_o, b_h * 100 + b_t * 10 + b_o
        need(a - b > 0 and a <= hi and b >= 100)
        style = r.randrange(3)
        prompt = [f"{a} \u2212 {b} = ?", f"Subtract {b} from {a}.",
                  f"A library has {a} books. {b} books are borrowed. How many books are left?"][style]
        steps = [f"Subtract hundreds, tens and ones: {a} \u2212 {b} = {a - b}."]
        return Item(prompt, num(a - b), steps, _w(a - b, [a - b + 100, a - b - 100, a - b + 10, a + b]),
                    check=FN("sub", a=a, b=b), qtype="procedural", tags=("place-value",))
    return f


def place3_items(kind="value"):
    def f(r, L):
        h = r.randint(1, 9)
        t = r.randint(0, 9)
        o = r.randint(0, 9)
        n = h * 100 + t * 10 + o
        if kind == "expanded":
            need(sum(1 for v in (h, t, o) if v) >= 2)
            chunks = [f"{h * 100}"] + ([f"{t * 10}"] if t else []) + ([f"{o}"] if o else [])
            ans = " + ".join(chunks)
            prompt = f"Write {n} in expanded form."
            chk = FN("expanded3", n=n)
            wrong = [(f"{h * 100} + {t * 10}", "left out the ones"),
                     (f"{h} + {t} + {o}", "used the digits, not their values"),
                     (f"{h * 100} + {t} + {o}", "did not give the tens its value")]
            tags = ("place-value",)
        elif kind == "hundred_more":
            step = r.choice([10, 100])
            ans = num(n + step)
            prompt = r.choice([f"What is {step} more than {n}?", f"Add {step} to {n}.", f"{n} plus {step} = ?"])
            chk = FN("add", a=n, b=step)
            wrong = _w(n + step, [n - step if n - step > 0 else n + 1, n + 1, n + 10, n + 100])
            tags = ("place-value", "fluency")
        else:
            which = r.choice(["hundreds", "tens", "ones"])
            val = {"hundreds": h * 100, "tens": t * 10, "ones": o}[which]
            ans = num(val)
            prompt = f"In {n}, what is the value of the digit in the {which} place?"
            chk = FN("digit_value3", n=n, which=which)
            wrong = _w(val, [{"hundreds": h, "tens": t, "ones": o}[which], val * 10, val // 10 if val >= 10 else val + 1])
            tags = ("place-value", "reasoning")
        dg = Diagram("place3", {"hundreds": h, "tens": t, "ones": o, "caption": f"{n}"},
                     f"A place value chart for {n}: {h} hundreds, {t} tens and {o} ones.")
        return Item(prompt, ans, [f"{n} has {h} hundreds, {t} tens and {o} ones.", f"The answer is {ans}."],
                    wrong, check=chk, qtype="conceptual", tags=tags, diagram=dg)
    return f


def compare3_items(symbol=False):
    def f(r, L):
        a = r.randint(100, 999)
        b = a + r.choice([-1, 1]) * r.choice([1, 2, 5, 10, 20, 50, 100])
        b = max(100, min(999, b))
        need(a != b)
        if symbol:
            ans = ">" if a > b else "<"
            prompt = f"Compare. Write >, <, or =.  {a}  ___  {b}"
            chk = FN("symbol", a=a, b=b)
            wrong = [("<", "picked the wrong sign") if ans == ">" else (">", "picked the wrong sign"),
                     ("=", "the numbers are not equal")]
        else:
            big = max(a, b)
            ans = num(big)
            prompt = f"Which number is greater, {a} or {b}?"
            chk = FN("which_number", a=a, b=b, which="greater")
            wrong = _w(big, [min(a, b), abs(a - b) + 100, big + 10])
        return Item(prompt, ans, [f"Compare the hundreds first, then the tens, then the ones.", f"The answer is {ans}."],
                    wrong, check=chk, qtype="conceptual", tags=("compare",))
    return f


def order3_items(n=3):
    def f(r, L):
        vals = r.sample(range(105, 995), n)
        ans = ", ".join(str(v) for v in sorted(vals))
        prompt = "Put the numbers in order from least to greatest.\n" + ", ".join(str(v) for v in vals)
        return Item(prompt, ans, [f"Order: {ans}."],
                    [(", ".join(str(v) for v in sorted(vals, reverse=True)), "ordered from greatest to least")],
                    check=FN("sorted", values=vals, direction="asc"), qtype="conceptual", tags=("order",))
    return f


def skip_count_items(step):
    def f(r, L):
        start = step * r.randint(1, 9)
        seqv = [start + step * k for k in range(5)]
        i = r.randint(1, 4)
        missing = seqv[i]
        shown = ["___" if k == i else str(v) for k, v in enumerate(seqv)]
        prompt = f"Count by {step}s. What number is missing?\n" + ", ".join(shown)
        return Item(prompt, num(missing), [f"The pattern adds {step} each time.", f"The missing number is {missing}."],
                    _w(missing, [missing + step, missing - step, missing + 1]),
                    check=FN("skip_seq", values=[v for v in seqv], missing=missing, step=step),
                    qtype="procedural", tags=("counting",),
                    diagram=Diagram("numberline", {"min": seqv[0], "max": seqv[-1], "step": step,
                                                   "marks": [v for v in seqv if v != missing]},
                                    f"A number line from {seqv[0]} to {seqv[-1]} counting by {step}s, with one number hidden."))
    return f


def numberline_items(kind="jump"):
    def f(r, L):
        if kind == "locate":
            lo, hi = 0, r.choice([100, 1000])
            step = 10 if hi == 100 else 100
            p = r.randint(1, (hi // step) - 1) * step
            ans = num(p)
            prompt = "Which number does the arrow point to?"
            chk = FN("count", n=p)
            wrong = _w(p, [p + step, p - step, p + 1])
            tags = ("counting",)
        else:
            lo, hi = 0, r.choice([100, 200])
            a = r.randint(10, 60)
            b = r.randint(5, min(40, hi - a))
            p = None
            ans = num(a + b)
            prompt = r.choice([f"Start at {a}. Jump {b} more. Where do you land?",
                               f"Use the number line: {a} + {b} = ?"])
            chk = FN("add", a=a, b=b)
            wrong = _w(a + b, [a + b + 10, a - b if a > b else a + b + 1, a + b - 10])
            tags = ("counting", "fluency")
        dg = Diagram("numberline", {"min": lo, "max": hi, "step": 10 if hi <= 200 else 100,
                                    "point": p, "jumps": [] if p is not None else [[a, a + b, 0, f"+{b}"]]},
                     f"A number line from {lo} to {hi}" + (f" with an arrow at {p}." if p is not None else f" showing a jump of {b} from {a}."))
        return Item(prompt, ans, [f"Read the number line.", f"The answer is {ans}."], wrong,
                    check=chk, qtype="visual", tags=tags, diagram=dg)
    return f


# ------------------------------------------------------------------ measurement
def lineplot_items(kind="at"):
    def f(r, L):
        values = [r.choice([2, 3, 4, 5, 6, 7]) for _ in range(r.randint(6, 9))]
        need(len(set(values)) >= 3)
        if kind == "total":
            ans = num(sum(values))
            prompt = "The line plot shows the lengths of some pencils in inches. What is the total length of all the pencils?"
            chk = FN("lineplot_total", values=values)
            wrong = _w(sum(values), [sum(values) + 1, len(values), max(values) * len(values)])
        elif kind == "most":
            counts = {v: values.count(v) for v in set(values)}
            best = max(counts.values())
            need(list(counts.values()).count(best) == 1)
            mode = [v for v, c in counts.items() if c == best][0]
            ans = num(mode)
            prompt = "Which length appears most often on the line plot?"
            chk = FN("lineplot_mode", values=values)
            wrong = _w(ans, [max(values), min(values), mode + 1])
        else:
            v = r.choice(values)
            ans = num(values.count(v))
            prompt = f"How many pencils are {v} inches long?"
            chk = FN("lineplot_at", values=values, value=v)
            wrong = _w(values.count(v), [values.count(v) + 1, len(values), v])
        return Item(prompt, ans, ["Read the number of X marks above the value.", f"The answer is {ans}."], wrong,
                    check=chk, qtype="visual", tags=("data", "measurement"),
                    diagram=Diagram("lineplot", {"values": values, "min": min(values), "max": max(values)},
                                    "A line plot of pencil lengths in inches: " +
                                    ", ".join(f"{v} inches appears {values.count(v)} times" for v in sorted(set(values))) + "."))
    return f


def measure_unit_items(kind="metric"):
    def f(r, L):
        metric = kind == "metric"
        if metric:
            options = [("the length of a pencil", "centimeters", "meters", "centimeters", "a pencil is shorter than a meter"),
                       ("the height of a door", "meters", "centimeters", "meters", "a door is taller than a meter"),
                       ("the width of a book", "centimeters", "meters", "centimeters", "a book is shorter than a meter"),
                       ("the length of a playground", "meters", "centimeters", "meters", "a playground is much longer than a meter")]
        else:
            options = [("the length of a crayon", "inches", "feet", "inches", "a crayon is shorter than a foot"),
                       ("the height of a room", "feet", "inches", "feet", "a room is taller than a foot"),
                       ("the length of a shoe", "inches", "feet", "inches", "a shoe is shorter than a foot"),
                       ("the length of a school bus", "feet", "inches", "feet", "a bus is much longer than a foot")]
        thing, big, small, ans, why = r.choice(options)
        prompt = f"Which unit would you use to measure {thing}?"
        opts = [ans, big if ans == small else small]
        need(opts[0] != opts[1])
        return Item(prompt, ans, [f"{why.capitalize()}."], [(opts[1], "chose the unit that is too large or too small")],
                    check=KEY(ans), qtype="conceptual", tags=("measurement",), mode="mc",
                    options=[(ans, True), (opts[1], False)])
    return f


def measure_compare_items(kind="metric"):
    def f(r, L):
        unit = "centimeters" if kind == "metric" else "inches"
        a, b = r.randint(12, 40), r.randint(12, 40)
        need(a != b)
        left, right = "pencil", "ribbon"
        style = r.randrange(3)
        if style == 0:
            ans = f"the {left}" if a > b else f"the {right}"
            prompt = f"Which is longer?"
            chk = FN("longer_lbl", a=a, b=b, left=left, right=right)
            wrong = [(f"the {right}" if a > b else f"the {left}", "picked the shorter object")]
        elif style == 1:
            ans = f"the {left}" if a < b else f"the {right}"
            prompt = "Which is shorter?"
            chk = FN("shorter_lbl", a=a, b=b, left=left, right=right)
            wrong = [(f"the {right}" if a < b else f"the {left}", "picked the longer object")]
        else:
            ans = num(abs(a - b))
            prompt = f"How much longer is the longer one?"
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
        rows, cols = r.randint(2, 5), r.randint(2, 6)
        total = rows * cols
        if kind == "rows":
            ans = num(rows)
            prompt = f"The array shows {total} dots. How many rows are there?"
            chk = FN("array_rows", rows=rows, cols=cols)
            wrong = _w(rows, [cols, total - rows, rows + 1])
        else:
            ans = num(total)
            prompt = r.choice([f"How many dots are in this array?",
                               f"There are {rows} rows with {cols} dots in each row. How many dots?",
                               f"Write the total: {rows} rows of {cols}."])
            chk = FN("array_total", rows=rows, cols=cols)
            wrong = _w(total, [rows + cols, total - rows, total + cols])
        return Item(prompt, ans, [f"{rows} rows of {cols} is {rows} \u00d7 {cols} = {total}.", f"The answer is {ans}."],
                    wrong, check=chk, qtype="visual", tags=("geometry", "counting"),
                    diagram=Diagram("array", {"rows": rows, "cols": cols, "caption": ""},
                                    f"An array with {rows} rows and {cols} dots in each row."))
    return f


def repeated_add_items():
    def f(r, L):
        groups, each = r.randint(2, 5), r.randint(2, 5)
        total = groups * each
        ans = " + ".join([str(each)] * groups)
        prompt = f"There are {groups} groups with {each} in each group. Which repeated addition shows the total?"
        pool = [f"{groups} + {each}", " + ".join([str(each + 1)] * groups),
                " + ".join([str(groups)] * each), " + ".join([str(each)] * (groups + 1))]
        wrong = []
        for t in pool:
            if t != ans and t not in wrong:
                wrong.append(t)
        return Item(prompt, ans, [f"{groups} groups of {each} is {ans} = {total}."],
                    [(w, "wrote the groups and the size, not the size repeated") for w in wrong],
                    check=FN("repeat_add", groups=groups, each=each), qtype="conceptual",
                    tags=("counting",), mode="mc", options=[(ans, True)] + [(w, False) for w in wrong])
    return f


def even_odd_items():
    def f(r, L):
        n = r.randint(10, 99)
        ans = "even" if n % 2 == 0 else "odd"
        style = r.randrange(3)
        if style == 0:
            prompt = f"Is {n} even or odd?"
        elif style == 1:
            prompt = f"Look at {n}. Is it even or odd?"
        else:
            prompt = f"{n} counters are put into pairs. Is {n} even or odd?"
        return Item(prompt, ans, [f"Look at the ones digit: {n % 10}.", f"{n} is {ans}."],
                    [("odd" if ans == "even" else "even", "read the ones digit incorrectly")],
                    check=FN("even_odd", n=n), qtype="conceptual", tags=("reasoning", "counting"))
    return f


def doubles_items():
    def f(r, L):
        n = r.randint(2, 12)
        style = r.randrange(2)
        if style == 0:
            prompt = f"What is double {n}?"
        else:
            prompt = f"{n} + {n} = ?"
        return Item(prompt, num(2 * n), [f"Double {n} means {n} + {n}.", f"{n} + {n} = {2 * n}."],
                    _w(2 * n, [2 * n + 1, 2 * n - 2, n + 2]),
                    check=FN("add", a=n, b=n), qtype="procedural", tags=("fluency",))
    return f


# ------------------------------------------------------------------ money and time
def money_items(kind="count"):
    def f(r, L):
        if kind == "word":
            d = r.randint(1, 9)
            q = r.randint(0, 3)
            cents = d * 10 + q * 25
            nm = name(r)
            prompt = f"{nm} has {d} dimes and {q} quarters. How much money is that?"
            ans = f"{cents}\u00a2" if cents < 100 else f"${cents / 100:.2f}"
            chk = FN("money_cents", cents=cents)
            wrong = _w(cents, [cents + 10, cents - 10 if cents > 10 else cents + 25, cents + 25])
            dg = Diagram("coins", {"coins": [{"value": 10, "count": d}, {"value": 25, "count": q}],
                                   "caption": f"{d} dimes and {q} quarters"},
                         f"{d} dimes and {q} quarters.")
        else:
            vals = [r.choice([1, 5, 10, 25]) for _ in range(r.randint(3, 5))]
            cents = sum(vals)
            ans = f"{cents}\u00a2" if cents < 100 else f"${cents / 100:.2f}"
            prompt = r.choice(["How much money is shown?", "Count the coins. What is the total?"])
            chk = FN("money_cents", cents=cents)
            wrong = _w(cents, [cents + 5, cents - 5 if cents > 5 else cents + 10, cents + 10])
            dg = Diagram("coins", {"coins": [{"value": v, "count": vals.count(v)} for v in sorted(set(vals))],
                                   "caption": "Coins"},
                         "Coins worth " + ", ".join(f"{vals.count(v)} of {v}\u00a2" for v in sorted(set(vals))) + ".")
        return Item(prompt, ans, [f"Add the coin values: {cents}\u00a2.", f"The total is {ans}."],
                    wrong, check=chk, qtype="visual", tags=("measurement",), diagram=dg)
    return f


def time5_items():
    def f(r, L):
        h = r.randint(1, 12)
        m = r.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
        ans = clock_text(h, m)
        style = r.randrange(3)
        prompt = ["What time is shown?", "Write the time on the clock.", "Read the clock. What time is it?"][style]
        wrong = [(clock_text(h, (m + 5) % 60), "moved the minute hand too far"),
                 (clock_text((h % 12) + 1, m), "moved the hour hand"),
                 (clock_text((h % 12) + 1, (m + 5) % 60), "moved both hands")]
        return Item(prompt, ans, [f"The hour hand is between {h} and {(h % 12) + 1}.",
                                  f"The minute hand is on {m // 5 if m % 5 == 0 else m}.",
                                  f"The time is {ans}."],
                    wrong, check=FN("clock", h=h, m=m), qtype="visual", tags=("time",),
                    diagram=Diagram("clock", {"hour": h, "minute": m}, f"An analog clock showing {ans}."))
    return f


def time_word_items():
    def f(r, L):
        h = r.randint(1, 11)
        m = r.choice([0, 15, 30, 45])
        what = r.choice(["eat lunch", "go to recess", "read a story", "line up for the bus", "start math"])
        part = "a.m." if h < 12 else "p.m."
        need(h <= 11)
        ans = clock_text(h, m) + " " + part
        prompt = f"School {what}s at {clock_text(h, m)}. Is that in the {part}?"
        prompt = f"School {what}s at {clock_text(h, m)}. Write the time with a.m. or p.m."
        return Item(prompt, ans, ["Morning times are a.m. and afternoon times are p.m.", f"The answer is {ans}."],
                    [(clock_text(h, m) + (" p.m." if part == "a.m." else " a.m."), "swapped a.m. and p.m.")],
                    check=FN("clock_ampm", h=h, m=m, part=part), qtype="conceptual", tags=("time",))
    return f


# ------------------------------------------------------------------ geometry
def polygon_items(kind="name"):
    def f(r, L):
        shapes = {"pentagon": 5, "hexagon": 6, "quadrilateral": 4, "triangle": 3}
        k = r.choice(list(shapes))
        sides = shapes[k]
        if kind == "sides":
            ans = num(sides)
            prompt = f"How many sides does this shape have?"
            chk = FN("polygon_sides", kind=k)
            wrong = _w(sides, [sides + 1, sides - 1, sides + 2])
        elif kind == "corners":
            ans = num(sides)
            prompt = f"How many corners does this shape have?"
            chk = FN("polygon_corners", kind=k)
            wrong = _w(sides, [sides + 1, sides - 1, 0])
        else:
            ans = k
            prompt = "What is the name of this shape?"
            chk = KEY(k, "square" if k == "quadrilateral" else ("hexagon" if k == "pentagon" else "triangle"))
            wrong = [("hexagon", "counted the sides wrong") if k != "hexagon" else ("pentagon", "counted the sides wrong"),
                     ("triangle", "counted the sides wrong")]
        label = f"{sides} sides"
        return Item(prompt, ans, [f"Count the sides: {sides}.", f"The shape is a {k}."], wrong,
                    check=chk, qtype="visual", tags=("geometry",),
                    diagram=Diagram("polygon", {"shapes": [{"type": k, "color": "blue", "label": label}],
                                                "caption": "A shape"},
                                    f"A {k} with {sides} sides and {sides} corners."))
    return f


def thirds_items(kind="name"):
    def f(r, L):
        parts = r.choice([2, 3, 4])
        word = {2: "halves", 3: "thirds", 4: "fourths"}[parts]
        one = {2: "half", 3: "third", 4: "fourth"}[parts]
        shape = r.choice(["rectangle", "circle"])
        shaded = r.randint(1, parts)
        if kind == "count":
            ans = num(parts)
            prompt = f"The shape is cut into equal parts. How many equal parts are there?"
            chk = FN("partition_count", parts=parts)
            wrong = _w(parts, [parts + 1, parts - 1, shaded])
        elif kind == "shaded":
            ans = f"{shaded}/{parts}"
            prompt = "What fraction of the shape is shaded?"
            chk = FN("fraction_shaded", parts=parts, shaded=shaded)
            wrong = [(f"{parts - shaded}/{parts}", "counted the unshaded parts"),
                     (f"{shaded}/{parts + 1}", "counted the parts wrong")]
        else:
            one_part = r.random() < 0.5
            ans = one if one_part else word
            prompt = (f"The shape is cut into {parts} equal parts. What is one part called?"
                      if one_part else "What are the equal parts called?")
            chk = FN("part_name", parts=parts)
            wrong = [(w, "used the wrong fraction word") for w in ({2: "thirds", 3: "fourths", 4: "halves"}[parts],
                                                                   "quarters" if parts != 4 else "halves")]
        return Item(prompt, ans, [f"The whole is cut into {parts} equal parts.", f"One part is one {one}; the parts are {word}."],
                    wrong, check=chk, qtype="visual", tags=("geometry", "reasoning"),
                    diagram=Diagram("partition", {"shape": shape, "parts": parts, "shaded": shaded,
                                                  "caption": f"{parts} equal parts, {shaded} shaded"},
                                    f"A {shape} cut into {parts} equal parts, with {shaded} shaded."))
    return f


# ------------------------------------------------------------------ problem solving
def two_step_items():
    def f(r, L):
        a = r.randint(20, 60)
        b = r.randint(5, 25)
        c = r.randint(3, min(20, a + b - 1))
        ans = a + b - c
        nm = name(r)
        thing = r.choice(THINGS)
        prompt = (f"{nm} had {a} {thing}. {nm} got {b} more, then gave {c} away. "
                  f"How many {thing} does {nm} have now?")
        return Item(prompt, num(ans), [f"First add: {a} + {b} = {a + b}.", f"Then subtract: {a + b} - {c} = {ans}."],
                    _w(ans, [a + b, a + b + c, a - b - c if a > b + c else ans + 1, c]),
                    check=EX(f"{a}+{b}-{c}"), qtype="multi-step", tags=("multistory", "multistep"))
    return f


def tape_compare_items():
    def f(r, L):
        a = r.randint(30, 90)
        b = r.randint(10, a - 1)
        ans = a - b
        nm, nm2 = name(r), name(r)
        thing = r.choice(THINGS)
        prompt = f"{nm} has {a} {thing}. {nm2} has {b}. How many more {thing} does {nm} have?"
        return Item(prompt, num(ans), [f"Compare: {a} - {b} = {ans}."],
                    _w(ans, [a + b, b, ans + 10]),
                    check=FN("sub", a=a, b=b), qtype="word-problem", tags=("compare",),
                    diagram=Diagram("tape", {"unit": a, "caption": f"Compare {a} and {b}",
                                             "rows": [{"label": nm, "len": a, "text": f"{a}"},
                                                      {"label": nm2, "len": b, "text": f"{b}", "color": "orange"}]},
                                    f"A tape diagram comparing {a} and {b}."))
    return f


def round10_items():
    def f(r, L):
        n = r.randint(11, 99)
        down = n // 10 * 10
        up = down + 10
        ans = down if n - down < 10 else up
        need(n % 10 != 5)
        prompt = r.choice([f"Which ten is {n} closest to?", f"Round {n} to the nearest ten."])
        return Item(prompt, num(ans), [f"{n} is between {down} and {up}.", f"It is closer to {ans}."],
                    _w(ans, [up if ans == down else down, ans + 10]),
                    check=FN("round10", n=n), qtype="conceptual", tags=("place-value", "reasoning"))
    return f


def estimate_items():
    def f(r, L):
        a, b = r.randint(11, 49), r.randint(11, 49)
        ra, rb = a // 10 * 10, b // 10 * 10
        ans = ra + rb
        prompt = f"Estimate the sum by rounding each number to the nearest ten: {a} + {b}."
        return Item(prompt, num(ans), [f"{a} rounds to {ra} and {b} rounds to {rb}.", f"{ra} + {rb} = {ans}."],
                    _w(ans, [a + b, ans + 10, ans - 10]),
                    check=FN("round_sum", a=a, b=b), qtype="conceptual", tags=("place-value", "reasoning"))
    return f


def method_compare_items():
    def f(r, L):
        a = r.randint(11, 49)
        b = r.randint(11, 49)
        methods = [("make ten", f"Break {b} apart to make 10 with {a}."),
                   ("count on", f"Start at {a} and count on {b}."),
                   ("use doubles", f"Double {a} and adjust."),
                   ("break apart a ten", f"Split {b} into tens and ones, then add each part."),
                   ("use a known fact", f"Start from a fact you know and adjust.")]
        idx = r.randrange(len(methods))
        name_, why = methods[idx]
        ans = name_
        wrong = [m[0] for i, m in enumerate(methods) if i != idx][:3]
        prompt = f"Which strategy would you use to find {a} + {b}?"
        return Item(prompt, ans, [why], [(w, "names a different strategy") for w in wrong],
                    check=KEY(ans), qtype="explain", tags=("reasoning",), mode="mc",
                    options=[(ans, True)] + [(w, False) for w in wrong])
    return f


def strategy_items():
    def f(r, L):
        a = r.randint(21, 79)
        b = r.randint(11, 19)
        strategy = r.randrange(3)
        if strategy == 0:
            ans = f"Add {b} in two steps: {a} + 10 + {b - 10}."
            prompt = f"Which strategy finds {a} + {b}?"
        elif strategy == 1:
            ans = f"Make a ten: {a} + {10 - a % 10} + {b - (10 - a % 10)}."
            prompt = f"Which strategy finds {a} + {b}?"
        else:
            ans = f"Count on {b} from {a}."
            prompt = f"Which strategy finds {a} + {b}?"
        wrong = [f"Multiply {a} by {b}.", f"Subtract {b} from {a}.", f"Add {a} and {b} and then add 10 again."]
        return Item(prompt, ans, ["Break one number apart to make the addition easier."],
                    [(w, "describes a different operation") for w in wrong],
                    check=KEY(ans), qtype="explain", tags=("reasoning",), mode="mc",
                    options=[(ans, True)] + [(w, False) for w in wrong])
    return f
