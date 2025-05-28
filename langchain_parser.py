from langchain_community.document_loaders import (
    PyPDFLoader, UnstructuredPDFLoader,
    UnstructuredWordDocumentLoader, Docx2txtLoader,
    UnstructuredExcelLoader
)
from langchain.schema import Document
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def ocr_pdf_to_document(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)
    return [Document(page_content=text, metadata={"source": pdf_path, "method": "ocr"})]

def load_pdf(path):
    try:
        docs = PyPDFLoader(path).load()
        if docs and any(doc.page_content.strip() for doc in docs):
            return docs
    except Exception:
        pass
    try:
        docs = UnstructuredPDFLoader(path).load()
        if docs and any(doc.page_content.strip() for doc in docs):
            return docs
    except Exception as e:
        print(f"PDF parsing failed for {path}: {e}")
    # OCR fallback
    print(f"Falling back to OCR for {path}")
    try:
        return ocr_pdf_to_document(path)
    except Exception as e:
        print(f"OCR failed for {path}: {e}")
        return []

def load_word(path):
    try:
        return UnstructuredWordDocumentLoader(path).load()
    except Exception:
        try:
            return Docx2txtLoader(path).load()
        except Exception as e:
            print(f"Word parsing failed for {path}: {e}")
            return []

def load_excel(path):
    try:
        return UnstructuredExcelLoader(path).load()
    except Exception as e:
        print(f"Excel parsing failed for {path}: {e}")
        return []

def ocr_image_to_document(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return [Document(page_content=text, metadata={"source": image_path, "method": "ocr_image"})]

def load_documents(file_paths):
    docs = []
    for path in file_paths:
        ext = os.path.splitext(path)[1].lower()
        if ext == ".pdf":
            docs.extend(load_pdf(path))
        elif ext in [".docx", ".doc"]:
            docs.extend(load_word(path))
        elif ext in [".xlsx", ".xls"]:
            docs.extend(load_excel(path))
        elif ext in [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif"]:
            docs.extend(ocr_image_to_document(path))
        else:
            print(f"Unsupported file type: {path}")
    # Post-processing: remove empty docs, clean text, etc.
    docs = [doc for doc in docs if doc.page_content.strip()]
    return docs

def save_parsed_documents(docs, text_path, meta_path):
    import json
    with open(text_path, 'w', encoding='utf-8') as text_f, open(meta_path, 'w', encoding='utf-8') as meta_f:
        for doc in docs:
            text_f.write(doc.page_content)
            text_f.write("\n\n--- PAGE BREAK ---\n\n")
            json.dump({"content": doc.page_content, "metadata": doc.metadata}, meta_f, ensure_ascii=False)
            meta_f.write("\n")