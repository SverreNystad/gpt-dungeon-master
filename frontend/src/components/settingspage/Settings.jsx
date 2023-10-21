import React, { useContext, useEffect} from 'react';
import { SettingsContext } from '../../contexts/SettingsContext'; // adjust the import path as needed
import AudioOutputSelector from "./AudioOutputSelector";
import MicrophoneDetector from "./MicrophoneDetector";
const SettingsPage = () => {
    const { settings, updateSetting, resetToDefaults, toggleFullScreen } = useContext(SettingsContext);
    
    // Fetch the list of microphones when the component mounts and update context
    const handleMicrophonesChange = (newMics, selectedMic) => {
        // Update your context or state with the new microphones
        updateSetting('microphones', newMics);

        if (selectedMic) {
            updateSetting('selectedMic', selectedMic);
        }
    };
    
    // Fetch the list of microphones when the component mounts and update context
    const handleOutputDevicesChange = (newDevices, selectedOutputDevice) => {
        // Update your context or state with the new devices
        updateSetting('outputDevices', newDevices);

        if (selectedOutputDevice) {
            updateSetting('selectedOutputDevice', selectedOutputDevice);
        }
    };

    // handler for changes in settings
    const handleSettingChange = (setting) => (e) => {
      updateSetting(setting, e.target.value);
    };

    return (
        <div>
            <h1>Settings</h1>

            {/* Audio Settings */}
            <section>
                <h2>Audio Settings</h2>
                <div>
                    <label>Background Music Volume</label>
                    <input 
                        type="range" 
                        min="0" max="1" 
                        step="0.01" 
                        value={settings.backgroundVolume} 
                        onChange={handleSettingChange("backgroundVolume")} 
                    />

                    <label>DM narration Volume</label>
                    <input 
                        type="range" 
                        min="0" max="1" 
                        step="0.01" 
                        value={settings.gptSpeech} 
                        onChange={handleSettingChange("gptSpeech")} 
                    />
                    <label> Mute sound</label>
                    <input 
                        type="checkbox" 
                        checked={settings.mute} 
                        onChange={handleSettingChange("mute")} 
                    />
                </div>
                <AudioOutputSelector outPutDevice={settings.selectedOutputDevice} onDevicesChange={handleOutputDevicesChange} />
                <MicrophoneDetector currentMic={settings.selectedMic} onMicrophonesChange={handleMicrophonesChange} />
            </section>

            {/* Display Settings */}
            <section>
                <h2>Display Settings</h2>
                <div>
                    <label>Screen Resolution</label>
                    <select value={settings.resolution} onChange={handleSettingChange("resolution")}>
                        <option value="1920x1080">1920x1080</option>
                        <option value="1280x720">1280x720</option>
                        <option value="800x600">800x600</option>
                        {/* Add as many resolutions as you need */}
                    </select>
                    <label>
                    <input 
                        type="checkbox" 
                        checked={settings.isFullscreen} 
                        onChange={toggleFullScreen} 
                    />
                  Fullscreen Mode
                </label>
                </div>
            </section>

            {/* Language and Subtitles */}
            <section>
                <h2>Language and Subtitles</h2>
                <div>
                    <label>Language</label>
                    <select value={settings.language} onChange={handleSettingChange('language')}>
                        <option value="en">English</option>
                        <option value="es">Spanish</option>
                        <option value="de">German</option>
                        {/* Add as many languages as you support */}
                    </select>
                </div>
            </section>

            {/* Reset Options */}
            <section>
                <h2>Reset Options</h2>
                <button onClick={resetToDefaults}>Reset to Defaults</button>
            </section>
        </div>
    );
}

export default SettingsPage;
