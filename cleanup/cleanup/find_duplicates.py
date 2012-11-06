import csv
from csvwrapper import CSVWrapper, normalise_strings, denormalise_strings

import sys

def detect_and_strip_duplicates(values):
    norm_values, map = normalise_strings(values)
    
    new_values = []
    for value in norm_values:
        if value not in new_values:
            new_values.append(value)
        else:
            print values, '. Duplicate was:', value
            
    return denormalise_strings(new_values, map)

def main(argv=None):
    if not argv:
        argv=sys.argv
    IN = argv[1]
    c = CSVWrapper(IN)
    
    c.apply_global_cell_function(detect_and_strip_duplicates)
    
    
if __name__ == '__main__':
    main()