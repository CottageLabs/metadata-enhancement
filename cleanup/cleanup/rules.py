"""
A set of rules implemented over the CSVWrapper which manage the
metadata cleanup tasks
"""

from csvwrapper import normalise_strings, denormalise_strings

# Data shared between common functions and rules
known_organisations = ["Aston Business School", "Aston University", "Bangor University", "Barrow in Furness 6th Form College", "Bede College", "Bexley College", "Bishop Auckland College", "Blackburn College", "Blackburn University Centre", "Boston College", "Bournemouth University", "Bournemouth and Poole College", "Bournville College", "Bradford College", "Bradford University", "Braintree College", "Bristol University", "Brockenhurst College", "Brunel University", "Burton College", "CILIP", "Calderdale College", "Camberwell college of the arts", "Canterbury Christ Church University", "Cardiff Metropolitan University", "Cardiff University", "Central Saint Martins College of Art And Design", "Coleg Llandrillo Cymru", "Colorado School of Mines", "Core-Materials", "Coventry University", "Craven College", "Croyden College", "De Montfort University", "Deeside College", "Dipex", "Division for Lifelong Learning - University of Bath", "Doncaster College", "Dunstable College", "EDINA", "East Durham and Houghall College", "Edge Hill University", "Edinburgh Napier University", "Fuseworks", "Gateshead College", "Gateway College", "Glasgow Caledonian University", "Grimsby College", "Harlow College", "Hartlepool College", "Hartpury College", "Harvard Law School", "Henley College", "Hibernia College", "Highbury College", "Huddersfield College", "Hull College", "Imperial College London", "Imperial College, London", "Institution of Enterprise", "JISC", "Keele University", "King's College London", "Lancaster University", "Learning And Skills Network Ltd", "Leeds College of Building", "Leeds General University", "Leeds Metropolitan University", "Leicester College", "Leicester University", "Liverpool John Moores University", "London College of Communication", "London College of Fashion", "London Metropolitan University", "Loughborough University", "MIMAS", "Manchester Metropolitan University", "Massey University", "Melbourne School of Population Health", "Middlesbrough College", "Morley College", "Nelson and Colne College", "Nescot College", "New College Nottingham", "New College Telford", "Newcastle College", "Newcastle Under Lyme College", "Newcastle University", "North Hertfordshire College", "North West London College", "Northampton College", "Northumbria University", "Nottingham University", "Oaklands College", "Open Educational Repository In Support of Computer Science", "Open University", "Oxford Brookes University", "Oxford University", "Penwith College", "Peterborough College", "Phg", "Phgk", "Plymouth University", "Priestley College", "Queen Mary University of London", "Queen's University Belfast", "Reading University", "Redcar & Cleveland College", "Regent College", "Regent's College", "Roehampton University", "Rolls-Royce University Technology Centre", "Rose Bruford College of Theatre and Performance", "Royal Holloway University", "Royal Society of Chemistry", "Royal Veterinary College", "Saylor Foundation", "Scotland's Colleges", "Sheffield Hallam University", "Somerset College of Arts & Technology", "South Devon College", "South East Essex VI Form College", "South Thames College", "Southampton Solent University", "Southport College", "St Brendan's 6th Form College", "St George's, University of London", "Staffordshire University", "Stamford College", "Stevenson College", "Stockton 6th Form College", "Stockton Riverside College", "Stoke on Trent 6th Form College", "Technical University of Denmark", "Teesside University", "Thames Valley University", "The Learning Bank", "The University of Liverpool", "Totton College", "Tyne Metropolitan College", "UCLAN", "University College Falmouth", "University College London", "University Federico II", "University Portsmouth", "University for the Creative Arts", "University of Aberdeen", "University of Ancona", "University of Bath", "University of Bedfordshire", "University of Birmingham", "University of Bolton", "University of Bradford", "University of Brighton", "University of Bristol", "University of British Columbia", "University of Cambridge", "University of Central Lancashire", "University of Cumbria", "University of Derby", "University of Dundee", "University of East London", "University of Edinburgh", "University of Exeter", "University of Ferrara", "University of Genoa", "University of Glamorgan", "University of Glasgow", "University of Gloucestershire", "University of Hertfordshire", "University of Hull", "University of Keele", "University of Leeds", "University of Leicester", "University of Leuven", "University of Lincoln", "University of Liverpool", "University of Manchester", "University of Minnesota", "University of New South Wales", "University of Northumbria", "University of Nottingham", "University of Oxford", "University of Padova", "University of Portsmouth", "University of Reading", "University of Sheffield", "University of Southampton", "University of Stockholm", "University of Strathclyde", "University of Surrey", "University of Ulster", "University of Wales, Newport", "University of Warwick", "University of Westminster", "University of Wolverhampton", "University of Worcester", "University of York", "University of the Arts London", "Varndean College", "Wakefield College", "West Hertforsdhire College", "West Kent College", "West Nottinghamshire College", "Weston College", "Winstanley College", "Worcester College of Technology", "Worcester University", "X4L Healthier Nation", "York St John University"]

