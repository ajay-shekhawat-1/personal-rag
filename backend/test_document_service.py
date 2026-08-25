from app.services.document_service import extract_text


FILE_PATH = "test.doc"


print("Extracting document...")

text = extract_text(FILE_PATH)

print("\n========== EXTRACTED TEXT ==========\n")
print(text)

print("\n====================================")
print("Characters:", len(text))