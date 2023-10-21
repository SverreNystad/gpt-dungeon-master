import React, { useState } from 'react';

const SettingsPage = () => {
    // You might have state variables to track each setting, which could potentially be fetched from a server or local storage
    const [backgroundVolume, setBackgroundVolume] = useState(0.5); // assuming 0.5 is the default value
    const [gptSpeech, setGptSpeech] = useState(0.5); // assuming 0.5 is the default value
    
    // State variable for resolution setting
    const [resolution, setResolution] = useState('1920x1080'); // default value
    
    // State variable for language setting
    const [language, setLanguage] = useState('en'); // default value is English

    const resetToDefaults = () => {
        setBackgroundVolume(0.5);
        setGptSpeech(0.5);
        setResolution('1920x1080');
        setLanguage('en');
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
                        value={backgroundVolume} 
                        onChange={(e) => setBackgroundVolume(e.target.value)} 
                    />

                    <label>DM Speech Volume</label>
                    <input 
                        type="range" 
                        min="0" max="1" 
                        step="0.01" 
                        value={gptSpeech} 
                        onChange={(e) => setGptSpeech(e.target.value)} 
                    />
                    {/* Other audio controls go here */}
                </div>
            </section>

            {/* Display Settings */}
            <section>
                <h2>Display Settings</h2>
                <div>
                    <label>Screen Resolution</label>
                    <select value={resolution} onChange={(e) => setResolution(e.target.value)}>
                        <option value="1920x1080">1920x1080</option>
                        <option value="1280x720">1280x720</option>
                        <option value="800x600">800x600</option>
                        {/* Add as many resolutions as you need */}
                    </select>
                </div>
            </section>

            {/* Language and Subtitles */}
            <section>
                <h2>Language and Subtitles</h2>
                <div>
                    <label>Language</label>
                    <select value={language} onChange={(e) => setLanguage(e.target.value)}>
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
