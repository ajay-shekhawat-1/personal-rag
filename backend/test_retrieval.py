from app.services.embedding_service import create_embeddings
from app.services.qdrant_service import search_chunks


QUESTION = "What is this document about?"


print()
print("=" * 60)
print("QDRANT RETRIEVAL TEST")
print("=" * 60)


# -----------------------------------------
# 1. Create question embedding
# -----------------------------------------

print("\n1. Creating question embedding...")

query_embedding = create_embeddings(
    [QUESTION]
)[0]

print(
    f"Question vector dimension: "
    f"{len(query_embedding)}"
)


# -----------------------------------------
# 2. Search Qdrant
# -----------------------------------------

print("\n2. Searching Qdrant...")

results = search_chunks(
    query_embedding=query_embedding,
    user_id="default",
    limit=5,
)


print(
    f"Results returned: {len(results)}"
)


# -----------------------------------------
# 3. Display results
# -----------------------------------------

print("\n3. Retrieved chunks:")

for index, result in enumerate(results):

    print("\n" + "=" * 60)

    print(
        f"RESULT {index + 1}"
    )

    print("=" * 60)

    print(
        f"Score: {result.score}"
    )

    print(
        f"Source: "
        f"{result.payload.get('source_name')}"
    )

    print(
        f"Chunk ID: "
        f"{result.payload.get('chunk_id')}"
    )

    print()

    print(
        result.payload.get("text")
    )


print()
print("=" * 60)
print("RETRIEVAL TEST COMPLETE")
print("=" * 60)