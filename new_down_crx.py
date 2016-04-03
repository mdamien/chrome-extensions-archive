import json
from pprint import pprint as pp
from download_crx import down
from parse_infos import extract_manifest_of_file
from random import shuffle

import os
import shutil

TMP_FILE = 'crawled/tmp/tmp_crx_{ext_id}.zip'

"""
#one time thing for crx/ already downloaded

extlist = json.load(open('data/top10000.json'))
ids = set([ext['ext_id'] for ext in extlist])

for name in os.listdir('crawled/crx'):
	print(name)
	ext_id = name.split('.')[0]
	if ext_id in ids:
		print('ok')
		full_filename = 'crawled/crx/'+name
		manifest = extract_manifest_of_file(full_filename)
		if manifest and 'version' in manifest:
			print(manifest['version'])
			version = manifest['version']
			path = 'crawled/crx_history/'+ext_id+'/'
			os.makedirs(path, exist_ok=True)
			shutil.move(full_filename, path+version+'.zip')
"""

extlist = json.load(open('data/top10000.json'))
shuffle(extlist)

for ext in extlist:
	ext_id = ext['ext_id']
	print(ext['name'])
	print(ext_id)
	tmp_file = TMP_FILE.format(ext_id=ext_id)
	try:
		down(ext_id, tmp_file)
	except Exception as e:
		print('fail to download:', e)
	manifest = extract_manifest_of_file(tmp_file)
	if manifest and 'version' in manifest:
		pp(manifest['version'])
		version = manifest['version']
		path = 'crawled/crx_history/'+ext_id+'/'
		os.makedirs(path, exist_ok=True)
		shutil.move(tmp_file, path+version+'.zip')
	else:
		try:
		    os.remove(tmp_file)
		except OSError:
		    pass

GIT_AUTHOR_DATE="1459717948 +0200"