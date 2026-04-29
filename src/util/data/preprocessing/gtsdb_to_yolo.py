import pandas as pd
from PIL import Image
import os

def gtsdb_to_yolo(df_gtsdb, images_dir):
    """
    Convert GTSDB dataframe (no header) to YOLO format using PIL.

    Args:
        df_gtsdb: DataFrame with columns:
                  0=filename, 1=x1, 2=y1, 3=x2, 4=y2, 5=class_id
        images_dir: path to directory with images

    Returns:
        DataFrame with columns:
        [filename, class_id, x_center, y_center, width, height]
    """

    records = []
    size_cache = {}

    for i in range(len(df_gtsdb)):
        row = df_gtsdb.iloc[i]

        filename = row.iloc[0]
        x1 = row.iloc[1]
        y1 = row.iloc[2]
        x2 = row.iloc[3]
        y2 = row.iloc[4]

        # get image size (with caching)
        if filename not in size_cache:
            img_path = os.path.join(images_dir, filename)

            with Image.open(img_path) as img:
                w, h = img.size  # PIL gives (width, height)

            size_cache[filename] = (w, h)
        else:
            w, h = size_cache[filename]

        # convert to YOLO format
        x_center = ((x1 + x2) / 2) / w
        y_center = ((y1 + y2) / 2) / h
        width = (x2 - x1) / w
        height = (y2 - y1) / h

        records.append([
            filename,
            0,  # single class
            x_center,
            y_center,
            width,
            height
        ])

    df_yolo = pd.DataFrame(
        records,
        columns=["filename", "class_id", "x_center", "y_center", "width", "height"]
    )

    return df_yolo