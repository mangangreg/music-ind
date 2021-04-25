#!/usr/bin/env python
'''
author: Greg Mangan
description: Transformation tools for musicbrainapp ETL, related to parsing html
'''

import re
import sys
import pdb
import hashlib
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from tools import common_tools as ctools

def get_year_links(html):
    ''' Get the links for top 10 '''
    # Get the list of "Top 10 Singles by Year" page from wikipedia

    soup = BeautifulSoup(requests.get(st.url_list_of_lists).content, 'html.parser')
    table = soup.select('#Top-ten_singles_by_year')[0].parent.next_sibling.next_sibling
    a_tags = table.findAll('a')
    return [st.wiki_base_url + link.attrs['href'] for link in a_tags]