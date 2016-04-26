import os, json, datetime, arrow

DIR = 'crawled/pages_infos_history/{id}/'
FILE = '{date}.json'

def is_stored_recent(ext_id, THRESHOLD=60*24): #24h
	dirpath = DIR.format(id=ext_id)
	if os.path.exists(dirpath):
		latest = max([arrow.get(x.replace('.json','')) for x in os.listdir(dirpath)])
		diff = latest.datetime - datetime.datetime.now(datetime.timezone.utc)
		minutes = diff.seconds // 3600
		return minutes < THRESHOLD
	return False

def store_infos_history(ext_id, infos):
	date = datetime.datetime.utcnow().isoformat()
	dirpath = DIR.format(id=ext_id)
	os.makedirs(dirpath, exist_ok=True)
	filepath = dirpath+FILE.format(date=date)
	json.dump(infos, open(filepath, 'w'), indent=2)

if __name__ == "__main__":
	print(is_stored_recent('fghfkeajhcmoohfcfmdkajambdcanmob'))