import csv, sys

in_file = sys.argv[1]
out_file = sys.argv[2]

reader = csv.reader(open(in_file))

mimes = {}
for row in reader:
    if not row[0] in mimes.keys():
        mimes[row[0]] = [row[1]]
    else:
        mimes[row[0]].append(row[1])

writer = csv.writer(open(out_file, "wb"))
writer.writerow(['id', 'dc.format'])
for id, types in mimes.iteritems():
    norm_types = []
    for t in types:
        if not t == "application/octet-stream" and t not in norm_types:
            norm_types.append(t)
    writer.writerow([id, "||".join(norm_types)])
    