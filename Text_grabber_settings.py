import gettext
import os
import shutil
import tkinter as tk
from ctypes import windll
from pathlib import Path
from tkinter import PhotoImage
from tkinter import filedialog
from tkinter.ttk import Labelframe

import ttkbootstrap as ttk
import win32con
import win32gui
from ttkbootstrap import Frame
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.tooltip import ToolTip

import image_edit
import locale
from Settings_module import SVV as SV

Window_Text_grabber: ttk.Window
Window_Hidden: ttk.Toplevel
Window_settings_app: ttk.Toplevel


current_locale, encoding = locale.getdefaultlocale()


gettext.install('T_test', 'locale/')

ru_translation = gettext.translation('T_test', 'locale/', fallback=True, languages=['ru'])
en_translation = gettext.NullTranslations()




class ToolTipImage(ToolTip):
    def __init__(self, widget, text=None, bootstyle=None, wraplength=None, delay=250, image=None, **kwargs):
        super().__init__(widget, text, bootstyle, wraplength, delay, **kwargs)
        self.image = image

    def show_tip(self, *_):
        """Create a show the tooltip window"""
        if self.toplevel:
            return
        x = self.widget.winfo_pointerx() + 25
        y = self.widget.winfo_pointery() + 10

        self.toplevel = ttk.Toplevel(position=(x, y), **self.toplevel_kwargs)
        lbl = ttk.Label(
            master=self.toplevel,
            padding=0,
            image=self.image
        )
        lbl.pack(fill=ttk.BOTH, expand=ttk.YES)

        add_text = True if self.text else False

        if add_text:
            lbl_label = ttk.Label(
                master=self.toplevel,
                text="\t" + self.text,
                justify=ttk.LEFT,
                wraplength=self.wraplength,

            )
            lbl_label.pack(fill=ttk.BOTH, expand=ttk.YES, )
        else:
            lbl_label = None
        if self.bootstyle:
            # noinspection PyArgumentList
            lbl.configure(bootstyle=self.bootstyle)
            if add_text:
                # noinspection PyArgumentList
                lbl_label.configure(bootstyle=self.bootstyle)
        else:
            lbl.configure(style="tooltip.TLabel")
            if add_text:
                lbl_label.configure(style="tooltip.TLabel")

class NewCheckButton(ttk.Checkbutton):
    def __init__(self, parent, text, sv_key, sv_key_text, tooltip_text=None, tooltip_image=None, wraplength=320, command_add=None, **pack_kwargs):
        self.sv_key_text = sv_key_text
        self.command_add = command_add
        self.var = ttk.BooleanVar(value=sv_key)

        super().__init__(parent, text=text, variable=self.var, command=self.checkbtn_command)
        if tooltip_image:
            if tooltip_text:
                ToolTipImage(self,text=tooltip_text, wraplength=wraplength, image=tooltip_image)
        elif tooltip_text:
            ToolTip(self, text=tooltip_text, wraplength=wraplength)

    def checkbtn_command(self):
        SV.set(self.sv_key_text, self.var.get())
        if self.command_add:
            self.command_add()

    def get(self):
        return self.var.get()



class HeaderFrame(Frame):
    def __init__(self, app, main_frame):
        super().__init__(main_frame)
        self.app = app
        self.main_frame = main_frame
        self.build_ui()

    def Title_language_selector_selected(self, event):
        if event.widget.get() == 'Русский':
            ru_translation.install()
            SV.Settings_language = 'ru'

            print("Russian lang set")
        else:
            en_translation.install()
            SV.Settings_language = 'en'

            print("Eng lang set")

        SV.set('Settings_language', SV.Settings_language)
        self.app.rebuild_ui()

    def build_ui(self):
        label = ttk.Label(self, text=_('Text Grabber Settings'), style='Title.TLabel')
        label.pack(side='left')
        ttk.Button(self, text='⨉', command=self.app.exit_app, style='Close.TButton').pack(side='right', padx=(5,0))
        # noinspection PyArgumentList
        Header_lang_selector_combo = ttk.Combobox(self, values=list(self.app.LANG_MAP), state='readonly', bootstyle='light')
        Header_lang_selector_combo.pack(side='right', padx=(5,0))
        ToolTip(Header_lang_selector_combo, text=_("Select Language of Settings Programm"), wraplength=320)



        Header_lang_selector_combo.bind("<<ComboboxSelected>>", self.Title_language_selector_selected)
        Header_lang_selector_combo.current(1 if SV.Settings_language == 'ru' else 0)

        label2 = ttk.Label(self, text="Language:")
        label2.pack(side='right', padx=0)

        self.pack(fill='x', padx=(0,0), pady=0)


        self.bind("<ButtonPress-1>", self.start_move)
        label.bind("<ButtonPress-1>", self.start_move)
        label2.bind("<ButtonPress-1>", self.start_move)
        self.bind("<ButtonRelease-1>", self.stop_move)
        label.bind("<ButtonRelease-1>", self.stop_move)
        label2.bind("<ButtonRelease-1>", self.stop_move)
        self.bind("<B1-Motion>", self.do_move)
        label.bind("<B1-Motion>", self.do_move)
        label2.bind("<B1-Motion>", self.do_move)

    def start_move(self, event):
        """Начало перемещения окна"""
        self.app._drag_start_x = event.x_root
        self.app._drag_start_y = event.y_root
        self.app._drag_win_x = self.app.winfo_x()
        self.app._drag_win_y = self.app.winfo_y()

    def stop_move(self, event):
        """Окончание перемещения"""
        self.app._drag_start_x = None
        self.app._drag_start_y = None

    def do_move(self, event):
        """Процесс перемещения окна"""
        if not hasattr(self.app, '_drag_start_x') or self.app._drag_start_x is None:
            return

        # Вычисляем смещение относительно начальной позиции
        delta_x = event.x_root - self.app._drag_start_x
        delta_y = event.y_root - self.app._drag_start_y

        # Новая позиция окна
        new_x = self.app._drag_win_x + delta_x
        new_y = self.app._drag_win_y + delta_y

        # Обновляем геометрию окна
        self.app.geometry(f"+{new_x}+{new_y}")

