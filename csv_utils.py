import csv
import copy

class CSVUtils(object):
    multival_sep = None # The string which is used to separate multiple values within one field
    column_pos = {}
    columns = []
    data = []

    def __init__(self, csv_filename, multival_sep = None):
        self.multival_sep = multival_sep.strip() # trim whitespace off both ends of the separator string
        self.load(csv_filename)
        
    def load(self, csv_filename):
        with open(csv_filename, 'rb') as csvfile:
            content = csv.reader(csvfile)
            
            col_num = 0
            self.columns = content.next()
            for col_name in self.columns:
                self.column_pos[col_name] = col_num
                col_num += 1
                
            for row in content:
                for field in row:
                    if multival_sep:
                        field = multival_str2list(field, multival_sep)
                        # if len(field) <= 1:
                            # field = ''.join(field)
                self.data.append(row)
                
    def save(self, output_filename):
        with open(output_filename, 'wb') as csvfile:
            output = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            output.writerow(self.columns)
            output.writerows(self.data)
    
    def get_column_position(self, column_name):
        try:
            return self.column_pos[column_name]
        except KeyError as e:
            print 'One of the column names does not exist in the CSV.'
            raise # still have to kill the script + this provides tech. info to techie users
    
    def delete_column(self, column_name):
        column_position = self.get_column_position(column_name)
        
        for row in self.data:
            del row[column_position]
            
        del self.columns[column_position]
    
    def merge_columns(self, merge_this_name, into_that_name):
        '''Merges two CSV columns. If there are overlapping values, the fields are concatenated (i.e. non-destructive merging - no data is overwritten).
        
        Takes two column names as its two parameters.
            The first column is the one that you want to try to merge with the second one. The first column will be deleted after a successful merge.
            The second column is the one that will end up with all the data - the one you are merging *into*. After a successful merge, it will have the data from both columns.
        '''
        
        merge_this = self.get_column_position(merge_this_name)
        into_that = self.get_column_position(into_that_name)
        
        row_count = 2 # skip the column headings row when counting
        for row in self.data:
            pass
        
        
    def interactive_merge(self, merge_this_name, into_that_name):
        '''Tries to merge two CSV columns. Stops and asks you what to do if it finds overlapping values. Answering "n" (no) stops the process.
        
        Takes two column names as its two parameters.
            The first column is the one that we want to try to merge with the second one. The first column will be deleted after a successful merge.
            The second column is the one that will end up having all the data - the one we are merging *into*. After a successful merge, it will have the data from both columns.
        '''
        
        merge_this = self.get_column_position(merge_this_name)
        into_that = self.get_column_position(into_that_name)
        
        row_count = 2 # skip the column headings row when counting
        for row in self.data:
            
            if row[merge_this] and row[into_that]:
                print
                print '[Row #' + str(row_count) + '] Overlapping values while trying to merge', '"' + merge_this_name + '"', 'into', '"' + into_that_name + '"',':'
                print merge_this_name, ':', row[merge_this]
                print into_that_name, ':', row[into_that]
                
                answer = raw_input('Do you want to overwrite "' + row[into_that] + '" from "' + into_that_name + '" with "' + row[merge_this] + '" from "' + merge_this_name + '" ? (y/n): ')
                
                if answer == 'n':
                    return
        
            if row[merge_this]:
                row[into_that] = row[merge_this]
            
            del row[merge_this]
            row_count += 1
        
        del self.columns[merge_this]
        
    def debug(self):
        print '##### Columns #####'
        print self.columns
        print
        print '##### Look-up dictionary of column positions by column name #####'
        print self.column_pos
        print
        print '##### Data (first row only) #####'
        print self.data[0]
        print

def multival_str2list(multival_str, multival_sep, trim_whitespace = True):
    '''Returns a list of the values contained within multival_str. Uses multival_sep to break up multival_str into a list.
        
    Takes an optional trim_whitespace parameter (defaults to True). If True, it will trim the whitespace off both ends of each value after breaking up your string.
    '''
    
    result = multival_str.split(multival_sep)
    
    if trim_whitespace:
        result = clean_list(result)
    
    return result
    
def multival_list2str(multival_list, multival_sep, trim_whitespace = True):
    '''Returns a string - joins the values contained within multival_list using multival_sep.
    
    Takes an optional trim_whitespace parameter (defaults to True). If True, it will trim the whitespace off both ends of each value before packing it up into a string.
    '''
    
    work_on = multival_list
    
    if trim_whitespace:
        work_on = clean_list(work_on)
    
    return multival_sep.join(work_on)
        
def clean_list(list):
    '''Clean up a list of values (e.g. coming from an HTML form). Returns a list.
    Returns an empty list if given an empty list.

    Example: you have a list of tags. This is coming in
    as a single string: e.g. "tag1, tag2, ". You .split(',') that into
    list = ["tag1"," tag2", ""].
    
    You want to both trim the whitespace from list[1] and remove the empty
    element - list[2]. That's what this function does.
    
    What it does (a.k.a. algorithm):
    1. Trim whitespace on both ends of individual strings
    2. Remove empty strings
    3. Only check for empty strings AFTER splitting and trimming the 
    individual strings (in order to remove empty list elements).
    '''
    return [clean_item for clean_item in [item.strip() for item in list] if clean_item]