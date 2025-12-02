# given text splitt into chunks
def text_splitter(text, chunk_size=5, overlap=3):
    chunks=[]
    start=0
    while start<len(text):
        end=start+chunk_size
        chunk=text[start:end]
        chunks.append(chunk)
        start+=chunk_size-overlap
    return chunks

# given pdf text into chunks
import PyPDF2
def pdf_to_text(file_path):
    text = ""
    with open(file_path, 'rb') as file: 
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"          
    return text 

# Example usage
file_path = 'AI_30_Day_QA_Project_Roadmap.pdf' 
pdf_text = pdf_to_text(file_path)
chunks = text_splitter(pdf_text, chunk_size=15, overlap=10)
print(chunks)