#!/usr/bin/env python
'''
author: Greg Mangan
description: Project paths for musicbrainapp
'''
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
ROOT = here.parents[0]
# DATA = ROOT / 'data'
# TOP10 = DATA / 'wiki-top-10'
# SONGS = DATA / 'songs'

MONGO_ENV = ROOT/'.mongo.env'

db = {
    'address': "localhost",
    'port': 27017
}