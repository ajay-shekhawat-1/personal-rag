from app.services.llm_service import generate_answer


question = "What is Python?"

context = """
Python is a high-level programming language.
It is widely used for data science, machine learning,
web development, automation, and artificial intelligence.
"""


print("Sending request to Groq...")

answer = generate_answer(
    question=question,
    context=context,
)


print("\nAnswer:")
print(answer)