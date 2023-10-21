import React from 'react';
import { Link } from 'react-router-dom';
import './MainMenu.css';

function MainMenu() {
  return (
    <div className="main-menu">
      <Link to="/new-campaign"><button>Start New Campaign</button></Link>
      <Link to="/existing-campaign"><button>Continue Existing Campaign</button></Link>
      <Link to="/rules-lookup"><button>Rules Lookup</button></Link>
      <Link to="/settings"><button>Settings</button></Link>
      <Link to="/quit"><button>Quit</button></Link>
    </div>
  );
}

export default MainMenu;
