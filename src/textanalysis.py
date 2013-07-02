from pymongo import MongoClient
import nltk
import numpy as np
import matplotlib.pyplot as plt

client = MongoClient()
db = client.yelp


def textlen_avgscore(param = 'info_len'):
	restaurants = db.restaurant.find({})

	tlength = list()
	tscore = list()

	counter = 0
	for res in restaurants:
		tlength.append(res[param])
		tscore.append(res['score']['useful'])

		counter += 1
		if counter%1000 == 0:
			print counter

	minlen = min(tlength)
	maxlen = max(tlength)

	X = range(minlen,maxlen+1)
	Y = [0]*(maxlen-minlen+1)
	Z = [0]*(maxlen-minlen+1)

	for (tl,ts) in zip(tlength,tscore):
		Y[tl-minlen] += ts
		Z[tl-minlen] += 1

	avg = [0]*(maxlen-minlen+1)

	for idx in range(maxlen+1-minlen):
		if Z[idx] == 0:
			avg[idx] = avg[idx-1]
		else:
			avg[idx] = float(Y[idx])/Z[idx]


	#avg = np.divide(Y,Z)

	plt.scatter(X, avg)
	plt.show()

def userprofile_score():
	restaurants = db.restaurant.find({})

	useruse = list()
	score = list()

	counter = 0
	for res in restaurants:
		useruse.append(res['user_votes']['useful'])
		score.append(res['score']['useful'])
		counter += 1
		if counter%1000 == 0:
			print counter


	plt.scatter(useruse,score)
	plt.show()

#textlen_avgscore('info_len')
userprofile_score()