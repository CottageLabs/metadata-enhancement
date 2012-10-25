"""
Helps with manual processing tasks by exporting the note* columns into separate spreadsheets alongside fields of interest and Jorum item ID-s.
"""

import sys

from csvwrapper import CSVWrapper

if len(sys.argv) == 3:
    CSV = sys.argv[1]
    if not CSV:
        print "Please supply a path to a csv file to process"
        exit()
    OUTDIR = sys.argv[2]
    if not OUTDIR:
        print "Please supply a path to an output directory"
        exit()
else:
    print "Usage: python", sys.argv[0], "<csv_input> <output_dir>"
    print "First argument must be a path to a csv file to process"
    print "Second argument must be a path to a directory where the output files can be written (UNIX-style, ending in /)"
    exit()
    
interesting_cols = {
    'note.dc.publisher[en]': ['id', 'dc.publisher[en]', 'dc.contributor.author[en]'],
    'note.organisations': ['id', 'dc.contributor.author[en]', 'dc.subject[en]', 'dc.publisher[en]']
}

look_for = {
    'note.dc.publisher[en]': ['possible person name'],
    'note.organisations': ['possible org name']
}

filenames = {
    'note.dc.publisher[en]': 'problems-publisher.csv',
    'note.organisations': 'problems-organisations.csv'
}

# load the csv
print "Loading csv from " + CSV + " ..."
c = CSVWrapper(CSV)
print "done"
print

for col in interesting_cols.keys():
    print 'Saving interesting data wrt column', col, 'to', OUTDIR + filenames[col] 
    print 'Slicing off these columns:', ', '.join(interesting_cols[col])
    c.save(OUTDIR + filenames[col], interesting_cols[col], col, look_for[col])
    print '... done'
    print

for col, csv in filenames.items():
    tmp = CSVWrapper(OUTDIR + csv)
    print 'Number of potential problems in', col, '=', len(tmp.csv_dict['id']), '.',
    print 'Potential problem means:', ', '.join(look_for[col])