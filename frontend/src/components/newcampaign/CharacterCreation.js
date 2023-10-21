// CharacterCreation.js
import React, { useState } from 'react';

const CharacterCreation = ({ onCreateCharacter }) => {
    const [character, setCharacter] = useState({
        name: '',
        race: '', 
        class: '',
        // other attributes...
    });

    const handleInputChange = (event) => {
        const { name, value } = event.target;
        setCharacter({ ...character, [name]: value });
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        onCreateCharacter(character);
    };

    return (
        <div>
            <h2>Create a Character</h2>
            <form onSubmit={handleSubmit}>
                {/* Input for character's name */}
                <div>
                    <label>Name:</label>
                    <input
                        type="text"
                        name="name"
                        value={character.name}
                        onChange={handleInputChange}
                        required
                    />
                </div>
                
                {/* Dropdown for character's race */}
                <div>
                    <label>Race:</label>
                    <select
                        name="race"
                        value={character.race}
                        onChange={handleInputChange}
                        required
                    >
                        <option value="human">Human</option>
                        <option value="elf">Elf</option>
                        {/* other races */}
                    </select>
                </div>

                {/* Dropdown for character's class */}
                <div>
                    <label>Class:</label>
                    <select
                        name="class"
                        value={character.class}
                        onChange={handleInputChange}
                        required
                    >
                        <option value="warrior">Warrior</option>
                        <option value="mage">Mage</option>
                        {/* other classes */}
                    </select>
                </div>

                {/* Other inputs for additional attributes */}

                <button type="submit">Create Character</button>
            </form>
        </div>
    );
}

export default CharacterCreation;
