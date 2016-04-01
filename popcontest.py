import json

DATA = json.load(open('enriched.json'))

def safeint(n):
    try:
        return int(n)
    except:
        return -1 

filtered = sorted((x for x in DATA), key=lambda x: -safeint(x.get('user_count')))[:10000]
json.dump(filtered, open('top10000.json','w'), indent=2, sort_keys=True)