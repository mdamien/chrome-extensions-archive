import urllib.request
import json
import os.path
import random

import json, requests

from store_infos_history import store_infos_history, is_stored_recent
from parse_infos import parse_page

from termcolor import colored
bad = lambda x: colored(x, 'red')
good = lambda x: colored(x, 'green')

urls = json.load(open('crawled/sitemap/final.json'))

for url in urls:
	print(url)
	ext_id = url.split('/')[-1]
	if not is_stored_recent(ext_id):
		try:
			req = requests.get(url)
			if req.status_code != 200:
				print(bad('bad status code:'), req.status_code)
				continue
			page_html = req.text
		except Exception as e:
			print(bad('fail to download page: '+url), e)
			continue
		infos = parse_page(page_html)
		store_infos_history(ext_id, infos)
	else:
		print('already stored recently')