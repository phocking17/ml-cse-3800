import pandas as pd
import scipy.signal

def peaks(file, parameter_list):
	### Curve to find peaks
	signal_array=file[parameter_list[0]]
	peak_obj=scipy.signal.find_peaks(signal_array)