def detect_overlapping_strings(list):
    d = {}
    list2 = list[:]
    for i in list:
        for i2 in list2:
                if i in i2:
                        if d.has_key(i):
                                print i, ':: contained within ::', i2
                        d[i] = True
                        
def output_list(list, outpath):
    with open(outpath, 'wb') as out:
        out.write('["')
        out.write('", "'.join(list))
        out.write('"]')
        
def get_rules():
    """
    Get a list of the current rules (function objects, so - callable).
    """
    import types, string
    import rules
    
    runrules = []
    for rule_no in range(1,100):
        for letter in string.ascii_lowercase:
            for a in dir(rules):
                if a.startswith('rule' + str(rule_no) + letter) and isinstance(rules.__dict__.get(a), types.FunctionType):
                    
                    runrules.append(rules.__dict__.get(a))
    return runrules