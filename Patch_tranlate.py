# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree as ET
import shutil

files = []
new_list = []

list_of_labels_list = ["label", "labelNoun", "labelPlural", "text", "description", "jobString", "desc",
                       "customLabel", "customLetterLabel", "customLetterText", "ingestCommandString",
                       "ingestReportString", "outOfFuelMessage",
                       "name", "summary", 'pawnSingular', 'pawnsPlural',  #
                       "reportString"]  # Список Тэгов для вывода в печать
list_of_tags = ["Message", "Label", "label", "Title", "Text", "gerund", "Gerund"]
# Список неполных тэгов
# Этот список ищется в Тэге (например, "Message" в <outOfFuelMessage> должно найтись)

list_of_path = ["rulesStrings", "customLetterText"]  # Список Тэгов перед <li> для вывода
list_of_forbidden_character_in_label = ["{", "}", "\'"]  # Список запрещенных символов в label
list_of_forbidden_tags = ['defaultLabelColor']  # Список запрещенных для вывода тэгов
list_of_folders_to_translate = ['Common', '/']  # Список папок для поиска Defs и Languages и т.д.

Language_translate_from = 'English'
Language = 'Russian'


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
    shutil.copy(src_path, dst_path)
    print('Copied')
