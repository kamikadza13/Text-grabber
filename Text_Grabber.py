# -*- coding: utf-8 -*-
import copy
import ctypes
import glob
import html
import os
import re
import shutil
import threading
import xml.etree.ElementTree as ET
from ctypes import windll
from dataclasses import dataclass
from html import escape
from logging import warning
from os.path import exists as file_exists
from re import match
from re import sub
from shutil import copy as shcopy
from shutil import copytree
from shutil import rmtree
from tkinter import Button
from tkinter import filedialog

import icecream
import lxml.etree as etree
import pyperclip
import ttkbootstrap
import ttkbootstrap as ttk_boot
from lxml.etree import XMLParser
from pathvalidate import sanitize_filename
from printy import printy, escape as printy_escape
from result import Ok, Err, is_ok, is_err
from ttkbootstrap.dialogs import Messagebox

import Check_New_Version
import Loadfolder_module
import Text_grabber_settings
import image_edit
from text2 import parent_folders

# from print_color import print

Version_of_Text_grabber = "1.3.5"

global exitString
global folder
global exitString1
global list_of_forbidden_character_in_label1

icecream.install()

# ic.disable()

class CheckboxGloabal:
    def get(self):
        pass

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

    a = printy_escape(str(string))
    return a



#   Текст startwith через regex - значит нужно экранировать спец символы типа $
tag_endwith_skip = ['\\nodes\\Set\\name', ]
text_startwith_skip = ['RGB', r'\$', ]





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


Parent_Name_list = []
Parent_Name_list_that_has_parent = []
Parent_elem = []
Error_log = []


class FoldersProg:
    prog = os.path.realpath(__file__).partition("_internal")[0].rpartition("\\")[0]
    mod = ''


pathes_to_parent_folders = []


#  ----------------------------------
#  ----------------------------------



Window_Text_grabber = ttkbootstrap.Window
Window_settings_app = ttkbootstrap.Window
New_Name = 'Default mod name'



S = Text_grabber_settings.SettingsValues



def update_settings():

    global Window_Text_grabber

    global S
    S = Text_grabber_settings.update_settings_new(Window_Text_grabber)

    printy("Settings updated", 'n')



def adding_elems(root1: ET.Element, elem: ET.Element, first_time_called=True):
    # print(f"Добавляется элемент: {elem.tag} в {root1.tag}")
    if root1.get('Inherit') != 'False':
        if first_time_called:
            tag_elem = root1.find(elem.tag)
            if tag_elem is None:
                root1.insert(0, copy.deepcopy(elem))
            else:
                # print("adding Tag exist in root")
                if len(elem):
                    for a in elem:
                        tag_elem.insert(0, copy.deepcopy(a))
                else:
                    # print("No childs")
                    if tag_elem.text is None:
                        if elem.text is not None:
                            print(f"\tReplace text of element that has child")
                            tag_elem.text = elem.text

        # if root1.find(elem.tag) is None:
        #     if first_time_called:
        #         root1.append(copy.deepcopy(elem))
        #     else:
        #         root1.insert(0, copy.deepcopy(elem))
        # else:
        #     for e in elem:
        #         adding_elems(root1.find(elem.tag), e, False)
    #     else:
    #     # print(f"Элемент {elem.tag} существует в {root1.tag} {root1.attrib}")
    #     if elem.tag != "li":
    #         for e in elem:
    #             adding_elems(root1.find(elem.tag), e, False)
    #     else:
    #
    #         # print(f"Нужно добавить <li>, когда <li> уже есть в {root1.tag}")
    #         if len(elem):
    #             # print(Добавляемый <li> элемент имеет наследников)
    #             if root1.find(elem.tag):
    #                 for e in elem:
    #                     adding_elems(root1.find(elem.tag), e, False)
    #             else:
    #                 # print("В руте нет наследников")
    #                 root1.insert(0, copy.deepcopy(elem))
    #         else:
    #             # print("У <li> нет детей")
    #             if not any(x1.text == elem.text for x1 in root1):
    #                 root1.insert(0, copy.deepcopy(elem))
    #             else:
    #                 print(f"li с текстом {elem.text} уже есть в {root1.tag}")
    #                 pass

ruleFiles_list = {}

"""
Если файл в моде существует в 2х экземплярах, то берется в таком порядке:
папка версий, потом Common потом '/' 
Но в проге обратный порядок т.к. файлы будут заменять друг-друга...
хм... а вообще не будут, и будет создаваться копии, но в разных папках
ну и пофиг.

Может быть стоит запилить проверку чтобы не было одинаковых файлов... в папке версий, потом Common потом '/' 
"""


