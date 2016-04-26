import os.path, os, datetime, random
DIR = 'crawled/pages/'

from store_infos_history import store_infos_history

from parse_infos import parse_page
from tqdm import tqdm

files = os.listdir(DIR)
random.shuffle(files)

for file in tqdm(files):
	fullpath = DIR+file
	time = datetime.datetime.fromtimestamp(os.path.getmtime(fullpath))
	ext_id = file.replace('.html','')
	content = open(fullpath).read()
	try:
		infos = parse_page(content)
	except Exception as e:
		print('failed to parse', fullpath)
		continue
	infos['ext_id'] = ext_id
	#print(ext_id, time.isoformat())
	store_infos_history(ext_id, infos, time)