from random import choice
from flask import Flask, render_template, request
import polyvore
app = Flask(__name__)

@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/search')
def search():
	terms = request.args.get("q")
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