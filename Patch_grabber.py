import copy
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from pprint import pprint
from typing import Dict, List, Tuple, Union

import lxml
import lxml.etree as etree
from lxml.etree import Element, _Element
from printy import printy

from GlobFunc import xml_get_text
from GlobVars import state

DEBUG_mode = False
@dataclass
class Pp:
    req_modsID_list: List[str] = None
    '''[
    Ludeon.RimWorld.Royalty,
    zhrocks11.letstrade
    ]'''
    # mods: Dict[Path, tuple[str]] = None

    ModSettingsFramework_Keyed_id_list = None
    '''
    [
        RM_GestaltLevel1Bandwith
        RM_GestaltLevel2Bandwith
    ]
    
            <Operation Class="ModSettingsFramework.PatchOperationSliderFloat">
        	<id>RM_GestaltLevel1Bandwith</id>'''


    all_grabbed_Keyed_list: Dict[Path, List[str]] = None
    '''{Path: [<Elem1>, <Elem2>]}'''
    def __post_init__(self):
        self.req_modsID_list = []
        self.ModSettingsFramework_Keyed_id_list = []
        self.all_grabbed_Keyed_list = {}



@dataclass
class Reqmod:
    steamId: str = None
    name: str = None
    steamName: str = None
    packageId: str = None
    last_v: list = None

    def __lt__(self, other):
        if not isinstance(other, Reqmod):
            return NotImplemented

        # Обрабатываем None как пустой список
        self_ver = self.last_v or []
        other_ver = other.last_v or []

        return self_ver < other_ver

founded_mods_by_name = {
    'Core': '',

    'Royalty': 'Ludeon.Rimworld.Royalty',
    'Rimworld - Royality': 'Ludeon.Rimworld.Royalty',
    'Royalty [Official DLC]': 'Ludeon.Rimworld.Royalty',

    'Ideology': 'Ludeon.Rimworld.Ideology',
    'Rimworld - Ideology': 'Ludeon.Rimworld.Ideology',
    'Ideology [Official DLC]': 'Ludeon.Rimworld.Ideology',

    'Biotech': 'Ludeon.Rimworld.Biotech',
    'Rimworld - Biotech': 'Ludeon.Rimworld.Biotech',
    'Biotech [Official DLC]': 'Ludeon.Rimworld.Biotech',

    'Anomaly': 'Ludeon.Rimworld.Anomaly',
    'Rimworld - Anomaly': 'Ludeon.Rimworld.Anomaly',
    'Anomaly [Official DLC]': 'Ludeon.Rimworld.Anomaly',

    'Vanilla Factions Expanded - Ancients': 'oskarpotocki.vfe.vfea',
    'Vanilla Factions Expanded Ancients': 'oskarpotocki.vfe.vfea',

    'Vanilla Factions Expanded - Classical': 'oskarpotocki.vfe.classical',
    'Vanilla Factions Expanded Classical': 'oskarpotocki.vfe.classical',

    'Vanilla Factions Expanded - Deserters': 'oskarpotocki.vfe.deserters',
    'Vanilla Factions Expanded Deserters': 'oskarpotocki.vfe.deserters',
    'Deserters': 'oskarpotocki.vfe.deserters',

    'Vanilla Factions Expanded - Empire': 'oskarpotocki.vfe.empire',
    'Vanilla Factions Expanded Empire': 'oskarpotocki.vfe.empire',

    'Vanilla Factions Expanded - Insectoids 2': 'oskarpotocki.vfe.insectoid2',
    'Vanilla Factions Expanded Insectoids 2': 'oskarpotocki.vfe.insectoid2',

    'Vanilla Factions Expanded - Mechanoids': 'oskarpotocki.vfe.mechanoid',
    'Vanilla Factions Expanded Mechanoids': 'oskarpotocki.vfe.mechanoid',

    'Vanilla Factions Expanded - Medieval': 'oskarpotocki.vanillafactionsexpanded.medievalmodule',
    'Vanilla Factions Expanded Medieval': 'oskarpotocki.vanillafactionsexpanded.medievalmodule',

    'Vanilla Factions Expanded - Megacorp': 'oskarpotocki.vfe.megacorp',
    'Vanilla Factions Expanded Megacorp': 'oskarpotocki.vfe.megacorp',

    'Vanilla Factions Expanded - Pirates': 'oskarpotocki.vfe.pirates',
    'Vanilla Factions Expanded Pirates': 'oskarpotocki.vfe.pirates',

    'Vanilla Factions Expanded - Settlers': 'oskarpotocki.vanillafactionsexpanded.settlersmodule',
    'Vanilla Factions Expanded Settlers': 'oskarpotocki.vanillafactionsexpanded.settlersmodule',

    'Vanilla Factions Expanded - Tribals': 'oskarpotocki.vfe.tribals',
    'Vanilla Factions Expanded Tribals': 'oskarpotocki.vfe.tribals',

    'Vanilla Factions Expanded - Vikings': 'oskarpotocki.vfe.vikings',
    'Vanilla Factions Expanded Vikings': 'oskarpotocki.vfe.vikings',

    'Vanilla Chemfuel Expanded': 'vanillaexpanded.vchemfuele',

    'Combat Extended': 'ceteam.combatextended',
    'CE': 'ceteam.combatextended',

    'Vanilla Anomaly Expanded - Insanity': 'vanillaexpanded.vanomalyeinsanity',
    'Vanilla Anomaly Expanded Insanity': 'vanillaexpanded.vanomalyeinsanity'
}



