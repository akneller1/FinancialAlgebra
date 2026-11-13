"""Grade 2 authoring helpers. Re-exports the Grade 3 helpers (tools/grade3-authoring/g3lib.py), which re-export the shared
problem toolkit (tools/grade5-authoring/g5lib.py: Item, W, fam, EX/KEY/FN checks, Diagram, derived formats).
Family contract (same as Grades 3-5): f(r, L) -> Item, L = 0 Remedial (cp2), 1 Standard (cp1), 2 Advanced (honors)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(HERE, "..", "grade3-authoring"))
sys.path.append(os.path.join(HERE, "..", "grade5-authoring"))
from g3lib import *            # noqa: F401,F403
from g5lib import _norm        # noqa: F401
import g5lib as _g5

# short, decodable names for second-grade reading
NAMES = ["Ava", "Ben", "Cam", "Dev", "Ella", "Finn", "Gus", "Hana", "Ian", "Jada", "Kai", "Lena", "Max", "Nia", "Omar",
         "Pia", "Raj", "Rosa", "Sam", "Tess", "Uma", "Leo", "Zoe", "Mia", "Eli", "Ana", "Ted", "Ivy", "Luis", "Mei", "Noah", "Amir"]
_g5.NAMES[:] = NAMES

ONES_W = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen",
          "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS_W = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def words(n):
    """Number name for 0..1000 (hyphenated two-digit names: forty-six)."""
    if n < 20:
        return ONES_W[n]
    if n < 100:
        return TENS_W[n // 10] + ("-" + ONES_W[n % 10] if n % 10 else "")
    if n < 1000:
        return ONES_W[n // 100] + " hundred" + (" " + words(n % 100) if n % 100 else "")
    return "one thousand"


def expanded(n):
    """Expanded form without zero terms: 406 -> '400 + 6'."""
    parts = [n // 100 * 100, n // 10 % 10 * 10, n % 10]
    return " + ".join(str(p) for p in parts if p) or "0"


def cents(n):
    return f"{n}¢"


def dollars(c):
    """Amount in cents as $D.CC."""
    return f"${c // 100}.{c % 100:02d}"


COINV = {"penny": 1, "nickel": 5, "dime": 10, "quarter": 25}
COINPL = {"penny": "pennies", "nickel": "nickels", "dime": "dimes", "quarter": "quarters"}


def coin_list(cs):
    """['quarter','dime','dime'] -> '1 quarter and 2 dimes'"""
    from collections import Counter
    c = Counter(cs)
    order = [k for k in ("quarter", "dime", "nickel", "penny") if c[k]]
    parts = [f"{c[k]} {k if c[k] == 1 else COINPL[k]}" for k in order]
    return parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1]


def pl(n, w):
    """'1 ten', '3 tens', '1 hundred', '0 ones'"""
    return f"{n} {w}" if n == 1 else f"{n} {w}s"


def tens_ones(n):
    return f"{pl(n // 10, 'ten')} and {pl(n % 10, 'one')}"


def hto(n):
    return f"{pl(n // 100, 'hundred')}, {pl(n // 10 % 10, 'ten')}, and {pl(n % 10, 'one')}"


def ampm(h24):
    return "AM" if h24 < 12 else "PM"


def art(w):
    """'an apple', 'a pencil'"""
    return ("an " if w[:1].lower() in "aeiou" else "a ") + w


def Art(w):
    a = art(w)
    return a[0].upper() + a[1:]
