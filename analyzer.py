import parser
from collections import Counter

def count_tickers(tickers):
    result = Counter(tickers)
    return result

def most_common_tickers(tickers,maximum):
    result = tickers.most_common(maximum)
    return result

def has_positive_words(text):
    positive_words=['call','calls','bull','bulls''bullish','moon','diamond','liftoff','yolo','rocket','hold','holding']
    words = parser.preprocess_and_split_text(text)
    if(any(item in words for item in positive_words)):
        return True
    else:
        return False

def has_negative_words(text):
    negative_words=['bear','bears','bearish','put','puts','rainbow','short','sell']
    words = parser.preprocess_and_split_text(text)
    if(any(item in words for item in negative_words)):
        return True
    else:
        return False

def determine_sentiment(text):
    return