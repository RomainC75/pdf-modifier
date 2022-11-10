import pdfrw
from datetime import date
from dotenv import dotenv_values
config = dotenv_values(".env.folders")

TEMP_FOLDER = config['TEMP_FOLDER']
OUTPUT_FOLDER = config['OUTPUT_FOLDER']

pdf_template = TEMP_FOLDER+"doc_empty.pdf"
pdf_output = OUTPUT_FOLDER+"folder/output.pdf"

ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'

today_date = date.today()

today = {
    'day' : str(today_date.day) if today_date.day>=10 else '0'+str(today_date.day),
    'month' : str(today_date.month) if today_date.month>=10 else '0'+str(today_date.month),
    'year' : today_date.year
}

data_dict = {
    'EMPLOYEUR_NOM': 'BARILLET',
    'EMPLOYEUR_PRENOM': 'Renaud',
    'EMPLOYEUR_QUAL_GERANT': True,
    'EMPLOYEUR_MOTIF_RUPTURE': "fin de contrat à durée déterminée ou fin d'acceuil occasionnel",
    'EMPLOYEUR_LIEU_SIGN': "Paris",
    'EMPLOYEUR_DATE_SIGN_J':today['day'],
    'EMPLOYEUR_DATE_SIGN_M': today['month'],
    'EMPLOYEUR_DATE_SIGN_A':today['year'],
    'EMPLOYEUR_CORRES_NOM': "Brun Ludovic",
    'EMPLOYEUR_CORRES_EMAIL': "paye.rh@labellevilloise.com",
    'EMPLOYEUR_CORRES_TEL':"0153273574"
}



def fill_pdf(input_name, output_name):
    input_pdf_path = TEMP_FOLDER+input_name
    output_pdf_path = OUTPUT_FOLDER+output_name
    template_pdf = pdfrw.PdfReader(input_pdf_path)
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
                                annotation.update(pdfrw.PdfDict(
                                    AS=pdfrw.PdfName('Yes')))
                        else:
                            annotation.update(
                                pdfrw.PdfDict(V='{}'.format(data_dict[key]))
                            )
                            annotation.update(pdfrw.PdfDict(AP=''))
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)
    
                
# print("==>date", date.today())

# fill_pdf("doc_empty.pdf", "temp.pdf")