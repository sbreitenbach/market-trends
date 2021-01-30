from collections import Counter

def count_tickers(tickers):
    result = Counter(tickers)
    return result

def most_common_tickers(tickers,maximum):
    result = tickers.most_common(maximum)
    return result