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

Running this script on the result of "flatten" with the "roll" option will result in the following file:
id,dc.subject[en]
100,keyword1||keyword2||kayword1
101,keyword3

So flatten <-> roll.
"""

import sys, csv

from csvwrapper import CSVWrapper

def flatten(c, pivot_col, target_col):
    csv_rows = []
    for id in c.csv_dict[target_col].keys():
            
        cell = c.csv_dict[target_col][id]
        
        tokenised_values = []
        for value in cell:
            tokenised_values += c._tokenise(value)
        
        for tv in tokenised_values:
            csv_row = []
            csv_row.append(c._serialise(c.csv_dict[pivot_col][id]))
            csv_row.append(tv)
            csv_rows.append(csv_row)
            
    return csv_rows
    
def roll(csv_rows, pivot_col, target_col):
    c = CSVWrapper()
    first = True
    c.csv_dict = {}
    header_index_map = {}
    for row in csv_rows:
        for i in range(len(row)): # be explicit about reading the indices of the row
            if first:
                c.csv_dict[row[i]] = {}
                header_index_map[i] = row[i]
            else:
                key = header_index_map[i]
                c.csv_dict[key].setdefault(int(row[0]), [])
                c.add_value(key, int(row[0]), *c._tokenise(row[i]))
        if first: 
            first = False
            
    c.populate_ids()
    return c

def main(argv=None):
    if not argv:
        argv = sys.argv
    
    if len(sys.argv) == 4:
        argument_parse_error = \
        """ERROR: Please specify which file you want to work on, which is the pivot column and which is the target column. Your first argument should have this format: <pivot_column>,<target_column>:<input_file>.csv"""
        
        try:
            OPERATION = sys.argv[1]
            
            IN = sys.argv[2]
            IN = IN.split(':')
            PIVOT_COL = IN[0].split(',')[0]
            TARGET_COL = IN[0].split(',')[1]
            IN = IN[1]
            
            OUT = sys.argv[3]
                
        except IndexError:
            print argument_parse_error
            exit()
            
        if not PIVOT_COL or not TARGET_COL or not IN:
            print argument_parse_error
            exit()
            
    else:
        print "Usage: python", sys.argv[0], "(flatten|roll) <pivot_column>,<target_column>:<input_file>.csv <output_filename>.csv"
        print "1. First argument is which operation to perform on the data - flatten or roll up"
        print "2. The second argument has three components. Pivot column is the column which identifies individual records (usually something like 'id'). Target column is the one that you want flattened / rolled up. Finally, the input file is a UNIX-style path to the CSV you want to process."
        print "3. Third argument is a UNIX-style path to an output CSV file"
        exit()
        
    if OPERATION not in ['flatten', 'roll']:
        print 'ERROR: Operation to be performed needs to be either "flatten" or "roll" (no quotes)'
        exit()
    
    if OPERATION == 'flatten':
        print 'FLATTENING'
        
    elif OPERATION == 'roll':
        print 'ROLLING UP'
        
    print 'Loading', IN,
    
    if OPERATION == 'flatten':
        c = CSVWrapper(IN)
        
    elif OPERATION == 'roll':
        with open(IN, 'rb') as f:
            r = csv.reader(f)
            c = []
            for row in r:
                c.append(row)
                
    print '... done.'
    
    if OPERATION == 'flatten':
        print 'Flattening',
        c.filter_columns(PIVOT_COL, TARGET_COL)
        
        csv_rows = [[PIVOT_COL, TARGET_COL]] # results header row
        csv_rows += flatten(c, PIVOT_COL, TARGET_COL)
        
    elif OPERATION == 'roll':
        print 'Rolling up',
        c_out = roll(c, PIVOT_COL, TARGET_COL)
        
    print 'with pivot:', PIVOT_COL, 'and target:', TARGET_COL

    print 'Saving', OUT,
    
    if OPERATION == 'flatten':
        with open(OUT, "wb") as f:
            writer = csv.writer(f)
            writer.writerows(csv_rows)
            
    elif OPERATION == 'roll':
        c_out.save(OUT)

    print '... done.'
        
if __name__ == '__main__':
    main()