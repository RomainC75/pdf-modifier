from PyPDF2 import PdfMerger
from glob import glob
import dotenv
config = dotenv.dotenv_values()

merger = PdfMerger()

pdfPaths = glob('../data/merge/'+'*.pdf')

for pdf_path in pdfPaths:
    print('path :',pdf_path)
    merger.append(pdf_path)

merger.write("merged-pdf.pdf")
merger.close()