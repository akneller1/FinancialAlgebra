"""Numbers to 1,000 — Grade 2 question families for numbers-to-1000."""
from fam2 import *

DOMAIN = 'nbt'

SKILLS = {
    1: {"name": 'Compose a hundred from ten tens', "fams": [baseten_items('regroup'), place3_items('value'), domain_facts_items('nbt')]},
    2: {"name": 'Represent numbers as hundreds, tens, and ones', "fams": [place3_items('value'), baseten_items('build'), domain_facts_items('nbt')]},
    3: {"name": 'Write three-digit numbers in numerals and expanded form', "fams": [place3_items('expanded'), place3_items('hundred_more'), domain_facts_items('nbt')]},
    4: {"name": 'Regroup among hundreds, tens, and ones', "fams": [place3_items('value'), baseten_items('regroup'), domain_facts_items('nbt')]},
    5: {"name": 'Count by tens and hundreds within 1,000', "fams": [skip_count_items(), skip_count_items(100), domain_facts_items('nbt')]},
    6: {"name": 'Place three-digit numbers on number lines', "fams": [numberline_items('locate'), skip_count_items(), domain_facts_items('nbt')]},
    7: {"name": 'Compare three-digit numbers using place value', "fams": [compare3_items(symbol=True), compare3_items(), domain_facts_items('nbt')]},
    8: {"name": 'Order three-digit numbers from least to greatest', "fams": [order3_items(), order3_items(4), domain_facts_items('nbt')]},
}
