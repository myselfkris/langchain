# convert pdf files to text
import PyPDF2
import os
from sentence_transformers import SentenceTransformer,util
import numpy as np
import faiss
import nltk
nltk.download('punkt')
nltk.download('punkt_tab') 


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
# split text into sentence
sentences = nltk.sent_tokenize(text)
print(f"Number of sentences: {len(sentences)}")

# compute embeddings for each sentence
model=SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(sentences)

#compute similarity between consecutive sentences
similarities=[util.cos_sim(embeddings[i],embeddings[i+1]).item() for i in range(len(embeddings)-1)]
print("hi")
print(f"Similarities between consecutive sentences: {similarities}")
# based on similarity threshold, merge sentences
threshold=0.75
merged_sentences=[]
current_sentence=sentences[0]
for i in range(1,len(sentences)):
    if similarities[i-1]>threshold:
        current_sentence+=" "+sentences[i]
    else:
        merged_sentences.append(current_sentence)
        current_sentence=sentences[i]
merged_sentences.append(current_sentence)
print(f"Number of merged sentences: {len(merged_sentences)}")
# create embeddings for merged sentences
merged_embeddings=model.encode(merged_sentences)    
print(f"Merged embeddings shape: {merged_embeddings.shape}")  
# save merged embeddings to faiss index
dimension = merged_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)  # L2 distance index   
index.add(np.array(merged_embeddings))  # add embeddings to index
faiss.write_index(index, 'faiss_index.index')
print("FAISS index saved as 'faiss_index.index'")
# save merged sentences to a text file
with open('merged_sentences.txt', 'w', encoding='utf-8') as f:
    for sentence in merged_sentences:
        f.write(sentence + "\n")
#get user query
query="What is CPU scheduling?"
query_embedding=model.encode([query])
# load faiss index
index = faiss.read_index('faiss_index.index')
# search for similar sentences
k=1
D, I = index.search(np.array(query_embedding), k)  # D is distances, I is indices
print(f"Top {k} similar sentences indices: {I}")
print(f"Top {k} similar sentences distances: {D}")
for idx in I[0]:
    print(merged_sentences[idx])
print("done")



