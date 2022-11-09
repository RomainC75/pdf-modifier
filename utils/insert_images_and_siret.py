# install PyMuPDF
import fitz

DOCS_FOLDER='../data/docs/'
OUTPUT_FOLDER = '../data/output/'
STAMP_FOLDER = '../data/stamps/'

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


def insert_siret_on_every_pages(siret_str, file_handle):
    p=fitz.Point(500,20)
    for page in file_handle:
        page.insert_text(p, siret_str, color=(1,0,0))


def insert_images_and_siret(siret_str, input_name, output_name):
    input_file=DOCS_FOLDER+input_name
    output_file = OUTPUT_FOLDER+output_name

    file_handle = fitz.open(input_file)
    insert_siret_on_every_pages(siret_str, file_handle)
    insert_image(file_handle)

    file_handle.save(output_file)

insert_images_and_siret("83825502400021","doc_empty.pdf","withSiret.pdf")