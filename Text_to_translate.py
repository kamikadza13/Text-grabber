# -*- coding: utf-8 -*-
from tkinter import Tk
from tkinter import Label
from re import match
from re import sub
from os.path import expanduser
from os import makedirs
from glob import glob
import os

from html import escape
from shutil import copytree
from shutil import copy as shcopy
from shutil import rmtree

import xml.etree.ElementTree as ET
from os.path import exists as file_exists
from os.path import isfile as isfile

global exitString
global folder
global exitString1
global list_of_forbidden_character_in_label1

Parent_Name = []
Parent_Name_that_has_parent = []
Parent_elem = []
settings_path = ""


def Settings():
    global settings_path
    settings_ini_file_path = expanduser("~\RimTextGrabber\Settings.ini")
    settings_path = settings_ini_file_path

    if not file_exists(settings_ini_file_path):
        makedirs(settings_ini_file_path.rpartition("\\")[0], exist_ok=True)
        with open(settings_ini_file_path, 'w', encoding="utf-8") as settings:
            text = """Language=Russian
Autor=Kamikadza13
Name_add=rus
# That Name_add will be added in the end of mod name in About.xml
Description=Translation of
Add_comment=True"""
            settings.write(text)
        window = Tk()
        window.minsize(300, 100)
        window.title("RimTextGrabber")
        label = Label(window, text=f"No settings file found\nA new settings file has been created along the path:")
        label.pack()
        texxt = Label(window, text=f"{settings_ini_file_path}", foreground="white", background="black")
        texxt.pack()
        window.attributes('-topmost', True)
        window.mainloop()
    else:
        if isfile(settings_ini_file_path):
            print(f"File {settings_ini_file_path} exists")
            settigs_is_norm = True
            with open(settings_ini_file_path, 'r', encoding="utf-8") as settings:
                if all(match("Language", settings_param) is None for settings_param in settings):
                    settigs_is_norm = False
                if all(match("Autor", settings_param) is None for settings_param in settings):
                    settigs_is_norm = False
                if all(match("Name_add", settings_param) is None for settings_param in settings):
                    settigs_is_norm = False
                if all(match("Description", settings_param) is None for settings_param in settings):
                    settigs_is_norm = False
                if all(match("Add_comment", settings_param) is None for settings_param in settings):
                    settigs_is_norm = False
            if not settigs_is_norm:
                with open(settings_ini_file_path, 'w', encoding="utf-8") as settings:
                    text = """Language=Russian
Autor=Kamikadza13
Name_add=rus
# That Name_add will be added in the end of mod name in About.xml
Description=Translation of
Add_comment=True"""
                    settings.write(text)
                window = Tk()
                window.minsize(300, 100)
                window.title("RimTextGrabber")
                label = Label(window, text=f"Bad settings file\nA new settings file has been created along the path:")
                label.pack()
                texxt = Label(window, text=f"{settings_ini_file_path}", foreground="white", background="black")
                texxt.pack()
                window.attributes('-topmost', True)
                window.mainloop()


Class_replace = [("QuestNode_", ""), ("CompProperties_", "Comp_"), ("ScenPart_", "")]

listOfNumbers = "'0'"
for x in range(1, 100):
    listOfNumbers += ", '" + str(x) + "'"

listOfNumbers = [str(aaaaaaaaa) for aaaaaaaaa in range(100)]
files = []
new_list = []

list_of_labels_list = ["label", "labelNoun", "labelPlural", "text", "description", "jobString", "desc",
                       "customLabel", "customLetterLabel", "customLetterText", "ingestCommandString",
                       "ingestReportString", "outOfFuelMessage",
                       "name", "summary", 'pawnSingular', 'pawnsPlural', 'adjective', 'ideoName', 'member', 'type',  #
                       "reportString"]  # Список Тэгов для вывода в печать
list_of_tags = ["Message", "Label", "label", "Title", "Text", "gerund", "Gerund", "Explanation"]
# Список неполных тэгов
# Этот список ищется в Тэге (например, "Message" в <outOfFuelMessage> должно найтись)

list_of_path = ["rulesStrings", "customLetterText", "thoughtStageDescriptions", "symbolPacks"]
# Список Тэгов перед <li> для вывода
"""
например:
<li Class="PreceptComp_SituationalThought">				
	<thought>AM_Mood_Volatile</thought>
	<thoughtStageDescriptions>
		<li>Spiders in my face</li>
		<li>Clown in the sky looking at me</li>
		<li>Liquorice tastes like betrayal</li>
	</thoughtStageDescriptions>
"""
list_of_forbidden_tags = ['defaultLabelColor']  # Список запрещенных для вывода тэгов
list_of_forbidden_part_of_path = ['verbs']
list_of_forbidden_part_of_label = ['ЛАЖА', 'Texture', 'colorChannels']  # Список запрещенных для вывода тэгов
list_of_forbidden_text = ['True', 'False', 'true', 'false']  # Список запрещенных слов для вывода
# Если выводиимый тест будет совпадать полностью строке из списка, он не будет выводиться

