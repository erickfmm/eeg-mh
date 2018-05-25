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

if __name__ == '__main__':
	print("to read files")
	datas = getDeap.getDataDeap('./data_preprocessed_python/')
	print("files readed, len: "+str(len(datas)))
	print("to extract features")
	inputs = []
	outputs = []
	i = 1
	segment_exact_indexed_signals = []
	clean_signals = []
	the_data = []
	names = []
	for data in datas:
		outputs.append(data['tag'])
		the_data.append([])
		inputs.append([])
		min_length = 4234
		max_length = 5386
		f3 = segmentSignal.get_exact_index_segment(data['data']['f3'], min_length, max_length)
		c4 = segmentSignal.get_exact_index_segment(data['data']['c4'], min_length, max_length)
		segment_exact_indexed_signals.append([[f3], [c4]])
	wavelet = denoise.wavelet_all_frames(segment_exact_indexed_signals, 'db5')
	beta = denoise.butter_all_frames(segment_exact_indexed_signals, 12.5, 30, fs=128, order=4)
	beta1 = denoise.butter_all_frames(segment_exact_indexed_signals, 12.5, 16.0, fs=128, order=4)
	beta2 = denoise.butter_all_frames(segment_exact_indexed_signals, 16.5, 20, fs=128, order=4)
	beta3 = denoise.butter_all_frames(segment_exact_indexed_signals, 20.5, 28, fs=128, order=4)
	alpha = denoise.butter_all_frames(segment_exact_indexed_signals, 8.0, 12.0, fs=128, order=4)
	clean_signals = [segment_exact_indexed_signals, wavelet, beta, beta1, beta2, beta3, alpha]
	for iClean in range(len(clean_signals)):
		print("obteniendo componentes para limpieza: ", end="")
		print(iClean)
		print("exact")
		the_data, imf_sizes_exact = getComponents.getMaxComponentsEMDVariants(the_data, clean_signals[iClean], getComponents.getExactSignal)
		print("emd")
		the_data, imf_sizes_emd = getComponents.getMaxComponentsEMDVariants(the_data, clean_signals[iClean], getComponents.getEMDs)
		print("eemd")
		the_data, imf_sizes_eemd = getComponents.getMaxComponentsEMDVariants(the_data, clean_signals[iClean], getComponents.getEEMD)
		print("ceemdan")
		the_data, imf_sizes_ceemdan = getComponents.getMaxComponentsEMDVariants(the_data, clean_signals[iClean], getComponents.getCEEMDAN)
	names.extend(["exact"] * imf_sizes_exact)
	names.extend(["emd"] * imf_sizes_emd)
	names.extend(["eemd"] * imf_sizes_eemd)
	names.extend(["ceemdan"] * imf_sizes_ceemdan)
	names_clean = []
	for iClean in range(len(clean_signals)):
		for iNames in range(len(names)):
			names_clean.append(str(iClean)+"_"+str(names[iNames]))
	#names = names * iClean
	
	names = names_clean
	print("a obtener energia")
	extractFeatures.getEnergies(inputs, the_data)
	print("a obtener sample entropy")
	extractFeatures.getSampleEntropies(inputs, the_data, 128, 2, 0.15, 1)
	names = names * 2
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
	print("inputs len: "+str(len(inputs)))
	print("inputs[0] len: "+str(len(inputs[0])))
	print("outputs len: "+str(len(outputs)))
	
	print("to learn")
	#optimization.all_combinations_of_features(inputs, outputs, classification.svm_rbf)

	loop = asyncio.get_event_loop()

	
	try:
		for i_c in range(-10, 10):
			loop.run_until_complete(training.mifun_train(i_c, inputs, outputs, 'rbf'))
	finally:
		loop.close()
	print("bai bai")
	
	# Save to file in the current working directory
	#pkl_filename = "pickle_model.pkl"  
	#with open(pkl_filename, 'wb') as file:  
	#    pickle.dump(model, file)