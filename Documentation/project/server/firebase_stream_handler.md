# Firebase Stream Handler for BSL Translation

This Python script provides tools for managing and interacting with video streams stored in Firebase Realtime Database. It offers functionality to create test streams, view existing streams, and list all streams in the database - primarily designed to work with the BSL (British Sign Language) Translation system.

## Base64 Image Conversion Functions

The script includes utility functions to convert between base64 encoded strings (used in Firebase) and OpenCV image objects:

```python
def base64_to_image(base64_string):
    """Convert base64 string to an OpenCV image."""
    img_data = base64.b64decode(base64_string)
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def image_to_base64(image):
    """Convert OpenCV image to base64 string."""
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode('utf-8')
```

These functions are essential for the two-way communication between the computer's camera/display and the Firebase database.

## Creating Test Streams

The script can create test streams using the local webcam, which is useful for testing the BSL translation system without a Raspberry Pi:

```python
def create_test_stream():
    """Create a test stream in Firebase using a webcam."""
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    stream_id = f"test_stream_{int(time.time())}"
    stream_ref = db.reference(f'/streams/{stream_id}')
    
    # Set initial stream info
    stream_ref.set({
        'status': 'active',
        'started_at': int(time.time() * 1000),
        'resolution': '640x480',
        'frame_rate': 15,
        'latest_frame': {
            'frame_number': 0,
            'timestamp': int(time.time() * 1000),
            'data': ''
        }
    })
```

This function:
1. Opens the default webcam
2. Creates a unique stream ID based on the current timestamp
3. Sets up the initial stream metadata in Firebase
4. Continually captures frames, encodes them to base64, and uploads them

The loop that captures and uploads frames:

```python
try:
    frame_number = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Resize frame to reduce data size
        frame = cv2.resize(frame, (640, 480))
        
        # Convert to base64
        base64_data = image_to_base64(frame)
        
        # Update the latest frame
        latest_frame_ref = stream_ref.child('latest_frame')
        latest_frame_ref.update({
            'frame_number': frame_number,
            'timestamp': int(time.time() * 1000),
            'data': base64_data
        })
        
        # Display the frame locally
        cv2.imshow('Test Stream', frame)
        
        frame_number += 1
        time.sleep(0.066)  # ~15 FPS
```

## Viewing Existing Streams

The script can connect to and display streams from Firebase, which is useful for viewing the video feed from a Raspberry Pi:

```python
def get_stream_frames(stream_id):
    """Get frames from an existing stream."""
    stream_ref = db.reference(f'/streams/{stream_id}')
    stream_info = stream_ref.get()
    
    if not stream_info:
        print(f"Error: Stream {stream_id} not found")
        return
    
    print(f"Connected to stream: {stream_id}")
    print(f"Status: {stream_info.get('status', 'unknown')}")
    if 'started_at' in stream_info:
        started_at = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stream_info['started_at'] / 1000))
        print(f"Started at: {started_at}")
```

This function connects to a specified stream and continuously polls for new frames:

```python
try:
    cv2.namedWindow('Stream Viewer', cv2.WINDOW_NORMAL)
    
    while True:
        frame_data = latest_frame_ref.get()
        
        if not frame_data or 'data' not in frame_data:
            print("No frame data available")
            time.sleep(0.5)
            continue
        
        # Check if this is a new frame
        if 'frame_number' in frame_data and frame_data['frame_number'] == last_frame_number:
            time.sleep(0.1)  # Short sleep to avoid excessive polling
            continue
        
        # Convert base64 to image
        frame = base64_to_image(frame_data['data'])
        if frame is None:
            print("Failed to decode frame")
            time.sleep(0.5)
            continue
        
        # Display the frame
        cv2.imshow('Stream Viewer', frame)
```

## Saving Frames for BSL Interpretation

When viewing a stream, each frame is also saved to a local file for use by the BSL interpreter:

```python
# Save frame data to file for BSL interpreter
frame_info = {
    'frame_number': frame_data.get('frame_number', 0),
    'timestamp': frame_data.get('timestamp', 0),
    'data': frame_data.get('data', '')
}

with open('current_frame.json', 'w') as f:
    json.dump(frame_info, f)
```

This creates a bridge between the stream viewer and the BSL interpretation system by saving each frame to a file that can be read by the interpreter.

## Listing Active Streams

The script can list all streams in the Firebase database, including their status and start time:

```python
def list_active_streams():
    """List all active streams in the database."""
    streams_ref = db.reference('/streams')
    streams = streams_ref.get()
    
    if not streams:
        print("No streams found in the database")
        return
    
    active_streams = []
    
    for stream_id, stream_data in streams.items():
        status = stream_data.get('status', 'unknown')
        started_at = stream_data.get('started_at', 0)
        
        if started_at:
            started_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(started_at / 1000))
        else:
            started_str = 'Unknown'
        
        print(f"Stream ID: {stream_id}")
        print(f"  Status: {status}")
        print(f"  Started: {started_str}")
        
        if status == 'active':
            active_streams.append(stream_id)
```

This function provides a quick overview of all streams in the database, making it easy to identify active streams for viewing.

## Main Function and Command-Line Interface

The script uses `argparse` to create a command-line interface with three main operations:

```python
def main():
    parser = argparse.ArgumentParser(description='Firebase Stream Handler')
    parser.add_argument('--create', action='store_true', help='Create a test stream using webcam')
    parser.add_argument('--list', action='store_true', help='List all streams')
    parser.add_argument('--view', metavar='STREAM_ID', help='View a specific stream')
    
    args = parser.parse_args()
```

The main function also handles Firebase initialization:

```python
# Initialize Firebase
# Path to your Firebase credentials JSON file
cred_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'firebase-credentials.json')

if not os.path.exists(cred_path):
    print(f"Error: Firebase credentials file not found at {cred_path}")
    print("Please create a service account key file from the Firebase console")
    return

cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://bsltranslator-93f00-default-rtdb.europe-west1.firebasedatabase.app/'
})
```

## Usage Examples

The script can be run in several ways:

1. Create a test stream using the local webcam:
   ```
   python firebase_stream_handler.py --create
   ```

2. List all streams in the database:
   ```
   python firebase_stream_handler.py --list
   ```

3. View a specific stream:
   ```
   python firebase_stream_handler.py --view stream_id
   ```