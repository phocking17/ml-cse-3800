### Transforms dataframes into testing dataframes
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def transform_to_classes(data, parameter_list):
	for parameter in parameter_list:
		le = LabelEncoder()
		data[parameter] = le.fit_transform(data[parameter])
	return data

def prepare_for_testing(dataframe, success_category, drop_columns_list=None, select_columns_list = None):
	X = dataframe.drop(success_category, axis=1)
	if drop_columns_list is None:
		pass
	else:
		for selection in drop_columns_list:
			X = X.drop(selection, axis=1)
	if select_columns_list is None:
		pass
	else:
		X = dataframe[select_columns_list]
	y = dataframe[success_category]
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
	sc = StandardScaler()
	X_train = sc.fit_transform(X_train)
	X_test = sc.transform(X_test)
	return [X_train, X_test, y_train, y_test]