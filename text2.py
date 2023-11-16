import logging
import os
import xml.etree.ElementTree as ET


Rimworld_mods_folder_path_ = r"D:\Games\steamapps\workshop\content\294100"

about_path_ = r'D:\Games\steamapps\workshop\content\294100\2479560240\About\About.xml'



def parent_folders(Rimworld_mods_folder_path, about_path):
    def open_about(about_path__):
        path = os.path.normpath(about_path__)
        try:
            with open(path, encoding="utf-8") as about:
                parse = ET.parse(about)
                root1 = parse.getroot()
                return root1
        except Exception as ex:
            print(ex)
            return None

    def read_dependence_from_abot(root1):
        dependence_list_1 = {}
        load_after_packageid = []
        for data in root1:
            if "moddependencies" == data.tag.lower():
                all_dependence = [_ for _ in data]
                if all_dependence:
                    for idx, dependence in enumerate(all_dependence):
                        dd = {}
                        # dependence_list_1.update({"#": str(idx)})
                        steam_id, packageid = '', '',
                        for a in dependence:

                            tag = a.tag.lower()
                            match tag:
                                case 'packageid':
                                    if a.text is not None:
                                        packageid = a.text
                        dd.update({"packageId": packageid})

                        dependence_list_1[idx] = dd

            if "loadafter" == data.tag.lower():
                for _ in data:
                    load_after_packageid.append(_.text)

        packageid_list = [_ for _ in [dependence_list_1[a]["packageId"] for a in dependence_list_1]]

        for _ in load_after_packageid:
            if _ not in packageid_list:
                dependence_list_1[len(dependence_list_1) + 1] = {"packageId": _}
        return dependence_list_1

    def read_folders_package_id(folders_: list):
        aa = {}
        packageId = ""
        for idx, f in enumerate(folders_):
            about = f"{f}\\About\\About.xml"
            root_ = open_about(about)
            # ET.dump(root_)
            if root_ is not None:
                for ch in root_:
                    tag = ch.tag
                    match tag:
                        case 'packageId':
                            packageId = ch.text
                            break
                        case 'packageid':
                            packageId = ch.text
                            break
                        case 'Packageid':
                            packageId = ch.text
                            break
                        case 'PackageId':
                            packageId = ch.text
                            break
                        case _:
                            packageId = ""

            else:
                packageId = ""
            # print(f, packageId)
            aa[idx] = {"path": f, "packageId": packageId}
        return aa

    def search_folders_to_add_parent(folders_to_check: dict, dependence_list_: dict):
        _ = []
        for a in folders_to_check:
            if folders_to_check[a]['packageId'] in [dependence_list_[b]['packageId'] for b in dependence_list_]:
                _.append(folders_to_check[a]['path'])
                # print(folders_to_check[a]['path'])
        return _

    root = open_about(about_path)
    dependence_list = read_dependence_from_abot(root)

    if Rimworld_mods_folder_path:
        folders = list(filter(os.path.isdir,
                              [os.path.join(Rimworld_mods_folder_path, f) for f in
                               os.listdir(Rimworld_mods_folder_path)]))

        folders_package_id = read_folders_package_id(folders)
        path_to_parents_folder = search_folders_to_add_parent(folders_package_id, dependence_list)
    else:
        return None


    return path_to_parents_folder


if __name__ == '__main__':

    print(parent_folders(Rimworld_mods_folder_path_, about_path_))
