import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || '/v1',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add token
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

// Response interceptor to handle 401s
api.interceptors.response.use((response) => {
    return response;
}, (error) => {
    if (error.response && error.response.status === 401) {
        // Optional: trigger logout if token expires
        // localStorage.removeItem('token');
        // window.location.href = '/login';
    }
    return Promise.reject(error);
});

export default api;
