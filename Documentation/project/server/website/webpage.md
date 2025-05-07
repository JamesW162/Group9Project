# webpage.html documentation

### 1. User Authentication System

The site includes basic authentication features that check if a user is logged in before accessing the translation services:

```javascript
window.onload = function() {
    if (localStorage.getItem('logged_in') !== 'true') {
        window.location.href = 'login.html';
    }
};
```

### 2. Header & Navigation

The header section contains a logo and navigation buttons:

```html
<header>
    <img src="logo.png" alt="Website Logo" onerror="this.src='data:image/png;base64,...'">
    <div class="header-buttons">
        <button class="header-button" id="home-btn">Main Page</button>
        <button class="header-button" id="logout-btn">Log Out</button>
    </div>
</header>
```

### 3. Translation Display Area

A dedicated area shows the translated text from the sign language:

```html
<div id="translationText" class="translation-box">
    <p>Your translation will appear here once a stream is connected...</p>
</div>
```

### 4. Video Stream Connection Interface

Users can select and connect to available BSL video streams:

```html
<div id="streamSelector">
    <label for="streamId">Your Stream: </label>
    <select id="streamId"></select>
    <button id="connectBtn" class="stream-btn">Connect</button>
    <button id="refreshBtn" class="stream-btn">Refresh Stream</button>
    <button id="startInterpreterBtn" class="stream-btn">Start Interpreter</button>
</div>
```

### 5. Firebase Integration

The application integrates with Firebase for real-time database functionality:

```javascript
const firebaseConfig = {
    apiKey: "AIzaSyAEzhS9bkzcN5-YLuvta9Vm2aYM6DYl2PU",
    authDomain: "bsltranslator-93f00.firebaseapp.com",
    databaseURL: "https://bsltranslator-93f00-default-rtdb.europe-west1.firebasedatabase.app/",
    projectId: "bsltranslator-93f00",
    storageBucket: "bsltranslator-93f00.appspot.com",
    messagingSenderId: "547548973040",
    appId: "1:547548973040:web:4c7b2802aedcf6e84a7f35"
};
```

## Core Functionality

### Device & User Identification

The site associates users with a Personal Identifier ID (PIID) to manage their streams:

```javascript
function loadUserPIID() {
    const userPIID = localStorage.getItem('user_piid');
    
    if (userPIID) {
        // PIID already in localStorage
        devicePIID.textContent = userPIID;
        loadUserStreams(userPIID);
    } else {
        // Look up PIID from Firebase based on user email
        // ...
    }
}
```

### Stream Management

The application loads streams associated with the user's device:

```javascript
function loadUserStreams(piid) {
    if (!piid) {
        displayError('No Device ID assigned. Cannot load streams.');
        return;
    }
    
    const streamsRef = database.ref('/streams');
    streamsRef.once('value', (snapshot) => {
        // ...display user's streams in the dropdown...
    });
}
```

### Connecting to Streams

Users can connect to their streams and view the video content:

```javascript
function connectToStream() {
    const streamId = streamSelector.value;
    if (!streamId) {
        displayError('Please select a stream');
        return;
    }
    
    // Set up stream references and listeners
    currentStreamId = streamId;
    currentStreamRef = database.ref(`/streams/${streamId}`);
    
    // Listen for new frames
    latestFrameRef = database.ref(`/streams/${streamId}/latest_frame`);
    latestFrameRef.on('value', (frameSnapshot) => {
        const frameData = frameSnapshot.val();
        if (frameData && frameData.data) {
            displayFrame(frameData);
            // ...
        }
    });
}
```

### BSL Interpretation

The site includes functionality to start an interpreter service for sign language translation:

```javascript
function startInterpreter() {
    if (!currentStreamId) {
        displayError('Please connect to a stream first');
        return;
    }
    
    fetch('/start-interpreter', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ stream_id: currentStreamId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            interpreterActive = true;
            updateInterpreterStatus(true);
            // ...
        }
    });
}
```

### Translation Updates

The application periodically checks for new translations:

```javascript
function checkForTranslationUpdates() {
    fetch('/translation-data?' + new Date().getTime())
        .then(response => response.json())
        .then(data => {
            if (data && data.translation) {
                updateTranslationText(data.translation);
            }
        });
}

// Set up translation update checker
setInterval(checkForTranslationUpdates, 1000);
```

## User Experience Features

### Loading Animations

The interface includes a loading animation while initializing:

```javascript
let dots = "";
const interval = setInterval(() => {
    dots = dots.length < 3 ? dots + "." : ""; // Cycle through '.', '..', '...'
    loadingText.textContent = `Loading Translation ${dots}`;
}, 500);
```

### Error Handling

The site provides user-friendly error messages:

```javascript
function displayError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    setTimeout(() => {
        errorMessage.style.display = 'none';
    }, 5000); // Hide after 5 seconds
}
```

### Status Indicators

Visual indicators show the status of the interpreter and stream:

```javascript
function updateInterpreterStatus(active) {
    interpreterStatusIndicator.className = active ? 
        'status-indicator status-active' : 
        'status-indicator status-inactive';
    
    interpreterStatusText.textContent = active ? 
        'BSL Interpreter: Active and Processing' : 
        'BSL Interpreter: Not Running';
}
```