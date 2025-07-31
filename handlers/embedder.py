from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
def create_vector_store(chunks):
    texts = [c["text"] for c in chunks]
    metadatas = [{"page": c["page"]} for c in chunks]
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    return FAISS.from_texts(texts, embeddings, metadatas=metadatas)

