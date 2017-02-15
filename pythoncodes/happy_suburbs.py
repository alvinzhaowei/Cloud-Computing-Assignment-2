# coding: utf-8
from __future__ import division
import couchdb 
from couchdb.mapping import Document, TextField, IntegerField, DictField, Mapping
import re

#this code is used to count the ratio of happy ,unhappy and netural in different areas
#the result will be stored in couchdb


#define the tyoe of dictionary    
def location_dictionary(dictionary):
    dictionary = {"positive":0, "negative":0,"neutral":0,"times":0}
    
    return dictionary


def return_times(dictionary0,dictionary1,dictionary2,dictionary3,dictionary4,dictionary5,
    dictionary6,dictionary7,dictionary8,times,texttype1):
    times = dictionary0[texttype1]+dictionary1[texttype1]\
    +dictionary2[texttype1]+dictionary3[texttype1]\
    +dictionary4[texttype1]+dictionary5[texttype1]\
    +dictionary6[texttype1]+dictionary7[texttype1]\
    +dictionary8[texttype1]
    return times

#define the type of dictionary
def result_dictionary(dictionary):
    dictionary = {"positive":0, "negative":0,"neutral":0}
    return dictionary

# return the special data type from all discionaries
def return_list(dictionary0,dictionary1,dictionary2,dictionary3,dictionary4,dictionary5,
    dictionary6,dictionary7,dictionary8,list_positive,texttype1):
    list_positve = []
    list_positve.append(dictionary0[texttype1])
    list_positve.append(dictionary1[texttype1])
    list_positve.append(dictionary2[texttype1])
    list_positve.append(dictionary3[texttype1])
    list_positve.append(dictionary4[texttype1])
    list_positve.append(dictionary5[texttype1])
    list_positve.append(dictionary6[texttype1])
    list_positve.append(dictionary7[texttype1])
    list_positve.append(dictionary8[texttype1])
    return list_positve

#keep two decimal part
def format (result):
    result = float("{0:.2f}".format(result))
    return result 

# the method is used to calcute the average result 
def process_result(dictionary,dictionary_result):

    if dictionary["times"]== 0:
        dictionary["times"] = 1

    dictionary_result["positive"] = format(dictionary["positive"]/dictionary["times"])
    dictionary_result["negative"] = format(dictionary["negative"]/dictionary["times"])
    dictionary_result["neutral"] = format(dictionary["neutral"]/dictionary["times"])
  
       

# do the statistics of sentiment result and times in different suburbs
def count_data(dictionary,label):
        dictionary["times"] = dictionary["times"]+1
        if label == 1:
            dictionary["positive"] = dictionary["positive"]+1
        elif label == 0:
            dictionary["neutral"] = dictionary["neutral"]+1
        elif label == -1:
            dictionary["negative"] = dictionary["negative"]+1
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


server = couchdb.Server('http://115.146.95.129:5984/',full_commit = True, session = None)   # the url of the server
#db = server['dstwitter']
db = server['new_dstweet']
#db = server['twitter']     # the name of the database

# server = couchdb.Server('http://127.0.0.1:5984/',full_commit = True, session = None)   # the url of the server
# db = server['mydatabase']    # the name of the database
# dbstore = server.create("myresult")

# try:
#     server.delete('district_happy')
#     print "successfully delete"
# except:
#         print "there is no database can be deleted"
# dbstore = server.create('district_happy')
# print ('successfully created new db')


try:
    dbstore = server['district_happy']
    dbstore.delete(dbstore["1"])
    dbstore.delete(dbstore["2"])
    dbstore.delete(dbstore["3"])
    dbstore.delete(dbstore["4"])

except:
    dbstore = server.create('district_happy')
    print ('successfully created new db')


