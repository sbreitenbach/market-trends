#ignore ETF, ROTH, IRA, COVID, SEC, REIT, EOW
import csv
import demoji
import re

matches=[]

def preprocess_and_split_text(text):
    text_without_emojis = demoji.replace_with_desc(text,sep=" ")
    result = text_without_emojis.split()
    return result

def remove_non_uppercase_characters(text):
    result = re.sub('[^A-Z]+', '', text)
    return result

def is_dollar_sign_match(word):
    if(word.isupper() and word[0]=="$"):
        #print(word)
        return True
    else: 
        return False

def is_full_symbol_match(word):
    if((1<= len(word) <=4) and word.isupper()):
        return True
    else:
        return False

with open('sample_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            words = preprocess_and_split_text(row["title"])
            for word in words:
                if((1<= len(word) <=5)):
                    if(is_dollar_sign_match(word)):
                        symbol = remove_non_uppercase_characters(word)
                        matches.append(symbol)
                    elif (is_full_symbol_match(word)):
                        symbol = remove_non_uppercase_characters(word)
                        matches.append(symbol)
                    #print(word)
                #print(row["title"],word,row["symbol"])


print(matches)