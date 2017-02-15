import couchdb
import tweepy
import time
from couchdb.mapping import Document, TextField,DictField,Mapping
from sets import Set

API_KEY = "A6ZJ2Cd5yLkjP0UHgmOZ3EJl2"
API_SECRET = "cQZ7B2r94IqgAg71voCJQWgwbItnclNWACMbpuJSZXdhnXdMcq"

class DsTweet(Document):
    _id = TextField()
    district = TextField()

class Tweet(Document):

    user = DictField(Mapping.build(screen_name = TextField()))


def main():
    auth = tweepy.AppAuthHandler(API_KEY, API_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    couch = couchdb.Server('http://115.146.95.129:5984/')
    user_screen_name = Set()
    db = couch['dsTwistter']
    print ('successfully connected')

    for id in db:
        tweet= Tweet.load(db,id)
        name = tweet.user.screen_name
        if name not in user_screen_name:
            user_screen_name.add(name)
            print name
        for friend in tweepy.Cursor(api.friends, screen_name= name).items():
            name = friend.screen_name
            time.sleep(0.05)
            if name not in user_screen_name:
                user_screen_name.add(name)
                print name


if __name__ == '__main__':
    main()