def search_mod_id_by_name(data, modNamed_set: set[str]):

    if not modNamed_set:
        return []

    founded_ids_list = []
    founded_modname_not_founded_id_list = []

    modname_list = list(modNamed_set)

    def founded_mods_by_name_func(modname_list):

        remove_list = []
        for name in modname_list:
            if founded_mods_by_name.get(name):
                founded_ids_list.append(founded_mods_by_name.get(name))
                remove_list.append(name)


        for r in remove_list:
            modname_list.remove(r)
        return modname_list

    modname_list = founded_mods_by_name_func(modname_list)
    if not modname_list:
        return founded_ids_list

    def get_dict_elems_by_name(mod_list):

        def parse_version(version_str):
            # Извлекаем основную часть (до первого пробела)
            clean_version = version_str.split()[0]
            # Разбиваем на компоненты по точкам
            parts = clean_version.split('.')
            # Конвертируем каждую часть в число
            return [int(part) for part in parts]



        if DEBUG_mode:
            print('Searching:', mod_list)
        results = {a: [] for a in mod_list}

        for mod_id_elem in data['database']:
            """mod_id_elem like 1274936357"""
            # print(mod_id_elem)
            # try:

            name = data['database'][mod_id_elem].get('name')
            steamName = data['database'][mod_id_elem].get('steamName')
            if name in mod_list or steamName in mod_list:
                packageId = data['database'][mod_id_elem].get('packageId')
                gameVersions = data['database'][mod_id_elem].get('gameVersions')
                if gameVersions:
                    last_v = parse_version(max(gameVersions, key=parse_version))
                else:
                    last_v = None
                req = Reqmod(steamId=mod_id_elem, name=name, steamName=steamName, packageId=packageId, last_v=last_v)
                if DEBUG_mode:
                    print('req', req)
                    print('results:', results)
                if name in results:
                    results[name].append(req)
                else:
                    results[steamName].append(req)

            # except Exception as ex:
            #     print(ex, 'Error finding name/stamname in', mod_id_elem)
            #     continue
        return results

    elems_by_name_from_database = get_dict_elems_by_name(modname_list)


    for searching_mod_name in elems_by_name_from_database:

        if elems_by_name_from_database[searching_mod_name]:
            "Поиск среди результатов элемента с самой последней версией и получение его packageId"

            maxv_elem = max(elems_by_name_from_database[searching_mod_name]) # type: Reqmod
            packageId = getattr(maxv_elem, 'packageId')
            if packageId:
                if DEBUG_mode:
                    pprint(elems_by_name_from_database[searching_mod_name], width=120)

                founded_ids_list.append(packageId)
                continue
            founded_modname_not_founded_id_list.append(maxv_elem)
    if DEBUG_mode:
        pprint(founded_modname_not_founded_id_list)
    # TODO: founded_modname_not_founded_id_list сделать по нему поиск когда-нибудь
    return  founded_ids_list


sabaka_names_all_patch_grabber = []


patches_file_count = 0