# add \' versions for all organisations which have an apostrophe in the name
known_organisations_lookup = known_organisations[:]
for o in known_organisations_lookup:
    if "'" in o:
        known_organisations.append(o.replace("'", "\\'"))
        

norm_known_organisations, map_known_organisations = normalise_strings(known_organisations)

ignore_if_org_present = {
    'university of wales': 'University of Wales, Newport',
}

canonical_org_forms = {
    # non-canonical -> canonical mapping
    'University of Wales - Newport': 'University of Wales, Newport',
    'Stafforshire University': "Staffordshire University",
    "Fuseworks": "Fusedworks",
    'bradford managment school': "Bradford University",
    "Bradford Management School": "Bradford University",
    "Department of Criminology Leicester University": "Leicester University",
    "Department of Materials Science and Metallurgy, University of Cambridge": "University of Cambridge",
    "School of Geography, University of Leeds": "University of Leeds",
    (u"King"+u'\u2019'+u"s College London").encode('utf-8'): "King's College London",
    "Imperial College": "Imperial College London",
    "Liverpool John Moroes University": "Liverpool John Moores University",
    "coventy university": "Coventry University",
    "Leeds Metropolitian University": "Leeds Metropolitan University"
}

org_keywords = ['university', 'institution', 'school', 'college']

columns_added_by_cleanup = ['manual.dc.publisher[en].is_not_person_name', 'manual.organisations.add_to_publisher', 'note.dc.publisher[en]', 'note.organisations']

# Functions shared between different rules
###########################################################
def add_column_to_csv(csv_wrapper, column):
    csv_wrapper.add_column(column)
    # if column not in columns_added_by_cleanup:
        # columns_added_by_cleanup.append(column)

def strip_duplicates(values):
    norm_values, map = normalise_strings(values)
    
    new_values = []
    for value in norm_values:
        if value not in new_values:
            new_values.append(value)
            
    return denormalise_strings(new_values, map)
    
def split_by_semicolon(values):
        new_values = []
        for value in values:
            results = value.split(';')
            # strip preceding/trailing whitespace and empty elements after the split
            results = clean_list(results)
            new_values += results
        return new_values

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
    
def may_be_org(data):
    """
    Returns the given string if the given string looks like an organisation 
    name (certain keywords). 
    False otherwise.
    """
    value = data.strip().lower()
    if not value:
    # it's definitely NOT an organisation if it's only whitespace
        return False
    
    import re
    for word in org_keywords:
        if re.search('('+word+'\s|\s'+word+')', value):
            return data
    
    return False
    
def is_known_org(data):
    value = data.strip().lower()
    if not value:
    # it's definitely NOT a known organisation if it's only whitespace
        return False
    
    if value in norm_known_organisations:
        return data
    else:
        return False
        
def may_be_nonorg(data):
    if may_be_org(data) or is_known_org(data):
        return False # not a non-org
        
    return data
    
def contains_known_org(data):
    value = data.strip().lower()
    if not value:
    # it's definitely NOT a known organisation if it's only whitespace
        return False

    for o in norm_known_organisations:
        if o in value:
            return map_known_organisations[o]
        
    nonc = contains_non_canonical_org(data)
    if nonc:
        return nonc
    
    return False
    
def contained_within_known_org(data):
    """
    Check whether the given string is contained within a known organisation's name and return the known organisation which matches (first hit).
    False otherwise.
    """
    value = data.strip().lower()
    if not value:
    # it's definitely NOT a known organisation if it's only whitespace
        return False
        
    for o in norm_known_organisations:
        if value in o:
            return map_known_organisations[o]
    
    return False
    
def contains_non_canonical_org(data):
    """
    Return canonical form if so.
    """
    value = data.strip().lower()
    if not value:
    # it was only whitespace
        return False

    keys = canonical_org_forms.keys()
    
    norm_keys, map = normalise_strings(keys)
    
    for o in norm_keys:
        if o in value:
            return canonical_org_forms[map[value]]
        
    return False
        
