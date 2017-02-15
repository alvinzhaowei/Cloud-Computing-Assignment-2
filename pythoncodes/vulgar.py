import couchdb 
from couchdb.mapping import Document, TextField
import re
import nltk


server = couchdb.Server('http://115.146.95.129:5984/',full_commit = True, session = None)
db = server['new_dstweet']
	
#server = couchdb.Server()
#db = server['twit']

def vulgarDict():
	f = open("vulgar.txt")
	vulgardict = set()
	for line in f:
		line = re.sub(r"\n", "", line)
		vulgardict.add(line)
	return vulgardict



class Tweet(Document):
	_id = TextField()
	_rec = TextField()
	text = TextField()
	district = TextField()
	

def vulgarAnalysis():
	count ={'Melbourne_Inner':0,'Melbourne_West':0,'Melbourne_North_West':0,\
	'Melbourne_North_East':0,'Melbourne_Inner_East':0,'Melbourne_Outer_East':0,\
	'Melbourne_South_East':0,'Mornington_Peninsula':0,'Melbourne_Inner_South':0}
	word = {}
	for id in db:

		tweet= Tweet.load(db,id)
		#print tweet._id, tweet.text
		#preprocess the tweet
		location = tweet.district
		tweet = tweet.text
		wnl = nltk.WordNetLemmatizer()
		#count ={'Melbourne_Inner':0,'Melbourne_West':0,'Melbourne_North_West':0,'Melbourne_North_East':0,'Melbourne_Inner_East':0,'Melbourne_Outer_East':0,'Melbourne_South_East':0,'Mornington_Peninsula':0,'Melbourne_Inner_South':0}
		
		if tweet is not None:
			tweet = re.sub(r"[^0-9a-zA-Z]+", " ", tweet)
			tweet = re.sub(r"http\S+|@\w+", " ", tweet)
			word_tokenizer = nltk.tokenize.regexp.WordPunctTokenizer()
			tokenized_sentence = word_tokenizer.tokenize(tweet)
	
			for t in tokenized_sentence:
				t = wnl.lemmatize(t.lower()) 
				
				#if the word in the vulgardict, then the tweet is vulgardict
				#else the tweet is not vulgardict
				if t in vulgardict:
					count[location] = count.get(location,0)+1 
					word[t] = word.get(t,0)+1
#					print t
#					print count
					break
		
	return count, word

vulgardict = vulgarDict()
result, word = vulgarAnalysis()
print result
#print vulgardict
vw = server['vulgarword']

for i in result:
	vw.save({i: result[i]})

for i in word:
	vw.save({i: word[i]})
	
