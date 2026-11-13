"""Cross-skill deduplication for the Grade 2 banks (same engine as Grade 1)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "units"))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "grade1-authoring")))
os.environ["G1_OUTLINE"] = "outline2"
os.environ["G1_OUT"] = os.path.join(HERE, "out")
os.environ["G1_MODS"] = ",".join(["g2u01_add_sub_data", "g2u02_within100", "g2u03_length",
                                 "g2u04_number_line", "g2u05_numbers1000", "g2u06_geometry_time_money",
                                 "g2u07_within1000", "g2u08_equal_groups", "g2u09_together"])
import figs2          # noqa: F401  registers Grade 2 diagram kinds
import dedupe1

if __name__ == "__main__":
    dedupe1.main()