class GeneralFrame(Frame):
    def __init__(self, app, main_frame, master_frame,):
        super().__init__(master=master_frame)
        self.app = app
        self.main_frame = main_frame
        self.Note_book: ttk.Notebook = master_frame
        self.build_ui()


    def build_ui(self):


        def frame_top():
            f1 = Frame(self, padding=(30, 5, 50, 5))
            f1.pack(expand=False, fill=tk.X)
            languages = ["Russian", "Catalan", "ChineseSimplified", "ChineseTraditional", "Czech", "Dutch", "French",
                         "German", "Hungarian", "Italian", "Korean", "Polish", "PortugueseBrazilian", "Romanian", "Spanish", "SpanishLatin",
                         "Turkish", "Ukrainian", _("Enter your language")]
            Label = ttk.Label(f1, text=_("Translate mod into:"))
            Label.pack(expand=False, side='left', padx=10)
            Label_tooltip_text = _(
                f"Choose the language you are going to translate mods into.\nRimworld has been officially translated into several languages, and in order for your translation of the mod to be automatically added to the game, and not act as a separate new language, use the preset languages from the list"
                f"\nIf you want to change the program language, then the language is selected at the top next to the program close button"
            )
            Label.ToolTip = ToolTip(Label, Label_tooltip_text, wraplength=320)

            # noinspection PyArgumentList
            Lang_selector = ttk.Combobox(f1, values=languages, state="readonly", bootstyle='light')
            Lang_selector.set(SV.Game_language)

            #   Disable MouseWheel chosing
            Lang_selector.bind("<MouseWheel>", 'break')

            def callbackFunc(event):
                SV.Game_language = event.widget.get()
                SV.set('Game_language', SV.Game_language)
                if SV.Game_language == languages[-1]:
                    Lang_selector['state'] = "!readonly"
                    Lang_selector.set('')
                else:
                    Lang_selector['state'] = "readonly"

            Lang_selector.bind("<<ComboboxSelected>>", callbackFunc)
            Lang_selector.bind("<Return>", callbackFunc)
            Lang_selector.pack(expand=True, fill=tk.X, side='left')
            Lang_selector.ToolTip = ToolTip(Lang_selector, Label_tooltip_text, wraplength=320)

        def frame_select_pathes():
            P_frame = Frame(self, padding=(30, 5, 50, 5))
            P_frame.pack(expand=False, fill=tk.X)

            P = ttk.Labelframe(self, text=_("Pathes to Rimworld folders"), padding=(30, 5))
            P.pack(fill='x', padx=20, pady=10)

            f1 = ttk.Frame(P)
            f1.pack(anchor='nw')

            def Select_Data_Path():
                a = filedialog.askdirectory(title=_("Select Data folder"))
                if a == '':
                    SV.Path_to_Data = None
                    f1.Label['text'] = _("Rimworld Data:\nNone")
                    Messagebox.show_warning(message=_('Folder Not selected'), parent=self.app, position=(300, 300))
                    SV.set('Path_to_Data', SV.Path_to_Data)
                    f1.Label['text'] = _("Rimworld Data:\n{Path_to_Data}").format(Path_to_Data=SV.Path_to_Data)
                else:
                    path = Path(a)
                    if path.name != 'Data':
                        SV.Path_to_Data = None
                        f1.Label['text'] = _("Rimworld Data:\nNone")
                        Messagebox.show_warning(message=_('Folder Not selected - Selected path is not Data folder'), parent=self.app, position=(300, 300))
                        SV.set('Path_to_Data', SV.Path_to_Data)
                        f1.Label['text'] = _("Rimworld Data:\n{Path_to_Data}").format(Path_to_Data=SV.Path_to_Data)

                SV.Path_to_Data = str(Path(a))
                SV.set('Path_to_Data', SV.Path_to_Data)
                f1.Label['text'] = _("Rimworld Data:\n{Path_to_Data}").format(Path_to_Data=SV.Path_to_Data)

            f1.Path_to_Data = ttk.Button(f1, text=_("Select path to Rimworld Data"), width=50, command=Select_Data_Path)
            f1.Path_to_Data.pack(expand=False, fill=tk.X, side='left')
            f1.Label = ttk.Label(f1, text=_("Rimworld Data:\n{Path_to_Data}").format(Path_to_Data=SV.Path_to_Data), wraplength=500)
            f1.Label.pack(padx=(20, 20), anchor='nw')
            f1.Path_to_Data.ToolTip = ToolTip(
                f1.Path_to_Data,
                _('Please specify the Data folder of the game, it will help to extract the text better. This is not necessary, but it allows you to find parent-child dependencies.'),
                wraplength=320)

            f2 = ttk.Frame(P)
            f2.pack(expand=False, fill=tk.X)

            def Select_Mod_Path():
                a = filedialog.askdirectory(title=_("Select MOD folder"))
                if a == '':
                    SV.set('Path_to_Mod_folder', None)
                else:
                    SV.set('Path_to_Mod_folder', str(Path(a)))

                f2.Label['text'] = _(
                    "Rimworld Mods Folder:\n{Path_to_Mod_folder}").format(Path_to_Mod_folder=SV.Path_to_Mod_folder)

            f2.Path_to_Mod = ttk.Button(f2, text=_("Select path to Rimworld Mods Folder"), width=50, command=Select_Mod_Path)
            f2.Path_to_Mod.pack(expand=False, fill=tk.X, side='left')
            f2.Label = ttk.Label(f2, text=_(
                "Rimworld Mods Folder:\n{Path_to_Mod_folder}").format(Path_to_Mod_folder=SV.Path_to_Mod_folder), wraplength=500)
            f2.Label.pack(padx=(20, 20), anchor='nw')

            f3 = ttk.Frame(P)
            f3.pack(expand=False, fill=tk.X)

            def Select_Another_Path():
                a = filedialog.askdirectory(title=_("Select Another mod folder"))
                if a == '':
                    SV.set('Path_to_Another_folder', None)
                else:
                    SV.set('Path_to_Another_folder', str(Path(a)))

                f3.Label['text'] = _(
                    "Another Rimworld Mods Folder:\n{Path_to_Another_folder}").format(Path_to_Another_folder=SV.Path_to_Another_folder)

            f3.Path_to_Another = ttk.Button(f3, text=_("Select path to another Rimworld Mods Folder"), width=50, command=Select_Another_Path)
            f3.Path_to_Another.pack(expand=False, fill=tk.X, side='left')
            f3.Label = ttk.Label(f3, text=_(
                "Another Rimworld Mods Folder:\n{Path_to_Another_folder}").format(Path_to_Another_folder=SV.Path_to_Another_folder), wraplength=500)
            f3.Label.pack(padx=(20, 20), anchor='nw')
            f3.Path_to_Another.ToolTip = ToolTip(
                f3.Path_to_Another,
                _('If you suddenly store mods somewhere else, you can specify this folder here. In this case, the program will work better with mods that depend on other mods (in case the values for translation are inherited from another mod).'),
                wraplength=320)

        def extraction_rules_frame():
            FF = ttk.Labelframe(self, text=_("Extraction files rules"))
            FF.pack(anchor=tk.N, side=tk.LEFT, padx=15)

            F = ttk.Frame(FF, padding=10)
            F.pack(anchor=tk.W)


            NewCheckButton(F,
                           _("Delete old version folders"),
                           SV.Delete_old_versions_translation,
                           'Delete_old_versions_translation',
                           tooltip_text=_('Delete (Not extract) text for older versions of Rimworld.\nBy default, the program extracts text for all available versions ( ... 1.0, 1.1, 1.2 ...). You can leave only the newest version, so as not to translate too much (Which I advise you to do)')
                           ).pack(anchor=tk.W, pady=(0, 0))

            NewCheckButton(F,
                           _("Merge Folders"),
                           SV.Merge_folders,
                           'Merge_folders',
                           tooltip_text=_('Merge version and Language folders into one Language folder\n(If there is only one version folder)')
                           ).pack(anchor=tk.W, pady=(10, 0))

            NewCheckButton(F,
                           _("Not rename files"),
                           SV.Not_rename_files,
                           'Not_rename_files',
                           tooltip_text=_("Files are automatically renamed depending on the folders they fall into. This is necessary to prevent the files from having the same names, which may lead to the fact that the game will not read the translation files.\n(Check the box if you don't like it and you want to keep the original titles)"
                                          )
                           ).pack(anchor=tk.W, pady=(10, 0))

            NewCheckButton(F,
                           _("Copy original patches"),
                           SV.Copy_original_patches,
                           'Copy_original_patches',
                           tooltip_text=_("If you don't trust text extraction from patches - It is many times more complex and the error rate can be high. When this option is enabled - the Program will copy patches that it thinks have text in them, so that you can manually check the extracted text. It will be in a separate folder - “From_patches”"
                                          )
                           ).pack(anchor=tk.W, pady=(10, 0))

        def other_frame():
            FF = ttk.Labelframe(self, text=_("Other"))
            FF.pack(anchor=tk.N, side=tk.LEFT, padx=(5, 0))

            F1 = ttk.Frame(FF, padding=10)
            F1.pack()


            NewCheckButton(F1,
                           _("Check updates"),
                           SV.Check_update,
                           'Check_update',
                           tooltip_text=_("Check updates from GitHub and Download it if find new version"
                                          )
                           ).pack(anchor=tk.W, pady=(0, 0))

            NewCheckButton(F1,
                           _("Adding xml-version-encoding string"),
                           SV.Adding_xml_version_encoding_string_ckeckbtn,
                           'Adding_xml_version_encoding_string_ckeckbtn',
                           tooltip_text=_('Add <?xml version="1.0" encoding="utf-8"?> at start of xml files'
                                          )
                           ).pack(anchor=tk.W, pady=(10, 0))


            NewCheckButton(F1,
                           _("Adding xml-version-encoding string in Keyed"),
                           SV.Adding_xml_version_encoding_string_in_Keyed,
                           'Adding_xml_version_encoding_string_in_Keyed',
                           tooltip_text=_('Add <?xml version="1.0" encoding="utf-8"?> at start of Keyed xml files'
                                          )
                           ).pack(anchor=tk.W, pady=(10, 0))

        def only_russian():
            FF = ttk.Labelframe(self, text=_("Russian language"))
            FF.pack(anchor=tk.N, side=tk.LEFT, padx=(5, 0))

            F1 = ttk.Frame(FF, padding=10)
            F1.pack()

            NewCheckButton(F1,
                           _("tools and death messages into russian"),
                           SV.Translate_tools_into_russian,
                           'Translate_tools_into_russian',
                           tooltip_text=_('Translate stock->приклад, barrel->ствол, acid fangs->кислотные клыки и т.п.'
                                          )
                           ).pack(anchor=tk.W, pady=(0, 0))


        self.Note_book.add(self, text=_('General Settings'))

        frame_top()
        frame_select_pathes()
        extraction_rules_frame()
        other_frame()
        only_russian()

