import cv2


class EmotionDetector:


    def __init__(self):
        cascade_path = cv2.data.haarcascades

        self.face_cascade = cv2.CascadeClassifier(
            cascade_path + "haarcascade_frontalface_default.xml"
        )
        self.smile_cascade = cv2.CascadeClassifier(
            cascade_path + "haarcascade_smile.xml"
        )


        if self.face_cascade.empty():
            raise RuntimeError(
                "Failed to load haarcascade_frontalface_default.xml "
                f"from '{cascade_path}'. Your OpenCV install may be "
                "missing its data files -- try 'pip install --upgrade "
                "--force-reinstall opencv-python'."
            )

        if self.smile_cascade.empty():
            raise RuntimeError(
                "Failed to load haarcascade_smile.xml "
                f"from '{cascade_path}'. Your OpenCV install may be "
                "missing its data files -- try 'pip install --upgrade "
                "--force-reinstall opencv-python'."
            )

    def detect(self, frame, box):
        """
        frame : full BGR frame from the camera
        box   : (x1, y1, x2, y2) person bounding box from PersonDetector

        Returns a mood string: "Happy", "Neutral", or None if no
        face could be found in the box (e.g. person facing away,
        too far from camera, or badly lit).
        """
        x1, y1, x2, y2 = box

        h, w = frame.shape[:2]
        x1 = max(0, min(x1, w - 1))
        x2 = max(0, min(x2, w - 1))
        y1 = max(0, min(y1, h - 1))
        y2 = max(0, min(y2, h - 1))

        if x2 <= x1 or y2 <= y1:
            return None


        head_bottom = y1 + int((y2 - y1) * 0.55)
        head_crop = frame[y1:head_bottom, x1:x2]

        if head_crop.size == 0:
            return None

        gray = cv2.cvtColor(head_crop, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=4,
            minSize=(20, 20),
        )

        if len(faces) == 0:
            return None

        fx, fy, fw, fh = max(faces, key=lambda f: f[2] * f[3])
        face_roi = gray[fy:fy + fh, fx:fx + fw]

        smiles = self.smile_cascade.detectMultiScale(
            face_roi,
            scaleFactor=1.7,
            minNeighbors=15,
            minSize=(20, 20),
        )

        return "Happy" if len(smiles) > 0 else "Neutral"
    

    
