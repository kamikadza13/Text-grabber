import os
from pathlib import Path
from xml import etree

from lxml import etree as ET


def find_patches_with_text(patches_list: dict[Path, Path], Tags_to_extraction: list[str]):
    if not patches_list:
        return


    for path, nfolder in patches_list.items():

        try:
            with open(path, 'r', encoding="utf-8") as xml_file:
                # print(p)
                # input()
                tree = ET.parse(xml_file)
            root = tree.getroot()
            operations = root.findall("Operation")

                # Remove Operation tags
            for operation in operations:
                if operation.get('Class') == 'PatchOperationSequence':
                    ops = operation.find("operations")
                    if ops is not None:
                        for li in ops:
                            a = li.iter(Tags_to_extraction)
                            if not list(a):
                                ops.remove(li)

                a = operation.iter(Tags_to_extraction)
                if not list(a):
                    root.remove(operation)
            if not root.getchildren():
                continue
            elif all([isinstance(a, etree._Comment) for a in root]):
                # ET.dump(root)
                # print("Комментарии")
                continue
            else:
                ...
                # print("Try write patch to:", os.path.join(np, tf.name))
                os.makedirs(nfolder, exist_ok=True)

                tree.write(nfolder / path.name, pretty_print=True, encoding='utf-8')

        except ET.ParseError as ex:
            print("Patch reading/writing/text-detecting error")
            print(ex)



