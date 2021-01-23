import json
import logging
import praw

##Begin Config##
logging.basicConfig(filename='log.log',
                    filemode='a',
                    format='%(asctime)s %(levelname)s %(funcName)s %(lineno)d %(message)s',
                    datefmt="%Y-%m-%dT%H:%M:%S%z",
                    level=logging.DEBUG)
##End Config##

def returns_true():
    return True

if __name__ == '__main__':
    with open('secretConfig.json') as json_file:
        data=json.load(json_file)
        my_client_id=data["reddit"]["client_id"]
        my_client_secret=data["reddit"]["client_secret"]
        my_password=data["reddit"]["password"]
        my_username=data["reddit"]["username"]

    with open('publicConfig.json') as json_file:
        data=json.load(json_file)
        my_user_agent=data["reddit"]["user_agent"]
        my_subreddits=data["reddit"]["subreddits"]


    reddit = praw.Reddit(client_id=my_client_id, client_secret=my_client_secret,
                        password=my_password, user_agent=my_user_agent,
                        username=my_username)

    for subreddit in my_subreddits:
        for submission in reddit.subreddit(subreddit).hot(limit=20):
            print(subreddit,submission.title, submission.score, submission.upvote_ratio)