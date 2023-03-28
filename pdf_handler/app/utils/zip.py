import shutil
import os

zip_file_name = './app/data/pdf_result'
output_folder = './app/data/output'
docs_folder = './app/data/docs'

def zip_output():
    name = shutil.make_archive(zip_file_name, 'zip', output_folder)
    print(f"ZIP NAME : {name}",flush=True)

def remove_folder_content(path):
    shutil.rmtree(path)
    os.mkdir(path)

def zip_and_remove_output():
    zip_output()
    remove_folder_content(output_folder)
    remove_folder_content(docs_folder)
