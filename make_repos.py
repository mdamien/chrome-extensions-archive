import os
import json
import shlex
import shutil

import subprocess
from subprocess import STDOUT, check_output

from distutils.version import LooseVersion

from blacklist import BLACKLIST

from random import shuffle

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

FNULL = open(os.devnull, 'w')

EXT_LIST = json.load(open('data/new_top10k.json'))
EXT_LIST = [x for x in EXT_LIST if x['ext_id'] not in BLACKLIST]
EXT_LIST = EXT_LIST[:1000]
shuffle(EXT_LIST)

def create_one(ext):
	ext_id = ext['ext_id']
	name = ext.get('name')
	print(ext_id, name)
	print(os.getcwd())
	crx_dir = "crx_history/"+ext_id
	if os.path.exists(crx_dir):
		tmp_dir = 'tmp/history/'+ext_id
		shutil.copytree(crx_dir, tmp_dir)
		os.chdir(tmp_dir)
		files = os.listdir()
		files = sort_semverfiles(files)
		prevdir = None
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
				os.system('echo {} > .git/description'.format(
					shlex.quote(name)))
			else:
				os.system('mv ../'+prevdir+'/.git .')
				os.system('git add -A . > /dev/null')
				os.system('git commit -m "{}" > /dev/null'.format(
					shlex.quote(dirname)))
			os.chdir('..')
			prevdir = dirname
		final_target_dir = '../../../../server/repos/'+ext_id
		try:
			shutil.rmtree(final_target_dir)
		except:
			pass
		shutil.move(prevdir, final_target_dir)
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
		create_one(ext)