"""Putting It All Together — Grade 1 question families for putting-it-all-together."""
from families import *

DOMAIN = 'oa'

SKILLS = {
    1: {"name": 'Practice sums and differences within 20', "fams": [mixed_facts_items(20), add_items(hi=20, sums_to=20), sub_items(hi=20)]},
    2: {"name": 'Build reliable fact fluency within 10', "fams": [mixed_facts_items(10), fact_family_items(10), domain_facts_items('oa')]},
    3: {"name": 'Use related facts or make-ten strategies when needed', "fams": [fact_family_items(20), make_ten_items(), count_on_difference_items()]},
    4: {"name": 'Solve change-unknown stories', "fams": [story_items('change-unknown'), story_items('start-unknown'), domain_facts_items('md')], "domain": 'md'},
    5: {"name": 'Solve compare-difference-unknown stories', "fams": [story_items('compare'), compare_groups_items('fewer'), domain_facts_items('md')], "domain": 'md'},
    6: {"name": 'Solve part-whole unknown-addend stories', "fams": [story_items('partwhole'), missing_addend_items(20), partition_numbers_items()], "domain": 'md'},
    7: {"name": 'Use diagrams and equations for story situations', "fams": [equation_items(), story_items('compare'), domain_facts_items('md')], "domain": 'md'},
    8: {"name": 'Organize and count collections through 120', "fams": [count_collection_items(120), count_120_items(), count_by_items(10, 120)], "domain": 'md'},
    9: {"name": 'Write numerals to represent counted collections', "fams": [write_numeral_items(), count_collection_items(120), domain_facts_items('md')], "domain": 'md'},
    10: {"name": 'Represent numbers using different tens-and-ones groupings', "fams": [tens_ones_equiv_items(), write_numeral_items(), count_collection_items(120)]},
    11: {"name": 'Solve place-value number riddles', "fams": [number_riddle_items(), tens_ones_equiv_items(), domain_facts_items('oa')]},
}
