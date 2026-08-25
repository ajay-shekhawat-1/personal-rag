from app.services.embedding_service import create_embedding


text = "This is a test document for my personal RAG system."

vector = create_embedding(text)

print("Vector dimension:", len(vector))
print("First 5 values:", vector[:5])