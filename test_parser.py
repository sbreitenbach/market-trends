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