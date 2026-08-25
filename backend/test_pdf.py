from app.services.document_loader import extract_text_from_pdf


PDF_PATH = "test_data/sample.pdf"


print("Reading PDF...")

text = extract_text_from_pdf(PDF_PATH)

print("\nPDF extraction successful!")
print("Characters extracted:", len(text))

print("\nFirst 1000 characters:")
print(text[:1000])
