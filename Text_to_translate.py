# -*- coding: utf-8 -*-

import glob
import os
import shutil
import html

# import glob
import xml.etree.ElementTree as ET
from os.path import exists as file_exists
from os.path import isfile as isfile

global exitString
global folder
global exitString1
global list_of_forbidden_character_in_label1
Class_replace = [("QuestNode_", ""), ("CompProperties_", "Comp_"), ("ScenPart_", "")]

listOfNumbers = "'0'"
for x in range(1, 100):
    listOfNumbers += ", '" + str(x) + "'"

listOfNumbers = [str(a) for a in range(100)]
files = []
new_list = []

list_of_labels_list = ["label", "labelNoun", "labelPlural", "text", "description", "jobString", "desc",
                       "customLabel", "customLetterLabel", "customLetterText", "ingestCommandString",
                       "ingestReportString", "outOfFuelMessage",
                       "name", "summary", 'pawnSingular', 'pawnsPlural',  #
                       "reportString"]  # Список Тэгов для вывода в печать
list_of_tags = ["Message", "Label", "label", "Title", "Text"]
# Список неполных тэгов
# Этот список ищется в Тэге (например, "Message" в <outOfFuelMessage> должно найтись)

list_of_path = ["rulesStrings", "customLetterText"]  # Список Тэгов перед <li> для вывода
list_of_forbidden_character_in_label = ["{", "}", "\'"]  # Список запрещенных символов в label
list_of_forbidden_tags = ['defaultLabelColor']  # Список запрещенных для вывода тэгов
list_of_folders_to_translate = ['Common', '/']  # Список папок для поиска Defs и Languages и т.д.

Language_translate_from = 'English'
Language = 'Russian'


def zamena_v_li_classe(a1, classes):
    global Class_replace
    new_tag = ""
    for inx, cls in enumerate(Class_replace):
        if cls[0] in classes:
            new_tag = a1.get('Class')
            new_tag = new_tag.replace(Class_replace[inx][0], Class_replace[inx][1])
            break

        else:
            new_tag = "li"
    return new_tag


def replace_child_li(parent, forbidden_name_list):
    element2 = parent.findall('li')
    for idx3, a1 in enumerate(element2):
        new_tag = find_new_path_for_li(a1, forbidden_name_list)
        new_tag = new_tag.replace(" ", "_")
        classes = a1.get('Class')
        if classes is not None:
            new_tag = zamena_v_li_classe(a1, classes)
        if new_tag == "li":
            new_tag = str(idx3)
        a1.tag = new_tag


def find_new_path_for_li(child, forbidden_character):
    element = child.find("./customLabel")
    if element is None:
        element = child.find("./def")
        if element is None:
            element = child.find("./label")
            if element is None:
                element = ""
    if element != "":
        for forbidden in forbidden_character:  # Список запрещенных символов в имени
            a1 = element
            if not isinstance(a1, str):
                if a1.text.find(forbidden) == -1:
                    element = element.text
                else:
                    element = "li"
    if element == "":
        element = "li"
    return element


def adding_in_string(stringa, elem_path, child):
    text1 = child.text
    text1 = html.escape(text1, quote=False)
    if elem_path.rpartition('/')[0] == "comps":
        stringa.append("%s/%s,%s" % (elem_path, "", text1))
    else:
        stringa.append("%s/%s,%s" % (elem_path, child.tag, text1))


def replace_defname(child):
    a1 = child.find('./defName')
    if a1 is not None:
        child.tag = child.tag + "/" + a1.text


def print_path_of_elems(elem, elem_path=""):
    global exitString
    global list_of_forbidden_character_in_label
    for child in elem:
        if not list(child) and child.text:
            # print(child.tag)
            if any(child.tag != d for d in list_of_forbidden_tags):  # Проверка запрещенных тэгов
                if any(child.tag == a for a in list_of_labels_list):  # Проверка на соответствие списку тэгов
                    adding_in_string(exitString, elem_path, child)
                elif any(child.tag == b for b in listOfNumbers):  # Проверка, что последний тэг - <li> (точнее
                    # порядковый номер <li>)
                    if any(a in elem_path.rpartition('/')[2] for a in list_of_path):
                        # Проверка последнего тэга перед ли, если в списке, то печатать
                        adding_in_string(exitString, elem_path, child)
                elif any(b in child.tag for b in list_of_tags):  # Проверка на не полный тэг
                    adding_in_string(exitString, elem_path, child)
        else:
            replace_defname(child)
            replace_child_li(child, list_of_forbidden_character_in_label)
            print_path_of_elems(child, "%s/%s" % (elem_path, child.tag))


