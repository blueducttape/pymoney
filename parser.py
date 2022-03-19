import json
import requests
import re


URL_API = "https://www.cbr-xml-daily.ru/daily_json.js"


def get_data(url):
    try:
        full_page = requests.get(url).json()  # получен json файл и приведен к словарю
        with open("rates", 'w') as f:
            json.dump(full_page, fp=f, sort_keys=True, indent=4)  # данные с сайта ЦБ в формате json в файл
    except OSError:
        with open("rates", "r") as f:
            full_page = json.load(f)
    return full_page


data = get_data(URL_API)
date = data["Date"]

pattern = re.search(r"(?P<Year>\d{4})-(?P<Month>\d{2})-(?P<Day>\d{2})T(?P<Time>.{8})(?P<GMT>.{6})", date)
result_date = pattern.groupdict()

day = result_date["Day"]
month = result_date["Month"]
year = result_date["Year"]
time = result_date["Time"]
GMT = result_date["GMT"]

