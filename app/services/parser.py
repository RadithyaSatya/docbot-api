import re
from typing import List
import fitz


def extract_text_from_pdf(file_path: str)->str:
    doc = fitz.open(file_path)
    text = ""
    for page in doc: 
        text += page.get_text()
    return text

def extract_text_from_txt(file_path: str)->str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
    
def split_text_to_chunks(text: str, max_length: int = 500)->List[str]:
    paragraph = re.split(r"\n{2,}", text)
    chunks = []
    current_chunk = ""

    for para in paragraph:
        if len(current_chunk) + len(para) <= max_length:
            current_chunk+=" "+para
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para

    if current_chunk: 
        chunks.append(current_chunk.strip())
    
    return chunks