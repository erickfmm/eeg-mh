from sklearn import svm
from sklearn.model_selection import cross_val_score
from sklearn import neural_network

def train_svm(inputs, outputs, kernel, C, degree, gamma):
	clf = svm.SVC(kernel=kernel, C=C, degree=degree, gamma=gamma)
	scores = cross_val_score(clf, inputs, outputs, cv=10)
	model = clf.fit(inputs, outputs)
	return model, scores

def train_svm_linear(inputs, outputs, C):
	clf = svm.LinearSVC(C=C)
	scores = cross_val_score(clf, inputs, outputs, cv=10)
	model = clf.fit(inputs, outputs)
	return model, scores

def classify(model, input):
	return model.predict([input])[0]

def train_MLP(inputs, outputs):
	clf = neural_network.MLPClassifier()
	scores = cross_val_score(clf, inputs, outputs, cv=10)
	model = clf.fit(inputs, outputs)
	return model, scores
