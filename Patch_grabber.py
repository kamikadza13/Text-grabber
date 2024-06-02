import copy
import os
import re
import shutil
from dataclasses import dataclass
from tkinter.filedialog import askdirectory

import appdirs
import lxml.etree as etree
from printy import printy, escape as printy_escape


@dataclass
class RootElemAndElems:
    """
    root_tag: etree.Element
    last_node: etree.Element
    """
    root_tag: etree.Element
    last_node: etree.Element




# Parent_name_list_patch_grabber, Parent_elem_patch_grabber = [], []
# output_folder = ''



sabaka_names_all_patch_grabber = []

















def main(patches_folder='', output_folder='', tags_to_extract=None, output_in_one_File=False):

    list_of_extract_tags_patch_grabber = []
    sibling_list_patch_grabber = []
    Keyed_tags_patch_grabber = []
    Needed_mods = []


    def operation_selector(a: etree.Element):



        def output_not_in_siblings(r: etree.Element):
            _ = etree.tostring(r, encoding=str, pretty_print=True, with_tail=False)
            if _ in sibling_list_patch_grabber:
                # print(f"Элемент уже выведен : {_}")
                return False
            sibling_list_patch_grabber.append(_)
            return True

        # def update_parents(Parent_name_lis: list, Parent_elem_lis: list, sabaka_name: etree.Element, xpath: str):
        #     print("def update_parents:")
        #     print(Parent_name_lis)
        #     print(Parent_elem_lis)
        #     print(sabaka_name)
        #     print(xpath)
        #     ...

        def xpath_to_elems(xpath: str, value: etree.Element):
            def make_elem_tree_by_elems_str(list_of_elems: list) -> RootElemAndElems:
                # for idx, el in enumerate(list_of_elems):
                #     if "[" in el:
                #         print(f"[ in elem tag: {el}")
                #         list_of_elems[idx] = re.sub(fr"\[.*]", '', el)
                start_pos = 1
                if ("<" or ">") in list_of_elems[0]:
                    print("Bad xml creating - add random Thingdef", xpath)
                    root_node = etree.Element('ThingDef')
                    start_pos = 0
                else:
                    root_node = etree.Element(list_of_elems[0])

                last_node = root_node
                for elem in list_of_elems[start_pos:]:
                    if "defName" in elem:
                        last_node.append(etree.fromstring(elem))
                    elif '@Class' in elem:
                        last_node.attrib["Class"] = re.sub(fr'@Class="(.*)"', '\\1', elem)
                    else:
                        last_node = etree.SubElement(last_node, elem)
                # print("root_node", root_node, "last_node", last_node)
                _ = RootElemAndElems(root_node, last_node)
                return _

            def clear_xpath(xpath_: str):
                _ = xpath_
                xpath_ = re.sub(fr'not\(.*?\)', '', xpath_).replace("\n", "").replace("\t", "").replace("[]",
                                                                                                        '').strip()
                if xpath_.startswith("*/"):
                    xpath_ = re.sub(r"\*/(.*?Def\[)|\*/(.*?Def/)", "\\1\\2", xpath)
                # if xpath_ != _:
                #     print("xpath_ до:   ", _)
                #     print("xpath_ после:", xpath_)
                return xpath_

            value_str = etree.tostring(value, encoding=str, pretty_print=True, with_tail=False)
            if not any([a in value_str for a in list_of_extract_tags_patch_grabber]):
                del value_str
                return None

            xpath = clear_xpath(xpath)
            # or_count = len(re.findall(r' or ', xpath))

            defnames = re.findall(r'defName\s?=\s?[\"|\'](.*?)[\"|\']', xpath)
            sabaka_names = re.findall(r'@Name\s?=\s?[\"|\'](.*?)[\"|\']', xpath)
            sabaka_classes = re.findall(r'@Class\s?=\s?[\"|\'](.*?)[\"|\']', xpath)
            # if sabaka_classes:
            #     print('sabaka_classes', sabaka_classes)
            # if sabaka_names:
            #     print('sabaka_names', sabaka_names)
            exit_list = []

            if xpath in ["/", "//", "", "Defs", "/Defs", '//Defs']:
                for ch in value:
                    if output_not_in_siblings(ch):
                        current_grabbed_text.append(etree.tostring(ch, pretty_print=True, encoding=str))

                return None

            def split_xpath(_):
                _ = re.sub(r"\[.*]", "", _)
                _ = re.split(r'/|(<defName.*_defName>)|(@Class=".*")', _)
                _ = [b.replace("_defName", "/defName") for b in _ if b not in ["Defs", "Def", None, ""]]
                return _

            # if or_count > 0:
            # print('or_count: ', or_count)
            if defnames:
                for defname in defnames:
                    # print('xpath', xpath)
                    a = re.sub(fr"\[.*{defname}.*?]", fr"<defName>{defname}<_defName>", xpath)
                    if sabaka_classes:
                        for sabaka_class in sabaka_classes:
                            a = re.sub(fr"\[.*{sabaka_class}.*?]", fr'@Class="{sabaka_class}"', a)
                            c = split_xpath(a)
                            # print('sabaka_class', a)
                            b = make_elem_tree_by_elems_str(c)
                            exit_list.append(b)
                    else:
                        c = split_xpath(a)
                        # print('Only defnames', a)
                        b = make_elem_tree_by_elems_str(c)
                        exit_list.append(b)

            elif sabaka_names:
                for sabaka_name in sabaka_names:
                    sabaka_names_all_patch_grabber.append(sabaka_name)
                    # update_parents(Parent_name_list_patch_grabber, Parent_elem_patch_grabber, sabaka_name, xpath)


            else:
                # print("xpath without defname")
                # text_final.append("<!-- xpath without defname -->\n")
                current_grabbed_text.append(f"<!-- {xpath} -->\n")
                if "[" in xpath:
                    xpath = re.sub(r"\[.*]", "", xpath)
                    a = re.split(r"/", xpath)
                    a = [b for b in a if b]
                    # print(f"NO defnames:", a)
                    exit_list.append(make_elem_tree_by_elems_str(a))
            # print(f'xpath', repr(xpath))

            return exit_list

        def PatchOperationAdd(operation_add: etree.Element):
            xpath = ""
            value = ""
            for a in operation_add:
                if a.tag == "xpath":
                    xpath = a.text
                if a.tag == "value":
                    value = a
            # if 'rulesStrings' in xpath:
            #     return
            list_of_roots_and_elems_to_add = xpath_to_elems(xpath, value)

            if list_of_roots_and_elems_to_add is None:
                return

            for roots_and_elems in list_of_roots_and_elems_to_add:

                for child in value:
                    roots_and_elems.last_node.append(copy.deepcopy(child))
                # print(f"Добавление элемента: {roots_and_elems.root_tag.tag}")

                if output_not_in_siblings(roots_and_elems.root_tag):
                    # current_grabbed_text.append(
                    #     f"<!-- PatchOperationAdd: Be careful, try to ADD at the end of defname-->\n")
                    current_grabbed_text.append(
                        etree.tostring(roots_and_elems.root_tag, pretty_print=True, encoding=str))
                    # current_grabbed_text.append(f"<!-- PatchOperationAdd - EDD-->\n")

        def PatchOperationReplace(operation_replace: etree.Element):
            xpath = ""
            value = etree.Element("d")

            for a in operation_replace:
                if a.tag == "xpath":
                    # print(f"xpath = {a.text}")
                    xpath = a.text
                if a.tag == "value":
                    value = a

            # if 1 == 1:
            try:
                list_of_roots_and_elems_to_add = xpath_to_elems(xpath, value)
                if list_of_roots_and_elems_to_add is None:
                    return None
                for roots_and_elems in list_of_roots_and_elems_to_add:
                    for child in value:
                        try:
                            if roots_and_elems.root_tag == roots_and_elems.last_node:
                                current_grabbed_text.append(
                                    etree.tostring(roots_and_elems.root_tag, pretty_print=True, encoding=str))
                                continue

                            _ = roots_and_elems.last_node.getparent()
                            _.append(copy.deepcopy(child))
                            _.remove(roots_and_elems.last_node)
                        except Exception as ex:
                            print("Error:", ex)
                    if output_not_in_siblings(roots_and_elems.root_tag):
                        current_grabbed_text.append(
                            etree.tostring(roots_and_elems.root_tag, pretty_print=True, encoding=str))
                        current_grabbed_text.append("\n")
            except Exception as ex:
                print("Error:", ex)

        def PatchOperationSequence(op: etree.Element):
            for a1 in op:
                if a1.tag == "operations":
                    for operation in a1:
                        operation_selector(operation)
                elif a1.tag == 'match':
                    operation_selector(a1)

        def PatchOperationFindMod(Operation_Class_PatchOperationFindMod: etree.Element):
            New_mods = []
            for ch in Operation_Class_PatchOperationFindMod:
                match ch.tag.lower():
                    case "mods":
                        for li in ch:
                            New_mods.append(li.text)
                            current_grabbed_text.append(f"\n<!-- Mod START: {li.text} -->\n")
                            # print(mod_name)
                    case "match":
                        operation_selector(ch)
                    case "nomatch":
                        operation_selector(ch)
                    case "casetrue":
                        for a in ch:
                            operation_selector(a)
                    case "casefalse":
                        for a in ch:
                            operation_selector(a)

            current_grabbed_text.append(f"\n<!-- Mods END: {New_mods} -->\n")

        def PatchOperationConditional(Operation_Class_PatchOperationConditional: etree.Element):
            for ch in Operation_Class_PatchOperationConditional:
                if ch.tag == "match":
                    operation_selector(ch)
                if ch.tag == "nomatch":
                    operation_selector(ch)

        def PatchOperationMakeGunCECompatible(Patch_elem: etree.Element):
            if not any(el.tag == 'defName' for el in Patch_elem):
                return
            Patch_elem.tag = 'ThingDef'

            current_grabbed_text.append(etree.tostring(Patch_elem, pretty_print=True, encoding=str))
            current_grabbed_text.append("\n")

        def ModSettingsFramework(Patch_elem: etree.Element):
            """
            from patch:
            <Operation Class="ModSettingsFramework.PatchOperationSliderFloat">
                <label>Tweak Gestalt Level 1 Control Groups</label>
        		<tooltip>Adjust how many control groups the Gestalt Engine has when level 1. Default: 1</tooltip>
        		<id>RM_GestaltLevel1Control</id>
                ...
        		to
                <RM_GestaltLevel1Bandwith>Настроить проп. способность Гештальта 1-го уровня</RM_GestaltLevel1Bandwith>
                <RM_GestaltLevel1BandwithTooltip>Регулирует, сколько пропускной способности имеет Механизм Гештальта на первом уровне. По умолчанию: 6</RM_GestaltLevel1BandwithTooltip>
        	Keyed:

        		"""
            label = ''
            tooltip = ''
            idd = ''
            for item in Patch_elem:
                if item.tag == 'label':
                    label = item.text
                if item.tag == 'tooltip':
                    tooltip = item.text
                if item.tag == 'id':
                    idd = item.text
            if idd:
                if label:
                    if idd not in Keyed_tags_patch_grabber:


                        current_grabbed_Keyed.append(f"<{idd}>{label}</{idd}>")
                        Keyed_tags_patch_grabber.append(idd)
                if tooltip:
                    if idd + 'Tooltip' not in Keyed_tags_patch_grabber:
                        current_grabbed_Keyed.append(f"<{idd}Tooltip>{tooltip}</{idd}Tooltip>")
                        Keyed_tags_patch_grabber.append(idd + 'Tooltip')

        Op_class: str = a.get("Class", '')

        match Op_class:

            case "PatchOperationSequence":
                PatchOperationSequence(a)
            case "AlphaPrefabs.PatchOperationModOption":
                PatchOperationSequence(a)
            case "PatchOperationFindMod":
                PatchOperationFindMod(a)
            case "XmlExtensions.FindMod":
                PatchOperationFindMod(a)
            case "PatchOperationAdd":
                PatchOperationAdd(a)
            case "XmlExtensions.PatchOperationSafeAdd":
                PatchOperationAdd(a)
            case "XmlExtensions.PatchOperationAddOrReplace":
                PatchOperationAdd(a)
            case "PatchOperationReplace":
                PatchOperationReplace(a)
            case "PatchOperationInsert":
                PatchOperationReplace(a)
            case "PatchOperationTest":
                PatchOperationSequence(a)
            case "PatchOperationConditional":
                PatchOperationConditional(a)

            # Combat Extended
            case "CombatExtended.PatchOperationMakeGunCECompatible":
                PatchOperationMakeGunCECompatible(a)

            # Other
            case _:
                if Op_class.partition(".")[0] == 'ModSettingsFramework':
                    ModSettingsFramework(a)
                for child in a:
                    operation_selector(child)




    printy(f"\t\t\t\\{printy_escape(patches_folder)}", 'p>', end='')
    printy(f"--->", 'b>', end='')
    printy(f"{printy_escape(output_folder)}", 'p>')




    def find_patch_pathes():
        _a = []
        for dirpath, dirnames, filenames in os.walk(patches_folder):
            for name in filenames:
                if name.endswith(".xml"):

                    _a.append(f"{dirpath}\\{name}")
        return _a

    founded_patches = find_patch_pathes()

    # print('Founded patches:', founded_patches)

    if tags_to_extract is None:
        with open(os.path.join(appdirs.user_config_dir(roaming=True), r'Text_grabber\Settings\E1_Tags_to_extraction.txt'), encoding="utf8") as tag_file:
            for line in tag_file:
                list_of_extract_tags_patch_grabber.append(line.strip("\n "))
    else:
        for line in tags_to_extract:
            list_of_extract_tags_patch_grabber.append(line.strip("\n "))


    all_text_dict_list = {}
    all_grabbed_Keyed_list = {}

    for file in founded_patches:
        # try:
        with open(file, encoding="utf-8") as patch:
            # print(f"file:", file)

            # text_final_patch_grabber.append(f"<!-- Filename: {file} -->\n")
            parser = etree.XMLParser(remove_comments=True, remove_blank_text=True, )
            tree = etree.parse(patch, parser)
            root = tree.getroot()
        current_grabbed_text = []
        current_grabbed_Keyed = []

        for operation1 in root:

            operation_selector(operation1)
        if current_grabbed_text:
            if not all([string.strip('\n ').startswith('<!--') for string in current_grabbed_text]):
                all_text_dict_list[file] = current_grabbed_text

        if current_grabbed_Keyed:
            if not all([string.strip('\n ').startswith('<!--') for string in current_grabbed_Keyed]):
                all_grabbed_Keyed_list[file] = current_grabbed_Keyed
    # except Exception as ex:
    #     logging.warning(ex)
    #     print(ex)

    # for f in all_text_dict_list:
    #     print(f, all_text_dict_list[f])

    def output_to_files(oneFile=False):


        if oneFile:
            text = []
            for file_text_dict in all_text_dict_list:
                text.append(f'<!-- {file_text_dict} -->')
                for i in all_text_dict_list[file_text_dict]:
                    text.append(i)
            output_file_path = os.path.join(output_folder, 'Grabbed_Defs_from_patches.xml')

            if not os.path.exists(output_file_path):
                os.makedirs(output_folder, exist_ok=True)
            else:
                printy(f"File already Exists - replace: .\\{printy_escape(output_folder)}", 'r>')

            printy(f"\t\t\t\t{printy_escape(output_file_path)}", 'p>')
            with open(fr"{output_file_path}", "w", encoding="utf-8") as new_patch_file:
                new_patch_file.write("<Defs>\n")
                for l1 in text:
                    new_patch_file.write(l1)
                new_patch_file.write("\n</Defs>")


        else:
            filename_list = []
            for file_text_dict in all_text_dict_list:
                file_name = file_text_dict.rpartition('\\')[2].removesuffix('.xml') + "_Defs"
                if file_name not in filename_list:
                    filename_list.append(file_name)
                else:
                    counter = 0
                    file_name_mask = "{}{}"
                    while file_name_mask.format(file_name, counter) in filename_list:
                        counter += 1

                    file_name = file_name_mask.format(file_name, counter)
                    filename_list.append(file_name)


                patches_f = file_text_dict.partition('\\Patches\\')[2].rpartition('\\')[0]
                # print('patches_f', patches_f)
                output_file_path = os.path.join(output_folder, patches_f, file_name + ".xml")
                if not os.path.exists(output_file_path):
                    os.makedirs(os.path.join(output_folder, patches_f), exist_ok=True)
                else:
                    printy(f"File already Exists - replace: .\\{printy_escape(output_folder)}", 'r>')

                printy(f"\t\t\t\t{printy_escape(output_file_path)}", 'p>')
                with open(fr"{output_file_path}", "w", encoding="utf-8") as new_patch_file:
                    new_patch_file.write("<Defs>\n")
                    new_patch_file.write(f'<!-- {file_text_dict} -->\n')

                    for l1 in all_text_dict_list[file_text_dict]:
                        new_patch_file.write(l1)
                    new_patch_file.write("\n</Defs>")



    output_to_files(output_in_one_File)


    if all_grabbed_Keyed_list:
        return all_grabbed_Keyed_list
    else:
        return None

