import os
import re
from os.path import exists as file_exists, isfile as isfile
from pathlib import Path
from shutil import copy as shcopy

from lxml import etree as etree
from printy import printy

from GlobVars import mod_data
from Settings_module import SVV as S


def get_searching_folders_with_reqires():
    """
    dict[Path, tuple]
    Возвращает словарь путей и требуемых модов для поиска.
    Формат возвращаемого значения:
    {
        'path1': ('mod1', 'mod2', ...),
        'path2': (),
        ...
    }

    Порядок загрузки:
    / -> Common -> 1.5
    """

    def no_LoadFolder_way():
        printy('\tNo loadFolders.xml - searching Common and versions folders', 'y>')

        pathes = {Path(''): ()}

        if file_exists('Common') and not isfile('Common'):
            pathes[Path('Common')] = ()

        versions = [fname for fname in os.listdir(".") if re.search(r"^\d+\.\d+$", fname) and os.path.isdir(fname)]
        print("\t  Version Folders: ", versions)
        if versions:
            if S.Delete_old_versions_translation:
                mv = max(versions, key=lambda v: tuple(map(int, v.split('.'))))
                print("\t  Max Version - ", mv)
                pathes[Path(mv)] = ()
                mod_data.max_version_by_folders = mv
            else:
                for v in versions:
                    pathes[Path(v)] = ()
        return pathes

    def LoadFolder_way():
        printy('\tloadFolders.xml found', 'y>')
        os.makedirs('_Translation', exist_ok=True)
        shcopy("loadFolders.xml", "_Translation/loadFolders.xml")



        with open('loadFolders.xml', 'r', encoding="utf-8") as lf:
            tree1 = etree.parse(lf)
        root1 = tree1.getroot()
        # Папки перевода from loadFolders.xml
        pathes: {str: ()} = {}
        """{Loadfolder path, (Required mods tuple)}"""


        etree.dump(root1)
        max_v: str = max([rim_version.tag for rim_version in root1 if not isinstance(rim_version, etree._Comment)])
        mod_data.max_version_by_Loadfolders = max_v

        def add_pathes_by_ver(ver_p: etree.Element, pathes: {str: ()}):
            for li in ver_p:  # type: etree.Element
                raw_path = li.text or ""
                normalized_path = Path(raw_path.strip("/\\"))

                r_mod = li.get('IfModActive')
                if r_mod is None:
                    req_mods = ()
                else:
                    req_mods = tuple(r_mod.split(', '))

                if file_exists(normalized_path) or normalized_path == '.':
                    if normalized_path not in pathes or req_mods == ():
                        pathes[normalized_path] = req_mods

        if S.Delete_old_versions_translation:
            add_pathes_by_ver(root1.find(max_v), pathes)
        else:
            for rim_version in root1:
                add_pathes_by_ver(rim_version, pathes)

        return pathes

    if not file_exists('loadFolders.xml'):
        pathes__ = no_LoadFolder_way()
    else:
        pathes__ = LoadFolder_way()

    printy('\tPathes to search: ', 'y>', end='')
    printy(
        f'Only newest verion - {S.Delete_old_versions_translation}',
        '<y')
    try:
        ml = max(len(str(key)) + 2 for key in pathes__)
        ml2 = max(len(str(*value)) + 2 for value in pathes__.values())
        print(f'\t\t|{"Path":^{ml}}', end="")
        print(f'| {"Requirement":^{ml2}} |')
        for a in pathes__:
            print(f'\t\t|{str(a):^{ml}}', end='')
            print(f'| {str(*pathes__[a]):^{ml2}} |' if pathes__[a] else f"| {'None':^{ml2}} |")
    except Exception as ex:
        print("Some printing error!?", ex)


    return pathes__
