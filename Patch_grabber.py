import copy
import os
import re
import lxml.etree as etree
from dataclasses import dataclass

@dataclass
class RootElemAndElems:
    root_tag: etree.Element
    last_node: etree.Element



list_of_extract_tags = []
Parent_name_list, Parent_elem = [], []

patches_folder = os.path.abspath(r"C:\Desktop\1\Patches")
output_folder = patches_folder.rpartition("\\")[0]

patches = []
text_final = []

sabaka_names_all = []
sibling_list = []

# for path, subdirs, files in os.walk(rimworld_data_folder):
#     for file in files:
#         if "Defs" in path:
#             if file.endswith('.xml'):
#                 with open(file) as patch:
#                     # parser = etree.XMLParser(remove_comments=True, remove_blank_text=True)
#                     # tree = etree.parse(patch, parser)
#                     # root = tree.getroot()


def find_patch_pathes():
    for dirpath, dirnames, filenames in os.walk(patches_folder):
        for name in filenames:
            if name.endswith(".xml"):
                patches.append(f"{dirpath}\\{name}")


find_patch_pathes()

with open(r'C:\Text_grabber\Settings\Tag to extraction.txt', encoding="utf8") as tag_file:
    for line in tag_file:
        list_of_extract_tags.append(line.strip("\n "))


def output_not_in_siblings(r: etree.Element):
    _ = etree.tostring(r, encoding=str, pretty_print=True, with_tail=False)
    if _ in sibling_list:
        # print(f"Элемент уже выведен : {_}")
        return False
    sibling_list.append(_)
    return True

def update_parents(Parent_name_lis: list, Parent_elem_lis: list, sabaka_name: etree.Element, xpath: str):
    print("def update_parents:")
    print(Parent_name_lis)
    print(Parent_elem_lis)
    print(sabaka_name)
    print(xpath)
    ...


def xpath_to_elems(xpath: str, value: etree.Element):
    def make_elem_tree_by_elems_str(list_of_elems: list) -> RootElemAndElems:
        # for idx, el in enumerate(list_of_elems):
        #     if "[" in el:
        #         print(f"[ in elem tag: {el}")
        #         list_of_elems[idx] = re.sub(fr"\[.*]", '', el)
        root_node = etree.Element(list_of_elems[0])
        last_node = root_node
        for elem in list_of_elems[1:]:
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
        xpath_ = re.sub(fr'not\(.*?\)', '', xpath_).replace("\n", "").replace("\t", "").replace("[]", '').strip()
        if xpath_.startswith("*/"):
            xpath_ = re.sub(r"\*/(.*?Def\[)|\*/(.*?Def/)", "\\1\\2", xpath)
        # if xpath_ != _:
        #     print("xpath_ до:   ", _)
        #     print("xpath_ после:", xpath_)
        return xpath_

    value_str = etree.tostring(value, encoding=str, pretty_print=True, with_tail=False)
    if not any([a in value_str for a in list_of_extract_tags]):
        del value_str
        return None

    xpath = clear_xpath(xpath)
    or_count = len(re.findall(r' or ', xpath))

    defnames = re.findall(r'defName\s?=\s?[\"|\'](.*?)[\"|\']', xpath)
    sabaka_names = re.findall(r'@Name\s?=\s?[\"|\'](.*?)[\"|\']', xpath)
    sabaka_classes = re.findall(r'@Class\s?=\s?[\"|\'](.*?)[\"|\']', xpath)
    if sabaka_classes:
        print('sabaka_classes', sabaka_classes)
    if sabaka_names:
        print('sabaka_names', sabaka_names)
    exit_list = []

    if xpath in ["/", "//", "", "Defs", "/Defs", '//Defs']:
        for ch in value:
            if output_not_in_siblings(ch):
                text_final.append(etree.tostring(ch, pretty_print=True, encoding=str))

        return None


    def split_xpath(_):
        _ = re.sub(r"\[.*]", "", _)
        _ = re.split(r'/|(<defName.*_defName>)|(@Class=".*")', _)
        _ = [b.replace("_defName", "/defName") for b in _ if b not in ["Defs", "Def", None, ""]]
        return _

    if or_count > 0:
        print('or_count: ', or_count)
    if defnames:
        for defname in defnames:
            print('xpath', xpath)
            a = re.sub(fr"\[.*{defname}.*?]", fr"<defName>{defname}<_defName>", xpath)
            if sabaka_classes:
                for sabaka_class in sabaka_classes:
                    a = re.sub(fr"\[.*{sabaka_class}.*?]", fr'@Class="{sabaka_class}"', a)
                    c = split_xpath(a)
                    print('sabaka_class', a)
                    b = make_elem_tree_by_elems_str(c)
                    exit_list.append(b)
            else:
                c = split_xpath(a)
                print('Only defnames', a)
                b = make_elem_tree_by_elems_str(c)
                exit_list.append(b)

    elif sabaka_names:
        for sabaka_name in sabaka_names:
            sabaka_names_all.append(sabaka_name)
            update_parents(Parent_name_list, Parent_elem, sabaka_name, xpath)


    else:
        print("xpath without defname")
        # text_final.append("<!-- xpath without defname -->\n")
        text_final.append(f"<!-- {xpath} -->\n")
        if "[" in xpath:
            xpath = re.sub(r"\[.*]", "", xpath)
            a = re.split(r"/", xpath)
            a = [b for b in a if b]
            print(f"NO defnames:", a)
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
            text_final.append(etree.tostring(roots_and_elems.root_tag, pretty_print=True, encoding=str))
            text_final.append("\n")


