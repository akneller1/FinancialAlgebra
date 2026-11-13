"""Re-presentation layer for the Grade 1 deduplication pass.

When the same fact appears in two different skills, one copy is re-expressed as a different
task form. The mathematics is untouched — the item keeps its check (so verify1 still derives
the answer from stored inputs) and its answer — only the wording changes, and for arithmetic
we may wrap the same numbers in a short story.

Picture questions keep their picture (a clock with no clock is not a question); their wording
is varied instead. `templates()` returns (text, needs_picture) pairs.
"""
import re
from g1lib import Item, _norm

OBJECTS = ["apples", "stickers", "blocks", "marbles", "shells", "crayons", "books", "beans",
           "buttons", "tiles", "cards", "beads", "cups", "cones", "flowerpots", "ribbons",
           "pencils", "pretzels", "stamps", "balloons"]
NAMES = ["Ava", "Ben", "Carmen", "Dev", "Elena", "Femi", "Grace", "Hiro", "Isla", "Jamal",
         "Kai", "Lena", "Marco", "Nia", "Omar", "Priya", "Rosa", "Sam", "Tariq", "Uma",
         "Zoe", "Mateo", "Aisha", "Noah", "Sofia", "Liam", "Mei", "Diego", "Hana", "Eli"]


def _plural(word, n):
    return word if int(n) == 1 else word


def _add_templates(a, b, r):
    out = [(f"What is {a} + {b}?", False), (f"{a} + {b} = ___", False),
           (f"Add {a} and {b}.", False), (f"Find the sum of {a} and {b}.", False),
           (f"{b} + {a} = ___", False), (f"___ = {a} + {b}", False)]
    for k in range(6):
        n, m = r.randrange(len(NAMES)), r.randrange(len(NAMES))
        o = OBJECTS[r.randrange(len(OBJECTS))]
        out.append((f"{NAMES[n]} has {a} {o}. {NAMES[m]} gives {b} more {o}. How many {o} does {NAMES[n]} have now?", False))
        out.append((f"{a} {o} in a box and {b} more {o} on the table. How many {o} in all?", False))
    return out


def _sub_templates(a, b, r):
    out = [(f"What is {a} \u2212 {b}?", False), (f"{a} \u2212 {b} = ___", False),
           (f"Subtract {b} from {a}.", False), (f"Find {a} take away {b}.", False),
           (f"___ = {a} \u2212 {b}", False)]
    for k in range(5):
        n = NAMES[r.randrange(len(NAMES))]
        o = OBJECTS[r.randrange(len(OBJECTS))]
        out.append((f"{n} has {a} {o} and gives {b} away. How many {o} are left?", False))
        out.append((f"There are {a} {o}. {b} {o} are used. How many {o} are left?", False))
    return out


def _missing_templates(total, part, r):
    out = [(f"{part} + ___ = {total}", False), (f"{total} \u2212 {part} = ___", False),
           (f"What number completes {part} + ___ = {total}?", False), (f"___ = {total} \u2212 {part}", False)]
    for k in range(5):
        n = NAMES[r.randrange(len(NAMES))]
        o = OBJECTS[r.randrange(len(OBJECTS))]
        out.append((f"{n} has {part} {o}. How many more {o} are needed to have {total}?", False))
        out.append((f"{n} needs {total} {o} for a game and has {part}. How many more {o} does {n} need?", False))
    return out


def _place_templates(t, o, r):
    out = [(f"What number is {t} tens and {o} ones?", False), (f"{t} tens + {o} ones = ___", False),
           (f"Write the number: {t} tens, {o} ones.", False), (f"How many in all: {t} tens and {o} ones?", False)]
    for k in range(4):
        n = NAMES[r.randrange(len(NAMES))]
        out.append((f"{n} counts {t} full ten-frames and {o} more counters. How many counters in all?", False))
        out.append((f"A number has {t} tens and {o} ones. What is the number?", False))
    return out


def _ones_templates(n, t, r):
    return [(f"How many ones are in {n}?", False), (f"Which digit is in the ones place of {n}?", False),
            (f"In {n}, the ones digit is ___ .", False), (f"What is the ones digit of {n}?", False),
            (f"Look at {n}. How many ones does it have?", False)]


def _clock_templates(r):
    return [("What time is shown?", True), ("Write the time shown on the clock.", True),
            ("Read the clock. What time is it?", True), ("The clock shows ___ .", True),
            ("Look at the clock. What time does it show?", True)]


def _shape_templates(r):
    return [("What shape is this?", True), ("Name the shape.", True), ("Which shape is shown?", True),
            ("This shape is a ___ .", True), ("Look at the picture. What shape is it?", True)]


def _solid_templates(r):
    return [("What solid is this?", True), ("Name the solid.", True), ("Which solid is shown?", True),
            ("This solid is a ___ .", True)]


def _partition_templates(parts, r):
    if parts == 4:
        return [("What are the equal parts called?", True), ("The shape is cut into 4 equal parts. Name one part.", True),
                ("Each part is one ___ of the whole.", True), ("Four equal parts are called ___ .", True)]
    return [("What are the equal parts called?", True), ("The shape is cut into 2 equal parts. Name one part.", True),
            ("Each part is one ___ of the whole.", True), ("Two equal parts are called ___ .", True)]


def _ruler_templates(r):
    return [("How long is the object?", True), ("Use the ruler. How many units long is it?", True),
            ("Measure the object with the ruler. How long is it?", True), ("The object is ___ units long.", True)]


def _tally_templates(r):
    return [("Look at the tally chart. How many in all?", True), ("How many marks are there in all?", True),
            ("Count the tally marks. What is the total?", True)]


