"""Measuring Length — Grade 2 question families for measuring-length."""
from fam2 import *

DOMAIN = 'md'

SKILLS = {
    1: {"name": 'Measure objects in centimeters using a ruler', "fams": [ruler_items(), count_collection_items(120), domain_facts_items('md')]},
    2: {"name": 'Estimate and measure lengths in meters', "fams": [measure_unit_items('metric'), ruler_items(), domain_facts_items('md')]},
    3: {"name": 'Select appropriate metric measuring tools', "fams": [measure_unit_items('metric'), domain_facts_items('md')]},
    4: {"name": 'Solve length comparison problems within 100', "fams": [measure_compare_items('metric'), length_word_items(), domain_facts_items('md')]},
    5: {"name": 'Measure length in inches and feet', "fams": [measure_unit_items('customary'), ruler_items(), domain_facts_items('md')]},
    6: {"name": 'Estimate lengths using customary units', "fams": [measure_unit_items('customary'), length_compare_items(), domain_facts_items('md')]},
    7: {"name": 'Select units and measuring tools appropriate to an object', "fams": [measure_unit_items('customary'), measure_unit_items('metric'), domain_facts_items('md')]},
    8: {"name": 'Solve one- and two-step length word problems', "fams": [length_word_items(), two_step_items(), domain_facts_items('md')]},
    9: {"name": 'Record whole-number measurement data', "fams": [lineplot_items('at'), tally_items('total'), domain_facts_items('md')]},
    10: {"name": 'Create labeled line plots of length measurements', "fams": [lineplot_items('at'), lineplot_items('total'), domain_facts_items('md')]},
    11: {"name": 'Interpret measurement data shown in line plots', "fams": [lineplot_items('most'), lineplot_items('total'), domain_facts_items('md')]},
}
