"""Adding and Subtracting within 100 — Grade 2 question families for adding-subtracting-100."""
from fam2 import *

DOMAIN = 'oa'

SKILLS = {
    1: {"name": 'Represent tens and ones using base-ten blocks', "fams": [baseten_items('build'), baseten_items('value'), domain_facts_items('oa')]},
    2: {"name": 'Add two-digit numbers without regrouping', "fams": [add2_items(compose=False), domain_facts_items('oa')]},
    3: {"name": 'Subtract two-digit numbers without decomposing a ten', "fams": [sub2_items(regroup=False), domain_facts_items('oa')]},
    4: {"name": 'Use related addition to find an unknown addend', "fams": [fluency_items(), add2_items(compose=False), domain_facts_items('oa')]},
    5: {"name": 'Trade one ten for ten ones to subtract', "fams": [sub2_items(regroup=True), baseten_items('regroup'), domain_facts_items('oa')]},
    6: {"name": 'Use place-value drawings to model subtraction within 100', "fams": [sub2_items(regroup=True), baseten_items('value'), domain_facts_items('oa')]},
    7: {"name": 'Compare and explain different subtraction methods', "fams": [strategy_items(), domain_facts_items('oa')]},
    8: {"name": 'Use tape diagrams for addition and subtraction stories', "fams": [tape_compare_items(), two_step_items(), domain_facts_items('oa')]},
    9: {"name": 'Solve one-step addition and subtraction problems within 100', "fams": [add2_items(), sub2_items(), domain_facts_items('oa')]},
    10: {"name": 'Solve two-step word problems within 100', "fams": [two_step_items(), tape_compare_items(), domain_facts_items('oa')]},
    11: {"name": 'Solve problems with the unknown in different positions', "fams": [fluency_items(), two_step_items(), domain_facts_items('oa')]},
}
