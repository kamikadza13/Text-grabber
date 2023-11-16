import configparser
import gettext
import os
import shutil
import sys
import tkinter as tk
from ctypes import windll
from tkinter import PhotoImage
from tkinter import filedialog

import ttkbootstrap as ttk
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.tooltip import ToolTip

import locale
import image_edit


current_locale, encoding = locale.getdefaultlocale()

class SettingsPath:
    Tags_to_extraction = r"Settings\\Tags_to_extraction.txt"
    Part_of_tag_to_extraction = r"Settings\\Part_of_tag_to_extraction.txt"
    Tags_before_li = r"Settings\\Tag_before_li.txt"

    Forbidden_tag = r"Settings\\Forbidden_tags.txt"
    Forbidden_part_of_tag = r"Settings\\Forbidden_part_of_tag.txt"
    Forbidden_part_of_path = r"Settings\\Forbidden_part_of_path.txt"

    Forbidden_text = r"Settings\\Forbidden_tags.txt"
    Li_Class_Replace = r"Settings\\Li_Class_Replace.txt"
    Folders_to_search = r"Settings\\Folders_to_search_Defs.txt"


class WindowSettings:
    color2_Dark_grey = "#313131"  # Dark grey
    color3_Grey = "#595959"  # Grey
    color_grey_blue = '#505E8C'
    color_yellow_meadow = '#ECDB54'

    font1 = 'Consolas 11'
    Title_font_color = color_yellow_meadow

    Title_bg = '#313131'
    geometry = '+300+400'
    minsizeX, minsizeY = (200, 50)


datapath = os.path.dirname(sys.argv[0]) + "/locale/"


locale_path = 'locale/'
gettext.install('T_test', locale_path)

# gettext.install('GUI_config', datapath, names=("ngettext",))
ru_i18n = gettext.translation('T_test', locale_path, fallback=False, languages=['ru'])
en_i18n = gettext.translation('T_test', locale_path, fallback=False, languages=['en'])


language_changed = False




# ttk.themes.standard['darkly']['colors']['primary'] =  "#375a7f"
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
        if self.text:
            lbl_label = ttk.Label(
                master=self.toplevel,
                text="\t" + self.text,
                justify=ttk.LEFT,
                wraplength=self.wraplength,

            )
            lbl_label.pack(fill=ttk.BOTH, expand=ttk.YES, )
        if self.bootstyle:
            lbl.configure(bootstyle=self.bootstyle)
            if self.text:
                lbl_label.configure(bootstyle=self.bootstyle)
        else:
            lbl.configure(style="tooltip.TLabel")
            if self.text:
                lbl_label.configure(style="tooltip.TLabel")


General_settings_path = 'Settings\\Settings.ini'
config = configparser.RawConfigParser(allow_no_value=True)
config.optionxform = str


class SettingsValues:
    #   [General]
    Settings_language = _('En')
    Game_language = 'Russian'

    Path_to_Data = _('None')
    Path_to_Mod_folder = _('None')
    Path_to_Another_folder = _('None')

    Delete_old_versions_translation = True
    Merge_folders = True
    Not_rename_files = False

    #   [Comments]
    Add_filename_comment = True
    Add_comment = True
    Comment_add_EN = True
    Comment_starting_similar_as_ogiganal_text = True
    Comment_spacing_before_tag = False
    Comment_replace_n_as_new_line = True

    #  [Grabbing]
    Add_stuffAdjective_and_mark_it = True
    Add_stuffAdjective_and_mark_it_text = 'Adjective ~LABEL~'

    Check_at_least_one_letter_in_text = False
    add_titleFemale = True
    add_titleShortFemale = True
    Tkey_system_on = True

    tags_left_spacing = "	"
    Add_new_line_next_defname = True

    labelPlural = True
    labelMale = False
    labelFemale = False
    labelMalePlural = False
    labelFemalePlural = False



    #  [About.xml]
    Author = 'Kamikadza13'
    New_Name = '~MOD_NAME~ rus'
    Add_mod_Dependence = True
    Description = ''

    #  [Preview]
    Image_on_Preview = True
    Position = 'UL'
    Offset_x = 0
    Offset_y = 0


def settings_config_update_write():
    with open(General_settings_path, 'w') as aaa:
        config.write(aaa)


def settings_config_read(parent1: ttk.Window | ttk.Toplevel | tk.Tk | tk.Toplevel):
    try:
        config.read(General_settings_path, "utf8")


    except Exception as ex:
        def settings_read_error():
            print('Settings read Error')
            Messagebox.show_error(parent=parent1, alert=True,
                                  message=_(f"Can't read settings! Restoring default settings..."))

        parent1.after(1000, settings_read_error)
        config.read(r'Settings_original\\Settings.ini', "utf8")
        shutil.copy(r'Settings_original\\Settings.ini', General_settings_path)
        config.read(General_settings_path, "utf8")

    SettingsValues.Settings_language = config.get('General', 'Settings_language')
    SettingsValues.Game_language = config.get('General', 'Game_language')
    SettingsValues.Path_to_Data = config.get('General', 'Path_to_Data')
    SettingsValues.Path_to_Mod_folder = config.get('General', 'Path_to_Mod_folder')
    SettingsValues.Path_to_Another_folder = config.get('General', 'Path_to_Another_folder')
    SettingsValues.Delete_old_versions_translation = config.getboolean('General', 'Delete_old_versions_translation')
    SettingsValues.Merge_folders = config.getboolean('General', 'Merge_folders')
    SettingsValues.Not_rename_files = config.getboolean('General', 'Not_rename_files')

    SettingsValues.Add_filename_comment = config.getboolean('Comment', 'Add_filename_comment')
    SettingsValues.Add_comment = config.getboolean('Comment', 'Add_comment')
    SettingsValues.Comment_add_EN = config.getboolean('Comment', 'Comment_add_EN')
    SettingsValues.Comment_starting_similar_as_ogiganal_text = config.getboolean('Comment',
                                                                                 'Comment_starting_similar_as_ogiganal_text')
    SettingsValues.Comment_spacing_before_tag = config.getboolean('Comment', 'Comment_spacing_before_tag')
    SettingsValues.Comment_replace_n_as_new_line = config.getboolean('Comment', 'Comment_replace_n_as_new_line')

    SettingsValues.Check_at_least_one_letter_in_text = config.getboolean('Grabbing',
                                                                         'Check_at_least_one_letter_in_text')
    SettingsValues.add_titleFemale = config.getboolean('Grabbing', 'add_titleFemale')
    SettingsValues.add_titleShortFemale = config.getboolean('Grabbing', 'add_titleShortFemale')
    SettingsValues.Add_stuffAdjective_and_mark_it = config.getboolean('Grabbing', 'Add_stuffAdjective_and_mark_it')
    SettingsValues.Add_stuffAdjective_and_mark_it_text = config.get('Grabbing',
                                                                    'Add_stuffAdjective_and_mark_it_text')
    SettingsValues.labelPlural = config.getboolean('Grabbing', 'labelPlural')
    SettingsValues.labelMale = config.getboolean('Grabbing', 'labelMale')
    SettingsValues.labelFemale = config.getboolean('Grabbing', 'labelFemale')
    SettingsValues.labelMalePlural = config.getboolean('Grabbing', 'labelMalePlural')
    SettingsValues.labelFemalePlural = config.getboolean('Grabbing', 'labelFemalePlural')
    SettingsValues.tags_left_spacing = config.get('Grabbing', 'tags_left_spacing').strip('"')
    SettingsValues.Add_new_line_next_defname = config.getboolean('Grabbing', 'Add_new_line_next_defname')
    SettingsValues.Tkey_system_on = config.getboolean('Grabbing', 'Tkey_system_on')

    SettingsValues.Author = config.get('About.xml', 'Author')
    SettingsValues.New_Name = config.get('About.xml', 'New_Name')
    SettingsValues.Add_mod_Dependence = config.getboolean('About.xml', 'Add_mod_Dependence')

    with open(r'Settings\\Description.txt', encoding="utf8") as desc:
        SettingsValues.Description = desc.read().strip(" \n")

    SettingsValues.Image_on_Preview = config.getboolean('Preview', 'Image_on_Preview')
    SettingsValues.Position = config.get('Preview', 'Position')
    SettingsValues.Offset_x = config.getint('Preview', 'Offset_x')
    SettingsValues.Offset_y = config.getint('Preview', 'Offset_y')

    if SettingsValues.Settings_language == 'ru':
        ru_i18n.install()
    else:
        en_i18n.install()


