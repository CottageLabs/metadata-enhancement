import csvwrapper, sys
from copy import deepcopy

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
    config_params = config.split(":")
    pivot = config_params[0]
    file = config_params[1]
    overwrite = False
    if len(config_params) == 3 and config_params[2] == 'overwrite':
        overwrite = True
    
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
            target_ids = target.find_in_column(pivot, values[0]) # there is only one value in the source table
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
                # if there are repeated ids in the target, then this is indicative of multiple
                # values to be entered into the same column (note that this does not de-duplicate)
                if column.has_key(t):
                    column[t] += deepcopy(d[id])
                else:
                    column[t] = deepcopy(d[id])
        columns[key] = column
    print "    done"
    print "    (skipped " + str(len(skips)) + " ids)"
    print
    
    for name, column in columns.iteritems():
        if name == "id" or name == pivot:
            continue
        print "    stitching column " + name
        if overwrite:
            print '    Overwriting existing column contents.'
            target.incorporate_column(name, column, overwrite=True)
        else:
            target.incorporate_column(name, column)
        print "    done"
        print

print "Saving to " + out_file + " ..."
target.save(out_file)
print "done"