#!/usr/bin/env python
'''
author: Greg Mangan
description: Script to grab the 'Top 10 by year' wikipedia page
    (http://en.wikipedia.org/wiki/List_of_Billboard_Hot_100_top-ten_singles)
'''
import sys
import json
from pathlib import Path

import click
import pymongo
from bs4 import BeautifulSoup

sys.path.append(Path(__file__).resolve().parents[1])
from tools import extract_tools as etools
from tools import common_tools as ctools
from tools import db_tools as dbtools
from tools import paths

def get_wiki_page(url, page_type=None):

    Mongo = dbtools.MongoConnect()
    Mongo.connect()
    db = Mongo.connection['landing']

    page_response = etools.fetch_webpage(url)
    if not page_response['_ok']:
        raise ValueError('Unable to get page')

    else:
        print('Grabbed by year page successfully, inserting into db...')

        db_resp = db.wiki_html.update_one(
            filter = {'page_id': page_response['page_id']},
            update = {
                '$set': {'page_type':page_type, **page_response},
                '$inc': {'_version':1},
                '$currentDate':{'_updated':{'$type':'date'}}
            },
            upsert=True
        )
        parsed_db_resp =  dbtools.parse_mongo_result(db_resp)
        return parsed_db_resp


def get_year_links():
    # Get the list of "Top 10 Singles by Year" page from the "List of Billboard Hot 100" page_id
    Mongo = dbtools.MongoConnect()
    Mongo.connect()
    db = Mongo.connection['landing']

    res = db.wiki_html.find_one({'page_type':'billboard100_by_year'})
    if not res:
        # If page not there, get it
        get_wiki_page(etools.url_billboard100_by_year,'billboard100_by_year')
        res = db.wiki_html.find_one({'page_type':'billboard100_by_year'})

    soup = BeautifulSoup(res['html'], 'html.parser')
    table = soup.select('#Top-ten_singles_by_year')[0].parent.next_sibling.next_sibling
    a_tags = table.findAll('a')
    return [ctools.wiki_base_url + link.attrs['href'] for link in a_tags]


# def determine