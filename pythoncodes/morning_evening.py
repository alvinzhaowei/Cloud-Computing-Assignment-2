# coding: utf-8
from __future__ import division
import couchdb 
from couchdb.mapping import Document, TextField, IntegerField, DictField, Mapping
import re

#this code is used to count count the ratio of morning happy, evening happy and morning unhappy and
#evening unhappy
#

#define the tyoe of dictionary    
def location_dictionary(dictionary):
    dictionary = {"morning":{"positive":0, "negative":0,"neutral":0,"times":0},
    "evening":{"positive":0, "negative":0,"neutral":0,"times":0}}
    return dictionary

#define the type of dictionary
def result_dictionary(dictionary):
    dictionary = {"morning":{"positive":0, "negative":0,"neutral":0},
    "evening":{"positive":0, "negative":0,"neutral":0}}
    return dictionary

def return_times(dictionary0,dictionary1,dictionary2,dictionary3,dictionary4,dictionary5,
    dictionary6,dictionary7,dictionary8,times,texttype1,texttype2):
    times = dictionary0[texttype1][texttype2]+dictionary1[texttype1][texttype2]\
    +dictionary2[texttype1][texttype2]+dictionary3[texttype1][texttype2]\
    +dictionary4[texttype1][texttype2]+dictionary5[texttype1][texttype2]\
    +dictionary6[texttype1][texttype2]+dictionary7[texttype1][texttype2]\
    +dictionary8[texttype1][texttype2]
    return times

# return the special data type from all discionaries
def return_list(dictionary0,dictionary1,dictionary2,dictionary3,dictionary4,dictionary5,
    dictionary6,dictionary7,dictionary8,list_positive,texttype1,texttype2):
    list_positve = []
    list_positve.append(dictionary0[texttype1][texttype2])
    list_positve.append(dictionary1[texttype1][texttype2])
    list_positve.append(dictionary2[texttype1][texttype2])
    list_positve.append(dictionary3[texttype1][texttype2])
    list_positve.append(dictionary4[texttype1][texttype2])
    list_positve.append(dictionary5[texttype1][texttype2])
    list_positve.append(dictionary6[texttype1][texttype2])
    list_positve.append(dictionary7[texttype1][texttype2])
    list_positve.append(dictionary8[texttype1][texttype2])
    return list_positve

#keep two decimal part
def format (result):
    result = float("{0:.2f}".format(result))
    return result 

# the method is used to calcute the average result 
def process_result(dictionary,dictionary_result):

    if dictionary["morning"]["times"]== 0:
        dictionary["morning"]["times"] = 1

    if dictionary["evening"]["times"]== 0:
        dictionary["evening"]["times"] = 1

    dictionary_result["morning"]["positive"] = format(dictionary["morning"]["positive"]/dictionary["morning"]["times"])
    dictionary_result["morning"]["negative"] = format(dictionary["morning"]["negative"]/dictionary["morning"]["times"])
    dictionary_result["morning"]["neutral"] = format(dictionary["morning"]["neutral"]/dictionary["morning"]["times"])
    dictionary_result["evening"]["positive"] = format(dictionary["evening"]["positive"]/dictionary["evening"]["times"])
    dictionary_result["evening"]["negative"] = format(dictionary["evening"]["negative"]/dictionary["evening"]["times"])
    dictionary_result["evening"]["neutral"] = format(dictionary["evening"]["neutral"]/dictionary["evening"]["times"])
       
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
def count_data(dictionary,time,label):
    if date_check (time) =="morning":
        dictionary["morning"]["times"] = dictionary["morning"]["times"]+1
        if label == 1:
            dictionary["morning"]["positive"] = dictionary["morning"]["positive"]+1
        elif label == 0:
            dictionary["morning"]["neutral"] = dictionary["morning"]["neutral"]+1
        elif label == -1:
            dictionary["morning"]["negative"] = dictionary["morning"]["negative"]+1
        else:
            pass
    elif date_check (time) == "evening":
        dictionary["evening"]["times"] = dictionary["evening"]["times"]+1
        if label == 1:
            dictionary["evening"]["positive"] = dictionary["evening"]["positive"]+1
        elif label == 0:
            dictionary["evening"]["neutral"] = dictionary["evening"]["neutral"]+1
        elif label == -1:
            dictionary["evening"]["negative"] = dictionary["evening"]["negative"]+1
        else:
            pass
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


#server = couchdb.Server('http://115.146.95.129:5984/') 
server = couchdb.Server('http://115.146.95.129:5984/',full_commit = True, session = None)   # the url of the server
#db = server['dstwitter']
db = server['new_dstweet']
#db = server['twitter']     # the name of the database

