#!/usr/bin/env python
'''
author: Greg Mangan
description: A shell for debugging
'''

import sys
import importlib
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from tools import common_tools as ctools

reload = importlib.reload
import_dict = {
    'tools.common_tools': 'ctools',
    'tools.extract_tools': 'etools',
    'tools.transform_tools': 'ttools',
    'tools.db_tools': 'dbtools',
    'tools.load_tools': 'ltools',
    'tools.paths': 'paths'

}

print('')
for mod, alias in import_dict.items():
    globals().update({alias:importlib.import_module(mod)})
    print(f"Imported {mod} as {alias}")

MC = dbtools.MongoConnect()
MC.connect()

print(f"Imported MongoConnection as MC")