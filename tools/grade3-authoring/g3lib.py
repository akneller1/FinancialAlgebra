"""Grade 3 authoring helpers. Re-exports the shared problem toolkit (tools/grade5-authoring/g5lib.py: Item, W, fam,
checks EX/KEY/FN, Diagram, derived formats) and adds Grade 3 formatting: unreduced fractions, clock times, contexts.
Family contract (same as Grade 5): f(r, L) -> Item, L = 0 Remedial (cp2), 1 Standard (cp1), 2 Advanced (honors)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(HERE, "..", "grade5-authoring"))
from g5lib import *            # noqa: F401,F403  (Item, W, fam, EX, KEY, FN, Diagram, need, pick, name, comma, mc_key, Reject ...)
from g5lib import _norm        # noqa: F401
import g5lib as _g5

# Shorter, familiar names for third-grade reading (decodable, varied backgrounds).
NAMES = ["Ava", "Ben", "Cora", "Dev", "Ella", "Finn", "Gabi", "Hugo", "Isla", "Jada", "Kai", "Lena", "Max", "Nia", "Omar",
         "Pia", "Raj", "Rosa", "Sam", "Tess", "Uma", "Leo", "Zoe", "Mia", "Eli", "Ana", "Theo", "Ivy", "Luis", "Mei", "Noah", "Amir"]
_g5.NAMES[:] = NAMES

ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
DEN_WORD = {2: "halves", 3: "thirds", 4: "fourths", 6: "sixths", 8: "eighths"}
DEN_ONE = {2: "half", 3: "third", 4: "fourth", 6: "sixth", 8: "eighth"}
G3_DENS = [2, 3, 4, 6, 8]


def fr(n, d):
    """Unreduced fraction text a/b (Grade 3 keeps the partition the student sees)."""
    return f"{n}/{d}"


def tm(h, m):
    """Clock time text, 12-hour, no a.m./p.m.: 4:05."""
    h = (h - 1) % 12 + 1
    return f"{h}:{m:02d}"


def add_min(h, m, k):
    t = h * 60 + m + k
    return (t // 60 - 1) % 12 + 1, t % 60


def mins(n):
    return f"{n} {'minute' if n == 1 else 'minutes'}"


def times_word(n):
    return ONES[n] if 0 <= n <= 10 else str(n)


# Grade 3 repeated-addition select-all cards must test ONE idea per card.
# The core eg_repeated family alternates between finding a total and counting
# addends. Both are valid on their own, but mixing them in a four-choice
# "matched answer" card makes one choice test a different task.
from g5lib import select_of as _shared_select_of


def select_of(core, k_true=2, k_false=2):
    if core.__name__ != "eg_repeated":
        return _shared_select_of(core, k_true, k_false)

    def groups_only(r, L):
        if L == 0:
            g, n = r.randint(2, 5), r.randint(2, 5)
        elif L == 1:
            g, n = r.randint(3, 6), r.randint(3, 8)
        else:
            g, n = r.randint(4, 7), r.randint(4, 9)
        summands = " + ".join([str(n)] * g)
        return Item(
            f"Complete the equation: {summands} = ___ × {n}", g,
            [f"Count the addends: there are {g} addends of {n}.",
             f"{summands} = {g} × {n}."],
            [W(g + 1, "counted one extra addend"),
             W(g - 1, "missed one addend"),
             W(g * n, "used the total instead of the group count")],
            FN("repadd_groups", sum=summands, addend=n),
            qtype="fill-blank", tags={"multiple-representations"}
        )

    groups_only.__name__ = core.__name__
    groups_only.levels = core.levels
    groups_only.mode = core.mode
    groups_only.qtype = core.qtype
    return _shared_select_of(groups_only, k_true, k_false)
