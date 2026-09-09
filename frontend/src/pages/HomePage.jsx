import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Sparkles,
  Utensils,
  Calendar,
  Compass,
  ArrowRight,
  Star,
  Clock,
  ShieldCheck,
  Award,
  Mic,
  Leaf,
  Plus
} from 'lucide-react';
import { useCart } from '../context/CartContext';
import api from '../services/api';

export default function HomePage() {
  const { openChatWithPrompt, addToCart } = useCart();
  const [featuredItems, setFeaturedItems] = useState([]);

  useEffect(() => {
    // Load top rated menu items
    api.getMenuItems().then((items) => {
      setFeaturedItems(items.slice(0, 4));
    }).catch(console.error);
  }, []);

  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-overlay" />
        <div className="container hero-container">
          <div className="hero-content">
            <div className="hero-badge">
              <Sparkles size={16} color="#f59e0b" />
              <span>Next-Gen Dining with AI Concierge</span>
            </div>
            <h1 className="hero-title">
              Artisan Flavors Meets <br />
              <span className="text-gradient">Intelligent Hospitality</span>
            </h1>
            <p className="hero-subtitle">
              Welcome to Gourmet Haven. Experience gourmet culinary creations paired with our instant conversational AI assistant for seamless table bookings, dietary recommendations, and rapid ordering.
            </p>
            <div className="hero-cta-group">
              <button
                className="btn btn-primary hero-btn"
                onClick={() => openChatWithPrompt('Hello!')}
              >
                <Sparkles size={18} />
                <span>Chat with AI Concierge</span>
              </button>
              <Link to="/booking" className="btn btn-secondary hero-btn">
                <Calendar size={18} />
                <span>Reserve a Table</span>
              </Link>
              <Link to="/menu" className="btn btn-secondary hero-btn">
                <Utensils size={18} />
                <span>Explore Menu</span>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Chef's Signature Highlights */}
      <section className="featured-section">
        <div className="container">
          <div className="section-header-row">
            <div>
              <span className="section-tag">Gourmet Selection</span>
              <h2 className="section-title">Chef's Signature Dishes</h2>
            </div>
            <Link to="/menu" className="btn btn-secondary view-all-btn">
              <span>View All Menu</span>
              <ArrowRight size={16} />
            </Link>
          </div>

          <div className="dish-grid">
            {featuredItems.map((dish) => (
              <div key={dish.id} className="dish-card">
                <div className="dish-image-wrapper">
                  <img src={dish.image} alt={dish.name} className="dish-img" loading="lazy" />
                  <span className={dish.is_vegetarian ? 'badge badge-veg dish-veg-badge' : 'badge badge-nonveg dish-veg-badge'}>
                    {dish.is_vegetarian ? '🌱 Veg' : '🍗 Non-Veg'}
                  </span>
                  <span className="badge badge-gold dish-rating-badge">
                    <Star size={12} fill="#fbbf24" color="#fbbf24" /> {dish.rating}
                  </span>
                </div>
                <div className="dish-body">
                  <h3 className="dish-title">{dish.name}</h3>
                  <p className="dish-desc">{dish.description}</p>
                  <div className="dish-footer">
                    <div className="dish-price-area">
                      <span className="dish-price-label">Price</span>
                      <span className="dish-price-val">${dish.price.toFixed(2)}</span>
                    </div>
                    <div className="dish-action-group">
                      <button
                        className="dish-ask-ai-btn"
                        onClick={() => openChatWithPrompt(`Tell me more about ${dish.name} and its ingredients`)}
                        title="Ask AI about this dish"
                      >
                        <Sparkles size={14} />
                      </button>
                      <button
                        className="btn btn-primary dish-add-btn"
                        onClick={() => addToCart(dish, 1)}
                      >
                        <Plus size={16} />
                        <span>Add</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* AI Features Grid */}
      <section className="features-section">
        <div className="container">
          <div className="features-intro">
            <span className="section-tag">Smart Hospitality</span>
            <h2>Why Dine with Gourmet Haven?</h2>
            <p>We blend culinary art with modern artificial intelligence to deliver effortless service from reservation to dessert.</p>
          </div>

          <div className="features-grid">
            <div className="feature-box">
              <div className="feature-icon-box">
                <Sparkles size={24} color="#ea580c" />
              </div>
              <h3>Intelligent AI Concierge</h3>
              <p>Ask for dietary accommodations, ingredient transparency, wine pairings, or chef recommendations 24/7 in plain English.</p>
            </div>

            <div className="feature-box">
              <div className="feature-icon-box">
                <Mic size={24} color="#ea580c" />
              </div>
              <h3>Hands-Free Voice Ordering</h3>
              <p>Speak naturally using our built-in speech recognition to book tables and add items to your cart on the go.</p>
            </div>

            <div className="feature-box">
              <div className="feature-icon-box">
                <Calendar size={24} color="#ea580c" />
              </div>
              <h3>Instant Table Confirmation</h3>
              <p>Select your favorite ambiance (Window View, Skyline Balcony, Garden Patio) with live availability and zero wait time.</p>
            </div>

            <div className="feature-box">
              <div className="feature-icon-box">
                <Compass size={24} color="#ea580c" />
              </div>
              <h3>Live Kitchen Status</h3>
              <p>Track your food progress in real time from prep to table service with step-by-step transparency.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Reservation CTA Banner */}
      <section className="booking-cta-section">
        <div className="container">
          <div className="booking-cta-banner">
            <div className="booking-cta-content">
              <h2>Reserve Your Exclusive Table Tonight</h2>
              <p>Celebrate birthdays, anniversaries, or an intimate dinner with personalized service and custom chef menus.</p>
              <div className="booking-cta-btns">
                <Link to="/booking" className="btn btn-primary">
                  <span>Book a Table Online</span>
                  <ArrowRight size={18} />
                </Link>
                <button
                  className="btn btn-secondary"
                  onClick={() => openChatWithPrompt('I want to book a table for 4 guests tomorrow at 7:30 PM')}
                >
                  <Sparkles size={16} color="#f59e0b" />
                  <span>Ask AI to Book</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
