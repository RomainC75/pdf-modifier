# install PyMuPDF
import os 
import pdfrw
from datetime import date
import fitz
from dotenv import dotenv_values
config = dotenv_values(".env.folders") 
from utils import SecuExtractor

ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'


DOCS_FOLDER = os.environ['DOCS_FOLDER']
TEMP_FOLDER = os.environ['TEMP_FOLDER']
STAMP_FOLDER = os.environ['STAMP_FOLDER']
OUTPUT_FOLDER = os.environ['OUTPUT_FOLDER']


class PdfHandler:
    def __init__( self, \
            siret:str, \
            first_name:str, \
            last_name:str, \
            contract_start_date:str, \
            sign_day: dict, \
            worker_folder:str, \
            base_pdf:str, \
            sign_last_day_of_month=True ) -> None:

        self.base_pdf = base_pdf
        self.output_temp_name = 'temp.pdf'
        self.output_file_name = f'{siret}_AER_{last_name}_{first_name}_{contract_start_date}.pdf'
        self.worker_folder = worker_folder

        self.sign_last_day_of_month=sign_last_day_of_month
        self.sign_day = sign_day
        self.secuExtractor = SecuExtractor(self.base_pdf)
        self.extracted_secu = self.secuExtractor.extract_secu_as_string()

        self.first_name = first_name
        self.last_name = last_name
        self.contract_start_date = contract_start_date
        

    def insert_images_and_siret(self) -> None:
        input_file=DOCS_FOLDER+self.base_pdf
        output_file = TEMP_FOLDER+self.output_temp_name
        file_handle = fitz.open(input_file)
        self.insert_siret_on_first_page(file_handle)
        self.insert_image(file_handle)
        file_handle.save(output_file,garbage=3, deflate=True)


    def insert_siret_on_first_page(self, file_handle) -> None:
        # p=fitz.Point(550,20)
        p=fitz.Point(228,157)
        full_str = f'{self.extracted_secu}, {self.first_name} {self.last_name}'
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


    def get_data_dict(self):
        data_dict = {
            'EMPLOYEUR_NOM': 'BARILLET',
            'EMPLOYEUR_PRENOM': 'Renaud',
            'EMPLOYEUR_QUAL_GERANT': True,
            'EMPLOYEUR_MOTIF_RUPTURE': "fin de contrat à durée déterminée ou fin d'acceuil occasionnel",
            'EMPLOYEUR_LIEU_SIGN': "Paris",
            'EMPLOYEUR_DATE_SIGN_J':self.sign_day['day'],
            'EMPLOYEUR_DATE_SIGN_M': self.sign_day['month'],
            'EMPLOYEUR_DATE_SIGN_A':self.sign_day['year'],
            'EMPLOYEUR_CORRES_NOM': "Brun Ludovic",
            'EMPLOYEUR_CORRES_EMAIL': "paye.rh@labellevilloise.com",
            'EMPLOYEUR_CORRES_TEL':"0153273574"
        }
        return data_dict

    def fill_pdf(self):
        input_pdf_path = TEMP_FOLDER+self.output_temp_name
        output_pdf_path = self.worker_folder+'/'+self.output_file_name
        # print('output : ', output_pdf_path)
        template_pdf = pdfrw.PdfReader(input_pdf_path)
        data_dict = self.get_data_dict()
        for page in template_pdf.pages:
            annotations = page[ANNOT_KEY]
            for annotation in annotations:
                if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                    if annotation[ANNOT_FIELD_KEY]:
                        key = annotation[ANNOT_FIELD_KEY][1:-1]
                        # print(key)                        
                        if key in data_dict.keys():
                            if type(data_dict[key]) == bool:
                                if data_dict[key] == True:
                                    annotation.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true'),AS=pdfrw.PdfName('Yes')))
                            else:
                                annotation.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true'),V='{}'.format(data_dict[key])))
                                annotation.update(pdfrw.PdfDict(AP=''))
        template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
        pdfrw.PdfWriter().write(output_pdf_path, template_pdf)
        
        # print('done', output_pdf_path)
        return output_pdf_path


# insert_images_and_siret("83825502400021","doc_empty.pdf","withSiret.pdf")