def normalise_dates(value):
    from datetime import datetime
    # 2009-08-21T01:50:21+01:00
    # 2009-12-02T13:31:56+00:00
    # Thu, 18 Mar 2010 06:21:19 +0000
    formats = [
        "%a, %d %b %Y %H:%M:%S +0100",
        "%a, %d %b %Y %H:%M:%S +0000",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%d",
        "%B %Y",
        "%d-%m-%Y",
        "%m-%d-%Y",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%Y",
        "%Y-%m-%dT%H:%M:%S+01:00",
        "%Y-%m-%dT%H:%M:%S+00:00",
#        "%Y-%m-%dT%H:%M:%SZ%B %Y" # can't parse this format, unfortunately
    ]
    parses = []
    for format in formats:
        try:
            dt = datetime.strptime(value, format)
            parses.append(dt)
        except ValueError:
            continue
    
    if len(parses) == 0:
        # we couldn't convert the date, so remove it
        return None
    if len(parses) == 1:
        # successfully parsed the date
        return parses[0].strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        # ambiguous date format, so remove it
        return None
    
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
    
    # 1.b.ii. DiPEX (x1) -> dc.publisher[en] (as DIPEx)
    item_ids = csv_wrapper.find_in_column(working_on, 'DiPEX')
    for item_id in item_ids:
        csv_wrapper.add_value('dc.publisher[en]', item_id, 'DIPEx')
        csv_wrapper.delete_value(working_on, item_id, 'DiPEX')
    
    # 1.b.iii. iCase bioukoer (x3) -> dc.subject[en], split by whitespace, add ukoer to subject also
    item_ids = csv_wrapper.find_in_column(working_on, 'iCase bioukoer')
    for item_id in item_ids:
        csv_wrapper.add_value('dc.subject[en]', item_id, *['iCase', 'bioukoer', 'ukoer'])
        csv_wrapper.delete_value(working_on, item_id, 'iCase bioukoer')
    
    # 1.b.iv. Rong Yang (x1) -> move to dc.contributor.author[en]
    item_ids = csv_wrapper.find_in_column(working_on, 'Rong Yang')
    for item_id in item_ids:
        csv_wrapper.add_value('dc.contributor.author[en]', item_id, 'Rong Yang')
        csv_wrapper.delete_value(working_on, item_id, 'Rong Yang')
        
    # 1.b.v. UCLAN (x1) -> delete value, add uclanoer to dc.subject[en]
    item_ids = csv_wrapper.find_in_column(working_on, 'UCLAN')
    for item_id in item_ids:
        csv_wrapper.add_value('dc.subject[en]', item_id, 'uclanoer')
        csv_wrapper.delete_value(working_on, item_id, 'UCLAN')
    
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

# 2.f. split dc.contributor.author[en] values by semicolon
def rule2f_author(csv_wrapper):
    csv_wrapper.apply_cell_function('dc.contributor.author[en]', split_by_semicolon)
    
# 2.g. if value == 'contributor', delete it (only Author columns)
# dc.contributor.author[en] should be the only Author column left at this point
def rule2g_author(csv_wrapper):
    item_ids = csv_wrapper.find_in_column('dc.contributor.author[en]', 'contributor')
    for item_id in item_ids:
        csv_wrapper.delete_value('dc.contributor.author[en]', item_id, 'contributor')

# 2.h. if value is a VCARD, get the name and leave only the name
def rule2h_author(csv_wrapper):
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
    csv_wrapper.apply_cell_function('dc.creator', split_by_semicolon)
    
# 3.c. merge dc.creator into dc.contributor.author[en], effectively 
# eliminating the Creator column group
def rule3c_creator(csv_wrapper):
    csv_wrapper.merge_columns('dc.creator', 'dc.contributor.author[en]')
    
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
    
# 4.d. merge dc.contributor[en] into dc.contributor.author[en]
def rule4d_contributor(csv_wrapper):
    csv_wrapper.merge_columns('dc.contributor[en]', 'dc.contributor.author[en]')
    
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
        stripchars.append(u'\u2019'.encode('utf-8')) 
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
        
        for value in values:
            results = []
            results = value.split(',')
            for result in results:
                results2 = []
                results2 = result.split(';')
                if len(results2) > 1:
                    new_values += clean_list(results2)
                else:
                    new_values.append(result.strip())
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

