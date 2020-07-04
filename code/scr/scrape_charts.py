import sys
import requests
import json

import click
import pandas as pd
from tqdm import tqdm
tqdm.pandas()
from bs4 import BeautifulSoup

sys.path.append('..')
from tools import scrape_tools as st
from tools import paths

def get_year_links():
    # Get the list of "Top 10 Singles by Year" page from wikipedia
    soup = BeautifulSoup(requests.get(st.url_list_of_lists).content, 'html.parser')
    table = soup.select('#Top-ten_singles_by_year')[0].parent.next_sibling.next_sibling
    a_tags = table.findAll('a')
    return [st.wiki_base_url + link.attrs['href'] for link in a_tags]

dir = paths.DATA/'wiki-top-10'
def pull_table(yp_url, out=True, write_path=dir):

    def tidy_cell(cell, col=None, year=None):
        cell_text = st.clean_text(cell.text)
        if col in ['entry_date', 'peak_date']:
            cell_text += f' {year}'
        return cell_text

    # Get year from url
    year = yp_url.split('_')[-1]

    # Get html from wikipedia
    soup = BeautifulSoup(requests.get(yp_url).content, 'html.parser')

    # Assuming it's always the first table
    if not soup.select('table.wikitable'):
        return
    table = soup.select('table.wikitable')[0]
    n_cols = len(table.find('tr').find_all('th'))

    rowspan_fix = []
    output_rows=[]

    for i, row in enumerate(table.find_all('tr')):
        output_row = []

        for j, cell in enumerate(row.find_all('td')):
            rowspan = cell.attrs.get('rowspan')
            if rowspan:
                rowspan_fix += [(k,j, cell) for k in range(i+1, i+int(rowspan))]

            output_row.append(cell)
        output_rows.append(output_row)

    for (i,j,cell) in rowspan_fix:
        output_rows[i].insert(j, cell)

    # Build table of tag elelement cells
    df = pd.DataFrame(output_rows)
    df = df[df.columns[:6]].copy() #Drop ref column if it's there
    df.columns = ['entry_date', 'single', 'artist', 'peak', 'peak_date', 'weeks_in_top']
    df.dropna(inplace=True)


    # Tidy up cells, extract data
    for col in [x for x in df.columns if x!='single']:
        df[col] = df[col].apply(lambda x: tidy_cell(x, col, year))

    df['single_url'] = df.single.apply(lambda x: x.find('a').attrs['href']  if x.find('a') else None)
    df.single = df.single.apply(lambda x: tidy_cell(x))

    # Write table
    if out:
        df.to_csv(write_path/f'{year}.csv',index=False)
    return df

@click.command()
@click.option("--pull_year", "-y", default=None, help="Year to pull")
def main(pull_year):
    # Pull one
    year_links = get_year_links()
    if pull_year:
        yl = [link for link in year_links if link.endswith(pull_year)][0]
        pull_table(yl)
    else:
        # Pull all
        for yl in year_links:
            pull_table(yl)

if __name__ == '__main__':
    main()
