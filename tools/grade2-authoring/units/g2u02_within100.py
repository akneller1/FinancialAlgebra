"""Adding and Subtracting within 100 — Grade 2 question families for adding-subtracting-100."""
from fam2 import *

DOMAIN = 'oa'

SKILLS = {
    1: {"name": 'Represent tens and ones using base-ten blocks', "fams": [baseten_items('build'), baseten_items('value')]},
    2: {"name": 'Add two-digit numbers without regrouping', "fams": [add2_items(compose=False), fluency_items()]},
    3: {"name": 'Subtract two-digit numbers without decomposing a ten', "fams": [sub2_items(regroup=False), fluency_items()]},
    4: {"name": 'Use related addition to find an unknown addend', "fams": [missing_addend_items(), fact_family_items(100)]},
    5: {"name": 'Trade one ten for ten ones to subtract', "fams": [sub2_items(regroup=True), baseten_items('regroup')]},
    6: {"name": 'Use place-value drawings to model subtraction within 100', "fams": [sub2_items(regroup=True), baseten_items('value', limit=100)]},
    7: {"name": 'Compare and explain different subtraction methods', "fams": [strategy_items(), sub2_items(regroup=True), baseten_items('regroup')]},
    8: {"name": 'Use tape diagrams for addition and subtraction stories', "fams": [tape_compare_items(100), two_step_items(100)]},
    9: {"name": 'Solve one-step addition and subtraction problems within 100', "fams": [add2_items(), sub2_items()]},
    10: {"name": 'Solve two-step word problems within 100', "fams": [two_step_items(100), tape_compare_items(100)]},
    11: {"name": 'Solve problems with the unknown in different positions', "fams": [add2_items(), two_step_items(100)]},
}
