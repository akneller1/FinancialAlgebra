"""Adding, Subtracting, and Working with Data — Grade 1 question families for adding-subtracting-working-data."""
from families import *

DOMAIN = 'oa'

SKILLS = {
    1: {"name": 'Count on or back to add or subtract 1 and 2', "fams": [add1_items(), add1_items(back=True), one_more_less_items(12), count_items(hi=20)]},
    2: {"name": 'Use ten-frames to model sums through 10', "fams": [add_items(hi=10, sums_to=10, diagram='tenframe'), missing_addend_items(10), make_ten_fill_items()]},
    3: {"name": 'Build fluency with addition and subtraction facts through 10', "fams": [add_items(hi=10, sums_to=10), sub_items(hi=10), mixed_facts_items(10), fact_family_items(10)]},
    4: {"name": 'Sort collections into chosen categories', "fams": [sort_items(), compare_groups_items('which'), domain_facts_items('md')], "domain": 'md'},
    5: {"name": 'Collect survey responses and tally category counts', "fams": [tally_items('count_one'), tally_items('total'), domain_facts_items('md')], "domain": 'md'},
    6: {"name": 'Represent categorical data with objects, marks, or numerals', "fams": [tally_items('count_one'), graph_items('pictograph'), domain_facts_items('md')], "domain": 'md'},
    7: {"name": 'Read tally marks and organized counts', "fams": [tally_items('read'), tally_items('count_one'), domain_facts_items('md')], "domain": 'md'},
    8: {"name": 'Find how many objects belong to each category', "fams": [graph_items('pictograph'), tally_items('total'), domain_facts_items('md')], "domain": 'md'},
    9: {"name": 'Compare category totals and answer questions about the data', "fams": [compare_groups_items('more'), compare_groups_items('fewer'), graph_items('bargraph')], "domain": 'md'},
}
