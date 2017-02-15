import couchdb
from couchdb.mapping import Document, TextField, DictField, ListField,FloatField, Mapping, IntegerField


class District(Document):
    name = TextField()
    subDistrict = ListField(DictField(Mapping.build(
        teenager_count=IntegerField(),
        teenager_rate=FloatField()
    )))


class new_District(Document):
    _id = TextField()
    name = TextField()
    teenager_count = IntegerField()
    teenager_rate = FloatField()


def main():

    couch = couchdb.Server('http://115.146.95.129:5984/')

    db = couch['teenager']
    try:
        new_db = couch['teenager_done']
    except:
        new_db = couch.create('teenager_done')

    print ('successfully connected')

    for i,id in enumerate(db):
        district = District.load(db,id)
        new_district = new_District(_id = str(i),name = district.name)
        sub_districts = district.subDistrict
        allcount = 0
        teenagercount = 0
        for sub_district in sub_districts:
            num = sub_district.teenager_count
            if num == 0:
                continue
            teenagercount = teenagercount + num
            rate = sub_district.teenager_rate
            allnum = int(num / (rate/100))
            allcount = allcount + allnum
        allrate = float("{0:.2f}".format(float(teenagercount) / allcount * 100))
        new_district.teenager_count = allcount
        new_district.teenager_rate = allrate
        new_district.store(new_db)


if __name__ == '__main__':
    main()