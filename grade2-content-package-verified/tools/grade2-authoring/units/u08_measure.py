"""Unit 8: Measuring Length (measuring-length). 2.MD.A.1-4, 2.MD.D.9."""
from g2lib import *

UNIT_ID = "measuring-length"

SHORT = ["pencil", "crayon", "marker", "key", "eraser", "spoon", "leaf", "feather", "ribbon", "paper strip", "straw", "nail", "comb", "toy car"]
# typical lengths: (object, inches, centimeters, curved) — benchmark values used by the estimate and tool items
OBJ = {"eraser": (2, 5, False), "paper clip": (1, 3, False), "crayon": (3, 8, False), "pencil": (7, 18, False), "book": (10, 25, False),
       "shoe": (9, 23, False), "spoon": (6, 15, False), "desk": (36, 90, False), "door": (80, 200, False), "classroom": (360, 900, False),
       "hallway": (1200, 3000, False), "school bus": (480, 1200, False), "car": (170, 430, False), "bed": (75, 190, False), "baseball bat": (32, 80, False),
       "waist": (24, 60, True), "tree trunk": (60, 150, True), "pumpkin": (40, 100, True), "head": (20, 52, True)}
TOOLS = ["ruler", "yardstick", "meter stick", "measuring tape"]


def unit_of(L, r):
    return pick(r, ["inches", "centimeters"])


# ============================================================== S1 Measuring with a Ruler
def ruler_item(r, L):
    unit = unit_of(L, r)
    Lr = 12 if unit == "inches" else 15
    ln = r.randint(2, Lr - 1)
    start = 0 if L == 0 else (r.randint(1, Lr - ln) if L == 2 or r.random() < 0.5 else 0)
    need(start + ln <= Lr)
    obj = pick(r, SHORT)
    return unit, Lr, start, start + ln, obj


@fam("012")
def ru_read(r, L):
    unit, Lr, s0, e, obj = ruler_item(r, L)
    alt = f"{Art(obj)} above a ruler marked in {unit} from 0 to {Lr}. The {obj} starts at the {s0} mark and ends at the {e} mark."
    ln = e - s0
    return Item(f"How long is the {obj}?", f"{ln} {unit}", [f"The {obj} goes from {s0} to {e}." if s0 else f"The {obj} starts at 0 and ends at {e}.", f"Count the spaces: {e} − {s0} = {ln} {unit}." if s0 else f"It is {ln} {unit} long."],
                [W(f"{e} {unit}", "read the end mark without starting at 0") if s0 else W(f"{ln + 1} {unit}", "counted the tick marks instead of the spaces"), W(f"{ln - 1} {unit}", "started counting at 1"), W(f"{ln} {'centimeters' if unit == 'inches' else 'inches'}", "used the wrong unit")],
                FN("measure2", start=s0, end=e, unit=unit), qtype="visual",
                diagram=Diagram("ruler2", {"length": Lr, "unit": unit, "objects": [{"start": s0, "end": e, "label": obj}]}, alt))


@fam("12")
def ru_offset(r, L):
    unit = unit_of(L, r)
    Lr = 12 if unit == "inches" else 15
    s0 = r.randint(1, 5)
    e = r.randint(s0 + 2, Lr)
    obj = pick(r, SHORT)
    alt = f"{Art(obj)} above a ruler marked in {unit} from 0 to {Lr}. The {obj} starts at the {s0} mark and ends at the {e} mark."
    return Item(f"The {obj} does not start at 0. How long is it?", f"{e - s0} {unit}", [f"It goes from {s0} to {e}.", f"{e} − {s0} = {e - s0} {unit}."],
                [W(f"{e} {unit}", "read the end mark"), W(f"{e - s0 + 1} {unit}", "counted the tick marks"), W(f"{e + s0} {unit}", "added the marks")],
                FN("measure2", start=s0, end=e, unit=unit), qtype="visual",
                diagram=Diagram("ruler2", {"length": Lr, "unit": unit, "objects": [{"start": s0, "end": e, "label": obj}]}, alt))


@fam("012")
def ru_two(r, L):
    unit = unit_of(L, r)
    Lr = 12 if unit == "inches" else 15
    a, b = r.randint(3, Lr), r.randint(2, Lr - 1)
    s1 = 0 if L == 0 else r.randint(0, 3)
    need(s1 + b <= Lr and a != b)
    o1, o2 = r.sample(SHORT, 2)
    which = pick(r, [0, 1])
    ln = a if which == 0 else b
    alt = f"Two objects above a ruler marked in {unit}. The {o1} goes from 0 to {a}. The {o2} goes from {s1} to {s1 + b}."
    return Item(f"How long is the {[o1, o2][which]}?", f"{ln} {unit}", [f"The {[o1, o2][which]} goes from {[0, s1][which]} to {[a, s1 + b][which]}.", f"It is {ln} {unit} long."],
                [W(f"{[b, a][which]} {unit}", "measured the other object"), W(f"{ln + 1} {unit}", "counted the tick marks"), W(f"{s1 + b} {unit}", "read the end mark") if which == 1 and s1 else W(f"{ln - 1} {unit}", "started at 1")],
                FN("measure2", start=[0, s1][which], end=[a, s1 + b][which], unit=unit), qtype="visual",
                diagram=Diagram("ruler2", {"length": Lr, "unit": unit, "objects": [{"start": 0, "end": a, "label": o1}, {"start": s1, "end": s1 + b, "label": o2}]}, alt))


