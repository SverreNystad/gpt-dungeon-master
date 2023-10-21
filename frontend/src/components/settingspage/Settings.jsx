import React, { useContext  } from 'react';
import { SettingsContext } from '../../contexts/SettingsContext'; // adjust the import path as needed

const SettingsPage = () => {
    const { settings, updateSetting, resetToDefaults } = useContext(SettingsContext);

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

                    <label>DM Speech Volume</label>
                    <input 
                        type="range" 
                        min="0" max="1" 
                        step="0.01" 
                        value={settings.gptSpeech} 
                        onChange={handleSettingChange("gptSpeech")} 
                    />
                    {/* Other audio controls go here */}
                </div>
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
                        onChange={settings.toggleFullscreen} 
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
