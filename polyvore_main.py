from flask import Flask, render_template, request
import polyvore
app = Flask(__name__)

@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/search')
def search():
	terms = request.args.get("q")
	results = polyvore.PolyvoreSet.search(terms)
	# return str(results)
	return render_template("results.html", sets=results[0:3])

if __name__ == '__main__':
    app.run(debug = True)