import demoji
import parser

demoji.download_codes()


def test_is_valid_dollar_sign_match():
    a = "$GME"
    b = parser.is_dollar_sign_match(a)
    assert(b == True)


def test_not_valid_dollar_sign_match():
    a = "GME"
    b = parser.is_dollar_sign_match(a)
    assert(b == False)


def test_not_valid_dollar_sign_match_with_call_abbreviation():
    a = "$65C"
    b = parser.is_dollar_sign_match(a)
    assert(b == False)


def test_not_valid_dollar_sign_match_with_put_abbreviation():
    a = "$50P"
    b = parser.is_dollar_sign_match(a)
    assert(b == False)


def test_preprocess_and_split_text_with_emojis():
    a = "bottle 🚀"
    b = parser.preprocess_and_split_text(a)
    assert(b == ['bottle', 'rocket'])


def test_remove_non_uppercase_characters_with_multiple_symbols():
    a = "$GME?"
    b = parser.remove_non_uppercase_characters(a)
    assert(b == "GME")


def test_remove_non_uppercase_characters_with_symbols():
    a = "$GME"
    b = parser.remove_non_uppercase_characters(a)
    assert(b == "GME")


def test_remove_non_uppercase_characters_with_commas():
    a = "GME,"
    b = parser.remove_non_uppercase_characters(a)
    assert(b == "GME")


def test_remove_non_uppercase_characters_with_numbers():
    a = "GME123"
    b = parser.remove_non_uppercase_characters(a)
    assert(b == "GME")


def test_remove_non_uppercase_characters_with_spaces():
    a = " GME "
    b = parser.remove_non_uppercase_characters(a)
    assert(b == "GME")


def test_remove_non_uppercase_or_dollar_characters_with_question_mark():
    a = "$CLOV?"
    b = parser.remove_non_uppercase_or_dollar_characters(a)
    # print(b)
    assert(b == "$CLOV")


def test_remove_non_uppercase_or_dollar_characters_with_parentheses():
    a = "($CLOV)"
    b = parser.remove_non_uppercase_or_dollar_characters(a)
    assert(b == "$CLOV")


def test_remove_non_uppercase_or_dollar_characters_with_apostrophe():
    a = "AFRM's"
    b = parser.remove_non_uppercase_or_dollar_characters(a)
    assert(b == "AFRM")


def test_is_full_symbol_match():
    a = "GME"
    b = parser.is_full_symbol_match(a)
    assert(b == True)


def test_is_not_full_symbol_match_with_5_chars():
    a = "$PLTR"
    b = parser.is_full_symbol_match(a)
    assert(b == False)


def test_is_not_full_symbol_match_with_lowercase():
    a = "gme"
    b = parser.is_full_symbol_match(a)
    assert(b == False)


def test_is_symbol_excluded():
    a = "ATH"
    b = parser.is_symbol_excluded(a)
    assert(b == True)


def test_is_symbol_not_excluded():
    a = "GME"
    b = parser.is_symbol_excluded(a)
    assert(b == False)


def test_single_extract_tickers():
    a = "buy GME"
    b = parser.extract_tickers(a)
    assert(b == ['GME'])


def test_mutliple_extract_tickers():
    a = "buy GME and PLTR"
    b = parser.extract_tickers(a)
    assert(b == ['GME', 'PLTR'])


def test_extract_tickers_with_excludsions():
    a = "Complete PLTR DD ahead of Demo Day (Valuation Included)"
    b = parser.extract_tickers(a)
    assert(b == ['PLTR'])


def test_extract_tickers_no_matchs():
    a = "ETF Data center REIT surefire or am I wrong?"
    b = parser.extract_tickers(a)
    assert(b == [])


def test_extract_tickers_with_parentheses():
    a = "Clover Health ($CLOV) will moon soon"
    b = parser.extract_tickers(a)
    assert(b == ['CLOV'])


def test_extract_tickers_with_question():
    a = "Thoughts on $CLOV?"
    b = parser.extract_tickers(a)
    assert(b == ['CLOV'])


def test_extract_tickers_with_multiple_matches_and_parentheses():
    a = "Defense Stocks (LMT, RTX, NOC, GD, BA) should I invest in them OR GME?"
    b = parser.extract_tickers(a)
    assert(b == ['LMT', 'RTX', 'NOC', 'GD', 'BA', 'GME'])


def test_format_company_name():
    a = "Foo & Bar Inc."
    b = parser.format_company_name(a)
    assert(b == "foo bar")


def test_match_company_name_to_ticker():
    a = "Apple plans to build a self driving car in 2025"
    b = parser.match_company_name_to_ticker(a)
    assert(b == ['AAPL'])


def test_is_image_true():
    a = "foo.bar/image.png"
    b = parser.is_image(a)
    assert(b == True)


def test_is_image_false():
    a = "foo.bar/home"
    b = parser.is_image(a)
    assert(b == False)
