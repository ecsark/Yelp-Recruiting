"""

10702 of 22956 testing reviews lack business info in training db
1205 of 5585 businesses in testing reviews do not exist in training db
but all businesses can be found in either training/testing db

9109 of 22956 test reviews lack user info in training db
1448 of them lack user info in either training/testing db
5710 of 11926 users in testing reviews do not exist in training db
605 of them are completely private users

"""

from pymongo import MongoClient
import nltk

client = MongoClient()
db = client.yelp

test = db.review_test.find()

na_bz = list()
na_usr = list()
bs = set()
us = set()

for t in test:
	bz = db.business.find_one({'business_id':t['business_id']})
	if bz is None:
		bz = db.business_test.find_one({'business_id':t['business_id']})
		if bz is None:
			na_bz.append(t['business_id'])
	usr = db.user.find_one({'user_id':t['user_id']})
	if usr is None:
		usr = db.user_test.find_one({'user_id':t['user_id']})
		if usr is None:
			na_usr.append(t['user_id'])

	bs.add(t['business_id'])
	us.add(t['user_id'])


print len(na_bz),len(set(na_bz))
print len(na_usr),len(set(na_usr))
print len(bs)
print len(us)