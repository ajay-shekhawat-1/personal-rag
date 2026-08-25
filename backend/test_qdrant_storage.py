from uuid import uuid4

from app.services.document_service import extract_text
from app.services.chunking_service import chunk_text
from app.services.embedding_service import create_embeddings
from app.services.qdrant_service import (
    create_collection_if_not_exists,
    insert_chunks,
)


FILE_PATH = "test.pdf"


print()
print("=" * 60)
print("QDRANT STORAGE TEST")
print("=" * 60)


# -----------------------------------------
# 1. Create collection
# -----------------------------------------

print("\n1. Checking Qdrant collection...")

result = create_collection_if_not_exists()

print(
    f"Collection: {result['collection']}"
)

print(
    f"Created now: {result['created']}"
)


# -----------------------------------------
# 2. Extract document
# -----------------------------------------

print("\n2. Extracting document...")

text = extract_text(FILE_PATH)

print(
    f"Characters extracted: {len(text)}"
)


# -----------------------------------------
# 3. Chunk document
# -----------------------------------------

print("\n3. Creating chunks...")

chunks = chunk_text(text)

print(
    f"Chunks created: {len(chunks)}"
)


# -----------------------------------------
# 4. Create embeddings
# -----------------------------------------

print("\n4. Creating embeddings...")

embeddings = create_embeddings(chunks)

print(
    f"Embeddings created: {len(embeddings)}"
)

print(
    f"Vector dimension: {len(embeddings[0])}"
)


# -----------------------------------------
# 5. Generate document ID
# -----------------------------------------

document_id = str(uuid4())


# -----------------------------------------
# 6. Store in Qdrant
# -----------------------------------------

print("\n5. Uploading vectors to Qdrant...")

stored = insert_chunks(
    chunks=chunks,
    embeddings=embeddings,
    source_name=FILE_PATH,
    source_type="pdf",
    document_id=document_id,
    user_id="default",
)


print(
    f"Vectors stored: {stored}"
)

print(
    f"Document ID: {document_id}"
)


print()
print("=" * 60)
print("QDRANT STORAGE SUCCESS")
print("=" * 60)