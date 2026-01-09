import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import Terminal from './components/Terminal';
import InputBar from './components/InputBar';
import Header from './components/Header';
import StatusBar from './components/StatusBar';
import { connectWebSocket, sendCommand, onCommandResult, onConnected } from './services/websocket';
import { executeCommand } from './services/api';

function App() {
  const [currentDirectory, setCurrentDirectory] = useState('~');
  const [commandHistory, setCommandHistory] = useState([]);
  const [isConnected, setIsConnected] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [focusInput, setFocusInput] = useState(false);
  const [systemStatus, setSystemStatus] = useState({
    gemini_available: false,
    mini_bash_available: false
  });

  useEffect(() => {
    // Connect to WebSocket
    connectWebSocket();
    
    // Set up event listeners
    onConnected((data) => {
      setIsConnected(true);
      setCurrentDirectory(data.current_directory || '~');
      console.log('✅ Connected to backend');
    });

    onCommandResult((data) => {
      setIsProcessing(false);
      addToHistory(data);
    });

    // Fetch initial status
    fetchSystemStatus();

    return () => {
      // Cleanup
    };
  }, []);

  const fetchSystemStatus = async () => {
    try {
      const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5002';
      const response = await fetch(`${API_URL}/api/health`);
      const data = await response.json();
      setSystemStatus({
        gemini_available: data.gemini_available,
        mini_bash_available: data.mini_bash_available
      });
      setCurrentDirectory(data.current_directory || '~');
    } catch (error) {
      console.error('Failed to fetch system status:', error);
    }
  };

  const addToHistory = (entry) => {
    setCommandHistory(prev => [...prev, {
      timestamp: new Date().toISOString(),
      ...entry
    }]);
  };

  const handleCommandSubmit = async (command, isVoice = false, preferredExecutor = 'mini-bash') => {
    if (!command.trim()) return;

    setIsProcessing(true);
    setInputValue(''); // Clear input after submit
    
    // Add user input to history immediately
    addToHistory({
      type: 'input',
      content: command,
      isVoice: isVoice,
      directory: currentDirectory,
      preferredExecutor: preferredExecutor
    });

    try {
      const result = await executeCommand(command, isVoice, preferredExecutor);
      
      // Update current directory if changed
      if (result.current_directory) {
        setCurrentDirectory(result.current_directory);
      }

      // Add result to history
      addToHistory({
        type: 'output',
        content: result.output || result.error,
        success: result.success,
        command: result.command,
        aiInterpretation: result.ai_interpretation,
        executor: result.executor,
        directory: result.current_directory
      });

    } catch (error) {
      addToHistory({
        type: 'error',
        content: error.message || 'Failed to execute command',
        success: false
      });
    } finally {
      setIsProcessing(false);
    }
  };

  const handleExampleClick = (exampleText) => {
    setInputValue(exampleText);
    setFocusInput(true);
    setTimeout(() => setFocusInput(false), 100);
  };

  return (
    <div className="App">
      <Header 
        isConnected={isConnected}
        systemStatus={systemStatus}
      />
      
      <StatusBar 
        currentDirectory={currentDirectory}
        isProcessing={isProcessing}
      />
      
      <Terminal 
        commandHistory={commandHistory}
        currentDirectory={currentDirectory}
        isProcessing={isProcessing}
        onExampleClick={handleExampleClick}
      />
      
      <InputBar 
        onCommandSubmit={handleCommandSubmit}
        isProcessing={isProcessing}
        currentDirectory={currentDirectory}
        inputValue={inputValue}
        setInputValue={setInputValue}
        focusInput={focusInput}
      />
    </div>
  );
}

export default App;