# 7.a. reformat the content of dc.date[] and dc.date.created into a timestamp where possible
def rule7a_date(csv_wrapper):
    csv_wrapper.apply_value_function("dc.date", normalise_dates)
    csv_wrapper.apply_value_function("dc.date[]", normalise_dates)
    csv_wrapper.apply_value_function("dc.date.created", normalise_dates)

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
    csv_wrapper.apply_value_function("dc.date.issued", normalise_dates)

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

# 8.a. delete dc.description.uri[en]
def rule8a_description(csv_wrapper):
    csv_wrapper.delete_column("dc.description.uri[en]")

# 8.b. migrate dc.description[] and dc.description[en-gb] to dc.description[en]
def rule8b_description(csv_wrapper):
    csv_wrapper.merge_columns("dc.description[]", "dc.description[en]")
    csv_wrapper.merge_columns("dc.description[en-gb]", "dc.description[en]")

# 9. Format columns
############################################################

# 9.a. Merge dc.format[] into dc.format
def rule9a_format(csv_wrapper):
    csv_wrapper.merge_columns("dc.format[]", "dc.format")

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

# 11. Title columns
#############################################################

# 11.a. merge dc.title[*] to dc.title[en]
def rule11a_title(csv_wrapper):
    csv_wrapper.merge_columns("dc.title[*]", "dc.title[en]")
    csv_wrapper.merge_columns("dc.title[]", "dc.title[en]")
    csv_wrapper.merge_columns("dc.title[en-US]", "dc.title[en]")
    csv_wrapper.merge_columns("dc.title[en-gb]", "dc.title[en]")
    
# 12. Identifier columns:
############################################################

# 12.a. merge dc.identifier.uri, dc.identifier.uri[] into dc.identifier.uri[en]
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
    matches = csv_wrapper.find_by_value_function_map('dc.publisher[en]', may_be_nonorg)
    
    add_column_to_csv(csv_wrapper,"note.dc.publisher[en]")
    add_column_to_csv(csv_wrapper,"manual.dc.publisher[en].is_not_person_name")
    
    for id, values in matches.items():
        for value in values:
            if not csv_wrapper.cell_contains('dc.contributor.author[en]', id, value):
                if not csv_wrapper.cell_contains("note.dc.publisher[en]", id, value):
                    csv_wrapper.add_value("note.dc.publisher[en]", id, value)

# 14. LOM columns:
##############################################################

# 14.a. extract any orgs from lom.vcard and place into dc.publisher[en]
# 14.b. delete lom.vcard
def rule14a_lom(csv_wrapper):
    def extract_org(value):
        """ BEGIN:vcard FN:J. Koenig ORG:University of Cambridge END:vcard """
        norm_value = ' '.join(value.splitlines())
        
        look_for_label = 'ORG:'
        
        start = norm_value.find(look_for_label)
        # in example: start == 25
        if start < 0:
            return None
        
        afterorg = norm_value[start + len(look_for_label):]
        # in example: afterorg == 'University of Cambridge END:vcard'
        
        next_label_end = afterorg.find(":")
        # in example: next_label_end == 27
        if next_label_end < 0:
            return None
        
        interim = afterorg[:next_label_end]
        # in example: interim == 'University of Cambridge END'
        
        end_of_ORG_value = interim.rfind(' ')
        # in example: end_of_ORG_value == 23
        if end_of_ORG_value < 0:
            return None
        
        org = afterorg[:end_of_ORG_value].strip()
        # in example: org == 'University of Cambridge'
        
        return org
        
    csv_wrapper.apply_value_function('lom.vcard', extract_org)
    csv_wrapper.merge_columns('lom.vcard', 'dc.publisher[en]')
    
# 15. Merge results of manual work into main dataset
###########################################################

# 15.a. Rule 13.b. detects potential person names in dc.publisher[en]
# helpman.py is then used to produce a slice of the dataset for human review.
# If a certain dc.publisher[en] suspicious value should NOT be copied over to 
# dc.contributor.author[en], this is noted by populating the item's
# manual.dc.publisher[en].is_not_person_name field (value is "y" by convention
# but any value in this field will do).
def rule15a_mergemanual(csv_wrapper):
    if csv_wrapper.csv_dict.has_key('manual.dc.publisher[en].is_not_person_name'):
        merge_ids = csv_wrapper.filter_rows('manual.dc.publisher[en].is_not_person_name', should_be_empty=True)
        csv_wrapper.c2c_copy_cells('note.dc.publisher[en]', 'dc.contributor.author[en]', merge_ids)
    
