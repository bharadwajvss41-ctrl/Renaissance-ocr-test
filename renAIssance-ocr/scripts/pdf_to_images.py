from pdf2image import convert_from_path, pdfinfo_from_path
import os
import traceback

PDF_DIR = "/content/drive/MyDrive/RenAIssance/data/pdfs"
IMG_DIR = "/content/drive/MyDrive/RenAIssance/data/images"

MAX_PAGES = 50   # 🔥 convert only first 50 pages

os.makedirs(IMG_DIR, exist_ok=True)

pdf_files = [f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]

print(f"Found {len(pdf_files)} PDF files")

for pdf_file in pdf_files:
    try:
        print("\n==============================")
        print(f"Processing: {pdf_file}")

        pdf_path = os.path.join(PDF_DIR, pdf_file)
        book_name = pdf_file.replace(".pdf", "")
        book_folder = os.path.join(IMG_DIR, book_name)
        os.makedirs(book_folder, exist_ok=True)

        # Get total pages
        info = pdfinfo_from_path(pdf_path)
        total_pages = info["Pages"]

        pages_to_convert = min(total_pages, MAX_PAGES)

        print(f"Total pages in PDF: {total_pages}")
        print(f"Will convert first {pages_to_convert} pages only")

        # Check already converted images
        existing_images = [
            f for f in os.listdir(book_folder) if f.endswith(".png")
        ]
        converted_pages = len(existing_images)

        print(f"Already converted pages: {converted_pages}")

        if converted_pages >= pages_to_convert:
            print("Required pages already converted. Skipping.")
            continue

        start_page = converted_pages + 1
        print(f"Resuming from page {start_page}")

        for page_number in range(start_page, pages_to_convert + 1):
            print(f"Converting page {page_number}/{pages_to_convert}")

            page = convert_from_path(
                pdf_path,
                dpi=200,  # 200 is stable and sufficient
                first_page=page_number,
                last_page=page_number
            )[0]

            image_path = os.path.join(book_folder, f"page_{page_number:03d}.png")
            page.save(image_path, "PNG")

        print(f"Finished {pdf_file}")

    except Exception as e:
        print("ERROR processing:", pdf_file)
        traceback.print_exc()

print("\nAll PDFs processed.")