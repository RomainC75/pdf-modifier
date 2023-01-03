import re
from os import mkdir
import random 
import shutil

def get_infos_from_filename(filename):
    
    try:
        matches = re.match(r'AE_([0-9]{14})_\d+_\d+_([^_]+)_([^_]+)_(\d+)_(\d+)_',filename)
        # siret, lastname, firstname, date
        return (matches.group(1),matches.group(2).capitalize(),matches.group(3).capitalize(),matches.group(5))
    except:
        print('===>error : ', filename)

def create_folder(path):
    try:
        mkdir(path)
    except:
        pass

def copy_to_merge_folder(file_to_copy, society_folder):
    create_folder(society_folder+'/01_merge')
    shutil.copy(file_to_copy,society_folder+'/01_merge')

def raise_random_error():
    if random.randint(0,1)==1:
        raise SyntaxError('error')
        
