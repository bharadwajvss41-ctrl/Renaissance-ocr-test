from pdf2image import convert_from_path
import os
import traceback

PDF_DIR = "/content/drive/MyDrive/RenAIssance/data/pdfs"
IMG_DIR = "/content/drive/MyDrive/RenAIssance/data/images"

print("Checking directories...")
print("PDF_DIR exists:", os.path.exists(PDF_DIR))
print("IMG_DIR exists:", os.path.exists(IMG_DIR))

os.makedirs(IMG_DIR, exist_ok=True)

pdf_files = os.listdir(PDF_DIR)
print(f"Found {len(pdf_files)} files in PDF_DIR")

for pdf_file in pdf_files:
    if not pdf_file.endswith(".pdf"):
        print(f"Skipping non-pdf file: {pdf_file}")
        continue

    try:
        pdf_path = os.path.join(PDF_DIR, pdf_file)
        print("\n==============================")
        print(f"Processing file: {pdf_file}")
        print(f"Full path: {pdf_path}")
        print("File exists:", os.path.exists(pdf_path))

        book_name = pdf_file.replace(".pdf", "")
        book_folder = os.path.join(IMG_DIR, book_name)
        os.makedirs(book_folder, exist_ok=True)

        print("Starting PDF conversion...")

        pages = convert_from_path(pdf_path, dpi=300)

        print(f"Total pages detected: {len(pages)}")

        for i, page in enumerate(pages):
            image_path = os.path.join(book_folder, f"page_{i+1:03d}.png")
            page.save(image_path, "PNG")

            if (i + 1) % 5 == 0:
                print(f"Saved {i+1} pages so far...")

        print(f"Finished {pdf_file}")

    except Exception as e:
        print("ERROR processing:", pdf_file)
        traceback.print_exc()
        continue

print("\nAll PDFs processed.")