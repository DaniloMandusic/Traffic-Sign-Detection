import shutil
import os
from PIL import Image

def process_split(file_list, split, grouped, images_src, base_out):
    images_dst_dir = os.path.join(base_out, "images", split)
    labels_dst_dir = os.path.join(base_out, "labels", split)

    if os.path.exists(images_dst_dir):
        shutil.rmtree(images_dst_dir)
    if os.path.exists(labels_dst_dir):
        shutil.rmtree(labels_dst_dir)

    os.makedirs(images_dst_dir, exist_ok=True)
    os.makedirs(labels_dst_dir, exist_ok=True)

    for filename in file_list:
        filename = str(filename).strip()

        img_src = os.path.join(images_src, filename)
        img_dst = os.path.join(base_out, "images", split, filename)

        label_dst = os.path.join(
            base_out, "labels", split, filename.replace(".ppm", ".txt")
        )

        # DEBUG
        if not os.path.exists(img_src):
            print("Missing file:", repr(img_src))
            continue

        shutil.copy(img_src, img_dst)

        rows = grouped.get_group(filename)

        with open(label_dst, "w") as f:
            for _, row in rows.iterrows():
                f.write(
                    f"{row['class_id']} "
                    f"{row['x_center']:.6f} "
                    f"{row['y_center']:.6f} "
                    f"{row['width']:.6f} "
                    f"{row['height']:.6f}\n"
                )

def check_dataset_integrity(base_dir):
    """
    Checks YOLO dataset integrity:
    - matching image/label counts
    - missing pairs
    - empty label files
    """

    splits = ["train", "val", "test"]

    for split in splits:
        print(f"\n🔍 Checking split: {split}")

        img_dir = os.path.join(base_dir, "images", split)
        lbl_dir = os.path.join(base_dir, "labels", split)

        images = set(os.listdir(img_dir))
        labels = set(os.listdir(lbl_dir))

        # normalize names (remove extensions)
        img_names = set(os.path.splitext(f)[0] for f in images)
        lbl_names = set(os.path.splitext(f)[0] for f in labels)

        # mismatches
        missing_labels = img_names - lbl_names
        missing_images = lbl_names - img_names

        print(f"Images: {len(images)}")
        print(f"Labels: {len(labels)}")

        if missing_labels:
            print(f"Missing labels for {len(missing_labels)} images")
            print(list(missing_labels)[:5])

        if missing_images:
            print(f"Missing images for {len(missing_images)} labels")
            print(list(missing_images)[:5])

        if not missing_labels and not missing_images:
            print("Image-label pairing OK")

        # check empty label files
        empty_labels = []
        for lbl in labels:
            path = os.path.join(lbl_dir, lbl)
            if os.path.getsize(path) == 0:
                empty_labels.append(lbl)

        if empty_labels:
            print(f"Empty label files: {len(empty_labels)}")
            print(empty_labels[:5])
        else:
            print("No empty labels")

        # optional: check values range
        bad_lines = 0
        for lbl in labels:
            path = os.path.join(lbl_dir, lbl)
            with open(path, "r") as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) != 5:
                        bad_lines += 1
                        continue

                    _, x, y, w, h = parts
                    x, y, w, h = map(float, [x, y, w, h])

                    if not (0 <= x <= 1 and 0 <= y <= 1 and 0 <= w <= 1 and 0 <= h <= 1):
                        bad_lines += 1

        if bad_lines:
            print(f"Invalid label lines: {bad_lines}")
        else:
            print("Label values valid")

def convert_dataset_ppm_to_jpg(images_root):
    """
    Converts all .ppm images in YOLO dataset folders
    (train/val/test) to .jpg and deletes originals.
    """

    splits = ["train", "val", "test"]

    for split in splits:
        folder = os.path.join(images_root, split)

        if not os.path.exists(folder):
            print(f"Skipping missing folder: {folder}")
            continue

        print(f"\nProcessing: {folder}")

        for file in os.listdir(folder):
            if not file.lower().endswith(".ppm"):
                continue

            ppm_path = os.path.join(folder, file)
            jpg_name = os.path.splitext(file)[0] + ".jpg"
            jpg_path = os.path.join(folder, jpg_name)

            try:
                with Image.open(ppm_path) as img:
                    rgb_img = img.convert("RGB")
                    rgb_img.save(jpg_path, "JPEG", quality=95)

                os.remove(ppm_path)  # remove original

                print(f"Converted: {file} → {jpg_name}")

            except Exception as e:
                print(f"FAILED: {file} | {e}")