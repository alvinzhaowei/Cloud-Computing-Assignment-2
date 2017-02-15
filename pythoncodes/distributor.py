#!/usr/bin/python
import couchdb
from couchdb.mapping import Document, TextField, DictField, ListField,FloatField, Mapping, IntegerField
import sentiment
import re


class Tweet(Document):
    id_str = TextField()
    text = TextField()
    created_at = TextField()
    geo = DictField(Mapping.build(
        type=TextField(),
        coordinates=ListField(FloatField())
    ),default=None)
    user = DictField(Mapping.build(screen_name=TextField()))


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


def couchdb_pager(db, view_name='_all_docs',
                  startkey=None, startkey_docid=None,
                  endkey=None, endkey_docid=None, bulk=5000):
    # Request one extra row to resume the listing there later.
    options = {'limit': bulk + 1}
    if startkey:
        options['startkey'] = startkey
        if startkey_docid:
            options['startkey_docid'] = startkey_docid
    if endkey:
        options['endkey'] = endkey
        if endkey_docid:
            options['endkey_docid'] = endkey_docid
    done = False
    while not done:
        view = db.view(view_name, **options)
        rows = []
        # If we got a short result (< limit + 1), we know we are done.
        if len(view) <= bulk:
            done = True
            rows = view.rows
        else:
            # Otherwise, continue at the new start position.
            rows = view.rows[:-1]
            last = view.rows[-1]
            options['startkey'] = last.key
            options['startkey_docid'] = last.id

        for row in rows:
            yield row.id


def read_district(fileName):
    f = open(fileName)
    districts = [[],[],[],[],[],[],[],[],[]]
    for i, line in enumerate(f):
        elements = line.split(',')
        for j, degree in enumerate(elements):
            elements[j] = float(degree)
        districts[i] = elements
    return districts


def district_distribute(districts, location):
    location_type = location.type
    location_lanlong = location.coordinates
    if location_type == 'Point':
        for i, district in enumerate(districts):
            if district[1] < location_lanlong[0]< district[3]:
                if district[0] < location_lanlong[1] < district[2]:
                    return i
        return 9
    if location_type == 'Polygon':
        location_lanlong = re.split('\]|\[|\,| ', str(location_lanlong))

        while '' in location_lanlong:
            location_lanlong.remove('')
        location.coordinates = location_lanlong
        for i, district in enumerate(districts):
            if district[0] < location_lanlong[0]:
                if district[2] > location_lanlong[2]:
                    if district[1] < location_lanlong[1]:
                        if district[3] > location_lanlong[5]:
                            return i
        return 9


def main():

    couch = couchdb.Server('http://115.146.95.129:5984/')
    # db = couch['twitter']
    db = couch['tweet2']
    try:
        new_db = couch['dstweet']
    except:
        new_db = couch.create('dstweet')
   
    print ('successfully connected')

    districts = read_district('Dds.txt')

    district_name = ['Melbourne_Inner', 'Melbourne_Inner_East', 'Melbourne_Inner_South',
                     'Melbourne_North_East', 'Melbourne_North_West', 'Melbourne_Outer_East',
                     'Melbourne_South_East', 'Melbourne_West', 'Mornington_Peninsula',
                     'Outside']
    count = 0
    for id in couchdb_pager(db):
        count = count + 1
        if count % 10000 == 0:
            print count
        tweet= Tweet.load(db,id)
        location = tweet.geo
        if not bool(location):
            continue
        text = tweet.text
        time = tweet.created_at
        id_str = tweet.id_str
        if id_str in new_db:
            continue
        district = district_name[district_distribute(districts, location)]
        sentimentValue = sentiment.sentiment_single_line(text)
        try:
            new_tweet = new_Tweet(_id= id_str, geo = location,
                                  text = text, created_time = time,
                                  sentiment = sentimentValue,district = district,
                                  screen_name = tweet.user.screen_name)
            new_tweet.store(new_db)
        except:
            print('exception')
            pass

    print ('finished')


if __name__ == '__main__':
    main()

