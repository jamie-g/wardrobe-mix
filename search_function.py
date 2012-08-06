import requests
import polyvore
from polyvore import Polyvore, PolyvoreThing, PolyvoreSet

barcode = "490900117210"
print barcode
r = requests.get("https://www.googleapis.com/shopping/search/v1/public/products?country=US&key=AIzaSyDYSIyGTRNGRvv2XDaGplJ7cp5kB0lJzbQ", params = {"q": barcode})
# searches Google Shopping with barcode information
print r
title = r.json['items'][0]['product']['title']
# gets text title from JSON
print title
r = requests.get("https://www.googleapis.com/customsearch/v1?key=AIzaSyDYSIyGTRNGRvv2XDaGplJ7cp5kB0lJzbQ&cx=013036536707430787589:_pqjad5hr1a&siteSearch=polyvore.com&allinurl: set?id &alt=json", params = {"q": title})
# uses Google to search Polyvore with title
print r.url
something = r.json['items'][0]['link']
# assigns variable to link
print something



# results = http://www.google.com/search?q=http://www.polyvore.com/%s % barcode_text
# setlist = []
# for result in results:
# 	if "set?id" in results:
# 		setlist.append()

if __name__ == "__main__":
	barcode = "490900117210"
