import cv2

def start_camera():
    # Open default camera (0)
    cap = cv2.VideoCapture(1)

    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error: Cannot open camera")
        return

    print("Press 'q' to exit")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame")
            break

        # Show frame
        cv2.imshow("Live Camera", frame)

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    start_camera()