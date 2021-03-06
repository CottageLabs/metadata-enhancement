import unittest
import csvwrapper
from copy import deepcopy

data = {
    "dc.description" : {1: ["desc1"], 2: ["desc2"], 3: ["desc3", "desc4"], 4: ['']},
    "dc.title" : {1: ["title1"], 2: ["desc1"], 3: ["title3", "title4"], 4 : ["findme", "title5", "copymetoo"]},
    "dc.identifier" : {1: ["id1"], 2: ["id2"], 3: ["id3", "desc1"], 4 : ['']},
    "dc.source" : {1: ["findme"], 2: [""], 3 : [""], 4 : ["copymetoo"]},
    "dc.description[en]" : {1: ["desc1"], 2: ["other"], 3: ["desc3", "desc5"], 4: ["desc6"]}
}

wrapper = csvwrapper.CSVWrapper()
wrapper.csv_dict = data
wrapper.populate_ids()

class TestCsvWrapper(unittest.TestCase):

    def test_01_apply_value_function(self):
        w = deepcopy(wrapper)
        
        def vf(value):
            if value == "desc1":
                return "updated"
            return value
        w.apply_value_function("dc.description", vf)
        
        assert w.csv_dict["dc.description"][1][0] == "updated"
        assert w.csv_dict["dc.description"][2][0] == "desc2"
        
    def test_02_apply_global_value_function(self):
        w = deepcopy(wrapper)
        
        def vf(value):
            if value == "desc1":
                return "updated"
            return value
        
        w.apply_global_value_function(vf)
        
        assert w.csv_dict["dc.description"][1][0] == "updated"
        assert w.csv_dict["dc.title"][2][0] == "updated"
        assert w.csv_dict["dc.identifier"][3][1] == "updated"
        
    def test_03_apply_cell_function(self):
        w = deepcopy(wrapper)
        
        def cf(values):
            if len(values) == 2:
                return [values[0] + values[1]]
            return values
        
        w.apply_cell_function("dc.description", cf)
        
        assert len(w.csv_dict["dc.description"][3]) == 1
        assert w.csv_dict["dc.description"][3][0] == "desc3desc4"
        
    def test_04_find_by_value_function(self):
        w = deepcopy(wrapper)
        
        def vf(value):
            if value == "findme":
                return True
            return False
        
        ids1 = w.find_by_value_function("dc.description", vf)
        ids2 = w.find_by_value_function("dc.title", vf)
        ids3 = w.find_by_value_function("dc.source", vf)
        
        assert len(ids1) == 0
        assert len(ids2) == 1
        assert len(ids3) == 1
        assert ids2[0] == 4
        assert ids3[0] == 1
        
    def test_05_delete_column(self):
        w = deepcopy(wrapper)
        
        assert w.csv_dict.has_key("dc.identifier")
        w.delete_column("dc.identifier")
        assert not w.csv_dict.has_key("dc.identifier")
    
    def test_06_add_column(self):
        w = deepcopy(wrapper)
        
        assert not w.csv_dict.has_key("dc.contributor")
        w.add_column("dc.contributor")
        assert w.csv_dict.has_key("dc.contributor")
        assert w.csv_dict["dc.contributor"].has_key(4)
        
    def test_07_delete_record(self):
        w = deepcopy(wrapper)
        
        assert w.csv_dict["dc.description"].has_key(1)
        w.delete_record(1)
        assert not w.csv_dict["dc.description"].has_key(1)
        assert not w.csv_dict["dc.title"].has_key(1)
        assert not w.csv_dict["dc.identifier"].has_key(1)
        assert not w.csv_dict["dc.source"].has_key(1)
        assert 1 not in w.ids
        
    def test_08_find_in_column(self):
        w = deepcopy(wrapper)
        
        ids = w.find_in_column("dc.description", "desc4")
        assert len(ids) == 1
        assert ids[0] == 3
        
        ids = w.find_in_column("dc.title", "title", True)
        assert len(ids) == 3, ids
        assert 1 in ids
        assert 3 in ids
        assert 4 in ids
        
    def test_09_merge_columns(self):
        w = deepcopy(wrapper)
        
        w.merge_columns("dc.description", "dc.description[en]")
        
        assert not w.csv_dict.has_key("dc.description")
        
        assert len(w.csv_dict["dc.description[en]"][1]) == 1
        assert "desc1" in w.csv_dict["dc.description[en]"][1]
        
        assert len(w.csv_dict["dc.description[en]"][2]) == 2
        assert "desc2" in w.csv_dict["dc.description[en]"][2]
        assert "other" in w.csv_dict["dc.description[en]"][2]
        
        assert len(w.csv_dict["dc.description[en]"][3]) == 3
        assert "desc3" in w.csv_dict["dc.description[en]"][3]
        assert "desc4" in w.csv_dict["dc.description[en]"][3]
        assert "desc5" in w.csv_dict["dc.description[en]"][3]
        
        assert len(w.csv_dict["dc.description[en]"][4]) == 1
        assert "desc6" in w.csv_dict["dc.description[en]"][4]
        
    def test_10_add_value(self):
        w = deepcopy(wrapper)
        
        w.add_value("dc.title", 1, "titleA")
        
        assert len(w.csv_dict["dc.title"][1]) == 2
        assert "titleA" in w.csv_dict["dc.title"][1]
        
        w.add_value("dc.identifier", 2, "idA", "idB")
        
        assert len(w.csv_dict["dc.identifier"][2]) == 3
        assert "idA" in w.csv_dict["dc.identifier"][2]
        assert "idB" in w.csv_dict["dc.identifier"][2]
    
    def test_11_delete_contents(self):
        w = deepcopy(wrapper)
        
        assert "findme" in w.csv_dict["dc.source"][1]
        w.delete_contents("dc.source", 1)
        assert "findme" not in w.csv_dict["dc.source"][1]
        assert len(w.csv_dict["dc.source"][1]) == 1
        
    def test_12_set_value(self):
        w = deepcopy(wrapper)
        
        w.set_value("dc.description", [1, 4], "newvalue")
        
        assert len(w.csv_dict["dc.description"][1]) == 1
        assert "newvalue" in w.csv_dict["dc.description"][1]
        
        assert len(w.csv_dict["dc.description"][4]) == 1
        assert "newvalue" in w.csv_dict["dc.description"][4]
    
    def test_13_c2c_copy_by_value_function(self):
        w = deepcopy(wrapper)
        
        def vf(value):
            if value == 'findme' or value == 'copymetoo':
                return True
            return False
        
        orig_title_4_len = len(w.csv_dict['dc.title'][4])
        
        w.c2c_copy_by_value_function('dc.source', 'dc.title', vf)
        
        # should NOT have duplicated the copymetoo entry
        assert len(w.csv_dict['dc.title'][4]) == orig_title_4_len
        # the last element in the first item in dc.title should have been 
        # copied over from dc.source - findme
        assert w.csv_dict['dc.title'][1][-1] == 'findme'
        
    def test_14_delete_value(self):
        w = deepcopy(wrapper)
        
        desc_3_len = len(w.csv_dict['dc.description'][3])
        
        w.delete_value('dc.description', 3, 'desc3')
        
        assert len(w.csv_dict['dc.description'][3]) == desc_3_len - 1
        assert 'desc3' not in w.csv_dict['dc.description'][3]

    def test_15_apply_global_cell_function(self):
        w = deepcopy(wrapper)
        
        def vf(values):
            return values + ['ADDEDBYTEST']
        
        w.apply_global_cell_function(vf)
        
        for column in w.csv_dict.keys():
            for id in w.csv_dict[column].keys():
                assert w.csv_dict[column][id][-1] == 'ADDEDBYTEST'

    def test_16_filter_rows(self):
        w = deepcopy(wrapper)
        
        filtered_rows = w.filter_rows('dc.source', should_be_empty=False)
        assert len(filtered_rows) == 2
        assert 1 in filtered_rows
        assert 4 in filtered_rows
        
    def test_17_filter_rows2(self):
        w = deepcopy(wrapper)
        
        filtered_rows = w.filter_rows('dc.source', should_be_empty=True)
        assert len(filtered_rows) == 2
        assert 2 in filtered_rows
        assert 3 in filtered_rows
        
    def test_18_cell_contains(self):
        w = deepcopy(wrapper)
        
        assert w.cell_contains('dc.title', 1, 'title1')
        assert w.cell_contains('dc.title', 3, 'title4')
        assert w.cell_contains('dc.title', 4, 'title5')
        assert not w.cell_contains('dc.title', 4, 'copyme')
        
    def test_19_find_by_value_function_map(self):
        w = deepcopy(wrapper)
        
        def vf(value):
            if value == "findme":
                return value
            return False
        
        matches1 = w.find_by_value_function_map("dc.description", vf)
        matches2 = w.find_by_value_function_map("dc.title", vf)
        matches3 = w.find_by_value_function_map("dc.source", vf)
        
        assert len(matches1) == 0
        assert len(matches2) == 1
        assert len(matches3) == 1
        assert matches2[4][0] == 'findme'
        assert matches3[1][0] == 'findme'
    
    def test_20_c2c_apply_value_function(self):
        w = deepcopy(wrapper)
        
        def vf(value):
            if value == "findme":
                return 'THIS_IN_DESTINATION'
            return False 
            
        w.c2c_apply_value_function('dc.source', 'dc.title', vf)
        
        # the last element in the first item in dc.title should have been 
        # changed, corresponding to the last element of dc.source
        # containing the string "findme"
        assert w.csv_dict['dc.title'][1][-1] == 'THIS_IN_DESTINATION'
        
    def test_21_c2c_copy_cells(self):
        w = deepcopy(wrapper)
        
        ids = [2,3]
        
        w.c2c_copy_cells('dc.identifier', 'dc.source', ids)
        assert 'id2' in w.csv_dict['dc.source'][2]
        assert "id3", "desc1" in w.csv_dict['dc.source'][3]
        
    def test_22_filter_columns(self):
        w = deepcopy(wrapper)
        
        w.filter_columns('dc.description', 'dc.title')
        
        assert w.csv_dict.has_key('dc.description')
        assert w.csv_dict.has_key('dc.title')
        assert not w.csv_dict.has_key("dc.identifier")
        assert not w.csv_dict.has_key("dc.source")
        assert not w.csv_dict.has_key("dc.description[en]")