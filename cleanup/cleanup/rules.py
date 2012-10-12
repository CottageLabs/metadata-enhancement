"""
A set of rules implemented over the CSVWrapper which manage the
metadata cleanup tasks
"""


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
