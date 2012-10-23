import unittest
import rules, csvwrapper
from copy import deepcopy

# 1 : [""], 2: [""], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']
data = {
    'dc.contributor.advisor[]': {1 : ["advisor1"], 2: ["advisor2"], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    'dc.contributor.advisor[en]': {1 : [""], 2 : ["advisor3"], 3: ['conadv'], 4: ['DiPEX'], 5: ['iCase bioukoer'], 6: ['Rong Yang'], 7: ['UCLAN']},
                                    
    'dc.contributor.author[]' : {1 : ["author1"], 2: [""], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    'dc.contributor.author' : {1 : [""], 2: [""], 3: ['author3'], 4: [''], 5: [''], 6: [''], 7: ['']},
    'dc.contributor.author[x-none]' : {1 : [""], 2: ["author2"], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    'dc.contributor.author[en]' : {1 : ["University of Here"], 2: ["College of Hard Knocks"], 3: [''], 4: ['contributor'], 5: ['Mark Foss ORG:University of Nottingham EMAIL:foss@nottingham.ac.uk END:vcard'], 6: ['uclanoer'], 7: ['uclan']},
    'dc.contributor.author[English]' : {1 : [""], 2: [""], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    'dc.contributor.author[en-gb]' : {1 : ["publisher1"], 2: [""], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    
    'dc.publisher[en]' : {1 : [""], 2: [""], 3: ['University of Glamorgan'], 4: ['Diamond Dragon School'], 5: ['Bond, James Bond'], 6: ['Archmage College'], 7: ['']},
    'dc.publisher' : {1 : ["test"], 2: [""], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    'dc.publisher[en-gb]' : {1 : ["test", 'test2'], 2: [""], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['test.email@example.com']},
    
    'dc.creator[]' : {1 : ["creator1"], 2: [""], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    'dc.creator' : {1 : [""], 2: ["creator2; creator3"], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    
    'dc.contributor' : {1 : ["test@test.com", "bob@example.com"], 2: ["University of Somewhere"], 3: ['alice@example.com'], 4: [''], 5: [''], 6: [''], 7: ['']},
    'dc.contributor[x-none]' : {1 : ["University of Over There"], 2: [""], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    'dc.contributor.other[en]' : {1 : ["other1"], 2: [""], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    'dc.contributor[en]' : {1 : ["SHIELD"], 2: ["Cat's Paws Sanctuary", 'Splott'], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['UCLAN']},
    
    "dc.subject[en]" : {1 : [" de-normalised  spacing    here "], 2: ['"quoted"', 'unquoted'], 3: ['Upper Case'], 4: ['split; this'], 5: ['and, this', 'but not this'], 6: ['Fairy College'], 7: ['wrong separation, of keywords, evil laughter']},
    "dc.subject[EN]" : {1 : ["subject1"], 2: [""], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    "dc.subject[]" : {1 : [""], 2: ["subject2"], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    "dc.subject[en-gb]" : {1 : ["subject3"], 2: [""], 3: [''], 4: [''], 5: ['another+test_of.emails.heh@sub.domain.tld', 'normal subject'], 6: [''], 7: ['']},
    "dc.subject[ene]" : {1 : [""], 2: ["subject4"], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['dup', 'dup', 'dup', 'dup']},
    
    'dc.subject.classification[]': {1 : ["class1"], 2: [""], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    'dc.subject.classification[en]': {1 : [""], 2: [""], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    
    'dc.description.sponsorship': {1 : ["sponsor1"], 2: [""], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    'dc.description.uri[en]': {1 : [""], 2: [""], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    'dc.description[]': {1 : ["desc1"], 2: [""], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    'dc.description[en]': {1 : [""], 2: [""], 3: ['no capital letter'], 4: ['shrt'], 5: [''], 6: [''], 7: ['']},
    'dc.description[en-gb]': {1 : [""], 2: ["desc2"], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    
    'dc.coverage.temporal[en]': {1 : ["sponsor1"], 2: [""], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    'dc.coverage.spatial[en]': {1 : ["sponsor1"], 2: [""], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    
    'dc.date[]': {1 : ["Tue, 16 Jun 2009 11:34:02 +0100"], 2: ["2012-01-01T00:00:00Z", "2011-01-01T00:00:00Z"], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    'dc.date': {1 : [""], 2: ["2012-01-01T00:00:00Z", "2011-01-01T00:00:00Z"], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    'dc.date.issued[]': {1 : ["date1"], 2: ["2012-01-01T00:00:00Z", "2011-01-01T00:00:00Z"], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    'dc.date.issued': {1 : [""], 2: ["2012-01-01T00:00:00Z", "2011-01-01T00:00:00Z"], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    'dc.date.created': {1 : [""], 2: ["2012-01-01T00:00:00Z", "2011-01-01T00:00:00Z"], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    'dc.date.created[en]': {1 : [""], 2: ["2012-01-01T00:00:00Z", "2011-01-01T00:00:00Z"], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    
    'dc.language[x-none]': {1 : [""], 2: [""], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    'dc.language': {1 : ['en'], 2: [""], 3: [''], 4: [''], 5: ['bg', 'gr'], 6: [''], 7: ['']},
    'dc.language[]': {1 : ["en"], 2: ["fr"], 3: ['de'], 4: ['es', 'es', 'en'], 5: ['bg', 'gr'], 6: [''], 7: ['']},
    'dc.language[de]': {1 : ["en"], 2: ["fr"], 3: ['de'], 4: ['es', 'es', 'es', 'en'], 5: ['bg', 'gr'], 6: [''], 7: ['']},
    'dc.language[en-GB]': {1 : ["en"], 2: [""], 3: [''], 4: ['ru'], 5: ['gr'], 6: ['zh'], 7: ['']},
    'dc.language[en-gb]': {1 : [""], 2: [""], 3: [''], 4: [''], 5: ['en'], 6: [''], 7: ['']},
    'dc.language[en]': {1 : ["en"], 2: ["en"], 3: ['en'], 4: ['en'], 5: ['en'], 6: ['en'], 7: ['']},
    'dc.language[fr]': {1 : [""], 2: [""], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},

    'dc.title[en]': {1 : ["Un"], 2: [""], 3: [''], 4: [''], 5: [''], 6: ['Chwech'], 7: ['saith']},
    'dc.title[*]': {1 : [""], 2: ["Dau"], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['']},
    'dc.title[]': {1 : [""], 2: [""], 3: ['tri'], 4: [''], 5: [''], 6: [''], 7: ['']},
    'dc.title[en-US]': {1 : [""], 2: [""], 3: [''], 4: ['Pedwar'], 5: [''], 6: [''], 7: ['']},
    'dc.title[en-gb]': {1 : [""], 2: [""], 3: [''], 4: [''], 5: ['Pimp'], 6: [''], 7: ['']},

    'dc.identifier.uri': {1 : ["10.1000/182"], 2: [""], 3: ['== fun!'], 4: [''], 5: [''], 6: [''], 7: ['']},
    'dc.identifier.uri[]': {1 : ["UUID"], 2: ["without context"], 3: ['== fun!'], 4: [''], 5: [''], 6: [''], 7: ['']},
    'dc.identifier.uri[en]': {1 : [""], 2: [""], 3: [''], 4: [''], 5: [''], 6: [''], 7: ['this resource is scottish']},
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
        assert len(w.csv_dict['dc.contributor.advisor[en]'][4]) == 0
        
        # 'iCase bioukoer' -> delete value and add 'iCase', 'bioukoer', 'ukoer' to dc.subject[en]
        assert "iCase" in w.csv_dict['dc.subject[en]'][5]
        assert "bioukoer" in w.csv_dict['dc.subject[en]'][5]
        assert "ukoer" in w.csv_dict['dc.subject[en]'][5]
        assert len(w.csv_dict['dc.contributor.advisor[en]'][5]) == 0
        
        # 'Rong Yang' -> move to 'dc.contributor.author[en]'
        assert len(w.csv_dict['dc.contributor.advisor[en]'][6]) == 0
        assert "Rong Yang" in w.csv_dict['dc.contributor.author[en]'][6]
        
        # UCLAN -> delete value and add uclanoer to dc.subject[en]
        assert len(w.csv_dict['dc.contributor.advisor[en]'][7]) == 0
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
        
        assert len(w.csv_dict['dc.contributor.author[en]'][4]) == 0
     
    def test_2g_author(self):
        w = deepcopy(wrapper)
        
        rules.rule2g_author(w)
        
        assert w.csv_dict['dc.contributor.author[en]'][5][0] == "Mark Foss"
    
    def test_2h_author(self):
        w = deepcopy(wrapper)
        
        rules.rule2h_author(w)
        
        assert w.csv_dict['dc.publisher[en]'][1][0] == "University of Here"
        assert w.csv_dict['dc.contributor.author[en]'][1][0] == "University of Here"
        
        assert w.csv_dict['dc.publisher[en]'][2][0] == "College of Hard Knocks"
        assert w.csv_dict['dc.contributor.author[en]'][2][0] == "College of Hard Knocks"
    
    def test_2i_author(self):
        w = deepcopy(wrapper)
        
        rules.rule2i_author(w)
        
        assert w.csv_dict['dc.contributor.author[en]'][6][0] == ""
        assert w.csv_dict['dc.contributor.author[en]'][7][0] == ""
    
    def test_3a_creator(self):
        w = deepcopy(wrapper)
        
        rules.rule3a_creator(w)
        
        assert "creator1" in w.csv_dict['dc.creator'][1]
        assert not w.csv_dict.has_key('dc.creator[]')
        
    def test_3b_creator(self):
        w = deepcopy(wrapper)
        
        rules.rule3b_creator(w)
        
        assert "creator2" in w.csv_dict['dc.creator'][2], w.csv_dict['dc.creator']
        assert "creator3" in w.csv_dict['dc.creator'][2]
    
    def test_3c_creator(self):
        w = deepcopy(wrapper)
        
        author_2_len = len(w.csv_dict['dc.contributor.author[en]'][2])
        
        rules.rule3c_creator(w)
        
        # check columns have been deleted / kept as appropriate
        assert not w.csv_dict.has_key('dc.creator')
        assert w.csv_dict.has_key('dc.contributor.author[en]')
        
        # check length
        assert len(w.csv_dict['dc.contributor.author[en]'][2]) == author_2_len + 1
        
        # now check for the merged content
        assert w.csv_dict['dc.contributor.author[en]'][2][-1] == 'creator2; creator3'
        
    
    def test_4a_contributor(self):
        w = deepcopy(wrapper)
        
        rules.rule4a_contributor(w)
        
        assert len(w.csv_dict['dc.contributor'][1]) == 1, w.csv_dict['dc.contributor']
        assert w.csv_dict['dc.contributor'][1][0] == ""
        assert w.csv_dict['dc.contributor'][2][0] == "University of Somewhere"
        assert w.csv_dict['dc.contributor'][3][0] == ""
    
    def test_4b_contributor(self):
        w = deepcopy(wrapper)
        
        rules.rule4b_contributor(w)
        
        assert "University of Somewhere" in w.csv_dict['dc.publisher[en]'][2]
        assert not w.csv_dict.has_key('dc.contributor')
        
    def test_4c_contributor(self):
        w = deepcopy(wrapper)
        
        rules.rule4c_contributor(w)
        
        assert "University of Over There" in w.csv_dict['dc.publisher[en]'][1]
        assert not w.csv_dict.has_key('dc.contributor[x-none]')

    def test_4d_contributor(self):
        w = deepcopy(wrapper)
        
        author_7_len = len(w.csv_dict['dc.contributor.author[en]'][7])
        
        rules.rule4d_contributor(w)
        
        assert not w.csv_dict.has_key('dc.contributor[en]')
        assert w.csv_dict.has_key('dc.contributor.author[en]')
        
        assert w.csv_dict['dc.contributor.author[en]'][1][-1] == 'SHIELD'
        assert w.csv_dict['dc.contributor.author[en]'][2][-2] == "Cat's Paws Sanctuary"
        assert w.csv_dict['dc.contributor.author[en]'][2][-1] == 'Splott'
        # 'UCLAN' should have been detected as being the same as 'uclan'
        # and NOT merged, leaving the legth of that field the same
        assert len(w.csv_dict['dc.contributor.author[en]'][7]) == author_7_len
        
    def test_5a_subject(self):
        w = deepcopy(wrapper)
        
        rules.rule5a_subject(w)
        
        assert "subject1" in w.csv_dict['dc.subject[en]'][1]
        assert not w.csv_dict.has_key('dc.subject[EN]')
        
        assert "subject2" in w.csv_dict['dc.subject[en]'][2]
        assert not w.csv_dict.has_key('dc.subject[]')
        
        assert "subject3" in w.csv_dict['dc.subject[en]'][1]
        assert not w.csv_dict.has_key('dc.subject[en-gb]')
        
        assert "subject4" in w.csv_dict['dc.subject[en]'][2]
        assert not w.csv_dict.has_key('dc.subject[ene]')
        
    def test_5b_subject(self):
        w = deepcopy(wrapper)
        
        rules.rule5b_subject(w)
        
        assert "other1" in w.csv_dict['dc.subject[en]'][1]
        assert not w.csv_dict.has_key('dc.contributor.other[en]')
        
    def test_5c_subject(self):
        w = deepcopy(wrapper)
        
        rules.rule5c_subject(w)
        
        assert "class1" in w.csv_dict['dc.subject.classification[en]'][1]
        assert not w.csv_dict.has_key('dc.subject.classification[]')
        
    def test_5d_subject(self):
        w = deepcopy(wrapper)
        
        rules.rule5d_subject(w)
        
        assert "sponsor1" in w.csv_dict['dc.subject[en]'][1]
        assert not w.csv_dict.has_key('dc.description.sponsorship')
        
    def test_5e_subject(self):
        w = deepcopy(wrapper)
        
        rules.rule5e_subject(w)
        
        assert "de-normalised spacing here" in w.csv_dict['dc.subject[en]'][1]
        assert "quoted" in w.csv_dict['dc.subject[en]'][2]
        assert "upper case" in w.csv_dict['dc.subject[en]'][3]
    
    def test_5f_subject(self):
        w = deepcopy(wrapper)
        
        rules.rule5f_subject(w)
        
        assert "split" in w.csv_dict['dc.subject[en]'][4]
        assert "this" in w.csv_dict['dc.subject[en]'][4], w.csv_dict['dc.subject[en]']
        assert "split; this" not in w.csv_dict['dc.subject[en]'][4]
        assert "and" in w.csv_dict['dc.subject[en]'][5]
        assert "this" in w.csv_dict['dc.subject[en]'][5]
        assert "and, this" not in w.csv_dict['dc.subject[en]'][5]
    
    def test_6a_coverage(self):
        w = deepcopy(wrapper)
        
        rules.rule6a_coverage(w)
        
        assert not w.csv_dict.has_key('dc.coverage.temporal[en]')
        
    def test_6b_coverage(self):
        w = deepcopy(wrapper)
        
        rules.rule6b_coverage(w)
        
        assert not w.csv_dict.has_key('dc.coverage.spatial[en]')
    
    def test_7a_date(self):
        w = deepcopy(wrapper)
        
        rules.rule7a_date(w)
        
        # Tue, 16 Jun 2009 11:34:02 +0100
        assert w.csv_dict['dc.date[]'][1][0] == "2009-06-16T11:34:02Z", w.csv_dict['dc.date[]'][1][0]
    
    def test_7b_date(self):
        w = deepcopy(wrapper)
        
        rules.rule7b_date(w)
        
        assert w.csv_dict['dc.date'][1][0] == "Tue, 16 Jun 2009 11:34:02 +0100"
        assert not w.csv_dict.has_key('dc.date[]')
    
    def test_7c_date(self):
        # no rule implementation after all
        pass
    
    def test_7d_date(self):
        w = deepcopy(wrapper)
        
        rules.rule7d_date(w)
        
        assert w.csv_dict['dc.date.issued'][1][0] == "date1"
        assert not w.csv_dict.has_key('dc.date.issued[]')
    
    def test_7e_date(self):
        w = deepcopy(wrapper)
        
        rules.rule7e_date(w)
        
        # 2011-01-01T00:00:00Z
        assert len(w.csv_dict['dc.date'][2]) == 1
        assert w.csv_dict['dc.date'][2][0] == "2011-01-01T00:00:00Z", w.csv_dict['dc.date']
        
        assert len(w.csv_dict['dc.date[]'][2]) == 1
        assert w.csv_dict['dc.date[]'][2][0] == "2011-01-01T00:00:00Z"
        
        assert len(w.csv_dict['dc.date.created'][2]) == 1
        assert w.csv_dict['dc.date.created'][2][0] == "2011-01-01T00:00:00Z"
        
        assert len(w.csv_dict['dc.date.created[en]'][2]) == 1
        assert w.csv_dict['dc.date.created[en]'][2][0] == "2011-01-01T00:00:00Z"
        
        assert len(w.csv_dict['dc.date.issued'][2]) == 1
        assert w.csv_dict['dc.date.issued'][2][0] == "2011-01-01T00:00:00Z"
        
        assert len(w.csv_dict['dc.date.issued[]'][2]) == 1
        assert w.csv_dict['dc.date.issued[]'][2][0] == "2011-01-01T00:00:00Z"
    
    def test_7f_date(self):
        w = deepcopy(wrapper)
        
        rules.rule7f_date(w)
        
        assert not w.csv_dict.has_key('dc.date.created[en]')
    
    def test_8a_description(self):
        w = deepcopy(wrapper)
        
        rules.rule8a_description(w)
        
        assert not w.csv_dict.has_key('dc.description.uri[en]')
    
    def test_8b_description(self):
        w = deepcopy(wrapper)
        
        rules.rule8b_description(w)
        
        assert w.csv_dict['dc.description[en]'][1][0] == "desc1"
        assert not w.csv_dict.has_key('dc.description[]')
        
        assert w.csv_dict['dc.description[en]'][2][0] == "desc2"
        assert not w.csv_dict.has_key('dc.description[en-gb]')
    
    def test_8c_description(self):
        w = deepcopy(wrapper)
        
        rules.rule8c_description(w)
        
        assert w.csv_dict['note.dc.description[en]'][3][0] == "possible issue"
        assert w.csv_dict['note.dc.description[en]'][4][0] == "possible issue"
    
    def test_10a_language(self):
        w = deepcopy(wrapper)
        
        rules.rule10a_language(w)
        
        assert not w.csv_dict.has_key('dc.language[x-none]')
        
    def test_10b_language(self):
        w = deepcopy(wrapper)
        
        rules.rule10b_language(w)
        
        assert not w.csv_dict.has_key('dc.language[]')
        assert not w.csv_dict.has_key('dc.language[de]')
        assert not w.csv_dict.has_key('dc.language[en-GB]')
        assert not w.csv_dict.has_key('dc.language[en-gb]')
        assert not w.csv_dict.has_key('dc.language[en]')
        assert not w.csv_dict.has_key('dc.language[fr]')
        assert w.csv_dict.has_key('dc.language')
        
        assert len(w.csv_dict['dc.language'][1]) == 1
        assert w.csv_dict['dc.language'][1][0] == 'en'
        
        assert len(w.csv_dict['dc.language'][2]) == 2
        assert w.csv_dict['dc.language'][2][0] == 'fr'
        assert w.csv_dict['dc.language'][2][1] == 'en'
        
        assert len(w.csv_dict['dc.language'][3]) == 2
        assert w.csv_dict['dc.language'][3][0] == 'de'
        assert w.csv_dict['dc.language'][3][1] == 'en'
        
        assert len(w.csv_dict['dc.language'][4]) == 4
        assert w.csv_dict['dc.language'][4][0] == 'es'
        assert w.csv_dict['dc.language'][4][1] == 'es'
        assert w.csv_dict['dc.language'][4][2] == 'en'
        assert w.csv_dict['dc.language'][4][3] == 'ru'
        
        assert len(w.csv_dict['dc.language'][5]) == 3
        assert w.csv_dict['dc.language'][5][0] == 'bg'
        assert w.csv_dict['dc.language'][5][1] == 'gr'
        assert w.csv_dict['dc.language'][5][2] == 'en'
        
        assert len(w.csv_dict['dc.language'][6]) == 2
        assert w.csv_dict['dc.language'][6][0] == 'zh'
        assert w.csv_dict['dc.language'][6][1] == 'en'
        
        assert len(w.csv_dict['dc.language'][7]) == 0
        
    def test_11a_title(self):
        w = deepcopy(wrapper)
        
        rules.rule11a_title(w)
        
        assert not w.csv_dict.has_key('dc.title[*]')
        assert not w.csv_dict.has_key('dc.title[]')
        assert not w.csv_dict.has_key('dc.title[en-US]')
        assert not w.csv_dict.has_key('dc.title[en-gb]')
        assert w.csv_dict.has_key('dc.title[en]')
        
        assert w.csv_dict['dc.title[en]'][1][0] == 'Un'
        assert w.csv_dict['dc.title[en]'][2][0] == 'Dau'
        assert w.csv_dict['dc.title[en]'][3][0] == 'tri'
        assert w.csv_dict['dc.title[en]'][4][0] == 'Pedwar'
        assert w.csv_dict['dc.title[en]'][5][0] == 'Pimp'
        assert w.csv_dict['dc.title[en]'][6][0] == 'Chwech'
        assert w.csv_dict['dc.title[en]'][7][0] == 'saith'
        
    def test_11b_title(self):
        w = deepcopy(wrapper)
        
        rules.rule11b_title(w)
        
        assert w.csv_dict.has_key('note.dc.title[en]')
        
        assert w.csv_dict['note.dc.title[en]'][1][0] == 'possible issue'
        assert w.csv_dict['note.dc.title[en]'][2][0] == 'possible issue'
        assert w.csv_dict['note.dc.title[en]'][3][0] == 'possible issue'
        assert w.csv_dict['note.dc.title[en]'][4][0] == 'possible issue'
        assert w.csv_dict['note.dc.title[en]'][5][0] == 'possible issue'
        assert w.csv_dict['note.dc.title[en]'][6][0] == ''
        assert w.csv_dict['note.dc.title[en]'][7][0] == 'possible issue'
        
    def test_12a_identifier(self):
        w = deepcopy(wrapper)
        
        rules.rule12a_identifier(w)
        
        assert not w.csv_dict.has_key('dc.identifier.uri[]')
        assert not w.csv_dict.has_key('dc.identifier.uri[en]')
        assert w.csv_dict.has_key('dc.identifier.uri')
        
        assert len(w.csv_dict['dc.identifier.uri'][1]) == 2
        assert w.csv_dict['dc.identifier.uri'][1][0] == '10.1000/182'
        assert w.csv_dict['dc.identifier.uri'][1][1] == 'UUID'
        
        assert w.csv_dict['dc.identifier.uri'][2][0] == 'without context'
        
        assert len(w.csv_dict['dc.identifier.uri'][3]) == 1
        assert w.csv_dict['dc.identifier.uri'][3][0] == '== fun!'
        
        assert len(w.csv_dict['dc.identifier.uri'][4]) + \
            len(w.csv_dict['dc.identifier.uri'][5]) + \
            len(w.csv_dict['dc.identifier.uri'][6]) == 0
        
        assert w.csv_dict['dc.identifier.uri'][7][0] == 'this resource is scottish'
        
    def test_13a_publisher(self):
        w = deepcopy(wrapper)
        
        rules.rule13a_publisher(w)
        
        assert not w.csv_dict.has_key('dc.publisher')
        assert not w.csv_dict.has_key('dc.publisher[en-gb]')
        assert w.csv_dict.has_key('dc.publisher[en]')

        assert len(w.csv_dict['dc.publisher[en]'][1]) == 2
        assert w.csv_dict['dc.publisher[en]'][1][0] == 'test'
        assert w.csv_dict['dc.publisher[en]'][1][1] == 'test2'
        
    def test_13b_publisher(self):
        w = deepcopy(wrapper)
        
        rules.rule13b_publisher(w)
        
        assert w.csv_dict.has_key('note.dc.publisher[en]')
        ''
        assert w.csv_dict['note.dc.publisher[en]'][3][0] == ''
        assert w.csv_dict['note.dc.publisher[en]'][4][0] == ''
        assert w.csv_dict['note.dc.publisher[en]'][5][0] == 'possible person name'
        assert w.csv_dict['note.dc.publisher[en]'][6][0] == ''
        
    def test_14a_general(self):
        w = deepcopy(wrapper)
        
        rules.rule14a_general(w)
        
        assert len(w.csv_dict['dc.subject[ene]'][7]) == 1
        assert w.csv_dict['dc.subject[ene]'][7][0] == 'dup'
        
    def test_14c_general(self):
        w = deepcopy(wrapper)
        
        rules.rule14c_general(w)
        
        assert w.csv_dict.has_key('note.organisations')
        assert w.csv_dict['note.organisations'][1][0] == 'possible org name'
        assert w.csv_dict['note.organisations'][2][0] == 'possible org name'
        assert w.csv_dict['note.organisations'][5][0] == 'possible org name'
        assert w.csv_dict['note.organisations'][6][0] == 'possible org name'
        
    def test_14d_general(self):
        w = deepcopy(wrapper)
        
        rules.rule14d_general(w)
        
        assert w.csv_dict['dc.publisher[en-gb]'][7][0] == ''
        assert w.csv_dict['dc.contributor'][1][0] == ''
        assert len(w.csv_dict['dc.subject[en-gb]'][5]) == 1
        assert w.csv_dict['dc.subject[en-gb]'][5][0] == 'normal subject'
        
    def test_14e_general(self):
        w = deepcopy(wrapper)
        
        rules.rule14e_general(w)
        
        assert w.csv_dict.has_key('note.dc.subject[en]')
        assert w.csv_dict['note.dc.subject[en]'][7][0] == 'long subject'