"""Generate units/uNN_*.py from the Grade 2 skill -> family mapping.

The mapping is the editorial decision of which question families serve each of the 89 Grade 2
skills in course-outlines/grade2.json. Modules are generated so a skill name can never drift
from the outline; skills with fewer than three families get the domain filler so every skill
can still reach 30 unique questions per level.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from outline2 import UNITS

DOMAIN = {"u01_add_sub_data": "oa", "u02_within100": "oa", "u03_length": "md", "u04_number_line": "nbt",
          "u05_numbers1000": "nbt", "u06_geometry_time_money": "g", "u07_within1000": "nbt",
          "u08_equal_groups": "oa", "u09_together": "oa"}

MAP = {
    "u01_add_sub_data": {
        1: ["make_ten_items()", "make_ten_fill_items()"],
        2: ["fact_family_items(20)", "sub_items(hi=20)"],
        3: ["add_items(hi=20, sums_to=20)", "doubles_items()", "add2_items(compose=False)"],
        4: ["sort_items()", "graph_items('pictograph')"],
        5: ["graph_items('bargraph')", "tally_items('total')"],
        6: ["graph_items('pictograph')", "graph_items('bargraph')"],
        7: ["graph_items('bargraph')", "tally_items('total')", "missing_addend_items(20)"],
        8: ["tape_compare_items()", "story_items('partwhole')"],
        9: ["sub2_items(regroup=False)", "story_items('compare')"],
        10: ["story_items('compare')", "missing_addend_items(20)"],
        11: ["story_match_items()", "equation_items()"],
    },
    "u02_within100": {
        1: ["base_ten_items('build')", "tens_ones_equiv_items()"],
        2: ["add2_items(compose=False)"],
        3: ["sub2_items(regroup=False)"],
        4: ["missing_addend_items(20)", "sub2_items(regroup=False)"],
        5: ["sub2_items(regroup=True)", "base_ten_items('regroup')"],
        6: ["sub2_items(regroup=True)", "base_ten_items('value')"],
        7: ["strategy_items()", "method_compare_items()"],
        8: ["tape_compare_items()", "story_items('join')"],
        9: ["add2_items()", "sub2_items()"],
        10: ["two_step_items()", "story_items('start-unknown')"],
        11: ["missing_addend_items(20)", "story_items('change-unknown')"],
    },
    "u03_length": {
        1: ["ruler_items()", "count_collection_items(120)"],
        2: ["measure_unit_items('metric')", "ruler_items()"],
        3: ["measure_unit_items('metric')"],
        4: ["measure_compare_items('metric')", "length_word_items()"],
        5: ["measure_unit_items('customary')", "ruler_items()"],
        6: ["measure_unit_items('customary')", "length_compare_items()"],
        7: ["measure_unit_items('customary')", "measure_unit_items('metric')"],
        8: ["length_word_items()", "two_step_items()"],
        9: ["lineplot_items('at')", "tally_items('total')"],
        10: ["lineplot_items('at')", "lineplot_items('total')"],
        11: ["lineplot_items('most')", "lineplot_items('total')"],
    },
    "u04_number_line": {
        1: ["numberline_items('locate')", "count_by_items(10, 100)"],
        2: ["numberline_items('jump')", "count_items(hi=100)"],
        3: ["numberline_items('locate')", "round10_items()"],
        4: ["numberline_items('jump')", "add_items(hi=60, sums_to=100)"],
        5: ["sub2_items(regroup=False)", "numberline_items('jump')"],
        6: ["story_items('join')", "numberline_items('jump')"],
        7: ["add2_items()", "skip_count_items(10)"],
    },
    "u05_numbers1000": {
        1: ["base_ten_items('regroup')", "place3_items('hundred_more')"],
        2: ["place3_items('value')", "base_ten_items('value')"],
        3: ["place3_items('expanded')", "write_numeral_items()"],
        4: ["place3_items('value')", "tens_ones_equiv_items()"],
        5: ["skip_count_items(100)", "skip_count_items(10)"],
        6: ["numberline_items('locate')", "skip_count_items(100)"],
        7: ["compare3_items(symbol=True)", "compare3_items()"],
        8: ["order3_items(3)", "order3_items(4)"],
    },
    "u06_geometry_time_money": {
        1: ["polygon_items('name')", "shape_identify_items()"],
        2: ["polygon_items('sides')", "polygon_items('corners')"],
        3: ["solid_items()", "compose_items()"],
        4: ["thirds_items('name')", "partition_items()"],
        5: ["thirds_items('name')", "thirds_items('count')"],
        6: ["thirds_items('name')", "thirds_items('shaded')"],
        7: ["equal_parts_items()", "thirds_items('shaded')"],
        8: ["time5_items()", "clock_items(half=True)"],
        9: ["time5_items()", "digital_items()"],
        10: ["time_word_items()", "time5_items()"],
        11: ["clock_items(half=True)", "time5_items()"],
        12: ["money_items('count')", "money_items('word')"],
        13: ["money_items('count')", "money_items('word')"],
        14: ["money_items('word')", "money_items('count')"],
        15: ["money_items('word')", "two_step_items()"],
    },
    "u07_within1000": {
        1: ["add3_items(compose=False)"],
        2: ["sub3_items()"],
        3: ["add3_items()", "numberline_items('jump')"],
        4: ["add3_items(compose=True)"],
        5: ["add3_items(compose=True)", "place3_items('hundred_more')"],
        6: ["strategy_items()", "explain_strategy_items()"],
        7: ["sub3_items()", "base_ten_items('regroup')"],
        8: ["sub3_items()", "sub2_items(regroup=True)"],
        9: ["sub3_items()", "base_ten_items('value')"],
        10: ["sub3_items()", "strategy_items()"],
    },
    "u08_equal_groups": {
        1: ["even_odd_items()", "count_items(hi=20)"],
        2: ["even_odd_items()", "count_collection_items(20)"],
        3: ["doubles_items()", "even_odd_items()"],
        4: ["array_items('rows')", "array_items('total')"],
        5: ["repeated_add_items()", "array_items('total')"],
        6: ["array_items('total')", "partition_items()"],
        7: ["array_items('total')", "array_items('rows')"],
    },
    "u09_together": {
        1: ["mixed_facts_items(20)", "fact_family_items(20)"],
        2: ["make_ten_items()", "missing_addend_items(20)"],
        3: ["lineplot_items('at')", "measure_compare_items('metric')"],
        4: ["place3_items('expanded')", "place3_items('value')"],
        5: ["add3_items()", "sub3_items()"],
        6: ["add2_items()", "sub2_items()"],
        7: ["tape_compare_items()", "equation_items()"],
        8: ["two_step_items()", "story_items('start-unknown')"],
        9: ["story_match_items()", "tape_compare_items()"],
    },
}


def build_module(name):
    idx = list(MAP).index(name)
    unit = UNITS[idx]
    domain = DOMAIN[name]
    lines = [f'"""{unit["name"]} — Grade 2 question families for {unit["id"]}."""',
             "from fam2 import *", "", f"DOMAIN = {domain!r}", "", "SKILLS = {"]
    for i, skill_name in enumerate(unit["skills"], 1):
        fams = list(MAP[name][i])
        if len(fams) < 3 and all("domain_facts_items" not in f for f in fams):
            fams.append(f"domain_facts_items({domain!r})")
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
