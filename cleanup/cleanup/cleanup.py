"""
Controlling class for applying metadata cleanup rules to the 
csv
"""

from csvwrapper import CSVWrapper
import rules

# obtain the csv file paths from the command line arguments
CSV = sys.argv.get(1)
if CSV is None or CSV == "":
    print "Please supply a path to a csv file to process"
    exit()

OUT = sys.argv.get(2)
if OUT is None or OUT = "":
    print "Please supply a path to a csv file to output to"
    exit()

# define the order of the rules to be run
rules = [rules.rule7a_date]

# load the csv
csv_wrapper = CSVWrapper(CSV)

# run through all the rules, passing in the wrapper each time
for rule in rules:
    rule(csv_wrapper)

# once we're finished, write out the results
csv_wrapper.save(OUT)