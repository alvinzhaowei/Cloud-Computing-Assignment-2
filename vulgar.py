import couchdb 
from couchdb.mapping import Document, TextField, IntegerField, DateTimeField
import re
import nltk
import gensim
from nltk.data import find
import math

#server = couchdb.Server('http://115.146.95.129:5984/',full_commit = True, session = None)
#db = server['twitter']
	
server = couchdb.Server()
db = server['twit']

def vulgarDict():
	f = open("vulgar.txt")
	vulgardict = set()
	for line in f:
		line = re.sub(r"\n", "", line)
		vulgardict.add(line)
	return vulgardict

vulgardict = vulgarDict()

class Tweet(Document):
	_id = TextField()
	_rec = TextField()
	text = TextField()
	geo = TextField()
	

	
for id in db:

	tweet= Tweet.load(db,id)
	#print tweet._id, tweet.text
	#preprocess the tweet
	location = tweet.geo
	tweet = tweet.text
	
	if tweet is not None:
		tweet = re.sub(r"[^0-9a-zA-Z]+", " ", tweet)
		tweet = re.sub(r"http\S+|@\w+", " ", tweet)
		word_tokenizer = nltk.tokenize.regexp.WordPunctTokenizer()
		tokenized_sentence = word_tokenizer.tokenize(tweet)
		
		#the function can return the location of the tweet
		#
		#
		location = 'Inner'
		count ={'Inner':0,'West':0,'NorthWest':0,'NorthEast':0,'InnerEast':0,'OuterEast':0,'SouthEast':0,'MorningtonPeninsula':0,'InnerSouth':0}
		
		wnl = nltk.stem.wordnet.WordNetLemmatizer()
		for t in tokenized_sentence:
			lem_tweet = wnl.lemmatize(t.lower()) 
			#if the word in the vulgardict, then the tweet is vulgardict
			#else the tweet is not vulgardict
			if t in vulgardict:
				count[location] = count.get(location)+1 
				break
