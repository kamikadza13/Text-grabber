import copy
from pathlib import Path
from typing import Dict, List

# from xml.etree import ElementTree as et
# from xml.etree.ElementTree import Element
from lxml import etree
from lxml.etree import _Element
from printy import printy

from GlobFunc import no_comment_parser
from GlobVars import Error_log


def adding_elems(current_elem_root: _Element, parent_elem_root: _Element, DEBUG_current_element=False, modify_original=False):
    def is_list_element(elem: _Element) -> bool:
        """Проверяет, является ли элемент списком."""
        children = list(elem)
        return len(children) > 0 and all(child.tag == 'li' for child in children)




    result_elem = current_elem_root if modify_original else copy.deepcopy(current_elem_root)


    #   Если в элементе есть атрибут "Inherit", то он ничего не наследует
    if current_elem_root.get('Inherit') == 'False':
        return result_elem



    # Собираем элементы родителя по тегам
    elems_by_tags: Dict[str, List[_Element]] = {}
    for e in parent_elem_root:
        #   Создаем для пустой список если тега нет, а дальше всем добавляем элементы
        elems_by_tags.setdefault(e.tag, []).append(copy.deepcopy(e))


    # if DEBUG_current_element:
    #
    #     print("Current elem:")
    #     etree.dump(result_elem)
    #
    #     print("Parent elem:")
    #     etree.dump(parent_elem_root)
    #
    #     print(elems_by_tags.keys())
    #     comps = elems_by_tags.get('comps')
    #     if comps:
    #         print('Parent Comps:')
    #         for a in comps[0]:
    #             etree.dump(a)


    for e in result_elem:

        # if e.get('Inherit') == 'False':
        #     continue

        if e.tag not in elems_by_tags or e.get('Inherit') == 'False':
            elems_by_tags[e.tag] = [e]
        else:
            #   Элемент есть в родителе
            #   Нужно проверить есть ли <li> в элементе, если так, то доавлять к родительским
            if is_list_element(e):   #   Все дети ли

                for li in e:
                    for idx, li_s in enumerate(elems_by_tags[e.tag][0]):
                        li_s: _Element
                        if len(li.attrib) > 0 and li.attrib == li_s.attrib:
                            if DEBUG_current_element:
                                print('Replaced:')
                                etree.dump(li_s)
                                etree.dump(li)
                            elems_by_tags[e.tag][0][idx] = li
                            break
                    else:
                        elems_by_tags[e.tag][0].append(li)
                continue
            #   Элемент заменяем на новый
            #   Если несколько с одинаковым тэгом, то заменяет первый.
            elems_by_tags[e.tag][0] = e

    result_elem.clear()
    result_elem.text = '\n\t'

    for elems in elems_by_tags.values():
        for el in elems:
            result_elem.append(el)

    if list(result_elem):
        result_elem[-1].tail = '\n'

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

    processed_idx = 0
    processed_parents_idx = 0

    final_parent_dict = {}  # Хранит финальные элементы с Name
    """{name: elem}"""
    curr_parent_dict = {}
    """{name: {'parent': elem.attrib.get('ParentName'), 'elem': elem}}"""

    if root_dir is None:
        return {}

    for xml_path in root_dir:
        try:
            tree = etree.parse(xml_path, parser=no_comment_parser)
            elements = tree.xpath("//*[@Name]")


            for elem in elements:



                try:
                    if processed_idx % 10 == 0:
                        printy(f"\r\tProcessed: {processed_parents_idx} Elements", 'b>', end='', )
                    processed_idx += 1
                except Exception:
                    pass


                name = elem.attrib['Name']
                processed_parents_idx += 1

                if 'ParentName' not in elem.attrib:
                    final_parent_dict[name] = elem
                else:
                    parent = elem.attrib.get('ParentName')
                    if parent in final_parent_dict:

                        new_elem = add_elts_from_par(elem, final_parent_dict[parent], )
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
        except Exception as e:
            Error_log.append(f"\nError processing {xml_path}: {e}")

    printy(f"\r\tProcessed: {processed_parents_idx} parents among {processed_idx} Elements", 'b>', end='', )

    def updating_parent_final_list():
        iteration_count = 0  # Счётчик итераций для защиты от бесконечных циклов
        MAX_ITERATIONS = 100  # Максимальное число итераций

        while curr_parent_dict and iteration_count < MAX_ITERATIONS:
            iteration_count += 1
            changed = False  # Флаг изменения словаря

            # Перебор копии ключей для безопасного удаления
            for name in list(curr_parent_dict.keys()):
                # Элемент мог быть удалён в этой же итерации
                if name not in curr_parent_dict:
                    continue

                parent = curr_parent_dict[name]['parent']
                # Если родитель готов - обрабатываем элемент
                if parent in final_parent_dict:
                    new_elem = add_elts_from_par(final_parent_dict[parent], curr_parent_dict[name]['elem'])
                    nName = new_elem.attrib.get('Name')
                    if nName is None:
                        new_elem.attrib['Name'] = name
                    final_parent_dict[name] = new_elem
                    del curr_parent_dict[name]  # Удаляем обработанный элемент
                    changed = True

            # Защита от зависания: выход если изменений не было
            if not changed:
                break

        # Добавляем оставшиеся элементы (зависшие или без родителя)
        for name, dic in curr_parent_dict.items():
            final_parent_dict[name] = dic['elem']


    "Нужен цикл проверки"

    updating_parent_final_list()

    # prev_size = len(curr_parent_dict)
    # while curr_parent_dict:
    #     curr_size = len(curr_parent_dict)
    #     if curr_size == prev_size:
    #         # print("Зависшие элементы:", *curr_parent_dict.keys())
    #         for name, dic in curr_parent_dict.items():
    #             final_parent_dict[name] = dic['elem']
    #         break  # Прерываем цикл, если размер не изменился
    #
    #
    #     prev_size = curr_size
    #     for name in list(curr_parent_dict.keys()):
    #         if name not in curr_parent_dict:
    #             continue
    #
    #         parent = curr_parent_dict[name]['parent']
    #         if parent in final_parent_dict:
    #             new_elem = add_elts_from_par(final_parent_dict[parent], curr_parent_dict.pop(name)['elem'])
    #             final_parent_dict[name] = new_elem
    #


    return final_parent_dict

def add_elts_from_par(current_root: _Element, parent_root: _Element, DEBUG_current_element=False, change_current_bool=False, ):
    if type(current_root) is not type(parent_root):
        print(type(current_root))
        print(type(parent_root))

    # print('root elem:')
    # et.dump(parent_root)
    # print('child elem:')
    # et.dump(current_root)

    try:
        if not len(parent_root):
            return current_root
        if not len(current_root):
            return parent_root

        # if change_current_bool:
        #     print("До:")
        #     etree.dump(current_root)

        new_elem = adding_elems(current_root, parent_root, DEBUG_current_element=DEBUG_current_element, modify_original=change_current_bool,)
        # if change_current_bool:
        #     print("После:")
        # etree.dump(new_elem)

        return new_elem
    except Exception as ex:
        print("Error add_elts_from_parent")
        etree.dump(parent_root)
        etree.dump(current_root)
        input()




