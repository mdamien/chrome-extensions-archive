import json
from collections import Counter

DATA = json.load(open('enriched.json'))

def attrget(item, key):
    keys = key.split('.')
    for key in keys:
        if item:
            item = item.get(key,'')
    return item

def stats(key=None, attrget=attrget, limit=10, inception=False, data=None):
    data = data if data else DATA
    def flat(arr):
        for x in arr:
            if type(x) == type([]):
                yield from flat(x)
            elif type(x) == str:
                yield x.strip()
            else:
                yield x

    c = Counter(flat([attrget(el,key) for el in data]))

    count_all = len(data)
    count_distinct = len(c)
    print()
    print(key,"   -   ",count_all,"values,",count_distinct,"distincts")
    print('----')

    for el,n in c.most_common(limit):
        p = n/count_all*100
        print("{:.1f}% ({}) {}".format(p,n,el))
    print()

    if inception:
        stats(key="---> "+key+'-ception', attrget=lambda i, k: i, data=c.values())

"""
stats('manifest.name')
stats('works_offline')
stats('by_google')
stats('autogen')
stats('available_on_android')
stats('family_unsafe')
stats('kiosk')
stats('page_lang_safe')
stats('offers.properties.price')
stats('version')
stats('item_category')
stats('user_count')
stats('full_description', lambda el,_: el.get('full_description')[:100].strip())
stats('category', lambda el,_: el.get('category','').split(','))#,limit=None)
stats('supported_regions', lambda el,_: el.get('supported_regions','').split(','))
"""

#how many extension with X+ users ?
def safeint(n):
    try:
        return int(n)
    except:
        return -1 

def catall():
    for x in DATA:
        r = safeint(attrget(x, 'user_count'))
        print(r)

def howmanypop(limit):
    result = sum(1 for x in DATA if safeint(attrget(x, 'user_count')) >= limit)
    print('in pop contest (',limit,'+ users) :', result)

howmanypop(1000)
howmanypop(2000)
howmanypop(3000)
howmanypop(4000)
howmanypop(5000)
#howmanypop(10000)