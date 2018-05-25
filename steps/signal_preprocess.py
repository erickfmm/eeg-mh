from scipy.signal import get_window
import numpy as np

def framing(signal, size, step):
	frames = []
	start = 0
	end = size
	while end < len(signal):
		frames.append(signal[start:end])
		start += step
		end += step
	#for x in frames:
	#	print(len(x))
	return frames

def windowing_time(signal, window_type):
	w = get_window(window_type, len(signal))
	new_signal = [signal[i]*w[i] for i in range(0, len(w))]
	return new_signal

def normalize_absmax(signal):
	maxim = np.max(signal)
	minim = np.min(signal)
	absolute_max = np.abs(maxim) if np.abs(maxim) > np.abs(minim) else np.abs(minim)
	for i in range(0, len(signal)):
		signal[i] = signal[i] / float(absolute_max)
	return signal
