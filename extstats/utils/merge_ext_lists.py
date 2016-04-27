import json

prev = json.load(open('data/enriched.json'))
curr = json.load(open('data/pages_parsed.json'))

exts_id = set(ext['ext_id'] for ext in curr)

for ext in prev:
	if ext['ext_id'] not in exts_id:
		ext['deleted'] = True
		curr.append(ext)

json.dump(curr, open('data/_merged.json','w'), indent=2)