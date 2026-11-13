"""Putting It All Together: explicit target-specific sources; no fallback."""
from aligned import source

SKILLS = {
    1: {"name": 'Practice sums and differences within 20', "fams": [source(7, 1)]},
    2: {"name": 'Build reliable fact fluency within 10', "fams": [source(7, 2)]},
    3: {"name": 'Use related facts or make-ten strategies when needed', "fams": [source(7, 3)]},
    4: {"name": 'Solve change-unknown stories', "fams": [source(7, 4)]},
    5: {"name": 'Solve compare-difference-unknown stories', "fams": [source(7, 5)]},
    6: {"name": 'Solve part-whole unknown-addend stories', "fams": [source(7, 6)]},
    7: {"name": 'Use diagrams and equations for story situations', "fams": [source(7, 7)]},
    8: {"name": 'Organize and count collections through 120', "fams": [source(7, 8)]},
    9: {"name": 'Write numerals to represent counted collections', "fams": [source(7, 9)]},
    10: {"name": 'Represent numbers using different tens-and-ones groupings', "fams": [source(7, 10)]},
    11: {"name": 'Solve place-value number riddles', "fams": [source(7, 11)]},
}
