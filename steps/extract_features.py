import numpy as np
import sys


def get_feature_vector31_audio(signal):
	features = []
	features.append(np.median(signal))
	features.append(np.mean(signal))
	features.append(np.std(signal))
	features.append(np.min(signal))
	features.append(np.max(signal))
	features.append(np.max(signal)-np.min(signal))

	ratios = []
	first_differences = []
	last_sample = 0
	first = True
	for sample in signal:
		if first:
			last_sample = sample
			first = False
			continue
		first_differences.append(np.absolute(sample - last_sample))
		ratios.append(np.absolute(sample / last_sample))
		last_sample = sample

	features.append(np.min(first_differences))
	features.append(np.max(first_differences))

	features.append(np.min(ratios))
	features.append(np.max(ratios))

	#########################################################
	#second step
	features.append(np.median(first_differences))
	features.append(np.mean(first_differences))
	features.append(np.std(first_differences))
	features.append(np.max(first_differences)-np.min(first_differences))
	#features.append(np.min(first_differences))
	#features.append(np.max(first_differences))

	second_step_ratios = []
	second_differences = []
	last_sample = 0
	first = True
	for sample in first_differences:
		if first:
			last_sample = sample
			first = False
			continue
		second_step_ratios.append(np.absolute(sample / last_sample))
		second_differences.append(np.absolute(sample - last_sample))
		last_sample = sample

	features.append(np.min(second_differences))
	features.append(np.max(second_differences))

	features.append(np.min(second_step_ratios))
	features.append(np.max(second_step_ratios))
	#############################################################################3
	#third step
	features.append(np.median(second_differences))
	features.append(np.mean(second_differences))
	features.append(np.std(second_differences))
	features.append(np.max(second_differences)-np.min(second_differences))
	#features.append(np.min(second_differences))
	#features.append(np.max(second_differences))

	third_step_ratios = []
	third_differences = []
	last_sample = 0
	first = True
	for sample in second_differences:
		if first:
			last_sample = sample
			first = False
			continue
		third_differences.append(np.absolute(sample - last_sample))
		third_step_ratios.append(np.absolute(sample / last_sample))
		last_sample = sample

	features.append(np.min(third_differences))
	features.append(np.max(third_differences))

	features.append(np.min(third_step_ratios))
	features.append(np.max(third_step_ratios))
	features.append(np.max(third_differences)-np.min(third_differences))
	"""
	Median, mean, standard deviation, minimum, maximum, minimum, maximum ratio, and maximum and minimum difference
	first order difference and two order difference and 6
	Median, mean, standard deviation, minimum, maximum, minimum, maximum ratio, and maximum and minimum difference
	"""
	#################
	fft = np.fft.fft(signal)
	features.append(np.absolute(np.median(fft)))
	features.append(np.absolute(np.mean(fft)))
	features.append(np.absolute(np.std(fft)))
	features.append(np.absolute(np.max(fft)))
	features.append(np.absolute(np.min(fft)))
	#features.append(np.absolute(np.min(fft)+np.max(fft))) #ni idea, dice "maximum and minimum" y no sé que es y es una sola cosa o no da la cantidad ._.
	features.append(np.absolute(np.max(fft)-np.min(fft)))
	"""
	Frequency
	Median, mean, standard deviation, maximum, minimum, maximum and minimum (¿6?)
	"""
	return features



#(double[] data, int numSamples/*N*/, int wlen/*m*/, double r/*r*/, int shift)
def CalcSampleEntropy(data, numSamples, wlen, r, shift):
	A = 0
	B = 0

	i = 0
	while i < numSamples - wlen * shift - shift:
		j = i + shift
		while j < numSamples - wlen * shift - shift:
			try:
				m = 0.0
				for k in range(wlen):
					m = np.max([m, np.abs(data[i + k * shift] - data[j + k * shift])])
				if (1.0/ m < r):
					B += 1
				elif (1.0 / np.max([m, np.abs(data[i + wlen * shift] - data[j + wlen * shift])]) < r):
					A += 1
			except:
				print("error in calc sample entropy en i: %d y j: %d" % (i, j))
				print("Unexpected error:", sys.exc_info()[0])
				return 0
			j += shift
		i += shift	
	if (A > 0 and B > 0):
		return -1 * np.log( float(A) / float(B))
	else:
		return 0

def energy(signal):
	energy = 0
	for x in signal:
		energy += np.abs(x)*np.abs(x)
	return energy

def zero_crossing_rate(signal):
	zcr = 0
	for i in range(1, len(signal)):
		zcr += 0.5 * (sign(signal[i]) - sign(signal[i-1]))
	return zcr
	#return feature.zero_crossing_rate(np.array(signal))

def sign(x):
	if x >= 0:
		return 1
	else:
		return -1

def getEnergies(features, signals):
	print("energy: ", end="")
	for iData in range(len(signals)):
		print(iData, end=" ")
		for iSignal in range(len(signals[iData])):
			features[iData].append(energy(signals[iData][iSignal]))
	print()
	return features

def getSampleEntropies(features, signals, numSamples, wlen, r, shift):
	print("sample entropy: ", end="")
	for iData in range(len(signals)):
		print(iData, end=" ")
		for iSignal in range(len(signals[iData])):
			features[iData].append(CalcSampleEntropy(signals[iData][iSignal], numSamples, wlen, r, shift))
	print()
	return features