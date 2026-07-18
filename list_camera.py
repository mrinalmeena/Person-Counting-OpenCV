"""
Helper script to figure out which camera index corresponds to your
iPhone (via Continuity Camera) vs. your Mac's built-in webcam.

It opens each index in turn, grabs one frame, and saves it as
camera_0.jpg, camera_1.jpg, etc. so you can look at the images and
see which one is the iPhone.
"""

import cv2

MAX_INDEX_TO_TRY = 5

for index in range(MAX_INDEX_TO_TRY):
    cap = cv2.VideoCapture(index)

    if not cap.isOpened():
        print(f"Index {index}: could not open (probably doesn't exist)")
        cap.release()
        continue

    success, frame = cap.read()

    if not success:
        print(f"Index {index}: opened but couldn't read a frame")
    else:
        filename = f"camera_{index}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Index {index}: OK -- saved a sample frame to {filename}")

    cap.release()

print("\nOpen the saved camera_*.jpg files and check which one shows")
print("your iPhone's view. That number is the index to use.")