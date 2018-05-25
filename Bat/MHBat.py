import numpy as np
import Bat.MHBatConfig as MHBatConfig
import Bat.MHBatSolution as MHBatSolution
import Bat.MHFeatureConfig as MHFeatureConfig
import Bat.Distribution as Distribution
import Bat.BinarizationStrategy as BinarizationStrategy

swarm = None
bestBat = None
newBat = None


t = 0
position = []
velocity = []
fitnessBats = None
inputs = []
outputs = []

def showResults():
	with open("fitness.txt", "w") as fitnessFile:
		fitnessFile.write(str(fitnessBats))
	with open("bat.txt", "w") as batsFile:
		batsFile.write("position = "+str(bestBat.getPosition()))
		batsFile.write("fitness = "+str(bestBat.getFitness()))
		batsFile.write("loudness = "+str(bestBat.getLoundness()))
		batsFile.write("radio = "+str(bestBat.getRadio()))
		batsFile.write("velocity = "+str(bestBat.getVelocity()))
		batsFile.write("frecuency = "+str(bestBat.getFrecuency()))

def newRandomBat():
	newBat = MHBatSolution(inputs, outputs)
	while True:
		position = []
		velocity = []
		for i in range(MHFeatureConfig.DIMENSION):
			position.append(Distribution.uniform(0, 2))
			velocity.append(position[i])
		newBat.setVelocity(velocity)
		newBat.setPosition(position)
		newBat.move()
		if newBat.isFeasible():
			break
	return newBat

def initialBatPopulation():
	swarm = []
	fitnessBats = []
	for i in range(MHBatConfig.T):
		fitnessBats.append(0)
	t = 0
	for i in range(MHBatConfig.N):
		newBat = newRandomBat()
		swarm.append(newBat)
	bestBat = swarm[0]

def chooseBestBat():
	for batInSwarm in swarm:
		if batInSwarm.getFitness() < bestBat.getFitness():
			bestBat = batInSwarm
	fitnessBats[t] = bestBat.getFitness();


def averageLoundness():
	avgLoundness = 0.0
	for batInSwarm in swarm:
		avgLoundness += arm.getLoundness()
	return avgLoundness / float(len(swarm))

def randomWalk():
	i = -1
	for batInSwarm in swarm:
		if Distribution.uniform() + 1 < batInSwarm.getLoundness() and bestBat.getFitness() > batInSwarm.getFitness():
			batInSwarm.setLoundness(MHBatConfig.ALPHA * batInSwarm.getLoundness())
			batInSwarm.setRadio(batInSwarm.getRadio() * (1 - Math.exp(-MHBatConfig.GAMMA * (t + 1))))
			i += 1
	bestBat = swarm[i] if i >=0 else bestBat



def changeLocationBat():
	#newBat = MHBatSolution()
	beta = 0
	for batInSwarm in swarm:
		while True:
			if batInSwarm != bestBat:
				#newBat = batInSwarm
				position = batInSwarm.getPosition()
				velocity = batInSwarm.getVelocity()

				if Distribution.uniform() > batInSwarm.getRadio():
					for i in range(MHFeatureConfig.DIMENSION):
						position[i] = BinarizationStrategy.toBinary(position[i] + MHBatConfig.EPSILON * averageLoundness())

				beta = Distribution.uniform()
				if Distribution.uniform() < batInSwarm.getLoundness() and batInSwarm.getFitness() < bestBat.getFitness():
					batInSwarm.setFrecuency(MHBatConfig.QMIN + (MHBatConfig.QMAX - MHBatConfig.QMIN) * beta)
					for i in range(MHFeatureConfig.DIMENSION):
						velocity[i] = velocity[i] + ((bestBat.getPosition()[i] - position[i]) * batInSwarm.getFrecuency())
						position[i] = BinarizationStrategy.toBinary(position[i] + velocity[i])
					batInSwarm.setVelocity(velocity)
					batInSwarm.setPosition(position)
					batInSwarm.move()
			if batInSwarm.isFeasible():
				break
		if batInSwarm.getFitness() < bestBat.getFitness():
			bestBat = batInSwarm

def run(inputs, outputs):
	inputs = inputs
	outputs = outputs
	initialBatPopulation()
    while (t < MHBatConfig.T):
        randomWalk()
        chooseBestBat()
        changeLocationBat()
        t += 1
    showResults()