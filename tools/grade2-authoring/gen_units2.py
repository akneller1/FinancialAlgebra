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
        1: ["fluency_items()", "strategy_items()"],
        2: ["fluency_items()", "fact_family_items(20)"],
        3: ["fluency_items()", "add2_items(compose=False)"],
        4: ["graph_data_items('pictograph')", "tally_data_items('count_one')"],
        5: ["graph_data_items('bargraph')", "tally_data_items('total')"],
        6: ["graph_data_items('pictograph')", "graph_data_items('bargraph')"],
        7: ["graph_data_items('bargraph')", "two_step_items()"],
        8: ["tape_compare_items()", "two_step_items()"],
        9: ["sub2_items(regroup=False)", "tape_compare_items()"],
        10: ["tape_compare_items()", "fluency_items()"],
        11: ["tape_compare_items()", "story_match_items()"],
    },
    "u02_within100": {
        1: ["baseten_items('build')", "baseten_items('value')"],
        2: ["add2_items(compose=False)"],
        3: ["sub2_items(regroup=False)"],
        4: ["fluency_items()", "add2_items(compose=False)"],
        5: ["sub2_items(regroup=True)", "baseten_items('regroup')"],
        6: ["sub2_items(regroup=True)", "baseten_items('value')"],
        7: ["strategy_items()"],
        8: ["tape_compare_items()", "two_step_items()"],
        9: ["add2_items()", "sub2_items()"],
        10: ["two_step_items()", "tape_compare_items()"],
        11: ["fluency_items()", "two_step_items()"],
    },
    "u03_length": {
        1: ["measure_compare_items('metric')", "ruler_items()"],
        2: ["measure_unit_items('metric')", "measure_compare_items('metric')"],
        3: ["measure_unit_items('metric')"],
        4: ["measure_compare_items('metric')", "two_step_items()"],
        5: ["measure_unit_items('customary')", "measure_compare_items('customary')"],
        6: ["measure_unit_items('customary')"],
        7: ["measure_unit_items('customary')", "measure_unit_items('metric')"],
        8: ["measure_compare_items('customary')", "two_step_items()"],
        9: ["lineplot_items('at')", "tally_data_items('total')"],
        10: ["lineplot_items('at')", "lineplot_items('total')"],
        11: ["lineplot_items('most')", "lineplot_items('total')"],
    },
    "u04_number_line": {
        1: ["numberline_items('locate')", "skip_count_items()"],
        2: ["numberline_items('jump')", "fluency_items()"],
        3: ["numberline_items('locate')", "round_items()"],
        4: ["numberline_items('jump')", "add2_items()"],
        5: ["sub2_items(regroup=False)", "numberline_items('jump')"],
        6: ["two_step_items()", "numberline_items('jump')"],
        7: ["add2_items()", "skip_count_items()"],
    },
    "u05_numbers1000": {
        1: ["baseten_items('regroup')", "place3_items('value')"],
        2: ["place3_items('value')", "baseten_items('build')"],
        3: ["place3_items('expanded')", "place3_items('hundred_more')"],
        4: ["place3_items('value')", "baseten_items('regroup')"],
        5: ["skip_count_items()", "skip_count_items(100)"],
        6: ["numberline_items('locate')", "skip_count_items()"],
        7: ["compare3_items(symbol=True)", "compare3_items()"],
        8: ["order3_items()", "order3_items(4)"],
    },
    "u06_geometry_time_money": {
        1: ["polygon_items('name')", "shape_items('name')"],
        2: ["polygon_items('sides')", "polygon_items('corners')"],
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
        15: ["money_items('word')", "two_step_items()"],
    },
    "u07_within1000": {
        1: ["add3_items(rename=False)"],
        2: ["sub3_items()"],
        3: ["add3_items()", "numberline_items('jump')"],
        4: ["add3_items(rename=True)"],
        5: ["add3_items()", "place3_items('hundred_more')"],
        6: ["strategy_items()"],
        7: ["sub3_items()", "baseten_items('regroup')"],
        8: ["sub3_items()", "sub2_items(regroup=True)"],
        9: ["sub3_items()", "baseten_items('value')"],
        10: ["sub3_items()", "strategy_items()"],
    },
    "u08_equal_groups": {
        1: ["even_odd_items()"],
        2: ["even_odd_items()", "array_items('total')"],
        3: ["doubles_items()", "even_odd_items()"],
        4: ["array_items('rows')", "array_items('total')"],
        5: ["repeated_add_items()", "array_items('total')"],
        6: ["array_items('total')", "repeated_add_items()"],
        7: ["array_items('total')", "array_items('rows')"],
    },
    "u09_together": {
        1: ["fluency_items()"],
        2: ["strategy_items()", "fluency_items()"],
        3: ["lineplot_items('at')", "measure_compare_items('metric')"],
        4: ["place3_items('expanded')", "place3_items('value')"],
        5: ["add3_items()", "sub3_items()"],
        6: ["add2_items()", "sub2_items()"],
        7: ["tape_compare_items()", "two_step_items()"],
        8: ["two_step_items()", "tape_compare_items()"],
        9: ["tape_compare_items()", "story_match_items()"],
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
