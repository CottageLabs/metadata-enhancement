"""
A set of rules implemented over the CSVWrapper which manage the
metadata cleanup tasks
"""
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
        csv_wrapper.add_value('dc.publisher', item_id, 'DIPEx')
        csv_wrapper.delete_contents(working_on, item_id)
    
    # 1.b.iii. iCase bioukoer (x3) -> dc.subject, split by whitespace, add ukoer to subject also
    item_ids = csv_wrapper.find_in_column(working_on, 'iCase bioukoer')
    for item_id in item_ids:
        csv_wrapper.add_value('dc.subject[en]', item_id, ['iCase', 'bioukoer', 'ukoer'])
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

# 2.a. merge dc.contributor.author[] into dc.contributor.author
def rule2a_author(csv_wrapper):
    csv_wrapper.merge_columns('dc.contributor.author[]', 'dc.contributor.author')

# 2.b. merge dc.contributor.author[x-none] into dc.contributor.author
def rule2b_author(csv_wrapper):
    csv_wrapper.merge_columns('dc.contributor.author[x-none]', 'dc.contributor.author')

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
    item_ids = csv_wrapper.find_in_column('dc.contributor.author[en]', 'vcard', partial = True)
    for item_id in item_ids:
        contents = csv_wrapper.get_contents('dc.contributor.author[en]', item_id)
        new_contents = []
        for value in contents:
            if 'vcard' in value:
                # The example of a VCARD that we have starts with the name
                # and continues with the ORG (ORGanisation) field. So finding 
                # where the ORG field starts gives us the end of the name 
                # (we have to get the character *before* the ORG field, so -1).
                end_of_name = value.find('ORG') - 1
                # Get only the name (ignoring the space character after it 
                # and the rest of the VCARD info).
                new_contents.append(value[:end_of_name])
            else:
                new_contents.append(value)
        csv_wrapper.set_contents('dc.contributor.author[en]', item_id, new_contents)

# 3. Creator column group
###########################################################

# 3.a. merge dc.creator[] into dc.creator
def rule3a_creator(csv_wrapper):
    csv_wrapper.merge_columns('dc.creator[]', 'dc.creator')
        
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
        return [oldest]
        
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
