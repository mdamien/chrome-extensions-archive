from crawl_comments import get_all_webstore_data

import urllib.request
import json
import os.path

FILENAME = "comments/{ID}.json"

for url in json.load(open('extension_list.json')):
    print(url)
    ext_id = url.split('/')[-1]
    filename = FILENAME.format(ID=ext_id)
    if not os.path.isfile(filename):
        try:
            comments = get_all_webstore_data(ext_id)
            with open(filename,'w') as f:
            	json.dump(comments, f, indent=2)
        except Exception as e:
            print('what ?', e)
