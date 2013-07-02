from pymongo import MongoClient
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import math
from progreporter import ProgressReporter
from regressor import FeatureLoader
import cPickle
import csv

class TestDataLoader(FeatureLoader):
	def __init__(self):		
		self.XX = [list() for i in range(6)] #input
		self.DD = [dict() for i in range(6)] #id
		self.map = dict()
		self.map[(False,False,False)] = 0
		self.map[(False,True,False)] = 1
		self.map[(False,True,True)] = 2
		self.map[(True,False,False)] = 3
		self.map[(True,True,False)] = 4
		self.map[(True,True,True)] = 5
		FeatureLoader.__init__(self)


	def loadFeature(self):
		reviews = self.db.review_test.find(timeout=False)
		for rev in reviews:
			sample = list()
			self.addReviewFeature(sample,rev)

			bv, u, uv = True, True, True

			bz = self.db.business.find_one({'business_id':rev['business_id']})
			if bz is None:
				bz = self.db.business_test.find_one({'business_id':rev['business_id']})
				bv = False
			self.addBzFeature(sample,bz)
			if bv:
				self.addBzVotes(sample,bz)

			usr = self.db.user.find_one({'user_id':rev['user_id']})
			if usr is None:
				uv = False
				usr = self.db.user_test.find_one({'user_id':rev['user_id']})
				if usr is None:
					u = False

			if u:
				self.addUserFeature(sample,usr)
				if uv:
					self.addUserVotes(sample,usr)

			sample.append((float(bz['stars']-rev['stars'])))
			if u:
				sample.append((float(usr['average_stars']-rev['stars'])))
				sample.append((float(usr['average_stars']-bz['stars'])))
			
			model_id = self.map[(bv,u,uv)]
			self.XX[model_id].append(sample)
			idx = len(self.DD[model_id])
			self.DD[model_id][rev['review_id']] = idx
			self.progress.prog()
		print 'Loading feature done!'


def trainModel(name,loadBzVotes=True,loadUsr=True,loadUsrVotes=True):
	features = FeatureLoader()
	features.loadFeature(loadBzVotes,loadUsr,loadUsrVotes)
	clf = RandomForestRegressor(n_estimators=100,verbose=1,n_jobs=2)

	clf.fit(np.asarray(features.X),np.asarray(features.Y))

	with open(model_dir+name+'.pkl','wb') as mod:
		cPickle.dump(clf,mod)


def loadModel(name):
	mod = open(model_dir+name+'.pkl','rb')
	model = cPickle.load(mod)
	mod.close()
	return model


model_dir = '/home/ecsark/Documents/Computer/DataMining/Contest/Yelp/src/model/'

#trainModel('bv1u1uv1',loadBzVotes=True,loadUsr=True,loadUsrVotes=True)
#trainModel('bv0u0uv0',loadBzVotes=False,loadUsr=False,loadUsrVotes=False)
#trainModel('bv0u1uv1',loadBzVotes=False,loadUsr=True,loadUsrVotes=True)
trainModel('bv1u0uv0',loadBzVotes=True,loadUsr=False,loadUsrVotes=False)
trainModel('bv1u1uv0',loadBzVotes=True,loadUsr=True,loadUsrVotes=False)
trainModel('bv0u1uv0',loadBzVotes=False,loadUsr=True,loadUsrVotes=False)

models = list()

loader = TestDataLoader()
loader.loadFeature()
print [len(x) for x in loader.XX]

modname = ['bv0u0uv0','bv0u1uv0','bv0u1uv1','bv1u0uv0','bv1u1uv0','bv1u1uv1']

YY = list()

for i in range(6):
	print 'Predicting model...'
	X = np.asarray(loader.XX[i])
	model = loadModel(modname[i])
	Y = model.predict(X)
	YY.append(list(Y))

templatefile = open('/home/ecsark/Documents/Computer/DataMining/Contest/Yelp/sample_submission.csv','rb')
template = csv.reader(templatefile)
submission = open('/home/ecsark/Documents/Computer/DataMining/Contest/Yelp/submission.csv','wb')
csvwriter = csv.writer(submission)
for row in template:
	revid = row[0]
	for i in range(6):
		index = loader.DD[i]
		if index.has_key(revid):
			score = YY[i][index[revid]]
			csvwriter.writerow((revid,math.exp(score)-1))
			break
	else:
		print revid + ' not found!'

submission.close()
templatefile.close()
