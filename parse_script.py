from langchain_parser import load_documents, save_parsed_documents

# Select your doc to parse here
doc_to_parse = "DocBank_test_files/100.tar_1705.04261.gz_main_black.pdf" 
# Choose a name to save as
save_name = "DocBank_1"

with open(doc_to_parse, "rb") as f:
    header = f.read(5)
    print(header)

docs = load_documents([doc_to_parse])

# Use save_name for both output files
text_path = f"{save_name}.txt"
meta_path = f"{save_name}_meta.jsonl"

save_parsed_documents(docs, text_path, meta_path)
print(f"Saved: {text_path}, {meta_path}")