def main(folder_required_mods: Tuple, patches_folder=Path('.'), tags_to_extract=None, database_path=None):
    """
    Return Keyed dict with list of strings: Dict[Path, List[str]]
        {Path: [<Elem1>, <Elem2>]}
    Also update """

    printy(f'\t\t\tProcessing patches: {patches_folder}', 'y>')

    @dataclass
    class ReqModAndText:
        """
        req_mods: Tuple[str]
        text: str"""
        req_mods: Tuple[str] | tuple
        text: str

    SS = Pp()
    SS.req_modsID_list.extend(folder_required_mods)
    '''Моды для всей папки с патчами'''



    # database_path = r'D:\Games\steamapps\workshop\content\294100\1847679158\db\db.json'
    with open(database_path, encoding='utf-8') as f:
        data: Dict[str, Dict] = json.load(f)


    list_of_extract_tags_patch_grabber = [ll.strip("\n ") for ll in tags_to_extract]

    sibling_list_patch_grabber = []

    def output_not_in_siblings(r: Element):
        q = etree.tostring(r, encoding=str, pretty_print=True, with_tail=False)
        if q in sibling_list_patch_grabber:
            # print(f"Элемент уже выведен : {_}")
            return False
        sibling_list_patch_grabber.append(q)
        return True



    def add_string_to_output(string_or_Element: Union[str, Element]):
        if output_not_in_siblings(string_or_Element):

            need_mods = tuple(SS.req_modsID_list) if SS.req_modsID_list else ()
            text = string_or_Element if string_or_Element is str else etree.tostring(string_or_Element, pretty_print=True, encoding=str)

            current_grabbed_Mod_and_string_list.append(ReqModAndText(need_mods,text))


    def operation_selector(a: Element):





        def xpath_to_elems(xpath: str, value: Element):

            @dataclass
            class RootElemAndElems:
                """
                root_tag: Element
                last_node: Element
                """
                root_tag: lxml.etree.Element
                last_node: lxml.etree.Element

            def make_elem_tree_by_elems_str(list_of_elems: list) -> RootElemAndElems:
                # for idx, el in enumerate(list_of_elems):
                #     if "[" in el:
                #         print(f"[ in elem tag: {el}")
                #         list_of_elems[idx] = re.sub(fr"\[.*]", '', el)
                start_pos = 1
                if ("<" or ">") in list_of_elems[0]:
                    print("Bad xml creating - add random Thingdef", xpath, patch_file_path)
                    root_node = Element('ThingDef')
                    start_pos = 0
                else:
                    root_node = Element(list_of_elems[0])

                last_node = root_node
                for elem in list_of_elems[start_pos:]:
                    if "defName" in elem:
                        last_node.append(etree.fromstring(elem))
                    elif '@Class' in elem:
                        last_node.attrib["Class"] = re.sub(fr'@Class="(.*)"', '\\1', elem)
                    else:
                        last_node = etree.SubElement(last_node, elem)
                # print("root_node", root_node, "last_node", last_node)
                return RootElemAndElems(root_node, last_node)

            def clear_xpath(xpath: str):

                def remove_not_recursive(s):
                    not_pos = s.find('not(')
                    if not_pos == -1:
                        return s

                    # Ищем логические операторы перед not(...)
                    operators = [' and ', ' or ', ' AND ', ' OR ']
                    op_pos = max((s.rfind(op, 0, not_pos) for op in operators), default=-1)

                    # Находим границы not(...)
                    start = not_pos
                    count = 1
                    i = start + 4
                    while i < len(s) and count > 0:
                        if s[i] == '(': count += 1
                        if s[i] == ')': count -= 1
                        i += 1

                    # Определяем границы для удаления
                    remove_start = op_pos if op_pos != -1 else start
                    remove_end = i

                    # Формируем новую строку
                    new_str = s[:remove_start] + s[remove_end:]

                    return remove_not_recursive(new_str)


                removed_NOT = remove_not_recursive(xpath)

                xpath = removed_NOT.replace("\n", "").replace("\t", "").replace("[]", '').strip()

                if xpath.startswith("*/"):
                    xpath = re.sub(r'^\*/(.*?Def.*?)([[/])', r'\1\2', xpath, count=1)

                return xpath


            def just_output_check(value):
                counter = 0
                val_lengh = len(list(value))

                for ch in value:
                    enwith_Def = False
                    has_defname_into = False
                    ch: _Element
                    if ch.tag.endswith("Def"):
                        enwith_Def = True
                    if ch.xpath('boolean(child::defName)'):
                        has_defname_into = True
                    if enwith_Def and has_defname_into:
                        counter += 1
                        add_string_to_output(ch)
                # print('counter', counter)
                # print('val_lengh', val_lengh)
                if counter == val_lengh:
                    return True
                return False


            elem_string = etree.tostring(value, encoding=str, pretty_print=True, with_tail=False)
            if not any([a in elem_string for a in list_of_extract_tags_patch_grabber]):
                return None



            if just_output_check(value):
                return None

            xpath = clear_xpath(xpath)

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
                    add_string_to_output(ch)
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
                #   TODO: sabaka_name Ничего не делает
                for sabaka_name in sabaka_names:
                    sabaka_names_all_patch_grabber.append(sabaka_name)
                    # update_parents(Parent_name_list_patch_grabber, Parent_elem_patch_grabber, sabaka_name, xpath)


            else:
                # print("xpath without defname")
                # text_final.append("<!-- xpath without defname -->\n")
                # current_grabbed_Mod_and_string_list.append(f"<!-- {xpath} -->\n")
                if "[" in xpath:
                    xpath = re.sub(r"\[.*]", "", xpath)
                    a = re.split(r"/", xpath)
                    a = [b for b in a if b]
                    # print(f"NO defnames:", a)
                    exit_list.append(make_elem_tree_by_elems_str(a))
            # print(f'xpath', repr(xpath))

            return exit_list

        def PatchOperationAdd(operation_add: Element):
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

                add_string_to_output(roots_and_elems.root_tag)

        def PatchOperationReplace(operation_replace: Element):
            xpath = ""
            value = Element("d")

            for a in operation_replace:
                if a.tag == "xpath":
                    # print(f"xpath = {a.text}")
                    xpath = a.text
                if a.tag == "value":
                    value = a

            try:
                list_of_roots_and_elems_to_add = xpath_to_elems(xpath, value)
                if list_of_roots_and_elems_to_add is None:
                    return None
                for roots_and_elems in list_of_roots_and_elems_to_add:
                    for child in value:

                        # dump(child)
                        try:
                            if roots_and_elems.root_tag == roots_and_elems.last_node:
                                add_string_to_output(roots_and_elems.root_tag)
                                continue

                            _ = roots_and_elems.last_node.getparent()
                            _.append(copy.deepcopy(child))
                            _.remove(roots_and_elems.last_node)
                        except Exception as ex:
                            print("Error:", ex)
                    add_string_to_output(roots_and_elems.root_tag)

            except Exception as ex:
                print("Error:", ex)

        def PatchOperationSequence(op: Element):
            for a1 in op:
                if a1.tag == "operations":
                    for operation in a1:
                        operation_selector(operation)
                elif a1.tag == 'match':
                    operation_selector(a1)



        def PatchOperationFindMod(operation_Class_PatchOperationFindMod: _Element):

            New_mods = []
            try:
                packageId_bool = bool(xml_get_text(operation_Class_PatchOperationFindMod, 'packageId'))

                if packageId_bool:
                    mods = operation_Class_PatchOperationFindMod.find('mods')
                    if mods is not None:
                        for li in mods:
                            mod = li.text if li.text is not None else ''
                            if mod:
                                New_mods.append(mod)
                                SS.req_modsID_list.append(mod)

                    caseTrue = operation_Class_PatchOperationFindMod.find('caseTrue')
                    if caseTrue is not None:
                        for c in caseTrue:
                            operation_selector(c)
                    caseFalse = operation_Class_PatchOperationFindMod.find('caseFalse')
                    if caseFalse is not None:
                        for mod in New_mods:
                            try:
                                SS.req_modsID_list.remove(mod)
                            except ValueError as ex:
                                continue

                        for c in caseFalse:
                            operation_selector(c)

                else:
                    for ch in operation_Class_PatchOperationFindMod:  # type: _Element
                        match ch.tag.lower():
                            case "mods":
                                mods_names_list = []
                                for li in ch:
                                    if li.text is not None:
                                        mods_names_list.append(li.text)

                                if mods_names_list:
                                    print("\tPatch FindMods:", mods_names_list)
                                    modIds = set(search_mod_id_by_name(data, set(mods_names_list)))
                                    if modIds:
                                        New_mods.extend(modIds)
                                        SS.req_modsID_list.extend(modIds)
                                # print(mod_name)
                            case "match":
                                operation_selector(ch)
                            case "nomatch":
                                for mod in New_mods:
                                    try:
                                        SS.req_modsID_list.remove(mod)
                                    except ValueError as ex:
                                        continue
                                operation_selector(ch)
                            case "casetrue":
                                for a in ch:
                                    operation_selector(a)
                            case "casefalse":
                                for mod in New_mods:
                                    try:
                                        SS.req_modsID_list.remove(mod)
                                    except ValueError as ex:
                                        continue
                                for a in ch:
                                    operation_selector(a)




            except Exception as ex:
                pass

            try:
                for mod in New_mods:
                    SS.req_modsID_list.remove(mod)
            except ValueError as ex:
                pass


        def PatchOperationConditional(Operation_Class_PatchOperationConditional: Element):
            for ch in Operation_Class_PatchOperationConditional:
                if ch.tag == "match":
                    operation_selector(ch)
                if ch.tag == "nomatch":
                    operation_selector(ch)

        def PatchOperationMakeGunCECompatible(Patch_elem: Element):
            if not any(el.tag == 'defName' for el in Patch_elem):
                return
            Patch_elem.tag = 'ThingDef'

            add_string_to_output(Patch_elem)

        def ModSettingsFramework(Patch_elem: Element):
            """
            from patch:
            <Operation Class="ModSettingsFramework.PatchOperationSliderFloat">
                <label>Tweak Gestalt Level 1 Bandwith</label>
        		<tooltip>Adjust how much bandwith the Gestalt Engine has when level 1. Default: 6</tooltip>
        		<id>RM_GestaltLevel1Bandwith</id>
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
                    if idd not in SS.ModSettingsFramework_Keyed_id_list:
                        current_grabbed_Keyed.append(f"<{idd}>{label}</{idd}>")
                        SS.ModSettingsFramework_Keyed_id_list.append(idd)
                if tooltip:
                    if idd + 'Tooltip' not in SS.ModSettingsFramework_Keyed_id_list:
                        current_grabbed_Keyed.append(f"<{idd}Tooltip>{tooltip}</{idd}Tooltip>")
                        SS.ModSettingsFramework_Keyed_id_list.append(idd + 'Tooltip')



        Op_class: str = a.get("Class", '')
        Op_mayrequire: str = a.get("MayRequire")
        new_req_modsID_for_Element = []
        if Op_mayrequire is not None:
            mod_ids = Op_mayrequire.split(',')
            for mod_id in mod_ids:
                m_id = mod_id.strip()
                new_req_modsID_for_Element.append(m_id)
                SS.req_modsID_list.append(m_id)

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

        for new_req_mod in new_req_modsID_for_Element:
            SS.req_modsID_list.remove(new_req_mod)


    # printy(f"\t\t\t\\{printy_escape(patches_folder)}", 'p>', end='')
    # printy(f"--->", 'b>')


    patches_file_pathes_list = [p for p in patches_folder.rglob("*.xml") if p.is_file()]
    '''Founded patches'''
    # print('Founded patches:', [str(path) for path in patches_file_pathes_list])




    all_mod_and_string_list_dict: Dict[Path, List[ReqModAndText]] = {}
    """
    req_mods: Tuple[str]
    text: str"""




    for patch_file_path in patches_file_pathes_list:
        # try:
        with open(patch_file_path, encoding="utf-8") as patch:
            # text_final_patch_grabber.append(f"<!-- Filename: {file} -->\n")
            parser = etree.XMLParser(remove_comments=True, remove_blank_text=True, )
            tree = etree.parse(patch, parser)
            root = tree.getroot()

        current_grabbed_Mod_and_string_list: List[ReqModAndText] = []

        current_grabbed_Keyed: list[str] = []
        '''<RM_GestaltLevel1Bandwith>Настроить проп. способность Гештальта 1-го уровня</RM_GestaltLevel1Bandwith>'''



        for operation1 in root:
            '!!!!!!!!!!!!!!!!!!!!'
            operation_selector(operation1)
            '!!!!!!!!!!!!!!!!!!!!'
        if current_grabbed_Mod_and_string_list:
            all_mod_and_string_list_dict[patch_file_path] = current_grabbed_Mod_and_string_list

        if current_grabbed_Keyed:

            state.keyed_from_patches[patch_file_path] = current_grabbed_Keyed



    def Update_glob_state_mod_folders():
        """Переделка словаря из
         {Путь: (моды), [текст]} в
            {
                (Моды): {Путь: [текст]}
            }
        """

        # state.mods_folders

        '''
        -----{
        -----(req mods): 
        ---------{Path:
        ------------[text1, text2]
        ---------}
        -----}
        '''
        # print('all_mod_and_string_list_dict', all_mod_and_string_list_dict)

        for orig_file_path in all_mod_and_string_list_dict:
            for req_and_text in all_mod_and_string_list_dict[orig_file_path]:
                if req_and_text.req_mods not in state.mods_folders:
                    state.mods_folders[req_and_text.req_mods] = {orig_file_path: [req_and_text.text]}
                else:
                    if orig_file_path not in state.mods_folders[req_and_text.req_mods]:
                        state.mods_folders[req_and_text.req_mods][orig_file_path] = [req_and_text.text]
                    else:
                        state.mods_folders[req_and_text.req_mods][orig_file_path].append(req_and_text.text)

    Update_glob_state_mod_folders()

    return

def print_Keyed(grabbed_Keyed_dict_list: dict, output_folder: str):
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


