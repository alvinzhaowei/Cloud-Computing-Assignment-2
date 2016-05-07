# coding: utf-8
from __future__ import division
import couchdb 
from couchdb.mapping import Document, TextField, IntegerField, DictField, Mapping
import re



server = couchdb.Server('http://115.146.95.129:5984/',full_commit = True, session = None)   # the url of the server
db = server['dstwitter']
#db = server['twitter']     # the name of the database

# server = couchdb.Server('http://127.0.0.1:5984//',full_commit = True, session = None)   # the url of the server
# db = server['mydatabase']    # the name of the database

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


def process_result(dictionary,dictionary_result):
    result_morning = dictionary["morning"]["value"]/dictionary["morning"]["times"]
    result_evening = dictionary["evening"]["value"]/dictionary["evening"]["times"]
    dictionary_result["morning"] = result_morning
    dictionary_result["evening"] = result_evening
    

def date_check (date_text):
    target_line_list = date_text.split(" ")
    if re.match(morning_regex,target_line_list[3]):
        return "morning"
    elif re.match(night_regex,target_line_list[3]):
        return "evening"
    else:
        pass
    


class Tweet(Document):
    district = TextField()
    text = TextField()
    created_time = TextField()
    sentiment = IntegerField()

      
for id in db:

    tweet= Tweet.load(db,id)
    time = tweet.created_time
    label = tweet.sentiment
    location = tweet.district

    if location =="Melbourne_Inner":
        if date_check (time) =="morning":
            Melbourne_Inner["morning"]["value"] = Melbourne_Inner["morning"]["value"]+label
            Melbourne_Inner["morning"]["times"] = Melbourne_Inner["morning"]["times"]+1
        elif date_check (time) == "evening":
            Melbourne_Inner["evening"]["value"] = Melbourne_Inner["evening"]["value"]+label
            Melbourne_Inner["evening"]["times"] = Melbourne_Inner["evening"]["times"]+1
        else:
            pass

    elif location =="Melbourne_Inner_East":
            if date_check (time) == "morning":
                Melbourne_Inner_East["morning"]["value"] = Melbourne_Inner_East["morning"]["value"]+label
                Melbourne_Inner_East["morning"]["times"] = Melbourne_Inner_East["morning"]["times"]+1
            elif date_check (time) == "evening":
                Melbourne_Inner_East["evening"]["value"] = Melbourne_Inner_East["evening"]["value"]+label
                Melbourne_Inner_East["evening"]["times"] = Melbourne_Inner_East["evening"]["times"]+1
            else:
                pass 

    elif location =="Melbourne_Inner_South":
            if date_check (time) == "morning":
                Melbourne_Inner_South["morning"]["value"] = Melbourne_Inner_South["morning"]["value"]+label
                Melbourne_Inner_South["morning"]["times"] = Melbourne_Inner_South["morning"]["times"]+1
            elif date_check (time) == "evening":
                Melbourne_Inner_South["evening"]["value"] = Melbourne_Inner_South["evening"]["value"]+label
                Melbourne_Inner_South["evening"]["times"] = Melbourne_Inner_South["evening"]["times"]+1
            else:
                pass 

    elif location =="Melbourne_North_East":
            if date_check (time) == "morning":
                Melbourne_North_East["morning"]["value"] = Melbourne_North_East["morning"]["value"]+label
                Melbourne_North_East["morning"]["times"] = Melbourne_North_East["morning"]["times"]+1
            elif date_check (time) == "evening":
                Melbourne_North_East["evening"]["value"] = Melbourne_North_East["evening"]["value"]+label
                Melbourne_North_East["evening"]["times"] = Melbourne_North_East["evening"]["times"]+1
            else:
                pass 

    elif location =="Melbourne_North_West":
            if date_check (time) == "morning":
                Melbourne_North_West["morning"]["value"] = Melbourne_North_West["morning"]["value"]+label
                Melbourne_North_West["morning"]["times"] = Melbourne_North_West["morning"]["times"]+1
            elif date_check (time) == "evening":
                Melbourne_North_West["evening"]["value"] = Melbourne_North_West["evening"]["value"]+label
                Melbourne_North_West["evening"]["times"] = Melbourne_North_West["evening"]["times"]+1
            else:
                pass 

    elif location =="Melbourne_Outer_East":
            if date_check (time) == "morning":
                Melbourne_Outer_East["morning"]["value"] = Melbourne_Outer_East["morning"]["value"]+label
                Melbourne_Outer_East["morning"]["times"] = Melbourne_Outer_East["morning"]["times"]+1
            elif date_check (time) == "evening":
                Melbourne_Outer_East["evening"]["value"] = Melbourne_Outer_East["evening"]["value"]+label
                Melbourne_Outer_East["evening"]["times"] = Melbourne_Outer_East["evening"]["times"]+1
            else:
                pass 

    elif location =="Melbourne_South_East":
            if date_check (time) == "morning":
                Melbourne_South_East["morning"]["value"] = Melbourne_South_East["morning"]["value"]+label
                Melbourne_South_East["morning"]["times"] = Melbourne_South_East["morning"]["times"]+1
            elif date_check (time) == "evening":
                Melbourne_South_East["evening"]["value"] = Melbourne_South_East["evening"]["value"]+label
                Melbourne_South_East["evening"]["times"] = Melbourne_South_East["evening"]["times"]+1
            else:
                pass 

    elif location =="Melbourne_West":
            if date_check (time) == "morning":
                Melbourne_West["morning"]["value"] = Melbourne_West["morning"]["value"]+label
                Melbourne_West["morning"]["times"] = Melbourne_West["morning"]["times"]+1
            elif date_check (time) == "evening":
                Melbourne_West["evening"]["value"] = Melbourne_West["evening"]["value"]+label
                Melbourne_West["evening"]["times"] = Melbourne_West["evening"]["times"]+1
            else:
                pass

    elif location =="Mornington_Peninsula":
            if date_check (time) == "morning":
                Mornington_Peninsula["morning"]["value"] = Mornington_Peninsula["morning"]["value"]+label
                Mornington_Peninsula["morning"]["times"] = Mornington_Peninsula["morning"]["times"]+1
            elif date_check (time) == "evening":
                Mornington_Peninsula["evening"]["value"] = Mornington_Peninsula["evening"]["value"]+label
                Mornington_Peninsula["evening"]["times"] = Mornington_Peninsula["evening"]["times"]+1
            else:
                pass 

    else:
        pass
        

