# GlobVars.py — Глобальное состояние приложения Text_grabber

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Tuple, List, Any


Error_log = []


@dataclass
class QueueData:
    """Данные для передачи между потоками и GUI."""
    new_fullpath: str = ""
    """change_to_mod_dir Путь, который нужно установить как текущую папку мода."""

@dataclass
class ModData:
    """Метаданные парсинга мода из About.xml и PublishedFileId.txt."""
    name: str = "Default name"
    package_id: str = "default.id"
    author: str = "Default Author"
    url: str = ""
    supported_versions: str = ""
    description: str = "Default description"

    mod_dependencies: Dict[str, str] = field(default_factory=dict)
    """Словарь зависимостей мода: {packageId: displayName}."""
    loadafter_list: List[str] = field(default_factory=list)

    max_version: str = "v1.5"
    max_version_by_folders: str = "0.1"
    max_version_by_Loadfolders: str = "v0.1"



@dataclass
class AppState:
    error_log: List[Any] = field(default_factory=list)
    prog = Path.cwd()

    new_loadfolder_pathes: List[Path] = field(default_factory=list)
    """<li>...</li>\n\t\t"""


    # Словарь всех модов и их папок:
    #   { (required_mod, ...): { Path: [text1, text2, ...] } }
    mods_folders: Dict[Tuple[str, ...], Dict[Path, List[str]]] = field(default_factory=dict)
    """
    -----{
    -----(req mods): 
    ---------{Path:
    ------------text1, text2]
    ---------}
    -----}
    """

    keyed_from_patches: Dict[Path, List[str]] = field(default_factory=dict)


@dataclass
class FolderData:
    """Результаты сканирования файловой структуры мода."""
    searching_pathes: Dict[Path, Tuple[str, ...]] = field(default_factory=dict)
    def_folders: List[Path] = field(default_factory=list)
    lang_folders: List[Path] = field(default_factory=list)

    patches_folders: Dict[Path, Tuple[str, ...]] = field(default_factory=dict)
    """path -> (required mods...)"""

    keyed_folders: List[Path] = field(default_factory=list)
    strings_folders: List[Path] = field(default_factory=list)

    patches_defs: Dict[Path, Path] = field(default_factory=dict)
    patches_pathes: Dict[Path, Path] = field(default_factory=dict)






@dataclass
class TranslatingFiles:




    """Маппинг файлов Defs/Keyed/Strings и список родителей."""
    defs: Dict[Path, Path] = field(default_factory=dict)
    keyed: Dict[Path, Path] = field(default_factory=dict)
    strings: Dict[Path, Path] = field(default_factory=dict)

    parent_list: Dict[str, list] = field(default_factory=dict)
    """par_list[name] = list(Elements)
    Словарь родителей: {name: [Element, ...]}.
    Тип Element — lxml.etree._Element, но указан как list для избежания
    тяжёлого импорта lxml при каждом обращении к GlobVars."""




state: AppState = AppState()
mod_data: ModData = ModData()
folders: FolderData = FolderData()
tf: TranslatingFiles = TranslatingFiles()
queue_data: QueueData = QueueData()
