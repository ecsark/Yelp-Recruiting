breviews = db.review.find({'business_id':'_1QQZuf4zZOyFCvXc0o6Vg'})
texts = list()
rvids = list()
for rv in breviews:
	texts.append(rv['text'])
	rvids.append(rv['review_id'])
nouns = list()
for t in texts:
	pos = tagger.tag(word_tokenize(t))
	noun = [p[0] for p in pos if p[1] in ['NNP','NN','NNPS']]
	nsent = string.join(noun)
	nouns.append(nsent)
vectorizer = CountVectorizer(min_df=1,stop_words='english')
nvec = vectorizer.fit_transform(nouns)

pca = RandomizedPCA(n_components=math.sqrt(len(texts)))
X = pca.fit_transform(nvec)

for i in range(len(rvids)):
	rvid = rvids[i]
	db.review.update({'review_id':rvid},{"$set": {"tfidf": X[i].tolist()}})



votes = list()
votesall = list()
for rvid in rvids:
	rv = db.review.find_one({'review_id':rvid})
	votes.append(rv['votes']['useful'])
	votesall.append(rv['votes']['useful']+rv['votes']['cool']+rv['votes']['funny'])