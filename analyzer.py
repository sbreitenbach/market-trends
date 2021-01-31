import demoji
from collections import Counter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def count_tickers(tickers):
    result = Counter(tickers)
    return result


def most_common_tickers(tickers, maximum=10):
    result = tickers.most_common(maximum)
    return result


def preprocess_and_split_text(text):
    wordlist = []
    text_without_emojis = demoji.replace_with_desc(text, sep=" ")
    words = text_without_emojis.split()
    for word in words:
        wordlist.append(word.lower())
    return wordlist


def has_positive_words(text):
    positive_words = ['call', 'calls', 'bull', 'bulls''bullish', 'diamond',
                      'gem', 'hold', 'holding', 'liftoff', 'moon', 'rocket', 'yolo']
    words = preprocess_and_split_text(text)
    if(any(item in words for item in positive_words)):
        return True
    else:
        return False


def has_negative_words(text):
    negative_words = ['bear', 'bears', 'bearish', 'imagine',
                      'put', 'puts', 'rainbow', 'sell', 'short']
    words = preprocess_and_split_text(text)
    if(any(item in words for item in negative_words)):
        return True
    else:
        return False


def get_VADER_score(text):
    VADER_analyzer = SentimentIntensityAnalyzer()
    vs = VADER_analyzer.polarity_scores(text)
    compound_score = vs['compound']
    return compound_score

# This may not be accurate and could easily be manipliated
# VADER is trained used social media data and the custom scoring for certain words may help
# Best way to approach this would likely be a custom trained model for each data source


def determine_sentiment(text):
    VADER_score = get_VADER_score(text)
    if(has_negative_words(text) and has_positive_words(text)):
        return VADER_score
    elif(has_positive_words(text)):
        adjusted_score = VADER_score + .02
        return adjusted_score
    elif(has_negative_words(text)):
        adjusted_score = VADER_score - .02
        return adjusted_score
    else:
        return VADER_score


def calculate_net_sentiment(most_common_tickers, post_list):
    result = []
    for i in most_common_tickers:
        common_ticker = i[0]
        occurances = i[1]
        sentiment_sum = 0
        average_sentiment = 0
        for post in post_list:
            post_ticker = post[0]
            post_text = post[1]
            if post_ticker == common_ticker:
                post_sentiment = determine_sentiment(post_text)
                sentiment_sum = sentiment_sum + post_sentiment
        # This could count the same ticker again if it's mentioned multiple times in a post
        # E.g. $GME $GME $GME to the moon!!! would be triple counted...
        # Could possiby use some kind of post id to prevent this
        average_sentiment = round((sentiment_sum/occurances), 4)
        scores = {common_ticker: {'mentions': occurances,
                                  'sentiment': average_sentiment}}
        result.append(scores)
    return result