def finish_string(tree2):
    global exitString
    global folder
    root_finish_string = tree2.getroot()
    exitString = []
    folder = []
    print_path_of_elems(root_finish_string)

    string = exitString
    # # """
    # # Добавление строки из глобальной переменной
    # # """

    string = [w.replace('\n', '') for w in string]

    for idx1, s in enumerate(string):
        s = s[1:]
        string[idx1] = s

    # # """
    # # Удаление '/' из начала пути
    # # """

    only_path = []
    only_tag = []
    only_text = []
    only_path_and_tag = []

    for i in range(0, len(string)):
        only_path_and_tag.append(string[i].partition(',')[0])
        only_path.append(string[i].partition(',')[0].rpartition('/')[0])
        only_tag.append(string[i].partition(',')[0].rpartition('/')[2])
        only_text.append(string[i].partition(',')[2])

    for i in range(0, len(only_path_and_tag)):
        #   Изменение одинаковых названий
        #   на name-0.label name-1.label и т.д.
        index = []
        for x1 in range(0, len(only_path_and_tag)):
            if x1 != i:
                # print(only_path_and_tag[x1])
                if str(only_path_and_tag[x1]) == str(only_path_and_tag[i]):
                    index.append(x1)
                if x1 == len(only_path_and_tag) - 1:
                    if len(index) > 0:
                        index.insert(0, i)
                        for j in range(0, len(index)):
                            only_path_and_tag[index[j]] = only_path_and_tag[index[j]].rpartition('/')[0] + "-" + \
                                                          str(j) + "/" + only_tag[index[j]]

    folder = [w.partition('/')[0] for w in string]
    #   Определение папки ... Def
    only_path_and_tag = [w.partition('/')[2] for w in only_path_and_tag]
    #   Удаление папки ...Def из пути

    only_path_and_tag = [w.replace('/', '.') for w in only_path_and_tag]
    all_text = ["<" + a + ">" + b + "</" + a + ">" for a, b in zip(only_path_and_tag, only_text)]

    Folder_and_text = []
    for idx3 in range(0, len(folder)):
        Folder_and_text.append((folder[idx3], all_text[idx3]))
        print(Folder_and_text[idx3])
    return Folder_and_text


def delete_empty_folders(root3):
    deleted = set()

    for current_dir, subdirs2, files2 in os.walk(root3, topdown=False):
        # print(current_dir)
        still_has_subdirs = any(subdir for subdir in subdirs2 if os.path.join(current_dir, subdir) not in deleted)
        # print("Есть подпапки: " + str(still_has_subdirs))
        # print("Есть файлы:    " + str(any(files2)))
        if not any(files2) and not still_has_subdirs:
            # print("Удаление папки:" + current_dir)
            os.rmdir(current_dir)
            deleted.add(current_dir)
        # print("--------")

    return deleted


"""
Если файл в моде существует в 2х экземплярах, то берется в таком порядке:
папка версий, потом Common потом '/' 
Но в проге обратный порядок т.к. файлы будут заменять друг-друга...
хм... а вообще не будут, и будет создаваться копии, но в разных папках
ну и пофиг.

Может быть стоит запилить проверку чтобы не было одинаковых файлов... в папке версий, потом Common потом '/' 
"""

""" Если нет 'loadFolders.xml'  """

