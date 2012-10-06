import csv

class CSVUtils(object):
    column_pos = {}
    columns = []
    data = []

    def __init__(self, csv_filename):
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
