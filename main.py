from os import path, mkdir
import re
from time import sleep
from glob import glob
from dotenv import dotenv_values
from tqdm import tqdm
import shutil

from utils import \
    PdfHandler, \
    get_infos_from_filename, \
    create_folder, \
    raise_random_error, \
    copy_to_merge_folder, \
    PDFMerger

SIRET_CONVERTOR ={
    '49320424200017':'LACHOPE'
}

#test working folders 
config = dotenv_values(".env.folders")
def handle_error(path):
    print("==> Error :")
    print(f"{path} doesn't exist !")
    raise FileNotFoundError

#test folders and files
if not path.exists("./data"):
    handle_error("./data")

for (key,subfolder) in config.items():
    if not path.exists(subfolder):
        handle_error(subfolder)

stamps = ["signature.png", "stamp.png"]
for stamp_filename in stamps:
    if not path.exists(config["STAMP_FOLDER"]+stamp_filename):
        handle_error(config["STAMP_FOLDER"]+stamp_filename)

error_file_names = []

#get every files names to work on
pdfPaths = glob(config['DOCS_FOLDER']+'*.pdf')
for pdfPath in tqdm(pdfPaths,desc="pdf documents"):
    try:
        pathFilename = path.split(pdfPath)
        siret, lastname, firstname, date = get_infos_from_filename(pathFilename[1])

        society_name = SIRET_CONVERTOR[siret]
        month = date[2:4]
        year = date[4:]
        
        society_folder = f'{config["OUTPUT_FOLDER"]}{society_name}_AER_{month}_{year}'
        worker_folder = f'{society_folder}/{lastname}_{firstname}'
    
        create_folder(society_folder)
        create_folder(worker_folder)
        
        pdfhandler = PdfHandler(\
            siret = SIRET_CONVERTOR[siret], \
            first_name = firstname, \
            last_name = lastname, \
            contract_start_date = date, \
            worker_folder = worker_folder, \
            base_pdf = pathFilename[1], \
            sign_last_day_of_month=True)

        pdfhandler.insert_images_and_siret()

        completed_file = pdfhandler.fill_pdf()
        copy_to_merge_folder(completed_file, society_folder)

    except:
        error_file_names.append(pdfPath)
        create_folder(f'{config["OUTPUT_FOLDER"]}00_errors')
        #TODO copy the file in the error folder
        shutil.copy(pdfPath, f'{config["OUTPUT_FOLDER"]}00_errors/{pathFilename[1]}')



print(f'Errors : {len(error_file_names)}')
if len(error_file_names)>0:
    for name in error_file_names:
        print(f'==>{name}')
    print(f'go to the folder /errors to handle these files separatly')

