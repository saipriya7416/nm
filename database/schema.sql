CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE menu_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT
);

CREATE TABLE menu_items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category_id INT REFERENCES menu_categories(id),
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    is_vegetarian BOOLEAN NOT NULL,
    image VARCHAR(255),
    availability BOOLEAN DEFAULT TRUE,
    ingredients TEXT,
    allergy_info TEXT,
    preparation_time INT,
    rating DECIMAL(3, 2)
);

CREATE TABLE restaurant_tables (
    id SERIAL PRIMARY KEY,
    capacity INT NOT NULL,
    location VARCHAR(100),
    status VARCHAR(20) CHECK (status IN ('Available', 'Reserved', 'Occupied', 'Cleaning', 'Maintenance'))
);

CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    table_id INT REFERENCES restaurant_tables(id),
    booking_date DATE NOT NULL,
    booking_time TIME NOT NULL,
    number_of_people INT NOT NULL,
    status VARCHAR(20) CHECK (status IN ('Pending', 'Confirmed', 'Cancelled', 'Completed', 'No-show')),
    special_requests TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    booking_id INT REFERENCES bookings(id),
    order_status VARCHAR(20) CHECK (order_status IN ('Order Placed', 'Confirmed', 'Preparing', 'Ready', 'Served', 'Completed', 'Cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(id),
    menu_item_id INT REFERENCES menu_items(id),
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(id),
    amount DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(20) CHECK (payment_method IN ('Cash', 'Card', 'UPI')),
    payment_status VARCHAR(20) CHECK (payment_status IN ('Pending', 'Paid', 'Failed', 'Refunded')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE food_preferences (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    preference TEXT
);

CREATE TABLE special_requests (
    id SERIAL PRIMARY KEY,
    booking_id INT REFERENCES bookings(id),
    request TEXT
);

CREATE TABLE restaurant_settings (
    id SERIAL PRIMARY KEY,
    setting_name VARCHAR(100) NOT NULL,
    setting_value VARCHAR(255) NOT NULL
);