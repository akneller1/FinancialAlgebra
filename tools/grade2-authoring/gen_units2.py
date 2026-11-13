"""Generate units/uNN_*.py from the Grade 2 skill -> family mapping.

The mapping is the editorial decision of which question families serve each of the 89 Grade 2
skills in course-outlines/grade2.json. Modules are generated so a skill name can never drift
from the outline; skills with fewer than three families get the domain filler so every skill
can still reach 30 unique questions per level.
"""
import os
import re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from outline2 import UNITS

DOMAIN = {"u01_add_sub_data": "oa", "u02_within100": "oa", "u03_length": "md", "u04_number_line": "nbt",
          "u05_numbers1000": "nbt", "u06_geometry_time_money": "g", "u07_within1000": "nbt",
          "u08_equal_groups": "oa", "u09_together": "oa"}

MAP = {
    "u01_add_sub_data": {
        1: ["fluency_items()", "strategy_items()"],
        2: ["fluency_items()", "fact_family_items(20)"],
        3: ["fluency_items()", "add2_items(compose=False)"],
        4: ["graph_data_items('pictograph')", "tally_data_items('count_one')"],
        5: ["graph_data_items('bargraph')", "tally_data_items('total')"],
        6: ["graph_data_items('pictograph')", "graph_data_items('bargraph')"],
        7: ["graph_data_items('bargraph')", "graph_data_items('pictograph')", "tally_data_items('total')"],
        8: ["tape_compare_items(100)", "two_step_items(100)"],
        9: ["sub2_items(regroup=False)", "tape_compare_items()"],
        10: ["tape_compare_items()", "tape_compare_items(limit=100)"],
        11: ["tape_compare_items()", "story_match_items()"],
    },
    "u02_within100": {
        1: ["baseten_items('build')", "baseten_items('value')"],
        2: ["add2_items(compose=False)"],
        3: ["sub2_items(regroup=False)"],
        4: ["missing_addend_items()", "fact_family_items(100)"],
        5: ["sub2_items(regroup=True)", "baseten_items('regroup')"],
        6: ["sub2_items(regroup=True)", "baseten_items('value')"],
        7: ["strategy_items()", "sub2_items(regroup=True)", "baseten_items('regroup')"],
        8: ["tape_compare_items(100)", "two_step_items(100)"],
        9: ["add2_items()", "sub2_items()"],
        10: ["two_step_items(100)", "two_step_items(limit=100)"],
        11: ["add2_items()", "two_step_items(100)"],
    },
    "u03_length": {
        1: ["measure_compare_items('metric', 100)", "ruler_items()"],
        2: ["measure_unit_items('metric')", "measure_compare_items('metric', 100)"],
        3: ["measure_unit_items('metric')"],
        4: ["measure_compare_items('metric', 100)", "two_step_items()"],
        5: ["measure_unit_items('customary')", "measure_compare_items('customary', 100)"],
        6: ["measure_unit_items('customary')"],
        7: ["measure_unit_items('customary')", "measure_unit_items('metric')"],
        8: ["measure_compare_items('customary', 100)", "two_step_items()"],
        9: ["lineplot_items('at')", "tally_data_items('total')"],
        10: ["lineplot_items('at')", "lineplot_items('total')"],
        11: ["lineplot_items('most')", "lineplot_items('total')"],
    },
    "u04_number_line": {
        1: ["numberline_items('locate')", "skip_count_items()"],
        2: ["numberline_items('jump')", "numberline_items('locate')"],
        3: ["numberline_items('locate')", "round_items()"],
        4: ["numberline_items('jump')", "add2_items()"],
        5: ["sub2_items(regroup=False)", "numberline_items('jump')"],
        6: ["two_step_items()", "numberline_items('jump')"],
        7: ["add2_items()", "skip_count_items()"],
    },
    "u05_numbers1000": {
        1: ["baseten_items('regroup')", "place3_items('value')"],
        2: ["place3_items('value')", "baseten_items('build')"],
        3: ["place3_items('expanded')", "place3_items('value')"],
        4: ["place3_items('value')", "baseten_items('regroup')"],
        5: ["skip_count_items()", "skip_count_items(100)"],
        6: ["numberline_items('locate')", "numberline_items('jump')"],
        7: ["compare3_items(symbol=True)", "compare3_items()"],
        8: ["order3_items()", "order3_items(4)", "order_choice_items()"],
    },
    "u06_geometry_time_money": {
        1: ["polygon_items('name')", "polygon_items('sides')", "polygon_items('corners')"],
        2: ["polygon_items('sides')", "polygon_items('corners')", "polygon_items('name')"],
        3: ["solid_items()", "polygon_items('name')"],
        4: ["thirds_items('name')", "thirds_items('count')"],
        5: ["thirds_items('count')", "thirds_items('name')"],
        6: ["thirds_items('name')", "thirds_items('shaded')"],
        7: ["thirds_items('shaded')", "thirds_items('count')"],
        8: ["time_items()"],
        9: ["time_items()", "time_word_items()"],
        10: ["time_word_items()", "time_items()"],
        11: ["time_items()"],
        12: ["money_items('count')", "money_items('word')"],
        13: ["money_items('count')", "money_items('word')"],
        14: ["money_items('word')", "money_items('count')"],
        15: ["money_items('word')", "money_items('count')"],
    },
    "u07_within1000": {
        1: ["add3_items(rename=False)", "place3_items('hundred_more')"],
        2: ["sub3_items(decompose=False, styles=(0, 1))", "sub3_items(decompose=False, styles=(2,))"],
        3: ["add3_items()", "numberline_items('jump')"],
        4: ["add3_items(rename=True, styles=(0, 1))", "add3_items(rename=True, styles=(2,))"],
        5: ["add3_items(rename=True, styles=(0, 1))", "add3_items(rename=True, styles=(2,))"],
        6: ["strategy_items()", "add3_items(rename=True)", "place3_items('value')"],
        7: ["sub3_items(decompose=True, styles=(0, 1))", "sub3_items(decompose=True, styles=(2,))"],
        8: ["sub3_items(decompose=True, styles=(0, 1))", "sub3_items(decompose=True, styles=(2,))"],
        9: ["sub3_items(decompose=True, styles=(0, 1))", "sub3_items(decompose=True, styles=(2,))"],
        10: ["sub3_items(decompose=True)", "strategy_items()"],
    },
    "u08_equal_groups": {
        1: ["even_odd_items()"],
        2: ["even_odd_items()", "array_items('total')"],
        3: ["doubles_items()", "even_odd_items()"],
        4: ["array_items('rows')", "array_items('total')", "array_items('cols')"],
        5: ["repeated_add_items()", "array_items('total')"],
        6: ["array_items('total')", "repeated_add_items()"],
        7: ["array_items('total')", "array_items('rows')", "array_items('cols')"],
    },
    "u09_together": {
        1: ["fluency_items()"],
        2: ["strategy_items()", "fluency_items()"],
        3: ["lineplot_items('at')", "measure_compare_items('metric', 100)"],
        4: ["place3_items('expanded')", "place3_items('value')"],
        5: ["add3_items()", "sub3_items()"],
        6: ["add2_items()", "sub2_items()"],
        7: ["tape_compare_items(100)", "two_step_items(100)"],
        8: ["two_step_items(100)", "two_step_items(limit=100)"],
        9: ["tape_compare_items()", "story_match_items()"],
    },
}


