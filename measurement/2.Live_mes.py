import cv2
import numpy as np

# Load homography
H = np.load("homography.npy")

points = []
captured = False
mouse_pos = (0,0)

# original camera resolution
orig_w = 640
orig_h = 480

# display window size
disp_w = 1000
disp_h = 750

scale_x = orig_w / disp_w
scale_y = orig_h / disp_h


def click_event(event, x, y, flags, param):
    global points, img_display, mouse_pos

    mouse_pos = (x,y)

    if not captured:
        return

    # convert mouse coordinate → real image coordinate
    x_real = int(x * scale_x)
    y_real = int(y * scale_y)

    if event == cv2.EVENT_LBUTTONDOWN:

        points.append([x_real, y_real])

        # smaller blue dot
        cv2.circle(img_display, (x_real, y_real), 3, (255,0,0), -1)

        if len(points) == 2:

            pts = np.array(points, dtype="float32").reshape(-1,1,2)
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


# CAMERA
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(3, orig_w)
cap.set(4, orig_h)

cv2.namedWindow("Measurement", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Measurement", disp_w, disp_h)

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

        display = cv2.resize(display, (disp_w, disp_h))
        cv2.imshow("Measurement", display)

    else:

        preview = img_display.copy()

        # convert mouse to image coordinates
        mx, my = mouse_pos
        mx_real = int(mx * scale_x)
        my_real = int(my * scale_y)

        # draw crosshair
        cv2.line(preview, (mx_real,0), (mx_real,orig_h), (150,150,150), 1)
        cv2.line(preview, (0,my_real), (orig_w,my_real), (150,150,150), 1)

        # live distance preview
        if len(points) == 1:

            pt1 = np.array(points[0], dtype="float32").reshape(-1,1,2)
            pt2 = np.array([[mx_real,my_real]], dtype="float32").reshape(-1,1,2)

            real_pt1 = cv2.perspectiveTransform(pt1, H)[0][0]
            real_pt2 = cv2.perspectiveTransform(pt2, H)[0][0]

            dist = np.linalg.norm(real_pt1 - real_pt2)

            pt1_draw = tuple(map(int, points[0]))
            pt2_draw = (mx_real, my_real)

            cv2.line(preview, pt1_draw, pt2_draw, (0,255,255), 1)

            mid = ((np.array(pt1_draw)+np.array(pt2_draw))//2).astype(int)

            cv2.putText(preview, f"{dist:.2f} cm",
                        tuple(mid), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0,255,255), 2)

        display = cv2.resize(preview, (disp_w, disp_h))
        cv2.imshow("Measurement", display)

    key = cv2.waitKey(1)

    if key == ord('c') and not captured:
        img_display = frame.copy()
        captured = True
        print("Image captured. Click first point.")

    if key == ord('r'):
        captured = False
        points.clear()
        print("Reset")

    if key == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()