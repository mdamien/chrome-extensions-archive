import glob
import extruct
import json
import re
from extruct.w3cmicrodata import MicrodataExtractor

from bs4 import BeautifulSoup

def pagemap_extract(html):
    pagemap = re.findall(r"(<PageMap>.*</PageMap>)", html, re.MULTILINE)[0]
    soup = BeautifulSoup(pagemap, "lxml")
    data = {}
    for attr in soup.find_all('attribute'):
        data[attr['name']] = attr.text
    return data

def scrap(html):
    soup = BeautifulSoup(html, "lxml")
    data = {}
    data['description'] = soup.find('pre').text.strip()
    return data

mde = MicrodataExtractor()

for filename in glob.glob("pages/*.html"):
    print(filename)
    ext_id = filename.split('.')[0].split('/')[-1]
    with open(filename) as f:
        html = f.read()
        data = {}
        data['meta'] = mde.extract(html)['items'][0]['properties']
        data['pagemap'] = pagemap_extract(html)
        data['scrap'] = scrap(html)
        with open('scratch/{}.json'.format(ext_id), 'w') as out:
            json.dump(data, out, indent=2, sort_keys=True)
