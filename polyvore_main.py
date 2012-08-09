from random import choice
from flask import Flask, render_template, request
import polyvore
app = Flask(__name__)

@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/search')
def search():
	# terms = request.args.get("q")
	# p = int(request.args.get("p", 1))
	# results = polyvore.PolyvoreSet.search(terms)
	# start = (p-1)*3
	# end = 3*p
	# results_length = len(results)
	# if end < results_length:
	# 	more=True
	# else:
	# 	more=False
	# # return str(results)
	# if len(results) >= 1:
	# 	return render_template("results.html", sets=results[start:end], terms=terms, p=p, more=more)
	# else:
	# 	return render_template("search_again.html")
	try:
		barcode = int(terms)
	# turns barcode into an integer, if not possible, jumps to 'except'
		r = requests.get("https://www.googleapis.com/shopping/search/v1/public/products?country=US&key=AIzaSyDYSIyGTRNGRvv2XDaGplJ7cp5kB0lJzbQ", params = {"q": barcode})
	# uses google shopping api to find barcode item
		terms = r.json['items'][0]['product']['title']
	# assigns variable 'terms' to the value of 'title'
		p = int(request.args.get("p", 1))
		results = polyvore.PolyvoreSet.search(terms)
	# assigns variable 'results' to the result of running the search function of the PolyvoreSet method with terms
		start = (p-1)*3
		end = 3*p
		results_length = len(results)
		if end < results_length:
			more=True
		else:
			more=False
		# return str(results)
		if len(results) >= 1:
			return render_template("results.html", sets=results[start:end], terms=terms, p=p, more=more)
		else:
			return render_template("search_again.html")

	except:
		p = int(request.args.get("p", 1))
		results = polyvore.PolyvoreSet.search(terms)
		start = (p-1)*3
		end = 3*p
		results_length = len(results)
		if end < results_length:
			more=True
		else:
			more=False
		# return str(results)
		if len(results) >= 1:
			return render_template("results.html", sets=results[start:end], terms=terms, p=p, more=more)
		else:
			return render_template("search_again.html")



if __name__ == '__main__':
    app.run(debug = True)