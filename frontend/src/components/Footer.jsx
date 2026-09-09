import React from 'react';
import { Link } from 'react-router-dom';
import { UtensilsCrossed, MapPin, Phone, Mail, Clock, Sparkles } from 'lucide-react';
import { useCart } from '../context/CartContext';

export default function Footer() {
  const { openChatWithPrompt } = useCart();

  return (
    <footer className="site-footer">
      <div className="container footer-container">
        <div className="footer-col brand-col">
          <div className="footer-brand">
            <div className="brand-icon">
              <UtensilsCrossed size={20} />
            </div>
            <span className="brand-title">Gourmet Haven</span>
          </div>
          <p className="footer-desc">
            An artisan dining sanctuary crafting modern continental flavors with cutting-edge AI hospitality.
          </p>
          <div className="footer-ai-badge" onClick={() => openChatWithPrompt('Hello!')}>
            <Sparkles size={14} color="#f59e0b" />
            <span>24/7 Conversational AI Concierge Enabled</span>
          </div>
        </div>

        <div className="footer-col">
          <h4>Explore</h4>
          <ul className="footer-links">
            <li><Link to="/menu">Artisan Menu</Link></li>
            <li><Link to="/booking">Table Reservations</Link></li>
            <li><Link to="/tracking">Live Order Tracking</Link></li>
            <li><a href="#about" onClick={(e) => { e.preventDefault(); openChatWithPrompt('Tell me about Gourmet Haven'); }}>About Story</a></li>
          </ul>
        </div>

        <div className="footer-col">
          <h4>Hours & Dining</h4>
          <ul className="footer-info-list">
            <li><Clock size={15} /> Mon - Thu: 10:00 AM - 10:30 PM</li>
            <li><Clock size={15} /> Fri - Sat: 10:00 AM - 11:30 PM</li>
            <li><Clock size={15} /> Sunday: 09:30 AM - 10:00 PM</li>
          </ul>
        </div>

        <div className="footer-col">
          <h4>Contact & Location</h4>
          <ul className="footer-info-list">
            <li><MapPin size={15} /> 452 Grand Blvd, Downtown Arts District</li>
            <li><Phone size={15} /> +1 (555) 342-8700</li>
            <li><Mail size={15} /> concierge@gourmethaven.com</li>
          </ul>
        </div>
      </div>

      <div className="footer-bottom">
        <div className="container footer-bottom-inner">
          <p>© {new Date().getFullYear()} Gourmet Haven. Crafted with AI Pairing & Precision.</p>
        </div>
      </div>
    </footer>
  );
}
