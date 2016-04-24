import json
from jinja2 import Template

template = Template(open('stats/template.html').read())

exts = json.load(open('data/new_top10k.json'))
crxs = json.load(open('data/crx_stats.json'))

for ext in exts:
	ext_id = ext['ext_id']
	ext['files'] = crxs.get(ext_id,[])

result = template.render(exts=exts)
open('stats/result.html','w').write(result)