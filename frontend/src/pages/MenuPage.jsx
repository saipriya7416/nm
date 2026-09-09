import React, { useState, useEffect } from 'react';
import {
  Search,
  Filter,
  Sparkles,
  Plus,
  Star,
  Clock,
  AlertCircle,
  Leaf,
  X,
  Check,
} from 'lucide-react';
import { useCart } from '../context/CartContext';
import api from '../services/api';

export default function MenuPage() {
  const { addToCart, openChatWithPrompt } = useCart();
  const [categories, setCategories] = useState([]);
  const [menuItems, setMenuItems] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [vegOnly, setVegOnly] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDish, setSelectedDish] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [cats, items] = await Promise.all([
        api.getMenuCategories(),
        api.getMenuItems(),
      ]);
      setCategories(cats);
      setMenuItems(items);
    } catch (err) {
      console.error('Error loading menu:', err);
    } finally {
      setLoading(false);
    }
  };

  const filteredItems = menuItems.filter((item) => {
    if (selectedCategory && item.category_id !== selectedCategory) return false;
    if (vegOnly && !item.is_vegetarian) return false;
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      return (
        item.name.toLowerCase().includes(q) ||
        item.description?.toLowerCase().includes(q) ||
        item.ingredients?.toLowerCase().includes(q)
      );
    }
    return true;
  });

  return (
    <div className="menu-page">
      {/* Menu Header */}
      <section className="page-hero-banner">
        <div className="container">
          <div className="page-hero-content">
            <span className="section-tag">Artisan Culinary Collection</span>
            <h1>Our Handcrafted Menu</h1>
            <p>
              Fresh, locally sourced organic ingredients prepared by master chefs. Filter by course, dietary preference, or ask our AI concierge for custom pairings.
            </p>
          </div>
        </div>
      </section>

      {/* Filter and Search Bar */}
      <section className="menu-controls-section">
        <div className="container">
          <div className="menu-controls-bar">
            {/* Search Input */}
            <div className="menu-search-box">
              <Search size={18} color="#a8a29e" />
              <input
                type="text"
                placeholder="Search dishes, ingredients (e.g. biryani, truffle, avocado)..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
              {searchQuery && (
                <button onClick={() => setSearchQuery('')} className="clear-search-btn">
                  <X size={15} />
                </button>
              )}
            </div>

            {/* Veg Toggle */}
            <button
              className={`veg-toggle-btn ${vegOnly ? 'active' : ''}`}
              onClick={() => setVegOnly(!vegOnly)}
            >
              <Leaf size={16} color={vegOnly ? '#22c55e' : '#a8a29e'} />
              <span>Vegetarian Only</span>
            </button>

            {/* Ask AI Prompt Button */}
            <button
              className="btn btn-secondary menu-ai-query-btn"
              onClick={() => openChatWithPrompt('What do you recommend from the menu today?')}
            >
              <Sparkles size={16} color="#f59e0b" />
              <span>Ask AI for Recommendations</span>
            </button>
          </div>

          {/* Category Tabs */}
          <div className="category-tabs-container">
            <button
              className={`category-tab ${selectedCategory === null ? 'active' : ''}`}
              onClick={() => setSelectedCategory(null)}
            >
              All Categories
            </button>
            {categories.map((cat) => (
              <button
                key={cat.id}
                className={`category-tab ${selectedCategory === cat.id ? 'active' : ''}`}
                onClick={() => setSelectedCategory(cat.id)}
              >
                {cat.name}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Menu Grid */}
      <section className="menu-items-section">
        <div className="container">
          {loading ? (
            <div className="menu-loading-state">
              <div className="loading-spinner" />
              <p>Loading culinary creations...</p>
            </div>
          ) : filteredItems.length === 0 ? (
            <div className="menu-empty-state">
              <AlertCircle size={40} color="#f59e0b" />
              <h3>No matching dishes found</h3>
              <p>Try searching with another keyword or ask our AI Concierge for recommendations!</p>
              <button
                className="btn btn-primary"
                onClick={() => {
                  setSelectedCategory(null);
                  setVegOnly(false);
                  setSearchQuery('');
                }}
              >
                Reset Filters
              </button>
            </div>
          ) : (
            <div className="dish-grid">
              {filteredItems.map((dish) => (
                <div
                  key={dish.id}
                  className="dish-card"
                  onClick={() => setSelectedDish(dish)}
                >
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
                    <div className="dish-header-row">
                      <h3 className="dish-title">{dish.name}</h3>
                    </div>
                    <p className="dish-desc">{dish.description}</p>
                    
                    <div className="dish-meta-info">
                      <span className="dish-prep-time">
                        <Clock size={13} /> {dish.preparation_time} mins
                      </span>
                      {dish.allergy_info && (
                        <span className="dish-allergy-tag">
                          {dish.allergy_info}
                        </span>
                      )}
                    </div>

                    <div className="dish-footer">
                      <div className="dish-price-area">
                        <span className="dish-price-label">Price</span>
                        <span className="dish-price-val">${dish.price.toFixed(2)}</span>
                      </div>
                      <div className="dish-action-group" onClick={(e) => e.stopPropagation()}>
                        <button
                          className="dish-ask-ai-btn"
                          onClick={() => openChatWithPrompt(`Tell me more about ${dish.name} and recommend pairings`)}
                          title="Ask AI Concierge about this dish"
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
          )}
        </div>
      </section>

      {/* Dish Details Modal */}
      {selectedDish && (
        <div className="modal-backdrop" onClick={() => setSelectedDish(null)}>
          <div className="modal-content dish-detail-modal" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close-btn" onClick={() => setSelectedDish(null)}>
              <X size={20} />
            </button>
            <div className="modal-dish-grid">
              <div className="modal-dish-img-container">
                <img src={selectedDish.image} alt={selectedDish.name} />
              </div>
              <div className="modal-dish-info">
                <div className="modal-dish-header">
                  <span className={selectedDish.is_vegetarian ? 'badge badge-veg' : 'badge badge-nonveg'}>
                    {selectedDish.is_vegetarian ? '🌱 Vegetarian' : '🍗 Non-Vegetarian'}
                  </span>
                  <span className="badge badge-gold">
                    <Star size={12} fill="#fbbf24" color="#fbbf24" /> {selectedDish.rating} / 5.0
                  </span>
                </div>
                <h2>{selectedDish.name}</h2>
                <p className="modal-dish-desc">{selectedDish.description}</p>

                <div className="modal-info-box">
                  <h4>Ingredients</h4>
                  <p>{selectedDish.ingredients || 'Chef proprietary blend'}</p>
                </div>

                <div className="modal-info-box">
                  <h4>Allergen & Prep Details</h4>
                  <p>{selectedDish.allergy_info || 'None declared'} • Prep time ~{selectedDish.preparation_time} minutes</p>
                </div>

                <div className="modal-footer-row">
                  <div>
                    <span className="dish-price-label">Price</span>
                    <span className="modal-dish-price">${selectedDish.price.toFixed(2)}</span>
                  </div>
                  <div className="modal-btn-group">
                    <button
                      className="btn btn-secondary"
                      onClick={() => {
                        setSelectedDish(null);
                        openChatWithPrompt(`Can you recommend what drinks or sides pair with ${selectedDish.name}?`);
                      }}
                    >
                      <Sparkles size={16} color="#f59e0b" />
                      <span>Ask AI Pairings</span>
                    </button>
                    <button
                      className="btn btn-primary"
                      onClick={() => {
                        addToCart(selectedDish, 1);
                        setSelectedDish(null);
                      }}
                    >
                      <Plus size={18} />
                      <span>Add to Cart</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
