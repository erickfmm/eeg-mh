import steps.helper as helper
import steps.denoise as denoise
import steps.training as training
import steps.extract_features as extractFeatures
import steps.get_data as getData
import steps.segment_signal as segmentSignal
import steps.optimization as optimization
import steps.get_components as getComponents
import steps.get_deap as getDeap
import pickle
import numpy as np
import asyncio
import sys
import Bat.MHBat as metaheurBat
import multiprocessing
import collections
import copy


def getCleaned():
	print("to read files")
	datas = getDeap.getDataDeap('./data_preprocessed_python/')
	print("files readed, len: "+str(len(datas)))
	print("to extract features")
	inputs = []
	outputs = []
	i = 1
	segment_exact_indexed_signals = []
	#clean_signals = []
	the_data = []
	names = []
	for data in datas:
		outputs.append(data['tag'])
		the_data.append([])
		inputs.append([])
		min_length = 4234
		max_length = 5386
		#f3 = segmentSignal.get_exact_index_segment(data['data']['f3'], min_length, max_length)
		#c4 = segmentSignal.get_exact_index_segment(data['data']['c4'], min_length, max_length)
		#segment_exact_indexed_signals.append([[f3], [c4]])
	pickle.dump(the_data, open("the_data.pkl", "wb"))
	pickle.dump(outputs, open("outputs.pkl", "wb"))
	pickle.dump(inputs, open("inputs.pkl", "wb"))
	#sys.exit()
	print("te save exact")
	pickle.dump(segment_exact_indexed_signals, open("segment_exact_indexed_signals.pkl", "wb"))
	print("to clean")
	wavelet = denoise.wavelet_all_frames(segment_exact_indexed_signals, 'db5')
	beta = denoise.butter_all_frames(segment_exact_indexed_signals, 12.5, 30, fs=128, order=4)
	theta = denoise.butter_all_frames(segment_exact_indexed_signals, 4, 7, fs=128, order=4)
	beta_opt = denoise.butter_all_frames(segment_exact_indexed_signals, 16, 31, fs=128, order=4)
	beta1 = denoise.butter_all_frames(segment_exact_indexed_signals, 12.5, 16.0, fs=128, order=4)
	beta2 = denoise.butter_all_frames(segment_exact_indexed_signals, 16.5, 20, fs=128, order=4)
	beta3 = denoise.butter_all_frames(segment_exact_indexed_signals, 20.5, 28, fs=128, order=4)
	alpha = denoise.butter_all_frames(segment_exact_indexed_signals, 8.0, 15.0, fs=128, order=4)
	clean_signals = [segment_exact_indexed_signals, wavelet, beta, beta1, beta2, beta3, alpha, theta, beta_opt]
	cleaned = {"exact": segment_exact_indexed_signals, "wavelet": wavelet, "beta": beta, "beta1": beta1, "beta2": beta2, "beta3": beta3, "alpha": alpha, "theta": theta, "beta_opt": beta_opt}
	print("to pickle")
	pickle.dump(cleaned, open("cleaned.pkl", "wb"))
	pickle.dump(clean_signals, open("clean_signals.pkl", "wb"))
	pickle.dump(wavelet, open("wavelet.pkl", "wb"))
	pickle.dump(beta1, open("beta1.pkl", "wb"))
	pickle.dump(beta2, open("beta2.pkl", "wb"))
	pickle.dump(beta3, open("beta3.pkl", "wb"))
	pickle.dump(beta, open("beta.pkl", "wb"))
	pickle.dump(alpha, open("alpha.pkl", "wb"))
	pickle.dump(theta, open("theta.pkl", "wb"))
	pickle.dump(beta_opt, open("beta_opt.pkl", "wb"))
	print("aaaaall saved")
	return clean_signals

def getComps(the_args):
	the_data =  copy.deepcopy(the_args["the_data"])
	cleaned = the_args["cleaned"]
	func = the_args["func"]
	iClean = the_args["iClean"]
	namefunc = the_args["namefunc"]
	names = []
	#the_data, sizes = getComponents.getMaxComponentsEMDVariants(the_data, cleaned, func)
	#print(the_data)
	for iData in range(len(the_data)):
		the_data[iData].append([1, 2, 4])
		the_data[iData].append([5, 4, 8])
	sizes = [1, 2, 67, -4]
	names.extend([str(iClean)+"_"+namefunc] * int(np.min(sizes)) * 2)
	return {
	"data": the_data,
	"sizes": sizes,
	"names": names
	}

