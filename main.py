from utils.insert_text_inside_forms import fill_pdf
from utils.insert_images_and_siret import insert_images_and_siret
from utils.extract_siret import extract_siret_as_string

# siret = extract_siret_as_string("doc_empty.pdf")

# fill_pdf("doc_empty.pdf","temp.pdf")
insert_images_and_siret("XXXXXXXXXXXXXXXXXXx", "temp.pdf", "output.pdf")
