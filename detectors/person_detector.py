from ultralytics import YOLO


class PersonDetector:

    def __init__(self):
        self.model = YOLO("models/yolov8n.pt")

    def detect(self, frame):

        results = self.model.track(
            frame,
            classes=[0],
            conf=0.5,
            persist=True,
            verbose=False,
        )

        persons = []

        if len(results) == 0:
            return persons

        boxes = results[0].boxes

        if boxes is None:
            return persons

        for box in boxes:

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            confidence = float(box.conf[0])

            track_id = int(box.id[0]) if box.id is not None else -1

            persons.append({
                "box": (x1, y1, x2, y2),
                "confidence": confidence,
                "id": track_id
            })

        return persons