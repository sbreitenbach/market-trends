import analyzer

def test_count_tickers():
    a = ['GME','BB','GME','MSFT','BB','GME']
    b = analyzer.count_tickers(a)
    c = {'GME': 3, 'BB': 2, 'MSFT': 1}
    assert(b==c)