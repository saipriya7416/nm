# 🍽️ Gourmet Haven — Restaurant AI Assistant

An intelligent, full-stack AI-powered restaurant application featuring conversational natural language ordering, multi-turn table reservations, menu recommendations, voice recognition, live order tracking, and interactive rich widgets.

---

## ✨ Features

- 🤖 **User-Friendly AI Concierge & Chatbot**:
  - **Conversational Booking**: Multi-turn slot filling for guests, date, time, and table preferences (Window, Balcony, Patio, VIP).
  - **Natural Ordering**: Order dishes by name and quantity (e.g. *"Order 2 Truffle Fries and 1 Mango Lassi"*).
  - **Dietary & Dish Queries**: Ask for vegetarian/vegan options, ingredient details, and allergen warnings.
  - **Live Status Tracking**: Check live progress of food orders and table reservation passes.
  - **Rich Interactive Widgets**: Dish cards with direct "+ Add to Cart", gold reservation passes, and itemized receipts rendered inside chat bubbles.
  - **Voice Input & Audio**: Built-in Speech-to-Text (Microphone) and Text-to-Speech (Audio playback).
  - **Quick Action Chips**: One-click prompt suggestions for zero-friction user experience.

- 📜 **Interactive Menu**:
  - Filter by category (Breakfast, Lunch, Dinner, Snacks, Beverages, Desserts).
  - Real-time search by dish name and ingredients.
  - Vegetarian filter toggle with allergen and prep time badges.
  - Detailed dish modal with nutrition and AI pairing recommendations.

- 🪑 **Table Reservations**:
  - Visual layout map displaying live table availability across dining zones.
  - Instant booking pass generation with reference codes.

- 🛍️ **Cart & Order Checkout**:
  - Slideout cart drawer with live subtotal, tax calculation, and dining modes (Dine-in, Takeaway, Delivery).

- 📦 **Live Order Tracking**:
  - Visual 4-step progress timeline: *Order Placed ➔ Preparing ➔ Ready ➔ Served*.

---

## 🛠️ Tech Stack

- **Frontend**: React 17, Vite 8, Lucide Icons, Modern CSS3 with Design Tokens
- **Backend**: Python 3.12, FastAPI, Uvicorn, Pydantic v2
- **Database & ORM**: SQLite / PostgreSQL, SQLAlchemy with auto-seeding
- **NLP & Chatbot**: Multi-Turn Slot Filling, Semantic Intent Engine, Web Speech API

---

## 🚀 Quick Start Guide

### 1. Start the Backend API

```powershell
cd backend
python -m uvicorn app.main:app --reload --port 8000
```
> The API will be available at `http://localhost:8000` (API Docs at `http://localhost:8000/docs`). Database tables and gourmet seed data are initialized automatically on startup!

### 2. Start the Frontend Development Server

```powershell
cd frontend
npm run dev
```
> Open your browser at `http://localhost:3000`.

---

## 💬 Sample Prompts to Try with the AI Chatbot

1. **Menu Recommendations**:
   - *"What vegetarian dishes do you recommend?"*
   - *"Show me your best desserts"*
   - *"Tell me about the Royal Chicken Biryani"*

2. **Table Reservations**:
   - *"Book a table for 4 tomorrow at 7:30 PM under John Doe near window"*
   - *"Reserve a table for 2 tonight"* (The bot will guide you step by step)

3. **Ordering Food**:
   - *"I want to order 2 Classic Fluffy Pancakes and 1 Mango Lassi"*
   - *"Order 1 Truffle Fries"*

4. **Tracking Status**:
   - *"Where is my order #1?"*
   - *"Check booking #1"*

5. **Restaurant Information**:
   - *"What are your opening hours and address?"*
   - *"Do you offer valet parking?"*