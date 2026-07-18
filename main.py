import cv2
import time

from utils.camera import Camera
from detectors.person_detector import PersonDetector
from detectors.emotion import EmotionDetector
from utils.drawing import (
    draw_hud,
    draw_corner_box,
    draw_scanner,
    draw_event_log,
)
from utils.event_logger import EventLogger



camera = Camera(camera_index=1)  
detector = PersonDetector()
emotion_detector = EmotionDetector()
logger = EventLogger()

prev_time = time.time()
frame_count = 0
previous_ids = set()
fps = 0.0


while True:

    frame = camera.read()

    if frame is None:
        break

    frame_count += 1


    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time


    persons = detector.detect(frame)


    current_ids = {
        person["id"]
        for person in persons
        if person["id"] != -1
    }

    entered = current_ids - previous_ids
    left = previous_ids - current_ids

    for pid in entered:
        logger.add(f"ID {pid} Entered")

    for pid in left:
        logger.add(f"ID {pid} Left")

    previous_ids = current_ids


    for person in persons:

        x1, y1, x2, y2 = person["box"]
        conf = person["confidence"]
        track_id = person["id"]

        draw_corner_box(frame, x1, y1, x2, y2)
        draw_scanner(frame, x1, y1, x2, y2, frame_count)

        if conf >= 0.90:
            color = (0, 255, 0)
        elif conf >= 0.75:
            color = (0, 255, 255)
        else:
            color = (0, 0, 255)

        cv2.putText(
            frame,
            f"ID {track_id} | {conf:.2f}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2,
        )

        mood = emotion_detector.detect(frame, (x1, y1, x2, y2))

        if mood is not None:
            mood_color = (0, 255, 0) if mood == "Happy" else (255, 255, 255)
            cv2.putText(
                frame,
                mood,
                (x1, y2 + 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                mood_color,
                2,
            )

    draw_hud(frame, len(persons), fps)
    draw_event_log(frame, logger.get_events())

    cv2.imshow("AI Vision Showcase", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()