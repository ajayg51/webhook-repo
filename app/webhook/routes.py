from flask import Blueprint, json, request, render_template
import sched, time, datetime


from app.extensions import *


info = 'data from api'

webhook = Blueprint('Webhook', __name__)

# will do later

# @webhook.errorhandler(404)
# def get_error_page(error):
#     print("here")
#     return "404 page not found"

@webhook.route('/', methods=["GET"])
def get_root():
    return render_template('index.html')



@webhook.route('/github', methods=['GET','POST'])
def get_gh_api():
    global info
    print("request")
    print(request)
    print("headers")
    print(request.headers)
    print("content-type")
    print(request.content_type)

    if(request.method == 'POST'):
        
        if(request.headers["Content-Type"]) == "application/json":
            eventType = request.headers["X-Github-Event"]
            print("Event type push/pull/merge")
            print(eventType)
            
            dumpData = json.dumps(request.json)
            info = json.loads(dumpData)
            info["eventType"] = eventType
            print("model data  : run.py \n :: ")
            print(info)
            postInfoToMongo(info)

            return "Success"
    else:
        print("get")
        
        return info



@webhook.route('/get-data',methods=['GET','POST'])
def get_data():
    print("cur timestamp :")
    print(datetime.datetime.now())
    data = get_atlas_data()
    print('data')
    print('')
    print(data)
    eventType = data['eventType']
    author = data['author']
    fromBranch = data['fromBranch']
    toBranch = data['toBranch']
    timestamp = data['timestamp']
    timestamp = datetime.datetime.fromisoformat(timestamp)
    timestamp = datetime.datetime.strptime(str(timestamp), "%Y-%m-%d %H:%M:%S%z")  
    timestamp = timestamp.strftime("%A %B %d %Y %H:%M:%S")
    
    timestampList = timestamp.split()
    print("timestamp list")
    print(timestampList)
    print("reversed timestamp list")
    print(timestampList[-1])
    hour = int(timestampList[-1].split(":")[0])
    print(hour)
    if(hour > 12):
        hour -= 12
        print("PM")
        timestamp += " PM" 
    else:
        print("AM")
        timestamp += " AM" 

    print('eventType')
    print(eventType)
    print('author')
    print(author)
    print('fromBranch')
    print(fromBranch)
    print('toBranch')
    print(toBranch)
    print('timestamp')
    print(timestamp)
    print()

    datum = {
        "eventType":eventType,
        "author":author,
        "fromBranch":fromBranch,
        "toBranch" : toBranch,
        "timestamp" : timestamp,
    }

    return datum
    
