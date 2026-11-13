"""Generate units/uNN_*.py from the skill -> family mapping below.

The mapping is the editorial decision of which question families serve each of the 93 Grade 1
skills; the unit modules are generated so a skill name can never drift from the outline.
Skills with fewer than three families get the domain filler (domain_facts_items) so every
skill has enough independent draws to reach 30 unique questions per level.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from outline import UNITS

DOMAIN = {"u01_add_sub_data": "oa", "u02_story": "oa", "u03_within20": "oa", "u04_numbers99": "nbt",
          "u05_within100": "nbt", "u06_length": "md", "u07_geometry_time": "g", "u08_together": "oa"}

MAP = {
    "u01_add_sub_data": {
        1: ["add1_items()", "add1_items(back=True)", "one_more_less_items(12)", "count_items(hi=20)"],
        2: ["add_items(hi=10, sums_to=10, diagram='tenframe')", "missing_addend_items(10)", "make_ten_fill_items()"],
        3: ["add_items(hi=10, sums_to=10)", "sub_items(hi=10)", "mixed_facts_items(10)", "fact_family_items(10)"],
        4: ["sort_items()", "compare_groups_items('which')"],
        5: ["tally_items('count_one')", "tally_items('total')"],
        6: ["tally_items('count_one')", "graph_items('pictograph')"],
        7: ["tally_items('read')", "tally_items('count_one')"],
        8: ["graph_items('pictograph')", "tally_items('total')"],
        9: ["compare_groups_items('more')", "compare_groups_items('fewer')", "graph_items('bargraph')"],
    },
    "u02_story": {
        1: ["story_items('join')", "story_items('partwhole')"],
        2: ["story_items('change-unknown')", "story_items('start-unknown')"],
        3: ["equation_items()", "story_items('join')"],
        4: ["equal_sign_items()", "true_false_equation_items()"],
        5: ["partition_numbers_items()", "missing_addend_items()"],
        6: ["story_items('partwhole')", "missing_addend_items()"],
        7: ["make_ten_fill_items()", "missing_addend_items()", "partition_numbers_items()"],
        8: ["compare_groups_items('more')", "compare_groups_items('fewer')"],
        9: ["compare_groups_items('fewer')", "story_items('compare')"],
        10: ["count_on_difference_items()", "story_items('compare')"],
        11: ["story_items('join')", "story_items('separate')", "story_items('compare')", "story_items('partwhole')"],
        12: ["make_ten_fill_items()", "partition_numbers_items()"],
        13: ["equation_items()", "story_items('join')"],
        14: ["story_match_items()", "equation_items()"],
    },
    "u03_within20": {
        1: ["add_items(hi=10, sums_to=10)", "mixed_facts_items(10)"],
        2: ["sub_items(hi=10)", "mixed_facts_items(10)"],
        3: ["fact_family_items(10)", "count_on_difference_items()"],
        4: ["compose_ten_items()", "base_ten_items('regroup')", "count_by_items(10, 90)"],
        5: ["teen_items()", "base_ten_items('value')"],
        6: ["teen_add_sub_items()", "teen_items()"],
        7: ["make_ten_fill_items()", "missing_addend_items(10)"],
        8: ["make_ten_items()", "three_addend_items(20)"],
        9: ["add_items(hi=20, sums_to=20)", "make_ten_items()"],
        10: ["three_addend_items(20)"],
        11: ["story_items('start-unknown')", "missing_addend_items(20)"],
        12: ["subtract_teen_items()", "teen_add_sub_items()"],
        13: ["fact_family_items(20)", "count_on_difference_items()"],
        14: ["count_on_difference_items()", "subtract_teen_items()"],
        15: ["story_items('separate')", "make_ten_fill_items()", "missing_addend_items(20)"],
    },
    "u04_numbers99": {
        1: ["base_ten_items('build')", "count_by_items(10, 90)"],
        2: ["count_by_items(10, 99)", "count_by_items(10, 120)"],
        3: ["add_multiple_of_ten_items()", "count_by_items(10, 99)"],
        4: ["base_ten_items('value')", "write_numeral_items()"],
        5: ["base_ten_items('value')", "count_collection_items(99)"],
        6: ["digit_value_items()", "teen_items()"],
        7: ["add_multiple_of_ten_items()", "count_by_items(10, 99)"],
        8: ["compare_numbers_items(99)", "number_riddle_items()"],
        9: ["compare_numbers_items(99, symbol=True)", "compare_numbers_items(99)"],
        10: ["order_numbers_items(99, 3)", "order_numbers_items(99, 4)"],
        11: ["tens_ones_equiv_items()", "write_numeral_items()"],
        12: ["base_ten_items('regroup')", "tens_ones_equiv_items()", "compose_ten_items()"],
        13: ["write_numeral_items()", "count_collection_items(99)", "number_riddle_items()"],
    },
    "u05_within100": {
        1: ["add_two_digit_items(compose=False)", "add_items(hi=20)"],
        2: ["add_two_digit_items(compose=False)", "add_multiple_of_ten_items()"],
        3: ["add_two_digit_items(compose=False)", "equation_items()"],
        4: ["add_two_digit_items(compose=True)", "make_ten_items()"],
        5: ["add_two_digit_items(compose=True)", "base_ten_items('value')"],
        6: ["add_two_digit_items(compose=False)", "add_multiple_of_ten_items()"],
        7: ["add_two_digit_items(compose=True)"],
        8: ["add_two_digit_items(compose=True)", "digit_value_items()"],
        9: ["add_two_digit_items(compose=True)", "explain_strategy_items()"],
    },
    "u06_length": {
        1: ["length_compare_items()", "ruler_items()"],
        2: ["length_compare_items()", "order_length_items()"],
        3: ["order_length_items()", "length_compare_items()"],
        4: ["ruler_items()", "length_compare_items()"],
        5: ["ruler_items()", "length_word_items()"],
        6: ["count_120_items()", "count_collection_items(120)", "count_items(hi=120, by=10)"],
        7: ["ruler_items()", "length_compare_items()"],
        8: ["length_word_items()", "story_items('compare')"],
        9: ["story_items('start-unknown')", "story_items('change-unknown')"],
        10: ["story_items('compare')", "length_word_items()", "equation_items()"],
    },
    "u07_geometry_time": {
        1: ["shape_identify_items()", "shape_attr_items('sides')"],
        2: ["solid_items()", "compose_items()"],
        3: ["compose_items()", "shape_identify_items()"],
        4: ["solid_items()", "compose_items()"],
        5: ["partition_items()", "partition_items('circle')"],
        6: ["partition_items('circle')", "partition_items()"],
        7: ["equal_parts_items()", "partition_items()"],
        8: ["partition_items()", "equal_parts_items()"],
        9: ["clock_items(half=False)", "digital_items()"],
        10: ["clock_items(half=True)"],
        11: ["digital_items()", "clock_items(half=True)"],
        12: ["clock_items(half=True)", "digital_items()"],
    },
    "u08_together": {
        1: ["mixed_facts_items(20)", "add_items(hi=20, sums_to=20)", "sub_items(hi=20)"],
        2: ["mixed_facts_items(10)", "fact_family_items(10)"],
        3: ["fact_family_items(20)", "make_ten_items()", "count_on_difference_items()"],
        4: ["story_items('change-unknown')", "story_items('start-unknown')"],
        5: ["story_items('compare')", "compare_groups_items('fewer')"],
        6: ["story_items('partwhole')", "missing_addend_items(20)", "partition_numbers_items()"],
        7: ["equation_items()", "story_items('compare')"],
        8: ["count_collection_items(120)", "count_120_items()", "count_by_items(10, 120)"],
        9: ["write_numeral_items()", "count_collection_items(120)"],
        10: ["tens_ones_equiv_items()", "write_numeral_items()", "count_collection_items(120)"],
        11: ["number_riddle_items()", "tens_ones_equiv_items()"],
    },
}

DATA_SKILLS = {("u01_add_sub_data", i) for i in (4, 5, 6, 7, 8, 9)}


def build_module(name):
    idx = list(MAP).index(name)
    unit = UNITS[idx]
    domain = DOMAIN[name]
    lines = [f'"""{unit["name"]} — Grade 1 question families for {unit["id"]}."""',
             "from families import *", "", f"DOMAIN = {domain!r}", "", "SKILLS = {"]
    for i, skill_name in enumerate(unit["skills"], 1):
        fams = list(MAP[name][i])
        if ("u01_add_sub_data", i) in DATA_SKILLS:
            domain_i = "md"
        else:
            domain_i = domain
        if len(fams) < 3 and all("domain_facts_items" not in f for f in fams):
            fams.append(f"domain_facts_items({domain_i!r})")
        extra = f', "domain": {domain_i!r}' if domain_i != domain else ""
        lines.append(f'    {i}: {{"name": {skill_name!r}, "fams": [{", ".join(fams)}]{extra}}},')
    lines.append("}")
    return "\n".join(lines) + "\n"


def main():
    for name in MAP:
        path = os.path.join(HERE, "units", name + ".py")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(build_module(name))
        print("wrote", os.path.basename(path))


if __name__ == "__main__":
    main()
