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
    CSV = sys.argv[1]
    if not CSV:
        print "Please supply a path to a csv file to process"
        exit()

    OUT = sys.argv[2]
    if not OUT:
        print "Please supply a path to a csv file to output to"
        exit()
    
    RULE = sys.argv[3] if len(sys.argv) > 3 else None
else:
    print "This script takes 2 or 3 arguments"
    print "1. path to a CSV file to process (input)"
    print "2. path to a CSV file to output to"
    print "3. a single rule name to run"
    exit()

# give the user some feedback on the run parameters
print "CONFIG: Modifying metadata in " + CSV
print "CONFIG: Writing changes to " + OUT
if RULE is not None:
    print "CONFIG: Running rule " + RULE

# define the order of the rules to be run
runrules = []
if RULE is not None: # just run the one rule
    runrules.append(rules.__dict__.get(RULE))
else: # run all of the rules
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
print "Loading csv from " + CSV + " ..."
csv_wrapper = CSVWrapper(CSV)
print "done"

# run through all the rules, passing in the wrapper each time
for rule in runrules:
    print "Executing rule " + rule.__name__ + " ..."
    rule(csv_wrapper)
    print "complete"

# once we're finished, write out the results
print "Saving ..."
csv_wrapper.save(OUT)