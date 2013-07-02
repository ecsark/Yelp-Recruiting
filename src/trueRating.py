# -*- coding: utf-8 -*-  
from pymongo import MongoClient
from nltk import sent_tokenize, word_tokenize, pos_tag, FreqDist
import nltk
tagger = nltk.data.load(nltk.tag._POS_TAGGER)
import string
from progreporter import ProgressReporter
import numpy as np
from sklearn.decomposition import RandomizedPCA

client = MongoClient()
db = client.yelp

class ProgressReporter():
	def __init__(self,interval=10000):
		self.counter = 0
		self.interval = interval

	def prog(self):
		self.counter += 1
		if self.counter%self.interval == 0:
			print self.counter

def addVotes2Bz():
	progress = ProgressReporter(1000)

	business = db.business.find()

	counter = 0

	for bz in business:
		review = db.review.find({'business_id':bz['business_id']})
		votes = {'useful':0,'funny':0,'cool':0}
		for rev in review:
			votes['useful'] += rev['votes']['useful']
			votes['funny'] += rev['votes']['funny']
			votes['cool'] += rev['votes']['cool']
		db.business.update({'_id':bz['_id']}, {"$set": {"votes": votes}})
		progress.prog()

def makeRestaurant():
	business = db.business.find({'categories':'Restaurants'},{'business_id':1,'stars':1,'review_count':1,'_id':0})

	counter = 0
	skip = 0

	for bz in business:
		reviews = db.review.find({'business_id':bz['business_id']},{'_id':0,'type':0})
		for rev in reviews:
			rev['bz_stars'] = bz['stars']
			rev['bz_reviews'] = bz['review_count']
			usr = db.user.find_one({'user_id':rev['user_id']})
			if usr is None:
				skip += 1
				continue
			
			rev['user_reviews'] = usr['review_count']
			rev['user_stars'] = usr['average_stars']
			rev['user_votes'] = usr['votes']
			db.restaurant.insert(rev)
			counter += 1
			if counter%200 == 0:
				print counter

	print 'skip:'+str(skip)
	print 'counter:'+str(counter)


def addVotes2Restaurant():
	business = db.business.find({'categories':'Restaurants'},{'_id':0,'votes':1,'business_id':1})

	counter = 0
	for bz in business:
		review = db.restaurant.find({'business_id':bz['business_id']})
		for rev in review:
			db.restaurant.update({'_id':rev['_id']},{"$set": {"bz_votes": bz['votes']}})
		counter += 1
		if counter%100 == 0:
			print counter


def addScore2Restaurant():
	review = db.restaurant.find()

	def calcScore(rev,score,prop):
		score[prop] = float(rev['votes'][prop] + 1)*rev['bz_reviews']/(rev['bz_votes'][prop] + 1)

	counter = 0

	for rev in review:
		score = {}
		calcScore(rev,score,'useful')
		calcScore(rev,score,'funny')
		calcScore(rev,score,'cool')
		db.restaurant.update({'_id':rev['_id']},{"$set": {"score": score}})
		counter += 1
		if counter%200 == 0:
			print counter


def addTextlen(collection):
	progress = ProgressReporter()
	reviews = collection.find({},{'text':1})
	counter = 0

	stopwords = set(nltk.corpus.stopwords.words('english'))
	evenmore = [',','.',"'ll","n't","'s"]
	for more in evenmore:
		stopwords.add(more)

	for rev in reviews:
		text = rev['text']
		text_len = len(nltk.word_tokenize(text))
		info_len = len(set(nltk.word_tokenize(text))-stopwords)
		collection.update({'_id':rev['_id']},{"$set": {"text_len": text_len,"info_len": info_len}})
		progress.prog()


def addCheckin2Business(business,checkin):	
	progress = ProgressReporter(1000)
	businesses = business.find()
	nocheckin = 0
	for bz in businesses:
		ck = checkin.find_one({'business_id':bz['business_id']})
		if ck is None:
			#print 'Checkin info not found for '+ bz['business_id']
			nocheckin += 1
			continue
		checkinfo = ck['checkin_info']
		cksum = sum(checkinfo.itervalues())
		business.update({'_id':bz['_id']},{'$set':{'checkins':cksum}})
		checkin.update({'_id':ck['_id']},{'$set':{'sum':cksum}})
		progress.prog()
	print 'updated checkins :' + str(progress.counter)
	print 'absent checkins: '+str(nocheckin)





def posAnalysis(collection):

	reviews = collection.find(timeout=False)

	__reportProgress.counter = 0

	skip = 1

	for rev in reviews:
		if skip%200 == 0:
			print 'skip'+str(skip)
		__reportProgress()
		if rev.has_key('tags'):
			skip += 1
			if rev['tags'].has_key('NN'):				
				continue

		sents = sent_tokenize(rev['text'])
		tokens = [word for sent in sents for word in word_tokenize(sent)]
		pos = tagger.tag([tok for tok in tokens if tok not in ',.-$\" '])
		tag_fd = FreqDist(tag for (word, tag) in pos)
		tags = dict()
		for (key,value) in tag_fd.items():
			k = key.replace('$','S')
			out = key.translate(string.maketrans("",""), string.punctuation)
			if len(out)>0:
				tags[k] = value
		collection.update({'_id':rev['_id']},{"$set": {"tags": tags}})		
		


#addVotes2Bz()

#makeRestaurant()

#addVotes2Restaurant()

#addScore2Restaurant()

addTextlen(db.review_test)

#posAnalysis(db.review_test)

#addCheckin2Business(db.business_test,db.checkin_test)