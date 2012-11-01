"""
Flattens or rolls up multi-valued columns in a CSV file.
Produces 1 output file per column.

For example:
id,dc.subject[en]
100,keyword1||keyword2||kayword1
101,keyword3

Running this script with the "flatten" option will result in the following file:
dc.subject[en]
100,keyword1
100,keyword2
100,kayword1
101,keyword3

Running this script on the result of "flatten" with the "rollup" option will result in the following file:
id,dc.subject[en]
100,keyword1||keyword2||kayword1
101,keyword3

So flatten <-> rollup.
"""

import sys

from csvwrapper import CSVWrapper

def flatten(c, pivot_col, target_col):
    pass
    
def roll(csvwrapper, pivot_col, target_col):
    pass

def main(argv=None):
    if not argv:
        argv = sys.argv
    
    if len(sys.argv) == 4:
    
        OPERATION = sys.argv[1]
        
        IN = sys.argv[2]
        IN = IN.split(':')
        PIVOT_COL = IN[0].split(',')[0]
        TARGET_COL = IN[0].split(',')[1]
        IN = IN[1]
        if not PIVOT_COL or not TARGET_COL or not IN:
            print "Please specify which file you want to work, which is the pivot column and which is the target column. Your first argument should have this format: <pivot_column>,<target_column>:<input_file>.csv"
            exit()
            
        OUT = sys.argv[3]
    else:
        print "Usage: python", sys.argv[0], "(flatten|rollup) <pivot_column>,<target_column>:<input_file>.csv <output_filename>.csv"
        print "1. First argument is which operation to perform on the data - flatten or roll up"
        print "2. The second argument has three components. Pivot column is the column which identifies individual records (usually something like 'id'). Target column is the one that you want flattened / rolled up. Finally, the input file is a UNIX-style path to the CSV you want to process."
        print "3. Third argument is a UNIX-style path to an output CSV file"
        exit()
        
    c = CSVWrapper(IN)

    c.filter_columns(PIVOT_COL, TARGET_COL)
    
    if OPERATION == 'flatten':
        flatten(c, PIVOT_COL, TARGET_COL)
    elif OPERATION == 'roll':
        roll(c, PIVOT_COL, TARGET_COL)
        
    c.save(OUT)
        
if __name__ == '__main__':
    main()