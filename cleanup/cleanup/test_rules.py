import unittest
import rules, csvwrapper
from copy import deepcopy

# 1 : [""], 2: [""], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']
data = {
    'dc.contributor.advisor[]': {1 : ["advisor1"], 2: ["advisor2"], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    'dc.contributor.advisor[en]': {1 : [""], 2 : ["advisor3"], 3: ['conadv'], 4: ['DiPEX'], 
                                    5: ['iCase bioukoer'], 6: ['Rong Yang'], 7: ['UCLAN']},
    "dc.subject[en]" : {1 : [""], 2: [""], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    "dc.contributor.author[en]" : {1 : [""], 2: [""], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    
    'dc.contributor.author[]' : {1 : ["author1"], 2: [""], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    'dc.contributor.author' : {1 : [""], 2: [""], 3: ['author3'], 4: [''], 5: [''], 6: [''], 7: ['']},
    'dc.contributor.author[x-none]' : {1 : [""], 2: ["author2"], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    'dc.contributor.author[en]' : {1 : [""], 2: [""], 3: [''], 4: ['contributor'], 5: ['Mark Foss ORG:University of Nottingham EMAIL:foss@nottingham.ac.uk END:vcard'], 6: [''], 7: ['']},
    'dc.contributor.author[English]' : {1 : [""], 2: [""], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    'dc.contributor.author[en-gb]' : {1 : ["publisher1"], 2: [""], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    'dc.publisher[en]' : {1 : [""], 2: [""], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']}
}

wrapper = csvwrapper.CSVWrapper()
wrapper.csv_dict = data
wrapper.populate_ids()

class TestRules(unittest.TestCase):
    def test_1a_advisor(self):
        w = deepcopy(wrapper)
        
        rules.rule1a_advisor(w)
        
        assert not w.csv_dict.has_key('dc.contributor.advisor[]')
        assert len(w.csv_dict['dc.contributor.advisor[en]'][1]) == 1
        assert "advisor1" in w.csv_dict['dc.contributor.advisor[en]'][1]
        assert len(w.csv_dict['dc.contributor.advisor[en]'][2]) == 2
        assert "advisor2" in w.csv_dict['dc.contributor.advisor[en]'][2]
        assert "advisor3" in w.csv_dict['dc.contributor.advisor[en]'][2]
        
    def test_1b_advisor(self):
        w = deepcopy(wrapper)
        
        rules.rule1b_advisor(w)
        
        # 'conadv' -> delete the row
        assert 3 not in w.ids
        
        # 'DiPEX' -> move to dc.publisher as DIPEx
        assert "DIPEx" in w.csv_dict['dc.publisher[en]'][4]
        assert w.csv_dict['dc.contributor.advisor[en]'][4][0] == ""
        
        # 'iCase bioukoer' -> delete value and add 'iCase', 'bioukoer', 'ukoer' to dc.subject[en]
        assert "iCase" in w.csv_dict['dc.subject[en]'][5]
        assert "bioukoer" in w.csv_dict['dc.subject[en]'][5]
        assert "ukoer" in w.csv_dict['dc.subject[en]'][5]
        assert w.csv_dict['dc.contributor.advisor[en]'][5][0] == ""
        
        # 'Rong Yang' -> move to 'dc.contributor.author[en]'
        assert w.csv_dict['dc.contributor.advisor[en]'][6][0] == ""
        assert "Rong Yang" in w.csv_dict['dc.contributor.author[en]'][6]
        
        # UCLAN -> delete value and add uclanoer to dc.subject[en]
        assert w.csv_dict['dc.contributor.advisor[en]'][7][0] == ""
        assert "uclanoer" in w.csv_dict['dc.subject[en]'][7]
        
    def test_1c_advisor(self):
        w = deepcopy(wrapper)
        
        rules.rule1c_advisor(w)
        
        assert not w.csv_dict.has_key("dc.contributor.advisor[en]")
    
    def test_2a_author(self):
        w = deepcopy(wrapper)
        
        rules.rule2a_author(w)
        
        assert "author1" in w.csv_dict['dc.contributor.author[en]'][1]
        assert not w.csv_dict.has_key('dc.contributor.author[]')
    
    def test_2b_author(self):
        w = deepcopy(wrapper)
        
        rules.rule2b_author(w)
        
        assert "author2" in w.csv_dict['dc.contributor.author[en]'][2]
        assert not w.csv_dict.has_key('dc.contributor.author[x-none]')
        
    def test_2c_author(self):
        w = deepcopy(wrapper)
        
        rules.rule2c_author(w)
        
        assert "author3" in w.csv_dict['dc.contributor.author[en]'][3]
        assert not w.csv_dict.has_key('dc.contributor.author')
    
    def test_2d_author(self):
        w = deepcopy(wrapper)
        
        rules.rule2d_author(w)
        
        assert not w.csv_dict.has_key('dc.contributor.author[English]')
    
    def test_2e_author(self):
        w = deepcopy(wrapper)
        
        rules.rule2e_author(w)
        
        assert "publisher1" in w.csv_dict['dc.publisher[en]'][1]
        assert not w.csv_dict.has_key('dc.contributor.author[en-gb]')
    
    def test_2f_author(self):
        w = deepcopy(wrapper)
        
        rules.rule2f_author(w)
        
        assert w.csv_dict['dc.contributor.author[en]'][4][0] == ""
     
    def test_2g_author(self):
        w = deepcopy(wrapper)
        
        rules.rule2g_author(w)
        
        assert w.csv_dict['dc.contributor.author[en]'][5][0] == "Mark Foss"