class TestApp(ttk.Toplevel):

    def __init__(self, master_widget):

        ttk.Toplevel.__init__(self, master=master_widget)
        self.protocol("WM_DELETE_WINDOW", exit_app)
        settings_config_read(self)
        a = self.style
        a.theme_use('darkly')

        self.Title_frame = ttk.Frame(self)
        self.Title_frame.pack(side=tk.TOP, fill=tk.X)

        self.Title_label = ttk.Label(self.Title_frame, text=_('Text Grabber Settings'),
                                     foreground=WindowSettings.Title_font_color)
        self.Title_label.pack(side=tk.LEFT, fill=tk.X, anchor=tk.CENTER)
        # Pack the close button to the right-most side

        self.Title_close_btn = tk.Button(self.Title_frame, text='x', bd=0, width=2, font=WindowSettings.font1,
                                         command=exit_app, bg=WindowSettings.Title_bg, takefocus=0)

        self.Title_close_btn.pack(side=tk.RIGHT)
        self.languages = ['English', 'Русский']

        self.Title_language_selector = ttk.Combobox(self.Title_frame, values=self.languages, state='readonly',
                                                    width=10, bootstyle='light', )
        self.Title_language_selector.pack(side=tk.RIGHT, padx=(0, 10))

        self.Title_language_Label = ttk.Label(self.Title_frame, text="Language =", width=10, )
        self.Title_language_Label.pack(side=tk.RIGHT, padx=(0, 10))
        self.Title_language_Label.ToolTip = ToolTip(self.Title_language_Label,
                                                    text=_("Select Language of Settings Programm"), wraplength=320)

        def Title_language_selector_selected(event):

            selection = self.Title_language_selector.get()
            match selection:
                case 'Русский':
                    ru_i18n.install()
                    SettingsValues.Settings_language = 'ru'
                case 'English':
                    en_i18n.install()
                    SettingsValues.Settings_language = 'en'
                case _:
                    en_i18n.install()
                    SettingsValues.Settings_language = 'en'
            config.set("General", "Settings_language", SettingsValues.Settings_language)
            settings_config_update_write()
            global language_changed
            language_changed = True
            restart_app(self)

        self.Title_language_selector.bind("<<ComboboxSelected>>", Title_language_selector_selected)
        self.Title_language_selector.current(1 if SettingsValues.Settings_language == 'ru' else 0)
        self.Title_language_selector.ToolTip = ToolTip(self.Title_language_selector,
                                                       text=_("Select Language of Settings Programm"), wraplength=320)

        self.Title_frame.bind("<ButtonPress-1>", self.start_move)
        self.Title_frame.bind("<ButtonRelease-1>", self.stop_move)
        self.Title_frame.bind("<B1-Motion>", self.do_move)

        self.Content_frame = ttk.Frame(self, padding=2, bootstyle='light')
        self.Content_frame.pack(expand=True, fill='both', side=tk.BOTTOM)
        self.Top_Notebook = ttk.Notebook(self.Content_frame)
        self.Top_Notebook.pack(expand=True, fill=tk.BOTH)
        self.General_Settings_frame = ttk.Frame(self.Top_Notebook, padding=10)
        self.General_Settings_frame.pack(expand=True, fill=tk.BOTH)

        # -- GENERAL SETTINGS FRAME
        # -- ----------------------
        # -- ----------------------
        # -- ----------------------
        # -- ----------------------
        # -- ----------------------
        self.General_Settings_frame.Frame1 = ttk.Frame(self.General_Settings_frame)
        self.General_Settings_frame.Frame1.pack(expand=False, fill=tk.X)
        self.languages = ["Russian", "Catalan", "ChineseSimplified", "ChineseTraditional", "Czech", "Dutch", "French",
                          "German",
                          "Hungarian", "Italian", "Korean", "Polish", "PortugueseBrazilian", "Romanian", "Spanish",
                          "SpanishLatin",
                          "Turkish", "Ukrainian", _("Enter your language")]
        self.General_Settings_frame.Frame1.Label = ttk.Label(self.General_Settings_frame.Frame1,
                                                             text=_("Select language:"))
        self.General_Settings_frame.Frame1.Label.pack(expand=True, fill=ttk.Y, side='left', anchor='ne', padx=10)
        self.General_Settings_frame.Frame1.Label.ToolTip = ToolTip(self.General_Settings_frame.Frame1.Label, _(
            f"Choose the language you are going to translate mods into."
            f"\n   Rimworld официально переведен на несколько языков и для чтобы ваш перевод мода был автоматически добавлен в игру, а не выступал как отдельный новый язык, используйте предустановленные языки из списка."
        ), wraplength=320)

        self.General_Settings_frame.Frame1.Lang_selector = ttk.Combobox(self.General_Settings_frame.Frame1,
                                                                        values=self.languages, state="readonly")
        #   Disable MouseWheel chosing
        self.General_Settings_frame.Frame1.Lang_selector.bind("<MouseWheel>", 'break')
        self.General_Settings_frame.Frame1.Lang_selector.set(SettingsValues.Game_language)

        def callbackFunc(event):
            lang = event.widget.get()
            SettingsValues.Game_language = lang
            config.set("General", "Game_language", lang)
            settings_config_update_write()
            if lang == self.languages[-1]:
                self.General_Settings_frame.Frame1.Lang_selector['state'] = "!readonly"
                self.General_Settings_frame.Frame1.Lang_selector.set('')
            else:
                self.General_Settings_frame.Frame1.Lang_selector['state'] = "readonly"

        self.General_Settings_frame.Frame1.Lang_selector.bind("<<ComboboxSelected>>", callbackFunc)
        self.General_Settings_frame.Frame1.Lang_selector.bind("<Return>", callbackFunc)
        self.General_Settings_frame.Frame1.Lang_selector.pack(expand=True, fill=tk.X, side='left')
        self.General_Settings_frame.Frame1.Lang_selector.ToolTip = ToolTip(
            self.General_Settings_frame.Frame1.Lang_selector, _(
                f"Choose the language you are going to translate mods into."
                f"\n   Rimworld has been officially translated into several languages, and in order for your translation of the mod to be automatically added to the game,"
                f" and not act as a separate new language, use the preset languages from the list.\n"
                f"  If you want to change the program language, then the language is selected at the top next to the program close button."
            ), wraplength=320)

        self.General_Settings_frame.Pathes_to_Rimworld_frame = ttk.Labelframe(self.General_Settings_frame,
                                                                              text=_("Pathes to Rimworld folders"),
                                                                              padding=10)
        self.General_Settings_frame.Pathes_to_Rimworld_frame.pack()

        self.General_Settings_frame.Frame3 = ttk.Frame(self.General_Settings_frame.Pathes_to_Rimworld_frame)
        self.General_Settings_frame.Frame3.pack(anchor='nw')

        def Frame3_Path_to_Data_select_path():
            a = filedialog.askdirectory(title=_("Select Data folder"))
            SettingsValues.Path_to_Data = a if a else 'None'
            config.set("General", "Path_to_Data", SettingsValues.Path_to_Data)
            settings_config_update_write()
            self.General_Settings_frame.Frame3.Label['text'] = _(f"Rimworld Data:\n{SettingsValues.Path_to_Data}")

        self.General_Settings_frame.Frame3.Path_to_Data = ttk.Button(self.General_Settings_frame.Frame3,
                                                                     text=_("Select path to Rimworld Data"), width=50,
                                                                     command=Frame3_Path_to_Data_select_path)
        self.General_Settings_frame.Frame3.Path_to_Data.pack(expand=False, fill=tk.X, side='left')
        self.General_Settings_frame.Frame3.Label = ttk.Label(self.General_Settings_frame.Frame3,
                                                             text=_(f"Rimworld Data:\n{SettingsValues.Path_to_Data}"),
                                                             wraplength=500)
        self.General_Settings_frame.Frame3.Label.pack(padx=(20, 20), anchor='nw')

        self.General_Settings_frame.Frame4 = ttk.Frame(self.General_Settings_frame.Pathes_to_Rimworld_frame)
        self.General_Settings_frame.Frame4.pack(expand=False, fill=tk.X)

        def Frame4_Path_to_Mod_select_path():
            a = filedialog.askdirectory(title=_("Select MOD folder"))
            SettingsValues.Path_to_Mod_folder = a if a else 'None'
            config.set("General", "Path_to_Mod_folder", SettingsValues.Path_to_Mod_folder)
            settings_config_update_write()
            self.General_Settings_frame.Frame4.Label['text'] = _(
                f"Rimworld Mods Folder:\n{SettingsValues.Path_to_Mod_folder}")

        self.General_Settings_frame.Frame4.Path_to_Mod = ttk.Button(self.General_Settings_frame.Frame4,
                                                                    text=_("Select path to Rimworld Mods Folder"),
                                                                    width=50, command=Frame4_Path_to_Mod_select_path)
        self.General_Settings_frame.Frame4.Path_to_Mod.pack(expand=False, fill=tk.X, side='left')
        self.General_Settings_frame.Frame4.Label = ttk.Label(self.General_Settings_frame.Frame4, text=_(
            f"Rimworld Mods Folder:\n{SettingsValues.Path_to_Mod_folder}"), wraplength=500)
        self.General_Settings_frame.Frame4.Label.pack(padx=(20, 20), anchor='nw')

        self.General_Settings_frame.Frame5 = ttk.Frame(self.General_Settings_frame.Pathes_to_Rimworld_frame)
        self.General_Settings_frame.Frame5.pack(expand=False, fill=tk.X)

        def Frame5_Path_to_Another_folder_select_path():
            a = filedialog.askdirectory(title=_("Select Another mod folder"))
            SettingsValues.Path_to_Another_folder = a if a else _('None')
            config.set("General", "Path_to_Another_folder", SettingsValues.Path_to_Another_folder)
            settings_config_update_write()
            self.General_Settings_frame.Frame5.Label['text'] = _(
                f"Another Rimworld Mods Folder:\n{SettingsValues.Path_to_Another_folder}")

        self.General_Settings_frame.Frame5.Path_to_Another_folder = ttk.Button(self.General_Settings_frame.Frame5,
                                                                               text=_(
                                                                                   "Select path to another Rimworld Mods Folder"),
                                                                               width=50,
                                                                               command=Frame5_Path_to_Another_folder_select_path)
        self.General_Settings_frame.Frame5.Path_to_Another_folder.pack(expand=False, fill=tk.X, side='left')
        self.General_Settings_frame.Frame5.Label = ttk.Label(self.General_Settings_frame.Frame5, text=_(
            f"Another Rimworld Mods Folder:\n{SettingsValues.Path_to_Another_folder}"), wraplength=500)
        self.General_Settings_frame.Frame5.Label.pack(padx=(20, 20), anchor='nw')
        self.General_Settings_frame.Frame5.Path_to_Another_folder.ToolTip = ToolTip(
            self.General_Settings_frame.Frame5.Path_to_Another_folder,
            _('If you suddenly store mods somewhere else, you can specify this folder here. In this case, the program will work better with mods that depend on other mods (in case the values for translation are inherited from another mod).'),
            wraplength=320)
        '''Если вы внезапно храните моды где-то еще, то можете указать эту папку тут. В этом случае программа будет лучше работать с модами, которые зависят от других модов (В случае, если значения для перевода наследуются от другого мода).'''

        self.General_Settings_frame.Frame6 = ttk.Labelframe(self.General_Settings_frame,
                                                            text=_("Extraction files rules"))
        self.General_Settings_frame.Frame6.pack(anchor=tk.W)
        # self.General_Settings_frame.Frame6.Label = ttk.Label(self.General_Settings_frame.Frame6, text=_("Extraction files rules"))
        # self.General_Settings_frame.Frame6.Label.pack(pady=(20, 0))

        self.General_Settings_frame.Frame_left = ttk.Frame(self.General_Settings_frame.Frame6, padding=10)
        self.General_Settings_frame.Frame_left.pack(anchor=tk.W, side=tk.LEFT)

        self.Delete_old_versions_language = ttk.BooleanVar(value=SettingsValues.Delete_old_versions_translation)

        def General_Settings_frame_Frame7_Delete_old_folders():
            SettingsValues.Delete_old_versions_translation = bool(self.Delete_old_versions_language.get())
            config.set("General", "Delete_old_versions_translation",
                       str(SettingsValues.Delete_old_versions_translation))
            settings_config_update_write()

        self.General_Settings_frame.Frame_left.Delete_old_version_translate = ttk.Checkbutton(
            self.General_Settings_frame.Frame_left, text=_("Delete old version folders"),
            variable=self.Delete_old_versions_language, command=General_Settings_frame_Frame7_Delete_old_folders)
        self.General_Settings_frame.Frame_left.Delete_old_version_translate.pack(anchor=tk.W, pady=(0, 0))
        self.General_Settings_frame.Frame_left.Delete_old_version_translate.ToolTip = ToolTip(
            self.General_Settings_frame.Frame_left.Delete_old_version_translate, text=_(
                'Delete (Not extract) text for older versions of Rimworld.\nBy default, the program extracts text for all available versions ( ... 1.0, 1.1, 1.2 ...). You can leave only the newest version, so as not to translate too much (Which I advise you to do)'),
            wraplength=320)

        self.Merge_folders = ttk.BooleanVar(value=SettingsValues.Merge_folders)

        def General_Settings_frame_Frame8_Merge_folders():
            SettingsValues.Merge_folders = bool(self.Merge_folders.get())
            config.set("General", "Merge_folders", str(SettingsValues.Merge_folders))
            settings_config_update_write()

        self.General_Settings_frame.Frame_left.Merge_folders = ttk.Checkbutton(self.General_Settings_frame.Frame_left,
                                                                               text=_("Merge Folders"),
                                                                               variable=self.Merge_folders,
                                                                               command=General_Settings_frame_Frame8_Merge_folders)
        self.General_Settings_frame.Frame_left.Merge_folders.pack(anchor=tk.W, pady=(10, 0))
        self.General_Settings_frame.Frame_left.Merge_folders.ToolTip = ToolTip(
            self.General_Settings_frame.Frame_left.Merge_folders,
            text=_('Merge version and Language folders into one Language folder\n'
                   '(If there is only one version folder)'), wraplength=320)

        self.Not_rename_files = ttk.BooleanVar(value=SettingsValues.Not_rename_files)

        def General_Settings_frame_Frame9_Not_rename():
            SettingsValues.Not_rename_files = bool(self.Not_rename_files.get())
            config.set("General", "Not_rename_files", str(SettingsValues.Not_rename_files))
            settings_config_update_write()

        self.General_Settings_frame.Frame_left.Not_rename = ttk.Checkbutton(self.General_Settings_frame.Frame_left,
                                                                            text=_("Not rename files"),
                                                                            variable=self.Not_rename_files,
                                                                            command=General_Settings_frame_Frame9_Not_rename)
        self.General_Settings_frame.Frame_left.Not_rename.pack(anchor=tk.W, pady=(10, 0))
        self.General_Settings_frame.Frame_left.Not_rename.ToolTip = ToolTip(
            self.General_Settings_frame.Frame_left.Not_rename, text=_(
                "Files are automatically renamed depending on the folders they fall into. This is necessary to prevent the files from having the same names, which may lead to the fact that the game will not read the translation files.\n"
                "(Check the box if you don't like it and you want to keep the original titles)"), wraplength=320)

        # -- COMMENT SETTINGS FRAME
        # -- ----------------------
        # -- ----------------------
        # -- ----------------------
        # -- ----------------------
        # -- ----------------------
        self.CommFrame = ttk.Frame(self.Top_Notebook)
        self.CommFrame.pack(expand=True, fill=tk.BOTH)

        self.CommFrame.Frame_all = ttk.Frame(self.CommFrame)
        self.CommFrame.Frame_all.pack(expand=False, fill=tk.X, padx=100)

        self.CommFrame.Frame_left = ttk.Frame(self.CommFrame.Frame_all)
        self.CommFrame.Frame_left.pack(anchor=tk.W, side=tk.LEFT)

        def CommFrame_Add_filename_comment():
            SettingsValues.Add_filename_comment = bool(self.Add_filename_comment.get())
            config.set("Comment", "Add_filename_comment",
                       str(SettingsValues.Add_filename_comment))
            settings_config_update_write()
            change_comm_checkbtn_img()

        self.Add_filename_comment = ttk.BooleanVar(value=SettingsValues.Add_filename_comment)
        self.CommFrame.Frame_left.Add_filename_comment = ttk.Checkbutton(self.CommFrame.Frame_left, text=_(
            "Add in file comment with FullPath of Original file"), variable=self.Add_filename_comment,
                                                                         command=CommFrame_Add_filename_comment)
        self.CommFrame.Frame_left.Add_filename_comment.pack(anchor=tk.W, pady=(10, 0))

        def CommFrame_Add_comment():
            SettingsValues.Add_comment = bool(self.Add_comment.get())
            config.set("Comment", "Add_comment",
                       str(SettingsValues.Add_comment))
            settings_config_update_write()

            if self.Add_comment.get():
                self.CommFrame.Frame_left.Comment_add_EN.configure(state='normal')
                self.CommFrame.Frame_right.Comment_starting_similar_as_ogiganal_text.configure(state='normal')
                self.CommFrame.Frame_right.Comment_spacing_before_tag.configure(state='normal')
                self.CommFrame.Frame_right.Comment_replace_n_as_new_line.configure(state='normal')

                if self.Comment_starting_similar_as_ogiganal_text.get():
                    self.CommFrame.Frame_right.Comment_spacing_before_tag.configure(state='normal')
                else:
                    self.CommFrame.Frame_right.Comment_spacing_before_tag.configure(state='disabled')
            else:
                self.CommFrame.Frame_left.Comment_add_EN.configure(state='disabled')
                self.CommFrame.Frame_right.Comment_starting_similar_as_ogiganal_text.configure(state='disabled')
                self.CommFrame.Frame_right.Comment_spacing_before_tag.configure(state='disabled')
                self.CommFrame.Frame_right.Comment_replace_n_as_new_line.configure(state='disabled')
            change_comm_checkbtn_img()

        self.Add_comment = ttk.BooleanVar(value=SettingsValues.Add_comment)
        self.CommFrame.Frame_left.Add_comment = ttk.Checkbutton(self.CommFrame.Frame_left,
                                                                text=_("Add comments to grabbed text"),
                                                                variable=self.Add_comment,
                                                                command=CommFrame_Add_comment)
        self.CommFrame.Frame_left.Add_comment.pack(anchor=tk.W, pady=(10, 0))

        def CommFrame_Comment_add_EN():
            SettingsValues.Comment_add_EN = bool(self.Comment_add_EN.get())
            config.set("Comment", "Comment_add_EN",
                       str(SettingsValues.Comment_add_EN))
            settings_config_update_write()
            change_comm_checkbtn_img()

        self.Comment_add_EN = ttk.BooleanVar(value=SettingsValues.Comment_add_EN)
        self.CommFrame.Frame_left.Comment_add_EN = ttk.Checkbutton(self.CommFrame.Frame_left,
                                                                   text=_('Add "EN:" before comment text'),
                                                                   variable=self.Comment_add_EN,
                                                                   command=CommFrame_Comment_add_EN)
        self.CommFrame.Frame_left.Comment_add_EN.pack(anchor=tk.W, pady=(10, 0))

        self.CommFrame.Frame_right = ttk.Frame(self.CommFrame.Frame_all)
        self.CommFrame.Frame_right.pack(anchor='nw', side=tk.RIGHT)

        def CommFrame_Comment_starting_similar_as_ogiganal_text():
            SettingsValues.Comment_starting_similar_as_ogiganal_text = bool(
                self.Comment_starting_similar_as_ogiganal_text.get())
            config.set("Comment", "Comment_starting_similar_as_ogiganal_text",
                       str(SettingsValues.Comment_starting_similar_as_ogiganal_text))
            settings_config_update_write()
            if self.Comment_starting_similar_as_ogiganal_text.get():
                self.CommFrame.Frame_right.Comment_spacing_before_tag.configure(state='normal')
            else:
                self.CommFrame.Frame_right.Comment_spacing_before_tag.configure(state='disabled')
            change_comm_checkbtn_img()

        self.Comment_starting_similar_as_ogiganal_text = ttk.BooleanVar(
            value=SettingsValues.Comment_starting_similar_as_ogiganal_text)
        self.CommFrame.Frame_right.Comment_starting_similar_as_ogiganal_text = ttk.Checkbutton(
            self.CommFrame.Frame_right, text=_("Place the comment text exactly above the original text"),
            variable=self.Comment_starting_similar_as_ogiganal_text,
            command=CommFrame_Comment_starting_similar_as_ogiganal_text)
        self.CommFrame.Frame_right.Comment_starting_similar_as_ogiganal_text.pack(anchor=tk.W, pady=(10, 0))

        def CommFrame_Comment_spacing_before_tag():
            SettingsValues.Comment_spacing_before_tag = bool(self.Comment_spacing_before_tag.get())
            config.set("Comment", "Comment_spacing_before_tag",
                       str(SettingsValues.Comment_spacing_before_tag))
            settings_config_update_write()
            change_comm_checkbtn_img()

        self.Comment_spacing_before_tag = ttk.BooleanVar(value=SettingsValues.Comment_spacing_before_tag)
        self.CommFrame.Frame_right.Comment_spacing_before_tag = ttk.Checkbutton(self.CommFrame.Frame_right, text=_(
            "Left spacing are in before the comment"), variable=self.Comment_spacing_before_tag,
                                                                                command=CommFrame_Comment_spacing_before_tag)
        self.CommFrame.Frame_right.Comment_spacing_before_tag.pack(anchor=tk.W, pady=(10, 0))

        def CommFrame_Comment_replace_n_as_new_line():
            SettingsValues.Comment_replace_n_as_new_line = bool(self.Comment_replace_n_as_new_line.get())
            config.set("Comment", "Comment_replace_n_as_new_line",
                       str(SettingsValues.Comment_replace_n_as_new_line))
            settings_config_update_write()
            change_comm_checkbtn_img()

        self.Comment_replace_n_as_new_line = ttk.BooleanVar(value=SettingsValues.Comment_replace_n_as_new_line)
        self.CommFrame.Frame_right.Comment_replace_n_as_new_line = ttk.Checkbutton(self.CommFrame.Frame_right, text=_(
            "Comment replace \\n as new line"), variable=self.Comment_replace_n_as_new_line,
                                                                                   command=CommFrame_Comment_replace_n_as_new_line)
        self.CommFrame.Frame_right.Comment_replace_n_as_new_line.pack(anchor=tk.W, pady=(10, 0))

        if not self.Add_comment.get():
            self.CommFrame.Frame_left.Comment_add_EN.configure(state='disabled')
            self.CommFrame.Frame_right.Comment_starting_similar_as_ogiganal_text.configure(state='disabled')
            self.CommFrame.Frame_right.Comment_spacing_before_tag.configure(state='disabled')
            self.CommFrame.Frame_right.Comment_replace_n_as_new_line.configure(state='disabled')

        if not self.Comment_starting_similar_as_ogiganal_text.get():
            self.CommFrame.Frame_right.Comment_spacing_before_tag.configure(state='disabled')

        def change_comm_checkbtn_img():
            def get_img_code() -> str:
                if self.Add_filename_comment.get():
                    a1 = 1
                else:
                    a1 = 0
                if self.Add_comment.get():
                    a2 = 1
                else:
                    a2 = 0
                if self.Comment_add_EN.get():
                    a3 = 1
                else:
                    a3 = 0
                if self.Comment_starting_similar_as_ogiganal_text.get():
                    a4 = 1
                else:
                    a4 = 0
                if self.Comment_spacing_before_tag.get():
                    a5 = 1
                else:
                    a5 = 0
                if self.Comment_replace_n_as_new_line.get():
                    a6 = 1
                else:
                    a6 = 0
                if a2 == 0:
                    a3, a4, a5, a6 = 0, 0, 0, 0
                if a4 == 0:
                    a5 = 0
                return str(a1) + str(a2) + str(a3) + str(a4) + str(a5) + str(a6)

            # self.Comm_Image_label.configure(image=PhotoImage(file=f'Images/Comments/{get_img_code()}.png'))
            self.Comm_Image.configure(file=f'Images/Comments/{get_img_code()}.png')

        self.Comm_Image_Frame = ttk.Frame(self.CommFrame)
        self.Comm_Image_Frame.pack(anchor=tk.CENTER)

        self.Comm_Image = PhotoImage(file='Images/Comments/000000.png')
        self.Comm_Image_label = ttk.Label(self.Comm_Image_Frame, image=self.Comm_Image)
        self.Comm_Image_label.pack(anchor=tk.CENTER)

        change_comm_checkbtn_img()

        # -- Grabbing SETTINGS FRAME
        # -- ----------------------
        # -- ----------------------
        # -- ----------------------
        # -- ----------------------
        # -- ----------------------
        self.GrabFrame = ttk.Frame(self.Top_Notebook)
        self.GrabFrame.pack(expand=True, fill=tk.BOTH)

        self.GrabFrame.Frame_all = ttk.Frame(self.GrabFrame)
        self.GrabFrame.Frame_all.pack(expand=False, fill=tk.X, padx=100)

        self.GrabFrame.Frame_left = ttk.LabelFrame(self.GrabFrame.Frame_all, text=_('StuffAdjective'))
        self.GrabFrame.Frame_left.pack(anchor=tk.W, side=tk.LEFT)

        def GrabFrame_Add_stuffAdjective_and_mark_it():
            SettingsValues.Add_stuffAdjective_and_mark_it = bool(self.Add_stuffAdjective_and_mark_it.get())
            config.set("Grabbing", "Add_stuffAdjective_and_mark_it",
                       str(SettingsValues.Add_stuffAdjective_and_mark_it))
            settings_config_update_write()
            if bool(self.Add_stuffAdjective_and_mark_it.get()):
                self.GrabFrame.Frame_left.Add_stuffAdjective_and_mark_it.mark_entry.configure(state='normal')
            else:
                self.GrabFrame.Frame_left.Add_stuffAdjective_and_mark_it.mark_entry.configure(state='disabled')

        self.Add_stuffAdjective_and_mark_it = ttk.BooleanVar(value=SettingsValues.Add_stuffAdjective_and_mark_it)
        self.GrabFrame.Frame_left.Add_stuffAdjective_and_mark_it = ttk.Checkbutton(self.GrabFrame.Frame_left, text=_(
            "Add stuffAdjective and mark it"), variable=self.Add_stuffAdjective_and_mark_it,
                                                                                   command=GrabFrame_Add_stuffAdjective_and_mark_it)
        self.GrabFrame.Frame_left.Add_stuffAdjective_and_mark_it.pack(anchor=tk.W, pady=(10, 0), padx=10)
        self.GrabFrame.Frame_left.Add_stuffAdjective_and_mark_it.ToolTip = ToolTip(
            self.GrabFrame.Frame_left.Add_stuffAdjective_and_mark_it, text=_(
                "Some materials can be used to build buildings / make objects, but the authors do not add a special label for this. And in translation it turns out: 'Made of stone'. This is normal for English, but not for some languages.  Therefore, I decided to add a special label to understand how to translate a word as an adjective/ genitive. \n You can write yourself how to designate such words in the text. To correctly translate such a word, you need to mentally put 'The house is made of' in front of it. \n '~LABEL~' will be replaced with the original word. If you just want to add such words for translation, but do not want to mark them separately, then you can only write '~LABEL~'."))
        '''Из некоторых материалов можно строить здания / делать предметы, но авторы не добавляет специальную метку для этого. И в переводе получается: 'Сделанный из камень'. Для английского языка это нормально, но для некоторых языков нет.  Поэтому я решил добавить специальную метку, чтобы понимать как нужно переводить слово как прилагательное / родительный падеж. \n  Вы можете написать сами как обозначать в тексте такие слова. \n '~LABEL~' будет заменен на оригинальное слово. Если вы хотите просто добавить такие слова для перевода, но не хотите их отдельно отмечать, то можете написать только '~LABEL~'.'''

        self.Add_stuffAdjective_and_mark_it_text_var = ttk.StringVar(
            value=SettingsValues.Add_stuffAdjective_and_mark_it_text)
        self.GrabFrame.Frame_left.Add_stuffAdjective_and_mark_it.mark_entry = ttk.Entry(self.GrabFrame.Frame_left,
                                                                                        textvariable=self.Add_stuffAdjective_and_mark_it_text_var,
                                                                                        width=32)
        self.GrabFrame.Frame_left.Add_stuffAdjective_and_mark_it.mark_entry.pack(anchor=tk.W, pady=(10, 10), padx=10)
        self.GrabFrame.Frame_left.Add_stuffAdjective_and_mark_it.mark_entry.ToolTip = ToolTip(
            self.GrabFrame.Frame_left.Add_stuffAdjective_and_mark_it.mark_entry, text=_(
                "'~LABEL~' will be replaced with the original word. \n If you just want to add such words for translation, but do not want to mark them separately, then you can only write '~LABEL~'"))

        def Add_stuffAdjective_and_mark_it_text_var_callback(*_):
            SettingsValues.Add_stuffAdjective_and_mark_it_text = self.Add_stuffAdjective_and_mark_it_text_var.get()
            if '~LABEL~' not in SettingsValues.Add_stuffAdjective_and_mark_it_text:
                self.Add_stuffAdjective_and_mark_it_text_var.set(
                    SettingsValues.Add_stuffAdjective_and_mark_it_text + "~LABEL~")
                SettingsValues.Add_stuffAdjective_and_mark_it_text = self.Add_stuffAdjective_and_mark_it_text_var.get()
            config.set("Grabbing", "Add_stuffAdjective_and_mark_it_text",
                       str(SettingsValues.Add_stuffAdjective_and_mark_it_text))
            settings_config_update_write()

        self.Add_stuffAdjective_and_mark_it_text_var.trace_add('write',
                                                               Add_stuffAdjective_and_mark_it_text_var_callback)

        self.GrabFrame.Frame_right = ttk.Frame(self.GrabFrame.Frame_all)
        self.GrabFrame.Frame_right.pack(anchor=tk.W, side=tk.RIGHT)

        self.Check_one_letter = ttk.BooleanVar(value=SettingsValues.Check_at_least_one_letter_in_text)

        def General_Settings_frame_Frame9_Check_one_letter():
            SettingsValues.Check_at_least_one_letter_in_text = bool(self.Check_one_letter.get())
            config.set("Grabbing", "Check_at_least_one_letter_in_text",
                       str(SettingsValues.Check_at_least_one_letter_in_text))
            settings_config_update_write()

        self.GrabFrame.Frame_right.Not_rename = ttk.Checkbutton(self.GrabFrame.Frame_right,
                                                                text=_("Check at least one letter in text"),
                                                                variable=self.Check_one_letter,
                                                                command=General_Settings_frame_Frame9_Check_one_letter)
        self.GrabFrame.Frame_right.Not_rename.pack(anchor=tk.W, pady=(10, 0))
        self.GrabFrame.Frame_right.Not_rename.ToolTip = ToolTip(self.GrabFrame.Frame_right.Not_rename, text=_(
            'Check if there is at least one letter in the extracted text. This is necessary so as not to extract all sorts of (255, 123, 112).\nYou may want to remove the flag if the mod adds various symbols without letters that you want to translate like "<--",\nI do not know why to translate it at all, but who knows ^_^'),
                                                                wraplength=320)

        self.add_titleFemale = ttk.BooleanVar(value=SettingsValues.add_titleFemale)

        def General_Settings_frame_Frame10_add_titleFemale():
            SettingsValues.add_titleFemale = bool(self.add_titleFemale.get())
            config.set("Grabbing", "add_titleFemale", str(SettingsValues.add_titleFemale))
            settings_config_update_write()

        self.GrabFrame.Frame_right.add_titleFemale = ttk.Checkbutton(self.GrabFrame.Frame_right, text=_(
            "Add titleFemale if it is not in the original file"), variable=self.add_titleFemale,
                                                                     command=General_Settings_frame_Frame10_add_titleFemale)
        self.GrabFrame.Frame_right.add_titleFemale.pack(anchor=tk.W, pady=(10, 0))

        self.add_titleShortFemale = ttk.BooleanVar(value=SettingsValues.add_titleShortFemale)

        def General_Settings_frame_Frame10_add_titleShortFemale():
            SettingsValues.add_titleShortFemale = bool(self.add_titleShortFemale.get())
            config.set("Grabbing", "add_titleShortFemale", str(SettingsValues.add_titleShortFemale))
            settings_config_update_write()

        self.GrabFrame.Frame_right.add_titleShortFemale = ttk.Checkbutton(self.GrabFrame.Frame_right, text=_(
            "Add titleShortFemale if it is not in the original file"), variable=self.add_titleShortFemale,
                                                                          command=General_Settings_frame_Frame10_add_titleShortFemale)
        self.GrabFrame.Frame_right.add_titleShortFemale.pack(anchor=tk.W, pady=(10, 0))

        def callback_Tkey_system_on():
            SettingsValues.Tkey_system_on = bool(self.Tkey_system_on.get())
            config.set("Grabbing", "Tkey_system_on", str(SettingsValues.Tkey_system_on))
            settings_config_update_write()

        self.Tkey_system_on = ttk.BooleanVar(value=SettingsValues.Tkey_system_on)
        self.GrabFrame.Frame_right.Tkey_system_on = ttk.Checkbutton(self.GrabFrame.Frame_right,
                                                                    text=_("QuestScriptDef Tkey system"),
                                                                    variable=self.Tkey_system_on,
                                                                    command=callback_Tkey_system_on)
        self.GrabFrame.Frame_right.Tkey_system_on.pack(anchor=tk.W, pady=(10, 0))
        self.GrabFrame.Frame_right.Tkey_system_on.ToolTip = ToolTip(self.GrabFrame.Frame_right.Tkey_system_on,
                                                                    text=_(
                                                                        "At 1.4 patch TKey system was broken. If the developers fix it, then enable this feature.\n The Tkey system is specifically designed to simplify long tag paths."))

        self.GrabFrame.Frame_2 = ttk.Frame(self.GrabFrame, )
        self.GrabFrame.Frame_2.pack(anchor=tk.W, pady=(5, 0))

        self.GrabFrame.Next_Frame = ttk.Frame(self.GrabFrame.Frame_2)
        self.GrabFrame.Next_Frame.pack(fill=ttk.Y, anchor=tk.W, pady=(5, 0), padx=(100, 15), side='left')

        def make_plural_frames():
            self.GrabFrame.Plurel_Frame = ttk.Labelframe(self.GrabFrame.Frame_2, text=_("PawnKindDef Plural labels"))
            self.GrabFrame.Plurel_Frame.pack(anchor=tk.W, pady=(5, 0), side='left', fill=ttk.Y)

            self.GrabFrame.Plurel_Frame_inside = ttk.Frame(self.GrabFrame.Plurel_Frame, padding=5)
            self.GrabFrame.Plurel_Frame_inside.pack(anchor=tk.W, padx=2)

            self.labelPlural = ttk.BooleanVar(value=SettingsValues.labelPlural)
            self.labelMale = ttk.BooleanVar(value=SettingsValues.labelMale)
            self.labelFemale = ttk.BooleanVar(value=SettingsValues.labelFemale)
            self.labelMalePlural = ttk.BooleanVar(value=SettingsValues.labelMalePlural)
            self.labelFemalePlural = ttk.BooleanVar(value=SettingsValues.labelFemalePlural)

            def callback_Plural_Checkbuttons():
                SettingsValues.labelPlural = bool(self.labelPlural.get())
                SettingsValues.labelMale = bool(self.labelMale.get())
                SettingsValues.labelFemale = bool(self.labelFemale.get())
                SettingsValues.labelMalePlural = bool(self.labelMalePlural.get())
                SettingsValues.labelFemalePlural = bool(self.labelFemalePlural.get())
                config.set("Grabbing", "labelPlural", str(SettingsValues.labelPlural))
                config.set("Grabbing", "labelMale", str(SettingsValues.labelMale))
                config.set("Grabbing", "labelFemale", str(SettingsValues.labelFemale))
                config.set("Grabbing", "labelMalePlural", str(SettingsValues.labelMalePlural))
                config.set("Grabbing", "labelFemalePlural", str(SettingsValues.labelFemalePlural))
                settings_config_update_write()

            self.GrabFrame.Plurel_Frame_inside.labelPlural = ttk.Checkbutton(self.GrabFrame.Plurel_Frame_inside,
                                                                             text=_("Add labelPlural"),
                                                                             variable=self.labelPlural,
                                                                             command=callback_Plural_Checkbuttons)
            self.GrabFrame.Plurel_Frame_inside.labelPlural.pack(anchor=tk.W, pady=(0, 0))
            self.GrabFrame.Plurel_Frame_inside.labelPlural.ToolTip = ToolTip(
                self.GrabFrame.Plurel_Frame_inside.labelPlural,
                text=_("Add missing tags to choose from in PawnKindDef if they don't exist."))

            self.GrabFrame.Plurel_Frame_inside.labelMale = ttk.Checkbutton(self.GrabFrame.Plurel_Frame_inside,
                                                                           text=_("Add labelMale"),
                                                                           variable=self.labelMale,
                                                                           command=callback_Plural_Checkbuttons)
            self.GrabFrame.Plurel_Frame_inside.labelMale.pack(anchor=tk.W, pady=(1, 0))
            self.GrabFrame.Plurel_Frame_inside.labelMale.ToolTip = ToolTip(self.GrabFrame.Plurel_Frame_inside.labelMale,
                                                                           text=_(
                                                                               "Add missing tags to choose from in PawnKindDef if they don't exist."))

            self.GrabFrame.Plurel_Frame_inside.labelFemale = ttk.Checkbutton(self.GrabFrame.Plurel_Frame_inside,
                                                                             text=_("Add labelFemale"),
                                                                             variable=self.labelFemale,
                                                                             command=callback_Plural_Checkbuttons)
            self.GrabFrame.Plurel_Frame_inside.labelFemale.pack(anchor=tk.W, pady=(1, 0))
            self.GrabFrame.Plurel_Frame_inside.labelFemale.ToolTip = ToolTip(
                self.GrabFrame.Plurel_Frame_inside.labelFemale,
                text=_("Add missing tags to choose from in PawnKindDef if they don't exist."))

            self.GrabFrame.Plurel_Frame_inside.labelMalePlural = ttk.Checkbutton(self.GrabFrame.Plurel_Frame_inside,
                                                                                 text=_("Add labelMalePlural"),
                                                                                 variable=self.labelMalePlural,
                                                                                 command=callback_Plural_Checkbuttons)
            self.GrabFrame.Plurel_Frame_inside.labelMalePlural.pack(anchor=tk.W, pady=(1, 0))
            self.GrabFrame.Plurel_Frame_inside.labelMalePlural.ToolTip = ToolTip(
                self.GrabFrame.Plurel_Frame_inside.labelMalePlural,
                text=_("Add missing tags to choose from in PawnKindDef if they don't exist."))

            self.GrabFrame.Plurel_Frame_inside.labelFemalePlural = ttk.Checkbutton(self.GrabFrame.Plurel_Frame_inside,
                                                                                   text=_("Add labelFemalePlural"),
                                                                                   variable=self.labelFemalePlural,
                                                                                   command=callback_Plural_Checkbuttons)
            self.GrabFrame.Plurel_Frame_inside.labelFemalePlural.pack(anchor=tk.W, pady=(1, 0))
            self.GrabFrame.Plurel_Frame_inside.labelFemalePlural.ToolTip = ToolTip(
                self.GrabFrame.Plurel_Frame_inside.labelFemalePlural,
                text=_("Add missing tags to choose from in PawnKindDef if they don't exist."))

        make_plural_frames()

        self.GrabFrame.Next_Frame_inside = ttk.LabelFrame(self.GrabFrame.Next_Frame, padding=5, text=_('Spacing'))
        self.GrabFrame.Next_Frame_inside.pack(anchor=tk.W, padx=0)

        self.GrabFrame.tags_left_spacing_frame = ttk.Frame(self.GrabFrame.Next_Frame_inside)
        self.GrabFrame.tags_left_spacing_frame.pack(anchor=tk.W, padx=10)

        self.GrabFrame.tags_left_spacing_radibtns_frame = ttk.Labelframe(self.GrabFrame.tags_left_spacing_frame,
                                                                         text=_('Grabbed lines left spacing'))
        self.GrabFrame.tags_left_spacing_radibtns_frame.pack(anchor=tk.W, pady=(5, 10))

        self.GrabFrame.tags_left_spacing_radibtns_frame_inside = ttk.Frame(
            self.GrabFrame.tags_left_spacing_radibtns_frame)
        self.GrabFrame.tags_left_spacing_radibtns_frame_inside.pack(anchor=tk.W, padx=5, pady=5)

        self.GrabFrame.tags_left_spacing_var = tk.StringVar(value=SettingsValues.tags_left_spacing)

        def tags_left_spacing_var_change():
            SettingsValues.tags_left_spacing = f'"{self.GrabFrame.tags_left_spacing_var.get()}"'
            config.set("Grabbing", "tags_left_spacing",
                       str(SettingsValues.tags_left_spacing))
            settings_config_update_write()

        self.GrabFrame.tags_left_spacing_var.trace("w", lambda *_: tags_left_spacing_var_change())
        self.GrabFrame.tags_left_spacing_radibtns_frame_inside.one_tab = ttk.Radiobutton(
            self.GrabFrame.tags_left_spacing_radibtns_frame_inside, text=_("One tab"), value='\t',
            variable=self.GrabFrame.tags_left_spacing_var)
        self.GrabFrame.tags_left_spacing_radibtns_frame_inside.one_tab.pack(anchor=tk.W, padx=(2, 0), pady=(1, 0))
        self.GrabFrame.tags_left_spacing_radibtns_frame_inside.one_tab.ToolTip_image = PhotoImage(
            file='Images/Grabbing/One_tab.png')
        self.GrabFrame.tags_left_spacing_radibtns_frame_inside.one_tab.ToolTip = ToolTipImage(
            self.GrabFrame.tags_left_spacing_radibtns_frame_inside.one_tab,
            image=self.GrabFrame.tags_left_spacing_radibtns_frame_inside.one_tab.ToolTip_image)

        self.GrabFrame.tags_left_spacing_radibtns_frame_inside.two_spaces = ttk.Radiobutton(
            self.GrabFrame.tags_left_spacing_radibtns_frame_inside, text=_("Two spaces"), value='  ',
            variable=self.GrabFrame.tags_left_spacing_var)
        self.GrabFrame.tags_left_spacing_radibtns_frame_inside.two_spaces.pack(anchor=tk.W, padx=(2, 0), pady=(0, 0))
        self.GrabFrame.tags_left_spacing_radibtns_frame_inside.two_spaces.ToolTip_image = PhotoImage(
            file='Images/Grabbing/Two_spaces.png')
        self.GrabFrame.tags_left_spacing_radibtns_frame_inside.two_spaces.ToolTip = ToolTipImage(
            self.GrabFrame.tags_left_spacing_radibtns_frame_inside.two_spaces,
            image=self.GrabFrame.tags_left_spacing_radibtns_frame_inside.two_spaces.ToolTip_image)

        self.GrabFrame.tags_left_spacing_radibtns_frame_inside.no_spaces = ttk.Radiobutton(
            self.GrabFrame.tags_left_spacing_radibtns_frame_inside, text=_("No spaces"), value='',
            variable=self.GrabFrame.tags_left_spacing_var)
        self.GrabFrame.tags_left_spacing_radibtns_frame_inside.no_spaces.pack(anchor=tk.W, padx=(2, 0), pady=(0, 2))
        self.GrabFrame.tags_left_spacing_radibtns_frame_inside.no_spaces.ToolTip_image = PhotoImage(
            file='Images/Grabbing/No_spaces.png')
        self.GrabFrame.tags_left_spacing_radibtns_frame_inside.no_spaces.ToolTip = ToolTipImage(
            self.GrabFrame.tags_left_spacing_radibtns_frame_inside.no_spaces,
            image=self.GrabFrame.tags_left_spacing_radibtns_frame_inside.no_spaces.ToolTip_image)

        def callback_Add_new_line_next_defname():
            SettingsValues.Add_new_line_next_defname = bool(self.Add_new_line_next_defname.get())
            config.set("Grabbing", "Add_new_line_next_defname", str(SettingsValues.Add_new_line_next_defname))
            settings_config_update_write()

        self.Add_new_line_next_defname = ttk.BooleanVar(value=SettingsValues.Add_new_line_next_defname)
        self.GrabFrame.Next_Frame_inside.Add_new_line_next_defname = ttk.Checkbutton(self.GrabFrame.Next_Frame_inside,
                                                                                     text=_(
                                                                                         "Add empty line before new grabbed defname"),
                                                                                     variable=self.Add_new_line_next_defname,
                                                                                     command=callback_Add_new_line_next_defname)
        self.GrabFrame.Next_Frame_inside.Add_new_line_next_defname.pack(anchor=tk.W, pady=(0, 0), padx=10)

        self.GrabFrame.Next_Frame_inside.Add_new_line_next_defname.ToolTip_image = PhotoImage(
            file='Images/Grabbing/Add_new_line_next_defname.png')

        self.GrabFrame.Next_Frame_inside.Add_new_line_next_defname.ToolTip = ToolTipImage(
            self.GrabFrame.Next_Frame_inside.Add_new_line_next_defname,
            image=self.GrabFrame.Next_Frame_inside.Add_new_line_next_defname.ToolTip_image,
            text=_("Divide the text into blocks by Defname"))

        # -- About SETTINGS FRAME
        # -- ----------------------
        # -- ----------------------
        # -- ----------------------
        # -- ----------------------
        # -- ----------------------

        self.AboutFrame = ttk.Frame(self.Top_Notebook)
        self.AboutFrame.pack(expand=True, fill=tk.BOTH)

        self.AboutFrame.F1 = ttk.Frame(self.AboutFrame, padding=10)
        self.AboutFrame.F1.pack(expand=False, fill=tk.X, padx=10, pady=(10, 0))

        self.AboutFrame.F1.left = ttk.Frame(self.AboutFrame.F1)
        self.AboutFrame.F1.left.pack(anchor='nw', side='left')

        self.AboutFrame.F1.right = ttk.Labelframe(self.AboutFrame.F1, text=_('Description'))
        self.AboutFrame.F1.right.pack(anchor='ne', padx=(5, 0), pady=(0, 0), side='right')

        self.AboutFrame.F1.right.Description = ttk.Text(self.AboutFrame.F1.right, height=10)
        self.AboutFrame.F1.right.Description.pack(padx=(5, 5), pady=(0, 5))

        def Description_callback(*_):
            SettingsValues.Description = self.AboutFrame.F1.right.Description.get(1.0, ttk.END)
            with open(r"Settings\\Description.txt", 'w', encoding='utf8') as desc_file:
                desc_file.write(SettingsValues.Description.strip(" \n"))
            about_example_update()

        self.AboutFrame.F1.right.Description.insert(0.0, SettingsValues.Description)
        self.AboutFrame.F1.right.Description.bind('<KeyRelease>', lambda e: Description_callback())

        self.AboutFrame.F1.fl1 = ttk.Frame(self.AboutFrame.F1.left)
        self.AboutFrame.F1.fl1.pack(anchor='nw')

        self.AboutFrame.F1.fl1.Author_label = ttk.Labelframe(self.AboutFrame.F1.fl1, text=_("Author"))
        self.AboutFrame.F1.fl1.Author_label.pack(anchor='nw', side='left')

        self.Author_Entry = ttk.StringVar(value=SettingsValues.Author)

        self.AboutFrame.F1.fl1.Author_Entry = ttk.Entry(self.AboutFrame.F1.fl1.Author_label,
                                                        textvariable=self.Author_Entry, width=32)
        self.AboutFrame.F1.fl1.Author_Entry.pack(anchor='nw', padx=5, pady=5)

        def Author_Entry_callback(*_):
            SettingsValues.Author = self.Author_Entry.get()
            config.set("About.xml", "Author",
                       str(SettingsValues.Author))
            settings_config_update_write()
            about_example_update()

        self.Author_Entry.trace_add('write', Author_Entry_callback)

        self.AboutFrame.F1.fl1.New_name_label = ttk.Labelframe(self.AboutFrame.F1.fl1, text=_("New Name"))
        self.AboutFrame.F1.fl1.New_name_label.pack(anchor='nw', side='left', padx=5)

        self.New_Name = ttk.StringVar(value=SettingsValues.New_Name)

        self.AboutFrame.F1.fl1.New_name_Entry = ttk.Entry(self.AboutFrame.F1.fl1.New_name_label,
                                                          textvariable=self.New_Name, width=32)
        self.AboutFrame.F1.fl1.New_name_Entry.pack(anchor='nw', padx=5, pady=5)
        self.AboutFrame.F1.fl1.New_name_Entry.ToolTip = ToolTip(self.AboutFrame.F1.fl1.New_name_Entry, text=_(
            '~MOD_NAME~ will be replaced with the name of the original mod.'))

        def New_Name_Entry_callback(*_):
            SettingsValues.New_Name = self.New_Name.get()
            config.set("About.xml", "New_Name",
                       str(SettingsValues.New_Name))
            if '~MOD_NAME~' not in SettingsValues.New_Name:
                self.New_Name.set("~MOD_NAME~")
                self.AboutFrame.F1.fl1.New_name_Entry.icursor(10)
                SettingsValues.New_Name = self.New_Name.get()
            settings_config_update_write()
            about_example_update()

        self.New_Name.trace_add('write', New_Name_Entry_callback)

        self.AboutFrame.F1.left.fl2 = ttk.Frame(self.AboutFrame.F1.left, padding=0)
        self.AboutFrame.F1.left.fl2.pack(anchor='nw', padx=(0, 0), pady=(5, 0))

        def Add_mod_Dependence_callback():
            SettingsValues.Add_mod_Dependence = bool(self.Add_mod_Dependence.get())
            config.set("About.xml", "Add_mod_Dependence", str(SettingsValues.Add_mod_Dependence))
            settings_config_update_write()
            about_example_update()

        self.Add_mod_Dependence = ttk.BooleanVar(value=SettingsValues.Add_mod_Dependence)
        self.AboutFrame.F1.left.fl2.Add_mod_Dependence = ttk.Checkbutton(self.AboutFrame.F1.left.fl2,
                                                                         text=_("Add modDependencies"),
                                                                         variable=self.Add_mod_Dependence,
                                                                         command=Add_mod_Dependence_callback)
        self.AboutFrame.F1.left.fl2.Add_mod_Dependence.pack(anchor=tk.W, pady=(0, 0), side='bottom')

        self.AboutFrame.F2 = ttk.Labelframe(self.AboutFrame, padding=5, text=_("Example About.xml"))
        self.AboutFrame.F2.pack(anchor='nw', expand=True, fill=tk.BOTH, padx=10, pady=(10, 0))
        self.AboutFrame.F2.about_example = ttk.Text(self.AboutFrame.F2, state='disabled')
        self.AboutFrame.F2.about_example.pack(expand=True, fill=tk.BOTH)

        def about_example_update():

            self.AboutFrame.F2.about_example.configure(state='normal')

            text = f'''<ModMetaData>
	<name>{SettingsValues.New_Name.replace("~MOD_NAME~", "Example mod")}</name>
	<author>{SettingsValues.Author}</author>
	<packageId>{SettingsValues.Author}.example1</packageId>
	<supportedVersions>
		<li>1.3</li>
		<li>1.4</li>
	</supportedVersions>
	<modDependencies>{"""
		<li>
			<packageId>example1.example2</packageId>
			<displayName>Example mod</displayName>
			<steamWorkshopUrl>https://steamcommunity.com/sharedfiles/filedetails/?id=0000000000</steamWorkshopUrl>
		</li>""" if SettingsValues.Add_mod_Dependence == True else ""}
	</modDependencies>
	<loadAfter>example1.example2</loadAfter>
	<description>{SettingsValues.Description.replace("~MOD_NAME~", "Example mod")}</description>
</ModMetaData>'''
            self.AboutFrame.F2.about_example.delete(1.0, ttk.END)
            self.AboutFrame.F2.about_example.insert(1.0, text)
            self.AboutFrame.F2.about_example.configure(state='disabled')

        about_example_update()

        # -- Preview SETTINGS FRAME
        # -- ----------------------
        # -- ----------------------
        # -- ----------------------
        # -- ----------------------
        # -- ----------------------
        self.Preview = ttk.Frame(self.Top_Notebook)
        self.Preview.pack(expand=True, fill=tk.BOTH)

        self.Preview.F = ttk.Frame(self.Preview, padding=(10, 10, 10, 10), width=20)
        self.Preview.F.pack(fill=ttk.X, anchor='nw')

        self.Preview.F_left = ttk.Frame(self.Preview.F, )  # text = "FLeft")
        self.Preview.F_left.pack(expand=False, anchor='nw', side='left')

        self.Preview.F_right = ttk.LabelFrame(self.Preview.F, text=_("Image position"))
        self.Preview.F_right.pack(expand=True, fill=ttk.BOTH, anchor='nw', side='right', padx=(100, 250))

        self.Preview.F_right.a1 = ttk.Frame(self.Preview.F_right, width=20, )
        self.Preview.F_right.a1.pack(side='left', fill=ttk.Y)

        self.Preview.F_right.a2 = ttk.Frame(self.Preview.F_right, )
        self.Preview.F_right.a2.pack(expand=True, side='left', fill=ttk.BOTH)

        self.Position = ttk.StringVar(value=SettingsValues.Position)

        self.Preview.R_top = ttk.Frame(self.Preview.F_right.a2, padding=(10, 10, 0, 10))
        self.Preview.R_top.pack(expand=True, fill=ttk.BOTH)

        self.Preview.R_top_1 = ttk.Frame(self.Preview.R_top, )
        self.Preview.R_top_1.pack(side='left', fill=ttk.BOTH, expand=True)
        self.Preview.R_top_2 = ttk.Frame(self.Preview.R_top, )
        self.Preview.R_top_2.pack(side='right', fill=ttk.BOTH, expand=True)

        self.Preview.R_top.TL = ttk.Radiobutton(self.Preview.R_top_1, text=_("Top left"), variable=self.Position,
                                                value='Top left')
        self.Preview.R_top.TL.pack(side="left")
        self.Preview.R_top.TR = ttk.Radiobutton(self.Preview.R_top_2, text=_("Top right"), variable=self.Position,
                                                value='Top right')
        self.Preview.R_top.TR.pack(side="left")

        self.Preview.R_mid = ttk.Frame(self.Preview.F_right.a2, padding=(10, 10, 0, 10))
        self.Preview.R_mid.pack(expand=True, fill=ttk.BOTH, padx=(0, 50), pady=20)
        self.Preview.R_mid.Center = ttk.Radiobutton(self.Preview.R_mid, text=_("Center"), variable=self.Position,
                                                    value='Center')
        self.Preview.R_mid.Center.pack(anchor='center')

        self.Preview.R_bot = ttk.Frame(self.Preview.F_right.a2, padding=(10, 10, 0, 10))
        self.Preview.R_bot.pack(expand=True, fill=ttk.BOTH)

        self.Preview.R_bot_1 = ttk.Frame(self.Preview.R_bot, )
        self.Preview.R_bot_1.pack(side='left', fill=ttk.BOTH, expand=True)
        self.Preview.R_bot_2 = ttk.Frame(self.Preview.R_bot, )
        self.Preview.R_bot_2.pack(side='right', fill=ttk.BOTH, expand=True)

        self.Preview.R_bot.BL = ttk.Radiobutton(self.Preview.R_bot_1, text=_("Bottom left"), variable=self.Position,
                                                value='Bottom left')
        self.Preview.R_bot.BL.pack(side='left', fill=ttk.BOTH, expand=True)
        self.Preview.R_bot.BR = ttk.Radiobutton(self.Preview.R_bot_2, text=_("Bottom right"), variable=self.Position,
                                                value='Bottom right')
        self.Preview.R_bot.BR.pack(side='right', fill=ttk.BOTH, expand=True)

        def Position_callback(*_):
            SettingsValues.Position = self.Position.get()
            config.set("Preview", "Position", SettingsValues.Position)
            settings_config_update_write()
            Preview_image_chage()

        self.Position.trace_add('write', Position_callback)

        def callback_Image_on_Preview():
            SettingsValues.Image_on_Preview = bool(self.Image_on_Preview.get())
            config.set("Preview", "Image_on_Preview", str(SettingsValues.Image_on_Preview))
            settings_config_update_write()
            self.Preview.F_left.F1.Select_img_btn.configure(
                state=('normal' if self.Image_on_Preview.get() else 'disabled'))
            self.Preview.F_left.F2_Offset_x.Entry.configure(
                state=('normal' if self.Image_on_Preview.get() else 'disabled'))
            self.Preview.F_left.F2_Offset_y.Entry.configure(
                state=('normal' if self.Image_on_Preview.get() else 'disabled'))

            self.Preview.R_bot.BL.configure(state=('normal' if self.Image_on_Preview.get() else 'disabled'))
            self.Preview.R_bot.BR.configure(state=('normal' if self.Image_on_Preview.get() else 'disabled'))
            self.Preview.R_mid.Center.configure(state=('normal' if self.Image_on_Preview.get() else 'disabled'))
            self.Preview.R_top.TL.configure(state=('normal' if self.Image_on_Preview.get() else 'disabled'))
            self.Preview.R_top.TR.configure(state=('normal' if self.Image_on_Preview.get() else 'disabled'))
            Preview_image_chage()

        self.Preview.F_left.F1 = ttk.Frame(self.Preview.F_left, padding=(10, 10, 0, 0))
        self.Preview.F_left.F1.pack(expand=False, anchor='nw')

        self.Image_on_Preview = ttk.BooleanVar(value=SettingsValues.Image_on_Preview)
        self.Preview.F_left.F1.Image_on_Preview_checkbox = ttk.Checkbutton(self.Preview.F_left.F1,
                                                                           variable=self.Image_on_Preview,
                                                                           text=_("Add an image to the preview"),
                                                                           command=callback_Image_on_Preview,
                                                                           padding=10)
        self.Preview.F_left.F1.Image_on_Preview_checkbox.pack(side='left')
        self.Preview.F_left.F1.Image_on_Preview_checkbox.ToolTip = ToolTip(
            self.Preview.F_left.F1.Image_on_Preview_checkbox, text=_("Add YOUR image to the original mod preview."))

        def callback_Select_img_btn():
            file = filedialog.askopenfile(filetypes=[('Png Images', '*.png')])
            if file is not None:
                file = file.name.replace('\\', '/')
                if file != r"Images\\Preview\\New_Image.png":
                    shutil.copy(file, r"Images\\Preview\\New_Image.png")

            Preview_image_chage()

        self.Preview.F_left.F1.Select_img_btn = ttk.Button(self.Preview.F_left.F1, text=_("Select Your image"),
                                                           command=lambda: callback_Select_img_btn(), state='disabled')
        self.Preview.F_left.F1.Select_img_btn.pack(padx=10, pady=10, side='left')
        self.Preview.F_left.F1.Select_img_btn.configure(state=('normal' if self.Image_on_Preview.get() else 'disabled'))

        self.Preview.F_left.F2 = ttk.Frame(self.Preview.F_left, padding=(20, 5, 0, 0))
        self.Preview.F_left.F2.pack(expand=False, anchor='nw')

        self.Preview.F_left.F2_Offset_x = ttk.Frame(self.Preview.F_left.F2, padding=(0, 0, 0, 0))
        self.Preview.F_left.F2_Offset_x.pack(expand=False, anchor='nw', side='left')

        self.Preview.F_left.F2_Offset_x.Label = ttk.Label(self.Preview.F_left.F2_Offset_x, text=_("x Offset"))
        self.Preview.F_left.F2_Offset_x.Label.pack(side='top')

        def Numeric_str(P):
            if str.isdigit(P) or P == "":
                return True
            else:
                return False

        numeric_validate = (self.register(Numeric_str))

        self.Offset_x = ttk.StringVar(value=str(SettingsValues.Offset_x))

        def Offset_callback(*_):
            if self.Offset_x.get() == '':
                SettingsValues.Offset_x = 0
            else:
                SettingsValues.Offset_x = int(self.Offset_x.get())

            if self.Offset_y.get() == '':
                SettingsValues.Offset_y = 0
            else:
                SettingsValues.Offset_y = int(self.Offset_y.get())

            config.set("Preview", "Offset_x", str(SettingsValues.Offset_x))
            config.set("Preview", "Offset_y", str(SettingsValues.Offset_y))
            settings_config_update_write()
            Preview_image_chage()

        self.Offset_x.trace_add('write', Offset_callback)

        self.Preview.F_left.F2_Offset_x.Entry = ttk.Entry(self.Preview.F_left.F2_Offset_x, textvariable=self.Offset_x,
                                                          validate='key', validatecommand=(numeric_validate, '%P'))
        self.Preview.F_left.F2_Offset_x.Entry.pack(side='bottom')

        self.Preview.F_left.F2_Offset_y = ttk.Frame(self.Preview.F_left.F2, padding=(10, 0, 0, 0))
        self.Preview.F_left.F2_Offset_y.pack(expand=False, anchor='nw', side='left')

        self.Preview.F_left.F2_Offset_y.Label = ttk.Label(self.Preview.F_left.F2_Offset_y, text=_("y Offset"))
        self.Preview.F_left.F2_Offset_y.Label.pack(side='top')

        self.Offset_y = ttk.StringVar(value=str(SettingsValues.Offset_y))
        self.Offset_y.trace_add('write', Offset_callback)

        self.Preview.F_left.F2_Offset_y.Entry = ttk.Entry(self.Preview.F_left.F2_Offset_y, textvariable=self.Offset_y)
        self.Preview.F_left.F2_Offset_y.Entry.pack(side='bottom')

        self.Preview.F_left.F2_Offset_x.Entry.configure(state=('normal' if self.Image_on_Preview.get() else 'disabled'))
        self.Preview.F_left.F2_Offset_y.Entry.configure(state=('normal' if self.Image_on_Preview.get() else 'disabled'))

        self.Preview.F_last = ttk.Frame(self.Preview, padding=(10, 10, 0, 0))
        self.Preview.F_last.pack(expand=True, fill=tk.BOTH, side='bottom')

        self.Preview.F_last.image = PhotoImage(file='Images/Preview/Preview_origianl.png')
        self.Preview.F_last.Label_image = ttk.Label(self.Preview.F_last, image=self.Preview.F_last.image)
        self.Preview.F_last.Label_image.pack()

        def Preview_image_chage():

            if self.Image_on_Preview.get():

                image_edit.add_custom_labe_on_preview(r"Images\\Preview\\Preview_origianl.png",
                                                      r"Images\\Preview\\New_Image.png",
                                                      self.Position.get(), SettingsValues.Offset_x,
                                                      SettingsValues.Offset_y).save(
                    r'Images\\Preview\\Preview_updated.png')

                self.Preview_image_updated = PhotoImage(file=r'Images\\Preview\\Preview_updated.png')

                self.Preview.F_last.Label_image.config(image=self.Preview_image_updated)
            else:
                self.Preview.F_last.Label_image.config(image=self.Preview.F_last.image)

        Preview_image_chage()

        # -- Advanced SETTINGS FRAME
        # -- ----------------------
        # -- ----------------------
        # -- ----------------------
        # -- ----------------------
        # -- ----------------------
        self.Advanced_Frame = ttk.Frame(self.Top_Notebook)
        self.Advanced_Frame.pack(fill=tk.BOTH)

        self.af = ttk.Frame(self.Advanced_Frame, padding=(10, 10, 10, 10))
        self.af.pack(expand=True, fill=ttk.BOTH)

        self.af.top = ttk.Frame(self.af)
        self.af.top.pack(fill=ttk.X)

        self.af.top.left = ttk.LabelFrame(self.af.top, text=_("Tags for extraction"))
        self.af.top.left.pack(expand=True, fill=ttk.BOTH, side='left', padx=(0, 5))

        self.af.top.left.btn1 = ttk.Button(self.af.top.left, text=_("Tags to extraction"),
                                           command=lambda: os.startfile(SettingsPath.Tags_to_extraction))
        self.af.top.left.btn1.pack(padx=10, pady=10)
        self.af.top.left.btn1.tooltip = ToolTip(self.af.top.left.btn1, wraplength=1000, text=_(
            '<Tags> to be extracted for translation, for example, if you want to extract "anima heart" from \n'
            '<label>anima heart</label>,\n'
            'then the list of tags to extract should be "label"'))

        self.af.top.left.btn2 = ttk.Button(self.af.top.left, text=_("Part of tag to extraction"),
                                           command=lambda: os.startfile(SettingsPath.Part_of_tag_to_extraction))
        self.af.top.left.btn2.pack(padx=10, pady=10)
        self.af.top.left.btn2.tooltip = ToolTip(self.af.top.left.btn2, wraplength=1000, text=_(
            'If you need to extract all <tags> that have a common part, for example, all <tags> with "Message". Such as:\n'
            '<NewMessage>Hello</NewMessage>\n'
            '<OldMessage>Hello</OldMessage>\n'
            '<Message1>Hello</Message1>\n'
            'Case-sensitive'))

        self.af.top.left.btn3 = ttk.Button(self.af.top.left, text=_("Tags before <li>"),
                                           command=lambda: os.startfile(SettingsPath.Tags_before_li))
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
                                            command=lambda: os.startfile(SettingsPath.Forbidden_tag))
        self.af.top.right.btn1.pack(padx=10, pady=10)
        self.af.top.right.btn1.tooltip = ToolTip(self.af.top.right.btn1, wraplength=1000, text=_(
            "<Tags> that will not be extracted. Usually you don't need to add much here, but if the program constantly extracts something superfluous, then it makes sense to prohibit the extraction of the tag in any way\n"
            "The first way is to prohibit the extraction of this particular <Tag>. "
            "In this case, those tags that completely match the list will not be extracted.\n"
            "For example <developmentalStageFilter>Baby, Child, Adult</developmentalStageFilter>\n"
            "Because this line is very similar to normal text, which it would be desirable to extract because there are spaces in it, <tag> should be banned."))

        self.af.top.right.btn2 = ttk.Button(self.af.top.right, text=_("Forbidden part of tag"),
                                            command=lambda: os.startfile(SettingsPath.Forbidden_part_of_tag))
        self.af.top.right.btn2.pack(padx=10, pady=10)
        self.af.top.right.btn2.tooltip = ToolTip(self.af.top.right.btn2, wraplength=1000, text=_(
            'If you need to prohibit extraction of all <tags> that have a common part,'
            ' for example, all <tags> with "Texture". Such as:\n'
            '<Texture>Texture1.png</Texture>\n'
            '<Old_Texture>Texture2.png</Old_Texture>\n'
            '<MetalTexture>Texture3.png</MetalTexture>\n'
            'Case-sensitive'))

        self.af.top.right.btn3 = ttk.Button(self.af.top.right, text=_("Forbidden part of path"),
                                            command=lambda: os.startfile(SettingsPath.Forbidden_part_of_path))
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
                                            command=lambda: os.startfile(SettingsPath.Forbidden_text))
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
                                            command=lambda: os.startfile(SettingsPath.Li_Class_Replace))
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

        self.af.top2.left.btn2 = ttk.Button(self.af.top2.left, text=_("Folders to search"),
                                            command=lambda: os.startfile(SettingsPath.Folders_to_search))
        self.af.top2.left.btn2.pack(padx=10, pady=10)
        self.af.top2.left.btn2.tooltip = ToolTip(self.af.top2.left.btn2, wraplength=800, text=_(
            'Folders in which the program will search for folders with the extracted text. In 1.4,\n'
            'there is only one such folder (not counting folders with the version number) this is "Common".\n'
            '"\\" added so that the game searches for folders in the root folder of the mod (do not delete it)'))

        self.Top_Notebook.add(self.General_Settings_frame, text=_('General Settings'))
        self.Top_Notebook.add(self.CommFrame, text=_('Comments'))
        self.Top_Notebook.add(self.GrabFrame, text=_('Grabbing'))
        self.Top_Notebook.add(self.AboutFrame, text=_('About.xml'))
        self.Top_Notebook.add(self.Preview, text=_('Preview'))
        self.Top_Notebook.add(self.Advanced_Frame, text=_('Advanced settings'))

        self.after(1, lambda: self.Top_Notebook.focus_set())
        self.Top_Notebook.select(0)

        self.geometry("1000x800+200+200")

    def start_move(self, event):
        """ change the (x, y) coordinate on mousebutton press and hold motion """
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        """ when mouse button is released set the (x, y) coordinates to None """
        self.x = None
        self.y = None

    def do_move(self, event):
        try:
            """ function to move the window """
            self.wm_state('normal')  # if window is maximized, set it to normal (or resizable)
            if not self.x or not self.y:
                return
            deltax = event.x - (self.x if self.x else 0)
            deltay = event.y - (self.y if self.y else 0)
            x = self.winfo_x() + deltax
            y = self.winfo_y() + deltay
            self.geometry(f"+{x}+{y}")
        except Exception as ex:
            return

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


