import axios from 'axios';

const API_BASE = ''; // Uses relative URLs with Vite proxy

const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

export const api = {
  // Chatbot Endpoints
  sendMessage: async (sessionId, message, userId = null, userName = null) => {
    const response = await apiClient.post('/chat/message', {
      session_id: sessionId,
      message: message,
      user_id: userId,
      user_name: userName,
    });
    return response.data;
  },

  getChatSuggestions: async () => {
    const response = await apiClient.get('/chat/suggestions');
    return response.data;
  },

  resetChatSession: async (sessionId) => {
    const response = await apiClient.post(`/chat/reset/${sessionId}`);
    return response.data;
  },

  // Menu Endpoints
  getMenuCategories: async () => {
    const response = await apiClient.get('/menu/categories');
    return response.data;
  },

  getMenuItems: async (params = {}) => {
    const response = await apiClient.get('/menu/items', { params });
    return response.data;
  },

  getMenuItem: async (id) => {
    const response = await apiClient.get(`/menu/items/${id}`);
    return response.data;
  },

  // Booking Endpoints
  getTables: async () => {
    const response = await apiClient.get('/bookings/tables');
    return response.data;
  },

  createBooking: async (bookingData) => {
    const response = await apiClient.post('/bookings', bookingData);
    return response.data;
  },

  getBooking: async (id) => {
    const response = await apiClient.get(`/bookings/${id}`);
    return response.data;
  },

  // Order Endpoints
  createOrder: async (orderData) => {
    const response = await apiClient.post('/orders', orderData);
    return response.data;
  },

  getOrder: async (id) => {
    const response = await apiClient.get(`/orders/${id}`);
    return response.data;
  },
};

export default api;
