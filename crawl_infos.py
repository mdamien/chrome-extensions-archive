import urllib.request
import json
import os.path
import random


FILENAME = "crawled/pages/{ID}.html"

urls = json.load(open('crawled/sitemap/final.json'))
random.shuffle(urls)

for url in urls:
    print(url)
    ext_id = url.split('/')[-1]
    filename = FILENAME.format(ID=ext_id)
    if not os.path.isfile(filename):
        try:
            urllib.request.urlretrieve(url, FILENAME.format(ID=ext_id))
        except Exception as e:
            print('what ?', e)
