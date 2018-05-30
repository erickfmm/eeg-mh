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



def getCs(signal, inputs, imfs_emd, min_emd, imfs_eemd, min_eemd, imfs_ceemdan, min_ceemdan, names, i, name_type):
	print(name_type)
	inputs[i].append(extractFeatures.energy(signal))
	inputs[i].append(extractFeatures.CalcSampleEntropy(signal, 128, 2, 0.15, 1))
	if i == 0:
		names.append(name_type+"_energy")
		names.append(name_type+"_sampentropy")
	emd = getComponents.getEMDs(signal)
	if len(emd) < min_emd:
		min_emd = len(emd)
		for iClean in range(len(imfs_emd)):
			for iEmd in range(len(imfs_emd[iClean])):
				imfs_emd[iClean][iEmd] = imfs_emd[iClean][iEmd][0:min_emd]
	elif len(emd) > min_emd:
		emd = emd[0:min_emd]
	imfs_emd[i].append(emd)
	#
	eemd = getComponents.getEEMD(signal)
	if len(eemd) < min_eemd:
		min_eemd = len(eemd)
		for iClean in range(len(imfs_eemd)):
			for iEemd in range(len(imfs_eemd[iClean])):
				imfs_eemd[iClean][iEemd] = imfs_eemd[iClean][iEemd][0:min_eemd]
	elif len(eemd) > min_eemd:
		eemd = eemd[0:min_eemd]
	imfs_eemd[i].append(eemd)
	#
	ceemdan = getComponents.getCEEMDAN(signal)
	if len(ceemdan) < min_ceemdan:
		min_ceemdan = len(ceemdan)
		for iClean in range(len(imfs_ceemdan)):
			for iCeemdan in range(len(imfs_ceemdan[iClean])):
				imfs_ceemdan[iClean][iCeemdan] = imfs_ceemdan[iClean][iCeemdan][0:min_ceemdan]
	elif len(ceemdan) > min_ceemdan:
		ceemdan = ceemdan[0:min_ceemdan]
	imfs_ceemdan[i].append(ceemdan)
	return inputs, imfs_emd, min_emd, imfs_eemd, min_eemd, imfs_ceemdan, min_ceemdan, names
	




