//Most useful reviewers
db.user.find({},{'votes.useful':1,'user_id':1,'_id':0}).sort({'votes.useful':-1}).limit(20)
------------------------------------------------------------------------------------------
{ "votes" : { "useful" : 24293 }, "user_id" : "DrKQzBFAvxhyjLgbPSW2Qw" }
{ "votes" : { "useful" : 23863 }, "user_id" : "w6Vv-kldGpmvSGqXvTbAdQ" }
{ "votes" : { "useful" : 23412 }, "user_id" : "qbfQRHLvZk5WSkKY0l_lMw" }
{ "votes" : { "useful" : 23080 }, "user_id" : "J3rNWRLRuZJ_0xsJalIhlA" }
{ "votes" : { "useful" : 21214 }, "user_id" : "8E0DGec8LNn6oDmPHmj-mg" }
{ "votes" : { "useful" : 20762 }, "user_id" : "xNb8pFe99ENj8BeMsCBPcQ" }
{ "votes" : { "useful" : 20648 }, "user_id" : "1h2Zmu7R9IMiK9FFYj-yhw" }
{ "votes" : { "useful" : 17740 }, "user_id" : "lxZSVeJz6KEBW1nlA3JKJg" }
{ "votes" : { "useful" : 17257 }, "user_id" : "mAuBHENS_DeFCQqrJC_UxA" }
{ "votes" : { "useful" : 16707 }, "user_id" : "spJUPXI7QaIctU0FO5c42w" }
{ "votes" : { "useful" : 15570 }, "user_id" : "mFOZOsPQOacWIMVSyXbEbg" }
{ "votes" : { "useful" : 15384 }, "user_id" : "2rlBbFPHyZjXSFSE8r551w" }
{ "votes" : { "useful" : 15190 }, "user_id" : "F9T6m1YdRFreyKDufcyoOQ" }
{ "votes" : { "useful" : 15014 }, "user_id" : "8J4IIYcqBlFch8T90N923A" }
{ "votes" : { "useful" : 13146 }, "user_id" : "Nn39wpr50dhP-i5r5-o1kw" }
{ "votes" : { "useful" : 12895 }, "user_id" : "ARe8Nr_YehB2ubsGJhZ-hg" }
{ "votes" : { "useful" : 12847 }, "user_id" : "Prsk7SiPZNfgcPyygOdGHg" }
{ "votes" : { "useful" : 12766 }, "user_id" : "nrOCJCQUgXwdUIwg8QHirw" }
{ "votes" : { "useful" : 12744 }, "user_id" : "AZuSSh8xMwLtoapGa02WZQ" }
{ "votes" : { "useful" : 12740 }, "user_id" : "AIVQg9enGug5woxehjmlGg" }


//Reviews by most useful reviewer
db.review.find({'user_id':'DrKQzBFAvxhyjLgbPSW2Qw'},{'_id':0,'business_id':0,'type':0,'user_id':0,'review_id':0})

/*
In the training set:
	4503/11537 businesses have label 'Restaurants'
	contributing to 160447/232965 reviews
In the test set:
	325/1205 businesses have label 'Restaurants'
	contributing to 6091/11077 reviews


skip:9111
counter:149319
*/
db.business_test.find({'categories':'Restaurants'}).count()
db.business_test.group( { cond:{'categories':'Restaurants'}, reduce: function(obj, prev){prev.sum += obj.review_count;}, initial:{sum:0} } )[0].sum;

/*

10702 of 22956 testing reviews lack business info in training database
1205 of 5585 businesses in testing reviews do not exist in training databse

9109 of 22956 test reviews lack user info in training database
5710 of 11926 users in testing reviews do not exist in training database

*/