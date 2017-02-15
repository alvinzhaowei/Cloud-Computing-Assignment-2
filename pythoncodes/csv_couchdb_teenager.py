import couchdb
from couchdb.mapping import Document, TextField, DictField, ListField,FloatField, Mapping,IntegerField

district_name = ['Melbourne_Inner', 'Melbourne_Inner_East', 'Melbourne_Inner_South',
                 'Melbourne_North_East', 'Melbourne_North_West', 'Melbourne_Outer_East',
                 'Melbourne_South_East', 'Melbourne_West', 'Mornington_Peninsula']


class District (Document):
    name = TextField()
    subDistrict = ListField(DictField(Mapping.build(
        name=TextField(),
        teenager_count = IntegerField(),
        teenager_rate = FloatField()
    )))


def readfile(filename):
    f = open(filename)
    lines = f.readlines()
    sub_districts = []
    for line in lines[1:]:
        elements = line.split(',')
        if elements[2] == 'null':
            elements[2] = 0
        try:
            int(elements[2])
            items = [elements[1][1:-2],elements[2],elements[3]]
        except:
            items = [elements[1][1:-2],elements[3],elements[2]]
        sub_districts.append(items)
    print sub_districts
    return sub_districts


def main():
    couch = couchdb.Server('http://115.146.95.129:5984/')
    try:
        db = couch.create('teenager')
    except:
        db = couch['teenager']
    for name in district_name:
        sub_district = readfile('./csv/teenager/'+name+'.csv')
        district = District(name = name)
        for item in sub_district:
            district.subDistrict.append(name = item[0],teenager_count = int(item[1]), teenager_rate = item[2])
        district.store(db)


if __name__ == '__main__':
    main()