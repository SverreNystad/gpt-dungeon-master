import React, { useState } from 'react';
import './CampaignOverview.css';

const mockCampaignData = {
        name: "The Quest for the Lost Artifact",
        summary: "The party has ventured through forests and dungeons in search of the lost artifact, which is said to hold immense power. After overcoming various challenges and making new allies, they find themselves on the cusp of the artifact's rumored location. But dark forces are also vying for its power...",
        characters: [
            {
                name: "Eldon the Brave",
                portrait: "https://example.com/character1.jpg",  // URL to the character's portrait image
                level: 5,
                health: 85,
                class: "Warrior",
                // other stats here
            },
            {
                name: "Lyanna of the Shadows",
                portrait: "https://example.com/character2.jpg",  // URL to the character's portrait image
                level: 4,
                health: 65,
                class: "Rogue",
                // other stats here
            },
            // additional characters here
        ],
        quests: [
            {
                title: "Find the ancient map",
                description: "The party needs the ancient map believed to be located in the Mystic Library to continue their quest for the artifact.",
                status: "completed",
            },
            {
                title: "Secure the Silver Key",
                description: "The Silver Key unlocks the chamber where the artifact is said to be hidden. Rumors suggest it's in the possession of a rogue sorcerer.",
                status: "in progress",
            },
            // additional quests here
        ],
        // other campaign data here
    };
    

const CampaignOverview = () => {
    // You would fetch campaignData from your state management or props
    const [campaignData, setCampaignData] = useState(mockCampaignData);
    return (
        <div className="campaign-overview">
            <div className="campaign-header">
                <h1>{campaignData.name}</h1> {/* Campaign Name */}
            </div>
            
            <div className="main-overview-area">
                {/* Campaign Summary */}
                <section className="campaign-summary">
                    <h2>Summary</h2>
                    <p>{campaignData.summary}</p>
                </section>
                
                {/* Character Overview */}
                <section className="character-overview">
                    <h2>Characters</h2>
                    <div className="character-cards">
                        {campaignData.characters.map((character, index) => (
                            <div key={index} className="character-card">
                                <img src={character.portrait} alt={`character-${index}`} />
                                <h3>{character.name}</h3>
                                {/* Display other character info here */}
                            </div>
                        ))}
                    </div>
                </section>
                
                {/* Quest Log */}
                <section className="quest-log">
                    <h2>Quest Log</h2>
                    <ul>
                        {campaignData.quests.map((quest, index) => (
                            <li key={index}>
                                <span className={`status ${quest.status}`}>{quest.status}</span>
                                <span className="title">{quest.title}</span>
                                <p className="description">{quest.description}</p>
                            </li>
                        ))}
                    </ul>
                </section>
                
                {/* World Map */}
                <section className="world-map">
                    <h2>World Map</h2>
                    {/* Your map component would go here */}
                </section>
            </div>
        </div>
    );
}

export default CampaignOverview;
