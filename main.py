import cv2
import datetime
import os
from background import BackgroundSubtractor
from detector   import ObjectDetector
from tracker    import KLTTracker

def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    bg  = BackgroundSubtractor()
    det = ObjectDetector(min_area=1500)
    klt = KLTTracker()

    prev_had_boxes = False
    os.makedirs("alerts", exist_ok=True)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        fg_mask = bg.apply(frame)
        boxes   = det.detect(fg_mask)
        trails  = klt.update(frame, fg_mask)

        # Draw bounding boxes
        for (x, y, w, h) in boxes:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 200, 120), 2)
            cv2.putText(frame, "MOTION", (x, y-8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 120), 1)

        # Draw KLT optical flow trails
        for (new, old) in trails:
            try:
                new = new.ravel()
                old = old.ravel()
                a, b = int(new[0]), int(new[1])
                c, d = int(old[0]), int(old[1])
                cv2.line(frame,   (a, b), (c, d), (255, 165, 0), 2)
                cv2.circle(frame, (a, b), 3, (0, 255, 255), -1)
            except (IndexError, ValueError):
                continue

        # HUD overlay
        status = "ALERT" if boxes else "CLEAR"
        color  = (0, 80, 255) if boxes else (0, 200, 0)
        cv2.putText(frame, f"Status: {status}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        cv2.putText(frame, f"Objects: {len(boxes)}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        # Save alert frames
        if boxes:
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            cv2.imwrite(f"alerts/alert_{ts}.jpg", frame)

        # Sound alert on new motion (macOS)
        if boxes and not prev_had_boxes:
            os.system("afplay /System/Library/Sounds/Ping.aiff &")
        prev_had_boxes = bool(boxes)

        cv2.imshow("Smart Surveillance — press Q to quit", frame)
        cv2.imshow("Foreground Mask", fg_mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()