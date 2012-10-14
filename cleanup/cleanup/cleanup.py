"""
Controlling class for applying metadata cleanup rules to the 
csv
"""

import sys, types
from csvwrapper import CSVWrapper
import rules

CSV = None
OUT = None
RULE = None

# obtain the csv file paths from the command line arguments
# and optionally the rule we want to run

if len(sys.argv) > 2:
    CSV = sys.argv.get(1)
    if not CSV:
        print "Please supply a path to a csv file to process"
        exit()

    OUT = sys.argv.get(2)
    if not OUT:
        print "Please supply a path to a csv file to output to"
        exit()
    
    RULE = sys.argv.get(3)
else:
    print "This script takes 2 or 3 arguments"
    print "1. path to a CSV file to process (input)"
    print "2. path to a CSV file to output to"
    print "3. a single rule name to run"
    exit()

# define the order of the rules to be run

# runrules = [rule1a_advisor, rules.rule7a_date]
runrules = []
if RULE is not None:
    runrules.append(rules.__dict__.get(RULE))
else:
    # Instead of defining manually, get all the functions defined by the rules 
    # module whose names start with "rule" in ALPHABETICAL order (fine for our 
    # module).
    runrules = [ # Make a list of ..
        rules.__dict__.get(a) # .. the actual function objects corresponding to ..
        for a in dir(rules) # .. all names in the rules module ..
        if a.startswith('rule') # .. which start with "rule" ..
        and isinstance(rules.__dict__.get(a), types.FunctionType) # .. and represent a function.
        ]  
  
# load the csv
csv_wrapper = CSVWrapper(CSV)

# run through all the rules, passing in the wrapper each time
for rule in runrules:
    rule(csv_wrapper)

# once we're finished, write out the results
csv_wrapper.save(OUT)