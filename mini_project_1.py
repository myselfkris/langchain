import PyPDF2
import os
from sentence_transformers import SentenceTransformer, util
import numpy as np
import faiss
import nltk

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('punkt_tab')

# ---------- 1. Extract text from PDF ----------
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

# ---------- 2. Split and clean text ----------
def split_into_sentences(text):
    sentences = nltk.sent_tokenize(text)
    return [s.strip() for s in sentences if s.strip()]

# ---------- 3. Build FAISS index ----------
def build_faiss_index(sentences, model_name='all-MiniLM-L6-v2', threshold=0.75):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(sentences)

    # Merge similar sentences
    similarities = [util.cos_sim(embeddings[i], embeddings[i+1]).item() 
                    for i in range(len(embeddings)-1)]
    merged = []
    current = sentences[0]
    for i in range(1, len(sentences)):
        if similarities[i-1] > threshold:
            current += " " + sentences[i]
        else:
            merged.append(current)
            current = sentences[i]
    merged.append(current)

    merged_embeddings = model.encode(merged)
    dim = merged_embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(merged_embeddings))

    return model, index, merged

# ---------- 4. Ask question ----------
def ask_question(model, index, merged_sentences, k=3):
    while True:
        query = input("\nAsk your question (or type 'exit' to quit): ")
        if query.lower() in ['exit', 'quit']:
            break
        query_embedding = model.encode([query])
        D, I = index.search(np.array(query_embedding), k)
        print("\nTop relevant answers:\n")
        for idx in I[0]:
            print("•", merged_sentences[idx])
        print("-" * 60)

# ---------- MAIN ----------
if __name__ == "__main__":
    pdf_path = "UNIT II PROCESS SCHEDULING OS.pdf"  # Change as needed
    print("Extracting text...")
    text = extract_text_from_pdf(pdf_path)
    sentences = split_into_sentences(text)
    print(f"Total sentences: {len(sentences)}")

    print("Building FAISS index...")
    model, index, merged = build_faiss_index(sentences)

    print("✅ Ready! You can now ask questions about your PDF.")
    ask_question(model, index, merged)
