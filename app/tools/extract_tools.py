#!/usr/bin/env python
'''
author: Greg Mangan
description: Extraction tools for musicbrainapp, related to scraping
'''

import re
import sys
import pdb
import hashlib
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from musicbrainapp.tools import common_tools as ctools

url_list_of_lists = 'http://en.wikipedia.org/wiki/List_of_Billboard_Hot_100_top-ten_singles'


re_citation = r"\[\d{1,3}\]"

def get_page_title(html):
    ''' Get the value of the html <title>

    Inputs:
        - html(str): the page source html string
    Output:
        (str) the title if found (else None)
    '''
    if not html:
        return None

    match = re_title.search(html)
    if match:
        return match.groupdict()['title']

def fetch_webpage(url):
    ''' Fetch a webpage. Return html source.
    Inputs:
        - url (str): the url to fetch

    Output:
        (dict) with keys: url(str), _ok(bool), html(str), title(str)
    '''
    output = {}
    output['url'] = url
    output['page_id'] = ctools.gen_id(url)

    resp = requests.get(url)

    output['_ok'] = resp.ok
    output['html'] = resp.content.decode() if resp.ok else None
    output['title'] = get_page_title(output['html'])

    return output

def clean_text(string):
    ''' Clean common cell text from a <td> tag '''
    string = string.replace('\xa0', ' ').replace('\n',' ')
    string = re.sub(re_citation, '', string).strip()
    return string

def missing_link(name, soup):
    ''' Find a hpyerlink for a given name '''
    if soup.find('a', text=name):
        return soup.find('a', text=name).attrs.get('href')
    else:
        return None

def extract_list(td, soup):
    '''
    Extract names and URLs from horizontal lists of hyperlinks

    Inputs:
        td (bs4 tag)
    Output:
        (list of dict) with keys name(str), url(str), order(i)
    '''
    result_list = []
    classes = td.attrs.get('class', '')
    # ul case
    if 'hlist' in classes:
        for i, li in enumerate(td.find_all('li')):
            name = clean_text(li.text)
            url = li.find('a').attrs.get('href') if li.find('a') else missing_link(name, soup)
            result_list.append({'name': name, 'url': url, 'order': i})

    # One big list case
    else :
        # Parse "a,b, and c" text case
        if ',' and 'and' in td.text:
            # Split apart from the last 'and'
            it = re.finditer(r'and', td.text)
            a1, a2 = list(it)[-1].span()

            nlist = [clean_text(x) for x in (td.text[:a1] + ',' + td.text[a2:]).split(',')]

            for i, name in enumerate(nlist):
                url = missing_link(name, td)
                result_list.append({'name': name, 'url': missing_link(name, soup), 'order': i})
    # Just text
        else:
            name = clean_text(td.text)
            result_list.append({'name': name , 'url':missing_link(name, soup), 'order': 0})
    return result_list
