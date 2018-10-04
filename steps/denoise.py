import pywt
from scipy.signal import butter, lfilter

def denoise_wavelet(signal, type_wavelet='db5'):
	cA, cD = pywt.dwt(signal, type_wavelet)
	return cA

def butter_bandpass(lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=4):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def pre_emphasis(signal, alpha):
	new_signal = []
	new_signal.append(signal[0] - alpha * signal[0])
	for i in range(1, len(signal)):
		new_signal.append(signal[i] - alpha * signal[i-1])
		#new_signal.append(1 - alpha * (1/signal[i]))
	return new_signal


def butter_all_frames(signals, lowcut, highcut, fs, order=4):
	print("butter: ", end="")
	newSignals = []
	for iData in range(len(signals)):
		print(iData, end=" ")
		newSignals.append([])
		for iChannel in range(len(signals[iData])):
			newSignals[iData].append([])
			for iFrame in range(len(signals[iData][iChannel])):
				#frame = signals[iData][iChannel][iFrame]
				newSignals[iData][iChannel].append([])
				newSignals[iData][iChannel][iFrame] = butter_bandpass_filter(signals[iData][iChannel][iFrame], lowcut, highcut, fs, order)
	return newSignals

def wavelet_all_frames(signals, type_wavelet='db5'):
	print("wavelet: ", end="")
	newSignals = []
	for iData in range(len(signals)):
		print(iData, end=" ")
		newSignals.append([])
		for iChannel in range(len(signals[iData])):
			newSignals[iData].append([])
			for iFrame in range(len(signals[iData][iChannel])):
				#frame = signals[iData][iChannel][iFrame]
				newSignals[iData][iChannel].append([])
				newSignals[iData][iChannel][iFrame] = denoise_wavelet(signals[iData][iChannel][iFrame], type_wavelet)
	print()
	return newSignals

def preemphasis_all_frames(signals, alpha):
	newSignals = []
	for iData in range(len(signals)):
		print([iData])
		newSignals.append([])
		for iChannel in range(len(signals[iData])):
			newSignals[iData].append([])
			for iFrame in range(len(signals[iData][iChannel])):
				#frame = signals[iData][iChannel][iFrame]
				newSignals[iData][iChannel].append([])
				newSignals[iData][iChannel][iFrame] = pre_emphasis(signals[iData][iChannel][iFrame], alpha)
	return newSignals