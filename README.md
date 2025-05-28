## Project Overview
This project provides robust document parsing and evaluation tools for PDFs, Word, and Excel files, with a focus on supporting RAG-based AI systems and benchmarking parser performance using DocBank-style test cases. It includes unified parsing, OCR fallback, and scoring scripts for fair evaluation against annotated ground truth.

## System Requirements
This project requires the following system tools:

- **Poppler** (for PDF parsing)
    - Windows: [Download here](https://github.com/oschwartz10612/poppler-windows/releases/) and add the `bin` directory to your `PATH`.
    - macOS: `brew install poppler`
    - Linux: `sudo apt-get install poppler-utils`
- **Tesseract OCR** (for image and scanned PDF OCR)
    - Windows: [Download here](https://github.com/UB-Mannheim/tesseract/wiki) and add the install directory to your `PATH`.
    - macOS: `brew install tesseract`
    - Linux: `sudo apt-get install tesseract-ocr`

## Python Requirements
Install all Python dependencies with:
```bash
pip install -r requirements.txt
```

## Usage

### Parsing Documents
Use the provided `langchain_parser.py` functions to parse documents. Example:
```python
from langchain_parser import load_pdf, save_parsed_documents

docs = load_pdf("DocBank_test_files/100.tar_1705.04261.gz_main_black.pdf")
save_parsed_documents(docs, "DocBank_1.txt", "DocBank_1_meta.jsonl")
```
Or use `load_documents([path])` for unified parsing of PDFs, images, Word, and Excel files.

### Scoring Parser Performance
To evaluate your parser against DocBank-style ground truth:
```bash
python parse_scoring_script.py
```
This will compare parsed output to the text extracted from DocBank annotation files and report F1 and similarity scores. Results are saved to `parse_scores.json`.

### DocBank Test File Format
DocBank `.txt` files are tab-separated annotation files. The scoring script extracts the 9th column (text) from each line, ignoring layout and label info, to create a fair ground truth for text comparison.

## Running Tests
To run the parser test:
```bash
pytest tests/test_langchain_parser.py
```

## Troubleshooting
- **Poppler or Tesseract not found:** Ensure their install directories are in your system `PATH` and restart your terminal.
- **Missing Python modules:** Run `pip install -r requirements.txt`.
- **FileNotFoundError:** Check that your data files and test files are in the correct directories.
- **Import errors:** Run scripts from the project root directory.



