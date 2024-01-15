import os

import requests
from printy import printy


def Check_new_version():
    url = 'https://github.com/kamikadza13/Text-grabber/releases/latest'
    r = requests.get(url)
    vers = r.url.split('/')[-1]
    return vers

def Download_new_version():
    printy("Need to Update", 'r')
    os.system(f"start \"\" https://github.com/kamikadza13/Text-grabber/releases/latest/download/Text_Grabber.zip")


def Check_And_Update(Version_of_Text_grabber):
    try:
        version = Check_new_version()
        if version > Version_of_Text_grabber:
            Download_new_version()
            return True
    except Exception as e:
        printy("Can't Update", 'r')
        print(e)
    return False


if __name__ == '__main__':
    ver2 = Check_new_version()
    if ver2 > "1.0.0":
        Download_new_version()



'''
https://github.com/kamikadza13/Text-grabber/releases/latest/download/Text_Grabber.zip
'''



