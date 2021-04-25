import os
import sys
import pdb
from pathlib import Path

import pymongo
from dotenv import load_dotenv

sys.path.append(Path(__file__).resolve().parents[1])
from tools import paths

MONGO_RESULTS_ATTRIBUTES = {
    'update': ('acknowledged', 'matched_count', 'modified_count', 'ok', 'upserted_id'),
    'insert_one': ('acknowledged', 'inserted_id'),
    'insert_many': ('acknowledged', 'inserted_ids'),
}

class MongoConnect:
    def __init__(self, user=None, password=None, host=None, port=None, database=None, env_file=paths.MONGO_ENV):

        # Load the env file
        load_dotenv(env_file)

        self.user = user or os.getenv('MONGO_USER')
        self.password = password or os.getenv('MONGO_PASSWORD')
        self.host = host or os.getenv('MONGO_HOST') or 'localhost'
        self.port = port or os.getenv('MONGO_PORT') or 27017
        self.database = database or os.getenv('MONGO_DATABASE')

        # Build the URI
        self.URI = self._constructURI()

        # Initialise connection and db
        self.connection = None
        self.db = None

    def _constructURI(self):
        return f"mongodb://{self.user}:{self.password}@{self.host}:{self.port}"

    def connect(self):
        self.connection = pymongo.MongoClient(self.URI)
        self.db = self.connection[self.database]

    # TODO indexing

def parse_mongo_result(res):
    '''
    Parse the useful info from a mongo response

    Inputs:
        - res (pymongo.results): a mongo.results.__ object

    Output:
        (dict)

    '''
    if type(res) == pymongo.results.UpdateResult:

        output = {k:res.__getattribute__(k) for k in dir(res) if k in MONGO_RESULTS_ATTRIBUTES['update']}

    # Convert bson ObjectId to string
    for k in output:
        if k.endswith('_id'):
            print(output[k])
            output[k] = str(output[k])
        elif k.endswith('_ids'):
            print(output[k])
            output[k] = [str(x) for x in output[k]]

    return output


def get_seen_wiki_year_pages():
    MC = MongoConnect(database='landing')
    MC.connect()
    db = MC.db
    res = db.wiki_html.find({'page_type':'billboard100_year'}, {'html':0})
    if res:
        return list(res)
