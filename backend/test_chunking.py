from app.services.document_service import extract_text
from app.services.chunking_service import chunk_text


FILE_PATH = "test.pdf"


print("Extracting document...")

text = extract_text(FILE_PATH)

print("Characters extracted:", len(text))

print("\nCreating chunks...")

chunks = chunk_text(text)

print("Number of chunks:", len(chunks))


for index, chunk in enumerate(chunks[:5]):
    print("\n" + "=" * 60)
    print(f"CHUNK {index}")
    print("=" * 60)
    print(chunk[:500])