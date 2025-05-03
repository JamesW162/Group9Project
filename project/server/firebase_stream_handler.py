import cv2
import base64
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
import argparse
import os
import json

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
    
    print(f"Created test stream with ID: {stream_id}")
    
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
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except KeyboardInterrupt:
        print("Stream interrupted by user")
    finally:
        # Set stream status to ended
        stream_ref.update({'status': 'ended'})
        cap.release()
        cv2.destroyAllWindows()
        print(f"Test stream {stream_id} ended")

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
    
    latest_frame_ref = stream_ref.child('latest_frame')
    last_frame_number = -1
    
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
            
            # Update last frame number
            last_frame_number = frame_data.get('frame_number', -1)
            
            # Save frame data to file for BSL interpreter
            frame_info = {
                'frame_number': frame_data.get('frame_number', 0),
                'timestamp': frame_data.get('timestamp', 0),
                'data': frame_data.get('data', '')
            }
            
            with open('current_frame.json', 'w') as f:
                json.dump(frame_info, f)
            
            # Check for exit key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except KeyboardInterrupt:
        print("Viewer interrupted by user")
    finally:
        cv2.destroyAllWindows()
        print(f"Disconnected from stream {stream_id}")

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
    
    print(f"\nTotal streams: {len(streams)}")
    print(f"Active streams: {len(active_streams)}")
    
    return active_streams

def main():
    parser = argparse.ArgumentParser(description='Firebase Stream Handler')
    parser.add_argument('--create', action='store_true', help='Create a test stream using webcam')
    parser.add_argument('--list', action='store_true', help='List all streams')
    parser.add_argument('--view', metavar='STREAM_ID', help='View a specific stream')
    
    args = parser.parse_args()
    
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
    
    if args.create:
        create_test_stream()
    elif args.list:
        list_active_streams()
    elif args.view:
        get_stream_frames(args.view)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()