// App.js

import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import AppRoutes from './routes/Routes';
import { SettingsProvider } from './contexts/SettingsContext'; // adjust the import path as needed

function App() {
  return (
    <SettingsProvider>
      <Router>
        <div>
          <AppRoutes  />
        </div>
      </Router>
    </SettingsProvider>
  );
}

export default App;
