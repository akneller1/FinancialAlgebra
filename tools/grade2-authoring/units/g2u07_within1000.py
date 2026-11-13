"""Adding and Subtracting within 1,000 — Grade 2 question families for adding-subtracting-1000."""
from fam2 import *

DOMAIN = 'nbt'

SKILLS = {
    1: {"name": 'Add three-digit numbers without composing units', "fams": [add3_items(rename=False, styles=(0, 1)), add3_items(rename=False, styles=(2,))]},
    2: {"name": 'Subtract three-digit numbers without decomposing units', "fams": [sub3_items(decompose=False, styles=(0, 1)), sub3_items(decompose=False, styles=(2,))]},
    3: {"name": 'Represent sums and differences with base-ten diagrams or number lines', "fams": [add3_items(), numberline_items('jump')]},
    4: {"name": 'Compose a new ten when adding three-digit numbers', "fams": [add3_items(rename=True, styles=(0, 1)), two_digit_items('add', compose=True, styles=(2,))]},
    5: {"name": 'Compose a new hundred when adding three-digit numbers', "fams": [add3_items(rename=True, styles=(0, 1)), two_digit_items('add', compose=True, styles=(2,))]},
    6: {"name": 'Explain different place-value addition methods', "fams": [strategy_items(), add3_items(rename=True), place3_items('value')]},
    7: {"name": 'Decompose a hundred into tens when subtracting', "fams": [sub3_items(decompose=True, styles=(0, 1)), two_digit_items('sub', compose=True, styles=(2,))]},
    8: {"name": 'Decompose a ten into ones when subtracting', "fams": [sub3_items(decompose=True, styles=(0, 1)), two_digit_items('sub', compose=True, styles=(2,))]},
    9: {"name": 'Model subtraction with decomposing multiple units', "fams": [sub3_items(decompose=True, styles=(0, 1)), sub3_items(decompose=True, styles=(2,))]},
    10: {"name": 'Choose and explain efficient subtraction strategies', "fams": [sub3_items(decompose=True), strategy_items()]},
}
