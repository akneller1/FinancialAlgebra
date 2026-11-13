"""Unit 11: Picture Graphs and Bar Graphs (graphs-data). 2.MD.D.10 (single-unit scale, up to four categories)."""
from g2lib import *

UNIT_ID = "graphs-data"

TOPICS = [("Favorite Fruit", ["apple", "banana", "grape", "pear"], "votes", "children"),
          ("Pets in Our Class", ["dog", "cat", "fish", "bird"], "pets", "pets"),
          ("Favorite Sport", ["soccer", "tennis", "swim", "run"], "votes", "children"),
          ("Books Read", ["Mia", "Leo", "Ivy", "Sam"], "books", "books"),
          ("Weather This Month", ["sunny", "rainy", "cloudy", "snowy"], "days", "days"),
          ("Lunch Choice", ["pizza", "tacos", "soup", "salad"], "votes", "children"),
          ("Shells Found", ["Ana", "Ben", "Kai", "Zoe"], "shells", "shells")]
ICONS = {"votes": "star", "pets": "circle", "books": "square", "days": "circle", "shells": "star"}


def data(r, L, k=None):
    title, cats, unit, who = pick(r, TOPICS)
    k = k or (3 if L == 0 else pick(r, [3, 4]))
    cats = cats[:k]
    hi = 10 if L == 0 else 15 if L == 1 else 20
    vals = [r.randint(1, hi) for _ in cats]
    need(len(set(vals)) == len(vals))
    return title, cats, vals, unit, who, hi


def data_text(cats, vals, unit):
    return ", ".join(f"{c} {v}" for c, v in zip(cats, vals))


def pic(title, cats, vals, unit):
    alt = f"A picture graph titled {title}. Each picture stands for 1. " + "; ".join(f"{c}: {v} pictures" for c, v in zip(cats, vals)) + "."
    return Diagram("picgraph", {"title": title, "cats": cats, "symbols": vals, "key": 1, "icon": ICONS.get(unit, "star"), "unit": unit[:-1] if unit.endswith("s") else unit}, alt)


def bar(title, cats, vals, unit, hi, horiz=False):
    top = hi if hi <= 12 else 20
    alt = f"A bar graph titled {title} with a scale of 1. " + "; ".join(f"{c}: {v}" for c, v in zip(cats, vals)) + "."
    return Diagram("bargraph1", {"title": title, "cats": cats, "vals": vals, "top": max(top, max(vals)), "ylabel": f"Number of {unit}", "horizontal": horiz}, alt)


def graph(r, L, title, cats, vals, unit, hi):
    kind = pick(r, ["pic", "bar"])
    return (kind, pic(title, cats, vals, unit)) if kind == "pic" else (kind, bar(title, cats, vals, unit, hi, horiz=r.random() < 0.3))


# ============================================================== S1 Reading Picture Graphs
@fam("012")
def pg_value(r, L):
    title, cats, vals, unit, who, hi = data(r, L)
    i = r.randrange(len(cats))
    return Item(f"Look at the picture graph. How many {unit} are for {cats[i]}?", f"{vals[i]} {unit}", [f"Each picture stands for 1.", f"Count the pictures in the {cats[i]} row: {vals[i]} {unit}."],
                [W(f"{vals[(i + 1) % len(vals)]} {unit}", "read the wrong row"), W(f"{vals[i] + 1} {unit}", "counted one picture twice"), W(f"{sum(vals)} {unit}", "counted every row")],
                FN("pic_value", syms=vals, key=1, i=i, unit=unit), qtype="visual", diagram=pic(title, cats, vals, unit))


@fam("012", mode="mc")
def pg_most(r, L):
    title, cats, vals, unit, who, hi = data(r, L)
    want = pick(r, ["most", "fewest"])
    j = vals.index(max(vals) if want == "most" else min(vals))
    it = mc_key(f"Look at the picture graph. Which has the {want} {unit}?", cats[j], [c for c in cats if c != cats[j]] + (["They are all the same"] if len(cats) == 3 else []),
                [f"Find the {'longest' if want == 'most' else 'shortest'} row.", f"{cats[j]} has {vals[j]}."], qtype="visual", diagram=pic(title, cats, vals, unit), r=r)
    it.check = FN("graph_extreme", cats=cats, vals=vals, want=want)
    return it


