import PyPDF2

# open PDF file in read-binary mode
with open( "","b") as pdf_file:
    reader = PyPDF2.PdfReader(pdf_file)  # create reader object
    text = ""
    for page in reader.pages:
        text += page.extract_text()  # extract text from each page

print(text)
