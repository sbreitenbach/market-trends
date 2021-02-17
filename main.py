import analyzer
import json
import logging
import multiprocessing
import parser
import praw
from praw.models import MoreComments
from prawcore.exceptions import RequestException, ServerError

##Begin Config##
logging.basicConfig(filename='log.log',
                    filemode='a',
                    format='%(asctime)s %(levelname)s %(funcName)s %(lineno)d %(message)s',
                    datefmt="%Y-%m-%dT%H:%M:%S%z",
                    level=logging.INFO)
##End Config##


def get_reddit_data(subreddits, number_of_posts, number_of_comments):
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
    except (RequestException, ServerError) as e:
        print(f"Network error {e}")
        logging.error(f"Network error")
    return submissions


class Ticker_Worker(multiprocessing.Process):

    def __init__(self, task_queue, ticker_result_queue, posts_result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.ticker_result_queue = ticker_result_queue
        self.posts_result_queue = posts_result_queue

    def run(self):
        proc_name = self.name
        logging.debug(f"Starting {proc_name}")
        while True:
            post = self.task_queue.get()
            if post is None:
                logging.debug('%s: Exiting' % proc_name)
                self.task_queue.task_done()
                break
            extracted_tickers = parser.extract_tickers(post)
            for ticker in extracted_tickers:
                self.ticker_result_queue.put(ticker)
                ticker_post = [ticker, post]
                self.posts_result_queue.put(ticker_post)
            if(run_company_match):
                company_name_matches = parser.match_company_name_to_ticker(
                    post)
                for ticker in company_name_matches:
                    self.ticker_result_queue.put(ticker)
                    ticker_post = [ticker, post]
                    self.posts_result_queue.put(ticker_post)
            self.task_queue.task_done()
        return


if __name__ == '__main__':
    with open('secretConfig.json') as json_file:
        data = json.load(json_file)
        my_client_id = data["reddit"]["client_id"]
        my_client_secret = data["reddit"]["client_secret"]
        my_password = data["reddit"]["password"]
        my_username = data["reddit"]["username"]

    with open('publicConfig.json') as json_file:
        data = json.load(json_file)
        my_user_agent = data["reddit"]["user_agent"]
        my_subreddits = data["reddit"]["subreddits"]
        my_number_of_posts_to_crawl = data["reddit"]["number_of_posts_to_crawl"]
        my_number_of_comments_to_crawl = data["reddit"]["number_of_comments_to_crawl"]
        my_number_of_tickers_to_include = data["reddit"]["number_of_tickers_to_include"]
        run_company_match = data["settings"]["run_company_match"]

    print("Getting data from reddit...")
    logging.info("Getting data from reddit")
    # TODO clean up "posts" and "symbols" naming convention
    posts = get_reddit_data(
        my_subreddits, my_number_of_posts_to_crawl, my_number_of_comments_to_crawl)
    tickers = []
    post_list = []
    count_of_posts = len(posts)
    print(f"Processing data for {count_of_posts} posts...")
    logging.info(f"Processing data for {count_of_posts} posts...")

    tasks = multiprocessing.JoinableQueue()
    ticker_results = multiprocessing.Queue()
    posts_results = multiprocessing.Queue()

    num_workers = multiprocessing.cpu_count() - 1
    if (num_workers<1):
         num_workers = 1
    print('Creating %d workers' % num_workers)
    consumers = [Ticker_Worker(tasks, ticker_results, posts_results)
                 for i in range(num_workers)]
    for w in consumers:
        w.start()

    for post in posts:
        tasks.put(post)

    for i in range(num_workers):
        tasks.put(None)

    tasks.join()

    print("Collecting tickers from results")
    while not ticker_results.empty():
        ticker = ticker_results.get()
        tickers.append(ticker)

    while not posts_results.empty():
        ticker_post = posts_results.get()
        post_list.append(ticker_post)

    count_of_tickers = len(tickers)
    print(f"Found {count_of_tickers} tickers, starting analysis...")
    logging.info(f"Found {count_of_tickers} tickers, starting analysis...")
    ticker_occurances = analyzer.count_tickers(tickers)
    most_common_tickers = analyzer.most_common_tickers(
        ticker_occurances, my_number_of_tickers_to_include)
    
    post_list = analyzer.trim_post_list(most_common_tickers, post_list)
    print(analyzer.calculate_net_sentiment(most_common_tickers, post_list))
    logging.info(analyzer.calculate_net_sentiment(
        most_common_tickers, post_list))
