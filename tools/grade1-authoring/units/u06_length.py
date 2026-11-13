"""Length Measurements Within 120 Units — Grade 1 question families for length-measurement-120."""
from families import *

DOMAIN = 'md'

SKILLS = {
    1: {"name": 'Compare the lengths of objects directly', "fams": [length_compare_items(), ruler_items(), domain_facts_items('md')]},
    2: {"name": 'Use a third object to compare lengths indirectly', "fams": [length_compare_items(), order_length_items(), domain_facts_items('md')]},
    3: {"name": 'Order objects from shortest to longest', "fams": [order_length_items(), length_compare_items(), domain_facts_items('md')]},
    4: {"name": 'Line up equal-size measuring units without gaps', "fams": [ruler_items(), length_compare_items(), domain_facts_items('md')]},
    5: {"name": 'Count repeated length units to measure objects', "fams": [ruler_items(), length_word_items(), domain_facts_items('md')]},
    6: {"name": 'Count and write quantities up to 120', "fams": [count_120_items(), count_collection_items(120), count_items(hi=120, by=10)]},
    7: {"name": 'Compare measurements made using the same unit', "fams": [ruler_items(), length_compare_items(), domain_facts_items('md')]},
    8: {"name": 'Solve comparison word problems involving length', "fams": [length_word_items(), story_items('compare'), domain_facts_items('md')]},
    9: {"name": 'Find unknown starts or changes in subtraction stories', "fams": [story_items('start-unknown'), story_items('change-unknown'), domain_facts_items('md')]},
    10: {"name": 'Model story problems with drawings and equations', "fams": [story_items('compare'), length_word_items(), equation_items()]},
}
