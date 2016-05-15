import os
import json
import shlex
import shutil
import subprocess
from subprocess import STDOUT, check_output
from distutils.version import LooseVersion
from random import shuffle

from .CONSTS import CRX_DIRECTORY

# TODO code quality is veryyy low (chdir, duplication)

def attrget(item, key):
    keys = key.split('.')
    for key in keys:
        if item:
            item = item.get(key, '')
    return item


def sort_semverfiles(files):
    def keyfunc(filename):
        return LooseVersion(filename.replace('.zip', ''))
    return sorted(files, key=keyfunc)


FNULL = open(os.devnull, 'w')

def get_latest_version(ext_id):
    return filename

def extract(ext_id):
    crx_dir = CRX_DIRECTORY+ext_id
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
        #shutil.rmtree(tmp_dir)
    else:
        print('no crx, so saddddd', crx_dir)
    print()
    print()