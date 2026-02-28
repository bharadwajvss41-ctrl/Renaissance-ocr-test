import os
import evaluate

GT_DIR = "/content/drive/MyDrive/RenAIssance/data/ground_truth"
PRED_DIR = "/content/drive/MyDrive/RenAIssance/data/predictions"

cer_metric = evaluate.load("cer")
wer_metric = evaluate.load("wer")

all_gt = []
all_pred = []

for book in os.listdir(GT_DIR):

    gt_book_path = os.path.join(GT_DIR, book)
    pred_book_path = os.path.join(PRED_DIR, book)

    for file in os.listdir(gt_book_path):
        if file.endswith(".txt"):

            gt_path = os.path.join(gt_book_path, file)
            pred_path = os.path.join(pred_book_path, file)

            if not os.path.exists(pred_path):
                continue

            with open(gt_path, "r", encoding="utf-8") as f:
                gt_text = f.read()

            with open(pred_path, "r", encoding="utf-8") as f:
                pred_text = f.read()

            all_gt.append(gt_text)
            all_pred.append(pred_text)

cer = cer_metric.compute(predictions=all_pred, references=all_gt)
wer = wer_metric.compute(predictions=all_pred, references=all_gt)

print(f"\nCharacter Error Rate (CER): {cer:.4f}")
print(f"Word Error Rate (WER): {wer:.4f}")