@fam("012")
def pg_total(r, L):
    title, cats, vals, unit, who, hi = data(r, L)
    return Item(f"Look at the picture graph. How many {unit} are shown in all?", f"{sum(vals)} {unit}", [f"Add the rows: {' + '.join(map(str, vals))}.", f"{' + '.join(map(str, vals))} = {sum(vals)} {unit}."],
                [W(f"{len(cats)} {unit}", "counted the rows"), W(f"{sum(vals[:-1])} {unit}", "left out a row"), W(f"{max(vals)} {unit}", "gave the biggest row")],
                FN("pic_sum", syms=vals, key=1, idx=list(range(len(vals))), unit=unit), qtype="visual", diagram=pic(title, cats, vals, unit))


@fam("012", mode="mc")
def pg_key(r, L):
    title, cats, vals, unit, who, hi = data(r, L)
    i = r.randrange(len(cats))
    good = f"{vals[i]} {unit}"
    bad = [f"{vals[i] + 1} {unit}", f"{vals[i] - 1 if vals[i] > 1 else vals[i] + 2} {unit}", f"{len(cats)} {unit}" if len(cats) != vals[i] else f"{vals[i] + 3} {unit}"]
    it = mc_key(f"Each picture stands for 1. How many {unit} are for {cats[i]}?", good, bad, ["Count the pictures in the row.", good], qtype="visual", diagram=pic(title, cats, vals, unit), r=r)
    it.check = FN("pic_value", syms=vals, key=1, i=i, unit=unit)
    return it


@fam("012")
def pg_two(r, L):
    title, cats, vals, unit, who, hi = data(r, L)
    i, j = r.sample(range(len(cats)), 2)
    return Item(f"Look at the picture graph. How many {unit} are for {cats[i]} and {cats[j]} together?", f"{vals[i] + vals[j]} {unit}", [f"{cats[i]}: {vals[i]}. {cats[j]}: {vals[j]}.", f"{vals[i]} + {vals[j]} = {vals[i] + vals[j]} {unit}."],
                [W(f"{abs(vals[i] - vals[j])} {unit}", "subtracted instead of adding"), W(f"{vals[i]} {unit}", "used only one row"), W(f"{sum(vals)} {unit}", "added every row")],
                FN("pic_sum", syms=vals, key=1, idx=[i, j], unit=unit), qtype="visual", diagram=pic(title, cats, vals, unit))


@fam("012", mode="mc")
def pg_error(r, L):
    title, cats, vals, unit, who, hi = data(r, L)
    i = r.randrange(len(cats))
    nm = name(r)
    good = f"No. Each picture stands for 1, so {cats[i]} has {vals[i]}."
    bad = [f"Yes. {cats[i]} has {vals[i] + 1}.", f"No. {cats[i]} has {len(cats)}.", f"Yes. You count the label too."]
    it = mc_key(f"{nm} says {cats[i]} has {vals[i] + 1} {unit} because {nm} counted the label as a picture. Is {nm} right?", good, bad, ["Count only the pictures.", good],
                qtype="error-analysis", tags={"misconception"}, diagram=pic(title, cats, vals, unit), r=r)
    it.check = FN("graph_claim", cats=cats, vals=vals, i=i)
    return it


# ============================================================== S2 Reading Bar Graphs
@fam("012")
def bg_value(r, L):
    title, cats, vals, unit, who, hi = data(r, L)
    i = r.randrange(len(cats))
    return Item(f"Look at the bar graph. How many {unit} are for {cats[i]}?", f"{vals[i]} {unit}", [f"Find where the {cats[i]} bar ends and read across to the scale.", f"The bar ends at {vals[i]}."],
                [W(f"{vals[i] + 1} {unit}", "read the grid line above"), W(f"{vals[i] - 1} {unit}", "read the grid line below") if vals[i] > 1 else W(f"{vals[i] + 2} {unit}", "misread the scale"), W(f"{vals[(i + 1) % len(vals)]} {unit}", "read the wrong bar")],
                FN("bar_value", vals=vals, i=i, unit=unit), qtype="visual", diagram=bar(title, cats, vals, unit, hi, r.random() < 0.3))


