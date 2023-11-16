import copy
import logging
from tkinter import filedialog
import os
import shutil
from os.path import exists as file_exists
import lxml.etree as ET
import tkinter as tk
import lxml.etree as etree


import pyperclip
from difflib import SequenceMatcher

folder_translated = ""
folder_grabbed = ""
remove_original_tags_if_replaced = True
make_copy_deleted_files_ = False



# folder_grabbed = os.path.abspath(r'C:\Desktop\1\Update_mods_trouble\_Translation')
# folder_translated = os.path.abspath(r"C:\Desktop\1\Update_mods_trouble\Translated")



def add_elem_in_new_file(file: str, elem_list: list):
    with open(file, 'r', encoding="utf-8") as xml_file:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for el in elem_list:
            print(el.tag)
            root.append(el)
    with open(file, 'wb') as xml_file:
        tree.write(xml_file, encoding="utf-8")




def pop_comments(items: ET.Element):
    for idx, item in enumerate(items):
        if item.tag is ET.Comment:
            items.pop(idx)
            pop_comments(items)
            break



def update_translate():

    Updated_translate_folder = os.path.abspath(folder_translated + "\\" + "Updated_translate")
    if not file_exists(Updated_translate_folder): return
    new_xml_path = []
    new_xml_folder = []
    # print(f"Существует Updated_translate: {Updated_translate_folder}")

    for path, subdirs, files in os.walk(Updated_translate_folder):
        for file in files:
            if file.endswith('.xml'):
                if file != ('loadFolders.xml' or "About.xml"):
                    if "DefInjected" in path:
                        folder_in_DefInjected = path.rpartition('DefInjected\\')[2].partition('\\')[0]
                    else:
                        folder_in_DefInjected = ""
                        print(f'No DefInjected folder in {path + "/" + file}')

                    new_xml_path.append(path.lstrip(".\\") + "/" + file)
                    new_xml_folder.append(folder_in_DefInjected)

    old_xml_path = []
    old_xml_folder = []

    for path, subdirs, files in os.walk(folder_translated):
        for file in files:
            if file.endswith('.xml'):
                if file != ('loadFolders.xml' or "About.xml") and "Updated_translate" not in path:
                    if "DefInjected" in path:
                        folder_in_DefInjected = path.rpartition('DefInjected\\')[2].partition('\\')[0]
                    else:
                        folder_in_DefInjected = ""
                        print(f'No DefInjected folder in {path + "/" + file}')

                    old_xml_path.append(path.lstrip(".\\") + "/" + file)
                    old_xml_folder.append(folder_in_DefInjected)

    folders = set(old_xml_folder)

    folders_elements = [[i] for i in folders]
    # print('folders_elements', folders_elements)
    for fold_idx, folder in enumerate(folders):
        for inx, old_fold in enumerate(old_xml_folder):
            if old_fold == folder:
                file = old_xml_path[inx]
                with open(file, 'r', encoding="utf-8") as xml_file:
                    root = ET.parse(xml_file).getroot()
                    # print(f"Open file {file}")
                items = list(root)
                # print(f"Addind translated items:")
                # print([f'{i.tag} {i.text}' for i in items])

                pop_comments(items)
                # print(f"Очистка комментариев---------------------------------")
                # print(f"Addind translated items:")
                # print([f'{i.tag} {i.text}' for i in items])
                if len(folders_elements[fold_idx]) > 1:
                    for i in items:
                        folders_elements[fold_idx][1].append(i)
                        folders_elements[fold_idx][2].append(file)
                else:
                    folders_elements[fold_idx].append(items)
                    folders_elements[fold_idx].append([])
                    for item in items:
                        folders_elements[fold_idx][2].append(file)


    for indx, f in enumerate(new_xml_path):
        fold = new_xml_folder[indx]
        with open(f, 'r', encoding="utf-8") as xml_file:
            tree = ET.parse(xml_file)
            root = tree.getroot()

        print(f"File: {f}")
        removed_tags_and_xml = {}
        for folder_idx, the_folder in enumerate([folders_elements[i] for i in range(len(folders_elements))]):
            # print(the_folder[0])
            # print(fold)
            SequenceMatcher_ratio = SequenceMatcher(None, the_folder[0], fold).ratio()
            # print("Comparing:", the_folder[0], fold, "||", "SequenceMatcher ratio:", SequenceMatcher_ratio)
            if SequenceMatcher_ratio > 0.5:
                # print(the_folder)
                the_folder_tags = list(map(lambda item: item.tag, the_folder[1]))
                # print(f"All translated tags:")
                # print(the_folder_tags)
                the_folder_text = list(map(lambda item: item.text, the_folder[1]))
                # print("the_folder_text:", the_folder_text)
                # print(the_folder_tags)
                for r in root:
                    if r.tag is not ET.Comment:
                        # print(f"Element: '{r}'")
                        # print(f"tag text: {r.tag} {r.text}")
                        for item_idx, tag in enumerate(the_folder_tags):
                            # print(tag)
                            if r.tag == tag:
                                element_path = folders_elements[folder_idx][2][item_idx]
                                if not list(r):
                                    # print(f"Element: '{r}'")
                                    # print(f"tag text: {r.tag} {r.text}")
                                    # print(f"--------------------------Замена текста {r.text} на {the_folder_text[item_idx]}")
                                    r.text = the_folder_text[item_idx]
                                    # print(folders_elements)
                                else:
                                    # print(f"Замена элемента {r} на {the_folder[1][item_idx]}")
                                    r.clear()
                                    r.text = the_folder[1][item_idx].text
                                    r.tail = the_folder[1][item_idx].tail
                                    for _ in the_folder[1][item_idx]:
                                        r.append(copy.deepcopy(_))

                                if remove_original_tags_if_replaced:
                                    if element_path in removed_tags_and_xml:
                                        # print(f'{element_path} в removed_tags_and_xml:{removed_tags_and_xml}')
                                        # print("removed_tags_and_xml[element_path]", removed_tags_and_xml[element_path])
                                        removed_tags_and_xml[element_path].append(r)
                                    else:
                                        # print(f"Добавление {r} в {removed_tags_and_xml}")
                                        removed_tags_and_xml[element_path] = [r]
                                        # print(f"Итого {removed_tags_and_xml}")

        if remove_original_tags_if_replaced:
            if removed_tags_and_xml:
                remove_tag_from_old_translate_xml_file(removed_tags_and_xml)
        with open(f, 'wb') as xml_file:
            tree.write(xml_file, encoding="utf-8")

