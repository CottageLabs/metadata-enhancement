import csv, copy
import lommer

print 'Processing LOM-s into a CSV with the most interesting stuff...'


interesting_data = {}
interesting_data['general.coverage'] = dict.fromkeys(lommer.loms.keys())
not_found_counts = {}

found = {}
found['general.coverage'], not_found_counts['general.coverage'] = lommer.search('/top:manifest/top:metadata/imsd:lom/imsd:general/imsd:coverage/imsd:langstring')

for id, elems in found['general.coverage'].iteritems():
    # normalise spacing incl. newlines
    if elems[0].text:
        filtered_text = ' '.join(elems[0].text.split())
    else:
        filtered_text = ''
    interesting_data['general.coverage'][id] = filtered_text


csvdata = []
csvheaders = ['id', 'general.coverage']
csvdata.append(csvheaders)

    
for id, value in iter(sorted(interesting_data['general.coverage'].iteritems())):
    csvrow = [id, value]
    csvdata.append(copy.deepcopy(csvrow))
    

where_to = raw_input('Where would you like to save the resulting CSV?: ')

with open(where_to, 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(csvdata)
