import io from 'socket.io-client';

const WS_URL = process.env.REACT_APP_WS_URL || 'http://localhost:5002';

let socket = null;
let isConnected = false;

export const connectWebSocket = () => {
  if (socket && isConnected) {
    return socket;
  }

  socket = io(WS_URL, {
    transports: ['websocket', 'polling'],
    reconnection: true,
    reconnectionDelay: 1000,
    reconnectionAttempts: 5,
  });

  socket.on('connect', () => {
    isConnected = true;
    console.log('✅ WebSocket connected');
  });

  socket.on('disconnect', () => {
    isConnected = false;
    console.log('❌ WebSocket disconnected');
  });

  socket.on('error', (error) => {
    console.error('WebSocket error:', error);
  });

  return socket;
};

export const disconnectWebSocket = () => {
  if (socket) {
    socket.disconnect();
    socket = null;
    isConnected = false;
  }
};

export const sendCommand = (command, isVoice = false) => {
  if (socket && isConnected) {
    socket.emit('execute_command', {
      command,
      is_voice: isVoice,
    });
  } else {
    console.error('WebSocket not connected');
  }
};

export const onConnected = (callback) => {
  if (socket) {
    socket.on('connected', callback);
  }
};

export const onCommandResult = (callback) => {
  if (socket) {
    socket.on('command_result', callback);
  }
};

export const onCommandExecuted = (callback) => {
  if (socket) {
    socket.on('command_executed', callback);
  }
};

export const getConnectionStatus = () => {
  return isConnected;
};

export default {
  connectWebSocket,
  disconnectWebSocket,
  sendCommand,
  onConnected,
  onCommandResult,
  onCommandExecuted,
  getConnectionStatus,
};

