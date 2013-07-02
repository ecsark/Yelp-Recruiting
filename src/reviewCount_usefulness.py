from pymongo import MongoClient
import numpy as np
import matplotlib.pyplot as plt

client = MongoClient()
db = client.yelp

results = db.user.find({},{'user_id':1,'review_count':1,'votes.useful':1,'_id':0})

review_count = list()
useful_count = list()

for res in results:
	review_count.append(res['review_count'])
	useful_count.append(res['votes']['useful'])

plt.scatter(review_count, useful_count)

plt.show()


"""
f = open('/home/ecsark/Documents/Computer/DataMining/Contest/Yelp/data/reviewCount_usefulness.csv','wb')
for res in results:
	#f.write(res['user_id']+','+str(res['review_count'])+','+str(res['votes']['useful'])+'\n')
	f.write(str(res['review_count'])+','+str(res['votes']['useful'])+'\n')
f.close()
"""
