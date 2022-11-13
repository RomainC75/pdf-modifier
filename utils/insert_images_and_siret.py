# install PyMuPDF
import fitz
from dotenv import dotenv_values
config = dotenv_values(".env.folders") 

DOCS_FOLDER = config['DOCS_FOLDER']
TEMP_FOLDER = config['TEMP_FOLDER']
STAMP_FOLDER = config['STAMP_FOLDER']

def insert_image(file_handle):
    signature = STAMP_FOLDER+"signature.png"
    stamp = STAMP_FOLDER+"stamp.png"

    # define the position (upper-right corner)
    signature_rectangle = fitz.Rect(30,520,190,610)
    stamp_rectangle = fitz.Rect(400,520,550,610)

    # retrieve the first page of the PDF
    first_page = file_handle[7]

    # open image files
    signature_img = open(signature, "rb").read()
    stamp_img = open(stamp, "rb").read()
    img_xref = 0

    # add the image
    first_page.insert_image(signature_rectangle, stream=signature_img , xref=img_xref)
    first_page.insert_image(stamp_rectangle, stream=stamp_img , xref=img_xref)


def insert_siret_on_every_pages(data_txt, file_handle):
    p=fitz.Point(550,20)
    for page in file_handle:
        print("page : ", page)
        for index, info in enumerate(data_txt):
            page.insert_text((p[0],p[1]+index*10) , info, color=(0,0,0),fontsize=5)


def insert_images_and_siret(data_txt, input_name, output_name):
    input_file=DOCS_FOLDER+input_name
    output_file = TEMP_FOLDER+output_name

    print(data_txt, input_file, output_file)
    file_handle = fitz.open(input_file)
    insert_siret_on_every_pages(data_txt, file_handle)
    insert_image(file_handle)

    file_handle.save(output_file)

# insert_images_and_siret("83825502400021","doc_empty.pdf","withSiret.pdf")