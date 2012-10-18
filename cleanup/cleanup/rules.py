"""
A set of rules implemented over the CSVWrapper which manage the
metadata cleanup tasks
"""

# Functions shared between different rules
###########################################################

def clean_list(list):
    # strip whitespace off both ends and remove empty elements from the list
    return [clean_item for clean_item in [item.strip() for item in list] if clean_item]

def strip_email(values):
    import re
    x = "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}"
    new_values = []
    for value in values:
        if re.match(x, value) is None:
            new_values.append(value)
    return new_values

def detect_oddities(value):
    # check for capitalisation - surprisingly tricky
    capitalised = value.split(" ")[0].istitle()
    if not capitalised:
        return True
    # check for surprisingly short strings
    if len(value) < 5:
        return True
    return False
    
def may_be_org(data):
    """
    True if the given string looks like an organisation name (certain keywords). 
    False otherwise.
    """
    value = data.lower()
    org_keywords = ['university', 'institution', 'school', 'college']
    for word in org_keywords:
        if word in value:
            return True
    
    return False
        
def is_known_org(data):
    known_organisations = ['x4l healthier nation', 'leeds metropolitan university', 'cilip', 'the learning bank', 'university of york', 'institution of enterprise', 'open educational repository in support of computer science', 'uclan', 'uclanoer']
    
    if data.lower() in known_organisations:
        return True
    else:
        return False
        
# 1. Advisor columns
###########################################################

# 1.a. merge dc.contributor.advisor[] into dc.contributor.advisor[en]
def rule1a_advisor(csv_wrapper):
    csv_wrapper.merge_columns('dc.contributor.advisor[]', 'dc.contributor.advisor[en]')

# 1.b. Move the following values to the following locations:
def rule1b_advisor(csv_wrapper):
    working_on = 'dc.contributor.advisor[en]' # column we're working on
    
    # 1.b.i. conadv (x1) -> delete record
    item_ids = csv_wrapper.find_in_column(working_on, 'conadv')
    for item_id in item_ids:
        csv_wrapper.delete_record(item_id)
    
    # 1.b.ii. DiPEX (x1) -> dc.publisher (as DIPEx)
    item_ids = csv_wrapper.find_in_column(working_on, 'DiPEX')
    for item_id in item_ids:
        csv_wrapper.add_value('dc.publisher[en]', item_id, 'DIPEx')
        csv_wrapper.delete_contents(working_on, item_id)
    
    # 1.b.iii. iCase bioukoer (x3) -> dc.subject, split by whitespace, add ukoer to subject also
    item_ids = csv_wrapper.find_in_column(working_on, 'iCase bioukoer')
    for item_id in item_ids:
        csv_wrapper.add_value('dc.subject[en]', item_id, *['iCase', 'bioukoer', 'ukoer'])
        csv_wrapper.delete_contents(working_on, item_id)
    
    # 1.b.iv. Rong Yang (x1) -> move to dc.contributor.author[en]
    item_ids = csv_wrapper.find_in_column(working_on, 'Rong Yang')
    for item_id in item_ids:
        csv_wrapper.add_value('dc.contributor.author[en]', item_id, 'Rong Yang')
        csv_wrapper.delete_contents(working_on, item_id)
        
    # 1.b.v. UCLAN (x1) -> delete value, add uclanoer to dc.subject
    item_ids = csv_wrapper.find_in_column(working_on, 'UCLAN')
    for item_id in item_ids:
        csv_wrapper.add_value('dc.subject[en]', item_id, 'uclanoer')
        csv_wrapper.delete_contents(working_on, item_id)
    
# 1.c. delete Advisor column group
# dc.contributor.advisor[en] should be the only column left from the Advisor group by now
def rule1c_advisor(csv_wrapper):
    csv_wrapper.delete_column('dc.contributor.advisor[en]')
    
    
# 2. Author column group
###########################################################

# 2.a. merge dc.contributor.author[] into dc.contributor.author[en]
def rule2a_author(csv_wrapper):
    csv_wrapper.merge_columns('dc.contributor.author[]', 'dc.contributor.author[en]')

# 2.b. merge dc.contributor.author[x-none] into dc.contributor.author[en]
def rule2b_author(csv_wrapper):
    csv_wrapper.merge_columns('dc.contributor.author[x-none]', 'dc.contributor.author[en]')