p_to_fold_lang = []
pathes_to_DeftoTranslate = []
if not file_exists('loadFolders.xml'):
    # Проверка существования loadFolders.xml
    print("-----------------------------------------------------")
    print('loadFolders.xml не существует')
    max_version = ""
    common = ""
    all_tanslate_folders = []
    Num_folders = []
    All_folders = [name for name in os.listdir(".") if os.path.isdir(name)]
    print("Все папки для поиска папки версий:")
    print(All_folders)
    for fa in All_folders:
        if fa.replace(".", "1").isnumeric():
            Num_folders.append(fa)
    print("Все папки версий:")
    print(Num_folders)
    if Num_folders:
        max_version = max(Num_folders)
        max_version += '/'
    else:
        max_version = ""
    print("Максимальная верися " + max_version[:-1]) if max_version != "" else print()

    if file_exists('Common') and not isfile(file_exists('Common')):
        common = 'Common/'
    pathes = ['/']
    common != "" and pathes.append(common)  # Если common не равен "" выполнить вторую часть
    # Более короткая версия:
    # if common != "":
    #   pathes.append(common)
    max_version != "" and pathes.append(max_version)
    print('Загружаем список pathes  =')
    print('\n'.join(pathes))
    for path in pathes:
        print("-----------------------------------------------------")
        if path == "/":
            print("Папка: " + "/")
            path = ""
        else:
            print("Папка: " + path)

        if file_exists(path + "Defs") and not isfile(file_exists(path + "Defs")):
            print("В " + (path if path != "" else "/") + " cуществует Defs")
            shutil.copytree(path + "Defs", "_Translation/" + path + "/Languages/"
                            + Language + "/Defs_to_translate",
                            symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)
            print("Копирование в _Translation/" + path + "/Languages/" + Language + "/Defs_to_translate")
            pathes_to_DeftoTranslate.append((os.path.normpath(("_Translation/" + path + "/Languages/" +
                                                               Language + "/Defs_to_translate"))).replace("\\", "/"))
            print("pathes_to_DeftoTranslate = " + (os.path.normpath(("_Translation/" + path + "/Languages/" +
                                                                     Language + "/Defs_to_translate"))).replace("\\",
                                                                                                                "/"))
            os.makedirs((os.path.normpath(("_Translation/" + path + "/Languages/" +
                                           Language + "/DefInjected"))).replace("\\", "/"), exist_ok=True)

        else:
            pass
            print("В " + (path if path != "" else "/") + " не найдено /Defs")

        # if file_exists(path + "Patches") and not isfile(file_exists(path + "Patches")):
        #     print("В " + (path if path != "" else "/") + " cуществует Patches")
        #     shutil.copytree(path + "Patches", "_Translation/" + path + "/Languages/"
        #                     + Language + "/Patches_to_translate",
        #                     symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)
        #     print("Копирование в _Translation/" + path + "/Languages/" + Language + "/Patches_to_translate")
        # else:
        #     pass
        #     print("В " + (path if path != "" else "/") + " не найдено /Patches")

        if file_exists(path + "Languages/English/Keyed") and not \
                isfile(file_exists(path + "Languages/English/Keyed")):
            print("В " + (path if path != "" else "/") + " cуществует Languages/English/Keyed")
            shutil.copytree(path + "Languages/English/Keyed", "_Translation/Languages/"
                            + Language + "/Keyed",
                            symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)
            print("Копирование в _Translation/Languages/" + Language + "/Keyed")
        else:
            print("В " + (path if path != "" else "/") + " не найдено /Languages/English/Keyed")
            ''' Проверка Keyes в других языках '''
            if glob.glob(path + 'Languages/*/Keyed'):
                print("В " + (path if path != "" else "/") + " cуществует Languages/?/Keyed")
                path1 = str(glob.glob(path + 'Languages/*/Keyed')[0]).replace("//", "/").replace("\\", "/")
                shutil.copytree(path1, "_Translation/Languages/"
                                + Language + "/Keyed",
                                symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)
                print("Копирование в _Translation/Languages/" + Language + "/Keyed")
            else:
                pass
                print("В " + (path if path != "" else "/") + " не найдено /Languages/?/Keyed")

        if file_exists(path + "Languages/English/Strings") and not \
                isfile(file_exists(path + "Languages/English/Strings")):
            print("В " + (path if path != "" else "/") + " cуществует /Languages/English/Strings")
            shutil.copytree(path + "Languages/English/Strings", "_Translation/Languages/"
                            + Language + "/Strings",
                            symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)
            print("Копирование в _Translation/Languages/" + Language + "/Strings")
        else:
            print("В " + (path if path != "" else "/") + " не найдено /Languages/English/Strings")
            ''' Проверка Keyes в других языках '''
            if glob.glob(path + 'Languages/*/Strings'):
                print("В " + (path if path != "" else "/") + " cуществует Languages/?/Strings")
                path1 = str(glob.glob(path + 'Languages/*/Strings')[0]).replace("//", "/").replace("\\", "/")
                shutil.copytree(path1, "_Translation/Languages/"
                                + Language + "/Strings",
                                symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)
                print("Копирование в _Translation/Languages/" + Language + "/Strings")
            else:
                pass
                print("В " + (path if path != "" else "/") + " не найдено /Languages/?/Strings")
