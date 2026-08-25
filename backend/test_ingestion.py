from app.services.document_service import extract_text
from app.services.chunking_service import chunk_text
from app.services.embedding_service import create_embeddings


FILE_PATH = "test.pdf"


print("1. Extracting document...")

text = extract_text(FILE_PATH)

print("Characters:", len(text))


print("\n2. Creating chunks...")

chunks = chunk_text(text)

print("Chunks:", len(chunks))


print("\n3. Creating embeddings...")

embeddings = create_embeddings(chunks)

print("Embeddings:", len(embeddings))


print("\n4. Checking dimensions...")

for index, embedding in enumerate(embeddings[:5]):
    print(
        f"Chunk {index}: "
        f"{len(embedding)} dimensions"
    )


print("\nPipeline test completed successfully.")