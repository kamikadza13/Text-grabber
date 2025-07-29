from pathlib import Path

from lxml import etree
from printy import printy

from Get_database_by_list_of_pathes_of_mods import MultiIndexDict
from GlobVars import mod_data
from Text_Grabber import escape_printy_string

DEBUG = True


def get_modDependencies():
    id_and_names = []
    printy('\t\t\tAbout.xml modDependencies Required mods:', '<o')

    for package_id in mod_data.modDependencies:
        name = mod_data.modDependencies[package_id].get('displayName')
        if name is not None:
            printy(f'\t\t\t\t{escape_printy_string(name):^30}|{package_id}', 'o>')
            id_and_names.append((package_id, name))
        else:
            printy(f'\t\t\t\t{" " * 30}|{package_id}', 'o>')
            id_and_names.append((package_id, None))

    return id_and_names


def get_loadAfter():
    return mod_data.loadafter_list


def unpack_result(r: dict):
    n: str = r['name']
    pi: str = r['packageid']
    p: str = str(r['path'])
    return n, pi, p


def search_in_database_by_id(database: MultiIndexDict, iid, search_name):
    results = database.find(packageid=iid)
    l = len(results)
    match l:
        case 1:
            name, pid, path = unpack_result(results[0])
            printy(f'\t\tFounded full match: {escape_printy_string(name)} | {escape_printy_string(path)}', 'y>')
            return results
        case a if a > 1:
            printy(f'\t\tFounded few results:', '<r')
            for res in results:
                name, pid, path = unpack_result(res)
                printy(f'\t\t\t{escape_printy_string(name)} | {escape_printy_string(pid)} | {escape_printy_string(path)}', '<r')
            return results
        case _:
            printy(f'\t\tNOT FOUNDED {escape_printy_string(iid)} | {escape_printy_string(search_name)}\n\t\tTry to another method', 'r')
            return None


def search_in_database_by_name(database, iid, search_name):
    results = database.find(name=search_name)

    l = len(results)
    match l:
        case 1:
            name, pid, path = unpack_result(results[0])
            printy(f'\t\tFounded full match: {escape_printy_string(name)} | {escape_printy_string(path)}', 'y>')
            return results
        case a if a > 1:
            printy(f'\t\tFounded few results:', '<r')
            for res in results:
                name, pid, path = unpack_result(res)
                printy(f'\t\t\t{escape_printy_string(name)} | {escape_printy_string(pid)} | {escape_printy_string(path)}', '<r')
            return results
        case _:
            printy(f'\t\tNOT FOUNDED {escape_printy_string(iid)} | {escape_printy_string(search_name)}\n\t\tTry to another method', 'r')
            return None


def search_in_database_by_fuzzyname(database, iid, search_name):
    results = database.fuzzy_find(name=search_name)

    l = len(results)
    match l:
        case 1:
            name, pid, path = unpack_result(results[0])
            printy(f'\t\tFounded full match: {escape_printy_string(name)} | {escape_printy_string(path)}', 'y>')
            return results
        case a if a > 1:
            printy(f'\t\tFounded few results:', '<r')
            for res in results:
                name, pid, path = unpack_result(res)
                printy(f'\t\t\t{escape_printy_string(name)} | {escape_printy_string(pid)} | {escape_printy_string(path)}', '<r')
            return results
        case _:
            printy(f'\t\tNOT FOUNDED {escape_printy_string(iid)} | {escape_printy_string(search_name)}\n\t\tTry to another method', 'r')
            return None


def search_in_database_by_part_find(database, iid, search_name):
    results = database.partial_find(name=search_name)

    l = len(results)
    match l:
        case 1:
            name, pid, path = unpack_result(results[0])
            printy(f'\t\tFounded full match: {escape_printy_string(name)} | {escape_printy_string(path)}', 'y>')
            return results
        case a if a > 1:
            printy(f'\t\tFounded few results:', '<r')
            for res in results:
                name, pid, path = unpack_result(res)
                printy(f'\t\t\t{escape_printy_string(name)} | {escape_printy_string(pid)} | {escape_printy_string(path)}', '<r')
            return results
        case _:
            printy(f'\t\tNOT FOUNDED {escape_printy_string(iid)} | {escape_printy_string(search_name)}\n\t\tTry to another method', 'r')
            return None


def get_loadFolders():
    try:
        tree = etree.parse('LoadFolders.xml')
        return list(set(
            element.get("IfModActive")
            for element in tree.xpath("//*[@IfModActive]")
        )) or None  # Возвращаем None при пустом результате

    except Exception as ex:
        print(f"Error reading LoadFolders.xml: {ex}")
        return None




def get_may_require_values(path:Path):
    try:
        tree = etree.parse(path)
        # Используем XPath для поиска всех элементов с атрибутом MayRequire
        elements = tree.xpath("//*[@MayRequire]")

        # Извлекаем значения атрибута и возвращаем уникальные

        return list(set(element.get("MayRequire") for element in elements if element.get("MayRequire") is not None)) or None

    except Exception as ex:
        print(f"Error processing XML: {ex}")
        return None


def main(database: MultiIndexDict):
    parent_pathes: list[Path] = []
    founded_ids = []
    founded_names = []
    printy('-----------------------------------------------------------------------------------------', '<o')
    searching_ids_and_names = get_modDependencies()
    printy('-----------------------------------------------------------------------------------------', '<o')
    for iid, name in searching_ids_and_names:

        results = search_in_database_by_id(database, iid, name)
        if results is None:
            results = search_in_database_by_name(database, iid, name)
            if results is None:
                results = search_in_database_by_fuzzyname(database, iid, name)
                if results is None:
                    results = search_in_database_by_part_find(database, iid, name)
        if results is not None:
            for r in results:
                founded_ids.append(r['packageid'])
                founded_names.append(r['name'])
                parent_pathes.append(r['path'])
    printy('-----------------------------------------------------------------------------------------', '<o')
    searching_ids = get_loadAfter()

    if searching_ids:
        printy('\t\t\tAbout.xml loadAfter mods', '<o')
        printy(f'\t\t\t{escape_printy_string(str(searching_ids))}', '<o')
    for iid in searching_ids:
        if iid not in founded_ids:
            results = search_in_database_by_id(database, iid, None)
            if results is not None:
                for r in results:
                    founded_ids.append(r['packageid'])
                    founded_names.append(r['name'])
                    parent_pathes.append(r['path'])

    searching_ids = get_loadFolders()

    if searching_ids is not None:
        printy('\t\t\tLoadfolders mods', '<o')
        printy(f'\t\t\t{escape_printy_string(str(searching_ids))}', '<o')
        for iid in searching_ids:
            if iid not in founded_ids:
                results = search_in_database_by_id(database, iid, None)
                if results is not None:
                    for r in results:
                        founded_ids.append(r['packageid'])
                        founded_names.append(r['name'])
                        parent_pathes.append(r['path'])

    return set(parent_pathes)
