"""Adding Within 100 — Grade 1 question families for adding-within-100."""
from families import *

DOMAIN = 'nbt'

SKILLS = {
    1: {"name": 'Add a one-digit number to a two-digit number without regrouping', "fams": [add_two_digit_items(compose=False), add_items(hi=20), domain_facts_items('nbt')]},
    2: {"name": 'Add two two-digit numbers without composing a ten', "fams": [add_two_digit_items(compose=False), add_multiple_of_ten_items(), domain_facts_items('nbt')]},
    3: {"name": 'Record place-value addition methods as equations', "fams": [add_two_digit_items(compose=False), equation_items(), domain_facts_items('nbt')]},
    4: {"name": 'Compose a ten to add a one-digit and a two-digit number', "fams": [add_two_digit_items(compose=True), make_ten_items(), domain_facts_items('md')], "domain": 'md'},
    5: {"name": 'Use base-ten drawings to show regrouping', "fams": [add_two_digit_items(compose=True), base_ten_items('value'), domain_facts_items('md')], "domain": 'md'},
    6: {"name": 'Record equivalent addition methods', "fams": [add_two_digit_items(compose=False), add_multiple_of_ten_items(), domain_facts_items('md')], "domain": 'md'},
    7: {"name": 'Add two two-digit numbers by composing a ten', "fams": [add_two_digit_items(compose=True), domain_facts_items('md')], "domain": 'md'},
    8: {"name": 'Connect visual models to written place-value steps', "fams": [add_two_digit_items(compose=True), digit_value_items(), domain_facts_items('md')], "domain": 'md'},
    9: {"name": 'Explain why different regrouping methods give the same sum', "fams": [add_two_digit_items(compose=True), explain_strategy_items(), domain_facts_items('md')], "domain": 'md'},
}