@fam("012", mode="mc")
def bg_most(r, L):
    title, cats, vals, unit, who, hi = data(r, L)
    want = pick(r, ["most", "fewest"])
    j = vals.index(max(vals) if want == "most" else min(vals))
    it = mc_key(f"Look at the bar graph. Which has the {want} {unit}?", cats[j], [c for c in cats if c != cats[j]] + (["They are all the same"] if len(cats) == 3 else []),
                [f"Find the {'tallest' if want == 'most' else 'shortest'} bar.", f"{cats[j]} has {vals[j]}."], qtype="visual", diagram=bar(title, cats, vals, unit, hi), r=r)
    it.check = FN("graph_extreme", cats=cats, vals=vals, want=want)
    return it


@fam("012", mode="mc")
def bg_which(r, L):
    title, cats, vals, unit, who, hi = data(r, L)
    i = r.randrange(len(cats))
    it = mc_key(f"Look at the bar graph. Which bar shows {vals[i]} {unit}?", cats[i], [c for c in cats if c != cats[i]] + (["no bar"] if len(cats) == 3 else []),
                [f"Find {vals[i]} on the scale and look for the bar that ends there.", f"{cats[i]} shows {vals[i]}."], qtype="visual", diagram=bar(title, cats, vals, unit, hi), r=r)
    it.check = FN("bar_has", cats=cats, vals=vals, v=vals[i])
    return it


@fam("012")
def bg_total(r, L):
    title, cats, vals, unit, who, hi = data(r, L)
    return Item(f"Look at the bar graph. How many {unit} are there in all?", f"{sum(vals)} {unit}", [f"Read every bar: {', '.join(map(str, vals))}.", f"{' + '.join(map(str, vals))} = {sum(vals)} {unit}."],
                [W(f"{len(cats)} {unit}", "counted the bars"), W(f"{max(vals)} {unit}", "read only the tallest bar"), W(f"{sum(vals) - vals[-1]} {unit}", "left out a bar")],
                FN("bar_combo", vals=vals, plus=list(range(len(vals))), minus=[], unit=unit), qtype="visual", diagram=bar(title, cats, vals, unit, hi))


@fam("12")
def bg_odd(r, L):
    title, cats, vals, unit, who, hi = data(r, 2)
    need(any(v % 2 for v in vals) and max(vals) > 12)
    i = next(k for k, v in enumerate(vals) if v % 2)
    return Item(f"The scale has a grid line for every 1 but a number on every other line. How many {unit} are for {cats[i]}?", f"{vals[i]} {unit}",
                [f"The {cats[i]} bar ends on a line between {vals[i] - 1} and {vals[i] + 1}.", f"So it shows {vals[i]}."],
                [W(f"{vals[i] - 1} {unit}", "read the number below"), W(f"{vals[i] + 1} {unit}", "read the number above"), W(f"{vals[i] + 2} {unit}", "counted by 2s past the bar")],
                FN("bar_value", vals=vals, i=i, unit=unit), qtype="visual", diagram=bar(title, cats, vals, unit, hi))


@fam("012", mode="mc")
def bg_error(r, L):
    title, cats, vals, unit, who, hi = data(r, L)
    i = r.randrange(len(cats))
    nm = name(r)
    good = f"{vals[i]}, because the top of the bar lines up with {vals[i]} on the scale"
    bad = [f"{vals[i] + 1}, because there are {vals[i] + 1} grid lines up to the top", f"{vals[i] - 1 if vals[i] > 1 else vals[i] + 2}, because you start counting at 1", f"{len(cats)}, because there are {len(cats)} bars"]
    need(len(set(b.split(",")[0] for b in bad)) == 3 and str(vals[i]) not in [b.split(",")[0] for b in bad])
    it = mc_key(f"{nm} counted the grid lines to read the {cats[i]} bar, starting with the line at 0. What does the bar really show?", good, bad, ["Read the number where the bar ends.", good + "."],
                qtype="error-analysis", tags={"misconception"}, diagram=bar(title, cats, vals, unit, hi), r=r)
    it.check = FN("lead_value", value=vals[i])
    return it


