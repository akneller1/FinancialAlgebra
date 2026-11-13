"""Equal Groups — Grade 2 question families for equal-groups."""
from fam2 import *

DOMAIN = 'oa'

SKILLS = {
    1: {"name": 'Sort numbers up to 20 as odd or even', "fams": [even_odd_items(), domain_facts_items('oa')]},
    2: {"name": 'Pair objects to recognize even quantities', "fams": [even_odd_items(), array_items('total'), domain_facts_items('oa')]},
    3: {"name": 'Write even numbers as sums of equal addends', "fams": [doubles_items(), even_odd_items(), domain_facts_items('oa')]},
    4: {"name": 'Identify rows and columns in arrays', "fams": [array_items('rows'), array_items('total'), domain_facts_items('oa')]},
    5: {"name": 'Write repeated-addition equations for arrays up to 5 by 5', "fams": [repeated_add_items(), array_items('total'), domain_facts_items('oa')]},
    6: {"name": 'Partition rectangles into equal-size square arrays', "fams": [array_items('total'), repeated_add_items(), domain_facts_items('oa')]},
    7: {"name": 'Count total squares by rows or columns', "fams": [array_items('total'), array_items('rows'), domain_facts_items('oa')]},
}
