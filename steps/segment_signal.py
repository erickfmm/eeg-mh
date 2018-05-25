

#gsr, 6, 256
def get_middle_seconds(signal, seconds, frequency):
	half_seconds = seconds/2
	min = int(len(signal)/2-(frequency*half_seconds))
	max = int(len(signal)/2+(frequency*half_seconds))
	return signal[min:max]

def get_exact_index_segment(signal, min_length, max_length):
	if(len(signal) < max_length):
		raise Exception("not enough elements in signal")
	length = max_length - min_length
	newSignal = signal[min_length:max_length]
	if(len(newSignal) == length):
		return newSignal
	else:
		raise Exception("different length in signal")