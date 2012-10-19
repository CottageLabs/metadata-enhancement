import csvwrapper, sys

files = []
for i in range(1, len(sys.argv)):
    files.append(sys.argv[i])
target_file = files[0]
out_file = files[-1]
files.remove(target_file)
files.remove(out_file)

target = csvwrapper.CSVWrapper(target_file)

for config in files:
    pivot, file = config.split(":")
    source = csvwrapper.CSVWrapper(file)
    source_pivot = source.csv_dict[pivot]
    
    targets = {}
    for id, values in source_pivot.iteritems():
        target_ids = target.find_in_column(pivot, values[0])
        targets[id] = target_ids
    
    columns = {}
    for key, d in source.csv_dict.iteritems():
        column = {}
        for id in d.keys():
            for t in targets[id]:
                column[t] = d[id]
        columns[key] = column
    
    for name, column in columns.iteritems():
        if name == "id" or name == pivot:
            continue
        print "incorporating " + name
        target.incorporate_column(name, column)
        print "done"
        print

target.save(out_file)