class CommentFrame(Frame):
    def __init__(self, app, main_frame, master_frame,):
        super().__init__(master=master_frame)
        self.app = app
        self.main_frame = main_frame
        self.Note_book: ttk.Notebook = master_frame
        self.Note_book.add(self, text=_('Comments'))

        def change_comm_checkbtn_img():
            def get_img_code() -> str:
                a1 = 1 if self.Add_filename_comment.get() else 0
                a2 = 1 if self.Add_comment.get() else 0
                a3 = 1 if self.Comment_add_EN.get() else 0
                a4 = 1 if self.Comment_starting_similar_as_ogiganal_text.get() else 0
                a5 = 1 if self.Comment_spacing_before_tag.get() else 0
                a6 = 1 if self.Comment_replace_n_as_new_line.get() else 0

                if a2 == 0:
                    a3, a4, a5, a6 = 0, 0, 0, 0
                if a4 == 0:
                    a5 = 0
                return str(a1) + str(a2) + str(a3) + str(a4) + str(a5) + str(a6)

            self.Comm_Image.configure(file=f'Images/Comments/{get_img_code()}.png')

        def CommFrame_Add_comment():
            if self.Add_comment.get():
                self.Comment_add_EN.configure(state='normal')
                self.Comment_starting_similar_as_ogiganal_text.configure(state='normal')
                self.Comment_spacing_before_tag.configure(state='normal')
                self.Comment_replace_n_as_new_line.configure(state='normal')

                if self.Comment_starting_similar_as_ogiganal_text.get():
                    self.Comment_spacing_before_tag.configure(state='normal')
                else:
                    self.Comment_spacing_before_tag.configure(state='disabled')
            else:
                self.Comment_add_EN.configure(state='disabled')
                self.Comment_starting_similar_as_ogiganal_text.configure(state='disabled')
                self.Comment_spacing_before_tag.configure(state='disabled')
                self.Comment_replace_n_as_new_line.configure(state='disabled')
            change_comm_checkbtn_img()

        Frame_all = ttk.Frame(self)
        Frame_all.pack(expand=False, fill=tk.X, padx=50)

        fl = ttk.Frame(Frame_all, padding=10)
        fl.pack(anchor=tk.W, side=tk.LEFT, )


        self.Add_filename_comment = NewCheckButton(fl,
                       _("Add in file comment with FullPath of Original file"),
                       SV.Add_filename_comment,
                       'Add_filename_comment',
                       command_add=change_comm_checkbtn_img,
                       )
        self.Add_filename_comment.pack(anchor=tk.W, pady=(5,0))

        self.Add_comment = NewCheckButton(fl,
                       _("Add comments to grabbed text"),
                       SV.Add_comment,
                       'Add_comment',
                       command_add=CommFrame_Add_comment,
                       )
        self.Add_comment.pack(anchor=tk.W, pady=(5,0))

        self.Comment_add_EN = NewCheckButton(fl,
                       _('Add "EN:" before comment text'),
                       SV.Comment_add_EN,
                       'Comment_add_EN',
                       command_add=change_comm_checkbtn_img,
                       )
        self.Comment_add_EN.pack(anchor=tk.W, pady=(5,0))

        fr = ttk.Frame(Frame_all, padding=10)
        fr.pack(anchor='nw', side=tk.RIGHT,)

        def Comment_starting_similar_as_ogiganal_text_func():

            if self.Comment_starting_similar_as_ogiganal_text.get():
                self.Comment_spacing_before_tag.configure(state='normal')
            else:
                self.Comment_spacing_before_tag.configure(state='disabled')
            change_comm_checkbtn_img()


        self.Comment_starting_similar_as_ogiganal_text = NewCheckButton(fr,
                       _('Place the comment text exactly above the original text'),
                       SV.Comment_starting_similar_as_ogiganal_text,
                       'Comment_starting_similar_as_ogiganal_text',
                       command_add=Comment_starting_similar_as_ogiganal_text_func,
                       )
        self.Comment_starting_similar_as_ogiganal_text.pack(anchor=tk.W, pady=(5,0))


        self.Comment_spacing_before_tag = NewCheckButton(fr,
                       _('Left spacing are in before the comment'),
                       SV.Comment_spacing_before_tag,
                       'Comment_spacing_before_tag',
                       command_add=change_comm_checkbtn_img,
                       )
        self.Comment_spacing_before_tag.pack(anchor=tk.W, pady=(5,0))

        self.Comment_replace_n_as_new_line = NewCheckButton(fr,
                       _('Comment replace \\n as new line'),
                       SV.Comment_replace_n_as_new_line,
                       'Comment_replace_n_as_new_line',
                       command_add=change_comm_checkbtn_img,
                       )
        self.Comment_replace_n_as_new_line.pack(anchor=tk.W, pady=(5,0))

        if not self.Add_comment.get():
            self.Comment_add_EN.configure(state='disabled')
            self.Comment_starting_similar_as_ogiganal_text.configure(state='disabled')
            self.Comment_spacing_before_tag.configure(state='disabled')
            self.Comment_replace_n_as_new_line.configure(state='disabled')
        if not self.Comment_starting_similar_as_ogiganal_text.get():
            self.Comment_spacing_before_tag.configure(state='disabled')

        Comm_Image_Frame = ttk.Frame(self)
        Comm_Image_Frame.pack(anchor=tk.CENTER)

        self.Comm_Image = PhotoImage(file='Images/Comments/000000.png')
        self.Comm_Image_label = ttk.Label(Comm_Image_Frame, image=self.Comm_Image)
        self.Comm_Image_label.pack(anchor=tk.CENTER)

        change_comm_checkbtn_img()

