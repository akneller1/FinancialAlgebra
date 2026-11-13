"""Addition and Subtraction on the Number Line — Grade 2 question families for number-line-addition-subtraction."""
from fam2 import *

DOMAIN = 'nbt'

SKILLS = {
    1: {"name": 'Interpret equal intervals on a number line', "fams": [numberline_items('locate'), count_by_items(10, 100), domain_facts_items('nbt')]},
    2: {"name": 'Represent whole numbers within 100 as distances from zero', "fams": [numberline_items('jump'), count_items(hi=100), domain_facts_items('nbt')]},
    3: {"name": 'Locate and estimate unlabeled numbers on a number line', "fams": [numberline_items('locate'), round10_items(), domain_facts_items('nbt')]},
    4: {"name": 'Show addition as jumps along a number line', "fams": [numberline_items('jump'), add_items(hi=60, sums_to=100), domain_facts_items('nbt')]},
    5: {"name": 'Show subtraction as jumps or distances', "fams": [sub2_items(regroup=False), numberline_items('jump'), domain_facts_items('nbt')]},
    6: {"name": 'Use number lines to represent story problems within 100', "fams": [story_items('join'), numberline_items('jump'), domain_facts_items('nbt')]},
    7: {"name": 'Choose efficient jumps of tens and ones', "fams": [add2_items(), skip_count_items(10), domain_facts_items('nbt')]},
}
