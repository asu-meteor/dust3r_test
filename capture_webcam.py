import cv2

def capture_photos_from_all_webcams(output_folder="webcam_photos"):
    """
    Captures a photo from each webcam connected to the computer.
    Saves the photos in the specified output folder.

    :param output_folder: Directory where photos will be saved.
    """
    import os

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    index = 0  # Webcam index
    captured_devices = []  # Keep track of devices that successfully captured a frame

    while True:
        # Attempt to open webcam
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)  # Use CAP_DSHOW on Windows for better performance
        if not cap.isOpened():
            print(f"No more webcams found. Stopping at index {index}.")
            break

        # Read a frame from the webcam
        ret, frame = cap.read()
        if ret:
            # Save the captured frame
            file_name = os.path.join(output_folder, f"webcam_{index}.jpg")
            cv2.imwrite(file_name, frame)
            print(f"Photo captured from webcam {index} and saved to {file_name}.")
            captured_devices.append(index)
        else:
            print(f"Failed to capture from webcam {index}.")

        # Release the current webcam
        cap.release()
        index += 1

    # Notify if no webcams were found
    if not captured_devices:
        print("No webcams were detected on this system.")
    else:
        print(f"Captured photos from the following webcams: {captured_devices}")

if __name__ == "__main__":
    capture_photos_from_all_webcams()
