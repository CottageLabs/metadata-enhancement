"""
Controlling class for applying metadata cleanup rules to the 
csv
"""

import sys, types, string
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
print

# define the order of the rules to be run
runrules = []
if RULE is not None: # just run the one rule
    runrules.append(rules.__dict__.get(RULE))
else: # run all of the rules
    # Instead of defining manually, get all the functions defined by the rules 
    # module whose names start with "rule" in ALPHABETICAL order (fine for our 
    # module).
    # FIXME: is this going to work when there are more than 10 rulesets, with the
    # ASCIIBETICAL sorting that we'll get?  Note to self: check asciibetical sorting
    # rules
    # FIXME: No, you're right, it starts from 10, goes to 11, just amazing. 
    # Implemented a "solution" below. At least they'll run in order now, even 
    # though it's ugly. Format is: rule<rule_no><sub_rule_letter>
    
    for rule_no in range(1,16): # 1 to 15 (incl. 15)
        for letter in string.ascii_lowercase:
            for a in dir(rules):
                if a.startswith('rule' + str(rule_no) + letter) and isinstance(rules.__dict__.get(a), types.FunctionType):
                    
                    runrules.append(rules.__dict__.get(a))

# For the moment, manually code the rules
runrules = [
    rules.rule1a_advisor, rules.rule1b_advisor, rules.rule1c_advisor, # deal with the advisor column group
    rules.rule2a_author, rules.rule2b_author, rules.rule2c_author,  # deal with the author column group
    rules.rule2d_author, rules.rule2e_author, rules.rule2f_author,  #
    rules.rule2g_author,                                            #
    rules.rule3a_creator, rules.rule3b_creator,  # deal with creator column group
    rules.rule4a_contributor, rules.rule4b_contributor, rules.rule4c_contributor # contributor column group
    ]

# load the csv
print "Loading csv from " + CSV + " ..."
csv_wrapper = CSVWrapper(CSV)
print "done"
print

# run through all the rules, passing in the wrapper each time
count_run = 0
for rule in runrules:
    print "Executing rule " + rule.__name__ + " ..."
    rule(csv_wrapper)
    count_run += 1
    print "complete"
print

print 'Ran', count_run, 'rules'
print

# once we're finished, write out the results
print "Saving to " + OUT + " ..."
csv_wrapper.save(OUT)
print "done"