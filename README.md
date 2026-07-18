# Person Counting

A real-time webcam demo which uses a 
YOLOv8 model to detect and track people in frame, draws a HUD-style
overlay with live stats, logs entry/exit events per tracked person,
and reads each person's mood (Happy / Neutral) from their face.

No manual counting needed — point your webcam at the classroom and
the model detects everyone automatically, with a live headcount and
a scrolling event log of who entered or left frame.

---

## Features

- **Person detection & tracking** — YOLOv8 (`ultralytics`) detects
  people and assigns each one a persistent ID using the built-in
  ByteTrack tracker, so the same person keeps the same ID as they
  move around.
- **Live headcount HUD** — a translucent panel shows the current
  number of people in frame and live FPS.
- **Entry / exit event log** — a scrolling panel logs
  `"ID X Entered"` / `"ID X Left"` events with timestamps as people
  move in and out of frame.
- **Mood detection** — for each detected person, a lightweight
  OpenCV Haar-cascade face + smile detector labels them
  `"Happy"` or `"Neutral"` under their bounding box.
- **Confidence-coded boxes** — bounding box label color shifts
  green → yellow → red based on detection confidence.

---

## Project structure

```
OPEN CV
├── main.py                  # Main live webcam pipeline (run this)
├── test_camera.py           # Standalone webcam sanity check
├── test_yolo.py             # Standalone YOLO detection sanity check
├── test_emotion.py          # Standalone face+smile detector sanity check
├── requirements.txt
├── models/
│   └── yolov8n.pt           # YOLOv8 nano weights
├── detectors/
│   ├── person_detector.py   # YOLO person detection + tracking
│   ├── emotion.py           # Haar-cascade mood detection
|
└── utils/
    ├── camera.py            # Webcam capture wrapper
    ├── drawing.py            # HUD / corner-box / scanner-line drawing
    ├── event_logger.py       # Rolling entry/exit event log

            
```

---

## Setup

1. **Create and activate a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Make sure `models/yolov8n.pt` is present** (it should already be
   in the repo). If missing, `ultralytics` will auto-download it the
   first time `YOLO("models/yolov8n.pt")` is called.

---

## Running it

**Full live demo:**
```bash
python main.py
```
A window titled **"AI Vision Showcase"** will open showing your
webcam feed with bounding boxes, mood labels, HUD, and event log.
Press **`q`** to quit.


## How it works

1. `utils/camera.py` grabs and mirrors frames from the webcam.
2. `detectors/person_detector.py` runs YOLOv8 with tracking
   (`model.track(..., persist=True)`) so each person gets a stable ID
   across frames, not just a fresh detection every frame.
3. `main.py` compares this frame's IDs against the previous frame's
   IDs to detect who entered or left, logging it via
   `utils/event_logger.py`.
4. For each detected person, `detectors/emotion.py` crops the top
   portion of their bounding box (where the face should be) and runs
   OpenCV's built-in Haar cascades to detect a face, then a smile
   within that face, to determine mood.
5. `utils/drawing.py` renders the corner-bracket boxes, scanning
   line effect, HUD panel, and event log onto the frame each loop.

---

## Known limitations

- **Mood detection is heuristic, not deep-learning-based.** It uses
  OpenCV's Haar cascades (fast, no downloads, but less accurate than
  a trained model). It only distinguishes Happy vs. Neutral, and can
  miss faces that are angled, too small, poorly lit, or partially
  turned away from the camera.
- **`test_yolo.py` hardcodes `device="mps"`** (Apple Silicon GPU). If
  you're not on a Mac, either remove that argument or change it to
  `device="cpu"` (or `"cuda"` if you have an NVIDIA GPU).
- **Re-entry isn't true re-identification.** If a tracked person
  leaves frame and comes back, YOLO's tracker usually assigns them a
  new ID rather than recognizing them as the same person. Real
  re-identification would need face embeddings, which is a bigger
  project.
- **`face_detector.py`, `hand_detector.py`, `pose_detector.py`,
  `colors.py`, and `fps.py` are empty stub files** — placeholders for
  future features (see Roadmap).

---


## Controls

| Key | Action        |
|-----|---------------|
| `q` | Quit the app  |
