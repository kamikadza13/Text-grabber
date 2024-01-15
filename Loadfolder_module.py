import os
import xml.etree.ElementTree as ET
from glob import glob
from os.path import exists as file_exists
from os.path import isfile as isfile
from shutil import copy as shcopy
from shutil import copytree
from shutil import rmtree

from printy import printy

# from Text_to_translate import pathes_to_DeftoTranslate

path_to_Def = []
path_to_Patch = []

files_to_translate_new_path = []
patches_new_path = []
files_to_translate_name = []
files_to_translate_path = []

'''
(path + "\\" if path != "" else "")
'''


def make_path_to_folders(path: str, Language):
    if file_exists((path + "\\" if path != "" else "") + "Defs"):
        path_to_Def.append(path)
        # print("\t\tВ " + path + " cуществует Defs")
        # print(path_to_Def)
        os.makedirs((os.path.normpath(
            ("_Translation\\" + (path + "\\" if path != "" else "") + "Languages\\" + Language + "\\DefInjected"))), exist_ok=True)

    if file_exists((path + "\\" if path != "" else "") + "Languages\\English\\Keyed"):
        copytree((path + "\\" if path != "" else "") + "Languages\\English\\Keyed",
                 "_Translation\\Languages\\" + Language + "\\Keyed",
                 symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)
        print(f"\t\tCopied Keyed from {os.path.abspath(path)}\\Languages\\English\\Keyed")

    else:
        if glob((path + "\\" if path != "" else "") + 'Languages\\*\\Keyed'):
            copytree(str(glob((path + "\\" if path != "" else "") + 'Languages\\*\\Keyed')[0]),
                     "_Translation\\Languages\\" + Language + "\\Keyed", symlinks=False, ignore=None,
                     ignore_dangling_symlinks=False, dirs_exist_ok=True)
            print(f"\t\tCopied Keyed from {os.path.abspath(path)}Languages\\?\\Keyed")

    if file_exists((path + "\\" if path != "" else "") + "Languages\\English\\Strings"):
        copytree((path + "\\" if path != "" else "") + "Languages\\English\\Strings",
                 "_Translation\\Languages\\" + Language + "\\Strings",
                 symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)
        print(f"\t\tCopied Strings from {os.path.abspath(path)}\\Languages\\English\\Strings")
    else:
        if glob((path + "\\" if path != "" else "") + 'Languages\\*\\Strings'):
            copytree(str(glob((path + "\\" if path != "" else "") + 'Languages\\*\\Strings')[0]),
                     "_Translation\\Languages\\" + Language + "\\Strings",
                     symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)
            print(f"\t\tCopied Strings from {os.path.abspath(path)}Languages\\?\\Strings")

    if file_exists((path + "\\" if path != "" else "") + "Patches"):
        path_to_Patch.append(path)
        # print("\t\tВ " + path + " cуществует Patches")




def make_files_path_to_translate(Language):
    printy('\t\tMaking pathes to files', 'y>')
    pathes = set(path_to_Def)
    printy('\t\tFiles:', 'y>')
    for idx, p_ in enumerate(pathes):
        # print("Папка оригинала:'" + p_)
        for path, subdirs, files in (os.walk(p_ + "\\Defs") if p_ != "" else os.walk(p_ + "Defs")):
            # print("     Файлы:")
            for file in files:
                if file.endswith('.xml'):
                    files_to_translate_name.append(file)
                    printy(f'\t\t\t{os.path.normpath(path + "//" + file)}')
                    files_to_translate_path.append(os.path.normpath(path + '\\' + file))
                    files_to_translate_new_path.append(os.path.normpath(("_Translation\\" + (p_ + "\\" if p_ != "" else "") + "Languages\\" + Language + "\\" + "DefInjected")))


    for path in path_to_Patch:
        patches_new_path.append("_Translation\\" + path)




def main(Language):
    def no_loadfolder():
        printy('\tNo loadFolders.xml', 'y>')

        pathes = ['']
        if file_exists('Common') and not isfile('Common'):
            pathes.append('Common')
        All_folders = [name for name in os.listdir(".") if os.path.isdir(name)]
        versions = [folder_name for folder_name in All_folders if folder_name.replace(".", "1").isnumeric()]
        if versions:
            pathes.append(max(versions))

        # print('Cписок pathes  =')
        # print(pathes)
        printy('\tSearching Defs, Keyed, Strings, Patches', 'y>')
        for path in set(pathes):
            make_path_to_folders(path, Language)
        make_files_path_to_translate(Language)

    def loadfolder():
        printy('\tloadFolders.xml found', 'y>')

        if not os.path.exists('_Translation'):
            os.makedirs('_Translation')
        shcopy("loadFolders.xml", "_Translation\\loadFolders.xml")
        with open('loadFolders.xml', 'r', encoding="utf-8") as xml_file:
            tree1 = ET.parse(xml_file)
        root1 = tree1.getroot()
        # Папки перевода from loadFolders.xml
        pathes = []
        for version in root1:
            for fold in version:
                if not any(path == fold.text for path in pathes):
                    if fold.text is not None:
                        # print(fold.text)
                        if fold.text.endswith("/"):
                            pathes.append(fold.text[:-1].replace("\\", "/"))
                        else:
                            pathes.append(fold.text.replace("\\", "/"))
                    else:
                        pathes.append("")

        # print('Cписок pathes  =')
        # print(pathes)
        printy('\tSearching Defs, Keyed, Strings, Patches', 'y>')

        for path in set(pathes):
            make_path_to_folders(path, Language)
        make_files_path_to_translate(Language)

    if file_exists("_Translation"):
        rmtree("_Translation")
    if not file_exists('loadFolders.xml'):
        no_loadfolder()
    else:
        loadfolder()


if __name__ == '__main__':
    main("Russian")
