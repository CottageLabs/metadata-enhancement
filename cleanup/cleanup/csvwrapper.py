"""
Wrapper class and utility functions for reading, writing and modifying
a CSV
"""
import csv

class CSVWrapper(object):

    def __init__(self, csv_file_path):
        self.source_csv_path = csv_file_path
        self.csv_dict = self.populate_csv_dict()
        self.ids = self.populate_ids()
    
    ##########################################################
    # initialisation functions
    ##########################################################
    
    def popualte_csv_dict(self):
        """
        from self.source_csv_path, load csv and populate the
        csv_dict, of the form:
        
        self.csv_dict = {
           "<column name>": {
              <item id 1> : ["<column value>", "<column value>", ...],
              <item id 2> : ...
           },
          ...
        }
        """
        pass
        
    def populate_ids(self):
        """
        from self.csv_dict, obtain a list of the item ids in the dataset
        for convenience in member functions
        """
        # grab any old column, they all have all item ids in them
        column = self.csv_dict.keys()[0]
        
        # store the list of keys
        self.ids = column.keys()

    def save(self, path):
        """
        Save the self.csv_dict as a csv file to the supplied file path
        """
        pass

    ##########################################################
    # csv manipulation functions
    ##########################################################
    
    def apply_value_function(column, fn):
        """
        Apply the supplied value to every value in the supplied column
        """
        pass