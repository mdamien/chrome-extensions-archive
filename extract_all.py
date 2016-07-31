# extract all sources in one big directory to make it easy to grep through all the sources

import os
import shlex
from tqdm import tqdm
import shutil
import subprocess
from subprocess import STDOUT, check_output

from extstats.CONSTS import CRX_DIRECTORY as DIR
from distutils.version import LooseVersion

DESTINATION = 'crawled/sources/{ext_id}/{version}'

def sort_semverfiles(files):
    def keyfunc(filename):
        return LooseVersion(filename.replace('.zip', ''))
    return sorted(files, key=keyfunc)

for ext in os.listdir(DIR):
    files = os.listdir(DIR + ext)
    files_details = []
    latest = sort_semverfiles(files)[-1]
    fullpath = DIR + ext + '/' + latest
    size = os.path.getsize(fullpath)
    if size > 100000000: #100mb
        continue
    print(fullpath, size)
    dest = DESTINATION.format(ext_id=ext, version=latest.replace('.zip', ''))
    try:
        shutil.rmtree(dest)
    except FileNotFoundError:
        pass
    os.makedirs(dest, exist_ok=True)
    try:
        check_output('unzip {} -d {}'.format(shlex.quote(fullpath), shlex.quote(dest)), timeout=60, shell=True)
    except subprocess.CalledProcessError as e:
        print('error:', e.returncode, ' - ', e.cmd)
    except subprocess.TimeoutExpired:
        pass
