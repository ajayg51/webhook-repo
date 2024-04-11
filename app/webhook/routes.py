from flask import Blueprint, json, request, render_template
import sched, time, datetime

# import git, subprocess, requests, os, shutil
# import pytz


from app.extensions import *
# from app.template import *


info = 'data from api'

webhook = Blueprint(
    'webhook',
    __name__,
 )



# REPO_URL = "https://github.com/ajayg51/action-repo.git"
# LOCAL_REPO_PATH = "/Volumes/ajaySafeBox/0_projects/dev/0_self/3_python/action-repo"

# LOCAL_ACTION_REPO = git.Repo(LOCAL_REPO_PATH)



# will do later

# @webhook.errorhandler(404)
# def get_error_page(error):
#     print("here")
#     return "404 page not found"

@webhook.route('/', methods=["GET"])
def get_root():
    # return "Hello world"
    return render_template('index.html')

@webhook.route('/e1', methods=["GET"])
def get_action_repo_info():
    request_data = request.get_json()
    data = {
        "request" : {
            "branch" : "master"
        }
    }




@webhook.route('/e2', methods=["GET"])
def get_webhook_repo_info():
    # return "Hello world"
    return render_template('index.html')


# def get_github_response_api():
#     global info
#     print("request")
#     print(request)
#     print("headers")
#     print(request.headers)
#     print("content-type")
#     print(request.content_type)

#     if(request.method == 'POST'):
        
#         if(request.headers["Content-Type"]) == "application/json":
#             eventType = request.headers["X-Github-Event"]
#             print("Event type push/pull/merge")
#             print(eventType)
            
#             dumpData = json.dumps(request.json)
#             info = json.loads(dumpData)
#             info["eventType"] = eventType
#             print("model data  : run.py \n :: ")
#             print(info)
#             postInfoToMongo(info)

#             return "Success"
#     else:
#         print("get")
        
#         return info

# def get_commit_info():
  
#     try:
#         # localRepoHeadCommit = LOCAL_REPO_LAST_HEAD_COMMIT_ID
        
        

#         eventType = ""
#         # if len(localRepoHeadCommit.parents) > 1 :
#         #     eventType = "Merge"
#         #     print("Merge request found")
        
#         LOCAL_REPO_LAST_HEAD_COMMIT_ID = LOCAL_ACTION_REPO.head.commit
#         LOCAL_REPO_LAST_HEAD_COMMIT_ID_HASH = LOCAL_ACTION_REPO.head.object.hexsha


#         print("local - repo")
#         print(LOCAL_ACTION_REPO)
#         print("local - head")
#         print(LOCAL_REPO_LAST_HEAD_COMMIT_ID_HASH)

#         # remoteRepo = LOCAL_ACTION_REPO.remotes.origin
#         # remoteRepo.fetch()
#         # REMOTE_REPO_HEAD_COMMIT_ID_HASH = remoteRepo.refs["main"].object.hexsha
        
#         destinationDir = "./push/repo"
#         if(os.path.exists(destinationDir)):
#             shutil.rmtree(destinationDir)


#         remoteRepo = git.Repo.clone_from(REPO_URL, destinationDir, depth=1)
#         remoteRepoHeadCommit = remoteRepo.head.commit
#         print("remote head")
#         print(remoteRepoHeadCommit)


#         commitBranch = "N/A"

#         commitAuthor = LOCAL_REPO_LAST_HEAD_COMMIT_ID.author.name
#         commitMessage = LOCAL_REPO_LAST_HEAD_COMMIT_ID.message

#         timestamp = LOCAL_REPO_LAST_HEAD_COMMIT_ID.authored_datetime
#         print("timestamp")
#         print(timestamp)

#         timestamp =  datetime.datetime.strptime(str(timestamp), '%Y-%m-%d %H:%M:%S%z')
#         timestamp = timestamp.strftime('%d %B %Y %I:%M:%S %p') 
    
        
#         fromBranch = "N/A as Push event"
#         toBranch = "N/A as Push event"

#         for ref in LOCAL_ACTION_REPO.references:
#             if isinstance(ref, git.Head): 
#                 branch_name = ref.name
#                 for b_commit in LOCAL_ACTION_REPO.iter_commits(branch_name):
#                     if b_commit == LOCAL_REPO_LAST_HEAD_COMMIT_ID:
#                         print("branch - name")
#                         print(branch_name)
#                         commitBranch = branch_name

#         if LOCAL_REPO_LAST_HEAD_COMMIT_ID != remoteRepoHeadCommit :
#             eventType = "PUSH git action"
#             print("Push git action found")

