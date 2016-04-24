import json
from pprint import pprint as pp
from download_crx import down
from parse_infos import extract_manifest_of_file, parse_page
from random import shuffle

from termcolor import colored

import sys
import os
import shutil
import requests


ORDER_BY_POP = len(sys.argv) > 1 and sys.argv[1] == 'by_pop'
SPECIFIC_EXT = sys.argv[1] if not ORDER_BY_POP and len(sys.argv) > 1 else None
print('ORDER_BY_POP ?', ORDER_BY_POP)

TMP_FILE = 'crawled/tmp/tmp_crx_{ext_id}.zip'
DEST_DIR = 'crawled/crx_history/{ext_id}/'
DEST_FILE = '{dir}/{version}.zip'

extlist = json.load(open('data/new_top10k.json'))

if not ORDER_BY_POP:
	shuffle(extlist)

bad = lambda x: colored(x, 'red')
good = lambda x: colored(x, 'green')

for ext in extlist:
	ext_id = ext['ext_id']
	if SPECIFIC_EXT and ext_id != SPECIFIC_EXT:
		continue
	print()
	print(ext['name'])
	print(ext_id)
	tmp_file = TMP_FILE.format(ext_id=ext_id)

	#get current version
	url = ext['url']
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
	current_version = infos['version']
	print('current_version:', current_version)

	target_dir_path = DEST_DIR.format(ext_id=ext_id)
	target_file_path = DEST_FILE.format(dir=target_dir_path, version=current_version)

	#download extension
	if not os.path.isfile(target_file_path):
		#^^^ caveat, the guy can have the same version name displayed but different versions
		try:
			down(ext_id, tmp_file)
		except Exception as e:
			print(bad('fail to download crx:'), e)
			continue
		manifest = extract_manifest_of_file(tmp_file)
		if manifest and 'version' in manifest:
			version = manifest['version']
			print(good('manifest version:'), version)
			#current_version represent version_name so it can be different than the version stored
			target_file_path = DEST_FILE.format(dir=target_dir_path, version=version)
			if os.path.isfile(target_file_path):
				print(bad("file is already here, here's the version_name"), 
					manifest.get('version_name'),
					'and .version=',manifest.get('version'))
				os.remove(tmp_file)
				continue
			print(good('version is added :D'))
			#assert current_version == version_name or version
			os.makedirs(target_dir_path, exist_ok=True)
			shutil.move(tmp_file, target_file_path)
		else:
			try:
			    os.remove(tmp_file)
			except OSError:
			    pass
	else:
		print('latest version already downloaded')

GIT_AUTHOR_DATE="1459717948 +0200"