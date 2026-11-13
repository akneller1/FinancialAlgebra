"""Addition and Subtraction on the Number Line — Grade 2 question families for number-line-addition-subtraction."""
from fam2 import *

DOMAIN = 'nbt'

SKILLS = {
    1: {"name": 'Interpret equal intervals on a number line', "fams": [numberline_items('locate'), skip_count_items()]},
    2: {"name": 'Represent whole numbers within 100 as distances from zero', "fams": [numberline_items('jump', limit=100), numberline_items('locate', limit=100)]},
    3: {"name": 'Locate and estimate unlabeled numbers on a number line', "fams": [numberline_items('locate'), round_items()]},
    4: {"name": 'Show addition as jumps along a number line', "fams": [numberline_items('jump'), add2_items()]},
    5: {"name": 'Show subtraction as jumps or distances', "fams": [sub2_items(regroup=False), numberline_items('jump')]},
    6: {"name": 'Use number lines to represent story problems within 100', "fams": [two_step_items(limit=100), numberline_items('jump', limit=100)]},
    7: {"name": 'Choose efficient jumps of tens and ones', "fams": [add2_items(), skip_count_items()]},
}
