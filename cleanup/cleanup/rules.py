"""
A set of rules implemented over the CSVWrapper which manage the
metadata cleanup tasks
"""
# 1. Advisor columns
###########################################################
def rule1a_advisor(csv_wrapper):
    csv_wrapper.merge_columns('dc.contributor.advisor[]', 'dc.contributor.advisor[en]')

def rule1b_advisor(csv_wrapper):
    working_on = 'dc.contributor.advisor[en]' # column we're working on
    
    # i
    item_ids = csv_wrapper.find_in_column(working_on, 'conadv')
    for item_id in item_ids:
        csv_wrapper.delete_record(item_id)
    
    # ii
    item_ids = csv_wrapper.find_in_column(working_on, 'DiPEX')
    for item_id in item_ids:
        csv_wrapper.set_value('dc.publisher', item_id, 'DIPEx')
        csv_wrapper.delete_value(working_on, item_id)
    
    # iii
    item_ids = csv_wrapper.find_in_column(working_on, 'iCase bioukoer')
    for item_id in item_ids:
        csv_wrapper.set_value('dc.subject[en]', item_id, ['iCase', 'bioukoer', 'ukoer'])
        csv_wrapper.delete_value(working_on, item_id)
    
    # iv
    item_ids = csv_wrapper.find_in_column(working_on, 'Rong Yang')
    for item_id in item_ids:
        csv_wrapper.set_value('dc.contributor.author[en]', item_id, 'Rong Yang')
        csv_wrapper.delete_value(working_on, item_id)
        
    # v
    item_ids = csv_wrapper.find_in_column(working_on, 'UCLAN')
    for item_id in item_ids:
        csv_wrapper.set_value('dc.subject[en]', item_id, 'uclanoer')
        csv_wrapper.delete_value(working_on, item_id)
        
    # vi
    item_ids = csv_wrapper.find_in_column(working_on, '||')
    for item_id in item_ids:
        csv_wrapper.delete_record(item_id)
    
def rule1c_advisor(csv_wrapper):
    csv_wrapper.delete_column('dc.contributor.advisor[en]')
    
# Date columns
###########################################################

# 7.a. reformat the content of dc.date[] into a timestamp
def rule7a_date(csv_wrapper):
    # from form: Tue, 16 Jun 2009 11:34:02 +0100
    # to form: 2010-11-10T10:09:17Z
    def date_converter(data):
        from datetime import datetime
        dt = datetime.strptime(d, "%a, %d %b %Y %H:%M:%S +0100")
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    csv_wrapper.apply_value_function("dc.date[]", date_converter)

# 7.b. merge dc.date[] into dc.date
# 7.c. merge dc.date.accessioned[*] into dc.date.accessioned
# 7.d. merge dc.date.issued[en] into to dc.date.issued
# 7.e. ensure that all dc.date.* fields have only one value; propose to keep the oldest value, where there is more than one
# 7.f. Delete dc.date.created[en] column
