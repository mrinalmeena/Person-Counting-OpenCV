import cv2


def draw_hud(frame, students, fps):
    overlay = frame.copy()

    # Glass panel
    cv2.rectangle(overlay, (15, 15), (360, 160), (30, 30, 30), -1)
    cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, frame)

    # Border
    cv2.rectangle(frame, (15, 15), (360, 160), (0, 255, 255), 2)

    cv2.putText(
        frame,
        "AI VISION SHOWCASE",
        (30, 45),
        cv2.FONT_HERSHEY_DUPLEX,
        0.8,
        (0, 255, 255),
        2,
    )

    cv2.putText(
        frame,
        f"Students : {students}",
        (30, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
    )

    cv2.putText(
        frame,
        f"FPS : {int(fps)}",
        (30, 110),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
    )

    cv2.putText(
        frame,
        "STATUS : ACTIVE",
        (30, 140),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 255, 0),
        2,
    )


def draw_event_log(frame, events):
    x = frame.shape[1] - 340
    y = 20

    overlay = frame.copy()

    cv2.rectangle(
        overlay,
        (x, y),
        (x + 320, y + 230),
        (20, 20, 20),
        -1,
    )

    cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, frame)

    cv2.rectangle(
        frame,
        (x, y),
        (x + 320, y + 230),
        (255, 255, 0),
        2,
    )

    cv2.putText(
        frame,
        "AI EVENT LOG",
        (x + 15, y + 30),
        cv2.FONT_HERSHEY_DUPLEX,
        0.7,
        (255, 255, 0),
        2,
    )

    offset = 60

    for event in events:
        cv2.putText(
            frame,
            event,
            (x + 15, y + offset),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
        )
        offset += 22


def draw_corner_box(frame, x1, y1, x2, y2, color=(0, 255, 255), thickness=2):
    line = 25

    # Top Left
    cv2.line(frame, (x1, y1), (x1 + line, y1), color, thickness)
    cv2.line(frame, (x1, y1), (x1, y1 + line), color, thickness)

    # Top Right
    cv2.line(frame, (x2 - line, y1), (x2, y1), color, thickness)
    cv2.line(frame, (x2, y1), (x2, y1 + line), color, thickness)

    # Bottom Left
    cv2.line(frame, (x1, y2 - line), (x1, y2), color, thickness)
    cv2.line(frame, (x1, y2), (x1 + line, y2), color, thickness)

    # Bottom Right
    cv2.line(frame, (x2 - line, y2), (x2, y2), color, thickness)
    cv2.line(frame, (x2, y2 - line), (x2, y2), color, thickness)


def draw_scanner(frame, x1, y1, x2, y2, frame_count):

    # Clamp coordinates to the frame
    h, w = frame.shape[:2]

    x1 = max(0, min(x1, w - 1))
    x2 = max(0, min(x2, w - 1))
    y1 = max(0, min(y1, h - 1))
    y2 = max(0, min(y2, h - 1))

    if x2 <= x1 or y2 <= y1:
        return

    height = y2 - y1
    scan_y = y1 + (frame_count % height)

    cv2.line(
        frame,
        (x1 + 5, scan_y),
        (x2 - 5, scan_y),
        (255, 255, 0),
        2,
    )