list_of_folders_to_translate = ['Common', '/']  # Список папок для поиска Defs и Languages и т.д.
Error_log = []
Language = ""
Autor = ""
Name_add = ""
Description = ""
Add_comment = True
Settings()

if file_exists(settings_path):
    with open(settings_path, 'r', encoding="utf-8") as settings:
        for settings_param in settings:
            if settings_param.find("Language") != -1:
                Language = settings_param.partition("Language")[2].strip(' =').strip('\n')
            if settings_param.find("Autor") != -1:
                Autor = settings_param.partition("Autor")[2].strip(' =').strip('\n')
            if settings_param.find("Name_add") != -1:
                Name_add = settings_param.partition("Name_add")[2].strip(' =').strip('\n')
            if settings_param.find("Description") != -1:
                Description = settings_param.partition("Description")[2].strip(' =').strip('\n')
            if settings_param.find("Add_comment") != -1:
                Add_comment = settings_param.partition("Add_comment")[2].strip(' =').strip('\n').lower() == "true"
if Language == "":
    Language = 'Russian'
if Autor == "":
    Autor = 'Kamikadza13'
if Name_add == "":
    Name_add = 'rus'
if Description == "":
    Description = 'Перевод'
if Autor == "Kamikadza13":
    Description = 'Перевод'
    Add_comment = True


#  ----------------------------------
#  ----------------------------------

#  Добавление родителей


def Parent_append(root11: ET.Element):
    for r in root11:
        elems = []
        # ET.dump(r)
        if 'Name' in r.keys():
            name = r.get("Name")
            # print(f"Есть имя {name}")
            if 'ParentName' in r.keys():
                par_name = r.get("ParentName")
                # print(f"Есть родитель {par_name} у {name}")
            else:
                par_name = "none"
            for rr in r:
                # print(f'добавляется элемент {rr.tag}  {rr.text}')
                elems.append(rr)
            if name not in Parent_Name:
                # print(f"{name} не в Parent_Name:{Parent_Name}")
                Parent_Name.append(name)
                Parent_Name_that_has_parent.append(par_name)
                Parent_elem.append(elems)
            else:
                print(f"Попытка добавить новое имя в Parent_Name но,\nв списке родителей"
                      f" {Parent_Name} уже есть имя {name} с индексом {Parent_Name.index(name)}")
                indx = Parent_Name.index(name)
                add_elems_into_list(Parent_elem[indx], elems)
                # for e in elems:
                #     if e.tag not in [x11.tag for x11 in Parent_elem[indx]]:
                #         Parent_elem[indx].append(e)


def print_Name_parent_elem():
    for i, pn in enumerate(Parent_Name):
        print(
            f'имя:{pn : <25}'
            f'родитель:{str(Parent_Name_that_has_parent[i]) : <7}'
            f'элементы:{[x11.tag + "." + x11.text for x11 in Parent_elem[i]]}'
        )
    print("-------------------------")


def adding_elems(root1: ET.Element, elem: ET.Element):
    if root1.find(elem.tag) is None:
        # elem.text.strip("\n\t\r")
        # print("Добавлен элемент " + elem.tag)
        root1.append(elem)
    else:
        # print(f"Элемент {elem.tag} существует в {root1.tag} {root1.attrib}")
        if elem.tag != "li":
            for e in elem:
                adding_elems(root1.find(elem.tag), e)
        else:
            # print(f"Нужно добавить <li>, когда <li> уже есть в {root1.tag}")
            if len(elem):
                # print(f"Добавляемый <li> элемент имеет наследников")

                if root1.find(elem.tag):
                    # print("У <li> Есть дети")
                    # print("рут:")
                    # ET.dump(root1)
                    # print("добавляемый эл-т")
                    # ET.dump(elem)
                    for e in elem:
                        adding_elems(root1.find(elem.tag), e)
                else:
                    # print("В руте нет наследников")
                    # print("рут:")
                    # ET.dump(root1)
                    # print("добавляемый эл-т")
                    # ET.dump(elem)
                    # elem.text.strip("\n\t\r")
                    root1.append(elem)

            else:
                # print("У <li> нет детей")
                if not any(x.text == elem.text for x in root1):
                    # print("li с таким текстом нет, добавляем его")
                    # elem.text.strip("\n\t\r")
                    root1.append(elem)
                else:
                    print(f"li с текстом {elem.text} уже есть в {root1.tag}")
                    pass


def add_elems_into_list(list_of_elems: list, list_of_elems_to_add: list):
    print(f"изначально:\n{[x.tag for x in list_of_elems]}")
    exist_root = ET.Element("root1")
    for l in list_of_elems:
        exist_root.append(l)
    # ET.dump(exist_root)
    for elem in list_of_elems_to_add:
        adding_elems(exist_root, elem)
    list_of_elems = []
    for el in exist_root:
        list_of_elems.append(el)
    # print("итого")
    # ET.dump(exist_root)
    print(f"итого:\n{[x.tag for x in list_of_elems]}")
    return list_of_elems


