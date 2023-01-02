from os import path, mkdir
import re
from time import sleep
from glob import glob
from dotenv import dotenv_values
from tqdm import tqdm

# from utils import get_infos_from_filename, extract_secu_as_string, fill_pdf, insert_images_and_siret
from utils import SecuExtractor, PdfHandler, get_infos_from_filename, create_folder

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
        print('0 : ',pathFilename[0])

        #society folder
        #person folder

        siret, lastname, firstname, date = get_infos_from_filename(pathFilename[1])
        print(siret, lastname, firstname, date)

        society_name = SIRET_CONVERTOR[siret]
        month = date[2:4]
        year = date[4:]
        society_folder = f'{config["OUTPUT_FOLDER"]}/{society_name}_AER_{month}_{year}'
        worker_folder = f'{society_folder}/{lastname}_{firstname}'
        print('=====§§§§§§ ',society_folder, worker_folder)
        
        create_folder(society_folder)
        create_folder(worker_folder)

        
        pdfhandler = PdfHandler(SIRET_CONVERTOR[siret], firstname, lastname, date, "doc_empty.pdf", sign_last_day_of_month=True)
        pdfhandler.insert_images_and_siret()
        pdfhandler.fill_pdf()
    except:
        error_file_names.append(pdfPath)

print(f'Errors : {len(error_file_names)}')
if len(error_file_names)>0:
    for name in error_file_names:
        print(f'==>{name}')
    print(f'go to the folder /errors to handle these files separatly')


#     print(siret,lastname, firstname)
#     insert_images_and_siret([secu_string, lastname,firstname], pathFilename[1], "temp.pdf")
#     fill_pdf( "temp.pdf", pathFilename[1] ) 
    



# print("errors : ",errors)
# try:
#     pdfhandler = PdfHandler("Bob","Sinclar","doc_empty.pdf","withSiret.pdf", sign_last_day_of_month=True )
#     # pdfhandler = PdfHandler("doc_empty.pdf","withSiret.pdf")
#     pdfhandler.insert_images_and_siret()
#     print('===')
#     pdfhandler.fill_pdf()
# except :
#     print('import error')




#get every files names to work on
# pdfPaths = glob(config['DOCS_FOLDER']+'*.pdf')
# for pdfPath in tqdm(pdfPaths,desc="pdf documents"):
#     pathFilename = path.split(pdfPath)
    
#     secu_string=extract_secu_as_string(pathFilename[1])
#     if len(secu_string)!=13 and len(secu_string)!=15:
#         print("Secu number : wrong length : ", secu_string, len(secu_string))
#         errors+=1

#     siret, lastname, firstname = get_infos_from_filename(pathFilename[1])
#     print(siret,lastname, firstname)
#     insert_images_and_siret([secu_string, lastname,firstname], pathFilename[1], "temp.pdf")
#     fill_pdf( "temp.pdf", pathFilename[1] ) 