# 2.c. merge dc.contributor.author into dc.contributor.author[en]
def rule2c_author(csv_wrapper):
    csv_wrapper.merge_columns('dc.contributor.author', 'dc.contributor.author[en]')
    
# 2.d. delete dc.contributor.author[English]
def rule2d_author(csv_wrapper):
    csv_wrapper.delete_column('dc.contributor.author[English]')
    
# 2.e. merge dc.contributor.author[en-gb] into dc.publisher[en]
def rule2e_author(csv_wrapper):
    csv_wrapper.merge_columns('dc.contributor.author[en-gb]', 'dc.publisher[en]')

# 2.f. if value == 'contributor', delete it (only Author columns)
# dc.contributor.author[en] should be the only Author column left at this point
def rule2f_author(csv_wrapper):
    item_ids = csv_wrapper.find_in_column('dc.contributor.author[en]', 'contributor')
    for item_id in item_ids:
        csv_wrapper.delete_contents('dc.contributor.author[en]', item_id)

# 2.g. if value is a VCARD, get the name and leave only the name
def rule2g_author(csv_wrapper):
    def replace_vcard(data):
        if 'vcard' in data:
            # The example of a VCARD that we have starts with the name
            # and continues with the ORG (ORGanisation) field. So finding 
            # where the ORG field starts gives us the end of the name 
            # (we have to get the character *before* the ORG field, so -1).
            end_of_name = data.find('ORG') - 1
            # Get only the name (ignoring the space character after it 
            # and the rest of the VCARD info).
            return data[:end_of_name]
        else:
            return data
        
    csv_wrapper.apply_value_function('dc.contributor.author[en]', replace_vcard)
    
# 2.h. Copy all organisation names to dc.publisher[en] where possible.
def rule2h_author(csv_wrapper):
    src = 'dc.contributor.author[en]'
    dst = 'dc.publisher[en]'
    
    # 2.h.i. pattern match on "university", "institution", "school"
    csv_wrapper.c2c_copy_by_value_function(src, dst, may_be_org)
    
    # 2.h.ii. check for known, commonly appearing organisations
    csv_wrapper.c2c_copy_by_value_function(src, dst, is_known_org)
    
    
# 2.i. if value == 'uclanoer' || value == 'uclan' -> delete value
def rule2i_author(csv_wrapper):
    def delete_uclan_uclanoer_authors(data):
        if data == 'uclan' or data == 'uclanoer':
            return None
        else:
            return data
    
    csv_wrapper.apply_value_function('dc.contributor.author[en]', delete_uclan_uclanoer_authors)
    
# 3. Creator column group
###########################################################

# 3.a. merge dc.creator[] into dc.creator
def rule3a_creator(csv_wrapper):
    csv_wrapper.merge_columns('dc.creator[]', 'dc.creator')
        
# 3.b. split names separated by ";" into separate values
def rule3b_creator(csv_wrapper):
    def split_by_semicolon(values):
        new_values = []
        for value in values:
            results = value.split(';')
            # strip preceding/trailing whitespace and empty elements after the split
            results = [clean_item.strip() for clean_item in results if clean_item]
            new_values += results
        return new_values
        
    csv_wrapper.apply_cell_function('dc.creator', split_by_semicolon)
    
# 4. Contributor column group
###########################################################

# 4.a. Detect all email addresses in dc.contributor and remove
def rule4a_contributor(csv_wrapper):
    csv_wrapper.apply_cell_function('dc.contributor', strip_email)
    
# 4.b. Move all non-email addresses from dc.contributor to dc.publisher[en]
# Previous rule 4.a. should have removed all e-mail addresses, so we basically
# need to move all the strings remaining in dc.contributor to dc.publisher[en].
# This would result in a completely empty dc.contributor, so actually what we 
# want to do is merge dc.contributor INTO dc.publisher[en].
def rule4b_contributor(csv_wrapper):
    csv_wrapper.merge_columns('dc.contributor', 'dc.publisher[en]')
    
# 4.c. Move all from dc.contributor[x-none] to dc.publisher[en]
# In other words, merge dc.contributor[x-none] INTO dc.publisher[en]
def rule4c_contributor(csv_wrapper):
    csv_wrapper.merge_columns('dc.contributor[x-none]', 'dc.publisher[en]')
    
