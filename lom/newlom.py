import sys, glob, csv
from lxml import etree

namespaces = {
    'top': 'http://www.imsglobal.org/xsd/imscp_v1p1',
    'imsd': 'http://www.imsglobal.org/xsd/imsmd_v1p2',
    'imsmd': 'http://www.imsglobal.org/xsd/imsmd_v1p2'
}

xpaths = {
#    'general.coverage' : '/top:manifest/top:metadata/imsd:lom/imsd:general/imsd:coverage/imsd:langstring',
#    'lifecycle.version' : '/top:manifest/top:metadata/imsd:lom/imsd:lifecycle/imsd:version/imsd:langstring',
    'lom.vcard' : '/top:manifest/top:metadata/imsd:lom/imsd:lifecycle/imsd:contribute/imsd:centity/imsd:vcard',
    'date.created' : '/top:manifest/top:metadata/imsd:lom/imsd:lifecycle/imsd:contribute/imsd:date/imsd:datetime',
#    'lifecycle.contribute.role' : '/top:manifest/top:metadata/imsd:lom/imsd:lifecycle/imsd:contribute/imsd:role/imsd:value/imsd:langstring',
    'lom.educational.learningresourcetype' : '/top:manifest/top:metadata/imsd:lom/imsd:educational/imsd:learningresourcetype/imsd:value/imsd:langstring',
    'lom.educational.intendedenduserrole' : '/top:manifest/top:metadata/imsd:lom/imsd:educational/imsd:intendedenduserrole/imsd:value/imsd:langstring',
    'lom.educational.context' : '/top:manifest/top:metadata/imsd:lom/imsd:educational/imsd:context/imsd:value/imsd:langstring',
    'lom.educationa.typicallearningtime' : '/top:manifest/top:metadata/imsd:lom/imsd:educational/imsd:typicallearningtime/imsd:datetime',
    'lom.educational.description' : '/top:manifest/top:metadata/imsd:lom/imsd:educational/imsd:description/imsd:langstring',
#    'educational.language' : '/top:manifest/top:metadata/imsd:lom/imsd:educational/imsd:language',
#    'relation' : '/top:manifest/top:metadata/imsd:lom/imsd:relation/imsd:resource/imsd:description/imsd:langstring',
    'lom.classification' : '/top:manifest/top:metadata/imsd:lom/imsd:classification/imsd:taxonpath/imsd:taxon/imsd:entry/imsd:langstring',
    'lom.classification.type' : '/top:manifest/top:metadata/imsd:lom/imsd:classification/imsd:taxonpath/imsd:source/imsd:langstring',
}

def search(q, xml):
    result = try_xpath(xml, q)
    if not result:
        result = try_xpath(xml, q.replace('/imsd:', '/imsmd:'))
    return result
    
def try_xpath(lom, q):
    result = lom.xpath(q, namespaces = namespaces)
    if len(result) > 0:
        return result
    return None

def get_text_values(xpath_result):
    values = []
    if xpath_result:
        for r in xpath_result:
            values.append(r.text)
    return values

def register_field(fields, name, id, values):
    if not fields.has_key(name):
        fields[name] = {}
    if not fields[name].has_key(id):
        fields[name][id] = ['']
    if values is None or len(values) == 0:
        values = ['']
    fields[name][id] = values

def save(csv_dict, path):
    """
    Save the self.csv_dict as a csv file to the supplied file path
    """
    with open(path, "wb") as f:
        writer = csv.writer(f)
        
        # first, the headers
        header_index_map = {}
        header_row = []
        
        keys = csv_dict.keys()
        keys.sort() 
        keys = keys
        
        i = 0
        for header in keys:
            header_row.append(header)
            header_index_map[header] = i
            i += 1
        writer.writerow(['id'] + header_row)
        
        # now, each item id
        ids = csv_dict[keys[1]].keys()
        ids.sort()
        for id in ids:
            item_row = [id] + [None] * len(csv_dict.keys())
            for header, i in header_index_map.iteritems():
                i += 1
                v = [c for c in csv_dict[header][id] if c is not None]
                item_row[i] = "||".join(v)
                if item_row[i] is not None:
                    item_row[i] = item_row[i].encode('ascii', 'ignore')
            writer.writerow(item_row)

if len(sys.argv) > 2:
    loms_dir = sys.argv[1]
    out = sys.argv[2]

lomfnames = glob.glob(loms_dir + '*.xml')

interesting_fields = {}
for fname in lomfnames:
    id = int(fname[fname.rfind('/') + 1 : fname.rfind('.')])
    xml = etree.parse(fname)
    for name, xpath in xpaths.iteritems():
        result = search(xpath, xml)
        register_field(interesting_fields, name, id, get_text_values(result))

save(interesting_fields, out)
    
    
