import re

def get_infos_from_filename(filename):
    matches = re.match(r'AE_([0-9]{14})_\d+_\d+_([^_]+)_([^_]+)',filename)
    # return {
    #     "siret":matches.group(1),
    #     "lastname":matches.group(2),
    #     "firstname":matches.group(3),
    # }
    return (matches.group(1),matches.group(2),matches.group(3))