# server = couchdb.Server('http://127.0.0.1:5984/',full_commit = True, session = None)   # the url of the server
# db = server['mydatabase']    # the name of the database
# dbstore = server.create("myresult")

# try:
#     server.delete('myresult_morning_evening')
#     print "successfully delete"
# except:
#     print "there is no database can be deleted"


# dbstore = server.create('myresult_morning_evening')
# print ('successfully created new db')



try:
    dbstore = server['myresult_morning_evening']
    dbstore.delete(dbstore["1"])
    dbstore.delete(dbstore["2"])
    dbstore.delete(dbstore["3"])
    dbstore.delete(dbstore["4"])

except:
    dbstore = server.create('myresult_morning_evening')
    print ('successfully created new db')


morning_regex = '^(0[6-9]|1[0-1]):[0-5]\d{1}:([0-5]\d{1})$'   
night_regex = '^(1[8-9]|2[0-3]):[0-5]\d{1}:([0-5]\d{1})$'  

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
#k = 0
for id in couchdb_pager(db):
    #k+=1
    tweet= Tweet.load(db,id)
    time = tweet.created_time
    label = tweet.sentiment
    location = tweet.district

    if location =="Melbourne_Inner":
        count_data(Melbourne_Inner,time,label)

    elif location =="Melbourne_Inner_East":
        count_data(Melbourne_Inner_East,time,label)

    elif location =="Melbourne_Inner_South":
        count_data(Melbourne_Inner_South,time,label)

    elif location =="Melbourne_North_East":
        count_data(Melbourne_North_East,time,label) 

    elif location =="Melbourne_North_West":
        count_data(Melbourne_North_West,time,label)

    elif location =="Melbourne_Outer_East":
        count_data(Melbourne_Outer_East,time,label) 

    elif location =="Melbourne_South_East":
        count_data(Melbourne_South_East,time,label)

    elif location =="Melbourne_West":
        count_data(Melbourne_West,time,label)

    elif location =="Mornington_Peninsula":
        count_data(Mornington_Peninsula,time,label)

    else:
        pass
    # if k  ==100:
    #     break           
               
doc1 = {"_id":"1","Melbourne_Inner":Melbourne_Inner,
"Melbourne_Inner_East":Melbourne_Inner_East,
"Melbourne_Inner_South":Melbourne_Inner_South,
"Melbourne_North_East":Melbourne_North_East,
"Melbourne_North_West":Melbourne_North_West,
"Melbourne_Outer_East":Melbourne_Outer_East,
"Melbourne_South_East":Melbourne_South_East,
"Mornington_Peninsula":Mornington_Peninsula,
"Melbourne_West":Melbourne_West}

#count the times of tweets

morning_positive_times = return_times(Melbourne_Inner, Melbourne_Inner_East, Melbourne_Inner_South,
Melbourne_North_East, Melbourne_North_West, Melbourne_Outer_East, 
    Melbourne_South_East, Melbourne_West, Mornington_Peninsula, 
    "morning_positive_times","morning","positive")

morning_negative_times = return_times(Melbourne_Inner, Melbourne_Inner_East, Melbourne_Inner_South,
Melbourne_North_East, Melbourne_North_West, Melbourne_Outer_East, 
    Melbourne_South_East, Melbourne_West, Mornington_Peninsula, 
    "morning_negative_times","morning","negative")

evening_positive_times = return_times(Melbourne_Inner, Melbourne_Inner_East, Melbourne_Inner_South,
Melbourne_North_East, Melbourne_North_West, Melbourne_Outer_East, 
    Melbourne_South_East, Melbourne_West, Mornington_Peninsula, 
    "evening_positive_times","evening","positive")

evening_negative_times = return_times(Melbourne_Inner, Melbourne_Inner_East, Melbourne_Inner_South,
Melbourne_North_East, Melbourne_North_West, Melbourne_Outer_East, 
    Melbourne_South_East, Melbourne_West, Mornington_Peninsula, 
    "evening_negative_times","evening","negative")



morning_times_in_nine_location = return_times(Melbourne_Inner, Melbourne_Inner_East, Melbourne_Inner_South,
Melbourne_North_East, Melbourne_North_West, Melbourne_Outer_East, 
    Melbourne_South_East, Melbourne_West, Mornington_Peninsula, 
    "morning_times_in_nine_location","morning","times")


