from bs4 import BeautifulSoup

import requests
import datetime
import re
import time

import locale
locale.setlocale(locale.LC_TIME, "de_DE.utf-8")
from database_interface import *

headers = {

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
}

def time_stamp():
    return time.strftime("%Y-%m-%d")

def extract_case_num(text, prefix):
    cases_raw = text.split(prefix)[1]
    return int(re.findall("[0-9]+", cases_raw)[0])   

# Options: debug, cookies
def scrape(url, community_id, cases_func, date_func = None, name="", parent_community_id=None, options={}):
    req = requests.get(url,headers=headers, cookies=options.get('cookies'))
    bs = BeautifulSoup(req.text, "html.parser")
    if options.get('debug'):
        print(repr(bs.text))
    date = time_stamp() if date_func is None else date_func(bs)
    cases = cases_func(bs)
    if options.get('debug'):
        print(str(cases) + " Fälle am " + date)
    else:
        add_to_database(community_id, date, cases, name, parent_community_id)




