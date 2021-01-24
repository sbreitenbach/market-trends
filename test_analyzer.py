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