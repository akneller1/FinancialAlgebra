"""Geometry and Time — Grade 1 question families for geometry-time."""
from families import *

DOMAIN = 'g'

SKILLS = {
    1: {"name": 'Describe defining attributes of common flat shapes', "fams": [shape_identify_items(), shape_attr_items('sides'), domain_facts_items('g')]},
    2: {"name": 'Identify and compare common solid shapes', "fams": [solid_items(), compose_items(), domain_facts_items('g')]},
    3: {"name": 'Build composite two-dimensional shapes', "fams": [compose_items(), shape_identify_items(), domain_facts_items('g')]},
    4: {"name": 'Compose solid figures from smaller shapes', "fams": [solid_items(), compose_items(), domain_facts_items('md')], "domain": 'md'},
    5: {"name": 'Partition rectangles into two and four equal pieces', "fams": [partition_items(), partition_items('circle'), domain_facts_items('md')], "domain": 'md'},
    6: {"name": 'Partition circles into halves and fourths', "fams": [partition_items('circle'), partition_items(), domain_facts_items('md')], "domain": 'md'},
    7: {"name": 'Explain why equal-sized parts matter', "fams": [equal_parts_items(), partition_items(), domain_facts_items('md')], "domain": 'md'},
    8: {"name": 'Describe halves and quarters using words', "fams": [partition_items(), equal_parts_items(), domain_facts_items('md')], "domain": 'md'},
    9: {"name": 'Read analog clocks to the hour', "fams": [clock_items(half=False), digital_items(), domain_facts_items('md')], "domain": 'md'},
    10: {"name": 'Read analog clocks to the half hour', "fams": [clock_items(half=True), domain_facts_items('g')]},
    11: {"name": 'Write matching digital times', "fams": [digital_items(), clock_items(half=True), domain_facts_items('g')]},
    12: {"name": 'Draw hour and minute hands for given times', "fams": [clock_items(half=True), digital_items(), domain_facts_items('g')]},
}
