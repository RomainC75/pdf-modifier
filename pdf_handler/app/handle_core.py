from os import path, mkdir
import os
from glob import glob
from dotenv import dotenv_values
from tqdm import tqdm
import shutil
from utils import \
    PdfHandler, \
    get_infos_from_filename, \
    create_folder, \
    copy_to_merge_folder, \
    merge_pdfs, \
    SIRET_CONVERTOR, \
    get_selected_date

#test working folders 

def handle_core(db_publish, selectedDate):
    
    def handle_error(path):
        print("==> Error :")
        print(f"{path} doesn't exist !")
        raise FileNotFoundError

    #test folders and files
    if not path.exists("./app/data"):
        handle_error("./app/data")


    stamps = ["signature.png", "stamp.png"]
    for stamp_filename in stamps:
        if not path.exists(os.environ["STAMP_FOLDER"]+stamp_filename):
            handle_error(os.environ["STAMP_FOLDER"]+stamp_filename)


    error_file_names = []
    merge_folders_paths = []

    # ============================
    sign_day = get_selected_date(selectedDate)
    

    pdfPaths = glob(os.environ['DOCS_FOLDER']+'*.pdf')
    print(f"==> pdfPaths : {pdfPaths}", flush=True)
    for pdfPath in tqdm(pdfPaths,desc="pdf documents"):
        try:
            pathFilename = path.split(pdfPath)
            siret, lastname, firstname, date = get_infos_from_filename(pathFilename[1])

            society_name = SIRET_CONVERTOR[siret]
            month = date[2:4]
            year = date[4:]
            
            society_folder = f'{os.environ["OUTPUT_FOLDER"]}{society_name}_AER_{month}_{year}'
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
                sign_day = sign_day, \
                sign_last_day_of_month=True)

            pdfhandler.insert_images_and_siret()

            completed_file = pdfhandler.fill_pdf()

            new_merge_folder_path = copy_to_merge_folder(completed_file, society_folder)
            if new_merge_folder_path:
                merge_folders_paths.append({
                    'folder_path': new_merge_folder_path,
                    'folder_name': f'{society_name}_AER_{month}_{year}',
                    })

        except Exception as inst:
            # if error => copy to the "error" folder
            print('==>ERROR : ',inst)
            error_file_names.append(pdfPath)
            create_folder(f'{os.environ["OUTPUT_FOLDER"]}00_errors')
            shutil.copy(pdfPath, f'{os.environ["OUTPUT_FOLDER"]}00_errors/{pathFilename[1]}')


    print('\n======Results======\n')
    print(f'PDF handled => {len(pdfPaths)}')
    print(f'No Error => {len(pdfPaths)-len(error_file_names)}')
    print(f'Errors => {len(error_file_names)}')
    if len(error_file_names)>0:
        for name in error_file_names:
            print(f'==>{name}')
        print(f'go to the folder /errors to handle these files separatly')

    for merge_folder_obj in merge_folders_paths:
        merge_pdfs(merge_folder_obj)
