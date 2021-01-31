import analyzer
import json
import logging
import parser
import praw
from praw.models import MoreComments
from requests import RequestException

##Begin Config##
logging.basicConfig(filename='log.log',
                    filemode='a',
                    format='%(asctime)s %(levelname)s %(funcName)s %(lineno)d %(message)s',
                    datefmt="%Y-%m-%dT%H:%M:%S%z",
                    level=logging.INFO)
##End Config##


def get_reddit_data(subreddits,number_of_posts,number_of_comments):
    submissions = []
    reddit = praw.Reddit(client_id=my_client_id, client_secret=my_client_secret,
                        password=my_password, user_agent=my_user_agent,
                        username=my_username)
    try:
        for subreddit in subreddits:
            for submission in reddit.subreddit(subreddit).hot(limit=number_of_posts):
                submissions.append(submission.title)
                submissions.append(submission.selftext)
                submission.comments.replace_more(limit=number_of_comments)
                for comment in submission.comments.list():
                    if isinstance(comment, MoreComments):
                        continue
                    else:
                        submissions.append(comment.body)
    except RequestException:
        print("Network error")
        logging.warning("Network error")
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
        my_number_of_posts_to_crawl=data["reddit"]["number_of_posts_to_crawl"]
        my_number_of_comments_to_crawl=data["reddit"]["number_of_comments_to_crawl"]
        my_number_of_tickers_to_include=data["reddit"]["number_of_tickers_to_include"]

    print("Getting data from reddit...")
    logging.info("Getting data from reddit")
    #TODO clean up "posts" and "symbols" naming convention
    posts = get_reddit_data(my_subreddits,my_number_of_posts_to_crawl,my_number_of_comments_to_crawl)
    tickers = []
    post_list = []
    count_of_posts=len(posts)
    print(f"Processing data for {count_of_posts} posts...")
    for post in posts:
        extracted_tickers = parser.extract_tickers(post)
        for ticker in extracted_tickers:
            tickers.append(ticker)
            post_list.append([ticker,post])
    count_of_tickers = len(tickers)
    print(f"Found {count_of_tickers} tickers, starting analysis...")
    ticker_occurances = analyzer.count_tickers(tickers)
    most_common_tickers = analyzer.most_common_tickers(ticker_occurances,my_number_of_tickers_to_include)
    print(analyzer.calculate_net_sentiment(most_common_tickers,post_list))