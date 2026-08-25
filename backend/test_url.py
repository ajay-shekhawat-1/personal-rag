from app.services.document_service import extract_url


URL = "https://example.com"


print("Extracting website...")

text = extract_url(URL)

print("Characters extracted:", len(text))

print("\nFirst 1000 characters:")
print(text[:1000])