class GrabFrame(Frame):
    def __init__(self, app, main_frame, master_frame,):
        super().__init__(master=master_frame)
        self.app = app
        self.main_frame = main_frame
        self.Note_book: ttk.Notebook = master_frame
        self.Note_book.add(self, text=_('Grabbing'))

        # self = ttk.Frame(self.Note_book)
        # self.pack(expand=True, fill=tk.BOTH)

        def F1():


            self.F1 = ttk.LabelFrame(self, text=_('Сommon'))
            self.F1.pack(expand=False, fill=tk.X, padx=50, pady=(10,0))


            f1 = Frame(self.F1, padding=10)
            f1.pack(anchor='ne', side='left', fill='y')

            Check_at_least_one_letter_in_text = NewCheckButton(f1,
                           _("Check at least one letter in text"),
                           SV.Check_at_least_one_letter_in_text,
                           'Check_at_least_one_letter_in_text',
                           tooltip_text=_('Check if there is at least one letter in the extracted text. This is necessary so as not to extract all sorts of (255, 123, 112).\nYou may want to remove the flag if the mod adds various symbols without letters that you want to translate like "<--",\nI do not know why to translate it at all, but who knows ^_^'
                                          )
                           )
            Check_at_least_one_letter_in_text.pack(anchor=tk.W, pady=(5,0))



        def F2():



            self.F2 = ttk.LabelFrame(self, text=_('Add missing translation'))
            self.F2.pack(fill=tk.X, padx=50, pady=(10,0))

            f21 = Frame(self.F2, padding=10)
            f21.pack(anchor=tk.W, pady=(5, 0), side='left', fill='y')

            add_titleFemale = NewCheckButton(f21,
                           _("Add titleFemale if it is not in the original file"),
                           SV.add_titleFemale,
                           'add_titleFemale',
                           )
            add_titleFemale.pack(anchor=tk.W, pady=(5,0))

            add_titleShortFemale = NewCheckButton(f21,
                           _("Add titleShortFemale if it is not in the original file"),
                           SV.add_titleShortFemale,
                           'add_titleShortFemale',
                           )
            add_titleShortFemale.pack(anchor=tk.W, pady=(5,0))

            f22 = Frame(self.F2, padding=10)
            f22.pack(anchor=tk.W, pady=(5, 0), side='left')

            plural_tooltip_text = _("Add missing tags to choose from in PawnKindDef if they don't exist.")

            labelPlural = NewCheckButton(f22,
                                         _("Add labelPlural"),
                                         SV.labelPlural,
                                         'labelPlural',
                                         tooltip_text=plural_tooltip_text
                                         )
            labelPlural.pack(anchor=tk.W, pady=(5,0))

            labelMale = NewCheckButton(f22,
                                       _("Add labelMale"),
                                       SV.labelMale,
                                         'labelMale',
                                       tooltip_text=plural_tooltip_text
                                       )
            labelMale.pack(anchor=tk.W, pady=(5,0))

            labelFemale = NewCheckButton(f22,
                                         _("Add labelFemale"),
                                         SV.labelFemale,
                                         'labelFemale',
                                         tooltip_text=plural_tooltip_text
                                         )
            labelFemale.pack(anchor=tk.W, pady=(5,0))

            labelMalePlural = NewCheckButton(f22,
                                             _("Add labelMalePlural"),
                                             SV.labelMalePlural,
                                         'labelMalePlural',
                                             tooltip_text=plural_tooltip_text
                                             )
            labelMalePlural.pack(anchor=tk.W, pady=(5,0))

            labelFemalePlural = NewCheckButton(f22,
                                               _("Add labelFemalePlural"),
                                               SV.labelFemalePlural,
                                         'labelFemalePlural',
                                               tooltip_text=plural_tooltip_text
                                               )
            labelFemalePlural.pack(anchor=tk.W, pady=(5,0))

            f23 = Frame(self.F2, padding=10)
            f23.pack(anchor=tk.W, side=tk.LEFT, fill='y')

            def Add_stuffAdjective_and_mark_it_command():
                if self.Add_stuffAdjective_and_mark_it.get():
                    mark_entry.configure(state='normal')
                else:
                    mark_entry.configure(state='disabled')

            self.Add_stuffAdjective_and_mark_it = NewCheckButton(f23,
                                                                 _("Add stuffAdjective and mark it"),
                                                                 SV.Add_stuffAdjective_and_mark_it,
                                                                 'Add_stuffAdjective_and_mark_it',
                                                                 command_add=Add_stuffAdjective_and_mark_it_command,
                                                                 tooltip_text=_("Some materials can be used to build buildings / make objects, but the authors do not add a special label for this. And in translation it turns out: 'Made of stone'. This is normal for English, but not for some languages.  Therefore, I decided to add a special label to understand how to translate a word as an adjective/ genitive. \n You can write yourself how to designate such words in the text. To correctly translate such a word, you need to mentally put 'The house is made of' in front of it. \n '~LABEL~' will be replaced with the original word. If you just want to add such words for translation, but do not want to mark them separately, then you can only write '~LABEL~'."
                                                                                )
                                                                 )
            self.Add_stuffAdjective_and_mark_it.pack(anchor=tk.W, pady=(5,0))

            Add_stuffAdjective_and_mark_it_text_var = ttk.StringVar(value=SV.Add_stuffAdjective_and_mark_it_text)
            mark_entry = ttk.Entry(f23, textvariable=Add_stuffAdjective_and_mark_it_text_var, width=32)
            mark_entry.pack(anchor=tk.W, pady=(10, 10), padx=10)
            ToolTip(mark_entry, text=_(
                    "'~LABEL~' will be replaced with the original word. \n If you just want to add such words for translation, but do not want to mark them separately, then you can only write '~LABEL~'"))

            def Add_stuffAdjective_and_mark_it_text_var_callback(*_):
                SV.Add_stuffAdjective_and_mark_it_text = Add_stuffAdjective_and_mark_it_text_var.get()
                if '~LABEL~' not in SV.Add_stuffAdjective_and_mark_it_text:
                    Add_stuffAdjective_and_mark_it_text_var.set(
                        SV.Add_stuffAdjective_and_mark_it_text + "~LABEL~")
                    SV.Add_stuffAdjective_and_mark_it_text = Add_stuffAdjective_and_mark_it_text_var.get()
                SV.set('Add_stuffAdjective_and_mark_it_text', SV.Add_stuffAdjective_and_mark_it_text)

            Add_stuffAdjective_and_mark_it_text_var.trace_add('write', Add_stuffAdjective_and_mark_it_text_var_callback)

        def F3():




            self.F3 = ttk.LabelFrame(self, text='Spacing')
            self.F3.pack(fill='both', padx=50, pady=(10,0))

            f31 = ttk.Labelframe(self.F3, text=_("Grabbed lines left spacing"), padding=10)
            f31.pack(anchor=tk.W, pady=(5, 0), side='left', padx=10)



            tags_left_spacing_var = tk.StringVar(value=SV.tags_left_spacing)

            f31.one_tab = ttk.Radiobutton(f31,
                                          text=_("One tab"),
                                          value='tab',
                                          variable=tags_left_spacing_var
                                          )
            f31.one_tab.pack(anchor=tk.W, padx=(2, 0), pady=(1, 0))
            f31.one_tab.ToolTip_image = PhotoImage(
                file='Images/Grabbing/One_tab.png')
            f31.one_tab.ToolTip = ToolTipImage(f31.one_tab,
                image=f31.one_tab.ToolTip_image)

            f31.two_spaces = ttk.Radiobutton(
                f31, text=_("Two spaces"), value='space2',
                variable=tags_left_spacing_var
                )
            f31.two_spaces.pack(anchor=tk.W, padx=(2, 0), pady=(0, 0))
            f31.two_spaces.ToolTip_image = PhotoImage(
                file='Images/Grabbing/Two_spaces.png')
            f31.two_spaces.ToolTip = ToolTipImage(f31.two_spaces,
                image=f31.two_spaces.ToolTip_image)


            f31.fore_spaces = ttk.Radiobutton(
                f31, text=_("Fore spaces"), value='space4',
                variable=tags_left_spacing_var
                )
            f31.fore_spaces.pack(anchor=tk.W, padx=(2, 0), pady=(0, 0))
            f31.fore_spaces.ToolTip_image = PhotoImage(
                file='Images/Grabbing/Fore_spaces.png')
            f31.fore_spaces.ToolTip = ToolTipImage(f31.fore_spaces,
                image=f31.fore_spaces.ToolTip_image)

            f31.no_spaces = ttk.Radiobutton(
                f31, text=_("No spaces"), value='space0',
                variable=tags_left_spacing_var
                )
            f31.no_spaces.pack(anchor=tk.W, padx=(2, 0), pady=(0, 2))
            f31.no_spaces.ToolTip_image = PhotoImage(
                file='Images/Grabbing/No_spaces.png')
            f31.no_spaces.ToolTip = ToolTipImage(f31.no_spaces,
                image=f31.no_spaces.ToolTip_image)


            def set_tags_left_spacing_var(*kwargs):
                SV.set('tags_left_spacing', tags_left_spacing_var.get())

            tags_left_spacing_var.trace("w", set_tags_left_spacing_var)



            f32 = ttk.Labelframe(self.F3, text=_("Separating empty lines"), padding=10)
            f32.pack(anchor=tk.W, pady=(5, 0), side='left', fill='y')

            Add_new_line_next_defname_ToolTip_image = PhotoImage(file='Images/Grabbing/Add_new_line_next_defname.png')

            def callback_Add_new_line_next_defname():
                Add_new_line_next_defname_treshhold.configure(state='normal' if Add_new_line_next_defname.get() else 'disabled')

            Add_new_line_next_defname = NewCheckButton(f32,
                                            text=_("Divide the text into blocks by Defname"),
                                            sv_key=SV.Add_new_line_next_defname,
                                            sv_key_text='Add_new_line_next_defname',
                                            tooltip_text=_("Add empty line before each new grabbed defname"),
                                            tooltip_image=Add_new_line_next_defname_ToolTip_image,
                                            command_add=callback_Add_new_line_next_defname
                                            )

            Add_new_line_next_defname.pack(anchor=tk.W, pady=(5,0))

            Add_new_line_next_defname_treshhold = NewCheckButton(f32,
                                            text=_("Threshold for adding an empty line"),
                                            sv_key=SV.Add_new_line_next_defname_treshhold,
                                            sv_key_text='Add_new_line_next_defname_treshhold',
                                            tooltip_text=_("Empty lines will be added if there are many lines with the same defname in the file. (If the number of different defnames is less than half of all strings.)"
                                                           ),
                                            state='normal' if Add_new_line_next_defname.get() else 'disabled'
                                            )

            Add_new_line_next_defname_treshhold.pack(anchor=tk.W, pady=(5,0))


        def Other():
            other_frame = Labelframe(self, text=_('Other'), padding=10)
            other_frame.pack(anchor='se', side=tk.BOTTOM)

            Tkey_system_on = NewCheckButton(other_frame,
                                            _("QuestScriptDef Tkey system"),
                                            SV.Tkey_system_on,
                                            'Tkey_system_on',
                                            tooltip_text=_("At 1.4 patch TKey system was broken. If the developers fix it, then enable this feature.\n The Tkey system is specifically designed to simplify long tag paths."
                                                           )
                                            )

            Tkey_system_on.pack(anchor=tk.W, pady=(5, 0))

        F1()
        F2()
        F3()
        Other()

