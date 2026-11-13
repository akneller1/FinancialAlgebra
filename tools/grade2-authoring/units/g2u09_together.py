"""Putting It All Together — Grade 2 question families for putting-it-all-together."""
from fam2 import *

DOMAIN = 'oa'

SKILLS = {
    1: {"name": 'Recall addition and subtraction facts within 20', "fams": [fluency_items(limit=20), doubles_items()]},
    2: {"name": 'Use known facts and make-ten strategies', "fams": [strategy_items(), fluency_items()]},
    3: {"name": 'Measure lengths and represent measurement data', "fams": [lineplot_items('at'), measure_compare_items('metric', 100)]},
    4: {"name": 'Represent hundreds, tens, and ones in multiple ways', "fams": [place3_items('expanded'), place3_items('value')]},
    5: {"name": 'Add and subtract within 1,000 using place-value methods', "fams": [add3_items(), sub3_items()]},
    6: {"name": 'Build fluency with two-digit addition and subtraction', "fams": [add2_items(), sub2_items()]},
    7: {"name": 'Represent one-step problems with equations and diagrams', "fams": [tape_compare_items(100), two_step_items(100)]},
    8: {"name": 'Solve two-step story problems within 100', "fams": [two_step_items(100), tape_compare_items(100)]},
    9: {"name": 'Write stories to match equations or diagrams', "fams": [tape_compare_items(), story_match_items()]},
}
