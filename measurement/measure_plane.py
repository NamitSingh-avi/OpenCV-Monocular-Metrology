import cv2
import numpy as np

# Load homography
H = np.load("homography.npy")

points = []
captured = False

def click_event(event, x, y, flags, param):
    global points, img_display

    if not captured:
        return

    if event == cv2.EVENT_LBUTTONDOWN:
        points.append([x, y])

        cv2.circle(img_display, (x,y), 5, (255,0,0), -1)

        if len(points) == 2:
            pts = np.array(points, dtype="float32").reshape(-1,1,2)

            # Convert to real-world
            real_pts = cv2.perspectiveTransform(pts, H)

            p1 = real_pts[0][0]
            p2 = real_pts[1][0]

            dist = np.linalg.norm(p1 - p2)

            print(f"Distance: {dist:.2f} cm")

            pt1 = tuple(map(int, points[0]))
            pt2 = tuple(map(int, points[1]))

            cv2.line(img_display, pt1, pt2, (255,0,0), 2)

            mid = ((np.array(pt1)+np.array(pt2))//2).astype(int)

            cv2.putText(img_display, f"{dist:.2f} cm",
                        tuple(mid), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (255,0,0), 2)

            points = []

# === CAMERA ===
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(3, 640)
cap.set(4, 480)

cv2.namedWindow("Measurement")
cv2.setMouseCallback("Measurement", click_event)

while True:
    if not captured:
        ret, frame = cap.read()
        if not ret:
            break

        display = frame.copy()
        cv2.putText(display, "Press 'c' to capture",
                    (20,30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0,255,0), 2)

        cv2.imshow("Measurement", display)

    else:
        cv2.imshow("Measurement", img_display)

    key = cv2.waitKey(1)

    if key == ord('c') and not captured:
        img_display = frame.copy()
        captured = True
        print("Image captured. Click 2 points to measure.")

    if key == ord('r'):
        captured = False
        points.clear()
        print("Reset")

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()