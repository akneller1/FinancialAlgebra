"""Grade 1 authoring helpers. Re-exports the Grade 2 helpers (tools/grade2-authoring/g2lib.py), which re-export the
Grade 3 and Grade 5 toolkits (Item, W, fam, EX/KEY/FN checks, Diagram, derived formats).
Family contract (same as Grades 2-5): f(r, L) -> Item, L = 0 Remedial (cp2), 1 Standard (cp1), 2 Advanced (honors)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(HERE, "..", "grade2-authoring"))
from g2lib import *            # noqa: F401,F403
from g2lib import _norm        # noqa: F401
import g5lib as _g5

# short, decodable names for first-grade reading
NAMES = ["Ava", "Ben", "Cam", "Dev", "Eli", "Finn", "Gus", "Ian", "Jay", "Kai", "Max", "Mia", "Nia", "Sam", "Tess", "Zoe",
         "Leo", "Ana", "Ted", "Ivy", "Mei", "Pam", "Raj", "Rosa", "Uma", "Liz", "Tom", "Dan", "Kim", "Abe"]
_g5.NAMES[:] = NAMES

# plural object nouns a first grader can read (singular, plural)
THINGS = [("apple", "apples"), ("ball", "balls"), ("bead", "beads"), ("block", "blocks"), ("book", "books"), ("car", "cars"),
          ("crayon", "crayons"), ("pen", "pens"), ("rock", "rocks"), ("shell", "shells"), ("sticker", "stickers"), ("marble", "marbles"),
          ("button", "buttons"), ("hat", "hats"), ("egg", "eggs"), ("leaf", "leaves"), ("cup", "cups"), ("kite", "kites"), ("cookie", "cookies")]
ANIMALS = [("bird", "birds"), ("duck", "ducks"), ("frog", "frogs"), ("bug", "bugs"), ("bee", "bees"), ("fish", "fish"), ("cat", "cats"), ("dog", "dogs")]


def animal(r):
    return pick(r, ANIMALS)


def thing(r):
    return pick(r, THINGS)


def ns(n, t):
    """'1 apple', '3 apples' for a THINGS pair."""
    return f"{n} {t[0] if n == 1 else t[1]}"


def wrong_near(ans, lo=0, hi=120, extra=()):
    """Plain off-by-one / off-by-two distractors with reasons, kept in range."""
    out = list(extra)
    for d, y in ((1, "counted one too many"), (-1, "counted one too few"), (2, "made a counting mistake"), (-2, "made a counting mistake")):
        if lo <= ans + d <= hi:
            out.append(W(ans + d, y))
    return out
