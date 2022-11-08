import PyPDF2

# file = open("./folder/Doc.pdf", mode='rb')
file = open("Doc_full.pdf", mode='rb')

pdf_reader = PyPDF2.PdfFileReader(file)

numP = pdf_reader.numPages


page_one = pdf_reader.getPage(7)

file.close()
print(page_one.extractText())

print(numP)