def remove_tag_from_old_translate_xml_file(dct: dict):
    for file in dct:
        if make_copy_deleted_files_:
            _ = os.path.normpath(file).replace('\\Languages\\', "\\Languages_copied_files\\").rpartition("\\")[0]
            name = os.path.normpath(file).replace('\\Languages\\', "\\Languages_copied_files\\").rpartition("\\")[2]
            print("_ :", _)
            print("name :", name)
            if file_exists(_):
                shutil.rmtree(_)
            os.makedirs(_, exist_ok=True)
            logging.warning(f"Make copy:\n{file} into \n{_}\\{name}")
            shutil.copy(file, _ + '/' + name)


        with open(file, 'r', encoding="utf-8") as xml_file:
            parser = etree.XMLParser(remove_comments=True, remove_blank_text=True, )
            tree = ET.parse(xml_file, parser)
        root = tree.getroot()
        # print("Начальный файл")
        # ET.dump(root)
        for el in dct[file]:
            for ch in root:
                if ch.tag == el.tag:
                    # print(f"Удаление {el.tag} из {file}")
                    ch.getparent().remove(ch)
                    break
        # print("Итоговый файл")
        # ET.dump(root)

        def remove_file(_: str):
            print(f"Empty xml - Remove empty file: {_}")
            os.remove(_)

        if len(root) == 0:
            print("No children, Len = 0")
            remove_file(file)
        elif all([ch.text is None for ch in root]):
            remove_file(file)
        else:
            with open(file, 'r', encoding="utf-8") as xml_file:
                parser = etree.XMLParser(remove_blank_text=True)
                tree = ET.parse(xml_file, parser)
            root = tree.getroot()
            for el in dct[file]:
                for ch in root:
                    if ch.tag == el.tag:
                        # print(f"Удаление {el.tag} из {file}")
                        ch.getparent().remove(ch)
                        break

            with open(file, 'w', encoding="utf-8") as xml_file:
                new_xml = etree.tostring(tree, pretty_print=True, encoding=str)
                xml_file.write(new_xml)


    print("--------")