# ============================================================== S3 Solving Problems with Graphs
@fam("012")
def sp_more(r, L):
    title, cats, vals, unit, who, hi = data(r, L)
    i, j = r.sample(range(len(cats)), 2)
    if vals[i] < vals[j]:
        i, j = j, i
    kind, dg = graph(r, L, title, cats, vals, unit, hi)
    return Item(f"Look at the graph. How many more {unit} are for {cats[i]} than for {cats[j]}?", f"{vals[i] - vals[j]} {unit}",
                [f"{cats[i]}: {vals[i]}. {cats[j]}: {vals[j]}.", f"{vals[i]} − {vals[j]} = {vals[i] - vals[j]} {unit}."],
                [W(f"{vals[i] + vals[j]} {unit}", "added instead of finding the difference"), W(f"{vals[i]} {unit}", "gave one amount"), W(f"{vals[i] - vals[j] + 1} {unit}", "counted one extra")],
                FN("bar_diff", vals=vals, i=i, j=j, unit=unit), qtype="visual", diagram=dg)


@fam("012")
def sp_fewer(r, L):
    title, cats, vals, unit, who, hi = data(r, L)
    i, j = r.sample(range(len(cats)), 2)
    if vals[i] > vals[j]:
        i, j = j, i
    kind, dg = graph(r, L, title, cats, vals, unit, hi)
    return Item(f"Look at the graph. How many fewer {unit} are for {cats[i]} than for {cats[j]}?", f"{vals[j] - vals[i]} {unit}",
                [f"{cats[j]}: {vals[j]}. {cats[i]}: {vals[i]}.", f"{vals[j]} − {vals[i]} = {vals[j] - vals[i]} {unit}."],
                [W(f"{vals[i] + vals[j]} {unit}", "added instead of finding the difference"), W(f"{vals[i]} {unit}", "gave one amount"), W(f"{vals[j] - vals[i] - 1 if vals[j] - vals[i] > 1 else vals[j] - vals[i] + 2} {unit}", "made a counting mistake")],
                FN("bar_diff", vals=vals, i=j, j=i, unit=unit), qtype="visual", diagram=dg)


@fam("012")
def sp_together(r, L):
    title, cats, vals, unit, who, hi = data(r, L)
    i, j = r.sample(range(len(cats)), 2)
    kind, dg = graph(r, L, title, cats, vals, unit, hi)
    return Item(f"Look at the graph. How many {unit} are for {cats[i]} and {cats[j]} together?", f"{vals[i] + vals[j]} {unit}",
                [f"{cats[i]}: {vals[i]}. {cats[j]}: {vals[j]}.", f"{vals[i]} + {vals[j]} = {vals[i] + vals[j]} {unit}."],
                [W(f"{abs(vals[i] - vals[j])} {unit}", "subtracted instead of adding"), W(f"{sum(vals)} {unit}", "added every category"), W(f"{vals[i] + vals[j] + 1} {unit}", "counted one extra")],
                FN("bar_combo", vals=vals, plus=[i, j], minus=[], unit=unit), qtype="visual", diagram=dg)


@fam("012")
def sp_takeapart(r, L):
    title, cats, vals, unit, who, hi = data(r, L)
    i = r.randrange(len(cats))
    tot = sum(vals)
    kind, dg = graph(r, L, title, cats, vals, unit, hi)
    return Item(f"Look at the graph. There are {tot} {unit} in all. How many are NOT for {cats[i]}?", f"{tot - vals[i]} {unit}",
                [f"{cats[i]} has {vals[i]}.", f"{tot} − {vals[i]} = {tot - vals[i]} {unit}."],
                [W(f"{vals[i]} {unit}", "gave the amount for " + cats[i]), W(f"{tot + vals[i]} {unit}", "added instead of subtracting"), W(f"{tot - vals[i] + 1} {unit}", "counted one extra")],
                FN("bar_combo", vals=vals, plus=[k for k in range(len(vals)) if k != i], minus=[], unit=unit), qtype="visual", diagram=dg)


