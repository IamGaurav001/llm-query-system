import fitz  

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    return [{"text": page.get_text(), "page": i+1} for i, page in enumerate(doc)]
