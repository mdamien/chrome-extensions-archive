import json
import urllib.request

DOWNLOAD_URL = "https://clients2.google.com/service/update2/crx?response=redirect&prodversion=31.0.1609.0&x=id%3D{ID}%26uc"
FILENAME = "crx/{ID}.zip"

for url in json.load(open('extension_list.json')):
    ext_id = url.split('/')[-1]
    print(ext_id)
    try:
        urllib.request.urlretrieve(DOWNLOAD_URL.format(ID=ext_id),
            FILENAME.format(ID=ext_id))
    except Exception as e:
        print('paid extension ?', e)
