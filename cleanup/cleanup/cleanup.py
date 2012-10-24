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
    
    for rule_no in range(1,100):
        for letter in string.ascii_lowercase:
            for a in dir(rules):
                if a.startswith('rule' + str(rule_no) + letter) and isinstance(rules.__dict__.get(a), types.FunctionType):
                    
                    runrules.append(rules.__dict__.get(a))

# For the moment, manually code the rules
runrules = [
    # advisor
    rules.rule1a_advisor, rules.rule1b_advisor, rules.rule1c_advisor,
    # author
    rules.rule2a_author, rules.rule2b_author, rules.rule2c_author, rules.rule2d_author, rules.rule2e_author, rules.rule2f_author, rules.rule2g_author, rules.rule2h_author, rules.rule2i_author,
    # creator
    rules.rule3a_creator, rules.rule3b_creator, rules.rule3c_creator,
    # contributor
    rules.rule4a_contributor, rules.rule4b_contributor, rules.rule4c_contributor, rules.rule4d_contributor, 
    # subject
    rules.rule5a_subject, rules.rule5b_subject, rules.rule5c_subject, rules.rule5d_subject, rules.rule5e_subject, rules.rule5f_subject, 
    # coverage
    rules.rule6a_coverage, rules.rule6b_coverage,
    # date
    rules.rule7a_date, rules.rule7b_date, rules.rule7c_date, rules.rule7d_date, rules.rule7e_date, rules.rule7f_date,
    # description
    rules.rule8a_description, rules.rule8b_description, rules.rule8c_description,
    # format
    rules.rule9a_format,
    # language
    rules.rule10a_language, rules.rule10b_language,
    # title
    rules.rule11a_title, rules.rule11b_title,
    # identifier
    rules.rule12a_identifier,
    # publisher
    rules.rule13a_publisher, rules.rule13b_publisher,
    # LOM
    rules.rule14a_lom,
    # general tidying
    rules.rule16a_general, rules.rule16c_general, rules.rule16d_general, rules.rule16e_general
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