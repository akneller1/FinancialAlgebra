"""Geometry, Time, and Money — Grade 2 question families for geometry-time-money."""
from fam2 import *

DOMAIN = 'g'

SKILLS = {
    1: {"name": 'Identify and draw triangles, quadrilaterals, pentagons, and hexagons', "fams": [polygon_items('name'), shape_items('name'), domain_facts_items('g')]},
    2: {"name": 'Classify shapes by sides, corners, and other attributes', "fams": [polygon_items('sides'), polygon_items('corners'), domain_facts_items('g')]},
    3: {"name": 'Describe cubes and faces of solid shapes', "fams": [solid_items(), polygon_items('name'), domain_facts_items('g')]},
    4: {"name": 'Partition rectangles and circles into two equal parts', "fams": [thirds_items('name'), thirds_items('count'), domain_facts_items('g')]},
    5: {"name": 'Partition rectangles and circles into thirds and fourths', "fams": [thirds_items('count'), thirds_items('name'), domain_facts_items('g')]},
    6: {"name": 'Describe shares using fraction words', "fams": [thirds_items('name'), thirds_items('shaded'), domain_facts_items('g')]},
    7: {"name": 'Recognize that equal shares may have different shapes', "fams": [thirds_items('shaded'), thirds_items('count'), domain_facts_items('g')]},
    8: {"name": 'Read analog clocks to five-minute intervals', "fams": [time_items(), domain_facts_items('g')]},
    9: {"name": 'Write time digitally and on analog clock faces', "fams": [time_items(), time_word_items(), domain_facts_items('g')]},
    10: {"name": 'Use a.m. and p.m. in daily situations', "fams": [time_word_items(), time_items(), domain_facts_items('g')]},
    11: {"name": 'Relate half past and quarter past to clock partitions', "fams": [time_items(), domain_facts_items('g')]},
    12: {"name": 'Identify quarters, dimes, nickels, and pennies', "fams": [money_items('count'), money_items('word'), domain_facts_items('g')]},
    13: {"name": 'Count combinations of coins and bills', "fams": [money_items('count'), money_items('word'), domain_facts_items('g')]},
    14: {"name": 'Relate one dollar to 100 cents', "fams": [money_items('word'), money_items('count'), domain_facts_items('g')]},
    15: {"name": 'Solve money word problems within 100 without requiring decimal notation', "fams": [money_items('word'), two_step_items(), domain_facts_items('g')]},
}
