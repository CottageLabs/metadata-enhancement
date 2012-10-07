import csv
from csv_utils import CSVUtils

# ~~ DEFINITIONS ~~
inp = None # relative path to input file
md = None # handle to CSVUtils object which we'll use to process the Main Dataset
choice_first_run = True # boolean flag for whether you've done anything yet, used by the menu

def interactive_merge():
    global md, inp
    print 'Interactive CSV column merge, working on"' + inp + '".'
    print 
    merge_this = raw_input('Which column would you like to merge with another one? (i.e. the one that you want DELETED after the merge is complete): ')
    into_that = raw_input('Which column are you going merge "' + merge_this + '" into? (i.e. the one that will hold the data from both columns after the merge): ')

    md.interactive_merge(merge_this, into_that)
    choice()

def delete_column():
    global md
    column_name = raw_input('Which column would you like to delete?: ')
    md.delete_column(column_name)
    choice()
    
def save_sorted_columns():
    global md, inp
    print 'Exporting an alphabetically sorted list of columns found in "'+inp+'", separated by UNIX-style new lines.'
    out_path = raw_input('Enter export filename (can be relative UNIX-style path): ')
    sorted_cols = sorted(md.columns)
    sorted_cols = "\n".join(sorted_cols)
    with open(out_path, 'wb') as out:
        out.write(sorted_cols)
    choice()
    
def debug():
    global md
    md.debug()
    choice()
    
def load():
    global md, inp
    md = CSVUtils(inp)
    
def save():
    global md
    print 'Saving file - be careful, if you repeat the input filename as the output filename on the line below, you will be overwriting your original CSV without further warning!'
    out_name = raw_input('Output filename: ')
    md.save(out_name)
    choice()
    
def choice():
    global inp
    global choice_first_run
    
    print
    if not choice_first_run:
        print '[Done] Last operation was successful.'
        print
    print 'What would you like to do with "' + inp + '"?'
    print 'im - interactive merge'
    print 'dc - delete column'
    print 'ec - export a newline-delimited list of the column names found in your CSV (alphabetically sorted)'
    print 'debug - print out some information about your CSV'
    print 's - save to file (you will asked which file, no auto overwrite)'
    print 'q - quit'
    which = raw_input('What\'ll it be?: ')
    print
    
    choice_first_run_orig = choice_first_run
    choice_first_run = False
    
    if which == 'im':
        interactive_merge()
    elif which == 'dc':
        delete_column()
    elif which == 'ec':
        save_sorted_columns()
    elif which == 'debug':
        debug()
    elif which == 's':
        save()
    elif which == 'q':
        return
    else:
        choice_first_run = choice_first_run_orig
        print '[Error] I don\'t understand what you want to do with your CSV. Unknown option: "' + which + '"'
        print 'Choose, again.'
        choice()
    
# ~~ ACTIONS (script flow starts here) ~~
inp = raw_input('Enter relative UNIX-style path to the CSV you want to work on: ')
load()
choice()