// MicrophoneDetector.js
import React, { useState, useEffect } from 'react';

const MicrophoneDetector = ({currentMic, onMicrophonesChange }) => {
  const [microphones, setMicrophones] = useState([]);
  const [selectedMic, setSelectedMic] = useState(currentMic);

  useEffect(() => {
    // Request permission and fetch microphones
    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(stream => {
        // After obtaining an audio stream, enumerate the devices
        navigator.mediaDevices.enumerateDevices()
          .then(devices => {
            const mics = devices.filter(device => device.kind === 'audioinput');
            setMicrophones(mics);
            onMicrophonesChange(mics, selectedMic); // Pass the default mic as a second argument

            // When no microphone is selected, select the first one
            if (mics.length > 0 && selectedMic == '') {
              setSelectedMic(mics[0].deviceId);
            }
            stream.getTracks().forEach(track => track.stop()); // Stop the used stream
          });
      })
      .catch(err => {
        console.error("Error fetching devices: ", err);
      });
  }, [selectedMic]);

  const handleMicChange = (e) => {
    setSelectedMic(e.target.value);
    // Here, you might also want to notify the parent component of the selection change
  };

  return (
    <div>
      <label>Microphone</label>
      <select value={selectedMic} onChange={handleMicChange}>
        {microphones.map((mic, index) => (
          <option key={mic.deviceId} value={mic.deviceId}>
            {mic.label || `Microphone ${index + 1}`}
          </option>
        ))}
      </select>
    </div>
  );
};

export default MicrophoneDetector;
