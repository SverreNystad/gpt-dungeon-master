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
    // ... other settings ...
  });

  // Function to update individual setting
  const updateSetting = (key, value) => {
    setSettings(prevSettings => ({
      ...prevSettings,
      [key]: value,
    }));
  };

  // Function to reset all settings to default
  const resetToDefaults = () => {
    setSettings({
      language: 'en',
      backgroundVolume: 0.5,
      gptSpeech: 0.5,
      resolution: '1920x1080',
      isFullscreen: false,
      // ... other settings ...
    });
  };

  return (
    <SettingsContext.Provider value={{ settings, updateSetting, resetToDefaults }}>
      {children}
    </SettingsContext.Provider>
  );
};