@fam("012", mode="mc")
def ru_how(r, L):
    obj = pick(r, SHORT)
    good = "Line up one end of the object with 0 and read the number at the other end."
    bad = ["Line up one end of the object with 1 and read the number at the other end.", "Count all the tick marks under the object.", "Line up the middle of the object with 0."]
    if L:
        good = "Line up one end with a mark, then count the units from that mark to the other end."
        bad[0] = "Read the number at the end of the object, even if it does not start at 0."
    it = mc_key(f"What is the right way to measure {art(obj)} with a ruler?", good, bad, ["Measuring counts the units (spaces) the object covers.", good], qtype="conceptual", r=r)
    return it


@fam("012")
def ru_mark(r, L):
    unit = unit_of(L, r)
    s0 = 0 if L == 0 else r.randint(1, 6)
    e = s0 + r.randint(2, 9)
    obj = pick(r, SHORT)
    return Item(f"{Art(obj)} lies along a ruler. One end is at the {s0} mark and the other end is at the {e} mark. How long is the {obj} in {unit}?", f"{e - s0} {unit}",
                [f"Count the {unit} from {s0} to {e}.", f"{e} − {s0} = {e - s0} {unit}."],
                [W(f"{e} {unit}", "read only the end mark") if s0 else W(f"{e + 1} {unit}", "counted the tick marks"), W(f"{e + s0} {unit}", "added the marks"), W(f"{e - s0 + 1} {unit}", "counted the tick marks")],
                FN("measure2", start=s0, end=e, unit=unit), qtype="procedural", claim=f"Length from the {s0} mark to the {e} mark")


@fam("012", mode="mc")
def ru_error(r, L):
    unit = unit_of(L, r)
    Lr = 12 if unit == "inches" else 15
    s0 = r.randint(1, 4)
    e = r.randint(s0 + 3, Lr)
    obj = pick(r, SHORT)
    nm = name(r)
    alt = f"{Art(obj)} above a ruler marked in {unit} from 0 to {Lr}. The {obj} starts at the {s0} mark and ends at the {e} mark."
    good = f"No. The {obj} starts at {s0}, so it is {e - s0} {unit} long."
    bad = [f"Yes. The {obj} ends at {e}.", f"No. It is {e + s0} {unit} long.", f"No. It is {e - s0 + 1} {unit} because you count every mark."]
    it = mc_key(f"{nm} says the {obj} is {e} {unit} long. Is {nm} right?", good, bad, [f"The {obj} goes from {s0} to {e}.", f"{e} − {s0} = {e - s0} {unit}."], qtype="error-analysis", tags={"misconception"}, r=r,
                diagram=Diagram("ruler2", {"length": Lr, "unit": unit, "objects": [{"start": s0, "end": e, "label": obj}]}, alt))
    it.check = FN("measure_claim", start=s0, end=e, unit=unit, obj=obj)
    return it


# ============================================================== S2 Choosing a Measuring Tool and Unit
def best_tool(inches, curved):
    if curved:
        return "measuring tape"
    if inches <= 12:
        return "ruler"
    if inches <= 40:
        return "yardstick or meter stick"
    return "measuring tape"


@fam("012", mode="mc")
def tl_tool(r, L):
    obj = pick(r, [o for o in OBJ if L or not OBJ[o][2]])
    inch, cm, curved = OBJ[obj]
    good = best_tool(inch, curved)
    opts = ["ruler", "yardstick or meter stick", "measuring tape", "a paper clip"]
    q = f"Which tool is best for measuring {'around ' if curved else 'the length of '}{art(obj)}?"
    it = mc_key(q, good, [o for o in opts if o != good], [f"A ruler is 12 inches; a yardstick is 36 inches, a meter stick is 100 centimeters, and the measuring tape is long and bends.", f"The best tool is a {good}."], r=r)
    it.check = FN("best_tool", inches=inch, curved=curved)
    return it


