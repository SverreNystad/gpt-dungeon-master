import React, { useState, useEffect, useRef } from 'react';
import './MainGameplayPage.css'; // assuming you have corresponding CSS file

const MainGameplayPage = () => {
    const [inputMessage, setInputMessage] = useState('');
    const [conversation, setConversation] = useState([]);
    const endOfMessagesRef = useRef(null);

    const scrollToBottom = () => {
        endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(scrollToBottom, [conversation]); // scroll to bottom when conversation updates

    const handleInputChange = (event) => {
        setInputMessage(event.target.value);
    };

    const handleSubmit = () => {
        if (!inputMessage.trim()) return; // prevent empty messages

        // Here, you would typically send the message to your backend or GPT API
        // and then receive a response to add to the conversation.
        // For demonstration, we'll just add the message directly to our conversation log:
        const newMessage = { text: inputMessage, sender: 'player' };
        setConversation([...conversation, newMessage]);

        // Simulate a DM response
        setTimeout(() => {
            const dmResponse = { text: `You said: "${inputMessage}"`, sender: 'dm' };
            setConversation(prev => [...prev, dmResponse]);
        }, 1000);

        setInputMessage(''); // clear the input after sending
    };

    const handleKeyPress = (event) => {
        if (event.key === 'Enter') {
            handleSubmit();
        }
    };

    return (
        <div className="main-gameplay">
            <div className="conversation-area">
                {conversation.map((message, index) => (
                    <div key={index} className={`message ${message.sender}`}>
                        <span>{message.text}</span>
                    </div>
                ))}
                <div ref={endOfMessagesRef} />
            </div>

            <div className="input-area">
                <input
                    type="text"
                    value={inputMessage}
                    onChange={handleInputChange}
                    onKeyPress={handleKeyPress}
                    placeholder="Type your message..."
                />
                <button onClick={handleSubmit}>Send</button>
            </div>
        </div>
    );
}

export default MainGameplayPage;
