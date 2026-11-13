"""Adding Within 100: explicit target-specific sources; no fallback."""
from aligned import source

SKILLS = {
    1: {"name": 'Add a one-digit number to a two-digit number without regrouping', "fams": [source(4, 1)]},
    2: {"name": 'Add two two-digit numbers without composing a ten', "fams": [source(4, 2)]},
    3: {"name": 'Record place-value addition methods as equations', "fams": [source(4, 3)]},
    4: {"name": 'Compose a ten to add a one-digit and a two-digit number', "fams": [source(4, 4)]},
    5: {"name": 'Use base-ten drawings to show regrouping', "fams": [source(4, 5)]},
    6: {"name": 'Record equivalent addition methods', "fams": [source(4, 6)]},
    7: {"name": 'Add two two-digit numbers by composing a ten', "fams": [source(4, 7)]},
    8: {"name": 'Connect visual models to written place-value steps', "fams": [source(4, 8)]},
    9: {"name": 'Explain why different regrouping methods give the same sum', "fams": [source(4, 9)]},
}