@fam("012", mode="mc")
def tl_unit(r, L):
    obj = pick(r, [o for o in OBJ if not OBJ[o][2]])
    inch, cm, _ = OBJ[obj]
    sys_ = pick(r, ["us", "metric"])
    if sys_ == "us":
        good = "inches" if inch < 24 else "feet"
        opts = ["inches", "feet"]
    else:
        good = "centimeters" if cm < 100 else "meters"
        opts = ["centimeters", "meters"]
    it = mc_key(f"Which unit is better for measuring the length of the {obj}: {opts[0]} or {opts[1]}?", good, [o for o in opts if o != good] + ["cups", "pounds"] if L == 0 else [o for o in opts if o != good] + ["grams" if sys_ == "metric" else "pounds", "liters" if sys_ == "metric" else "cups"],
                [f"Use smaller units for shorter objects and bigger units for longer objects.", f"{Art(obj)} is best measured in {good}."], r=r)
    it.check = FN("best_unit", inches=inch, cm=cm, system=sys_)
    return it


@fam("012")
def tl_ruler_count(r, L):
    k = r.randint(2, 5) if L == 0 else r.randint(3, 9)
    tool, size, unit = pick(r, [("12-inch ruler", 12, "inches"), ("meter stick", 100, "centimeters")]) if L else ("12-inch ruler", 12, "inches")
    need(size * k <= 1000)
    nm = name(r)
    return Item(f"{nm} measures a rug with a {tool}. The {tool} fits end to end {k} times with no gaps. How long is the rug in {unit}?", f"{size * k} {unit}",
                [f"Each {tool} is {size} {unit}.", f"Add {size} {k} times: {' + '.join([str(size)] * k)} = {size * k} {unit}."],
                [W(f"{k} {unit}", "counted the rulers, not the units"), W(f"{size * (k + 1)} {unit}", "counted one extra"), W(f"{size + k} {unit}", "added the two numbers")],
                EX("+".join([str(size)] * k), unit=unit), qtype="word-problem", tags={"modeling"})


@fam("12", mode="mc")
def tl_why(r, L):
    obj = pick(r, ["hallway", "classroom", "school bus"])
    good = f"A measuring tape, because it is long and does not need to be moved many times."
    bad = ["A ruler, because it has the most marks.", "A paper clip, because it is the smallest unit.", "A ruler, because it is easy to carry."]
    it = mc_key(f"{name(r)} wants to measure the length of the {obj}. Which tool is the best choice, and why?", good, bad,
                [f"{Art(obj)} is very long.", "A long tool means fewer moves and fewer mistakes."], qtype="explain", tags={"reasoning"}, r=r)
    return it


@fam("2", mode="mc")
def tl_mixed(r, L):
    a, b = r.sample([o for o in OBJ if not OBJ[o][2]], 2)
    need(abs(OBJ[a][0] - OBJ[b][0]) > 10)
    short, long_ = (a, b) if OBJ[a][0] < OBJ[b][0] else (b, a)
    need(OBJ[short][0] < 24 <= OBJ[long_][0])
    good = f"inches for the {short} and feet for the {long_}"
    bad = [f"feet for the {short} and inches for the {long_}", f"feet for both", f"pounds for both"]
    it = mc_key(f"{name(r)} will measure a {a} and also a {b}. Which units make the most sense?", good, bad, ["Small units fit short objects; bigger units fit long objects.", good + "."], qtype="conceptual", tags={"reasoning"}, r=r)
    it.check = FN("pair_units", short=OBJ[short][0], long=OBJ[long_][0])
    return it


@fam("012", mode="sa")
def tl_tool_sa(r, L):
    obj = pick(r, [o for o in OBJ if L or not OBJ[o][2]])
    inch, cm, curved = OBJ[obj]
    good = best_tool(inch, curved)
    return Item(f"Name the best tool for measuring {'around ' if curved else 'the length of '}{art(obj)}: ruler, yardstick or meter stick, or measuring tape.", good,
                ["A ruler is short, a yardstick or meter stick is medium, and the measuring tape is long and bends.", f"The best tool is a {good}."],
                [W(x, "chose a tool that does not fit the length") for x in ("ruler", "yardstick or meter stick", "measuring tape") if x != good],
                FN("best_tool", inches=inch, curved=curved), qtype="conceptual")


@fam("012", mode="sa")
def tl_unit_sa(r, L):
    obj = pick(r, [o for o in OBJ if not OBJ[o][2]])
    inch, cm, _ = OBJ[obj]
    sys_ = pick(r, ["us", "metric"])
    opts = ["inches", "feet"] if sys_ == "us" else ["centimeters", "meters"]
    good = (opts[0] if inch < 24 else opts[1]) if sys_ == "us" else (opts[0] if cm < 100 else opts[1])
    return Item(f"Would you measure the length of the {obj} in {opts[0]} or {opts[1]}?", good, ["Short objects: small units. Long objects: big units.", f"Use {good}."],
                [W([o for o in opts if o != good][0], "chose a unit that does not fit the length")], FN("best_unit", inches=inch, cm=cm, system=sys_), qtype="conceptual")


# ============================================================== S3 Measuring with Different Units
PAIRS = [("inches", "feet", 12), ("centimeters", "meters", 100), ("paper clips", "pencils", None), ("cubes", "craft sticks", None)]


