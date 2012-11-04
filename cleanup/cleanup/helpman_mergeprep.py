"""
Helps with manual processing tasks by modifying the spreadsheets produced by 
helpman.py for manual review, deleting all supplementary columns from them. 
These help the human review but should not be merged back into the main dataset.
"""

import sys

from csvwrapper import CSVWrapper
import helpman

filenames = helpman.filenames.values()
delete_cols = helpman.mergeprep_delete_cols

if len(sys.argv) == 3:
    INDIR = sys.argv[1]
    if not INDIR:
        print "Please supply a path to an input directory"
        exit()
    OUTDIR = sys.argv[2]
    if not OUTDIR:
        print "Please supply a path to an output directory"
        exit()
else:
    print "Usage: python", sys.argv[0], "<input_dir> <output_dir>"
    print "First argument must be a path to a directory. The script will process the following filenames (produced by helpman.py): " + ", ".join(filenames)
    print "Second argument must be a path to a directory where the output files can be written (UNIX-style, ending in /)"
    exit()

csvs = {}
for f in filenames:
    # load the csvs
    print "Loading csv from ", INDIR + f, " ..."
    csvs[f] = CSVWrapper(INDIR + f)
    print "done"
    print

for filename, c in csvs.items():
    print 'Processing', filename
    print 'Deleting these columns:', ', '.join(delete_cols[filename])
    
    for col in delete_cols[filename]:
        c.delete_column(col)
    
    print 'Saving', OUTDIR + filename,
    c.save(OUTDIR + filename)
    print '... done'
    print