def append_the_data(the_data, the_data2):
	for iData in range(len(the_data)):
		for iData2 in range(len(the_data2[iData])):
			the_data[iData].append(the_data2[iData][iData2])
	return the_data

def procccMult(the_args):
	iClean = the_args["iClean"]
	cleaned = the_args["cleaned"]
	the_data = copy.deepcopy(the_args["the_data"])
	pool = multiprocessing.Pool()
	the_args = [{
	"the_data": the_data,
	"cleaned": cleaned,
	"func": getComponents.getExactSignal,
	"iClean": iClean,
	"namefunc": "exact",
	},{
	"the_data": the_data,
	"cleaned": cleaned,
	"func": getComponents.getEMDs,
	"iClean": iClean,
	"namefunc": "emd",
	},{
	"the_data": the_data,
	"cleaned": cleaned,
	"func": getComponents.getEEMD,
	"iClean": iClean,
	"namefunc": "eemd",
	},{
	"the_data": the_data,
	"cleaned": cleaned,
	"func": getComponents.getCEEMDAN,
	"iClean": iClean,
	"namefunc": "ceemdan",
	}]
	#names = []
	res = pool.map(getComps, the_args)
	names = [val for l in res for val in l["names"]]
	for the_data2 in res:
		append_the_data(the_data, the_data2["data"])
	return {"names": names, "data": the_data}

def getFeatsPool():
	#pool = multiprocessing.Pool()
	the_data = pickle.load(open("the_data.pkl", "rb"))
	clean_signals = pickle.load(open("clean_signals.pkl", "rb"))
	#to_data = []
	#res = []
	for iClean in range(len(clean_signals)):
		my_data = {
		"iClean": iClean,
		"cleaned": clean_signals[iClean],
		"the_data": the_data# copy.deepcopy(the_data)
		}
		#to_data.append(my_data)
		#res.append(procccMult(to_data))
		the_data = procccMult(my_data)["data"]
		#append_the_data(the_data, the_data2["data"])
	#res = pool.map(procccMult, to_data)
	#for the_data2 in res:
		#append_the_data(the_data, the_data2["data"])
	print(the_data)

#def getAlFeats(the_data):


