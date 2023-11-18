import React, { useEffect, useState } from "react";
import './StartScreen.css';

function StartScreen() {
  const imageUrl = process.env.PUBLIC_URL + '/assets/loading-screen.png';
  const imageUrlZoomedIn = process.env.PUBLIC_URL + '/assets/gpt-dungeon-master-logo.png';
  
  const [zoom, setZoom] = useState(false);
  const [image, setImage] = useState(imageUrl);
  const [switchImage, setSwitchImage] = useState(false);

  useEffect(() => {
    if (switchImage) {
      
      // If the image is the logo then don't switch it back to the loading screen
      if (image === imageUrlZoomedIn) {
        return;
      }
      // Set a delay for the zoom effect to be reversed before changing the image
      const timeout = setTimeout(() => {
        setImage(imageUrlZoomedIn);
        // Remove the zoom effect before changing the image
        setZoom(false);
        setSwitchImage(false); // reset to initial state
      }, 1000); // 2000ms = 2s for the zoom effect

      return () => clearTimeout(timeout);
    }
  }, [switchImage]);

  const handleKeyPress = () => {
    if (!zoom && !switchImage) {
      setZoom(true);
      // Set a delay for the zoom effect to be noticeable, then trigger the image switch
      // setTimeout(() => setSwitchImage(true), 1000); // 2000ms = 2s for the zoom effect
    }
  }

  return (
    <div 
      className={`image-container ${zoom ? 'zoom' : ''}`} 
      style={{backgroundImage: `url(${image})`}}
      tabIndex={0} // necessary to detect key presses
      onKeyDown={handleKeyPress}
    >
      {/* Content goes here */}
    </div>
  );
}

export default StartScreen;
