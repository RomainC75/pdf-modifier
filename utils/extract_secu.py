import pytesseract
import cv2
import numpy as np
import re
import os
from pdf2image import convert_from_path
from dotenv import dotenv_values
import json

config = dotenv_values(".env.folders")

DOCS_FOLDER= config["DOCS_FOLDER"]
TEMP_FOLDER = config["TEMP_FOLDER"]




def convert_first_page_to_image(path_to_empty_pdf):
    doc = convert_from_path(path_to_empty_pdf)
    # path, fileName = os.path.split(path_to_empty_pdf)
    # fileBaseName, fileExtension = os.path.splitext(fileName)
    #write down first page
    page_to_analyse = doc[0]
    page_to_analyse.save(TEMP_FOLDER+'temp.jpg', 'JPEG')


def select_rectangle_and_change_colors(img):
    cv2.imshow('img', img)
    # startP=(230,670)
    # endP=(755,730)
    
    startP=(390,1870)
    endP=(960,1950)
    secu_rect = img[startP[1]:endP[1], startP[0]:endP[0] ]
    # print(filter(lambda triad:triad[0][0]!=255, secu_rect))
    yellow_bottom=[]
    yellow_top=[]

    # secu_morphed = cv2.cvtColor(secu_rect, cv2.COLOR_BGR2GRAY)
    # secu_morphed = cv2.GaussianBlur(secu_morphed,(5,5),0)
    # secu_morphed = cv2.Canny(secu_morphed,75,100)

    # secu_morphed = cv2.cvtColor(secu_rect, cv2.COLOR_BGR2BGRA)
    # secu_morphed = cv2.Canny(secu_morphed,75,100)
    # low_color = np.array([0, 0, 0])
    # high_color = np.array([180, 179, 50])
    # secu_morphed = cv2.inRange(secu_rect,low_color, high_color)
    # secu_morphed = cv2.bitwise_not(secu_morphed)
    
    
    
    cv2.imwrite(TEMP_FOLDER+'selection.jpg', secu_rect)
    return secu

def extract_secu_as_string(emptypdf_name):
    pdf_path = DOCS_FOLDER+emptypdf_name
    # convert and create "temp.jpg"
    convert_first_page_to_image(pdf_path)
    
    img = cv2.imread(TEMP_FOLDER+'temp.jpg')
    secu_morphed = select_rectangle_and_change_colors(img)
    
    txt = pytesseract.image_to_string(secu_morphed).encode("utf-8")
    print("raw : ", txt)
    txt = txt.decode('ascii')
    secu = re.findall(r"[0-9]",txt)
    secu_string = "".join(secu)
    print("n° SECU  : ", secu_string)
    return secu_string

# extract_secu_as_string('doc_empty.pdf')