import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const projectAPI = {
  createProject: async (description, name, autonomous_mode = true) => {
    const response = await api.post('/api/projects/create', { 
      description, 
      name, 
      autonomous_mode 
    });
    return response.data;
  },

  listProjects: async () => {
    const response = await api.get('/api/projects');
    return response.data;
  },

  getProject: async (projectId) => {
    const response = await api.get(`/api/projects/${projectId}`);
    return response.data;
  },

  getFileContent: async (projectId, filePath) => {
    const response = await api.get(`/api/projects/${projectId}/file-content`, {
      params: { file_path: filePath }
    });
    return response.data;
  },

  downloadProject: async (projectId) => {
    const response = await api.get(`/api/projects/${projectId}/download`, {
      responseType: 'blob',
    });
    return response.data;
  },
  
  deleteProject: async (projectId) => {
    const response = await api.delete(`/api/projects/${projectId}`);
    return response.data;
  },

  enhancePrompt: async (promptText) => {
    const response = await api.post('/api/enhance-prompt', { prompt: promptText });
    return response.data;
  },
};

export const employeeAPI = {
  listEmployees: async () => {
    const response = await api.get('/api/employees');
    return response.data;
  },
};

export const createWebSocket = () => {
  return new WebSocket(`ws://localhost:8000/ws`);
};

export default api;