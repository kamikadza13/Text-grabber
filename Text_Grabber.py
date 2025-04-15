# -*- coding: utf-8 -*-
import ctypes
import glob
import os
import re
import threading
import xml.etree.ElementTree as ET
from ctypes import windll
from dataclasses import dataclass
from os.path import exists as file_exists
from os.path import isfile as isfile
from pathlib import Path
from re import sub
from shutil import copy as shcopy
from shutil import copytree
from shutil import rmtree
from tkinter import Button
from tkinter import filedialog
from typing import Dict, Tuple

import lxml.etree as etree
import pyperclip
import ttkbootstrap
import ttkbootstrap as ttk_boot
import win32con
import win32gui
from lxml.etree import XMLParser
from pathvalidate import sanitize_filename
from printy import printy, escape as printy_escape
from ttkbootstrap.dialogs import Messagebox

import Check_New_Version
import Finalizing
import Patch_grabber
import Text_grabber_settings
import image_edit
from Finish_string_module import finish_string
from GlobFunc import xml_get_text
from GlobVars import SS
from GlobVars import folders
from GlobVars import mod_data
from GlobVars import state
from GlobVars import tf
from Patch_copy_module import find_patches_with_text
from text2 import add_elts_from_par
from text2 import find_parents_in_list_of_pathes
from text2 import parent_folders

Version_of_Text_grabber = "1.4.2"
Last_Rimworld_version = "1.5"

global exitString
global folder
global exitString1
global list_of_forbidden_character_in_label1


@dataclass
class FolderDefnamePathText:
    folder: str
    defname: str
    path: str
    text: str


def exit_prog():
    os._exit(0)
    Window_Text_grabber.destroy()


def escape_printy_string(string):
    return printy_escape(str(string))


#   Текст startwith через regex - значит нужно экранировать спец символы типа $

include_in_QOL = False
incompatibleWith_QOL = '''\n	<incompatibleWith>
		<li>kamikadza13qol.all</li>
	</incompatibleWith>'''
include_in_QOL_description = '''Перевод ~MOD_NAME~

Этот перевод включен в мой перевод кучи мелких QOL модов:
QOL rus
https://steamcommunity.com/sharedfiles/filedetails/?id=2791163039

Если вы заметили что-то не переведенное, то напишите об этом в комментариях под переводом ^_^

если поставите сборку переводов, то этот мод не нужен
(зайдите посмотрите, там много вкусного'''

dont_close_console_after_end = False


Error_log = []
Notification_log = []

Window_Text_grabber = ttkbootstrap.Window
Window_settings_app = ttkbootstrap.Window
New_Name = 'Default mod name'

from Settings_module import SVV as S
# S = Text_grabber_settings.SettingsValues




def reading_about():
    try:
        tree3 = etree.parse("About/About.xml")
        root3 = tree3.getroot()  #type: etree._Element

        def get_steam_id_PublishedFileId() -> str:
            try:
                path = Path('About') / 'PublishedFileId.txt'
                with open(path, 'r') as PublishedFileId:
                    steam_id = str(PublishedFileId.read())
                return 'https:/steamcommunity.com/sharedfiles/filedetails/?id=' + steam_id
            except Exception as ex:
                printy("Reading PublishedFileId.txt error", 'n')

                state.error_log.append(ex)
                return ''

        def get_supportedVersions():
            _ = root3.find("supportedVersions")
            b = ''
            max_ver = '1.5'

            if _ is not None:
                b = '\n'
                for a in _:
                    cur_ver = a.text
                    if cur_ver > max_ver:
                        max_ver = cur_ver
                    b += f'\t\t<li>{cur_ver}</li>\n'
                b += '\t'
            max_ver = 'v' + max_ver
            return b, max_ver

        def get_modDependencies():
            """dependence_dict[packageId]=
                       {'displayName': displayName,
                        'steamWorkshopUrl': steamWorkshopUrl,
                        'downloadUrl': downloadUrl,
                        'steamID': steamID}"""
            dependence_dict = {}
            dependencies_list = []
            for data in root3:
                if data.tag.lower() == "moddependencies":
                    dependencies_list = [li for li in data]
                elif data.tag.lower() == 'moddependenciesbyversion':
                    dependencies_list = [li for li in data[-1]]
            if dependencies_list:
                for dependence in dependencies_list:
                    packageId, displayName, steamWorkshopUrl, downloadUrl, steamID = '', '', '', '', ''
                    for a in dependence:
                        try:
                            if a.tag == 'packageId':
                                packageId = a.text
                            if a.tag == 'displayName':
                                displayName = a.text
                            if a.tag == 'steamWorkshopUrl':
                                steamWorkshopUrl = a.text
                            if a.tag == 'downloadUrl':
                                downloadUrl = a.text
                        except Exception as ex:
                            print("Error reading mod modDependencies:")
                            print(etree.tostring(a))

                    if steamWorkshopUrl:
                        b = re.search(r'.*steam.*?(\d{9,11})', steamWorkshopUrl)
                        if b:
                            steamID = b.group(1)
                    elif downloadUrl:
                        b = re.search(r'.*steam.*?(\d{9,11})', steamWorkshopUrl)
                        if b:
                            steamID = b.group(1)

                    if packageId:
                        dependence_dict[packageId] = {'displayName': displayName,
                                                      'steamWorkshopUrl': steamWorkshopUrl,
                                                      'downloadUrl': downloadUrl,
                                                      'steamID': steamID}
            return dependence_dict

        mod_data.name = xml_get_text(root3, 'name')
        mod_data.packageId = xml_get_text(root3, 'packageId')
        mod_data.author = xml_get_text(root3, 'author')

        mod_data.supportedVersions, mod_data.max_version = get_supportedVersions()
        mod_data.description = xml_get_text(root3, 'description')

        mod_data.url = get_steam_id_PublishedFileId()

        mod_data.modDependencies = get_modDependencies()





    except Exception as ex:
        printy("Reading About.xml error", 'n')
        state.error_log.append(ex)
        pass


