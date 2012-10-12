"""
Controlling class for applying metadata cleanup rules to the 
csv
"""

import sys
import types

from csvwrapper import CSVWrapper
import rules


# obtain the csv file paths from the command line arguments
if len(sys.argv) > 2:
    CSV = sys.argv[1]
    if not CSV:
        print "Please supply a path to a csv file to process"
        exit()

    OUT = sys.argv[2]
    if not OUT:
        print "Please supply a path to a csv file to output to"
        exit()
else:
    print "This script takes 2 arguments"
    print "1. path to a CSV file to process (input)"
    print "2. path to a CSV file to output to"
    exit()

# define the order of the rules to be run
# runrules = [rule1a_advisor, rules.rule7a_date]

# instead of defining manually, get all the functions defined by the rules module (they will be ordered as they are defined in the rules source)
# see http://stackoverflow.com/questions/139180/listing-all-functions-in-a-python-module#answer-139258 
runrules = [rules.__dict__.get(a) for a in dir(rules)
  if isinstance(rules.__dict__.get(a), types.FunctionType)]

# load the csv
csv_wrapper = CSVWrapper(CSV)

# run through all the rules, passing in the wrapper each time
for rule in runrules:
    rule(csv_wrapper)

# once we're finished, write out the results
csv_wrapper.save(OUT)