else:
    print("-----------------------------------------------------")
    print('loadFolders.xml существует')
    src_path = "loadFolders.xml"
    dst_path = r"_Translation\loadFolders.xml"
    if not os.path.exists('_Translation'):
        os.makedirs('_Translation')
    shutil.copy(src_path, dst_path)
    with open('loadFolders.xml', 'r') as xml_file:
        tree1 = ET.parse(xml_file)
    # tree1 = ET.parse('loadFolders.xml')
    root1 = tree1.getroot()
    # ET.dump(root1)
    # Папки перевода из loadFolders.xml
    pathes = []
    for version in root1:
        for fold in version:
            if any(x == fold.text + "/" for x in pathes):
                pass
            else:
                print(fold.text)
                pathes.append((fold.text if fold.text != "/" else "") + "/")

    print(pathes)
    print("-----------------------------------------------------")
    print('loadFolders.xml Folders:')
    print("---------")
    print("\n".join(pathes))
    print("---------End of Folders from loadFolders.xml---------")
    print("-----------------------------------------------------")
    print("---------Начало поиска папок Defs, Keys, Strings в loadFolders.xml Folders-------")
    for path in pathes:
        print("-----------------------------------------------------")
        if path == "/":
            print("Папка: " + "/")
            path = ""
        else:
            print("Папка: " + path)

        if file_exists(path + "Defs") and not isfile(file_exists(path + "Defs")):
            print("В " + (path if path != "" else "/") + " cуществует Defs")
            shutil.copytree(path + "Defs", "_Translation/" + path + "/Languages/"
                            + Language + "/Defs_to_translate",
                            symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)
            print("Копирование в _Translation/" + path + "/Languages/" + Language + "/Defs_to_translate")
            pathes_to_DeftoTranslate.append((os.path.normpath(("_Translation/" + path + "/Languages/" +
                                                               Language + "/Defs_to_translate"))).replace("\\", "/"))
            print("pathes_to_DeftoTranslate = " + (os.path.normpath(("_Translation/" + path + "/Languages/" +
                                                                     Language + "/Defs_to_translate"))).replace("\\",
                                                                                                                "/"))
            os.makedirs((os.path.normpath(("_Translation/" + path + "/Languages/" +
                                           Language + "/DefInjected"))).replace("\\", "/"), exist_ok=True)

        else:
            pass
            print("В " + (path if path != "" else "/") + " не найдено /Defs")

        # if file_exists(path + "Patches") and not isfile(file_exists(path + "Patches")):
        #     print("В " + (path if path != "" else "/") + " cуществует Patches")
        #     shutil.copytree(path + "Patches", "_Translation/" + path + "/Languages/"
        #                     + Language + "/Patches_to_translate",
        #                     symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)
        #     print("Копирование в _Translation/" + path + "/Languages/" + Language + "/Patches_to_translate")
        # else:
        #     pass
        #     print("В " + (path if path != "" else "/") + " не найдено /Patches")

        if file_exists(path + "Languages/English/Keyed") and not \
                isfile(file_exists(path + "Languages/English/Keyed")):
            print("В " + (path if path != "" else "/") + " cуществует Languages/English/Keyed")
            shutil.copytree(path + "Languages/English/Keyed", "_Translation/Languages/"
                            + Language + "/Keyed",
                            symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)
            print("Копирование в _Translation/Languages/" + Language + "/Keyed")
        else:
            print("В " + (path if path != "" else "/") + " не найдено /Languages/English/Keyed")
            ''' Проверка Keyes в других языках '''
            if glob.glob(path + 'Languages/*/Keyed'):
                print("В " + (path if path != "" else "/") + " cуществует Languages/?/Keyed")
                path1 = str(glob.glob(path + 'Languages/*/Keyed')[0]).replace("//", "/").replace("\\", "/")
                shutil.copytree(path1, "_Translation/Languages/"
                                + Language + "/Keyed",
                                symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)
                print("Копирование в _Translation/Languages/" + Language + "/Keyed")
            else:
                pass
                print("В " + (path if path != "" else "/") + " не найдено /Languages/?/Keyed")

        if file_exists(path + "Languages/English/Strings") and not \
                isfile(file_exists(path + "Languages/English/Strings")):
            print("В " + (path if path != "" else "/") + " cуществует /Languages/English/Strings")
            shutil.copytree(path + "Languages/English/Strings", "_Translation/Languages/"
                            + Language + "/Strings",
                            symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)
            print("Копирование в _Translation/Languages/" + Language + "/Strings")
        else:
            print("В " + (path if path != "" else "/") + " не найдено /Languages/English/Strings")
            ''' Проверка Keyes в других языках '''
            if glob.glob(path + 'Languages/*/Strings'):
                print("В " + (path if path != "" else "/") + " cуществует Languages/?/Strings")
                path1 = str(glob.glob(path + 'Languages/*/Strings')[0]).replace("//", "/").replace("\\", "/")
                shutil.copytree(path1, "_Translation/Languages/"
                                + Language + "/Strings",
                                symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)
                print("Копирование в _Translation/Languages/" + Language + "/Strings")
            else:
                pass
                print("В " + (path if path != "" else "/") + " не найдено /Languages/?/Strings")
    print("-----------------------------------------------------")

