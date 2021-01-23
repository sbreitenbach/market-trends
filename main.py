import analyzer
import json
import logging
import parser
import praw

##Begin Config##
logging.basicConfig(filename='log.log',
                    filemode='a',
                    format='%(asctime)s %(levelname)s %(funcName)s %(lineno)d %(message)s',
                    datefmt="%Y-%m-%dT%H:%M:%S%z",
                    level=logging.DEBUG)
##End Config##


def get_reddit_data(subreddits,number_of_posts):
    submissions = []
    reddit = praw.Reddit(client_id=my_client_id, client_secret=my_client_secret,
                        password=my_password, user_agent=my_user_agent,
                        username=my_username)
    for subreddit in subreddits:
        for submission in reddit.subreddit(subreddit).hot(limit=number_of_posts):
            submissions.append(submission.title)
    return submissions

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

    posts = get_reddit_data(my_subreddits,50)
    tickers = []
    for post in posts:
        extracted_tickers = parser.extract_tickers(post)
        for ticker in extracted_tickers:
            tickers.append(ticker)
    
    print(analyzer.count_tickers(tickers))