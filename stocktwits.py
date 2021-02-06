import json
import logging
import requests
from requests import RequestException

with open('secretConfig.json') as json_file:
    data = json.load(json_file)
    token = data["stocktwits"]["token"]


def get_trending_stocks():
    result = []
    try:
        url = f"https://api.stocktwits.com/api/2/trending/symbols.json?access_token={token}"
        response = requests.request("GET", url)
        if (response.ok):
            response_json = json.loads(response.text)
            for sybmbol in response_json['symbols']:
                extracted_sybmbol = sybmbol['symbol']
                result.append(extracted_sybmbol)
            return result
        else:
            return result
    except RequestException:
        print("Network error")
        logging.warning("Network error")
        return result