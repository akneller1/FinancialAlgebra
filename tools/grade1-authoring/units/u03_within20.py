"""Adding and Subtracting within 20 — Grade 1 question families for adding-subtracting-within-20."""
from families import *

DOMAIN = 'oa'

SKILLS = {
    1: {"name": 'Practice addition facts with totals to 10', "fams": [add_items(hi=10, sums_to=10), mixed_facts_items(10), domain_facts_items('oa')]},
    2: {"name": 'Practice subtraction facts within 10', "fams": [sub_items(hi=10), mixed_facts_items(10), domain_facts_items('oa')]},
    3: {"name": 'Explain related addition and subtraction facts', "fams": [fact_family_items(10), count_on_difference_items(), domain_facts_items('oa')]},
    4: {"name": 'Compose 10 ones into one ten', "fams": [compose_ten_items(), base_ten_items('regroup'), count_by_items(10, 90)], "domain": 'md'},
    5: {"name": 'Express teen numbers as ten and extra ones', "fams": [teen_items(), base_ten_items('value'), domain_facts_items('md')], "domain": 'md'},
    6: {"name": 'Add and subtract ones to or from teen numbers without regrouping', "fams": [teen_add_sub_items(), teen_items(), domain_facts_items('md')], "domain": 'md'},
    7: {"name": 'Fill unknowns in equations involving 10', "fams": [make_ten_fill_items(), missing_addend_items(10), domain_facts_items('md')], "domain": 'md'},
    8: {"name": 'Use make-ten strategies for sums within 20', "fams": [make_ten_items(), three_addend_items(20), domain_facts_items('md')], "domain": 'md'},
    9: {"name": 'Add two one-digit numbers whose sum exceeds 10', "fams": [add_items(hi=20, sums_to=20), make_ten_items(), domain_facts_items('md')], "domain": 'md'},
    10: {"name": 'Combine three addends within 20', "fams": [three_addend_items(20), domain_facts_items('oa')]},
    11: {"name": 'Solve start-unknown addition word problems', "fams": [story_items('start-unknown'), missing_addend_items(20), domain_facts_items('oa')]},
    12: {"name": 'Subtract from teen numbers with ten-frames', "fams": [subtract_teen_items(), teen_add_sub_items(), domain_facts_items('oa')]},
    13: {"name": 'Use related addition facts to subtract', "fams": [fact_family_items(20), count_on_difference_items(), domain_facts_items('oa')]},
    14: {"name": 'Count on and make a ten to find differences', "fams": [count_on_difference_items(), subtract_teen_items(), domain_facts_items('oa')]},
    15: {"name": 'Solve subtraction stories and missing-addend equations', "fams": [story_items('separate'), make_ten_fill_items(), missing_addend_items(20)]},
}
