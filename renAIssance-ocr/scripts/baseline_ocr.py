import pytesseract
from PIL import Image
import os

IMG_DIR = "/content/drive/MyDrive/RenAIssance/data/images"
GT_DIR = "/content/drive/MyDrive/RenAIssance/data/ground_truth"
PRED_DIR = "/content/drive/MyDrive/RenAIssance/data/predictions"

os.makedirs(PRED_DIR, exist_ok=True)

for book in os.listdir(GT_DIR):

    book_gt_path = os.path.join(GT_DIR, book)
    book_img_path = os.path.join(IMG_DIR, book)
    book_pred_path = os.path.join(PRED_DIR, book)

    os.makedirs(book_pred_path, exist_ok=True)

    print(f"\nProcessing book: {book}")

    for gt_file in os.listdir(book_gt_path):
        if gt_file.endswith(".txt"):

            image_name = gt_file.replace(".txt", ".png")
            image_path = os.path.join(book_img_path, image_name)

            if not os.path.exists(image_path):
                print(f"Image not found: {image_name}")
                continue

            image = Image.open(image_path)

            # You may change language if needed
            text = pytesseract.image_to_string(image, lang="spa")

            output_path = os.path.join(book_pred_path, gt_file)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)

            print(f"OCR done for {image_name}")

print("\nBaseline OCR completed.")