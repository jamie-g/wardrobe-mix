from random import choice
from flask import Flask, render_template, request
import polyvore
app = Flask(__name__)
import logging
import requests
logger = app.logger

GOOGLE_URL = "https://www.googleapis.com/shopping/search/v1/public/products?country=US"
GOOGLE_KEY = "AIzaSyDYSIyGTRNGRvv2XDaGplJ7cp5kB0lJzbQ"

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
		terms = get_title_from_google(terms)
		logger.debug("Our new terms are %s from google"%terms)

	results = polyvore.PolyvoreSet.search(terms)
	logger.debug("Result set is %d items"%(len(results)))

	if len(results) > 0:
		start = (p-1)*3
		end = 3*p
		more = end < len(results)
		return render_template("results.html", sets=results[start:end], terms=terms, p=p, more=more)
	else:
		return render_template("search_again.html")



	# Paginate if necessary
	# results = polyvore.PolyvoreSet.search(terms)
	# # return str(results)


# function		
	# try:
	# 	barcode = int(terms)
	# # turns barcode into an integer, if not possible, jumps to 'except'
	# 	r = requests.get("https://www.googleapis.com/shopping/search/v1/public/products?country=US&key=AIzaSyDYSIyGTRNGRvv2XDaGplJ7cp5kB0lJzbQ", params = {"q": barcode})
	# # uses google shopping api to find barcode item
	# 	terms = r.json['items'][0]['product']['title']
	# # assigns variable 'terms' to the value of 'title'
	# 	p = int(request.args.get("p", 1))
	# 	results = polyvore.PolyvoreSet.search(terms)
	# # assigns variable 'results' to the result of running the search function of the PolyvoreSet method with terms
	# 	start = (p-1)*3
	# 	end = 3*p
	# 	results_length = len(results)
	# 	if end < results_length:
	# 		more=True
	# 	else:
	# 		more=False
	# 	# return str(results)
	# 	if len(results) >= 1:
	# 		return render_template("results.html", sets=results[start:end], terms=terms, p=p, more=more)
	# 	else:
	# 		return render_template("search_again.html")

	# except:
	# 	p = int(request.args.get("p", 1))
	# 	results = polyvore.PolyvoreSet.search(terms)
	# 	start = (p-1)*3
	# 	end = 3*p
	# 	results_length = len(results)
	# 	if end < results_length:
	# 		more=True
	# 	else:
	# 		more=False
	# 	# return str(results)
	# 	if len(results) >= 1:
	# 		return render_template("results.html", sets=results[start:end], terms=terms, p=p, more=more)
	# 	else:
	# 		return render_template("search_again.html")



if __name__ == '__main__':
    app.run(debug = True)