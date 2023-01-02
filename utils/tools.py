import re
from os import mkdir

def get_infos_from_filename(filename):
    try:
        matches = re.match(r'AE_([0-9]{14})_\d+_\d+_([^_]+)_([^_]+)_(\d+)_(\d+)_',filename)
        # return {
        #     "siret":matches.group(1),
        #     "lastname":matches.group(2),
        #     "firstname":matches.group(3),
        #     "date"
        # }
        return (matches.group(1),matches.group(2).capitalize(),matches.group(3).capitalize(),matches.group(5))
    except:
        print('===>error : ', filename)

def create_folder(path):
    try:
        mkdir(path)
    except:
        pass

