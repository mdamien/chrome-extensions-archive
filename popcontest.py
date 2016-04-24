import json

DATA = json.load(open('data/pages_parsed.json'))
print(len(DATA), 'extensions')

def safeint(n):
    try:
        return int(n)
    except:
        return -1 

filtered = sorted((x for x in DATA), key=lambda x: -safeint(x.get('user_count')))[:20000]
for x in filtered[:20]:
	print(x['ext_id'], x['name'], x['user_count'])

print()
print('--bottom:')
for x in filtered[-20:]:
	print(x['ext_id'], x['name'], x['user_count'])

json.dump(filtered, open('data/new_top20k.json','w'), indent=2, sort_keys=True)