Melbourne_Inner = location_dictionary("dictionary")
Melbourne_Inner_East = location_dictionary("dictionary")
Melbourne_Inner_South = location_dictionary("dictionary")
Melbourne_North_East = location_dictionary("dictionary")
Melbourne_North_West = location_dictionary("dictionary")
Melbourne_Outer_East = location_dictionary("dictionary")
Melbourne_South_East = location_dictionary("dictionary")
Melbourne_West = location_dictionary("dictionary")
Mornington_Peninsula = location_dictionary("dictionary")


Melbourne_Inner_result = result_dictionary("dictionary")
Melbourne_Inner_East_result = result_dictionary("dictionary")
Melbourne_Inner_South_result = result_dictionary("dictionary")
Melbourne_North_East_result = result_dictionary("dictionary")
Melbourne_North_West_result = result_dictionary("dictionary")
Melbourne_Outer_East_result = result_dictionary("dictionary")
Melbourne_South_East_result = result_dictionary("dictionary")
Melbourne_West_result = result_dictionary("dictionary")
Mornington_Peninsula_result = result_dictionary("dictionary") 


#for id in db:

for id in couchdb_pager(db):
    tweet= Tweet.load(db,id)
    label = tweet.sentiment
    location = tweet.district

    if location =="Melbourne_Inner":
        count_data(Melbourne_Inner,label)

    elif location =="Melbourne_Inner_East":
        count_data(Melbourne_Inner_East,label)

    elif location =="Melbourne_Inner_South":
        count_data(Melbourne_Inner_South,label)

    elif location =="Melbourne_North_East":
        count_data(Melbourne_North_East,label) 

    elif location =="Melbourne_North_West":
        count_data(Melbourne_North_West,label)

    elif location =="Melbourne_Outer_East":
        count_data(Melbourne_Outer_East,label) 

    elif location =="Melbourne_South_East":
        count_data(Melbourne_South_East,label)

    elif location =="Melbourne_West":
        count_data(Melbourne_West,label)

    elif location =="Mornington_Peninsula":
        count_data(Mornington_Peninsula,label)

    else:
        pass

doc1 = {"_id":"1","Melbourne_Inner":Melbourne_Inner,
"Melbourne_Inner_East":Melbourne_Inner_East,
"Melbourne_Inner_South":Melbourne_Inner_South,
"Melbourne_North_East":Melbourne_North_East,
"Melbourne_North_West":Melbourne_North_West,
"Melbourne_Outer_East":Melbourne_Outer_East,
"Melbourne_South_East":Melbourne_South_East,
"Mornington_Peninsula":Mornington_Peninsula,
"Melbourne_West":Melbourne_West}

dbstore.save(doc1)

positive_times = return_times(Melbourne_Inner, Melbourne_Inner_East, Melbourne_Inner_South,
Melbourne_North_East, Melbourne_North_West, Melbourne_Outer_East, 
    Melbourne_South_East, Melbourne_West, Mornington_Peninsula, 
    "positive_times","positive")

negative_times = return_times(Melbourne_Inner, Melbourne_Inner_East, Melbourne_Inner_South,
Melbourne_North_East, Melbourne_North_West, Melbourne_Outer_East, 
    Melbourne_South_East, Melbourne_West, Mornington_Peninsula, 
    "negative_times","negative")


neutral_times = return_times(Melbourne_Inner, Melbourne_Inner_East, Melbourne_Inner_South,
Melbourne_North_East, Melbourne_North_West, Melbourne_Outer_East, 
    Melbourne_South_East, Melbourne_West, Mornington_Peninsula, 
    "neutral_times","neutral")

total_times = return_times(Melbourne_Inner, Melbourne_Inner_East, Melbourne_Inner_South,
Melbourne_North_East, Melbourne_North_West, Melbourne_Outer_East, 
    Melbourne_South_East, Melbourne_West, Mornington_Peninsula, 
    "total_times","times")




if total_times ==0:
                    total_times = total_times+1

positive_ratio = format(positive_times/total_times)
negative_ratio = format(negative_times/total_times)
neutral_ratio = format(neutral_times/total_times)

