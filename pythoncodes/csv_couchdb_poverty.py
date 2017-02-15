import couchdb
from couchdb.mapping import Document, TextField, DictField, ListField,FloatField, Mapping

district_name = ['Melbourne_Inner', 'Melbourne_Inner_East', 'Melbourne_Inner_South',
                 'Melbourne_North_East', 'Melbourne_North_West', 'Melbourne_Outer_East',
                 'Melbourne_South_East', 'Melbourne_West', 'Mornington_Peninsula']


class District (Document):
    name = TextField()
    subDistrict = ListField(DictField(Mapping.build(
        name=TextField(),
        poverty_rate = FloatField()
    )))


def readfile(filename):
    f = open(filename)
    lines = f.readlines()
    sub_districts = []
    for line in lines[1:]:
        elements = line.split(',')
        if elements[2] == 'null':
            elements[2] = 0
        items = [elements[1][1:-2],elements[2]]
        sub_districts.append(items)
    return sub_districts


def main():
    couch = couchdb.Server('http://115.146.95.129:5984/')
    try:
        db = couch.create('poverty')
    except:
        db = couch['poverty']
    for name in district_name:
        sub_district = readfile('./csv/poverty/'+name+'.csv')
        district = District(name = name)
        for item in sub_district:
            district.subDistrict.append(name = item[0],poverty_rate = float(item[1]))
        district.store(db)


if __name__ == '__main__':
    main()