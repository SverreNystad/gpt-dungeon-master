import React, { createContext, useState } from 'react';

export const SettingsContext = createContext();

export const SettingsProvider = ({ children }) => {
  // State for settings
  const [settings, setSettings] = useState({
    language: 'en',
    backgroundVolume: 0.5,
    gptSpeech: 0.5,
    resolution: '1920x1080',
    isFullscreen: false,
    mute: false,
    selectedMic: '',
    microphones: [],
    selectedOutputDevice: '',
    outputDevices: [],
    // ... other settings ...
  });

  // Function to update individual setting
  const updateSetting = (key, value) => {
    setSettings(prevSettings => ({
      ...prevSettings,
      [key]: value,
    }));
  };
  
  // Toggle fullscreen
  const toggleFullScreen = () => {
    if (!document.fullscreenElement) {
        if (document.documentElement.requestFullscreen) {
          document.documentElement.requestFullscreen();
        } else if (document.documentElement.mozRequestFullScreen) { /* Firefox */
          document.documentElement.mozRequestFullScreen();
        } else if (document.documentElement.webkitRequestFullscreen) { /* Chrome, Safari and Opera */
          document.documentElement.webkitRequestFullscreen();
        } else if (document.documentElement.msRequestFullscreen) { /* IE/Edge */
          document.documentElement.msRequestFullscreen();
        }
        updateSetting('isFullscreen', true); // update your state variable
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      } else if (document.mozCancelFullScreen) { /* Firefox */
        document.mozCancelFullScreen();
      } else if (document.webkitExitFullscreen) { /* Chrome, Safari and Opera */
        document.webkitExitFullscreen();
      } else if (document.msExitFullscreen) { /* IE/Edge */
        document.msExitFullscreen();
      }
      updateSetting('isFullscreen', false); // update your state variable
    }
}

  // Function to reset all settings to default
  const resetToDefaults = () => {
    setSettings({
      language: 'en',
      backgroundVolume: 0.5,
      gptSpeech: 0.5,
      resolution: '1920x1080',
      isFullscreen: false,
      mute: false,
      selectedMic: '',
      microphones: [],
      selectedOutputDevice: '',
      outputDevices: [],
      // ... other settings ...
    });
    toggleFullScreen();

  };

  return (
    <SettingsContext.Provider value={{ settings, updateSetting, resetToDefaults, toggleFullScreen}}>
      {children}
    </SettingsContext.Provider>
  );
};


