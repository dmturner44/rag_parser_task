import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from langchain_parser import load_documents

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), '..', 'test_files')

ALL_FILES = [
    # PDFs
    "recipe_book.pdf",
    "empty.pdf",
    # Word
    "on_oura_data.docx",
    "empty.docx",
    # Excel
    "excel_calc.xlsx",
    "clinical_train.csv",
    "empty.xlsx",
    "0001-xlsx.xlsx",
    "0001-xlsx-nomagic.xlsx"
]

TEST_FILES = [
    "recipe_book.pdf",
    "0001-xlsx.xlsx"
]

@pytest.mark.parametrize("filenames", [TEST_FILES])
def test_load_documents_all(filenames):
    paths = [os.path.join(TEST_FILES_DIR, fname) for fname in filenames]
    docs = load_documents(paths)
    assert isinstance(docs, list)
    # For each non-empty file, ensure at least one doc with content and correct source
    for fname in filenames:
        if "empty" not in fname and "corrupted" not in fname:
            assert any(doc.page_content.strip() and doc.metadata.get("source", "").endswith(fname) for doc in docs)
    # Check metadata for all docs
    for doc in docs:
        assert "source" in doc.metadata

# Edge case: corrupted file
def test_corrupted_file():
    path = os.path.join(TEST_FILES_DIR, "corrupted.pdf")
    docs = load_documents([path])
    assert docs == []  
