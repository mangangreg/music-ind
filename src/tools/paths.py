from pathlib import Path
import sys

here = Path.cwd().absolute()

ROOT = here.parent.parent
DATA = ROOT / 'data'
TOP10 = DATA / 'wiki-top-10'
SONGS = DATA / 'songs'
