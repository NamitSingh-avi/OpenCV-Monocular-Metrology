import cv2
import numpy as np

FOCAL_LENGTH = 666
KNOWN_WIDTH = 5.4  # cm

img = cv2.imread("img_1.png")
if img is None:
    print("Image not found")
    exit()

img = cv2.resize(img, (640, 480))

# === COLOR DETECTION ===
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_blue = np.array([85, 40, 40])
upper_blue = np.array([140, 255, 255])

mask = cv2.inRange(hsv, lower_blue, upper_blue)

# === STRONG CLEANING ===
kernel = np.ones((7,7), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=3)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)

# === FIND CONTOURS ===
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if len(contours) == 0:
    print("No contours found")
    exit()

# === TAKE LARGEST CONTOUR ===
largest = max(contours, key=cv2.contourArea)

area = cv2.contourArea(largest)

if area < 1000:
    print("Object too small")
else:
    x, y, w, h = cv2.boundingRect(largest)

    distance = (KNOWN_WIDTH * FOCAL_LENGTH) / w

    cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
    cv2.putText(img, f"{distance:.2f} cm", (x,y-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

    print(f"Width (pixels): {w}")
    print(f"Distance: {distance:.2f} cm")

cv2.imshow("Mask", mask)
cv2.imshow("Result", img)

cv2.waitKey(0)
cv2.destroyAllWindows()