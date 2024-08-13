import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000';

//api for non-authenticated routes
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
  },
});

//api for authenticated routes
export const createAuthApi = (accessToken: string | undefined) => {
  if (!accessToken) {
    throw new Error('Access token is not set');
  }
  
  const authApi = axios.create({
    baseURL: API_BASE_URL,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Authorization': 'Bearer ' + accessToken,
    },
  });

  return authApi;
};


export default api;