import copy
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as et

from lxml import etree

from GlobVars import mod_data


@dataclass
class SearchClass:
    another_fold_ids: dict[str, Path] = None

    def __post_init__(self):
        # Инициализируем списки при создании
        self.another_fold_ids = {}





sc = SearchClass({})

def parent_folders(Mod_folder: Path | None, Another_folder: Path | None):

    def searching_packageIds(failed_steam_id):
        """Searching mod dep by id"""

        if failed_steam_id:
            print(f"Fail find steamID '{failed_steam_id}'. Try find by packageId")
            print(f"Search by packageId finished")
        for f in Another_folder.iterdir():  # type: Path
            if not f.is_dir():
                continue
            if (f / 'About' / 'About.xml').exists():
                with open(f / 'About' / 'About.xml', 'r', encoding="utf-8") as lf:
                    tree = etree.parse(lf)
                root = tree.getroot()
                for el in root:  # type: etree.Element
                    if el.tag.lower() == 'packageid':
                        sc.another_fold_ids[el.tag.lower] = f
                        continue
        for packageId in mod_data.modDependencies:
            if packageId in sc.another_fold_ids:
                np = Path(Another_folder) / packageId
                if np.exists():
                    parent_dict[packageId] = np

    def searching_steam_id():
        failed_steam_id = ''
        for packageId, details in mod_data.modDependencies.items():
            if details['steamID']:
                np = Path(Mod_folder) / mod_data.modDependencies[packageId]['steamID']
                if np.exists():
                    parent_dict[packageId] = np
                else:
                    failed_steam_id = packageId

            else:
                failed_steam_id = packageId

        if failed_steam_id:
            searching_packageIds(failed_steam_id)



    parent_dict = {}
    """{ PackageID : Path }"""

    if not Mod_folder:
        if Another_folder:
            searching_packageIds(None)
        else:
            return None
    else:
        searching_steam_id()

    return parent_dict



def adding_elems(current_elem_root: et.Element, parent_elem_root: et.Element, modify_original=False):

    result_elem = current_elem_root if modify_original else copy.deepcopy(current_elem_root)

    if current_elem_root.get('Inherit') == 'False':
        return result_elem

    # Словарь для группировки дочерних элементов по тегам
    children_by_tag = {}
    for child in result_elem:
        children_by_tag.setdefault(child.tag, []).append(child)

    # Обрабатываем элементы из второго элемента
    for parent_elem_child in parent_elem_root:
    # for parent_elem_child in parent_elem_root.iterchildren():
        # Проверяем атрибут Inherit
        if parent_elem_child.get('Inherit') == 'False':
            continue
        # Создаем копию для безопасного использования
        new_child = copy.deepcopy(parent_elem_child)
        new_child.attrib.pop('Inherit', None)  # Удаляем атрибут Inherit если есть

        # Поиск соответствующего элемента в первом
        existing_children = children_by_tag.get(new_child.tag, [])

        if existing_children:
            # Объединяем детей: сначала новые, потом существующие
            existing = existing_children[0]
            merged_children = list(new_child) + list(existing)
            existing.clear()  # Удаляем старых детей
            for child in merged_children:
                existing.append(child)
        else:
            # Добавляем новый элемент в начало
            result_elem.insert(0, new_child)
            # Обновляем словарь
            children_by_tag.setdefault(new_child.tag, []).insert(0, new_child)

    return result_elem

    #
    # # print(f"Добавляется элемент: {elem.tag} в {root1.tag}")
    # if root.get('Inherit') != 'False':
    #     tag_elem = root.find(parent_elem_root.tag) if parent_elem_root.tag is not etree.Comment else None
    #
    #     if tag_elem is None:
    #         root.insert(0, copy.deepcopy(parent_elem_root))
    #     else:
    #         # print("adding Tag exist in root")
    #         if len(parent_elem_root):
    #             for a in parent_elem_root:
    #                 tag_elem.insert(0, copy.deepcopy(a))
    #         else:
    #             # print("No childs")
    #             if tag_elem.text is None:
    #                 if parent_elem_root.text is not None:
    #                     print(f"\tReplace text of element that has child")
    #                     tag_elem.text = parent_elem_root.text
    # return root


def find_parents_in_list_of_pathes(root_dir: list[Path]):
    """{name: elem}"""


    final_parent_dict = {}  # Хранит финальные элементы с Name
    """{name: elem}"""
    curr_parent_dict = {}
    """{name: {'parent': elem.attrib.get('ParentName'), 'elem': elem}}"""

    if root_dir is None:
        return {}

    for xml_path in root_dir:
        # try:
        tree = et.parse(xml_path)
        # tree = etree.parse(xml_path)
        for elem in tree.iter():
            if 'Name' not in elem.attrib:
                continue

            name = elem.attrib['Name']

            if 'ParentName' not in elem.attrib:
                final_parent_dict[name] = elem
            else:
                parent = elem.attrib.get('ParentName')
                if parent in final_parent_dict:



                    new_elem = add_elts_from_par(elem, final_parent_dict[parent])
                    final_parent_dict[name] = new_elem
                else:
                    if parent not in curr_parent_dict:
                        curr_parent_dict[name] = {'parent': elem.attrib.get('ParentName'),
                                                  'elem': elem}
                    else:
                        'Проверка нашелся ли уже финальный родитель у родителя текущего элемента'
                        par_name = curr_parent_dict[parent]['parent']
                        if par_name in final_parent_dict:
                            'Нашелся финальный родитель у родителя. Добавление Родителя par_name в финальный словарь'
                            new_elem = add_elts_from_par(curr_parent_dict.pop(parent)['elem'], final_parent_dict[par_name])
                            final_parent_dict[parent] = new_elem
                            'Добавление name в финальный словарь'
                            new_elem = add_elts_from_par(elem, final_parent_dict[par_name])
                            final_parent_dict[name] = new_elem

                        else:
                            'Финального родителя у родителя текущего элемента нет'
                            curr_parent_dict[name] = {'parent': elem.attrib.get('ParentName'),
                                                      'elem': elem}
        # except Exception as e:
        #     print(f"Error processing {xml_path}: {e}")

    "Нужен цикл проверки"
    prev_size = len(curr_parent_dict)
    while curr_parent_dict:
        curr_size = len(curr_parent_dict)
        if curr_size == prev_size:
            # print("Зависшие элементы:", *curr_parent_dict.keys())
            for name, dic in curr_parent_dict.items():
                final_parent_dict[name] = dic['elem']
            break  # Прерываем цикл, если размер не изменился


        prev_size = curr_size
        for name in list(curr_parent_dict.keys()):
            if name not in curr_parent_dict:
                continue

            parent = curr_parent_dict[name]['parent']
            if parent in final_parent_dict:
                new_elem = add_elts_from_par(final_parent_dict[parent], curr_parent_dict.pop(name)['elem'])
                final_parent_dict[name] = new_elem



    return final_parent_dict

def add_elts_from_par(current_root: etree.Element, parent_root: etree.Element, change_current_bool=False):
    if type(current_root) is not type(parent_root):
        print(type(current_root))
        print(type(parent_root))
    # print('root elem:')
    # etree.dump(parent)
    # print('child elem:')
    # etree.dump(child)
    try:
        if not len(parent_root):
            return current_root
        if not len(current_root):
            return parent_root

        new_elem = adding_elems(current_root, parent_root, change_current_bool)
        return new_elem
    except Exception as ex:
        print("Error add_elts_from_par")
        etree.dump(parent_root)
        etree.dump(current_root)




