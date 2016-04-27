import json

exts = json.load(open('enriched.json'))

def count(ext):
	return -int(ext.get('user_count', "-1"))

for ext in sorted(exts, key=count)[:30]:
	print(ext.get('name',''),':',ext['user_count'])
	#print(ext.get('ext_id'))