# 5. Subject column group
###########################################################

# 5.a. Merge all dc.subject[*] fields into dc.subject[en]
def rule5a_subject(csv_wrapper):
    csv_wrapper.merge_columns('dc.subject[EN]', 'dc.subject[en]')
    csv_wrapper.merge_columns('dc.subject[]', 'dc.subject[en]')
    csv_wrapper.merge_columns('dc.subject[en-gb]', 'dc.subject[en]')
    csv_wrapper.merge_columns('dc.subject[ene]', 'dc.subject[en]')

# 5.b. Merge dc.contributor.other[en] into dc.subject[en]
def rule5b_subject(csv_wrapper):
    csv_wrapper.merge_columns('dc.contributor.other[en]', 'dc.subject[en]')

# 5.c. Merge dc.subject.classification[] into dc.subject.classification[en]
def rule5c_subject(csv_wrapper):
    csv_wrapper.merge_columns('dc.subject.classification[]', 'dc.subject.classification[en]')

# 5.d. merge dc.description.sponsorship into dc.subject[en]
def rule5d_subject(csv_wrapper):
    csv_wrapper.merge_columns('dc.description.sponsorship', 'dc.subject[en]')

# 5.e. normalise subject keywords
# only one subject column left at this point: dc.subject[en]
def rule5e_subject(csv_wrapper):
    # 5.e.i. normalise spacing
    # 5.e.ii. strip quotes
    # 5.e.iii. to lower case
    def normalise_keywords(data):
        # normalise spacing
        result = ' '.join(data.split())
        
        # strip quotes
        stripchars = ['"']
        # "smart" quotes
        stripchars.append(u'\u201c'.encode('utf-8')) 
        stripchars.append(u'\u201d'.encode('utf-8'))
        
        for char in stripchars:
            result = result.replace(char, '')
            
        # to lower case
        # NOTE: This will probably mess up Unicode data as it is.
        result = result.lower()
        
        return result
    
    csv_wrapper.apply_value_function("dc.subject[en]", normalise_keywords)

# 5.f. for all fields with a single value (i.e. no || in the field), detect and split on "," and ";"
# only one subject column left at this point: dc.subject[en]
# NOTE: implementing this for all values in all fields in Subject, not just single-valued ones
def rule5f_subject(csv_wrapper):
    
    def fix_multival(values):
        new_values = []
        splitchars = [',', ';']
        for value in values:
            results = []
            tripped = False
            for char in splitchars:
                results = value.split(char)
                if len(results) > 1:
                    new_values += [x.strip() for x in results]
                    tripped = True
            if not tripped:
                new_values.append(value)
        return new_values
    
    csv_wrapper.apply_cell_function("dc.subject[en]", fix_multival)

# 6. Coverage column group
###########################################################

# 6.a. delete dc.coverage.temporal[en]
def rule6a_coverage(csv_wrapper):
    csv_wrapper.delete_column("dc.coverage.temporal[en]")
    
# 6.b. delete dc.coverage.spatial[en]
def rule6b_coverage(csv_wrapper):
    csv_wrapper.delete_column("dc.coverage.spatial[en]")


# 7. Date columns
###########################################################

# 7.a. reformat the content of dc.date[] into a timestamp
def rule7a_date(csv_wrapper):
    # from form: Tue, 16 Jun 2009 11:34:02 +0100
    # to form: 2010-11-10T10:09:17Z
    def date_converter(data):
        from datetime import datetime
        try:
            dt = datetime.strptime(data, "%a, %d %b %Y %H:%M:%S +0100")
            return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            # we couldn't convert the date, so leave it as is
            return data
    csv_wrapper.apply_value_function("dc.date[]", date_converter)

# 7.b. merge dc.date[] into dc.date
def rule7b_date(csv_wrapper):
    csv_wrapper.merge_columns("dc.date[]", "dc.date")

# 7.c. merge dc.date.accessioned[*] into dc.date.accessioned
# FIXME: this data does not seem to be present in the latest metadata export
def rule7c_date(csv_wrapper):
    pass

# 7.d. merge dc.date.issued[] into to dc.date.issued
def rule7d_date(csv_wrapper):
    csv_wrapper.merge_columns("dc.date.issued[]", "dc.date.issued")