def update_Parent_Name_elems(Parent_Name1, Parent_Name_that_has_parent1, Parent_elem1):
    for i, pn in enumerate(Parent_Name_that_has_parent1):
        if pn != "none":
            if pn not in Parent_Name1:
                print(f"Есть родитель {pn}, но он не в списке Parent_Name1\nУбираем родителя из списка")
                Parent_Name_that_has_parent1[i] = "none"
    # print_Name_parent_elem()
    while True:
        for i, pn in enumerate(Parent_Name_that_has_parent1):
            if pn != "none":
                if pn in Parent_Name1:  # Если родитель есть в листе имен
                    print(f"У {Parent_Name1[i]} Есть родитель {pn}, и он в списке Parent_Name1")
                    j = Parent_Name1.index(pn)
                    if Parent_Name_that_has_parent1[j] == "none":
                        print(f"Есть родитель {pn}, и у него нет родителя")
                        print(Parent_elem1[j])
                        print(Parent_Name1[j])
                        print(f"Попытка добавить {[x.tag for x in Parent_elem1[j]]} в {Parent_Name1[j]}")
                        Parent_elem1[i] = add_elems_into_list(Parent_elem1[i], Parent_elem1[j])
                        # print(f"Удаляем у {Parent_Name1[i]} родителя {Parent_Name_that_has_parent1[i]}")
                        Parent_Name_that_has_parent1[i] = "none"
                else:
                    print("Какая-то лажа")
                    print(f"Есть родитель {pn}, но он не в списке Parent_Name1\nУбираем родителя из списка")
                    Parent_Name_that_has_parent1[i] = "none"

        # print_Name_parent_elem()

        if all(p == "none" for p in Parent_Name_that_has_parent):
            break


def adding_elems_into_root_by_Parent_elem(root: ET.Element):
    for r in root:
        # print(f"Тэг:    {r.tag}\nЭлемен: {[x.tag for x in r]}\nАттриб: {r.attrib}\nТекст:  {r.text}")
        if 'ParentName' in r.keys():
            key = r.get('ParentName')
            for inx, pn in enumerate(Parent_Name):
                if pn == key:
                    for pe in Parent_elem[inx]:
                        adding_elems(r, pe)
                    print(f"Добавляются элменты {[x.tag for x in Parent_elem[inx]]} в \n{r.tag}.{r.attrib}")


#  ----------------------------------
#  ----------------------------------


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


def replace_child_li(parent: ET.Element):
    element2 = parent.findall('li')
    if element2:
        # print("Изначальный элемент без земененных <li>")
        # ET.dump(parent)
        for idx3, a1 in enumerate(element2):
            new_tag = find_new_path_for_li(a1)
            new_tag = new_tag.replace(" ", "_")
            classes = a1.get('Class')
            if classes is not None:
                new_tag = zamena_v_li_classe(a1, classes)
            if new_tag == "li":
                new_tag = str(idx3)
            a1.tag = new_tag
        # print("--Итоговый элемент с заменненными <li>--")
        # ET.dump(parent)


def replace_rulestring(parent: ET.Element):
    text_list = []
    text = "\n"
    a = "\t\t<li>"
    b = "</li>\n"
    for li in parent:
        if li.tag == "li":
            text += a + li.text + b
    parent.clear()
    parent.text = text


def find_new_path_for_li(child: ET.Element):
    element = child.find("./customLabel")
    if element is None:
        element = child.find("./def")
        if element is None:
            element = child.find("./label")
            if element is None:
                element = ""
    if element != "":
        # print(element.text)
        if not all(str(x11).isalpha() or str(x11).isnumeric() or str(x11).isspace() for x11 in element.text):
            element = "li"
        else:
            element = "li"
            # element = element.text
            #
            #   element = "li" Убрать, когда пойму, когда можно заменять на label
            #   element = element.text вернуть
            #
    if element == "":
        element = "li"
    return element


