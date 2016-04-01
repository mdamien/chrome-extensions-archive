import json
import urllib.request
import os.path
import sys

DOWNLOAD_URL = "https://clients2.google.com/service/update2/crx?response=redirect&prodversion=31.0.1609.0&x=id%3D{ID}%26uc"
FILENAME = "crx/{ID}.crx"

def down(ext_id):
    print('down', ext_id)
    filename = FILENAME.format(ID=ext_id)
    if not os.path.isfile(filename) or os.path.getsize(filename) == 0:
	    try:
	        urllib.request.urlretrieve(DOWNLOAD_URL.format(ID=ext_id),
	            FILENAME.format(ID=ext_id))
	    except Exception as e:
	        print('paid extension ?', e)	

if len(sys.argv) > 1:
	down(sys.argv[1])
else:
	for url in json.load(open('extension_list.json')):
	    ext_id = url.split('/')[-1]
	    down(ext_id)
