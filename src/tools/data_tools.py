import sys
import json
from pathlib import Path 

import pandas as pd

root = '../..' if Path(__file__).resolve().parent == Path.cwd() else '.'
sys.path.append(root)
from src.tools import paths
from src.tools import scrape_tools as st

def load_charts(year):
    '''Load charts for a given year'''
    fpath = paths.DATA/'wiki-top-10'/f"{year}.csv"
    df = pd.read_csv(fpath)
    return df

def load_single(single_url):
    id = st.gen_id(single_url)
    fpath = paths.DATA/'songs'/f"{id}.json"

    if not fpath.exists():
        raise ValueError('File does not exist for this song')

    else:
        return json.load((open(fpath)), encoding="utf-8")