def adding_in_string(stringa, elem_path, child: ET.Element):
    text1 = child.text
    text1 = escape(text1, quote=False)
    text1 = text1.replace("li&gt;", "li>")
    text1 = text1.replace("&lt;li", "<li")
    text1 = text1.replace("&lt;/li", "</li")
    # text1 = text1.replace("\\n", "\n")
    print(elem_path)
    print(elem_path.count("/"))
    for ft in list_of_forbidden_text:
        if text1 == ft:
            print("Запрещенный текст: Пропускается строка - ", "%s/%s, text: %s" % (elem_path, child.tag, text1))
            return None
    for fp in list_of_forbidden_part_of_path:
        if fp in elem_path:
            print("Запрещенный путь: Пропускается строка - ", "%s/%s, text: %s" % (elem_path, child.tag, text1))
            return None
    for fp in list_of_forbidden_part_of_label:
        if fp in child.tag:
            print("Запрещенный тэг/label: Пропускается строка - ", "%s/%s, text: %s" % (elem_path, child.tag, text1))
            return None
    if elem_path.count("/") < 2:  # Проверка пути, есть ли там, что-то кроме tag
        return None
    if elem_path.rpartition('/')[0] == "comps":
        stringa.append("%s/%s,%s" % (elem_path, "", text1))
    else:
        stringa.append("%s/%s,%s" % (elem_path, child.tag, text1))
        # print("%s/%s,%s" % (elem_path, child.tag, text1))


def replace_defname(child: ET.Element):
    a1 = child.find('./defName')
    if a1 is not None:
        if " " in a1.text:
            Error_log.append(f'Пришлось заменить defName {child.tag + "/" + a1.text}'
                             f' на {child.tag + "/" + a1.text.replace(" ", "_")}')
            child.tag = child.tag + "/" + a1.text

        else:
            child.tag = child.tag + "/" + a1.text.replace(" ", "_")


def make_path_to_branch(elem: ET.Element):
    for idxx, child in enumerate(elem):
        tag = child.tag.rpartition("/")[2]
        if child.tag == "li":
            child.tag = str(idxx)
        child.tag = elem.tag + "/" + child.tag
        child.tag = child.tag.strip('\t').strip(' ')
        if not list(child) and child.text:
            if any(ll1 == tag for ll1 in list_of_labels_list):
                print(child.tag + "\t\t" + child.text)
            elif any(lot in tag for lot in list_of_tags):
                if any(a in tag for a in list_of_forbidden_part_of_label):
                    continue
                else:
                    print(child.tag + "\t\t" + child.text)

            pass
        else:
            make_path_to_branch(child)


def Go_search_Name_class(list_of_files: list):
    for idx_1, fi_w_name in enumerate(list_of_files):
        try:
            print("     Чтение из " + fi_w_name)
            with open(fi_w_name, 'r', encoding="utf-8") as xml_f:
                tree_name = ET.parse(xml_f)
            # print("File:  " + files_to_translate_name[idx_1])
            root_name = tree_name.getroot()
            Parent_append(root_name)
            update_Parent_Name_elems(Parent_Name, Parent_Name_that_has_parent, Parent_elem)

        except ET.ParseError:
            print(f"Не открывается файл {fi_w_name}")
            pass
    pass


def pawnKind_add_strings(elem: ET.Element):
    list_pawn = ['labelPlural', 'labelMale', 'labelMalePlural', 'labelFemale', 'labelFemalePlural']
    add_elem = []
    if elem.find('label') is not None:
        label_text = str(elem.find('label').text)
        for idx_, l_pawn in enumerate(list_pawn):
            add_elem.append(ET.Element(l_pawn))
            if elem.find(l_pawn) is None:
                elem.append(add_elem[idx_])
                txt = str(l_pawn.partition("label")[2])
                # print(txt)
                txt = txt.replace('ePlural', 'e Plural')
                # print(txt)
                add_elem[idx_].text = txt + " " + label_text

    """
    Скопировать в ScenarioDef.scenario
    label (переименовать в name) и description из ScenarioDef если там нет


    """


def ScenarioDef_add_strings(elem: ET.Element):
    if elem.find('scenario') is not None:
        scenario = elem.find('scenario')
        # print(f"Есть ветка scenario")
        if scenario.find("name") is None:
            label = elem.find("label")
            if label is not None:
                scenario.append(label)

        if scenario.find("description") is None:
            description = elem.find("description")
            if description is not None:
                scenario.append(description)
    else:
        print(f"Нет ветки scenario???")
        label = elem.find("label")
        scenario = ET.SubElement(elem, "scenario")
        if label is not None:
            scenario.append(label)
        description = elem.find("description")
        if description is not None:
            scenario.append(description)


