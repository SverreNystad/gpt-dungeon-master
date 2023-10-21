// SomeNotFoundComponent.js
import React from 'react';
import { Link } from 'react-router-dom';

const SomeNotFoundComponent = () => {
  const containerStyle = {
    padding: '20px',
    textAlign: 'center',
    backgroundColor: '#282c34', // dark background
    color: 'white', // light text
    minHeight: '100vh', // full screen height
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: 'calc(10px + 2vmin)',
    lineHeight: '1.6',
  };

  const linkStyle = {
    color: '#61dafb', // light blue, similar to React's color
    textDecoration: 'underline',
  };
  const imageUrl = process.env.PUBLIC_URL + '/assets/404_GPT_DUNGEON_MASTER.png';
  return (
    <div style={containerStyle}>
      <h1>404 - Not Found</h1>
      <img src={imageUrl} alt="assets/404_GPT_DUNGEON_MASTER.png" />
      <p>
        Brave adventurer, you've bravely ventured into the unknown, and alas, found yourself in the barren wastelands of... Error 404! The ancient scrolls did not foretell of this! The page you seek has either been claimed by dragons, spirited away by mischievous fairies, or never existed in this realm to begin with.
      </p>
      <p>
        Fear not! For it's not the end of your journey. Grab your map, recalibrate your compass, or perhaps consult a wise wizard. There are plenty of other treacherous dungeons to explore and mystical treasures to uncover!
      </p>
      <p>Choose your path:</p>
      <p>
        <Link to="/" style={linkStyle}>Return to the safety of the Home Village</Link>
      </p>
      <p>
        If you believe this to be the work of dark sorcery, <span style={linkStyle}>send a raven to our support mages</span> (Contact Support).
      </p>
      <p>Remember, it's not about the destination, but the epic (and occasionally error-ridden) journey!"</p>
    </div>
  );
};

export default SomeNotFoundComponent;
