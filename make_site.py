import json, datetime, os, glob
from jinja2 import Template
from tqdm import tqdm

from extstats.download_crx import DOWNLOAD_URL

from removal_requests import EXT_IDS as IDS_TO_AVOID_CRAWLING

from extstats import templates

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

exts = sorted((ext for ext in exts if len(ext['files']) > 0 and ext['ext_id'] not in IDS_TO_AVOID_CRAWLING and ext.get('name')),
    key=lambda x: (-safeint(x.get('user_count')), x.get('name')))
# exts = exts[:10]

files_count = sum(len(ext['files']) for ext in exts)

exts_groups = list(split_list(exts, 50000))

DEST = '../site/chrome-extensions-archive/'

TEST_ONE = False

if not TEST_ONE:
    for i, group in tqdm(enumerate(exts_groups)):
        page = i + 1
        name = ('pages/' + str(page) if page > 1 else 'index') + '.html'
        result = templates.list(exts=group,
            exts_count=len(exts),
            files_count=files_count,
            pages=len(exts_groups),
            total_size=total_size,
            name=name,
            page=page)
        open(DEST + name, 'w').write(result)

files = glob.glob(DEST + 'ext/*')
for f in files:
    os.remove(f)

for ext in tqdm(exts):
    result = templates.ext(ext=ext)
    open(DEST + 'ext/' + ext['ext_id'] + '.html', 'w').write(result)
