import React from 'react';
import './StatusBar.css';

function StatusBar({ currentDirectory, isProcessing }) {
  const getShortPath = (path) => {
    const home = process.env.HOME || '~';
    return path.replace(home, '~');
  };

  return (
    <div className="status-bar glass">
      <div className="status-left">
        <span className="directory-icon">📁</span>
        <span className="directory-path">{getShortPath(currentDirectory)}</span>
      </div>
      
      <div className="status-right">
        {isProcessing && (
          <div className="processing-indicator">
            <div className="spinner"></div>
            <span>Processing...</span>
          </div>
        )}
      </div>
    </div>
  );
}

export default StatusBar;

