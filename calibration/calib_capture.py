import cv2
import os

def start_camera():
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("Error: Cannot open camera")
        return

    # Set resolution
    cap.set(3, 640)
    cap.set(4, 480)

    # Create folder
    save_path = "calib_images"
    os.makedirs(save_path, exist_ok=True)

    img_count = 0

    print("Press 's' to save image | 'q' to quit")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame")
            break

        cv2.imshow("Camera", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            filename = f"{save_path}/img_{img_count}.png"
            cv2.imwrite(filename, frame)
            print(f"Saved: {filename}")
            img_count += 1

        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    start_camera()