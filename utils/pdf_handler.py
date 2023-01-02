# install PyMuPDF
import fitz
from dotenv import dotenv_values
config = dotenv_values(".env.folders") 

DOCS_FOLDER = config['DOCS_FOLDER']
TEMP_FOLDER = config['TEMP_FOLDER']
STAMP_FOLDER = config['STAMP_FOLDER']

# ex : image and siret

class PdfHandler:
    def __init__(self, data_list:list, empty_pdf:str, output_file_name:str) -> None:
        self.data_list = data_list
        self.empty_pdf = empty_pdf
        self.output_file_name = output_file_name

    def insert_images_and_siret(self) -> None:
        input_file=DOCS_FOLDER+self.empty_pdf
        output_file = TEMP_FOLDER+self.output_file_name
        file_handle = fitz.open(input_file)
        self.insert_siret_on_first_page(file_handle)
        self.insert_image(file_handle)
        file_handle.save(output_file,garbage=3, deflate=True)
        print('--', output_file)

    def insert_siret_on_first_page(self, file_handle) -> None:
        # p=fitz.Point(550,20)
        p=fitz.Point(228,157)
        full_str = f'{self.data_list[0]}, {self.data_list[1]} {self.data_list[2]}'
        file_handle[0].insert_text( (p[0],p[1]) , full_str, color=(0,0,0),fontsize=6)

    def insert_image(self, file_handle):
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

# insert_images_and_siret("83825502400021","doc_empty.pdf","withSiret.pdf")