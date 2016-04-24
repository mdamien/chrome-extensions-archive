import os, json, datetime

DIR = 'crawled/pages_infos_history/{id}/'
FILE = '{date}.json'

def store_infos_history(ext_id, infos):
	date = datetime.datetime.utcnow().isoformat()
	dirpath = DIR.format(id=ext_id)
	os.makedirs(dirpath, exist_ok=True)
	filepath = dirpath+FILE.format(date=date)
	json.dump(infos, open(filepath, 'w'), indent=2)