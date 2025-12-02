# convert pdf files into embeddings
import PyPDF2
import os   
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
# function to extract text from pdf
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text
pdf_path = 'UNIT II PROCESS SCHEDULING OS.pdf'  # replace with your PDF file path
text = extract_text_from_pdf(pdf_path)
print(f"Extracted text length: {len(text)} characters")

# split text into chunks
def split_text_into_chunks(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
        if i + chunk_size >= len(words):
            break
    return chunks
chunks = split_text_into_chunks(text)
print(f"Number of chunks: {len(chunks)}")

# create a chunks based on semantic similarity
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(chunks)   
print(f"Embeddings shape: {embeddings.shape}")  
# save embeddings to faiss index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)  # L2 distance index
index.add(np.array(embeddings))  # add embeddings to index
faiss.write_index(index, 'faiss_index.index')
print("FAISS index saved as 'faiss_index.index'")
# save chunks to a text file
with open('chunks.txt', 'w', encoding='utf-8') as f:
    for chunk in chunks:
        f.write(chunk.replace('\n', ' ') + '\n---\n')  # separate chunks by ---
print("Chunks saved to 'chunks.txt'")       
# Now you have a FAISS index and corresponding text chunks saved for later use. 
# You can load the index and chunks later for retrieval tasks.
# You can load the index and chunks later for retrieval tasks.  
# Load FAISS index      

index = faiss.read_index('faiss_index.index')
# Load chunks       
with open('chunks.txt', 'r', encoding='utf-8') as f:
    chunks = f.read().split('\n---\n')
print(f"Loaded {len(chunks)} chunks from 'chunks.txt'")
# Example query
query = "What is process scheduling in operating systems?"

query_embedding = model.encode([query])
D, I = index.search(np.array(query_embedding), k=3)  # retrieve top 3 similar chunks
print("Top 3 similar chunks:")
for i in I[0]:
    print(chunks[i])
    print("-----")









