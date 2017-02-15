import tweepy
import json
import sentiment
import couchdb
from couchdb.mapping import Document, TextField, DictField, ListField,FloatField, Mapping, IntegerField

API_KEY = "A6ZJ2Cd5yLkjP0UHgmOZ3EJl2"
API_SECRET = "cQZ7B2r94IqgAg71voCJQWgwbItnclNWACMbpuJSZXdhnXdMcq"

MAX_TWEETS = 5000000
TWEETS_PER_QRY = 100
TWEET_AMOUNT_PER_USER = 200
screen_names = set()


def initialize_db(db_name):
    couch = couchdb.Server('http://115.146.95.129:5984/')
    try:
        db = couch[db_name]
        # print 'The existing DB: \'%s\' will be used...' % db_name
        return db
    except:
        db = couch.create(db_name)
        print 'DB: \'%s\' has been created' % db_name
        return db


class new_Tweet(Document):
    _id = TextField()
    text = TextField()
    created_time = TextField()
    geo = DictField(Mapping.build(
        type=TextField(),
        coordinates=ListField(FloatField())
    ),default=None)
    sentiment = IntegerField()
    district = TextField()
    screen_name =  TextField()


def district_write_data(data,district,db):
    json_str = json.dumps(data)
    json_o = json.loads(json_str)
    text = json_o['text']
    _id = json_o['id_str']
    created_time = json_o['created_at']
    sentimentValue = sentiment.sentiment_single_line(text)
    geoType = json_o['geo']['type']
    lang_long = json_o['geo']['coordinates']
    new_tweet = new_Tweet(_id = _id, created_time = created_time,
                          district = district, sentiment = sentimentValue,
                          geo=dict(type=geoType,coordinates=lang_long),text=text)
    new_tweet.store(db)


def get_all_tweets_by_screen_name(screen_name, api, district,db):
    tweet_count = 0
    print ('--Now begin to crawl %s\'s tweets...' % screen_name)
    alltweets = []
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)
    alltweets.extend(new_tweets)
    for tweet in new_tweets:
        tweet_count += 1
        if tweet_count > TWEET_AMOUNT_PER_USER:
            return
        else:

            district_write_data(tweet._json, district,db)
            print ("Download {0} tweets".format(tweet_count) + " from user: %s" % screen_name)
    last_id = alltweets[-1].id - 1
    while len(new_tweets) > 0:
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=last_id)
        alltweets.extend(new_tweets)
        for tweet in new_tweets:
            tweet_count += 1
            if tweet_count > TWEET_AMOUNT_PER_USER:
                return
            else:
                district_write_data(tweet._json,district,db)
                print ("Download {0} tweets".format(tweet_count) + " from user: %s" % screen_name)
        last_id = alltweets[-1].id - 1

    print ('--%s has %d tweets in all' % (screen_name, len(alltweets)))
    print ('\n')


def main():
    '''
    :param argv: argv[1]: which api will be chosen, streaming/search.
                 argv[2]: the name of the DB , if not existing, create one, or, use the existing db with this name
    :return:
    '''
    # Initialization...
    auth = tweepy.AppAuthHandler(API_KEY, API_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    new_db = initialize_db('new_dstweet')
    db = initialize_db('dstweet1')
    for id in db:
        tweet = new_Tweet.load(db,id)
        new_screen_name = tweet.screen_name
        district = tweet.district
        if new_screen_name in screen_names:
            continue
        else:
            screen_names.add(new_screen_name)
        try:
            get_all_tweets_by_screen_name(new_screen_name.strip(), api, district,new_db)
        except Exception as e:
            print e
            continue


if __name__ == '__main__':
    main()