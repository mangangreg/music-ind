from flask import jsonify

from webapp import app
from scripts import extract, transform
from tools import db_tools as dbtools
@app.route("/")
def hello():
    return "UPDATED New routes.py! Hello Greg from Flask in a uWSGI Nginx Docker container with \
     Python 3.8 (from the example template)"

@app.route("/test")
def test():
    return "New test!"

@app.route("/api/getWikiBillboardByYear")
def getWikiBillboardByYear():
    url = extract.etools.url_billboard100_by_year
    mongo_response = extract.get_wiki_page(url,'billboard100_by_year')
    return jsonify({'data': mongo_response})

@app.route("/api/getTop10ByYearUrls")
def get_top10_by_year_urls():
    ''' Get the urls by year for the top10 pages'''
    links = extract.get_year_links()
    return jsonify({'data': {'links': links}})

# TODO move this to an airflow routine
@app.route("/api/getChartPages")
def getChartPages():

    years_seen = dbtools.get_seen_wiki_year_pages()
    years_seen_urls = set(x['url'] for x in years_seen)


    years_links = extract.get_year_links()
    N = len(years_links)
    grabbed = 0
    for i, link in enumerate(years_links):
        if (link not in years_seen_urls) or i==N-1:

            res = extract.get_wiki_page(link,'billboard100_year')
            if res:
                print(res)
                grabbed +=1
    return jsonify({'data':{'grabbed':N}})
