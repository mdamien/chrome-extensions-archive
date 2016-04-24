# some stats about collected crxs

import os
from tqdm import tqdm

DIR = 'crawled/crx_history/'

ext_obj = {}
exts = []

for ext in tqdm(os.listdir(DIR)):
	files = os.listdir(DIR+ext)
	exts.append({
		'ext': ext,
		'files': files,
	})
	ext_obj[ext] = files

exts.sort(key=lambda x: -len(x['files']))

for ext in exts:
	print(ext['ext'], len(ext['files']))
	print(*ext['files'])
	if len(ext['files']) < 2:
		break

import json
with open('data/crx_stats.json','w') as f:
	json.dump(ext_obj, f, indent=2)