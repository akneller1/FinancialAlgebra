"""Unit 9: Graphs, Measurement Data, and Line Plots (graphs-measurement-data)."""
from g3lib import *
from fractions import Fraction as Fr

UNIT_ID = "graphs-measurement-data"
TOPICS = [("Favorite Fruit", ["Apple", "Banana", "Grape", "Pear"], "apple", "votes"), ("Books Read", ["Mon", "Tue", "Wed", "Thu"], "book", "books"),
          ("Favorite Season", ["Spring", "Summer", "Fall", "Winter"], "star", "votes"), ("Pets at Home", ["Dogs", "Cats", "Fish", "Birds"], "smile", "pets"),
          ("Field Day Points", ["Red", "Blue", "Green", "Gold"], "star", "points")]


def pic_data(r, L):
    title, cats, icon, unit = pick(r, TOPICS)
    key = pick(r, [2, 5, 10]) if L == 0 else pick(r, [2, 4, 5, 10]) if L == 1 else pick(r, [4, 6, 8, 10])
    halves = L > 0 and key % 2 == 0
    syms = [Fr(r.randint(1, 6)) + (Fr(1, 2) if halves and r.random() < 0.4 else 0) for _ in cats]
    need(len(set(syms)) == len(syms))
    vals = [int(s * key) for s in syms]
    return title, cats, icon, unit, key, syms, vals


def pg_diag(title, cats, icon, unit, key, syms):
    alt = f"A picture graph titled {title}. Key: each symbol = {key} {unit}. " + "; ".join(
        f"{c}: {mixed(s)} {'symbol' if s == 1 else 'symbols'}" for c, s in zip(cats, syms)) + "."
    return Diagram("picgraph", {"title": title, "cats": cats, "symbols": [frac(s) for s in syms], "key": key, "icon": icon, "unit": unit}, alt)


# ============================================================== S1 Picture Graphs
@fam("012")
def pg_read(r, L):
    title, cats, icon, unit, key, syms, vals = pic_data(r, L)
    i = r.randrange(len(cats))
    return Item(f"Use the picture graph. How many {unit} for {cats[i]}?", f"{vals[i]} {unit}",
                [f"Each symbol is {key}. {cats[i]} has {mixed(syms[i])} symbols.", f"{mixed(syms[i])} × {key} = {vals[i]} {unit}." if syms[i].denominator == 1 else f"{int(syms[i])} × {key} = {int(syms[i]) * key}, plus half of {key} is {key // 2}: {vals[i]} {unit}."],
                [W(f"{mixed(syms[i])} {unit}" if syms[i].denominator == 1 else f"{int(syms[i])} {unit}", "counted the symbols instead of using the key"), W(f"{vals[i] + key // 2 if syms[i].denominator != 1 else vals[i] + key} {unit}", "counted a half symbol as a whole" if syms[i].denominator != 1 else "counted one extra symbol"),
                 W(f"{vals[i] - key} {unit}", "missed a symbol")],
                FN("pic_value", syms=[frac(s) for s in syms], key=key, i=i, unit=unit), qtype="visual", diagram=pg_diag(title, cats, icon, unit, key, syms))


@fam("012")
def pg_more(r, L):
    title, cats, icon, unit, key, syms, vals = pic_data(r, L)
    i, j = r.sample(range(len(cats)), 2)
    if vals[i] < vals[j]:
        i, j = j, i
    return Item(f"How many more {unit} for {cats[i]} than for {cats[j]}?", f"{vals[i] - vals[j]} {unit}",
                [f"{cats[i]}: {vals[i]}. {cats[j]}: {vals[j]}.", f"{vals[i]} − {vals[j]} = {vals[i] - vals[j]} {unit}."],
                [W(f"{vals[i] + vals[j]} {unit}", "added instead of subtracting"), W(f"{mixed(syms[i] - syms[j])} {unit}", "subtracted symbols without using the key"), W(f"{vals[i]} {unit}", "gave one total")],
                FN("pic_diff", syms=[frac(s) for s in syms], key=key, i=i, j=j, unit=unit), qtype="visual", diagram=pg_diag(title, cats, icon, unit, key, syms))