class AboutFrame(Frame):
    def __init__(self, app, main_frame, master_frame,):
        super().__init__(master=master_frame)
        self.app = app
        self.main_frame = main_frame
        self.Note_book: ttk.Notebook = master_frame
        self.Note_book.add(self, text=_('About'))


        def about_example_update():
            self.about_example.configure(state='normal')

            text = f'''<ModMetaData>
            <name>{SV.New_Name.replace("~MOD_NAME~", "Example mod")}</name>
            <author>{SV.Author}</author>
            <packageId>{SV.Author.replace(' ', "")}.example1</packageId>
            <supportedVersions>
                <li>1.3</li>
                <li>1.4</li>
            </supportedVersions>
            <modDependencies>{"""
                <li>
                    <packageId>example1.example2</packageId>
                    <displayName>Example mod</displayName>
                    <steamWorkshopUrl>https://steamcommunity.com/sharedfiles/filedetails/?id=0000000000</steamWorkshopUrl>
                </li>""" if SV.Add_mod_Dependence == True else ""}
            </modDependencies>
            <loadAfter>example1.example2</loadAfter>
            <description>{SV.Description.replace("~MOD_NAME~", "Example mod").replace("~MOD_DESCRIPTION~", "ORIGINAL MOD DESCRIPTION...").replace("~MOD_URL~", "https://steamcommunity.com/sharedfiles/filedetails/?id=0000000000")}</description>
        </ModMetaData>'''
            self.about_example.delete(1.0, ttk.END)
            self.about_example.insert(1.0, text)
            self.about_example.configure(state='disabled')

        def F1():


            F1 = Frame(self)
            F1.pack(expand=0, fill='x', padx=(20,10), pady=(10, 0))

            fl = ttk.Frame(F1)
            fl.pack(anchor='nw', side='left', expand=0)
            fl_top = ttk.Frame(fl)
            fl_top.pack(side='top', fill='x')

            fl1 = ttk.LabelFrame(fl_top, text=_('Author'), padding=10)
            fl1.pack(anchor='nw', side='left', fill='x')

            self.Author_Entry_stringVar = ttk.StringVar(value=SV.Author)

            Author_Entry_entry = ttk.Entry(fl1, textvariable=self.Author_Entry_stringVar, width=32)
            Author_Entry_entry.pack(anchor='nw', padx=5, pady=5)

            def Author_Entry_callback(*_):
                SV.set('Author', self.Author_Entry_stringVar.get())

                about_example_update()

            self.Author_Entry_stringVar.trace_add('write', Author_Entry_callback)



            fl2 = ttk.Labelframe(fl_top, text=_("New Name"), padding=10)
            fl2.pack(anchor='nw', side='left', padx=5, fill='x')

            self.New_NameStringVar = ttk.StringVar(value=SV.New_Name)

            New_name_Entry = ttk.Entry(fl2,
                       textvariable=self.New_NameStringVar, width=32)
            New_name_Entry.pack(anchor='nw', padx=5, pady=5)
            New_name_Entry.ToolTip = ToolTip(New_name_Entry, text=_(
                '~MOD_NAME~ will be replaced with the name of the original mod.'))

            def New_Name_Entry_callback(*_):
                SV.set('New_Name', self.New_NameStringVar.get())

                if '~MOD_NAME~' not in SV.New_Name:
                    self.New_NameStringVar.set("~MOD_NAME~")
                    New_name_Entry.icursor(10)
                    SV.set('New_Name', self.New_NameStringVar.get())

                about_example_update()

            self.New_NameStringVar.trace_add('write', New_Name_Entry_callback)

            fl_bottom = ttk.Frame(fl)
            fl_bottom.pack(side='top', fill='both')

            fl3 = ttk.Frame(fl_bottom, padding=0)
            fl3.pack(anchor='nw', padx=(0, 0), pady=(5, 0), )


            Add_mod_Dependence = NewCheckButton(fl3,
                                                _("Add modDependencies"),
                                                SV.Add_mod_Dependence,
                                                'Add_mod_Dependence',
                                                command_add=about_example_update
                                                )
            Add_mod_Dependence.pack(anchor=tk.W, pady=(5,0))


            fr = ttk.Frame(F1,)
            fr.pack(anchor='nw', side='right', fill='both', expand=True)

            fr1 = ttk.Labelframe(fr, text=_('Description'))
            fr1.pack(padx=(5, 0), pady=(0, 0), expand=True, fill='x')

            fr1.Description = ttk.Text(fr1, height=10)
            fr1.Description.pack(padx=(5, 5), pady=(0, 5), expand=True, fill='x')
            fr1.Description.ToolTip = ToolTip(fr1.Description, text=_(
                '~MOD_NAME~ will be replaced with the name of the original mod\n'
                '~MOD_DESCRIPTION~ will be replaced with the original mod description\n'
                '~MOD_URL~ will be replaced with the original mod URL'), wraplength=500)

            def Description_callback(*_):
                SV.Description = fr1.Description.get(1.0, ttk.END)
                with open(SV.SettingsPath.SettingsPath_AppData / SV.SettingsPath.Description, 'w', encoding='utf8') as desc_file:
                    desc_file.write(SV.Description)
                about_example_update()

            fr1.Description.insert(0.0, SV.Description)
            fr1.Description.bind('<KeyRelease>', lambda e: Description_callback())

        F1()


        F2 = ttk.Labelframe(self, padding=5, text=_("Example About.xml"))
        F2.pack(anchor='nw', expand=True, fill=tk.BOTH, padx=10, pady=(10, 0))
        self.about_example = ttk.Text(F2, state='disabled')
        self.about_example.pack(expand=True, fill=tk.BOTH)

        about_example_update()

