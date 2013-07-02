from pymongo import MongoClient
import nltk

client = MongoClient()
db = client.yelp

reviews = db.restaurant.find().sort([('score.useful',1),('bz_reviews',-1)]).limit(20)


f = open('/home/ecsark/Documents/Computer/DataMining/Contest/Yelp/data/examples_bad.txt','wb')
for rev in reviews:
	f.write('score:' + "%.2f" % rev['score']['useful'] + ', ')
	f.write('useful:' + str(rev['votes']['useful']) + ', ')
	f.write('funny:' + str(rev['votes']['funny']) + ', ')
	f.write('cool:' + str(rev['votes']['cool']) + ', ')
	f.write('stars:' + str(rev['stars']) + '/' + str(rev['bz_stars']) + '\n')
	f.write('bz_reviews:' + str(rev['bz_reviews']) + ', ')
	f.write('user_stars:' + str(rev['user_stars']) + ', ')
	f.write('user_votes:' + str(rev['user_votes']) + '\n')
	f.write(rev['text'] + '\n\n\n')

f.close()
