#This section of the code was written by Aidan Riley


#IMPORTANT NOTE
#line 26 of the march clinical data excel file needs to be corrected so that the two numbers are spaced apart


from openpyxl import load_workbook
import os

#functions for pairing row names with indicies
def col_name_dict(workbook):
    for row in workbook.iter_rows(min_row=1,max_row=1,values_only=True):
        tup = row
    dict = {tup[i]:i for i in range(len(tup))}
    return dict


#A class that stores the information from the Clinical Data Excel sheet for the March Data
class patient:
    def __init__(self,data,type):
        if type == 'march':
            self.type=type
            self.bank_nums = data[0]
            self.age = data[1]
            self.treatment = data[2]
            self.cyle = data[3]
            self.t_size = data[4]
            self.nodal_status = data[5]
            self.ER = data[6]
            self.PR = data[7]
            self.HER2_IHC = data[8]
            self.HER2_FISH = data[9]
            self.histo = data[10]
            self.clinical_response = data[11]
            self.pathologic_response = data[12]
        elif type == 'junepre':
            self.type = type
            self.bank_nums = data[0],data[1]
            self.age = data[3]
            self.treatment = data[5]
            self.cyle = data[6]
            self.t_size = data[7]
            self.nodal_status = data[8]
            self.ER = data[9]
            self.PR = data[10]
            self.HER2_IHC = data[11]
            self.HER2_FISH = data[12]
            self.histo = data[13]
            self.clinical_response = data[14]
            self.pathologic_response = data[15]
        elif type == 'junepre':
            self.type = type
            self.bank_nums = data[0], data[1]
            self.age = data[3]
            self.treatment = data[5]
            self.cyle = data[6]
            self.t_size = data[7]
            self.nodal_status = data[8]
            self.ER = data[9]
            self.PR = data[10]
            self.HER2_IHC = data[11]
            self.HER2_FISH = data[12]
            self.histo = data[13]
            #no clinical/pathological response in post-op june sheet
            #self.clinical_response = data[14]
            #self.pathologic_response = data[15]

    def __str__(self):
        return '%s %s \n' % (self.type,self.bank_nums)

#this will extract the clinical data from a specific excel file
#type can be equal to 'june' or 'march'
#output is a list of patient objects
def parse_file(file,ver):
    output = []
    #go through each row, and create a patient for the values in each column of that row
    for row in file.iter_rows(min_row=2, max_row=file.max_row, values_only=True):
        if row[0] is None:
            pass
        else:
            output.append(patient(row,ver))
    return output
#this function will call parse_file on the entire folder that the data is stored in
def parse_folder(folder):
    file_list = os.listdir(folder)
    obj_lst = []
    for file in file_list:
        if file[0:6] == 'Normal':
            pass
        elif file[-11:-7] == 'june':
            ver = 'junepre'
            book_one = load_workbook('%s' % (folder+'\\'+file))['Pre-op FAC']
            obj_lst = obj_lst + parse_file(book_one,ver)

            ver = 'junepost'
            book_two = load_workbook('%s' % (folder+'\\'+file))['Post-op']
            obj_lst = obj_lst + parse_file(book_two,ver)
        else:
            ver = 'march'
            book = load_workbook('%s' % (folder + '\\' + file))['Sheet1']
            obj_lst = obj_lst + parse_file(book, ver)
    return obj_lst

y = parse_folder("clinical_data")