@fam("012", mode="mc")
def sp_eq(r, L):
    title, cats, vals, unit, who, hi = data(r, L)
    i, j = r.sample(range(len(cats)), 2)
    if vals[i] < vals[j]:
        i, j = j, i
    kind, dg = graph(r, L, title, cats, vals, unit, hi)
    good = f"{vals[i]} − {vals[j]} = ?"
    bad = [f"{vals[i]} + {vals[j]} = ?", f"{vals[j]} − ? = {vals[i]}", f"? − {vals[i]} = {vals[j]}"]
    it = mc_key(f"Look at the graph. Which equation finds how many more {unit} are for {cats[i]} than for {cats[j]}?", good, bad, ["Compare by subtracting the smaller amount from the bigger one.", f"{good}; ? = {vals[i] - vals[j]}."],
                qtype="visual", tags={"modeling"}, diagram=dg, r=r)
    it.check = FN("story_eq", ans=vals[i] - vals[j], given=sorted([vals[i], vals[j]]))
    return it


@fam("2")
def sp_two_step(r, L):
    title, cats, vals, unit, who, hi = data(r, 2, 4)
    i, j, k = r.sample(range(4), 3)
    need(vals[i] + vals[j] != vals[k])
    big = vals[i] + vals[j]
    kind, dg = graph(r, 2, title, cats, vals, unit, hi)
    return Item(f"Look at the graph. How many more {unit} are for {cats[i]} and {cats[j]} together than for {cats[k]}?" if big > vals[k] else
                f"Look at the graph. How many fewer {unit} are for {cats[i]} and {cats[j]} together than for {cats[k]}?", f"{abs(big - vals[k])} {unit}",
                [f"{cats[i]} and {cats[j]}: {vals[i]} + {vals[j]} = {big}.", f"Compare with {cats[k]} ({vals[k]}): {max(big, vals[k])} − {min(big, vals[k])} = {abs(big - vals[k])} {unit}."],
                [W(f"{big} {unit}", "did only the first step"), W(f"{big + vals[k]} {unit}", "added all three"), W(f"{abs(vals[i] - vals[k])} {unit}", "compared only one category")],
                FN("bar_combo", vals=vals, plus=[i, j] if big > vals[k] else [k], minus=[k] if big > vals[k] else [i, j], unit=unit), qtype="multi-step", tags={"multistep"}, diagram=dg)


@fam("012")
def sp_text_more(r, L):
    title, cats, vals, unit, who, hi = data(r, L)
    i, j = r.sample(range(len(cats)), 2)
    if vals[i] < vals[j]:
        i, j = j, i
    return Item(f"A bar graph shows {data_text(cats, vals, unit)}. How many more for {cats[i]} than {cats[j]}?", vals[i] - vals[j],
                [f"{cats[i]}: {vals[i]}. {cats[j]}: {vals[j]}.", f"{vals[i]} − {vals[j]} = {vals[i] - vals[j]}."],
                [W(vals[i] + vals[j], "added instead of finding the difference"), W(vals[i], "gave one amount"), W(vals[i] - vals[j] + 1, "counted one extra")],
                FN("bar_diff", vals=vals, i=i, j=j), qtype="word-problem", tags={"graph"})


@fam("012")
def sp_text_all(r, L):
    title, cats, vals, unit, who, hi = data(r, L)
    return Item(f"A picture graph shows {data_text(cats, vals, unit)}. How many are shown in all?", sum(vals),
                [f"Add every category: {' + '.join(map(str, vals))}.", f"The total is {sum(vals)}."],
                [W(sum(vals[:-1]), "left out a category"), W(len(cats), "counted the categories"), W(max(vals), "gave the biggest amount")],
                FN("bar_combo", vals=vals, plus=list(range(len(vals))), minus=[]), qtype="word-problem", tags={"graph"})