def print_path_of_elems(elem: ET.Element, root3: ET.Element, elem_path=""):
    global exitString
    for child in elem:
        if 'Abstract' in child.attrib:
            if child.attrib['Abstract'].lower() == 'true':
                continue  # пропуск абстрактного объекта (continue переходит к следующему for)
        if not list(child) and child.text:
            if any(child.tag != d for d in list_of_forbidden_tags):  # Проверка запрещенных тэгов
                #  # Проверка запрещенных путей
                if any(c.isalpha() for c in child.text):  # Есть хотя бы один буквенный символ
                    if any(child.tag == a for a in list_of_labels_list):  # Проверка на соответствие списку тэгов
                        adding_in_string(exitString, elem_path, child)
                    elif any(child.tag == b for b in listOfNumbers):  # Проверка, что последний тэг - <li> (точнее
                        # порядковый номер <li>)
                        if any(a in elem_path.rpartition('/')[2] for a in list_of_path):
                            # Проверка последнего тэга перед ли, если в списке, то печатать
                            adding_in_string(exitString, elem_path, child)
                    elif any(b in child.tag for b in list_of_tags):  # Проверка на не полный тэг
                        adding_in_string(exitString, elem_path, child)
                    elif " " in child.text:
                        adding_in_string(exitString, elem_path, child)

        else:
            if elem.tag.partition("/")[0] == "PawnKindDef":
                pawnKind_add_strings(elem)  # Если PawnKindDef, то добавить необходимые labelPlural
            if elem.tag.partition("/")[0] == "ScenarioDef":
                ScenarioDef_add_strings(elem)  # Если ScenarioDef, то добавить ['name', 'description'] в scenario

            replace_defname(child)
            if child.tag.lower() in ["rulesstrings", "rulefiles", "rulesfiles"]:
                replace_rulestring(child)
                adding_in_string(exitString, elem_path, child)
            else:
                replace_child_li(child)
            print_path_of_elems(child, root3, "%s/%s" % (elem_path, child.tag))


def finish_string(tree2):
    global exitString
    global folder
    root_finish_string = tree2.getroot()
    exitString = []
    folder = []
    print_path_of_elems(root_finish_string, root_finish_string)

    string = exitString
    # # """
    # # Добавление строки из глобальной переменной
    # # """

    # string = [w.replace('\n', '\\n') for w in string]

    for idx1, s11 in enumerate(string):
        s11 = s11[1:]
        string[idx1] = s11

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

    print("\n ---".join(string))

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


def make_about_folder():
    s1_path = "About/preview.png"
    d_path = "_Translation/About"
    os.makedirs(d_path, exist_ok=True)
    if file_exists(s1_path):
        shcopy(s1_path, d_path)
    tree3 = ET.parse("About/About.xml")
    root3 = tree3.getroot()
    sv = root3.find("supportedVersions")
    supportedVersions = ET.tostring(sv, encoding='utf8')
    supportedVersions = str(supportedVersions).partition('<supportedVersions>')[2].rpartition('</supportedVersions>')[0]
    supportedVersions = supportedVersions.replace("\\n", "\n").replace("\\t", "\t")
    name = root3.find("name").text
    packageId = root3.find("packageId").text
    with open('_Translation/About/About.xml', 'w', encoding="utf-8") as about_1:
        about_1.write('<?xml version="1.0" encoding="utf-8"?>' + "\n")
        about_1.write('<ModMetaData>' + "\n")
        about_1.write("\t" + '<name>' + name + " " + Name_add + '</name>' + "\n")
        about_1.write("\t" + '<author>' + Autor + '</author>' + "\n")
        if len(Autor + "." + packageId) > 60:
            if len(Autor + "." + packageId.partition(".")[0]) > 60:
                about_1.write("\t" + '<packageId>' + "Need_less_than_60_symbols" + '</packageId>' + "\n")
            else:
                about_1.write("\t" + '<packageId>' + Autor + "." + packageId.partition(".")[0] + '</packageId>' + "\n")
        else:
            about_1.write("\t" + '<packageId>' + Autor + "." + packageId + '</packageId>' + "\n")

        about_1.write("\t" + '<supportedVersions>' + supportedVersions + '</supportedVersions>' + "\n")
        about_1.write("\t" + '<loadAfter>\n\t\t<li>' + packageId + '</li>\n\t</loadAfter>' + "\n")
        about_1.write("\t" + '<description>' + Description + " " + name + '</description>' + "\n")
        about_1.write('</ModMetaData>')


#  ----------------
#  Errors


def Error_parse_error(name):
    Error_log.append("Ошибка чтения " + name)


def Error_delete_path_def_to_trans(func, pathz, _):
    Error_log.append("Ошибка удаления " + str(func) + " " + str(pathz) + " " + str(_))


"""
Если файл в моде существует в 2х экземплярах, то берется в таком порядке:
папка версий, потом Common потом '/' 
Но в проге обратный порядок т.к. файлы будут заменять друг-друга...
хм... а вообще не будут, и будет создаваться копии, но в разных папках
ну и пофиг.

Может быть стоит запилить проверку чтобы не было одинаковых файлов... в папке версий, потом Common потом '/' 
"""

""" Если нет 'loadFolders.xml'  """


# p_to_fold_lang = []


