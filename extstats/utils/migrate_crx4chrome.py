import os, shutil
from tqdm import tqdm

from extstats.parse_infos import extract_manifest_of_file

SOURCE_DIR = 'crawled/crx4chrome/'
DEST_DIR = 'crawled/crx/'

for ext_id in os.listdir(SOURCE_DIR):
    dir_fullpath = SOURCE_DIR+ext_id
    for version_file in os.listdir(dir_fullpath):
        version_path = dir_fullpath+'/'+version_file
        data = extract_manifest_of_file(version_path)
        if data:
            version = data['version']
            dest_dir = DEST_DIR + ext_id + '/'
            destpath = dest_dir + version + '.zip'
            if not os.path.exists(destpath):
                print('adding', ext_id, version)
                os.makedirs(dest_dir, exist_ok=True)
                shutil.copy(version_path, destpath)
