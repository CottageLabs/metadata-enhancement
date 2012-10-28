import csvwrapper, os, sys

original_file = sys.argv[1]
cleaned_file = sys.argv[2]
outdir = sys.argv[3]

ROW_COUNT = 500
CMD = "./dspace metadata-import "

print "CONFIG: original DSpace export file: " + original_file
print "CONFIG: cleaned metadata file (to be imported): " + cleaned_file
print "CONFIG: output directory: " + outdir
print "CONFIG: rows per import file: " + str(ROW_COUNT)
print

print "loading original DSpace export file ..."
original = csvwrapper.CSVWrapper(original_file)
print "done"
print

print "loading cleaned metadata file ..."
cleaned = csvwrapper.CSVWrapper(cleaned_file)
print "done"
print

original_columns = original.csv_dict.keys()
cleaned_columns = cleaned.csv_dict.keys()
blanks = [c for c in original_columns if c not in cleaned_columns]

import_script = ""

start = 0
end = ROW_COUNT

count = 1
done = False
while not done:
    if end > len(cleaned.ids):
        end = len(cleaned.ids)
        done = True
    
    print "chunking " + str(start) + " to " + str(end) + " ..."
    
    ids = cleaned.ids[start:end]
    subset = cleaned.subset(ids)
    for blank in blanks:
        subset.add_column(blank)
    
    out_file = os.path.join(outdir, "import" + str(count) + ".csv")
    print "... writing to " + out_file + " ..."
    
    subset.save(out_file)
    import_script += CMD + out_file + "\n"
    
    count += 1
    start = end
    end = end + ROW_COUNT
    print "done"
    print

out_file = os.path.join(outdir, "import.sh")
print "writing import script to " + out_file + "..."
f = open(out_file, "wb")
f.write(import_script)
f.close()
print "done"
