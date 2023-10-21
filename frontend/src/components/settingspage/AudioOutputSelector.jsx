import React, { useState, useEffect } from 'react';

const AudioOutputSelector = ({ onDevicesChange }) => {
  const [outputDevices, setOutputDevices] = useState([]);
  const [selectedOutputDevice, setSelectedOutputDevice] = useState('');

  useEffect(() => {
    // Request permission and fetch output devices
    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(stream => {
        // After obtaining an audio stream, enumerate the devices
        navigator.mediaDevices.enumerateDevices()
          .then(devices => {
            const outputs = devices.filter(device => device.kind === 'audiooutput');
            setOutputDevices(outputs);
            stream.getTracks().forEach(track => track.stop()); // Stop the used stream
            onDevicesChange(outputs); // Notify parent component of the change
          });
      })
      .catch(err => {
        console.error("Error fetching devices: ", err);
      });
  }, [onDevicesChange]);

  const handleOutputDeviceChange = (e) => {
    setSelectedOutputDevice(e.target.value);
  };

  return (
    <div>
      <label>Output Device</label>
      <select value={selectedOutputDevice} onChange={handleOutputDeviceChange}>
        {outputDevices.map((device, index) => (
          <option key={device.deviceId} value={device.deviceId}>
            {device.label || `Device ${index + 1}`}
          </option>
        ))}
      </select>
    </div>
  );
};

export default AudioOutputSelector;
