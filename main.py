### Import libraries
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os
import copy
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

### Imports Machine Learning Tools
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier

### Imports Helper Functions
import testing_formatting
import array_module
from machine_learning_template import *
import Generate_Report
import create_pandas

##################################################################################################################
### Create Learning Objects Here
Learn_Object_List = []
##################################################################################################################
### Random Forest Classifier
RandomForest = learn('RandomForestClassifier', RandomForestClassifier(n_estimators=20))
#n_estimators = how many forests

Learn_Object_List.append(RandomForest)

##################################################################################################################
### SVM Classifier
clf = learn('CLF', SVC())

Learn_Object_List.append(clf)

##################################################################################################################
### Neural Network
mlpc = learn('MLPC', MLPClassifier(hidden_layer_sizes = (7,7,7), max_iter=500))

Learn_Object_List.append(mlpc)

##################################################################################################################
##################################################################################################################
### Ends Learning Objects
##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
### Set Broad Test Parameters
##################################################################################################################
### Data to test file
file = 'test_advanced.csv'
### List of categorical data for processing
categorical = ['type','month','treatment','t_size','nodal_status','ER','PR','HER2_IHC','HER2_FISH','histo']
### Float data
floats=['mz', 'intensity']
### Name of success column in data
success = 'treatment'
### Restrict Data to certain variables
restriction = ['undergrad', 'lawschool']
##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
### Ends Broad Test Parameters
##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
### Training by Model
##################################################################################################################
##################################################################################################################

### import main data file
main_file = pd.read_csv("pandas_data.csv")
### Remove clinical coding and switch to binary
main_file=main_file.replace('+','1')
main_file=main_file.replace('-','0')

print(main_file['mz'].iloc[10][1])
### Converts arrays imported as lists to list-types
main_file=testing_formatting.transform_to_float(main_file, floats)

### Select Module to treat the mz and intensity data
### array_module.module(file, [Paramater List]) -> See documentation for details
### Peaks -> Collects X number of peaks
dataframe=array_module.peaks(main_file, ['mz'])
print(dataframe)
##################################################################################################################
##################################################################################################################
##################################################################################################################

### Creates compatible labels for categorical data (strings)
encoding = testing_formatting.transform_to_classes(dataframe,categorical)

### Breaks into list
testing_objects_list=testing_formatting.prepare_for_testing(encoding, success,['bank_nums','mz','intensity'])

##################################################################################################################
model_output=[]
### Training, creation of learner output objects
limit_mls = []
for model in Learn_Object_List:
	limit_mls.append(copy.deepcopy(model))
model_results = []
for ml_model in limit_mls:
	model_output.append(learner(testing_objects_list[2], testing_objects_list[0], testing_objects_list[1], ml_model))

##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################


### Output and results (See below as reference)
Compare_scoring_matrix = []
count = 0
true_score=testing_objects_list[3]

### Move to Out Folder
def get_parent_dir(directory):
    return os.path.dirname(directory)

os.chdir('out')

### For every model tested, outputs the predicted score vs the real score (as lists)
for i in model_output:
	c = 0
	t = 0
	for j,k in zip(i.prediction.tolist(),true_score.tolist()):
		if j==k:
			c+=1
		t+=1
	print(c/t)


### VISUALIZATIONS HERE










'''



print(Compare_scoring_matrix)
t = sns.heatmap(Compare_scoring_matrix, annot=True, xticklabels=['Accuracy', 'Offset', 'Threshold', 'Accuracy', 'Offset', 'Threshold'], yticklabels=['limit_s1', 'limit_s2', 'limit_s3', 'limit_n1', 'limit_n2', 'limit_n3', 'stan_1', 'stan_2', 'stan_3', 'true_1', 'true_2', 'true_3'], vmin=0, vmax=1)
t.add_patch(Rectangle((0,0), 3, 3, fill=False, edgecolor='blue', lw=3))
t.add_patch(Rectangle((0,3), 3, 3, fill=False, edgecolor='blue', lw=3))
t.add_patch(Rectangle((0,6), 3, 3, fill=False, edgecolor='blue', lw=3))
t.add_patch(Rectangle((0,9), 3, 3, fill=False, edgecolor='blue', lw=3))
t.add_patch(Rectangle((3,0), 3, 3, fill=False, edgecolor='blue', lw=3))
t.add_patch(Rectangle((3,3), 3, 3, fill=False, edgecolor='blue', lw=3))
t.add_patch(Rectangle((3,6), 3, 3, fill=False, edgecolor='blue', lw=3))
t.add_patch(Rectangle((3,9), 3, 3, fill=False, edgecolor='blue', lw=3))
t.set_xlabel('Scores')
t.set_ylabel('Models')
plt.savefig('Summary_Heatmap')
'''