"""Numbers to 99 — Grade 1 question families for numbers-to-99."""
from families import *

DOMAIN = 'nbt'

SKILLS = {
    1: {"name": 'Build groups of ten from loose ones', "fams": [base_ten_items('build'), count_by_items(10, 90), domain_facts_items('nbt')]},
    2: {"name": 'Count by tens through two-digit numbers', "fams": [count_by_items(10, 99), count_by_items(10, 120), domain_facts_items('nbt')]},
    3: {"name": 'Add and subtract complete tens', "fams": [add_multiple_of_ten_items(), count_by_items(10, 99), domain_facts_items('nbt')]},
    4: {"name": 'Represent numbers to 99 in tens and ones', "fams": [base_ten_items('value'), write_numeral_items(), domain_facts_items('md')], "domain": 'md'},
    5: {"name": 'Draw base-ten models for two-digit numbers', "fams": [base_ten_items('value'), count_collection_items(99), domain_facts_items('md')], "domain": 'md'},
    6: {"name": 'Explain the value of tens and ones digits', "fams": [digit_value_items(), teen_items(), domain_facts_items('md')], "domain": 'md'},
    7: {"name": 'Add and subtract multiples of ten', "fams": [add_multiple_of_ten_items(), count_by_items(10, 99), domain_facts_items('md')], "domain": 'md'},
    8: {"name": 'Compare two-digit numbers by place value', "fams": [compare_numbers_items(99), number_riddle_items(), domain_facts_items('md')], "domain": 'md'},
    9: {"name": 'Use less-than, greater-than, and equal signs', "fams": [compare_numbers_items(99, symbol=True), compare_numbers_items(99), domain_facts_items('md')], "domain": 'md'},
    10: {"name": 'Order two-digit numbers using models and numeral comparisons', "fams": [order_numbers_items(99, 3), order_numbers_items(99, 4), domain_facts_items('nbt')]},
    11: {"name": 'Show equivalent tens-and-ones decompositions', "fams": [tens_ones_equiv_items(), write_numeral_items(), domain_facts_items('nbt')]},
    12: {"name": 'Regroup a ten as ten ones', "fams": [base_ten_items('regroup'), tens_ones_equiv_items(), compose_ten_items()]},
    13: {"name": 'Recognize different representations of the same two-digit number', "fams": [write_numeral_items(), count_collection_items(99), number_riddle_items()]},
}
