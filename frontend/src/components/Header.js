import React from 'react';
import './Header.css';

function Header({ isConnected, systemStatus }) {
  return (
    <header className="header glass">
      <div className="header-left">
        <div className="logo">
          <span className="logo-icon">🤖</span>
          <h1 className="logo-text">AI Terminal</h1>
        </div>
        <div className="subtitle">Voice-Powered Command Shell</div>
      </div>
      
      <div className="header-right">
        <div className="status-badges">
          <div className={`status-badge ${systemStatus.gemini_available ? 'active' : 'inactive'}`}>
            <span className="badge-icon">🧠</span>
            <span className="badge-text">Gemini AI</span>
          </div>
          
          <div className={`status-badge ${systemStatus.mini_bash_available ? 'active' : 'inactive'}`}>
            <span className="badge-icon">💻</span>
            <span className="badge-text">Mini Bash</span>
          </div>
          
          <div className={`status-badge ${isConnected ? 'active' : 'inactive'}`}>
            <span className={`status-indicator ${isConnected ? 'status-connected' : 'status-disconnected'}`}></span>
            <span className="badge-text">{isConnected ? 'Connected' : 'Disconnected'}</span>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;

