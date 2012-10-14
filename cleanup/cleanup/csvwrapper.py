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
        with open(self.source_csv_path) as f:
            reader = csv.reader(f)
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
        with open(path, "wb") as f:
            writer = csv.writer(f)
            
            # first, the headers
            header_index_map = {}
            header_row = []
            # lets have all the keys in alphabetical order, bringing "id" and "collection"
            # to the front
            keys = self.csv_dict.keys()
            keys.sort() 
            keys = ['id', 'collection'] + [k for k in keys if k != 'id' and k != 'collection']
            
            i = 0
            for header in keys:
                header_row.append(header)
                header_index_map[header] = i
                i += 1
            writer.writerow(header_row)
            
            # now, each item id
            for id in self.ids:
                item_row = [None] * len(self.csv_dict.keys())
                for header, i in header_index_map.iteritems():
                    item_row[i] = self._serialise(self.csv_dict[header][id])
                writer.writerow(item_row)
    
    def _tokenise(self, cell_value):
        return [v.strip() for v in cell_value.split("||")]
    
    def _serialise(self, cell_values):
        return "||".join(cell_values)

    ##########################################################
    # csv manipulation functions
    ##########################################################
    
    def apply_value_function(self, column, fn):
        """
        Apply the supplied function to every value in each of the cells the supplied column
        (i.e. if there are more than one value in the cell, apply the function independently
        to each value)
        """
        for id in self.ids:
            original_values = self.csv_dict[column][id]
            new_values = []
            for original_value in original_values:
                new_value = fn(original_value)
                if new_value: # leave out '', None and so on - a nice way to delete values
                    new_values.append(new_value)
            self.csv_dict[column][id] = new_values
    
    def apply_cell_function(self, column, fn):
        """
        Apply the supplied function to every cell in the supplied column (i.e. to
        the array of values in that cell as a whole, not the individual values)
        """
        pass
    
    def find_by_value_function(self, column, fn):
        """
        Apply the supplied function to every cell in the supplied column, and for
        every cell where the function returns True, record the id, and return an
        array of all matching ids.
        """
        pass
    
    def delete_column(self, column):
        """
        Delete a column from the dataset with all its data.
        """
        pass
        
    def add_column(self, column):
        """
        Add a column with the given name
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
        
    def add_value(self, column, item_id, *values):
        """
        Add the specified value(s) to the existing contents of the cell. The cell to be modified is specified by the column and Jorum item ID. Multiple values are allowed in the form of *args.
        """
        pass
        
    def delete_contents(self, column, item_id):
        """
        Deletes the contents of a cell specified by the column and Jorum item ID.
        """
        # Maybe do sth. like self.set_contents(column, item_id, '')
        pass
        
    def set_value(self, column, item_ids, value):
        """
        set the value of a supplied column to the supplied value for the given
        item ids
        """
        pass

    # Deprecated method templates below - if found to be required, move above 
    # this line and uncomment.
    # def get_contents(self, column, item_id):
        # """
        # Get the contents of a cell identified by the column and Jorum item ID.
        # """
        # pass
    
    #def set_contents(self, column, item_id, *values):
        # """
        # Set the value of a cell to the specified value(s). The cell to be modified is specified by the column and Jorum item ID. Multiple values are allowed in the form of *args.
        # """
        # pass