class PreviewFrame(Frame):
    def __init__(self, app, main_frame, master_frame,):
        super().__init__(master=master_frame)
        self.app = app
        self.main_frame = main_frame
        self.Note_book: ttk.Notebook = master_frame
        self.Note_book.add(self, text=_('Preview'))


        self.F = ttk.Frame(self, padding=(10, 10, 10, 10), width=20)
        self.F.pack(fill=ttk.X, anchor='nw')

        self.F_left = ttk.Frame(self.F, )  # text = "FLeft")
        self.F_left.pack(expand=False, anchor='nw', side='left')

        self.F_right = ttk.LabelFrame(self.F, text=_("Image position"))
        self.F_right.pack(expand=True, fill=ttk.BOTH, anchor='nw', side='right', padx=(100, 250))

        self.F_right.a1 = ttk.Frame(self.F_right, width=20, )
        self.F_right.a1.pack(side='left', fill=ttk.Y)

        self.F_right.a2 = ttk.Frame(self.F_right, )
        self.F_right.a2.pack(expand=True, side='left', fill=ttk.BOTH)

        self.Position = ttk.StringVar(value=SV.Preview_Position)

        self.R_top = ttk.Frame(self.F_right.a2, padding=(10, 10, 0, 10))
        self.R_top.pack(expand=True, fill=ttk.BOTH)

        self.R_top_1 = ttk.Frame(self.R_top, )
        self.R_top_1.pack(side='left', fill=ttk.BOTH, expand=True)
        self.R_top_2 = ttk.Frame(self.R_top, )
        self.R_top_2.pack(side='right', fill=ttk.BOTH, expand=True)

        self.R_top.TL = ttk.Radiobutton(self.R_top_1, text=_("Top left"), variable=self.Position,
         value='Top left')
        self.R_top.TL.pack(side="left")
        self.R_top.TR = ttk.Radiobutton(self.R_top_2, text=_("Top right"), variable=self.Position,
         value='Top right')
        self.R_top.TR.pack(side="left")

        self.R_mid = ttk.Frame(self.F_right.a2, padding=(10, 10, 0, 10))
        self.R_mid.pack(expand=True, fill=ttk.BOTH, padx=(0, 50), pady=20)
        self.R_mid.Center = ttk.Radiobutton(self.R_mid, text=_("Center"), variable=self.Position,
             value='Center')
        self.R_mid.Center.pack(anchor='center')

        self.R_bot = ttk.Frame(self.F_right.a2, padding=(10, 10, 0, 10))
        self.R_bot.pack(expand=True, fill=ttk.BOTH)

        self.R_bot_1 = ttk.Frame(self.R_bot, )
        self.R_bot_1.pack(side='left', fill=ttk.BOTH, expand=True)
        self.R_bot_2 = ttk.Frame(self.R_bot, )
        self.R_bot_2.pack(side='right', fill=ttk.BOTH, expand=True)

        self.R_bot.BL = ttk.Radiobutton(self.R_bot_1, text=_("Bottom left"), variable=self.Position,
         value='Bottom left')
        self.R_bot.BL.pack(side='left', fill=ttk.BOTH, expand=True)
        self.R_bot.BR = ttk.Radiobutton(self.R_bot_2, text=_("Bottom right"), variable=self.Position,
         value='Bottom right')
        self.R_bot.BR.pack(side='right', fill=ttk.BOTH, expand=True)

        def Position_callback(*_):
            SV.set('Preview_Position', self.Position.get())
            Preview_image_chage()

        self.Position.trace_add('write', Position_callback)

        def callback_Image_on_Preview():
            SV.Image_on_Preview = bool(self.Image_on_Preview.get())
            SV.set('Image_on_Preview', SV.Image_on_Preview)

            self.F_left.F1.Select_img_btn.configure(
                state=('normal' if self.Image_on_Preview.get() else 'disabled'))
            self.F_left.F2_Offset_x.Entry.configure(
                state=('normal' if self.Image_on_Preview.get() else 'disabled'))
            self.F_left.F2_Offset_y.Entry.configure(
                state=('normal' if self.Image_on_Preview.get() else 'disabled'))

            self.R_bot.BL.configure(state=('normal' if self.Image_on_Preview.get() else 'disabled'))
            self.R_bot.BR.configure(state=('normal' if self.Image_on_Preview.get() else 'disabled'))
            self.R_mid.Center.configure(state=('normal' if self.Image_on_Preview.get() else 'disabled'))
            self.R_top.TL.configure(state=('normal' if self.Image_on_Preview.get() else 'disabled'))
            self.R_top.TR.configure(state=('normal' if self.Image_on_Preview.get() else 'disabled'))
            Preview_image_chage()

        self.F_left.F1 = ttk.Frame(self.F_left, padding=(10, 10, 0, 0))
        self.F_left.F1.pack(expand=False, anchor='nw')

        self.Image_on_Preview = ttk.BooleanVar(value=SV.Image_on_Preview)
        self.F_left.F1.Image_on_Preview_checkbox = ttk.Checkbutton(self.F_left.F1,       variable=self.Image_on_Preview,       text=_("Add an image to the preview"),       command=callback_Image_on_Preview,       padding=10)
        self.F_left.F1.Image_on_Preview_checkbox.pack(side='left')
        self.F_left.F1.Image_on_Preview_checkbox.ToolTip = ToolTip(
            self.F_left.F1.Image_on_Preview_checkbox, text=_("Add YOUR image to the original mod preview."))

        def callback_Select_img_btn():
            file = filedialog.askopenfile(filetypes=[('Png Images', '*.png')])
            if file is not None:
                file = file.name.replace('\\', '/')
                if file != r"Images\\Preview\\New_Image.png":
                    shutil.copy(file, r"Images\\Preview\\New_Image.png")

            Preview_image_chage()

        self.F_left.F1.Select_img_btn = ttk.Button(self.F_left.F1, text=_("Select Your image"),command=lambda: callback_Select_img_btn(), state='disabled')
        self.F_left.F1.Select_img_btn.pack(padx=10, pady=10, side='left')
        self.F_left.F1.Select_img_btn.configure(state=('normal' if self.Image_on_Preview.get() else 'disabled'))

        self.F_left.F2 = ttk.Frame(self.F_left, padding=(20, 5, 0, 0))
        self.F_left.F2.pack(expand=False, anchor='nw')

        self.F_left.F2_Offset_x = ttk.Frame(self.F_left.F2, padding=(0, 0, 0, 0))
        self.F_left.F2_Offset_x.pack(expand=False, anchor='nw', side='left')

        self.F_left.F2_Offset_x.Label = ttk.Label(self.F_left.F2_Offset_x, text=_("x Offset"))
        self.F_left.F2_Offset_x.Label.pack(side='top')

        def Numeric_str(new_text: str, widget_name: str):
            def is_number(ss):
                try:
                    int(ss)
                    return True
                except ValueError:
                    return False

            if widget_name.endswith('offset_x_Entry'):
                x_entry = True
            else:
                x_entry = False


            Zero = False
            match new_text:
                case '' | '-':
                    True_path = True
                    Zero = True
                case str(s) if s.endswith(' '):
                    True_path = False
                case str(s) if is_number(s):
                    True_path = True
                    Zero = False
                case _:
                    True_path = False

            if True_path:
                if Zero:
                    if x_entry:
                        SV.set('Preview_Offset_x', 0)
                    else:
                        SV.set('Preview_Offset_y', 0)
                else:
                    if x_entry:
                        SV.set('Preview_Offset_x', int(new_text))
                    else:
                        SV.set('Preview_Offset_y', int(new_text))
                Preview_image_chage()
                return True
            else:
                return False




        numeric_validate = self.register(Numeric_str)

        self.Offset_x = ttk.StringVar(value=str(SV.Preview_Offset_x))

        self.F_left.F2_Offset_x.Entry = ttk.Entry(self.F_left.F2_Offset_x, textvariable=self.Offset_x,
                                                  validate='key',
                                                  validatecommand=(numeric_validate, '%P', '%W'), name='offset_x_Entry')
        self.F_left.F2_Offset_x.Entry.pack(side='bottom')

        self.F_left.F2_Offset_y = ttk.Frame(self.F_left.F2, padding=(10, 0, 0, 0))
        self.F_left.F2_Offset_y.pack(expand=False, anchor='nw', side='left')

        self.F_left.F2_Offset_y.Label = ttk.Label(self.F_left.F2_Offset_y, text=_("y Offset"))
        self.F_left.F2_Offset_y.Label.pack(side='top')

        self.Offset_y = ttk.StringVar(value=str(SV.Preview_Offset_y))

        self.F_left.F2_Offset_y.Entry = ttk.Entry(self.F_left.F2_Offset_y, textvariable=self.Offset_y,
                                                  validate='key',
                                                  validatecommand=(numeric_validate, '%P', '%W'), name='offset_y_Entry')
        self.F_left.F2_Offset_y.Entry.pack(side='bottom')

        self.F_left.F2_Offset_x.Entry.configure(state=('normal' if self.Image_on_Preview.get() else 'disabled'))
        self.F_left.F2_Offset_y.Entry.configure(state=('normal' if self.Image_on_Preview.get() else 'disabled'))

        self.F_last = ttk.Frame(self, padding=(10, 10, 0, 0))
        self.F_last.pack(expand=True, fill=tk.BOTH, side='bottom')

        self.F_last.image = PhotoImage(file='Images/Preview/Preview_origianl.png')
        self.F_last.Label_image = ttk.Label(self, image=self.F_last.image)
        self.F_last.Label_image.pack()

        def Preview_image_chage():

            if self.Image_on_Preview.get():
                image_edit.add_custom_labe_on_preview(r"Images\\Preview\\Preview_origianl.png",
                                                      r"Images\\Preview\\New_Image.png",
                                                      self.Position.get(), SV.Preview_Offset_x, SV.Preview_Offset_y).save(r'Images\\Preview\\Preview_updated.png')

                self.self_image_updated = PhotoImage(file=r'Images\\Preview\\Preview_updated.png')

                self.F_last.Label_image.config(image=self.self_image_updated)
            else:
                self.F_last.Label_image.config(image=self.F_last.image)

        Preview_image_chage()

