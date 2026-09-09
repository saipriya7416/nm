# Restaurant AI Assistant Backend

## Overview
This backend application is built using FastAPI and serves as the server-side component for the Restaurant AI Assistant project. It provides RESTful APIs for managing restaurant operations, including user authentication, menu management, table bookings, and order processing.

## Project Structure
- **app/**: Contains the main application logic.
  - **auth/**: User authentication logic (JWT, registration, login).
  - **chatbot/**: Chatbot implementation for handling user interactions.
  - **database/**: Database connection and configuration for PostgreSQL.
  - **models/**: Database models representing the application's data structure.
  - **routes/**: FastAPI route definitions for handling API requests.
  - **schemas/**: Pydantic schemas for request and response validation.
  - **services/**: Business logic for handling bookings and orders.
  - **main.py**: Entry point of the FastAPI application.

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd restaurant-ai-assistant/backend
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Copy the `.env.example` file to `.env` and update the values as needed for your local setup.

5. **Run the Application**
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints
- **Authentication**
  - `POST /register`: Register a new user.
  - `POST /login`: Authenticate a user.

- **Menu Management**
  - `GET /menu`: Retrieve the menu items.
  - `POST /menu`: Add a new menu item.
  - `PUT /menu/{id}`: Update an existing menu item.
  - `DELETE /menu/{id}`: Remove a menu item.

- **Table Management**
  - `GET /tables`: Retrieve all tables.
  - `POST /tables`: Add a new table.
  - `PUT /tables/{id}`: Update table information.

- **Booking Management**
  - `POST /bookings`: Create a new booking.
  - `GET /bookings`: Retrieve all bookings.
  - `GET /bookings/{id}`: Retrieve a specific booking.
  - `PUT /bookings/{id}`: Update a booking.
  - `DELETE /bookings/{id}`: Cancel a booking.

- **Order Management**
  - `POST /orders`: Place a new order.
  - `GET /orders`: Retrieve all orders.
  - `GET /orders/{id}`: Retrieve a specific order.
  - `PUT /orders/{id}`: Update order status.

## Database Setup
Run the SQL commands in `database/schema.sql` to create the necessary tables in your PostgreSQL database. Use `database/seed.sql` to populate the database with initial data.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.