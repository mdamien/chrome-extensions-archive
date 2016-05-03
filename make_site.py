import json, datetime
from jinja2 import Template

from extstats.download_crx import DOWNLOAD_URL

# jinja thing
from jinja2 import evalcontextfilter, Environment, FileSystemLoader
@evalcontextfilter
def add_commas(eval_ctx, value):
    return "{:,}".format(int(value))
env = Environment(loader=FileSystemLoader('extstats'))
env.filters['add_commas'] = add_commas
template = env.get_template('template.html')


VIEW_SOURCE_URL = "https://robwu.nl/crxviewer/crxviewer.html?crx="

exts = json.load(open('data/PAGES.json'))
print('enriched loaded')
crxs = json.load(open('data/crx_stats.json'))
print('file stats loaded')

for ext in exts:
    ext_id = ext['ext_id']
    ext['files'] = crxs.get(ext_id,[])
    ext['download_link'] = DOWNLOAD_URL.format(ID=ext_id)
    ext['view_source'] = VIEW_SOURCE_URL+ext['download_link']
    for file in ext['files']:
        file['storage_url'] = "https://storage.googleapis.com/chrmexts/crx/{ext_id}/{file}".format(
            ext_id=ext_id, file=file['name'])
    if not 'user_count' in ext:
        print(ext)

def safeint(n):
    try:
        return int(n)
    except:
        return -1

def split_list(L, n):
    assert type(L) is list, "L is not a list"
    for i in range(0, len(L), n):
        yield L[i:i+n]

exts = sorted((ext for ext in exts if len(ext['files']) > 0),
    key=lambda x: (-safeint(x.get('user_count')), x.get('name')))

files_count = sum(len(ext['files']) for ext in exts)

exts_groups = list(split_list(exts, 5000))

for i, group in enumerate(exts_groups):
	page = i + 1
	result = template.render(exts=group, exts_count=len(exts),
	    files_count=files_count, VIEW_SOURCE_URL=VIEW_SOURCE_URL,
	    now=datetime.datetime.now(), pages=len(exts_groups), page=page)
	name = 'pages/' + str(page) if page > 1 else 'index'
	open('../chrome-extensions-archive/{}.html'.format(name), 'w').write(result)
