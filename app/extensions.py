from pymongo import MongoClient

# Setup MongoDB here
uri = "mongodb+srv://ajaygug18cs:lKxlCW5spkSSYATo@ajayg51.wac04mp.mongodb.net/?retryWrites=true&w=majority&appName=ajayg51"





db_data = {
    "commitAuthor": "",
    "commitBranch":"",
    "commitMessage":"",
    "eventType" : "",
    "fromBranch":"",
    "toBranch":"",
    "timestamp":""
}





post_schema = {
#     "commitAuthor": "Ajay Kumar Gond",
#   "commitBranch": "origin/main",
#   "commitMessage": "Merge pull request #4 from ajayg51/pr_check_branch\n\nM run.py at 4:48",
#   "eventType": "Merge",
#   "fromBranch": "N/A",
#   "timestamp": "Wed, 10 Apr 2024 11:19:56 GMT",
#   "toBranch": "N/A"
    'commitAuthor':{
        'type' : 'string',
        'required' : True,
    },
    'commitBranch':{
        'type' : 'string',
        'required' : True,
    },
    'commitMessage':{
        'type' : 'string',
        'required' : True,
    },
    'eventType' : {
        'type' : 'string',
        'required' : True,
    },
    'commitAuthor' : {
        'type' : 'string',
        'required' : True,
    },
    'fromBranch' : {
        'type' : 'string',
        'required' : True,
    },
    'toBranch' : {
        'type' : 'string',
        'required' : True,
    },
    'timestamp' : {
        'type' : 'string',
        'required' : True,
    }
}


def parseInfo(infoModel):
    
    # infoModel = {
    #         "commitMessage": commitMessage,
    #         "commitAuthor": commitAuthor,
    #         "commitDateTime": commitDateTime,
    #         "eventType" : eventType,
    #     }

    commitBranch = infoModel["commitBranch"] 
    authorName = infoModel["commitAuthor"]
    commitMsg = infoModel["commitMessage"]
    fromBranch = infoModel["fromBranch"]
    toBranch = infoModel["toBranch"]
    eventType = infoModel["eventType"]
    timeStamp = infoModel["timestamp"]

    print("eventType : ")
    print(eventType)
    print()
    print("author : ")
    print(authorName)
    datum = {
        "commitBranch" : commitBranch,
        "commitAuthor":authorName,
        "commitMessage":commitMsg,
        "fromBranch":fromBranch,
        "toBranch" : toBranch,
        "eventType" : eventType,
        "timestamp" : timeStamp,
    }

    return datum
    

def postInfoToMongo(dataModel): 
    # print("postInfoToMongo : extensions.py :: \n")
    # print()
    # print(data)
    
    client = MongoClient(uri)
    db = client.webhooks
    collection = db.get_collection('gh-webhooks')


    print("db")
    print(db)
    print("\n\ncollection")
    print(collection)

    
    datum = parseInfo(dataModel)


    try:
        
        # client.admin.command('ping')
        # print("Pinged your deployment. You successfully connected to MongoDB!")

        collection.insert_one(datum)
        print("Added dataum to MongoDB database")
        
        # Close the connection
        client.close()
        

    except Exception as e:
        print("Error : Exception")
        print(e)    


def get_atlas_data():
    client = MongoClient(uri)
    db = client.webhooks
    try:
        collection = db.get_collection('gh-webhooks')
        cursor = collection.find({})
        data = []
        print("cursor")
        print(cursor)
        for datum in cursor:
            data.append(datum)
        data.reverse()

        return data[0]

        # return cursor[-1]
        
        client.close()

    except Exception as e:
        
        print("Error : Exception")
        print(e)    
        return("Exception : check logs")
    return "something went wrong!"


   

