from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_text(pages):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = []
    for p in pages:
        texts = splitter.split_text(p["text"])
        for t in texts:
            chunks.append({"text": t, "page": p["page"]})
    return chunks
