import configparser
import os.path
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import List, Any, Dict

import appdirs


@dataclass
class SettingsValues:
    class SettingsPath:
        Prog_name = 'Text_grabber'

        SettingsPath_AppData = Path(appdirs.user_config_dir(Prog_name, appauthor=False, roaming=True))
        r'''C:\Users\Kamikadza13\AppData\Roaming\Text_grabber'''


        General_settings_path = Path('Settings') / 'A1_Settings.ini'
        Description = Path('Settings') / 'A2_Description.txt'
        tags_left_spacing = Path('Settings') / 'A3_Tags_left_spacing.txt'

        # Extraction
        Tags_to_extraction = Path('Settings') / 'E1_Tags_to_extraction.txt'

        Part_of_tag_to_extraction = Path('Settings') / 'E2_Part_of_tag_to_extraction.txt'
        Tags_before_li = Path('Settings') / 'E3_Tag_before_li.txt'
        # Forbidden
        Forbidden_tag = Path('Settings') / 'F1_Forbidden_tags.txt'
        Forbidden_part_of_tag = Path('Settings') / 'F2_Forbidden_part_of_tag.txt'
        Forbidden_part_of_path = Path('Settings') / 'F3_Forbidden_part_of_path.txt'
        Forbidden_text = Path('Settings') / 'F4_Forbidden_text.txt'
        # Other
        Li_Class_Replace = Path('Settings') / 'O1_Li_Class_Replace.txt'


        A2_Description = '''Перевод ~MOD_NAME~

~MOD_DESCRIPTION~
~MOD_URL~

Если вы заметили что-то не переведенное, то напишите об этом в комментариях под переводом ^_^

Также мой перевод кучи мелких QOL модов
QOL rus
https://steamcommunity.com/sharedfiles/filedetails/?id=2791163039
(зайдите посмотрите, там много вкусного)'''
        A3_Tags_left_spacing = "\t"

        E1_Tags_to_extraction = '''label
labelNoun
labelPlural
text
description
jobString
desc
customLabel
customLetterLabel
customLetterText
ingestCommandString
ingestReportString
outOfFuelMessage
name
summary
pawnSingular
pawnsPlural
adjective
ideoName
member
theme
reportString
stuffAdjective
deathMessage
letterText
slateRef
text
title
titleshort
verb
commandDesc
commandLabel
baseInspectLine
leaderTitle
structureLabel'''
        E2_Part_of_tag_to_extraction = '''Message
Label
label
Title
Text
gerund
Gerund
Explanation
title
description'''
        E3_Tag_before_li = '''rulesStrings
rulesFiles
customLetterText'''

        F1_Forbidden_tags = '''defaultLabelColor
thingClass
only
developmentalStageFilter
context
count
value
offset
volume
drawSize
wornGraphicPath
labelKey
messageTypeDef
texturePath
explanationKeyAbstract
texture
allowedDevelopmentalStages'''
        F2_Forbidden_part_of_tag = '''Texture
colorChannels
foodType
showMessageIfOwned
labelUsedInLogging
texPath
developmentalStageFilter'''
        F3_Forbidden_part_of_path = '''colorChannels
shadowData'''
        F4_Forbidden_text = '''True
False
true
false
asker
askerIsNull
siteThreatChance
Mote
mote'''

        O1_Li_Class_Replace = '''QuestNode_=
ScenPart_='''


    #   [General]
    Settings_language: str = 'en'
    Game_language: str = 'Russian'

    Path_to_Data: str | None = None
    Path_to_Mod_folder: str | None = None
    Path_to_Another_folder: str | None = None

    Delete_old_versions_translation: bool = True
    Merge_folders: bool = True
    Not_rename_files: bool = False

    Copy_original_patches: bool = False
    Check_update: bool = True

    Adding_xml_version_encoding_string_ckeckbtn: bool = False

    Adding_xml_version_encoding_string_in_Keyed: bool = True

    Translate_tools_into_russian: bool = True

    #   [Comments]
    Add_filename_comment: bool = True
    Add_comment: bool = True
    Comment_add_EN: bool = True
    Comment_starting_similar_as_ogiganal_text: bool = True
    Comment_spacing_before_tag: bool = False
    Comment_replace_n_as_new_line: bool = True

    #  [Grabbing]
    Add_stuffAdjective_and_mark_it: bool = True
    Add_stuffAdjective_and_mark_it_text: str = 'Adjective ~LABEL~'

    Check_at_least_one_letter_in_text: bool = False
    add_titleFemale: bool = True
    add_titleShortFemale: bool = True


    tags_left_spacing: str = 'tab'
    tags_left_spacing_dict = {'tab': '\t',
                              'space0': '',
                              'space2': '  ',
                              'space4': '    ',
                              }

    labelPlural: bool = True
    labelMale: bool = False
    labelFemale: bool = False
    labelMalePlural: bool = False
    labelFemalePlural: bool = False

    def get_plural_list(self):
        listt = []
        if self.labelPlural:
            listt.append('labelPlural')
        if self.labelMale:
            listt.append('labelMale')
        if self.labelFemale:
            listt.append('labelFemale')
        if self.labelMalePlural:
            listt.append('labelMalePlural')
        if self.labelFemalePlural:
            listt.append('labelFemalePlural')
        return listt

    Add_new_line_next_defname: bool = True
    Add_new_line_next_defname_treshhold: bool = True

    Tkey_system_on: bool = True





    #  [About.xml]
    Author: str = 'Kamikadza13'
    New_Name: str = '~MOD_NAME~ rus'
    Add_mod_Dependence: bool = True
    Description: str = '' # A2_Description.txt

    #  [Preview]
    Image_on_Preview: bool = True
    Preview_Position: str = 'Top right'
    Preview_Offset_x: int = 0
    Preview_Offset_y: int = 0

    # [Other]

    Tags_to_extraction = []
    Part_of_tag_to_extraction = []
    Tags_before_li = []

    Forbidden_tag = []
    Forbidden_part_of_tag = []
    Forbidden_part_of_path = []
    Forbidden_text = []

    Li_Class_Replace = []


    section_defaults = {
        'General': {
            # Extraction
            'Settings_language': 'en',
            'Game_language': 'Russian',
            'Path_to_Data': None,
            'Path_to_Mod_folder': None,
            'Path_to_Another_folder': None,
            'Delete_old_versions_translation': True,
            'Merge_folders': True,
            'Not_rename_files': False,
            'Copy_original_patches': False,
            # Other
            'Check_update': True,
            'Adding_xml_version_encoding_string_ckeckbtn': False,
            'Adding_xml_version_encoding_string_in_Keyed': True,
            'Translate_tools_into_russian': True,

        },
        'Comment': {
            'Add_filename_comment': True,
            'Add_comment': True,
            'Comment_add_EN': True,
            'Comment_starting_similar_as_ogiganal_text': True,
            'Comment_spacing_before_tag': False,
            'Comment_replace_n_as_new_line': False,
        },
        'Grabbing': {
            'Check_at_least_one_letter_in_text': True,
            'add_titleFemale': True,
            'add_titleShortFemale': True,
            'labelPlural': True,
            'labelMale': False,
            'labelFemale': False,
            'labelMalePlural': False,
            'labelFemalePlural': False,
            'Add_stuffAdjective_and_mark_it': True,
            'Add_stuffAdjective_and_mark_it_text': 'Adjective ~LABEL~',
            'tags_left_spacing': 'tab',
            'Add_new_line_next_defname': True,
            'Add_new_line_next_defname_treshhold': True,
            'Tkey_system_on': True,
        },
        'About.xml': {
            'Author': 'Kamikadza13',
            'New_Name': '~MOD_NAME~ rus',
            'Add_mod_Dependence': True,
        },
        'Preview': {
            'Image_on_Preview': True,
            'Preview_Position': 'Top right',
            'Preview_Offset_x': 0,
            'Preview_Offset_y': 0,
        },
    }

    section_config = configparser.RawConfigParser(allow_no_value=False)
    section_config.optionxform = str

    def get(self, name):
        return getattr(self, name)


    def set(self, name, value):
        print(f'Set {name} - {value}')
        if not hasattr(self, name):
            raise Exception
        setattr(self, name, value)

        for section in self.section_config.sections():
            if self.section_config.has_option(section, name):
                self.section_config.set(section, name, value)
        self.write()
        return

        # Перебираем все существующие секции


    def write(self):
        with open(self.SettingsPath.SettingsPath_AppData / self.SettingsPath.General_settings_path, 'w', encoding='utf-8') as aaa:
            SettingsValues.section_config.write(aaa)

