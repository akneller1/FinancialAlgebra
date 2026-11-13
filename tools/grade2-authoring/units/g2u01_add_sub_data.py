"""Adding, Subtracting, and Working with Data — Grade 2 question families for adding-subtracting-working-data."""
from fam2 import *

DOMAIN = 'oa'

SKILLS = {
    1: {"name": 'Use a make-ten strategy to add within 20', "fams": [fluency_items(), strategy_items(), domain_facts_items('oa')]},
    2: {"name": 'Subtract within 20 using related addition facts', "fams": [fluency_items(), fact_family_items(20), domain_facts_items('oa')]},
    3: {"name": 'Build fluency with mental addition within 50', "fams": [fluency_items(), add2_items(compose=False), domain_facts_items('oa')]},
    4: {"name": 'Organize categories into picture graphs', "fams": [graph_data_items('pictograph'), tally_data_items('count_one'), domain_facts_items('oa')]},
    5: {"name": 'Construct bar graphs using categorical data', "fams": [graph_data_items('bargraph'), tally_data_items('total'), domain_facts_items('oa')]},
    6: {"name": 'Interpret picture and bar graphs', "fams": [graph_data_items('pictograph'), graph_data_items('bargraph'), domain_facts_items('oa')]},
    7: {"name": 'Solve one- and two-step graph questions within 20', "fams": [graph_data_items('bargraph'), two_step_items(), domain_facts_items('oa')]},
    8: {"name": 'Interpret the parts and totals in tape diagrams', "fams": [tape_compare_items(), two_step_items(), domain_facts_items('oa')]},
    9: {"name": 'Find the difference between two quantities within 100', "fams": [sub2_items(regroup=False), tape_compare_items(), domain_facts_items('oa')]},
    10: {"name": 'Find an unknown larger or smaller quantity from a comparison', "fams": [tape_compare_items(), fluency_items(), domain_facts_items('oa')]},
    11: {"name": 'Match equations to comparison diagrams', "fams": [tape_compare_items(), story_match_items(), domain_facts_items('oa')]},
}
