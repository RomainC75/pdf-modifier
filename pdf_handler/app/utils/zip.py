import shutil
import os
import zipfile

zip_file_name = os.environ['PRIVATE_FOLDER']+'/'+os.environ['PDF_RESULT_BASENAME']
output_folder = os.environ["OUTPUT_FOLDER"]
docs_folder = os.environ["DOCS_FOLDER"]

# os.environ["PRIVATE_FOLDER"]

def zip_output():
    name = shutil.make_archive(zip_file_name, 'zip', output_folder)
    print(f"ZIP NAME : {name}",flush=True)

def tar_output():
    name = shutil.make_archive(zip_file_name, 'tar', output_folder)
    print(f"ZIP NAME : {name}",flush=True)

def zipfile_output():
    zipobj = zipfile.ZipFile(zip_file_name + '.zip', 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(output_folder) + 1
    for base, dirs, files in os.walk(output_folder):
        for file in files:
            fn = os.path.join(base, file)
            zipobj.write(fn, fn[rootlen:])


def remove_folder_content(path):
    shutil.rmtree(path)
    os.mkdir(path)

def zip_and_remove_output():
    tar_output()
    remove_folder_content(output_folder)
    remove_folder_content(docs_folder)
