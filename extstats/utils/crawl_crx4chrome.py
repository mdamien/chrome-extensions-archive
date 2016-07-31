import requests
import urllib.request
from bs4 import BeautifulSoup
import os, re
import shutil

DEST_DIR = 'crawled/crx4chrome/{ext_id}/'
DEST_FILE = '{dir}/{version}.zip'

from extstats.parse_infos import extract_manifest_of_file, parse_page

from termcolor import colored
def bad(x): return colored(x, 'red')
def good(x): return colored(x, 'green')
ok = print
# print = lambda *x: ''

TMP_FILE = 'crawled/tmp/tmp_crx_{ext_id}.zip'

def try_down_version(url):
    print(url)
    html = requests.get(url).text
    result = re.findall(r"https://chrome.google.com/webstore/detail/(.*)\?utm", html)
    if len(result) < 1:
        print(bad('no extensions at this url'))
        return
    ext_id = re.findall(r"https://chrome.google.com/webstore/detail/(.*)\?utm", html)[0]
    print('ext_id', ext_id)

    soup = BeautifulSoup(html, "lxml")
    link = soup.find('a', {'rel': 'nofollow'})
    href = link.attrs['href']
    print('storage url:', href)
    print(link.text, href)

    tmp_file = TMP_FILE.format(ext_id=ext_id)

    try:
        urllib.request.urlretrieve(href, tmp_file)
    except Exception as e:
        print(bad('fail to download crx:'), e)
        return

    manifest = None
    try:
        manifest = extract_manifest_of_file(tmp_file)
    except Exception as e:
        print(bad('bad download, parse of manifest failed'), e) 

    target_dir_path = DEST_DIR.format(ext_id=ext_id)

    if manifest and 'version' in manifest:
        version = manifest['version']
        print(good('manifest version:'), version)
        # current_version represent version_name so it can be different than the version stored
        target_file_path = DEST_FILE.format(dir=target_dir_path, version=version)
        if os.path.isfile(target_file_path):
            print(bad("file is already here, here's the version_name"),
                manifest.get('version_name'),
                'and .version=', manifest.get('version'))
            os.remove(tmp_file)
            return
        ok(good('version is added :D'), manifest['version'], url)
        # assert current_version == version_name or version
        os.makedirs(target_dir_path, exist_ok=True)
        shutil.move(tmp_file, target_file_path)
    else:
        try:
            os.remove(tmp_file)
        except OSError:
            pass
        except FileNotFoundError:
            pass

def crawl_version(url):
    print(url)
    c4c_id = url.split('/')[-2]
    try_down_version("http://www.crx4chrome.com/down/"+c4c_id+"/cdn/")

    """
    html = requests.get(url).text
    soup = BeautifulSoup(html, "lxml")
    download_links = soup.find_all('a', class_='spec')
    for link in download_links:
        href = link.attrs['href']
        if "/cdn" in href: # or "/crx/" in href:
            print(link.text)
            try_down_version("http://www.crx4chrome.com"+link.attrs['href'])
    """


"""
# wow, http://www.crx4chrome.com/history/0/ is very interresting
for i in range(2800):
    url = "http://www.crx4chrome.com/history/{i}".format(i=i)
    resp = requests.get(url)
    html = resp.text
    soup = BeautifulSoup(html, "lxml")
    history = soup.find(class_='history')
    if history:
        print(len(history))
        link = soup.find(id='tpcrn-breadcrumbs').find_all('a')[-1]
        href = link.attrs['href']
        ext_id = href.split('/')[-2]
        print(i, href, ext_id)
        #break
        for link in history.find_all('a'):
            print(link.text)
            crawl_version("http://www.crx4chrome.com"+link.attrs['href'])
"""

for i in range(6261, 40000):
    print('---', i, '---')
    try_down_version("http://www.crx4chrome.com/down/{i}/cdn/".format(i=i))
