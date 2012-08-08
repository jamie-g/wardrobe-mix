import requests

class Polyvore(object):
    @classmethod
    def search(cls, terms):
        url = cls.SEARCH_URL
        raw_results = requests.get(url, params = {"query": terms, ".out": "json"})
        results = raw_results.json

        items = results['result']['items']

        objs = []
        for item in items:
            objs.append(cls(item))

        return objs


class PolyvoreThing(Polyvore):
    SEARCH_URL = "http://www.polyvore.com/cgi/shop"

    def __init__(self, fields):
        self.paid_url = fields.get('paid_url')
        self.id = int(fields['thing_id'])
        self.offer = fields.get('offer')
        self.save_count = int(fields.get('save_count', 0))
        self.url = fields['url']
        self.display_url = fields['displayurl']
        self.description = fields.get('description')
        self.seo_title = fields['seo_title']
        self.title = fields['title']
        self.display_price = fields.get('display_price')
        self.orig_price = fields.get('orig_price')

    def __str__(self):
        return "<PolyvoreThing:%d %s>"%(self.id, self.title)

    def image_url(self, size="y"):
        url_template = "http://ak2.polyvoreimg.com/cgi/img-thing/size/%s/tid/%d.png"
        return url_template%(size, self.id)


class PolyvoreSet(Polyvore):
    SEARCH_URL = "http://www.polyvore.com/cgi/search.sets"

    def __init__(self, fields):
        self.img_width = fields['imgw']
        self.img_height = fields['imgh']
        self.user_name = fields['user_name']
        self.uuid = fields['spec_uuid']
        self.seo_title = fields['seo_title']
        self.user_url = fields['userurl']
        self.id = int(fields['object_id'])
        self.title = fields['title']
        self.user_id = int(fields['createdby'])
        self.score = float(fields['score_total'])
        self.url = "http://www.polyvore.com" + fields['clickurl'].replace("..", "")
        self._things = []

    def image_url(self, size="y"):
        base_url = "http://ak2.polyvoreimg.com/cgi/img-set/cid/%d/id/%s/size/%s.jpg"
        return base_url%(self.id, self.uuid, size)
        pass

    @property
    def things(self):
        if self._things != []:
            return self._things

        r = requests.get(self.url, params={".out": "json"})
        raw_thing_data = r.json
        items = raw_thing_data['overlay_items']
        item_objs = []
        for item in items:
            item_objs.append(PolyvoreThing(item))

        self._things = item_objs
        return self._things

    def __str__(self):
        return ""


if __name__ == "__main__":
    sets = PolyvoreSet.search("brown pants")
