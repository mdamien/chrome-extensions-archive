# extract extensions one by one to look for patterns

import os
import json
import shlex
import shutil

import subprocess
from subprocess import STDOUT, check_output

from distutils.version import LooseVersion

from random import shuffle

from extstats.CONSTS import CRX_DIRECTORY


def attrget(item, key):
    keys = key.split('.')
    for key in keys:
        if item:
            item = item.get(key, '')
    return item


def sort_semverfiles(files):
    """
    in a perfect world, I would just sort by creation

    >>> sort_semverfiles(['2.0.zip', '1.0.zip', '3.0.1-beta.zip'])
    ['1.0.zip', '2.0.zip', '3.0.1-beta.zip']

    """
    def keyfunc(filename):
        return LooseVersion(filename.replace('.zip', ''))
    return sorted(files, key=keyfunc)

FNULL = open(os.devnull, 'w')

EXT_LIST = json.load(open('data/PAGES.json'))
# shuffle(EXT_LIST)


def analyze(ext):
    ext_id = ext['ext_id']
    name = ext.get('name')
    print(ext_id, name)
    crx_dir = 'crx_history/'+ext_id
    if os.path.exists(crx_dir):
        tmp_dir = 'tmp/history/'+ext_id
        if os.path.exists(tmp_dir):
            return
        shutil.copytree(crx_dir, tmp_dir)
        os.chdir(tmp_dir)
        files = os.listdir()
        files = sort_semverfiles(files)
        prevdir = None
        for i, file in enumerate(files):
            print('doing', file)
            print('dtrx..')
            check_output('dtrx {} 2>&1 > /dev/null'.format(shlex.quote(file)), timeout=60, shell=True)
            dirname = file.replace('.zip', '')  # = version_name
            os.chdir(dirname)  # security is crazy low
            # os.system('grep -Ri -C 2 "API_KEY" .')
            # os.system('ack-grep -R "UA\-[0-9]+\-[0-9]+" .')
            os.system('ack-grep -Ri "API_*KEY" .')
            os.chdir('..')
            prevdir = dirname
        try:
            shutil.rmtree(final_target_dir)
        except:
            pass
        print(ext_id, 'done')
        os.chdir('../../..')
        shutil.rmtree(tmp_dir)
    else:
        print('no crx, so saddddd', crx_dir)
    print()
    print()

if __name__ == '__main__':
    import doctest
    doctest.testmod()

    os.chdir('crawled')
    for ext in EXT_LIST:
        analyze(ext)
