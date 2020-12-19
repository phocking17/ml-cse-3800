import os
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
def get_parent_dir(directory):
    return os.path.dirname(directory)
    
def confusion_to_threshold(confusion_matrix):
	TP = confusion_matrix[1][1]
	FN = confusion_matrix[1][0]
	FP = confusion_matrix[0][1]
	TN = confusion_matrix[0][0]
	raw_threshold = TP/(TP+FN)
	adjusted_threshold = (TP-(0.25*FP))/(TP+FN)
	return raw_threshold, adjusted_threshold

def one_off_score(y_true, y_pred):
	count = 0
	correct = 0
	one_off = 0
	for true, pred in zip(y_true, y_pred):
		if true == pred:
			correct+=1
		elif true == pred+1 or true == pred-1:
			one_off+=1
		count+=1
	one_off_adjusted = (correct + (one_off/2))/count
	one_off_full = (correct + one_off)/count
	return one_off_full, one_off_adjusted

def diversity_metrics(x_test, prediction):
	group_dict = dict()
	x = x_test.transpose()
	gender = np.unique(x[0])
	ethnicity = np.unique(x[1])
	x_test = x.transpose()
	for g in gender:
		for e in ethnicity:
			new = (g, e)
			group_dict[new]=0
	x_test = np.column_stack([x_test,prediction])

	for i in x_test:
		#print(i)
		g = i[0]
		e = i[1]
		if i[-1]==1:
			group_dict[(g,e)]+=1
		else:
			pass
	return group_dict


def Generate_Report(test_name, x_test, y_test, prediction, t_cutoff, t_aim, runtime):
	### Generates Numerical Scores
	np.set_printoptions(threshold=np.inf)
	accuracy_score_m = accuracy_score(y_test, prediction)
	offset_accuracy_score_full, offset_accuracy_score_adjusted = one_off_score(y_test, prediction)
	y_thresh_test = []
	y_thresh_pred = []
	for i in y_test:
		if i < t_aim:
			y_thresh_test.append(0)
		else:
			y_thresh_test.append(1)
	for j in prediction:
		if j < t_cutoff:
			y_thresh_pred.append(0)
		else:
			y_thresh_pred.append(1)
	confusion_matrix_raw = confusion_matrix(y_test, prediction)
	confusion_matrix_threshold = confusion_matrix(y_thresh_test, y_thresh_pred)
	threshold_raw, threshold_adjusted = confusion_to_threshold(confusion_matrix_threshold)
	div = diversity_metrics(x_test, y_thresh_pred)

	### Create Documnetation
	path = test_name
	os.mkdir(path)
	os.chdir(path)
	file = open(path, 'w')

	file.write('Test Report: '+ str(path))
	file.write('\n')
	file.write('Runtime: '+ str(runtime)+ ' seconds \n')
	file.write('\n\n\n')
	file.write('Scoring: '+ '\n')
	file.write('Accuracy Score: '+ str(accuracy_score_m)+ '\n')
	file.write('Offset Accuracy Score (Full): '+ str(offset_accuracy_score_full)+ '\n')
	file.write('Offset Accuracy Score (Adjusted): '+ str(offset_accuracy_score_adjusted)+ '\n')
	file.write('Threshold Score (Full): '+ str(threshold_raw)+ '\n')
	file.write('Threshold Score (Adjusted): '+ str(threshold_adjusted) + '\n')
	file.write('\n\n\n')
	file.write('Confusion Matrices: \n')
	file.write('Scoring Matrix: '+ str(confusion_matrix_raw)+'\n\n')
	file.write('Threshold Matrix ' + '(' + str(t_cutoff) + ', ' + str(t_aim) +'): \n' + str(confusion_matrix_threshold) + '\n\n')
	file.write('----------------------------------------------------------------------------------\n')
	file.write('----------------------------------------------------------------------------------\n')
	file.write('----------------------------------------------------------------------------------\n')
	file.write('Raw Data (For Record Keeping Purposes)--------------------------------------------\n')
	file.write('----------------------------------------------------------------------------------\n')
	file.write('----------------------------------------------------------------------------------\n')
	file.write('----------------------------------------------------------------------------------\n')
	file.write('Predicted Scores \n')
	file.write(str(prediction)+ '\n\n\n')
	file.write('Actual Scores \n')
	pd.set_option('display.max_rows', None)
	file.write(str(y_test)+ '\n\n\n')
	file.write('Predicted Thresholds \n')
	file.write(str(y_thresh_pred)+ '\n\n\n')
	file.write('Actual Thresholds \n')
	file.write(str(y_thresh_test)+ '\n\n\n')
	[file.write(str(i)+ ':'+str(j)+'\n') for i,j in zip(div.keys(), div.values())]

	file.close()

	h1_name = str(path)+'_heatmap_scores.png'
	h2_name = str(path)+'_threshold_scores.png'
	t = sns.heatmap(confusion_matrix_raw)
	t.set_ylabel('Actual')
	t.set_xlabel('Predicted')
	plt.savefig(h1_name)
	plt.clf()

	sns.heatmap(confusion_matrix_threshold, annot=True, xticklabels=["Don't Hire", 'Hire'], yticklabels=['Bad Candidate', 'Good Candidate'])
	plt.savefig(h2_name)
	plt.clf()

	return [accuracy_score_m, offset_accuracy_score_adjusted, threshold_adjusted]
