from flask import Blueprint, json, request, render_template
import sched, time, datetime, git, subprocess, requests, os, shutil


from app.extensions import *


info = 'data from api'

webhook = Blueprint('Webhook', __name__)



REPO_URL = "https://github.com/ajayg51/action-repo.git"
LOCAL_REPO_PATH = "/Volumes/ajaySafeBox/0_projects/dev/0_self/3_python/action-repo"

LOCAL_ACTION_REPO = git.Repo(LOCAL_REPO_PATH)
LOCAL_REPO_LAST_HEAD_COMMIT_ID = LOCAL_ACTION_REPO.head.commit
LOCAL_REPO_LAST_HEAD_COMMIT_ID_HASH = LOCAL_ACTION_REPO.head.object.hexsha



# will do later

# @webhook.errorhandler(404)
# def get_error_page(error):
#     print("here")
#     return "404 page not found"

@webhook.route('/', methods=["GET"])
def get_root():
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

def get_commit_info(commit_id):
  
    try:
        commit = LOCAL_ACTION_REPO.commit(commit_id) 
        commitAuthor = commit.author.name
        commitMessage = commit.message
        timestamp = commit.authored_datetime
        commitBranch = "N/A"
        fromBranch = "N/A"
        toBranch = "N/A"
        
        



        for ref in LOCAL_ACTION_REPO.references:
            if isinstance(ref, git.Head): 
                branch_name = ref.name
                for b_commit in LOCAL_ACTION_REPO.iter_commits(branch_name):
                    if b_commit == commit:
                        print("branch - name")
                        print(branch_name)
                        commitBranch = branch_name

        eventType = ""
        if len(commit.parents) > 1 :
            eventType = "Merge"
            print("Merge request found")
        

        print("local - repo")
        print(LOCAL_ACTION_REPO)
        print("local - head")
        print(LOCAL_REPO_LAST_HEAD_COMMIT_ID_HASH)

        remoteRepo = LOCAL_ACTION_REPO.remotes.origin
        remoteRepo.fetch()
        REMOTE_REPO_HEAD_COMMIT_ID_HASH = remoteRepo.refs["main"].object.hexsha
        print("remote - head")
        print(REMOTE_REPO_HEAD_COMMIT_ID_HASH)
        if LOCAL_REPO_LAST_HEAD_COMMIT_ID_HASH != REMOTE_REPO_HEAD_COMMIT_ID_HASH :
            eventType = "Push"
            print("Push git action found")

        print("commit")
        print(commit)
        print("author")
        print(commitAuthor)
        print("commit-msg")
        print(commitMessage)
        print("commitBranch")
        print(commitBranch)

        infoModel = {
            "commitBranch" : commitBranch,
            "commitMessage": commitMessage,
            "commitAuthor": commitAuthor,
            "fromBranch" : fromBranch,
            "toBranch" : toBranch,
            "timestamp": timestamp,
            "eventType" : eventType,
        }
        postInfoToMongo(infoModel)
        
        return infoModel

    except subprocess.CalledProcessError as e:
        print("Exception on process, rc=", e.returncode, "output=", e.output)
        return "Exception found (check logs) "
    
    return "Nothing found"




def print_git_changes(diff):
    for change in diff.change_type:
        chgs = list(diff.iter_change_type(change))
        if len(chgs) == 0:
            continue
        print("change type",change)  
        print("changes")
        for chg in chgs:
            print(chg.b_path)


# LISTENS TO ACTION PERFORMED ON REMOTE REPO : ACTION-REPO

@webhook.route('/action-repo-changes-listener', methods=["GET"])
def get_listen_for_changes_on_action_repo():
    
    print("local - repo")
    print(LOCAL_ACTION_REPO)
    print("local - head")
    print(LOCAL_REPO_LAST_HEAD_COMMIT_ID_HASH)

    remoteRepo = LOCAL_ACTION_REPO.remotes.origin
    remoteRepo.fetch()
    REMOTE_REPO_HEAD_COMMIT_ID_HASH = remoteRepo.refs["main"].object.hexsha
    print("remote - head")
    print(REMOTE_REPO_HEAD_COMMIT_ID_HASH)
    
    # REPO_REMOTE_HEAD_COMMIT_ID = remoteRepo.refs["main"].object.hexsha
    info = get_commit_info(REMOTE_REPO_HEAD_COMMIT_ID_HASH)
    print("info : ")
    print(info)

    
    diff = LOCAL_REPO_LAST_HEAD_COMMIT_ID.diff(REMOTE_REPO_HEAD_COMMIT_ID_HASH)
    print("diff")
    print(diff)
    print_git_changes(diff)

    if LOCAL_REPO_LAST_HEAD_COMMIT_ID_HASH != REMOTE_REPO_HEAD_COMMIT_ID_HASH:
        msg = "Remote action-repo changed : PUSH"
        print(msg)
    
    return info


@webhook.route('/detect-pull-request', methods=['GET','POST'])
def detect_pull_requests():
    
    

    # commitId of branch which has raised PR
    commitId = "4136091bce3b20d9c70bef47e05c5f7ae30016cf"

    owner = "ajayg51"
    repo = "action-repo"
    accessToken = "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"


    headers = {
        'Authorization': f'token {accessToken}',
        'Accept': 'application/vnd.github.groot-preview+json'  # Required for retrieving pull requests
    }
    url = f'https://api.github.com/repos/{owner}/{repo}/commits/{commitId}/pulls'
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            pull_requests = response.json()
            print("PULL REQUEST")
            print(pull_requests)

            latest_PR = pull_requests[0]
            commitBranch = latest_PR["head"]["label"]
            commitMsg = latest_PR["title"]
            author = latest_PR["user"]["login"]
            timestamp = latest_PR["created_at"]
            fromBranch = latest_PR["head"]["ref"]
            toBranch = latest_PR["base"]["ref"]

            print('author')
            print(author)

            print('timestamp')
            print(timestamp)

            print('from branch')
            print(fromBranch)


            print('to branch')
            print(toBranch)
            

            infoModel = {
                "commitBranch" : commitBranch,
                "commitAuthor" : author,
                "commitMessage" : commitMsg ,
                "fromBranch" : fromBranch,
                "toBranch" : toBranch,
                "eventType" : "PULL-REQUEST",
                "timestamp" : timestamp
            }

            postInfoToMongo(infoModel)

            return infoModel

        else:
            print(f"Failed to fetch pull request information. Status code: {response.status_code}")
            return str(response.status_code)

    except Exception as e:
        print(f"Request Exception: {e}")
        return "Exception : "
    return "No info found"


@webhook.route('/get-merged-branch-info', methods=['GET', 'POST'])
def get_merged_branch_info():
    try:
        destinationDir = "./clone/repo"
        if(os.path.exists(destinationDir)):
            shutil.rmtree(destinationDir)

        remoteRepo = git.Repo.clone_from(REPO_URL, destinationDir, depth=1)
        headCommit = remoteRepo.head.commit
        print("head")
        print(headCommit)

        merged_commits_info = []
        
        if len(headCommit.parents) > 1:
                merged_commit_info = {
                    'commit_hash': headCommit.hexsha,
                    'author': headCommit.author.name,
                    'author_email': headCommit.author.email,
                    'commit_date': headCommit.committed_datetime,
                    'message': headCommit.message,
                }
                merged_commits_info.append(merged_commit_info)
        print("Merged commits info")
        print(merged_commits_info)

        return merged_commits_info
    
    except git.exc.GitCommandError as e:
        print(f"Git Command Error: {e}")
        return "Exception found : check logs"
    
    return "abcd"


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
    
