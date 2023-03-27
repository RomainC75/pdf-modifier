import os
import pytesseract
import cv2
import numpy as np
import re
from pdf2image import convert_from_path
from dotenv import dotenv_values

# config = dotenv_values(".env.folders")

DOCS_FOLDER= os.environ["DOCS_FOLDER"]
TEMP_FOLDER = os.environ["TEMP_FOLDER"]


class SecuExtractor:
    def __init__(self, emptypdf_name) -> None:
        self.emptypdf_name = emptypdf_name
        self.pdf_path = DOCS_FOLDER+self.emptypdf_name
    
    def convert_first_page_to_image(self):
        print('convert first page : ', self.pdf_path)
        first_page = convert_from_path(self.pdf_path, dpi=600, first_page=2, last_page=2)
        first_page[0].save(TEMP_FOLDER+'temp.jpg', 'JPEG')

    def select_rectangle_and_change_colors(self, img):
        startP=(1600,450)
        endP=(3300,520)
        secu_rect = img[startP[1]:endP[1], startP[0]:endP[0] ]
        # cv2.imshow("secu ", secu_rect)
        secu_morphed = cv2.cvtColor(secu_rect, cv2.COLOR_BGR2BGRA)
        cv2.imwrite(TEMP_FOLDER+'selection.jpg', secu_morphed)
        return secu_morphed

    def extract_secu_as_string(self):
        try:
            print('0.5')
            self.convert_first_page_to_image()
            print('1')
            img = cv2.imread(TEMP_FOLDER+'temp.jpg')
            print('2')
            secu_morphed = self.select_rectangle_and_change_colors(img)
            print('3')
            txt = pytesseract.image_to_string(secu_morphed).encode("utf-8")
            print('4')
            txt_decode = txt.decode('utf-8')
            print('5')
            secu = re.findall(r"[0-9]*",txt_decode)
            print('6')
            secu_string = "".join(secu)
            print('7')
            print("n° SECU  : ", secu_string)
            
            return secu_string
        except :
            raise ImportError('could not extract SECU number')


