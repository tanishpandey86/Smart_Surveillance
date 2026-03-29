# Smart Surveillance System

A real-time motion detection and object tracking system built with Python and OpenCV. Detects moving objects from a live webcam feed, draws bounding boxes, tracks motion trails using KLT Optical Flow, saves alert snapshots, and plays a sound alert on macOS — all with zero external dataset required.

---

## Demo

| Feature | Description |
|---|---|
| Motion Detection | Detects any moving object in the camera frame |
| Bounding Boxes | Green rectangle drawn around every moving object |
| Optical Flow Trails | Orange trails showing direction and speed of movement |
| HUD Status | Real-time CLEAR / ALERT status on screen |
| Auto Snapshot | Saves JPG to `alerts/` folder when motion is detected |
| Sound Alert | Plays macOS ping sound when motion starts |

---

## Project Structure

```
Smart_Surveillance/
├── main.py            # Entry point — main pipeline and UI loop
├── background.py      # MOG2 background subtraction logic
├── detector.py        # Contour-based object detector
├── tracker.py         # KLT optical flow tracker
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

---

## How It Works — Workflow

```
Camera Feed (Webcam)
        │
        ▼
┌─────────────────────┐
│  Background         │  MOG2 learns the static background
│  Subtraction        │  over ~500 frames (~16 seconds)
│  (background.py)    │  Outputs a foreground mask
└────────┬────────────┘
         │  Foreground Mask
         ▼
┌─────────────────────┐
│  Object Detection   │  Finds contours in the mask
│  (detector.py)      │  Returns bounding boxes for
│                     │  objects above min_area threshold
└────────┬────────────┘
         │  Bounding Boxes
         ▼
┌─────────────────────┐
│  KLT Optical Flow   │  Tracks feature points across frames
│  Tracker            │  Computes motion direction and speed
│  (tracker.py)       │  Returns trails (new → old point pairs)
└────────┬────────────┘
         │  Trails + Boxes
         ▼
┌─────────────────────┐
│  Visualization      │  Draws boxes, trails, HUD overlay
│  + Alerts           │  Saves snapshots, plays sound alert
│  (main.py)          │
└─────────────────────┘
         │
         ▼
  Live Window Output
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.9+ | Core language |
| OpenCV (`cv2`) | Camera access, image processing, MOG2, KLT |
| NumPy | Array operations for optical flow |
| imutils | Frame resizing utilities |

---

## Requirements

- macOS (tested on macOS Sonoma with M3 Pro chip)
- Python 3.9 or higher
- Built-in or external webcam

---

## Local Setup — Run on Your Machine

### Step 1 — Clone the repository

```bash
git clone https://github.com/tanishpandey86/Smart_Surveillance.git
cd Smart_Surveillance
```

### Step 2 — Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

> On Windows use: `venv\Scripts\activate`

### Step 3 — Install dependencies

```bash
pip install opencv-python numpy torch torchvision imutils Pillow
```

### Step 4 — Grant camera permission (macOS only)

Go to **System Settings → Privacy & Security → Camera** and enable access for **Terminal** (or your IDE like VS Code).

### Step 5 — Run the system

```bash
python main.py
```

Two windows will open:
- **Smart Surveillance** — live camera feed with bounding boxes and motion trails
- **Foreground Mask** — binary mask showing detected motion regions (white = motion)

Press **Q** to quit.

---

## Configuration

You can tune these parameters inside `main.py` and the module files:

| Parameter | File | Default | Description |
|---|---|---|---|
| `min_area` | `detector.py` | `1500` | Minimum pixel area to count as an object. Increase for wider scenes. |
| `history` | `background.py` | `500` | Number of frames MOG2 uses to learn background |
| `varThreshold` | `background.py` | `16` | Sensitivity of motion detection. Lower = more sensitive |
| `maxCorners` | `tracker.py` | `100` | Max feature points tracked per frame |
| Camera index | `main.py` | `0` | `0` = built-in webcam. Change to `1` for external camera |
| Resolution | `main.py` | `1280x720` | Camera capture resolution |

---

## Output

When motion is detected, alert snapshots are automatically saved to the `alerts/` folder:

```
Smart_Surveillance/
└── alerts/
    ├── alert_20240315_143022_123456.jpg
    ├── alert_20240315_143023_456789.jpg
    └── ...
```

The `alerts/` folder is excluded from Git via `.gitignore` — snapshots stay local only.

---

## Syllabus Coverage (CSE3010 Computer Vision)

This project directly implements concepts from 4 modules:

| Module | Concept Used |
|---|---|
| Module 1 — Image Processing | Morphological operations, thresholding, convolution in `background.py` |
| Module 2 — Depth & Camera | Frame-to-frame geometry, camera access and calibration |
| Module 3 — Feature Extraction & Segmentation | Contour detection, region-based object segmentation in `detector.py` |
| Module 4 — Motion Analysis | Background subtraction (MOG2), KLT Optical Flow tracking in `tracker.py` |

---

## No Dataset Required

This system is **fully unsupervised**. It requires no pre-collected dataset. The MOG2 algorithm self-trains by observing your live camera feed for the first ~16 seconds (500 frames). The KLT tracker and contour detector are purely mathematical — no training involved.

---

## Possible Extensions

| Extension | Tools Needed |
|---|---|
| Person vs car classification | YOLOv8 + COCO dataset |
| Face detection and recognition | OpenCV Haar Cascades or MediaPipe |
| Web dashboard for remote viewing | Flask + Socket.IO |
| Email / SMS alert on motion | smtplib / Twilio API |
| Record video clips on motion | `cv2.VideoWriter` |

---

## Author

**Tanish Pandey**
GitHub: [@tanishpandey86](https://github.com/tanishpandey86)

---

## License

This project is open source and available under the [MIT License](LICENSE).
