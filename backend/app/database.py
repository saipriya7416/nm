import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection URL - defaults to local SQLite database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./restaurant.db")

# For SQLite, check_same_thread needs to be False
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """FastAPI Dependency for database session management."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initializes tables and seeds baseline restaurant data if the database is empty."""
    from app.models import MenuCategory, MenuItem, RestaurantTable, User, Booking, Order, OrderItem
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Seed categories if none exist
        if db.query(MenuCategory).count() == 0:
            categories_data = [
                {"id": 1, "name": "Breakfast", "description": "Fresh and energizing morning favorites"},
                {"id": 2, "name": "Lunch", "description": "Hearty gourmet midday meals and bowls"},
                {"id": 3, "name": "Dinner", "description": "Chef-curated evening entrees and specialties"},
                {"id": 4, "name": "Snacks", "description": "Quick bites, finger foods, and appetizers"},
                {"id": 5, "name": "Beverages", "description": "Craft smoothies, artisan coffees, and refreshing drinks"},
                {"id": 6, "name": "Desserts", "description": "Decadent cakes, pastries, and sweet delights"}
            ]
            for cat in categories_data:
                db.add(MenuCategory(**cat))
            db.commit()

        # Seed menu items if none exist
        if db.query(MenuItem).count() == 0:
            menu_items_data = [
                # Breakfast
                {
                    "name": "Classic Fluffy Pancakes",
                    "category_id": 1,
                    "description": "Stack of golden fluffy buttermilk pancakes served with pure maple syrup, fresh berries, and whipped butter.",
                    "price": 150.00,
                    "is_vegetarian": True,
                    "image": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=500&auto=format&fit=crop&q=60",
                    "availability": True,
                    "ingredients": "Organic Flour, Farm Fresh Milk, Free-Range Eggs, Cane Sugar, Butter",
                    "allergy_info": "Contains Dairy, Gluten, Eggs",
                    "preparation_time": 15,
                    "rating": 4.8
                },
                {
                    "name": "Avocado & Poached Egg Sourdough",
                    "category_id": 1,
                    "description": "Toasted artisan sourdough topped with smashed Haas avocado, poached organic eggs, cherry tomatoes, and microgreens.",
                    "price": 220.00,
                    "is_vegetarian": True,
                    "image": "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=500&auto=format&fit=crop&q=60",
                    "availability": True,
                    "ingredients": "Sourdough Bread, Fresh Avocado, Poached Eggs, Cherry Tomatoes, Chili Flakes",
                    "allergy_info": "Contains Gluten, Eggs",
                    "preparation_time": 12,
                    "rating": 4.9
                },
                # Lunch
                {
                    "name": "Crispy Caesar Salad",
                    "category_id": 2,
                    "description": "Crisp romaine lettuce tossed in house Caesar dressing, garlic herb croutons, and aged Parmesan flakes.",
                    "price": 200.00,
                    "is_vegetarian": True,
                    "image": "https://images.unsplash.com/photo-1546793665-c74683f339c1?w=500&auto=format&fit=crop&q=60",
                    "availability": True,
                    "ingredients": "Romaine Lettuce, Garlic Herb Croutons, Parmesan Cheese, House Caesar Dressing",
                    "allergy_info": "Contains Dairy, Gluten",
                    "preparation_time": 10,
                    "rating": 4.5
                },
                {
                    "name": "Truffle Mushroom Risotto",
                    "category_id": 2,
                    "description": "Creamy Arborio rice with sautéed wild forest mushrooms, black truffle oil, and shaved Pecorino cheese.",
                    "price": 380.00,
                    "is_vegetarian": True,
                    "image": "https://images.unsplash.com/photo-1633964913295-ceb43826e7c9?w=500&auto=format&fit=crop&q=60",
                    "availability": True,
                    "ingredients": "Arborio Rice, Wild Mushrooms, Truffle Oil, Pecorino Cheese, White Wine",
                    "allergy_info": "Contains Dairy",
                    "preparation_time": 22,
                    "rating": 4.9
                },
                # Dinner
                {
                    "name": "Royal Chicken Biryani",
                    "category_id": 3,
                    "description": "Fragrant basmati rice slow-cooked with tender marinated chicken pieces, saffron, whole aromatic spices, and caramelized onions.",
                    "price": 450.00,
                    "is_vegetarian": False,
                    "image": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=500&auto=format&fit=crop&q=60",
                    "availability": True,
                    "ingredients": "Basmati Rice, Marinated Chicken, Saffron, Ghee, Mint, Cashews, Spices",
                    "allergy_info": "Contains Tree Nuts, Dairy",
                    "preparation_time": 25,
                    "rating": 4.9
                },
                {
                    "name": "Grilled Herb Salmon",
                    "category_id": 3,
                    "description": "Pan-seared Atlantic salmon fillet glazed with lemon herb butter, served with roasted asparagus and garlic mash.",
                    "price": 580.00,
                    "is_vegetarian": False,
                    "image": "https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=500&auto=format&fit=crop&q=60",
                    "availability": True,
                    "ingredients": "Atlantic Salmon, Lemon, Butter, Fresh Rosemary, Garlic, Asparagus",
                    "allergy_info": "Contains Fish, Dairy",
                    "preparation_time": 20,
                    "rating": 4.8
                },
                {
                    "name": "Paneer Butter Masala & Naan",
                    "category_id": 3,
                    "description": "Soft cottage cheese cubes simmered in a rich tomato, butter, and cashew gravy, served with fresh garlic naan.",
                    "price": 320.00,
                    "is_vegetarian": True,
                    "image": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=500&auto=format&fit=crop&q=60",
                    "availability": True,
                    "ingredients": "Paneer, Tomatoes, Fresh Cream, Butter, Cashew Paste, Spices, Garlic Naan",
                    "allergy_info": "Contains Dairy, Nuts, Gluten",
                    "preparation_time": 18,
                    "rating": 4.7
                },
                # Snacks
                {
                    "name": "Crispy Golden Truffle Fries",
                    "category_id": 4,
                    "description": "Hand-cut potatoes fried to perfection, tossed in white truffle oil, rosemary sea salt, and served with roasted garlic aioli.",
                    "price": 160.00,
                    "is_vegetarian": True,
                    "image": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=500&auto=format&fit=crop&q=60",
                    "availability": True,
                    "ingredients": "Idaho Potatoes, Truffle Oil, Rosemary, Garlic Aioli",
                    "allergy_info": "None (Aioli has eggs)",
                    "preparation_time": 10,
                    "rating": 4.6
                },
                {
                    "name": "Artisan Margherita Flatbread",
                    "category_id": 4,
                    "description": "Stone-baked crispy flatbread topped with San Marzano tomato sauce, fresh buffalo mozzarella, and fragrant basil leaves.",
                    "price": 240.00,
                    "is_vegetarian": True,
                    "image": "https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=500&auto=format&fit=crop&q=60",
                    "availability": True,
                    "ingredients": "Stoneground Dough, San Marzano Tomatoes, Buffalo Mozzarella, Fresh Basil, EVOO",
                    "allergy_info": "Contains Gluten, Dairy",
                    "preparation_time": 15,
                    "rating": 4.8
                },
                # Beverages
                {
                    "name": "Fresh Alphonso Mango Lassi",
                    "category_id": 5,
                    "description": "Velvety traditional yogurt smoothie blended with ripe Alphonso mangoes, cardamom, and pistachio slivers.",
                    "price": 120.00,
                    "is_vegetarian": True,
                    "image": "https://images.unsplash.com/photo-1546173159-315724a31696?w=500&auto=format&fit=crop&q=60",
                    "availability": True,
                    "ingredients": "Greek Yogurt, Alphonso Mango Pulp, Green Cardamom, Crushed Pistachio",
                    "allergy_info": "Contains Dairy, Tree Nuts",
                    "preparation_time": 5,
                    "rating": 4.9
                },
                {
                    "name": "Iced Vanilla Caramel Latte",
                    "category_id": 5,
                    "description": "Double espresso shot with creamy oat milk, Madagascar vanilla bean syrup, and a buttery caramel drizzle.",
                    "price": 140.00,
                    "is_vegetarian": True,
                    "image": "https://images.unsplash.com/photo-1517256064527-09c73fc73e38?w=500&auto=format&fit=crop&q=60",
                    "availability": True,
                    "ingredients": "Arabica Espresso, Oat Milk, Vanilla Bean, Caramel Drizzle",
                    "allergy_info": "Oat-based (Gluten-free option)",
                    "preparation_time": 5,
                    "rating": 4.7
                },
                # Desserts
                {
                    "name": "Molten Chocolate Lava Cake",
                    "category_id": 6,
                    "description": "Warm Belgian dark chocolate cake with a luscious gooey center, served with Madagascar vanilla bean gelato.",
                    "price": 260.00,
                    "is_vegetarian": True,
                    "image": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=500&auto=format&fit=crop&q=60",
                    "availability": True,
                    "ingredients": "Belgian Dark Chocolate, Butter, Farm Eggs, Sugar, Vanilla Gelato",
                    "allergy_info": "Contains Dairy, Gluten, Eggs",
                    "preparation_time": 15,
                    "rating": 5.0
                },
                {
                    "name": "Classic New York Berry Cheesecake",
                    "category_id": 6,
                    "description": "Velvety smooth cream cheese filling over a buttery graham cracker crust, topped with wild strawberry reduction.",
                    "price": 280.00,
                    "is_vegetarian": True,
                    "image": "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?w=500&auto=format&fit=crop&q=60",
                    "availability": True,
                    "ingredients": "Cream Cheese, Graham Crackers, Wild Strawberries, Fresh Cream",
                    "allergy_info": "Contains Dairy, Gluten",
                    "preparation_time": 5,
                    "rating": 4.8
                }
            ]
            for item in menu_items_data:
                db.add(MenuItem(**item))
            db.commit()

        # Seed restaurant tables if none exist
        if db.query(RestaurantTable).count() == 0:
            tables_data = [
                {"capacity": 2, "location": "Window View", "status": "Available"},
                {"capacity": 2, "location": "Cozy Corner", "status": "Available"},
                {"capacity": 4, "location": "Main Dining Hall", "status": "Available"},
                {"capacity": 4, "location": "Window View", "status": "Available"},
                {"capacity": 4, "location": "Garden Patio", "status": "Available"},
                {"capacity": 6, "location": "Skyline Balcony", "status": "Available"},
                {"capacity": 6, "location": "Main Dining Hall", "status": "Available"},
                {"capacity": 8, "location": "Private VIP Lounge", "status": "Available"},
                {"capacity": 4, "location": "Open Terrace", "status": "Available"},
                {"capacity": 2, "location": "Garden Patio", "status": "Available"}
            ]
            for tbl in tables_data:
                db.add(RestaurantTable(**tbl))
            db.commit()

        # Seed default user if none exists
        if db.query(User).count() == 0:
            demo_user = User(
                name="Alex Morgan",
                email="alex@example.com",
                phone="+1 555-0199",
                hashed_password="demo_secure_password"
            )
            db.add(demo_user)
            db.commit()

    finally:
        db.close()
