import React, { useContext } from 'react'; // <-- useContext is imported here
import { Link } from 'react-router-dom';
import './MainMenu.css';
import routes from '../../routes/routeDefinitions.jsx';

// import React, { useContext  } from 'react';
import { SettingsContext } from '../../contexts/SettingsContext'; // adjust the import path as needed

function MainMenu() {
  const { settings } = useContext(SettingsContext); // <-- Using useContext here to consume the context

  console.log("MainMenu");
  console.log(settings);
  return (
    <div className="main-menu">
      <Link to={routes.newCampaign}><button>Start New Campaign</button></Link>
      <Link to={routes.existingCampaign}><button>Continue Existing Campaign</button></Link>
      <Link to={routes.rulesLookup}><button>Rules Lookup</button></Link>
      <Link to={routes.settings}><button>Settings</button></Link>
      <Link to={routes.quit}><button>Quit</button></Link>
    </div>
  );
}

export default MainMenu;