def main():
    pathes_to_DeftoTranslate = []

    if file_exists("_Translation"):
        rmtree("_Translation")

    if not file_exists('loadFolders.xml'):
        # Проверка существования loadFolders.xml
        print("-----------------------------------------------------")
        print('loadFolders.xml не существует')
        common = ""
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
                copytree(path + "Defs", "_Translation/" + path + "/Languages/"
                                + Language + "/Defs_to_translate",
                                symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)
                print("Копирование в _Translation/" + path + "/Languages/" + Language + "/Defs_to_translate")
                pathes_to_DeftoTranslate.append((os.path.normpath(("_Translation/" + path + "/Languages/" +
                                                                   Language + "/Defs_to_translate"))).replace("\\",
                                                                                                              "/"))
                print("pathes_to_DeftoTranslate = " + (os.path.normpath(("_Translation/" + path + "/Languages/" +
                                                                         Language + "/Defs_to_translate"))).replace(
                    "\\",
                    "/"))
                os.makedirs((os.path.normpath(("_Translation/" + path + "/Languages/" +
                                               Language + "/DefInjected"))).replace("\\", "/"), exist_ok=True)

            else:
                pass
                print("В " + (path if path != "" else "/") + " не найдено /Defs")

            # if file_exists(path + "Patches") and not isfile(file_exists(path + "Patches")):
            #     print("В " + (path if path != "" else "/") + " cуществует Patches")
            #     copytree(path + "Patches", "_Translation/" + path + "/Languages/"
            #                     + Language + "/Patches_to_translate",
            #                     symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)
            #     print("Копирование в _Translation/" + path + "/Languages/" + Language + "/Patches_to_translate")
            # else:
            #     pass
            #     print("В " + (path if path != "" else "/") + " не найдено /Patches")

            if file_exists(path + "Languages/English/Keyed") and not \
                    isfile(file_exists(path + "Languages/English/Keyed")):
                print("В " + (path if path != "" else "/") + " cуществует Languages/English/Keyed")
                copytree(path + "Languages/English/Keyed", "_Translation/Languages/"
                                + Language + "/Keyed",
                                symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)
                print("Копирование в _Translation/Languages/" + Language + "/Keyed")
            else:
                print("В " + (path if path != "" else "/") + " не найдено /Languages/English/Keyed")
                ''' Проверка Keyes в других языках '''
                if glob(path + 'Languages/*/Keyed'):
                    print("В " + (path if path != "" else "/") + " cуществует Languages/?/Keyed")
                    path1 = str(glob(path + 'Languages/*/Keyed')[0]).replace("//", "/").replace("\\", "/")
                    copytree(path1, "_Translation/Languages/"
                                    + Language + "/Keyed",
                                    symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)
                    print("Копирование в _Translation/Languages/" + Language + "/Keyed")
                else:
                    pass
                    print("В " + (path if path != "" else "/") + " не найдено /Languages/?/Keyed")

            if file_exists(path + "Languages/English/Strings") and not \
                    isfile(file_exists(path + "Languages/English/Strings")):
                print("В " + (path if path != "" else "/") + " cуществует /Languages/English/Strings")
                copytree(path + "Languages/English/Strings", "_Translation/Languages/"
                                + Language + "/Strings",
                                symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)
                print("Копирование в _Translation/Languages/" + Language + "/Strings")
            else:
                print("В " + (path if path != "" else "/") + " не найдено /Languages/English/Strings")
                ''' Проверка Keyes в других языках '''
                if glob(path + 'Languages/*/Strings'):
                    print("В " + (path if path != "" else "/") + " cуществует Languages/?/Strings")
                    path1 = str(glob(path + 'Languages/*/Strings')[0]).replace("//", "/").replace("\\", "/")
                    copytree(path1, "_Translation/Languages/"
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
        shcopy(src_path, dst_path)
        with open('loadFolders.xml', 'r', encoding="utf-8") as xml_file:
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
                copytree(path + "Defs", "_Translation/" + path + "/Languages/"
                                + Language + "/Defs_to_translate",
                                symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)
                print("Копирование в _Translation/" + path + "/Languages/" + Language + "/Defs_to_translate")
                pathes_to_DeftoTranslate.append((os.path.normpath(("_Translation/" + path + "/Languages/" +
                                                                   Language + "/Defs_to_translate"))).replace("\\",
                                                                                                              "/"))
                print("pathes_to_DeftoTranslate = " + (os.path.normpath(("_Translation/" + path + "/Languages/" +
                                                                         Language + "/Defs_to_translate"))).replace(
                    "\\",
                    "/"))
                os.makedirs((os.path.normpath(("_Translation/" + path + "/Languages/" +
                                               Language + "/DefInjected"))).replace("\\", "/"), exist_ok=True)

            else:
                pass
                print("В " + (path if path != "" else "/") + " не найдено /Defs")

            # if file_exists(path + "Patches") and not isfile(file_exists(path + "Patches")):
            #     print("В " + (path if path != "" else "/") + " cуществует Patches")
            #     copytree(path + "Patches", "_Translation/" + path + "/Languages/"
            #                     + Language + "/Patches_to_translate",
            #                     symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)
            #     print("Копирование в _Translation/" + path + "/Languages/" + Language + "/Patches_to_translate")
            # else:
            #     pass
            #     print("В " + (path if path != "" else "/") + " не найдено /Patches")

            if file_exists(path + "Languages/English/Keyed") and not \
                    isfile(file_exists(path + "Languages/English/Keyed")):
                print("В " + (path if path != "" else "/") + " cуществует Languages/English/Keyed")
                copytree(path + "Languages/English/Keyed", "_Translation/Languages/"
                                + Language + "/Keyed",
                                symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)
                print("Копирование в _Translation/Languages/" + Language + "/Keyed")
            else:
                print("В " + (path if path != "" else "/") + " не найдено /Languages/English/Keyed")
                ''' Проверка Keyes в других языках '''
                if glob(path + 'Languages/*/Keyed'):
                    print("В " + (path if path != "" else "/") + " cуществует Languages/?/Keyed")
                    path1 = str(glob(path + 'Languages/*/Keyed')[0]).replace("//", "/").replace("\\", "/")
                    copytree(path1, "_Translation/Languages/"
                                    + Language + "/Keyed",
                                    symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)
                    print("Копирование в _Translation/Languages/" + Language + "/Keyed")
                else:
                    pass
                    print("В " + (path if path != "" else "/") + " не найдено /Languages/?/Keyed")

            if file_exists(path + "Languages/English/Strings") and not \
                    isfile(file_exists(path + "Languages/English/Strings")):
                print("В " + (path if path != "" else "/") + " cуществует /Languages/English/Strings")
                copytree(path + "Languages/English/Strings", "_Translation/Languages/"
                                + Language + "/Strings",
                                symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)
                print("Копирование в _Translation/Languages/" + Language + "/Strings")
            else:
                print("В " + (path if path != "" else "/") + " не найдено /Languages/English/Strings")
                ''' Проверка Keyes в других языках '''
                if glob(path + 'Languages/*/Strings'):
                    print("В " + (path if path != "" else "/") + " cуществует Languages/?/Strings")
                    path1 = str(glob(path + 'Languages/*/Strings')[0]).replace("//", "/").replace("\\", "/")
                    copytree(path1, "_Translation/Languages/"
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
            # print("     Файлы:")
            for name in files:
                # print("Имя:")
                # print(name.replace('\\', '/'))
                files_to_translate_name.append(name.replace('\\', '/'))
                # print("Путь:")
                # print(path.replace('\\', '/'))
                # print("Путь + Имя:")
                files_to_translate.append((os.path.join(path, name)).replace("\\", "/"))
                # print(os.path.join(path, name).replace('\\', '/'))
                pth = path.partition("/Defs_to_translate")[0] + "/DefInjected"
                # print("Путь к папке с переводом (Далее добавится папка типа Defs)")
                # print(pth)
                files_to_translate_path.append(pth)
        # print("----------")
    print("---------------------------------------------------------------------------------------------------------")
    print("--Начало чтения из файлов--")

    Go_search_Name_class(files_to_translate)
    print("---------------------------------------------------------------------------------------------------------")
    print("---------------------------------------------------------------------------------------------------------")
    print("---------------------------------------------------------------------------------------------------------")
    # for i in Parent_elem:
    #     for j in i:
    #         ET.dump(j)

    # print("----_____----")
    # print("Name of attrib_name: " + "\nName of attrib_name: ".join(Name_class_name))
    # print("----_____----")

    for fl_idx, fil in enumerate(files_to_translate):
        try:
            print("     Чтение из " + fil)
            with open(fil, 'r', encoding="utf-8") as xml_file:
                tree = ET.parse(xml_file)
            # tree = ET.parse(fil)
            print("File:  " + files_to_translate_name[fl_idx])
            root = tree.getroot()
            # ET.dump(root)
            print("Добавление элементов из родителей")
            adding_elems_into_root_by_Parent_elem(root)
            # ET.dump(root)
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
                print("----------------Try CREATE FILE-----------------------")
                print("Old File name: " + file_name)
                print("Old Full path:" + file_full_path)
                print("File name:    " + file_name1)
                print("New catrgoty: " + file_path1)
                file_path_plus_name = file_path1 + "/" + file_name1 + ".xml"
                print("New name/path:" + file_path_plus_name)
                if file_exists(file_path_plus_name):
                    with open(file_path_plus_name, "r", encoding="utf-8") as Write_file:
                        old_txt = Write_file.read()
                        old_txt = old_txt.replace('\n</LanguageData>', '')
                        text = [old_txt, "<!--" + file_full_path.replace(
                            '_Translation', "").replace(
                            '/Languages/' + Language + "/Defs_to_translate", "/Defs")
                                + "-->"]
                        for f2 in Folder_and_text_1:
                            if f2[0] == f1:
                                if Add_comment:
                                    comm = sub('<.+?>(.*)</.+?>', '<!-- \\1 -->', f2[1].replace('\n', '\\n'))
                                    comm = comm.replace('\\n', '\n')
                                    text.append(comm)
                                text.append(f2[1])
                        text.append('\n</LanguageData>')
                else:
                    text = ['<?xml version="1.0" encoding="utf-8"?>', '<LanguageData>',
                            "<!--" + file_full_path.replace(
                                '_Translation', "").replace(
                                '/Languages/' + Language + "/Defs_to_translate", "/Defs")
                            + "-->"]
                    for f2 in Folder_and_text_1:
                        if f2[0] == f1:
                            if Add_comment:
                                lenth_of_path = len(f2[1].partition(">")[0]) - 4
                                comm = " " * lenth_of_path + sub('<.+?>(.*)</.+?>', '<!-- \\1 -->',
                                                                    f2[1].replace('\n', '\\n'))
                                comm = comm.replace('\\n', '\n')
                                text.append(comm)

                            text.append(f2[1])
                    text.append('\n</LanguageData>')
                os.makedirs(file_path1, exist_ok=True)
                with open(file_path_plus_name, "w", encoding="utf-8") as Write_file:
                    for l1 in text:
                        print(l1)
                        Write_file.write("%s\n" % l1)

                print("     End of Folder       ")
                print("----------------------------")

            # print('\n'.Folder_and_text_1[0])
            # print('\n'.join(Folder_and_text_1[1]))
        except ET.ParseError:
            print("|||--ERROR--|||      " + "Error in file:     " +
                  fil.partition("_Translation/")[2].replace("Defs_to_translate", "Defs"))
            Error_parse_error(fil.partition("_Translation/")[2].replace("Defs_to_translate", "Defs")
                              .replace("Languages/" + Language + "/", ""))
            # Error_log.append("Ошибка чтения" + fil.partition("_Translation/")[2].replace("Defs_to_translate", "Defs"))
            print("Пропуск файла")
            # input("Press Enter to continue")
            print("--------------------------------------")
            pass

    pathes_to_DeftoTranslate1 = set(pathes_to_DeftoTranslate)
    for p1 in pathes_to_DeftoTranslate1:
        # Error_log.append("Путь к удалению " + p1)
        rmtree(p1, ignore_errors=False, onerror=Error_delete_path_def_to_trans)

    print("--------------------------------------")
    root2 = '_Translation'
    print("Удаление пустых папок")
    delete_empty_folders(root2)

    """
    Проверка loadFolders на наличие папок
    """
    if file_exists('loadFolders.xml'):
        with open('loadFolders.xml', 'r', encoding="utf-8") as xml_file:
            tree1 = ET.parse(xml_file)
        root1 = tree1.getroot()
        pathes = []
        removable_element = []
        for version in root1:
            # ET.dump(version)
            for li in reversed(version):
                # ET.dump(li)
                if li.text == "/":
                    # print("Пропуск _Translation/" + li.text)
                    pass
                else:
                    # print("Папка существует =" + str(file_exists("_Translation/" + li.text)))
                    if not file_exists("_Translation/" + li.text):
                        print("Папка не существует _Translation/" + li.text + "\n Удаление")
                        version.remove(li)
                    # else:
                    #     # print("Папка существует _Translation/" + li.text)
                    #     pass

        #         version.remove(re)
        tree1.write('_Translation/loadFolders.xml')

    print("----------------------------------------------")
    print("----------------------------------------------")
    print("----------------------------------------------")
    print("Copy patches")

    full_path_to_label_patch = []
    patch_fullname = []
    shpfiles = []

    for dirpath, subdirs, files in os.walk("."):
        for x in subdirs:
            if x == "Patches":
                shpfiles.append((dirpath + "/" + x).replace("\\", "/").replace("./", ""))

    for s in shpfiles:
        for path, subdirs, files in os.walk(s):
            for name in files:
                patch_fullname.append(os.path.join(path, name).replace("\\\\", "/").replace("\\", "/"))
    print(patch_fullname)

    for paf in patch_fullname:
        with open(paf, 'r', encoding="utf-8") as xml_file:
            tree = ET.parse(xml_file)
        root = tree.getroot()
        for label in list_of_labels_list:
            for a in root.iter(label):
                if any(paf == c for c in full_path_to_label_patch):
                    pass
                else:
                    full_path_to_label_patch.append(paf)

    for idx, a in enumerate(full_path_to_label_patch):
        print(a)
        src_path = a
        dst_path = "_Translation/" + a.rpartition("/")[0]
        dst_path = dst_path.replace("Patches", "_Patches")
        print("Путь: " + dst_path)
        os.makedirs(dst_path, exist_ok=True)
        shcopy(src_path, dst_path)
        print('Copied')

    make_about_folder()
    if Error_log:
        with open('_Translation/Error_log.txt', 'w', encoding="utf-8") as er_log:
            for el in Error_log:
                er_log.write(el + "\n")

    print("----------------------------------------------")
    print("All done")
    # input("Press Enter to exit")


if __name__ == '__main__':
    main()

# TODO: Поправить <> в Color и остальном