def main():



    translated_xml_path = []
    new_xml_to_translate_path = []
    global folder_translated, folder_grabbed
    os.chdir(folder_grabbed)

    for path, subdirs, files in os.walk("."):
        for file in files:
            if file.endswith('.xml'):
                if file != ('loadFolders.xml' or "About.xml"):
                    new_xml_to_translate_path.append(path.lstrip(".\\") + "/" + file)


    os.chdir(folder_translated)
    for path, subdirs, files in (os.walk(".")):
        for file in files:
            if file.endswith('.xml'):
                if file != ('loadFolders.xml' or "About.xml"):
                    translated_xml_path.append(path.lstrip(".\\") + "/" + file)



    if file_exists(f'Updated_translate'):
        shutil.rmtree('Updated_translate')

    os.makedirs(f"Updated_translate", exist_ok=True)
    for inx, file in enumerate(new_xml_to_translate_path):
        if file in translated_xml_path:
            # print(f"Same file in same folders:{file}")
            with open(folder_grabbed + "/" + file, 'r', encoding="utf-8", errors='ignore') as xml_file:
                root = ET.parse(xml_file).getroot()
            Grabbed_elements = list(root)
            with open(file, 'r', encoding="utf-8", errors='ignore') as xml2_file:
                root2 = ET.parse(xml2_file).getroot()
            Translated_elements = list(root2)
            elements2_tag = []
            adding_elems = []
            print(f"Grabbed:{Grabbed_elements}")
            print(f"Translated:{Translated_elements}")
            for TrE in Translated_elements:
                elements2_tag.append(TrE.tag)
            for GrE in Grabbed_elements:
                if GrE.tag not in elements2_tag:
                    adding_elems.append(GrE)
            if adding_elems:
                print(f"adding_elems:{adding_elems}")
                os.makedirs("Updated_translate/" + file.rpartition("/")[0], exist_ok=True)
                shutil.copyfile(file, "Updated_translate/" + file)
                add_elem_in_new_file("Updated_translate/" + file, adding_elems)
        else:
            print(f"No same file in same folder {file}")
            os.makedirs("Updated_translate/" + file.rpartition("/")[0], exist_ok=True)
            shutil.copy(folder_grabbed + '/' + file, "Updated_translate/" + file)

    # for file in new_xml_to_translate_path:
    #     os.makedirs("Updated_translate/" + file.rpartition("/")[0], exist_ok=True)
    #     shutil.copy(folder_grabbed + '/' + file, "Updated_translate/" + file)


    update_translate()


