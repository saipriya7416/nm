from datetime import datetime
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field

# ----------------- Auth & User Schemas -----------------
class UserBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserOut(UserBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut

# ----------------- Menu Schemas -----------------
class MenuCategoryOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

class MenuItemBase(BaseModel):
    name: str
    category_id: int
    description: Optional[str] = None
    price: float
    is_vegetarian: bool = True
    image: Optional[str] = None
    availability: bool = True
    ingredients: Optional[str] = None
    allergy_info: Optional[str] = None
    preparation_time: int = 15
    rating: float = 4.5

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemOut(MenuItemBase):
    id: int
    category_name: Optional[str] = None

    class Config:
        from_attributes = True

# ----------------- Table & Booking Schemas -----------------
class RestaurantTableOut(BaseModel):
    id: int
    capacity: int
    location: str
    status: str

    class Config:
        from_attributes = True

class BookingCreate(BaseModel):
    customer_name: str
    customer_phone: Optional[str] = None
    customer_email: Optional[str] = None
    date: str
    time: str
    number_of_people: int
    table_preference: Optional[str] = "Any"
    special_requests: Optional[str] = None
    user_id: Optional[int] = None

class BookingOut(BaseModel):
    id: int
    customer_name: str
    customer_phone: Optional[str] = None
    customer_email: Optional[str] = None
    date: str
    time: str
    number_of_people: int
    table_preference: Optional[str] = None
    special_requests: Optional[str] = None
    table_id: Optional[int] = None
    status: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ----------------- Order Schemas -----------------
class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int = 1

class OrderItemOut(BaseModel):
    id: int
    menu_item_id: int
    name: Optional[str] = None
    quantity: int
    price: float

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    customer_name: str = "Guest"
    customer_phone: Optional[str] = None
    order_type: str = "Dine-in" # Dine-in, Takeaway, Delivery
    table_number: Optional[int] = None
    payment_method: str = "Card"
    special_instructions: Optional[str] = None
    items: List[OrderItemCreate]
    user_id: Optional[int] = None

class OrderOut(BaseModel):
    id: int
    customer_name: str
    customer_phone: Optional[str] = None
    order_type: str
    table_number: Optional[int] = None
    total_amount: float
    status: str
    payment_method: str
    payment_status: str
    special_instructions: Optional[str] = None
    created_at: Optional[datetime] = None
    items: List[OrderItemOut] = []

    class Config:
        from_attributes = True

# ----------------- Chatbot Schemas -----------------
class QuickReply(BaseModel):
    label: str
    payload: str
    icon: Optional[str] = None

class ChatMessageIn(BaseModel):
    session_id: str
    message: str
    user_id: Optional[int] = None
    user_name: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class ChatMessageOut(BaseModel):
    session_id: str
    message: str
    intent: Optional[str] = "general"
    action_type: Optional[str] = None # e.g. "SHOW_MENU", "BOOKING_CONFIRMATION", "ORDER_CONFIRMATION", "STATUS_LOOKUP"
    quick_replies: List[QuickReply] = []
    structured_data: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None

class ChatSuggestion(BaseModel):
    title: str
    prompt: str
    category: str
    icon: str
