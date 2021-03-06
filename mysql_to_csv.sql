TABLE yelp.business 
INTO OUTFILE 'business.csv'
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY '\\'
LINES TERMINATED BY '\n';

TABLE yelp.category 
INTO OUTFILE 'category.csv'
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY '\\'
LINES TERMINATED BY '\n';

TABLE yelp.review 
INTO OUTFILE 'review.csv'
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY '\\'
LINES TERMINATED BY '\n';

SELECT rid, review_id, business_id, user_id,
	stars, date, useful_votes, funny_votes, cool_votes
FROM yelp.review
INTO OUTFILE 'review_notext.csv'
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY '\\'
LINES TERMINATED BY '\n';

TABLE yelp.user 
INTO OUTFILE 'user.csv'
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY '\\'
LINES TERMINATED BY '\n';