from pymongo import MongoClient
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import math

client = MongoClient()
db = client.yelp

def reviewCount_usefulness():
	results = db.user.find({},{'user_id':1,'review_count':1,'votes.useful':1,'_id':0})

	review_count = list()
	useful_count = list()

	for res in results:
		review_count.append(res['review_count'])
		useful_count.append(res['votes']['useful'])

	plt.scatter(review_count, useful_count)
	plt.show()


def reviewCount_avgusefulness():
	results = db.restaurant.find()

	review_count = list()
	useful_count = list()

	for res in results:
		review_count.append(res['user_reviews'])
		useful_count.append(float(res['score']['useful'])/res['user_reviews'])

	plt.scatter(review_count, useful_count)
	plt.show()

def usefulDistribution():
	reviews = db.review.find({},{'votes.useful':1,'_id':0}).sort('votes.useful',-1)
	max_count = reviews[0]['votes']['useful']
	count = [0] * (max_count + 1)
	for rev in reviews:
		count[rev['votes']['useful']] += 1

	plt.bar(range(max_count+1),count)
	plt.show()


def restaurantRatingDeviation():
	reviews = db.restaurant.find()
	deviation = list()
	score = list()
	devdict = dict()
	for rev in reviews:
		dev = rev['stars'] - rev['bz_stars']
		if dev not in devdict.keys():
			devdict[dev] = (0,0)
		num = devdict[dev][0]
		votes = devdict[dev][1]
		devdict[dev] = (num+1, votes+rev['score']['useful'])

	useful_count=list()
	for k in devdict.keys():
		deviation.append(k)
		useful_count.append(float(devdict[k][1])/devdict[k][0])

	plt.bar(deviation,useful_count, width = 0.25)
	plt.show()


def usefulDistribution():
	reviews = db.review.find({},{'votes.useful':1,'_id':0}).sort('votes.useful',-1)
	max_count = reviews[0]['votes']['useful']
	count = [0] * (max_count + 1)
	for rev in reviews:
		count[rev['votes']['useful']] += 1

	plt.bar(range(max_count+1),count)
	plt.show()


def ratingDeviation():
	reviews = db.review.find()
	busienss_col = db.business.find({},{'business_id':1,'stars':1,'_id':0})

	business = dict()

	for bz in busienss_col:
		business[bz['business_id']] = bz['stars']


	
	deviation = list()
	useful_count = list()

	"""
	for res in reviews:
		useful_count.append(res['votes']['useful'])
		deviation.append(abs(res['stars'] - business[res['business_id']]))

	plt.scatter(useful_count,deviation)
	"""

	devdict = dict()
	for rev in reviews:
		dev = rev['stars'] - business[rev['business_id']]
		if dev not in devdict.keys():
			devdict[dev] = (0,0)

		num = devdict[dev][0]
		votes = devdict[dev][1]
		devdict[dev] = (num+1, votes+rev['votes']['useful']+rev['votes']['funny']+rev['votes']['cool'])



	for k in devdict.keys():
		deviation.append(k)
		useful_count.append(float(devdict[k][1])/devdict[k][0])

	plt.bar(deviation,useful_count, width = 0.25)
	plt.show()


def scoreDistribution(pace = 0.2):
	restaurants = db.restaurant.find()

	scores = list()

	for res in restaurants:
		scores.append(res['score']['useful'])

	max_score = max(scores)
	gpnum = int(max_score/pace) + 1
	count = [0]*gpnum

	for sc in scores:
		count[int(sc/pace)] += 1

	plt.bar(range(gpnum),count)
	plt.show()


def votes2date():
	reviews = db.review.find()
	scores = list()
	date = list()
	for rev in reviews:
		d = int(rev['date'].replace('-',''))
		year = d/10000
		d = d-year*10000
		month = d/100
		day = d-100*month
		s = (datetime(year,month,day)-datetime(2005,1,1)).total_seconds()
		date.append(s)
		v = rev['votes']
		scores.append(v['useful']+v['funny']+v['cool'])
	plt.scatter(date,scores)
	plt.show()


def singlevotes2date():
	reviews = db.review.find({'business_id':'hW0Ne_HTHEAgGF1rAdmR-g'})
	scores = list()
	date = list()
	for rev in reviews:
		d = int(rev['date'].replace('-',''))
		year = d/10000
		d = d-year*10000
		month = d/100
		day = d-100*month
		s = (datetime(year,month,day)-datetime(2005,1,1)).total_seconds()
		date.append(s)
		v = rev['votes']
		scores.append(v['useful']+v['funny']+v['cool'])
	plt.scatter(date,scores)
	plt.show()

reviewCount_usefulness()
#reviewCount_avgusefulness()
#usefulDistribution()
#restaurantRatingDeviation()
#ratingDeviation()
#scoreDistribution(pace = 0.1)
#votes2date()
#singlevotes2date()