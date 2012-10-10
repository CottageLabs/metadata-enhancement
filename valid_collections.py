import csv
import string
import copy

def load_defs(csv_filename):
    '''Load JACS and LearningDirect definitions given a path to a CSV. Returns a tuple:
    (reverse lookup dictionary of all titles mapped to respective codes, special titles)

    Special titles can be mapped to multiple codes, e.g.:
    "Statistics": "X100"
    "Statistics": "F450"
    '''
    with open(csv_filename, 'rb') as csvfile:
        defs = csv.reader(csvfile)
        lookup_by_title = {} # the reverse lookup dict - use a title as a key to get the related code
        lookup_by_code = {} # the usual lookup - give a code, get a title
        
        # Some titles have multiple codes attached to them.
        # In other words, there are several codes with the same title.
        # This is bad for the kind of reverse lookup we're doing.
        # We don't have to care about this as long as *our* collection titles aren't one of those "multiple code" ones. So that's what we need to check!
        special_titles = {}
        
        for row in defs:
            cur_code = row[0]
            orig_title = row[1]
            cur_title = orig_title.lower()
            
            lookup_by_code[cur_code] = orig_title
        
            # collect the "multiple code" special titles
            if cur_title in lookup_by_title:
                # this title is already in the dict, so it maps to multiple codes
                special_titles[cur_title] = True
            else:
                # this is just a normal title, put it in the reverse lookup dict
                lookup_by_title[cur_title] = cur_code
        
        return lookup_by_code, lookup_by_title, special_titles

        
def validate_jorum_cols(csv_filename, community, lookup_by_code, lookup_by_title, trouble_lookup):
    with open(csv_filename, 'rb') as csvfile:
        cur_jorum_collections = csv.reader(csvfile)
        invalid_count = 0
        valid_collections = [] # list of lists - ready to be written to CSV
        
        for row in cur_jorum_collections:
            col_id = row[0]
            col_name = row[1]
            
            # transformation 1a - FE titles "ampersand -> and"
            if community == 'FE':
                col_name = col_name.replace('&','and')
                
            # transformation 1b - HE titles "and -> ampersand"
            if community == 'HE':
                col_name = col_name.replace('and','&')
                
            # transformation 2 - lowercase collection name before comparison
            col_name = col_name.lower()
            
            valid = True # valid collection
            if col_name in trouble_lookup:
                print 'WARNING! Jorum collection"', col_name, 'matches multiple', community, 'codes.'
                valid = False
                
            if col_name not in lookup_by_title:
                print col_name
                valid = False
                invalid_count += 1
                
            if valid:
                if col_name in valid_collections:
                    print 'WARNING! Duplicate (valid) collection name', col_name, 'in community', community, '.'
                else:
                # Everything is fine, it's not a duplicate title, it's a valid collection
                # So get the corresponding LD or JACS code
                    code = lookup_by_title[col_name]
                    definition_title = lookup_by_code[code]
                    
                    result_row = []
                    result_row.append(col_id)
                    result_row.append(community)
                    
                    if community == 'FE':
                        result_row.append('')
                        result_row.append('')
                        result_row.append(code)
                        result_row.append(definition_title)
                    elif community == 'HE':
                        result_row.append(code)
                        result_row.append(definition_title)
                        result_row.append('')
                        result_row.append('')
                        
                    valid_collections.append(copy.copy(result_row))
                
        print '-- ' + str(invalid_count) + ' invalid ' + community + ' collection names'
        print
        
        return valid_collections

ld_by_code, ld_by_title, ld_trouble = load_defs('../HEIFESFAQ1_LDCS_CODES.csv')
jacs_by_code, jacs_by_title, jacs_trouble = load_defs('../JACS3_20120529.csv')

        
valid_fe = validate_jorum_cols('../current_collections_FE.csv', 'FE', ld_by_code, ld_by_title, ld_trouble)

valid_he = validate_jorum_cols('../current_collections_HE.csv', 'HE', jacs_by_code, jacs_by_title, jacs_trouble)

headings = ['Handle', 'HE/FE', 'JACS Code', 'JACS Name', 'LD Code', 'LD Name']

with open('../jorum_collections.csv', 'wb') as csvfile:
    output = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
    output.writerow(headings)
    output.writerows(valid_fe + valid_he)