# BSL bridge implementation documentation
This Python script implements a real-time British Sign Language (BSL) gesture recognition system. It uses OpenCV, MediaPipe, and a pre-trained ML model to predict hand gestures and convert them into text. The results are streamed live and synchronized with a Firebase Realtime Database.

---

## 📦 Dependencies

* Python 3.7+
* OpenCV (`cv2`)
* MediaPipe
* scikit-learn
* NumPy
* NLTK
* requests
* Firebase Admin SDK

Install dependencies:

```bash
pip install opencv-python mediapipe scikit-learn numpy nltk requests firebase-admin
```

---

## 🧠 Functionality Overview

### 🔍 Stream Input Handling

* Reads the active stream ID from `active_stream.txt` or via command-line.

### 🧾 Word Validation

* Downloads and uses NLTK corpus of English words.
* Falls back to a small dictionary if download fails.

### ☁️ Firebase Realtime DB

* Connects using credentials from `bsltranslator-93f00-firebase-adminsdk-fbsvc-55978db132.json`.
* Retrieves available video streams and writes final recognized translations.

### ✋ Hand Detection & Recognition

* Uses MediaPipe to extract hand landmarks.
* Predicts BSL letters using a trained ML model (`model.p`).
* Maintains a gesture buffer to smooth predictions.

### 💡 Word Suggestions

* Suggests English words based on the current letter input using `difflib`.
* Finalizes a word after 3.5 seconds of inactivity.

### 🖼️ Frame Processing

* Draws hand landmarks.
* Displays current buffer and suggestion.
* Converts base64 image frames for processing.

---

## 🛠️ Key Components

### `process_frame(frame)`

* Core function that processes image frames for hand landmarks, runs predictions, and updates current translation buffer.

### `get_word_suggestions(fragment, dictionary)`

* Uses `difflib.get_close_matches()` to suggest possible completions.

### `update_translation_data(translation)`

* Saves latest recognized sentence to a local JSON and optionally updates an HTTP endpoint.

### `get_available_streams(piid=None)`

* Queries Firebase to get active stream list.

---

## 📁 Files Required

* `model.p`: Pickle file containing your trained ML model.
* `active_stream.txt`: Contains stream ID for input source.
* `bsltranslator-93f00-firebase-adminsdk-fbsvc-55978db132.json`: Firebase credentials file.

---

## 🖥️ Running the Script

```bash
python script_name.py [optional_stream_id]
```

* If `optional_stream_id` is omitted, it will use `active_stream.txt`.

---

## 🔒 Error Handling

* Handles missing files, Firebase errors, prediction issues, and fallback paths for reliability.

---

## 🔧 Customization

You may:

* Replace the ML model with your own.
* Change the gesture-to-letter mappings.
* Extend with sentence prediction or speech output.

---

## 🧪 Testing

Make sure to:

* Verify `model.p` matches the expected input size.
* Ensure MediaPipe hands are correctly detecting landmarks.
* Check Firebase access is valid.

---

## ✨ License

MIT

---

## 🙋 Support

For issues or contributions, feel free to open a GitHub issue or pull request.
