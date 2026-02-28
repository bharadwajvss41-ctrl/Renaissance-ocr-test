from docx import Document
import os

GT_DIR = "/content/drive/MyDrive/RenAIssance/data/ground_truth"

for book in os.listdir(GT_DIR):
    book_path = os.path.join(GT_DIR, book)

    if not os.path.isdir(book_path):
        continue

    for file in os.listdir(book_path):
        if file.endswith(".docx"):

            docx_path = os.path.join(book_path, file)
            txt_path = os.path.join(
                book_path, file.replace(".docx", ".txt")
            )

            print(f"Converting {docx_path}")

            doc = Document(docx_path)
            text = "\n".join([p.text for p in doc.paragraphs])

            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(text)

print("\nConversion complete.")