from pymongo import MongoClient
from progreporter import ProgressReporter
from operator import itemgetter

client = MongoClient()
db = client.yelp

businesses = db.business.find(timeout=False)

categories = dict()

progress = ProgressReporter()

for bz in businesses:
	cate = bz['categories']
	for c in cate:
		if not categories.has_key(c):
			categories[c] = 0
		categories[c] += 1
	progress.prog()


caterank = sorted(categories.iteritems(),key=itemgetter(1),reverse=True)

print len	(caterank)