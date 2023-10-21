// MicrophoneDetector.js
import React, { useState, useEffect } from 'react';

const MicrophoneDetector = ({ onMicrophonesChange }) => {
  const [microphones, setMicrophones] = useState([]);
  const [selectedMic, setSelectedMic] = useState('');

  useEffect(() => {
    // Request permission and fetch microphones
    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(stream => {
        // After obtaining an audio stream, enumerate the devices
        navigator.mediaDevices.enumerateDevices()
          .then(devices => {
            const mics = devices.filter(device => device.kind === 'audioinput');
            setMicrophones(mics);
  
            // Find the microphone that matches the one in the stream
            const defaultMic = stream.getTracks().find(track => track.kind === 'audio').getSettings().deviceId;
            setSelectedMic(defaultMic);
            onMicrophonesChange(mics, defaultMic); // Pass the default mic as a second argument
  
            stream.getTracks().forEach(track => track.stop()); // Stop the used stream
          });
      })
      .catch(err => {
        console.error("Error fetching devices: ", err);
      });
  }, [onMicrophonesChange]);

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
