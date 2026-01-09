import React, { useEffect, useRef } from 'react';
import './Terminal.css';

function Terminal({ commandHistory, currentDirectory, isProcessing, onExampleClick }) {
  const terminalRef = useRef(null);

  useEffect(() => {
    // Auto-scroll to bottom when new content is added
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [commandHistory]);

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString();
  };

  const renderHistoryEntry = (entry, index) => {
    if (entry.type === 'input') {
      return (
        <div key={index} className="terminal-line input-line fade-in">
          <span className="prompt">
            <span className="prompt-symbol">➜</span>
            <span className="prompt-dir">{entry.directory?.split('/').pop() || '~'}</span>
            <span className="prompt-indicator">$</span>
          </span>
          <span className="command-text">
            {entry.isVoice && <span className="voice-badge">🎤</span>}
            {entry.content}
          </span>
          <span className="timestamp">{formatTimestamp(entry.timestamp)}</span>
        </div>
      );
    }

    if (entry.type === 'output') {
      return (
        <div key={index} className="terminal-line output-line fade-in">
          {entry.aiInterpretation && (
            <div className="ai-interpretation">
              <span className="ai-badge">🤖 AI:</span>
              <span className="ai-command">{entry.command}</span>
              <span className="ai-confidence">
                ({(entry.aiInterpretation.confidence * 100).toFixed(0)}% confident)
              </span>
            </div>
          )}
          
          {entry.content && (
            <pre className={entry.success ? 'output-success' : 'output-error'}>
              {entry.content}
            </pre>
          )}
          
          {entry.executor && (
            <div className="executor-badge">
              Executed by: <span className="executor-name">{entry.executor}</span>
            </div>
          )}
        </div>
      );
    }

    if (entry.type === 'error') {
      return (
        <div key={index} className="terminal-line error-line fade-in">
          <span className="error-icon">❌</span>
          <span className="error-text">{entry.content}</span>
        </div>
      );
    }

    return null;
  };

  return (
    <div className="terminal-container" ref={terminalRef}>
      <div className="terminal-content">
        {commandHistory.length === 0 ? (
          <div className="welcome-message">
            <h2>🎉 Welcome to AI-Powered Terminal!</h2>
            <p>Start by typing a command in natural language or use your voice.</p>
            <div className="examples">
              <h3>Try these examples:</h3>
              <ul>
                <li onClick={() => onExampleClick && onExampleClick("show me all python files")}>
                  "show me all python files"
                </li>
                <li onClick={() => onExampleClick && onExampleClick("open config.json in vscode")}>
                  "open config.json in vscode"
                </li>
                <li onClick={() => onExampleClick && onExampleClick("go to downloads folder")}>
                  "go to downloads folder"
                </li>
                <li onClick={() => onExampleClick && onExampleClick("list all files with details")}>
                  "list all files with details"
                </li>
                <li onClick={() => onExampleClick && onExampleClick("find adi.c and open it")}>
                  "find adi.c and open it"
                </li>
              </ul>
            </div>
          </div>
        ) : (
          commandHistory.map((entry, index) => renderHistoryEntry(entry, index))
        )}
        
        {isProcessing && (
          <div className="processing-line pulse">
            <div className="spinner"></div>
            <span>Processing your request...</span>
          </div>
        )}
      </div>
    </div>
  );
}

export default Terminal;