def PatchOperationReplace(operation_replace: etree.Element):
    xpath = ""
    value = etree.Element("d")

    for a in operation_replace:
        if a.tag == "xpath":
            # print(f"xpath = {a.text}")
            xpath = a.text
        if a.tag == "value":
            value = a

    list_of_roots_and_elems_to_add = xpath_to_elems(xpath, value)
    if list_of_roots_and_elems_to_add is None:
        return None
    for roots_and_elems in list_of_roots_and_elems_to_add:
        for child in value:
            _ = roots_and_elems.last_node.getparent()
            _.append(copy.deepcopy(child))
            _.remove(roots_and_elems.last_node)
        if output_not_in_siblings(roots_and_elems.root_tag):
            text_final.append(etree.tostring(roots_and_elems.root_tag, pretty_print=True, encoding=str))
            text_final.append("\n")


def PatchOperationSequence(op: etree.Element):
    for a1 in op:
        if a1.tag == "operations":
            for operation in a1:
                operation_selector(operation)


def PatchOperationFindMod(Operation_Class_PatchOperationFindMod: etree.Element):
    for ch in Operation_Class_PatchOperationFindMod:
        if ch.tag.lower() == "mods":
            for li in ch:
                text_final.append(f"\n<!-- Mod:{li.text} -->\n")
                # print(mod_name)
        if ch.tag.lower() == "match":
            operation_selector(ch)
        if ch.tag.lower() == "nomatch":
            operation_selector(ch)


def XmlExtensions_FindMod(_: etree.Element):
    for ch in _:
        match ch.tag.lower():
            case "mods":
                for li in ch:
                    text_final.append(f"\n<!-- Mod:{li.text} -->\n")
            case "casetrue":
                for a in ch:
                    operation_selector(a)
            case "casefalse":
                for a in ch:
                    operation_selector(a)


def PatchOperationConditional(Operation_Class_PatchOperationConditional: etree.Element):
    for ch in Operation_Class_PatchOperationConditional:
        if ch.tag == "match":
            operation_selector(ch)
        if ch.tag == "nomatch":
            operation_selector(ch)


def operation_selector(a: etree.Element):
    Op_class = a.attrib["Class"]
    match Op_class:

        case "PatchOperationSequence":
            PatchOperationSequence(a)
        case "PatchOperationFindMod":
            PatchOperationFindMod(a)
        case "XmlExtensions.FindMod":
            XmlExtensions_FindMod(a)
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


