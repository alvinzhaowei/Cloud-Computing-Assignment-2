# -*- coding: utf-8 -*-
__author__ = 'songjian'
import tweepy
import json
import sys
import couchdb
import time
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Variables that contains the user credentials to access Twitter API
access_token = "722011495060471808-UBN8XgxujwuuWdgzp72mUIM9K4btGIh"
access_token_secret = "s6FTHy9ZWDcEaIWXxE90c8gm7OakW0DE60qlMVreKcY1A"
consumer_key = "2VP6A9p8t8XA48dLD8RUFubUr"
consumer_secret = "55A3K54NolROQDlqATzcIAQ4OeCpx1nd3icupthWlNv3gVsxgp"

API_KEY = "A6ZJ2Cd5yLkjP0UHgmOZ3EJl2"
API_SECRET = "cQZ7B2r94IqgAg71voCJQWgwbItnclNWACMbpuJSZXdhnXdMcq"

MAX_TWEETS = 5000000
TWEETS_PER_QRY = 100

GEOBOX_MELBOURNE = [144.4427490234, -38.2338654156, 145.546875, -37.4835765504]
GEO_CIRCLE_INFO = "-37.817999,145.008244,20km"

file_path_streaming = './streaming.txt'
file_path_search = './tweet_id.txt'
count = 0  # a global varaible for tweets number counting with streaming API chosen
doc_id = None  # a global varaible for recording the id of the doc in database
# tweets_doc = {}
tweets_set = set()
f_streaming = open(file_path_streaming, 'a')


def initialize_db(db_name):
    couch = couchdb.Server()
    try:
        db = couch[db_name]
        # print 'The existing DB: \'%s\' will be used...' % db_name
        return db
    except:
        db = couch.create(db_name)
        print 'DB: \'%s\' has been created' % db_name
        return db


def write_data_to_db(data):
    db = initialize_db(sys.argv[2])
    global count
    doc = {count: data}
    db.save(doc)


# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def on_data(self, data):
        global count
        global f_streaming
        # f_streaming.write(data)
        # tweets_doc[count] = data
        write_data_to_db(data)
        count += 1
        print count, data
        return True

    def on_error(self, status):
        if status == 420:
            print status
            # sys.exit()
            return False


def get_since_id():
    id_list = []
    try:
        f_r = open(file_path_search, 'r')
        for i in f_r.readlines():
            if "-" not in i:
                i = int(i)
                id_list.append(i)
        return max(id_list)
    except:
        return None


def main():
    '''
    :param argv: argv[1]: which api will be chosen, streaming/search.
                 argv[2]: the name of the DB , if not existing, create one, or, use the existing db with this name
    :return:
    '''
    # Initialization...
    api_type = sys.argv[1]
    # This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()

    auth1 = OAuthHandler(consumer_key, consumer_secret)
    auth1.set_access_token(access_token, access_token_secret)

    auth = tweepy.AppAuthHandler(API_KEY, API_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    tweet_count = 0

    if api_type == 'search':
        since_id = get_since_id()
        if not since_id:
            print "This is your first time to invoke this script ^_^ "
        else:
            print "The task will start from tweet NO." + str(since_id)

        with open(file_path_search, 'a') as f:
            time_stamp = time.strftime('%Y-%m-%d-%H-%M', time.localtime(time.time()))
            f.write(str(time_stamp) + '\n')

            while tweet_count < MAX_TWEETS:
                try:
                    if not since_id:
                        new_tweets = api.search(q="*", geocode=GEO_CIRCLE_INFO, count=TWEETS_PER_QRY)
                    else:
                        new_tweets = api.search(q="*", geocode=GEO_CIRCLE_INFO, count=TWEETS_PER_QRY,
                                                since_id=since_id)
                    global count
                    for tweet in new_tweets:
                        json_str = json.dumps(tweet._json)
                        print count, json_str
                        count += 1
                        write_data_to_db(json_str)

                    if not new_tweets:
                        print ("No more tweets found")
                    tweet_count += len(new_tweets)
                    print ("Download {0} tweets".format(tweet_count))
                    max_id = new_tweets[-1].id
                    f.write(str(max_id) + '\n')
                except tweepy.TweepError as e:
                    print ("ERROR FOUND: " + str(e))
                    break

            f.close()
    elif api_type == 'streaming':
        while True:
            try:
                stream = Stream(auth1, l)
                stream.filter(locations=GEOBOX_MELBOURNE)
            except Exception as e:
                print e
                continue
    else:
        print 'For the 1st para, neither \"streaming\" nor \"search\" has been correctly input'


if __name__ == '__main__':
    main()
