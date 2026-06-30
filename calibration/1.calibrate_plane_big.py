import cv2
import numpy as np

points_img = []
captured = False

# camera resolution
orig_w = 640
orig_h = 480

# much larger display window
disp_w = 1600
disp_h = 1200

scale_x = orig_w / disp_w
scale_y = orig_h / disp_h

# === REAL WORLD COORDINATES (cm) ===
points_real = np.array([
    [0, 0],
    [10, 0],
    [10, 10],
    [0, 10]
], dtype="float32")


def click_event(event, x, y, flags, param):
    global points_img, img_display

    if not captured:
        return

    # convert display mouse coordinates to original pixel coordinates
    x_real = int(x * scale_x)
    y_real = int(y * scale_y)

    if event == cv2.EVENT_LBUTTONDOWN:

        points_img.append([x_real, y_real])
        print(f"Clicked: {x_real}, {y_real}")

        cv2.circle(img_display, (x_real,y_real), 6, (0,0,255), -1)

        if len(points_img) == 4:

            pts_img = np.array(points_img, dtype="float32")

            H, _ = cv2.findHomography(pts_img, points_real)

            print("\nHomography Matrix:\n", H)

            np.save("homography.npy", H)
            print("Saved as homography.npy")


# CAMERA
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(3, orig_w)
cap.set(4, orig_h)

cv2.namedWindow("Calibration", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Calibration", disp_w, disp_h)

cv2.setMouseCallback("Calibration", click_event)


while True:

    if not captured:

        ret, frame = cap.read()
        if not ret:
            break

        display = frame.copy()

        cv2.putText(display, "Press 'c' to capture",
                    (20,40), cv2.FONT_HERSHEY_SIMPLEX,
                    1.0, (0,255,0), 2)

        display = cv2.resize(display, (disp_w, disp_h))

        cv2.imshow("Calibration", display)

    else:

        display = cv2.resize(img_display, (disp_w, disp_h))
        cv2.imshow("Calibration", display)

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