LIMITABLE = {"fluency_items", "numberline_items", "graph_data_items", "tally_data_items",
             "strategy_items", "baseten_items",
             "skip_count_items", "two_step_items", "tape_compare_items", "measure_compare_items"}


# skills reviewed by hand and re-familied to match their stated task
REVIEWED = {
    ("u02_within100", 2): ["two_digit_items('add', styles=(0, 1))", "two_digit_items('add', styles=(2,))"],
    ("u02_within100", 3): ["two_digit_items('sub', styles=(0, 1))", "two_digit_items('sub', styles=(2,))"],
    ("u01_add_sub_data", 10): ["tape_compare_items()", "tape_compare_items(limit=100)"],
    ("u05_numbers1000", 3): ["place3_items('expanded')", "place3_items('value')"],
    ("u06_geometry_time_money", 11): ["time_items(marks=(15, 30, 45))", "time_word_items()"],
    ("u08_equal_groups", 1): ["even_odd_items()", "skip_count_items(2, limit=20)"],
    ("u02_within100", 10): ["two_step_items(100)", "two_step_items(limit=100)"],
    ("u07_within1000", 1): ["add3_items(rename=False, styles=(0, 1))", "add3_items(rename=False, styles=(2,))"],
    ("u07_within1000", 2): ["sub3_items(decompose=False, styles=(0, 1))", "sub3_items(decompose=False, styles=(2,))"],
    ("u07_within1000", 4): ["add3_items(rename=True, styles=(0, 1))", "two_digit_items('add', compose=True, styles=(2,))"],
    ("u07_within1000", 5): ["add3_items(rename=True, styles=(0, 1))", "two_digit_items('add', compose=True, styles=(2,))"],
    ("u07_within1000", 7): ["sub3_items(decompose=True, styles=(0, 1), borrow='hundred')",
                            "sub3_items(decompose=True, styles=(2,), borrow='hundred')"],
    ("u07_within1000", 8): ["sub3_items(decompose=True, styles=(0, 1))", "two_digit_items('sub', compose=True, styles=(2,))"],
    ("u07_within1000", 9): ["sub3_items(decompose=True, styles=(0, 1))", "sub3_items(decompose=True, styles=(2,))"],
}
for (_unit, _idx), _fams in REVIEWED.items():
    MAP[_unit][_idx] = _fams

