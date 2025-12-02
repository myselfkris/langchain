import streamlit as st
import PyPDF2
import nltk
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer, util

# Download NLTK data (only runs first time)
nltk.download('punkt')
nltk.download('punkt_tab')
# ---------- 1. Extract text from PDF ----------
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content + "\n"
    return text

# ---------- 2. Split and clean text ----------
def split_into_sentences(text):
    sentences = nltk.sent_tokenize(text)
    return [s.strip() for s in sentences if s.strip()]

# ---------- 3. Build FAISS index ----------
def build_faiss_index(sentences, model_name='all-MiniLM-L6-v2', threshold=0.75):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(sentences)

    # Merge similar consecutive sentences to improve context
    similarities = [
        util.cos_sim(embeddings[i], embeddings[i + 1]).item()
        for i in range(len(embeddings) - 1)
    ]
    merged = []
    current = sentences[0]
    for i in range(1, len(sentences)):
        if similarities[i - 1] > threshold:
            current += " " + sentences[i]
        else:
            merged.append(current)
            current = sentences[i]
    merged.append(current)

    merged_embeddings = model.encode(merged)
    dim = merged_embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(merged_embeddings).astype('float32'))

    return model, index, merged

# ---------- 4. Streamlit UI ----------
st.set_page_config(page_title="PDF Q&A App", layout="wide")
st.title("📚 PDF Question Answering App")
st.markdown("Upload a PDF, and then ask questions to search through its content intelligently.")

# File upload
uploaded_file = st.file_uploader("📎 Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    st.info("⏳ Extracting text from PDF...")
    text = extract_text_from_pdf(uploaded_file)
    sentences = split_into_sentences(text)
    st.success(f"✅ Extracted {len(sentences)} sentences from the PDF.")

    with st.spinner("🔍 Building semantic search index..."):
        model, index, merged_sentences = build_faiss_index(sentences)
    st.success("✅ Index built! You can now ask questions.")

    # Question input
    query = st.text_input("💬 Ask a question about the PDF:")
    k = st.slider("Number of answers", 1, 10, 3)

    if query:
        query_embedding = model.encode([query])
        D, I = index.search(np.array(query_embedding).astype('float32'), k)

        st.markdown("### 📌 Top relevant answers:")
        for idx in I[0]:
            st.write(f"- {merged_sentences[idx]}")

else:
    st.warning("📄 Please upload a PDF file to get started.")
