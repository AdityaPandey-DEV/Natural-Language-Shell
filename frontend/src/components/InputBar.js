import React, { useState, useRef, useEffect } from 'react';
import './InputBar.css';

function InputBar({ onCommandSubmit, isProcessing, currentDirectory, inputValue, setInputValue, focusInput }) {
  const [isRecording, setIsRecording] = useState(false);
  const [recognition, setRecognition] = useState(null);
  const [executor, setExecutor] = useState('mini-bash'); // 'mini-bash' or 'system-terminal'
  const inputRef = useRef(null);

  // Focus input when focusInput prop changes
  useEffect(() => {
    if (focusInput && inputRef.current) {
      inputRef.current.focus();
    }
  }, [focusInput]);

  useEffect(() => {
    // Initialize speech recognition
    if ('webkitSpeechRecognition' in window) {
      const recognitionInstance = new window.webkitSpeechRecognition();
      recognitionInstance.continuous = false;
      recognitionInstance.interimResults = false;
      recognitionInstance.lang = 'en-US';

      recognitionInstance.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInputValue(transcript);
        setIsRecording(false);
        // Auto-submit after voice input
        setTimeout(() => {
          handleSubmit(transcript, true);
        }, 500);
      };

      recognitionInstance.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setIsRecording(false);
      };

      recognitionInstance.onend = () => {
        setIsRecording(false);
      };

      setRecognition(recognitionInstance);
    }
  }, []);

  const handleSubmit = (commandText = null, isVoice = false) => {
    const command = commandText || inputValue;
    if (command.trim() && !isProcessing) {
      onCommandSubmit(command, isVoice, executor);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleVoiceClick = () => {
    if (!recognition) {
      alert('Speech recognition is not supported in your browser. Please use Chrome or Edge.');
      return;
    }

    if (isRecording) {
      recognition.stop();
      setIsRecording(false);
    } else {
      setIsRecording(true);
      recognition.start();
    }
  };

  const handleClear = () => {
    setInputValue('');
    inputRef.current?.focus();
  };

  return (
    <div className="input-bar glass">
      <div className="input-container">
        <div className="input-prefix">
          <span className="prefix-symbol">$</span>
          <span className="prefix-dir">{currentDirectory.split('/').pop() || '~'}</span>
        </div>
        
        <input
          ref={inputRef}
          type="text"
          className="command-input"
          placeholder="Type a command in natural language... (e.g., 'show all python files')"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={isProcessing || isRecording}
        />
        
        {inputValue && (
          <button
            className="btn-clear"
            onClick={handleClear}
            title="Clear input"
          >
            ✕
          </button>
        )}
      </div>
      
      <div className="input-actions">
        <select
          className="executor-dropdown"
          value={executor}
          onChange={(e) => setExecutor(e.target.value)}
          disabled={isProcessing}
          title="Choose executor"
        >
          <option value="mini-bash">💻 Mini-Bash</option>
          <option value="system-terminal">🖥️ Mac Terminal</option>
        </select>

        <button
          className={`btn-voice ${isRecording ? 'recording' : ''}`}
          onClick={handleVoiceClick}
          disabled={isProcessing}
          title={isRecording ? 'Stop recording' : 'Start voice input'}
        >
          {isRecording ? (
            <>
              <span className="recording-indicator pulse"></span>
              <span className="btn-icon">⏹️</span>
            </>
          ) : (
            <span className="btn-icon">🎤</span>
          )}
        </button>
        
        <button
          className="btn-submit"
          onClick={() => handleSubmit()}
          disabled={!inputValue.trim() || isProcessing || isRecording}
          title="Execute command"
        >
          <span className="btn-icon">▶️</span>
          <span className="btn-text">Execute</span>
        </button>
      </div>
    </div>
  );
}

export default InputBar;

