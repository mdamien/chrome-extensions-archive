import os, shutil
from tqdm import tqdm

from extstats.parse_infos import extract_manifest_of_file

SOURCE_DIR = '/media/rob/backup/all_crx/crx/'
DEST_DIR = '/media/rob/backup/exts/'

for file in tqdm(os.listdir(SOURCE_DIR)):
    ext_id = file.replace('.crx', '')
    fullpath = SOURCE_DIR+file
    data = extract_manifest_of_file(fullpath)
    if data:
        version = data['version']
        dest_dir = DEST_DIR + ext_id + '/'
        destpath = dest_dir + version + '.zip'
        if os.path.exists(destpath) and os.path.isdir(destpath):
            shutil.rmtree(destpath)
        if not os.path.exists(destpath):
            os.makedirs(dest_dir, exist_ok=True)
            shutil.copy(fullpath, destpath)
