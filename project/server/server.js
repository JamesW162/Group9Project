const express = require('express');
const path = require('path');
const fs = require('fs');
const app = express();
const port = 3000;

// Enable CORS for local development
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  next();
});

// Serve static files from the 'website' directory
app.use(express.static(path.join(__dirname, 'website')));

// Handle JSON requests
app.use(express.json());

// Path to the translation data file
const translationDataPath = path.join(__dirname, 'translation_data.json');

// Default translation data
const defaultTranslation = {
  translation: "Waiting for BSL translation...",
  timestamp: Date.now()
};

// Initialize translation data file if it doesn't exist
if (!fs.existsSync(translationDataPath)) {
  try {
    fs.writeFileSync(translationDataPath, JSON.stringify(defaultTranslation));
    console.log('Created initial translation_data.json file');
  } catch (err) {
    console.error('Error creating translation data file:', err);
  }
}

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

// Default route handler
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'website', 'main.html'));
});

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

// Start the server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});