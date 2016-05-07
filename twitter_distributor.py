import couchdb
from couchdb.mapping import Document, TextField, DictField, ListField,FloatField, Mapping, IntegerField
import sentiment


class Tweet(Document):
    id_str = TextField()
    text = TextField()
    created_at = TextField()
    geo = DictField(Mapping.build(
        type = TextField(),
        coordinates = ListField(FloatField())
    ),default=None)


class new_Tweet(Document):
    _id = TextField()
    text = TextField()
    created_time = TextField()
    geo = DictField(Mapping.build(
        type = TextField(),
        coordinates = ListField(FloatField())
    ),default=None)
    sentiment = IntegerField()
    district = TextField()


def read_district(fileName):
    f = open(fileName)
    districts = [[],[],[],[],[],[],[],[],[]]
    for i, line in enumerate(f):
        elements = line.split(',')
        for j, degree in enumerate(elements):
            elements[j] = float(degree)
        districts[i] = elements
    return districts


def district_distribute(districts, location_type, location_lanlong):
    if location_type == 'Point':
        for i, district in enumerate(districts):
            if district[1] < location_lanlong[0]< district[3]:
                if district[0] < location_lanlong[1] < district[2]:
                    return i
        return 10
    if location_type == 'Polygon':
        return 10


def main():

    couch = couchdb.Server('http://115.146.95.129:5984/')
    # db = couch['twitter']
    db = couch['test']
    print ('successfully connected')
    try:
        new_db = couch['dstwitter']
    except:
        new_db = couch.create('dstwitter')

    print ('successfully created new db')

    districts = read_district('Dds.txt')

    district_name = ['Melbourne_Inner', 'Melbourne_Inner_East', 'Melbourne_Inner_South',
                     'Melbourne_North_East', 'Melbourne_North_West', 'Melbourne_Outer_East',
                     'Melbourne_South_East', 'Melbourne_West', 'Mornington_Peninsula',
                     'Outside']
    for id in db:
        tweet= Tweet.load(db,id)
        location = tweet.geo
        if not bool(location):
            continue
        location_type = location.type
        location_lanlong = location.coordinates
        text = tweet.text
        time = tweet.created_at
        id_str = tweet.id_str
        if id_str in new_db:
            continue
        district = district_name[district_distribute(districts, location_type, location_lanlong)]
        sentimentValue = sentiment.sentiment_single_line(text)
        new_tweet = new_Tweet(_id= id_str, geo = location, text = text, created_time = time, sentiment = sentimentValue,district = district)
        new_tweet.store(new_db)


if __name__ == '__main__':
    main()
