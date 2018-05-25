import steps.learning_model as l_model

async def mifun_train(i_c, inputs, outputs, kernel, degree=3, gamma='auto'):
		model, scores = l_model.train_svm(inputs, outputs, kernel, 2**i_c, degree=degree, gamma=gamma)
		print(str(i_c)+kernel+" Accuracy: %0.3f. Standard Deviation: %0.3f" % (scores.mean(), scores.std()))
		print(scores)

async def mifun_train_linear(i_c, inputs, outputs):
		model, scores = l_model.train_svm_linear(inputs, outputs, 2**i_c)
		print(str(i_c)+"Linear Accuracy: %0.3f. Standard Deviation: %0.3f" % (scores.mean(), scores.std()))
		print(scores)

async def mifun_train_mlp(inputs, outputs):
		model, scores = l_model.train_MLP(inputs, outputs)
		print("MLP Accuracy: %0.3f. Standard Deviation: %0.3f" % (scores.mean(), scores.std()))
		print(scores)
