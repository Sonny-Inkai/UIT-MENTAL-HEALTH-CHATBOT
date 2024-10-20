// ChatIcon.jsx
import React, { useState } from 'react';
import '../CSS/ChatIcon.css';

const ChatIcon = () => {
  const [showPopup, setShowPopup] = useState(false);
  const [isFullScreen, setIsFullScreen] = useState(false);

  const handleClick = () => {
    setShowPopup(!showPopup);
  };

  const handleFullScreenToggle = () => {
    setIsFullScreen(!isFullScreen);
  };

  return (
    <div className="chat-container">
      <div className="chat-icon" onClick={handleClick}>
        <span className="chat-icon-text">💬</span>
      </div>
      {showPopup && (
        <div className={`chat-popup ${isFullScreen ? 'full' : ''}`}>
          <div className="chat-popup-header">
            <span className="chat-title">UIT ChatBot</span>
            <div className="chat-controls">
              <button className="control-btn full-screen-btn" onClick={handleFullScreenToggle}>⛶</button>
            </div>
          </div>
          <div className="chat-popup-body">
            <div className="chat-message">
              <span className="chat-icon">👥</span>
              <span className="chat-text">Xin chào, UIT ChatBot đang nghe</span>
            </div>
          </div>
          <div className="chat-popup-footer">
            <input type="text" placeholder="Nhập tin nhắn" className="chat-input" />
            <button className="send-btn">👤</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatIcon;
