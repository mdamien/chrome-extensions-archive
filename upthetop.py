import os
import json
import shlex
import shutil

import subprocess
from subprocess import check_call

from distutils.version import LooseVersion

from upload_github import create_repo

"""
todo:
-make backups  :D :D :D :D (gitlab, my own "codesearch",..)
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


created = []
with open('data/repo_created') as f:
	created = [f.strip() for f in f.readlines() if len(f.strip()) > 0]

def save_created():
	with open('../data/repo_created','w') as f:
		for repo in created:
			f.write(repo+'\n')

FNULL = open(os.devnull, 'w')

if __name__ == '__main__':
	import doctest
	doctest.testmod()

	ext_list = json.load(open('data/new_top10k.json'))[20:]
	os.chdir('crawled')
	for ext in ext_list[:1000]:
		ext_id = ext['ext_id']
		print(ext_id, ext.get('name'))
		print(os.getcwd())
		crx_dir = "crx_history/"+ext_id
		if os.path.exists(crx_dir):
			if ext_id not in created:
				print('current dir',os.getcwd())
				create_repo(ext_id, ext.get('name'))
				created.append(ext_id)
				save_created()
			tmp_dir = 'tmp/history/'+ext_id
			shutil.copytree(crx_dir, tmp_dir)
			os.chdir(tmp_dir)
			files = os.listdir()
			files = sort_semverfiles(files)
			prevdir = None
			for i, file in enumerate(files):
				subprocess.call(['dtrx',file], stdout=FNULL, stderr=subprocess.STDOUT)
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
					os.system('git remote add origin git@github.com:chrome-exts/{}.git'.format(ext_id))
					os.system('git push -uf origin master')
				os.chdir('..')
				prevdir = dirname
			print(os.listdir())
			os.chdir('../../..')
			print('current dir',os.getcwd())
			shutil.rmtree(tmp_dir)
		else:
			print('no crx, so saddddd')
		print()