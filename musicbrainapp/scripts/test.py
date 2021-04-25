import re
import sys
from pathlib import Path

root = '../..' if Path(__file__).resolve().parent == Path.cwd() else '.'
sys.path.append(root)

from src.tools import paths
from src.tools import data_tools as dt
from src.tools import scrape_tools as st
from src.scripts import scrape_songpage as ss

# bruce = ss.pull_info('/wiki/Streets_of_Philadelphia', False, Path.cwd())
sara = ss.pull_info('/wiki/Sara_(Fleetwood_Mac_song)',False, Path.cwd())
print(sara)