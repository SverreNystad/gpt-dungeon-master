import React, { useEffect, useState } from 'react';

function MicrophoneDetector() {
  const [microphones, setMicrophones] = useState([]);

  useEffect(() => {
    // Request microphone access
    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(stream => {
        // Access granted, now get devices
        navigator.mediaDevices.enumerateDevices()
          .then(devices => {
            const mics = devices.filter(device => device.kind === 'audioinput');
            setMicrophones(mics);
          })
          .catch(err => {
            console.error("An error occurred while trying to get the list of devices: ", err);
          });

        // Stop the tracks, we don't need to keep streaming audio
        stream.getTracks().forEach(track => track.stop());
      })
      .catch(err => {
        console.error("An error occurred while trying to get permission to use the microphone: ", err);
      });
  }, []); // Empty dependency array means this useEffect runs once when component mounts

  return (
    <div>
      <h1>Available Microphones:</h1>
      <ul>
        {microphones.map((mic, index) => (
          <li key={index}>{mic.label || `Microphone ${index + 1}`}</li>
        ))}
      </ul>
    </div>
  );
}

export default MicrophoneDetector;
