# some stats about collected crxs

import os, time
from tqdm import tqdm

from extstats.CONSTS import CRX_DIRECTORY as DIR

from distutils.version import LooseVersion


#DIR = 'crawled/crx4chrome/'

def sort_semverfiles(files):
    def keyfunc(filename):
        return LooseVersion(filename.replace('.zip', ''))
    return sorted(files, key=keyfunc)

ext_obj = {}
exts = []

TO_RM = []
for ext in tqdm(os.listdir(DIR)):
    files = os.listdir(DIR+ext)
    files_details = []
    try:
        for file in sort_semverfiles(files):
            fullpath = DIR+ext+'/'+file
            size = os.path.getsize(fullpath)
            if size < 10:
                print(ext, file, 'IS 0000000', size)
                TO_RM.append('rm '+fullpath)
            files_details.append({
                'name': file,
                'size': size,
                'created': time.ctime(os.path.getctime(fullpath))
            })
    except TypeError as e:
        print('error with ', ext, files)
        raise e

    exts.append({
        'ext': ext,
        'files': files,
    })
    ext_obj[ext] = files_details

if len(TO_RM) > 0:
    for RM in TO_RM:
        print(RM)

exts.sort(key=lambda x: -len(x['files']))

for ext in exts[:10]:
    print(ext['ext'], len(ext['files']))
    print(*ext['files'])

import json
with open('data/crx_stats.json','w') as f:
    json.dump(ext_obj, f, indent=2)
