import cv2


class Camera:
    def __init__(self, camera_index=0, width=1280, height=720):
        self.cap = cv2.VideoCapture(camera_index)

        if not self.cap.isOpened():
            raise RuntimeError("❌ Could not open camera.")

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def read(self):
        success, frame = self.cap.read()

        if not success:
            return None

        # Mirror the frame for a natural webcam view
        frame = cv2.flip(frame, 1)

        return frame

    def release(self):
        if self.cap.isOpened():
            self.cap.release()

        cv2.destroyAllWindows()