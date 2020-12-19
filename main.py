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
from machine_learning_template import *

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
main_file=main_file.replace('+','1')
main_file=main_file.replace('-','0')
print(main_file.iloc[0])
dataframe=main_file

### We run combination to objects, feature adjustments, and conversion to pandas here

##################################################################################################################
##################################################################################################################
##################################################################################################################

encoding = testing_formatting.transform_to_classes(dataframe,categorical)
testing_objects_list=testing_formatting.prepare_for_testing(encoding, success,['bank_nums','mz','intensity'])

##################################################################################################################
testing_list=[]
model_output=[]
### Training, creation of learner output objects
limit_mls = []
for model in Learn_Object_List:
	limit_mls.append(copy.deepcopy(model))
model_results = []
for ml_model in limit_mls:
	model_output.append(learner(testing_objects_list[2], testing_objects_list[0], testing_objects_list[1], ml_model))
testing_list.append(model_output)

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

main = get_parent_dir(os.getcwd())
os.chdir(main)
os.chdir('out')

for lisp in testing_list:
	for model in lisp:
		test_name = 'test_list_'+str(count)+'_' + model.name + '.txt'
		temp1 = Generate_Report.Generate_Report(test_name, test_normalized[1], y_test_n_s, model.prediction, 6, 4, model.runtime)
		count+=1
		temp_dir = get_parent_dir(os.getcwd())
		os.chdir(temp_dir)
		test_name = 'test_list_'+str(count)+'_' + model.name + '.txt'
		temp2 = Generate_Report.Generate_Report(test_name, test_normalized[1], y_test_normal, model.prediction, 6, 4, model.runtime)
		count+=1
		temp = temp1 + temp2
		temp_dir = get_parent_dir(os.getcwd())
		os.chdir(temp_dir)
		Compare_scoring_matrix.append(temp)

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