class SettingsLoader:
    def __init__(self, config_path: Path, SV: SettingsValues):
        self.config_path = config_path
        self.SV = SV
        self.config = configparser.RawConfigParser()
        self.config.optionxform = str
        self.config.read(self.config_path)


        self.not_founded_values_dict = {}

        # Дефолтные значения для секций


    def get_value(self, section: str, option: str, default_val) -> Any:
        """Универсальный метод для получения значений"""
        try:
            if isinstance(default_val, bool):
                return self.config.getboolean(section, option)
            if isinstance(default_val, int):
                return self.config.getint(section, option)
            if isinstance(default_val, float):
                return self.config.getfloat(section, option)
            if isinstance(default_val, str):
                return self.config.get(section, option)
            match option:
                case 'Path_to_Data' | 'Path_to_Mod_folder' | 'Path_to_Another_folder':
                    return str(Path(self.config.get(section, option)))
                case _:
                    return self.config.get(section, option)

        except (configparser.NoSectionError, configparser.NoOptionError):
            default_value = self.SV.section_defaults.get(section, {}).get(option)
            if default_value is None:
                default_value = self.SV.get(option)
            self.not_founded_values_dict[section,option] = default_value
            print(f"Not found option -> Restore default value {option}={default_value}")
            return default_value

    def load_file_content(self, file_path: Path, default_content: str, strip=True) -> str | None:
        """Загрузка содержимого файла с созданием дефолтного при отсутствии"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if strip:
                    return f.read().strip()
                else:
                    return f.read()
        except FileNotFoundError:

            file_path.parent.mkdir(parents=True, exist_ok=True)
            self.Errors.append(f"Not found option -> Restore default value: {file_path.name} '{default_content}'")
            # print(f"Not found option -> Restore default value: {file_path.name} '{default_content}'")

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(default_content)
            return default_content
        except Exception as e:
            self.Errors.append(f"Error reading {file_path}: {str(e)}")

            print(f"Error reading {file_path}: {str(e)}")
            return default_content

    def load_list_from_file(self, file_path: Path, default_content: str,
                          processor: callable = lambda x: x) -> List[str]:
        """Загрузка списка из файла"""
        content = self.load_file_content(file_path, default_content)
        return [processor(line.strip()) for line in content.splitlines() if line.strip()]


    @cached_property
    def settings(self) -> Dict[str, Any]:
        result = {}
        for section, defaults in self.SV.section_defaults.items():
            result[section] = {}
            for key, default_val in defaults.items():
                result[section][key] = self.get_value(section, key, default_val)
        return result

    @cached_property
    def text_or_list_of_string_settings(self):
        r = {}


        r['Description'] = self.load_file_content(
            self.SV.SettingsPath.Description,
            self.SV.SettingsPath.A2_Description, strip=False)

        r['Tags_to_extraction'] = self.load_list_from_file(
            self.SV.SettingsPath.Tags_to_extraction,
            self.SV.SettingsPath.E1_Tags_to_extraction,
            str.lower
        )

        r['Part_of_tag_to_extraction'] = self.load_list_from_file(
            self.SV.SettingsPath.Part_of_tag_to_extraction,
            self.SV.SettingsPath.E2_Part_of_tag_to_extraction,
            str.lower
        )

        r['Tags_before_li'] = self.load_list_from_file(
            self.SV.SettingsPath.Tags_before_li,
            self.SV.SettingsPath.E3_Tag_before_li,
            str.lower
        )

        r['Forbidden_tag'] = self.load_list_from_file(
            self.SV.SettingsPath.Forbidden_tag,
            self.SV.SettingsPath.F1_Forbidden_tags,
            str.lower
        )

        r['Forbidden_part_of_tag'] = self.load_list_from_file(
            self.SV.SettingsPath.Forbidden_part_of_tag,
            self.SV.SettingsPath.F2_Forbidden_part_of_tag,
            str.lower
        )

        r['Forbidden_part_of_path'] = self.load_list_from_file(
            self.SV.SettingsPath.Forbidden_part_of_path,
            self.SV.SettingsPath.F3_Forbidden_part_of_path,
            str.lower
        )

        r['Forbidden_text'] = self.load_list_from_file(
            self.SV.SettingsPath.Forbidden_text,
            self.SV.SettingsPath.F4_Forbidden_text,
            str.lower
        )

        r['Li_Class_Replace'] = self.load_list_from_file(
            self.SV.SettingsPath.Li_Class_Replace,
            self.SV.SettingsPath.O1_Li_Class_Replace,
            str.lower
        )
        return r

    Errors = []

def get_config_values(SV: SettingsValues):
    cur_dir = Path.cwd()
    script_dir = Path(appdirs.user_config_dir('Text_grabber', appauthor=False, roaming=True))
    os.chdir(script_dir)
    loader = SettingsLoader(config_path=SV.SettingsPath.General_settings_path, SV=SV)

    for section, sec_dict in loader.settings.items():
        for key, value in sec_dict.items():
            setattr(SV, key, value)


    for key, value in loader.text_or_list_of_string_settings.items():
        setattr(SV, key, value)


    for secstin, diction in loader.settings.items():
        SV.section_config.add_section(secstin)
        for key, value in diction.items():
            SV.section_config.set(section=secstin, option=key, value=SV.get(key))

    SV.write()

    os.chdir(cur_dir)


print('Settings module')
SVV = SettingsValues()
get_config_values(SVV)


