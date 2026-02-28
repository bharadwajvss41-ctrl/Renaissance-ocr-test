import pytesseract
from PIL import Image
import os
import traceback

IMG_DIR = "/content/drive/MyDrive/RenAIssance/data/images"
GT_DIR = "/content/drive/MyDrive/RenAIssance/data/ground_truth"

PRED_RAW_DIR = "/content/drive/MyDrive/RenAIssance/data/predictions_raw"
PRED_CROP_DIR = "/content/drive/MyDrive/RenAIssance/data/predictions_cropped"

os.makedirs(PRED_RAW_DIR, exist_ok=True)
os.makedirs(PRED_CROP_DIR, exist_ok=True)

for book in os.listdir(GT_DIR):

    print("\n==============================")
    print(f"Processing book: {book}")

    book_gt_path = os.path.join(GT_DIR, book)
    book_img_path = os.path.join(IMG_DIR, book)

    raw_book_path = os.path.join(PRED_RAW_DIR, book)
    crop_book_path = os.path.join(PRED_CROP_DIR, book)

    os.makedirs(raw_book_path, exist_ok=True)
    os.makedirs(crop_book_path, exist_ok=True)

    for gt_file in os.listdir(book_gt_path):

        if not gt_file.endswith(".txt"):
            continue

        try:
            image_name = gt_file.replace(".txt", ".png")
            image_path = os.path.join(book_img_path, image_name)

            if not os.path.exists(image_path):
                print(f"Image missing: {image_name}")
                continue

            print(f"OCR on {image_name}")

            image = Image.open(image_path)

            # ===== RAW OCR =====
            raw_text = pytesseract.image_to_string(image, lang="spa")

            with open(os.path.join(raw_book_path, gt_file), "w", encoding="utf-8") as f:
                f.write(raw_text)

            # ===== CROPPED OCR =====
            width, height = image.size

            cropped = image.crop((
                int(width * 0.08),     # left margin cut
                int(height * 0.12),    # top margin cut
                int(width * 0.92),     # right margin cut
                int(height * 0.88)     # bottom margin cut
            ))

            cropped_text = pytesseract.image_to_string(cropped, lang="spa")

            with open(os.path.join(crop_book_path, gt_file), "w", encoding="utf-8") as f:
                f.write(cropped_text)

            print(f"Done: {image_name}")

        except Exception:
            traceback.print_exc()

print("\nOCR experiment completed.")