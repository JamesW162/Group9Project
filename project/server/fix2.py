#!/usr/bin/env python3
# bsl_fixes.py - Apply common fixes to the BSL interpreter

import os
import sys
import subprocess
import platform
import json
import shutil
from pathlib import Path

def create_empty_model():
    """Create a placeholder model file for testing purposes"""
    try:
        import pickle
        import numpy as np
        from sklearn.ensemble import RandomForestClassifier
        
        # Create a simple placeholder model
        model = RandomForestClassifier(n_estimators=10)
        X = np.random.rand(10, 42*2)  # 42 landmarks * 2 dimensions (x,y) for one hand
        y = ['A', 'B', 'C', 'D', 'E'] * 2  # 5 dummy classes
        model.fit(X, y)
        
        # Save the model
        with open('model.p', 'wb') as f:
            pickle.dump({'model': model}, f)
        
        print("✓ Created placeholder model.p for testing")
        return True
    except Exception as e:
        print(f"✗ Failed to create model file: {str(e)}")
        return False

def create_firebase_credential():
    """Create a placeholder Firebase credential file for testing"""
    cred_content = {
      "type": "service_account",
      "project_id": "bsltranslator-93f00",
      "private_key_id": "55978db132xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEuwIBADANBgkqhkiG9w0BAQEFAASCBKUwggShAgEAAoIBAQCxxxxxxxxxxx\n-----END PRIVATE KEY-----\n",
      "client_email": "firebase-adminsdk-fbsvc@bsltranslator-93f00.iam.gserviceaccount.com",
      "client_id": "000000000000000000000",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40bsltranslator-93f00.iam.gserviceaccount.com",
      "universe_domain": "googleapis.com"
    }
    
    try:
        with open('bsltranslator-93f00-firebase-adminsdk-fbsvc-55978db132.json', 'w') as f:
            json.dump(cred_content, f, indent=2)
        
        print("✓ Created placeholder Firebase credential file")
        print("  Note: This is just a template file and won't work with real Firebase!")
        return True
    except Exception as e:
        print(f"✗ Failed to create credential file: {str(e)}")
        return False

def create_stream_id_file():
    """Create a test active_stream.txt file"""
    try:
        with open('active_stream.txt', 'w') as f:
            f.write("20250504_155249")  # Use the stream ID from your error message
        
        print("✓ Created active_stream.txt with test stream ID")
        return True
    except Exception as e:
        print(f"✗ Failed to create stream ID file: {str(e)}")
        return False

def create_empty_translation_data():
    """Create an empty translation data file"""
    try:
        with open('translation_data.json', 'w') as f:
            json.dump({"translation": "BSL Translation will appear here...", "timestamp": 0}, f)
        
        print("✓ Created empty translation_data.json file")
        return True
    except Exception as e:
        print(f"✗ Failed to create translation data file: {str(e)}")
        return False