def get_searching_folders_with_reqires():
    """
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

        max_v: str = max([rim_version.tag for rim_version in root1])
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


def get_defs_lang_patch_folders(fldrs: Dict[Path, Tuple]):
    """
        Получение Существующих путей к Def, Languages, Patches
        folders.def_folders
        folders.lang_folders
        folders.patches_folders
    """

    for path_obj in fldrs:
        try:
            defs_path = path_obj / 'Defs'
            lang_path = path_obj / 'Languages'
            patches_path = path_obj / 'Patches'

            if defs_path.is_dir():
                folders.def_folders.append(defs_path)

            if lang_path.is_dir():
                folders.lang_folders.append(lang_path)

            if patches_path.is_dir():
                folders.patches_folders[patches_path] = fldrs[path_obj]


        except PermissionError:
            print(f"Нет доступа к директории: {path_obj}")
        except FileNotFoundError:
            print(f"Директория не найдена: {path_obj}")


def get_Keyed_Strings_folders(folders_to_search: dict[Path, Tuple]):
    """folders.keyed_folders, folders.strings_folders"""

    def first_founded_lang(folder_: Path):
        """Return first language folder"""
        lang_sort_order_list = ['English', 'German', 'Polish', 'French', 'Spanish', 'PortugueseBrasilian',
                                'Spanish', 'Russian', 'ChineseTraditional', 'ChineseSimplified']
        folders1 = os.listdir(folder_)
        for lang in lang_sort_order_list:
            for ff in folders1:
                if ff.endswith(lang):
                    return folder_ / ff
        return None

    for lan in folders_to_search:
        founded_lang = first_founded_lang(lan)
        '1.5/Languages/English'
        if founded_lang:

            keyed_path = founded_lang / 'Keyed'
            if keyed_path.is_dir():
                folders.keyed_folders.append(keyed_path)

            strings_path = founded_lang / 'Strings'
            if strings_path.is_dir():
                folders.strings_folders.append(strings_path)


def make_files_path_to_translate(folders_: list[Path]):
    """{file path: new path}"""
    TranslatingFiles_ = {}
    for folder_path in folders_:
        printed_ = False
        for path, subdirs, files in os.walk(folder_path):
            folder_name = folder_path.name
            if 'DefInjected' in path:
                continue
            if files and not printed_:
                printed_ = True
                printy(f'\t\t\t{escape_printy_string(folder_path)}:', '<y')
            for file in files:

                if file.endswith('.xml') or (folder_name == 'Strings' and file.endswith('.txt')):
                    printy(f'\t\t\t\t{escape_printy_string(os.path.join(path, file))}')
                    match folder_name:
                        case "Keyed":
                            np = Path('_Translation') / str(folder_path).partition('Languages\\')[0] / 'Languages' / S.Game_language / 'Keyed'
                        case "Strings":
                            lang_replace = sub(r"(.*Languages\\).+?(\\.*)", r'\1' + S.Game_language + r'\2', path)
                            np = Path('_Translation') / lang_replace
                        case "Patches":
                            np = Path('_Translation') / "Copied_patches" / folder_path.parent
                        case "Defs":
                            np = Path('_Translation') / folder_path.parent / 'Languages' / S.Game_language / 'DefInjected'
                        case 'Grabbed_Defs_from_patches':
                            np = Path('_Translation') / folder_path.parent / 'Languages' / S.Game_language / 'DefInjected'
                        case _:
                            np = Path('_Translation') / folder_path.parent / 'Languages' / S.Game_language / 'SomeThingGoesWrong?'

                    TranslatingFiles_[Path(path) / file] = np
    return TranslatingFiles_



def patches():
    def get_database_path():
        database_path1 = ''
        if S.Path_to_Mod_folder:
            printy('\t\t\t\t[n>]Try get Mod Database into Steam mods folder:@', end="")
            database_path1 = Path(S.Path_to_Mod_folder) / '1847679158/db/db.json'
            printy(f'[<n] -> {escape_printy_string(database_path1)}@')

        if not os.path.exists(database_path1):
            printy('\t\t\t\t[n>]No Mod Database - get file from Textgrabber folder@')
            database_path1 = state.prog / 'db.json'
        else:
            printy('\t\t\t\t[n]Mod Database Founded@')
        return database_path1

    if folders.patches_folders:

        printy(f'\t\tTry grab Defs from patches into "_Translation/Grabbed_Defs_from_patches"', 'n')

        database_path = get_database_path()

        patches_file_count = 0
        for pf in folders.patches_folders:
            Patch_grabber.main(patches_folder=pf,
                               folder_required_mods=folders.patches_folders[pf],
                               tags_to_extract=S.Tags_to_extraction,
                               database_path=database_path)

        "Получили state.mods_folders"

        if state.keyed_from_patches:
            for file in state.keyed_from_patches:
                path = Path(
                    '_Translation') / 'From_patches' / 'No mods required' / 'Languages' / S.Game_language / 'Keyed'
                os.makedirs(path, exist_ok=True)

                li_elem = f'<li>From_patches/No mods required</li>\n\t\t'
                if li_elem not in state.new_loadfolder_pathes:
                    state.new_loadfolder_pathes.append(li_elem)
                new_name = str(file.stem) + str(patches_file_count) + str(file.suffix)
                patches_file_count += 1
                new_path = path / new_name
                with open(new_path, "w", encoding="utf-8") as new_patch_file:
                    patches_file_count += 1
                    new_patch_file.write("<LanguageData>\n")
                    for line in state.keyed_from_patches[file]:
                        new_patch_file.write("\t" + line + "\n")
                    new_patch_file.write(r"</LanguageData>")


        # from pprint import pprint
        # pprint(state.mods_folders, sort_dicts=False, width=200)
        '''
        -----{
        -----(req mods): 
        ---------{Path:
        ------------text1, text2]
        ---------}
        -----}
        '''
        # print('state.mods_folders:', state.mods_folders)
        for mf in state.mods_folders:
            # print('mf: ', mf)
            # print(state.mods_folders[mf])
            mod_folder_name_req_from_tuple = sub('[^0-9a-zA-Z]+', '_', str(mf[0])) if mf else ""
            new_grabbed_folder_path = Path('_Translation') / 'Grabbed_Defs_from_patches' / mod_folder_name_req_from_tuple
            # print(new_grabbed_folder_path)
            os.makedirs(new_grabbed_folder_path, exist_ok=True)

            for filepath in state.mods_folders[mf]:

                new_file_path = new_grabbed_folder_path / str(filepath.stem + str(patches_file_count) + filepath.suffix)
                with open(new_file_path, "w", encoding="utf-8") as new_patch_file:
                    patches_file_count += 1
                    new_patch_file.write("<Defs>\n")

                    if mf:
                        new_patch_file.write(f'<!-- {list(mf)} -->\n')

                    for l1 in state.mods_folders[mf][filepath]:
                        new_patch_file.write(l1)
                    new_patch_file.write("\n</Defs>")

                    new_modfold_name_req_from_tuple = mod_folder_name_req_from_tuple if mod_folder_name_req_from_tuple else "No mods required"

                    np = Path(
                        '_Translation') / 'From_patches' / new_modfold_name_req_from_tuple / 'Languages' / S.Game_language / "DefInjected"

                    folders.patches_defs[new_file_path] = np

                    loadfolder_path = Path('From_patches') / new_modfold_name_req_from_tuple

                    if mf:
                        li_elem = f'<li IfModActive="{mf[0]}">{loadfolder_path.as_posix()}</li>\n\t\t'
                    else:
                        li_elem = f'<li>{loadfolder_path.as_posix()}</li>\n\t\t'

                    if li_elem not in state.new_loadfolder_pathes:
                        state.new_loadfolder_pathes.append(li_elem)

        printy(f'\t\tPatches in: {escape_printy_string(folders.patches_folders)}', 'o')
        printy('\t\tFiles in Patches:', 'o')
        folders.patches_pathes = make_files_path_to_translate(list(folders.patches_folders))
        # print('folders.patches_pathes')
        # for a in folders.patches_pathes:
        #     print(a, folders.patches_pathes[a])


def main(Inputed_path_to_mod="", Floodgauge: ttk_boot.Floodgauge = ttk_boot.Floodgauge):
    def is_version(string: str):
        return string.replace(".", "0").isdecimal()

    def change_to_mod_dir(Inputed_path_to_mod_2: str):

        if Inputed_path_to_mod_2 == "":
            folder_selected = os.path.normpath(filedialog.askdirectory(title="Select MOD folder"))
            if not folder_selected or folder_selected == ".":
                exit_prog()
            Fullpath = Path(folder_selected)
        else:
            Fullpath = Path(Inputed_path_to_mod_2)

        SS.p_full = Fullpath
        SS.p_name = Fullpath.name
        SS.p_root = Fullpath.parent
        printy(f'\tWork directory: "{SS.p_full}", Mod folder: {SS.p_name}', 'n')

        os.chdir(SS.p_full)

    change_to_mod_dir(Inputed_path_to_mod)

    Window_Text_grabber.Enter_textbox.delete(0, 'end')
    Window_Text_grabber.Enter_textbox.insert(0, SS.p_full)
    rmtree('_Translation', ignore_errors=True)
    rmtree('__Defs_from_patches', ignore_errors=True)
    rmtree('__Keyed_from_patches', ignore_errors=True)

    printy("Reading About.xml and PublishedFileId.xml", 'n')
    reading_about()

    printy('Searching pathes to root folders', 'n')
    folders.searching_pathes = get_searching_folders_with_reqires()
    """{'Path(path1)': (reqired_mods,)}"""

    printy('Searching pathes Defs, Languages, Patches folders', 'n')
    get_defs_lang_patch_folders(folders.searching_pathes)
    """Получение Существующих путей к Def, Languages, Patches"""

    printy('Searching pathes Keyed, Strings folders', 'n')
    get_Keyed_Strings_folders(folders.lang_folders)

    # printy('\tSearching Defs, Keyed, Strings, Patches, Languages', 'y>')

    delete_folders = []

    patches()
    print()


    if folders.def_folders:
        printy(f'\t\tDefs in: {escape_printy_string(folders.def_folders)}', 'o')
        printy('\t\tFiles in Defs:', 'o')
        tf.Defs = make_files_path_to_translate(folders.def_folders)

    if folders.keyed_folders:
        printy(f'\t\tKeyed in: {escape_printy_string(folders.keyed_folders)}', 'o')
        printy('\t\tFiles in Keyed:', 'o')
        tf.Keyed = make_files_path_to_translate(folders.keyed_folders)

    if folders.strings_folders:
        printy(f'\t\tStrings in: {escape_printy_string(folders.strings_folders)}', 'o')
        printy('\t\tFiles in Strings:', 'o')
        tf.Strings = make_files_path_to_translate(folders.strings_folders)

    # if patches_defs_pathes:
    #     print("Patches Defs ", list(patches_defs_pathes))
    #     print('tf.Defs.update(patches_defs_pathes)')
    #     print(tf.Defs)
    #     tf.Defs.update(patches_defs_pathes)
    #     print(tf.Defs)

    # tf.Patches = make_files_path_to_translate([Path('_Translation/Grabbed_Defs_from_patches')])

    if folders.patches_defs:
        # print("Patches Defs ", list(folders.patches_defs))
        tf.Defs.update(folders.patches_defs)
        # print(tf.Defs)


    print()




    # find_parent_elems_in_file_path_list(tf.Defs)


    Floodgauge['value'] = 10
    printy("Searching parents", 'n')

    'Add translated mod parents pathes'
    parent_xml_pathes = [d for d in tf.Defs]
    """List of parent pathes"""

    'Add Data parents pathes'
    parent_xml_pathes.extend([a for a in Path(S.Path_to_Data).glob('*/Defs/**/*.xml')])


    printy("Searching parents... Done ", 'n')
    print()
    Floodgauge['value'] = 20

    printy("Finding defs in parents", 'n')
    parent_mod_pathes_dict = parent_folders(S.Path_to_Mod_folder, S.Path_to_Another_folder)
    """{ PackageID : Path }"""
    if parent_mod_pathes_dict:
        for mod_path in parent_mod_pathes_dict.values():
            parent_xml_pathes.extend([a for a in mod_path.rglob('*.xml') if 'Defs' in a.parts])
    printy("Finding defs in parents... Done ", 'n')
    print()



    printy("Updating parent dict ", 'n')
    tf.Parent_list = find_parents_in_list_of_pathes(parent_xml_pathes)
    """{name: elem}"""
    printy("Updating parent dict... Done ", 'n')


    Floodgauge['value'] = 30

    print()



    printy('Writing Files...', 'c')


    # print(tf.Defs.keys())
    for fl_idx, fil in enumerate(tf.Defs):
        try:
            Floodgauge['value'] = 30 + int(60 * (fl_idx / len(tf.Defs)))

            # print("     Чтение из ", str(fil))
            with open(fil, 'r', encoding="utf-8", errors='ignore') as xml_file:
                tree = ET.parse(xml_file)
            # tree = ET.parse(fil)
            root = tree.getroot()

            # print("Добавление элементов из родителей")

            def adding_elems_into_root_by_Parent_elem(root: etree.Element):

                for r in root:  #type: etree.Element

                    # xml.etree.ElementTree.dump(r)
                    ParentName = r.get('ParentName')
                    if ParentName is None:
                        continue
                    if ParentName not in tf.Parent_list:
                        print("Не найден родитель", ParentName)

                        continue
                    if r.tag != tf.Parent_list[ParentName].tag:
                        if S.Game_language == "Russian":
                            Error_log.append(f"Файл: {fil}\n"
                                             f"Класс родителя отличается от Класса наследника\n"
                                             f"{r.tag} {r.attrib} and {tf.Parent_list[ParentName].tag} {tf.Parent_list[ParentName].attrib}\n"
                                             f"Это не критическая ошибка. Но, возможно, придется переместить файл в папку, соответствующую классу родителя\n")
                        else:
                            Error_log.append(f"File: {fil}\n"
                                             f"The class of the parent differs from the class of the heir\n"
                                             f"{r.tag} {r.attrib} and {tf.Parent_list[ParentName].tag} {tf.Parent_list[ParentName].attrib}\n"
                                             f"That is not critical error. But you may have to move the file to the folder corresponding to the parent class.\n")

                    # print(f"Добавляются элементы {[x.tag for x in tf.Parent_list[ParentName]]} в:")
                    # ET.dump(r)


                    add_elts_from_par(r, tf.Parent_list[ParentName], change_current_bool=True)

                    # for elements_in_parent_Def in reversed([j for j in tf.Parent_list[ParentName]]):
                    #     adding_elems(r, elements_in_parent_Def)
                    # print(f"Рут после добавления:")
                    # ET.dump(r)
                    # print(f"{r.tag}.{r.attrib}")

            adding_elems_into_root_by_Parent_elem(root)

            FDPT, XmlExtensions_Keyed = finish_string(tree)

            # print('FDPT:')
            # print(FDPT)

            from Finish_string_module import FolderDefnamePathText
            FDPT: list[FolderDefnamePathText]
            """    
            folder: str
            defname: str
            path: str
            text: str
            """

            if not FDPT:
                continue

            # print('FDPT:', FDPT)
            Folders = set([e.folder for e in FDPT])

            if FDPT:
                # print()
                printy(f"File:               [y>]{escape_printy_string(fil)}@")

            # print("Начало разбивания файла на папки")
            for folder_idx, fldr in enumerate(Folders):
                # print('f1', fldr)
                # print('fil', fil)
                # print('tf.Defs', tf.Defs[fil])




                file_path1 = tf.Defs[fil] / fldr
                # printy(f"{file_path1=}")

                if S.Not_rename_files:
                    nn = fil.stem
                    np = (tf.Defs[fil] / fldr / nn).with_suffix('.xml')

                else:
                    nn = fil.stem + "_" + fldr.rpartition('.')[2].rpartition('_')[2]
                    np = (tf.Defs[fil] / fldr / nn).with_suffix('.xml')

                if len(str(np.resolve())) > 240:
                    nn = fil.stem.rpartition(".")[2].rpartition("_")[2] + str(fl_idx) + "_" + str(folder_idx)
                    np = (tf.Defs[fil] / fldr / nn).with_suffix('.xml')


                printy(
                    f'Folder: [y<]{escape_printy_string(fldr): <28}@ --> [<y]{str(np).partition("_Translation")[2]}@')

                if file_exists(np):
                    with open(np, "r", encoding="utf-8") as Write_file:
                        old_txt = Write_file.read()
                    text_start = old_txt.replace('\n</LanguageData>', '')
                else:
                    if S.Adding_xml_version_encoding_string_ckeckbtn:
                        text_start = '<?xml version="1.0" encoding="utf-8"?>\n<LanguageData>'
                    else:
                        text_start = '<LanguageData>'


                text_body = []
                text_end = '</LanguageData>'

                if S.Add_filename_comment:
                    text_body.append(f"<!-- {str(fil)} -->")

                add_new_line_at_new_defname_Boolean = True
                last_defname = ''

                if S.Add_new_line_next_defname:
                    last_defname = FDPT[0].defname
                    defnames = set(elem.defname for elem in FDPT)
                    if S.Add_new_line_next_defname_treshhold:
                        if (len(defnames) / len(FDPT)) <= 0.6:
                            add_new_line_at_new_defname_Boolean = True
                        else:
                            add_new_line_at_new_defname_Boolean = False

                for elem in FDPT:

                    if elem.folder == fldr:

                        if S.Add_new_line_next_defname:
                            if add_new_line_at_new_defname_Boolean:
                                if last_defname != elem.defname:
                                    text_body.append('')
                                    last_defname = elem.defname

                        if S.Add_comment:
                            # _ = f2[1]   #.replace('\n', '\\n')
                            _ = elem.text.replace('\n', '***_new_n_new_***')
                            while "--" in _:
                                _ = _.replace("--", "-")

                            lenth_of_path = len(f'<{elem.defname}.{elem.path}>') - 5

                            if S.Comment_add_EN:
                                lenth_of_path -= 4

                            comm_spacing = ''
                            if S.Comment_starting_similar_as_ogiganal_text:
                                comm_spacing = " " * lenth_of_path
                            if "<li>" in _:
                                comm_spacing = ''

                            if S.Comment_spacing_before_tag:
                                com_sp_before = comm_spacing
                                comm_spacing = ''
                            else:
                                com_sp_before = ''

                            comm = f'{com_sp_before}<!--{comm_spacing} {"EN: " if S.Comment_add_EN else ""}{elem.text} -->'.replace(
                                '***_new_n_new_***', '\n')
                            if S.Comment_replace_n_as_new_line:
                                comm = comm.replace('\\n', '\n')

                            text_body.append(comm)
                        text_body.append(f"<{elem.defname}.{elem.path}>{elem.text}</{elem.defname}.{elem.path}>")

                os.makedirs(file_path1, exist_ok=True)

                with open(np, "w", encoding="utf-8") as Write_file:
                    Write_file.write(f"{text_start}\n")
                    for idx, line in enumerate(text_body):
                        Write_file.write(f"{S.tags_left_spacing_dict[S.tags_left_spacing]}{line}\n")

                    Write_file.write(f"{text_end}")

                # print("     End of Folder       ")
                # print("----------------------------")

            if XmlExtensions_Keyed:
                Keyed_path = Path('_Translation') / 'Languages' / S.Game_language / 'Keyed' / fil.stem.rpartition("\\")[2] + fil.suffix
                printy(
                    f"Founed  XmlExtensions.SettingsMenuDef -> [<y]Creating Keyed file:@ [y]{escape_printy_string(str(Keyed_path))}")
                Keyed_path.parent.mkdir(parents=True, exist_ok=True)
                with open(Keyed_path, 'w', encoding='utf-8') as Keyed:
                    if S.Adding_xml_version_encoding_string_in_Keyed:
                        Keyed.write(r'<?xml version="1.0" encoding="utf-8"?>')
                        Keyed.write('\n')

                    Keyed.write('<LanguageData>\n')

                    for i in XmlExtensions_Keyed:
                        Keyed.write(f"\t<{i[0]}>{i[1]}</{i[0]}>\n")
                    Keyed.write('\n</LanguageData>')

            # print('\n'.Folder_and_text_1[0])
            # print('\n'.join(Folder_and_text_1[1]))
        except ET.ParseError:
            Error_log.append(
                "Ошибка чтения " + str(fil) + "\n\n")

            print("Пропуск файла")
            # input("Press Enter to continue")
            print("--------------------------------------")
            pass

    printy("Writing Files... Done", 'c')
    print()

    printy("Processing Keyed", 'n')
    for p, np in tf.Keyed.items():
        os.makedirs(np, exist_ok=True)
        print("Copy", p, " in ", np)
        shcopy(p, np)
    printy("Processing Keyed... Done", 'n')
    print()

    printy("Processing Strings", 'n')
    for p, np in tf.Strings.items():
        os.makedirs(np, exist_ok=True)
        print("Copy", p, " in ", np)

        shcopy(p, np)
    printy("Processing Strings... Done", 'n')
    print()

    if S.Copy_original_patches is True:
        printy("Processing copy patches with text", 'n')
        # print('patches_pathes:', folders.patches_pathes) # Заменил patches_folders на patches_pathes
        find_patches_with_text(folders.patches_pathes, Tags_to_extraction=S.Tags_to_extraction)
        printy("Processing copy patches with text... Done", 'n')
        print()

    root2 = '_Translation'

    # raise Exception

    def remove_empty_folders(path):
        """Рекурсивно удаляет все пустые папки, начиная с указанного пути."""
        if not os.path.isdir(path):
            return False  # Если это не папка, пропускаем

        # Получаем список всех элементов в папке
        entries = os.listdir(path)

        # Рекурсивно проверяем все подпапки
        has_non_empty = False
        for entry in entries:
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):
                if remove_empty_folders(full_path):  # Если подпапка не пуста
                    has_non_empty = True

        # Если папка пуста, удаляем её
        if not has_non_empty and not entries:
            print(f"Удаление пустой папки: {path}")
            os.rmdir(path)
            return False
        return True  # Папка не пуста


    try:
        remove_empty_folders(root2)
    except Exception as ex:
        printy(r'[r]\[ERROR\]@ delete_empty_folders', predefined='<m')
        Error_log.append(f"Error delete_empty_folders {ex} \n\n")
    Floodgauge['value'] = 90

    if S.Delete_old_versions_translation:
        try:
            printy("Delete old versions", 'n')
            folders_in__translation = glob.glob("_Translation\\*\\", recursive=False)
            folders_name_in__translation = [sub('_Translation\\\\(.*)\\\\', '\\1', i) for i in folders_in__translation]
            versions_name_in__translation = [i for i in folders_name_in__translation if is_version(i)]
            if versions_name_in__translation:
                max_version = max(versions_name_in__translation)
                for version in versions_name_in__translation:
                    if version != max_version:
                        version = str(version)
                        rmtree(f"_Translation\\{version}")
            printy("Delete old versione... Done", 'n')
            print()


        except Exception as ex:
            printy(r"[r]\[ERROR\]@ Delete old versions", predefined='<m')
            print()
            Error_log.append(f"Error Delete_old_versions_translation {ex} \n\n")


    if S.Merge_folders:
        printy("Merge folders", 'n')

        # folders_in__translation = glob.glob("_Translation/*/", recursive=False)
        # folders_name_in__translation = [sub('_Translation\\\\(.*)\\\\', '\\1', i) for i in folders_in__translation]
        # versions_name_in__translation = [float(i) for i in folders_name_in__translation if is_version(i)]

        if file_exists("_Translation\\Languages"):
            try:
                with os.scandir('_Translation') as scandir:
                    versions_name_in__translation = [entry.name for entry in scandir if
                                                     (entry.is_dir() and is_version(entry.name))]

                if len(versions_name_in__translation) == 1:
                    versions_name_in__translation = versions_name_in__translation[0]
                    if file_exists(f"_Translation\\{versions_name_in__translation}\\Languages"):
                        copytree(f"_Translation\\{versions_name_in__translation}\\Languages", "_Translation\\Languages",
                                 dirs_exist_ok=True)
                        rmtree(f"_Translation\\{versions_name_in__translation}\\Languages")
            except Exception as ex:
                Error_log.append(f"Error Merge_folders {ex} \n\n")
                printy(fr"[r]\[ERROR\]@ Merge_folders {escape_printy_string(str(ex))} \n\n", predefined='<m')
                print()
        printy("Merge folders... Done", 'n')
        print()

    def Rename_Keyed_files():
        try:
            if file_exists("About\\About.xml"):
                tree3 = ET.parse("About\\About.xml")
                name_of_mod = tree3.getroot().find("name").text.replace(" ", "_")
                name_of_mod = "".join(x for x in name_of_mod if x.isalnum())
                for path, subdirs, files in os.walk(f'_Translation'):
                    for name in files:
                        if path.rpartition("\\")[2] == "Keyed":
                            newName = f"{name_of_mod}_Keyed_{name}"
                            os.rename(os.path.join(path, name), os.path.join(path, newName))
        except Exception as ex:
            Error_log.append(f"Error Rename_Keyed_files {ex} \n\n")
            printy(fr"[r]\[ERROR\]@ Rename_Keyed_files {escape_printy_string(str(ex))} \n\n", predefined='<m')

    if not S.Not_rename_files:
        Rename_Keyed_files()

    if S.Add_comment:
        printy("Add Comments into Keyed", 'n')
        parser_no_delete_comments = XMLParser(remove_comments=False, remove_blank_text=False, remove_pis=True)
        for path, subdirs, files in os.walk(f'_Translation'):
            for name in files:
                # if path.rpartition("\\")[2] == "Keyed":
                if "\\Keyed\\" in os.path.join(path, name):
                    # try:
                    with open(f"{path}\\{name}", encoding='utf-8') as Keyed_file:
                        tree = etree.parse(Keyed_file, parser_no_delete_comments)
                        root = tree.getroot()
                        root.text = f'\n{S.tags_left_spacing_dict[S.tags_left_spacing]}'

                        for line in root:
                            # input(line.text + f' tail = {line.tail.encode()}')
                            if line.tag is not etree.Comment:
                                try:
                                    a = etree.Comment(
                                        f' {"EN: " if S.Comment_add_EN else ""}{line.text.replace("--", "-")} ')
                                    a.tail = f'\n{S.tags_left_spacing_dict[S.tags_left_spacing]}'
                                    line.addprevious(a)
                                except Exception as ex:
                                    print(ex, "Error comment adding:", line.text)

                            else:
                                a = line.getprevious()
                                if a is not None and a.tail is not None:
                                    a.tail = '\n' * (a.tail.count('\n')) + f'\t\t'
                                else:
                                    root.text = '\n' + f'\t\t'
                            if line.tail is not None:
                                line.tail = '\n' * (line.tail.count('\n')) + f'{S.tags_left_spacing_dict[S.tags_left_spacing]}'
                            else:
                                line.tail = '\n' + f'{S.tags_left_spacing_dict[S.tags_left_spacing]}'

                        try:
                            root[-1].tail = '\n'
                        except IndexError:
                            printy("[r]\tIndex Error at {path}\\{name}")


                    with open(f"{path}\\{name}", "wb") as Keyed_file:
                        if S.Adding_xml_version_encoding_string_in_Keyed:
                            Keyed_file.write(bytes('<?xml version="1.0" encoding="utf-8" ?>\n', encoding='utf8'))
                        Keyed_file.write(etree.tostring(root, encoding="utf-8"))
                    # except Exception as ex:
                    #     warning("Bad Keyed Comment adding" + str(ex))
                    #     Error_log.append("Bad Keyed Comment adding" + str(ex))
        printy("Add Comments into Keyed... Done", 'n')
        print()

    global New_Name

    if file_exists('About\\About.xml'):

        def make_about_folder():
            global New_Name
            printy('Make About folder', 'n')
            s1_path = "About\\preview.png"
            d_path = "_Translation\\About"

            def get_steam_id_PublishedFileId() -> str:
                try:
                    path = 'About\\PublishedFileId.txt'
                    with open(path, 'r') as PublishedFileId:
                        steam_id = PublishedFileId.read()
                    return 'https:/steamcommunity.com/sharedfiles/filedetails/?id=' + steam_id
                except Exception as ex:
                    return ''

            os.makedirs(d_path, exist_ok=True)
            if file_exists(s1_path):
                shcopy(s1_path, d_path)
            tree3 = ET.parse("About\\About.xml")
            root3 = tree3.getroot()

            mod_url = f'{get_steam_id_PublishedFileId()}'

            def get_supportedVersions():
                _ = root3.find("supportedVersions")
                b = ''
                if _:
                    b = '\n'
                    for a in _:
                        b += f'\t\t<li>{a.text}</li>\n'
                    b += '\t'
                return b

            name = root3.find("name").text
            description = root3.find("description")
            if description is not None:
                if description.text is not None:
                    description = description.text
                else:
                    description = ""
            else:
                description = ""
            packageId = root3.find("packageId").text
            New_Name = S.New_Name.replace("~MOD_NAME~", name)
            supportedVersions = get_supportedVersions()

            if len(S.Author + "." + packageId) > 60:
                if len(S.Author + "." + packageId.partition(".")[0]) > 60:
                    New_packageId = "NEED_LESS_60_SYMBOLS.ERROR"
                else:
                    New_packageId = S.Author.replace(" ", "") + "." + packageId.partition(".")[0]
            else:
                New_packageId = S.Author.replace(" ", "") + "." + packageId
            modDependencies = f"""
		<li>
			<packageId>{packageId}</packageId>
			<displayName>{name}</displayName>
			<steamWorkshopUrl>{mod_url}</steamWorkshopUrl>
		</li>""" if S.Add_mod_Dependence else ""
            if include_in_QOL:
                new_desc = include_in_QOL_description.replace("~MOD_NAME~", name).replace("~MOD_DESCRIPTION~",
                                                                                          description).replace(
                    "~MOD_URL~", mod_url)
            else:
                new_desc = S.Description.replace("~MOD_NAME~", name).replace("~MOD_DESCRIPTION~", description).replace(
                    "~MOD_URL~", mod_url)
            about_text = f'''<ModMetaData>
	<name>{New_Name}</name>
	<author>{S.Author}</author>
	<packageId>{New_packageId}</packageId>
	<supportedVersions>{supportedVersions}</supportedVersions>
	<modDependencies>{modDependencies}
	</modDependencies>
	<loadAfter>
		<li>{packageId}</li>
	</loadAfter>{incompatibleWith_QOL if include_in_QOL else ''}
	<description>{new_desc}</description>
</ModMetaData>'''

            with open('_Translation\\About\\About.xml', "w", encoding='utf-8') as f:
                f.write(about_text)
            printy('Make About folder... Done', 'n')
            print()

        make_about_folder()
        if S.Image_on_Preview:
            image_edit.main(str(state.prog / "Images/Preview/New_Image.png"),
                            S.Preview_Position,
                            S.Preview_Offset_x, S.Preview_Offset_y)

    try:
        remove_empty_folders(root2)
    except Exception as ex:
        Error_log.append(f"Error delete_empty_folders {ex} \n\n")
        printy(fr"[r]\[ERROR\]@ delete_empty_folders {escape_printy_string(str(ex))} \n\n", predefined='<m')



    def loadfolder_check_folders():
        """
        Проверка loadFolders на наличие папок
        """

        def exist():
            printy("Loadfolder.xml remove empty folders...", 'n')

            with open('loadFolders.xml', 'r', encoding="utf-8") as xml_file:
                tree1 = ET.parse(xml_file)
            root1 = tree1.getroot()
            max_v = "1.0"

            if state.new_loadfolder_pathes:
                printy("\t[o>]Add patches_defs_folders into Loadfolder@")
                print("\t\t", end='')
                for lf in state.new_loadfolder_pathes:
                    printy(escape_printy_string(lf), "o", end="")
                for vv in root1:
                    vv[-1].tail = '\n\t\t'
                    for lii in state.new_loadfolder_pathes:
                        el = ET.fromstring(lii)
                        el.tail = '\n\t\t'
                        vv.append(el)
                    else:
                        vv[-1].tail = "\n\t"


            for v in root1:
                try:
                    v_cur = v.tag.replace('v', '')  # "v1.5 -> 1.5"
                except Exception as ex:
                    print("Bad Loadfolder version - > Check loadfolder.xml")
                    v_cur = "1.0"
                if max_v < v_cur:
                    max_v = v_cur

            printy(f'   Max version [r]{escape_printy_string(max_v)}@')


            for v in reversed(root1):
                v_cur = v.tag[1:]
                for li in reversed(v):
                    if li.text == str(v.tag[1:]):
                        if S.Delete_old_versions_translation:
                            li.text = str(max_v)
                    if li.text == "/":
                        pass
                    elif li.text is not None:
                        try:

                            if S.Delete_old_versions_translation:
                                if v_cur == li.text.partition("\\")[0]:
                                    li.text = li.text.replace(str(v_cur), str(max_v))
                        except ValueError:
                            pass
                        if not file_exists("_Translation\\" + li.text):
                            # printy(f"   Not need folder [<y]{escape_printy_string(li.text)}@ --> Removing")
                            v.remove(li)

            def is_li_empty(li):
                return li.text is None or li.text.strip() == ''

            # Поиск и удаление всех пустых элементов <li>
            remove_li_list = []
            for v in root1:
                for li in v:

                    if is_li_empty(li):
                        print('Пустой ли')
                        remove_li_list.append((v,li))
            for v, li in remove_li_list:
                v.remove(li)

            tree1.write('_Translation\\loadFolders.xml')

            def check_necessity_loadfolder():
                with open('_Translation\\loadFolders.xml', 'r', encoding="utf-8") as xml_file:
                    tree1 = ET.parse(xml_file)
                root1 = tree1.getroot()
                for v in reversed(root1):
                    for li in reversed(v):
                        if li.text != "/":
                            # print("Check another path:", str(max_v), li.text)
                            if not str(max_v) == li.text:
                                # print('another_path = True -> not delete LoadFolder')
                                printy("Loadfolder.xml remove empty folders... Done", 'n')
                                print()
                                return
                if file_exists('_Translation\\loadFolders.xml'):
                    os.remove(f"_Translation\\loadFolders.xml")
                    printy("Loadfolder.xml remove empty folders... Done --> [r]Loadfolder.xml not needed.@",
                           predefined='n')
                    print()

            check_necessity_loadfolder()

        if file_exists('LoadFolders.xml'):
            exist()



        else:
            if state.new_loadfolder_pathes:
                printy("Loadfolder.xml creating for patches...", 'n')
                printy("\t[o>]Add patches_defs_folders into Loadfolder@")

                printy("\t\t", end='')
                for lf in state.new_loadfolder_pathes:
                    printy(escape_printy_string(lf), "o")

                loadFolders = ET.Element('loadFolders')
                loadFolders.text = "\n\t"

                vers = ET.SubElement(loadFolders, mod_data.max_version)
                vers.text = '\n\t\t'
                vers.tail = "\n"

                # print('Seach folders:', seach_folders)
                for s_f in folders.searching_pathes:
                    if (Path("_Translation") / s_f).exists():
                        li = ET.SubElement(vers, "li")
                        li.text = str(s_f) if str(s_f) != '.' else '/'
                        li.tail = "\n\t\t"
                for s_f in state.new_loadfolder_pathes:
                    li = ET.fromstring(s_f)
                    li.tail = "\n\t\t"
                    vers.append(li)
                vers[-1].tail = "\n\t"


                with open(f"_Translation\\LoadFolders.xml", "wb") as fff:
                    fff.write(ET.tostring(loadFolders, encoding="utf-8"))
                printy("Loadfolder.xml creating for patches...Done", 'n')

                # print("Add patches_defs_folders into Loadfolder")
                # for vv in root1:
                #     for lii in state.loadfolder_folders_to_add:
                #         el = ET.fromstring(lii)
                #         el.tail = '\n\t\t'
                #         vv.append(el)
                #     else:
                #         vv[-1].tail = "\n\t"


    loadfolder_check_folders()

    try:
        remove_empty_folders(root2)
    except Exception as ex:
        Error_log.append(f"Error delete_empty_folders {ex} \n\n")
        printy(fr"[r]\[ERROR\]@ delete_empty_folders {escape_printy_string(str(ex))} \n\n", predefined='<m')

    delete_folders.append(Path("_Translation") / "Grabbed_Defs_from_patches")
    try:
        if delete_folders:
            for ff in delete_folders:
                rmtree(ff, ignore_errors=True)
    except Exception as ex:
        Error_log.append(f"Error Delete {delete_folders} {ex} \n\n")

    # try:
    printy("Check for identical file names.", 'n')

    Finalizing.main(state.prog)
    printy("Check for identical file names... Done", 'n')


    # except Exception as ex:
    #     printy(fr"[r]\[ERROR\]@ Need error log --> [r]@ {escape_printy_string(str(ex))} \n\n", predefined='<m')


    def check_li_in_patches():
        xml_files = []
        check_path = Path('_Translation') / 'From_patches'

        if check_path.exists() and check_path.is_dir():
            # Рекурсивный поиск всех XML-файлов
            xml_files = list(check_path.rglob('*.xml'))

        for file_path in xml_files:
            with open(file_path, encoding='utf-8') as file:
                content = file.read()
                if '.0.' in content:
                    if S.Settings_language == 'ru':
                        Notification_log.append(f'В патче {file_path} есть <li>. Чтобы правильно перевести необходимо проверить правильно ли земенятся <li> на 0 (Часто это не так).')
                    else:
                        Notification_log.append(f'The patch {file_path} has <li>.  To translate correctly it is necessary to check if <li> is correctly grounded to 0 (Often it is not).')


    printy("Check li in patches", 'n')
    try:
        check_li_in_patches()
    except Exception as ex:
        print(ex)


    try:

        rmtree(New_Name, ignore_errors=True)
        copytree("_Translation",
                 sanitize_filename(New_Name), dirs_exist_ok=True)
        rmtree('_Translation', ignore_errors=True)
    except Exception as ex:
        Error_log.append(f"Error rename _Translation {ex} \n\n")
        printy(fr"[r]\[ERROR\]@ rename _Translation {escape_printy_string(str(ex))} \n\n", predefined='<m')

    if Error_log or Notification_log:
        printy(r"[r]\[ERROR\]@ Need error log --> [r]Opening Error_log.txt@", predefined='<m')
        _Tr = sanitize_filename(New_Name)
        os.makedirs(_Tr, exist_ok=True)
        with open(fr'{_Tr}\\Error_log.txt', 'w', encoding="utf-8") as er_log:
            for el in Error_log:
                er_log.write(el + "\n")
                # print(f"Write error {el}")
            for el in Notification_log:
                er_log.write(el + "\n")

        os.startfile(fr'{_Tr}\\Error_log.txt')
        # print('Нажмите "Enter" для выхода' if S.Game_language == "Russian" else 'Press "Enter" to exit.')
        # input()





    print("----------------------------------------------")
    print("All done")
    Floodgauge['value'] = 100
    if Error_log:
        ...
    if Pause_checkbox_var.get():
        os.chdir(str(state.prog))
        print('Нажмите "Enter" для выхода' if S.Settings_language == "Russian" else 'Press "Enter" to exit.')
        input()
        exit_prog()
    else:
        exit_prog()


Pause_checkbox_var: ttkbootstrap.BooleanVar


class TestApp(ttk_boot.Window):

    def disable_btns_switch(self, disable: bool):
        if disable:
            for _ in self.btns:
                _['state'] = 'disabled'
        else:
            for _ in self.btns:
                _['state'] = 'active'

    def __init__(self):

        @dataclass
        class WindowSettings:
            label = f'Text Grabber v.{Version_of_Text_grabber}'

            color2_Dark_grey = "#313131"  # Dark grey
            color3_Grey = "#595959"  # Grey
            color_grey_blue = '#505E8C'
            color_yellow_meadow = '#ECDB54'

            font1 = 'Consolas 10'
            Title_font_color = color_yellow_meadow

            Title_bg = '#313131'
            geometry = '+300+400'
            minsizeX, minsizeY = (200, 50)

        ttk_boot.Window.__init__(self, WindowSettings.label, themename="darkly")

        # Create a style

        path_entry = ttk_boot.StringVar(
            value=(f"Путь к моду..." if S.Settings_language == "ru" else f"Path to Mod Folder..."))

        self.option_add("*tearOff", False)
        # set overrideredirect to True to remove the windows default decorators
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.geometry(WindowSettings.geometry)  # you may or may not want to initialize the geometry of the window
        self.minsize(WindowSettings.minsizeX, WindowSettings.minsizeY)

        # (x, y) coordinates from top left corner of the window
        self.x = None
        self.y = None

        self.configure(background=WindowSettings.color3_Grey)
        self.Title_frame = ttk_boot.Frame(self, )
        self.Title_frame.pack(side=ttk_boot.TOP, fill=ttk_boot.X)

        self.Title_label = ttk_boot.Label(self.Title_frame, text=WindowSettings.label,
                                          foreground=WindowSettings.Title_font_color)
        self.Title_label.pack(side=ttk_boot.LEFT, fill=ttk_boot.X, anchor=ttk_boot.CENTER)
        # Pack the close button to the right-most side

        self.Title_close_btn = Button(self.Title_frame, text='x', bd=0, width=2, font=WindowSettings.font1,
                                      command=self.destroy, bg=WindowSettings.Title_bg, takefocus=0)

        self.Title_close_btn.pack(side=ttk_boot.RIGHT)

        self.call('encoding', 'system', 'utf-8')

        # Now you may want to move your window (obviously), so the respective events are bound to the functions
        self.Title_frame.bind("<ButtonPress-1>", self.start_move)
        self.Title_frame.bind("<ButtonRelease-1>", self.stop_move)
        self.Title_frame.bind("<B1-Motion>", self.do_move)

        self.Content_frame = ttk_boot.Frame(self, padding=5)
        self.Content_frame.pack(expand=True, fill='both', side=ttk_boot.BOTTOM)

        self.Main_frame = ttk_boot.Frame(self.Content_frame)
        self.Main_frame.pack(expand=True, fill='x', anchor='nw')

        self.Enter_textbox = ttk_boot.Entry(self.Main_frame, textvariable=path_entry, width=50,
                                            foreground=WindowSettings.color3_Grey)

        def on_entry_click(*_):
            self.Enter_textbox['foreground'] = 'white'
            self.Enter_textbox.delete(0, 'end')
            self.Enter_textbox.unbind('<FocusIn>')

        self.Enter_textbox.bind('<FocusIn>', on_entry_click)

        def keypress(e):
            if e.keycode == 86 and e.keysym != 'v':
                self.Enter_textbox.insert(ttk_boot.END, pyperclip.paste())
            elif e.keycode == 67 and e.keysym != 'c':
                pyperclip.copy(self.Enter_textbox.get())
            elif e.keycode == 88 and e.keysym != 'x':
                pyperclip.copy(self.Enter_textbox.get())
                self.Enter_textbox.delete(0, ttk_boot.END)

        self.Enter_textbox.bind("<Control-KeyPress>", keypress)
        self.Enter_textbox.bind('<Return>', lambda _: run_main(path_entry.get()))
        self.Enter_textbox.pack(fill='y', side='left', )
        self.Enter_textbox.event_add('<<Paste>>', '<Control-igrave>')

        def run_main(path=""):
            go_main(path)

        self.Enter_button = ttk_boot.Button(self.Main_frame, text="...", width=5, command=run_main, )
        self.Enter_button.pack(side='right', padx=(3, 0), )

        self.Main_frame2 = ttk_boot.Frame(self.Content_frame, padding=0)
        self.Main_frame2.pack(expand=True, fill='x', anchor='nw', )
        # noinspection PyArgumentList
        self.menubtn = ttk_boot.Menubutton(self.Main_frame2,
                                           text=(f"Быстрые настройки" if S.Settings_language == "ru" else f"Fast settings"),
                                           bootstyle="outline", )

        self.menu = ttk_boot.Menu(self.menubtn)

        global Pause_checkbox_var
        Pause_checkbox_var = ttk_boot.BooleanVar(value=False)
        Show_console_checkbox_var = ttk_boot.BooleanVar(value=False)

        def Show_console_checkbox_var_toggle():
            raise_console(Show_console_checkbox_var.get())

        ch_style = {'selectcolor': WindowSettings.color_yellow_meadow, 'foreground': WindowSettings.Title_font_color}
        fast_checkbuttons = {
            1: {'label': (f"Пауза по завершению" if S.Settings_language == "ru" else f"Pause at the end"),
                'variable': Pause_checkbox_var},
            2: {'label': (f"Показывать консоль" if S.Settings_language == "ru" else f"Show console"),
                'variable': Show_console_checkbox_var, 'command': Show_console_checkbox_var_toggle},

        }

        def Pause_checkbox_var_callback(*_):
            if Pause_checkbox_var.get():
                Show_console_checkbox_var.set(True)
                Show_console_checkbox_var_toggle()

        Pause_checkbox_var.trace_add('write', Pause_checkbox_var_callback)

        for value in fast_checkbuttons.values():
            self.menu.add_checkbutton(**value, **ch_style)

        self.menubtn['menu'] = self.menu

        self.menubtn.pack(anchor='sw', side='left', fill='both', pady=(5, 0))

        self.settings_image = ttk_boot.ImageTk.PhotoImage(file="Images\\Settings_icon.png", master=self)

        def run_settings_gui():
            # Window_Text_grabber.withdraw()
            Text_grabber_settings.run_from_main_prog(Window_Text_grabber, )

        self.settings_button = ttk_boot.Button(self.Main_frame2, image=self.settings_image,
                                               command=lambda: run_settings_gui())
        self.settings_button.pack(anchor='ne', side='right', expand=False, pady=(5, 0))

        self.Main_frame3 = ttk_boot.Frame(self.Content_frame, padding=5)
        self.Main_frame3.pack(expand=True, fill='x', anchor='nw', )
        self.Main_frame3.pack_forget()

        self.Floodgauge = ttk_boot.Floodgauge(self.Main_frame3, length=200, mask='Grabbing Progress {}%',
                                              bootstyle="secondary", maximum=100)
        self.Floodgauge.pack(anchor='s', side='bottom', expand=True, fill='both')

        self.btns = [self.Enter_button, self.settings_button, ]  # self.menubtn, ]

    def start_move(self, event):
        """ change the (x, y) coordinate on mousebutton press and hold motion """
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        """ when mouse button is released set the (x, y) coordinates to None """
        self.x = None
        self.y = None

    def do_move(self, event):
        """ function to move the window """
        self.wm_state('normal')  # if window is maximized, set it to normal (or resizable)
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")

    def size_change(self, event):
        """ function to change window size """
        self.wm_state('normal')
        x1 = self.winfo_pointerx()
        y1 = self.winfo_pointery()
        x0 = self.winfo_rootx()
        y0 = self.winfo_rooty()
        if (x1 - x0) < 0:
            x0 = 0
        if (y1 - y0) < 0:
            y0 = 0
        self.geometry(f"{x1 - x0}x{y1 - y0}")
        return

    def on_deiconify(self, event):
        """ function to deiconify or window """
        self.overrideredirect(True)

    def update_fast_checkBTNs(self):
        def include_in_QOL_bool_switch():
            global include_in_QOL
            include_in_QOL = include_in_QOL_bool.get()
            print(f"{include_in_QOL=}")

        if S.Author != 'Kamikadza13':
            return

        include_in_QOL_bool = ttk_boot.BooleanVar(value=False)
        self.menu.add_checkbutton(label="Включено в QOL", variable=include_in_QOL_bool,
                                  command=include_in_QOL_bool_switch)


def go_main(path):
    Window_Text_grabber.disable_btns_switch(True)
    Window_Text_grabber.Main_frame3.pack()
    Window_Text_grabber.update()

    t1 = threading.Thread(target=main, args=[path, Window_Text_grabber.Floodgauge], daemon=True)
    t1.start()


if __name__ == '__main__':

    def raise_console(Show_console: bool):
        """Brings up the Console Window."""
        if Show_console:
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 4)
        else:
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)


    def set_appwindow(root):

        hwnd = windll.user32.GetParent(root.winfo_id())
        hicon = win32gui.LoadImage(None, 'Images\\icons8-text-67.ico', win32con.IMAGE_ICON, 0, 0,
                                   win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE)
        win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, hicon)
        win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_SMALL, hicon)
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                               win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_APPWINDOW)

        root.wm_withdraw()
        root.after(10, lambda: root.wm_deiconify())
        windll.user32.SetForegroundWindow(hwnd)




    raise_console(False)
    Window_Text_grabber = TestApp()



    def updater():
        if S.Check_update:

            try:
                newest_version = Check_New_Version.Get_newest_version_number()
                if newest_version > Version_of_Text_grabber:
                    if S.Settings_language == 'ru':
                        dialog_message = f"Доступна новая версия Text grabber {newest_version}. Скачать?"
                        dialog_download = "Скачать"
                        dialog_cansel = "Не скачивать"
                    else:
                        dialog_message = f"New version avalible {newest_version}. Download?"
                        dialog_download = "Download"
                        dialog_cansel = "Cancel"

                    Update_dialog = ttkbootstrap.dialogs.MessageDialog(dialog_message, buttons=[dialog_cansel,
                                                                                                dialog_download + ":success"])
                    Update_dialog.show()

                    result = Update_dialog.result
                    # print('result: ', result)
                    if result == dialog_download:
                        Check_New_Version.Download_new_version()
                        printy("Need to Update", 'r')
                        Window_Text_grabber.destroy()
                    else:
                        printy(f"Latest version {Version_of_Text_grabber}", 'n')

            except Exception as e:
                printy(f"[r]\[ERROR\]@ version updater", predefined='<m')
                print(e)
                Error_log.append(f"Error version updater {e} \n\n")


    Window_Text_grabber.after(10, lambda: set_appwindow(root=Window_Text_grabber))

    Window_Text_grabber.withdraw()


    Window_Text_grabber.update_fast_checkBTNs()
    Window_Text_grabber.after(100, lambda: updater())

    # update_settings()

    # Window_Text_grabber.after(1000, lambda: update_settings())
    Window_Text_grabber.mainloop()

'''
pyinstaller Text_Grabber.spec




pyinstaller --noconfirm Text_Grabber.spec
Copy-Item -Path Images -Destination dist/Text_Grabber -Recurse
Copy-Item -Path locale -Destination dist/Text_Grabber -Recurse
Copy-Item -Path db.json -Destination dist/Text_Grabber
Compress-Archive -Path "dist/Text_Grabber" -DestinationPath "dist/Text_Grabber.zip" -update
'''
