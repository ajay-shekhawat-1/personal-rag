import textract

FILE_PATH = "test.doc"

print("Reading DOC file...")

text = textract.process(FILE_PATH)

text = text.decode("utf-8", errors="ignore")

print("\nExtracted text:")
print(text)

print("\nCharacter count:", len(text))