def update_code(original_file, output_file):
    """Create a fixed version of the code"""
    try:
        # Read the original file
        with open(original_file, 'r') as f:
            content = f.read()
        
        # Make fixes to the code
        updates = {
            # Fix 1: Make Firebase initialization optional and better error handling
            "try:\n    # Look for the credentials file in common locations": 
            "try:\n    print('Attempting to initialize Firebase...')\n    # Look for the credentials file in common locations",
            
            "if not cred_found:\n        print(\"Firebase credentials file not found. Please ensure it exists in one of these locations:\")": 
            "if not cred_found:\n        print(\"Firebase credentials file not found. Continuing in offline mode.\")\n        print(\"WARNING: Some features may not work without Firebase credentials.\")",
            
            "if not cred_found:\n        print(\"Firebase credentials file not found. Please ensure it exists in one of these locations:\")\n        for path in credential_paths:\n            print(f\"  - {path}\")\n        sys.exit(1)": 
            "if not cred_found:\n        print(\"Firebase credentials file not found. Continuing in offline mode.\")\n        print(\"WARNING: Some features may not work without Firebase credentials.\")",
            
            # Fix 2: Skip NLTK download if it fails
            "try:\n    nltk.download('words', quiet=True)\n    word_dict = set(word.upper() for word in words.words())": 
            "try:\n    nltk.download('words', quiet=True)\n    try:\n        word_dict = set(word.upper() for word in words.words())\n    except LookupError:\n        # Create a fallback dictionary if NLTK data failed to download\n        print(\"Failed to download NLTK words corpus, using fallback dictionary\")\n        word_dict = set(['HELLO', 'THANK', 'YOU', 'PLEASE', 'HELP', 'GOOD', 'BAD', \n                         'YES', 'NO', 'MAYBE', 'HOW', 'WHAT', 'WHERE', 'WHEN', 'WHO'])",
            
            # Fix 3: Add offline mode for Firebase
            "def get_available_streams():\n    \"\"\"Get list of active streams from Firebase.\"\"\"": 
            "def get_available_streams():\n    \"\"\"Get list of active streams from Firebase.\"\"\"\n    # Check if we're in offline mode\n    if not firebase_admin._apps:\n        print(\"Running in offline mode, can't get streams from Firebase\")\n        return {\"offline_test_stream\": {\"status\": \"active\"}}",
            
            # Fix 4: Add better model loading with default fallback
            "if not model_loaded:\n        print(\"Model file not found. Please ensure model.p exists in one of these locations:\")\n        for path in model_paths:\n            print(f\"  - {path}\")\n        sys.exit(1)": 
            "if not model_loaded:\n        print(\"Model file not found. Creating a simple placeholder model...\")\n        try:\n            from sklearn.ensemble import RandomForestClassifier\n            model = RandomForestClassifier(n_estimators=10)\n            X = np.random.rand(10, 42*2)  # 42 landmarks * 2 dimensions\n            y = ['A', 'B', 'C', 'D', 'E'] * 2  # 5 dummy classes\n            model.fit(X, y)\n            print(\"Created placeholder model for testing\")\n            model_loaded = True\n        except Exception as e:\n            print(f\"Failed to create placeholder model: {e}\")\n            sys.exit(1)",
            
            # Fix 5: Make Firebase update operations optional
            "def start_stream_processing(stream_id):\n    \"\"\"Start processing frames from the selected stream.\"\"\"": 
            "def start_stream_processing(stream_id):\n    \"\"\"Start processing frames from the selected stream.\"\"\"\n    \n    # Check if we're in offline mode\n    offline_mode = not firebase_admin._apps\n    if offline_mode:\n        print(\"Running in offline mode with test data\")",
            
            # Fix 6: Add offline test mode
            "    # Get reference to the latest frame\n    latest_frame_ref = db.reference(f'/streams/{stream_id}/latest_frame')": 
            "    # Get reference to the latest frame\n    if not offline_mode:\n        latest_frame_ref = db.reference(f'/streams/{stream_id}/latest_frame')\n    else:\n        print(\"Using offline test mode with simulated frames\")",
            
            # Fix 7: Add offline test frame generator
            "            # Get the latest frame data\n            frame_data = latest_frame_ref.get()": 
            "            # Get the latest frame data\n            if not offline_mode:\n                frame_data = latest_frame_ref.get()\n            else:\n                # Generate test frame in offline mode\n                import time\n                import numpy as np\n                import base64\n                \n                # Create a simple test frame\n                test_frame = np.zeros((480, 640, 3), dtype=np.uint8)\n                test_frame[:,:] = (100, 100, 100)  # Gray background\n                \n                # Add a timestamp\n                cv2.putText(test_frame, f\"Test Frame - {time.strftime('%H:%M:%S')}\", \n                            (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)\n                \n                # Encode to base64\n                _, buffer = cv2.imencode('.jpg', test_frame)\n                jpg_as_text = base64.b64encode(buffer).decode('utf-8')\n                \n                # Create frame data structure\n                frame_data = {\n                    'data': jpg_as_text,\n                    'frame_number': int(time.time() * 10) % 1000,  # Pseudo-unique frame number\n                    'timestamp': int(time.time())\n                }\n                \n                # Sleep to limit frame rate\n                time.sleep(0.1)",
            
            # Fix 8: Make stream status check optional
            "            # Periodically check if the stream is still active\n            current_time = time.time()\n            if current_time - last_status_check > 30:  # Check every 30 seconds\n                stream_ref = db.reference(f'/streams/{stream_id}')\n                stream_data = stream_ref.get()\n                if not stream_data or stream_data.get('status') != 'active':\n                    print(f\"Stream {stream_id} is no longer active.\")\n                    running = False\n                    break\n                last_status_check = current_time": 
            "            # Periodically check if the stream is still active\n            current_time = time.time()\n            if not offline_mode and current_time - last_status_check > 30:  # Check every 30 seconds\n                try:\n                    stream_ref = db.reference(f'/streams/{stream_id}')\n                    stream_data = stream_ref.get()\n                    if not stream_data or stream_data.get('status') != 'active':\n                        print(f\"Stream {stream_id} is no longer active.\")\n                        running = False\n                        break\n                except Exception as e:\n                    print(f\"Error checking stream status: {e}\")\n                last_status_check = current_time",
        }
        
        # Apply all the updates
        for old_str, new_str in updates.items():
            content = content.replace(old_str, new_str)
        
        # Write the fixed content to the output file
        with open(output_file, 'w') as f:
            f.write(content)
        
        print(f"✓ Created fixed version of the code: {output_file}")
        return True
    except Exception as e:
        print(f"✗ Failed to update code: {str(e)}")
        return False

def install_required_dependencies():
    """Install required dependencies"""
    dependencies = [
        'mediapipe', 
        'opencv-python', 
        'numpy', 
        'nltk', 
        'firebase-admin',
        'scikit-learn'  # Needed for the placeholder model
    ]
    
    print("Installing required dependencies...")
    
    for dep in dependencies:
        try:
            print(f"Installing {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✓ Installed {dep}")
        except Exception as e:
            print(f"✗ Failed to install {dep}: {str(e)}")
    
    return True

def main():
    """Main function to apply fixes"""
    print("\n===== BSL Interpreter Fix Tool =====\n")
    
    # Ask user what they want to do
    print("Options:")
    print("1. Fix everything automatically")
    print("2. Create missing files only")
    print("3. Install dependencies only")
    print("4. Create fixed version of code only")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == '1' or choice == '2' or choice == '1':
        # Create missing files
        print("\nCreating missing files...")
        create_empty_model()
        create_firebase_credential()
        create_stream_id_file()
        create_empty_translation_data()
    
    if choice == '1' or choice == '3':
        # Install dependencies
        print("\nInstalling dependencies...")
        install_required_dependencies()
    
    if choice == '1' or choice == '4':
        # Create fixed version of code
        print("\nCreating fixed version of code...")
        update_code('paste.txt', 'bsl_interpreter_fixed.py')
    
    print("\n===== Next Steps =====")
    if choice == '1' or choice == '4':
        print("1. Run the fixed version with:")
        print("   python bsl_interpreter_fixed.py")
    else:
        print("1. Run the original script:")
        print("   python paste.txt")
    
    print("\nNote: You may need to press 'q' or ESC to exit the application if it runs successfully.\n")

if __name__ == "__main__":
    main()