# Traffic Sign Detection
Traffic sign detection with YOLO model. 

## Dataset
- German Traffic Sign Detection Benchmark Dataset
- 900 images with 0-6 traffic signs per image
- Source: [German Traffic Signs Image Dataset](https://benchmark.ini.rub.de/gtsdb_dataset.html#Downloads)

## Tech Stack
- Python
- Matplotlib / Seaborn

## Model
- Yolo v8 nano

## Training
- 500 images training and 150 images validation
- 50 epochs
- Saving best and last checkpoint

## Evaluation
- Precision: 96%
- Recall: 96%
- mAP 0.5: 96%
- mAP 0.5-0.95: 80%