def _graph_templates(r):
    return [("Look at the graph. How many in all?", True), ("How many does the graph show in all?", True),
            ("Add the rows of the graph. How many in all?", True)]


def _compare_templates(r):
    return [("Which is longer?", True), ("Look at the two groups. Which one is longer?", True),
            ("Which object is longer?", True)]


def _ten_ones_templates(r):
    return [("How many ones are in 1 ten?", False), ("1 ten = ___ ones.", False),
            ("How many ones make one ten?", False), ("One ten is the same as ___ ones.", False),
            ("A full ten-frame holds how many counters?", False)]


def _shape_attr_templates(sides, r):
    return [(f"How many sides does this shape have?", True), ("Count the sides. How many are there?", True),
            (f"This shape has ___ sides.", True), ("How many straight sides does it have?", True)]


def _shape_kind_templates(kind, what, r):
    k = str(kind)
    return [(f"How many {what} does a {k} have?", True), (f"A {k} has ___ {what}.", True),
            (f"Count the {what} on the {k}. How many are there?", True)]


def _array_templates(r):
    return [("How many dots are in this array?", True), ("Count the dots in the array. How many are there?", True),
            ("This array has ___ dots.", True), ("Find the total number of dots.", True)]


def _rows_templates(r):
    return [("How many rows are in this array?", True), ("Count the rows in the array.", True),
            ("The array has ___ rows.", True)]


def _even_odd_templates(n, r):
    return [(f"Is {n} even or odd?", False), (f"Look at {n}. Is it even or odd?", False),
            (f"{n} counters are put into pairs. Is {n} even or odd?", False),
            (f"Tell whether {n} is even or odd.", False)]


def _polygon_templates(kind, what, r):
    k = str(kind)
    return [(f"How many {what} does this shape have?", True), (f"Count the {what}. How many are there?", True),
            (f"This {k} has ___ {what}.", True), (f"How many {what} are on the {k}?", True)]


def _parts_templates(r):
    return [("What are the equal parts called?", True), ("Name the equal parts of this shape.", True),
            ("Each part is one ___ of the whole.", True), ("What is this share called?", True)]


def _count_templates(r):
    return [("How many?", False), ("Count them. How many are there?", False), ("Count: ___ .", False)]


def _money_templates(r):
    return [("How much money is shown?", True), ("Count the coins. What is the total?", True),
            ("These coins are worth ___ .", True), ("Find the value of the coins.", True)]


def templates(check, r):
    """(text, needs_picture) pairs that re-ask the same mathematics in another form."""
    if check.get("k") != "fn":
        return []
    fn = check.get("fn")
    try:
        if fn == "add":
            return _add_templates(int(check["a"]), int(check["b"]), r)
        if fn == "sub":
            return _sub_templates(int(check["a"]), int(check["b"]), r)
        if fn == "missing_part":
            return _missing_templates(int(check["total"]), int(check["part"]), r)
        if fn == "tens_ones":
            return _place_templates(int(check["tens"]), int(check["ones"]), r)
        if fn in ("ones_of", "equiv_ones", "tens_from_ones"):
            return _ones_templates(int(check.get("n", check.get("ones", 0))), int(check.get("tens", 0)), r)
        if fn == "array_total":
            return _array_templates(r)
        if fn == "array_rows":
            return _rows_templates(r)
        if fn == "even_odd":
            return _even_odd_templates(int(check["n"]), r)
        if fn in ("polygon_sides", "polygon_corners"):
            return _polygon_templates(check.get("kind", "shape"), "sides" if fn == "polygon_sides" else "corners", r)
        if fn == "part_name":
            return _parts_templates(r)
        if fn == "count":
            return _count_templates(r)
        if fn == "money_cents":
            return _money_templates(r)
        if fn == "ten_ones":
            return _ten_ones_templates(r)
        if fn == "shape_attr_name":
            return _shape_attr_templates(int(check.get("sides", 4)), r)
        if fn in ("shape_sides", "shape_corners"):
            return _shape_kind_templates(check.get("kind", "shape"), "sides" if fn == "shape_sides" else "corners", r)
        if fn == "equal_parts":
            return [("Does this shape show equal parts?", True), ("Are the parts of this shape equal?", True),
                    ("Look at the parts. Are they equal?", True)]
        if fn in ("clock", "half_hour", "clock_minutes"):
            return _clock_templates(r)
        if fn == "shape_name":
            return _shape_templates(r)
        if fn == "solid_name":
            return _solid_templates(r)
        if fn in ("partition_word", "partition_count"):
            return _partition_templates(int(check.get("parts", 2)), r)
        if fn == "ruler":
            return _ruler_templates(r)
        if fn.startswith("tally"):
            return _tally_templates(r)
        if fn.startswith("graph"):
            return _graph_templates(r)
        if fn in ("longer_ab", "shorter", "longer", "which_group", "more_count"):
            return _compare_templates(r)
    except (KeyError, TypeError, ValueError):
        return []
    return []


def rewrite(item, check, used_texts, r, diagram=None):
    """Return an Item re-asking the same question, or None when no unused wording is left."""
    pool = templates(check, r)
    if not pool:
        return None
    fresh = [(t, need) for t, need in pool if _norm(t) not in used_texts]
    if not fresh:
        return None
    prompt, needs_pic = fresh[r.randrange(len(fresh))]
    if needs_pic and diagram is None:
        return None
    it = Item(prompt, item["answer"], item.get("solutionSteps") or ["Work it out."],
              check=check, qtype=(item.get("_meta") or {}).get("questionType") or "procedural", tags=())
    it.misconception = None
    it.diagram = diagram if needs_pic else None
    return it
