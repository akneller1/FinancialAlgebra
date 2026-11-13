"""Numbers to 1,000 — Grade 2 question families for numbers-to-1000."""
from fam2 import *

DOMAIN = 'nbt'

SKILLS = {
    1: {"name": 'Compose a hundred from ten tens', "fams": [baseten_items('regroup'), place3_items('value')]},
    2: {"name": 'Represent numbers as hundreds, tens, and ones', "fams": [place3_items('value'), baseten_items('build')]},
    3: {"name": 'Write three-digit numbers in numerals and expanded form', "fams": [place3_items('expanded'), place3_items('value')]},
    4: {"name": 'Regroup among hundreds, tens, and ones', "fams": [place3_items('value'), baseten_items('regroup')]},
    5: {"name": 'Count by tens and hundreds within 1,000', "fams": [skip_count_items(limit=1000), skip_count_items(100)]},
    6: {"name": 'Place three-digit numbers on number lines', "fams": [numberline_items('locate'), numberline_items('jump')]},
    7: {"name": 'Compare three-digit numbers using place value', "fams": [compare3_items(symbol=True), compare3_items()]},
    8: {"name": 'Order three-digit numbers from least to greatest', "fams": [order3_items(), order3_items(4), order_choice_items()]},
}
