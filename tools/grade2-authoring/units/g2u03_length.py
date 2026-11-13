"""Measuring Length — Grade 2 question families for measuring-length."""
from fam2 import *

DOMAIN = 'md'

SKILLS = {
    1: {"name": 'Measure objects in centimeters using a ruler', "fams": [measure_compare_items('metric', 100), ruler_items()]},
    2: {"name": 'Estimate and measure lengths in meters', "fams": [measure_unit_items('metric'), measure_compare_items('metric', 100)]},
    3: {"name": 'Select appropriate metric measuring tools', "fams": [measure_unit_items('metric'), measure_compare_items('metric', 100)]},
    4: {"name": 'Solve length comparison problems within 100', "fams": [measure_compare_items('metric', 100), two_step_items(limit=100)]},
    5: {"name": 'Measure length in inches and feet', "fams": [measure_unit_items('customary'), measure_compare_items('customary', 100)]},
    6: {"name": 'Estimate lengths using customary units', "fams": [measure_unit_items('customary'), measure_compare_items('customary', 100)]},
    7: {"name": 'Select units and measuring tools appropriate to an object', "fams": [measure_unit_items('customary'), measure_unit_items('metric')]},
    8: {"name": 'Solve one- and two-step length word problems', "fams": [measure_compare_items('customary', 100), two_step_items()]},
    9: {"name": 'Record whole-number measurement data', "fams": [lineplot_items('at'), tally_data_items('total')]},
    10: {"name": 'Create labeled line plots of length measurements', "fams": [lineplot_items('at'), lineplot_items('total')]},
    11: {"name": 'Interpret measurement data shown in line plots', "fams": [lineplot_items('most'), lineplot_items('total')]},
}
