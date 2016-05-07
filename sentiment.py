# coding: utf-8
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import nltk
import re


re_at = re.compile(r'@[\w]+')  # a regular expression which match all the string which starts with @
re_http = re.compile(r'https?(:|;|.)?/+[\w./?]+')  # a regular expression which match all the url which starts with http
re_hash_tag = re.compile(r'#[a-zA-Z]+')  # match all the string starts with ‘#’
re_lower = re.compile(r'a-z')  # a regular expression which match all the lower case
list_of_corpus = set(nltk.corpus.words.words())  # put all the English words included in NLTK into a set
english_stop_words = set(nltk.corpus.stopwords.words('english')) 
 # put all the English stopwords included in NLTK into a set



# preprocess single line tweet
def preprocess(tweet):
    tweet = tweet.lower()  # lower case each line with out string start with '#'
    remove_at_tweet = re.sub(re_at, "", tweet).strip()  # each line remove at
    remove_http_tweet = re.sub(re_http, "", remove_at_tweet).strip()  # each line remove http
    remove_hashtag_tweet = re.sub(re_hash_tag, "", remove_http_tweet).strip()  # remove the string start with '#' for each line
    sectences_list = tokenize.sent_tokenize(remove_hashtag_tweet)  # put the segment result into sentence list
    return sectences_list


def sentiment_single_line(line):
    sid = SentimentIntensityAnalyzer()
    total_sum = 0
    tweet_length = 0
    tweet_after_process = preprocess(line)  # a list which contain a list

    if tweet_after_process==[]:
        return 0
    else:
        for sentence in tweet_after_process:
            ss = sid.polarity_scores(sentence)
            total_sum += ss["compound"] * len(sentence)
            tweet_length += len(sentence)
            total_sum = total_sum / tweet_length
            if total_sum < -0.03:
                return -1
            elif total_sum > 0.03:
                return 1
            else:
                return 0


#test
print sentiment_single_line("hello, I am fine")
print sentiment_single_line("www.google.com")
print sentiment_single_line("I am very very sad")

