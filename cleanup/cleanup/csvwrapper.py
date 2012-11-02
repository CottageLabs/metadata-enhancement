"""
Wrapper class and utility functions for reading, writing and modifying
a CSV
"""
import csv
from copy import deepcopy

class CSVWrapper(object):

    def __init__(self, csv_file_path=None):
        self.csv_dict = None
        self.ids = None
        if csv_file_path is not None:
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

    def save(self, path, save_keys_override=None, save_items_override=None):
        """
        Save the self.csv_dict as a csv file to the supplied file path
        """
        with open(path, "wb") as f:
            writer = csv.writer(f)
            
            # first, the headers
            header_index_map = {}
            header_row = []
            
            if save_keys_override:
                keys = save_keys_override
            else:
                keys = self.csv_dict.keys()
                # lets have all the keys in alphabetical order, bringing "id" and 
                # "collection" to the front if they exist
                keys.sort()
                if 'id' in keys and 'collection' in keys:
                    keys = ['id', 'collection'] + [k for k in keys if k != 'id' and k != 'collection']
                elif 'id' in keys:
                    keys = ['id'] + [k for k in keys if k != 'id']
                    
            i = 0
            for header in keys:
                header_row.append(header)
                header_index_map[header] = i
                i += 1
            writer.writerow(header_row)
            
            # now, each item id
            for id in self.ids:
                
                if save_items_override:
                    if id not in save_items_override:
                        continue
                                
                item_row = [None] * len(keys)
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
        
        The value function (fn) MUST either return the original value or a modified
        value.  If it does not return, then the original value will be lost
        """
        if not self.csv_dict.has_key(column):
            return
        for id in self.ids:
            original_values = self.csv_dict[column][id]
            new_values = []
            for original_value in original_values:
                new_value = fn(original_value)
                if new_value: # leave out '', None and so on - a nice way to delete values
                    new_values.append(new_value)
            if len(new_values) == 0:
                new_values = ['']
            self.csv_dict[column][id] = new_values
    
    def apply_global_value_function(self, fn):
        """
        apply the supplied function to every value in every cell in the whole document
        """
        for column in self.csv_dict.keys():
            self.apply_value_function(column, fn)
            
    def apply_global_cell_function(self, fn):
        """
        apply the supplied function to every cell in the whole document
        """
        for column in self.csv_dict.keys():
            self.apply_cell_function(column, fn)
    
    def apply_cell_function(self, column, fn):
        """
        Apply the supplied function to every cell in the supplied column (i.e. to
        the array of values in that cell as a whole, not the individual values)
        """
        if not self.csv_dict.has_key(column):
            return
        for id in self.ids:
            original_values = self.csv_dict[column][id]
            new_values = fn(original_values)
            if len(new_values) == 0:
                new_values = ['']
            self.csv_dict[column][id] = new_values
    
    def find_by_value_function(self, column, fn):
        """
        Apply the supplied function to every cell in the supplied column, and for
        every cell where the function returns True, record the id, and return an
        array of all matching ids.
        """
        if not self.csv_dict.has_key(column):
            return
        found = []
        for id in self.ids:
            values = self.csv_dict[column][id]
            for value in values:
                if fn(value):
                    found.append(id)
        return found
        
    def find_by_value_function_map(self, column, fn):
        """
        Apply the supplied function to every cell in the supplied column, and for
        every cell where the function returns a value (not False), record the 
        id and the value, and return a dictionary of all matching values like 
        this: {id: ["value1", "value2"]}.
        """
        if not self.csv_dict.has_key(column):
            return
        found = {}
        found_per_id = []
        for id in self.ids:
            values = self.csv_dict[column][id]
            for value in values:
                if fn(value):
                    if id not in found:
                        found[id] = []
                    found[id].append(value)
        return found
    
    def c2c_copy_by_value_function(self, src, dst, fn):
        """
        column-to-column copying of values if applied function returns True
        
        Apply the function that's being passed in to each value in each cell of the source column. Copy each value for which the function returns true to the destination column.
        """
        if not self.csv_dict.has_key(src) or not self.csv_dict.has_key(dst):
            return
            
        for id in self.ids:
            values = self.csv_dict[src][id]
            for value in values:
                if fn(value):
                    self.add_value(dst, id, value)
    
    def c2c_apply_value_function(self, src, dst, fn):
        """
        If the given function returns a non-False value after being applied to
        the src column, put that value into the dst column.
        
        Do not modify dst if the function returns False.
        """
        if not self.csv_dict.has_key(src) or not self.csv_dict.has_key(dst):
            return
            
        for id in self.ids:
            values = self.csv_dict[src][id]
            for value in values:
                if fn(value):
                    self.add_value(dst, id, fn(value))
                    
    def c2c_copy_cells(self, src, dst, ids):
        """
        Add the contents of certain specified cells from the src column to the dst column
        """
        if not self.csv_dict.has_key(src) or not self.csv_dict.has_key(dst):
            return
            
        for id in ids:
            if not self.csv_dict[src].has_key(id) or not self.csv_dict[dst].has_key(id):
                return
                
            self.add_value(dst, id, *self.csv_dict[src][id])
    
    def delete_column(self, column):
        """
        Delete a column from the dataset with all its data.
        """
        if not self.csv_dict.has_key(column):
            return
        del self.csv_dict[column]
        
    def add_column(self, column):
        """
        Add a column with the given name
        """
        if self.csv_dict.has_key(column):
            return
        self.csv_dict[column] = {}
        for id in self.ids:
            self.csv_dict[column][id] = ['']
        
    def delete_record(self, item_id):
        """
        Delete a record (row) given the item_id of the item that's stored in the record.
        """
        key_existed = False
        
        for column in self.csv_dict.keys():
            if self.csv_dict[column].has_key(item_id):
                key_existed = True
                del self.csv_dict[column][item_id]
        
        if key_existed:
            self.ids.remove(item_id)
        
    def find_in_column(self, column, search_for, partial=False):
        """
        Find all records which contain the specified value in the specified column 
        and return a list of the matching Jorum item ID-s. Pass partial = True to 
        get it to return records whose values only partially match the search term.
        """
        if not self.csv_dict.has_key(column):
            return []
        found = []
        for id in self.ids:
            values = self.csv_dict[column][id]
            counted = False
            for value in values:
                if partial:
                    if search_for in value:
                        found.append(id)
                        counted = True
                else:
                    if search_for == value:
                        found.append(id)
                        counted = True
                if counted:
                    # no need to look any further if we've already caught
                    # this item id
                    break
        return found
        
    def merge_columns(self, src, dst):
        """
        Merges two CSV columns. If there are overlapping values, the fields are 
        concatenated (i.e. non-destructive merging - no data is overwritten).
        
        Takes two column names as its first two parameters.
            The first column is the one that you want to try to merge with the 
                second one. The first column will be deleted after a successful 
                merge.
            The second column is the one that will end up with all the data - 
                the one you are merging *into*. After a successful merge, it will 
                have the data from both columns.
        """
        if not self.csv_dict.has_key(src) or not self.csv_dict.has_key(dst):
            return
        
        for id in self.ids:
            src_values = self.csv_dict[src][id]
            dst_values = self.csv_dict[dst][id]
            merged_values = self._combine(src_values, dst_values)
            self.csv_dict[dst][id] = merged_values
        
        self.delete_column(src)
    
    def _combine(self, src_values, dst_values):
        src_norm, map = normalise_strings(src_values)
        
        dst_norm, dst_map = normalise_strings(dst_values)
        map.update(dst_map) # merge src_ and dst_ reverse lookup maps
        
        norm_result = dst_norm + [a for a in src_norm if a not in dst_norm]
        return denormalise_strings(norm_result, map)
    
    def add_value(self, column, item_id, *values):
        """
        Add the specified value(s) to the existing contents of the cell. 
        The cell to be modified is specified by the column and Jorum item 
        ID. Multiple values are allowed in the form of *args.
        """
        if not self.csv_dict.has_key(column) or not self.csv_dict[column].has_key(item_id):
            return
        existing_values = self.csv_dict[column][item_id]
        new_values = self._combine(values, existing_values)
        self.csv_dict[column][item_id] = new_values
        
    def delete_contents(self, column, item_id):
        """
        Deletes the contents of a cell specified by the column and Jorum item ID.
        """
        if not self.csv_dict.has_key(column) or not self.csv_dict[column].has_key(item_id):
            return
        self.csv_dict[column][item_id] = ['']

    def delete_value(self, column, item_id, del_value):
        """
        Deletes the specified value from the contents of the cell specified by the column and Jorum item ID.
        """
        if not self.csv_dict.has_key(column) or not self.csv_dict[column].has_key(item_id):
            return
        
        # normalise representation of all values in specified cell
        cell_norm, map = normalise_strings(self.csv_dict[column][item_id])
        
        # delete all instances of specified value to be deleted
        cmpval = del_value.strip().lower()
        cell_norm = [v for v in cell_norm if v != cmpval]
        
        # put the remaining values back into the cell using their original 
        # representations
        self.csv_dict[column][item_id] = denormalise_strings(cell_norm, map)
        
    def set_value(self, column, item_ids, value):
        """
        set the value of a supplied column to the supplied value for the given
        item ids (an array)
        """
        if not self.csv_dict.has_key(column):
            return
        for id in item_ids:
            if not self.csv_dict[column].has_key(id):
                continue
            self.csv_dict[column][id] = [value]
            
    def incorporate_column(self, column_name, column, overwrite=False):
        if not self.csv_dict.has_key(column_name):
            self.csv_dict[column_name] = {}
        for id in self.ids:
            v = []
            if id in column.keys():
                v = column[id]
            existing = self.csv_dict[column_name].get(id, [])
            if overwrite:
                new = v
            else:
                new = self._combine(v, existing)
            self.csv_dict[column_name][id] = new
            
    def subset(self, item_ids):
        new_dict = {}
        for key, d in self.csv_dict.iteritems():
            new_dict[key] = {}
            for i in item_ids:
                new_dict[key][i] = deepcopy(d[i])
        sub = CSVWrapper()
        sub.csv_dict = new_dict
        sub.populate_ids()
        return sub

    def filter_rows(self, filter_column, should_be_empty):
        """
        Return a list of item ID-s where the filter column contains or does not contain a value.
        If should_be_empty is True, then the id is only added to the results if it's filter_column field is empty.
        If should_be_empty is False, then there must be some content in the id's filter_column field for it to be let through the filter.
        """
        if not self.csv_dict.has_key(filter_column):
            if should_be_empty:
                return self.ids
            else:
                return []
        
        slice_ids = []
        for id in self.ids:
            if (
                not self.csv_dict[filter_column][id] \
                or (
                    len(self.csv_dict[filter_column][id]) == 1 \
                    and not self.csv_dict[filter_column][id][0]
                   )
                ) \
                ^ should_be_empty:
            # skip the item if we have no interest in it - the filter
            # column field for this item is empty
                continue
            
            slice_ids.append(id)

        return slice_ids
        
    def filter_columns(self, *keep_columns):
        """
        Deletes all columns in the CSV *except* the ones passed in as parameters to this method.
        """
        for col in self.csv_dict.keys():
            if col not in keep_columns:
                self.delete_column(col)
        
    def cell_contains(self, column, id, searchstr):
        if not self.csv_dict.has_key(column):
            return
        if not self.csv_dict[column].has_key(id):
            return
        
        norm_search = searchstr.strip().lower()
        norm_target_cell, map = normalise_strings(self.csv_dict[column][id])
        
        if norm_search in norm_target_cell:
            return True
            
        return False
                
def normalise_strings(list_of_str):
    """
    Given a list of strings, will return a tuple:
    
    (list of normalised strings, map[normalised strings -> original ones])
    "normalised" means stripped of leading/trailing whitespace and lowercased.
    """
    norm = []
    map = {}
    for str in list_of_str:
        norm_str = str.strip().lower()
        if norm_str:
            norm.append(norm_str)
            map[norm_str] = str
    return (norm, map)
    
def denormalise_strings(list_of_str, map):
    """
    Given a list of normalised strings and a lookup map, will return the original versions of the strings.
    
    "normalised" means stripped of leading/trailing whitespace and lowercased.
    The map is a dictionary:
    map['string'] = '  StriNg '
    """
    return [map.get(r) for r in list_of_str]