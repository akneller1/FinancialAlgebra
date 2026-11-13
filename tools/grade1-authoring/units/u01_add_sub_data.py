"""Adding, Subtracting, and Working with Data: explicit target-specific sources; no fallback."""
from aligned import source

SKILLS = {
    1: {"name": 'Count on or back to add or subtract 1 and 2', "fams": [source(0, 1)]},
    2: {"name": 'Use ten-frames to model sums through 10', "fams": [source(0, 2)]},
    3: {"name": 'Build fluency with addition and subtraction facts through 10', "fams": [source(0, 3)]},
    4: {"name": 'Sort collections into chosen categories', "fams": [source(0, 4)]},
    5: {"name": 'Collect survey responses and tally category counts', "fams": [source(0, 5)]},
    6: {"name": 'Represent categorical data with objects, marks, or numerals', "fams": [source(0, 6)]},
    7: {"name": 'Read tally marks and organized counts', "fams": [source(0, 7)]},
    8: {"name": 'Find how many objects belong to each category', "fams": [source(0, 8)]},
    9: {"name": 'Compare category totals and answer questions about the data', "fams": [source(0, 9)]},
}
