import os
import json
import shlex
import shutil
import portalocker

import subprocess
from subprocess import STDOUT, check_output

from distutils.version import LooseVersion

from upload_github import create_repo

from blacklist import BLACKLIST

from random import shuffle

"""
todo:
-make backups  :D :D :D :D (gitlab, my own "codesearch",..)
-track latest version pushed (to only update new versions arrived)
"""

def attrget(item, key):
    keys = key.split('.')
    for key in keys:
        if item:
            item = item.get(key,'')
    return item

def sort_semverfiles(files):
	"""
	in a perfect world, I would just sort by creation 

	>>> sort_semverfiles(['2.0.zip', '1.0.zip', '3.0.1-beta.zip'])
	['1.0.zip', '2.0.zip', '3.0.1-beta.zip']

	"""
	def keyfunc(filename):
		return LooseVersion(filename.replace('.zip',''))
	return sorted(files, key=keyfunc)

CREATED_FILE = '../../../../data/repo_created'
def get_created():
	with portalocker.Lock(CREATED_FILE, mode='r', truncate=None,
			flags=portalocker.LOCK_SH, timeout=1) as f:
		return json.load(f)

def add_to_created(ext_id, infos):
	#lock strategy fail :( - dafuq damien!
	created = get_created()
	created[ext_id] = infos
	with portalocker.Lock(CREATED_FILE, mode='a', 
			flags=portalocker.LOCK_EX, timeout=1) as f:
		json.dump(created, f)

FNULL = open(os.devnull, 'w')

EXT_LIST = json.load(open('data/new_top10k.json'))
EXT_LIST = [x for x in EXT_LIST if x['ext_id'] not in BLACKLIST]
shuffle(EXT_LIST)

def upload_one(ext):
	ext_id = ext['ext_id']
	print(ext_id, ext.get('name'))
	print(os.getcwd())
	crx_dir = "crx_history/"+ext_id
	if os.path.exists(crx_dir):
		tmp_dir = 'tmp/history/'+ext_id
		shutil.copytree(crx_dir, tmp_dir)
		os.chdir(tmp_dir)
		files = os.listdir()
		files = sort_semverfiles(files)
		prevdir = None
		if ext_id not in get_created():
			print('current dir',os.getcwd())
			create_repo(ext_id, ext.get('name'), ext.get('url'))
			add_to_created(ext_id, files[-1].replace('.zip',''))
		for i, file in enumerate(files):
			print('doing', file)
			print('dtrx..')
			check_output('dtrx {}'.format(shlex.quote(file)), timeout=60, shell=True)
			dirname = file.replace('.zip','') # = version_name
			os.chdir(dirname) #security is crazy low
			if not prevdir: #first, init the dir
				os.system('git init > /dev/null')
				os.system('git config user.name "-"')
				os.system('git config user.email "-"')
				os.system('git add -A . > /dev/null')
				os.system('git commit -m "{}" > /dev/null'.format(
					shlex.quote(dirname)))
			else:
				os.system('mv ../'+prevdir+'/.git .')
				os.system('git add -A . > /dev/null')
				os.system('git commit -m "{}" > /dev/null'.format(
					shlex.quote(dirname)))
			if i == len(files)-1:
				print('git push')
				os.system('git remote add origin git@github.com:chrome-exts/{}.git'.format(ext_id))
				os.system('git push -uf origin master')
			os.chdir('..')
			prevdir = dirname
		print(ext_id,'done')
		os.chdir('../../..')
		shutil.rmtree(tmp_dir)
	else:
		print('no crx, so saddddd')
	print()
	print()

if __name__ == '__main__':
	import doctest
	doctest.testmod()

	os.chdir('crawled')
	for ext in EXT_LIST:
		upload_one(ext)