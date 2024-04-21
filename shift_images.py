import argparse
import base64
import os
import warnings
from io import BytesIO

from PIL import Image


def trans_per_img(img_path):
    """Converts image to a base64 string."""
    img = Image.open(img_path)
    img_buffer = BytesIO()
    img.save(img_buffer, format=img.format)
    byte_data = img_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    base64_str = base64_str.decode("utf-8")
    return base64_str


def extract_id(filename):
    """Extracts the numeric ID from the filename."""
    # Assuming the filename format is "Image14001003-4422.jpg"
    base_name = os.path.basename(filename)  # e.g., "Image14001003-4422.jpg"
    base_name = base_name.replace('.jpg', '')  # Remove the extension
    id_part = base_name.split('-')[-1]  # Split by '-' and take the last part
    prefix_part = base_name.split('-')[0][5:]  # Remove 'Image' and take the number
    return prefix_part + id_part  # Concatenate to form the full ID


def save_images_to_tsv(image_folder, val_count, train_dir, val_dir, only_val=0):
    """Saves images to .tsv files divided into train and validation sets."""
    files = [f for f in os.listdir(image_folder) if f.endswith('.jpg')]
    files.sort()  # Optional: sort files to maintain a consistent order
    train_files = files[val_count:]  # Remaining files go to train
    val_files = files[:val_count]  # First 'val_count' files go to validation

    # Function to write data to a file
    def write_to_file(files, filename):
        with open(filename, 'w') as f:
            for i, file in enumerate(files):
                if i % 100 == 0:
                    print(i)
                img_path = os.path.join(image_folder, file)
                img_id = extract_id(file)
                base64_img = trans_per_img(img_path)
                f.write(f"{img_id}\t{base64_img}\n")

    if only_val != 0 & val_count != 0:
        print('only valid!')
        write_to_file(val_files, val_dir)
        return
    # Write training and validation files
    if val_count != 0:
        print('prepare train!')
    else:
        print('prepare test!')
    write_to_file(train_files, train_dir)
    if val_count != 0:
        print('prepare valid!')
        write_to_file(val_files, val_dir)


warnings.filterwarnings('ignore')
parser = argparse.ArgumentParser()
parser.add_argument('--image_folder', type=str, default='K:\dataset\B题-数据\附件2\ImageData',
                    help='image_folder')
parser.add_argument('--save_dir', type=str, default="taidi_data/train_imgs.tsv",
                    help='save_dir')
parser.add_argument('--val_dir', type=str, default="taidi_data/valid_imgs.tsv",
                    help='save_dir')
parser.add_argument('--only_val', type=int, default=0,
                    help='save_dir')
parser.add_argument('--val_count', type=int, default=0,
                    help='val_count')
opts = parser.parse_args()

# Example usage
image_folder = opts.image_folder  # Set your image folder path
val_count = opts.val_count  # Set the number of validation images
save_images_to_tsv(image_folder, val_count, opts.save_dir, opts.val_dir, opts.only_val)