print("-----------------------------------------------------")
print("-----------------------------------------------------")

pathes_to_DeftoTranslate = list(filter(None, pathes_to_DeftoTranslate))
print("Папки:")
print(pathes)
print("Все пути до переводов")
print("\n".join(pathes_to_DeftoTranslate))
# pathes_to_patches = list(filter(None, pathes_to_patches))
# print(pathes_to_patches)
print("-----------------------------------------------------")
files_to_translate = []
files_to_translate_name = []
files_to_translate_path = []
print("     Поиск путей к файлам для перевода")
for idx, p_ in enumerate(pathes_to_DeftoTranslate):
    print("Папка оригинала:     '" + pathes[idx] + "'")
    print("Перевод папки:'" + p_)
    for path, subdirs, files in os.walk(p_):
        print("     Файлы:")
        for name in files:
            print("Имя:")
            print(name.replace('\\', '/'))
            files_to_translate_name.append(name.replace('\\', '/'))
            print("Путь:")
            print(path.replace('\\', '/'))
            print("Путь + Имя:")
            files_to_translate.append((os.path.join(path, name)).replace("\\", "/"))
            print(os.path.join(path, name).replace('\\', '/'))
            pth = path.partition("/Defs_to_translate")[0] + "/DefInjected"
            print("Путь к папке с переводом (Далее добавится папка типа Defs)")
            print(pth)
            files_to_translate_path.append(pth)
            print("---")

    print("----------")
print("---------------------------------------------------------------------------------------------------------")
print("--Начало чтения из файлов--")

