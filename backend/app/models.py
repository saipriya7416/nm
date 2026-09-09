from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    hashed_password = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    bookings = relationship("Booking", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")

class MenuCategory(Base):
    __tablename__ = 'menu_categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)

    items = relationship("MenuItem", back_populates="category")

class MenuItem(Base):
    __tablename__ = 'menu_items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    category_id = Column(Integer, ForeignKey('menu_categories.id'), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    is_vegetarian = Column(Boolean, default=True)
    image = Column(String(500), nullable=True)
    availability = Column(Boolean, default=True)
    ingredients = Column(Text, nullable=True)
    allergy_info = Column(Text, nullable=True)
    preparation_time = Column(Integer, default=15)
    rating = Column(Float, default=4.5)

    category = relationship("MenuCategory", back_populates="items")
    order_items = relationship("OrderItem", back_populates="menu_item")

class RestaurantTable(Base):
    __tablename__ = 'restaurant_tables'

    id = Column(Integer, primary_key=True, index=True)
    capacity = Column(Integer, nullable=False)
    location = Column(String(100), default="Main Dining Hall")
    status = Column(String(20), default="Available") # Available, Reserved, Occupied

    bookings = relationship("Booking", back_populates="table")

class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    table_id = Column(Integer, ForeignKey('restaurant_tables.id'), nullable=True)
    customer_name = Column(String(100), nullable=False)
    customer_phone = Column(String(20), nullable=True)
    customer_email = Column(String(100), nullable=True)
    date = Column(String(20), nullable=False)
    time = Column(String(20), nullable=False)
    number_of_people = Column(Integer, nullable=False)
    table_preference = Column(String(100), nullable=True)
    special_requests = Column(Text, nullable=True)
    status = Column(String(20), default="Confirmed") # Pending, Confirmed, Cancelled, Completed
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="bookings")
    table = relationship("RestaurantTable", back_populates="bookings")

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    customer_name = Column(String(100), default="Guest")
    customer_phone = Column(String(20), nullable=True)
    order_type = Column(String(20), default="Dine-in") # Dine-in, Takeaway, Delivery
    table_number = Column(Integer, nullable=True)
    total_amount = Column(Float, default=0.0)
    status = Column(String(20), default="Order Placed") # Order Placed, Preparing, Ready, Served, Completed, Cancelled
    payment_method = Column(String(20), default="Card") # Card, Cash, UPI
    payment_status = Column(String(20), default="Pending") # Pending, Paid
    special_instructions = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    menu_item_id = Column(Integer, ForeignKey('menu_items.id'), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem", back_populates="order_items")

class ChatHistory(Base):
    __tablename__ = 'chat_histories'

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), index=True, nullable=False)
    sender = Column(String(20), nullable=False) # 'user' or 'bot'
    message = Column(Text, nullable=False)
    structured_data = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
