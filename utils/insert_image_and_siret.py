# install PyMuPDF
import fitz

def insert_image(input_file, output_file):

    signature = "./data/"+"signature.png"
    stamp = "./data/"+"stamp.png"

    # define the position (upper-right corner)
    signature_rectangle = fitz.Rect(30,520,190,610)
    stamp_rectangle = fitz.Rect(400,520,550,610)

    # retrieve the first page of the PDF
    file_handle = fitz.open(input_file)
    first_page = file_handle[7]

    # an image file
    signature_img = open(signature, "rb").read()
    stamp_img = open(stamp, "rb").read()
    img_xref = 0

    # add the image
    # first_page.insert_image(signature_rectangle, fileName=signature)
    first_page.insert_image(signature_rectangle, stream=signature_img , xref=img_xref)
    first_page.insert_image(stamp_rectangle, stream=stamp_img , xref=img_xref)

    file_handle.save("./output/"+output_file)


def insert_siret_on_every_pages(input_file, output_file):
    file_handle = fitz.open(input_file)
    for page in file_handle:
        #insert text
        pass
    



insert_image("doc.pdf","output.pdf")
insert_siret_on_every_pages("doc.pdf","output.pdf")