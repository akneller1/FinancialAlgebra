"""Build the Grade 2 (math2) banks with the shared Grade 1 builder.

Usage: python3 build2.py [unit-module ...]
Writes question-banks/math2/<unit>.json, meta/<unit>.meta.json,
assets/math2/<unit>/<id>.png and tools/grade2-authoring/out/<unit>.checks.json.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
G1 = os.path.abspath(os.path.join(HERE, "..", "grade1-authoring"))
sys.path.insert(0, HERE)
sys.path.insert(0, G1)

MODS = ["g2u01_add_sub_data", "g2u02_within100", "g2u03_length", "g2u04_number_line", "g2u05_numbers1000",
        "g2u06_geometry_time_money", "g2u07_within1000", "g2u08_equal_groups", "g2u09_together"]
os.environ["G1_OUTLINE"] = "outline2"
os.environ["G1_EXTRAS"] = "extras2"
os.environ["G1_OUT"] = os.path.join(HERE, "out")
os.environ["G1_MODS"] = ",".join(MODS)

import figs2          # noqa: F401  (registers the Grade 2 diagram kinds)
import build1
import sys as _sys
_sys.path.insert(0, os.path.join(HERE, "units"))

if __name__ == "__main__":
    build1.main()
