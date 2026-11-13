"""Adding and Subtracting within 1,000 — Grade 2 question families for adding-subtracting-1000."""
from fam2 import *

DOMAIN = 'nbt'

SKILLS = {
    1: {"name": 'Add three-digit numbers without composing units', "fams": [add3_items(rename=False), domain_facts_items('nbt')]},
    2: {"name": 'Subtract three-digit numbers without decomposing units', "fams": [sub3_items(), domain_facts_items('nbt')]},
    3: {"name": 'Represent sums and differences with base-ten diagrams or number lines', "fams": [add3_items(), numberline_items('jump'), domain_facts_items('nbt')]},
    4: {"name": 'Compose a new ten when adding three-digit numbers', "fams": [add3_items(rename=True), domain_facts_items('nbt')]},
    5: {"name": 'Compose a new hundred when adding three-digit numbers', "fams": [add3_items(), place3_items('hundred_more'), domain_facts_items('nbt')]},
    6: {"name": 'Explain different place-value addition methods', "fams": [strategy_items(), domain_facts_items('nbt')]},
    7: {"name": 'Decompose a hundred into tens when subtracting', "fams": [sub3_items(), baseten_items('regroup'), domain_facts_items('nbt')]},
    8: {"name": 'Decompose a ten into ones when subtracting', "fams": [sub3_items(), sub2_items(regroup=True), domain_facts_items('nbt')]},
    9: {"name": 'Model subtraction with decomposing multiple units', "fams": [sub3_items(), baseten_items('value'), domain_facts_items('nbt')]},
    10: {"name": 'Choose and explain efficient subtraction strategies', "fams": [sub3_items(), strategy_items(), domain_facts_items('nbt')]},
}