for fl_idx, fil in enumerate(files_to_translate):
    try:
        print("     Чтение из " + fil)
        with open(fil, 'r') as xml_file:
            tree = ET.parse(xml_file)
        # tree = ET.parse(fil)
        print("File:  " + files_to_translate_name[fl_idx])

        root = tree.getroot()
        Folder_and_text_1 = finish_string(tree)
        print(fil)
        file_name = files_to_translate_name[fl_idx]
        file_full_path = fil
        file_path = files_to_translate_path[fl_idx]
        print("-----------------------------------------------------")
        Folders = []
        for f in Folder_and_text_1:
            if f[0] not in Folders:
                Folders.append(f[0])
        print("Папки для создания в DefInjected")
        print("Для этого файла")
        print(Folders)
        print("----------------------------")
        # print("load File: " + file_name)
        print("Начало разбивания файла на папки")
        for f1 in Folders:
            file_name1 = file_name.rpartition(".xml")[0] + "_" + str(f1)
            file_path1 = file_path + "/" + f1
            print("Folder:" + f1)
            text = ['<?xml version="1.0" encoding="utf-8"?>', '<LanguageData>']
            for f2 in Folder_and_text_1:
                if f2[0] == f1:
                    text.append(f2[1])
            text.append('</LanguageData>')
            # print('\n'.join(text))
            print("----------------Try CREATE FILE-----------------------")
            print("Ol File name: " + file_name)
            print("Old Full path:" + file_full_path)
            print("File name:    " + file_name1)
            print("New catrgoty: " + file_path1)
            file_path_plus_name = file_path1 + "/" + file_name1 + ".xml"
            print("New name/path:" + file_path_plus_name)
            os.makedirs(file_path1, exist_ok=True)
            Write_file = open(file_path_plus_name, "w")
            print("\n".join(text))
            # print("Вывод в:      " + file_path1 + "/DefInjected/" + f1 + "/")
            for l1 in text:
                Write_file.write("%s\n" % l1)
            Write_file.close()
            print("     End of Folder       ")
            print("----------------------------")

        # print('\n'.Folder_and_text_1[0])
        # print('\n'.join(Folder_and_text_1[1]))
    except ET.ParseError:
        print("|||--ERROR--|||      " + "Error in file:     " +
              fil.partition("_Translation/")[2].replace("Defs_to_translate", "Defs"))
        print("Пропуск файла")
        input("Press Enter to continue")
        print("--------------------------------------")
        pass

for p1 in pathes_to_DeftoTranslate:
    # print("Удаление папки:")
    # print(p1)
    shutil.rmtree(p1)
print("--------------------------------------")
root2 = '_Translation'
print("Удаление пустых папок")
delete_empty_folders(root2)

"""
Проверка loadFolders на наличие папок
"""
if file_exists('loadFolders.xml'):
    with open('loadFolders.xml', 'r') as xml_file:
        tree1 = ET.parse(xml_file)
    # tree1 = ET.parse('loadFolders.xml')
    root1 = tree1.getroot()
    # ET.dump(root1)
    # Папки перевода из loadFolders.xml
    pathes = []
    removable_element = []
    for version in root1:
        for fold in version:
            if any(x == fold.text + "/" for x in pathes):
                pass
            else:
                txt = (fold.text if fold.text != "/" else "")
                if txt != "":
                    if file_exists("_Translation/" + txt):
                        pass
                        # print("_Translation/" + txt + " существует")
                    else:
                        # print("_Translation/" + txt + " НЕ существует")
                        removable_element.append(fold)

            # print("-----------")
    for version in reversed(root1):
        for re in removable_element:
            version.remove(re)
    tree1.write('_Translation/loadFolders.xml')

# for path, subdirs, files in os.walk("Patches"):
#     for name in files:
#         patch_fullname = os.path.join(path, name)
#
#
#
# def patch_strings(elem, elem_path=""):
#     global exitString1
#     global list_of_forbidden_character_in_label1
#     for child in elem:
#         if not list(child) and child.text:
#             # print(child.tag)
#             if any(child.tag != d for d in list_of_forbidden_tags):  # Проверка запрещенных тэгов
#                 if any(child.tag == a for a in list_of_labels_list):  # Проверка на соответствие списку тэгов
#                     adding_in_string(exitString, elem_path, child)
#                 elif any(child.tag == b for b in listOfNumbers):  # Проверка, что последний тэг - <li> (точнее
#                     # порядковый номер <li>)
#                     if any(a in elem_path.rpartition('/')[2] for a in list_of_path):
#                         # Проверка последнего тэга перед ли, если в списке, то печатать
#                         adding_in_string(exitString, elem_path, child)
#                 elif any(b in child.tag for b in list_of_tags):  # Проверка на не полный тэг
#                     adding_in_string(exitString, elem_path, child)
#         else:
#             replace_defname(child)
#             replace_child_li(child, list_of_forbidden_character_in_label)
#             print_path_of_elems(child, "%s/%s" % (elem_path, child.tag))
#
#
#
#
# for paf in patch_fullname:
#     pass
#     tree = ET.parse(paf)
#     Folder_and_text_1 = finish_string(tree)
# os.system("pause")
# input()
print("----------------------------------------------")
print("All done")
input("Press Enter to exit")