def getFeatures():
	#clean_signals = getCleaned()
	the_data = pickle.load(open("the_data.pkl", "rb"))
	clean_signals = pickle.load(open("clean_signals.pkl", "rb"))
	for iClean in range(len(clean_signals)):
		print("obteniendo componentes para limpieza: ", end="")
		print(iClean)
		print("exact")
		the_data, imf_sizes_exact = getComponents.getMaxComponentsEMDVariants(the_data, clean_signals[iClean], getComponents.getExactSignal)
		print("emd")
		the_data, imf_sizes_emd = getComponents.getMaxComponentsEMDVariants(the_data, clean_signals[iClean], getComponents.getEMDs)
		#print("eemd")
		#the_data, imf_sizes_eemd = getComponents.getMaxComponentsEMDVariants(the_data, clean_signals[iClean], getComponents.getEEMD)
		#print("ceemdan")
		#the_data, imf_sizes_ceemdan = getComponents.getMaxComponentsEMDVariants(the_data, clean_signals[iClean], getComponents.getCEEMDAN)
		name_file = "the_data_comps_untilclean_"+str(iClean)+".pkl"
		pickle.dump(the_data, open(name_file, "wb"))
		names.extend([str(iClean)+"_"+"exact"] * int(np.min(imf_sizes_exact)) * 2)
		names.extend([str(iClean)+"_"+"emd"] * int(np.min(imf_sizes_emd)) * 2)
		#names.extend([str(iClean)+"_"+"eemd"] * int(np.min(imf_sizes_eemd)) * 2)
		#names.extend([str(iClean)+"_"+"ceemdan"] * int(np.min(imf_sizes_ceemdan)) * 2)
	#names_clean = []
	#for iClean in range(len(clean_signals)):
	#	for iNames in range(len(names)):
	#		names_clean.append(str(iClean)+"_"+str(names[iNames]))
	#names = names * iClean
	
	#names = names_clean
	print("a obtener energia")
	extractFeatures.getEnergies(inputs, the_data)
	print("a obtener sample entropy")
	extractFeatures.getSampleEntropies(inputs, the_data, 128, 2, 0.15, 1)
	#names = names * 2
	names_feat = []
	for iNames in range(len(names)):
		names_feat.append(str(names[iNames])+"_energy")

	for iNames in range(len(names)):
		names_feat.append(str(names[iNames])+"_sampleentropy")
	names = names_feat

	with open("names.txt", "w") as namesFile:
		namesFile.write(str(names))
	with open("features.txt", "w") as featsFile:
		featsFile.write(str(inputs))
	with open("outputs.txt", "w") as outsFile:
		outsFile.write(str(outputs))
	return inputs, outputs
	#the_data, imf_sizes = getComponents.getMaxComponentsEMDVariants(the_data, segment_exact_indexed_signals, getComponents.getEMDs)
	#the_data, imf_sizes2 = getComponents.getMaxComponentsEMDVariants(the_data, segment_exact_indexed_signals, getComponents.getEEMD)
	#print(the_data[0])
	#print(len(the_data[0]))
	#print(len(the_data[1]))
	#print(len(the_data[2]))
	#print(len(the_data))
	#print(len(the_data[1][0]))
	#print(imf_sizes)
	#sys.exit()
	#for data in datas:
		#print("Processing input: %d Percentage: %0.1f%% of secs: %0.2f" % (i, i*100/len(datas), len(data['data']['f3'])/128))
		#cA = denoise.denoise_butterworth(data['data'])
		#cA = denoise.denoise_wavelet(cA)
		
		#f3 = segmentSignal.get_exact_index_segment(data['data']['f3'], min_length, max_length)
		#c4 = segmentSignal.get_exact_index_segment(data['data']['c4'], min_length, max_length)
		#f3 = denoise.butter_bandpass_filter(f3, 4.0, 45.0, 128, order=4)
		#c4 = denoise.butter_bandpass_filter(c4, 4.0, 45.0, 128, order=4)
		#imfsF3 = getComponents.getEMDs(f3)
		#imfsC4 = getComponents.getEMDs(c4)
		#print("length f3 imfs: "+str(len(imfsF3)))
		#print("length c4 imfs: "+str(len(imfsC4)))
		#features = []
		#if(len(imfsF3) >= 4 and len(imfsC4) >= 4):
		#	for iImfs in range(4):
		#		features.append(extractFeatures.CalcSampleEntropy(imfsF3[iImfs], 128, 2, 0.15, 1))
		#		features.append(extractFeatures.CalcSampleEntropy(imfsC4[iImfs], 128, 2, 0.15, 1))
		#		
		#extracted_signal = segmentSignal.get_middle_seconds(cA, 30, 256)
		#features = extractFeatures.get_feature_vector(extracted_signal)
		#sub_features = [features[2], 
		#	features[4], 
		#	features[6], 
		#	features[7], 
		#	features[8], 
		#	features[9], 
		#	features[10], 
		#	features[14], 
		#	features[15], 
		#	features[16], 
		#	features[17], 
		#	features[18], 
		#	features[22], 
		#	features[23], 
		#	features[27] ]
		#inputs.append(features)
		#outputs.append(data['tag'])
		#outputs.append(int(np.random.uniform(5)))
		#i += 1
	#print("inputs len: "+str(len(inputs)))
	#print("inputs[0] len: "+str(len(inputs[0])))
	#print("outputs len: "+str(len(outputs)))
	
	#print("to learn")
	#optimization.all_combinations_of_features(inputs, outputs, classification.svm_rbf)

	#loop = asyncio.get_event_loop()

	
	#try:
	#	for i_c in range(-10, 10):
	#		loop.run_until_complete(training.mifun_train(i_c, inputs, outputs, 'rbf'))
	#finally:
	#	loop.close()
	#print("bai bai")
	
	# Save to file in the current working directory
	#pkl_filename = "pickle_model.pkl"  
	#with open(pkl_filename, 'wb') as file:  
	#    pickle.dump(model, file)

if __name__ == '__main__':
	getFeatsPool()
	#getCleaned()
	#inputs, outputs = getFeatures()
	#metaheurBat.run(inputs, outputs)