#         print("local repo commit")
#         print(LOCAL_REPO_LAST_HEAD_COMMIT_ID)
#         print("remote repo commit")
#         print(remoteRepoHeadCommit)
#         print("author")
#         print(commitAuthor)
#         print("commit-msg")
#         print(commitMessage)
#         print("commitBranch")
#         print(commitBranch)
#         print("timestamp")
#         print(timestamp)


#         infoModel = {
#             "commitBranch" : commitBranch,
#             "commitMessage": commitMessage,
#             "commitAuthor": commitAuthor,
#             "fromBranch" : fromBranch,
#             "toBranch" : toBranch,
#             "timestamp": timestamp,
#             "eventType" : eventType,
#         }
        
#         # Post Push git action to DB
#         postInfoToMongo(infoModel)
        
#         return infoModel

#     except subprocess.CalledProcessError as e:
#         print("Exception on process, rc=", e.returncode, "output=", e.output)
#         return "Exception found (check logs) "
    
#     return "Nothing found"




# def print_git_changes(diff):
#     for change in diff.change_type:
#         chgs = list(diff.iter_change_type(change))
#         if len(chgs) == 0:
#             continue
#         print("change type",change)  
#         print("changes")
#         for chg in chgs:
#             print(chg.b_path)


# # push git action

# @webhook.route('/detect-push-event', methods=["GET"])
# def get_listen_for_changes_on_action_repo():
    
#     info = get_commit_info()
#     print("info : ")
#     print(info)
    
#     return info


# # detect PR
# @webhook.route('/detect-pull-request-event', methods=['GET','POST'])
# def detect_pull_requests():

#     commitId = LOCAL_ACTION_REPO.head.commit
#     print("commit id :: detect PR")
#     print(commitId)
    
    

#     owner = "ajayg51"
#     repo = "action-repo"
#     accessToken = "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"


#     headers = {
#         'Authorization': f'token {accessToken}',
#         'Accept': 'application/vnd.github.groot-preview+json'  # Required for retrieving pull requests
#     }
#     url = f'https://api.github.com/repos/{owner}/{repo}/commits/{commitId}/pulls'
    
#     try:
#         response = requests.get(url, headers=headers)
#         if response.status_code == 200:
#             pull_requests = response.json()
#             print("PULL REQUEST")
#             print(pull_requests)

#             latest_PR = pull_requests[-1]
#             commitBranch = latest_PR["head"]["label"]
#             commitMsg = latest_PR["title"]
#             author = latest_PR["user"]["login"]
#             timestamp = latest_PR["created_at"]
#             timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
#             timestamp = timestamp.strftime('%d %B %Y %I %M %S %p')


#             fromBranch = latest_PR["head"]["ref"]
#             toBranch = latest_PR["base"]["ref"]

#             print('author')
#             print(author)

#             print('timestamp')
#             print(timestamp)

#             print('from branch')
#             print(fromBranch)


#             print('to branch')
#             print(toBranch)
            

#             infoModel = {
#                 "commitBranch" : commitBranch,
#                 "commitAuthor" : author,
#                 "commitMessage" : commitMsg ,
#                 "fromBranch" : fromBranch,
#                 "toBranch" : toBranch,
#                 "eventType" : "PULL-REQUEST git action",
#                 "timestamp" : timestamp
#             }

#             # Post PR to DB
#             postInfoToMongo(infoModel)

#             return infoModel

#         else:
#             print(f"Failed to fetch pull request information. Status code: {response.status_code}")
#             return str(response.status_code)

#     except Exception as e:
#         print(f"Request Exception: {e}")
#         return "Exception : check logs "
#     return "No info found"


# @webhook.route('/detect-merge-event', methods=['GET', 'POST'])
# def get_merged_branch_info():
#     try:
#         # destinationDir = "./merged_pr/repo"
#         # if(os.path.exists(destinationDir)):
#         #     shutil.rmtree(destinationDir)

#         # remoteRepo = git.Repo.clone_from(REPO_URL, destinationDir, depth=1)
#         # headCommit = remoteRepo.head.commit
#         # print("head")
#         # print(headCommit)

        
#         LOCAL_REPO_LAST_HEAD_COMMIT_ID = LOCAL_ACTION_REPO.head.commit
#         LOCAL_REPO_LAST_HEAD_COMMIT_ID_HASH = LOCAL_ACTION_REPO.head.object.hexsha

        
#         commitAuthor = LOCAL_REPO_LAST_HEAD_COMMIT_ID.author.name
#         commitMessage = LOCAL_REPO_LAST_HEAD_COMMIT_ID.message
#         timestamp = LOCAL_REPO_LAST_HEAD_COMMIT_ID.authored_datetime

