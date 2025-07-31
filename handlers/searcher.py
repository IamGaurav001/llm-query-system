from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

def create_vector_store(chunks):
    texts = [c["text"] for c in chunks]
    metadatas = [{"page": c["page"]} for c in chunks]
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    return FAISS.from_texts(texts, embeddings, metadatas=metadatas)

def search_similar_chunks(vectorstore, query, k=3):
    return vectorstore.similarity_search_with_score(query, k=k)
