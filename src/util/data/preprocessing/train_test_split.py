import shutil
import os

def process_split(file_list, split, grouped, images_src, base_out):
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