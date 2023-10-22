// NavigationBar.js
import React from 'react';
import './NavigationBar.css';
import { Link } from 'react-router-dom';
import routes from '../../routes/routeDefinitions.jsx';

const NavigationBar = ({ onCharacterStatsClick }) => {
    return (
        <div className="navigation-bar">
            <nav>
                <ul>
                    <li><Link to={routes.mainMenu}>Home</Link></li>
                    <li><Link to="/campaign-overview">Campaign Overview</Link></li>
                    <li><button onClick={onCharacterStatsClick}>Character Stats</button></li>
                    <li><Link to={routes.settings}>Settings</Link></li>
                    {/* Additional sections can be added here */}
                </ul>
            </nav>
        </div>
    );
}

export default NavigationBar;