class AdvancedFrame(Frame):
    def __init__(self, app, main_frame, master_frame,):
        super().__init__(master=master_frame)
        self.app = app
        self.main_frame = main_frame
        self.Note_book: ttk.Notebook = master_frame
        self.Note_book.add(self, text=_('Advanced'))

        self.af = ttk.Frame(self, padding=(10, 10, 10, 10))
        self.af.pack(expand=True, fill=ttk.BOTH)

        self.af.top = ttk.Frame(self.af)
        self.af.top.pack(fill=ttk.X)

        self.af.top.left = ttk.LabelFrame(self.af.top, text=_("Tags for extraction"))
        self.af.top.left.pack(expand=True, fill=ttk.BOTH, side='left', padx=(0, 5))

        self.af.top.left.btn1 = ttk.Button(self.af.top.left, text=_("Tags to extraction"),
    command=lambda: os.startfile(SV.SettingsPath.SettingsPath_AppData / SV.SettingsPath.Tags_to_extraction))
        self.af.top.left.btn1.pack(padx=10, pady=10)
        self.af.top.left.btn1.tooltip = ToolTip(self.af.top.left.btn1, wraplength=1000, text=_(
            '<Tags> to be extracted for translation, for example, if you want to extract "anima heart" from \n'
            '<label>anima heart</label>,\n'
            'then the list of tags to extract should be "label"'))

        self.af.top.left.btn2 = ttk.Button(self.af.top.left, text=_("Part of tag to extraction"),
    command=lambda: os.startfile(SV.SettingsPath.SettingsPath_AppData / SV.SettingsPath.Part_of_tag_to_extraction))
        self.af.top.left.btn2.pack(padx=10, pady=10)
        self.af.top.left.btn2.tooltip = ToolTip(self.af.top.left.btn2, wraplength=1000, text=_(
            'If you need to extract all <tags> that have a common part, for example, all <tags> with "Message". Such as:\n'
            '<NewMessage>Hello</NewMessage>\n'
            '<OldMessage>Hello</OldMessage>\n'
            '<Message1>Hello</Message1>\n'
            'Case-sensitive'))

        self.af.top.left.btn3 = ttk.Button(self.af.top.left, text=_("Tags before <li>"),
    command=lambda: os.startfile(SV.SettingsPath.SettingsPath_AppData / SV.SettingsPath.Tags_before_li))
        self.af.top.left.btn3.pack(padx=10, pady=10)
        self.af.top.left.btn3.tooltip = ToolTip(self.af.top.left.btn3, wraplength=1000, text=_(
            'A list of <tags> that are in front of a set of consecutive <li> that need to be output\nlike:'
            '<rulePack>\n'
            '    <rulesStrings>\n'
            '        <li>RBTStownend->Fieldarmy Base</li>\n'
            '        <li>RBTStownend->Power Station</li>\n'
            '        <li>RBTStownend->Powerplant</li>\n'
            '    </rulesStrings>\n'
            '</rulePack>\n'
            '\n'
            'Add tags here only if you are completely sure that Rimworld supports these lists\n'
            'So, for example, in 1.3 "thoughtStageDescriptions" are not supported, and you have to write each line separately'))

        self.af.top.right = ttk.LabelFrame(self.af.top, text=_("Forbidden"))
        self.af.top.right.pack(expand=True, fill=ttk.BOTH, side='left', padx=(5, 0))

        self.af.top.right.btn1 = ttk.Button(self.af.top.right, text=_("Forbidden tags"),
     command=lambda: os.startfile(SV.SettingsPath.SettingsPath_AppData / SV.SettingsPath.Forbidden_tag))
        self.af.top.right.btn1.pack(padx=10, pady=10)
        self.af.top.right.btn1.tooltip = ToolTip(self.af.top.right.btn1, wraplength=1000, text=_(
            "<Tags> that will not be extracted. Usually you don't need to add much here, but if the program constantly extracts something superfluous, then it makes sense to prohibit the extraction of the tag in any way\n"
            "The first way is to prohibit the extraction of this particular <Tag>. "
            "In this case, those tags that completely match the list will not be extracted.\n"
            "For example <developmentalStageFilter>Baby, Child, Adult</developmentalStageFilter>\n"
            "Because this line is very similar to normal text, which it would be desirable to extract because there are spaces in it, <tag> should be banned."))

        self.af.top.right.btn2 = ttk.Button(self.af.top.right, text=_("Forbidden part of tag"),
     command=lambda: os.startfile(SV.SettingsPath.SettingsPath_AppData / SV.SettingsPath.Forbidden_part_of_tag))
        self.af.top.right.btn2.pack(padx=10, pady=10)
        self.af.top.right.btn2.tooltip = ToolTip(self.af.top.right.btn2, wraplength=1000, text=_(
            'If you need to prohibit extraction of all <tags> that have a common part,'
            ' for example, all <tags> with "Texture". Such as:\n'
            '<Texture>Texture1.png</Texture>\n'
            '<Old_Texture>Texture2.png</Old_Texture>\n'
            '<MetalTexture>Texture3.png</MetalTexture>\n'
            'Case-sensitive'))

        self.af.top.right.btn3 = ttk.Button(self.af.top.right, text=_("Forbidden part of path"),
     command=lambda: os.startfile(SV.SettingsPath.SettingsPath_AppData / SV.SettingsPath.Forbidden_part_of_path))
        self.af.top.right.btn3.pack(padx=10, pady=10)
        self.af.top.right.btn3.tooltip = ToolTip(self.af.top.right.btn3, wraplength=1000, text=_(
            'If you need to prohibit all tags that have a common part of the path: So for\n'
            '<TraitDef>\n'
            '   <defName>ReunionCharacter</defName>\n'
            '   <degreeDatas>\n'
            '       <li>\n'
            '           <label>Ally</label>\n'
            '       </li>\n'
            '   </degreeDatas>\n'
            '</TraitDef>\n'
            'The path to the text "Ally" will be"/TraitDef/ReunionCharacter/degreeDatas/li/label"\n'
            'And you can prohibit, for example, /degreeDatas/li/'))

        self.af.top.right.btn4 = ttk.Button(self.af.top.right, text=_("Forbidden text"),
     command=lambda: os.startfile(SV.SettingsPath.SettingsPath_AppData / SV.SettingsPath.Forbidden_text))
        self.af.top.right.btn4.pack(padx=10, pady=10)
        self.af.top.right.btn4.tooltip = ToolTip(self.af.top.right.btn4, wraplength=800, text=_(
            "Sometimes it is necessary to prohibit not the <Tag> but the text. For example, all sorts of true false can sometimes be extracted by the program\n"
            "<ThingDef>\n"
            "   <defName>AnimaHeart</defName>\n"
            "   <useHitPoints_label>true</useHitPoints_label>\n"
            "</ThingDef>\n"
            "Since there is a label in the <useHitPoints_label> tag, such a tag may be mistakenly extracted. Therefore, you can either prohibit such a tag, or prohibit the text 'true'. "
            "If the text in the Tag completely matches the text added to the prohibited list, it will not be extracted"))

        self.af.top2 = ttk.Frame(self.af)
        self.af.top2.pack(fill=ttk.X)

        self.af.top2.left = ttk.LabelFrame(self.af.top2, text=_("Other"))
        self.af.top2.left.pack(side='left')

        self.af.top2.left.btn1 = ttk.Button(self.af.top2.left, text=_("<li> class replace"),
     command=lambda: os.startfile(SV.SettingsPath.SettingsPath_AppData / SV.SettingsPath.Li_Class_Replace))
        self.af.top2.left.btn1.pack(padx=10, pady=10)
        self.af.top2.left.btn1.tooltip = ToolTip(self.af.top2.left.btn1, wraplength=800, text=_(
            'Sometimes TranslationReport wants some <li> to be replaced not with numbers, but with text, depending on "li Class=" for example:\n'
            '<QuestScriptDef>\n'
            '  <li Class="QuestNode_Letter">\n'
            '      <label>Quest expired</label>\n'
            '  </li>\n'
            '<QuestScriptDef>\n'
            '\n'
            'Normally the extracted text would be like this: \n'
            '<0.label>Quest expired<0.label> '
            'But the game wants him to be like this:\n'
            '<Letter.label>Quest expired<Letter.label>\n'
            'And the game takes the "Letter" from the <li> class, so I added the replacement of QuestNode_ with an empty string'))








