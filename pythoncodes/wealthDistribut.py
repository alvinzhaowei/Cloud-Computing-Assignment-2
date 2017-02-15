import couchdb
from couchdb.mapping import Document, TextField, DictField, ListField,FloatField, Mapping, IntegerField


class District(Document):
    name = TextField()
    subDistrict = ListField(DictField(Mapping.build(
        poverty_rate=FloatField()
    )))


class new_District(Document):
    _id = TextField()
    name = TextField()
    poverty_rate = FloatField()


def main():

    couch = couchdb.Server('http://115.146.95.129:5984/')

    db = couch['poverty']
    try:
        new_db = couch['poverty_done']
    except:
        new_db = couch.create('poverty_done')

    print ('successfully connected')

    for i,id in enumerate(db):
        district = District.load(db,id)
        new_district = new_District(_id = str(i),name = district.name)
        sub_districts = district.subDistrict
        rateall = 0
        districtNum = 0
        for sub_district in sub_districts:
            rate = sub_district.poverty_rate
            if rate == 0:
                continue
            rateall = rateall + rate
            districtNum = districtNum + 1
        avg = float("{0:.2f}".format(rateall / districtNum))
        new_district.poverty_rate = avg
        new_district.store(new_db)


if __name__ == '__main__':
    main()