# process_result(Melbourne_Inner,Melbourne_Inner_result)
# process_result(Melbourne_Inner_East,Melbourne_Inner_East_result)
# process_result(Melbourne_Inner_South,Melbourne_Inner_South_result)
# process_result(Melbourne_North_East,Melbourne_North_East_result)
# process_result(Melbourne_North_West,Melbourne_North_West_result)
# process_result(Melbourne_Outer_East,Melbourne_Outer_East_result)
# process_result(Melbourne_South_East,Melbourne_South_East_result)
# process_result(Melbourne_West,Melbourne_West_result)
# process_result(Mornington_Peninsula,Mornington_Peninsula_result)


print  "Melbourne_Inner", Melbourne_Inner
print  "Melbourne_Inner_East", Melbourne_Inner_East
print  "Melbourne_Inner_South", Melbourne_Inner_South
print  "Melbourne_North_East", Melbourne_North_East
print  "Melbourne_North_West", Melbourne_North_West
print  "Melbourne_Outer_East", Melbourne_Outer_East
print  "Melbourne_South_East", Melbourne_South_East
print  "Melbourne_West", Melbourne_West
print  "Mornington_Peninsula", Mornington_Peninsula



# print  "Melbourne_Inner_result", Melbourne_Inner_result
# print  "Melbourne_Inner_East_result", Melbourne_Inner_East_result
# print  "Melbourne_Inner_South_result", Melbourne_Inner_South_result
# print  "Melbourne_North_East_result", Melbourne_North_East_result
# print  "Melbourne_North_West_result", Melbourne_North_West_result
# print  "Melbourne_Outer_East_result", Melbourne_Outer_East_result
# print  "Melbourne_South_East_result", Melbourne_South_East_result
# print  "Melbourne_West_result", Melbourne_West_result
# print  "Mornington_Peninsula_result", Mornington_Peninsula_result









        