# 7.e. ensure that all dc.date.* fields have only one value; propose to keep the oldest value, where there is more than one
def rule7e_date(csv_wrapper):
    def date_reduce(values):
        """ reduce the list of date values to one date - the oldest """
        from datetime import datetime
        # if there is only one value, no need to do more
        if len(values) <= 1:
            return values
        dts = []
        for value in values:
            try:
                dt = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
                dts.append(dt)
            except ValueError:
                # if we can't parse all of the dates, we might as well stop
                return values
        # figure out the oldest date from the list
        oldest = dts[0]
        for i in range(1, len(dts)):
            if oldest > dts[i]:
                oldest = dts[i]
        return [datetime.strftime(oldest, "%Y-%m-%dT%H:%M:%SZ")]
        
    # possible date fields:
    # dc.date
    # dc.date.created
    # dc.date.created[en]
    # dc.date.issued
    # dc.date.issued[]
    # dc.date[]
    csv_wrapper.apply_cell_function("dc.date", date_reduce)
    csv_wrapper.apply_cell_function("dc.date.created", date_reduce)
    csv_wrapper.apply_cell_function("dc.date.created[en]", date_reduce)
    csv_wrapper.apply_cell_function("dc.date.issued", date_reduce)
    csv_wrapper.apply_cell_function("dc.date.issued[]", date_reduce)
    csv_wrapper.apply_cell_function("dc.date[]", date_reduce)

# 7.f. Delete dc.date.created[en] column
def rule7f_date(csv_wrapper):
    csv_wrapper.delete_column("dc.date.created[en]")

# 8. Description columns
#############################################################

# 8.a. delete dc.description.uri
def rule8a_description(csv_wrapper):
    csv_wrapper.delete_column("dc.description.uri[en]")

# 8.b. migrate dc.description[] and dc.description[en-gb] to dc.description[en]
def rule8b_description(csv_wrapper):
    csv_wrapper.merge_columns("dc.description[]", "dc.description[en]")
    csv_wrapper.merge_columns("dc.description[en-gb]", "dc.description[en]")

# 8.c. Validate content (check for short strings, starting with capital letters, etc)
def rule8c_description(csv_wrapper):
    ids = csv_wrapper.find_by_value_function("dc.description[en]", detect_oddities)
    csv_wrapper.add_column("note.dc.description[en]")
    csv_wrapper.set_value("note.dc.description[en]", ids, "possible issue")

# 9. Format columns
############################################################

# These need to be replaced with the values calculated directly from the DSpace database
# FIXME: we need the source data first
# copy(select item2bundle.item_id, bitstreamformatregistry.mimetype from bitstream join bundle2bitstream on bitstream.bitstream_id = bundle2bitstream.bitstream_id join item2bundle on bundle2bitstream.bundle_id = item2bundle.bundle_id join bitstreamformatregistry on bitstream.bitstream_format_id = bitstreamformatregistry.bitstream_format_id) to 'formats.csv' with csv header;

# 10. Language columns
#############################################################

# 10.a. delete dc.language[x-none]
def rule10a_language(csv_wrapper):
    csv_wrapper.delete_column("dc.language[x-none]")

# 10.b. merge all dc.language[*] to dc.language
def rule10b_language(csv_wrapper):
    # dc.language
    # dc.language[]
    # dc.language[de]
    # dc.language[en-GB]
    # dc.language[en-gb]
    # dc.language[en]
    # dc.language[fr]
    csv_wrapper.merge_columns("dc.language[]", "dc.language")
    csv_wrapper.merge_columns("dc.language[de]", "dc.language")
    csv_wrapper.merge_columns("dc.language[en-GB]", "dc.language")
    csv_wrapper.merge_columns("dc.language[en-gb]", "dc.language")
    csv_wrapper.merge_columns("dc.language[en]", "dc.language")
    csv_wrapper.merge_columns("dc.language[fr]", "dc.language")

# 10.c. validate and convert all language codes to <two-letter>[-<two letter>] form

# FIXME: Looking at the data, all the codes are two letters,
# except for a bunch of en-gb or en-GB codes.  We can therefore easily normalise,
# and use something like babel to validate the codes to make sure there are no 
# oddities.

