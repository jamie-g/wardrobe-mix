from random import choice
from flask import Flask, render_template, request
import polyvore
import os
app = Flask(__name__)
import logging
import requests
import google_scrape
logger = app.logger

GOOGLE_URL = "https://www.googleapis.com/shopping/search/v1/public/products?country=US"
GOOGLE_KEY = "AIzaSyDYSIyGTRNGRvv2XDaGplJ7cp5kB0lJzbQ"
# BARCODE_WEB

def is_int(string, default = 0):
	try:
		num = int(string)
		return num
	except:
		return default

def is_barcode(terms):
	terms = terms.strip()
	if len(terms) != 12 and len(terms) != 13:
		logger.debug("Terms is %d long"%(len(terms)))
		return False

	if not is_int(terms):
		logger.debug("Terms is not an integer")
		return False

	return True

# def scan():
# 	http://zxing.appspot.com/scan?ret=http://foo.com/products/{CODE}/description&SCAN_FORMATS=UPC_A,EAN_13

def get_title_from_google(barcode):
	r = requests.get(GOOGLE_URL, params = {"q": barcode, "key": GOOGLE_KEY})
	results = r.json
	num_results = results['totalItems']

	if num_results > 0:
		terms = results['items'][0]['product']['title']
	else:
		terms = barcode
	
	return terms

@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/search')
def search():
	terms = request.args.get("q")
	p = is_int(request.args.get("p"), 1)

	logger.debug("Searching for %s"%terms)

	if is_barcode(terms):
		logger.debug("%s is a barcode"%terms)
		new_terms = get_title_from_google(terms)
		logger.debug("Our new terms are %s from google"%new_terms)
		results = google_scrape.get_polyvore_from_google(new_terms)
	else:
		results = polyvore.PolyvoreSet.search(terms)
	
	logger.debug("Result set is %d items"%(len(results)))

	if len(results) > 0:
		start = (p-1)*3
		end = 3*p
		more = end < len(results)
		return render_template("results.html", sets=results[start:end], terms=terms, p=p, more=more)
	else:
		return render_template("search_again.html")

if __name__ == '__main__':
   port = int(os.environ.get('PORT', 5000))
   app.run(host='0.0.0.0', port=port)