def getFeatures():
	print("to read files")
	datas = getDeap.getDataDeap('./data_preprocessed_python/')
	print("files readed, len: "+str(len(datas)))
	print("to extract features")
	inputs = []
	outputs = []
	i = 0
	#segment_exact_indexed_signals = []
	clean_signals = []
	the_data = []
	names = []

	imfs_emd = []
	min_emd = 1000
	
	imfs_eemd = []
	min_eemd = 1000
	
	imfs_ceemdan = []
	min_ceemdan = 1000
	for data in datas:
		print("reading data: "+str(i)+" of a total: "+str(len(datas))+", so "+str(i/float(len(datas)) * 100.0)+"%")
		outputs.append(data['tag'])
		the_data.append([])
		inputs.append([])
		imfs_emd.append([])
		imfs_eemd.append([])
		imfs_ceemdan.append([])
		min_length = 4234
		max_length = 5386
		f3 = segmentSignal.get_exact_index_segment(data['data']['f3'], min_length, max_length)
		c4 = segmentSignal.get_exact_index_segment(data['data']['c4'], min_length, max_length)
		#segment_exact_indexed_signals.append([[f3], [c4]])
		## Clean
		#none
		f3_d = f3
		c4_d = c4
		inputs, imfs_emd, min_emd, imfs_eemd, min_eemd, imfs_ceemdan, min_ceemdan, names = getCs(f3_d, inputs, imfs_emd, min_emd, imfs_eemd, min_eemd, imfs_ceemdan, min_ceemdan, names, i, "f3_none")
		inputs, imfs_emd, min_emd, imfs_eemd, min_eemd, imfs_ceemdan, min_ceemdan, names = getCs(c4_d, inputs, imfs_emd, min_emd, imfs_eemd, min_eemd, imfs_ceemdan, min_ceemdan, names, i, "c4_none")
		
		#wavelet
		f3_d = denoise.denoise_wavelet(f3, 'db5')
		c4_d = denoise.denoise_wavelet(c4, 'db5')

		inputs, imfs_emd, min_emd, imfs_eemd, min_eemd, imfs_ceemdan, min_ceemdan, names = getCs(f3_d, inputs, imfs_emd, min_emd, imfs_eemd, min_eemd, imfs_ceemdan, min_ceemdan, names, i, "f3_wavelet")
		inputs, imfs_emd, min_emd, imfs_eemd, min_eemd, imfs_ceemdan, min_ceemdan, names = getCs(c4_d, inputs, imfs_emd, min_emd, imfs_eemd, min_eemd, imfs_ceemdan, min_ceemdan, names, i, "c4_wavelet")

		#beta
		f3_d = denoise.butter_bandpass_filter(f3, 12.5, 30, fs=128, order=4)
		c4_d = denoise.butter_bandpass_filter(c4, 12.5, 30, fs=128, order=4)

		inputs, imfs_emd, min_emd, imfs_eemd, min_eemd, imfs_ceemdan, min_ceemdan, names = getCs(f3_d, inputs, imfs_emd, min_emd, imfs_eemd, min_eemd, imfs_ceemdan, min_ceemdan, names, i, "f3_beta")
		inputs, imfs_emd, min_emd, imfs_eemd, min_eemd, imfs_ceemdan, min_ceemdan, names = getCs(c4_d, inputs, imfs_emd, min_emd, imfs_eemd, min_eemd, imfs_ceemdan, min_ceemdan, names, i, "c4_beta")
		#beta1
		f3_d = denoise.butter_bandpass_filter(f3, 12.5, 16.0, fs=128, order=4)
		c4_d = denoise.butter_bandpass_filter(c4, 12.5, 16.0, fs=128, order=4)

		inputs, imfs_emd, min_emd, imfs_eemd, min_eemd, imfs_ceemdan, min_ceemdan, names = getCs(f3_d, inputs, imfs_emd, min_emd, imfs_eemd, min_eemd, imfs_ceemdan, min_ceemdan, names, i, "f3_beta1")
		inputs, imfs_emd, min_emd, imfs_eemd, min_eemd, imfs_ceemdan, min_ceemdan, names = getCs(c4_d, inputs, imfs_emd, min_emd, imfs_eemd, min_eemd, imfs_ceemdan, min_ceemdan, names, i, "c4_beta1")
		#beta2
		f3_d = denoise.butter_bandpass_filter(f3, 16.5, 20, fs=128, order=4)
		c4_d = denoise.butter_bandpass_filter(c4, 16.5, 20, fs=128, order=4)

		inputs, imfs_emd, min_emd, imfs_eemd, min_eemd, imfs_ceemdan, min_ceemdan, names = getCs(f3_d, inputs, imfs_emd, min_emd, imfs_eemd, min_eemd, imfs_ceemdan, min_ceemdan, names, i, "f3_beta2")
		inputs, imfs_emd, min_emd, imfs_eemd, min_eemd, imfs_ceemdan, min_ceemdan, names = getCs(c4_d, inputs, imfs_emd, min_emd, imfs_eemd, min_eemd, imfs_ceemdan, min_ceemdan, names, i, "c4_beta2")
		#beta3
		f3_d = denoise.butter_bandpass_filter(f3, 20.5, 28, fs=128, order=4)
		c4_d = denoise.butter_bandpass_filter(c4, 20.5, 28, fs=128, order=4)

		inputs, imfs_emd, min_emd, imfs_eemd, min_eemd, imfs_ceemdan, min_ceemdan, names = getCs(f3_d, inputs, imfs_emd, min_emd, imfs_eemd, min_eemd, imfs_ceemdan, min_ceemdan, names, i, "f3_beta3")
		inputs, imfs_emd, min_emd, imfs_eemd, min_eemd, imfs_ceemdan, min_ceemdan, names = getCs(c4_d, inputs, imfs_emd, min_emd, imfs_eemd, min_eemd, imfs_ceemdan, min_ceemdan, names, i, "c4_beta3")
		#alpha
		f3_d = denoise.butter_bandpass_filter(f3, 8.0, 12.0, fs=128, order=4)
		c4_d = denoise.butter_bandpass_filter(c4, 8.0, 12.0, fs=128, order=4)

		inputs, imfs_emd, min_emd, imfs_eemd, min_eemd, imfs_ceemdan, min_ceemdan, names = getCs(f3_d, inputs, imfs_emd, min_emd, imfs_eemd, min_eemd, imfs_ceemdan, min_ceemdan, names, i, "f3_alpha")
		inputs, imfs_emd, min_emd, imfs_eemd, min_eemd, imfs_ceemdan, min_ceemdan, names = getCs(c4_d, inputs, imfs_emd, min_emd, imfs_eemd, min_eemd, imfs_ceemdan, min_ceemdan, names, i, "c4_alpha")
		i += 1
	print("processed, now to insert emds")
	print("emd")
	for iData in range(len(imfs_emd)):
		for iClean in range(len(imfs_emd[iData])):
			for iImf in range(len(imfs_emd[iData][iClean])):
				inputs[iData].append(extractFeatures.energy(imfs_emd[iData][iClean][iImf]))
				inputs[iData].append(extractFeatures.CalcSampleEntropy(imfs_emd[iData][iClean][iImf], 128, 2, 0.15, 1))
				if iData == 0:
					names.append("channel"+str(iClean%2)+"_clean"+str(int(iClean/2))+"_emd_energy_cleanraw"+str(iClean))
					names.append("channel"+str(iClean%2)+"_clean"+str(int(iClean/2))+"_emd_sampentropy_cleanraw"+str(iClean))
	print("eemd")
	for iData in range(len(imfs_eemd)):
		for iClean in range(len(imfs_eemd[iData])):
			for iImf in range(len(imfs_eemd[iData])):
				inputs[iData].append(extractFeatures.energy(imfs_eemd[iData][iClean][iImf]))
				inputs[iData].append(extractFeatures.CalcSampleEntropy(imfs_eemd[iData][iClean][iImf], 128, 2, 0.15, 1))
				if iData == 0:
					names.append("channel"+str(iClean%2)+"_clean"+str(int(iClean/2))+"_eemd_energy_cleanraw"+str(iClean))
					names.append("channel"+str(iClean%2)+"_clean"+str(int(iClean/2))+"_eemd_sampentropy_cleanraw"+str(iClean))
	print("cemdan")
	for iData in range(len(imfs_ceemdan)):
		for iClean in range(len(imfs_ceemdan[iData])):
			for iImf in range(len(imfs_ceemdan[iData][iClean])):
				inputs[iData].append(extractFeatures.energy(imfs_ceemdan[iData][iClean][iImf]))
				inputs[iData].append(extractFeatures.CalcSampleEntropy(imfs_ceemdan[iData][iClean][iImf], 128, 2, 0.15, 1))
				if iData == 0:
					names.append("channel"+str(iClean%2)+"_clean"+str(int(iClean/2))+"_ceemdan_energy_cleanraw"+str(iClean))
					names.append("channel"+str(iClean%2)+"_clean"+str(int(iClean/2))+"_ceemdan_sampentropy_cleanraw"+str(iClean))
	print("ready all processing, to write")
	print("----------------------------------------------------------------")
	#wavelet = denoise.wavelet_all_frames(segment_exact_indexed_signals, 'db5')
	#beta = denoise.butter_all_frames(segment_exact_indexed_signals, 12.5, 30, fs=128, order=4)
	#beta1 = denoise.butter_all_frames(segment_exact_indexed_signals, 12.5, 16.0, fs=128, order=4)
	#beta2 = denoise.butter_all_frames(segment_exact_indexed_signals, 16.5, 20, fs=128, order=4)
	#beta3 = denoise.butter_all_frames(segment_exact_indexed_signals, 20.5, 28, fs=128, order=4)
	#alpha = denoise.butter_all_frames(segment_exact_indexed_signals, 8.0, 12.0, fs=128, order=4)
	#clean_signals = [segment_exact_indexed_signals, wavelet, beta, beta1, beta2, beta3, alpha]
	#for iClean in range(len(clean_signals)):
	#	print("obteniendo componentes para limpieza: ", end="")
	#	print(iClean)
	#	print("exact")
	#	the_data, imf_sizes_exact = getComponents.getMaxComponentsEMDVariants(the_data, clean_signals[iClean], getComponents.getExactSignal)
	#	print("emd")
	#	the_data, imf_sizes_emd = getComponents.getMaxComponentsEMDVariants(the_data, clean_signals[iClean], getComponents.getEMDs)
	#	print("eemd")
	#	the_data, imf_sizes_eemd = getComponents.getMaxComponentsEMDVariants(the_data, clean_signals[iClean], getComponents.getEEMD)
	#	print("ceemdan")
	#	the_data, imf_sizes_ceemdan = getComponents.getMaxComponentsEMDVariants(the_data, clean_signals[iClean], getComponents.getCEEMDAN)
	#names.extend(["exact"] * int(np.min(imf_sizes_exact)))
	#names.extend(["emd"] * int(np.min(imf_sizes_emd)))
	#names.extend(["eemd"] * int(np.min(imf_sizes_eemd)))
	#names.extend(["ceemdan"] * int(np.min(imf_sizes_ceemdan)))
	#names_clean = []
	#for iClean in range(len(clean_signals)):
	#		for iNames in range(len(names)):
	#		names_clean.append(str(iClean)+"_"+str(names[iNames]))
	#names = names * iClean
	
	#names = names_clean
	#print("a obtener energia")
	#extractFeatures.getEnergies(inputs, the_data)
	#print("a obtener sample entropy")
	#extractFeatures.getSampleEntropies(inputs, the_data, 128, 2, 0.15, 1)
	#names = names * 2
	#names_feat = []
	#for iNames in range(len(names)):
	#	names_feat.append(str(names[iNames])+"_energy")
	#
	#for iNames in range(len(names)):
	#	names_feat.append(str(names[iNames])+"_sampleentropy")
	#names = names_feat

	with open("names.txt", "w") as namesFile:
		namesFile.write(str(names))
	with open("features.txt", "w") as featsFile:
		featsFile.write(str(inputs))
	with open("outputs.txt", "w") as outsFile:
		outsFile.write(str(outputs))
	print("to return")
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
	inputs, outputs = getFeatures()
	metaheurBat.run(inputs, outputs)
