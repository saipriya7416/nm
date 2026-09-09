INSERT INTO menu_categories (name) VALUES 
('Breakfast'),
('Lunch'),
('Snacks'),
('Dinner'),
('Beverages'),
('Desserts');

INSERT INTO menu_items (name, category, description, price, vegetarian, image, availability, ingredients, allergy_info, preparation_time, rating) VALUES 
('Pancakes', 'Breakfast', 'Fluffy pancakes served with syrup.', 150, TRUE, 'pancakes.jpg', TRUE, 'Flour, Milk, Eggs, Sugar', 'Contains gluten', 15, 4.5),
('Caesar Salad', 'Lunch', 'Crispy romaine lettuce with Caesar dressing.', 200, TRUE, 'caesar_salad.jpg', TRUE, 'Romaine Lettuce, Croutons, Caesar Dressing', 'Contains dairy', 10, 4.0),
('Chicken Biryani', 'Dinner', 'Spicy chicken biryani with fragrant rice.', 500, FALSE, 'chicken_biryani.jpg', TRUE, 'Chicken, Rice, Spices', 'Contains nuts', 30, 4.8),
('Chocolate Cake', 'Desserts', 'Rich chocolate cake with frosting.', 250, TRUE, 'chocolate_cake.jpg', TRUE, 'Flour, Cocoa, Sugar, Eggs', 'Contains gluten', 20, 4.7),
('Mango Lassi', 'Beverages', 'Refreshing yogurt drink with mango.', 100, TRUE, 'mango_lassi.jpg', TRUE, 'Yogurt, Mango, Sugar', 'Contains dairy', 5, 4.6),
('French Fries', 'Snacks', 'Crispy golden fries served with ketchup.', 100, TRUE, 'french_fries.jpg', TRUE, 'Potatoes, Oil, Salt', 'None', 10, 4.5);

INSERT INTO restaurant_tables (capacity, location, status) VALUES 
(2, 'Near window', 'Available'),
(4, 'Center', 'Available'),
(6, 'Balcony', 'Available'),
(4, 'Near entrance', 'Reserved'),
(2, 'Corner', 'Occupied'),
(4, 'Patio', 'Available'),
(6, 'Main Hall', 'Cleaning'),
(2, 'Near kitchen', 'Maintenance'),
(4, 'VIP Room', 'Available'),
(6, 'Outdoor', 'Available');

INSERT INTO users (name, email, phone, password) VALUES 
('John Doe', 'john@example.com', '1234567890', 'hashed_password_1'),
('Jane Smith', 'jane@example.com', '0987654321', 'hashed_password_2');

INSERT INTO bookings (user_id, table_id, date, time, number_of_people, status) VALUES 
(1, 1, '2023-10-15', '19:00', 2, 'Confirmed'),
(2, 2, '2023-10-16', '20:00', 4, 'Pending');

INSERT INTO orders (user_id, booking_id, status) VALUES 
(1, 1, 'Order Placed'),
(2, 2, 'Preparing');