class TestApp(ttk.Toplevel):

    LANG_MAP = {'English': 'en', 'Русский': 'ru'}



    def rebuild_ui(self):
        TestApp(master=self.master)
        self.destroy()

    def exit_app(self):
        self.master.deiconify()

        # self.master.destroy()

        self.destroy()


    def _create_main_frame(self):
        """Создаёт/пересоздаёт интерфейс"""

        if SV.Settings_language == 'ru':
            ru_translation.install()
        else:
            en_translation.install()

        if hasattr(self, 'main_frame'):
            self.main_frame.destroy()  # Уничтожаем главный фрейм

        self.main_frame = Frame(self)
        self.main_frame.pack(fill=tk.X)

    def _create_Header_Frame(self):
        self.Header = HeaderFrame(self, self.main_frame)

    def _create_Content_frame(self):
        # noinspection PyArgumentList
        Content_frame = ttk.Frame(self, padding=2, bootstyle='light')
        Content_frame.pack(expand=True, fill='both', side=tk.BOTTOM)
        self.Top_Notebook = ttk.Notebook(Content_frame)
        self.Top_Notebook.pack(expand=True, fill=tk.BOTH)

    def _create_GeneralFrame(self):
        self.Genearal_ = GeneralFrame(self, self.main_frame, master_frame=self.Top_Notebook)

    def _create_CommentFrame(self):
        self.Comment_ = CommentFrame(self, self.main_frame, master_frame=self.Top_Notebook)

    def _create_GrabFrame(self):
        self.Grab_ = GrabFrame(self, self.main_frame, master_frame=self.Top_Notebook)

    def _create_AboutFrame(self):
        self.About_ = AboutFrame(self, self.main_frame, master_frame=self.Top_Notebook)

    def _create_PreviewFrame(self):
        self.Preview_ = PreviewFrame(self, self.main_frame, master_frame=self.Top_Notebook)

    def _create_AdvancedFrame(self):
        self.Advanced_ = AdvancedFrame(self, self.main_frame, master_frame=self.Top_Notebook)

    def __init__(self, master: ttk.Window):
        self.master: ttk.Window = master
        super().__init__(master=master, title='Settings')

        self.overrideredirect(True)
        # self.attributes('-topmost', True)

        self.style.theme_use('darkly')
        self.protocol("WM_DELETE_WINDOW", self.exit_app)
        self.geometry("1000x800+200+200")
        self._create_main_frame()
        self._create_Header_Frame()
        self._create_Content_frame()
        self._create_GeneralFrame()
        self._create_CommentFrame()
        self._create_GrabFrame()
        self._create_AboutFrame()
        self._create_PreviewFrame()
        self._create_AdvancedFrame()





        self.bind_all("<Key>", self._onKeyRelease, "+")
        self.after(1, lambda: self.Top_Notebook.focus_set())
        self.raise_tab(0)
        self.geometry("1000x800+200+200")

    def raise_tab(self, idx):
        self.Top_Notebook.select(idx)



    def size_change(self, event):
        """ function to change window size """
        self.wm_state('normal')
        x1 = self.winfo_pointerx()
        y1 = self.winfo_pointery()
        x0 = self.winfo_rootx()
        y0 = self.winfo_rooty()
        if (x1 - x0) < 0:
            x0 = 0
        if (y1 - y0) < 0:
            y0 = 0
        self.geometry(f"{x1 - x0}x{y1 - y0}")
        return

    def on_deiconify(self, event):
        """ function to deiconify or window """
        self.overrideredirect(True)

    # def exit_app(self):
    #     Window_Hidden.destroy()
    #
    #     if language_changed:
    #         Window_Text_grabber.destroy()
    #     else:
    #         Window_Text_grabber.deiconify()

    def _onKeyRelease(self, event):
        self.ctrl = (event.state & 0x4) != 0
        if event.keycode == 88 and self.ctrl and event.keysym.lower() != "x":
            event.widget.event_generate("<<Cut>>")

        if event.keycode == 86 and self.ctrl and event.keysym.lower() != "v":
            event.widget.event_generate("<<Paste>>")

        if event.keycode == 67 and self.ctrl and event.keysym.lower() != "c":
            event.widget.event_generate("<<Copy>>")








def run_from_main_prog(master: ttk.Window):

    master.withdraw()
    a = TestApp(master=master,)

    def set_appwindow(root):

        hwnd = windll.user32.GetParent(root.winfo_id())
        hicon = win32gui.LoadImage(None, 'Images\\icons8-text-67.ico', win32con.IMAGE_ICON, 0, 0,
                                   win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE)
        win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, hicon)
        win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_SMALL, hicon)
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                               win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_APPWINDOW)

        root.wm_withdraw()
        root.after(10, lambda: root.wm_deiconify())
        windll.user32.SetForegroundWindow(hwnd)
    a.after(10, lambda: set_appwindow(root=a))

    master.mainloop()



if __name__ == '__main__':
    Window_Text_grabber = ttk.Window(title="Text grabber dummy window")

    Window_Text_grabber.withdraw()

    TestApp(master=Window_Text_grabber)
    Window_Text_grabber.mainloop()


r'''
Не это!
pybabel init -D T_test -i locale/T_test.pot -d locale -l ru --no-wrap
pybabel init -D T_test -i locale/T_test.pot -d locale -l en --no-wrap


Вот это!
pybabel extract -o locale/T_test.pot --no-wrap Text_grabber_settings.py 
pybabel update -D T_test -i locale/T_test.pot -d locale -l ru --no-wrap
pybabel compile -D T_test -i locale\ru\LC_MESSAGES\T_test.po -o locale\ru\LC_MESSAGES\T_test.mo
'''

