"""Unit 8: Measurement and Unit Conversions (4.MD.A.1-3)."""
from g4lib import *

UNIT_ID = "measurement-unit-conversions"
CUST = [("feet", "inches", 12, "length"), ("yards", "feet", 3, "length"), ("yards", "inches", 36, "length"), ("pounds", "ounces", 16, "weight"), ("gallons", "quarts", 4, "capacity"),
        ("quarts", "pints", 2, "capacity"), ("pints", "cups", 2, "capacity"), ("quarts", "cups", 4, "capacity"), ("tons", "pounds", 2000, "weight"), ("miles", "feet", 5280, "length")]
METR = [("kilometers", "meters", 1000, "length"), ("meters", "centimeters", 100, "length"), ("kilograms", "grams", 1000, "mass"), ("liters", "milliliters", 1000, "capacity"), ("centimeters", "millimeters", 10, "length")]
TIME = [("hours", "minutes", 60), ("minutes", "seconds", 60), ("days", "hours", 24), ("weeks", "days", 7)]
SG = {"feet": "foot", "inches": "inch", "yards": "yard", "pounds": "pound", "ounces": "ounce", "gallons": "gallon", "quarts": "quart", "pints": "pint", "cups": "cup", "tons": "ton", "miles": "mile",
      "kilometers": "kilometer", "meters": "meter", "centimeters": "centimeter", "kilograms": "kilogram", "grams": "gram", "liters": "liter", "milliliters": "milliliter", "millimeters": "millimeter",
      "hours": "hour", "minutes": "minute", "seconds": "second", "days": "day", "weeks": "week"}


def pool(sys_, L):
    p = CUST if sys_ == "c" else METR
    if sys_ == "c":
        return p[:7] if L == 0 else p[:9] if L == 1 else p
    return p[:4] if L < 2 else p


