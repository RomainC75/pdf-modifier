import pytesseract
import cv2
import numpy as np
import re
import os
from pdf2image import convert_from_path
from dotenv import dotenv_values
import json
import pandas as pd
import math
from matplotlib import pyplot as plt
from unidecode import unidecode

config = dotenv_values(".env.folders")

DOCS_FOLDER= config["DOCS_FOLDER"]
TEMP_FOLDER = config["TEMP_FOLDER"]




def convert_first_page_to_image_and_save_to_tempFile(path_to_empty_pdf):
    first_page = convert_from_path(path_to_empty_pdf, dpi=600, first_page=1, last_page=1)
    # path, fileName = os.path.split(path_to_empty_pdf)
    # fileBaseName, fileExtension = os.path.splitext(fileName)
    #write down first page
    
    
    first_page[0].save(TEMP_FOLDER+'temp.jpg', 'JPEG')


def select_rectangle_and_change_colors(img):
    # cv2.imshow('img', img)
    # startP=(230,670)
    # endP=(755,730)
    
    startP=(1180,5620)
    endP=(2650,5800)
    img_raw = img[startP[1]:endP[1], startP[0]:endP[0] ]
    # print(filter(lambda triad:triad[0][0]!=255, secu_rect))
    


    img_hsv = cv2.cvtColor(img_raw, cv2.COLOR_BGR2HSV)
    img_changing = cv2.cvtColor(img_raw, cv2.COLOR_RGB2GRAY)
    low_color = np.array([0, 0, 0])
    high_color = np.array([180, 255, 30])
    blackColorMask = cv2.inRange(img_hsv, low_color, high_color)
    img_inversion = cv2.bitwise_not(img_changing)
    img_black_filtered = cv2.bitwise_and(img_inversion, img_inversion, mask = blackColorMask)
    img_final_inversion = cv2.bitwise_not(img_black_filtered)

    # img_final_inversion = cv2.GaussianBlur(img_final_inversion,(5,5),0)
    img_final_inversion = cv2.blur(img_final_inversion,(5,5),0)

    # cv2.imshow("raw", img_raw)
    # cv2.imshow("mask", blackColorMask)
    # cv2.imshow("changing :", img_changing)
    # cv2.imshow("filterd : ", img_black_filtered)
    # cv2.imshow("negatif : ", img_inversion)
    # cv2.imshow("final ? ", img_final_inversion)

    img_copy=img_raw.copy()
    img_canny = cv2.Canny(img_copy, 180, 200, apertureSize=3)

    

    # secu_morphed = cv2.cvtColor(secu_rect, cv2.COLOR_BGR2GRAY)
    # secu_morphed = cv2.GaussianBlur(secu_morphed,(5,5),0)
    # secu_morphed = cv2.Canny(secu_morphed,75,100)

    
    
    cv2.imwrite(TEMP_FOLDER+'selection.jpg', img_final_inversion)


    return img_final_inversion

def extract_secu_as_string(emptypdf_name):
    pdf_path = DOCS_FOLDER+emptypdf_name
    # convert and create "temp.jpg"
    convert_first_page_to_image_and_save_to_tempFile(pdf_path)
    
    img = cv2.imread(TEMP_FOLDER+'temp.jpg')
    secu_morphed = select_rectangle_and_change_colors(img)

    

    #remove
    #just print the layers and data
    data = pytesseract.image_to_data(secu_morphed)
    # convert to pandas
    dataList = list(map(lambda x: x.split('\t'),data.split('\n') ))
    df = pd.DataFrame(dataList[1:],columns=dataList[0])
    df.dropna(inplace=True)
    print("===> DATA : ",data)

    
    # txt = pytesseract.image_to_string(secu_morphed).encode("utf-8")
    # print("raw : ", txt, len(txt))
    # txt = txt.decode('ascii')
    # secu = re.findall(r"[0-9]",txt)
    # secu_string = "".join(secu)
    # print("n° SECU  : ", secu_string)

    txt_raw = pytesseract.image_to_string(secu_morphed)
    txt = unidecode(txt_raw)
    secu = re.findall(r"[0-9]",txt)
    secu_string = "".join(secu)
    print("n° SECU  : ", secu_string, " len : ", len(secu_string))

    #remove
    #rectangles
    d = pytesseract.image_to_data(secu_morphed, output_type=pytesseract.Output.DICT)
    
    NbBoites = len(d['level'])
    print ("Nombre de boites: " + str(NbBoites))
    for i in range(NbBoites):
        # Récupère les coordonnées de chaque boite
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        # Affiche un rectangle
        cv2.rectangle(secu_morphed, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # cv2.imshow('img', secu_morphed)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    return secu_string

# extract_secu_as_string('doc_empty.pdf')