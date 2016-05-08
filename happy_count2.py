# coding: utf-8
from __future__ import division
import couchdb 
from couchdb.mapping import Document, TextField, IntegerField, DictField, Mapping
import re



server = couchdb.Server('http://115.146.95.129:5984/',full_commit = True, session = None)   # the url of the server
db = server['dstwitter']
#db = server['twitter']     # the name of the database

# server = couchdb.Server('http://127.0.0.1:5984/',full_commit = True, session = None)   # the url of the server
# db = server['mydatabase']    # the name of the database
# dbstore = server.create("myresult")
try:
    dbstore = server['myresult_morning_evening']
except:
    dbstore = server.create('myresult_morning_evening')
    print ('successfully created new db')

morning_regex = '^(0[6-9]|1[0-1]):[0-5]\d{1}:([0-5]\d{1})$'   
night_regex = '^(1[8-9]|2[0-3]):[0-5]\d{1}:([0-5]\d{1})$'
    

Melbourne_Inner = {"morning":{"value":0,"times":0},"evening":{"value":0,"times":0}}
Melbourne_Inner_East = {"morning":{"value":0,"times":0},"evening":{"value":0,"times":0}}
Melbourne_Inner_South = {"morning":{"value":0,"times":0},"evening":{"value":0,"times":0}}
Melbourne_North_East = {"morning":{"value":0,"times":0},"evening":{"value":0,"times":0}}
Melbourne_North_West  = {"morning":{"value":0,"times":0},"evening":{"value":0,"times":0}}
Melbourne_Outer_East = {"morning":{"value":0,"times":0},"evening":{"value":0,"times":0}}
Melbourne_South_East = {"morning":{"value":0,"times":0},"evening":{"value":0,"times":0}}
Melbourne_West = {"morning":{"value":0,"times":0},"evening":{"value":0,"times":0}}
Mornington_Peninsula = {"morning":{"value":0,"times":0},"evening":{"value":0,"times":0}}

Melbourne_Inner_result = {"morning":0,"evening":0}
Melbourne_Inner_East_result = {"morning":0,"evening":0}
Melbourne_Inner_South_result = {"morning":0,"evening":0}
Melbourne_North_East_result = {"morning":0,"evening":0}
Melbourne_North_West_result = {"morning":0,"evening":0}
Melbourne_Outer_East_result = {"morning":0,"evening":0}
Melbourne_South_East_result = {"morning":0,"evening":0}
Melbourne_West_result = {"morning":0,"evening":0}
Mornington_Peninsula_result = {"morning":0,"evening":0}

# the method is used to calcute the average result 
def process_result(dictionary,dictionary_result):
    result_morning = dictionary["morning"]["value"]/dictionary["morning"]["times"]
    result_evening = dictionary["evening"]["value"]/dictionary["evening"]["times"]
    result_morning = float("{0:.3f}".format(result_morning))
    result_evening = float("{0:.3f}".format(result_evening))
    dictionary_result["morning"] = result_morning
    dictionary_result["evening"] = result_evening
    
# check the time of the tweet, morining, evening or pass
def date_check (date_text):
    target_line_list = date_text.split(" ")
    if re.match(morning_regex,target_line_list[3]):
        return "morning"
    elif re.match(night_regex,target_line_list[3]):
        return "evening"
    else:
        pass

# do the statistics of sentiment result and times in different suburbs
def count_data(dictionary,time):
    if date_check (time) =="morning":
        dictionary["morning"]["value"] = dictionary["morning"]["value"]+label
        dictionary["morning"]["times"] = dictionary["morning"]["times"]+1
    elif date_check (time) == "evening":
        dictionary["evening"]["value"] = dictionary["evening"]["value"]+label
        dictionary["evening"]["times"] = dictionary["evening"]["times"]+1
    else:
        pass
    

