// src/components/ChatIcon.jsx
import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import '../CSS/ChatIcon.css';
import { CircularProgress, IconButton } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import CloseIcon from '@mui/icons-material/Close';
import FullscreenIcon from '@mui/icons-material/Fullscreen';
import ZoomInIcon from '@mui/icons-material/ZoomIn';

const ChatIcon = () => {
  const [showPopup, setShowPopup] = useState(false);
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Xin chào, UIT Healing đang nghe bạn!' }
  ]);
  const [userInput, setUserInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [popupSize, setPopupSize] = useState('small'); // small, large, fullscreen
  const inputRef = useRef(null);
  const chatBodyRef = useRef(null);
  const responseRef = useRef(null);

  const handleClick = () => {
    setShowPopup(!showPopup);
    if (!showPopup) {
      setTimeout(() => inputRef.current?.focus(), 100); // Focus vào input khi mở popup
    }
  };

  const handleInputChange = (event) => {
    setUserInput(event.target.value);
  };

  const handleSendMessage = async () => {
    if (userInput.trim() !== '') {
      setMessages([...messages, { sender: 'user', text: userInput }]);
      setUserInput(''); // Xóa input sau khi gửi
      setLoading(true); // Bắt đầu quá trình chờ phản hồi

      try {
        const response = await axios.post('http://localhost:5000/generate-response', {
          query: userInput,
        });
        setMessages(prevMessages => [...prevMessages, { sender: 'bot', text: formatBotResponse(response.data.response) }]);
      } catch (error) {
        console.error('Error generating response:', error);
        setMessages(prevMessages => [...prevMessages, { sender: 'bot', text: 'Xin lỗi, hiện tại mình không thể trả lời. Vui lòng thử lại sau.' }]);
      } finally {
        setLoading(false); // Quá trình tải hoàn tất
      }
    }
  };

  const formatBotResponse = (text) => {
    // Sử dụng regex để làm cho nội dung trả lời từ chatbot đẹp hơn
    return text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Đậm chữ cho các đoạn bôi đậm
      .replace(/(\d+\.\s.*?):/g, '<strong>$1</strong>:') // Đậm các bước và tiêu đề
      .replace(/\n/g, '<br>'); // Thêm ngắt dòng phù hợp
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleSendMessage();
    }
  };

  const handleZoomIn = () => {
    setPopupSize(popupSize === 'small' ? 'large' : popupSize === 'large' ? 'small' : 'large');
  };

  const handleFullScreen = () => {
    setPopupSize(popupSize === 'fullscreen' ? 'small' : 'fullscreen');
  };

  useEffect(() => {
    if (chatBodyRef.current) {
      chatBodyRef.current.scrollTop = chatBodyRef.current.scrollHeight;
      if (loading) {
        responseRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }
  }, [messages, loading]);

  return (
    <div className="chat-container">
      <div className="chat-icon" onClick={handleClick}>
        <IconButton color="primary">
          {showPopup ? (
            <CloseIcon />
          ) : (
            <img
              src="/uit-mental-health.png"
              alt="Chat Icon"
              className="chat-icon-img"
            />
          )}
        </IconButton>
      </div>
      {showPopup && (
        <div className={`chat-popup ${popupSize}`}>
          <div className="chat-popup-header">
            <img
              src="/uit-mental-health.png"
              alt="Chat Icon"
              className="chat-header-icon"
            />
            <span className="chat-title">UIT Healing</span>
            <div className="chat-controls">
              <IconButton onClick={handleZoomIn}>
                <ZoomInIcon />
              </IconButton>
              <IconButton onClick={handleFullScreen}>
                <FullscreenIcon />
              </IconButton>
              <IconButton onClick={handleClick}>
                <CloseIcon />
              </IconButton>
            </div>
          </div>
          <div className="chat-popup-body" ref={chatBodyRef}>
            {messages.map((message, index) => (
              <div key={index} className={`chat-message ${message.sender}`} ref={message.sender === 'bot' ? responseRef : null}>
                <div className={`chat-bubble ${message.sender}`} dangerouslySetInnerHTML={{ __html: message.text }}></div>
              </div>
            ))}
            {loading && (
              <div className="chat-message bot">
                <div className="chat-bubble bot">
                  <CircularProgress size={20} />
                </div>
              </div>
            )}
          </div>
          <div className="chat-popup-footer">
            <input
              type="text"
              placeholder="Nhập tin nhắn"
              className="chat-input"
              value={userInput}
              onChange={handleInputChange}
              onKeyPress={handleKeyPress}
              ref={inputRef}
            />
            <IconButton color="primary" onClick={handleSendMessage}>
              <SendIcon />
            </IconButton>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatIcon;