
# Chrome Extensions Archive: No updates since Feb 4. 2019
**In maintenance: disk is full ! (2 To)**

The goal is to provide a complete archive of the chrome web store with version
history.

You can see the current status of what's archived and download the files here:
[dam.io/chrome-extensions-archive/](http://dam.io/chrome-extensions-archive/)


## Installing the extensions

To install an extension, go to `chrome://extensions/` and drop the file.

To avoid the auto-update, [load it as an unpacked extension](http://stackoverflow.com/a/24577660/1075195)

Files are named as `.zip` but they are the exact same `.crx` stored on the store.

## Running the scripts

**scripts are python 3.5+ only**

Install dependencies: `pip3 install -r req.txt`

Create some folders and initialize some files:

```
mkdir data
mkdir crawled
mkdir crawled/sitemap
mkdir crawled/pages
mkdir crawled/crx
mkdir crawled/tmp
mkdir ../site
mkdir ../site/chrome-extensions-archive
mkdir ../site/chrome-extensions-archive/ext
echo "{}" > data/not_in_sitemap.json
```

Crawling:

- `crawl_sitemap.py`: gets you the list of all the extensions in `data/sitemap.json`
- `crawl_crx.py`: use `data/sitemap.json` to download the crx

Site & stats:

- `scan_pages_history_to_big_list.py`: makes `data/PAGES.json` by scanning the pages
you crawled
- `crx_stats.py`: makes `data/crx_stats.json` (what's currently stored)
- `make_site.py`: use `data/crx_stats.json` + `data/PAGES.json` to generate the site
- `make_json_site.py`: `data/crx_stats.json` + `data/PAGES.json` to generate JSON

Then I serve the files directly with nginx (see nginx.conf file for example)

## Helping out

I have a few things in mind for the future:

- diff of extensions versions as a web interface
- malware/adware analysis
- running an alternative web store (better search, firefox support,...)

Don't hesitate to reach out (here on issues, damien@dam.io or @dam_io on twitter)

To propose changes, just do a PR.

