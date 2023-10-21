// App.js

import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import AppRoutes from './routes/Routes';
import MainMenu from './components/mainmenu/MainMenu';
// ... other imports

function App() {
  return (
    <Router>
      <div>
        <AppRoutes  />
      </div>
    </Router>
  );
}

export default App;
