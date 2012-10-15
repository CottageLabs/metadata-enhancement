import unittest
import csvwrapper
from copy import deepcopy

data = {
    "dc.description" : {1: ["desc1"], 2: ["desc2"], 3: ["desc3", "desc4"]}
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
        