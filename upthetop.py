import os
import json
import shlex

from subprocess import check_call

SCRIPT = """
python3 download_crx.py {ext_id}
python3 upload_github.py {ext_id} {name}
cp crx/{ext_id}.crx github_upload/{ext_id}.zip
cd github_upload/
#todo git clone --depth=1 old one
rm -rf {ext_id}/
dtrx {ext_id}.zip
cd {ext_id}
git init
git config user.name "-"
git config user.email "-"
git add -A .
git commit -m "{version}"
git remote add origin git@github.com:chrome-exts/{ext_id}.git
git push -uf origin master
"""

def attrget(item, key):
    keys = key.split('.')
    for key in keys:
        if item:
            item = item.get(key,'')
    return item

for ext in json.load(open('top10000.json'))[:20]:
	print(ext['ext_id'],ext.get('name'))
	script = SCRIPT.format(ext_id=ext['ext_id'],
		name=shlex.quote(ext.get('name','')),
		date='$(date -R)',
		version=attrget(ext, 'version'))
	#print(script)
	check_call(script, shell=True)