### template engine
import html, types

def render(node):
    assert node is not None  # TODO: None => '' ?

    if type(node) in (tuple, list, types.GeneratorType):
        return ''.join(render(child) for child in node)

    if type(node) == str:
        return html.escape(node)

    children_rendered = ''
    if node.children:
        children_rendered = render(node.children)

    attrs_rendered = ''
    if node.attrs:
        # TODO: really, should I ignore the None values ?
        # TODO: class_, is_, ...
        attrs_rendered = ' ' + ' '.join(
            html.escape(key.replace('class_', 'class')) + '="' + html.escape(value) + '"'
            for key, value in node.attrs.items()
            if value is not None)

    if node.tag in ('br', 'img', 'hr'):
        assert not node.children
        return '<{tag}{attrs} />'.format(tag=node.tag, attrs=attrs_rendered)

    return '<{tag}{attrs}>{children}</{tag}>'.format(
        tag=node.tag, children=children_rendered, attrs=attrs_rendered)

class Node:
    def __init__(self, tag, attrs=None, children=None):
        assert tag
        self.tag = tag
        self.attrs = attrs
        self.children = children

    def __truediv__(self, children):
        if type(children) not in (tuple, list):
            children = (children,)
        self.children = children
        return self

    def __str__(self):
        return render(self)

class _H:
    def __getattr__(self, tag):
        return lambda **attrs: Node(tag, attrs)
H = _H()

### templates
import datetime, json

VIEW_SOURCE_URL = "/source/crxviewer.html?crx="

def _base(content='', title_prefix=''):
    return render(H.html() / (
      H.head() / (
        H.meta(charset="utf-8"),
        H.meta(content="width=device-width, initial-scale=1", name="viewport"),
        H.title() / (title_prefix + "Chrome Extensions Archive"),
        H.link(href="/style.css", media="screen", rel="stylesheet", type="text/css"),
      ),
      H.body() / (
        H.a(href='/') / (H.h1() / "Chrome Extensions Archive"),
        H.div(style='text-align: right') /
          H.a(href="https://github.com/mdamien/chrome-extensions-archive") /
            "github.com/mdamien/chrome-extensions-archive",
        H.hr(),
        content,
      ),
    ))

def _add_commas(n):
    return "{:,}".format(int(n))

def _sizeof_fmt(num):
    for unit in ['', 'Ko', 'Mo', 'Go', 'To']:
        if abs(num) < 1024.0:
            return "%3.1f%s" % (num, unit)
        num /= 1024.0
    return "%.1f%s" % (num, 'Yi')

def _nl2br(text):
    return ((t, H.br()) for t in text.split('\n') if t)

def _ext(ext):
    return (
        H.small(class_='extlink') / (
            H.a(href='/ext/%s.html' % ext['ext_id']) / ('#' + ext['ext_id'])),
        H.h2(id=ext['ext_id']) / (H.a(href=ext['url']) / ext['name']),
        H.small() / _add_commas(ext['user_count']),
        H.ul() / ((
            H.li() / (
                H.a(href=file['storage_url']) / (
                    file['name'].replace('.zip', ''),
                    ' - ',
                    H.small() / (' ', _sizeof_fmt(file['size'])),
                ),
                H.small() /
                    H.a(target='_blank', rel='noreferrer',
                            href=VIEW_SOURCE_URL + file['storage_url']),
            )
        ) for file in ext['files'])
    )

def list(exts, page, pages, name, exts_count, files_count, total_size):
    def _page(p):
        link = H.a(href='/' + name) / (' %d ' % p)
        if p == page:
            return H.strong() / link
        return link

    def _ext(ext):
        return (
            H.small(class_='extlink') / (
                H.a(href='/ext/%s.html' % ext['ext_id']) / ('#' + ext['ext_id'])),
            H.h2(id=ext['ext_id']) / (H.a(href=ext['url']) / ext['name']),
            H.small() / _add_commas(ext['user_count']),
            H.ul() / ((
                H.li() / (
                    H.a(href=file['storage_url']) / (
                        file['name'].replace('.zip', ''),
                        ' - ',
                        H.small() / (' ', _sizeof_fmt(file['size'])),
                    ),
                    H.small() /
                        H.a(target='_blank', rel='noreferrer',
                                href=VIEW_SOURCE_URL + file['storage_url']),
                )
            ) for file in ext['files'])
        )

    return _base((
        H.div(style="text-align: center") / (
            H.strong() / _add_commas(exts_count),
            ' extensions, ',
            H.strong() / _add_commas(files_count),
            ' versions, ',
            H.strong() / _sizeof_fmt(total_size),
            ' stored',
            H.br(),
            'Last update: ' + datetime.datetime.now().strftime('%Y-%m-%d'),
        ),
        H.div(style="text-align: center") / (
            'Pages:',
            *(_page(p) for p in range(1, pages)),
            '(ordered by # of users)'
        ),
        H.hr(),
        *(_ext(ext) for ext in exts),
    ))

def ext(ext):
    return _base((
        *_ext(ext),
        H.p(class_='description') / _nl2br(ext['full_description']),
        H.hr(),
        H.pre(class_='pprint') / json.dumps(ext, indent=2, sort_keys=True)
    ), title_prefix=ext['name'])
