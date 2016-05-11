import os, json, datetime, arrow

from .CONSTS import PAGES_DIRECTORY


DIR = PAGES_DIRECTORY + '{id}/'
FILE = '{date}.json'

TO_RM = []

def latest_stored_sorted(ext_id):
    dirpath = DIR.format(id=ext_id)
    if os.path.exists(dirpath):
        files = os.listdir(dirpath)
        files_infos = []
        for file in files:
            time = arrow.get(file.replace('.json', ''))
            diff = time.datetime - datetime.datetime.now(datetime.timezone.utc)
            files_infos.append({
                'fullpath': os.path.join(dirpath, file),
                'name': file,
                'time': time,
                'diff': diff,
            })
        return list(reversed(sorted(files_infos, key=lambda x: x['time'])))

def is_404(latest):
    try:
        content = json.load(open(latest['fullpath']))
        latest['content'] = content
        if 'status' not in content and 'name' not in content:
            print('problem with', latest, ': no infos')
            STOPME
    except Exception as e:
        if len(open(latest['fullpath']).read().strip()) == 0:
            TO_RM.append('rm '+latest['fullpath'])
            # print(TO_RM); exiiit
            return False
        else:
            raise e
    return content.get('status', 200) == 404


def latest_good(ext_id):
    latests = latest_stored_sorted(ext_id)
    if latests:
        for i, version in enumerate(latests):
            if not is_404(version):
                version['deleted'] = i > 0
                return version


def latest_stored(ext_id):
    latests = latest_stored_sorted(ext_id)
    if latests:
        return latests[0]


# recent or 404
def is_stored_recent(ext_id):
    latest = latest_stored(ext_id)
    if latest:
        if is_404(latest):
            return True
        return latest['diff'].days == -1
    return False

def store_infos_history(ext_id, infos, date=None):
    if date is None:
        date = datetime.datetime.utcnow()
    data = date.isoformat()
    dirpath = DIR.format(id=ext_id)
    os.makedirs(dirpath, exist_ok=True)
    filepath = dirpath+FILE.format(date=date)
    json.dump(infos, open(filepath, 'w'), indent=2, sort_keys=True)

if __name__ == "__main__":
    print(is_stored_recent('fghfkeajhcmoohfcfmdkajambdcanmob'))