# 15.b. Rule 16.e. detects potential organisation names in 
# dc.contributor.author[en] and dc.subject[en] . helpman.py is then used to 
# produce a slice for human review. When the main cleanup.py module is run 
# again, all values in manual.organisations.add_to_publisher will be added to 
# the corresponding dc.publisher[en].
def rule15b_mergemanual(csv_wrapper):
    if csv_wrapper.csv_dict.has_key('manual.organisations.add_to_publisher'):
        merge_ids = csv_wrapper.filter_rows('manual.organisations.add_to_publisher', should_be_empty=False)
        csv_wrapper.c2c_copy_cells('manual.organisations.add_to_publisher', 'dc.publisher[en]', merge_ids)
            
# 16. General tidying
###########################################################

# 16.a. detect and delete all e-mail addresses
def rule16a_general(csv_wrapper):
    csv_wrapper.apply_global_cell_function(strip_email)

# 16.b. delete the contents of all fields where the only value in the field is 
# "||", the multiple value separator
# NOTE: this rule doesn't actually need to be implemented, as the general deduplication
# task will deal with it

# 16.c. for all fields with multiple values, de-duplicate repeated values
# this rule should cover both of these ...
def rule16c_general(csv_wrapper):
    csv_wrapper.apply_global_cell_function(strip_duplicates)

# 16.d. Copy all organisation names from dc.contributor.author[en] and dc.subject[en] to dc.publisher[en] where possible.
def rule16d_general(csv_wrapper):
    csv_wrapper.c2c_apply_value_function('dc.contributor.author[en]', 'dc.publisher[en]', contains_known_org)
    csv_wrapper.c2c_apply_value_function('dc.subject[en]', 'dc.publisher[en]', contains_known_org)
    
# 16.e. auto-detect and flag instances of "university", "institution", 
# "school", "college" etc, and report on the rows where these occur, for possible 
# manual intervention
def rule16e_general(csv_wrapper):
    # dc.contributor.author[en]
    # dc.subject[en]
    
    def review_if_not_already_in_target(target, matches):
        # for all items where the source fields tripped the org. name detection
        for id, values in matches.items():
        
            # for each value which might be an org. name
            # e.g. "Emanuil Tolev (University of Manchester)"
            for value in values:
                norm_val = value.strip().lower()
                
                # check whether the target field doesn't already have this suspicious string
                if not csv_wrapper.cell_contains(target, id, value):
                    # no, the target field doesn't have this exact string as a stand-alone value
                    
                    # e.g.: rules 2.i. and 5.g. would have detected and placed "University of Manchester" in the target field, but not "Emanuil Tolev (University of Manchester)"
                
                    # check if this value (which tripped the org. name detection)
                    # contains a known organisation
                    known_org = contains_known_org(value)
                    # e.g. "University of Manchester"
                    if known_org:
                        # it does - so check whether the target field contains this known organisation
                        # it did not have the exact value we're looking for, but rules 2.i. and 5.g. might have copied *just* the organisation name
                        if not csv_wrapper.cell_contains(target, id, known_org):
                            # finally, if it's completely unknown, add it to the notes
                            csv_wrapper.add_value("note.organisations", id, value)
                    else:
                        # no known organisation present in suspicious value
                        
                        # there are certain values we ignore if the target field contains a certain organisation name
                        # e.g. we ignore "university of wales" if the target field already has "University of Wales, Newport"
                        if ignore_if_org_present.has_key(norm_val):
                            if not csv_wrapper.cell_contains(target, id, ignore_if_org_present[norm_val]):
                                csv_wrapper.add_value("note.organisations", id, value)
                        
                        else:
                            csv_wrapper.add_value("note.organisations", id, value)

    add_column_to_csv(csv_wrapper,"note.organisations")
    add_column_to_csv(csv_wrapper,'manual.organisations.add_to_publisher')
    
    matches1 = csv_wrapper.find_by_value_function_map("dc.contributor.author[en]", may_be_org)
    matches2 = csv_wrapper.find_by_value_function_map("dc.subject[en]", may_be_org)
    
    review_if_not_already_in_target('dc.publisher[en]', matches1)
    review_if_not_already_in_target('dc.publisher[en]', matches2)

# 16.f. delete intermediary columns which were used for metadata enhancement
def rule16f_general(csv_wrapper):
    for col in columns_added_by_cleanup:
        csv_wrapper.delete_column(col)