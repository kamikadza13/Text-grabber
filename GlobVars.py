# GlobVars.py
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple, List

from lxml import etree


@dataclass
class ModData:
    name = "Default name"
    packageId = "default.id"
    author = 'Default Autor'
    url = ''
    supportedVersions = ''
    description = 'Default description'

    modDependencies: dict
    """dependence_dict[packageId]=
               {'displayName': displayName,
                'steamWorkshopUrl': steamWorkshopUrl,
                'downloadUrl': downloadUrl,
                'steamID': steamID}"""

    max_version = 'v1.5'
    max_version_by_folders = '0.1'
    max_version_by_Loadfolders = 'v0.1'


@dataclass
class AppState:
    exit_string: list = None
    current_folder: str = ""
    error_log: list = None
    parent_names: list = None

    prog = Path.cwd()

    new_loadfolder_pathes: list = None
    f'<li>...</li>\n\t\t'

    mods_folders: Dict[Tuple, Dict[Path, List[str]]] = None
    '''
    -----{
    -----(req mods): 
    ---------{Path:
    ------------text1, text2]
    ---------}
    -----}
    '''

    keyed_from_patches: dict[Path, list[str]] = None


    def __post_init__(self):
        # Инициализируем списки при создании
        self.exit_string = []
        self.error_log = []
        self.parent_names = []
        self.new_loadfolder_pathes = []

        self.mods_folders = {}
        '''
        -----{
        -----(req mods): 
        ---------{Path:
        ------------text1, text2]
        ---------}
        -----}
        '''

        self.keyed_from_patches = {}





@dataclass
class SsS:
    p_full = Path()
    p_root = Path()
    p_name = Path()


@dataclass
class A1:
    searching_pathes: dict[Path, Tuple] = None

    def_folders: list[Path] = None
    lang_folders: list[Path] = None
    patches_folders: dict[Path, Tuple] = None
    'path , (required mods...)'

    keyed_folders: list[Path] = None
    strings_folders: list[Path] = None

    patches_defs: dict[Path, Path] = None
    patches_pathes: dict[Path, Path] = None



    def __post_init__(self):
        # Инициализируем списки при создании
        self.searching_pathes = {}

        self.def_folders = []
        self.lang_folders = []
        self.patches_folders = {}

        self.keyed_folders = []
        self.strings_folders = []



        self.patches_defs = {}
        self.patches_pathes = {}







@dataclass
class TranslatingFiles:
    Defs: dict[Path, Path] = None
    Keyed: dict[Path, Path] = None
    Strings: dict[Path, Path] = None

    Parent_list: dict[str, list[etree.Element]] = None
    '''par_list[name] = list(Elements)'''




    def __post_init__(self):
        self.Defs = {}
        self.Keyed = {}
        self.Strings = {}


        self.Parent_list = {}


state = AppState()
mod_data = ModData(modDependencies={})
SS = SsS()
folders = A1()
tf = TranslatingFiles()


