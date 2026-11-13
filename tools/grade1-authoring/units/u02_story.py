"""Addition and Subtraction Story Problems — Grade 1 question families for addition-subtraction-story-problems."""
from families import *

DOMAIN = 'oa'

SKILLS = {
    1: {"name": 'Solve result-unknown stories within 10', "fams": [story_items('join'), story_items('partwhole'), domain_facts_items('oa')]},
    2: {"name": 'Solve change-unknown stories within 10', "fams": [story_items('change-unknown'), story_items('start-unknown'), domain_facts_items('oa')]},
    3: {"name": 'Interpret and write equations for story situations', "fams": [equation_items(), story_items('join'), domain_facts_items('oa')]},
    4: {"name": 'Explain what the equal sign means', "fams": [equal_sign_items(), true_false_equation_items(), domain_facts_items('md')], "domain": 'md'},
    5: {"name": 'Partition numbers within 10 into parts', "fams": [partition_numbers_items(), missing_addend_items(), domain_facts_items('md')], "domain": 'md'},
    6: {"name": 'Solve total-unknown and addend-unknown situations', "fams": [story_items('partwhole'), missing_addend_items(), domain_facts_items('md')], "domain": 'md'},
    7: {"name": 'Write equations with missing numbers in different positions', "fams": [make_ten_fill_items(), missing_addend_items(), partition_numbers_items()], "domain": 'md'},
    8: {"name": 'Model comparison stories with objects or drawings', "fams": [compare_groups_items('more'), compare_groups_items('fewer'), domain_facts_items('md')], "domain": 'md'},
    9: {"name": 'Find how many more or fewer in a pair of groups', "fams": [compare_groups_items('fewer'), story_items('compare'), domain_facts_items('md')], "domain": 'md'},
    10: {"name": 'Use addition to explain a subtraction difference', "fams": [count_on_difference_items(), story_items('compare'), domain_facts_items('oa')]},
    11: {"name": 'Solve mixed story types within 10', "fams": [story_items('join'), story_items('separate'), story_items('compare'), story_items('partwhole')]},
    12: {"name": 'Use a blank or box to represent an unknown', "fams": [make_ten_fill_items(), partition_numbers_items(), domain_facts_items('oa')]},
    13: {"name": 'Match several equations to the same story', "fams": [equation_items(), story_items('join'), domain_facts_items('oa')]},
    14: {"name": 'Write a story that matches a given equation', "fams": [story_match_items(), equation_items(), domain_facts_items('oa')]},
}
