"""Geometry and Time: explicit target-specific sources; no fallback."""
from aligned import source

SKILLS = {
    1: {"name": 'Describe defining attributes of common flat shapes', "fams": [source(6, 1)]},
    2: {"name": 'Identify and compare common solid shapes', "fams": [source(6, 2)]},
    3: {"name": 'Build composite two-dimensional shapes', "fams": [source(6, 3)]},
    4: {"name": 'Compose solid figures from smaller shapes', "fams": [source(6, 4)]},
    5: {"name": 'Partition rectangles into two and four equal pieces', "fams": [source(6, 5)]},
    6: {"name": 'Partition circles into halves and fourths', "fams": [source(6, 6)]},
    7: {"name": 'Explain why equal-sized parts matter', "fams": [source(6, 7)]},
    8: {"name": 'Describe halves and quarters using words', "fams": [source(6, 8)]},
    9: {"name": 'Read analog clocks to the hour', "fams": [source(6, 9)]},
    10: {"name": 'Read analog clocks to the half hour', "fams": [source(6, 10)]},
    11: {"name": 'Write matching digital times', "fams": [source(6, 11)]},
    12: {"name": 'Draw hour and minute hands for given times', "fams": [source(6, 12)]},
}
