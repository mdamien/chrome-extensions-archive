import json, datetime

exts = json.load(open('data/PAGES.json'))
print('enriched loaded')
crxs = json.load(open('data/crx_stats.json'))
print('file stats loaded')

DATA = []

for ext in exts[:40000]:
    try:
        DATA.append({
            'id': ext['ext_id'],
            'name': ext['name'],
            'files': crxs.get(ext['ext_id'],[])
        })
    except Exception as e:
        print(ext)
        print(e)
        break

json.dump(DATA, open('../exts-site/data.json','w'), sort_keys=True)