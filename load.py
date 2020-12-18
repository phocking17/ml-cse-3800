### Converts SECTRA MS in XML form to a list of dictionaries
### This section written by Patrick Hocking
import xmltodict
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy import signal

class sample:
	def __init__(self, name, mz, intensity):
		self.name = name
		self.mz = mz
		self.intensity = intensity
		self.type_f = name[0:2]
		self.sample_num = name[2:]
		self.peaks = self.find_peaks_local()
	
	def find_peaks_local(self):
		inten = np.array(self.intensity)
		peaks = signal.find_peaks(inten)
		peaks_list = np.ndarray.tolist(peaks[0])
		return peaks_list

	def __str__(self):
		return '%s %s %s \n' % (self.name, self.type_f, self.sample_num)


### Load file
def load_XML(file_name):
	file = open(file_name, 'r')
	init_dic = xmltodict.parse(file.read())
	return init_dic

def import_files(folder_list):
	full_obj = []
	for folder in folder_list:
		file_list = os.listdir(folder)
		xmls = [load_XML(folder+'\\'+i) for i in file_list]
		for j in xmls:
			name = j['spectrum']['spectrumName']
			if name[-3:] == '(2)':
				pass
			else:
				raw_data = j['spectrum']['processedData']['processedDataSamples']
				data_split = raw_data.split('\n\t\t')
				data_split = [i.split(',') for i in data_split]
				
				X= []
				Y= []
				for i in data_split:
					X.append(float(i[0]))
					Y.append(float(i[1]))
				full_obj.append(sample(name, X, Y))
	return full_obj


def plot_inputs_all(out_files):
	fig, ax = plt.subplots()
	for i in out_files:
		ax.plot(i.mz, i.intensity)

		ax.set(xlabel='m/z', ylabel='intensity',
		       title='About as simple as it gets, folks')
		ax.grid()

	plt.show()

def categories(out_files):
	type_dict = dict()
	for i in out_files:
		if i.type_f in type_dict:
			type_dict[i.type_f].append(i)
		else:
			type_dict[i.type_f]=[i]
	return type_dict

def find_max(xs):
	max_xs = 0
	for i in xs:
		if max(i) > max_xs:
			max_xs = max(i)
		else:
			pass
	return max_xs

def plot_averages(categories):
	st = []
	for sampletype in categories:
		xs = [i.mz for i in categories[sampletype]]
		ys = [i.intensity for i in categories[sampletype]]
		max_xs = find_max(xs)
		mean_x_axis = [i for i in range(0, int(max_xs)+1)]
		ys_interp = [np.interp(mean_x_axis, xs[i], ys[i]) for i in range(len(xs))]
		mean_y_axis = np.mean(ys_interp, axis=0)
		st.append([mean_x_axis, mean_y_axis])
	fig, ax = plt.subplots()
	for i in st:
		ax.plot(i[0], i[1])

		ax.set(xlabel='m/z', ylabel='intensity',)
		ax.grid()
	ax.legend([sampletype for sampletype in categories])
	plt.show()

def peaks_concentration(categories, conc_width, end_r):
	r1 = 0
	r2 = end_r
	range_list = []
	iterator = 0
	while iterator < end_r:
		range_list.append(iterator)
		iterator+=conc_width

	def peaks_range(sample, range_list):
		peak_conc = []
		iterator = 0
		while iterator < len(range_list):
			l = range_list[iterator]
			r = range_list[iterator+1]
			count = len(list(x for x in list1 if l <= x <= r))
			peak_conc.append(count)
			iterator+=1
		return peak_conc


	for sampletype in categories:
		cat = categories[sampletype]
		cat.sort(key=lambda x: x.name)
		names = [i.names for i in cat]
		values = [peaks_range(sam, range_list) for sam in cat]
		npvalues = np.array(values)

		fig, ax = plt.subplots()
		im = ax.imshow(npvalues)

		# We want to show all ticks...
		ax.set_xticks(np.arange(len(values)))
		ax.set_yticks(np.arange(len(names)))
		# ... and label them with the respective list entries
		ax.set_xticklabels(values)
		ax.set_yticklabels(names)

		# Rotate the tick labels and set their alignment.
		plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
		         rotation_mode="anchor")

		ax.set_title("Harvest of local farmers (in tons/year)")
		fig.tight_layout()
		plt.show()




june_xml_low = import_files(["low_mass_june03\\LowPrePostJune03\\RawXML"])
march_xml_low = import_files(["low_mass_march03\\LowNorPrePost\\RawXML"])





















def pull_xy(files_list):
	out_files = []
	for file in files_list:
		rawx = load_XML(file)

		raw_data = rawx['spectrum']['processedData']['processedDataSamples']
		name = rawx['spectrum']['spectrumName']
		data_split = raw_data.split('\n\t\t')
		data_split = [i.split(',') for i in data_split]
		
		X= []
		Y= []
		for i in data_split:
			X.append(float(i[0]))
			Y.append(float(i[1]))
		out_files.append(sample(name, X, Y))
	return out_files








