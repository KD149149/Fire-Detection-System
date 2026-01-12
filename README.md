# Fire-Detection-System
# Fire-Detection-System
Here’s a professional, clear, and concise README for your fire detection project:

---

# AI-Powered Fire Detection System

## Overview

This project implements a **real-time fire detection system** using a live camera feed. It leverages **YOLOv8** for accurate fire detection, highlights fire regions with a red bounding box, logs all detected events into an Excel file, and records the processed video.

The system is suitable for **safety monitoring, industrial surveillance, and smart home applications**.

---

## Features

* Real-time **fire detection** using YOLOv8.
* **Bounding boxes** drawn only around fire regions.
* **Confidence scores** displayed for detected fire.
* **Event logging** to Excel with timestamps.
* **Video recording** of detection output.

---

## Requirements

* Python 3.10 or higher
* OpenCV
* Pandas
* XlsxWriter
* Ultralytics YOLOv8 (`pip install ultralytics`)

---

## Installation

1. Clone this repository:

```bash
git clone <repository_url>
cd fire-detection
```

2. Install dependencies:

```bash
pip install opencv-python pandas xlsxwriter ultralytics
```

3. Ensure you have a YOLOv8 model:

   * Use a **pre-trained model** (`yolov8n.pt`) or a **custom fire-detection YOLO model**.

---

## Usage

1. Run the fire detection script:

```bash
python fire_detection.py
```

2. The system will:

   * Open a live webcam feed.
   * Detect fire in real-time and highlight it with a **red bounding box** and confidence score.
   * Record the video as `fire_detection_output.avi`.
   * Log all fire events to `fire_events.xlsx`.

3. Press **`q`** to stop the detection and save outputs.

---

## Files

* `fire_detection.py` – Main Python script for real-time fire detection.
* `fire_events.xlsx` – Excel log of fire events (generated at runtime).
* `fire_detection_output.avi` – Recorded video of the live detection (generated at runtime).

---

## Notes

* The detection accuracy depends on the YOLO model used.
* Adjust confidence thresholds if needed to reduce false positives.
* Ensure proper lighting for optimal detection performance.

---

## License

This project is open-source and not free to use for educational, research, and commercial purposes. can contact me @kajaldadas149@gmail.com

