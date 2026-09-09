import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { ShoppingBag, Sparkles, Calendar, UtensilsCrossed, Compass, User, Edit3 } from 'lucide-react';
import { useCart } from '../context/CartContext';

export default function Navbar() {
  const { cartCount, setIsCartOpen, setIsChatOpen, userName, setIsNameModalOpen } = useCart();
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <header className="navbar-header">
      <div className="container navbar-container">
        <Link to="/" className="navbar-brand">
          <div className="brand-icon">
            <UtensilsCrossed size={22} />
          </div>
          <div className="brand-text">
            <span className="brand-title">Gourmet Haven</span>
            <span className="brand-sub">AI Culinary Lounge</span>
          </div>
        </Link>

        <nav className="navbar-nav">
          <Link to="/" className={`nav-link ${isActive('/') ? 'active' : ''}`}>
            Home
          </Link>
          <Link to="/menu" className={`nav-link ${isActive('/menu') ? 'active' : ''}`}>
            Menu
          </Link>
          <Link to="/booking" className={`nav-link ${isActive('/booking') ? 'active' : ''}`}>
            Reservations
          </Link>
          <Link to="/tracking" className={`nav-link ${isActive('/tracking') ? 'active' : ''}`}>
            Track Order
          </Link>
        </nav>

        <div className="navbar-actions">
          {/* User Name Chip */}
          {userName && (
            <button
              className="user-profile-chip"
              onClick={() => setIsNameModalOpen(true)}
              title="Click to edit your name"
            >
              <User size={14} color="#fbbf24" />
              <span className="user-name-text">{userName}</span>
            </button>
          )}

          {/* AI Assistant Button */}
          <button
            className="btn btn-secondary nav-chat-btn"
            onClick={() => setIsChatOpen(true)}
            title="Chat with AI Concierge"
          >
            <Sparkles size={16} color="#f59e0b" />
            <span className="nav-chat-btn-text">AI Assistant</span>
          </button>

          {/* Cart Trigger */}
          <button
            className="cart-nav-btn"
            onClick={() => setIsCartOpen(true)}
            aria-label="View Cart"
          >
            <ShoppingBag size={20} />
            {cartCount > 0 && <span className="cart-badge-count">{cartCount}</span>}
          </button>
        </div>
      </div>
    </header>
  );
}

