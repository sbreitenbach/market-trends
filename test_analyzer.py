import analyzer
from collections import Counter

def test_count_tickers():
    a = ['GME','BB','GME','MSFT','BB','GME']
    b = analyzer.count_tickers(a)
    c = {'GME': 3, 'BB': 2, 'MSFT': 1}
    assert(b==c)

def test_most_common_tickers():
    a={'GME': 3, 'BB': 2, 'MSFT': 1}
    b = Counter(a)
    c=analyzer.most_common_tickers(b,2)
    d=[('GME',3),('BB',2)]

def test_has_positive_words_false():
    a='foo'
    b=analyzer.has_positive_words(a)
    assert(b==False)

def test_has_positive_words_true():
    a='rocket'
    b=analyzer.has_positive_words(a)
    assert(b==True)

def test_has_positive_words_true_with_emojis():
    a='🚀🚀🚀'
    b=analyzer.has_positive_words(a)
    assert(b==True)

def test_has_positive_words_true_with_uppercase():
    a="ROCKET"
    b=analyzer.has_positive_words(a)
    assert(b==True)

def test_has_negative_words_false():
    a='foo'
    b=analyzer.has_negative_words(a)
    assert(b==False)

def test_has_negative_words_true():
    a='put'
    b=analyzer.has_negative_words(a)
    assert(b==True)

def test_has_negative_words_false_with_emoji():
    a='🐻'
    b=analyzer.has_negative_words(a)
    assert(b==True)

def test_has_negative_words_true_with_capitals():
    a='SELL NOW'
    b=analyzer.has_negative_words(a)
    assert(b==True)

def test_preprocess_and_split_text():
    a = "HELLO WORLD 🚀"
    b = analyzer.preprocess_and_split_text(a)
    c = ['hello','world','rocket']
    assert(b==c)

def test_get_VADER_score_positive():
    a = "THIS STOCK IS THIS BEST IT IS GOING TO THE MOON!!! 🚀"
    b = analyzer.get_VADER_score(a)
    assert(b>0)

def test_get_VADER_score_negative():
    a = "this is not a good investment, i lost everything 😔"
    b = analyzer.get_VADER_score(a)
    assert(b<0)