def conv_wrongs(x, f, to, big, small):
    v = x * f
    return [W(f"{comma(x + f)} {small}", "added instead of multiplying"), W(f"{comma(x)} {small}", "did not convert"), W(f"{comma(v + f)} {small}", "counted one group too many"),
            W(f"{comma(v * 10)} {small}" if f in (10, 100, 1000) else f"{comma(v - x)} {small}", "used the wrong number of zeros" if f in (10, 100, 1000) else "made a multiplication mistake"),
            W(f"{comma(v // (f * f))} {small}" if v % (f * f) == 0 and v // (f * f) not in (x,) else f"{comma(v + 1)} {small}", "divided instead of multiplying")]


def gen_convert(sys_, name_):
    def f(r, L):
        big, small, k, _ = pick(r, pool(sys_, L))
        x = r.randint(2, 9) if L == 0 else r.randint(3, 25) if L == 1 else r.randint(12, 60)
        if k >= 2000:
            x = r.randint(2, 9)
        v = x * k
        return Item(f"{comma(x)} {big} = ___ {small}", f"{comma(v)} {small}", [f"1 {SG[big]} = {comma(k)} {small}.", f"{comma(x)} × {comma(k)} = {comma(v)} {small}."],
                    conv_wrongs(x, k, small, big, small), FN("convert", x=str(x), frm=big, to=small), qtype="fill-blank", claim=f"{comma(x)} {big} in {small}")
    f.__name__ = name_
    return fam("012")(f)


def gen_table(sys_, name_):
    def f(r, L):
        big, small, k, _ = pick(r, pool(sys_, L))
        need(k < 2000)
        xs = sorted(r.sample(range(1, 10 if L < 2 else 16), 4))
        i = r.randrange(1, 4)
        rows = [[str(x), "?" if j == i else comma(x * k)] for j, x in enumerate(xs)]
        alt = f"A two-column table. The columns are {big} and {small}. " + "; ".join(f"{a} {big}, {b} {small}" for a, b in rows) + "."
        return Item(f"The table shows measurements in {big} and {small}. What number replaces the question mark?", comma(xs[i] * k), [f"1 {SG[big]} = {comma(k)} {small}, so multiply the number of {big} by {comma(k)}.", f"{xs[i]} × {comma(k)} = {comma(xs[i] * k)}."],
                    [W(comma(xs[i] + k), "added instead of multiplying"), W(comma(xs[i - 1] * k + k) if xs[i - 1] + 1 != xs[i] else comma(xs[i] * k + k), "added one more group to the row above"), W(comma(xs[i] * k * 10) if k in (10, 100, 1000) else comma(xs[i] * (k - 1)), "used the wrong conversion fact")],
                    FN("convert", x=str(xs[i]), frm=big, to=small, bare=True), qtype="visual", diagram=Diagram("table", {"header": [big.title(), small.title()], "rows": rows}, alt), tags={"modeling"})
    f.__name__ = name_
    return fam("012")(f)


def gen_compare(sys_, name_):
    def f(r, L):
        big, small, k, _ = pick(r, pool(sys_, L))
        need(k < 2000)
        x = r.randint(2, 9 if L < 2 else 20)
        y = x * k + pick(r, [-1, 1]) * r.randint(1, max(2, k // 2)) if r.random() < 0.85 else x * k
        need(y > 0)
        a, b = f"{comma(x)} {big}", f"{comma(y)} {small}"
        s = "<" if x * k < y else ">" if x * k > y else "="
        flip = r.random() < 0.5
        left, right = (b, a) if flip else (a, b)
        s2 = {"<": ">", ">": "<", "=": "="}[s] if flip else s
        return Item(f"Compare. Write <, > or = to make the statement true: {left} ___ {right}", s2, [f"Convert to the smaller unit: {a} = {comma(x * k)} {small}.", f"{comma(x * k)} {s} {comma(y)}, so {left} {s2} {right}."],
                    [W(z, "compared the numbers without converting units") for z in "<>=" if z != s2], FN("measure_cmp", a=left, b=right), qtype="conceptual", claim=f"Compare {left} and {right}")
    f.__name__ = name_
    return fam("012", mode="sa")(f)


def gen_mixed(sys_, name_):
    def f(r, L):
        big, small, k, _ = pick(r, pool(sys_, L))
        need(k < 2000)
        a = r.randint(1, 6 if L < 2 else 15)
        b = r.randint(1, k - 1)
        v = a * k + b
        return Item(f"{a} {big} {b} {small} = ___ {small}", f"{comma(v)} {small}", [f"{a} {big} = {a} × {comma(k)} = {comma(a * k)} {small}.", f"{comma(a * k)} + {b} = {comma(v)} {small}."],
                    [W(f"{comma(a * k)} {small}", f"forgot to add the extra {small}"), W(f"{a + b} {small}", "added without converting"), W(f"{a}{b} {small}" if int(f"{a}{b}") != v else f"{comma(v + 1)} {small}", "wrote the two numbers side by side"), W(f"{comma(v + k)} {small}", "counted one group too many")],
                    FN("compound_to_small", big=big, small=small, a=a, b=b), qtype="fill-blank", claim=f"{a} {big} {b} {small} in {small}")
    f.__name__ = name_
    return fam("012")(f)


cu_convert, me_convert = gen_convert("c", "cu_convert"), gen_convert("m", "me_convert")
cu_table, me_table = gen_table("c", "cu_table"), gen_table("m", "me_table")
cu_compare, me_compare = gen_compare("c", "cu_compare"), gen_compare("m", "me_compare")
cu_mixed, me_mixed = gen_mixed("c", "cu_mixed"), gen_mixed("m", "me_mixed")

CU_SENSE = [("the length of a pencil", "inches", ["feet", "yards", "miles"]), ("the height of a door", "feet", ["inches", "miles", "ounces"]), ("the distance between two cities", "miles", ["inches", "feet", "pounds"]),
            ("the weight of a strawberry", "ounces", ["pounds", "tons", "cups"]), ("the weight of a large dog", "pounds", ["ounces", "tons", "gallons"]), ("the weight of a truck", "tons", ["ounces", "pounds", "miles"]),
            ("the amount of water in a bathtub", "gallons", ["cups", "ounces", "feet"]), ("the amount of milk in a drinking glass", "cups", ["gallons", "pounds", "yards"]), ("the length of a football field", "yards", ["inches", "miles", "tons"]),
            ("the length of a paper clip", "inches", ["yards", "miles", "pounds"]), ("the amount of soup in a large pot", "quarts", ["tons", "inches", "ounces of weight"]), ("the weight of a bag of potatoes", "pounds", ["ounces", "tons", "quarts"])]
ME_SENSE = [("the length of a ladybug", "millimeters", ["meters", "kilometers", "liters"]), ("the width of a hand", "centimeters", ["meters", "kilometers", "grams"]), ("the length of a classroom", "meters", ["millimeters", "kilometers", "kilograms"]),
            ("the distance of a long bike ride", "kilometers", ["centimeters", "millimeters", "liters"]), ("the mass of a paper clip", "grams", ["kilograms", "liters", "meters"]), ("the mass of a bicycle", "kilograms", ["grams", "milliliters", "centimeters"]),
            ("the amount of medicine in a spoon", "milliliters", ["liters", "grams", "meters"]), ("the amount of water in a large bottle", "liters", ["milliliters", "kilograms", "kilometers"]), ("the height of a flagpole", "meters", ["centimeters", "kilometers", "grams"]),
            ("the mass of a watermelon", "kilograms", ["grams", "liters", "meters"]), ("the length of a new crayon", "centimeters", ["kilometers", "meters", "liters"]), ("the amount of juice in a small juice box", "milliliters", ["liters", "kilograms", "centimeters"])]
CU_ABOUT = [("How long is a school bus?", "about 40 feet", ["about 40 inches", "about 40 miles", "about 4 inches"]), ("How much does a loaf of bread weigh?", "about 1 pound", ["about 1 ounce", "about 1 ton", "about 100 pounds"]),
            ("How much water does a kitchen sink hold?", "about 5 gallons", ["about 5 cups", "about 5 pints", "about 500 gallons"]), ("How tall is a fourth grader?", "about 4 feet", ["about 4 inches", "about 4 yards", "about 40 feet"]),
            ("How long is a new pencil?", "about 7 inches", ["about 7 feet", "about 7 yards", "about 70 inches"]), ("How much does a small car weigh?", "about 1 ton", ["about 1 pound", "about 10 ounces", "about 100 tons"])]
ME_ABOUT = [("How tall is a classroom door?", "about 2 meters", ["about 2 centimeters", "about 2 kilometers", "about 20 meters"]), ("What is the mass of a large textbook?", "about 1 kilogram", ["about 1 gram", "about 100 kilograms", "about 10 grams"]),
            ("How much water does a bathtub hold?", "about 200 liters", ["about 200 milliliters", "about 2 liters", "about 2 milliliters"]), ("How long is a fingernail?", "about 1 centimeter", ["about 1 meter", "about 1 kilometer", "about 10 meters"]),
            ("What is the mass of a grape?", "about 5 grams", ["about 5 kilograms", "about 500 grams", "about 50 kilograms"]), ("How far can you walk in 15 minutes?", "about 1 kilometer", ["about 1 meter", "about 1 centimeter", "about 100 kilometers"])]


def gen_sense(sense, about, name_):
    def f(r, L):
        if r.random() < 0.6:
            what, good, bad = pick(r, sense)
            return mc_key(f"Which unit is the best choice to measure {what}?", good, bad, [f"Think about the size of each unit.", f"{good.capitalize()} are a sensible unit for {what}."], qtype="conceptual", r=r)
        q, good, bad = pick(r, about)
        return mc_key(f"Choose the most reasonable estimate. {q}", good, bad, ["Picture the size of each unit, then picture the object.", f"The most reasonable estimate is {good}."], qtype="real-world", r=r)
    f.__name__ = name_
    return fam("012", mode="mc")(f)


cu_sense, me_sense = gen_sense(CU_SENSE, CU_ABOUT, "cu_sense"), gen_sense(ME_SENSE, ME_ABOUT, "me_sense")


@fam("012")
def cu_word(r, L):
    big, small, k, kind = pick(r, pool("c", L))
    need(k < 2000)
    x = r.randint(2, 9) if L < 2 else r.randint(6, 24)
    nm = name(r)
    s = {"length": f"{nm} has a piece of rope that is {x} {big} long. How many {small} long is the rope?", "weight": f"A box of books weighs {x} {big}. How many {small} does it weigh?",
         "capacity": f"{nm} makes {x} {big} of lemonade. How many {small} of lemonade is that?"}[kind]
    if L == 2:
        y = r.randint(1, k - 1) if k > 2 else 1
        v = x * k - y
        s2 = {"length": f"{nm} has a rope that is {x} {big} long and cuts off {y} {small}. How many {small} of rope are left?", "weight": f"A crate weighs {x} {big}. After {y} {small} are removed, how many {small} does the crate weigh?",
              "capacity": f"{nm} makes {x} {big} of lemonade and pours out {y} {small}. How many {small} are left?"}[kind]
        return Item(s2, f"{comma(v)} {small}", [f"{x} {big} = {x} × {k} = {comma(x * k)} {small}.", f"{comma(x * k)} − {y} = {comma(v)} {small}."],
                    [W(f"{comma(x * k)} {small}", "stopped after converting"), W(f"{x - y if x > y else x + y} {small}", "subtracted without converting"), W(f"{comma(x * k + y)} {small}", "added instead of subtracting"), W(f"{comma(v - k)} {small}", "made a multiplication mistake")],
                    FN("compound_to_small", big=big, small=small, a=x, b=-y), qtype="multi-step", tags={"multistep"})
    return Item(s, f"{comma(x * k)} {small}", [f"1 {SG[big]} = {k} {small}.", f"{x} × {k} = {comma(x * k)} {small}."], conv_wrongs(x, k, small, big, small), FN("convert", x=str(x), frm=big, to=small), qtype="word-problem")


@fam("012")
def me_word(r, L):
    big, small, k, kind = pick(r, pool("m", L))
    x = r.randint(2, 9) if L < 2 else r.randint(6, 24)
    nm = name(r)
    y = r.randint(1, 9) * (k // 10) if k >= 100 else r.randint(1, 9)
    if L == 0:
        s = {"length": f"A hallway is {x} {big} long. How many {small} long is it?", "mass": f"A pumpkin has a mass of {x} {big}. What is its mass in {small}?", "capacity": f"A pitcher holds {x} {big} of water. How many {small} does it hold?"}[kind]
        return Item(s, f"{comma(x * k)} {small}", [f"1 {SG[big]} = {comma(k)} {small}.", f"{x} × {comma(k)} = {comma(x * k)} {small}."], conv_wrongs(x, k, small, big, small), FN("convert", x=str(x), frm=big, to=small), qtype="word-problem")
    v = x * k + y
    s = {"length": f"{nm} walks {x} {big} to the park and then {comma(y)} {small} more to the pond. How many {small} does {nm} walk in all?", "mass": f"A bag of rice has a mass of {x} {big}. {nm} adds {comma(y)} {small} more rice. What is the total mass in {small}?",
         "capacity": f"A cooler holds {x} {big} of water. {nm} adds {comma(y)} {small} more. How many {small} of water are in the cooler now?"}[kind]
    return Item(s, f"{comma(v)} {small}", [f"{x} {big} = {x} × {comma(k)} = {comma(x * k)} {small}.", f"{comma(x * k)} + {comma(y)} = {comma(v)} {small}."],
                [W(f"{comma(x * k)} {small}", "stopped after converting"), W(f"{comma(x + y)} {small}", "added without converting"), W(f"{comma(x * k - y)} {small}", "subtracted instead of adding"), W(f"{comma(x * k * 10 + y)} {small}", "used the wrong conversion fact")],
                FN("compound_to_small", big=big, small=small, a=x, b=y), qtype="multi-step", tags={"multistep"})


@fam("12")
def me_fraction(r, L):
    big, small, k, kind = pick(r, METR[:4])
    n, d = pick(r, [(1, 2), (1, 4), (3, 4), (1, 10), (3, 10), (1, 5), (2, 5)])
    v = k * n // d
    return Item(f"{n}/{d} {SG[big]} = ___ {small}", f"{comma(v)} {small}", [f"1 {SG[big]} = {comma(k)} {small}.", f"{n}/{d} of {comma(k)}: {comma(k)} ÷ {d} = {comma(k // d)}, and {n} × {comma(k // d)} = {comma(v)} {small}."],
                [W(f"{comma(k // d)} {small}" if n > 1 else f"{comma(k * d)} {small}", "used only the denominator" if n > 1 else "multiplied by the denominator"), W(f"{comma(k)} {small}", "ignored the fraction"), W(f"{comma(v * 10)} {small}", "used the wrong number of zeros"), W(f"{n * d} {small}", "multiplied the numerator and denominator")],
                FN("convert", x=f"{n}/{d}", frm=big, to=small), qtype="fill-blank", tags={"challenge"})


# ============================================================== S3 Time and Elapsed Time
def tfmt(m):
    m %= 24 * 60
    h, mm = divmod(m, 60)
    ap = "AM" if h < 12 else "PM"
    h12 = h % 12 or 12
    return f"{h12}:{mm:02d} {ap}"


def dur(m):
    h, mm = divmod(m, 60)
    parts = []
    if h:
        parts.append(f"{h} hour{'s' if h != 1 else ''}")
    if mm:
        parts.append(f"{mm} minute{'s' if mm != 1 else ''}")
    return " ".join(parts)


def tcase(r, L):
    start = r.randint(6 * 12, 20 * 12) * 5
    if L == 2:
        start += r.randint(0, 4)
    d = r.randint(2, 11) * 5 if L == 0 else r.randint(13, 35) * 5 if L == 1 else r.randint(50, 200)
    return start, d


@fam("012")
def tm_convert(r, L):
    big, small, k = pick(r, TIME)
    x = r.randint(2, 9) if L < 2 else r.randint(6, 15)
    if L and r.random() < 0.5 and k != 7:
        b = r.randint(5, k - 1)
        v = x * k + b
        return Item(f"{x} {big} {b} {small} = ___ {small}", f"{comma(v)} {small}", [f"{x} {big} = {x} × {k} = {x * k} {small}.", f"{x * k} + {b} = {comma(v)} {small}."],
                    [W(f"{x * k} {small}", f"forgot to add the extra {small}"), W(f"{x + b} {small}", "added without converting"), W(f"{x * 100 + b} {small}", f"used 100 instead of {k}"), W(f"{v + k} {small}", "counted one group too many")],
                    FN("compound_to_small", big=big, small=small, a=x, b=b), qtype="fill-blank")
    return Item(f"{x} {big} = ___ {small}", f"{comma(x * k)} {small}", [f"1 {SG[big]} = {k} {small}.", f"{x} × {k} = {comma(x * k)} {small}."],
                [W(f"{x * 100} {small}" if k == 60 else f"{x * 10} {small}", f"used the wrong number instead of {k}"), W(f"{x + k} {small}", "added instead of multiplying"), W(f"{x * k + k} {small}", "counted one group too many"), W(f"{x} {small}", "did not convert")],
                FN("convert", x=str(x), frm=big, to=small), qtype="fill-blank", claim=f"{x} {big} in {small}")


@fam("012")
def tm_elapsed_minutes(r, L):
    start, d = tcase(r, min(L, 1))
    need(d < 120)
    what = pick(r, ["A music lesson", "Soccer practice", "A bus ride", "A science show", "Recess and lunch", "A swim class"])
    return Item(f"{what} starts at {tfmt(start)} and ends at {tfmt(start + d)}. How many minutes long is it?", f"{d} minutes",
                [f"Count from {tfmt(start)} to the next hour, then on to {tfmt(start + d)}." if (start % 60) + d >= 60 else f"The hour is the same, so subtract the minutes.", f"The time is {d} minutes."],
                [W(f"{abs(((start + d) % 60) - (start % 60)) or d + 10} minutes", "subtracted only the minutes"), W(f"{d + 40} minutes", "treated an hour as 100 minutes"), W(f"{d + 60} minutes", "counted an extra hour"), W(f"{d - 5 if d > 10 else d + 5} minutes", "miscounted by 5 minutes")],
                FN("elapsed", start=tfmt(start), end=tfmt(start + d), unit="minutes"), qtype="real-world")


@fam("012", mode="mc")
def tm_elapsed_hm(r, L):
    start, d = tcase(r, max(L, 1))
    need(d > 60 and d % 60)
    what = pick(r, ["A movie", "A hike", "A baseball game", "A road trip", "A school play", "A museum visit"])
    return Item(f"{what} starts at {tfmt(start)} and ends at {tfmt(start + d)}. How long does it last?", dur(d),
                [f"Count whole hours from {tfmt(start)}: {d // 60} hour{'s' if d >= 120 else ''} takes you to {tfmt(start + d // 60 * 60)}.", f"Then count {d % 60} more minutes to {tfmt(start + d)}. Total: {dur(d)}."],
                [W(dur(d + 60), "counted an extra hour"), W(dur(d - 60) if d > 120 else dur(d + 40), "counted too few hours" if d > 120 else "treated an hour as 100 minutes"), W(dur(d // 60 * 60 + (60 - d % 60)) if d % 60 != 30 else dur(d + 10), "subtracted the minutes in the wrong order")],
                FN("elapsed", start=tfmt(start), end=tfmt(start + d), unit="hm"), qtype="real-world")


@fam("012", mode="mc")
def tm_end(r, L):
    start, d = tcase(r, L)
    what = pick(r, ["A class", "A cartoon", "Band practice", "A train ride", "A cooking lesson", "A soccer game"])
    back = r.random() < 0.4
    if back:
        end = start + d
        return Item(f"{what} lasted {dur(d)} and ended at {tfmt(end)}. What time did it start?", tfmt(start), [f"Count back {dur(d)} from {tfmt(end)}.", f"It started at {tfmt(start)}."],
                    [W(tfmt(end + d), "counted forward instead of back"), W(tfmt(start + 60), "missed an hour when counting back"), W(tfmt(start - 10), "miscounted the minutes")], FN("time_add", start=tfmt(end), minutes=-d), qtype="real-world")
    return Item(f"{what} starts at {tfmt(start)} and lasts {dur(d)}. What time does it end?", tfmt(start + d), [f"Count on {dur(d)} from {tfmt(start)}.", f"It ends at {tfmt(start + d)}."],
                [W(tfmt(start + d + 60), "counted an extra hour"), W(tfmt(start - d), "counted back instead of forward"), W(tfmt(start + d - 40) if (start % 60) + (d % 60) >= 60 else tfmt(start + d + 10), "did not regroup 60 minutes as 1 hour" if (start % 60) + (d % 60) >= 60 else "miscounted the minutes")],
                FN("time_add", start=tfmt(start), minutes=d), qtype="real-world")


@fam("012", mode="mc")
def tm_clock(r, L):
    h, m = r.randint(1, 12), r.randint(0, 11) * 5
    d = r.randint(2, 9) * 5 if L == 0 else r.randint(7, 19) * 5 if L == 1 else r.randint(20, 40) * 5
    start = h % 12 * 60 + m
    f = lambda t: f"{(t // 60) % 12 or 12}:{t % 60:02d}"
    alt = f"An analog clock. The hour hand points {'at' if m == 0 else 'just past'} {h} and the minute hand points at {m // 5 or 12}. The time is {h}:{m:02d}."
    return Item(f"The clock shows the time now. What time will it be in {dur(d)}?", f(start + d), [f"The clock shows {h}:{m:02d}.", f"Count on {dur(d)}: {f(start + d)}."],
                [W(f(start + d + 60), "counted an extra hour"), W(f(start + d - 5), "miscounted by 5 minutes"), W(f(start - d + 720), "counted back instead of forward"), W(f(start + d + 10), "miscounted the minutes")],
                FN("clock_add", h=h, m=m, minutes=d), qtype="visual", diagram=Diagram("clock", {"h": h, "m": m}, alt))


@fam("012", mode="mc")
def tm_two_events(r, L):
    start, d1 = tcase(r, min(L, 1))
    d2 = r.randint(2, 9) * 5
    nm = name(r)
    end = start + d1 + d2
    return Item(f"{nm} starts homework at {tfmt(start)}. {nm} works on math for {dur(d1)} and then reads for {dur(d2)}. What time does {nm} finish?", tfmt(end),
                [f"Total time: {dur(d1)} + {dur(d2)} = {dur(d1 + d2)}.", f"{dur(d1 + d2)} after {tfmt(start)} is {tfmt(end)}."],
                [W(tfmt(start + d1), "forgot the reading time"), W(tfmt(end + 60), "counted an extra hour"), W(tfmt(start + abs(d1 - d2)) if d1 != d2 else tfmt(end + 15), "subtracted the two times")],
                FN("time_add", start=tfmt(start), minutes=d1 + d2), qtype="multi-step", tags={"multistep"})


# ============================================================== S4 Measurement and Money Word Problems
def usd(c):
    return f"${c // 100}.{c % 100:02d}"


@fam("012")
def wm_money_total(r, L):
    a = r.randint(2, 9) * 100 + pick(r, [25, 50, 75] if L == 0 else list(range(5, 100, 5)) if L == 1 else list(range(1, 100)))
    b = r.randint(1, 9) * 100 + pick(r, [25, 50, 75] if L == 0 else list(range(5, 100, 5)) if L == 1 else list(range(1, 100)))
    i1, i2 = r.sample(["a sandwich", "a juice", "a notebook", "a kite", "a puzzle", "a poster", "a comic book", "a water bottle"], 2)
    return Item(f"{name(r)} buys {i1} for {usd(a)} and {i2} for {usd(b)}. What is the total cost?", usd(a + b), [f"Add the dollars and the cents: {usd(a)} + {usd(b)}.", f"The total is {usd(a + b)}."],
                [W(usd(a + b - 100), "forgot to regroup 100 cents as 1 dollar") if a % 100 + b % 100 >= 100 else W(usd(a + b + 100), "added an extra dollar"), W(usd(abs(a - b)), "subtracted instead of adding"), W(usd(a + b + 10), "made an addition mistake"), W(usd(a + b - 5) if L else usd(a + b + 25), "made an addition mistake with the cents")],
                EX(f"{a / 100:.2f} + {b / 100:.2f}"), qtype="word-problem")


@fam("012")
def wm_change(r, L):
    pay = pick(r, [500, 1000] if L == 0 else [1000, 2000] if L == 1 else [2000, 5000])
    c = r.randint(pay // 5, pay - 26)
    c = c // (25 if L == 0 else 5 if L == 1 else 1) * (25 if L == 0 else 5 if L == 1 else 1)
    need(c % 100)
    thing = pick(r, ["a book", "lunch", "a toy", "art supplies", "a game", "a shirt"])
    return Item(f"{name(r)} buys {thing} for {usd(c)} and pays with a ${pay // 100} bill. How much change should the cashier give back?", usd(pay - c),
                [f"Subtract the cost from the amount paid: ${pay // 100}.00 − {usd(c)}.", f"The change is {usd(pay - c)}."],
                [W(usd(pay - c + 100), "forgot to regroup a dollar"), W(usd(pay + c), "added instead of subtracting"), W(usd(pay - c + 10), "forgot to regroup a dime"), W(usd(pay - c - 100) if pay - c > 100 else usd(pay - c + 5), "made a subtraction mistake")],
                EX(f"{pay // 100} − {c / 100:.2f}"), qtype="word-problem")


@fam("012")
def wm_length(r, L):
    nm = name(r)
    if r.random() < 0.5:
        km, m = r.randint(1, 6), r.randint(1, 9) * 100 + (r.randint(1, 9) * 10 if L else 0)
        v = km * 1000 + m
        return Item(f"{nm} bikes {km} kilometers in the morning and {comma(m)} meters in the afternoon. How many meters does {nm} bike in all?", f"{comma(v)} meters",
                    [f"{km} kilometers = {comma(km * 1000)} meters.", f"{comma(km * 1000)} + {comma(m)} = {comma(v)} meters."],
                    [W(f"{comma(km + m)} meters", "added without converting"), W(f"{comma(km * 100 + m)} meters", "used 100 meters in a kilometer"), W(f"{comma(km * 1000)} meters", "left out the afternoon distance"), W(f"{comma(v + 1000)} meters", "counted an extra kilometer")],
                    EX(f"{km} × 1000 + {m}", unit="meters"), qtype="multi-step", tags={"multistep"})
    ft, pieces = r.randint(3, 9), pick(r, [2, 3, 4, 6])
    v = ft * 12 // pieces
    return Item(f"{nm} has a board that is {ft} feet long. {nm} cuts it into {pieces} equal pieces. How many inches long is each piece?", f"{v} inches",
                [f"{ft} feet = {ft} × 12 = {ft * 12} inches.", f"{ft * 12} ÷ {pieces} = {v} inches."],
                [W(f"{ft * 12} inches", "stopped after converting"), W(f"{ft * 12 * pieces} inches", "multiplied instead of dividing"), W(f"{ft * 10 // pieces} inches" if ft * 10 // pieces != v else f"{v + 1} inches", "used 10 inches in a foot"), W(f"{v + 12} inches", "made a division mistake")],
                FN("split_convert", x=ft, frm="feet", to="inches", pieces=pieces), qtype="multi-step", tags={"multistep"})


@fam("012")
def wm_liquid(r, L):
    liters = r.randint(2, 6)
    each = pick(r, [200, 250, 500] if L < 2 else [125, 200, 250, 400])
    need(liters * 1000 % each == 0)
    v = liters * 1000 // each
    if L == 0:
        ml = r.randint(1, 9) * 100
        return Item(f"A jug holds {liters} liters of juice. {name(r)} pours out {ml} milliliters. How many milliliters of juice are left in the jug?", f"{comma(liters * 1000 - ml)} milliliters",
                    [f"{liters} liters = {comma(liters * 1000)} milliliters.", f"{comma(liters * 1000)} − {ml} = {comma(liters * 1000 - ml)} milliliters."],
                    [W(f"{comma(liters * 1000 + ml)} milliliters", "added instead of subtracting"), W(f"{comma(liters * 100 - ml) if liters * 100 > ml else comma(ml - liters * 100)} milliliters", "used 100 milliliters in a liter"), W(f"{comma(liters * 1000)} milliliters", "stopped after converting")],
                    EX(f"{liters} × 1000 − {ml}", unit="milliliters"), qtype="multi-step", tags={"multistep"})
    return Item(f"A cooler holds {liters} liters of water. How many {each}‑milliliter cups can be filled from the cooler?", f"{v} cups",
                [f"{liters} liters = {comma(liters * 1000)} milliliters.", f"{comma(liters * 1000)} ÷ {each} = {v} cups."],
                [W(f"{liters * 100 // each if liters * 100 // each else v + 2} cups", "used 100 milliliters in a liter"), W(f"{v + 1} cups", "made a division mistake"), W(f"{v * 10} cups", "used the wrong number of zeros"), W(f"{liters * each} cups", "multiplied instead of dividing")],
                EX(f"{liters} × 1000 ÷ {each}", unit="cups"), qtype="multi-step", tags={"multistep"})


@fam("012")
def wm_mass(r, L):
    lb = r.randint(2, 9)
    k = r.randint(2, 6)
    if r.random() < 0.5:
        oz = r.randint(1, 15)
        v = lb * 16 + oz
        return Item(f"A puppy weighed {lb} pounds {oz} ounces at its checkup. How many ounces did the puppy weigh?", f"{v} ounces", [f"{lb} pounds = {lb} × 16 = {lb * 16} ounces.", f"{lb * 16} + {oz} = {v} ounces."],
                    [W(f"{lb * 16} ounces", "forgot to add the extra ounces"), W(f"{lb + oz} ounces", "added without converting"), W(f"{lb * 10 + oz} ounces", "used 10 ounces in a pound"), W(f"{v + 16} ounces", "counted an extra pound")],
                    FN("compound_to_small", big="pounds", small="ounces", a=lb, b=oz), qtype="word-problem")
    g = r.randint(2, 9) * 100 + (50 if L else 0)
    kg = r.randint(1, 4)
    need(kg * 1000 % 1 == 0)
    v = kg * 1000 - g
    return Item(f"A bag holds {kg} kilograms of flour. A baker uses {g} grams. How many grams of flour are left?", f"{comma(v)} grams", [f"{kg} kilograms = {comma(kg * 1000)} grams.", f"{comma(kg * 1000)} − {g} = {comma(v)} grams."],
                [W(f"{comma(kg * 1000 + g)} grams", "added instead of subtracting"), W(f"{comma(abs(kg * 100 - g))} grams", "used 100 grams in a kilogram"), W(f"{comma(kg * 1000)} grams", "stopped after converting"), W(f"{comma(v + 100)} grams", "made a subtraction mistake")],
                EX(f"{kg} × 1000 − {g}", unit="grams"), qtype="multi-step", tags={"multistep"})


@fam("012")
def wm_fraction(r, L):
    n, d = pick(r, [(1, 2), (1, 4), (3, 4)])
    k = r.randint(2, 4) * d if L else d * 2
    kind = r.randrange(3 if L else 2)
    if kind == 0:
        v = F(n, d) * k
        return Item(f"One lap around a track is {n}/{d} mile. {name(r)} runs {k} laps. How many miles is that?", f"{mixed(v)} miles", [f"{k} × {n}/{d} = {k * n}/{d}.", f"{k * n}/{d} = {mixed(v)} miles."],
                    [W(f"{k * n} miles", "ignored the denominator"), W(f"{mixed(v + 1)} miles", "added an extra mile"), W(f"{k + n} miles" if k + n != v else f"{mixed(v + 2)} miles", "added instead of multiplying")],
                    EX(f"{k} × {n}/{d}", unit="miles"), qtype="word-problem", tags={"modeling"})
    if kind == 1:
        v = 60 * n // d
        return Item(f"{name(r)} practices the violin for {n}/{d} hour. How many minutes is that?", f"{v} minutes", [f"1 hour = 60 minutes. 60 ÷ {d} = {60 // d}.", f"{n} × {60 // d} = {v} minutes."],
                    [W(f"{100 * n // d} minutes", "used 100 minutes in an hour"), W(f"{60 // d} minutes" if n > 1 else f"{60 * d} minutes", "used only the denominator" if n > 1 else "multiplied by the denominator"), W(f"{v + 15} minutes", "miscounted"), W("60 minutes", "ignored the fraction")],
                    FN("convert", x=f"{n}/{d}", frm="hours", to="minutes"), qtype="word-problem")
    w = r.randint(1, 3)
    v = w * 60 + 60 * n // d
    return Item(f"A movie is {w} {n}/{d} hours long. How many minutes long is the movie?", f"{v} minutes", [f"{w} hour{'s' if w > 1 else ''} = {w * 60} minutes and {n}/{d} hour = {60 * n // d} minutes.", f"{w * 60} + {60 * n // d} = {v} minutes."],
                [W(f"{w * 60} minutes", "left out the fraction of an hour"), W(f"{w * 100 + 100 * n // d} minutes", "used 100 minutes in an hour"), W(f"{v + 60} minutes", "counted an extra hour"), W(f"{w * 60 + n} minutes", "added the numerator as minutes")],
                FN("convert", x=f"{w} + {n}/{d}", frm="hours", to="minutes"), qtype="multi-step", tags={"multistep"})


# ============================================================== S5 Area and Perimeter of Rectangles
UNITS_L = ["feet", "meters", "inches", "yards", "centimeters"]


def rect_case(r, L):
    w = r.randint(3, 9) if L == 0 else r.randint(6, 25) if L == 1 else r.randint(12, 60)
    h = r.randint(2, 8) if L == 0 else r.randint(3, 12) if L == 1 else r.randint(5, 30)
    need(w != h)
    u = pick(r, UNITS_L)
    return max(w, h), min(w, h), u


def rect_dg(w, h, u, grid=False, wl=None, hl=None):
    wl, hl = wl or f"{w} {u}", hl or f"{h} {u}"
    alt = f"A rectangle. The length is labeled {wl}. The width is labeled {hl}." + (f" It is covered by a grid of {w} by {h} unit squares." if grid else "")
    return Diagram("rect_dims", {"w": w, "h": h, "wl": wl, "hl": hl, "grid": grid}, alt)


@fam("012")
def ap_area(r, L):
    w, h, u = rect_case(r, L)
    return Item(f"What is the area of the rectangle?", f"{comma(w * h)} square {u}", [f"Area = length × width.", f"{w} × {h} = {comma(w * h)} square {u}."],
                [W(f"{2 * (w + h)} square {u}", "found the perimeter instead of the area"), W(f"{w + h} square {u}", "added the length and width"), W(f"{comma(w * h + h)} square {u}", "made a multiplication mistake"), W(f"{comma(2 * w * h)} square {u}", "doubled the area")],
                FN("rect", w=w, h=h, what="area", unit=f"square {u}"), qtype="visual", diagram=rect_dg(w, h, u))


@fam("012")
def ap_perimeter(r, L):
    w, h, u = rect_case(r, L)
    return Item(f"What is the perimeter of the rectangle?", f"{2 * (w + h)} {u}", [f"Perimeter = 2 × length + 2 × width.", f"2 × {w} + 2 × {h} = {2 * w} + {2 * h} = {2 * (w + h)} {u}."],
                [W(f"{comma(w * h)} {u}", "found the area instead of the perimeter"), W(f"{w + h} {u}", "added only two sides"), W(f"{2 * w + h} {u}", "left out one side"), W(f"{2 * (w + h) + 2} {u}", "made an addition mistake")],
                FN("rect", w=w, h=h, what="perimeter", unit=u), qtype="visual", diagram=rect_dg(w, h, u))


@fam("012")
def ap_missing_from_area(r, L):
    w, h, u = rect_case(r, L)
    A = w * h
    thing = pick(r, ["garden", "rug", "poster", "patio", "sandbox", "bulletin board"])
    return Item(f"A rectangular {thing} has an area of {comma(A)} square {u}. Its length is {w} {u}. What is its width?", f"{h} {u}", [f"Area = length × width, so width = area ÷ length.", f"{comma(A)} ÷ {w} = {h} {u}."],
                [W(f"{comma(A - w)} {u}", "subtracted instead of dividing"), W(f"{comma(A * w)} {u}", "multiplied instead of dividing"), W(f"{(A - 2 * w) // 2 if (A - 2 * w) // 2 not in (h, A - w) and A > 2 * w else h + 2} {u}", "used the perimeter formula"), W(f"{h + 1} {u}", "made a division mistake")],
                EX(f"{A} ÷ {w}", unit=u), qtype="word-problem", tags={"reasoning"})


@fam("012")
def ap_missing_from_perimeter(r, L):
    w, h, u = rect_case(r, L)
    P = 2 * (w + h)
    thing = pick(r, ["playground", "picture frame", "garden", "pool", "field", "tabletop"])
    return Item(f"A rectangular {thing} has a perimeter of {P} {u}. Its length is {w} {u}. What is its width?", f"{h} {u}",
                [f"The two lengths use 2 × {w} = {2 * w} {u}.", f"{P} − {2 * w} = {2 * h} {u} for the two widths, and {2 * h} ÷ 2 = {h} {u}."],
                [W(f"{P - w} {u}", "subtracted the length only once"), W(f"{2 * h} {u}", "forgot to divide by 2"), W(f"{P // w} {u}" if P // w not in (h, 2 * h) else f"{h + 3} {u}", "used the area formula"), W(f"{h + 1} {u}", "made a subtraction mistake")],
                EX(f"({P} − 2 × {w}) ÷ 2", unit=u), qtype="multi-step", tags={"multistep", "reasoning"})


@fam("012", mode="mc")
def ap_which_measure(r, L):
    w, h, u = rect_case(r, L)
    kind, s = pick(r, [("perimeter", f"{name(r)} wants to put a fence around a rectangular garden that is {w} {u} long and {h} {u} wide."), ("area", f"{name(r)} wants to cover a rectangular floor that is {w} {u} long and {h} {u} wide with carpet."),
                       ("perimeter", f"{name(r)} wants to glue ribbon around the edge of a rectangular card that is {w} {u} long and {h} {u} wide."), ("area", f"{name(r)} wants to paint a rectangular wall that is {w} {u} long and {h} {u} high.")])
    P, A = 2 * (w + h), w * h
    good = f"Perimeter: {P} {u}" if kind == "perimeter" else f"Area: {comma(A)} square {u}"
    bad = [f"Area: {comma(A)} square {u}" if kind == "perimeter" else f"Perimeter: {P} {u}", f"Perimeter: {w + h} {u}", f"Area: {comma(A + h)} square {u}" if kind == "area" else f"Area: {P} square {u}"]
    return Item(s + " Which measurement is needed, and what is it?", good, [f"{'Going around the outside is perimeter' if kind == 'perimeter' else 'Covering a surface is area'}.", f"{good}."],
                [W(bad[0], "chose the wrong kind of measurement"), W(bad[1], "added only two sides"), W(bad[2], "computed incorrectly")],
                FN("rect_measure", w=w, h=h, kind=kind), qtype="real-world", tags={"modeling", "reasoning"})


@fam("012")
def ap_grid(r, L):
    w, h = r.randint(3, 12), r.randint(2, 8)
    need(w != h)
    what = pick(r, ["area", "perimeter"])
    v = w * h if what == "area" else 2 * (w + h)
    u = "square units" if what == "area" else "units"
    return Item(f"Each small square in the grid is 1 square unit. What is the {what} of the rectangle?", f"{v} {u}",
                [f"The rectangle is {w} units long and {h} units wide.", f"{w} × {h} = {v} square units." if what == "area" else f"2 × {w} + 2 × {h} = {v} units."],
                [W(f"{2 * (w + h) if what == 'area' else w * h} {u}", "mixed up area and perimeter"), W(f"{w + h} {u}", "added only two sides"), W(f"{v + w} {u}", "counted an extra row"), W(f"{v - 2} {u}" if what == "perimeter" else f"{v - h} {u}", "missed part of the figure")],
                FN("rect", w=w, h=h, what=what, unit=u), qtype="visual", diagram=rect_dg(max(w, h), min(w, h), "units", grid=True), tags={"modeling"})


@fam("12")
def ap_same_area(r, L):
    w, h, u = rect_case(r, 1)
    A = w * h
    w2 = pick(r, [x for x in range(2, A) if A % x == 0 and x not in (w, h, 1) and A // x <= 60] or [0])
    need(w2)
    return Item(f"Rectangle A is {w} {u} long and {h} {u} wide. Rectangle B has the same area as Rectangle A, and its length is {w2} {u}. What is the width of Rectangle B?", f"{A // w2} {u}",
                [f"Area of Rectangle A: {w} × {h} = {A} square {u}.", f"Width of Rectangle B: {A} ÷ {w2} = {A // w2} {u}."],
                [W(f"{A} {u}", "gave the area"), W(f"{h} {u}", "used the same width"), W(f"{abs(w + h - w2)} {u}" if abs(w + h - w2) not in (A // w2, h, 0) else f"{A // w2 + 2} {u}", "kept the perimeter the same instead of the area"), W(f"{A // w2 + 1} {u}", "made a division mistake")],
                EX(f"{w} × {h} ÷ {w2}", unit=u), qtype="multi-step", tags={"multistep", "challenge"})


@fam("2")
def ap_lshape(r, L):
    W_, H_ = r.randint(8, 14), r.randint(6, 10)
    nw, nh = r.randint(2, W_ - 3), r.randint(2, H_ - 3)
    u = pick(r, ["feet", "meters"])
    A = W_ * H_ - nw * nh
    alt = (f"An L-shaped figure made from a {W_} by {H_} rectangle with a {nw} by {nh} rectangle removed from the top right corner. Bottom side: {W_} {u}. Left side: {H_} {u}. "
           f"Top side: {W_ - nw} {u}. Right side: {H_ - nh} {u}. The cut-out corner is {nw} {u} wide and {nh} {u} tall.")
    dg = Diagram("rect_dims", {"w": W_, "h": H_, "notch": [nw, nh], "wl": f"{W_} {u}", "hl": f"{H_} {u}", "topl": f"{W_ - nw} {u}", "nwl": f"{nw} {u}", "nhl": f"{nh} {u}", "rightl": f"{H_ - nh} {u}"}, alt)
    return Item(f"The floor of a room is shaped like the figure. All the corners are right angles. What is the area of the floor?", f"{A} square {u}",
                [f"One way: find the large rectangle, {W_} × {H_} = {W_ * H_}, and subtract the missing corner, {nw} × {nh} = {nw * nh}.", f"{W_ * H_} − {nw * nh} = {A} square {u}."],
                [W(f"{W_ * H_} square {u}", "did not subtract the missing corner"), W(f"{2 * (W_ + H_)} square {u}", "found the perimeter"), W(f"{W_ * H_ + nw * nh} square {u}", "added the corner instead of subtracting it"), W(f"{(W_ - nw) * H_} square {u}", "used only one part of the figure")],
                FN("lshape_area", W=W_, H=H_, nw=nw, nh=nh, unit=f"square {u}"), qtype="multi-step", diagram=dg, tags={"multistep", "challenge"})


@fam("012")
def ap_square(r, L):
    s = r.randint(3, 9) if L == 0 else r.randint(11, 25) if L == 1 else r.randint(15, 60)
    u = pick(r, UNITS_L)
    what = pick(r, ["area", "perimeter"])
    if L == 2 and r.random() < 0.5:
        P = 4 * s
        it = Item(f"A square has a perimeter of {P} {u}. What is the area of the square?", f"{comma(s * s)} square {u}", [f"Each side is {P} ÷ 4 = {s} {u}.", f"Area = {s} × {s} = {comma(s * s)} square {u}."],
                    [W(f"{s} square {u}", "stopped after finding the side length"), W(f"{comma(P * P)} square {u}", "multiplied the perimeter by itself"), W(f"{P} square {u}", "gave the perimeter"), W(f"{2 * s} square {u}", "doubled the side instead of multiplying it by itself")],
                    EX(f"({P} ÷ 4) × ({P} ÷ 4)", unit=f"square {u}"), qtype="multi-step", tags={"multistep", "challenge"})
        it.consts = [4]
        return it
    v, uu = (s * s, f"square {u}") if what == "area" else (4 * s, u)
    it = Item(f"A square has sides that are {s} {u} long. What is the {what} of the square?", f"{comma(v)} {uu}", [f"All four sides of a square are {s} {u}.", f"{s} × {s} = {comma(v)} {uu}." if what == "area" else f"4 × {s} = {v} {uu}."],
                [W(f"{comma(4 * s if what == 'area' else s * s)} {uu}", "mixed up area and perimeter"), W(f"{2 * s} {uu}", "used only two sides"), W(f"{comma(v + s)} {uu}", "made a multiplication mistake"), W(f"{s} {uu}", "gave the side length")],
                EX(f"{s} × {s}" if what == "area" else f"4 × {s}", unit=uu), qtype="procedural")
    it.consts = [4]
    return it


SKILLS = {
    1: dict(name="Customary Units and Conversions", fams=[cu_convert, cu_table, cu_compare, cu_mixed, cu_sense, cu_word]),
    2: dict(name="Metric Units and Conversions", fams=[me_convert, me_table, me_compare, me_mixed, me_sense, me_word, me_fraction]),
    3: dict(name="Time and Elapsed Time", fams=[tm_convert, tm_elapsed_minutes, tm_elapsed_hm, tm_end, tm_clock, tm_two_events]),
    4: dict(name="Measurement and Money Word Problems", fams=[wm_money_total, wm_change, wm_length, wm_liquid, wm_mass, wm_fraction]),
    5: dict(name="Area and Perimeter of Rectangles", fams=[ap_area, ap_perimeter, ap_missing_from_area, ap_missing_from_perimeter, ap_which_measure, ap_grid, ap_same_area, ap_lshape, ap_square]),
}