def run_gui():


    def run_main():
        global folder_translated, folder_grabbed
        folder_translated = path_entry.get().replace("Path to Translated Folder...", "").strip()
        folder_grabbed = path_entry2.get().replace("Path to Grabbed (ready to translate) Mod Folder...", "").strip()


        if folder_translated != "" and folder_grabbed != "":
            gui_root.destroy()
            main()

    gui_root = tk.Tk()
    remove_original_tags_if_replaced_var = tk.BooleanVar()
    make_copy_deleted = tk.BooleanVar()
    gui_root.geometry("+300+400")
    gui_root.attributes('-topmost', True)

    path_entry = tk.StringVar()
    path_entry2 = tk.StringVar()

    gui_root.title("Translate Updater")
    gui_root.resizable(False, False)
    gui_root.configure(background='yellow')

    def on_entry_click(_, textbox):
        textbox.delete(0, 'end')
        textbox.config(fg='black')
        textbox.unbind('<FocusIn>')

    def keypress(e, textbox):
        if e.keycode == 86 and e.keysym != 'v':
            textbox.insert(tk.END, pyperclip.paste())
        elif e.keycode == 67 and e.keysym != 'c':
            pyperclip.copy(textbox.get())
        elif e.keycode == 88 and e.keysym != 'x':
            pyperclip.copy(textbox.get())
            textbox.delete(0, tk.END)

    Main_frame = tk.Frame(gui_root, background='red')
    Main_frame.pack(expand=True, fill='x', anchor='nw')
    Enter_textbox_text = f"Path to Translated Folder"
    Enter_textbox = tk.Entry(Main_frame, textvariable=path_entry, width=50)
    Enter_textbox.insert(0, f'{Enter_textbox_text}...')
    Enter_textbox.bind('<FocusIn>', lambda e: on_entry_click(e, Enter_textbox))
    Enter_textbox.config(fg='grey')
    Enter_textbox.pack(side="left")


    Enter_textbox.bind("<Control-KeyPress>", lambda e: keypress(e, Enter_textbox))
    Enter_textbox.pack(expand=True, fill='both', anchor='nw', side='left')
    Enter_textbox.event_add('<<Paste>>', '<Control-igrave>')

    def enter_translated_mod_folder():
        global folder_translated
        folder_translated = os.path.abspath(filedialog.askdirectory(title="ALREADY TRANSLATED mod folder"))
        on_entry_click("_", Enter_textbox)
        Enter_textbox.insert(tk.END, folder_translated)


    Enter_button = tk.Button(Main_frame, text="...", width=3, command=enter_translated_mod_folder)
    Enter_button.pack(fill='x', anchor='ne', side='right')


    Main_frame2 = tk.Frame(gui_root, background='blue')
    Main_frame2.pack(expand=True, fill='x', anchor='nw')
    Enter_textbox_2_text = f"Path to Grabbed (ready to translate) Mod Folder"
    Enter_textbox_2 = tk.Entry(Main_frame2, textvariable=path_entry2, width=50)
    Enter_textbox_2.insert(0, f'{Enter_textbox_2_text}...')
    Enter_textbox_2.bind('<FocusIn>', lambda e: on_entry_click(e, Enter_textbox_2))
    Enter_textbox_2.config(fg='grey')
    Enter_textbox_2.pack(side="left")


    Enter_textbox_2.bind("<Control-KeyPress>", lambda e: keypress(e, Enter_textbox_2))
    Enter_textbox_2.pack(expand=True, fill='both', anchor='nw', side='left')
    Enter_textbox_2.event_add('<<Paste>>', '<Control-igrave>')

    def enter_grabbed_mod_folder():
        global folder_grabbed
        folder_grabbed = os.path.abspath(filedialog.askdirectory(title="NOT TRANSLATED but GRABBED text folder"))
        on_entry_click("_", Enter_textbox_2)
        Enter_textbox_2.insert(tk.END, folder_grabbed)

    Enter_button_2 = tk.Button(Main_frame2, text="...", width=3, command=enter_grabbed_mod_folder)
    Enter_button_2.pack(fill='x', anchor='ne', side='right')

    Main_frame3 = tk.Frame(gui_root, background='blue')
    Main_frame3.pack(expand=True, fill='x', anchor='nw')

    Run_button = tk.Button(Main_frame3, text="Run", width=3, command=run_main)
    Run_button.pack(expand=True, fill='x', anchor='nw')

    def checkbutton_changed():
        global remove_original_tags_if_replaced
        remove_original_tags_if_replaced = remove_original_tags_if_replaced_var.get()
        print("remove_original_tags_if_replaced", remove_original_tags_if_replaced)
        # Checkbox_make_copy_deleted_files.setvar('state', 'normal' if remove_original_tags_if_replaced else 'disabled')
        Checkbox_make_copy_deleted_files.configure(state=tk.NORMAL if remove_original_tags_if_replaced else 'disabled')

    def checkbutton_changed2():
        global make_copy_deleted_files_
        make_copy_deleted_files_ = make_copy_deleted.get()
        print("make_copy_deleted", make_copy_deleted_files_)

    global remove_original_tags_if_replaced
    global make_copy_deleted_files_

    Checkbox_remove_replaced_tags = tk.Checkbutton(Main_frame3, text="Remove replaced tags tags from ALREDY TRANSLATED files", width=3, command=checkbutton_changed, variable=remove_original_tags_if_replaced_var)
    remove_original_tags_if_replaced_var.set(remove_original_tags_if_replaced)
    Checkbox_remove_replaced_tags.pack(expand=True, fill='x', anchor='nw')


    make_copy_deleted.set(make_copy_deleted_files_)
    Checkbox_make_copy_deleted_files = tk.Checkbutton(Main_frame3, text="Make copy deleted files", width=3, command=checkbutton_changed2, variable=make_copy_deleted, state=tk.NORMAL if remove_original_tags_if_replaced else 'disabled')
    Checkbox_make_copy_deleted_files.configure(state=tk.NORMAL if remove_original_tags_if_replaced else 'disabled')

    Checkbox_make_copy_deleted_files.pack(expand=True, fill='x', anchor='nw')


    gui_root.mainloop()


if __name__ == '__main__':
    if folder_translated != "" and folder_grabbed != "":
        main()
    else:
        run_gui()



