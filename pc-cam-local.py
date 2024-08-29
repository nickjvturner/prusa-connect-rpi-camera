from flask import Flask, Response
import cv2
import time

# Define the filename to save the frames
# from secrets import image_path

# Define sleep in seconds duration to achieve desired fps
sleep_duration = 2

# Initialize the Flask app
app = Flask(__name__)

# Initialize the camera using OpenCV
camera = cv2.VideoCapture(0)  # '0' is the default device ID for the first USB camera


def rotate_frame(frame, angle):
    if angle == 90:
        return cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    elif angle == 180:
        return cv2.rotate(frame, cv2.ROTATE_180)
    elif angle == 270:
        return cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    else:
        return frame


def generate_frames(sleep_duration):
    last_saved_time = time.time()  # Record the start time to calculate the elapsed time

    while True:
        success, frame = camera.read()  # Read a frame from the USB camera
        if not success:
            break

        rotated_frame = rotate_frame(frame, 0)  # Rotate by 0 degrees, no rotation applied
        ret, buffer = cv2.imencode('.jpg', rotated_frame)
        frame = buffer.tobytes()

        # Send the frame to the client
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        # Get the current time
        current_time = time.time()

        # Check if 10 seconds have passed since the last save
        if current_time - last_saved_time >= 10:
            # Save the current frame to disk
            cv2.imwrite('latest_frame.jpg', rotated_frame)  # Save the frame as a .jpg file
            # print(f"Saved frame to {filename}")

            # Update the last saved time
            last_saved_time = current_time

        # Add delay to achieve desired fps
        time.sleep(sleep_duration)


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(sleep_duration), mimetype='multipart/x-mixed-replace; boundary=frame')


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
    app.run(host='0.0.0.0', port=5000)