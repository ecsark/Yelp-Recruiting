from pymongo import MongoClient
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn import cross_validation
from sklearn import metrics
import numpy as np
import math
from operator import itemgetter
from progreporter import ProgressReporter

class FeatureLoader(object):

	def __init__(self):
		client = MongoClient()
		self.db = client.yelp
		self.X = list()
		self.Y = list()
		self.cities = dict()
		self.initCategory()
		self.progress = ProgressReporter()


	def initCategory(self):
		businesses = self.db.business.find()
		categories = dict()
		for bz in businesses:
			cate = bz['categories']
			for c in cate:
				if not categories.has_key(c):
					categories[c] = 0
				categories[c] += 1
		self.caterank = sorted(categories.iteritems(),key=itemgetter(1),reverse=True)
		self.categories = [r[0] for r in self.caterank]
		print 'Category initialized'


	def getCategory(self,cateList):
		if len(cateList) == 0:
			return -1.0
		rank = []
		for c in cateList:
			if c in self.categories:
				rank.append(self.categories.index(c))

		if len(rank) == 0:
			return -1.0
		rank.sort()
		cate = rank[0]
		if len(rank)>1:
			cate += float(rank[1])/1000
		return cate


	def getTextPos(self,sample,rev):
		tag_fd = rev['tags']
		tagsum = 10.0
		if len(tag_fd) > 0:
			tagsum = float(sum(tag_fd.values()))
		#else:
			#print 'tag_fd len zero: '+ rev['review_id']

		#depreciated
		def __dictValue(tagName):
			if tag_fd.has_key(tagName):
				return float(tag_fd[tagName])
			else:
				return float(0)

		def add(tagNames, divisor=tagsum):
			if divisor==0:
				print 'divisor zero: '+ rev['review_id']
				divisor = 10
			count = 0.0
			for t in tagNames:
				if tag_fd.has_key(t):
					count += tag_fd[t]
			sample.append(count/divisor)

		#nouns
		add(['NN','NNS'])
		add(['NNP','NNPS'])
		#personal
		add(['PRP','PRPS'])

		#adjectives and adverbs
		add(['RB','RBR','RBS'])
		add(['JJ','JJR','JJS'])
		add(['RBR','JJR'])
		add(['RBS','JJS'])

		#determiners, conjunctions and pre-determiner
		add(['DT'])
		add(['CC'])
		add(['PDT'])

		#verbs
		vcollection = ['VB','VBD','VBG','VBN','VBP','VBZ']
		vcount = sum([tag_fd[t] for t in vcollection if tag_fd.has_key(t)])
		add(['VB','VBD','VBG','VBN','VBP','VBZ'])
		add(['VB','VBP'])
		add(['VBD','VBN'])

		#Wh-
		add(['WRB'])
		#modal auxiliary
		add(['MD'])

	
	def addUserVotes(self,sample,usr):
		sample.append(usr['votes']['useful'])
		sample.append(usr['votes']['useful']+usr['votes']['funny']+usr['votes']['cool'])
		sample.append(usr['votes']['useful']/usr['review_count'])
		sample.append((usr['votes']['useful']+usr['votes']['funny']+usr['votes']['cool'])/usr['review_count'])

	def addUserFeature(self,sample,usr):
		sample.append(usr['review_count'])
		sample.append(usr['average_stars'])

	def getCity(self,city):		
		if not self.cities.has_key(city):
			(self.cities)[city] = len(self.cities)
		return self.cities[city]

	def addBzVotes(self,sample,bz):
		sample.append(bz['votes']['useful'])
		totalvotes = bz['votes']['useful']+bz['votes']['funny']+bz['votes']['cool']		
		sample.append(totalvotes)
		if totalvotes == 0:
			sample.append(-1.0)
		else:
			sample.append(float(bz['votes']['useful'])/totalvotes)		

	def addBzFeature(self,sample,bz):
		sample.append(bz['review_count'])
		sample.append(bz['stars'])
		sample.append(self.getCity(bz['city']))
		sample.append(self.getCategory(bz['categories']))
		if bz.has_key('checkins'):
			sample.append(bz['checkins'])
		else:
			sample.append(0)

	def addReviewFeature(self,sample,rev):
		sample.append(rev['info_len'])
		sample.append(rev['text_len'])
		if rev['text_len'] == 0:
			sample.append(-1.0)
		else:
			sample.append(float(rev['text_len']-rev['info_len'])/rev['text_len'])
		sample.append(rev['stars'])
		sample.append(int(rev['date'].replace('-','')))
		self.getTextPos(sample,rev)

	def loadFeature(self,loadBzVotes=True,loadUsr=True,loadUsrVotes=True):
		reviews = self.db.restaurant.find(timeout=False)

		for rev in reviews:
			rev = self.db.review.find_one({'review_id':rev['review_id']})
			sample = list()
			bz = self.db.business.find_one({'business_id':rev['business_id']})			
			self.addReviewFeature(sample,rev)
			self.addBzFeature(sample,bz)
			if loadBzVotes:
				self.addBzVotes(sample,bz)
			if loadUsr:
				usr = self.db.user.find_one({'user_id':rev['user_id']})
				if usr is None:
					continue
				self.addUserFeature(sample,usr)
				if loadUsrVotes:
					self.addUserVotes(sample,usr)

			sample.append((float(bz['stars']-rev['stars'])))
			if loadUsr:
				sample.append((float(usr['average_stars']-rev['stars'])))
				sample.append((float(usr['average_stars']-bz['stars'])))
			
			self.X.append(sample)
			self.Y.append(math.log(rev['votes']['useful']+1))
			self.progress.prog()
		print 'Loading feature done!'


if __name__ == '__main__':
	loader = FeatureLoader()
	loader.loadFeature()
	X = np.asarray(loader.X)
	Y = np.asarray(loader.Y)

	print 'Loading data done!'
	#clf = RandomForestClassifier(n_estimators=100)
	#clf = RandomForestRegressor(n_estimators=100,verbose=1,n_jobs=2,max_features=None,compute_importances=True)
	clf = SVR(C=1.0, epsilon=0.2, tol = 1e-2, max_iter=10000)
	#clf.fit(X,Y)

	#print clf.feature_importances_

	
	scores = cross_validation.cross_val_score(clf,X,Y,cv=3,n_jobs=2,score_func=metrics.mean_squared_error)

	lscores = np.sqrt(scores)

	print lscores

	stsum = 0

	for sc in lscores:
		stsum += sc

	if len(lscores)>0:
		print stsum/len(lscores)
	