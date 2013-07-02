from pymongo import MongoClient
import json

folder = '/home/ecsark/Documents/Computer/DataMining/Contest/Yelp/yelp_test_set/'

client = MongoClient()

db = client.yelp

print 'Database name: '+db.name

def insert2collection(clt_name,jf_name):
	print 'Inserting data from '+jf_name+' to '+clt_name
	n_collection = db[clt_name]
	jfile = open(folder+jf_name,'r')
	lines = jfile.readlines()
	for line in lines:
		jdata = json.loads(line.rstrip('\n'))
		n_collection.insert(jdata)
	jfile.close()
	print 'finish!'

insert2collection('business_test','yelp_test_set_business.json')
insert2collection('checkin_test','yelp_test_set_checkin.json')
insert2collection('user_test','yelp_test_set_user.json')
insert2collection('review_test','yelp_test_set_review.json')
