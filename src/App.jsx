import React from 'react';
import Header from './components/Header';
import NavBar from './components/NavBar';
import MainContent from './components/MainContent';
import ChatIcon from './components/ChatICon';
import './App.css';

function App() {
  return (
    <div className="App">
      <Header />
      <NavBar />
      <MainContent />
      <ChatIcon />
    </div>
  );
}

export default App;
