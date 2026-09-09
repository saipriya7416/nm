import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import { CartProvider } from './context/CartContext';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import CartDrawer from './components/CartDrawer';
import ChatbotWidget from './components/Chatbot/ChatbotWidget';
import NameEntryModal from './components/NameEntryModal';

import HomePage from './pages/HomePage';
import MenuPage from './pages/MenuPage';
import BookingPage from './pages/BookingPage';
import OrderTrackingPage from './pages/OrderTrackingPage';

import './App.css';

export default function App() {
  return (
    <CartProvider>
      <Router>
        <div className="app-wrapper">
          <Navbar />
          <main className="main-content">
            <Switch>
              <Route exact path="/" component={HomePage} />
              <Route exact path="/menu" component={MenuPage} />
              <Route exact path="/booking" component={BookingPage} />
              <Route exact path="/tracking" component={OrderTrackingPage} />
            </Switch>
          </main>
          <Footer />

          {/* First-time Personalized Name Entry Screen */}
          <NameEntryModal />

          {/* Floating AI Chatbot Widget */}
          <ChatbotWidget />

          {/* Slideout Cart Drawer */}
          <CartDrawer />
        </div>
      </Router>
    </CartProvider>
  );
}
