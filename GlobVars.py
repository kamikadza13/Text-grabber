# GlobVars.py
import dataclasses
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

    modDependencies: dict = dataclasses.field(default_factory=dict)
    """dependence_dict[packageId]=
               {'displayName': displayName,
                'steamWorkshopUrl': steamWorkshopUrl,
                'downloadUrl': downloadUrl,
                'steamID': steamID}"""
    loadafter_list: list = dataclasses.field(default_factory=list)
    max_version = 'v1.5'
    max_version_by_folders = '0.1'
    max_version_by_Loadfolders = 'v0.1'


@dataclass
class AppState:
    exit_string: list = dataclasses.field(default_factory=list)
    current_folder: str = ""
    error_log: list = dataclasses.field(default_factory=list)
    parent_names: list = dataclasses.field(default_factory=list)

    prog = Path.cwd()

    new_loadfolder_pathes: list = dataclasses.field(default_factory=list)
    f'<li>...</li>\n\t\t'

    mods_folders: Dict[Tuple, Dict[Path, List[str]]] = dataclasses.field(default_factory=dict)
    '''
    -----{
    -----(req mods): 
    ---------{Path:
    ------------text1, text2]
    ---------}
    -----}
    '''

    keyed_from_patches: dict[Path, list[str]] = dataclasses.field(default_factory=dict)


@dataclass
class A1:
    searching_pathes: dict[Path, Tuple] = dataclasses.field(default_factory=dict)

    def_folders: list[Path] = dataclasses.field(default_factory=list)
    lang_folders: list[Path] = dataclasses.field(default_factory=list)
    patches_folders: dict[Path, Tuple] = dataclasses.field(default_factory=dict)
    'path , (required mods...)'

    keyed_folders: list[Path] = dataclasses.field(default_factory=list)
    strings_folders: list[Path] = dataclasses.field(default_factory=list)

    patches_defs: dict[Path, Path] = dataclasses.field(default_factory=dict)
    patches_pathes: dict[Path, Path] = dataclasses.field(default_factory=dict)






@dataclass
class TranslatingFiles:
    Defs: dict[Path, Path] = dataclasses.field(default_factory=dict)
    Keyed: dict[Path, Path] = dataclasses.field(default_factory=dict)
    Strings: dict[Path, Path] = dataclasses.field(default_factory=dict)

    Parent_list: dict[str, list[etree.Element]] = dataclasses.field(default_factory=dict)
    '''par_list[name] = list(Elements)'''



state = AppState()
mod_data = ModData()
folders = A1()
tf = TranslatingFiles()


