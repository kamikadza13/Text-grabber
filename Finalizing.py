import re
from pathlib import Path


def main(FP: Path):
    all_files = FP.rglob('*.xml')
    # all_files = list(Path(FP.mod).glob('RimThunder - Core rus/**/*.xml'))
    duble_list = []


    for file in all_files: # type: Path
        # print(file)
        fstem = file.stem
        # print(fstem)

        if fstem not in duble_list:
            duble_list.append(fstem)
            continue

        # print(f'"{fstem}" in Dousble list')
        match = re.search(r'(\d+)$', fstem)
        # print(match)

        if match:
            number = int(match.group(1)) + 1
            new_filename_without_suffix = re.sub(r'\d+$', str(number), fstem)
            file.rename(str(file.parent) + "\\" + new_filename_without_suffix + '.xml')
            duble_list.append(new_filename_without_suffix)

            print(f'    Renamed {file.name} to {new_filename_without_suffix + ".xml"}')
        else:
            file.rename(str(file.parent)  + "\\" + fstem + '0.xml')
            duble_list.append(fstem + '0')
            print(f'    Renamed {file.name} to {fstem + "0.xml"}')

    # print('duble_list', duble_list)





    # print(duble_list)


