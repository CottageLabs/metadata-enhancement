import csv, sys

in_file = sys.argv[1]
out_file = sys.argv[2]

reader = csv.reader(open(in_file))

wrs = {}
for row in reader:
    if row[0] == "item_id":
        continue
    if not row[0] in wrs.keys():
        wrs[row[0]] = [row[1]]
    else:
        wrs[row[0]].append(row[1])

writer = csv.writer(open(out_file, "wb"))
writer.writerow(['id', 'dc.relation', 'dc.relation.uri'])
for id, urls in wrs.iteritems():
    norm_urls = []
    for t in urls:
        if t not in norm_urls:
            norm_urls.append(t)
    writer.writerow([id, "WEB_LINK" ,"||".join(norm_urls)])
    