def set_appwindow(root):
    GWL_EXSTYLE = -20
    WS_EX_APPWINDOW = 0x00040000
    WS_EX_TOOLWINDOW = 0x00000080
    hwnd = windll.user32.GetParent(root.winfo_id())
    style = windll.user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)
    style = style & ~WS_EX_TOOLWINDOW
    style = style | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongPtrW(hwnd, GWL_EXSTYLE, style)
    root.wm_withdraw()
    root.after(10, lambda: root.wm_deiconify())


def restart_app(r=None):
    if r:
        r.destroy()

    r = TestApp(hidden_window)

    r.overrideredirect(True)
    r.after(10, lambda: set_appwindow(root=r))

    r.mainloop()


hidden_window = ttk.Window
app = ttk.Window


def exit_app():
    hidden_window.destroy()

    if language_changed:
        app.destroy()
    else:
        app.deiconify()


def main_from_prog(window, app_original):
    global hidden_window
    global app
    app = app_original
    hidden_window = window
    hidden_window.withdraw()

    restart_app()


def read_txt_settings(path):
    a = []
    with open(path, encoding="utf8") as tag_file:
        for line in tag_file:
            a.append(line.strip("\n "))
    return a


def get_settings_pack():
    settings_config_read(app)
    Tags_to_extraction = read_txt_settings(SettingsPath.Tags_to_extraction)
    Part_of_tag_to_extraction = read_txt_settings(SettingsPath.Part_of_tag_to_extraction)
    Forbidden_tag = read_txt_settings(SettingsPath.Forbidden_tag)
    Forbidden_tag = [a.lower() for a in Forbidden_tag]
    Forbidden_part_of_tag = read_txt_settings(SettingsPath.Forbidden_part_of_tag)
    Forbidden_part_of_path = read_txt_settings(SettingsPath.Forbidden_part_of_path)
    Forbidden_text = read_txt_settings(SettingsPath.Forbidden_text)
    a = read_txt_settings(SettingsPath.Li_Class_Replace)
    Li_Class_Replace = []
    for _ in a:
        Li_Class_Replace.append(_.split("=",1))

    Folders_to_search = read_txt_settings(SettingsPath.Folders_to_search)
    Tags_before_li = read_txt_settings(SettingsPath.Tags_before_li)

    list_pawn_tag = []
    if SettingsValues.labelPlural == True:
        list_pawn_tag.append('labelPlural')
    if SettingsValues.labelMale == True:
        list_pawn_tag.append('labelMale')
    if SettingsValues.labelFemale == True:
        list_pawn_tag.append('labelFemale')
    if SettingsValues.labelMalePlural == True:
        list_pawn_tag.append('labelMalePlural')
    if SettingsValues.labelFemalePlural == True:
        list_pawn_tag.append('labelFemalePlural')
    Settings_pack = [  # [General]
        SettingsValues.Settings_language,
        SettingsValues.Game_language,
        SettingsValues.Path_to_Data, SettingsValues.Path_to_Mod_folder, SettingsValues.Path_to_Another_folder,
        SettingsValues.Delete_old_versions_translation, SettingsValues.Merge_folders, SettingsValues.Not_rename_files,
        #   [Comments]
        SettingsValues.Add_filename_comment, SettingsValues.Add_comment, SettingsValues.Comment_add_EN,
        SettingsValues.Comment_starting_similar_as_ogiganal_text, SettingsValues.Comment_spacing_before_tag, SettingsValues.Comment_replace_n_as_new_line,
        #  [Grabbing]
        SettingsValues.Add_stuffAdjective_and_mark_it, SettingsValues.Add_stuffAdjective_and_mark_it_text,
        SettingsValues.Check_at_least_one_letter_in_text, SettingsValues.add_titleFemale, SettingsValues.add_titleShortFemale,
        SettingsValues.Tkey_system_on,
        SettingsValues.tags_left_spacing, SettingsValues.Add_new_line_next_defname,
        list_pawn_tag,
        #  [About.xml]
        SettingsValues.Author, SettingsValues.New_Name, SettingsValues.Add_mod_Dependence, SettingsValues.Description,
        #  [Preview]
        SettingsValues.Image_on_Preview, SettingsValues.Position, SettingsValues.Offset_x, SettingsValues.Offset_y,

        #  [Tags]
        Tags_to_extraction, Part_of_tag_to_extraction, Tags_before_li,
        Forbidden_tag, Forbidden_part_of_tag, Forbidden_part_of_path, Forbidden_text,
        Li_Class_Replace, Folders_to_search,
    ]
    return Settings_pack


if __name__ == '__main__':
    app = ttk.Window(title="Main app")
    hidden_window = ttk.Toplevel(master=app, title="Hidden window")

    main_from_prog(hidden_window, app)
    app.mainloop()
    get_settings_pack()


# pybabel extract -o locale/T_test.pot Text_grabber_settings.py
# pybabel init -D T_test -i locale/T_test.pot -d po -l ru
# pybabel init -D T_test -i locale/T_test.pot -d po -l en
# pybabel update -D T_test -i locale/T_test.pot -d po -l ru
# pybabel update -D T_test -i locale/T_test.pot -d po -l en
# pybabel compile -D T_test -i locale\ru\LC_MESSAGES\T_test.po -o locale\ru\LC_MESSAGES\T_test.mo
# pybabel compile -D T_test -i locale\en\LC_MESSAGES\T_test.po -o locale\en\LC_MESSAGES\T_test.mo
