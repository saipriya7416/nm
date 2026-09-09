from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .routes import auth, menu, bookings, orders
from .chatbot.router import router as chatbot_router

app = FastAPI(
    title="Gourmet Haven - Restaurant AI Assistant API",
    description="Full-stack AI-powered restaurant backend with natural language chatbot, table booking, food ordering, and real-time tracking.",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    # Initialize database tables and seed baseline data
    init_db()

# Include Feature Routers
app.include_router(chatbot_router, prefix="/chat", tags=["Chatbot AI"])
app.include_router(menu.router, prefix="/menu", tags=["Menu"])
app.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

@app.get("/")
async def root():
    return {
        "status": "online",
        "restaurant": "Gourmet Haven",
        "message": "Welcome to Gourmet Haven AI Assistant API!",
        "docs": "/docs"
    }