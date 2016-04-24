import json
from jinja2 import Template

template = Template(open('stats/template.html').read())

exts = json.load(open('data/enriched.json'))
print('enriched loaded')
crxs = json.load(open('data/crx_stats.json'))
print('file stats loaded')

for ext in exts:
	ext_id = ext['ext_id']
	ext['files'] = crxs.get(ext_id,[])

def safeint(n):
    try:
        return int(n)
    except:
        return -1 

exts = sorted((ext for ext in exts if len(ext['files']) > 0), key=lambda x: -safeint(x.get('user_count')))

result = template.render(exts=exts)
open('stats/index.html','w').write(result)