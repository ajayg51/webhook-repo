from flask import Flask
# import subprocess
import git

app = Flask(__name__)

REPO_URL = "https://github.com/ajayg51/action-repo"
REPO_LOCAL_PATH = "/Volumes/ajaySafeBox/0_projects/dev/0_self/3_python/action-repo"

repo = git.Repo(REPO_LOCAL_PATH)
LOCAL_REPO_LAST_HEAD_COMMIT_ID = repo.head.commit
LOCAL_REPO_LAST_HEAD_COMMIT_ID_HASH = repo.head.object.hexsha


def print_git_changes(diffChanges):
    for change in diffChanges:
        chgs = list(diff.iter_change_type(change))
        if len(chgs) == 0:
            continue
        print("change type",change)  
        print("changes")
        for chg in chgs:
            print(chg.b_path)


@app.route("/", methods=["GET"])
def get_listen_for_changes_on_action_repo():
    
    print("repo")
    print(repo)
    print("local - head")
    print(LOCAL_REPO_LAST_HEAD_COMMIT_ID_HASH)

    remoteRepo = repo.remotes.origin

    remoteRepo.fetch()

    REPO_REMOTE_HEAD_COMMIT_ID_HASH = remoteRepo.refs["main"].object.hexsha
    
    print("remote - head")
    print(REPO_REMOTE_HEAD_COMMIT_ID_HASH)
    
    if LOCAL_REPO_LAST_HEAD_COMMIT_ID_HASH != REPO_REMOTE_HEAD_COMMIT_ID_HASH:
        diff = LOCAL_REPO_LAST_HEAD_COMMIT_ID.diff(REPO_REMOTE_HEAD_COMMIT_ID_HASH)
        print("diff")
        print(diff)
        print_git_changes(diff.change_type)

        msg = "Remote action-repo changed"
        print(msg)
        return msg
    
    return "No git action detected"

if __name__ == "__main__":
    app.run(host="localhost",port=4000,debug=False)

