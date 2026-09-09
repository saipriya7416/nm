import { createServer } from 'vite';

process.on('uncaughtException', (err) => console.error('Uncaught:', err));
process.on('unhandledRejection', (err) => console.error('Unhandled:', err));
process.on('exit', (code) => console.log('Process exiting with code:', code));

async function start() {
  const server = await createServer({
    server: {
      port: 3000,
      host: '0.0.0.0'
    }
  });
  await server.listen();
  console.log('Vite server running on http://localhost:3000/');
  
  // Continuous heartbeat to keep process alive indefinitely
  setInterval(() => {}, 1000);
}

start().catch((err) => {
  console.error('Failed to start Vite server:', err);
  process.exit(1);
});
