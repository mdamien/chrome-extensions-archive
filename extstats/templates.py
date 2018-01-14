import datetime, json

from lys import L

VIEW_SOURCE_URL = "/source/crxviewer.html?crx="


def _add_commas(n):
    return "{:,}".format(int(n))


def _sizeof_fmt(num):
    for unit in ['', 'Ko', 'Mo', 'Go', 'To']:
        if abs(num) < 1024.0:
            return "%3.1f %s" % (num, unit)
        num /= 1024.0
    return "%.1f %s" % (num, 'Yi')


def _nl2br(text):
    return ((t, L.br()) for t in text.split('\n') if t)


def _base(content, title_prefix=''):
    return str(L.html / (
      L.head / (
        L.meta(charset="utf-8"),
        L.meta(content="width=device-width, initial-scale=1", name="viewport"),
        L.title / (title_prefix + "Chrome Extensions Archive"),
        L.link(href="/style.css", media="screen", rel="stylesheet", type="text/css"),
      ),
      L.body() / (
        L.a(href='/') / (L.h1 / "Chrome Extensions Archive"),
        L.div(style='text-align: right') / (
            L.a(href="https://github.com/mdamien/chrome-extensions-archive") /
                "github.com/mdamien/chrome-extensions-archive"
        ),
        L.hr,
        content,
      ),
    ))


def _ext(ext):
    return L.div / (
        L.small('.extlink') / (
            L.a(href='/ext/%s.html' % ext['ext_id']) /
                ('#' + ext['ext_id'])
        ),
        L.h2(id=ext['ext_id']) /
            (L.a(href=ext['url'] if ext['url'] else '') / ext['name']),
        L.small / _add_commas(ext['user_count']),
        L.ul / ((
            L.li / (
                L.a(href=file['storage_url']) / (
                    file['name'].replace('.zip', ''),
                    ' - ',
                    L.small / (' ' + _sizeof_fmt(file['size'])),
                ),
                ' ',
                L.small / (
                    L.a(target='_blank', rel='noreferrer',
                            href=VIEW_SOURCE_URL + file['storage_url']) /
                        'view source'
                ),
            )
        ) for file in ext['files'])
    )

def _simple_ext(ext):
    return L.div / (L.a(href='/ext/%s.html' % ext['ext_id']) / ext.get('name'))


def list(exts, page, pages, name, exts_count, files_count, total_size):
    def _page(p):
        name = ('pages/' + str(p) if p > 1 else 'index') + '.html'
        link = L.a(href='/' + name) / (' %d ' % p)
        if p == page:
            return L.strong / link
        return link

    return _base((
        L.div(style="text-align: center") / (
            L.strong / _add_commas(exts_count),
            ' extensions, ',
            L.strong / _add_commas(files_count),
            ' versions, ',
            L.strong / _sizeof_fmt(total_size),
            ' stored',
            L.br,
            'Last update: ' + datetime.datetime.now().strftime('%Y-%m-%d'),
        ),
        L.div(style="text-align: center") / (
            'Pages:',
            *(_page(p) for p in range(1, pages)),
            '(ordered by # of users)'
        ),
        L.hr,
        *(_simple_ext(ext) for ext in exts),
    ))

def ext(ext):
    return _base((
        _ext(ext),
        L.p('.description') / _nl2br(ext['full_description']),
        L.small / (
            'Are you the owner of the extension ?',
            L.a('.removal-request', href='mailto:crx-removal@dam.io?subject=Extension removal request&body=' + str(ext.get('ext_id')) + '%0A%0A%0Aproof you are the owner of this extension:') / 'request removal from crx.dam.io',
        ),
        L.hr,
        L.pre('.pprint') / json.dumps(ext, indent=2, sort_keys=True)
    ), title_prefix=ext['name']+ ' - ')

