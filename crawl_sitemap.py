from __future__ import with_statement # we'll use this later, has to be here
from argparse import ArgumentParser

import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import lxml.etree
import json

import shutil

import signal
import sys

from tqdm import tqdm

class Sitemap(object):
    """Class to parse Sitemap (type=urlset) and Sitemap Index
    (type=sitemapindex) files"""

    def __init__(self, xmltext):
        xmlp = lxml.etree.XMLParser(recover=True, remove_comments=True, resolve_entities=False)
        self._root = lxml.etree.fromstring(xmltext, parser=xmlp)
        rt = self._root.tag
        self.type = self._root.tag.split('}', 1)[1] if '}' in rt else rt

    def __iter__(self):
        for elem in self._root.getchildren():
            d = {}
            for el in elem.getchildren():
                tag = el.tag
                name = tag.split('}', 1)[1] if '}' in tag else tag

                if name == 'link':
                    if 'href' in el.attrib:
                        d.setdefault('alternate', []).append(el.get('href'))
                else:
                    d[name] = el.text.strip() if el.text else ''

            if 'loc' in d:
                yield d


def sitemap_urls_from_robots(robots_text):
    """Return an iterator over all sitemap urls contained in the given
    robots.txt file
    """
    for line in robots_text.splitlines():
        if line.lstrip().startswith('Sitemap:'):
            yield line.split(':', 1)[1].strip()

results = set()
results = set(json.load(open('data/not_in_sitemap.json')))
print(results)

session = requests.Session()
retries = Retry(total=5,
                backoff_factor=0.1,
                status_forcelist=[503])
session.mount("https://chrome.google.com/", HTTPAdapter(max_retries=retries))

def signal_handler(signal, frame):
    print('Ctrl-C pressed; saving what we have so far')
    save()
    shutil.copy('crawled/sitemap/result.json','data/sitemap.json')
    sys.exit(0)

def save():
    json.dump(sorted(list(results)),
        open('crawled/sitemap/result.json','w'), indent=2, sort_keys=True)

def parse_sitemap(url, depth=0):
    resp = session.get(url)
    try:
        sitemap = Sitemap(resp.content)
    except:
        print('fuck', url)
        print(resp)
        print(resp.content)
        return
    if depth == 0:
        sitemap = tqdm(list(sitemap))
    for line in sitemap:
        if '/webstore/sitemap?' in line['loc']:
            parse_sitemap(line['loc'], depth+1)
        else:
            results.add(line['loc'].split('?')[0])
    save()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    parse_sitemap("https://chrome.google.com/webstore/sitemap")
    shutil.copy('crawled/sitemap/result.json','data/sitemap.json')
