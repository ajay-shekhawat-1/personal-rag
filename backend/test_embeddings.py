from app.services.embedding_service import create_embeddings


texts = [
    "Python is a programming language.",
    "Machine learning is a branch of artificial intelligence.",
    "Qdrant is a vector database.",
]


print("Creating embeddings...")

embeddings = create_embeddings(texts)

print("Number of embeddings:", len(embeddings))

for index, embedding in enumerate(embeddings):
    print(
        f"Embedding {index}: "
        f"dimension={len(embedding)}"
    )

print("\nFirst 5 values:")
print(embeddings[0][:5])