from pathlib import Path
from typing import List

from lxml import etree as etree
from lxml.etree import _Element

from GlobFunc import error_handler, xml_get_text, no_comment_parser
from GlobVars import mod_data


@error_handler(default='', error_text='Reading PublishedFileId.txt error')
def get_steam_id_PublishedFileId() -> str:
    path = Path('About') / 'PublishedFileId.txt'
    with open(path, 'r') as PublishedFileId:
        steam_id = str(PublishedFileId.read())
    return 'https:/steamcommunity.com/sharedfiles/filedetails/?id=' + steam_id

def get_supportedVersions(root3):
    _ = root3.find("supportedVersions")
    b = ''
    max_ver: str = '1.6'

    if _ is not None:
        b = '\n'
        for a in _:
            cur_ver = a.text
            if cur_ver > max_ver:
                max_ver = cur_ver
            b += f'\t\t<li>{cur_ver}</li>\n'
        b += '\t'
    max_ver = 'v' + max_ver
    return b, max_ver


@error_handler(default=dict(), error_text='Error reading mod modDependencies')
def get_modDependencies(root3):
    """dependence_dict{'packageId':displayName,}"""
    dependence_dict = {}
    dependencies_list : List[_Element] = []
    for data in root3:
        if data.tag.lower() == "moddependencies":
            dependencies_list = [li for li in data]
        elif data.tag.lower() == 'moddependenciesbyversion':
            dependencies_list = [li for li in data[-1]]
    if dependencies_list:
        for idx, li in enumerate(dependencies_list):
            packageId, displayName = str(idx), ''
            try:
                packageId = xml_get_text(li,'packageId')
                displayName = xml_get_text(li,'displayName', str(idx))
            except Exception as ex:
                print("Error reading mod modDependencies:")
                print(etree.tostring(li))

            if packageId:
                dependence_dict['packageId'] = displayName
    return dependence_dict

@error_handler(default=list(), error_text='Reading About.xml loadAfter error')
def get_loadafter_list(root3):

    loadafter_list: List[str] = []
    loadAfter = root3.find('loadAfter')
    if loadAfter is not None:
        for li in loadAfter:
            txt = li.text
            if txt:
                loadafter_list.append(str(txt))

    return loadafter_list

@error_handler(default=mod_data, error_text='Reading About.xml error')
def reading_about(data_path: str = 'About/About.xml'):
    tree3 = etree.parse(data_path, no_comment_parser)
    root3 = tree3.getroot()  #type: etree._Element

    mod_data.name = xml_get_text(root3, 'name')
    mod_data.packageId = xml_get_text(root3, 'packageId')
    mod_data.author = xml_get_text(root3, 'author')

    mod_data.supportedVersions, mod_data.max_version = get_supportedVersions(root3)
    mod_data.description = xml_get_text(root3, 'description')

    mod_data.url = get_steam_id_PublishedFileId()

    mod_data.loadafter_list = get_loadafter_list(root3)

    mod_data.modDependencies = get_modDependencies(root3)

    return mod_data