@fam("012")
def pg_total(r, L):
    title, cats, icon, unit, key, syms, vals = pic_data(r, L)
    k = 2 if L == 0 else len(cats)
    idx = r.sample(range(len(cats)), k)
    names = " and ".join(cats[i] for i in idx) if k == 2 else "all the categories"
    tot = sum(vals[i] for i in idx)
    return Item(f"How many {unit} in all for {names}?", f"{tot} {unit}", [f"Find each value using the key ({key}).", f"{' + '.join(str(vals[i]) for i in idx)} = {tot} {unit}."],
                [W(f"{mixed(sum(syms[i] for i in idx))} {unit}", "counted symbols instead of using the key"), W(f"{tot - key} {unit}", "missed a symbol"), W(f"{tot + key} {unit}", "counted an extra symbol")],
                FN("pic_sum", syms=[frac(s) for s in syms], key=key, idx=idx, unit=unit), qtype="visual", diagram=pg_diag(title, cats, icon, unit, key, syms))


@fam("12", mode="mc")
def pg_half(r, L):
    key = pick(r, [2, 4, 6, 8, 10])
    good = f"{key // 2}"
    bad = [str(key), "1", str(key * 2)]
    need(len(set(bad + [good])) == 4)
    it = mc_key(f"In a picture graph, each symbol stands for {key}. What does half of a symbol stand for?", good, bad, [f"Half of {key} is {key // 2}.", f"Half a symbol = {key // 2}."], r=r)
    it.check = EX(f"{key}/2")
    return it


@fam("012", mode="mc")
def pg_most(r, L):
    title, cats, icon, unit, key, syms, vals = pic_data(r, L)
    good = cats[vals.index(max(vals))]
    bad = [c for c in cats if c != good]
    it = mc_key(f"Which category has the most {unit}?", good, bad, ["Find the row with the most symbols.", f"{good} has {max(vals)} {unit}."], qtype="visual",
                diagram=pg_diag(title, cats, icon, unit, key, syms), r=r)
    it.check = FN("pic_most", syms=[frac(s) for s in syms], cats=cats)
    return it


@fam("2", mode="mc")
def pg_error(r, L):
    title, cats, icon, unit, key, syms, vals = pic_data(r, L)
    i = r.randrange(len(cats))
    need(syms[i].denominator == 1)
    good = f"{vals[i]}, because each symbol stands for {key}"
    bad = [f"{int(syms[i])}, because there are {int(syms[i])} symbols", f"{int(syms[i]) + key}, because you add the key", f"{key}, because the key is {key}"]
    need(len({vals[i], int(syms[i]), int(syms[i]) + key, key}) == 4)
    return mc_key(f"{name(r)} says {cats[i]} has {int(syms[i])} {unit}. What is the correct number?", good, bad, ["Use the key: each symbol stands for more than 1.", f"{int(syms[i])} × {key} = {vals[i]}."],
                  qtype="error-analysis", tags={"misconception"}, diagram=pg_diag(title, cats, icon, unit, key, syms), r=r)


