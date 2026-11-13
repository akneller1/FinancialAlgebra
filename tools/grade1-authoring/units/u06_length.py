"""Length Measurements Within 120 Units: explicit target-specific sources; no fallback."""
from aligned import source

SKILLS = {
    1: {"name": 'Compare the lengths of objects directly', "fams": [source(5, 1)]},
    2: {"name": 'Use a third object to compare lengths indirectly', "fams": [source(5, 2)]},
    3: {"name": 'Order objects from shortest to longest', "fams": [source(5, 3)]},
    4: {"name": 'Line up equal-size measuring units without gaps', "fams": [source(5, 4)]},
    5: {"name": 'Count repeated length units to measure objects', "fams": [source(5, 5)]},
    6: {"name": 'Count and write quantities up to 120', "fams": [source(5, 6)]},
    7: {"name": 'Compare measurements made using the same unit', "fams": [source(5, 7)]},
    8: {"name": 'Solve comparison word problems involving length', "fams": [source(5, 8)]},
    9: {"name": 'Find unknown starts or changes in subtraction stories', "fams": [source(5, 9)]},
    10: {"name": 'Model story problems with drawings and equations', "fams": [source(5, 10)]},
}
