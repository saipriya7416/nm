# Frontend Restaurant AI Assistant

This document provides an overview of the frontend part of the Restaurant AI Assistant project, including setup instructions and usage guidelines.

## Project Structure

The frontend project is organized as follows:

```
frontend/
├── src/
│   ├── components/   # Reusable React components
│   ├── pages/        # Main pages of the application
│   ├── services/     # API communication services
│   ├── hooks/        # Custom React hooks
│   └── styles/       # CSS styles for the application
├── package.json      # Project metadata and dependencies
└── README.md         # This documentation file
```

## Setup Instructions

1. **Clone the Repository**
   ```
   git clone <repository-url>
   cd restaurant-ai-assistant/frontend
   ```

2. **Install Dependencies**
   Ensure you have Node.js installed. Then run:
   ```
   npm install
   ```

3. **Run the Application**
   To start the development server, use:
   ```
   npm start
   ```
   The application will be available at `http://localhost:3000`.

## Usage Guidelines

- **Components**: Reusable components can be found in the `src/components` directory. These include buttons, forms, and chat interfaces that can be used throughout the application.

- **Pages**: The main pages of the application are located in `src/pages`. This includes the home page, login page, registration page, menu page, booking page, and admin dashboard.

- **Services**: API communication is handled in the `src/services` directory. This includes functions for fetching menu items, managing bookings, and handling user authentication.

- **Hooks**: Custom React hooks for managing state and side effects are located in `src/hooks`. These hooks can be used to handle user authentication and manage interactions with the chatbot.

- **Styles**: CSS files for styling the application are found in `src/styles`. These styles ensure a modern and responsive design.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.