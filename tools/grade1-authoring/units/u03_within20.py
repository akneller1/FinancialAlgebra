"""Adding and Subtracting within 20: explicit target-specific sources; no fallback."""
from aligned import source

SKILLS = {
    1: {"name": 'Practice addition facts with totals to 10', "fams": [source(2, 1)]},
    2: {"name": 'Practice subtraction facts within 10', "fams": [source(2, 2)]},
    3: {"name": 'Explain related addition and subtraction facts', "fams": [source(2, 3)]},
    4: {"name": 'Compose 10 ones into one ten', "fams": [source(2, 4)]},
    5: {"name": 'Express teen numbers as ten and extra ones', "fams": [source(2, 5)]},
    6: {"name": 'Add and subtract ones to or from teen numbers without regrouping', "fams": [source(2, 6)]},
    7: {"name": 'Fill unknowns in equations involving 10', "fams": [source(2, 7)]},
    8: {"name": 'Use make-ten strategies for sums within 20', "fams": [source(2, 8)]},
    9: {"name": 'Add two one-digit numbers whose sum exceeds 10', "fams": [source(2, 9)]},
    10: {"name": 'Combine three addends within 20', "fams": [source(2, 10)]},
    11: {"name": 'Solve start-unknown addition word problems', "fams": [source(2, 11)]},
    12: {"name": 'Subtract from teen numbers with ten-frames', "fams": [source(2, 12)]},
    13: {"name": 'Use related addition facts to subtract', "fams": [source(2, 13)]},
    14: {"name": 'Count on and make a ten to find differences', "fams": [source(2, 14)]},
    15: {"name": 'Solve subtraction stories and missing-addend equations', "fams": [source(2, 15)]},
}
