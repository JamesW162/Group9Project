// DOM elements

const streamSelector = document.getElementById('streamSelector');

const loadStreamBtn = document.getElementById('loadStreamBtn');

const stopStreamBtn = document.getElementById('stopStreamBtn');

const streamVideo = document.getElementById('streamVideo');

const streamInfo = document.getElementById('streamInfo');
 
// Variables to track state

let currentStreamId = null;

let frameListener = null;
 
/**

* Load available streams from Firebase

*/

function loadStreams() {

    const streamsRef = database.ref('/streams');

    streamsRef.once('value', (snapshot) => {

        const streams = snapshot.val();

        // Clear the selector

        streamSelector.innerHTML = '';

        if (!streams) {

            streamSelector.innerHTML = '<option value="">No streams available</option>';

            return;

        }

        // Add option for each stream

        Object.keys(streams).forEach((streamId) => {

            const stream = streams[streamId];

            const option = document.createElement('option');

            option.value = streamId;

            // Format date from timestamp

            let startedAt = 'Unknown';

            if (stream.started_at) {

                const date = new Date(stream.started_at);

                startedAt = date.toLocaleString();

            }

            option.textContent = `${streamId} (${startedAt}) - ${stream.status || 'unknown'}`;

            option.classList.add(`status-${stream.status || 'unknown'}`);

            streamSelector.appendChild(option);

        });

        // Add refresh option

        const refreshOption = document.createElement('option');

        refreshOption.value = 'refresh';

        refreshOption.textContent = '-- Refresh Stream List --';

        streamSelector.appendChild(refreshOption);

    });

}
 
/**

* Start viewing the selected stream

* @param {string} streamId - ID of the stream to view

*/

function startViewingStream(streamId) {

    currentStreamId = streamId;

    // Get stream info

    const streamRef = database.ref(`/streams/${streamId}`);

    streamRef.once('value', (snapshot) => {

        const streamData = snapshot.val();

        if (!streamData) {

            streamInfo.textContent = 'Stream not found.';

            return;

        }

        // Update stream info

        let infoText = `Stream ID: ${streamId}<br>`;

        infoText += `Status: <span class="status-${streamData.status || 'unknown'}">${streamData.status || 'unknown'}</span><br>`;

        if (streamData.started_at) {

            const date = new Date(streamData.started_at);

            infoText += `Started: ${date.toLocaleString()}<br>`;

        }

        if (streamData.ended_at) {

            const date = new Date(streamData.ended_at);

            infoText += `Ended: ${date.toLocaleString()}<br>`;

        }

        if (streamData.resolution) {

            infoText += `Resolution: ${streamData.resolution}<br>`;

        }

        if (streamData.frame_rate) {

            infoText += `Frame Rate: ${streamData.frame_rate} fps<br>`;

        }

        if (streamData.frames_sent) {

            infoText += `Frames Sent: ${streamData.frames_sent}<br>`;

        }

        streamInfo.innerHTML = infoText;

        // Start listening for frames

        startFrameListener(streamId);

    });

}
 
/**

* Start listening for new frames

* @param {string} streamId - ID of the stream to listen to

*/

function startFrameListener(streamId) {

    const frameRef = database.ref(`/streams/${streamId}/latest_frame`);

    // Listen for new frames

    frameListener = frameRef.on('value', (snapshot) => {

        const frameData = snapshot.val();

        if (!frameData || !frameData.data) {

            console.log('No frame data available');

            return;

        }

        // Update the image with the new frame

        streamVideo.src = `data:image/jpeg;base64,${frameData.data}`;

        // Update frame info in the stream info panel

        const frameInfoElement = document.getElementById('frameInfo');

        if (frameInfoElement) {

            const timestamp = new Date(frameData.timestamp).toLocaleTimeString();

            frameInfoElement.innerHTML = `Frame: ${frameData.frame_number}, Time: ${timestamp}`;

        } else {

            // Create frame info element if it doesn't exist

            const newFrameInfo = document.createElement('div');

            newFrameInfo.id = 'frameInfo';

            const timestamp = new Date(frameData.timestamp).toLocaleTimeString();

            newFrameInfo.innerHTML = `Frame: ${frameData.frame_number}, Time: ${timestamp}`;

            streamInfo.appendChild(newFrameInfo);

        }

    });

}
 
/**

* Stop viewing the current stream

*/

function stopViewingStream() {

    if (currentStreamId && frameListener) {

        // Stop listening for frames

        database.ref(`/streams/${currentStreamId}/latest_frame`).off('value', frameListener);

        frameListener = null;

        currentStreamId = null;

        // Reset the video display

        streamVideo.src = '';

        streamInfo.textContent = 'No stream selected. Please select a stream from the dropdown above.';

    }

}
 
// Event handlers

loadStreamBtn.addEventListener('click', () => {

    const streamId = streamSelector.value;

    // Handle refresh option

    if (streamId === 'refresh') {

        loadStreams();

        return;

    }

    if (!streamId) {

        alert('Please select a stream first');

        return;

    }

    // Stop current stream if any

    stopViewingStream();

    // Start viewing the selected stream

    startViewingStream(streamId);

});
 
stopStreamBtn.addEventListener('click', stopViewingStream);
 
// Initialize by loading available streams

document.addEventListener('DOMContentLoaded', loadStreams);
