import sys
import json
from pathlib import Path
from pymongo import MongoClient

from tqdm import tqdm

import pandas as pd

root = '../..' if Path(__file__).resolve().parent == Path.cwd() else '.'
sys.path.append(root)
from src.tools import paths
from src.tools import scrape_tools as st

client = MongoClient("localhost", 27017)


def load_charts(year):
    '''Load charts for a given year'''
    fpath = paths.DATA/'wiki-top-10'/f"{year}.csv"
    df = pd.read_csv(fpath)
    return df

def load_single(single_url):
    id = st.gen_id(single_url)
    fpath = paths.SONGS/f"{id}.json"

    if not fpath.exists():
        raise ValueError('File does not exist for this song')

    else:
        return json.load((open(fpath)), encoding="utf-8")

def refresh_db():
    client = MongoClient("localhost", 27017)
    db = client.musicind
    db.songs.delete_many({})
    song_paths = list(paths.SONGS.glob('*.json'))
    for song_file in tqdm(song_paths):
        song_data = json.load((open(song_file)), encoding="utf-8")
        db.songs.insert_one(song_data)
