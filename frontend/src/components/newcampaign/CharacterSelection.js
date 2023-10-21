// CharacterSelection.js
import React from 'react';

const CharacterSelection = ({ characters, onSelectCharacter }) => {
    return (
        <div>
            <h2>Select a Character</h2>
            <div>
                {characters.map((character, index) => (
                    <div key={index} onClick={() => onSelectCharacter(character)}>
                        <h3>{character.name}</h3>
                        <p>{character.description}</p>
                        {/* Other character details */}
                    </div>
                ))}
            </div>
        </div>
    );
}

export default CharacterSelection;
