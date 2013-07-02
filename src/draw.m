out = csvread('/home/ecsark/Documents/Computer/DataMining/Contest/Yelp/data/reviewCount_usefulness.csv');
reviewCount = out(:,1:1);
usefulCount = out(:,2:2);

%scatter(reviewCount,usefulCount)

usefulRate = usefulCount./reviewCount;

scatter(reviewCount, usefulRate)