from pymongo import MongoClient

# Setup MongoDB here
uri = "mongodb+srv://ajaygug18cs:lKxlCW5spkSSYATo@ajayg51.wac04mp.mongodb.net/?retryWrites=true&w=majority&appName=ajayg51"





db_data = {
    "eventType" : "",
    "author":"",
    "fromBranch":"",
    "toBranch":"",
    "timestamp":""
}





post_schema = {
    'eventType' : {
        'type' : 'string',
        'required' : True,
    },
    'author' : {
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
        "author":authorName,
        "commitMsg":commitMsg,
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
        
        client.close()

    except Exception as e:
        print("Error : Exception")
        print(e)    


   

