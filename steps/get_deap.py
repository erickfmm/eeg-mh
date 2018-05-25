import pickle
import os
import sys
from os.path import join

#folderToSearch = '../data_preprocessed_python/'
number_tags = {
	"Todo": 0,
	"LALV": 0,
	"LAHV": 0,
	"HALV": 0,
	"HAHV": 0#,
	#"YoLALV": 0,
	#"YoLAHV": 0,
	#"YoHALV": 0,
	#"YoHAHV": 0
}
def process_file(root, file, ifile, data):
	print(join(root, file))
	x = pickle.load(open(join(root, file), 'rb'), encoding='bytes')
	#print(x)
	for itrial in range(0, len(x[b'data'])):
		sessid = (ifile * 100) + itrial
		valence = x[b'labels'][itrial][0]
		arousal = x[b'labels'][itrial][1]
		dominance = x[b'labels'][itrial][2]
		liking = x[b'labels'][itrial][3]
		f3 = x[b'data'][itrial][2]
		c4 = x[b'data'][itrial][24]
		number_tags["Todo"] += 1
		if arousal < 5.5 and valence < 5.5:
			number_tags["LALV"] += 1
			emo = 0
			data.append({'tag': emo, 'data': {'f3': f3, 'c4': c4}, 'session': sessid})
			#LALV
		if arousal < 5.5 and valence >= 5.5:
			number_tags["LAHV"] += 1
			emo = 1
			data.append({'tag': emo, 'data': {'f3': f3, 'c4': c4}, 'session': sessid})
			#LAHV
		if arousal >= 5.5 and valence < 5.5:
			number_tags["HALV"] += 1
			emo = 2
			data.append({'tag': emo, 'data': {'f3': f3, 'c4': c4}, 'session': sessid})
			#HALV
		if arousal >= 5.5 and valence >= 5.5:
			number_tags["HAHV"] += 1
			emo = 3
			data.append({'tag': emo, 'data': {'f3': f3, 'c4': c4}, 'session': sessid})
				#HAHV

			#if (arousal <= 5 and valence < 5) or ((arousal > 5 and arousal < 6) and (valence > 5 and valence < 6)):
			#	number_tags["YoLALV"] += 1
			#	write_sql("YoLALV", f3, c4, sessid)
			#if arousal < 5 and valence >= 5:
			#	number_tags["YoLAHV"] += 1
			#	write_sql("YoLAHV", f3, c4, sessid)
			#if arousal >= 6 and valence <= 5:
			#	number_tags["YoHALV"] += 1
			#	write_sql("YoHALV", f3, c4, sessid)
			#if arousal >= 5 and valence >= 6:
			#	number_tags["YoHAHV"] += 1
			#	write_sql("YoHAHV", f3, c4, sessid)

def process_all(data, folderToSearch):
	ifile = 0
	for root, dirs, files in os.walk(folderToSearch):
		for file in files:
			if file.lower().endswith('.dat'):
				process_file(root, file, ifile,data)
				ifile = ifile + 1
				if ifile >= 2:
					return data
				#print(data)
	return data


def getDataDeap(folderToSearch):
	data = process_all([], folderToSearch)
	print(number_tags)
	return data

#if __name__ == '__main__':
#	print(number_tags)
#	data = process_all([])
#	print(len(data))
#	print(number_tags)