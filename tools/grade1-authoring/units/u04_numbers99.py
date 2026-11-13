"""Numbers to 99: explicit target-specific sources; no fallback."""
from aligned import source

SKILLS = {
    1: {"name": 'Build groups of ten from loose ones', "fams": [source(3, 1)]},
    2: {"name": 'Count by tens through two-digit numbers', "fams": [source(3, 2)]},
    3: {"name": 'Add and subtract complete tens', "fams": [source(3, 3)]},
    4: {"name": 'Represent numbers to 99 in tens and ones', "fams": [source(3, 4)]},
    5: {"name": 'Draw base-ten models for two-digit numbers', "fams": [source(3, 5)]},
    6: {"name": 'Explain the value of tens and ones digits', "fams": [source(3, 6)]},
    7: {"name": 'Add and subtract multiples of ten', "fams": [source(3, 7)]},
    8: {"name": 'Compare two-digit numbers by place value', "fams": [source(3, 8)]},
    9: {"name": 'Use less-than, greater-than, and equal signs', "fams": [source(3, 9)]},
    10: {"name": 'Order two-digit numbers using models and numeral comparisons', "fams": [source(3, 10)]},
    11: {"name": 'Show equivalent tens-and-ones decompositions', "fams": [source(3, 11)]},
    12: {"name": 'Regroup a ten as ten ones', "fams": [source(3, 12)]},
    13: {"name": 'Recognize different representations of the same two-digit number', "fams": [source(3, 13)]},
}
