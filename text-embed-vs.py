# convert the text files into embeddings 

# import the sentence transformer library
from sentence_transformers import SentenceTransformer

# load the pre- trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

# function to convert text to embeddings
def text_to_embeddings(text):
    embeddings = model.encode(text)
    return embeddings
text="Hello, this is a sample text to convert into embeddings.  Let's see how it works!"
embeddings = text_to_embeddings(text)


# store the embeddings in a file
import numpy as np  
np.save('text_embeddings.npy', embeddings)  
print("Embeddings saved to text_embeddings.npy")

# load the embeddings from the file
loaded_embeddings = np.load('text_embeddings.npy')  
print("Embeddings loaded from text_embeddings.npy")


# store the embeddings in a faisss database
import faiss
dimension = loaded_embeddings.shape[0]  # dimension of the embeddings
index = faiss.IndexFlatL2(dimension)  # build the index             
index.add(np.array([loaded_embeddings]))  # add the embeddings to the index
print("Embeddings added to the FAISS index")   
print("Total embeddings in the index:", index.ntotal)

#check the similarity between two texts
text2="This is another text to compare with the first one."
embeddings2 = text_to_embeddings(text2)
D, I = index.search(np.array([embeddings2]), k=83929)
  # search for the nearest neighbor
print("Distance:", D)   
print("Index of the nearest neighbor:", I)
print("Similarity score (lower is more similar):", I[0][0])



