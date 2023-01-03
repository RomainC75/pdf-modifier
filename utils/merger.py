from PyPDF2 import PdfMerger, PdfFileReader, PdfFileWriter
import fitz
from glob import glob
import dotenv
config = dotenv.dotenv_values()
from pdfrw import PdfReader, PdfWriter
# import aspose.words as aw

def PDFMerger (merge_folder):
    merger = PdfMerger()
    # pdfPaths = glob('../data/merge/'+'*.pdf')
    pdfPaths = glob(merge_folder+'*.pdf')
    for pdf_path in pdfPaths:
        print('path :',pdf_path)
        merger.append(pdf_path)
    merger.write("merged-pdf.pdf")
    merger.close()
# PDFMerger('../data/output/LACHOPE_AER_10_2022/01_merge/')

def PDFrw_Merger(merge_folder):
    writer = PdfWriter()
    pdfPaths = glob(merge_folder+'*.pdf')
    for inpfn in pdfPaths:
        writer.addpages(PdfReader(inpfn).pages)
    writer.write('MERGED.pdf')
# PDFrw_Merger('../data/output/LACHOPE_AER_10_2022/01_merge/')

# ===============================
# ===>>>
def merge_pdfs(merge_folder):
    pdfPaths = glob(merge_folder['folder_path']+'/*.pdf')
    pdf_writer = PdfFileWriter()
    for path in pdfPaths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open(f'{merge_folder["folder_path"]}/{merge_folder["folder_name"]}', 'wb') as out:
        pdf_writer.write(out)

# merge_pdfs('../data/output/LACHOPE_AER_10_2022/01_merge/')

# ===============================

# def PDF_aspose_merger():
#     # pdfPaths = glob('../data/merge/'+'*.pdf')
#     pdfPaths = glob('../data/output/LACHOPE_AER_10_2022/01_merge/'+'*.pdf')
    
#     output = aw.Document()
#     # Remove all content from the destination document before appending.
#     output.remove_all_children()

#     for pdf_path in pdfPaths:
#         print('path :',pdf_path)
#         input = aw.Document(pdf_path)
#         output.append_document(input, aw.ImportFormatMode.KEEP_SOURCE_FORMATTING)

#     output.save("MERGED.pdf")

# PDF_aspose_merger()

