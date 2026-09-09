import React, { useState } from 'react';
import { ArrowRight, Sparkles, User, UtensilsCrossed } from 'lucide-react';
import { useCart } from '../context/CartContext';

export default function NameEntryModal() {
  const { isNameModalOpen, saveUserName, userName } = useCart();
  const [inputName, setInputName] = useState(userName || '');

  if (!isNameModalOpen) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputName.trim()) {
      saveUserName(inputName.trim());
    }
  };

  return (
    <div className="name-modal-backdrop">
      <div className="name-modal-card">
        <div className="name-modal-badge">
          <UtensilsCrossed size={18} color="#ea580c" />
          <span>Gourmet Haven</span>
        </div>

        <h2 className="name-modal-title">
          👋 Welcome! Before we begin, what should I call you?
        </h2>

        <p className="name-modal-sub">
          Your personal AI companion will remember your name throughout table bookings, orders, and friendly chats.
        </p>

        <form onSubmit={handleSubmit} className="name-modal-form">
          <div className="name-input-container">
            <User size={18} className="name-input-icon" />
            <input
              type="text"
              autoFocus
              required
              placeholder="Enter your name"
              value={inputName}
              onChange={(e) => setInputName(e.target.value)}
              className="name-input-field"
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary name-submit-btn"
            disabled={!inputName.trim()}
          >
            <span>Continue</span>
            <ArrowRight size={18} />
          </button>
        </form>
      </div>
    </div>
  );
}
