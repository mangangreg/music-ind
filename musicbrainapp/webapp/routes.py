from flask import jsonify

from webapp import app
from scripts import extract, transform
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
