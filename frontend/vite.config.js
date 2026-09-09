import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    open: false,
    proxy: {
      '/chat': 'http://127.0.0.1:8000',
      '/menu': 'http://127.0.0.1:8000',
      '/bookings': 'http://127.0.0.1:8000',
      '/orders': 'http://127.0.0.1:8000',
      '/auth': 'http://127.0.0.1:8000',
    }
  }
});
