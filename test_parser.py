import parser

def test_is_valid_dollar_sign_match():
    a="$GME"
    b = parser.is_dollar_sign_match(a)
    assert(b==True)

def test_not_valid_dollar_sign_match():
    a="GME"
    b = parser.is_dollar_sign_match(a)
    assert(b==False)

def test_preprocess_and_split_text_with_emojis():
    a="bottle 🚀"
    b = parser.preprocess_and_split_text(a)
    assert(b==['bottle','rocket'])

def test_remove_non_uppercase_characters_with_multiple_symbols():
    a="$GME?"
    b = parser.remove_non_uppercase_characters(a)
    assert(b=="GME")

def test_remove_non_uppercase_characters_with_symbols():
    a="$GME"
    b = parser.remove_non_uppercase_characters(a)
    assert(b=="GME")

def test_remove_non_uppercase_characters_with_commas():
    a="GME,"
    b = parser.remove_non_uppercase_characters(a)
    assert(b=="GME")

def test_remove_non_uppercase_characters_with_numbers():
    a="GME123"
    b = parser.remove_non_uppercase_characters(a)
    assert(b=="GME")

def test_remove_non_uppercase_characters_with_spaces():
    a=" GME "
    b = parser.remove_non_uppercase_characters(a)
    assert(b=="GME")

def test_is_full_symbol_match():
    a="GME"
    b = parser.is_full_symbol_match(a)
    assert(b==True)

def test_is_not_full_symbol_match_with_5_chars():
    a="$PLTR"
    b = parser.is_full_symbol_match(a)
    assert(b==False)

def test_is_not_full_symbol_match_with_lowercase():
    a="gme"
    b = parser.is_full_symbol_match(a)
    assert(b==False)

def test_is_symbol_excluded():
    a="ATH"
    b = parser.is_symbol_excluded(a)
    assert(b==True)

def test_is_symbol_not_excluded():
    a="GME"
    b = parser.is_symbol_excluded(a)
    assert(b==False)

def test_single_extract_tickers():
    a="buy GME"
    b = parser.extract_tickers(a)
    assert(b==['GME'])

def test_mutliple_extract_tickers():
    a="buy GME and PLTR"
    b = parser.extract_tickers(a)
    assert(b==['GME','PLTR'])

def test_extract_tickers_with_excludsions():
    a="Complete PLTR DD ahead of Demo Day (Valuation Included)"
    b = parser.extract_tickers(a)
    assert(b==['PLTR'])

def test_extract_tickers_no_matchs():
    a="ETF Data center REIT surefire or am I wrong?"
    b = parser.extract_tickers(a)
    assert(b==[])


#TODO failed cases
"""
3K - 13K in 4 months. All stocks, no options. Can you tell when I stopped trading like a boomer? ['K', 'K']
Is it really this easy to get on the train? (GME) []
Thoughts on $CLOV? []
Clover Health ($CLOV) will moon soon []
Doing research on AFRM's S-1... what do you think about the stock []
Defense Stocks (LMT, RTX, NOC, GD, BA) ['RTX', 'NOC', 'GD', 'BA']
Is it too late to invest in GME, BB, PLTR, and AMC? I have been seeing a lot of hype around these stocks but am afraid I do not understand. ['GME', 'BB', 'AMC']
"""