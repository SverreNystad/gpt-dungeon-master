// NewCampaignPage.js
import React, { useState } from 'react';
import CharacterSelection from './CharacterSelection';
import CharacterCreation from './CharacterCreation';
const NewCampaignPage = () => {
    // State hooks for all the form fields
    const [campaignName, setCampaignName] = useState('');
    const [theme, setTheme] = useState('');
    const [difficulty, setDifficulty] = useState('');
    const [gameLength, setGameLength] = useState('');
    const [worldSize, setWorldSize] = useState('');
    const [enemyDensity, setEnemyDensity] = useState('');
    const [worldDescription, setWorldDescription] = useState('');
    const [startingPoint, setStartingPoint] = useState('');
    const [initialPlot, setInitialPlot] = useState('');
    const [character, setCharacter] = useState({}); // This could be an object with various character properties

    // ... other state variables as needed

    const handleSubmit = () => {
        // Handle form submission, like posting the data to an API or another handler
        const newCampaignData = {
            campaignName,
            theme,
            difficulty,
            gameLength,
            worldSize,
            enemyDensity,
            worldDescription,
            startingPoint,
            initialPlot,
            character,
            // ... other data as needed
        };
        console.log('Form Submitted', newCampaignData);
        // Here, you'd typically send 'newCampaignData' to your backend or state management system
    };
    const [campaign, setCampaign] = useState({
      name: '',
      theme: '',
      difficulty: '',
      // other campaign settings...
      character: null,  // This will hold the selected or created character
  });

  const [characters, setCharacters] = useState([
      // This would be fetched from your backend or from a local store
      { name: 'Thalion', description: 'Elven Archer', /* other attributes... */ },
      { name: 'Durnik', description: 'Dwarven Warrior', /* other attributes... */ },
      // other pre-made characters...
  ]);

  const handleSelectCharacter = (character) => {
      setCampaign({ ...campaign, character });
      // Redirect to the next step or enable it
  };

  const handleCreateCharacter = (character) => {
      setCharacters([...characters, character]);  // You might want to save this newly created character
      setCampaign({ ...campaign, character });
      // Redirect to the next step or enable it
  };

    return (
        <div>
            <h1>Start New Campaign</h1>
            <form onSubmit={handleSubmit}>
                {/* Campaign Creation */}
                <section>
                    <h2>Create a New Campaign</h2>
                    {/* Campaign Name */}
                    <div>
                        <label>Campaign Name:</label>
                        <input 
                            type="text" 
                            value={campaignName} 
                            onChange={(e) => setCampaignName(e.target.value)} 
                            required 
                        />
                    </div>
                    {/* Theme Selection */}
                    <div>
                        <label>Theme:</label>
                        <select value={theme} onChange={(e) => setTheme(e.target.value)} required>
                            <option value="fantasy">High Fantasy</option>
                            <option value="sci-fi">Sci-Fi</option>
                            <option value="gothic">Gothic Horror</option>
                            {/* ... other themes */}
                        </select>
                    </div>
                    {/* Difficulty Level */}
                    <div>
                        <label>Difficulty Level:</label>
                        <select value={difficulty} onChange={(e) => setDifficulty(e.target.value)} required>
                            <option value="easy">Easy</option>
                            <option value="medium">Medium</option>
                            <option value="hard">Hard</option>
                            <option value="nightmare">Nightmare</option>
                        </select>
                    </div>
                    {/* Other Parameters */}
                    <div>
                        <label>Game Length:</label>
                        <select value={gameLength} onChange={(e) => setGameLength(e.target.value)} required>
                            <option value="short">Short</option>
                            <option value="medium">Medium</option>
                            <option value="long">Long</option>
                        </select>
                    </div>
                    <div>
                        <label>World Size:</label>
                        <select value={worldSize} onChange={(e) => setWorldSize(e.target.value)} required>
                            <option value="small">Small</option>
                            <option value="medium">Medium</option>
                            <option value="large">Large</option>
                        </select>
                    </div>
                    <div>
                        <label>Enemy Density:</label>
                        <select value={enemyDensity} onChange={(e) => setEnemyDensity(e.target.value)} required>
                            <option value="low">Low</option>
                            <option value="medium">Medium</option>
                            <option value="high">High</option>
                        </select>
                    </div>
                </section>

                {/* Character Selection or Creation */}
                <h2>Character</h2>
            {campaign.character ? (
                <p>Character selected: {campaign.character.name}</p>
            ) : (
                <div>
                    <CharacterSelection 
                        characters={characters} 
                        onSelectCharacter={handleSelectCharacter} 
                    />
                    <CharacterCreation onCreateCharacter={handleCreateCharacter} />
                </div>
            )}

                {/* World Setting/Initial Plot Setup */}
                <section>
                    <h2>World Setting</h2>
                    <div>
                        <label>World Description:</label>
                        <textarea 
                            value={worldDescription} 
                            onChange={(e) => setWorldDescription(e.target.value)} 
                            required 
                        />
                    </div>
                    <div>
                        <label>Starting Point:</label>
                        <input 
                            type="text" 
                            value={startingPoint} 
                            onChange={(e) => setStartingPoint(e.target.value)} 
                            required 
                        />
                    </div>
                    <div>
                        <label>Initial Plot Hooks:</label>
                        <input 
                            type="text" 
                            value={initialPlot} 
                            onChange={(e) => setInitialPlot(e.target.value)} 
                            required 
                        />
                    </div>
                </section>

                <button type="submit">Start Campaign</button>
            </form>
        </div>
    );
}

export default NewCampaignPage;
