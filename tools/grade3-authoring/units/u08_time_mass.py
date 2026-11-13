"""Unit 8: Time, Liquid Volume, and Mass (time-volume-mass)."""
from g3lib import *

UNIT_ID = "time-volume-mass"


def clk(r, L):
    h = r.randint(1, 12)
    if L == 0:
        m = 5 * r.randint(0, 11)
    elif L == 1:
        m = r.randint(1, 59)
    else:
        m = pick(r, [r.randint(31, 59), r.randint(1, 59)])
    need(m % 5 or L == 0)
    return h, m


def clock_d(h, m):
    hr = "between the " + str(h) + " and the " + str(h % 12 + 1) if m else "on the " + str(h)
    mpos = f"on the {m // 5 if m // 5 else 12}" if m % 5 == 0 else f"{m % 5} small {'mark' if m % 5 == 1 else 'marks'} past the {m // 5 if m // 5 else 12}"
    return Diagram("clock", {"h": h, "m": m}, f"An analog clock. The hour hand is {hr}. The minute hand is {mpos}.")


# ============================================================== S1 Telling Time
@fam("012")
def tt_read(r, L):
    h, m = clk(r, L)
    wr = [W(tm(h % 12 + 1, m), "read the next hour because the hour hand is past the number") if m else W(tm(h, 5), "read the hour hand as minutes"),
          W(tm(h, m // 5) if m >= 10 and m // 5 != m else tm(h, (m + 30) % 60), "read the number the minute hand points to as the minutes"),
          W(tm(m // 5 if m // 5 else 12, h * 5 % 60), "switched the hour hand and the minute hand"), W(tm(h, (m + 5) % 60), "miscounted the minutes")]
    return Item("What time does the clock show?", tm(h, m), [f"The hour hand has passed the {h}, so the hour is {h}." if m else f"The hour hand is on the {h}.",
                                                            f"Count the minutes by 5s and then by 1s: {m}. The time is {tm(h, m)}."],
                wr, FN("clock", h=h, m=m), qtype="visual", diagram=clock_d(h, m))


@fam("012", mode="mc")
def tt_words(r, L):
    h, m = clk(r, L)
    need(m)
    phrase = pick(r, [f"{m} minutes past {h}", f"{m} minutes after {h}:00"]) if m < 30 or L == 0 else f"{60 - m} minutes before {h % 12 + 1}"
    good = tm(h, m)
    bad = [tm(h % 12 + 1, m), tm(h, 60 - m) if 60 - m != m else tm(h, (m + 10) % 60), tm(h - 1 if h > 1 else 12, m)]
    it = mc_key(f"Which time is {phrase}?", good, bad, [f"{phrase} is {m} minutes after {h}:00.", f"The time is {good}."], r=r)
    it.check = FN("clock", h=h, m=m)
    return it


@fam("012")
def tt_minute_hand(r, L):
    k = r.randint(1, 11)
    extra = r.randint(1, 4) if L else 0
    m = 5 * k + extra
    q = f"The minute hand points exactly at the {k}." if not extra else f"The minute hand points {extra} small {'mark' if extra == 1 else 'marks'} past the {k}."
    return _mh(q, k, extra, m)


def _mh(q, k, extra, m):
    it = Item(f"{q} How many minutes after the hour is it?", f"{m} minutes", [f"Each number on the clock is 5 minutes: {k} × 5 = {5 * k}.", f"{5 * k} + {extra} = {m} minutes." if extra else f"It is {m} minutes after the hour."],
              [W(f"{k + extra} minutes", "read the number as minutes"), W(f"{5 * k} minutes" if extra else f"{5 * k + 5} minutes", "forgot the small marks" if extra else "counted one number too far"), W(f"{m + 5} minutes", "counted one number too far")],
              EX(f"5*{k}+{extra}", unit="minutes"), qtype="conceptual")
    it.consts = [5]   # clock convention: each number is 5 minutes
    return it


@fam("012")
def tt_digital(r, L):
    h, m = clk(r, L)
    need(m)
    return Item(f"A digital clock shows {tm(h, m)}. How many minutes until {h % 12 + 1}:00?", f"{60 - m} minutes", [f"There are 60 minutes in an hour.", f"60 − {m} = {60 - m} minutes."],
                [W(f"{m} minutes", "gave the minutes after the hour"), W(f"{100 - m} minutes", "thought an hour has 100 minutes"), W(f"{60 - m + 1} minutes", "counted one extra minute")],
                FN("until_hour", m=m), qtype="procedural")


@fam("12", mode="mc")
def tt_hour_hand(r, L):
    h = r.randint(1, 12)
    m = pick(r, [r.randint(2, 12), r.randint(25, 35), r.randint(48, 58)])
    nxt = h % 12 + 1
    pos = f"just past the {h}" if m < 15 else f"about halfway between the {h} and the {nxt}" if m < 40 else f"almost at the {nxt}"
    good = pos
    bad = [x for x in [f"exactly on the {h}", f"exactly on the {nxt}", f"just past the {h}", f"about halfway between the {h} and the {nxt}", f"almost at the {nxt}"] if x != good][:3]
    it = mc_key(f"Where does the hour hand point at {tm(h, m)}?", good, bad, ["The hour hand moves slowly from one number to the next during the hour.", f"{m} minutes into the hour, it is {good}."],
                qtype="conceptual", tags={"reasoning"}, r=r)
    it.check = FN("hour_hand", h=h, m=m)
    return it


@fam("2", mode="mc")
def tt_error(r, L):
    h, m = r.randint(1, 11), r.randint(35, 58)
    good = f"{tm(h, m)}. The hour hand has not reached the {h + 1} yet."
    bad = [f"{tm(h + 1, m)}. The hour hand is closest to the {h + 1}.", f"{tm(h, m // 5)}. The minute hand is near the {m // 5}.", f"{tm(h + 1, 60 - m)}. Count back from the {h + 1}."]
    it = mc_key(f"{name(r)} read the clock as {tm(h + 1, m)}. What is the correct time?", good, bad, ["Until the minute hand gets to 12, it is still the earlier hour.", f"The time is {tm(h, m)}."],
                qtype="error-analysis", tags={"misconception"}, diagram=clock_d(h, m), r=r)
    it.check = FN("clock_lead", h=h, m=m)
    return it


# ============================================================== S2 Elapsed Time
def interval(r, L):
    h = r.randint(1, 11)
    if L == 0:
        m0 = 5 * r.randint(0, 6)
        d = 5 * r.randint(2, (55 - m0) // 5) if m0 < 45 else 10
        need(m0 + d <= 59)
    elif L == 1:
        m0 = r.randint(20, 55)
        d = r.randint(12, 55)
    else:
        m0 = r.randint(5, 58)
        d = r.randint(35, 95)
    return h, m0, d


@fam("012")
def el_find(r, L):
    h, m0, d = interval(r, L)
    h2, m2 = add_min(h, m0, d)
    t = pick(r, ["Soccer practice starts at {a} and ends at {b}. How long is practice?", "{nm} starts reading at {a} and stops at {b}. How many minutes does {nm} read?",
                 "A movie starts at {a} and ends at {b}. How long is the movie in minutes?"])
    return Item(t.format(a=tm(h, m0), b=tm(h2, m2), nm=name(r)), mins(d), [f"Count on from {tm(h, m0)} to {tm(h2, m2)}." + (f" {tm(h, m0)} to {h % 12 + 1}:00 is {60 - m0} minutes." if h2 != h else ""),
                                                                           f"The elapsed time is {d} minutes."],
                [W(mins(abs(m2 - m0) if abs(m2 - m0) != d else d + 10), "subtracted the minutes only"), W(mins(d + 40) if h2 != h else mins(d + 10), "treated the hour as 100 minutes" if h2 != h else "counted 10 extra minutes"),
                 W(mins(d - 5), "counted 5 minutes too few")], FN("elapsed", a=tm(h, m0), b=tm(h2, m2), unit="minutes"), qtype="word-problem", tags={"modeling"})


@fam("012")
def el_end(r, L):
    h, m0, d = interval(r, L)
    h2, m2 = add_min(h, m0, d)
    return Item(f"Art class starts at {tm(h, m0)}. It lasts {d} minutes. What time does it end?", tm(h2, m2),
                [f"Add {d} minutes to {tm(h, m0)}.", f"The class ends at {tm(h2, m2)}."],
                [W(f"{h}:{m0 + d}" if m0 + d >= 60 else tm(h2, (m2 + 10) % 60), "wrote more than 59 minutes instead of going to the next hour" if m0 + d >= 60 else "added 10 extra minutes"),
                 W(tm(h2 % 12 + 1, m2), "added an extra hour"), W(tm(h, (m0 + d) % 60) if m0 + d >= 60 else tm(h, abs(m0 - d) % 60), "forgot to change the hour" if m0 + d >= 60 else "subtracted the minutes")],
                FN("end_time", a=tm(h, m0), d=d), qtype="word-problem")


@fam("012")
def el_start(r, L):
    h, m0, d = interval(r, L)
    h2, m2 = add_min(h, m0, d)
    nm = name(r)
    return Item(f"{nm} finished a puzzle at {tm(h2, m2)}. It took {d} minutes. What time did {nm} start?", tm(h, m0),
                [f"Count back {d} minutes from {tm(h2, m2)}.", f"The start time was {tm(h, m0)}."],
                [W(tm(*add_min(h2, m2, d)), "added instead of counting back"), W(tm(h2, m0), "subtracted the minutes but kept the end hour") if h2 != h else W(tm(h, (m0 + 10) % 60), "counted back 10 minutes too few"),
                 W(tm(h - 1 if h > 1 else 12, m0), "went back an extra hour")], FN("end_time", a=tm(h, m0), d=d, rev=tm(h2, m2)), qtype="word-problem")


@fam("012")
def el_line(r, L):
    h, m0, d = interval(r, max(L, 1))
    h2, m2 = add_min(h, m0, d)
    need(h2 != h and m2 > 0)
    a, b = 60 - m0, m2
    alt = f"A time number line with marks at {tm(h, m0)}, {h2}:00 and {tm(h2, m2)}. A jump from {tm(h, m0)} to {h2}:00 is labeled {a} min; a jump from {h2}:00 to {tm(h2, m2)} is labeled {b} min."
    return Item(f"The number line shows the time from {tm(h, m0)} to {tm(h2, m2)}. How many minutes is that in all?", mins(d), [f"Add the jumps: {a} + {b}.", f"{a} + {b} = {d} minutes."],
                [W(mins(a), "used only the first jump"), W(mins(b), "used only the second jump"), W(mins(d + 40), "treated the hour as 100 minutes")],
                EX(f"{a}+{b}", unit="minutes"), qtype="visual",
                diagram=Diagram("timeline", {"ticks": [[0, tm(h, m0)], [a, f"{h2}:00"], [d, tm(h2, m2)]], "jumps": [[0, a, f"{a} min"], [a, d, f"{b} min"]]}, alt))


@fam("12", mode="mc")
def el_compare(r, L):
    h, m0, d1 = interval(r, L)
    d2 = d1 + pick(r, [-15, -10, 10, 15, 20])
    need(d2 > 5)
    a1, a2 = name(r), name(sub(r, 7))
    need(a1 != a2)
    e1 = add_min(h, m0, d1)
    e2 = add_min(h, m0, d2)
    good = f"{a1 if d1 > d2 else a2}, by {abs(d1 - d2)} minutes"
    bad = [f"{a2 if d1 > d2 else a1}, by {abs(d1 - d2)} minutes", f"{a1 if d1 > d2 else a2}, by {abs(d1 - d2) + 40} minutes", "They practiced the same amount of time."]
    it = mc_key(f"{a1} practiced piano from {tm(h, m0)} to {tm(*e1)}. {a2} practiced from {tm(h, m0)} to {tm(*e2)}. Who practiced longer, and by how much?", good, bad,
                [f"{a1}: {d1} minutes. {a2}: {d2} minutes.", f"{max(d1, d2)} − {min(d1, d2)} = {abs(d1 - d2)} minutes."], qtype="multi-step", tags={"multistep"}, r=r)
    it.check = FN("longer", people={a1: d1, a2: d2})
    return it


@fam("2")
def el_two_parts(r, L):
    h, m0 = r.randint(1, 10), r.randint(10, 50)
    d1, d2 = r.randint(15, 35), r.randint(10, 30)
    h2, m2 = add_min(h, m0, d1 + d2)
    return Item(f"{name(r)} starts homework at {tm(h, m0)}. Math takes {d1} minutes and reading takes {d2} minutes. What time is homework done?", tm(h2, m2),
                [f"Total time: {d1} + {d2} = {d1 + d2} minutes.", f"{tm(h, m0)} + {d1 + d2} minutes = {tm(h2, m2)}."],
                [W(tm(*add_min(h, m0, d1)), "added only the math time"), W(tm(*add_min(h, m0, d1 + d2 + 40)), "treated the hour as 100 minutes"), W(tm(*add_min(h, m0, d1 + d2 - 10)), "made an adding error")],
                FN("end_time", a=tm(h, m0), d=d1 + d2), qtype="multi-step", tags={"multistep"})


# ============================================================== S3 Liquid Volume
def scale_spec(r, L, unit="liters"):
    if L == 0:
        mx, st, le = pick(r, [(10, 1, 2), (10, 1, 5), (20, 2, 1)])
    elif L == 1:
        mx, st, le = pick(r, [(20, 2, 1), (20, 1, 5), (50, 5, 2), (40, 5, 2)])
    else:
        mx, st, le = pick(r, [(50, 5, 2), (100, 10, 2), (40, 2, 5), (100, 5, 4)])
    level = st * r.randint(2, mx // st - 1)
    need(level % (st * le) or L == 0)
    return mx, st, le, level


@fam("012")
def lv_read(r, L):
    mx, st, le, lv = scale_spec(r, L)
    alt = f"A container marked from 0 to {mx} liters with a mark every {st} {'liter' if st == 1 else 'liters'}, labeled every {st * le}. The water is at the {lv}-liter mark."
    return Item("How many liters of water are in the container?", f"{lv} liters", [f"Each small mark is {st} {'liter' if st == 1 else 'liters'}.", f"The water is at {lv} liters."],
                [W(f"{lv // st} liters", "counted marks instead of liters") if st > 1 else W(f"{lv + 1} liters", "read the next mark"), W(f"{lv + st} liters", "read the mark above"), W(f"{lv - st} liters", "read the mark below")],
                FN("read_scale", mx=mx, st=st, v=lv, unit="liters"), qtype="visual", diagram=Diagram("beaker", {"max": mx, "step": st, "label_every": le, "level": lv, "unit": "liters"}, alt))


@fam("012")
def lv_more(r, L):
    mx, st, le, lv = scale_spec(r, L)
    alt = f"A container marked from 0 to {mx} liters with a mark every {st} {'liter' if st == 1 else 'liters'}. The water is at the {lv}-liter mark."
    return Item(f"How many more liters are needed to fill the container to the {mx}-liter mark?", f"{mx - lv} liters", [f"The water is at {lv} liters.", f"{mx} − {lv} = {mx - lv} liters."],
                [W(f"{lv} liters", "gave the amount in the container"), W(f"{mx + lv} liters", "added"), W(f"{mx - lv - st} liters", "misread the water level")],
                EX(f"{mx}-{lv}", unit="liters"), qtype="visual", diagram=Diagram("beaker", {"max": mx, "step": st, "label_every": le, "level": lv, "unit": "liters"}, alt))


@fam("012", mode="mc")
def lv_estimate(r, L):
    thing, good, bad = pick(r, [("a bathtub full of water", "about 150 liters", ["about 1 liter", "about 15 grams", "about 1,500 kilograms"]),
                                ("a kitchen sink full of water", "about 20 liters", ["about 2 liters", "about 200 liters", "about 20 grams"]),
                                ("a large water bottle", "about 1 liter", ["about 10 liters", "about 100 liters", "about 1 kilogram of sand"]),
                                ("a bucket of water", "about 10 liters", ["about 1 liter", "about 100 liters", "about 10 grams"]),
                                ("a fish tank", "about 40 liters", ["about 4 liters", "about 400 liters", "about 40 grams"])])
    return mc_key(f"Which is the best estimate for {thing}?", good, bad, ["A large water bottle holds about 1 liter.", f"{thing.capitalize()} holds {good}."], qtype="real-world", r=r)


@fam("012", mode="mc")
def lv_unit(r, L):
    thing = pick(r, ["the water in a pool", "the juice in a jug", "the water in a watering can", "the milk in a carton", "the soup in a pot"])
    good = "liters"
    bad = ["grams", "kilograms", "inches"]
    return mc_key(f"Which unit is best for measuring {thing}?", good, bad, ["Liquid volume is measured in liters.", "Grams and kilograms measure mass; inches measure length."], r=r)


@fam("12")
def lv_tick(r, L):
    mx, st, le, lv = scale_spec(r, L)
    need(st > 1 or le > 1)
    alt = f"A container marked from 0 to {mx} liters. Labels are every {st * le} liters with {le - 1} unlabeled {'mark' if le - 1 == 1 else 'marks'} between labels."
    return Item(f"The labels on the container go up by {st * le}. There {'is' if le - 1 == 1 else 'are'} {le - 1} small {'mark' if le - 1 == 1 else 'marks'} between labels. How many liters is each mark worth?",
                f"{st} {'liter' if st == 1 else 'liters'}", [f"{le} equal spaces between labels make {st * le} liters.", f"{st * le} ÷ {le} = {st}."],
                [W(f"{st * le} liters", "used the label value"), W(f"1 liter" if st != 1 else "2 liters", "assumed each mark is 1"), W(f"{st * le // (le - 1) if le > 1 and (st * le) % (le - 1) == 0 and st * le // (le - 1) != st else st + 1} liters", "counted marks instead of spaces")],
                EX(f"{st * le}/{le}", unit="liters"), qtype="visual", diagram=Diagram("beaker", {"max": mx, "step": st, "label_every": le, "level": 0, "unit": "liters"}, alt))


@fam("2", mode="mc")
def lv_error(r, L):
    mx, st, le, lv = scale_spec(r, 2)
    need(st > 1 and lv // st != lv)
    good = f"{lv} liters. Each mark is {st} liters."
    bad = [f"{lv // st} liters. Count the marks.", f"{lv + st} liters. Read the next mark.", f"{mx} liters. The container is full."]
    alt = f"A container marked from 0 to {mx} liters with a mark every {st} liters. The water is at the {lv}-liter mark."
    return mc_key(f"{name(r)} says there are {lv // st} liters of water. What is the correct amount?", good, bad, [f"Each mark is {st} liters, not 1.", f"The water is at {lv} liters."],
                  qtype="error-analysis", tags={"misconception"}, diagram=Diagram("beaker", {"max": mx, "step": st, "label_every": le, "level": lv, "unit": "liters"}, alt), r=r)


# ============================================================== S4 Mass
def mass_spec(r, L):
    if L == 0:
        mx, st, le, unit = pick(r, [(10, 1, 2, "kilograms"), (100, 10, 2, "grams"), (20, 2, 1, "kilograms")])
    elif L == 1:
        mx, st, le, unit = pick(r, [(500, 50, 2, "grams"), (1000, 100, 2, "grams"), (20, 1, 5, "kilograms"), (50, 5, 2, "kilograms")])
    else:
        mx, st, le, unit = pick(r, [(1000, 50, 4, "grams"), (500, 25, 4, "grams"), (100, 5, 4, "kilograms")])
    v = st * r.randint(2, mx // st - 1)
    need(v % (st * le) or L == 0)
    return mx, st, le, unit, v


@fam("012")
def ms_read(r, L):
    mx, st, le, unit, v = mass_spec(r, L)
    obj = pick(r, ["box", "melon", "bag of rice", "pumpkin", "backpack"])
    alt = f"A scale from 0 to {mx} {unit} with a mark every {st}, labeled every {st * le}. The pointer is at {v}."
    return Item(f"What is the mass of the {obj}?", f"{comma(v)} {unit}", [f"Each small mark is {st} {unit}.", f"The pointer is at {comma(v)} {unit}."],
                [W(f"{v // st} {unit}", "counted marks instead of reading the scale") if st > 1 else W(f"{v + 1} {unit}", "read the next mark"), W(f"{comma(v + st)} {unit}", "read the mark after the pointer"), W(f"{comma(v - st)} {unit}", "read the mark before the pointer")],
                FN("read_scale", mx=mx, st=st, v=v, unit=unit), qtype="visual", diagram=Diagram("scale", {"max": mx, "step": st, "label_every": le, "value": v, "unit": unit, "object": obj}, alt))


@fam("012", mode="mc")
def ms_unit(r, L):
    heavy = ["a car", "a dog", "a bag of potatoes", "a third grader", "a bicycle", "a desk"]
    light = ["a paper clip", "a pencil", "a grape", "a crayon", "a coin", "a leaf"]
    if r.random() < 0.5:
        thing, good = pick(r, heavy), "kilograms"
        bad = ["grams", "liters", "inches"]
    else:
        thing, good = pick(r, light), "grams"
        bad = ["kilograms", "liters", "feet"]
    return mc_key(f"Which unit is best for measuring the mass of {thing}?", good, bad, ["Grams measure light objects; kilograms measure heavy objects.", f"Use {good} for {thing}."], r=r)


@fam("012", mode="mc")
def ms_estimate(r, L):
    thing, good, bad = pick(r, [("a paper clip", "about 1 gram", ["about 1 kilogram", "about 100 grams", "about 10 kilograms"]),
                                ("a large dictionary", "about 1 kilogram", ["about 1 gram", "about 100 kilograms", "about 10 grams"]),
                                ("a third grader", "about 30 kilograms", ["about 30 grams", "about 300 kilograms", "about 3 grams"]),
                                ("an apple", "about 150 grams", ["about 150 kilograms", "about 1 gram", "about 15 kilograms"]),
                                ("a bicycle", "about 12 kilograms", ["about 12 grams", "about 120 kilograms", "about 1 gram"])])
    return mc_key(f"Which is the best estimate for the mass of {thing}?", good, bad, ["Use benchmarks: a paper clip is about 1 gram and a large book is about 1 kilogram.", f"{thing.capitalize()} is {good}."],
                  qtype="real-world", r=r)


@fam("012")
def ms_balance(r, L):
    k = r.randint(2, 6) if L == 0 else r.randint(3, 9)
    w = pick(r, [10, 100]) if L < 2 else pick(r, [5, 20, 50])
    unit = "grams"
    return Item(f"A balance scale is level. One side has a toy. The other side has {k} weights of {w} grams each. What is the mass of the toy?", f"{k * w} grams",
                [f"The scale is level, so the masses are equal.", f"{k} × {w} = {k * w} grams."],
                [W(f"{k + w} grams", "added instead of multiplying"), W(f"{w} grams", "used only one weight"), W(f"{k} grams", "counted the weights")],
                EX(f"{k}*{w}", unit=unit), qtype="conceptual")


@fam("12")
def ms_tick(r, L):
    mx, st, le, unit, v = mass_spec(r, L)
    need(le > 1)
    alt = f"A scale from 0 to {mx} {unit}. Labels are every {st * le} with {le - 1} small {'mark' if le == 2 else 'marks'} between labels."
    return Item(f"The scale labels go up by {st * le} {unit} with {le - 1} small {'mark' if le == 2 else 'marks'} between labels. How much is each mark worth?", f"{st} {unit}",
                [f"There are {le} equal spaces between labels.", f"{st * le} ÷ {le} = {st} {unit}."],
                [W(f"{st * le} {unit}", "used the label value"), W(f"1 {unit[:-1]}" if st != 1 else f"2 {unit}", "assumed each mark is 1"), W(f"{st * 2} {unit}" if st * 2 != st * le else f"{st + 1} {unit}", "counted marks instead of spaces")],
                EX(f"{st * le}/{le}", unit=unit), qtype="visual", diagram=Diagram("scale", {"max": mx, "step": st, "label_every": le, "value": 0, "unit": unit}, alt))


@fam("2", mode="mc")
def ms_mass_size(r, L):
    good = "No. A bigger object is not always heavier; a balloon is big but very light."
    bad = ["Yes. Bigger objects always have more mass.", "Yes. Size and mass are the same thing.", "No. Smaller objects are always heavier."]
    return mc_key(f"{name(r)} says a large balloon must have more mass than a small rock because it is bigger. Is that right?", good, bad,
                  ["Mass is how heavy something is, not how big it is.", "Compare masses on a balance or a scale."], qtype="explain", tags={"reasoning"}, r=r)


# ============================================================== S5 Word Problems
@fam("012")
def mw_add(r, L):
    unit = pick(r, ["liters", "grams", "kilograms"])
    a, b = (r.randint(2, 9), r.randint(2, 9)) if L == 0 else (r.randint(12, 60), r.randint(15, 80)) if L == 1 else (r.randint(120, 480), r.randint(150, 450))
    t = {"liters": f"A pitcher has {a} liters of juice. {name(r)} pours in {b} more liters. How many liters are in the pitcher now?",
         "grams": f"A bag has {a} grams of flour. {name(r)} adds {b} grams more. How many grams of flour are in the bag?",
         "kilograms": f"One crate has a mass of {a} kilograms. Another crate has a mass of {b} kilograms. What is their total mass?"}[unit]
    return Item(t, f"{comma(a + b)} {unit}", [f"Join the amounts: {a} + {b}.", f"{a} + {b} = {comma(a + b)} {unit}."],
                [W(f"{abs(a - b)} {unit}", "subtracted instead of adding"), W(f"{comma(a * b)} {unit}", "multiplied"), W(f"{comma(a + b + 10)} {unit}", "made an adding error")],
                EX(f"{a}+{b}", unit=unit), qtype="word-problem")


@fam("012")
def mw_sub(r, L):
    unit = pick(r, ["liters", "grams", "kilograms"])
    a, b = (r.randint(6, 15), r.randint(2, 5)) if L == 0 else (r.randint(40, 95), r.randint(12, 38)) if L == 1 else (r.randint(400, 950), r.randint(120, 380))
    t = {"liters": f"A tank held {a} liters of water. {b} liters leaked out. How many liters are left?",
         "grams": f"A watermelon has a mass of {comma(a)} grams. A cantaloupe has a mass of {b} grams. How many more grams is the watermelon?",
         "kilograms": f"A bag of soil has a mass of {a} kilograms. {name(r)} uses {b} kilograms. How many kilograms are left?"}[unit]
    return Item(t, f"{comma(a - b)} {unit}", [f"Subtract: {a} − {b}.", f"{a} − {b} = {comma(a - b)} {unit}."],
                [W(f"{comma(a + b)} {unit}", "added instead of subtracting"), W(f"{comma(a - b + 10)} {unit}", "made a regrouping error"), W(f"{b} {unit}", "gave the smaller amount")],
                EX(f"{a}-{b}", unit=unit), qtype="word-problem")


@fam("012")
def mw_mult(r, L):
    unit = pick(r, ["liters", "grams", "kilograms"])
    k, v = (r.randint(2, 5), r.randint(2, 5)) if L == 0 else (r.randint(3, 9), r.randint(3, 9)) if L == 1 else (r.randint(4, 9), r.randint(6, 10))
    t = {"liters": f"Each bottle holds {v} liters. How many liters do {k} bottles hold?", "grams": f"Each block has a mass of {v} grams. What is the mass of {k} blocks?",
         "kilograms": f"Each bag of sand is {v} kilograms. What is the mass of {k} bags?"}[unit]
    return Item(t, f"{k * v} {unit}", [f"{k} equal groups of {v}.", f"{k} × {v} = {k * v} {unit}."],
                [W(f"{k + v} {unit}", "added instead of multiplying"), W(f"{k * v + v} {unit}", "added an extra group"), W(f"{v} {unit}", "gave the amount in one")],
                EX(f"{k}*{v}", unit=unit), qtype="word-problem")


@fam("012")
def mw_div(r, L):
    unit = pick(r, ["liters", "grams", "kilograms"])
    k, v = (r.randint(2, 5), r.randint(2, 5)) if L == 0 else (r.randint(3, 9), r.randint(3, 9)) if L == 1 else (r.randint(4, 9), r.randint(6, 10))
    T = k * v
    t = {"liters": f"{T} liters of lemonade are poured equally into {k} jugs. How many liters are in each jug?",
         "grams": f"{T} grams of beads are shared equally by {k} friends. How many grams does each friend get?",
         "kilograms": f"{T} kilograms of apples are packed equally into {k} crates. How many kilograms are in each crate?"}[unit]
    return Item(t, f"{v} {unit}", [f"Share {T} equally into {k} groups.", f"{T} ÷ {k} = {v} {unit}."],
                [W(f"{T - k} {unit}", "subtracted instead of dividing"), W(f"{T * k} {unit}" if T * k < 1000 else f"{T + k} {unit}", "multiplied instead of dividing"), W(f"{v + 1} {unit}", "used a nearby fact")],
                EX(f"{T}/{k}", unit=unit), qtype="word-problem")


@fam("012", mode="mc")
def mw_choose(r, L):
    k, v = r.randint(3, 9), r.randint(3, 9)
    T = k * v
    kind = pick(r, ["div", "mult", "sub"])
    if kind == "div":
        q, good = f"{T} liters of water fill {k} buckets equally. How many liters are in each bucket?", f"{T} ÷ {k}"
        bad = [f"{T} × {k}", f"{T} − {k}", f"{T} + {k}"]
    elif kind == "mult":
        q, good = f"Each jar holds {v} liters. How many liters do {k} jars hold?", f"{k} × {v}"
        bad = [f"{k} + {v}", f"{v} − {k}" if v > k else f"{k} − {v}", f"{k * v} ÷ {v}"]
    else:
        q, good = f"A box has a mass of {T} kilograms. After some books are taken out it has a mass of {v} kilograms. What mass of books was taken out?", f"{T} − {v}"
        bad = [f"{T} + {v}", f"{T} ÷ {v}", f"{T} × {v}"]
    need(len(set(bad + [good])) == 4)
    return mc_key(q + " Which expression solves the problem?", good, bad, ["Decide whether the story joins, separates, makes equal groups, or shares.", f"Use {good}."], qtype="explain", tags={"reasoning"}, r=r)


@fam("2")
def mw_beaker(r, L):
    mx, st, le, lv = scale_spec(r, 2)
    k = pick(r, [d for d in range(2, 6) if lv % d == 0 and lv // d >= 2] or [1])
    need(k > 1)
    alt = f"A container marked from 0 to {mx} liters with a mark every {st} liters. The water is at the {lv}-liter mark."
    return Item(f"The water in the container is poured equally into {k} buckets. How many liters go in each bucket?", f"{lv // k} liters",
                [f"Read the container: {lv} liters.", f"{lv} ÷ {k} = {lv // k} liters."],
                [W(f"{lv} liters", "did not share the water"), W(f"{lv * k} liters" if lv * k < 1000 else f"{lv + k} liters", "multiplied instead of dividing"), W(f"{(lv + st) // k if (lv + st) % k == 0 else lv // k + st} liters", "misread the container")],
                EX(f"{lv}/{k}", unit="liters"), qtype="visual", tags={"multiple-representations"}, diagram=Diagram("beaker", {"max": mx, "step": st, "label_every": le, "level": lv, "unit": "liters"}, alt))


@fam("2", mode="mc")
def mw_units_error(r, L):
    a, b = r.randint(2, 9), r.randint(200, 800)
    good = f"The units are different: {a} kilograms and {b} grams cannot be added as {a + b}."
    bad = [f"There is no mistake; the total is {a + b} grams.", f"There is no mistake; the total is {a + b} kilograms.", f"{name(r)} should have subtracted: {b - a}."]
    return mc_key(f"A bag of potatoes is {a} kilograms. A bag of carrots is {b} grams. {name(r)} says the total is {a + b} grams. What is wrong?", good, bad,
                  ["Only add masses that are in the same unit.", "Kilograms and grams are different units."], qtype="error-analysis", tags={"misconception"}, r=r)


SKILLS = {
    1: dict(name="Telling Time to the Nearest Minute", fams=[tt_read, tt_words, tt_minute_hand, tt_digital, tt_hour_hand, tt_error]),
    2: dict(name="Elapsed Time", fams=[el_find, el_end, el_start, el_line, el_compare, el_two_parts]),
    3: dict(name="Measuring Liquid Volume in Liters", fams=[lv_read, lv_more, lv_estimate, lv_unit, lv_tick, lv_error]),
    4: dict(name="Measuring Mass in Grams and Kilograms", fams=[ms_read, ms_unit, ms_estimate, ms_balance, ms_tick, ms_mass_size]),
    5: dict(name="Liquid Volume and Mass Word Problems", fams=[mw_add, mw_sub, mw_mult, mw_div, mw_choose, mw_beaker, mw_units_error]),
}