# ============================================================== S2 Bar Graphs
def bar_data(r, L):
    title, cats, icon, unit = pick(r, TOPICS)
    scl = pick(r, [1, 2, 5]) if L == 0 else pick(r, [2, 5, 10]) if L == 1 else pick(r, [5, 10, 20])
    half = L > 0 and scl % 2 == 0
    vals = [scl * r.randint(1, 8) + (scl // 2 if half and r.random() < 0.35 else 0) for _ in cats]
    need(len(set(vals)) == len(vals))
    top = scl * (max(vals) // scl + 1)
    return title, cats, unit, scl, vals, top


def bg_diag(title, cats, unit, scl, vals, top):
    alt = f"A bar graph titled {title}. The scale goes from 0 to {top} by {scl}s. " + "; ".join(f"{c}: {v}" for c, v in zip(cats, vals)) + "."
    return Diagram("bargraph", {"title": title, "cats": cats, "vals": vals, "scale": scl, "top": top, "ylabel": unit.capitalize()}, alt)


@fam("012")
def bg_read(r, L):
    title, cats, unit, scl, vals, top = bar_data(r, L)
    i = r.randrange(len(cats))
    v = vals[i]
    return Item(f"Use the bar graph. How many {unit} for {cats[i]}?", f"{v} {unit}",
                [f"The scale counts by {scl}s.", f"The bar for {cats[i]} ends at {v}" + (f", halfway between {v - scl // 2} and {v + scl // 2}." if v % scl else ".")],
                [W(f"{v - scl // 2 if v % scl else v - scl} {unit}", "read the line below the top of the bar"), W(f"{v // scl if v % scl == 0 and scl > 1 else v + scl} {unit}", "counted grid lines instead of using the scale" if v % scl == 0 and scl > 1 else "read the line above"),
                 W(f"{v + scl // 2 if v % scl else v + scl} {unit}", "read the line above the bar")],
                FN("bar_value", vals=vals, i=i, unit=unit), qtype="visual", diagram=bg_diag(title, cats, unit, scl, vals, top))


@fam("012")
def bg_more(r, L):
    title, cats, unit, scl, vals, top = bar_data(r, L)
    i, j = r.sample(range(len(cats)), 2)
    if vals[i] < vals[j]:
        i, j = j, i
    word = pick(r, ["more", "fewer"])
    q = f"How many more {unit} for {cats[i]} than for {cats[j]}?" if word == "more" else f"How many fewer {unit} for {cats[j]} than for {cats[i]}?"
    return Item(q, f"{vals[i] - vals[j]} {unit}", [f"{cats[i]}: {vals[i]}. {cats[j]}: {vals[j]}.", f"{vals[i]} − {vals[j]} = {vals[i] - vals[j]} {unit}."],
                [W(f"{vals[i] + vals[j]} {unit}", "added instead of subtracting"), W(f"{vals[i]} {unit}", "gave one bar's value"), W(f"{(vals[i] - vals[j]) // scl if scl > 1 and (vals[i] - vals[j]) % scl == 0 and (vals[i] - vals[j]) // scl != vals[i] - vals[j] else vals[i] - vals[j] + scl} {unit}", "counted grid spaces instead of using the scale")],
                FN("bar_diff", vals=vals, i=i, j=j, unit=unit), qtype="visual", diagram=bg_diag(title, cats, unit, scl, vals, top))


@fam("12")
def bg_two_step(r, L):
    title, cats, unit, scl, vals, top = bar_data(r, L)
    i, j, k = r.sample(range(len(cats)), 3)
    need(vals[i] + vals[j] > vals[k])
    d = vals[i] + vals[j] - vals[k]
    return Item(f"How many more {unit} for {cats[i]} and {cats[j]} together than for {cats[k]}?", f"{d} {unit}",
                [f"{cats[i]} + {cats[j]}: {vals[i]} + {vals[j]} = {vals[i] + vals[j]}.", f"{vals[i] + vals[j]} − {vals[k]} = {d} {unit}."],
                [W(f"{vals[i] + vals[j]} {unit}", "stopped after the first step"), W(f"{vals[i] + vals[j] + vals[k]} {unit}", "added all three"), W(f"{abs(vals[i] - vals[k])} {unit}", "used only one of the two bars")],
                FN("bar_combo", vals=vals, plus=[i, j], minus=[k], unit=unit), qtype="multi-step", tags={"multistep"}, diagram=bg_diag(title, cats, unit, scl, vals, top))


@fam("012", mode="mc")
def bg_which(r, L):
    title, cats, unit, scl, vals, top = bar_data(r, L)
    i = r.randrange(len(cats))
    good = cats[i]
    bad = [c for c in cats if c != good]
    it = mc_key(f"Which category has {vals[i]} {unit}?", good, bad, ["Find the bar that ends at that number on the scale.", f"{good} has {vals[i]}."], qtype="visual",
                diagram=bg_diag(title, cats, unit, scl, vals, top), r=r)
    it.check = FN("bar_has", vals=vals, cats=cats, v=vals[i])
    return it


@fam("12", mode="mc")
def bg_scale(r, L):
    title, cats, unit, scl, vals, top = bar_data(r, L)
    need(scl > 1)
    good = f"{scl}"
    bad = [str(x) for x in [1, scl * 2, scl + 1] if x != scl]
    need(len(set(bad)) == 3)
    it = mc_key("What does the space between two grid lines stand for on this bar graph?", good, bad, ["Look at the numbers on the scale.", f"They count by {scl}s."], qtype="visual",
                diagram=bg_diag(title, cats, unit, scl, vals, top), r=r)
    it.check = FN("bar_scale", scale=scl)
    return it


@fam("2")
def bg_missing(r, L):
    title, cats, unit, scl, vals, top = bar_data(r, L)
    T = sum(vals)
    i = r.randrange(len(cats))
    shown = [v if k != i else 0 for k, v in enumerate(vals)]
    alt = f"A bar graph titled {title}. The scale goes from 0 to {top} by {scl}s. " + "; ".join(f"{c}: {v}" if k != i else f"{c}: bar missing" for k, (c, v) in enumerate(zip(cats, vals))) + "."
    return Item(f"The bar for {cats[i]} is missing. There are {T} {unit} in all. How many {unit} for {cats[i]}?", f"{vals[i]} {unit}",
                [f"Add the bars you can see: {sum(shown)}.", f"{T} − {sum(shown)} = {vals[i]} {unit}."],
                [W(f"{sum(shown)} {unit}", "added the bars you can see"), W(f"{T} {unit}", "gave the total"), W(f"{vals[i] + scl} {unit}", "made an adding error")],
                EX(f"{T}-" + "-".join(str(v) for k, v in enumerate(vals) if k != i), unit=unit), qtype="multi-step", tags={"multistep", "reasoning"},
                diagram=Diagram("bargraph", {"title": title, "cats": cats, "vals": shown, "scale": scl, "top": top, "ylabel": unit.capitalize()}, alt))


# ============================================================== S3 Making Scaled Graphs
@fam("012")
def mk_symbols(r, L):
    key = pick(r, [2, 5, 10]) if L == 0 else pick(r, [2, 4, 5, 10])
    s = Fr(r.randint(2, 8)) + (Fr(1, 2) if L and key % 2 == 0 and r.random() < 0.5 else 0)
    v = int(s * key)
    return Item(f"In a picture graph, each symbol stands for {key}. How many symbols should be drawn to show {v}?", f"{mixed(s)}",
                [f"Divide by the key: {v} ÷ {key}.", f"{mixed(s)} symbols." + (f" The half symbol stands for {key // 2}." if s.denominator != 1 else "")],
                [W(str(v), "drew one symbol for each item"), W(str(int(s) + 1) if s.denominator != 1 else str(int(s) + 1), "rounded up to a whole symbol" if s.denominator != 1 else "drew one extra symbol"), W(str(v * key) if v * key < 200 else str(v + key), "multiplied by the key")],
                FN("symbols_for", v=v, key=key), qtype="procedural")


@fam("012")
def mk_bar_lines(r, L):
    scl = pick(r, [2, 5, 10])
    k = r.randint(2, 9)
    v = scl * k
    return Item(f"A bar graph's scale counts by {scl}s. The bar for {v} should end at which number on the scale?", f"{v}",
                [f"Find {v} on the scale; it is {k} spaces above 0.", f"The bar ends at {v}."],
                [W(str(k), "counted spaces instead of reading the scale"), W(str(v + scl), "went one line too far"), W(str(v - scl), "stopped one line short")], FN("bar_end", v=v), qtype="procedural") \
        if L == 0 else Item(f"A bar graph's scale counts by {scl}s. How many grid spaces tall is the bar for {v}?", k,
                            [f"Each space is {scl}.", f"{v} ÷ {scl} = {k} spaces."], [W(v, "used the value as the number of spaces"), W(k + 1, "counted the lines, including 0"), W(v * scl if v * scl < 300 else v + scl, "multiplied by the scale")],
                            FN("spaces_for", v=v, scale=scl), qtype="procedural")


@fam("012", mode="mc")
def mk_key_choice(r, L):
    k = pick(r, [5, 3, 4])
    data = sorted(r.sample(range(1, 10), 4))
    vals = [k * x for x in data]
    need(any(v % (2 * k) for v in vals))
    cands = [x for x in [2, 3, 4, 5, 6, 10] if x != k]
    bad_keys = [x for x in cands if any(v % x for v in vals)]
    need(len(bad_keys) >= 3)
    bad_keys = r.sample(bad_keys, 3)
    it = mc_key(f"The data are {', '.join(map(str, vals))}. Which key lets you show every number with whole symbols only?", f"each symbol = {k}", [f"each symbol = {x}" for x in bad_keys],
                ["Each number must be a multiple of the key.", f"All the numbers are multiples of {k}."], qtype="conceptual", tags={"reasoning"}, r=r)
    it.check = FN("key_whole", vals=vals)
    return it


@fam("12", mode="mc")
def mk_row(r, L):
    key = pick(r, [2, 4, 6, 10])
    s = Fr(r.randint(2, 6)) + Fr(1, 2)
    v = int(s * key)
    good = f"{int(s)} whole symbols and 1 half symbol"
    bad = [f"{v} whole symbols", f"{int(s) + 1} whole symbols", f"{int(s)} whole symbols"]
    it = mc_key(f"Each symbol = {key}. Which row shows {v}?", good, bad, [f"{v} ÷ {key} = {int(s)} with {key // 2} left over.", f"{key // 2} is half of {key}, so draw a half symbol."], r=r)
    it.check = FN("row_for", v=v, key=key)
    return it


@fam("2", mode="mc")
def mk_error(r, L):
    key = pick(r, [5, 10])
    v = key * r.randint(3, 7)
    good = f"Draw {v // key} symbols, because each symbol stands for {key}."
    bad = [f"Draw {v} symbols, one for each vote.", f"Draw {v // key + 1} symbols, one extra for the key.", f"Draw {key} symbols, because the key is {key}."]
    return mc_key(f"{name(r)} drew {v} symbols to show {v} votes. The key says each symbol = {key}. How should the row be fixed?", good, bad, [f"{v} ÷ {key} = {v // key}.", good],
                  qtype="error-analysis", tags={"misconception"}, r=r)


@fam("2")
def mk_scale_top(r, L):
    scl = pick(r, [5, 10])
    vals = [scl * r.randint(2, 9) for _ in range(4)]
    need(len(set(vals)) == 4)
    top = max(vals)
    return Item(f"{name(r)} is making a bar graph of {', '.join(map(str, vals))} with a scale that counts by {scl}s. How many grid spaces tall must the graph be to fit the tallest bar?", top // scl,
                [f"The tallest bar is {top}.", f"{top} ÷ {scl} = {top // scl} spaces."], [W(top, "used the value"), W(len(vals), "counted the bars"), W(top // scl + 1, "counted lines instead of spaces")],
                FN("spaces_for", v=top, scale=scl), qtype="multi-step", tags={"reasoning"})


# ============================================================== S4 Measuring to Halves and Quarters of an Inch
def length(r, L):
    den = 2 if L == 0 else 4
    whole = r.randint(1, 5)
    frac_ = r.randint(0 if L < 2 else 1, den - 1)
    v = Fr(whole) + Fr(frac_, den)
    need(v < 6)
    return v


def inch(v):
    return f"{mixed(v)} {'inch' if v == 1 else 'inches'}"


@fam("012")
def me_read(r, L):
    v = length(r, L)
    start = Fr(0) if L < 2 else Fr(pick(r, [0, 1]))
    end = start + v
    need(end <= 6)
    obj = pick(r, ["crayon", "eraser", "pencil", "leaf", "key", "ribbon"])
    alt = f"An inch ruler from 0 to 6 marked in fourths. {'An' if obj[0] in 'aeiou' else 'A'} {obj} starts at {mixed(start)} and ends at {mixed(end)}."
    return Item(f"How long is the {obj}, to the nearest {'half' if L == 0 else 'quarter'} inch?", inch(v),
                [f"The {obj} starts at {mixed(start)} and ends at {mixed(end)}." if start else f"The {obj} starts at 0.", f"Its length is {inch(v)}."],
                [W(inch(end) if start else inch(v + Fr(1, 4)), "read the end mark without subtracting the start" if start else "counted one extra quarter"), W(inch(Fr(int(v))) if v.denominator != 1 else inch(v + Fr(1, 2)), "read only the whole inch" if v.denominator != 1 else "read the next half mark"),
                 W(inch(v - Fr(1, 4)) if v > 1 else inch(v + Fr(1, 2)), "counted one quarter too few")],
                FN("measure", start=frac(start), end=frac(end)), qtype="visual", diagram=Diagram("ruler", {"length": 6, "den": 4, "start": frac(start), "end": frac(end), "object": obj}, alt))


@fam("012", mode="mc")
def me_parts(r, L):
    q, good, bad = pick(r, [("How many quarter inches are in 1 inch?", "4", ["2", "3", "8"]), ("How many half inches are in 1 inch?", "2", ["4", "1", "3"]),
                            ("How many quarter inches are in a half inch?", "2", ["4", "1", "3"]), ("How many quarter inches are in 2 inches?", "8", ["4", "6", "2"]),
                            ("How many half inches are in 3 inches?", "6", ["3", "5", "9"])])
    it = mc_key(q, good, bad, ["Each inch is split into 2 halves or 4 fourths (quarters).", f"The answer is {good}."], qtype="conceptual", r=r)
    it.check = FN("parts_in", q=q)
    return it


@fam("012", mode="mc")
def me_halfway(r, L):
    w = r.randint(0, 5)
    kind = pick(r, ["half", "quarter", "three"]) if L else "half"
    if kind == "half":
        q, good = f"Which mark is halfway between {w} and {w + 1} inches on a ruler?", Fr(w) + Fr(1, 2)
        bad = [Fr(w) + Fr(1, 4), Fr(w) + Fr(3, 4), Fr(w + 1) + Fr(1, 2)]
    elif kind == "quarter":
        q, good = f"Which mark is one quarter inch past {w} inches?", Fr(w) + Fr(1, 4)
        bad = [Fr(w) + Fr(1, 2), Fr(w + 1) + Fr(1, 4), Fr(w) + Fr(3, 4)]
    else:
        q, good = f"Which mark is one quarter inch before {w + 1} inches?", Fr(w) + Fr(3, 4)
        bad = [Fr(w + 1) + Fr(1, 4), Fr(w) + Fr(1, 4), Fr(w) + Fr(1, 2)]
    it = mc_key(q, inch(good), [inch(x) for x in bad], ["Each inch has marks for 1/4, 1/2 and 3/4.", f"The mark is at {mixed(good)}."], qtype="conceptual", r=r)
    it.check = FN("ruler_mark", q=q)
    return it


@fam("12")
def me_from_one(r, L):
    v = length(r, 1)
    end = 1 + v
    need(end <= 6)
    obj = pick(r, ["paper clip", "stick", "shell", "feather"])
    alt = f"An inch ruler from 0 to 6 marked in fourths. A {obj} starts at 1 and ends at {mixed(end)}."
    return Item(f"The {obj} does not start at 0. How long is it, to the nearest quarter inch?", inch(v),
                [f"It starts at 1 and ends at {mixed(end)}.", f"{mixed(end)} − 1 = {mixed(v)}, so it is {inch(v)}."],
                [W(inch(end), "read the end mark without subtracting the start"), W(inch(v - 1) if v > 1 else inch(v + 1), "subtracted an extra inch"), W(inch(v + Fr(1, 4)), "counted one extra quarter")],
                FN("measure", start="1", end=frac(end)), qtype="visual", diagram=Diagram("ruler", {"length": 6, "den": 4, "start": "1", "end": frac(end), "object": obj}, alt))


@fam("2", mode="mc")
def me_error(r, L):
    v = length(r, 2)
    end = 1 + v
    need(end <= 6)
    good = f"It is {inch(v)}. The ruler should start at 0, or subtract 1."
    bad = [f"It is {inch(end)}. Read where it ends.", f"It is {inch(Fr(int(end)))}. Only count whole inches.", f"It is {inch(v + Fr(1, 4))}. Count every mark."]
    alt = f"An inch ruler from 0 to 6 marked in fourths. A pencil starts at 1 and ends at {mixed(end)}."
    return mc_key(f"{name(r)} says the pencil is {inch(end)} long. What is wrong?", good, bad, ["The pencil starts at 1, not 0.", f"{mixed(end)} − 1 = {mixed(v)}."],
                  qtype="error-analysis", tags={"misconception"}, diagram=Diagram("ruler", {"length": 6, "den": 4, "start": "1", "end": frac(end), "object": "pencil"}, alt), r=r)


# ============================================================== S5 Line Plots
def lp_data(r, L):
    den = 2 if L == 0 else 4
    lo = r.randint(1, 3)
    vals = [Fr(lo) + Fr(r.randint(0, 2 * den), den) for _ in range(r.randint(8, 12) if L else r.randint(6, 9))]
    return den, lo, vals


def lp_d(den, lo, vals, what="Lengths of Pencils"):
    hi = lo + 2
    from collections import Counter
    cnt = Counter(vals)
    alt = f"A line plot titled {what}, from {lo} to {hi} inches marked in {'halves' if den == 2 else 'fourths'}. " + "; ".join(f"{mixed(v)}: {cnt[v]} X" for v in sorted(cnt)) + "."
    return Diagram("lineplot", {"lo": str(lo), "hi": str(hi), "den": den, "values": [frac(v) for v in vals], "title": what, "unit": "inches"}, alt)


@fam("012")
def lp_count(r, L):
    den, lo, vals = lp_data(r, L)
    from collections import Counter
    cnt = Counter(vals)
    x = pick(r, sorted(cnt))
    return Item(f"How many pencils are {inch(x)} long?", cnt[x], ["Find the value on the line plot and count the X marks above it.", f"There {'is' if cnt[x] == 1 else 'are'} {cnt[x]}."],
                [W(cnt[x] + 1, "counted an extra X"), W(len(vals), "counted all the X marks"), W(cnt.get(x + Fr(1, den), cnt[x] + 2), "looked at the next value")],
                FN("lp", values=[frac(v) for v in vals], op="count_at", x=frac(x)), qtype="visual", diagram=lp_d(den, lo, vals))


@fam("012")
def lp_total(r, L):
    den, lo, vals = lp_data(r, L)
    ask = pick(r, ["n", "gt"]) if L else "n"
    if ask == "n":
        return Item("How many pencils were measured in all?", len(vals), ["Each X is one pencil.", f"Count all the X marks: {len(vals)}."],
                    [W(len(vals) - 1, "missed an X"), W(len(set(vals)), "counted the values instead of the X marks"), W(len(vals) + 1, "counted an extra X")],
                    FN("lp", values=[frac(v) for v in vals], op="n"), qtype="visual", diagram=lp_d(den, lo, vals))
    x = Fr(lo + 1)
    n = sum(1 for v in vals if v > x)
    return Item(f"How many pencils are longer than {lo + 1} inches?", n, [f"Count the X marks to the right of {lo + 1}.", f"There are {n}."],
                [W(sum(1 for v in vals if v >= x), "included the pencils that are exactly " + str(lo + 1) + " inches"), W(len(vals) - n, "counted the shorter ones"), W(n + 1, "counted an extra X")],
                FN("lp", values=[frac(v) for v in vals], op="count_gt", x=str(lo + 1)), qtype="visual", diagram=lp_d(den, lo, vals))


@fam("012", mode="mc")
def lp_mode(r, L):
    den, lo, vals = lp_data(r, L)
    from collections import Counter
    cnt = Counter(vals)
    top = max(cnt.values())
    modes = [v for v in cnt if cnt[v] == top]
    need(len(modes) == 1 and len(cnt) >= 4)
    good = inch(modes[0])
    bad = [inch(v) for v in r.sample([v for v in cnt if v != modes[0]], 3)]
    it = mc_key("Which length was measured most often?", good, bad, ["Find the tallest stack of X marks.", f"{good} has {top} X marks."], qtype="visual", diagram=lp_d(den, lo, vals), r=r)
    it.check = FN("lp", values=[frac(v) for v in vals], op="mode", unit="inches")
    return it


@fam("012")
def lp_make(r, L):
    den, lo, vals = lp_data(r, L)
    from collections import Counter
    cnt = Counter(vals)
    x = pick(r, sorted(cnt))
    data = ", ".join(mixed(v) for v in vals)
    return Item(f"{name(r)} measured some ribbons (in inches): {data}. On a line plot, how many X marks go above {mixed(x)}?", cnt[x],
                [f"Count how many times {mixed(x)} appears in the list.", f"{mixed(x)} appears {cnt[x]} {'time' if cnt[x] == 1 else 'times'}."],
                [W(cnt[x] + 1, "counted a value twice"), W(len(vals), "counted all the data"), W(max(cnt[x] - 1, 0) if cnt[x] > 1 else 2, "missed one")],
                FN("lp", values=[frac(v) for v in vals], op="count_at", x=frac(x)), qtype="procedural")


@fam("12", mode="mc")
def lp_scale(r, L):
    den, lo, vals = lp_data(r, 1)
    need(any(v.denominator == 4 for v in vals))
    good = "in quarter inches"
    bad = ["in whole inches", "in half inches", "in tens"]
    data = ", ".join(mixed(v) for v in vals[:6])
    it = mc_key(f"The data are {data} inches. How should the line plot scale be marked?", good, bad, ["The scale must have a mark for every value in the data.", "Some values are in fourths, so mark the scale in quarter inches."],
                qtype="conceptual", tags={"reasoning"}, r=r)
    it.check = FN("scale_marks", values=[frac(v) for v in vals[:6]])
    return it


@fam("2")
def lp_compare(r, L):
    den, lo, vals = lp_data(r, 2)
    from collections import Counter
    cnt = Counter(vals)
    xs = sorted(cnt)
    need(len(xs) >= 3)
    a, b = r.sample(xs, 2)
    need(cnt[a] != cnt[b])
    if cnt[a] < cnt[b]:
        a, b = b, a
    return Item(f"How many more pencils are {inch(a)} long than {inch(b)} long?", cnt[a] - cnt[b], [f"{mixed(a)}: {cnt[a]} X. {mixed(b)}: {cnt[b]} X.", f"{cnt[a]} − {cnt[b]} = {cnt[a] - cnt[b]}."],
                [W(cnt[a] + cnt[b], "added"), W(cnt[a], "gave one count"), W(cnt[a] - cnt[b] + 1, "miscounted")],
                FN("lp", values=[frac(v) for v in vals], op="count_diff", x=frac(a), y=frac(b)), qtype="visual", tags={"multistep"}, diagram=lp_d(den, lo, vals))


SKILLS = {
    1: dict(name="Reading Scaled Picture Graphs", fams=[pg_read, pg_more, pg_total, pg_half, pg_most, pg_error]),
    2: dict(name="Reading Scaled Bar Graphs", fams=[bg_read, bg_more, bg_two_step, bg_which, bg_scale, bg_missing]),
    3: dict(name="Making Scaled Picture Graphs and Bar Graphs", fams=[mk_symbols, mk_bar_lines, mk_key_choice, mk_row, mk_error, mk_scale_top]),
    4: dict(name="Measuring to the Nearest Half and Quarter Inch", fams=[me_read, me_parts, me_halfway, me_from_one, me_error]),
    5: dict(name="Making and Reading Line Plots", fams=[lp_count, lp_total, lp_mode, lp_make, lp_scale, lp_compare]),
}
