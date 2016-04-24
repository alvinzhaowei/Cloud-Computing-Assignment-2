# coding: utf-8
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json
import nltk
import re

filename = "/Users/Sunjingjing/Desktop/streaming.json"  # give the file path
re_at = re.compile(r'@[\w]+')  # a regular expression which match all the string which starts with @
re_http = re.compile(r'http.*')  # a regular expression which match all the url which starts with http
re_hash_tag = re.compile(r'#[a-zA-Z]+')  # match all the string starts with ‘#’
re_lower = re.compile(r'a-z')  # a regular expression which match all the lower case
list_of_corpus = set(nltk.corpus.words.words())  # put all the English words included in NLTK into a set
english_stop_words = set(
    nltk.corpus.stopwords.words('english'))  # put all the English stopwords included in NLTK into a set
positive_list = []
negative_list = []
neutral_list = []
label = []


def preprocess(tweet):
    remove_at_tweet = re.sub(re_at, "", tweet).strip()  # each line remove at
    remove_http_tweet = re.sub(re_http, "", remove_at_tweet).strip()  # each line remove http
    remove_hashtag_tweet = re.sub(re_hash_tag, "",
                                  remove_http_tweet).strip()  # remove the string start with '#' for each line
    remove_hashtag_tweet = remove_hashtag_tweet.lower()  # lower case each line with out string start with '#'
    sectences_list = tokenize.sent_tokenize(remove_hashtag_tweet)  # put the segment result into sentence list
    return sectences_list


def preprocess_file(filename):
    tweets = []
    f = open(filename, 'r')
    for line in f:
        tweet_dict = json.loads(line)
        tweet_after_process = preprocess(tweet_dict["text"])  # a list which contain a list
        tweets.append(tweet_after_process)  # a list which contain a list which contain the sectence of each line
    return tweets


tweets = preprocess_file(filename)
sid = SentimentIntensityAnalyzer()
total_sum = 0
tweet_length = 0

for tweet in tweets:
    for sentence in tweet:
        # print sentence
        ss = sid.polarity_scores(sentence)
        total_sum += ss["compound"] * len(sentence)
        tweet_length += len(sentence)
    total_sum = total_sum / tweet_length
    print total_sum

    if total_sum < -0.03:
        label.append(-1)
    elif total_sum > 0.03:
        label.append(1)
    else:
        label.append(0)