class Tweet(Document):
    district = TextField()
    text = TextField()
    created_time = TextField()
    sentiment = IntegerField()


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

      
#for id in db:
for id in couchdb_pager(db):

    tweet= Tweet.load(db,id)
    time = tweet.created_time
    label = tweet.sentiment
    location = tweet.district

    if location =="Melbourne_Inner":
        count_data(Melbourne_Inner,time)

    elif location =="Melbourne_Inner_East":
        count_data(Melbourne_Inner_East,time)

    elif location =="Melbourne_Inner_South":
        count_data(Melbourne_Inner_South,time)

    elif location =="Melbourne_North_East":
        count_data(Melbourne_North_East,time) 

    elif location =="Melbourne_North_West":
        count_data(Melbourne_North_West,time)

    elif location =="Melbourne_Outer_East":
        count_data(Melbourne_Outer_East,time) 

    elif location =="Melbourne_South_East":
        count_data(Melbourne_South_East,time)

    elif location =="Melbourne_West":
        count_data(Melbourne_West,time)

    elif location =="Mornington_Peninsula":
        count_data(Mornington_Peninsula,time)

    else:
        pass
        
print  "Melbourne_Inner", Melbourne_Inner
print  "Melbourne_Inner_East", Melbourne_Inner_East
print  "Melbourne_Inner_South", Melbourne_Inner_South
print  "Melbourne_North_East", Melbourne_North_East
print  "Melbourne_North_West", Melbourne_North_West
print  "Melbourne_Outer_East", Melbourne_Outer_East
print  "Melbourne_South_East", Melbourne_South_East
print  "Melbourne_West", Melbourne_West
print  "Mornington_Peninsula", Mornington_Peninsula

doc1 = {"Melbourne_Inner":Melbourne_Inner,
"Melbourne_Inner_East":Melbourne_Inner_East,
"Melbourne_Inner_South":Melbourne_Inner_South,
"Melbourne_North_East":Melbourne_North_East,
"Melbourne_North_West":Melbourne_North_West,
"Melbourne_Outer_East":Melbourne_Outer_East,
"Melbourne_South_East":Melbourne_South_East,
"Mornington_Peninsula":Mornington_Peninsula}
dbstore.save(doc1)

try:
    process_result(Melbourne_Inner,Melbourne_Inner_result)
    process_result(Melbourne_Inner_East,Melbourne_Inner_East_result)
    process_result(Melbourne_Inner_South,Melbourne_Inner_South_result)
    process_result(Melbourne_North_East,Melbourne_North_East_result)
    process_result(Melbourne_North_West,Melbourne_North_West_result)
    process_result(Melbourne_Outer_East,Melbourne_Outer_East_result)
    process_result(Melbourne_South_East,Melbourne_South_East_result)
    process_result(Melbourne_West,Melbourne_West_result)
    process_result(Mornington_Peninsula,Mornington_Peninsula_result)

    doc2 = {"Melbourne_Inner_result":Melbourne_Inner_result,
    "Melbourne_Inner_East_result":Melbourne_Inner_East_result,
    "Melbourne_Inner_South_result":Melbourne_Inner_South_result,
    "Melbourne_North_East_result":Melbourne_North_East_result,
    "Melbourne_North_West_result":Melbourne_North_West_result,
    "Melbourne_Outer_East_result":Melbourne_Outer_East_result,
    "Melbourne_South_East_result":Melbourne_South_East_result,
    "Melbourne_West_result":Melbourne_West_result,
    "Mornington_Peninsula_result":Mornington_Peninsula_result}
    dbstore.save(doc2)

    print  "Melbourne_Inner_result", Melbourne_Inner_result
    print  "Melbourne_Inner_East_result", Melbourne_Inner_East_result
    print  "Melbourne_Inner_South_result", Melbourne_Inner_South_result
    print  "Melbourne_North_East_result", Melbourne_North_East_result
    print  "Melbourne_North_West_result", Melbourne_North_West_result
    print  "Melbourne_Outer_East_result", Melbourne_Outer_East_result
    print  "Melbourne_South_East_result", Melbourne_South_East_result
    print  "Melbourne_West_result", Melbourne_West_result
    print  "Mornington_Peninsula_result", Mornington_Peninsula_result

except:
       print "can not provide the result, division by zero"













        
