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
    startP=(400,1870)
    endP=(960,1950)
    secu_rect = img[startP[1]:endP[1], startP[0]:endP[0] ]
    # print(filter(lambda triad:triad[0][0]!=255, secu_rect))
    # secu_morphed = cv2.cvtColor(secu_rect, cv2.COLOR_BGR2GRAY)
    # secu_morphed = cv2.GaussianBlur(secu_morphed,(5,5),0)
    # secu_morphed = cv2.Canny(secu_morphed,75,100)

    # secu_morphed = cv2.cvtColor(secu_rect, cv2.COLOR_BGR2BGRA)
    # secu_morphed = cv2.Canny(secu_morphed,75,100)
    # low_color = np.array([0, 0, 0])
    # high_color = np.array([180, 179, 50])
    # secu_morphed = cv2.inRange(secu_rect,low_color, high_color)
    # secu_morphed = cv2.bitwise_not(secu_morphed)
    hsvImage = cv2.cvtColor(secu_rect, cv2.COLOR_BGR2HSV)
    grayscaleImage = cv2.cvtColor(secu_rect, cv2.COLOR_BGR2GRAY)

    yellow_bottom=np.array([25, 5, 70])
    yellow_top=np.array([35, 200, 255])
    bluepenMask = cv2.inRange(hsvImage, yellow_bottom, yellow_top)
    morphKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    bluepenMask = cv2.morphologyEx(bluepenMask, cv2.MORPH_CLOSE, morphKernel, None, None, 1, cv2.BORDER_REFLECT101)
    
    colorMask = cv2.add(grayscaleImage, bluepenMask)
    _, binaryImage = cv2.threshold(colorMask, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite(TEMP_FOLDER+'selection.jpg',binaryImage)
    thresh, im_bw = cv2.threshold(binaryImage, 210, 230, cv2.THRESH_BINARY)
    kernel = np.ones((1, 1), np.uint8)
    imgfinal = cv2.dilate(im_bw, kernel=kernel, iterations=1)
    
    #dilatation
    kernel = np.ones((5, 5), np.uint8)
    imgfinal = cv2.morphologyEx(imgfinal, cv2.MORPH_OPEN, kernel)
    cv2.imwrite(TEMP_FOLDER+'selection.jpg',binaryImage)


    # secu_morphed = cv2.bitwise_and(hsvImage, hsvImage, mask= mask) 
    
    
    
    
    # cv2.imwrite(TEMP_FOLDER+'selection.jpg', secu_morphed)
    return imgfinal

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