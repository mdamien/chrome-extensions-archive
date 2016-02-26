import urllib.request
import json
import os.path


FILENAME = "pages/{ID}.html"

for url in json.load(open('extension_list.json')):
    print(url)
    ext_id = url.split('/')[-1]
    filename = FILENAME.format(ID=ext_id)
    if not os.path.isfile(filename):
        try:
            urllib.request.urlretrieve(url, FILENAME.format(ID=ext_id))
        except Exception as e:
            print('what ?', e)
