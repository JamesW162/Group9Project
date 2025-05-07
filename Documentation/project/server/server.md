# Server.js documentation

## Overview

The server.js file creates an Express.js web server that serves the BSL interpreter web interface and manages communication between the web frontend and the Python-based BSL translation system.

## Server Setup and Configuration

The server is built using Express.js and configured to run on port 3000:

```javascript
const express = require('express');
const path = require('path');
const fs = require('fs');
const app = express();
const port = 3000;
```

CORS (Cross-Origin Resource Sharing) is enabled to allow requests from any origin during development:

```javascript
// Enable CORS for local development
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  next();
});
```

Static files are served from the 'website' directory:

```javascript
// Serve static files from the 'website' directory
app.use(express.static(path.join(__dirname, 'website')));
```

## Translation Data Management

The server manages a JSON file that stores the latest BSL translation data:

```javascript
// Path to the translation data file
const translationDataPath = path.join(__dirname, 'translation_data.json');

// Default translation data
const defaultTranslation = {
  translation: "Waiting for BSL translation...",
  timestamp: Date.now()
};
```

If the translation data file doesn't exist, the server creates it with default values:

```javascript
// Initialize translation data file if it doesn't exist
if (!fs.existsSync(translationDataPath)) {
  try {
    fs.writeFileSync(translationDataPath, JSON.stringify(defaultTranslation));
    console.log('Created initial translation_data.json file');
  } catch (err) {
    console.error('Error creating translation data file:', err);
  }
}
```

## API Endpoints

### 1. Reading translation data

The server provides an endpoint to retrieve the current translation:

```javascript
// API route for reading translation data
app.get('/translation-data', (req, res) => {
  try {
    // Check if file exists
    if (fs.existsSync(translationDataPath)) {
      const rawData = fs.readFileSync(translationDataPath);
      const data = JSON.parse(rawData);
      res.json(data);
    } else {
      console.log('Translation data file not found, returning default');
      res.json(defaultTranslation);
    }
  } catch (err) {
    console.error('Error reading translation data:', err);
    res.json(defaultTranslation);
  }
});
```

This endpoint reads the translation_data.json file and returns its contents. If the file is missing or corrupted, it returns the default translation data.

### 2. Updating translation data

The server provides an endpoint to update the translation data:

```javascript
// API route for updating translation data
app.post('/update-translation', (req, res) => {
  try {
    const { translation } = req.body;
    
    if (!translation) {
      return res.status(400).json({ error: 'Translation text is required' });
    }
    
    const data = {
      translation,
      timestamp: Date.now()
    };
    
    fs.writeFileSync(translationDataPath, JSON.stringify(data));
    console.log(`Translation updated: ${translation}`);
    
    res.json({ success: true });
  } catch (err) {
    console.error('Error updating translation:', err);
    res.status(500).json({ error: 'Failed to update translation' });
  }
});
```

This endpoint accepts a translation string in the request body, adds a timestamp, and saves it to the translation_data.json file.

### 3. Starting the interpreter

The server provides an endpoint to start the BSL interpreter Python script:

```javascript
// API route to start the interpreter
app.post('/start-interpreter', (req, res) => {
  try {
    const { stream_id } = req.body;
    
    if (!stream_id) {
      return res.status(400).json({ error: 'Stream ID is required' });
    }
    
    console.log(`Starting interpreter for stream: ${stream_id}`);
    
    // Save active stream ID to file
    fs.writeFileSync('active_stream.txt', stream_id);
    
    // Launch the Python script with the stream ID
    const { spawn } = require('child_process');
    const pythonProcess = spawn('python', ['bsl_bridge_intergration.py', stream_id]);
    
    // Store the process ID for potential later termination
    fs.writeFileSync('interpreter_pid.txt', pythonProcess.pid.toString());
    
    // Log stdout and stderr
    pythonProcess.stdout.on('data', (data) => {
      fs.appendFileSync('interpreter_output.log', data);
    });
    
    pythonProcess.stderr.on('data', (data) => {
      fs.appendFileSync('interpreter_error.log', data);
    });
    
    // Handle process exit
    pythonProcess.on('close', (code) => {
      console.log(`Interpreter process exited with code ${code}`);
    });
    
    res.json({
      success: true,
      message: `Interpreter started for stream: ${stream_id}`,
      pid: pythonProcess.pid
    });
  } catch (err) {
    console.error('Error starting interpreter:', err);
    res.status(500).json({ 
      success: false,
      error: 'Failed to start interpreter: ' + err.message 
    });
  }
});
```

This endpoint:
1. Accepts a stream_id parameter
2. Saves the stream ID to a file
3. Spawns a Python process to run the BSL interpreter script
4. Stores the process ID for later use
5. Sets up logging for the Python script's output
6. Returns success information to the client

## Default Route and Debugging

The server serves the main application HTML file as the default route:

```javascript
// Default route handler
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'website', 'main.html'));
});
```

A debugging endpoint is available to check the file structure:

```javascript
// Debug route to check file structure
app.get('/debug-files', (req, res) => {
  const websitePath = path.join(__dirname, 'website');
  const files = {
    currentDir: __dirname,
    websiteExists: fs.existsSync(websitePath),
    files: []
  };
  
  if (files.websiteExists) {
    try {
      files.files = fs.readdirSync(websitePath);
    } catch (err) {
      files.error = err.message;
    }
  }
  
  res.json(files);
});
```

This endpoint returns information about the server's directory structure and the contents of the website directory, which can be useful for debugging deployment issues.

## Starting the Server

Finally, the server starts listening on the specified port:

```javascript
// Start the server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
```