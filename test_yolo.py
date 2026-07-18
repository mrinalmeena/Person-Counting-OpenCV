
import cv2
from detectors.emotion import EmotionDetector
from utils.camera import Camera
 
 
camera = Camera()
emotion_detector = EmotionDetector()
 
print("Cascades loaded OK. Press 'q' to quit.")
 
while True:
    frame = camera.read()
 
    if frame is None:
        break
 
    h, w = frame.shape[:2]
 
    # Treat the WHOLE frame as one "person box" for this isolated test
    mood = emotion_detector.detect(frame, (0, 0, w, h))
 
    text = mood if mood is not None else "No face detected"
    color = (0, 255, 0) if mood == "Happy" else (0, 0, 255)
 
    cv2.putText(
        frame,
        text,
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        color,
        2,
    )
 
    cv2.imshow("Emotion Test", frame)
 
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
 
camera.release()
cv2.destroyAllWindows()
