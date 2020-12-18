import time

### Allows for easy packaging of machine learning and data
class learn:
	def __init__(self, name, lambda_code):
		self.name = name
		self.lambda_code = lambda_code
		self.prediction = False
		self.accuracy_score = 0
		self.classification_report = False
		self.confusion_matrix = False
		self.runtime = False
	


### Function accepts an X, Y testing and training data, and machine learning (learn class) method
### Outputs a class file with the appropriate metrics
def learner(y_train, X_train, X_test, learn_object):
	start_time = time.time()
	y_train = y_train.astype(int)
	learn_object.lambda_code.fit(X_train, y_train)
	predict = learn_object.lambda_code.predict(X_test)
	learn_object.prediction = predict
	end_time = time.time() - start_time
	learn_object.runtime = end_time
	return learn_object