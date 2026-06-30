import cv2
import numpy as np

print("All libraries working!")

# Create image FIRST
img = np.zeros((300,300,3), dtype=np.uint8)

# Then modify it
img[:] = (0,255,0)   # Green image

cv2.imshow("Test", img)
cv2.waitKey(0)
cv2.destroyAllWindows()