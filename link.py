from load import import_files
from excel_reading import parse_folder, Patient


#import the june and march low intensity xml files

#enter the path to the xml files here
june_xml_low = import_files(["low_mass_june03\\LowPrePostJune03\\RawXML"])
#march_xml_low = import_files(["low_mass_march03\\LowNorPrePost\\RawXML"])
#enter the name of your clinical data here
excel_lst = parse_folder("clinical_data")


class Patient_Linked(Patient):
    def __init__(self, mz, intensity):
        self.Patient.__init__()
        self.mz = mz
        self.intensity = intensity

    def __str__(self):
        return "%s %s" % (self.bank_nums,self.intensity)

#convert the sample data type into a dictionary for lookup
def samples_to_dict(sample_lst):
    dict = {}
    for sample in sample_lst:
        dict[int(sample.name[2:])] = sample
    return dict
#print(samples_to_dict(june_xml_low))

def link(xmls,excels):
    lookup = samples_to_dict(xmls)
    obj_lst = []
    for patient in excel_lst:
        #Retrieve the bank number identifier
        num_one = patient.bank_nums[0]
        num_two = patient.bank_nums[1]
        #Access the corresponding xml data
        mz_dat_one = lookup[num_one]
        mz_dat_two = lookup[num_two]
        #Create a new linked object and add to the output list
        obj_lst.append(Patient_Linked(patient, mz_dat_one.mz, mz_dat_one.intensity))
    return obj_lst



y = link(june_xml_low,excel_lst)
for entry in y:
    print(entry)