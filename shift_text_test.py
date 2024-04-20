import argparse
import json
import warnings

import csv


def extract_text_id(text_id):
    """Extracts the numeric part from the text ID."""
    # Assuming text_id format is "Word-1000004254"
    return int(text_id.split('-')[1])  # Split by '-' and convert to integer


def load_test_data_csv(csv_path):
    """Load text IDs and captions from a CSV file for the test dataset."""
    data = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)  # 默认逗号分隔符
        next(reader)  # Skip the header row
        for row in reader:
            if len(row) == 2:
                text_id = extract_text_id(row[0])
                caption = row[1]
                data.append({"text_id": text_id, "text": caption, "image_ids": []})
    return data


def save_jsonl(data, filename):
    """Save data to a JSONL file."""
    with open(filename, 'w', encoding='utf-8') as f:
        for entry in data:
            json.dump(entry, f, ensure_ascii=False)
            f.write('\n')


warnings.filterwarnings('ignore')
parser = argparse.ArgumentParser()
parser.add_argument('--data_csv_path', type=str, default='csv/ImageWordData.csv',
                    help='data_csv_path')
parser.add_argument('--test_tsv_path', type=str, default='taidi_data/train_imgs.tsv',
                    help='test_tsv_path')
parser.add_argument('--save_jsonl_path', type=str, default='taidi_data/test_texts.jsonl',
                    help='save_jsonl_path')
opts = parser.parse_args()
# Paths to your files
data_csv_path = opts.data_csv_path  # Your data.csv path
test_tsv_path = opts.test_tsv_path
# Paths to your files
# Load data
data = load_test_data_csv(data_csv_path)
jsonl_filename = opts.save_jsonl_path
save_jsonl(data, jsonl_filename)
