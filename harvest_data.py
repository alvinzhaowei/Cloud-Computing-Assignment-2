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

GEOBOX_MELBOURNE = [144.4427490234, -38.2338654156, 145.546875, -37.4835765504]

file_path_streaming = './streaming.txt'
file_path_search = './search.txt'
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


def is_duplicated(text):
    if text not in tweets_set:
        tweets_set.add(text)
        return False
    else:
        return True


def write_data_to_db(data):
    db = initialize_db(sys.argv[3])
    global doc_id
    global count
    if count == 0 or doc_id is None:
        document_id, doc_rev = db.save({count: data})
        doc_id = document_id
    else:
        doc = db[doc_id]
        doc[count] = data
        db[doc.id] = doc


# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def on_data(self, data):
        global count
        global f_streaming
        if len(sys.argv) == 4:
            f_streaming.write(data)
            # tweets_doc[count] = data
            write_data_to_db(data)
        elif len(sys.argv) == 5:
            if count < int(sys.argv[4]):
                f_streaming.write(data)
                write_data_to_db(data)
            else:
                sys.exit()
        count += 1
        print count, data
        return True

    def on_error(self, status):
        if status == 420:
            print status
            # sys.exit()
            return False


def main():
    '''
    :param argv: argv[1]: which api will be chosen, streaming/search.
                 argv[2]: which term will be searched
                 argv[3]: the name of the DB , if not existing, create one, or, use the existing db with this name
                 argv[4]: (if required) the number of tweets will be crawled, if search API is chosen, then argv[3] must be provided
    :return:
    '''
    # Initialization...
    api_type = sys.argv[1]
    term = sys.argv[2]
    if len(sys.argv) == 5:  # specific number of lines required
        how_many_tweets_wanted = sys.argv[4]
    # This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    if api_type == 'search':
        api = tweepy.API(auth)
        with open(file_path_search, 'a') as f:
            for tweet in tweepy.Cursor(api.search, q=term).items(int(how_many_tweets_wanted)):
                try:
                    json_str = json.dumps(tweet._json)
                    if not is_duplicated(json_str):
                        tweets_set.add(json_str)
                        global count
                        print count, json_str
                        # tweets_doc[count] = json_str
                        f.write(json_str + '\n')
                        write_data_to_db(json_str)
                        count += 1
                except Exception as e:
                    print e

            f.close()
    elif api_type == 'streaming':
        while True:
            try:
                if len(sys.argv) == 5 and count == sys.argv[4]:
                    break
                else:
                    stream = Stream(auth, l)
                    stream.filter(locations=GEOBOX_MELBOURNE)
            except Exception as e:
                print e
                continue
    else:
        print 'For the 1st para, neither \"streaming\" nor \"search\" has been correctly input'


if __name__ == '__main__':
    main()
