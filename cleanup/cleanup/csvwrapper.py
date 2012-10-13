"""
Wrapper class and utility functions for reading, writing and modifying
a CSV
"""
import csv

class CSVWrapper(object):

    def __init__(self, csv_file_path):
        self.source_csv_path = csv_file_path
        self.populate_csv_dict()
        self.populate_ids()
    
    ##########################################################
    # initialisation functions
    ##########################################################
    
    def populate_csv_dict(self):
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
        reader = csv.reader(open(self.source_csv_path))
        first = True
        self.csv_dict = {}
        header_index_map = {}
        for row in reader:
            for i in range(len(row)): # be explicit about reading the indices of the row
                if first:
                    self.csv_dict[row[i]] = {}
                    header_index_map[i] = row[i]
                else:
                    key = header_index_map[i]
                    self.csv_dict[key][int(row[0])] = self._tokenise(row[i])
            if first: 
                first = False
        
    def populate_ids(self):
        """
        from self.csv_dict, obtain a list of the item ids in the dataset
        for convenience in member functions
        """
        # grab any old column, they all have all item ids in them
        column = self.csv_dict.keys()[0]
        
        # store the list of keys
        self.ids = self.csv_dict[column].keys()

    def save(self, path):
        """
        Save the self.csv_dict as a csv file to the supplied file path
        """
        writer = csv.writer(open(path, "w"))
        
        # first, the headers
        header_index_map = {}
        header_row = []
        i = 0
        for header in self.csv_dict.keys():
            header_row[i] = header
            header_index_map[header] = i
            i += 1
        writer.writerow(header_row)
        
        # now, each item id
        # TODO - got to go
    
    def _tokenise(self, cell_value):
        return [v.strip() for v in cell_value.split("||")]
        

    ##########################################################
    # csv manipulation functions
    ##########################################################
    
    def apply_value_function(self, column, fn):
        """
        Apply the supplied function to every value in the supplied column
        """
        pass
        
        
    def delete_column(self, column):
        """
        Delete a column from the dataset with all its data.
        """
        pass
        
    def delete_record(self, item_id):
        """
        Delete a record (row) given the item_id of the item that's stored in the record.
        """
        pass
        
    def find_in_column(self, column, search_for, partial = False):
        """
        Find all records which contain the specified value in the specified column and return a list of the matching Jorum item ID-s. Pass partial = True to get it to return records whose values only partially match the search term.
        """
        return []
        
    def merge_columns(self, src, dst):
        """
        Merges two CSV columns. If there are overlapping values, the fields are concatenated (i.e. non-destructive merging - no data is overwritten).
        
        Takes two column names as its two parameters.
            The first column is the one that you want to try to merge with the second one. The first column will be deleted after a successful merge.
            The second column is the one that will end up with all the data - the one you are merging *into*. After a successful merge, it will have the data from both columns.
        """
        pass
    
    def get_contents(self, column, item_id):
        """
        Get the contents of a cell identified by the column and Jorum item ID.
        """
        pass
    
    def set_contents(self, column, item_id, *values):
        """
        Set the value of a cell to the specified value(s). The cell to be modified is specified by the column and Jorum item ID. Multiple values are allowed in the form of *args.
        """
        pass
        
    def add_value(self, column, item_id, *values):
        """
        Add the specified value(s) to the existing contents of the cell. The cell to be modified is specified by the column and Jorum item ID. Multiple values are allowed in the form of *args.
        """
        pass
        
    def delete_contents(self, column, item_id):
        """
        Deletes the contents of a cell specified by the column and Jorum item ID.
        """
        self.set_value(column, item_id, '')
