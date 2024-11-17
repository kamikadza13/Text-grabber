import os

import requests
from printy import printy


def Get_newest_version_number():
    url = 'https://github.com/kamikadza13/Text-grabber/releases/latest'
    r = requests.get(url)
    vers = r.url.split('/')[-1]
    return vers

def Download_new_version():
    os.system(f"start \"\" https://github.com/kamikadza13/Text-grabber/releases/latest/download/Text_Grabber.zip")


def Check_And_Update(Version_of_Text_grabber):
    try:
        version = Get_newest_version_number()
        if version > Version_of_Text_grabber:
            Download_new_version()
            return True
    except Exception as e:
        printy("Can't Update", 'r')
        print(e)
    return False


if __name__ == '__main__':
    ver2 = Get_newest_version_number()
    if ver2 > "1.0.0":
        Download_new_version()



'''
https://github.com/kamikadza13/Text-grabber/releases/latest/download/Text_Grabber.zip
'''



