import csv
import string

def load_defs(csv_filename):
    '''Load JACS and LearningDirect definitions given a path to a CSV. Returns a tuple:
    (reverse lookup dictionary of all titles mapped to respective codes, special titles)

    Special titles can be mapped to multiple codes, e.g.:
    "Statistics": "X100"
    "Statistics": "F450"
    '''
    with open(csv_filename, 'rb') as csvfile:
        defs = csv.reader(csvfile)
        reverse_lookup_dict = {} # the reverse lookup dict - use a title as a key to get the related code
        
        # Some titles have multiple codes attached to them.
        # In other words, there are several codes with the same title.
        # This is bad for the kind of reverse lookup we're doing.
        # We don't have to care about this as long as *our* collection titles aren't one of those "multiple code" ones. So that's what we need to check!
        special_titles = {}
        
        for row in defs:
            cur_code = row[0]
            cur_title = row[1].lower()
        
            # collect the "multiple code" special titles
            if cur_title in reverse_lookup_dict:
                # this title is already in the dict, so it maps to multiple codes
                special_titles[cur_title] = True
            else:
                # this is just a normal title, put it in the reverse lookup dict
                reverse_lookup_dict[cur_title] = cur_code
        
        return reverse_lookup_dict, special_titles

def check_jorum_cols(csv_filename, community, reverse_lookup, trouble_lookup):
    with open(csv_filename, 'rb') as csvfile:
        cur_jorum_collections = csv.reader(csvfile)
        invalid_count = 0
        for row in cur_jorum_collections:
            col_name = row[1]
            
            # transformation 1a - FE titles "ampersand -> and"
            if community == 'Further Education (FE)':
                col_name = col_name.replace('&','and')
                
            # transformation 1b - HE titles "and -> ampersand"
            if community == 'Higher Education (HE)':
                col_name = col_name.replace('and','&')
                
            # transformation 2 - lowercase collection name before comparison
            col_name = col_name.lower()
            
            if col_name in trouble_lookup:
                print 'WARNING! Jorum collection"', col_name, 'matches multiple', community, 'codes.'
            if col_name not in reverse_lookup:
                print col_name
                invalid_count += 1
                
        print '-- ' + str(invalid_count) + ' invalid ' + community + ' collection names'
        print

ld, ld_trouble = load_defs('../HEIFESFAQ1_LDCS_CODES.csv')
jacs, jacs_trouble = load_defs('../JACS3_20120529.csv')
        
check_jorum_cols('../current_collections_FE.csv', 'Further Education (FE)', ld, ld_trouble)
check_jorum_cols('../current_collections_HE.csv', 'Higher Education (HE)', jacs, jacs_trouble)