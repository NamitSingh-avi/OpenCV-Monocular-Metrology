import cv2
import numpy as np

# Your calibration values
K = np.array([
    [665.7286, 0, 311.9558],
    [0, 666.9915, 253.5926],
    [0, 0, 1]
])

dist = np.array([[-0.06816225, -0.24408809, 0.00459357, -0.00429742, 0.92943548]])

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

cap.set(3, 640)
cap.set(4, 480)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]

    # Get optimal new camera matrix
    new_K, roi = cv2.getOptimalNewCameraMatrix(K, dist, (w, h), 1, (w, h))

    # Undistort
    undistorted = cv2.undistort(frame, K, dist, None, new_K)

    # Show both
    cv2.imshow("Original", frame)
    cv2.imshow("Undistorted", undistorted)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()