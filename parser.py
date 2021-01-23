import csv
import demoji
import logging
import re

exclude_list = []
with open('exclude_list.txt') as reader:
    for word in reader:
        word = word.replace("\n", "")
        exclude_list.append(word)

def preprocess_and_split_text(text):
    text_without_emojis = demoji.replace_with_desc(text,sep=" ")
    result = text_without_emojis.split()
    return result

def remove_non_uppercase_characters(text):
    result = re.sub('[^A-Z]+', '', text)
    return result

def is_dollar_sign_match(word):
    if(word.isupper() and word[0]=="$"):
        return True
    else: 
        return False

def is_full_symbol_match(word):
    if((1<= len(word) <=4) and word.isupper()):
        return True
    else:
        return False

def is_symbol_excluded(symbol):
    if(symbol in exclude_list):
        return True
    else:
        return False

def extract_tickers(text):
    matches=[]
    words = preprocess_and_split_text(text)
    for word in words:
        if((1<= len(word) <=5)):
            if(is_dollar_sign_match(word)):
                symbol = remove_non_uppercase_characters(word)
                if(is_symbol_excluded(symbol)):
                    logging.debug(f"Symbol {symbol} was on the exclude list")
                else:  
                    matches.append(symbol)
            elif (is_full_symbol_match(word)):
                symbol = remove_non_uppercase_characters(word)
                if(is_symbol_excluded(symbol)):
                    logging.debug(f"Symbol {symbol} was on the exclude list")
                else:
                    matches.append(symbol)
            else:
                logging.debug(f"No pattern match found for {word}")
    return matches