import csv
import demoji
import logging
import math
import re
import requests
from datetime import datetime

exclude_list = []


def load_exlude_list():
    with open('exclude_list.txt') as reader:
        for word in reader:
            word = word.replace("\n", "")
            exclude_list.append(word)


def format_company_name(text):
    result = ""
    remove_variations = ['co','corp','corporation','etf','fund','holdings','inc','incorporated','llc','ltd','trust','reit']
    stripped_text = re.sub('[^a-zA-Z ]+', '', text)
    words = stripped_text.split()
    for word in words:
        word = word.lower()
        if word in remove_variations:
            pass
        else:
            result = result + word + " "
    result = result.rstrip()
    return result

valid_sybmol_list = []
company_list = []

def load_known_companies():
    todays_date = datetime.today().strftime('%Y-%m-%d')
    url = f"https://api.stocktwits.com/symbol-sync/{todays_date}.csv"
    try:
        with requests.Session() as s:
            download = s.get(url)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
            for row in my_list:
                valid_sybmol_list.append(row[1])
                company_list.append(format_company_name(row(2)),row[1])

    except requests.exceptions.RequestException as e:
        with open('cached_valid_tickers.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                valid_sybmol_list.append(row[1])


def preprocess_and_split_text(text):
    text_without_emojis = demoji.replace_with_desc(text, sep=" ")
    result = text_without_emojis.split()
    return result


def remove_non_uppercase_characters(text):
    result = re.sub('[^A-Z]+', '', text)
    return result


def remove_non_uppercase_or_dollar_characters(text):
    result = re.sub('[^A-Z$]+', '', text)
    return result


def is_dollar_sign_match(word):
    if(word.isupper() and word[0] == "$"):
        word_len = len(word)
        i = 1
        while i < word_len:
            char = word[i]
            if not (str.isalpha(char)):
                return False
            i += 1
        return True
    else:
        return False


def is_full_symbol_match(word):
    if((1 <= len(word) <= 4) and word.isupper()):
        return True
    else:
        return False


def is_symbol_excluded(symbol):
    if(symbol in exclude_list):
        return True
    else:
        return False

# There is an overlap of stock tickers to common words and terms (e.g. YOLO is a valid ticker)
# This is results in a large number of false positives being picked up by this parser, and it may filter out some valid tickers


def extract_tickers(text):
    matches = []
    words = preprocess_and_split_text(text)
    for word in words:
        if(word.isupper()):
            stripped_word = remove_non_uppercase_or_dollar_characters(word)
            if(1 <= len(stripped_word) <= 5):
                if(is_dollar_sign_match(stripped_word)):
                    symbol = remove_non_uppercase_characters(stripped_word)
                    if(is_symbol_excluded(symbol)):
                        logging.debug(
                            f"Symbol {symbol} was on the exclude list")
                    elif(symbol in valid_sybmol_list):
                        matches.append(symbol)
                    else:
                        logging.debug(
                            f"Symbol {symbol} was not found on the list of valid tickers")
                elif (is_full_symbol_match(stripped_word)):
                    symbol = remove_non_uppercase_characters(stripped_word)
                    if(is_symbol_excluded(symbol)):
                        logging.debug(
                            f"Symbol {symbol} was on the exclude list")
                    elif(symbol in valid_sybmol_list):
                        matches.append(symbol)
                    else:
                        logging.debug(
                            f"Symbol {symbol} was not found on the list of valid tickers")
                else:
                    logging.debug(
                        f"No pattern match found for {stripped_word}")
        else:
            logging.debug(f"No pattern match found for {word}")

    return matches


load_exlude_list()
load_known_companies()