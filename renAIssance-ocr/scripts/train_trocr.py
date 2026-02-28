import os
import torch
from PIL import Image
from datasets import Dataset
from transformers import (
    TrOCRProcessor,
    VisionEncoderDecoderModel,
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments,
    default_data_collator
)
import evaluate

IMG_DIR = "/content/drive/MyDrive/RenAIssance/data/images"
GT_DIR = "/content/drive/MyDrive/RenAIssance/data/ground_truth"

# ======================
# 1. Load image-text pairs
# ======================

data = []

for book in os.listdir(GT_DIR):
    gt_book_path = os.path.join(GT_DIR, book)
    img_book_path = os.path.join(IMG_DIR, book)

    for file in os.listdir(gt_book_path):
        if file.endswith(".txt"):
            image_path = os.path.join(img_book_path, file.replace(".txt", ".png"))
            text_path = os.path.join(gt_book_path, file)

            if os.path.exists(image_path):
                with open(text_path, "r", encoding="utf-8") as f:
                    text = f.read()

                data.append({
                    "image_path": image_path,
                    "text": text
                })

print("Total samples:", len(data))

dataset = Dataset.from_list(data)

# ======================
# 2. Train/Validation split
# ======================

dataset = dataset.train_test_split(test_size=0.2, seed=42)
train_ds = dataset["train"]
val_ds = dataset["test"]

print("Train size:", len(train_ds))
print("Val size:", len(val_ds))

# ======================
# 3. Load Processor & Model
# ======================

processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-printed")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-printed")

model.config.decoder_start_token_id = processor.tokenizer.cls_token_id
model.config.pad_token_id = processor.tokenizer.pad_token_id
model.config.eos_token_id = processor.tokenizer.sep_token_id
model.config.vocab_size = model.config.decoder.vocab_size

model.config.max_length = 512
model.config.early_stopping = True
model.config.no_repeat_ngram_size = 3
model.config.length_penalty = 2.0
model.config.num_beams = 4

# ======================
# 4. Preprocessing
# ======================

def preprocess(example):
    image = Image.open(example["image_path"]).convert("RGB")
    pixel_values = processor(images=image, return_tensors="pt").pixel_values[0]
    labels = processor.tokenizer(
        example["text"],
        padding="max_length",
        max_length=512,
        truncation=True
    ).input_ids

    return {
        "pixel_values": pixel_values,
        "labels": labels
    }

train_ds = train_ds.map(preprocess, remove_columns=train_ds.column_names)
val_ds = val_ds.map(preprocess, remove_columns=val_ds.column_names)

# ======================
# 5. Metrics
# ======================

cer_metric = evaluate.load("cer")

def compute_metrics(pred):
    pred_ids = pred.predictions
    label_ids = pred.label_ids

    pred_str = processor.batch_decode(pred_ids, skip_special_tokens=True)
    label_ids[label_ids == -100] = processor.tokenizer.pad_token_id
    label_str = processor.batch_decode(label_ids, skip_special_tokens=True)

    cer = cer_metric.compute(predictions=pred_str, references=label_str)

    return {"cer": cer}

# ======================
# 6. Training Arguments
# ======================

training_args = Seq2SeqTrainingArguments(
    output_dir="./trocr_output",
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    logging_strategy="epoch",
    num_train_epochs=15,
    learning_rate=5e-5,
    weight_decay=0.01,
    save_total_limit=2,
    predict_with_generate=True,
    fp16=torch.cuda.is_available(),
    load_best_model_at_end=True
)

# ======================
# 7. Trainer
# ======================

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=train_ds,
    eval_dataset=val_ds,
    data_collator=default_data_collator,
    tokenizer=processor.feature_extractor,
    compute_metrics=compute_metrics
)

trainer.train()

trainer.save_model("./trocr_finetuned")