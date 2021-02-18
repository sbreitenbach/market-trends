import csv
import demoji
import json
import logging
import math
import re
import requests
from datetime import datetime

exclude_list = []


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


def load_exlude_list():
    with open('exclude_list.txt') as reader:
        for word in reader:
            word = word.replace("\n", "")
            exclude_list.append(word)


def format_company_name(text):
    result = ""
    remove_variations = ['co', 'corp', 'corporation', 'etf', 'fund',
                         'holdings', 'inc', 'incorporated', 'llc', 'ltd', 'trust', 'reit']
    stripped_text = re.sub('[^a-zA-Z ]+', '', text)
    words = stripped_text.split()
    for word in words:
        word = word.lower()
        if word not in remove_variations:
            result = result + word + " "
    result = result.rstrip()
    return result


valid_sybmol_list = []
company_name_and_symbol_list = []


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
                symbol = remove_non_uppercase_characters(row[1])
                valid_sybmol_list.append(symbol)

                if(run_company_match):
                    company_name = format_company_name(row[2])
                    if(company_name != ""):
                        company_name_and_symbol = [company_name, symbol]
                        company_name_and_symbol_list.append(
                            company_name_and_symbol)

    except requests.exceptions.RequestException as e:
        with open('cached_valid_tickers.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                symbol = remove_non_uppercase_characters(row[1])
                valid_sybmol_list.append(symbol)

                if(run_company_match):
                    company_name = format_company_name(row[2])
                    if(company_name != ""):
                        company_name_and_symbol = [company_name, symbol]
                        company_name_and_symbol_list.append(
                            company_name_and_symbol)


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


def is_image(url):
    image_types = ['.jpg', '.jpeg', '.png']
    for image_type in image_types:
        if url.endswith(image_type):
            return True
    return False


with open('publicConfig.json') as json_file:
    data = json.load(json_file)
    run_company_match = data["settings"]["run_company_match"]
    run_image_ocr = data["settings"]["run_image_ocr"]

load_exlude_list()
load_known_companies()

if(run_company_match):
    import spacy
    nlp = spacy.load("en_core_web_sm")

    def match_company_name_to_ticker(text):
        matches = []

        doc = nlp(text)

        for ent in doc.ents:
            if (ent.label_ == "ORG"):
                possible_company = ent.text
                logging.debug(f"Found company {possible_company}")
                possible_company = format_company_name(possible_company)
                if(possible_company != ""):
                    for company in company_name_and_symbol_list:
                        company_name = company[0]
                        symbol = remove_non_uppercase_characters(company[1])
                        if(possible_company == company_name):
                            if not (is_symbol_excluded(symbol)):
                                logging.debug(
                                    f"matched {possible_company} full name {ent.text} with {company_name}")
                                matches.append(symbol)

        return matches

if(run_image_ocr):
    import io
    from PIL import Image
    import pytesseract

    def extract_text_from_image(url):
        result = ""
        try:
            response = requests.get(url)
            img = Image.open(io.BytesIO(response.content))
            result = pytesseract.image_to_string(img)
        except requests.exceptions.RequestException as e:
            logging.warning(f"Encountered network exception {e}")
        return result