# 11. Title columns
#############################################################

# 11.a. merge dc.title[*] to dc.title[en]
def rule11a_title(csv_wrapper):
    csv_wrapper.merge_columns("dc.title[*]", "dc.title[en]")

# 11.b. Validate content (check for short strings, starting with capital letters, etc)
def rule11b_title(csv_wrapper):
    ids = csv_wrapper.find_by_value_function("dc.title[en]", detect_oddities)
    csv_wrapper.add_column("note.dc.title[en]")
    csv_wrapper.set_value("note.dc.title[en]", ids, "possible issue")
    
    
# 12. Identifier columns:
############################################################

# 12.a. merge dc.identifier.uri, dc.identifier.uri[] and dc.identifier.uri[en]
def rule12a_identifier(csv_wrapper):
    csv_wrapper.merge_columns("dc.identifier.uri[]", "dc.identifier.uri")
    csv_wrapper.merge_columns("dc.identifier.uri[en]", "dc.identifier.uri")

# 13. Publisher columns:
############################################################

# 13.a. merge dc.publisher[*] into dc.publisher[en]
def rule13a_publisher(csv_wrapper):
    csv_wrapper.merge_columns("dc.publisher", "dc.publisher[en]")
    csv_wrapper.merge_columns("dc.publisher[en-gb]", "dc.publisher[en]")

# 13.b. auto-detect non-organisations names (e.g. "university", "school", etc) and flag for manual intervention
def rule13b_publisher(csv_wrapper):
    def detect_non_org(value):
        if value == "":
            return False
        compare = value.lower()
        if "university" in compare:
            return False
        if "school" in compare:
            return False
        if "college" in compare:
            return False
        return True
    ids = csv_wrapper.find_by_value_function("dc.publisher[en]", detect_non_org)
    csv_wrapper.add_column("note.dc.publisher[en]")
    csv_wrapper.set_value("note.dc.publisher[en]", ids, "possible person name")

# 14. General tidying
###########################################################

# 14.a. delete the contents of all fields where the only value in the field is 
# "||", the multiple value separator
# 14.b. for all fields with multiple values, de-duplicate repeated values
# this rule should cover both of these ...
def rule14a_general(csv_wrapper):
    csv_wrapper.deduplicate_values()

# 14.c. auto-detect and flag instances of "university", "institution", 
# "school", "college" etc, and report on the rows where these occur, for possible 
# manual intervention
def rule14c_general(csv_wrapper):
    # dc.contributor.author[en]
    # dc.subject
    # dc.contributor[en]
    # dc.creator
    def detect_org(value):
        if value == "":
            return False
        compare = value.lower()
        if "university" in compare:
            return True
        if "school" in compare:
            return True
        if "college" in compare:
            return True
        return False
    ids1 = csv_wrapper.find_by_value_function("dc.contributor.author[en]", detect_org)
    ids2 = csv_wrapper.find_by_value_function("dc.subject", detect_org)
    ids3 = csv_wrapper.find_by_value_function("dc.contributor[en]", detect_org)
    ids4 = csv_wrapper.find_by_value_function("dc.creator", detect_org)
    ids = ids1 + [x for x in ids2 if x not in ids1]
    ids = ids + [x for x in ids3 if x not in ids]
    ids = ids + [x for x in ids4 if x not in ids]
    csv_wrapper.add_column("note.organisations")
    csv_wrapper.set_value("note.organisations", ids, "possible org name")

# 14.d. detect and delete all e-mail addresses (have a way to check it's a safe delete first)
def rule14d_general(csv_wrapper):
    csv_wrapper.apply_global_value_function(strip_email)

# 14.e. detect subject keywords which are suspiciously long
def rule14e_general(csv_wrapper):
    def detect_long(values):
        if len(values) != 1:
            return False
        if len(values[0]) > 30: # that would be a pretty long keyword
            return True
        return False
    ids = csv_wrapper.find_by_value_function("dc.subject", detect_long)
    csv_wrapper.add_column("note.dc.subject")
    csv_wrapper.set_value("note.dc.subject", ids, "long subject")

# 14.f. auto-detect items which would have the defunct "Mathematical and Computer Science" JACS code
# FIXME: do we still need this?
def rule14f_general(csv_wrapper):
    pass
