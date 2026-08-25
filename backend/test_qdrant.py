from app.services.embedding_service import create_embedding
from app.services.qdrant_service import (
    insert_test_vector,
    search_test_vector,
)


text = "Python is a programming language used for data science."

print("Creating embedding...")

vector = create_embedding(text)

print("Vector dimension:", len(vector))

print("Inserting vector into Qdrant...")

insert_result = insert_test_vector(
    vector=vector,
    text=text,
)

print("Insert result:")
print(insert_result)

print("\nSearching Qdrant...")

results = search_test_vector(vector)

for result in results:
    print("\nScore:", result.score)
    print("Payload:", result.payload)