from PyEMD import EMD
from PyEMD import EEMD
from PyEMD import CEEMDAN
import numpy as np

def getEMDs(signal):
	emd = EMD()
	IMFs = emd(signal)
	return IMFs

def getEEMD(signal):
	eemd = EEMD()
	eIMFs = eemd(signal)
	return eIMFs

def getCEEMDAN(signal):
	ceemdan = CEEMDAN()
	cIMFs = ceemdan(signal)
	return cIMFs

def getExactSignal(signal):
	return [signal]


def getMaxComponentsEMDVariants(the_data, signals, Componentfunction):
	all_imfs = []
	imfs_sizes = []
	print("emd variant", end="")
	for iData in range(len(signals)):
		data_imfs = []
		print(iData, end=" ")
		for iChannel in range(len(signals[iData])):
			for iFrame in range(len(signals[iData][iChannel])):
				frame = signals[iData][iChannel][iFrame]
				#print(frame)
				imfs = Componentfunction(frame)
				imfs_sizes.append(len(imfs))
				data_imfs.append(imfs)
		all_imfs.append(data_imfs)
	min_imfs = np.min(imfs_sizes)
	print()
	print(min_imfs)
	#real_imfs = []
	for iData in range(len(all_imfs)):
		#data_imfs = []
		for iImfSet in range(len(all_imfs[iData])):
			for iMaxImfs in range(min_imfs):
				imf = all_imfs[iData][iImfSet][iMaxImfs]
				the_data[iData].append(imf)
		#real_imfs.append(data_imfs)
	return the_data, imfs_sizes