@fam("012")
def du_more(r, L):
    small, big, f = pick(r, PAIRS[:2] if L else PAIRS[2:])
    obj = pick(r, ["table", "rug", "board", "bench"])
    k = r.randint(2, 6)
    n = k * (f or r.randint(3, 5))
    which = pick(r, [small, big])
    ans = n if which == small else k
    return Item(f"{name(r)} measured a {obj} two ways. One measurement is {k} and the other is {n}. Which number goes with {which}?", ans,
                [f"{small.capitalize()} are shorter than {big}.", f"It takes more units when each unit is shorter, so {n} goes with {small} and {k} goes with {big}."],
                [W(k if ans == n else n, "thought a bigger unit gives a bigger number"), W(n - k, "subtracted the two numbers"), W(n + k, "added the two numbers")],
                FN("unit_number", small=small, big=big, nums=[k, n], which=which), qtype="conceptual", tags={"reasoning"})


@fam("012", mode="mc")
def du_why(r, L):
    small, big, f = pick(r, PAIRS)
    k = r.randint(2, 6)
    n = k * (f or r.randint(3, 5))
    obj = pick(r, ["desk", "shelf", "rope"])
    good = f"{small.capitalize()} are shorter than {big}, so it takes more {small} to cover the same length."
    bad = [f"The {obj} is longer when it is measured in {small}.", f"Someone made a mistake; the numbers should be the same.", f"{big.capitalize()} are shorter than {small}, so it takes more {big}."]
    it = mc_key(f"{Art(obj)} is {k} {big} long. It is also {n} {small} long. Why is the number of {small} greater?", good, bad, ["The length does not change. The unit size changes.", good], qtype="explain", tags={"reasoning"}, r=r)
    it.check = FN("smaller_more", small=small, big=big, text=good)
    return it


@fam("012")
def du_clips(r, L):
    a = r.randint(2, 5)
    m = r.randint(2, 4)
    obj = pick(r, ["book", "lunch box", "tablet", "tray"])
    u1, u2 = pick(r, [("pencils", "paper clips"), ("craft sticks", "cubes"), ("hands", "fingers")])
    nm = name(r)
    which = pick(r, ["longer", "shorter"])
    ans = u1 if which == "longer" else u2
    return Item(f"{nm} measured {art(obj)}. It was {a} {u1} long and {a * m} {u2} long. Which unit is {which}, {u1} or {u2}?", ans,
                [f"The same length took more {u2}, so each {u2[:-1] if u2.endswith('s') else u2} is shorter.", f"So {u1} are longer and {u2} are shorter."],
                [W(u2 if ans == u1 else u1, "thought more units means bigger units")], FN("unit_size", counts={u1: a, u2: a * m}, which=which), qtype="conceptual", tags={"reasoning"})


@fam("012", mode="mc")
def du_cm_m(r, L):
    k = r.randint(1, 3) if L == 0 else r.randint(1, 5)
    obj = pick(r, ["table", "rug", "jump rope", "board"])
    sysu = pick(r, ["m", "ft"])
    if sysu == "m":
        good, bad = f"{100 * k} centimeters", [f"{k} centimeters", f"{10 * k} centimeters", f"{k + 100} centimeters"]
        q = f"{Art(obj)} is {pl(k, 'meter')} long. 1 meter = 100 centimeters. How long is the {obj} in centimeters?"
        chk = FN("rep_unit", count=k, size=100, unit="centimeters")
    else:
        good, bad = f"{12 * k} inches", [f"{k} inches", f"{k + 12} inches", f"{10 * k} inches"]
        q = f"{Art(obj)} is {k} {'foot' if k == 1 else 'feet'} long. 1 foot = 12 inches. How long is the {obj} in inches?"
        chk = FN("rep_unit", count=k, size=12, unit="inches")
    need(len(set(bad)) == 3 and good not in bad)
    it = mc_key(q, good, bad, ["Add the size of one big unit once for each big unit.", good + "."], qtype="procedural", r=r)
    it.check = chk
    return it


@fam("2")
def du_predict(r, L):
    k = r.randint(2, 4)
    obj = pick(r, ["table", "rug", "jump rope"])
    nm = name(r)
    return Item(f"{nm} measured a {obj} using a 12-inch ruler and moved it {k} times end to end. Then {nm} measured it in feet. 1 foot = 12 inches. How many feet long is the {obj}?", f"{k} feet" if k > 1 else "1 foot",
                [f"Each 12-inch ruler is 1 foot.", f"{k} rulers = {k} feet."],
                [W(f"{12 * k} feet", "used the number of inches"), W(f"{k + 12} feet", "added the numbers"), W(f"{k * 10} feet", "thought 1 foot is 10 inches")],
                FN("rep_unknown", total=12 * k, times=12, unit="feet"), qtype="explain", tags={"reasoning"})


