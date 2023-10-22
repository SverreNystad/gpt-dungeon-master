import React, { useState, useEffect } from 'react';

const AudioOutputSelector = ({ outPutDevice, onDevicesChange }) => {
  const [outputDevices, setOutputDevices] = useState([]);
  const [selectedOutputDevice, setSelectedOutputDevice] = useState(outPutDevice);

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
            
            // When no output device is selected, select the first one
            if (outputs.length > 0 && selectedOutputDevice == '') {
              setSelectedOutputDevice(outputs[0].deviceId);
            }
            onDevicesChange(outputs, selectedOutputDevice); // Notify parent component of the change
          });
      })
      .catch(err => {
        console.error("Error fetching devices: ", err);
      });
  }, [selectedOutputDevice]);

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
