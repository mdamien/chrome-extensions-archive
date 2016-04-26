import json, random, os
from tqdm import tqdm

from store_infos_history import latest_good, TO_RM

DIR = 'crawled/pages_infos_history/'
ext_ids = os.listdir(DIR)

exts = []

urls = {url.split('/')[-1]:url for url in json.load(open('crawled/sitemap/final.json'))}

for ext_id in tqdm(ext_ids):
	latest = latest_good(ext_id)
	if latest:
		content = latest['content']
		content['ext_id'] = ext_id
		if 'url' not in content:
			if ext_id in urls:
				content['url'] = urls[ext_id]
			else:
				content['url'] = "https://chrome.google.com/webstore/detail/_/"+ext_id
		content['not_in_sitemap'] = ext_id not in urls
		exts.append(content)
	if len(TO_RM) % 100 == 10:
		print(len(TO_RM))

print(len(exts))

print(len(exts), 'extensions')

def safeint(n):
    try:
        return int(n)
    except:
        return -1 

exts = sorted((x for x in exts), key=lambda x: -safeint(x.get('user_count')))

json.dump(exts, open('data/__page_history_all.json','w'), indent=2, sort_keys=True)

for x in exts[:20]:
	print(x['name'], x['user_count'])

print()
print('deleted:')
for x in [x for x in exts if x.get('deleted')][:10]:
	print(x['name'], x['user_count'])

print('\n'.join(TO_RM))