# a second on-topic family for skills that only listed one
SECOND_FAMILY = {
    ("u02_within100", 2): "fluency_items()",
    ("u02_within100", 3): "fluency_items()",
    ("u02_within100", 7): ["sub2_items(regroup=True)", "baseten_items('regroup')"],
    ("u03_length", 3): "measure_compare_items('metric', 100)",
    ("u03_length", 6): "measure_compare_items('customary', 100)",
    ("u06_geometry_time_money", 8): "time_word_items()",
    ("u06_geometry_time_money", 11): "time_word_items()",
    ("u02_within100", 10): ["two_step_items(100)", "two_step_items(limit=100)"],
    ("u07_within1000", 1): [],
    ("u07_within1000", 2): [],
    ("u07_within1000", 4): [],
    ("u07_within1000", 6): ["add3_items(rename=True)", "place3_items('value')"],
    ("u08_equal_groups", 1): "doubles_items()",
    ("u09_together", 1): "doubles_items()",
}


def build_module(name):
    idx = list(MAP).index(name)
    unit = UNITS[idx]
    domain = DOMAIN[name]
    lines = [f'"""{unit["name"]} — Grade 2 question families for {unit["id"]}."""',
             "from fam2 import *", "", f"DOMAIN = {domain!r}", "", "SKILLS = {"]
    for i, skill_name in enumerate(unit["skills"], 1):
        fams = [f for f in MAP[name][i] if "domain_facts_items" not in f]
        cap = re.search(r"within (\d[\d,]*)", skill_name.lower())
        if cap:
            n = cap.group(1).replace(",", "")
            def _with(f):
                args = f[f.index("("):] if "(" in f else ""
                if ("limit=" in f or "," in args or re.search(r"\(\s*\d", f)
                        or f.split("(")[0] not in LIMITABLE):
                    return f
                base = f[:-1]
                sep = "" if base.endswith("(") else ", "
                return f"{base}{sep}limit={n})"
            fams = [_with(f) for f in fams]
        fams = [f for f in fams]
        if len(fams) < 2:
            extra = SECOND_FAMILY.get((name, i))
            if extra:
                fams.extend([extra] if isinstance(extra, str) else extra)
        lines.append(f'    {i}: {{"name": {skill_name!r}, "fams": [{", ".join(fams)}]}},')
    lines.append("}")
    return "\n".join(lines) + "\n"


def main():
    for nm in MAP:
        path = os.path.join(HERE, "units", "g2" + nm + ".py")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(build_module(nm))
        print("wrote", os.path.basename(path))


if __name__ == "__main__":
    main()
