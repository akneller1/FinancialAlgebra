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
    return [(f"What is the ones digit of {n}?", False), (f"Which digit is in the ones place of {n}?", False),
            (f"In {n}, the ones digit is ___ .", False), (f"What is the ones digit of {n}?", False),
            (f"Look at {n}. Which digit shows the ones place?", False)]


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


def _partition_count_templates(parts, r):
    return [("How many equal parts are shown?", True),
            ("Count the equal parts. How many are there?", True),
            ("The whole is split into how many equal pieces?", True),
            ("How many parts make this whole?", True)]


def _tens_from_ones_templates(ones, r):
    return [(f"How many groups of ten can be made from {ones} ones?", False),
            (f"{ones} ones make how many tens?", False),
            (f"Trade {ones} ones for tens. How many tens?", False)]


def _shorter_templates(r):
    return [("Which object is shorter?", True),
            ("Look at the two objects. Which one is shorter?", True),
            ("Which of the two is the shorter one?", True)]


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
    if sides == 0:
        return [("Which shape shown has no corners?", True), ("Name the shape without straight sides.", True),
                ("Find the circle among these shapes.", True)]
    return [(f"Which shape shown has {sides} sides?", True),
            (f"Name a shape in the picture with {sides} sides.", True),
            (f"Find the shape with {sides} sides.", True)]


def _shape_kind_templates(kind, what, r):
    k = str(kind)
    return [(f"How many {what} does a {k} have?", True), (f"A {k} has ___ {what}.", True),
            (f"Count the {what} on the {k}. How many are there?", True)]


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
        if fn in ("ones_of", "equiv_ones"):
            return _ones_templates(int(check.get("n", 0)), int(check.get("tens", 0)), r)
        if fn == "tens_from_ones":
            return _tens_from_ones_templates(int(check["ones"]), r)
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
        if fn == "partition_word":
            return _partition_templates(int(check.get("parts", 2)), r)
        if fn == "partition_count":
            return _partition_count_templates(int(check.get("parts", 2)), r)
        if fn == "ruler":
            return _ruler_templates(r)
        if fn.startswith("tally"):
            return _tally_templates(r)
        if fn.startswith("graph"):
            return _graph_templates(r)
        if fn == "shorter":
            return _shorter_templates(r)
        if fn in ("longer_ab", "longer", "which_group", "more_count"):
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