doc4 = {"_id":"4","Happy_ratio":positive_ratio,"Unhappy_ratio":negative_ratio,"Happy_times":positive_times,
"Unhappy_times":negative_times,"Total_times":total_times}

dbstore.save(doc4)

process_result(Melbourne_Inner,Melbourne_Inner_result)
process_result(Melbourne_Inner_East,Melbourne_Inner_East_result)
process_result(Melbourne_Inner_South,Melbourne_Inner_South_result)
process_result(Melbourne_North_East,Melbourne_North_East_result)
process_result(Melbourne_North_West,Melbourne_North_West_result)
process_result(Melbourne_Outer_East,Melbourne_Outer_East_result)
process_result(Melbourne_South_East,Melbourne_South_East_result)
process_result(Melbourne_West,Melbourne_West_result)
process_result(Mornington_Peninsula,Mornington_Peninsula_result)

doc2 = {"_id":"2","Melbourne_Inner_result":Melbourne_Inner_result,
"Melbourne_Inner_East_result":Melbourne_Inner_East_result,
"Melbourne_Inner_South_result":Melbourne_Inner_South_result,
"Melbourne_North_East_result":Melbourne_North_East_result,
"Melbourne_North_West_result":Melbourne_North_West_result,
"Melbourne_Outer_East_result":Melbourne_Outer_East_result,
"Melbourne_South_East_result":Melbourne_South_East_result,
"Melbourne_West_result":Melbourne_West_result,
"Mornington_Peninsula_result":Mornington_Peninsula_result}

dbstore.save(doc2)

positive = return_list(Melbourne_Inner_result, Melbourne_Inner_East_result, Melbourne_Inner_South_result,
Melbourne_North_East_result, Melbourne_North_West_result, Melbourne_Outer_East_result, 
    Melbourne_South_East_result, Melbourne_West_result, Mornington_Peninsula_result, 
    "positive","positive")

neutral = return_list(Melbourne_Inner_result, Melbourne_Inner_East_result, Melbourne_Inner_South_result,
Melbourne_North_East_result, Melbourne_North_West_result, Melbourne_Outer_East_result, 
    Melbourne_South_East_result, Melbourne_West_result, Mornington_Peninsula_result, 
    "nautral","neutral")

negative = return_list(Melbourne_Inner_result, Melbourne_Inner_East_result, Melbourne_Inner_South_result,
Melbourne_North_East_result, Melbourne_North_West_result, Melbourne_Outer_East_result, 
    Melbourne_South_East_result, Melbourne_West_result, Mornington_Peninsula_result, 
    "negative","negative")

positive.append(positive_ratio)
negative.append(negative_ratio)
neutral.append(neutral_ratio)

doc3 ={"_id":"3","Happy": positive,
       "Neutral": neutral,
       "Unhappy": negative,}
    
dbstore.save(doc3)

print
print 
print  "Melbourne_Inner", Melbourne_Inner
print  "Melbourne_Inner_East", Melbourne_Inner_East
print  "Melbourne_Inner_South", Melbourne_Inner_South
print  "Melbourne_North_East", Melbourne_North_East
print  "Melbourne_North_West", Melbourne_North_West
print  "Melbourne_Outer_East", Melbourne_Outer_East
print  "Melbourne_South_East", Melbourne_South_East
print  "Melbourne_West", Melbourne_West
print  "Mornington_Peninsula", Mornington_Peninsula
print 
print 
print  "Melbourne_Inner_result", Melbourne_Inner_result
print  "Melbourne_Inner_East_result", Melbourne_Inner_East_result
print  "Melbourne_Inner_South_result", Melbourne_Inner_South_result
print  "Melbourne_North_East_result", Melbourne_North_East_result
print  "Melbourne_North_West_result", Melbourne_North_West_result
print  "Melbourne_Outer_East_result", Melbourne_Outer_East_result
print  "Melbourne_South_East_result", Melbourne_South_East_result
print  "Melbourne_West_result", Melbourne_West_result


print 
print 
print "positive", positive
print "neutral", neutral
print "negative", negative












        
