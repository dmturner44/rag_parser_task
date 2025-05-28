import os
import re
import string
from collections import Counter
from langchain_parser import load_documents
from difflib import SequenceMatcher

TEST_DIR = "DocBank_test_files"

# Helper to extract prefix up to the second dot
PREFIX_RE = re.compile(r"^([^.]+\.[^.]+)")

def get_prefix(filename):
    match = PREFIX_RE.match(filename)
    return match.group(1) if match else None

def file_to_text(path):
    docs = load_documents([path])
    return "\n".join(doc.page_content for doc in docs)

def extract_text_from_docbank(txt_path):
    lines = []
    with open(txt_path, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 10:
                text = parts[0]
                if text and text != '##LTFigure##':
                    lines.append(text)
    return ' '.join(lines)

def normalize_tokens(tokens):
    table = str.maketrans('', '', string.punctuation)
    return [t.lower().translate(table) for t in tokens if t.strip()]

def f1_bag_of_words(pred, truth):
    pred_tokens = normalize_tokens(pred.split())
    truth_tokens = normalize_tokens(truth.split())
    pred_counter = Counter(pred_tokens)
    truth_counter = Counter(truth_tokens)
    tp = sum((pred_counter & truth_counter).values())
    fp = sum((pred_counter - truth_counter).values())
    fn = sum((truth_counter - pred_counter).values())
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def main():
    files = os.listdir(TEST_DIR)
    file_map = {}
    for fname in files:
        prefix = get_prefix(fname)
        if not prefix:
            continue
        ext = os.path.splitext(fname)[1].lower()
        file_map.setdefault(prefix, {})[ext] = fname

    results = []
    for prefix, group in file_map.items():
        txt_file = group.get('.txt')
        pdf_file = group.get('.pdf')
        jpg_file = group.get('.jpg')
        if not txt_file:
            print(f"Skipping {prefix}: no ground truth .txt file")
            continue
        gt_text = extract_text_from_docbank(os.path.join(TEST_DIR, txt_file))
        # Save normalized ground truth text for comparison
        gt_tokens = normalize_tokens(gt_text.split())
        gt_text_norm = ' '.join(gt_tokens)
        with open(f"{prefix}_ground_truth.txt", "w", encoding="utf-8") as f:
            f.write(gt_text_norm)
        pdf_f1 = jpg_f1 = None
        pdf_sim = jpg_sim = None
        if pdf_file:
            try:
                pdf_text = file_to_text(os.path.join(TEST_DIR, pdf_file))
                pdf_tokens = normalize_tokens(pdf_text.split())
                pdf_text_norm = ' '.join(pdf_tokens)
                with open(f"{prefix}_pdf_parsed.txt", "w", encoding="utf-8") as f:
                    f.write(pdf_text_norm)
                pdf_f1 = f1_bag_of_words(pdf_text, gt_text)
                pdf_sim = similarity(pdf_text, gt_text)
                print(f"{prefix} PDF F1 (bag-of-words): {pdf_f1:.3f} (similarity: {pdf_sim:.3f})")
            except Exception as e:
                print(f"Error parsing PDF for {prefix}: {e}")
        if jpg_file:
            try:
                jpg_text = file_to_text(os.path.join(TEST_DIR, jpg_file))
                jpg_tokens = normalize_tokens(jpg_text.split())
                jpg_text_norm = ' '.join(jpg_tokens)
                with open(f"{prefix}_jpg_parsed.txt", "w", encoding="utf-8") as f:
                    f.write(jpg_text_norm)
                jpg_f1 = f1_bag_of_words(jpg_text, gt_text)
                jpg_sim = similarity(jpg_text, gt_text)
                print(f"{prefix} JPG F1 (bag-of-words): {jpg_f1:.3f} (similarity: {jpg_sim:.3f})")
            except Exception as e:
                print(f"Error parsing JPG for {prefix}: {e}")
        results.append({
            'prefix': prefix,
            'pdf_f1_bag_of_words': pdf_f1,
            'pdf_similarity': pdf_sim,
            'jpg_f1_bag_of_words': jpg_f1,
            'jpg_similarity': jpg_sim
        })
    # Saving results
    import json
    with open('parse_scores.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("\nResults saved to parse_scores.json")

if __name__ == "__main__":
    main() 