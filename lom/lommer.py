import sys
import glob
from lxml import etree

#if len(sys.argv) > 1:
#    loms_dir = sys.argv[1]
#    if not loms_dir:
#        print "Please supply the directory where all the LOM .xml files reside (relative UNIX-style path ending in /)"
#        exit()
#else:
#    print "Please supply the directory where all the LOM .xml files reside (relative UNIX-style path ending in /)"
#    exit()

loms_dir = raw_input("Please supply the directory where all the LOM .xml files reside (relative UNIX-style path ending in /): ")

def try_xpath(lom, q):
    result = lom.xpath(q, namespaces = namespaces)
    if len(result) > 0:
        return result
    return None

def get_text(xpath_result):
    if xpath_result:
        return xpath_result[0].text
    return None

namespaces = {
    'top': 'http://www.imsglobal.org/xsd/imscp_v1p1',
    'imsd': 'http://www.imsglobal.org/xsd/imsmd_v1p2',
    'imsmd': 'http://www.imsglobal.org/xsd/imsmd_v1p2'
}

lomfnames = glob.glob(loms_dir + '*.xml')
loms = {}

print 'Loading LOM-s ...'
for fname in lomfnames:
    id = int(fname[fname.rfind('/') + 1 : fname.rfind('.')])
    loms[id] = etree.parse(fname)
print '[Done] Loaded', len(loms), 'LOM-s. Enjoy.'
print

def search(q):
    found = {}
    not_found = []
    for id, lom in loms.iteritems():
        result = try_xpath(lom, q)
        if not result:
            result = try_xpath(lom, q.replace('/imsd:', '/imsmd:'))
    
        if result:
            found[id] = result
        else:
            not_found.append(id)

    return (found, not_found)

# found, not_found = search('//imsd:title/imsd:langstring')

# print len(not_found), ' LOM-s whose title tags we couldn\'t find'