#         timestamp = datetime.datetime.strptime(str(timestamp), '%Y-%m-%d %H:%M:%S%z')
#         timestamp = timestamp.strftime('%d %B %Y %I %M %S %p')

#         commitBranch = "N/A"
#         fromBranch = "N/A as merge request"
#         toBranch = "N/A as merge request"
#         eventType = "MERGE git action"
        

#         if len(LOCAL_REPO_LAST_HEAD_COMMIT_ID.parents) > 1:
#                 print("Merged found")
#                 # commitAuthor = LOCAL_REPO_LAST_HEAD_COMMIT_ID.author.name
#                 # commitMessage = headCommit.message
#                 # timestamp = headCommit.authored_datetime
#         for ref in LOCAL_ACTION_REPO.references:
#             if isinstance(ref, git.Head): 
#                 branch_name = ref.name
#                 for b_commit in LOCAL_ACTION_REPO.iter_commits(branch_name):
#                     if b_commit == LOCAL_REPO_LAST_HEAD_COMMIT_ID:
#                         print("branch - name")
#                         print(branch_name)
#                         commitBranch = branch_name
                

#         print("local commit id")
#         print(LOCAL_REPO_LAST_HEAD_COMMIT_ID)
#         print("commitBranch")
#         print(commitBranch)
#         print("commitMessage")
#         print(commitMessage)

#         print("commitAuthor")
#         print(commitAuthor)
#         print("fromBranch")
#         print(fromBranch)
#         print("toBranch")
#         print(toBranch)
#         print("timestamp")
#         print(timestamp)
#         print("eventType")
#         print(eventType)
        
#         infoModel = {
#             "commitBranch" : commitBranch,
#             "commitMessage": commitMessage,
#             "commitAuthor": commitAuthor,
#             "fromBranch" : fromBranch,
#             "toBranch" : toBranch,
#             "timestamp": timestamp,
#             "eventType" : eventType,
#         }
        
#         # post Merge data to DB
#         postInfoToMongo(infoModel)

#         return infoModel
    
#     except git.exc.GitCommandError as e:
#         print(f"Git Command Error: {e}")
#         return "Exception found : check logs"
    
#     return "abcd"


# @webhook.route('/github', methods=['GET','POST'])
# def get_gh_api():
#     global info
#     print("request")
#     print(request)
#     print("headers")
#     print(request.headers)
#     print("content-type")
#     print(request.content_type)

#     if(request.method == 'POST'):
        
#         if(request.headers["Content-Type"]) == "application/json":
#             eventType = request.headers["X-Github-Event"]
#             print("Event type push/pull/merge")
#             print(eventType)
            
#             dumpData = json.dumps(request.json)
#             info = json.loads(dumpData)
#             info["eventType"] = eventType
#             print("model data  : run.py \n :: ")
#             print(info)
            # postInfoToMongo(info)

#             return "Success"
#     else:
#         print("get")
        
#         return info



# FETCHES DATA FROM MONGODB
@webhook.route('/get-data',methods=['GET'])
def get_data():
    print("cur timestamp :")
    print(datetime.datetime.now())
    data = get_atlas_data()
    print('data')
    print('')
    print(data)

    commitAuthor = data['commitAuthor']
    commitBranch = data['commitBranch']
    commitMessage = data['commitMessage']
    eventType = data['eventType']
    fromBranch = data['fromBranch']
    toBranch = data['toBranch']
    timestamp = data['timestamp']
    # timestamp =  datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S%z')
    # delhi_timezone = pytz.timezone('Asia/Kolkata')
    
    # timestamp = timestamp.replace(tzinfo=pytz.utc).astimezone(delhi_timezone)
    # timestamp = timestamp.strftime('%d %B %Y %I:%M:%S %p') 
    

    print('eventType')
    print(eventType)
    print('author')
    print(commitAuthor)
    print('fromBranch')
    print(fromBranch)
    print('toBranch')
    print(toBranch)
    print('timestamp')
    print(timestamp)
    print()


#     "commitAuthor": "Ajay Kumar Gond",
#   "commitBranch": "origin/main",
#   "commitMessage": "Merge pull request #4 from ajayg51/pr_check_branch\n\nM run.py at 4:48",
#   "eventType": "Merge",
#   "fromBranch": "N/A",
#   "timestamp": "Wed, 10 Apr 2024 11:19:56 GMT",
#   "toBranch": "N/A"
    datum = {
        "commitBranch":commitBranch,
        "commitMessage" : commitMessage,
        "commitAuthor":commitAuthor,
        "eventType":eventType,
        "fromBranch":fromBranch,
        "toBranch" : toBranch,
        "timestamp" : timestamp,
    }

    return datum
    
