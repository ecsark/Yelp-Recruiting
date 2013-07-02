function(){
	var histo = new Array(20);
	for(var i=0; i<20; i++){
		histo[i] = db.review.find({'votes.useful':i}).count();
	}
	return histo;
}

function(spec){
	var histo = new Array(spec);
	var interval = 5/spec;
	for(var i=0; i<spec; ++i){
		var lower = i*interval;
		var upper = lower + interval;
		var count = db.user.find({average_stars:{$gt: lower, $lte:upper}}).count();
		//var total = db.user.find({average_stars:{$gt: lower, $lte:upper}})
		var min = db.user.find({average_stars:{$gt: lower, $lte:upper}},{'_id':0,'votes.useful':1}).sort({'votes.useful':1}).limit(1).toArray();
		var max = db.user.find({average_stars:{$gt: lower, $lte:upper}},{'_id':0,'votes.useful':1}).sort({'votes.useful':-1}).limit(1).toArray();
		histo[i] = new Array(lower.toFixed(2),upper.toFixed(2),count,min[0].votes.useful,max[0].votes.useful);
	}
	return histo;
}

db.business.group({
	key:{'categories':1},
	initial:{count:0},
	reduce:function(curr, result){
		result.count+=1;
	}
})


function(num){
	var result = new Array(num);
	var uusers = db.user.find({},{'votes.useful':1,'user_id':1,'_id':0}).sort({'votes.useful':-1}).limit(num).toArray();
	for(var i=0; i<num; ++i){
		var reviewByUser = db.review.find({'user_id':uusers[i].user_id},{'votes.useful':1,'_id':0}).sort({'votes.useful':1}).toArray();
		result[i] = new Array(uusers[i].user_id,reviewByUser);
	}
	return result;
}


db.business.group({
	cond:{'categories':'Restaurants'},
	reduce: function(obj, prev){prev.sum += obj.review_count;},
	initial:{sum:0}
})[0].sum;