def main(Entered_path_to_mod="", Floodgauge: ttk_boot.Floodgauge = ttk_boot.Floodgauge):
    def is_version(string: str):
        if match(r"^\d+\.\d+$", string):
            return True
        else:
            return False

    def change_to_mod_dir(Entered_path_to_mod_2):

        if Entered_path_to_mod_2 == "":
            folder_selected = os.path.normpath(filedialog.askdirectory(title="Select MOD folder"))
            if folder_selected  == ".":
                exit_prog()

            if not folder_selected:
                exit_prog()
            Entered_path_to_mod_2 = folder_selected

        print(f"change_dir: {Entered_path_to_mod_2}")

        FoldersProg.mod = Entered_path_to_mod_2
        os.chdir(FoldersProg.mod)
    change_to_mod_dir(Entered_path_to_mod)

    Window_Text_grabber.Enter_textbox.delete(0, 'end')
    Window_Text_grabber.Enter_textbox.insert(0, FoldersProg.mod)

    shutil.rmtree('_Translation', ignore_errors=True)
    printy('Loadfolder_module', 'n')
    Loadfolder_module.main(S.Game_language)
    printy('Loadfolder_module... Done', 'n')
    print()


    #   TODO: rewrite all Loadfolder and parent adding

    files_to_translate = Loadfolder_module.files_to_translate_path
    files_to_translate_name = Loadfolder_module.files_to_translate_name
    files_to_translate_path = Loadfolder_module.files_to_translate_new_path

    def Go_search_Name_class(list_of_files: list):
        def parent_append(root11: ET.Element):
            for Defs in root11:
                elems = []
                # ET.dump(r)
                name = Defs.get("Name")
                if name is not None:
                    # print(f"Есть имя {name}")
                    if 'ParentName' in Defs.keys():
                        par_name = Defs.get("ParentName")
                        # print(f"Есть родитель {par_name} у {name}")
                    else:
                        par_name = "none"
                    for elemets in Defs:
                        # print(f'добавляется элемент {elemets.tag}  {elemets.text}')
                        elems.append(elemets)
                    if name not in Parent_Name_list:  # Parent_Name_list - список имен родителей
                        # print(f"{name} не в Parent_Name:{Parent_Name}")
                        Parent_Name_list.append(name)
                        Parent_Name_list_that_has_parent.append(par_name)
                        Parent_elem.append(Defs)
                    else:
                        ...

                        # print(f"Попытка добавить новое имя в Parent_Name но,\nв списке родителей"
                        #       f" {Parent_Name_list} уже есть имя {name} с индексом {Parent_Name_list.index(name)}")

                        # Error_log.append(f"Попытка добавить новое имя в Parent_Name но,\nв списке родителей"
                        #                  f" {Parent_Name_list} уже есть имя {name} с индексом {Parent_Name_list.index(name)}."
                        #                  f""
                        #                  f"Для этого случая код я закомментил, потому, что посчитал лишним.\n-------\n\n")

                        # indx = Parent_Name.index(name)
                        # add_elems_into_list(Parent_elem[indx], elems)

        for idx_1, fi_w_name in enumerate(list_of_files):
            try:
                good_parent = False
                if "\\Patches\\" not in fi_w_name:
                    if not fi_w_name.endswith("loadFolders.xml"):
                        if "\\Patches\\" not in fi_w_name:
                            if "\\Defs\\" in fi_w_name:
                                good_parent = True
                            elif fi_w_name.startswith('Defs\\'):
                                good_parent = True
                if good_parent:
                    # print("     Чтение из " + fi_w_name)
                    with open(fi_w_name, 'r', encoding="utf-8") as xml_f:
                        tree_name = ET.parse(xml_f)
                    # print("File:  " + files_to_translate_name[idx_1])
                    root_name = tree_name.getroot()
                    parent_append(root_name)
            except ET.ParseError:
                printy(fr"[r]\[ERROR\]@ Не открывается файл {escape_printy_string(fi_w_name)}", predefined='<m')

                Error_log.append(f"Не открывается файл {fi_w_name}")


    Go_search_Name_class(files_to_translate)
    parent_files_path = []

    os.chdir(FoldersProg.mod)


    Floodgauge['value'] = 10
    printy("Checking parents", 'n')

    def add_parent_foler_path_from_path(parent_files_path2: list, adding_pathes: list):
        for parent_path in adding_pathes:
            if not file_exists(parent_path):
                printy(fr"[r]\[ERROR\]@ Path to parent {escape_printy_string(parent_path)} did not exist", predefined='<m')

                # Error_log.append(f"Path to parent {parent_path} did not exist\n\n")
            for path, subdirs, files in os.walk(os.path.normpath(parent_path)):
                for file in files:
                    if file.endswith('.xml'):
                        parent_files_path2.append(path + "\\" + file)

    if S.Path_to_Data and file_exists(S.Path_to_Data):
        add_parent_foler_path_from_path(parent_files_path, [S.Path_to_Data])

    if file_exists("About\\About.xml"):
        p_folders_ = []
        if S.Path_to_Mod_folder and file_exists(S.Path_to_Mod_folder):
            mod_folder_par = parent_folders(S.Path_to_Mod_folder, "About\\About.xml")
            if mod_folder_par:
                p_folders_.extend(mod_folder_par)
        if S.Path_to_Another_folder and file_exists(S.Path_to_Another_folder):
            another_folder_par = parent_folders(S.Path_to_Another_folder, "About\\About.xml")
            if another_folder_par:
                p_folders_.extend(another_folder_par)

        if p_folders_:
            add_parent_foler_path_from_path(parent_files_path, p_folders_)

    printy("Checking parents... Done", 'n')
    print()
    Floodgauge['value'] = 20

    Go_search_Name_class(parent_files_path)

    # Patch_grabber.set_parents_list(Parent_Name_list, Parent_elem)
    Floodgauge['value'] = 30

    def copy_patches():
        printy("Copy patches", 'n')
        patch_fullpath = []
        patch_new_fullpath = []
        # ic(Loadfolder_module.path_to_Patch)
        # print(Loadfolder_module.path_to_Patch)
        for path_of_patch_folder in Loadfolder_module.path_to_Patch:
            for path, subdirs, files in os.walk(
                    "Patches" if path_of_patch_folder == "" else path_of_patch_folder + "\\Patches"):
                for name in files:
                    if name.endswith(".xml"):
                        # TODO: коммент попытка в патчи
                        patch_fullpath.append(os.path.join(path, name))
        full_path_to_label_patch = []
        if patch_fullpath:
            print('\t', end='')
            print('\t'.join(patch_fullpath))
        for inx, patch_path in enumerate(patch_fullpath):
            try:
                with open(patch_path, 'r', encoding="utf-8") as xml_file:
                    tree = ET.parse(xml_file)
                root = tree.getroot()
                for label in S.Tags_to_extraction:
                    for _ in root.iter(label):
                        if any(patch_path == c for c in full_path_to_label_patch):
                            pass
                        else:
                            full_path_to_label_patch.append(patch_path)
                            patch_new_fullpath.append("_Translation\\" + str(
                                patch_path.replace("\\Patches\\", "\\_Patches_to_translate\\").rpartition("\\")[0]))
            except ET.ParseError:
                Error_log.append("Ошибка чтения " + patch_path + "\n\n")

        for idx, patch in enumerate(full_path_to_label_patch):
            with open(patch, 'r', encoding="utf-8") as xml_file:
                tree = ET.parse(xml_file)
            root = tree.getroot()
            operations = root.findall("Operation")
            operations_to_delete = []
            for operation in operations:
                bool_delete = True
                for label in S.Tags_to_extraction:
                    b = list(operation.iter(label))
                    if b:
                        bool_delete = False
                        break
                if bool_delete:
                    operations_to_delete.append(operation)
            operations_to_delete = set(operations_to_delete)

            for o_t_d in operations_to_delete:
                root.remove(o_t_d)
            dst_path = patch_new_fullpath[idx]
            os.makedirs(dst_path, exist_ok=True)
            with open(dst_path + "\\" + str(patch.rpartition("\\")[2]), 'wb') as xml_file:
                tree.write(xml_file, encoding="utf-8")
        printy("Copy patches... Done",'n')
        print()

    copy_patches()

    def update_Parent_Name_elems(Parent_Name1, Parent_Name_that_has_parent1, Parent_elem1):
        printy('Update_Parent_Name_elems', 'n')
        for i, pn in enumerate(Parent_Name_that_has_parent1):
            if pn != "none":
                if pn not in Parent_Name1:
                    # Error_log.append(f"Есть родитель {pn}, но он не найден родитель\nУбираем родителя из списка\n--------")
                    # print(f"Есть родитель {pn}, но он не в списке Parent_Name1\nУбираем родителя из списка")
                    Parent_Name_that_has_parent1[i] = "none"
        # print_Name_parent_elem()
        while True:
            for i, pn in enumerate(Parent_Name_that_has_parent1):
                if pn != "none":
                    if pn in Parent_Name1:  # Если родитель есть в листе имен
                        # print(f"У {Parent_Name1[i]} Есть родитель {pn}, и он в списке Parent_Name1")
                        j = Parent_Name1.index(pn)
                        if Parent_Name_that_has_parent1[j] == "none":
                            # print(f"Есть родитель {pn}, и у него нет родителя")
                            # print(Parent_elem1[j])
                            # print(Parent_Name1[j])
                            # print(f"Попытка добавить {[x.tag for x in Parent_elem1[j]]} в {Parent_Name1[j]}")
                            for elems in reversed(Parent_elem1[j]):
                                adding_elems(Parent_elem1[i], elems)
                            # Parent_elem1[i] = add_elems_into_list(Parent_elem1[i], Parent_elem1[j])
                            # print(f"Удаляем у {Parent_Name1[i]} родителя {Parent_Name_that_has_parent1[i]}")
                            Parent_Name_that_has_parent1[i] = "none"
                    else:
                        Error_log.append(f"Has parent - {pn}, but it isn't in list\nremove parent from list\n--------\n\n")
                        printy(
                            fr"[r]\[ERROR\]@ Has parent - {escape_printy_string(pn)}, but it isn't in list\nremove parent from list",
                            predefined='<m')
                        Parent_Name_that_has_parent1[i] = "none"

            # print_Name_parent_elem()

            if all(p == "none" for p in Parent_Name_list_that_has_parent):
                break
        printy('Update_Parent_Name_elems... Done', 'n')
        print()

    update_Parent_Name_elems(Parent_Name_list, Parent_Name_list_that_has_parent, Parent_elem)


    printy('Reading Files...', '<o')
    print('\t', end='')
    print('\t'.join(files_to_translate))
    printy('Reading Files... Done', '<o')
    print()

    def finish_string(tree2) -> (list[FolderDefnamePathText], list[tuple] | None):
        XmlExtensions_Keyed = []

        def print_path_of_elems(elem: ET.Element, root3: ET.Element, elem_path="", first_time_start=False):
            def RulePackDef_def(rulePackDef: ET.Element):
                global ruleFiles_list
                defName_ET = rulePackDef.find('defName')
                if defName_ET is not None:
                    defname = defName_ET.text
                else:
                    return
                rulesFiles_ET = list(rulePackDef.iter('rulesFiles'))
                if rulesFiles_ET:
                    rulesFiles_ET = rulesFiles_ET[0]
                    for li in rulesFiles_ET:
                        a = li.text
                        b = a.partition("-")[0]
                        if not ruleFiles_list.get(defname):
                            ruleFiles_list[defname] = []
                        ruleFiles_list[defname].append((b, li))

                include = []
                include_ET = list(rulePackDef.iter('include'))
                if include_ET:
                    include_ET = include_ET[0]
                    for li in include_ET:
                        include.append(li.text)

                rulesStrings_ET = list(rulePackDef.iter('rulesStrings'))
                if rulesStrings_ET:
                    rulesStrings_ET = rulesStrings_ET[0]
                if include:
                    if not rulesFiles_ET:
                        rulesFiles = ET.Element('rulesFiles')
                    else:
                        rulesFiles = rulesFiles_ET
                    rulePackDef.insert(1, rulesFiles)

                    if not rulesStrings_ET:
                        rulesStrings_ET = ET.SubElement(rulePackDef, 'rulesStrings')
                    for defname_ in include:
                        if defname_ in ruleFiles_list:
                            for line in ruleFiles_list[defname_]:
                                if f'[{line[0]}]'.encode() in ET.tostring(rulesStrings_ET, method='xml'):
                                    rulesFiles.append(copy.deepcopy(line[1]))

            def BodyDef_rename_li(BodyDef: ET.Element):
                def parts_li_tag_rename(el: ET.Element):
                    parts = el.find('parts')
                    if parts is not None:
                        for li in parts:
                            customLabel = li.find('customLabel')
                            if customLabel is not None:
                                if customLabel.text is not None:
                                    li.tag = customLabel.text.replace(" ", "_").replace("-", "")
                            parts_li_tag_rename(li)

                corePart = BodyDef.find('corePart')
                if corePart is not None:
                    parts_li_tag_rename(corePart)

            def pawnKind_add_strings(elem: ET.Element):
                add_elem = []
                a = [elem]
                b = elem.find('lifeStages')
                orig_label_text = ''

                def get_label(elem_to_get_label: ET.Element):
                    _ = elem_to_get_label.find('label')
                    if _ is not None:
                        return str(elem.find('label').text)
                    return ""

                if b is not None:
                    for li in b:
                        if li is not None:
                            a.append(li)
                orig_label_text = get_label(elem)
                for els in a:
                    label_text = get_label(els)
                    if not label_text:
                        label_text = orig_label_text
                    if label_text:
                        for idx_, l_pawn in enumerate(S.list_pawn_tag):
                            add_elem.append(ET.Element(l_pawn))
                            if els.find(l_pawn) is None:
                                els.append(add_elem[idx_])
                                txt = str(l_pawn.partition("label")[2])
                                # print(txt)
                                txt = txt.replace('ePlural', 'e Plural')
                                # print(txt)
                                add_elem[idx_].text = txt + " " + label_text

            def ScenarioDef_add_strings(elem: ET.Element):
                if elem.find('scenario') is not None:
                    scenario = elem.find('scenario')
                    # print(f"Есть ветка scenario")
                    if scenario.find("name") is None:
                        label = elem.find("label")
                        if label is not None:
                            scenario_name = ET.SubElement(scenario, 'name')
                            scenario_name.text = label.text

                    if scenario.find("description") is None:
                        description = elem.find("description")
                        if description is not None:
                            scenario.append(description)
                else:
                    print(f"Нет ветки scenario???")
                    label = elem.find("label")
                    scenario = ET.SubElement(elem, "scenario")
                    if label is not None:
                        scenario_name = ET.SubElement(scenario, 'name')
                        scenario_name.text = label.text
                    description = elem.find("description")
                    if description is not None:
                        scenario.append(description)

            def DamageDef_add_strings(elem: ET.Element):
                if elem.find("deathMessage") is None:
                    if 'ParentName' in elem.attrib:
                        deathMessage = ET.SubElement(elem, "deathMessage")
                        a_00 = elem.attrib['ParentName']
                        if S.Game_language == "Russian":
                            match a_00:
                                case "Flame":
                                    deathMessage.text = "{0} был сожжен до смерти."
                                case "CutBase":
                                    deathMessage.text = "{0} был зарезан насмерть."
                                case "BluntBase":
                                    deathMessage.text = "{0} был избит до смерти."
                                case "Scratch":
                                    deathMessage.text = "{0} был растерзан до смерти."
                                case "Bite":
                                    deathMessage.text = "{0} был искусан до смерти."
                                case "Bomb":
                                    deathMessage.text = "{0} погиб при взрыве."
                                case "Arrow":
                                    deathMessage.text = "{0} был застрелен стрелой."
                                case _:
                                    deathMessage.text = "{0} был убит."
                        else:
                            match a_00:
                                case "Flame":
                                    deathMessage.text = "{0} has burned to death."
                                case "CutBase":
                                    deathMessage.text = "{0} has been cut to death."
                                case "BluntBase":
                                    deathMessage.text = "{0} has been beaten to death."
                                case "Scratch":
                                    deathMessage.text = "{0} has been torn to death."
                                case "Bite":
                                    deathMessage.text = "{0} has been bitten to death."
                                case "Bomb":
                                    deathMessage.text = "{0} has died in an explosion."
                                case "Arrow":
                                    deathMessage.text = "{0} has been shot to death by an arrow."
                                case _:
                                    deathMessage.text = "{0} has been killed."

            def comps_Li_Class_Replace(Def: ET.Element):
                comps = Def.find("comps")
                if comps is not None:
                    for li in comps:
                        compClass = li.find("compClass")
                        if compClass is not None:
                            # print(f"{Def.tag}:")
                            # print(f"Replace <li> by compClass {compClass.text}")
                            li.tag = compClass.text
                            if li.get("Class") is not None:
                                li.set('Class', "Li_Class_Replaced_by_compClass")

            def add_missing_verbs_if_verbClass(Def: ET.Element):
                verbs = Def.find("verbs")
                if verbs is not None:
                    for li in verbs:
                        verb_label = li.find("label")
                        if verb_label is None:
                            verb_Class = li.find("verbClass")
                            if verb_Class is not None:
                                verbs_new_verb_class = ET.SubElement(verbs, verb_Class.text)
                                if Def.find('label'):
                                    verb_new_label_text = Def.find('label').text
                                    if verb_new_label_text is not None:
                                        verb_new_label = ET.SubElement(verbs_new_verb_class, 'label')
                                        verb_new_label.text = verb_new_label_text

            def ThingDef_add_strings(elem: ET.Element):
                if S.Add_stuffAdjective_and_mark_it:

                    stuffProps = elem.find("stuffProps")
                    if stuffProps is not None:
                        categories = stuffProps.find("categories")
                        if categories is not None:
                            if elem.find("label") is not None:
                                label = elem.find("label").text
                            else:
                                label = "material"
                            a = stuffProps.find('stuffAdjective')
                            if a is None:
                                stuffAdjective = ET.SubElement(stuffProps, "stuffAdjective")

                                stuffAdjective.text = S.Add_stuffAdjective_and_mark_it_text.replace('~LABEL~', label)
                            else:
                                orig_text = a.text
                                a.text = S.Add_stuffAdjective_and_mark_it_text.replace('~LABEL~', orig_text)

            def add_title_short(Def: ET.Element):
                backstory = Def.find("backstory")
                if backstory is None:
                    backstory = ET.SubElement(Def, 'backstory')

                    baseDesc = Def.find("baseDesc")
                    if baseDesc is not None:
                        backstory_baseDesc = ET.SubElement(backstory, 'baseDesc')
                        backstory_baseDesc.text = baseDesc.text
                    else:
                        baseDescription = Def.find("baseDescription")
                        if baseDescription is not None:
                            backstory_baseDesc = ET.SubElement(backstory, 'baseDesc')
                            backstory_baseDesc.text = baseDescription.text
                    title = Def.find('title')
                    if title is not None:
                        backstory_title = ET.SubElement(backstory, 'title')
                        backstory_title.text = title.text
                    titleShort = Def.find('titleShort')
                    if titleShort is not None:
                        backstory_titleShort = ET.SubElement(backstory, 'titleShort')
                        backstory_titleShort.text = titleShort.text
                    else:
                        titleShort = ET.SubElement(Def, 'titleShort')
                        titleShort.text = title.text[:12]
                        backstory_titleShort = ET.SubElement(backstory, 'titleShort')
                        backstory_titleShort.text = titleShort.text
                else:
                    backstory_baseDesc = backstory.find("baseDesc")
                    if backstory_baseDesc is None:
                        baseDesc = Def.find("baseDesc")
                        if baseDesc is not None:
                            backstory_baseDesc = ET.SubElement(backstory, 'baseDesc')
                            backstory_baseDesc.text = baseDesc.text
                        else:
                            baseDescription = Def.find("baseDescription")
                            if baseDescription is not None:
                                backstory_baseDesc = ET.SubElement(backstory, 'baseDesc')
                                backstory_baseDesc.text = baseDescription.text

                    backstory_title = backstory.find('title')
                    if backstory_title is None:
                        title = Def.find("title")
                        if title is not None:
                            backstory_title = ET.SubElement(backstory, 'title')
                            backstory_title.text = title.text

                    backstory_titleShort = backstory.find('titleShort')
                    if backstory_titleShort is not None:
                        print(backstory_titleShort.tag)
                        print(backstory_titleShort.text)
                    if backstory_titleShort is None:
                        titleShort = Def.find("titleShort")
                        if titleShort is not None:
                            backstory_titleShort = ET.SubElement(backstory, 'titleShort')
                            backstory_titleShort.text = titleShort.text

                if S.add_titleFemale:
                    titleFemale = Def.find('titleFemale')
                    if titleFemale is None:
                        title = Def.find('title')
                        if title is not None:
                            titleFemale = ET.SubElement(Def, 'titleFemale')
                            titleFemale.text = title.text
                    backstory_titleFemale = backstory.find('titleFemale')
                    if backstory_titleFemale is None:
                        backstory_titleFemale = ET.SubElement(backstory, 'titleFemale')
                        backstory_titleFemale.text = titleFemale.text

                if S.add_titleShortFemale:
                    titleShortFemale = Def.find('titleShortFemale')
                    if titleShortFemale is None:
                        titleShort = Def.find("titleShort")
                        if titleShort is not None:
                            titleShortFemale = ET.SubElement(Def, 'titleShortFemale')
                            titleShortFemale.text = titleShort.text
                        else:
                            title = Def.find('title')
                            if title is not None:
                                titleShortFemale = ET.SubElement(Def, 'titleShortFemale')
                                if len(title.text) < 13:
                                    titleShortFemale.text = title.text
                                else:
                                    titleShortFemale.text = title.text[:12]

                        backstory_titleShortFemale = backstory.find('titleShortFemale')
                        if backstory_titleShortFemale is None:
                            backstory_titleShortFemale = ET.SubElement(backstory, 'titleShortFemale')
                            backstory_titleShortFemale.text = titleShortFemale.text

            def BackstoryDef_add_title_short(Def: ET.Element):
                if S.add_titleFemale:
                    titleFemale = Def.find('titleFemale')
                    if titleFemale is None:
                        title = Def.find('title')
                        if title is not None:
                            titleFemale = ET.SubElement(Def, 'titleFemale')
                            titleFemale.text = title.text

                if S.add_titleShortFemale:
                    titleShortFemale = Def.find('titleShortFemale')
                    if titleShortFemale is None:
                        titleShort = Def.find("titleShort")
                        if titleShort is not None:
                            titleShortFemale = ET.SubElement(Def, 'titleShortFemale')
                            titleShortFemale.text = titleShort.text
                        else:
                            title = Def.find('title')
                            if title is not None:
                                titleShortFemale = ET.SubElement(Def, 'titleShortFemale')
                                if len(title.text) < 13:
                                    titleShortFemale.text = title.text
                                else:
                                    titleShortFemale.text = title.text[:12]

            def TraitDef_add_strings(elem: ET.Element):
                if elem.find("degreeDatas") is not None:
                    degreeDatas = elem.find('degreeDatas')
                    for li in degreeDatas:
                        if li.find("labelFemale") is None:
                            if li.find("label") is not None:
                                labelFemale = ET.SubElement(li, "labelFemale")
                                labelFemale.text = li.find("label").text

            def Tkey_system_QuestScriptDef(elem: ET.Element):
                for element in elem.iter():
                    if 'TKey' in element.attrib:
                        TKey = ET.SubElement(elem, element.attrib['TKey'])
                        element_1 = ET.SubElement(TKey, 'slateRef')
                        element_1.text = element.text
                        element.clear()

            def replace_child_li(parent: ET.Element):
                def zamena_v_li_classe(li_class_name_: str):
                    new_tag_ = ""

                    for cls in S.Li_Class_Replace:
                        # print(f"Checking {cls[0]} in {li_class_name}")
                        if li_class_name_.startswith(cls[0]):
                            new_tag_ = li_class_name_.replace(cls[0], cls[1])
                            # print('new tag =', new_tag_)
                            break
                        elif li_class_name_.rpartition(".")[2].startswith(cls[0]):
                            new_tag_ = li_class_name_.rpartition(".")[2].replace(cls[0], cls[1])
                            # print('new tag =',new_tag_)
                            break
                        else:
                            # print(f"{cls[0]} not in {li_class_name}")
                            new_tag_ = "li"
                    return new_tag_

                def li_new_tag_by_child(li_: ET.Element) -> str:
                    for child_ in li_:
                        if child_.tag == 'def':
                            return child_.text
                    return 'li'

                element2 = parent.findall('li')
                if element2:
                    # print("Изначальный элемент без земененных <li>")

                    for idx3, li in enumerate(element2):

                        # ET.dump(a1)
                        new_tag = li_new_tag_by_child(li)
                        new_tag = new_tag.replace(" ", "_")
                        if new_tag == "li":
                            li_class_name = li.get('Class')
                            if li_class_name is not None:
                                new_tag = zamena_v_li_classe(li_class_name)
                            if new_tag == "li":
                                new_tag = str(idx3)
                        new_tag = new_tag.replace(" ", "_").replace("-", "")

                        # TODO: Тут добавил замену дефиса, может быть лишней

                        li.tag = new_tag
                    # print("--Итоговый элемент с заменненными <li>--")
                    # ET.dump(parent)

            def replace_rulestring(parent: ET.Element):
                # ET.dump(parent)
                text = "\n"
                a_0 = "\t\t<li>"
                b = "</li>\n"
                for li in parent:
                    if li.tag == "li":
                        text += a_0 + li.text + b
                text += S.tags_left_spacing
                parent.clear()
                parent.text = text

            def XmlExtensions_SettingsMenuDef(elem: ET.Element):
                settings = elem.find("settings")
                if settings is not None:
                    for element in settings.iter():
                        if element.tag == "li":
                            tKey = ''
                            tKey_text = ''
                            tKeyTip = ''
                            tKeyTip_text = ''
                            for el in element:
                                match el.tag:
                                    case 'tKey':
                                        tKey = el.text
                                    case 'label':
                                        tKey_text = el.text
                                        el.tag = 'Replaced'
                                        el.clear()
                                    case 'text':
                                        tKey_text = el.text
                                        el.tag = 'Replaced'
                                        el.clear()

                                    case 'tKeyTip':
                                        tKeyTip = el.text
                                        el.tag = 'Replaced'
                                        el.clear()

                                    case 'tooltip':
                                        tKeyTip_text = el.text
                                        el.tag = 'Replaced'
                                        el.clear()

                            if tKey and tKey_text:
                                XmlExtensions_Keyed.append((tKey, html.escape(tKey_text)))
                            if tKeyTip and tKeyTip_text:
                                XmlExtensions_Keyed.append((tKeyTip, html.escape(tKeyTip_text)))

            global exitString
            # print(f'ET.Dump:{elem.tag}{elem.attrib}')
            # ET.dump(elem)
            if first_time_start:
                for child in elem:
                    tag = child.tag.partition("\\")[0]
                    if tag == "AlienRace.ThingDef_AlienRace":
                        child.tag = child.tag.replace('AlienRace.ThingDef_AlienRace', 'ThingDef')
                    # atr = child_.get('Class')
                    # if atr:
                    #     if tag != 'ThingDef':
                    #         child_.tag = atr

            if elem.tag.partition("\\")[0] == "RulePackDef":
                RulePackDef_def(elem)
            if elem.tag.partition("\\")[0] == "BodyDef":
                BodyDef_rename_li(elem)
            if elem.tag.partition("\\")[0] == "PawnKindDef":
                pawnKind_add_strings(elem)  # Если PawnKindDef, то добавить необходимые labelPlural
            if elem.tag.partition("\\")[0] == "ScenarioDef":
                ScenarioDef_add_strings(elem)  # Если ScenarioDef, то добавить ['name', 'description'] в scenario
            if elem.tag.partition("\\")[0] == "DamageDef":
                DamageDef_add_strings(elem)
            if elem.tag.partition("\\")[0] == "ThingDef":
                comps_Li_Class_Replace(elem)
                add_missing_verbs_if_verbClass(elem)
                ThingDef_add_strings(elem)
            if elem.tag.partition("\\")[0] == "AlienRace.BackstoryDef":
                add_title_short(elem)
            if elem.tag.partition("\\")[0] == "AlienRace.AlienBackstoryDef":
                add_title_short(elem)
            if elem.tag.partition("\\")[0] == "BackstoryDef":
                BackstoryDef_add_title_short(elem)
            if elem.tag.partition("\\")[0] == "TraitDef":
                TraitDef_add_strings(elem)
            if elem.tag.partition("\\")[0] == "QuestScriptDef":
                if S.Tkey_system_on:
                    Tkey_system_QuestScriptDef(elem)
            if elem.tag.partition("\\")[0] == "XmlExtensions.SettingsMenuDef":
                XmlExtensions_SettingsMenuDef(elem)

            def adding_in_string(stringa, elem_path_: str, child_: ET.Element, print_now: bool = False):


                text1 = child_.text
                text1 = escape(text1, quote=False)
                text1 = text1.replace("li&gt;", "li>")
                text1 = text1.replace("&lt;li", "<li")
                text1 = text1.replace("&lt;/li", "</li")
                text1 = text1.replace("-&gt;", "->")
                text1 = text1.replace(' -- ', ' - ')

                try:
                    _, folder_, defname, path = elem_path_.split('\\', 3)
                    path = path.replace('\\', '.') + '.' + child_.tag.replace('\\', '.')
                except ValueError:
                    _, folder_, defname = elem_path_.split('\\', 3)
                    path = child_.tag.replace('\\', '.')

                if print_now:
                    if text1.isspace():
                        return None
                    stringa.append(FolderDefnamePathText(folder_, defname, path, text1))

                    return None

                if re.match(r"\d", elem_path_.partition("Def\\")[2]):
                    Error_log.append(f"Defname start with digit - that cause XML error: {elem_path_}")
                    printy(
                        fr"Skipping string {elem_path_ + '/' + child_.tag : <75} [r]Defname start with digit - that cause XML error: {elem_path_}@",
                        predefined='<m')
                    return None

                for _ in tag_endwith_skip:
                    if f"{elem_path_}\\{child_.tag : <100}".endswith(_):
                        print(f"Skipping string {elem_path_ + '/' + child_.tag : <75} text: {text1} ", end='')
                        printy(f"[r]Tag endwith {_}@")

                        return None

                for st in text_startwith_skip:
                    if match(st, text1):
                        print(f"Skipping string {elem_path_ + '/' + child_.tag : <75} text: {text1} ", end='')
                        printy(f"[r]String starts with {escape_printy_string(st)}@")
                        return None

                if "_" in text1:
                    if " " not in text1:
                        if child_.tag in S.Tags_to_extraction:
                            if elem_path_.count("\\") < 2:  # Проверка пути, есть ли там, что-то кроме tag
                                return None
                            if elem_path_.rpartition('\\')[0] == "comps":
                                printy(f"[r] VERY Strange string : {elem_path_}", end="")
                                print(f'{child_.tag} {text1}')
                                stringa.append(FolderDefnamePathText(folder_, defname, "", text1))

                            else:
                                stringa.append(FolderDefnamePathText(folder_, defname, path, text1))

                        print(f"Skipping string {elem_path_ + '/' + child_.tag : <75} text: ", end='')
                        printy(escape_printy_string(text1), 'r>', end=' ')
                        printy(f"[<r]- Just one word with Underlining@")
                        return None

                if text1 in S.Forbidden_text:
                    print(f"Skipping string {elem_path_ + '/' + child_.tag : <75} ", end='')
                    printy(f"[r]Forbidden text: @", end='')
                    printy(escape_printy_string(text1), 'r>')
                    return None

                for fp in S.Forbidden_part_of_path:
                    ep = sub("\\\\[0-9]+\\\\", r"\\li\\", elem_path_)
                    ep = sub("\\\\[0-9]+$", r"\\li", ep)
                    if fp in ep:
                        printy(
                            f"Skipping string {elem_path_.replace(fp, '[r]' + fp + '@') + '/' + child_.tag : <75} [r]Forbidden path: '{escape_printy_string(fp)}'@")
                        return None
                for fp in S.Forbidden_part_of_tag:
                    if fp in child_.tag:
                        printy(
                            f"Skipping string {elem_path_ + '/' + child_.tag.replace(fp, '[r]' + fp + '@') : <75} text: '{escape_printy_string(text1)}' [r]Forbidden part of tag '{escape_printy_string(fp)}'@")
                        return None
                if elem_path_.count("\\") < 2:  # Проверка пути, есть ли там, что-то кроме tag
                    return None
                if elem_path_.rpartition('\\')[0] == "comps":
                    printy(f"[r] VERY Strange string : {elem_path_}", end="")
                    print(f'{child_.tag} {text1}')
                    stringa.append(FolderDefnamePathText(folder_, defname, "", text1))

                else:
                    stringa.append(FolderDefnamePathText(folder_, defname, path, text1))

            def replace_defname(child_: ET.Element):
                # warning(f"Search Defname in {child.tag}")
                a1 = child_.find('.\\defName')
                if a1 is None:
                    a1 = child_.find('.\\defname')
                if a1 is None:
                    a1 = child_.find('.\\Defname')
                if a1 is None:
                    a1 = child_.find('.\\DefName')
                if a1 is None:
                    a1 = child_.find('defName')
                if a1 is None:
                    a1 = child_.find('Defname')
                if a1 is None:
                    a1 = child_.find('DefName')
                if a1 is not None:
                    # warning(f"Find Defname {a1.text}")
                    if " " in a1.text:
                        Error_log.append(f'Replacing defName {child_.tag + "/" + a1.text}'
                                         f' to {child_.tag + "/" + a1.text.replace(" ", "_")}\n\n')
                        printy(
                            f'Replacing defName [<r]{child_.tag + "/" + escape_printy_string(a1.text)}@ to [r>]{child_.tag + "/" + escape_printy_string(a1.text.replace(" ", "_"))}@')

                        child_.tag = child_.tag + "\\" + a1.text

                    else:
                        child_.tag = child_.tag + "\\" + a1.text.replace(" ", "_")

            for child in elem:

                if 'Abstract' in child.attrib:
                    if child.attrib['Abstract'].lower() == 'true':
                        continue  # пропуск абстрактного объекта (continue переходит к следующему for)
                if not list(child) and child.text:  # Нет детей и есть текст
                    # print(f"Проверка: {child_.tag.lower()}")
                    if not child.tag.lower() in S.Forbidden_tag:  # Проверка запрещенных тэгов

                        # print(f"НЕ Запрещенный тэг: {child_.tag.lower()} не в {S.Forbidden_tag}")
                        if (not S.Check_at_least_one_letter_in_text) or any(
                                c.isalpha() for c in child.text):  # Есть хотя бы один буквенный символ
                            if any(child.tag.lower() == _.lower() for _ in
                                   S.Tags_to_extraction):  # Проверка на соответствие Tags_to_extraction
                                adding_in_string(exitString, elem_path, child)
                            elif any(b.lower() in child.tag.lower() for b in
                                     S.Part_of_tag_to_extraction):  # Проверка на не полный тэг
                                adding_in_string(exitString, elem_path, child)
                            elif " " in child.text:
                                adding_in_string(exitString, elem_path, child)
                    else:
                        pass
                        # print(f"Запрещенный тэг: {child_.tag.lower()} в {S.Forbidden_tag}")

                else:
                    replace_defname(child)

                    if child.tag.lower() in [tag.lower() for tag in S.Tags_before_li]:

                        replace_rulestring(child)
                        adding_in_string(exitString, elem_path, child, print_now=True)
                    else:

                        replace_child_li(child)
                    print_path_of_elems(child, root3, "%s\\%s" % (elem_path, child.tag))

        global exitString
        global folder
        root_finish_string = tree2.getroot()
        exitString = []
        folder = []
        print_path_of_elems(root_finish_string, root_finish_string, '', True)

        strings = (exitString,XmlExtensions_Keyed if XmlExtensions_Keyed else None)

        return strings

    printy('Writing Files...', 'c')

    for fl_idx, fil in enumerate(files_to_translate):
        try:
            Floodgauge['value'] = 30 + int(60 * (fl_idx / len(files_to_translate)))

            # print("     Чтение из " + fil)
            with open(fil, 'r', encoding="utf-8", errors='ignore') as xml_file:
                tree = ET.parse(xml_file)
            # tree = ET.parse(fil)
            root = tree.getroot()
            # print("Добавление элементов из родителей")

            def adding_elems_into_root_by_Parent_elem(root: ET.Element, file: str):
                for r in root:
                    ParentName = r.get('ParentName')
                    if ParentName is not None:
                        for inx, pn in enumerate(Parent_Name_list):
                            if pn == ParentName:
                                if r.tag != Parent_elem[inx].tag:
                                    if S.Game_language == "Russian":
                                        Error_log.append(f"Файл: {file}\n"
                                                         f"Класс родителя отличается от Класса наследника\n"
                                                         f"{r.tag} {r.attrib} and {Parent_elem[inx].tag} {Parent_elem[inx].attrib}\n"
                                                         f"Это не критическая ошибка. Но, возможно, придется переместить файл в папку, соответствующую классу родителя\n"
                                                         )
                                    else:

                                        Error_log.append(f"File: {file}\n"
                                                         f"The class of the parent differs from the class of the heir\n"
                                                         f"{r.tag} {r.attrib} and {Parent_elem[inx].tag} {Parent_elem[inx].attrib}\n"
                                                         f"That is not critical error. But you may have to move the file to the folder corresponding to the parent class.\n"
                                                         )
                                # print(f"Добавляются элменты {[x.tag for x in Parent_elem[inx]]} в:")
                                # ET.dump(r)
                                for elements_in_parent_Def in reversed(Parent_elem[inx]):
                                    adding_elems(r, elements_in_parent_Def)
                                # print(f"Рут после добавления:")
                                # ET.dump(r)
                                # print(f"{r.tag}.{r.attrib}")
            adding_elems_into_root_by_Parent_elem(root, fil)
            FDPT, XmlExtensions_Keyed = finish_string(tree)


            # print(fil)
            file_name = files_to_translate_name[fl_idx]
            file_full_path = fil
            file_path = files_to_translate_path[fl_idx]
            Folders = []
            for elem in FDPT:
                if elem.folder.lower() not in [a.lower() for a in Folders]:
                    Folders.append(elem.folder)
            if Folders:
                # print()
                printy(f"File: [y>]{escape_printy_string(fil)}@")


            # print("Начало разбивания файла на папки")
            for folder_idx, f1 in enumerate(Folders):
                file_path1 = file_path + "\\" + f1
                printy(f"{file_path1=}")


                if S.Not_rename_files:
                    file_name1 = file_name.rpartition(".xml")[0]
                else:
                    if len(file_path1 + "\\" + file_name + "_" + str(f1).rpartition('.')[2].rpartition('_')[2]) < 140:
                        file_name1 = file_name.rpartition(".xml")[0] + "_" + str(f1).rpartition('.')[2].rpartition('_')[2]
                    else:
                        printy(f'{" "*15}[y<]{escape_printy_string(f1): <20}\\{escape_printy_string(file_full_path)}@ --> [r]The path is too long@ -> Reducing filemane + counter')
                        file_name1 = file_name.rpartition(".xml")[0].rpartition(".")[2].rpartition("_")[2] + str(fl_idx) + "_" + str(folder_idx)

                file_path_plus_name = file_path1 + "\\" + file_name1 + ".xml"
                # print("New name/path:" + file_path_plus_name.partition('_Translation/')[2])

                printy(f'Folder: [y<]{escape_printy_string(f1): <20}@  File: [y<]{escape_printy_string(file_full_path)}@ --> [<y]{file_path_plus_name.partition("_Translation")[2]}@')

                if file_exists(file_path_plus_name):
                    with open(file_path_plus_name, "r", encoding="utf-8") as Write_file:
                        old_txt = Write_file.read()
                    text_start = old_txt.replace('\n</LanguageData>', '')
                else:
                    text_start = '<?xml version="1.0" encoding="utf-8"?>\n<LanguageData>'

                text_body = []
                text_end = '</LanguageData>'

                if S.Add_filename_comment:
                    text_body.append("<!--" + file_full_path.replace('_Translation', "").replace(
                        '\\Languages\\' + S.Game_language + "\\Defs_to_translate", "\\Defs") + "-->")


                add_new_line_at_new_defname_Boolean = True
                last_defname = ''

                if S.Add_new_line_next_defname:
                    last_defname = FDPT[0].defname
                    defnames = []
                    [defnames.append(elem.defname) for elem in FDPT if elem.defname not in defnames]
                    if S.Add_new_line_next_defname_treshhold:
                        if (len(defnames)/len(FDPT)) <= 0.6:
                            add_new_line_at_new_defname_Boolean = True
                        else:
                            add_new_line_at_new_defname_Boolean = False



                for elem in FDPT:

                    if elem.folder.lower() == f1.lower():

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

                            comm = f'{com_sp_before}<!--{comm_spacing} {"EN: " if S.Comment_add_EN else ""}{elem.text} -->'.replace('***_new_n_new_***', '\n')
                            if S.Comment_replace_n_as_new_line:
                                comm = comm.replace('\\n', '\n')

                            text_body.append(comm)
                        text_body.append(f"<{elem.defname}.{elem.path}>{elem.text}</{elem.defname}.{elem.path}>")

                os.makedirs(file_path1, exist_ok=True)

                with open(file_path_plus_name, "w", encoding="utf-8") as Write_file:
                    Write_file.write(f"{text_start}\n")

                    # def find_defname(index):
                    #     if index > len(text_body):
                    #         return None
                    #
                    #     for a in text_body[index:]:
                    #         if "<!--" not in a:
                    #             find = match(r"^\s*<(\S+?)\.", a)
                    #             if find:
                    #                 return find.group(1)
                    #     else:
                    #         return None
                    #
                    # now_def_nm = None
                    # next_def_nm = None
                    for idx, line in enumerate(text_body):
                        Write_file.write(f"{S.tags_left_spacing}{line}\n")

                        # if S.Add_new_line_next_defname:
                        #     now_def_nm = find_defname(idx)
                        #     next_def_nm = find_defname(idx + 1)
                        #
                        #     if (now_def_nm is not None) and (next_def_nm is not None) and now_def_nm != next_def_nm:
                        #         Write_file.write("\n")

                    Write_file.write(f"{text_end}")

                # print("     End of Folder       ")
                # print("----------------------------")

            if XmlExtensions_Keyed:
                f_name_keyed = file_name.rpartition(".xml")[0].rpartition("\\")[2] + ".xml"
                Keyed_path = f'_Translation\\Languages\\{S.Game_language}\\Keyed\\{f_name_keyed}'
                printy(f"Founed  XmlExtensions.SettingsMenuDef -> [<y]Creating Keyed file:@ [y]{escape_printy_string(Keyed_path)}")
                os.makedirs(os.path.dirname(Keyed_path), exist_ok=True)
                with open(Keyed_path, 'w', encoding='utf-8') as Keyed:
                    Keyed.write('<LanguageData>\n')
                    for i in XmlExtensions_Keyed:
                        Keyed.write(f"\t<{i[0]}>{i[1]}</{i[0]}>\n")
                    Keyed.write('\n</LanguageData>')


            if Folders:
                print()
            # print('\n'.Folder_and_text_1[0])
            # print('\n'.join(Folder_and_text_1[1]))
        except ET.ParseError:
            Error_log.append("Ошибка чтения " + fil.partition("_Translation")[2].replace("Defs_to_translate", "Defs")
                              .replace("Languages\\" + S.Game_language + "\\", "") + "\n\n")

            print("Пропуск файла")
            # input("Press Enter to continue")
            print("--------------------------------------")
            pass

    printy("Writing Files... Done", 'c')
    print()
    root2 = '_Translation'

    def delete_empty_folders(root3):
        deleted = set()
        for current_dir, subdirs2, files2 in os.walk(root3, topdown=False):
            still_has_subdirs = any(subdir for subdir in subdirs2 if os.path.join(current_dir, subdir) not in deleted)
            if not any(files2) and not still_has_subdirs:
                os.rmdir(current_dir)
                deleted.add(current_dir)

        return deleted

    try:
        delete_empty_folders(root2)
    except Exception as ex:
        printy(r'[r]\[ERROR\]@ delete_empty_folders', predefined='<m')
        Error_log.append(f"Error delete_empty_folders {ex} \n\n")
    Floodgauge['value'] = 90

    if S.Delete_old_versions_translation:
        try:
            printy("Delete old versions", 'n')
            folders_in__translation = glob.glob("_Translation\\*\\", recursive=False)
            folders_name_in__translation = [sub('_Translation\\\\(.*)\\\\', '\\1', i) for i in folders_in__translation]
            versions_name_in__translation = [float(i) for i in folders_name_in__translation if is_version(i)]
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

    def loadfolder_check_folders():
        """
        Проверка loadFolders на наличие папок
        """
        if file_exists('loadFolders.xml'):
            printy("Loadfolder.xml remove empty folders...", 'n')

            with open('loadFolders.xml', 'r', encoding="utf-8") as xml_file:
                tree1 = ET.parse(xml_file)
            root1 = tree1.getroot()
            max_v = 1.0

            for v in reversed(root1):
                v_cur = float(v.tag[1:])
                if max_v < v_cur:
                    max_v = v_cur

            printy(f'   Max version [r]{escape_printy_string(max_v)}@')

            for v in reversed(root1):
                v_cur = float(v.tag[1:])
                for li in reversed(v):
                    if li.text == str(v.tag[1:]):
                        if S.Delete_old_versions_translation:
                            li.text = str(max_v)
                    if li.text == "/":
                        pass
                    elif li.text is not None:
                        try:
                            if S.Delete_old_versions_translation:
                                if v_cur == float(li.text.partition("\\")[0]):
                                    li.text = li.text.replace(str(v_cur), str(max_v))
                        except ValueError:
                            print(" Not a float")
                        if not file_exists("_Translation\\" + li.text):
                            printy(f"   Not need folder [<y]{escape_printy_string(li.text)}@ --> Removing")

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

    # loadfolder_check_folders()

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
                if path.rpartition("\\")[2] == "Keyed":
                    try:
                        with open(f"{path}\\{name}", encoding='utf-8') as Keyed_file:
                            tree = etree.parse(Keyed_file, parser_no_delete_comments)
                            root = tree.getroot()
                            root.text = f'\n{S.tags_left_spacing}'

                            for line in root:
                                # input(line.text + f' tail = {line.tail.encode()}')
                                if line.tag is not etree.Comment:

                                    a = etree.Comment(f' {"EN: " if S.Comment_add_EN else ""}{line.text} ')
                                    a.tail = f'\n{S.tags_left_spacing}'
                                    line.addprevious(a)
                                else:
                                    a = line.getprevious()
                                    if a is not None:
                                        a.tail = '\n' * (a.tail.count('\n')) + f'\t\t'
                                    else:
                                        root.text = '\n' + f'\t\t'
                                line.tail = '\n' * (line.tail.count('\n')) + f'{S.tags_left_spacing}'
                            try:
                                root[-1].tail = '\n'
                            except IndexError:
                                printy("[r]\tIndex Error at {path}\\{name}")
                        with open(f"{path}\\{name}", "wb") as Keyed_file:
                            Keyed_file.write(etree.tostring(root,  encoding="utf-8"))
                    except Exception as ex:
                        warning("Bad Keyed Comment adding" + str(ex))
                        Error_log.append("Bad Keyed Comment adding" + str(ex))
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
            New_Name = S.New_Name_before_replace.replace("~MOD_NAME~", name)
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
                new_desc = include_in_QOL_description.replace("~MOD_NAME~", name).replace("~MOD_DESCRIPTION~", description).replace(
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

            image_edit.main(FoldersProg.prog + "\\Images\\Preview\\New_Image.png", S.Position_of_image, S.Position_of_image_Offset_x, S.Position_of_image_Offset_y)

    loadfolder_check_folders()

    try:
        delete_empty_folders(root2)
    except Exception as ex:
        Error_log.append(f"Error delete_empty_folders {ex} \n\n")
        printy(fr"[r]\[ERROR\]@ delete_empty_folders {escape_printy_string(str(ex))} \n\n", predefined='<m')

    try:

        shutil.rmtree(New_Name, ignore_errors=True)
        shutil.copytree("_Translation",
                        sanitize_filename(New_Name), dirs_exist_ok=True)
        shutil.rmtree('_Translation', ignore_errors=True)
    except Exception as ex:
        Error_log.append(f"Error rename _Translation {ex} \n\n")
        printy(fr"[r]\[ERROR\]@ rename _Translation {escape_printy_string(str(ex))} \n\n", predefined='<m')



    if Error_log:
        printy(r"[r]\[ERROR\]@ Need error log --> [r]Opening Error_log.txt@", predefined='<m')
        _Tr = New_Name
        os.makedirs(_Tr, exist_ok=True)
        with open(fr'{_Tr}\\Error_log.txt', 'w', encoding="utf-8") as er_log:
            for el in Error_log:
                er_log.write(el + "\n")
                # print(f"Write error {el}")
        os.startfile(fr'{_Tr}\\Error_log.txt')
        # print('Нажмите "Enter" для выхода' if S.Game_language == "Russian" else 'Press "Enter" to exit.')
        # input()

    print("----------------------------------------------")
    print("All done")
    Floodgauge['value'] = 100
    if Pause_checkbox_var.get():
        os.chdir(FoldersProg.prog)
        print('Нажмите "Enter" для выхода' if S.Game_language == "Russian" else 'Press "Enter" to exit.')
        input()
        exit_prog()
    else:
        exit_prog()


Pause_checkbox_var = CheckboxGloabal()


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
            update_settings()
            go_main(path)

        self.Enter_button = ttk_boot.Button(self.Main_frame, text="...", width=5, command=run_main, )
        self.Enter_button.pack(side='right', padx=(3, 0), )

        self.Main_frame2 = ttk_boot.Frame(self.Content_frame, padding=0)
        self.Main_frame2.pack(expand=True, fill='x', anchor='nw', )

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
            Window_Text_grabber.withdraw()
            Text_grabber_settings.main_from_prog(Window_Text_grabber,)

        self.settings_button = ttk_boot.Button(self.Main_frame2, image=self.settings_image,
                                               command=lambda: run_settings_gui())
        self.settings_button.pack(anchor='ne', side='right', expand=False, pady=(5, 0))

        self.Main_frame3 = ttk_boot.Frame(self.Content_frame, padding=5)
        self.Main_frame3.pack(expand=True, fill='x', anchor='nw', )
        self.Main_frame3.pack_forget()

        self.Floodgauge = ttk_boot.Floodgauge(self.Main_frame3, length=200, mask='Grabbing Progress {}%',
                                              bootstyle="secondary", maximum=100)
        self.Floodgauge.pack(anchor='s', side='bottom', expand=True, fill='both')

        self.btns = [self.Enter_button, self.settings_button, ]#self.menubtn, ]

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
        self.menu.add_checkbutton(label="Включено в QOL",variable=include_in_QOL_bool,command=include_in_QOL_bool_switch)

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
        GWL_EXSTYLE = -20
        WS_EX_APPWINDOW = 0x00040000
        WS_EX_TOOLWINDOW = 0x00000080
        hwnd = windll.user32.GetParent(root.winfo_id())
        style = windll.user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)
        style = style & ~WS_EX_TOOLWINDOW
        style = style | WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongPtrW(hwnd, GWL_EXSTYLE, style)
        # re-assert the new window style
        root.wm_withdraw()
        root.after(10, lambda: root.wm_deiconify())


    def get_settings_lang():
        a = Text_grabber_settings.get_settings_language()
        if is_ok(a):
            S.Settings_language = a.ok()
        else:
            S.Settings_language = a.err()
        return a

    def settings_read_error(parent):
        print('Settings read Error')
        Messagebox.show_error(parent=parent, alert=True,
                              message="Невозможно прочитать настройки! Восстановление оригинальных настроек...\nУстановите настройки заново :("
                              if S.Settings_language == 'ru'
                              else "Can't read settings! Restoring default settings...\nPlease set the settings again :(")
        parent.settings_button.invoke()



    raise_console(False)
    Text_grabber_settings.check_settings_new()
    reading_settings_lang = get_settings_lang()
    Window_Text_grabber = TestApp()

    def update_settings_new():
        global S
        a = Text_grabber_settings.get_config_values(stop_on_error=True)
        match a:
            case Ok(value):
                S = value
                return True
            case Err(value):
                return False

    def settings_get_value_error():
        Text_grabber_settings.main_from_prog(Window_Text_grabber)

    def updater():
        if S.Check_update:
            if Check_New_Version.Check_And_Update(Version_of_Text_grabber):
                Window_Text_grabber.destroy()
            else:
                printy(f"Latest version {Version_of_Text_grabber}", 'n')


    Window_Text_grabber.after(10, lambda: set_appwindow(root=Window_Text_grabber))

    if is_err(reading_settings_lang):
        Window_Text_grabber.after(20, lambda: settings_read_error(Window_Text_grabber))
    else:
        update_settings_error = update_settings_new()
        if update_settings_error:
            pass
        else:
            Window_Text_grabber.withdraw()

            Window_Text_grabber.after(100, lambda: settings_get_value_error())

    Window_Text_grabber.update_fast_checkBTNs()
    Window_Text_grabber.after(100, lambda: updater())

    # update_settings()

    # Window_Text_grabber.after(1000, lambda: update_settings())
    Window_Text_grabber.mainloop()



'''
pyinstaller --noconfirm Text_Grabber.spec

'''
