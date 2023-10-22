// ImageDisplay.js
import React from 'react';
import './ImageDisplay.css';

const ImageDisplay = ({ images, onEnlarge}) => {
    // This function will trigger when the user clicks on an image. 
    // It will call the onEnlarge prop with the URL of the clicked image.
    const handleEnlarge = (imageUrl) => {
        onEnlarge(imageUrl);
    };

    return (
        <div className="image-display">
            {images.map((image, index) => (
                <div key={index} className="image-container">
                    <img 
                        src={image.url} 
                        alt={image.description} 
                        className="image" 
                        onClick={() => handleEnlarge(image.url)}
                    />
                </div>
            ))}
        </div>
    );
}

export default ImageDisplay;
