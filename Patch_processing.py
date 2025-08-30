import os
from pathlib import Path
from re import sub

from printy import printy

import Patch_grabber
from Get_database_by_list_of_pathes_of_mods import MultiIndexDict
from GlobFunc import escape_printy_string
from GlobVars import folders, state
from Settings_module import SVV as S


def patches(db:MultiIndexDict):

    if not folders.patches_folders:
        return

    printy(f'\t\tTry grab Defs from patches into "_Translation/Grabbed_Defs_from_patches"', 'n')
    printy('\t\tPatch_Grabber starts')

    patches_file_count = 0
    for pf in folders.patches_folders:
        Patch_grabber.main(patches_folder=pf,
                           folder_required_mods=folders.patches_folders[pf],
                           database=db
                           )

    "Получили state.mods_folders и state.keyed_from_patches"

    if state.keyed_from_patches:
        for file in state.keyed_from_patches:
            path = Path(
                '_Translation') / 'From_patches' / 'No mods required' / 'Languages' / S.Game_language / 'Keyed'
            os.makedirs(path, exist_ok=True)

            li_elem = f'<li>From_patches/No mods required</li>\n\t\t'
            if li_elem not in state.new_loadfolder_pathes:
                state.new_loadfolder_pathes.append(li_elem)
            new_name = str(file.stem) + str(patches_file_count) + str(file.suffix)
            patches_file_count += 1
            new_path = path / new_name
            with open(new_path, "w", encoding="utf-8") as new_patch_file:
                patches_file_count += 1
                new_patch_file.write("<LanguageData>\n")
                for line in state.keyed_from_patches[file]:
                    new_patch_file.write("\t" + line + "\n")
                new_patch_file.write(r"</LanguageData>")


    # from pprint import pprint
    # pprint(state.mods_folders, sort_dicts=False, width=200)
    '''
    -----{
    -----(req mods): 
    ---------{Path:
    ------------text1, text2]
    ---------}
    -----}
    '''
    # print('state.mods_folders:', state.mods_folders)
    for mf in state.mods_folders:
        # print('mf: ', mf)
        # print(state.mods_folders[mf])
        mod_folder_name_req_from_tuple = sub('[^0-9a-zA-Z]+', '_', str(mf[0])) if mf else ""
        new_grabbed_folder_path = Path('_Translation') / 'Grabbed_Defs_from_patches' / mod_folder_name_req_from_tuple
        # print(new_grabbed_folder_path)
        os.makedirs(new_grabbed_folder_path, exist_ok=True)

        for filepath in state.mods_folders[mf]:

            new_file_path = new_grabbed_folder_path / str(filepath.stem + str(patches_file_count) + filepath.suffix)
            with open(new_file_path, "w", encoding="utf-8") as new_patch_file:
                patches_file_count += 1
                new_patch_file.write("<Defs>\n")

                if mf:
                    new_patch_file.write(f'<!-- {list(mf)} -->\n')

                for l1 in state.mods_folders[mf][filepath]:
                    new_patch_file.write(l1)
                new_patch_file.write("\n</Defs>")

                new_modfold_name_req_from_tuple = mod_folder_name_req_from_tuple if mod_folder_name_req_from_tuple else "No mods required"

                np = Path(
                    '_Translation') / 'From_patches' / new_modfold_name_req_from_tuple / 'Languages' / S.Game_language / "DefInjected"

                folders.patches_defs[new_file_path] = np

                loadfolder_path = Path('From_patches') / new_modfold_name_req_from_tuple

                if mf:
                    li_elem = f'<li IfModActive="{mf[0]}">{loadfolder_path.as_posix()}</li>\n\t\t'
                else:
                    li_elem = f'<li>{loadfolder_path.as_posix()}</li>\n\t\t'

                if li_elem not in state.new_loadfolder_pathes:
                    state.new_loadfolder_pathes.append(li_elem)

        printy(f'\t\tPatches in:', 'o')
        for path, iids in folders.patches_folders.items():
            printy(f'\t\t{" ":<11}{escape_printy_string(path.as_posix())} : {escape_printy_string(str(iids))}', 'o')

        # print('folders.patches_pathes')
        # for a in folders.patches_pathes:
        #     print(a, folders.patches_pathes[a])
