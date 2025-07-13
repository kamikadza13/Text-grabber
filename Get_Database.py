import os
from pathlib import Path

import requests
from printy import printy

from Settings_module import SVV as S

sha_path = Path(S.SettingsPath.SettingsPath_AppData) / 'Settings' / 'Database' / 'sha.txt'
database_path = Path(S.SettingsPath.SettingsPath_AppData) / 'Settings' / 'Database' / 'steamDB.json'


def _get_sha():
    url = f"https://api.github.com/repos/RimSort/Steam-Workshop-Database/commits?path=steamDB.json&per_page=1"
    response = requests.get(url)
    response.raise_for_status()
    commit_data = response.json()
    if commit_data:
        latest_sha = commit_data[0]['sha']
        # print(f"Последний SHA для файла: {latest_sha}")
    else:
        print("Файл не найден или нет коммитов")
        return None

    return latest_sha


def _get_current_sha():
    try:
        with open(sha_path) as file:
            sha_text = file.read()
    except Exception as ex:
        sha_text = ''
    return sha_text


def _write_new_sha(sha_text):

    if not sha_path.exists():
        os.makedirs(sha_path.parent, exist_ok=True)

    with open(sha_path,'w') as file:
        printy("New SHA writed!")
        file.write(sha_text)


def _download_new_database():

    printy('Downloading new version of mod Database')

    download_url = f"https://raw.githubusercontent.com/RimSort/Steam-Workshop-Database/main/steamDB.json"
    file_content = requests.get(download_url).content
    return file_content

def _write_database(database):
    with open(database_path, 'wb') as f:  # 'wb' - запись в бинарном режиме
        f.write(database)
        printy("New Database writed - ", end='')
        print(database_path)

def compare_sha():
    new_sha = _get_sha()
    cur_sha = _get_current_sha()

    if new_sha == cur_sha:
        printy("Mods Database last version.")
        return

    _write_new_sha(new_sha)
    new_database = _download_new_database()
    _write_database(new_database)