def print_Keyed(grabbed_Keyed_dict_list: dict, output_folder: str):
    # TODO: Output like other Defs
    if grabbed_Keyed_dict_list:
        filename_list = []
        for gr_Keyed_dict in grabbed_Keyed_dict_list:
            file_name = gr_Keyed_dict.rpartition('\\')[2].removesuffix('.xml') + "_Keyed"
            if file_name not in filename_list:
                filename_list.append(file_name)
            else:
                counter = 0
                file_name_mask = "{}{}"
                while file_name_mask.format(file_name, counter) in filename_list:
                    counter += 1

                file_name = file_name_mask.format(file_name, counter)
                filename_list.append(file_name)

            patches_f = gr_Keyed_dict.partition('\\Patches\\')[2].rpartition('\\')[0]
            # print('patches_f', patches_f)
            output_file_path = os.path.join(output_folder, patches_f, file_name + ".xml")

            with open(fr"{output_file_path}", "w") as new_patch_file:

                new_patch_file.write('<LanguageData>\n')

                new_patch_file.write(f'<!-- {grabbed_Keyed_dict_list} -->\n')

                for l1 in grabbed_Keyed_dict_list[gr_Keyed_dict]:
                    new_patch_file.write(l1)

                new_patch_file.write('</LanguageData>')


if __name__ == "__main__":
    Defs_from_patches_folder = '_Translation\\Grabbed_Defs_from_patches'
    patches_folder1 = os.path.normpath(askdirectory())
    if os.path.exists(os.path.join(patches_folder1, 'Patches')):
        patches_folder1 = os.path.join(patches_folder1, 'Patches')
    # printy(f"Input:  {printy_escape(patches_folder1)}", 'p>')

    # patches_folder = os.path.abspath(r"D:\Games\steamapps\workshop\content\294100\3070780021\Alpha Prefabs rus\1.4\Mods\Ideology\_Patches_to_translate")
    output_folder1 = os.path.join(patches_folder1.rpartition("\\")[0], Defs_from_patches_folder)
    # printy(f"Output: {printy_escape(output_folder1)}", 'p>')



    shutil.rmtree(output_folder1, ignore_errors=True)


    output_folder_Keyed = os.path.join(patches_folder1.rpartition("\\")[0], '_Translation\\Grabbed_Keyed_from_patches')

    Keyed = main(patches_folder1, output_folder1)

    # print_Keyed(Keyed, output_folder_Keyed)



