"""
Helps with manual processing tasks by exporting the note* columns into separate spreadsheets alongside fields of interest and Jorum item ID-s.
"""

import sys

from csvwrapper import CSVWrapper

interesting_cols = {
    'note.dc.publisher[en]': ['id', 'dc.publisher[en]', 'dc.contributor.author[en]', 'note.dc.publisher[en]', 'manual.dc.publisher[en].is_not_person_name'],
    'note.organisations': ['id', 'dc.contributor.author[en]', 'dc.subject[en]', 'dc.publisher[en]', 'note.organisations', 'manual.organisations.add_to_publisher']
}

filenames = {
    'note.dc.publisher[en]': 'problems-publisher.csv',
    'note.organisations': 'problems-organisations.csv'
}

# which columns to delete when helpman_mergeprep.py is run
# after a human reviews the output of this script
mergeprep_delete_cols = {
    'problems-publisher.csv': ['dc.publisher[en]', 'dc.contributor.author[en]'],
    'problems-organisations.csv': ['dc.contributor.author[en]', 'dc.subject[en]', 'dc.publisher[en]']
}

def main(argv=None):
    if not argv:
        argv = sys.argv
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
        
    # load the csv
    print "Loading csv from " + CSV + " ..."
    c = CSVWrapper(CSV)
    print "done"
    print

    for col in interesting_cols.keys():
        print 'Saving interesting data wrt column', col, 'to', OUTDIR + filenames[col] 
        print 'Slicing off these columns:', ', '.join(interesting_cols[col])
        
        filtered_rows = c.filter_rows(col, should_be_empty=False)
        
        c.save(OUTDIR + filenames[col], interesting_cols[col], filtered_rows)
        
        print '... done'
        print

    for col, csv in filenames.items():
        tmp = CSVWrapper(OUTDIR + csv)
        print 'Number of items in', csv, '=', len(tmp.csv_dict['id']), '.'
    
if __name__ == '__main__':
    main()