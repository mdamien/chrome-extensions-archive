import json, datetime
from jinja2 import Template
from tqdm import tqdm

from extstats.download_crx import DOWNLOAD_URL

# jinja thing
from jinja2 import evalcontextfilter, Environment, FileSystemLoader, Markup, escape
import re

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

@evalcontextfilter
def add_commas(eval_ctx, value):
    return "{:,}".format(int(value))

@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n') \
        for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result
env = Environment(loader=FileSystemLoader('extstats'))
env.filters['add_commas'] = add_commas
env.filters['nl2br'] = nl2br
template = env.get_template('template.html')
template_ext = env.get_template('ext.html')



CRX2FF_URL = "https://crx2ff-yfrezangwq.now.sh"
VIEW_SOURCE_URL = "/source/crxviewer.html?crx="

exts = json.load(open('data/PAGES.json'))
print('enriched loaded')
crxs = json.load(open('data/crx_stats.json'))
print('file stats loaded')

total_size = 0

for ext in exts:
    ext_id = ext['ext_id']
    ext['files'] = list(reversed(crxs.get(ext_id, [])))
    total_size += sum([x['size'] for x in ext['files']])
    ext['download_link'] = DOWNLOAD_URL.format(ID=ext_id)
    ext['view_source'] = VIEW_SOURCE_URL+ext['download_link']
    for file in ext['files']:
        file['storage_url'] = "https://crx.dam.io/files/{ext_id}/{file}".format(
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

DEST = '../site/chrome-extensions-archive/'

TEST_ONE = False
#exts = exts[:10]

if not TEST_ONE:
    for i, group in tqdm(enumerate(exts_groups)):
        page = i + 1
        result = template.render(exts=group, exts_count=len(exts),
            files_count=files_count,
            VIEW_SOURCE_URL=VIEW_SOURCE_URL,
            CRX2FF_URL=CRX2FF_URL,
            now=datetime.datetime.now(),
            pages=len(exts_groups),
            total_size=total_size,
            page=page)
        name = 'pages/' + str(page) if page > 1 else 'index'
        open(DEST+name+'.html', 'w').write(result)


for ext in tqdm(exts):
    result = template_ext.render(ext=ext,
        VIEW_SOURCE_URL=VIEW_SOURCE_URL,
        CRX2FF_URL=CRX2FF_URL)
    name = 'ext/' + ext['ext_id']
    open(DEST+name+'.html', 'w').write(result)
