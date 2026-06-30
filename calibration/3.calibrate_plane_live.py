import cv2
import numpy as np

points_img = []
captured = False

# === REAL WORLD COORDINATES (cm) ===
points_real = np.array([
    [0, 0],
    [20, 0],
    [20, 20],
    [0, 20]
], dtype="float32")

def click_event(event, x, y, flags, param):
    global points_img, img_display

    if not captured:
        return

    if event == cv2.EVENT_LBUTTONDOWN:
        points_img.append([x, y])
        print(f"Clicked: {x}, {y}")

        cv2.circle(img_display, (x,y), 5, (0,0,255), -1)

        if len(points_img) == 4:
            pts_img = np.array(points_img, dtype="float32")

            H, _ = cv2.findHomography(pts_img, points_real)

            print("\nHomography Matrix:\n", H)

            np.save("homography.npy", H)
            print("Saved as homography.npy")

# === CAMERA ===
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(3, 640)
cap.set(4, 480)

cv2.namedWindow("Calibration")
cv2.setMouseCallback("Calibration", click_event)

while True:
    if not captured:
        ret, frame = cap.read()
        if not ret:
            break

        display = frame.copy()
        cv2.putText(display, "Press 'c' to capture",
                    (20,30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0,255,0), 2)

        cv2.imshow("Calibration", display)

    else:
        cv2.imshow("Calibration", img_display)

    key = cv2.waitKey(1)

    if key == ord('c') and not captured:
        img_display = frame.copy()
        captured = True
        print("Image captured. Now click 4 points.")

    if key == ord('r'):
        captured = False
        points_img.clear()
        print("Reset")

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()