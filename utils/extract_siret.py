import pytesseract
import cv2
import numpy as np
import re
import os
from pdf2image import convert_from_path

def convert_first_page_to_image(path_to_empty_pdf):
    doc = convert_from_path(path_to_empty_pdf)
    path, fileName = os.path.split(path_to_empty_pdf)
    fileBaseName, fileExtension = os.path.splitext(fileName)
    #write down first page
    page_to_analyse = doc[0]
    page_to_analyse.save('temp.jpg', 'JPEG')

def select_rectangle_and_change_images(img):
    cv2.imshow('img', img)
    startP=(230,670)
    endP=(755,730)
    siret_rect = img[startP[1]:endP[1], startP[0]:endP[0] ]
    siret_morphed = cv2.cvtColor(siret_rect, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('selection.jpg', siret_morphed)
    return siret_morphed

def extract_siret_as_string(path_to_empty_pdf):
    # convert and create "temp.jpg"
    convert_first_page_to_image(path_to_empty_pdf)
    
    img = cv2.imread('temp.jpg')

    siret_morphed = select_rectangle_and_change_images(img)
    # tried to filter the gray color
    # lower = np.array([220,220,220], dtype="uint8")  
    # upper = np.array([230,230,230], dtype="uint8")  
    # siret_filtered = cv2.inRange(siret_morphed, lower, upper)
    
    txt = pytesseract.image_to_string(siret_morphed).encode("utf-8")
    txt = txt.decode('ascii')
    siret = re.findall(r"[0-9]",txt)
    siret_string = "".join(siret)
    print("siret : ", siret_string)
    return siret_string


# extract_siret_as_string('../docs/doc_empty.pdf')