import argparse
import json
import os
import warnings

import csv


def extract_id_from_name(filename):
    """Extracts the numeric ID from the image filename."""
    base_name = os.path.basename(filename)  # e.g., "Image14001001-0000.jpg"
    base_name = base_name.replace('.jpg', '')  # Remove the extension
    id_part = base_name.split('-')[-1]  # Split by '-' and take the last part
    prefix_part = base_name.split('-')[0][5:]  # Remove 'Image' and take the number
    return int(prefix_part + id_part)  # Return as integer


def load_image_splits(tsv_path):
    """Load image ids from a tsv file."""
    with open(tsv_path, 'r') as file:
        return [int(line.split('\t')[0]) for line in file.readlines()]


def load_data_csv(csv_path):
    """Load captions and their associated image IDs from a CSV file."""
    data = {}
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)  # 使用默认的逗号分隔符
        next(reader)  # Skip the header row
        for row in reader:
            if len(row) == 2:  # Ensure row has exactly two elements
                img_id = extract_id_from_name(row[0])  # Extract ID from the filename
                data[img_id] = row[1]  # Map the ID to its caption
    return data


def save_jsonl(data, filename, image_ids_set):
    """Save text data to a JSONL file filtering by image IDs."""
    with open(filename, 'w', encoding='utf-8') as f:
        for img_id, caption in data.items():
            if img_id in image_ids_set:
                entry = {
                    "text_id": img_id,
                    "text": caption,
                    "image_ids": [img_id]
                }
                json.dump(entry, f, ensure_ascii=False)
                f.write('\n')


warnings.filterwarnings('ignore')
parser = argparse.ArgumentParser()
parser.add_argument('--data_csv_path', type=str, default='csv/ImageWordData.csv',
                    help='data_csv_path')
parser.add_argument('--train_tsv_path', type=str, default='taidi_data/train_imgs.tsv',
                    help='train_tsv_path')
parser.add_argument('--val_tsv_path', type=str, default='taidi_data/valid_imgs.tsv',
                    help='val_tsv_path')
opts = parser.parse_args()
# Paths to your files
data_csv_path = opts.data_csv_path  # Your data.csv path
train_tsv_path = opts.train_tsv_path  # Generated train_imgs.tsv
val_tsv_path = opts.val_tsv_path  # Generated val_imgs.tsv
# Load data
data = load_data_csv(data_csv_path)
train_image_ids = set(load_image_splits(train_tsv_path))
val_image_ids = set(load_image_splits(val_tsv_path))
# Save to JSONL files
save_jsonl(data, 'taidi_data/train_texts.jsonl', train_image_ids)
save_jsonl(data, 'taidi_data/valid_texts.jsonl', val_image_ids)