text_final.append("<Defs>\n")
print(patches)
for file in patches:
    # try:
    with open(file, encoding="utf-8") as patch:
        print(f"file:", file)
        text_final.append(f"<!-- {file} -->\n")
        parser = etree.XMLParser(remove_comments=True, remove_blank_text=True, )
        tree = etree.parse(patch, parser)
        root = tree.getroot()

    for operation1 in root:
        operation_selector(operation1)
# except Exception as ex:
#     logging.warning(ex)
#     print(ex)
text_final.append("\n</Defs>")
os.makedirs(output_folder + r"\\__Defs_from_patches\\", exist_ok=True)
file_final = output_folder + r"\\__Defs_from_patches\\_" + patches_folder.rpartition("\\")[2] + ".xml"
print(file_final)
with open(fr"{file_final}", "w") as new_patch_file:
    for line in text_final:
        new_patch_file.write(line)


def make_Def_xml():
    ...


def set_parents_list(Parent_name_list_get: list, Parent_elem_get: list):
    global Parent_name_list, Parent_elem
    Parent_name_list = Parent_name_list_get
    Parent_elem = Parent_elem_get

# if __name__ == '__main__':
#
#
# def run_gui():
#
#
#     def run_main():
#         global patches_folder
#         global output_folder
#         patches_folder = path_entry.get()
#         if path_entry.get() != "":
#             output_folder = patches_folder.rpartition("\\")[0]
#             gui_root.destroy()
#             main()
#
#     gui_root = tk.Tk()
#     gui_root.geometry("+300+400")
#     gui_root.attributes('-topmost', True)
#
#     path_entry = tk.StringVar()
#
#     gui_root.title("Patch to Defs")
#     gui_root.resizable(False, False)
#     gui_root.configure(background='yellow')
#
#     def on_entry_click(_, textbox):
#         textbox.delete(0, 'end')
#         textbox.config(fg='black')
#         textbox.unbind('<FocusIn>')
#
#     def keypress(e, textbox):
#         if e.keycode == 86 and e.keysym != 'v':
#             textbox.insert(tk.END, pyperclip.paste())
#         elif e.keycode == 67 and e.keysym != 'c':
#             pyperclip.copy(textbox.get())
#         elif e.keycode == 88 and e.keysym != 'x':
#             pyperclip.copy(textbox.get())
#             textbox.delete(0, tk.END)
#
#     Main_frame = tk.Frame(gui_root, background='red')
#     Main_frame.pack(expand=True, fill='x', anchor='nw')
#     Enter_textbox_text = f"Path to Patch folder"
#     Enter_textbox = tk.Entry(Main_frame, textvariable=path_entry, width=50)
#     Enter_textbox.insert(0, f'{Enter_textbox_text}...')
#     Enter_textbox.bind('<FocusIn>', lambda e: on_entry_click(e, Enter_textbox))
#     Enter_textbox.bind('<Return>', lambda _: run_main())
#     Enter_textbox.config(fg='grey')
#     Enter_textbox.pack(side="left")
#
#
#     Enter_textbox.bind("<Control-KeyPress>", lambda e: keypress(e, Enter_textbox))
#     Enter_textbox.pack(expand=True, fill='both', anchor='nw', side='left')
#     Enter_textbox.event_add('<<Paste>>', '<Control-igrave>')
#
#     def enter_translated_mod_folder():
#         folder_translated = os.path.abspath(filedialog.askdirectory(title="Patch folder"))
#         path_entry.set(folder_translated)
#         if folder_translated:
#             run_main()
#
#
#     Enter_button = tk.Button(Main_frame, text="...", width=3, command=enter_translated_mod_folder)
#     Enter_button.pack(fill='x', anchor='ne', side='right')
#
#     # Main_frame3 = tk.Frame(gui_root, background='blue')
#     # Main_frame3.pack(expand=True, fill='x', anchor='nw')
#
#     gui_root.mainloop()
#
#
# run_gui()
