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
MAKE_RELEASE = None

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
    
    MAKE_RELEASE = True if len(sys.argv) > 3 and sys.argv[3] == 'release' else False
    
    RULE = sys.argv[4] if len(sys.argv) > 4 else None
    
else:
    print "This script takes 2 mandatory and 2 optional arguments"
    print "[NEED] 1. path to a CSV file to process (input)"
    print "[NEED] 2. path to a CSV file to output to"
    print "[optional] 3. output version - the word 'release' or 'draft' (w/out the quotes)"
    print "[optional] 4. a single rule name to run"
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
    # For the moment, manually code the rules
    runrules = [
        # advisor
        rules.rule1a_advisor, rules.rule1b_advisor, rules.rule1c_advisor,
        # author
        rules.rule2a_author, rules.rule2b_author, rules.rule2c_author, 
        rules.rule2d_author, rules.rule2e_author, rules.rule2f_author, 
        rules.rule2g_author, rules.rule2h_author, rules.rule2i_author,
        # creator
        rules.rule3a_creator, rules.rule3b_creator, rules.rule3c_creator,
        # contributor
        rules.rule4a_contributor, rules.rule4b_contributor, rules.rule4c_contributor, 
        rules.rule4d_contributor, 
        # subject
        rules.rule5a_subject, rules.rule5b_subject, rules.rule5c_subject, 
        rules.rule5d_subject, rules.rule5e_subject, rules.rule5f_subject,
        # coverage
        rules.rule6a_coverage, rules.rule6b_coverage,
        # date
        rules.rule7a_date, rules.rule7b_date, rules.rule7c_date, 
        rules.rule7d_date, rules.rule7e_date, rules.rule7f_date,
        # description
        rules.rule8a_description, rules.rule8b_description,
        # format
        rules.rule9a_format,
        # language
        rules.rule10a_language, rules.rule10b_language,
        # title
        rules.rule11a_title,
        # identifier
        rules.rule12a_identifier,
        # publisher
        rules.rule13a_publisher, rules.rule13b_publisher, rules.rule13c_publisher,
        # LOM
        rules.rule14a_lom,
        # Merge results from manual processing
        rules.rule15a_mergemanual, rules.rule15b_mergemanual,
        # general tidying
        rules.rule16a_general, rules.rule16c_general, rules.rule16d_general, 
        rules.rule16e_general, rules.rule16f_general
    ]

draft_only_rules = []
release_only_rules = [rules.rule13c_publisher, rules.rule15a_mergemanual, rules.rule15b_mergemanual, rules.rule16c_general, rules.rule16f_general]

# load the csv
print "Loading csv from " + CSV + " ..."
csv_wrapper = CSVWrapper(CSV)
print "done"
print

if MAKE_RELEASE and not RULE:
    runrules = release_only_rules

# run through all the rules, passing in the wrapper each time
count_run = 0
for rule in runrules:

    # skip certain rules based on whether we're making a draft or release version
    if MAKE_RELEASE:
        if rule in draft_only_rules:
            continue
    else: # we're doing a draft
        if rule in release_only_rules:
            continue
    
    print "Executing rule " + rule.__name__ + " ...",
    rule(csv_wrapper)
    count_run += 1
    print "done."
print

print 'Ran', count_run, 'rules'
print

# once we're finished, write out the results
print "Saving to " + OUT + " ..."
csv_wrapper.save(OUT)
print "done"