# ============================================================== S4 Making Picture Graphs and Bar Graphs
def tally_d(title, cats, vals):
    alt = f"A tally chart titled {title}. " + "; ".join(f"{c}: {v} tally marks" for c, v in zip(cats, vals)) + "."
    return Diagram("tally", {"title": title, "cats": cats, "counts": vals}, alt)


@fam("012")
def mk_bar_height(r, L):
    title, cats, vals, unit, who, hi = data(r, L)
    i = r.randrange(len(cats))
    return Item(f"{name(r)} will make a bar graph from the tally chart. How tall should the bar for {cats[i]} be?", vals[i],
                [f"Count the tally marks for {cats[i]}; each bundle is 5.", f"There are {vals[i]}, so the bar goes up to {vals[i]}."],
                [W(vals[i] + 1, "counted the slash as an extra mark") if vals[i] >= 5 else W(vals[i] + 1, "counted one mark twice"), W(vals[(i + 1) % len(vals)], "used the wrong row"), W(vals[i] // 5 + vals[i] % 5 if vals[i] >= 5 else vals[i] + 2, "counted each bundle as 1")],
                FN("tally_val", counts=vals, i=i), qtype="visual", diagram=tally_d(title, cats, vals))


@fam("012")
def mk_pic_count(r, L):
    title, cats, vals, unit, who, hi = data(r, L)
    i = r.randrange(len(cats))
    return Item(f"{name(r)} will make a picture graph from the tally chart. Each picture stands for 1. How many pictures go in the row for {cats[i]}?", vals[i],
                [f"Count the tally marks for {cats[i]}.", f"There are {vals[i]}, so draw {vals[i]} pictures."],
                [W(vals[i] + 1, "counted one mark twice"), W(vals[(i + 1) % len(vals)], "used the wrong row"), W(sum(vals), "counted all the tally marks")],
                FN("tally_val", counts=vals, i=i), qtype="visual", diagram=tally_d(title, cats, vals))


@fam("012", mode="mc")
def mk_tallest(r, L):
    title, cats, vals, unit, who, hi = data(r, L)
    j = vals.index(max(vals))
    it = mc_key(f"{name(r)} will make a bar graph from the tally chart. Which category will have the tallest bar?", cats[j], [c for c in cats if c != cats[j]] + (["All the bars will be the same"] if len(cats) == 3 else []),
                ["The biggest count makes the tallest bar.", f"{cats[j]} has {vals[j]}."], qtype="visual", diagram=tally_d(title, cats, vals), r=r)
    it.check = FN("graph_extreme", cats=cats, vals=vals, want="most")
    return it


@fam("012", mode="mc")
def mk_parts(r, L):
    title, cats, vals, unit, who, hi = data(r, L)
    good = f"a title, a label for each bar, plus a scale that counts by 1s"
    bad = [f"only the bars", f"a title plus a scale that counts by 10s", f"one bar for all the {unit} together"]
    it = mc_key(f"{name(r)} is making a bar graph called “{title}.” What does the graph need?", good, bad, ["A bar graph needs a title, labels, and a scale.", "A Grade 2 bar graph uses a scale of 1."], qtype="conceptual", r=r)
    return it


@fam("012", mode="mc")
def mk_match(r, L):
    title, cats, vals, unit, who, hi = data(r, L)
    good = ", ".join(f"{c} {v}" for c, v in zip(cats, vals))
    def shuffled(k):
        rr = sub(r, k)
        vv = vals[:]
        rr.shuffle(vv)
        return vv
    bad = []
    for k in range(1, 10):
        vv = shuffled(k)
        s = ", ".join(f"{c} {v}" for c, v in zip(cats, vv))
        if vv != vals and s not in bad:
            bad.append(s)
    bad.append(", ".join(f"{c} {v + 1}" for c, v in zip(cats, vals)))
    bad = list(dict.fromkeys(bad))[:3]
    need(len(bad) == 3)
    it = mc_key(f"Which list of numbers matches the bar graph?", good, bad, ["Read each bar.", good + "."], qtype="visual", diagram=bar(title, cats, vals, unit, hi), r=r)
    it.check = FN("graph_list", cats=cats, vals=vals)
    return it


@fam("2")
def mk_add_cat(r, L):
    title, cats, vals, unit, who, hi = data(r, 2, 3)
    extra = r.randint(2, 9)
    tot = sum(vals) + extra
    return Item(f"The tally chart shows {len(cats)} groups. {name(r)} adds a new group with {extra}. How many will the graph show in all?", tot,
                [f"The chart has {' + '.join(map(str, vals))} = {sum(vals)}.", f"{sum(vals)} + {extra} = {tot}."],
                [W(sum(vals), "forgot the new group"), W(extra, "gave only the new group"), W(tot + 5, "counted a bundle twice")],
                EX("+".join(map(str, vals)) + f"+{extra}"), qtype="multi-step", tags={"multistep"}, diagram=tally_d(title, cats, vals))


@fam("012")
def mk_text_height(r, L):
    title, cats, vals, unit, who, hi = data(r, L)
    i = r.randrange(len(cats))
    return Item(f"Data: {data_text(cats, vals, unit)}. On a bar graph with a scale of 1, how tall is the {cats[i]} bar?", vals[i],
                [f"The data says {cats[i]} has {vals[i]}.", f"The bar goes up to {vals[i]} on the scale."],
                [W(vals[i] + 1, "counted one extra grid line"), W(vals[(i + 1) % len(vals)], "used the wrong category"), W(sum(vals), "added every category")],
                FN("tally_val", counts=vals, i=i), qtype="procedural", tags={"graph"})


@fam("012")
def mk_text_pics(r, L):
    title, cats, vals, unit, who, hi = data(r, L)
    i, j = r.sample(range(len(cats)), 2)
    return Item(f"Data: {data_text(cats, vals, unit)}. On a picture graph (1 picture each), how many pictures for {cats[i]} and {cats[j]}?", vals[i] + vals[j],
                [f"{cats[i]}: {vals[i]} pictures. {cats[j]}: {vals[j]} pictures.", f"{vals[i]} + {vals[j]} = {vals[i] + vals[j]}."],
                [W(abs(vals[i] - vals[j]), "subtracted instead of adding"), W(vals[i], "used only one row"), W(sum(vals), "added every row")],
                FN("bar_combo", vals=vals, plus=[i, j], minus=[]), qtype="procedural", tags={"graph"})


@fam("012")
def mk_text_diff(r, L):
    title, cats, vals, unit, who, hi = data(r, L)
    i, j = r.sample(range(len(cats)), 2)
    if vals[i] < vals[j]:
        i, j = j, i
    return Item(f"Data: {data_text(cats, vals, unit)}. On a bar graph, how much taller is the {cats[i]} bar than the {cats[j]} bar?", vals[i] - vals[j],
                [f"{cats[i]}: {vals[i]}. {cats[j]}: {vals[j]}.", f"{vals[i]} − {vals[j]} = {vals[i] - vals[j]}."],
                [W(vals[i] + vals[j], "added instead of subtracting"), W(vals[i], "gave the taller bar"), W(vals[i] - vals[j] + 1, "counted one extra")],
                FN("bar_diff", vals=vals, i=i, j=j), qtype="procedural", tags={"graph"})


SKILLS = {
    1: dict(name="Reading Picture Graphs", fams=[pg_value, pg_most, pg_total, pg_key, pg_two, pg_error]),
    2: dict(name="Reading Bar Graphs", fams=[bg_value, bg_most, bg_which, bg_total, bg_odd, bg_error]),
    3: dict(name="Solving Problems with Graphs", fams=[sp_more, sp_fewer, sp_together, sp_takeapart, sp_eq, sp_two_step, sp_text_more, sp_text_all]),
    4: dict(name="Making Picture Graphs and Bar Graphs", fams=[mk_bar_height, mk_pic_count, mk_tallest, mk_parts, mk_match, mk_add_cat, mk_text_height, mk_text_pics, mk_text_diff]),
}
