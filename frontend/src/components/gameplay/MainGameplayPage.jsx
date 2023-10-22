import React, { useState, useEffect, useRef } from 'react';
import './MainGameplayPage.css'; 
import NavigationBar from './NavigationBar';
import ChatInterface from './ChatInterface';
import ImageDisplay from './ImageDisplay';

const MainGameplayPage = () => {
    // State variables
    const [images, setImages] = useState([]);
    const [enlargedImageUrl, setEnlargedImageUrl] = useState(null);

    // Function to close the modal
    const handleCloseModal = () => {
        setEnlargedImageUrl(null);
    };

    return (
        <div className="main-gameplay">
            <NavigationBar />

            <div className="gameplay-body">
                {/* <CharacterInformation /> */}

                <div className="central-section">
                    <ChatInterface 
                        // props as needed
                    />
                    <ImageDisplay 
                        // props as needed
                        images={images}
                        onEnlarge={(imageUrl) => setEnlargedImageUrl(imageUrl)}
                    />
                </div>
            </div>
            {enlargedImageUrl && (
                <div className="modal" onClick={handleCloseModal}>
                    <span className="close" onClick={handleCloseModal}>&times;</span>
                    <img className="enlarged-image" src={enlargedImageUrl} alt="" />
                </div>
            )}
        </div>
    );
}

export default MainGameplayPage;
