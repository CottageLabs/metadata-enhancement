import csvwrapper, sys

files = []
for i in range(1, len(sys.argv)):
    files.append(sys.argv[i])
target_file = files[0]
out_file = files[-1]
files.remove(target_file)
files.remove(out_file)

print "CONFIG: main data source: " + target_file
print "CONFIG: output file :" + out_file
print

print "loading main data source ..."
target = csvwrapper.CSVWrapper(target_file)
print "done"

for config in files:
    pivot, file = config.split(":")
    
    print "Stitching file " + file + " on pivot: " + pivot
    
    print "    loading stitch file ..."
    source = csvwrapper.CSVWrapper(file)
    source_pivot = source.csv_dict[pivot]
    print "    done"
    print
    
    targets = {}
    if pivot == "id":
        for id in target.ids:
            targets[id] = [id]
    else:
        print "    pivot is not 'id' so building pivot table ..."
        for id, values in source_pivot.iteritems():
            target_ids = target.find_in_column(pivot, values[0])
            targets[id] = target_ids
        print "    done"
        print
    
    print "    expanding stitch data on pivot ..."
    skips = []
    columns = {}
    for key, d in source.csv_dict.iteritems():
        column = {}
        for id in d.keys():
            if not targets.has_key(id):
                # print "        skipping incoming id " + str(id)
                if id not in skips: skips.append(id)
            for t in targets.get(id, []):
                column[t] = d[id]
        columns[key] = column
    print "    done"
    print "    (skipped " + str(len(skips)) + " ids)"
    print
    
    for name, column in columns.iteritems():
        if name == "id" or name == pivot:
            continue
        print "    stitching column " + name
        target.incorporate_column(name, column)
        print "    done"
        print

print "Saving to " + out_file + " ..."
target.save(out_file)
print "done"