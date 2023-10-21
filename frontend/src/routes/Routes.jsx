// routes/Routes.js

import React from 'react';
import { Route, Routes } from 'react-router-dom';
import routes from './routeDefinitions';

// Import your page components
import MainMenu from '../components/mainmenu/MainMenu';
import NewCampaignPage from '../components/newcampaign/NewCampaign';
import ExistingCampaign from '../components/existingcampaign/ExistingCampaign';
import RulesLookup from '../components/ruleslookup/RulesLookup';
import SettingsPage from '../components/settingspage/Settings';
import Quit from '../components/quit/Quit';
import SomeNotFoundComponent from '../components/somenotfoundcomponent/SomeNotFoundComponent';
// ... other imports
import MainGameplayPage from '../components/gameplay/MainGameplayPage';

const AppRoutes  = () => {
  return (
    <Routes >
      <Route path={routes.gameplay} element={<MainGameplayPage/>} />
      <Route path="/" element={<MainMenu/>} />
      <Route path={routes.mainMenu} element={<MainMenu/>} />
      <Route path={routes.newCampaign} element={<NewCampaignPage/>} />
      <Route path={routes.existingCampaign} element={<ExistingCampaign/>} />
      <Route path={routes.settings} element={<SettingsPage/>}/>
      <Route path={routes.rulesLookup} element={<RulesLookup/>} />
      <Route path={routes.quit} element={<Quit/>} />
      <Route path="*" element={<SomeNotFoundComponent />} />
    </Routes >
  );
};

export default AppRoutes ;
