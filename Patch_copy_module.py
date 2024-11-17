import os
from dataclasses import dataclass

from lxml import etree as ET


@dataclass
class TranslatingFile:
    path: str
    name: str
    new_path: str

    def __repr__(self):
        return f"{self.path}"

def find_patches_with_text(patches_list: list[TranslatingFile], Tags_to_extraction: list[str]):
    if not patches_list:
        return


    for tf in patches_list:

        try:
            with open(tf.path, 'r', encoding="utf-8") as xml_file:
                # print(tf.path)
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
            elif all([a.tag is ET.Comment for a in root]):
                # ET.dump(root)
                # print("Комментарии")
                continue
            else:
                ...
                # print("Try write patch to:", os.path.join(tf.new_path, tf.name))
                os.makedirs(tf.new_path, exist_ok=True)
                tree.write(os.path.join(tf.new_path, tf.name), pretty_print=True, encoding='utf-8')

        except ET.ParseError as ex:
            print("Patch reading/writing/text-detecting error")
            print(ex)



