import pytesseract
import cv2
import numpy as np
import re
import os
from pdf2image import convert_from_path
from dotenv import dotenv_values

config = dotenv_values(".env.folders")

DOCS_FOLDER= config["DOCS_FOLDER"]
TEMP_FOLDER = config["TEMP_FOLDER"]

def convert_first_page_to_image(path_to_empty_pdf):
    doc = convert_from_path(path_to_empty_pdf)
    path, fileName = os.path.split(path_to_empty_pdf)
    fileBaseName, fileExtension = os.path.splitext(fileName)
    #write down first page
    page_to_analyse = doc[0]
    page_to_analyse.save(TEMP_FOLDER+'temp.jpg', 'JPEG')

def select_rectangle_and_change_colors(img):
    cv2.imshow('img', img)
    startP=(230,670)
    endP=(755,730)
    siret_rect = img[startP[1]:endP[1], startP[0]:endP[0] ]
    siret_morphed = cv2.cvtColor(siret_rect, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('selection.jpg', siret_morphed)
    return siret_morphed

def extract_siret_as_string(emptypdf_name):
    pdf_path = DOCS_FOLDER+emptypdf_name
    # convert and create "temp.jpg"
    convert_first_page_to_image(pdf_path)
    
    img = cv2.imread(TEMP_FOLDER+'temp.jpg')

    siret_morphed = select_rectangle_and_change_colors(img)
    
    txt = pytesseract.image_to_string(siret_morphed).encode("utf-8")
    txt = txt.decode('ascii')
    siret = re.findall(r"[0-9]",txt)
    siret_string = "".join(siret)
    print("siret : ", siret_string)
    return siret_string

# extract_siret_as_string('doc_empty.pdf')