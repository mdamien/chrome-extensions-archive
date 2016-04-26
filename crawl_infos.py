import urllib.request
import json, sys
import os.path
import random
from tqdm import tqdm

import json, requests

from store_infos_history import store_infos_history, is_stored_recent, TO_RM
from parse_infos import parse_page

from termcolor import colored
bad = lambda x: colored(x, 'red')
good = lambda x: colored(x, 'green')

urls = json.load(open('crawled/sitemap/final.json'))
random.shuffle(urls)

#for url in urls[11:13]:
for url in tqdm(urls):
	try:
		ext_id = url.split('/')[-1]
		if not is_stored_recent(ext_id):
			try:
				req = requests.get(url)
				if req.status_code == 404:
					print(bad('disapeered'), req.status_code)
					store_infos_history(ext_id, {
						'status': req.status_code,
					})
				if req.status_code != 200:
					print(bad('bad status code:'), req.status_code)
					continue
				page_html = req.text
			except Exception as e:
				print(bad('fail to download page: '+url), e)
				continue
			infos = parse_page(page_html)
			infos['ext_id'] = ext_id
			infos['url'] = url
			store_infos_history(ext_id, infos)
	except Exception as e:
		print('exception with', ext_id)
		raise e

print('RMS ?', len(TO_RM))
for rm in TO_RM:
	print(rm)