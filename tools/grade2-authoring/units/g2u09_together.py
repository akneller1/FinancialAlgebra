"""Putting It All Together — Grade 2 question families for putting-it-all-together."""
from fam2 import *

DOMAIN = 'oa'

SKILLS = {
    1: {"name": 'Recall addition and subtraction facts within 20', "fams": [fluency_items(), domain_facts_items('oa')]},
    2: {"name": 'Use known facts and make-ten strategies', "fams": [strategy_items(), fluency_items(), domain_facts_items('oa')]},
    3: {"name": 'Measure lengths and represent measurement data', "fams": [lineplot_items('at'), measure_compare_items('metric'), domain_facts_items('oa')]},
    4: {"name": 'Represent hundreds, tens, and ones in multiple ways', "fams": [place3_items('expanded'), place3_items('value'), domain_facts_items('oa')]},
    5: {"name": 'Add and subtract within 1,000 using place-value methods', "fams": [add3_items(), sub3_items(), domain_facts_items('oa')]},
    6: {"name": 'Build fluency with two-digit addition and subtraction', "fams": [add2_items(), sub2_items(), domain_facts_items('oa')]},
    7: {"name": 'Represent one-step problems with equations and diagrams', "fams": [tape_compare_items(), two_step_items(), domain_facts_items('oa')]},
    8: {"name": 'Solve two-step story problems within 100', "fams": [two_step_items(), tape_compare_items(), domain_facts_items('oa')]},
    9: {"name": 'Write stories to match equations or diagrams', "fams": [tape_compare_items(), story_match_items(), domain_facts_items('oa')]},
}
