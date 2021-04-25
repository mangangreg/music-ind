import re
import sys
import json
import requests
import pdb

import click
import pandas as pd
from tqdm import tqdm
tqdm.pandas()
from bs4 import BeautifulSoup

sys.path.append('../..')
from src.tools import scrape_tools as st
from src.tools import paths

SONGS_DIR = paths.DATA/'songs'

def pull_info(sp_url, out=True, write_path=SONGS_DIR):
    '''
        Pull all information about a song from a wikipedia 'song page'
        Inputs:
            - sp_url (str): a song page url, a relative url (/wiki/...) to a song page
            - out (bool): whether to output the file
            - write_path (str): the path to write the file to if out is True
        Outputs:
            Dictionary of song data
    '''
    try:
        # Generate id
        song_id = st.gen_id(sp_url)
        # Get page html
        soup = BeautifulSoup(requests.get(st.wiki_base_url + sp_url).content, 'html.parser')
        table = soup.select('table.infobox')[0]

        song_data = {}
        song_data['id'] = song_id
        song_data['title'] = table.find('tr').text.strip('"')
        song_data['url'] = sp_url

        # Loop through rows (tr) and identify by heading (th)
        for row in table.find_all('tr'):
            th = row.find('th')
            if th:
                # Artists
                if th.text.startswith('Single by'):
                    links = row.find_all('a')
                    if len(links)==1:
                        song_data.update({'name':row.text.split('Single by ')[1], 'url':None})
                    else:
                        song_data['artists'] = [
                            {'name': artist.text,
                            'url': artist.attrs['href'],
                            'order':i}
                            for i, artist in enumerate(links[1:])]
                # Release Date
                elif th.text.startswith('Released'):
                    song_data.update({'release_date': st.clean_text(row.find('td').text)})

                # Genres
                elif th.text.startswith('Genre'):
                    # song_data['genres'] = [st.clean_text(x.text) for x in row.find('td').find_all('a') if not re.match(re_ref,x.text)]
                    song_data['genres'] = [st.clean_text(x.text) for x in row.find('td').find_all('a') ]

                # Length
                elif th.text.startswith('Length'):
                    song_data.update({'length': st.clean_text(row.find('td').text)})

                # Songwriters
                elif th.text.startswith('Songwriter'):
                    song_data['songwriters'] = st.extract_list(row.find('td'), soup)

                # Producers
                elif th.text.startswith('Producer'):
                    song_data['producers'] = st.extract_list(row.find('td'), soup)

        if out:
            with open(write_path/f'{song_id}.json', 'w') as wfile:
                json.dump(song_data, wfile)

            # db.insert_one()
        return song_data

    except IndexError:
        print(sp_url)


def pull_all_songs(year=None):
    song_idx = [x.stem for x in(paths.SONGS).glob('*')]
    n_years = len(list(x for x in (paths.TOP10).glob('*') if x.is_dir()))

    if year:
        df = pd.read_csv(paths.TOP10/f"{year}.csv", usecols=['single_url'])
        for j, sp_url in df[df.single_url.notna()].single_url.iteritems():
            if st.gen_id(sp_url) not in song_idx:
                pull_info(sp_url)
                print(f"Downloading {sp_url} (id:{st.gen_id(sp_url)})")
    else:
        for year_csv in tqdm((paths.TOP10).iterdir(), total=n_years ):
            df = pd.read_csv(year_csv, usecols=['single_url'])
            for j, sp_url in df[df.single_url.notna()].single_url.iteritems():
                if st.gen_id(sp_url) not in song_idx:
                    pull_info(sp_url)
@click.command()
@click.option("--year", "-y", default=None, help="Year to pull")
def main(year):
    pull_all_songs(year)

if __name__ == '__main__':
    main()
