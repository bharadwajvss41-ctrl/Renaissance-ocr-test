from pdf2image import convert_from_path
import os

# === CHANGE THIS PATH IF NEEDED ===
PDF_DIR = "/content/drive/MyDrive/renAIssance_data/pdfs"
IMG_DIR = "/content/drive/MyDrive/renAIssance_data/images"

os.makedirs(IMG_DIR, exist_ok=True)

for pdf_file in os.listdir(PDF_DIR):
    if pdf_file.endswith(".pdf"):
        pdf_path = os.path.join(PDF_DIR, pdf_file)

        book_name = pdf_file.replace(".pdf", "")
        book_folder = os.path.join(IMG_DIR, book_name)
        os.makedirs(book_folder, exist_ok=True)

        print(f"Converting {pdf_file}...")

        pages = convert_from_path(pdf_path, dpi=300)

        for i, page in enumerate(pages):
            image_path = os.path.join(book_folder, f"page_{i+1:03d}.png")
            page.save(image_path, "PNG")

        print(f"Finished {pdf_file}")