@fam("012")
def du_eraser(r, L):
    k = r.randint(3, 6) if L == 0 else r.randint(4, 9)
    size = r.randint(2, 3) if L == 0 else r.randint(2, 5)
    obj = pick(r, ["book", "tray", "box", "notebook"])
    u = pick(r, ["inches", "centimeters"])
    return Item(f"{Art(obj)} is {k} erasers long. Each eraser is {size} {u} long. How long is the {obj} in {u}?", f"{k * size} {u}",
                [f"Add {size} once for each eraser: {' + '.join([str(size)] * k)}.", f"The {obj} is {k * size} {u} long."],
                [W(f"{k} {u}", "counted erasers, not units"), W(f"{k + size} {u}", "added the two numbers"), W(f"{(k + 1) * size} {u}", "counted one extra eraser")],
                EX("+".join([str(size)] * k), unit=u), qtype="word-problem", tags={"modeling"})


# ============================================================== S4 Estimating Lengths
def est_opts(obj, r, sys_):
    inch, cm, _ = OBJ[obj]
    if sys_ == "us":
        good = f"about {inch} inches" if inch < 24 else f"about {round(inch / 12)} feet"
        u = "inches" if inch < 24 else "feet"
        v = inch if inch < 24 else round(inch / 12)
        bad = [f"about {v} {'feet' if u == 'inches' else 'inches'}", f"about {v * 10} {u}", f"about {max(1, v // 10) if v >= 10 else v + 20} {u}"]
    else:
        good = f"about {cm} centimeters" if cm < 100 else f"about {round(cm / 100)} meters"
        u = "centimeters" if cm < 100 else "meters"
        v = cm if cm < 100 else round(cm / 100)
        bad = [f"about {v} {'meters' if u == 'centimeters' else 'centimeters'}", f"about {v * 10} {u}", f"about {max(1, v // 10) if v >= 10 else v + 40} {u}"]
    return good, bad, u, v


@fam("012", mode="mc")
def es_best(r, L):
    obj = pick(r, [o for o in OBJ if not OBJ[o][2] and o not in ("hallway", "classroom")])
    sys_ = pick(r, ["us", "metric"])
    good, bad, u, v = est_opts(obj, r, sys_)
    need(len(set(bad)) == 3 and good not in bad)
    it = mc_key(f"Which is the best estimate for the length of the {obj}?", good, bad,
                ["Use benchmarks: a paper clip is about 1 inch, a fingertip is about 1 centimeter, a long step is about 1 meter; a ruler is 1 foot.", f"{Art(obj)} is {good}."], r=r)
    it.check = FN("estimate_len", inches=OBJ[obj][0], cm=OBJ[obj][1])
    return it


@fam("012", mode="mc")
def es_unit(r, L):
    obj = pick(r, [o for o in OBJ if not OBJ[o][2] and o not in ("hallway", "classroom")])
    sys_ = pick(r, ["us", "metric"])
    good, bad, u, v = est_opts(obj, r, sys_)
    opts = ["inches", "feet", "centimeters", "meters"]
    it = mc_key(f"{Art(obj)} is about {v} ___ long. Which unit makes sense?", u, [o for o in opts if o != u], [f"Think about how long 1 {dict(inches='inch', feet='foot', centimeters='centimeter', meters='meter')[u]} is.", f"{Art(obj)} is about {v} {u}."], r=r)
    it.check = FN("estimate_unit", inches=OBJ[obj][0], cm=OBJ[obj][1], v=v)
    return it


