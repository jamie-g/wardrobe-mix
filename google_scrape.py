from bs4 import BeautifulSoup
import requests
import re
import polyvore

GOOGLE_URL = "http://www.google.com/search"
# POLYVORE_URL_TEMPLATE = "http://ak2.polyvoreimg.com/cgi/img-set/cid/%s/size/y.jpg"

def construct_query(terms):
	return "%s site:polyvore.com inurl:set"%terms


def get_polyvore_url(h3):
	url = h3.a['href']
	match = re.search("id%3D(\d+)&", url)
	# print url
	polyvore_id = match.group(1)
	p_set = polyvore.GooglePolyvoreSet(int(polyvore_id))
	return p_set

def get_polyvore_from_google(terms):
	q = construct_query(terms)
	r = requests.get(GOOGLE_URL, params={"q": q})
	html = r.content
	# print html

	soup = BeautifulSoup(html)

	h3s = soup.find_all("h3", {"class": "r"})
	# print h3s
	urls = []
	for h3 in h3s:
		urls.append(get_polyvore_url(h3))

	return urls


if __name__ == "__main__":
	print [ s.image_url() for s in get_polyvore_from_google("mossimo cateye glasses") ]