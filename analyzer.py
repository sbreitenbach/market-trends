import demoji
from collections import Counter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def count_tickers(tickers):
    result = Counter(tickers)
    return result

def most_common_tickers(tickers,maximum):
    result = tickers.most_common(maximum)
    return result
    
def preprocess_and_split_text(text):
    wordlist = []
    text_without_emojis = demoji.replace_with_desc(text,sep=" ")
    words = text_without_emojis.split()
    for word in words:
        wordlist.append(word.lower())
    return wordlist

def has_positive_words(text):
    positive_words=['call','calls','bull','bulls''bullish','diamond','gem','hold','holding','liftoff','moon','rocket','yolo']
    words = preprocess_and_split_text(text)
    if(any(item in words for item in positive_words)):
        return True
    else:
        return False

def has_negative_words(text):
    negative_words=['bear','bears','bearish','imagine','put','puts','rainbow','sell','short']
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

a="THIS STOCK IS THE BEST 💎🙌 BABY!!!"
print (determine_sentiment(a))