evening_times_in_nine_location = return_times(Melbourne_Inner, Melbourne_Inner_East, Melbourne_Inner_South,
Melbourne_North_East, Melbourne_North_West, Melbourne_Outer_East, 
    Melbourne_South_East, Melbourne_West, Mornington_Peninsula, 
    "evening_times_in_nine_location","evening","times")


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



morning_positive = return_list(Melbourne_Inner_result, Melbourne_Inner_East_result, Melbourne_Inner_South_result,
Melbourne_North_East_result, Melbourne_North_West_result, Melbourne_Outer_East_result, 
    Melbourne_South_East_result, Melbourne_West_result, Mornington_Peninsula_result, 
    "morning_positive","morning","positive")

morning_neutral = return_list(Melbourne_Inner_result, Melbourne_Inner_East_result, Melbourne_Inner_South_result,
Melbourne_North_East_result, Melbourne_North_West_result, Melbourne_Outer_East_result, 
    Melbourne_South_East_result, Melbourne_West_result, Mornington_Peninsula_result, 
    "morning_nautral","morning","neutral")

morning_negative = return_list(Melbourne_Inner_result, Melbourne_Inner_East_result, Melbourne_Inner_South_result,
Melbourne_North_East_result, Melbourne_North_West_result, Melbourne_Outer_East_result, 
    Melbourne_South_East_result, Melbourne_West_result, Mornington_Peninsula_result, 
    "morning_negative","morning","negative")


evening_positive = return_list(Melbourne_Inner_result, Melbourne_Inner_East_result, Melbourne_Inner_South_result,
Melbourne_North_East_result, Melbourne_North_West_result, Melbourne_Outer_East_result, 
    Melbourne_South_East_result, Melbourne_West_result, Mornington_Peninsula_result, 
    "evening_positive","evening","positive")

evening_neutral = return_list(Melbourne_Inner_result, Melbourne_Inner_East_result, Melbourne_Inner_South_result,
Melbourne_North_East_result, Melbourne_North_West_result, Melbourne_Outer_East_result, 
    Melbourne_South_East_result, Melbourne_West_result, Mornington_Peninsula_result, 
    "evening_neutral","evening","neutral")

evening_negative = return_list(Melbourne_Inner_result, Melbourne_Inner_East_result, Melbourne_Inner_South_result,
Melbourne_North_East_result, Melbourne_North_West_result, Melbourne_Outer_East_result, 
    Melbourne_South_East_result, Melbourne_West_result, Mornington_Peninsula_result, 
    "evening_negative","evening","negative")



totoal_positive_times = morning_positive_times+evening_positive_times

totoal_negative_times = morning_negative_times+evening_negative_times

total_times = morning_times_in_nine_location+evening_times_in_nine_location

if total_times ==0:
    total_times = total_times+1

morning_positive_ratio = format(morning_positive_times/total_times)

evening_positive_ratio = format(evening_positive_times/total_times)

if total_times ==0:
    total_times = total_times+1

morning_negative_ratio = format(morning_negative_times/total_times)

evening_negative_ratio = format(evening_negative_times/total_times)




morning_positive.append(morning_positive_ratio)
morning_negative.append(evening_positive_ratio)
evening_positive.append(morning_positive_ratio)
evening_negative.append(evening_negative_ratio)

doc3 ={"_id":"3","Morning_Happy": morning_positive,
       "Morning_Unhappy": morning_negative,
       "Evening_Happy": evening_positive,
       "Evening_Unhappy": evening_negative}

doc4 = {"_id":"4", "morning_happy":morning_positive_times, "morning_unhappy":morning_negative_times,
"evening_happy":evening_positive_times,"evening_unhappy":evening_negative_times,
"totoal_happy_times":totoal_positive_times,"morning_happy_ratio":morning_positive_ratio,
"morning_unhappy_ratio":morning_negative_ratio,
"evening_happy_ratio":evening_positive_ratio,"evening_unhappy_ratio":evening_negative_ratio,
"totoal_unhappy_times":totoal_negative_times,
"tatal_times_in_nine_location":total_times,"morning_times_in_nine_location":morning_times_in_nine_location,
"evening_times_in_nine_location":evening_times_in_nine_location}


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
print  "Mornington_Peninsula_result", Mornington_Peninsula_result

print 
print 
print "morning_positive", morning_positive
print "morning_neutral", morning_neutral
print "morning_negative", morning_negative

print "evening_positive", evening_positive
print "evening_neutral", evening_neutral
print "evening_negative", evening_negative





dbstore.save(doc1)
dbstore.save(doc2)
dbstore.save(doc3)
dbstore.save(doc4)










        
