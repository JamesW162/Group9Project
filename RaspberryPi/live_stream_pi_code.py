import time
import os
import io
import base64
import threading
from datetime import datetime
from picamera import PiCamera
import firebase_admin
from firebase_admin import credentials, db
# Configuration
FRAME_RATE = 5  # Lower frames per second to avoid database overload DO NOT GO HIGHER THAN 5
RESOLUTION = (320, 240)  # Lower resolution for better performance with database
QUALITY = 20  # JPEG compression quality (lower = smaller file size)
MAX_STREAM_TIME = 300  # Maximum streaming time in seconds (5 minutes)
STREAM_ID = datetime.now().strftime("%Y%m%d_%H%M%S")  # Unique ID for this stream
PIID=1
# Initialize Firebase with explicit parameters
# Path to your service account key file
cred_path = '/home/pi/Desktop/codes/bsltranslator-93f00-firebase-adminsdk-fbsvc-e79666a3dd.json'
cred = credentials.Certificate(cred_path)
# Define database URL explicitly
DATABASE_URL = 'https://bsltranslator-93f00-default-rtdb.europe-west1.firebasedatabase.app/'
# Initialize the app with database URL only
firebase_admin.initialize_app(cred, {
    'databaseURL': DATABASE_URL
})
def delete_all_previous_streams():
    """Delete all previous stream data from Firebase database"""
    try:
        # Get reference to streams
        streams_ref = db.reference('/streams')
        # Get all existing streams
        existing_streams = streams_ref.get()
        if existing_streams:
            print(f"Found {len(existing_streams)} previous streams. Deleting...")
            # Delete each stream
            for stream_id in existing_streams:
                if stream_id != STREAM_ID:  # Don't delete current stream if it exists
                    db.reference(f'/streams/{stream_id}').delete()
                    print(f"Deleted stream: {stream_id}")
        print("Previous streams cleanup completed.")
    except Exception as e:
        print(f"Error during stream cleanup: {e}")
# Database reference for stream status and latest frame
stream_ref = db.reference(f'/streams/{STREAM_ID}')
latest_frame_ref = db.reference(f'/streams/{STREAM_ID}/latest_frame')
class VideoStreamer:
    def __init__(self):
        self.camera = None
        self.running = False
        self.frame_count = 0
        self.start_time = 0
    def initialize_camera(self):
        """Set up the camera with appropriate settings"""
        self.camera = PiCamera()
        self.camera.resolution = RESOLUTION
        self.camera.framerate = 30  # Camera framerate (capture more than we send)
        # Wait for camera to initialize
        time.sleep(2)
        print("Camera initialized")
    def start_stream(self):
        """Start the video streaming process"""
        if self.running:
            print("Stream is already running")
            return
        # Delete previous streams before starting a new one
        delete_all_previous_streams()
        self.initialize_camera()
        self.running = True
        self.frame_count = 0
        self.start_time = time.time()
        # Update stream status in Firebase
        stream_ref.set({
            'status': 'active',
            'started_at': {'.sv': 'timestamp'},
            'resolution': f"{RESOLUTION[0]}x{RESOLUTION[1]}",
            'frame_rate': FRAME_RATE,
            'piid': PIID
        })
        # Start streaming in a separate thread
        stream_thread = threading.Thread(target=self._stream_frames)
        stream_thread.daemon = True
        stream_thread.start()
        print(f"Streaming started with ID: {STREAM_ID}")
        return STREAM_ID
    def stop_stream(self):
        """Stop the video streaming process"""
        self.running = False
        if self.camera:
            self.camera.close()
            self.camera = None
        # Update stream status in Firebase
        stream_ref.update({
            'status': 'ended',
            'ended_at': {'.sv': 'timestamp'},
            'frames_sent': self.frame_count
        })
        print(f"Streaming stopped after sending {self.frame_count} frames")
    def _stream_frames(self):
        """Continuously capture and send frames while running"""
        # Calculate delay between frames based on desired frame rate
        frame_delay = 1.0 / FRAME_RATE
        try:
            while self.running:
                loop_start = time.time()
                # Capture frame
                frame = io.BytesIO()
                self.camera.capture(frame, 'jpeg', quality=QUALITY, use_video_port=True)
                frame.seek(0)
                frame_data = frame.read()
                # Send frame to Firebase
                self._send_frame(frame_data)
                # Increment frame counter
                self.frame_count += 1
                # Check if max streaming time reached
                elapsed_time = time.time() - self.start_time
                if elapsed_time >= MAX_STREAM_TIME:
                    print(f"Maximum streaming time reached ({MAX_STREAM_TIME}s)")
                    self.stop_stream()
                    break
                # Calculate how long to wait until next frame
                processing_time = time.time() - loop_start
                sleep_time = max(0, frame_delay - processing_time)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                # Print progress every 10 frames
                if self.frame_count % 10 == 0:
                    fps = self.frame_count / (time.time() - self.start_time)
                    print(f"Streaming... {self.frame_count} frames sent ({fps:.2f} fps)")
        except Exception as e:
            print(f"Error in streaming: {e}")
            self.stop_stream()
    def _send_frame(self, frame_data):
        """Send a frame to Firebase Realtime Database as base64"""
        timestamp = int(time.time() * 1000)  # Millisecond timestamp
        # Convert frame to base64 for database storage
        encoded_frame = base64.b64encode(frame_data).decode('utf-8')
        # Create data object
        frame_info = {
            'data': encoded_frame,
            'timestamp': timestamp,
            'frame_number': self.frame_count
        }
        # Store in database
        latest_frame_ref.set(frame_info)
        # Also store in frame history (last 5 frames)
        if self.frame_count % 5 == 0:  # Only store every 5th frame in history
            history_ref = db.reference(f'/streams/{STREAM_ID}/frames/frame_{self.frame_count}')
            history_ref.set(frame_info)
def main():
    streamer = VideoStreamer()
    try:
        print(f"Starting stream with ID: {STREAM_ID}")
        print(f"Database URL: {DATABASE_URL}")
        # Start streaming
        streamer.start_stream()
        # Keep main thread alive while streaming
        while streamer.running:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Streaming interrupted by user")
    finally:
        streamer.stop_stream()
        print("Stream ended")
if __name__ == "__main__":
    main()
