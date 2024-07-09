import axios from 'axios';

const API_BASE_URL = 'http://your-api-base-url';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
  },
});

export default api;