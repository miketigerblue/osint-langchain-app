import axios from 'axios';

const apiClient = axios.create({
    baseURL: 'http://localhost:8000/api',
});

export const fetchThreats = async () => {
    const response = await apiClient.get('/threats');
    return response.data;
};
