import pytesseract
import cv2
import numpy as np
import re
from pdf2image import convert_from_path
from dotenv import dotenv_values

config = dotenv_values(".env.folders")

DOCS_FOLDER= config["DOCS_FOLDER"]
TEMP_FOLDER = config["TEMP_FOLDER"]

def convert_first_page_to_image(path_to_empty_pdf):
    first_page = convert_from_path(path_to_empty_pdf, dpi=600, first_page=2, last_page=2)    
    first_page[0].save(TEMP_FOLDER+'temp.jpg', 'JPEG')

def select_rectangle_and_change_colors(img):
    startP=(1600,450)
    endP=(3300,520)
    secu_rect = img[startP[1]:endP[1], startP[0]:endP[0] ]
    # cv2.imshow("secu ", secu_rect)
    secu_morphed = cv2.cvtColor(secu_rect, cv2.COLOR_BGR2BGRA)
    cv2.imwrite(TEMP_FOLDER+'selection.jpg', secu_morphed)
    return secu_morphed

def extract_secu_as_string(emptypdf_name):
    pdf_path = DOCS_FOLDER+emptypdf_name
    convert_first_page_to_image(pdf_path)
    img = cv2.imread(TEMP_FOLDER+'temp.jpg')
    secu_morphed = select_rectangle_and_change_colors(img)

    txt = pytesseract.image_to_string(secu_morphed).encode("utf-8")

    txt_decode = txt.decode('utf-8')
    secu = re.findall(r"[0-9]*",txt_decode)
    secu_string = "".join(secu)
    print("n° SECU  : ", secu_string)
    
    # if(len(secu)!=13):
    #     cv2.imshow('img', secu_morphed)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()
    return secu_string

# extract_secu_as_string('doc_empty.pdf')