@fam("012")
def es_bench(r, L):
    k = r.randint(3, 9)
    b, unit = pick(r, [("paper clip", "inches"), ("fingertip", "centimeters")]) if L else ("paper clip", "inches")
    obj = pick(r, ["pencil", "marker", "spoon", "comb", "book"])
    return Item(f"A {b} is about 1 {dict(inches='inch', centimeters='centimeter')[unit]} long. A {obj} is about {k} {b}s long. About how many {unit} long is the {obj}?", f"{k} {unit}",
                [f"Each {b} is about 1 {dict(inches='inch', centimeters='centimeter')[unit]}.", f"{k} {b}s are about {k} {unit}."],
                [W(f"{k + 1} {unit}", "counted one extra"), W(f"{10 * k} {unit}", "thought each one is 10 units"), W(f"{k} {'feet' if unit == 'inches' else 'meters'}", "used the wrong unit")],
                FN("rep_unit", count=k, size=1, unit=unit), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def es_reason(r, L):
    obj = pick(r, ["door", "car", "bed", "school bus"])
    inch, cm, _ = OBJ[obj]
    v = round(cm / 100)
    nm = name(r)
    good = f"No. A {obj} is about {v} meters long, so {v} centimeters is much too short."
    bad = [f"Yes. {v} centimeters is a good estimate.", f"No. It should be {v} inches.", f"Yes. All objects can be measured in centimeters."]
    it = mc_key(f"{nm} says {art(obj)} is about {v} centimeters long. Is that a reasonable estimate?", good, bad, ["1 centimeter is about the width of a fingertip.", good], qtype="error-analysis", tags={"misconception"}, r=r)
    return it


@fam("012")
def es_steps(r, L):
    k = r.randint(4, 12)
    nm = name(r)
    return Item(f"{nm}'s long step is about 1 meter. {nm} walks across a stage in {k} long steps. About how long is the stage, in meters?", f"{k} meters",
                [f"Each long step is about 1 meter.", f"{k} steps are about {k} meters."],
                [W(f"{k} centimeters", "used the wrong unit"), W(f"{100 * k} meters", "multiplied by 100"), W(f"{k + 1} meters", "counted one extra step")],
                FN("rep_unit", count=k, size=1, unit="meters"), qtype="word-problem", tags={"modeling"})


# ============================================================== S5 How Much Longer?
@fam("012")
def hl_ruler(r, L):
    unit = unit_of(L, r)
    Lr = 12 if unit == "inches" else 15
    a, b = r.randint(4, Lr), r.randint(2, Lr - 2)
    need(a - b >= 1)
    o1, o2 = r.sample(SHORT, 2)
    alt = f"Two objects above a ruler marked in {unit}, both starting at 0. The {o1} ends at {a}. The {o2} ends at {b}."
    return Item(f"How much longer is the {o1} than the {o2}?", f"{a - b} {unit}", [f"The {o1} is {a} {unit}; the {o2} is {b} {unit}.", f"{a} − {b} = {a - b} {unit}."],
                [W(f"{a + b} {unit}", "added the lengths"), W(f"{a} {unit}", "gave the longer length"), W(f"{a - b + 1} {unit}", "counted the tick marks")],
                EX(f"{a}-{b}", unit=unit), qtype="visual",
                diagram=Diagram("ruler2", {"length": Lr, "unit": unit, "objects": [{"start": 0, "end": a, "label": o1}, {"start": 0, "end": b, "label": o2}]}, alt))


@fam("012")
def hl_word(r, L):
    unit = pick(r, ["inches", "centimeters", "feet", "meters"]) if L else pick(r, ["inches", "centimeters"])
    a, b = (r.randint(8, 30), r.randint(3, 20)) if L == 0 else (r.randint(20, 95), r.randint(10, 60))
    need(a - b >= 2)
    o1, o2 = pick(r, [("blue ribbon", "red ribbon"), ("snake", "worm"), ("green rope", "yellow rope"), ("boat", "raft")])
    return Item(f"The {o1} is {a} {unit} long. The {o2} is {b} {unit} long. How much longer is the {o1}?", f"{a - b} {unit}",
                [f"Compare: {a} − {b}.", f"{a} − {b} = {a - b} {unit}."],
                [W(f"{a + b} {unit}", "added the lengths"), W(f"{a - b + 10} {unit}", "made a regrouping mistake"), W(f"{a} {unit}", "gave the longer length")],
                EX(f"{a}-{b}", unit=unit), qtype="word-problem", tags={"modeling"})


@fam("012", mode="mc")
def hl_mc(r, L):
    unit = unit_of(L, r)
    a, b = r.randint(5, 40), r.randint(3, 30)
    need(a - b >= 2)
    nm1, nm2 = name(r), name(sub(r, 2))
    need(nm1 != nm2)
    return Item(f"{nm1}'s paper strip is {a} {unit} long. {nm2}'s strip is {b} {unit} long. How much longer is {nm1}'s strip?", f"{a - b} {unit}",
                [f"{a} − {b}.", f"{a} − {b} = {a - b} {unit}."], [W(f"{a + b} {unit}", "added the lengths"), W(f"{a - b + 1} {unit}", "counted one extra"), W(f"{b} {unit}", "gave the shorter length")],
                EX(f"{a}-{b}", unit=unit), qtype="word-problem", mode="mc")


@fam("012", mode="mc")
def hl_units(r, L):
    n = r.randint(5, 30)
    o1, o2 = pick(r, [("crayon box", "pencil case"), ("leaf", "shell")])
    good = f"The {o1}, because 1 inch is longer than 1 centimeter"
    bad = [f"The {o2}, because 1 centimeter is longer than 1 inch", "They are the same length, because the numbers are the same", f"The {o2}, because centimeters are bigger"]
    it = mc_key(f"The {o1} is {n} inches long. The {o2} is {n} centimeters long. Which is longer?", good, bad, ["The numbers are the same, but the units are not.", "An inch is longer than a centimeter."], qtype="explain", tags={"reasoning"}, r=r)
    return it


@fam("2")
def hl_unknown(r, L):
    a, d = r.randint(20, 70), r.randint(5, 25)
    unit = pick(r, ["inches", "centimeters"])
    nm = name(r)
    return Item(f"{nm}'s plant is {a} {unit} tall. It is {d} {unit} shorter than the sunflower. How tall is the sunflower?", f"{a + d} {unit}",
                [f"The sunflower is {d} {unit} taller: {a} + {d}.", f"{a} + {d} = {a + d} {unit}."],
                [W(f"{a - d} {unit}", "subtracted because the story says “shorter”"), W(f"{a} {unit}", "gave the plant's height"), W(f"{a + d + 10} {unit}", "made a regrouping mistake")],
                EX(f"{a}+{d}", unit=unit), qtype="word-problem", tags={"modeling", "misconception"})


@fam("012")
def hl_three(r, L):
    a, b, c = r.sample(range(12, 60), 3)
    unit = pick(r, ["inches", "centimeters"])
    names_ = ["Mia", "Leo", "Ivy"]
    return Item(f"Three snakes are {a}, {b}, and {c} {unit} long. How much longer is the longest snake than the shortest snake?", f"{max(a, b, c) - min(a, b, c)} {unit}",
                [f"Longest: {max(a, b, c)}. Shortest: {min(a, b, c)}.", f"{max(a, b, c)} − {min(a, b, c)} = {max(a, b, c) - min(a, b, c)} {unit}."],
                [W(f"{max(a, b, c) - sorted([a, b, c])[1]} {unit}", "compared the wrong snakes"), W(f"{a + b + c} {unit}", "added all three"), W(f"{max(a, b, c)} {unit}", "gave the longest length")],
                EX(f"{max(a, b, c)}-{min(a, b, c)}", unit=unit), qtype="multi-step", tags={"multistep"})


# ============================================================== S6 Line Plots of Measurements
def lp_data(r, L):
    lo = r.randint(2, 6)
    span = 4 if L == 0 else 6
    n = r.randint(6, 9) if L == 0 else r.randint(9, 14)
    vals = sorted(r.randint(lo, lo + span - 1) for _ in range(n))
    need(len(set(vals)) >= 3)
    return lo, lo + span, vals


PLURAL = {"leaf": "leaves", "shoe": "shoes"}


def pls(obj):
    return PLURAL.get(obj, obj + "s")


def lp_diag(lo, hi, vals, obj, unit):
    alt = f"A line plot titled {obj.capitalize()} Lengths, from {lo} to {hi} {unit}. X marks: " + ", ".join(f"{vals.count(v)} at {v}" for v in range(lo, hi + 1) if vals.count(v)) + "."
    return Diagram("lineplot", {"lo": str(lo), "hi": str(hi), "den": 1, "values": [str(v) for v in vals], "title": f"{obj.capitalize()} Lengths", "unit": f"Length ({unit})"}, alt)


@fam("012")
def lp_at(r, L):
    lo, hi, vals = lp_data(r, L)
    obj, unit = pick(r, [("pencil", "inches"), ("leaf", "centimeters"), ("shoe", "inches"), ("crayon", "centimeters")])
    x = pick(r, sorted(set(vals)))
    k = vals.count(x)
    return Item(f"The line plot shows the lengths of some {pls(obj)}. How many {pls(obj)} are {x} {unit} long?", k,
                [f"Count the X marks above {x}.", f"There are {k}."], [W(x, "gave the length instead of the count"), W(k + 1, "counted an extra X"), W(len(vals), "counted all the X marks")],
                FN("lp", values=[str(v) for v in vals], op="count_at", x=str(x)), qtype="visual", diagram=lp_diag(lo, hi, vals, obj, unit))


@fam("012")
def lp_n(r, L):
    lo, hi, vals = lp_data(r, L)
    obj, unit = pick(r, [("pencil", "inches"), ("leaf", "centimeters"), ("ribbon", "inches"), ("stick", "centimeters")])
    return Item(f"The line plot shows the lengths of some {pls(obj)}. How many {pls(obj)} were measured in all?", len(vals),
                ["Each X is one object.", f"There are {len(vals)} X marks."], [W(len(set(vals)), "counted the lengths, not the X marks"), W(len(vals) - 1, "missed an X"), W(hi, "gave the biggest number on the line")],
                FN("lp", values=[str(v) for v in vals], op="n"), qtype="visual", diagram=lp_diag(lo, hi, vals, obj, unit))


@fam("012", mode="mc")
def lp_mode(r, L):
    lo, hi, vals = lp_data(r, L)
    from collections import Counter
    cnt = Counter(vals)
    mx = max(cnt.values())
    need(list(cnt.values()).count(mx) == 1)
    best = [v for v in cnt if cnt[v] == mx][0]
    obj, unit = pick(r, [("pencil", "inches"), ("leaf", "centimeters"), ("worm", "centimeters")])
    others = [v for v in range(lo, hi + 1) if v != best]
    r.shuffle(others)
    it = mc_key(f"The line plot shows the lengths of some {pls(obj)}. Which length has the most {pls(obj)}?", f"{best} {unit}", [f"{v} {unit}" for v in others[:3]],
                ["Find the tallest stack of X marks.", f"{best} {unit} has {mx} X marks."], qtype="visual", diagram=lp_diag(lo, hi, vals, obj, unit), r=r)
    it.check = FN("lp", values=[str(v) for v in vals], op="mode", unit=unit)
    return it


@fam("12")
def lp_diff(r, L):
    lo, hi, vals = lp_data(r, L)
    obj, unit = pick(r, [("pencil", "inches"), ("leaf", "centimeters"), ("craft stick", "centimeters")])
    return Item(f"The line plot shows the lengths of some {pls(obj)}. How much longer is the longest {obj} than the shortest {obj}?", f"{max(vals) - min(vals)} {unit}",
                [f"Longest: {max(vals)} {unit}. Shortest: {min(vals)} {unit}.", f"{max(vals)} − {min(vals)} = {max(vals) - min(vals)} {unit}."],
                [W(f"{hi - lo} {unit}", "used the ends of the number line"), W(f"{max(vals)} {unit}", "gave the longest length"), W(f"{max(vals) + min(vals)} {unit}", "added the lengths")],
                FN("lp", values=[str(v) for v in vals], op="diff", unit=unit), qtype="visual", diagram=lp_diag(lo, hi, vals, obj, unit))


@fam("012")
def lp_more(r, L):
    lo, hi, vals = lp_data(r, L)
    x = pick(r, sorted(set(vals))[1:-1] or [vals[0]])
    obj, unit = pick(r, [("pencil", "inches"), ("leaf", "centimeters")])
    k = sum(1 for v in vals if v > x)
    need(k > 0)
    return Item(f"The line plot shows the lengths of some {pls(obj)}. How many {pls(obj)} are longer than {x} {unit}?", k,
                [f"Count the X marks to the right of {x}.", f"There are {k}."], [W(k + vals.count(x), "included the X marks at " + str(x)), W(vals.count(x), "counted only the X marks at " + str(x)), W(len(vals) - k, "counted the shorter ones")],
                FN("lp", values=[str(v) for v in vals], op="count_gt", x=str(x)), qtype="visual", diagram=lp_diag(lo, hi, vals, obj, unit))


@fam("012")
def lp_from_list(r, L):
    lo, hi, vals = lp_data(r, L)
    x = pick(r, sorted(set(vals)))
    shown = vals[:]
    r.shuffle(shown)
    return Item(f"{name(r)} measured some shells, in centimeters: {', '.join(map(str, shown))}. On a line plot, how many X marks go above {x}?", vals.count(x),
                [f"Find each {x} in the list.", f"{x} is in the list {vals.count(x)} {'time' if vals.count(x) == 1 else 'times'}, so the line plot has that many X marks above {x}."],
                [W(vals.count(x) + 1, "counted an extra one"), W(x, "used the length"), W(len(vals), "counted every number")],
                FN("lp", values=[str(v) for v in vals], op="count_at", x=str(x)), qtype="procedural", tags={"graph"})


@fam("2")
def lp_total_at(r, L):
    lo, hi, vals = lp_data(r, 2)
    x, y = r.sample(sorted(set(vals)), 2)
    obj, unit = pick(r, [("pencil", "inches"), ("leaf", "centimeters")])
    k = vals.count(x) + vals.count(y)
    return Item(f"The line plot shows the lengths of some {pls(obj)}. How many {pls(obj)} are {x} {unit} or {y} {unit} long?", k,
                [f"{vals.count(x)} at {x} and {vals.count(y)} at {y}.", f"{vals.count(x)} + {vals.count(y)} = {k}."],
                [W(vals.count(x), "counted only one length"), W(x + y, "added the lengths"), W(k + 1, "counted an extra X")],
                FN("lp_two", values=[str(v) for v in vals], xs=[x, y]), qtype="visual", tags={"multistep"}, diagram=lp_diag(lo, hi, vals, obj, unit))


SKILLS = {
    1: dict(name="Measuring with a Ruler", fams=[ru_read, ru_offset, ru_two, ru_how, ru_mark, ru_error]),
    2: dict(name="Choosing a Measuring Tool and Unit", fams=[tl_tool, tl_unit, tl_ruler_count, tl_why, tl_mixed, tl_tool_sa, tl_unit_sa]),
    3: dict(name="Measuring with Different Units", fams=[du_more, du_why, du_clips, du_cm_m, du_predict, du_eraser]),
    4: dict(name="Estimating Lengths", fams=[es_best, es_unit, es_bench, es_reason, es_steps]),
    5: dict(name="How Much Longer?", fams=[hl_ruler, hl_word, hl_mc, hl_units, hl_unknown, hl_three]),
    6: dict(name="Line Plots of Measurements", fams=[lp_at, lp_n, lp_mode, lp_diff, lp_more, lp_from_list, lp_total_at]),
}
