# some stats about collected crxs

import os
from tqdm import tqdm

from distutils.version import LooseVersion

def sort_semverfiles(files):
	def keyfunc(filename):
		return LooseVersion(filename.replace('.zip',''))
	return sorted(files, key=keyfunc)

DIR = 'crawled/crx_history/'

ext_obj = {}
exts = []

for ext in tqdm(os.listdir(DIR)):
	files = os.listdir(DIR+ext)
	files_details = []
	for file in sort_semverfiles(files):
		fullpath = DIR+ext+'/'+file
		size = os.path.getsize(fullpath)
		files_details.append({
			'name': file,
			'size': size,
		})

	exts.append({
		'ext': ext,
		'files': files,
	})
	ext_obj[ext] = files_details

exts.sort(key=lambda x: -len(x['files']))

for ext in exts:
	print(ext['ext'], len(ext['files']))
	print(*ext['files'])
	if len(ext['files']) < 2:
		break

import json
with open('data/crx_stats.json','w') as f:
	json.dump(ext_obj, f, indent=2)