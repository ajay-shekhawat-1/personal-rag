from app.services.document_loader import extract_text_from_pdf
from app.services.chunker import chunk_text


PDF_PATH = "test_data/sample.pdf"


print("Reading PDF...")

text = extract_text_from_pdf(PDF_PATH)

print("Characters extracted:", len(text))

print("\nCreating chunks...")

chunks = chunk_text(
    text,
    chunk_size=500,
    chunk_overlap=100,
)

print("Number of chunks:", len(chunks))

for index, chunk in enumerate(chunks, start=1):
    print("\n" + "=" * 60)
    print(f"CHUNK {index}")
    print("=" * 60)
    print(chunk)