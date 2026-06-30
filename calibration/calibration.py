import cv2
import numpy as np
import glob

# Chessboard dimensions (INNER corners)
chessboard_size = (8, 5)

# Prepare object points (real world coordinates)
objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:8, 0:5].T.reshape(-1, 2)

objpoints = []  # 3D points
imgpoints = []  # 2D points

# Load calibration images
images = glob.glob('calib_images/*.png')

print(f"Found {len(images)} images")

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

    if ret:
        objpoints.append(objp)
        imgpoints.append(corners)

        # Draw corners (for verification)
        cv2.drawChessboardCorners(img, chessboard_size, corners, ret)
        cv2.imshow('Corners', img)
        cv2.waitKey(200)
    else:
        print(f"Chessboard NOT detected in {fname}")

cv2.destroyAllWindows()

# Calibration
ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None
)

print("\n=== Calibration Results ===")
print("Camera Matrix (K):\n", K)
print("\nDistortion Coefficients:\n", dist)