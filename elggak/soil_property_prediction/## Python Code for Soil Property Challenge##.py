## Python Code for Soil Property Challenge##
import numpy as np
import math
import os
import sys
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

def load_into_file(path, Header=True):
	File = open(path, 'r')
	lines = File.readlines()
	data = []
	features = []
	if Header is True:
		for feature in lines[0].split(',')[1:3595]:
			features.append(feature)
	PIDN = []
	Ca = []
	P = []
	pH = []
	SOC = []
	Sand = []
	count = 0
	for line in lines[1:]:
		sample = []
		values = line.split(',')
		PIDN.append(values[0])
		for val in values[1:3594]:
			sample.append(val)
		if values[3594] == "Topsoil":
			sample.append(1)
		else:
			sample.append(0)
		data.append(sample)
		Ca.append(values[3595])
		P.append(values[3596])
		pH.append(values[3597])
		SOC.append(values[3598])
		Sand.append(values[3599])
	return PIDN, features, data, Ca, P, pH, SOC, Sand

if __name__ == "__main__":
	path = "/home/manu/Documents/elggak/soil_property_prediction/training.csv"
	PIDN, features, data, Ca, P, pH, SOC, Sand = load_into_file(path)
	data_array = np.array(data)
	print data_array.shape
	pca = PCA(n_components = '1157')
	X_r = pca.fit(data).transform(data)
	# print(len(pca.explained_variance_ratio_))
	# print len(data[0]), len(Sand)
	# plt.plot(Sand)
	# plt.show()