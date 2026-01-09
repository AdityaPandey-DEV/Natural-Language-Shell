import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5002';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const executeCommand = async (command, isVoice = false, preferredExecutor = 'mini-bash') => {
  try {
    const response = await api.post('/api/execute', {
      command,
      is_voice: isVoice,
      preferred_executor: preferredExecutor,
    });
    return response.data;
  } catch (error) {
    console.error('Error executing command:', error);
    throw new Error(error.response?.data?.error || 'Failed to execute command');
  }
};

export const getCurrentDirectory = async () => {
  try {
    const response = await api.get('/api/directory');
    return response.data;
  } catch (error) {
    console.error('Error getting directory:', error);
    throw error;
  }
};

export const getCommandHistory = async (limit = 50) => {
  try {
    const response = await api.get('/api/history', {
      params: { limit },
    });
    return response.data;
  } catch (error) {
    console.error('Error getting history:', error);
    throw error;
  }
};

export const getFeedbackLog = async () => {
  try {
    const response = await api.get('/api/feedback');
    return response.data;
  } catch (error) {
    console.error('Error getting feedback:', error);
    throw error;
  }
};

export const searchFiles = async (filename, startDir) => {
  try {
    const response = await api.post('/api/search', {
      filename,
      start_dir: startDir,
    });
    return response.data;
  } catch (error) {
    console.error('Error searching files:', error);
    throw error;
  }
};

export const checkHealth = async () => {
  try {
    const response = await api.get('/api/health');
    return response.data;
  } catch (error) {
    console.error('Error checking health:', error);
    throw error;
  }
};

export default api;

