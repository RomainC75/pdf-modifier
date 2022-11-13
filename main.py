from os import path
import re
from time import sleep
from glob import glob
from dotenv import dotenv_values
from tqdm import tqdm

from utils import get_infos_from_filename, extract_secu_as_string, fill_pdf, insert_images_and_siret

#test working folders 
config = dotenv_values(".env.folders")
def print_error(path):
    print("==> Error :")
    print(f"{path} doesn't exist !")
    exit()
#test folders and files
if not path.exists("./data"):
    print_error("./data")

for (key,subfolder) in config.items():
    if not path.exists(subfolder):
        print_error(subfolder)

stamps = ["signature.png", "stamp.png"]
for stamp_filename in stamps:
    if not path.exists(config["STAMP_FOLDER"]+stamp_filename):
        print_error(config["STAMP_FOLDER"]+stamp_filename)


errors=0

#get every files names to work on
pdfPaths = glob(config['DOCS_FOLDER']+'*.pdf')
for pdfPath in tqdm(pdfPaths,desc="pdf documents"):
    pathFilename = path.split(pdfPath)
    
    secu_string=extract_secu_as_string(pathFilename[1])
    if len(secu_string)!=13 and len(secu_string)!=15:
        print("Secu number : wrong length : ", secu_string, len(secu_string))
        errors+=1

    siret, lastname, firstname = get_infos_from_filename(pathFilename[1])
    print(siret,lastname, firstname)
    insert_images_and_siret([secu_string,siret,lastname,firstname], pathFilename[1], "temp.pdf")
    fill_pdf( "temp.pdf", pathFilename[1] ) 
    
print("errors : ",errors)

