from flask import Flask, Response
import cv2
import time
import threading
from datetime import datetime

# Define sleep in seconds duration to achieve desired fps
sleep_duration = 2

# Initialize the Flask app
app = Flask(__name__)

# Initialize the camera using OpenCV
camera = cv2.VideoCapture(0)  # '0' is the default device ID for the first USB camera

# Global variable to store the last frame
last_frame = None
frame_lock = threading.Lock()  # Lock to synchronize access to the frame


def rotate_frame(frame, angle):
    if angle == 90:
        return cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    elif angle == 180:
        return cv2.rotate(frame, cv2.ROTATE_180)
    elif angle == 270:
        return cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    else:
        return frame


def add_timestamp_to_frame(frame):
    """Adds a timestamp to the frame."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current date and time
    font = cv2.FONT_HERSHEY_DUPLEX
    font_scale = 1
    color = (255, 255, 255)  # White color
    thickness = 1

    # Calculate the position for the bottom left corner
    text_size = cv2.getTextSize(timestamp, font, font_scale, thickness)[0]  # Get text size
    position = (10, frame.shape[0] - 10)  # 10 pixels from the left and 10 pixels from the bottom

    cv2.putText(frame, timestamp, position, font, font_scale, color, thickness, cv2.LINE_AA)


def capture_frames():
    """Continuously capture frames from the camera."""
    global last_frame
    while True:
        success, frame = camera.read()  # Read a frame from the USB camera
        if not success:
            break

        rotated_frame = rotate_frame(frame, 0)  # Rotate by 0 degrees, no rotation applied

        # Add timestamp to the frame
        add_timestamp_to_frame(rotated_frame)

        # Store the last frame with a lock
        with frame_lock:
            last_frame = rotated_frame

        time.sleep(sleep_duration)  # Add delay to achieve desired fps


def save_frame_periodically(interval=10):
    """Save the last captured frame every interval seconds."""
    global last_frame
    while True:
        time.sleep(interval)

        # Save the last frame to disk
        with frame_lock:
            if last_frame is not None:
                cv2.imwrite('latest_image.jpg', last_frame)  # Save the frame as a .jpg file
                print(f"Captured image saved successfully")


def generate_frames():
    """Generate frames for streaming."""
    global last_frame
    while True:
        with frame_lock:
            if last_frame is None:
                continue

            ret, buffer = cv2.imencode('.jpg', last_frame)
            frame = buffer.tobytes()

        # Send the frame to the client
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        time.sleep(sleep_duration)


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return '''
    <html>
        <head>
            <title>USB Camera</title>
        </head>
        <body>
            <h1>USB Camera Feed</h1>
            <img src="/video_feed">
        </body>
    </html>
    '''


if __name__ == '__main__':
    # Start threads for capturing frames and saving them periodically
    capture_thread = threading.Thread(target=capture_frames, daemon=True)
    save_thread = threading.Thread(target=save_frame_periodically, daemon=True)

    capture_thread.start()
    save_thread.start()

    # Start the Flask application
    app.run(host='0.0.0.0', port=5000)