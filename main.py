from os import path
from dotenv import dotenv_values
from utils.insert_text_inside_forms import fill_pdf
from utils.insert_images_and_siret import insert_images_and_siret
from utils.extract_siret import extract_siret_as_string
from time import sleep

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

#extract
siret = extract_siret_as_string("doc_empty.pdf")
insert_images_and_siret(siret, "doc_empty.pdf", "temp.pdf")
fill_pdf("temp.pdf","output.pdf")
