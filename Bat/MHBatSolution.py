import Bat.MHBatConfig as MHBatConfig
import steps.training as training

class MHBatSolution:

	def __init__(self, inputs, outputs):
		self.inputs = inputs
		self.outputs = outputs
		self.i_c = 0
		self.loundness = MHBatConfig.LOUNDNESS
		self.radio = MHBatConfig.PULSE
		self.position = []
		self.frecuency = 0.0
		self.velocity = []
		self.fitness = 0.0
		self.feasible = False

	def getPosition(self):
		return self.position

	def setPosition(self, position):
		self.position = position

	def getFrecuency(self):
		return self.frecuency

	def setFrecuency(self, frecuency):
		self.frecuency = frecuency

	def getVelocity(self):
		return self.velocity

	def setVelocity(self, velocity):
		self.velocity = velocity

	def getLoundness(self):
		return self.loundness

	def setLoundness(self, loundness):
		self.loundness = loundness

	def getRadio(self):
		return self.radio

	def setRadio(self, radio):
		self.radio = radio

	def move(self):
		accuracy = -1.0
		for i_c in range(-10, 10):
			try:
				scores = training.mifun_train(i_c, self.inputs, self.outputs, 'rbf')
				if scores.mean() > accuracy:
					accuracy = scores.mean()
					self.i_c = i_c
			except:
				print("error")
				self.feasible = False
		self.fitness = accuracy
		self.feasible = True

	def isFeasible(self):
		#move()
		return self.feasible

	def getFitness(self):
		return self.fitness
    