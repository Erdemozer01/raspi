import cv2
import numpy as np
import time

# --- AYARLAR ---
# STREAM_URL = "http://100.70.22.28:8080/video" # <<< KENDÄ° TELEFONUNUZUN IP VE PORTUNU YAZIN!

STREAM_URL = "http://192.168.1.2:8080/video"


FOCAL_LENGTH_PIXELS = 625.0


TARGET_OBJECT_REAL_WIDTH_CM = 20.0



def capture_frame_from_stream(stream_url):
    cap = cv2.VideoCapture(stream_url)
    time.sleep(1)  # Brief pause for connection
    if not cap.isOpened():
        print(f"Error: Could not connect to stream ({stream_url}).")
        return None
    ret, frame = cap.read()
    if not ret or frame is None:
        print("Error: Could not read frame from stream.")
        cap.release()
        return None
    cap.release()
    return frame


def detect_object_and_get_pixel_width(frame_to_process):
    # This function uses cv2.selectROI for manual object selection.
    # For automatic detection, you would need to implement an object detection algorithm here.
    print("INFO: Manual object selection using ROI.")
    print("In the new window, draw a rectangle around the object and press Enter.")

    # Open a window to select the object
    # showCrosshair=True displays crosshairs, fromCenter=False starts selection from top-left
    r = cv2.selectROI("Select Object and Press Enter", frame_to_process, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow("Select Object and Press Enter")  # Close the selection window immediately after

    # r is a tuple (x, y, w, h). w (width) is r[2].
    if r[2] > 0:  # If width is greater than 0, a valid selection was made
        return r[2]
    return 0  # Return 0 if no valid selection


# --- MAIN PROGRAM FLOW ---
if __name__ == "__main__":
    try:
        print("Capturing frame from camera stream...")
        frame = capture_frame_from_stream(STREAM_URL)

        if frame is not None:
            # Use a copy of the original frame for ROI selection
            # so the original frame isn't drawn on if you need it clean.
            selection_frame = frame.copy()
            cv2.imshow("Image Captured - Select Object (then press Enter in ROI window)", selection_frame)
            print("Please select the object you want to measure in the window named 'Image Captured...'.")

            target_object_pixel_width = detect_object_and_get_pixel_width(selection_frame)

            if target_object_pixel_width > 0:
                print(f"seçilen obje genişliği: {target_object_pixel_width}")

                if FOCAL_LENGTH_PIXELS > 0 and TARGET_OBJECT_REAL_WIDTH_CM > 0:
                    # Calculate distance
                    distance_cm = (TARGET_OBJECT_REAL_WIDTH_CM * FOCAL_LENGTH_PIXELS) / target_object_pixel_width

                    print(f"Hesaplanan Mesafe: {distance_cm:.2f} cm")

                    # Display the result on the original image
                    cv2.putText(frame, f"Mesafe: {distance_cm:.2f} cm", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.imshow("Result", frame)
                    cv2.waitKey(0)
                else:
                    print("Error: Focal length or object real width cannot be zero or negative.")
            else:
                print("Object not selected or width could not be measured.")
        else:
            print("Could not capture frame from camera stream.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Exiting program.")
        cv2.destroyAllWindows()
