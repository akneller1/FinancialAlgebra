"""Adding, Subtracting, and Working with Data — Grade 2 question families for adding-subtracting-working-data."""
from fam2 import *

DOMAIN = 'oa'

SKILLS = {
    1: {"name": 'Use a make-ten strategy to add within 20', "fams": [make_ten_items(), make_ten_fill_items(), domain_facts_items('oa')]},
    2: {"name": 'Subtract within 20 using related addition facts', "fams": [fact_family_items(20), sub_items(hi=20), domain_facts_items('oa')]},
    3: {"name": 'Build fluency with mental addition within 50', "fams": [add_items(hi=20, sums_to=20), doubles_items(), add2_items(compose=False)]},
    4: {"name": 'Organize categories into picture graphs', "fams": [sort_items(), graph_items('pictograph'), domain_facts_items('oa')]},
    5: {"name": 'Construct bar graphs using categorical data', "fams": [graph_items('bargraph'), tally_items('total'), domain_facts_items('oa')]},
    6: {"name": 'Interpret picture and bar graphs', "fams": [graph_items('pictograph'), graph_items('bargraph'), domain_facts_items('oa')]},
    7: {"name": 'Solve one- and two-step graph questions within 20', "fams": [graph_items('bargraph'), tally_items('total'), missing_addend_items(20)]},
    8: {"name": 'Interpret the parts and totals in tape diagrams', "fams": [tape_compare_items(), story_items('partwhole'), domain_facts_items('oa')]},
    9: {"name": 'Find the difference between two quantities within 100', "fams": [sub2_items(regroup=False), story_items('compare'), domain_facts_items('oa')]},
    10: {"name": 'Find an unknown larger or smaller quantity from a comparison', "fams": [story_items('compare'), missing_addend_items(20), domain_facts_items('oa')]},
    11: {"name": 'Match equations to comparison diagrams', "fams": [story_match_items(), equation_items(), domain_facts_items('oa')]},
}
